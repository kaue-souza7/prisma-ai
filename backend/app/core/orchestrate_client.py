"""Cliente único para o watsonx Orchestrate.

Centraliza autenticação IAM, chamadas HTTP, retry, timeout e logging.
Os três adaptadores (Mentor, Catalisador, Analista) usam apenas este módulo
— nenhum deles duplica HTTP ou lida com tokens IAM diretamente.

Contrato real confirmado do Orchestrate:
  POST {ORCHESTRATE_URL}/v1/orchestrate/{agent_uuid}/chat/completions
  Authorization: Bearer <token IAM>
  Body: {"stream": false, "messages": [{"role": "user", "content": "<payload JSON>"}]}
  Resposta: choices[0].message.content  (+ thread_id no topo)
"""
from __future__ import annotations

import asyncio
import json
import time
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import logger

# ─────────────────────────────────────────────
# Erros tipados
# ─────────────────────────────────────────────

class OrchestrateError(Exception):
    """Base para todos os erros do cliente Orchestrate."""
    def __init__(self, detail: str, status_code: int | None = None) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class OrchestrateAuthError(OrchestrateError):
    """Falha de autenticação (401)."""


class OrchestrateRateLimitError(OrchestrateError):
    """Rate limit atingido (429)."""


class OrchestrateTimeoutError(OrchestrateError):
    """Timeout na chamada ao Orchestrate."""


class OrchestrateEmptyResponseError(OrchestrateError):
    """Resposta recebida mas sem choices/content utilizável."""


# ─────────────────────────────────────────────
# Cache de token IAM em memória
# ─────────────────────────────────────────────

_IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
# Renova 5 minutos antes de expirar para evitar falhas de borda.
_TOKEN_RENEWAL_MARGIN_SECONDS = 300

_cached_token: str | None = None
_token_expires_at: float = 0.0
_token_lock = asyncio.Lock()


async def _fetch_iam_token(api_key: str) -> tuple[str, float]:
    """Troca a IBM Cloud API key por um token IAM de curta duração.

    Retorna (token, expires_at_timestamp).
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            _IAM_TOKEN_URL,
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": api_key,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        body = response.json()

    token = body["access_token"]
    expires_in = int(body.get("expires_in", 3600))
    expires_at = time.monotonic() + expires_in - _TOKEN_RENEWAL_MARGIN_SECONDS
    return token, expires_at


async def _get_iam_token() -> str:
    """Retorna o token IAM válido, renovando quando necessário."""
    global _cached_token, _token_expires_at

    async with _token_lock:
        if _cached_token and time.monotonic() < _token_expires_at:
            return _cached_token
        token, expires_at = await _fetch_iam_token(settings.orchestrate_api_key)
        _cached_token = token
        _token_expires_at = expires_at
        logger.debug("Token IAM renovado; expira em %.0fs", expires_at - time.monotonic())
        return token


def _invalidate_token() -> None:
    """Força renovação do token na próxima chamada (após 401)."""
    global _cached_token, _token_expires_at
    _cached_token = None
    _token_expires_at = 0.0


# ─────────────────────────────────────────────
# Circuit breaker simples por agente
# ─────────────────────────────────────────────

# Limite de falhas consecutivas antes de abrir o circuit breaker.
_CIRCUIT_FAIL_THRESHOLD = 5
# Tempo em segundos para tentar novamente após o circuito abrir.
_CIRCUIT_RESET_SECONDS = 60.0

# Estado por agent_id: (falhas_consecutivas, timestamp_da_abertura | None)
_circuit_state: dict[str, tuple[int, float | None]] = {}


def _circuit_is_open(agent_id: str) -> bool:
    fails, opened_at = _circuit_state.get(agent_id, (0, None))
    if opened_at is None:
        return False
    if time.monotonic() - opened_at > _CIRCUIT_RESET_SECONDS:
        # Tenta fechar o circuito (half-open)
        _circuit_state[agent_id] = (0, None)
        return False
    return True


def _circuit_record_success(agent_id: str) -> None:
    _circuit_state[agent_id] = (0, None)


def _circuit_record_failure(agent_id: str) -> None:
    fails, _ = _circuit_state.get(agent_id, (0, None))
    fails += 1
    if fails >= _CIRCUIT_FAIL_THRESHOLD:
        _circuit_state[agent_id] = (fails, time.monotonic())
        logger.warning("Circuit breaker aberto para agent_id=%s após %d falhas.", agent_id, fails)
    else:
        _circuit_state[agent_id] = (fails, None)


# ─────────────────────────────────────────────
# Chamada ao Orchestrate
# ─────────────────────────────────────────────

async def chat_completion(
    *,
    agent_id: str,
    payload: dict[str, Any],
    thread_id: str | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    """Envia uma mensagem ao agente e devolve o JSON bruto da resposta.

    Args:
        agent_id:  UUID do agente no Orchestrate (valor de ORCHESTRATE_*_AGENT_ID).
        payload:   Dicionário com o payload pedagógico. Será serializado em JSON
                   e colocado em messages[0].content.
        thread_id: Continua uma conversa existente (multi-turn).
        timeout:   Sobrescreve ORCHESTRATE_TIMEOUT_SECONDS para esta chamada.

    Returns:
        JSON bruto da resposta do Orchestrate
        (contém choices[0].message.content e, opcionalmente, thread_id).

    Raises:
        OrchestrateAuthError       — 401 mesmo após renovação de token.
        OrchestrateRateLimitError  — 429.
        OrchestrateTimeoutError    — timeout.
        OrchestrateEmptyResponseError — resposta sem choices.
        OrchestrateError           — outros erros HTTP (4xx/5xx).
    """
    # Circuit breaker — falha rápida quando o agente está com muitos erros consecutivos.
    if _circuit_is_open(agent_id):
        raise OrchestrateError(f"Circuit breaker aberto para agent_id={agent_id}.")

    base_url = settings.orchestrate_url.rstrip("/")
    url = f"{base_url}/v1/orchestrate/{agent_id}/chat/completions"
    effective_timeout = timeout if timeout is not None else settings.orchestrate_timeout_seconds

    body: dict[str, Any] = {
        "stream": False,
        "messages": [
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    }
    if thread_id:
        body["thread_id"] = thread_id

    t_start = time.monotonic()

    async def _do_request(token: str) -> httpx.Response:
        async with httpx.AsyncClient(timeout=effective_timeout) as client:
            return await client.post(
                url,
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )

    try:
        token = await _get_iam_token()
        response = await _do_request(token)

        # Renovação automática em 401.
        if response.status_code == 401:
            logger.info("Orchestrate retornou 401 — renovando token IAM.")
            _invalidate_token()
            token = await _get_iam_token()
            response = await _do_request(token)

        latency_ms = int((time.monotonic() - t_start) * 1000)
        logger.info(
            "Orchestrate agent=%s status=%d latency_ms=%d",
            agent_id, response.status_code, latency_ms,
        )

        if response.status_code == 401:
            _circuit_record_failure(agent_id)
            raise OrchestrateAuthError("Falha de autenticação após renovação de token.", 401)
        if response.status_code == 429:
            _circuit_record_failure(agent_id)
            raise OrchestrateRateLimitError("Rate limit atingido.", 429)
        if response.status_code >= 500:
            _circuit_record_failure(agent_id)
            raise OrchestrateError(f"Erro no servidor Orchestrate ({response.status_code}).", response.status_code)
        if response.status_code >= 400:
            _circuit_record_failure(agent_id)
            raise OrchestrateError(f"Erro HTTP {response.status_code}.", response.status_code)

        data = response.json()
        _circuit_record_success(agent_id)

    except (httpx.TimeoutException, asyncio.TimeoutError) as exc:
        _circuit_record_failure(agent_id)
        logger.warning("Orchestrate timeout agent=%s: %s", agent_id, exc.__class__.__name__)
        raise OrchestrateTimeoutError("Timeout na chamada ao Orchestrate.") from exc
    except OrchestrateError:
        raise
    except Exception as exc:  # noqa: BLE001
        _circuit_record_failure(agent_id)
        logger.warning("Orchestrate erro inesperado agent=%s: %s", agent_id, exc.__class__.__name__)
        raise OrchestrateError(str(exc)) from exc

    if not isinstance(data.get("choices"), list) or not data["choices"]:
        raise OrchestrateEmptyResponseError("Resposta do Orchestrate não contém choices.")

    return data
