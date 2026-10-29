"""Testes unitários do cliente Orchestrate — sem chamadas de rede reais.

Usa httpx.MockTransport para simular todas as respostas.
"""
from __future__ import annotations

import json
import time

import httpx
import pytest

from app.core import orchestrate_client as oc
from app.core.orchestrate_client import (
    OrchestrateAuthError,
    OrchestrateEmptyResponseError,
    OrchestrateError,
    OrchestrateRateLimitError,
    OrchestrateTimeoutError,
    chat_completion,
)

# Fixture para resetar estado global entre testes
@pytest.fixture(autouse=True)
def reset_client_state():
    """Reseta cache de token e circuit breaker entre testes."""
    oc._cached_token = None
    oc._token_expires_at = 0.0
    oc._circuit_state.clear()
    yield
    oc._cached_token = None
    oc._token_expires_at = 0.0
    oc._circuit_state.clear()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

_FAKE_TOKEN_RESPONSE = json.dumps({
    "access_token": "tok_abc123",
    "expires_in": 3600,
    "token_type": "Bearer",
})

_VALID_CHAT_RESPONSE = json.dumps({
    "thread_id": "thread-xyz",
    "choices": [
        {"message": {"role": "assistant", "content": '{"content": "Olá!"}'}}
    ],
})

_FAKE_REQUEST = httpx.Request("POST", "https://fake.example.com")


def _make_iam_response() -> httpx.Response:
    r = httpx.Response(200, content=_FAKE_TOKEN_RESPONSE.encode(), request=_FAKE_REQUEST)
    return r


def _make_chat_response(status: int = 200, body: str | None = None) -> httpx.Response:
    return httpx.Response(status, content=(body or _VALID_CHAT_RESPONSE).encode(), request=_FAKE_REQUEST)


class _SequentialTransport(httpx.MockTransport):
    """Retorna respostas em sequência para simular múltiplos requests."""

    def __init__(self, responses: list[httpx.Response]) -> None:
        self._responses = iter(responses)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        resp = next(self._responses)
        # Garante que o request está associado à resposta (necessário para raise_for_status)
        if resp.request is None:  # type: ignore[union-attr]
            resp.request = request  # type: ignore[assignment]
        return resp


def _patch_client(monkeypatch, responses: list[httpx.Response]) -> None:
    """Substitui httpx.AsyncClient por um mock com respostas pré-definidas."""
    transport = _SequentialTransport(responses)

    class _FakeAsyncClient:
        def __init__(self, **kwargs):
            self._transport = transport

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, **kwargs) -> httpx.Response:
            req = httpx.Request("POST", url)
            return self._transport.handle_request(req)

    monkeypatch.setattr(httpx, "AsyncClient", _FakeAsyncClient)


def _reset_token_cache():
    oc._cached_token = None
    oc._token_expires_at = 0.0


# ─────────────────────────────────────────────
# Testes de autenticação IAM
# ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_iam_token_is_fetched_and_cached(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    _patch_client(monkeypatch, [
        _make_iam_response(),   # 1ª chamada: token IAM
        _make_chat_response(),  # 2ª chamada: chat
    ])

    result = await chat_completion(agent_id="agent-uuid-123", payload={"msg": "hi"})
    assert result["thread_id"] == "thread-xyz"
    assert oc._cached_token == "tok_abc123"


@pytest.mark.asyncio
async def test_token_is_reused_from_cache(monkeypatch):
    """Segundo call não deve buscar novo token."""
    oc._cached_token = "tok_cached"
    oc._token_expires_at = time.monotonic() + 3000  # ainda válido
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    _patch_client(monkeypatch, [
        # Apenas a resposta do chat — sem IAM
        _make_chat_response(),
    ])

    result = await chat_completion(agent_id="agent-uuid-123", payload={"msg": "hi"})
    assert result["choices"][0]["message"]["content"]
    _reset_token_cache()


@pytest.mark.asyncio
async def test_401_triggers_token_renewal_and_retry(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    _patch_client(monkeypatch, [
        _make_iam_response(),               # token inicial
        _make_chat_response(401, "{}"),     # Orchestrate responde 401
        _make_iam_response(),               # renovação de token
        _make_chat_response(),              # retry bem-sucedido
    ])

    result = await chat_completion(agent_id="agent-uuid-123", payload={"msg": "hi"})
    assert result["thread_id"] == "thread-xyz"


@pytest.mark.asyncio
async def test_persistent_401_raises_auth_error(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    _patch_client(monkeypatch, [
        _make_iam_response(),               # token inicial
        _make_chat_response(401, "{}"),     # 401 original
        _make_iam_response(),               # renovação
        _make_chat_response(401, "{}"),     # 401 novamente
    ])

    with pytest.raises(OrchestrateAuthError):
        await chat_completion(agent_id="agent-uuid-123", payload={"msg": "hi"})


# ─────────────────────────────────────────────
# Testes de URL e corpo
# ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_chat_url_format(monkeypatch):
    """URL deve ser /v1/orchestrate/{uuid}/chat/completions."""
    _reset_token_cache()
    captured_urls: list[str] = []

    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    class _CapturingClient:
        def __init__(self, **kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, **kwargs):
            captured_urls.append(url)
            if "iam.cloud.ibm.com" in url:
                return _make_iam_response()
            return _make_chat_response()

    monkeypatch.setattr(httpx, "AsyncClient", _CapturingClient)

    await chat_completion(agent_id="my-uuid-abc", payload={"x": 1})
    chat_url = next(u for u in captured_urls if "iam" not in u)
    assert chat_url == "https://wxo.example.com/v1/orchestrate/my-uuid-abc/chat/completions"
    _reset_token_cache()


# ─────────────────────────────────────────────
# Testes de erros HTTP
# ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_429_raises_rate_limit_error(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")
    _patch_client(monkeypatch, [_make_iam_response(), _make_chat_response(429, "{}")])
    with pytest.raises(OrchestrateRateLimitError):
        await chat_completion(agent_id="uuid", payload={})


@pytest.mark.asyncio
async def test_500_raises_orchestrate_error(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")
    _patch_client(monkeypatch, [_make_iam_response(), _make_chat_response(500, "{}")])
    with pytest.raises(OrchestrateError) as exc_info:
        await chat_completion(agent_id="uuid", payload={})
    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_empty_choices_raises_empty_response_error(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")
    empty_body = json.dumps({"choices": []})
    _patch_client(monkeypatch, [_make_iam_response(), _make_chat_response(200, empty_body)])
    with pytest.raises(OrchestrateEmptyResponseError):
        await chat_completion(agent_id="uuid", payload={})


@pytest.mark.asyncio
async def test_timeout_raises_timeout_error(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")

    class _TimeoutClient:
        def __init__(self, **kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, **kwargs):
            if "iam.cloud.ibm.com" in url:
                return _make_iam_response()
            raise httpx.TimeoutException("timed out", request=None)

    monkeypatch.setattr(httpx, "AsyncClient", _TimeoutClient)
    with pytest.raises(OrchestrateTimeoutError):
        await chat_completion(agent_id="uuid", payload={})
    _reset_token_cache()


# ─────────────────────────────────────────────
# Testes de thread_id
# ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_thread_id_is_included_when_provided(monkeypatch):
    _reset_token_cache()
    monkeypatch.setattr("app.core.config.settings.orchestrate_api_key", "key123")
    monkeypatch.setattr("app.core.config.settings.orchestrate_url", "https://wxo.example.com")
    captured_bodies: list[dict] = []

    class _BodyCapture:
        def __init__(self, **kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, json=None, **kwargs):
            if json:
                captured_bodies.append(json)
            if "iam.cloud.ibm.com" in url:
                return _make_iam_response()
            return _make_chat_response()

    monkeypatch.setattr(httpx, "AsyncClient", _BodyCapture)
    await chat_completion(agent_id="uuid", payload={"x": 1}, thread_id="thread-99")
    chat_body = next(b for b in captured_bodies if "stream" in b)
    assert chat_body["thread_id"] == "thread-99"
    _reset_token_cache()
