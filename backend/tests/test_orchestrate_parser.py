"""Testes do extrator/validador de respostas do Orchestrate."""
from __future__ import annotations

import json

import pytest

from app.core.orchestrate_parser import (
    extract_agent_content,
    extract_agent_json,
    extract_thread_id,
    validate_analyst_insight_response,
    validate_analyst_synthesis_response,
    validate_catalyst_celebrate_response,
    validate_catalyst_next_step_response,
    validate_catalyst_onboarding_response,
    validate_mentor_response,
)


def _choices(content: str) -> dict:
    """Monta resposta padrão choices[0].message.content."""
    return {"choices": [{"message": {"content": content}}], "thread_id": "t1"}


# ─────────────────────────────────────────────
# extract_agent_content
# ─────────────────────────────────────────────

def test_extract_content_from_choices():
    data = _choices("Olá estudante!")
    assert extract_agent_content(data) == "Olá estudante!"


def test_extract_content_json_pure():
    """JSON puro em choices — retorna o bruto (para quem precisar do JSON)."""
    payload = json.dumps({"content": "Resposta do Mentor.", "suggestions": ["A", "B"]})
    data = _choices(payload)
    # Como é JSON com campo 'content', extrai o texto do campo.
    result = extract_agent_content(data)
    assert result == "Resposta do Mentor."


def test_extract_content_json_with_fences():
    raw = '```json\n{"content": "Texto cercado."}\n```'
    data = _choices(raw)
    assert extract_agent_content(data) == "Texto cercado."


def test_extract_content_text_before_json():
    raw = 'Aqui está: {"content": "Conteúdo real."}'
    data = _choices(raw)
    assert extract_agent_content(data) == "Conteúdo real."


def test_extract_content_plain_text():
    data = _choices("Apenas texto simples.")
    assert extract_agent_content(data) == "Apenas texto simples."


def test_extract_content_legacy_field():
    """Compatibilidade com campo 'content' no topo da resposta (legado)."""
    data = {"content": "Resposta legado.", "choices": []}
    assert extract_agent_content(data) == "Resposta legado."


def test_extract_content_empty_returns_none():
    assert extract_agent_content({}) is None
    assert extract_agent_content({"choices": []}) is None
    assert extract_agent_content({"choices": [{"message": {"content": ""}}]}) is None


def test_extract_content_choices_takes_priority_over_legacy():
    data = {
        "content": "legado",
        "choices": [{"message": {"content": "prioritário"}}],
    }
    assert extract_agent_content(data) == "prioritário"


# ─────────────────────────────────────────────
# extract_agent_json
# ─────────────────────────────────────────────

def test_extract_json_pure():
    payload = {"phase_order": [1, 2], "trail_modes": {"1": "standard"}}
    data = _choices(json.dumps(payload))
    result = extract_agent_json(data)
    assert result["phase_order"] == [1, 2]


def test_extract_json_with_md_fences():
    payload = {"severity": "attention", "action": "review", "message": "Revise!"}
    raw = f"```json\n{json.dumps(payload)}\n```"
    result = extract_agent_json(_choices(raw))
    assert result["severity"] == "attention"


def test_extract_json_with_text_around():
    payload = {"tipo": "continue", "mensagem": "Continue!"}
    raw = f"Aqui está minha recomendação:\n{json.dumps(payload)}\nBoa sorte!"
    result = extract_agent_json(_choices(raw))
    assert result["tipo"] == "continue"


def test_extract_json_returns_none_for_plain_text():
    result = extract_agent_json(_choices("Texto sem JSON."))
    assert result is None


def test_extract_json_returns_none_for_empty():
    assert extract_agent_json({}) is None


# ─────────────────────────────────────────────
# extract_thread_id
# ─────────────────────────────────────────────

def test_extract_thread_id():
    data = {"thread_id": "thread-abc", "choices": []}
    assert extract_thread_id(data) == "thread-abc"


def test_extract_thread_id_missing():
    assert extract_thread_id({}) is None
    assert extract_thread_id({"thread_id": ""}) is None


# ─────────────────────────────────────────────
# Validadores de schema
# ─────────────────────────────────────────────

def test_validate_mentor_response_valid():
    assert validate_mentor_response({"content": "Resposta.", "suggestions": ["A"]})
    assert validate_mentor_response({"content": "Resposta."})  # suggestions opcional


def test_validate_mentor_response_invalid():
    assert not validate_mentor_response({})
    assert not validate_mentor_response({"content": ""})
    assert not validate_mentor_response({"content": "ok", "suggestions": "não-é-lista"})


def test_validate_catalyst_onboarding_valid():
    data = {
        "phase_order": [1, 2, 3],
        "trail_modes": {"1": "standard"},
        "trail_1_auto_concluded": False,
        "rationale": "ok",
        "next_message": "próximo",
    }
    assert validate_catalyst_onboarding_response(data)


def test_validate_catalyst_onboarding_missing_field():
    data = {
        "phase_order": [1, 2, 3],
        "trail_1_auto_concluded": False,
        "rationale": "ok",
        "next_message": "ok",
        # trail_modes ausente
    }
    assert not validate_catalyst_onboarding_response(data)


def test_validate_catalyst_next_step_valid():
    assert validate_catalyst_next_step_response({"tipo": "start", "mensagem": "Vamos!"})
    assert validate_catalyst_next_step_response({"kind": "continue", "message": "Continue!"})


def test_validate_catalyst_next_step_invalid():
    assert not validate_catalyst_next_step_response({"tipo": "start"})  # sem mensagem
    assert not validate_catalyst_next_step_response({})


def test_validate_catalyst_celebrate_valid():
    assert validate_catalyst_celebrate_response({"celebration_message": "Parabéns!"})


def test_validate_catalyst_celebrate_invalid():
    assert not validate_catalyst_celebrate_response({})


def test_validate_analyst_insight_valid():
    assert validate_analyst_insight_response({
        "severity": "attention",
        "action": "review",
        "message": "Revise este conceito.",
    })


def test_validate_analyst_insight_invalid():
    assert not validate_analyst_insight_response({"severity": "attention", "action": "review"})


def test_validate_analyst_synthesis_valid():
    assert validate_analyst_synthesis_response({"short": "Síntese.", "full": {}})


def test_validate_analyst_synthesis_invalid():
    assert not validate_analyst_synthesis_response({"short": "ok"})  # sem 'full'
    assert not validate_analyst_synthesis_response({"full": {}})      # sem 'short'
