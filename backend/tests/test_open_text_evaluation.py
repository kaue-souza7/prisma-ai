from sqlalchemy import select

from app.core.config import settings
from app.modules.agents.evaluator import (
    OpenTextEvaluation,
    parse_open_text_evaluation,
)
from app.modules.journey import service as journey_service
from app.shared.models import Activity, Mission, Phase
from tests.conftest import auth_headers, register_verified_user


def test_parse_correct_verdict():
    evaluation = parse_open_text_evaluation(
        {"verdict": "correct", "feedback": "Boa resposta."}
    )
    assert evaluation is not None
    assert evaluation.verdict == "correct"
    assert evaluation.is_correct is True
    assert evaluation.feedback == "Boa resposta."


def test_parse_incorrect_verdict():
    evaluation = parse_open_text_evaluation(
        {"verdict": "INCORRECT", "feedback": "Faltou explicar o desconto."}
    )
    assert evaluation is not None
    assert evaluation.verdict == "incorrect"
    assert evaluation.is_correct is False


def test_parse_ambiguous_without_feedback_uses_clarification():
    evaluation = parse_open_text_evaluation({"verdict": "ambiguous"})
    assert evaluation is not None
    assert evaluation.verdict == "ambiguous"
    assert evaluation.is_correct is None
    assert "complementar" in evaluation.feedback.lower()


def test_parse_invalid_verdict_returns_none():
    assert parse_open_text_evaluation({"verdict": "maybe", "feedback": "x"}) is None
    assert parse_open_text_evaluation({"feedback": "x"}) is None


def test_parse_tolerates_punctuation_and_boolean():
    punctuation = parse_open_text_evaluation(
        {"verdict": "correct.", "feedback": "Boa."}
    )
    boolean = parse_open_text_evaluation({"verdict": False, "feedback": "Revise."})
    assert punctuation is not None and punctuation.is_correct is True
    assert boolean is not None and boolean.is_correct is False


def _activity_with_open_text() -> Activity:
    return Activity(
        mission_id=1,
        order=1,
        activity_type="open_text",
        content={
            "prompt": "Explique o conceito.",
            "feedback_static": "Resposta registrada.",
            "evaluation_criteria": ["Explica o conceito com um exemplo."],
        },
        points_value=10,
        is_active=True,
    )


async def test_evaluate_open_text_falls_back_without_mentor(monkeypatch):
    from app.modules.agents import evaluator

    monkeypatch.setattr(settings, "orchestrate_enabled", False)
    monkeypatch.setattr(settings, "orchestrate_mentor_enabled", False)
    evaluation = await evaluator.evaluate_open_text(
        activity=_activity_with_open_text(),
        student_answer="Uma resposta.",
        mission=Mission(id=1, phase_id=1, number=1, name="Missão", order=1),
        phase=Phase(id=1, number=1, name="Trilha", order=1),
        profile=None,
    )
    assert evaluation.verdict == "unavailable"
    assert evaluation.is_correct is None
    assert evaluation.feedback == "Resposta registrada."


async def test_open_text_submit_persists_agent_verdict(
    client, db_session, monkeypatch
):
    mission = (
        await db_session.execute(select(Mission).where(Mission.id == 1))
    ).scalar_one_or_none()
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    detail = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}", headers=headers
        )
    ).json()
    open_text = next(
        activity
        for activity in detail["activities"]
        if activity["activity_type"] == "open_text"
    )

    async def fake_evaluate(**kwargs):
        return OpenTextEvaluation(
            verdict="correct",
            is_correct=True,
            feedback="Você explicou o conceito e deu um exemplo.",
            source="orchestrate",
        )

    monkeypatch.setattr(journey_service.evaluator, "evaluate_open_text", fake_evaluate)

    response = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": open_text["id"],
            "response_data": {"text": "O bruto é antes dos descontos; o líquido é o que cai na conta."},
        },
        headers=headers,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["is_correct"] is True
    assert body["evaluation_status"] == "correct"
    assert body["feedback"] == "Você explicou o conceito e deu um exemplo."

    lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    matching = [
        item
        for item in lesson["steps"]
        if item.get("activity") and item["activity"]["id"] == open_text["id"]
    ]
    assert matching
    stored = matching[0]["user_response"]
    assert stored["is_correct"] is True
    assert stored["evaluation_status"] == "correct"
    assert stored["feedback"] == "Você explicou o conceito e deu um exemplo."


async def test_open_text_ambiguous_verdict_allows_one_resubmission(
    client, db_session, monkeypatch
):
    mission = (
        await db_session.execute(select(Mission).where(Mission.id == 1))
    ).scalar_one_or_none()
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    detail = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}", headers=headers
        )
    ).json()
    open_text = next(
        activity
        for activity in detail["activities"]
        if activity["activity_type"] == "open_text"
    )

    calls = {"count": 0}

    async def fake_evaluate(**kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            return OpenTextEvaluation(
                verdict="ambiguous",
                is_correct=None,
                feedback="Pode complementar com um exemplo?",
                source="orchestrate",
            )
        return OpenTextEvaluation(
            verdict="correct",
            is_correct=True,
            feedback="Agora ficou claro.",
            source="orchestrate",
        )

    monkeypatch.setattr(journey_service.evaluator, "evaluate_open_text", fake_evaluate)

    first = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": open_text["id"],
            "response_data": {"text": "Acho que tem a ver com descontos."},
        },
        headers=headers,
    )
    assert first.status_code == 200, first.text
    assert first.json()["evaluation_status"] == "ambiguous"

    second = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": open_text["id"],
            "response_data": {
                "text": "O bruto é antes dos descontos e o líquido é o valor recebido."
            },
        },
        headers=headers,
    )
    assert second.status_code == 200, second.text
    assert second.json()["evaluation_status"] == "correct"
    assert second.json()["is_correct"] is True

    third = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": open_text["id"],
            "response_data": {"text": "Mais uma tentativa."},
        },
        headers=headers,
    )
    assert third.status_code == 409
