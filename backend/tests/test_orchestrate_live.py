"""Teste de contrato ao vivo com o watsonx Orchestrate.

Não roda na suíte normal. Use apenas quando quiser validar os agentes reais:

    ORCHESTRATE_LIVE_TEST=1 docker compose exec backend pytest tests/test_orchestrate_live.py -q

Requer ORCHESTRATE_ENABLED=true e os UUIDs dos agentes no ambiente.
"""
import os

import pytest

from app.core.config import settings
from app.core.orchestrate_client import chat_completion
from app.core.orchestrate_parser import (
    extract_agent_json,
    validate_analyst_insight_response,
    validate_catalyst_next_step_response,
    validate_catalyst_onboarding_response,
)

pytestmark = pytest.mark.skipif(
    os.getenv("ORCHESTRATE_LIVE_TEST") != "1",
    reason="Defina ORCHESTRATE_LIVE_TEST=1 para rodar o contrato ao vivo.",
)


async def test_catalyst_onboarding_live():
    parsed = extract_agent_json(
        await chat_completion(
            agent_id=settings.orchestrate_catalyst_agent_id,
            payload={
                "agent": "catalyst",
                "action": "onboarding",
                "fixed_answers": {
                    "objetivo": "dividas",
                    "life_context": "ja_trabalho",
                    "urgency": "agora_preciso",
                    "knowledge_level_declared": "intermediate",
                },
                "conversation_history": [],
            },
        )
    )
    assert parsed is not None
    assert validate_catalyst_onboarding_response(parsed)
    assert len(parsed["phase_order"]) == 12


async def test_catalyst_next_step_live():
    parsed = extract_agent_json(
        await chat_completion(
            agent_id=settings.orchestrate_catalyst_agent_id,
            payload={
                "agent": "catalyst",
                "action": "next_step",
                "user_context": {
                    "personal_goal": "Sair das dívidas",
                    "trail_modes": {"1": "express"},
                    "trail_1_auto_concluded": True,
                },
                "progress": {
                    "completed_trails": [1],
                    "current_trail": 2,
                    "current_mission": 4,
                    "last_session_hours_ago": 24,
                },
                "analyst_signals": [],
                "reinforcement_topics": [],
            },
        )
    )
    assert parsed is not None
    assert validate_catalyst_next_step_response(parsed)


async def test_analyst_insight_live():
    parsed = extract_agent_json(
        await chat_completion(
            agent_id=settings.orchestrate_analyst_agent_id,
            payload={
                "agent": "analyst",
                "action": "insight",
                "scope": "mission",
                "competencies": [
                    {
                        "code": "1.1.1",
                        "name": "Distinguir salário bruto de líquido",
                        "status": "developing",
                        "reinforcement_suggested": True,
                    }
                ],
            },
        )
    )
    assert parsed is not None
    assert validate_analyst_insight_response(parsed)
    assert parsed["severity"] in {"attention", "positive", "neutral"}
