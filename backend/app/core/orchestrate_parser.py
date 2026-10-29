"""Extrator e validador de respostas do watsonx Orchestrate.

Centraliza toda a lógica de parsing — os adaptadores (Mentor, Catalisador,
Analista) não duplicam regex nem lógica de deserialização JSON.

Formatos aceitos pela API real:
  1. {"choices": [{"message": {"content": "<texto ou JSON>"}}], "thread_id": "..."}
  2. Texto puro ou JSON cercado por ```json ... ``` dentro de choices[0].message.content
  3. Compatibilidade legada: campos "content" / "output" / "response" no topo.
"""
from __future__ import annotations

import json
import re
from typing import Any

from app.core.logging import logger

# Padrão para remover cercas de markdown (```json ... ```)
_MD_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)


# ─────────────────────────────────────────────
# Extratores de texto bruto
# ─────────────────────────────────────────────

def _strip_md_fences(text: str) -> str:
    """Remove cercas de markdown e retorna o conteúdo interno."""
    match = _MD_FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text


def _try_extract_json_from_string(text: str) -> dict | None:
    """Tenta desserializar JSON da string.

    Aceita:
    - JSON puro
    - Texto antes/depois do JSON (busca o primeiro '{' e o último '}')
    - JSON cercado por ```json ... ```
    """
    stripped = _strip_md_fences(text).strip()
    # JSON puro
    if stripped.startswith("{"):
        try:
            result = json.loads(stripped)
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, ValueError):
            pass
    # JSON precedido/seguido por texto — extrai entre primeiro '{' e último '}'
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            result = json.loads(stripped[start:end + 1])
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, ValueError):
            pass
    return None


def _primary_content(data: dict[str, Any]) -> str | None:
    """Extrai o texto bruto da resposta do Orchestrate.

    Ordem de preferência:
    1. choices[0].message.content  (formato padrão OpenAI-compat / Orchestrate)
    2. content / output / response no topo (compatibilidade legada)
    """
    # 1. Formato padrão Orchestrate / OpenAI-compat
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        msg = choices[0].get("message", {})
        text = msg.get("content")
        if isinstance(text, str) and text.strip():
            return text.strip()

    # 2. Compatibilidade com respostas legadas
    for key in ("content", "output", "response"):
        value = data.get(key)
        if not value:
            continue
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            inner = value.get("content") or value.get("text")
            if isinstance(inner, str) and inner.strip():
                return inner.strip()

    return None


# ─────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────

def extract_agent_content(data: dict[str, Any]) -> str | None:
    """Extrai o conteúdo textual da resposta do Orchestrate.

    Se o texto primário for um JSON, extrai o campo de texto interno
    ('content', 'text', 'output', 'message').

    Retorna None quando não há conteúdo utilizável.
    """
    raw = _primary_content(data)
    if not raw:
        return None

    # Tenta expandir JSON interno para extrair o campo de texto.
    inner = _try_extract_json_from_string(raw)
    if isinstance(inner, dict):
        for key in ("content", "text", "output", "message"):
            value = inner.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        # O JSON inteiro era a resposta; devolve o bruto para quem precisar.
        return raw

    return raw


def extract_agent_json(data: dict[str, Any]) -> dict | None:
    """Extrai o JSON estruturado da resposta do Orchestrate.

    Aceita JSON puro, JSON cercado por cercas de markdown, e JSON precedido
    ou seguido de texto.

    Retorna None quando não há JSON utilizável.
    """
    raw = _primary_content(data)
    if not raw:
        return None

    result = _try_extract_json_from_string(raw)
    if result is None:
        logger.debug("extract_agent_json: sem JSON utilizável no conteúdo (keys=%s)", list(data.keys()))
    return result


def extract_thread_id(data: dict[str, Any]) -> str | None:
    """Extrai o thread_id da resposta do Orchestrate (multi-turn)."""
    tid = data.get("thread_id")
    if isinstance(tid, str) and tid.strip():
        return tid.strip()
    return None


# ─────────────────────────────────────────────
# Validadores de schema por agente
# ─────────────────────────────────────────────

def validate_mentor_response(data: dict) -> bool:
    """Schema Mentor: content (str) + suggestions (list)."""
    content = data.get("content")
    suggestions = data.get("suggestions")
    if not isinstance(content, str) or not content.strip():
        return False
    if suggestions is not None and not isinstance(suggestions, list):
        return False
    return True


def validate_catalyst_onboarding_response(data: dict) -> bool:
    """Schema Catalisador onboarding: phase_order + trail_modes + campos obrigatórios."""
    required = ("phase_order", "trail_modes", "trail_1_auto_concluded", "rationale", "next_message")
    for field in required:
        if field not in data:
            return False
    if not isinstance(data["phase_order"], list):
        return False
    if not isinstance(data["trail_modes"], dict):
        return False
    return True


def validate_catalyst_next_step_response(data: dict) -> bool:
    """Schema Catalisador next_step: tipo + mensagem."""
    return bool(data.get("tipo") or data.get("kind")) and bool(data.get("mensagem") or data.get("message"))


def validate_catalyst_celebrate_response(data: dict) -> bool:
    """Schema Catalisador celebrate_trail: celebration_message."""
    return bool(data.get("celebration_message"))


def validate_analyst_insight_response(data: dict) -> bool:
    """Schema Analista insight: severity + action + message."""
    return (
        bool(data.get("severity"))
        and bool(data.get("action"))
        and bool(data.get("message"))
    )


def validate_analyst_synthesis_response(data: dict) -> bool:
    """Schema Analista trail_synthesis: short + full."""
    return bool(data.get("short")) and ("full" in data)
