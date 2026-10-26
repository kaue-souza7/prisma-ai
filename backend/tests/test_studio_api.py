import pytest
from sqlalchemy import select

from app.core.config import settings
from app.modules.agents import studio_mentor
from app.modules.progress.service import add_coins, spend_coins
from app.modules.studio.service import set_generation_failed
from app.shared.models import (
    Activity,
    Competency,
    GeneratedContent,
    Mission,
    Phase,
    UserCompetencyProgress,
    UserPoints,
    UserResponse,
)
from tests.conftest import auth_headers, register_verified_user


async def _studio_phase(db_session, *, number: int = 98):
    phase = Phase(
        number=number,
        name="Fase do Estúdio",
        description="Criada apenas nos testes.",
        order=0,
        is_active=True,
    )
    db_session.add(phase)
    await db_session.flush()

    mission = Mission(
        phase_id=phase.id,
        number=1,
        name="Módulo do Estúdio",
        description="Criado apenas nos testes.",
        order=1,
        is_required=True,
        passing_score=70,
    )
    db_session.add(mission)
    await db_session.flush()

    competency = Competency(
        mission_id=mission.id,
        code="98.1.1",
        name="Competência do Estúdio",
        description=None,
        is_essential=True,
    )
    db_session.add(competency)
    await db_session.flush()

    activities = []
    for order in range(1, 11):
        activity = Activity(
            mission_id=mission.id,
            order=order,
            activity_type="multiple_choice",
            content={
                "prompt": f"Questão {order}",
                "options": [
                    {"value": "a", "label": "Incorreta"},
                    {"value": "b", "label": "Correta"},
                ],
                "correct_answer": "b",
                "feedback_correct": "Muito bem!",
                "feedback_incorrect": "Revise o conceito.",
                "competency_codes": ["98.1.1"],
            },
            points_value=10,
            is_active=True,
        )
        db_session.add(activity)
        activities.append(activity)

    await db_session.flush()
    return phase, mission, competency, activities


async def _answer_all(client, headers, mission, activities, *, correct_count: int):
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    last = None
    for index, activity in enumerate(activities):
        option = "b" if index < correct_count else "a"
        last = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": activity.id,
                "response_data": {"selected_option": option},
            },
            headers=headers,
        )
        assert last.status_code == 200, last.text
    return last


def _exercise_content() -> dict:
    return {
        "type": "exercicios",
        "questions": [
            {
                "prompt": "Qual é a correta?",
                "options": [
                    {"value": "a", "label": "Incorreta"},
                    {"value": "b", "label": "Correta"},
                ],
                "correct_answer": "b",
                "feedback_correct": "Muito bem!",
                "feedback_incorrect": "Revise o conceito.",
                "competency_codes": ["98.1.1"],
            },
            {
                "prompt": "Segunda questão",
                "options": [
                    {"value": "a", "label": "Incorreta"},
                    {"value": "b", "label": "Correta"},
                ],
                "correct_answer": "b",
                "feedback_correct": "Muito bem!",
                "feedback_incorrect": "Revise o conceito.",
                "competency_codes": ["98.1.1"],
            },
        ],
    }


async def test_add_and_spend_coins(client, db_session):
    user, _ = await register_verified_user(client, db_session)
    points = (
        await db_session.execute(
            select(UserPoints).where(UserPoints.user_id == user.id)
        )
    ).scalar_one()
    points.coins = 5
    await db_session.flush()

    assert await add_coins(db_session, user.id, 3) == 8

    with pytest.raises(ValueError, match="saldo_insuficiente"):
        await spend_coins(db_session, user.id, 10)

    assert await spend_coins(db_session, user.id, 8) == 0


async def test_correct_answer_awards_two_prisms(client, db_session):
    _, mission, _, activities = await _studio_phase(db_session)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    result = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": activities[0].id,
            "response_data": {"selected_option": "b"},
        },
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert result.json()["coins_earned"] == 2
    assert summary.json()["coins"] == 2


async def test_module_completion_awards_prisms_by_score_band(client, db_session):
    _, mission, _, activities = await _studio_phase(db_session, number=98)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    last = await _answer_all(
        client, headers, mission, activities, correct_count=8
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    # 8 acertos × 2 + 15 de aprovação (80%).
    assert summary.json()["coins"] == 31
    assert last.json()["coins_earned"] == 15


async def test_excellence_awards_extra_prisms(client, db_session):
    _, mission, _, activities = await _studio_phase(db_session, number=98)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    last = await _answer_all(
        client, headers, mission, activities, correct_count=9
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    # 9 acertos × 2 + 25 de excelência (90%).
    assert summary.json()["coins"] == 43
    assert last.json()["coins_earned"] == 25


async def test_retry_does_not_duplicate_prisms(client, db_session):
    _, mission, _, activities = await _studio_phase(db_session, number=98)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    await _answer_all(client, headers, mission, activities, correct_count=10)
    before = await client.get("/api/v1/progress/summary", headers=headers)
    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": True},
        headers=headers,
    )
    last = await _answer_all(client, headers, mission, activities, correct_count=10)
    after = await client.get("/api/v1/progress/summary", headers=headers)

    assert retry.status_code == 200
    assert before.json()["coins"] == 45
    assert last.json()["coins_earned"] == 0
    assert after.json()["coins"] == before.json()["coins"]


async def test_generation_failure_refunds_the_spent_prisms(client, db_session):
    phase, mission, _, _ = await _studio_phase(db_session)
    user, _ = await register_verified_user(client, db_session)
    points = (
        await db_session.execute(
            select(UserPoints).where(UserPoints.user_id == user.id)
        )
    ).scalar_one()
    points.coins = 80
    generation = GeneratedContent(
        user_id=user.id,
        format="flashcards",
        phase_id=phase.id,
        mission_id=mission.id,
        style_hint=None,
        content={},
        coins_spent=20,
        status="generating",
    )
    db_session.add(generation)
    await db_session.flush()

    await set_generation_failed(db_session, generation.id)
    await set_generation_failed(db_session, generation.id)
    await db_session.refresh(points)

    assert generation.status == "failed"
    assert points.coins == 100


async def test_studio_generate_requires_coursed_phase(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    phase_result = await db_session.execute(select(Phase).order_by(Phase.order))
    phase = phase_result.scalars().first()

    response = await client.post(
        "/api/v1/studio/generate",
        json={"format": "flashcards", "phase_id": phase.id},
        headers=headers,
    )

    assert response.status_code == 403
    assert "não cursou" in response.json()["error"]["message"]


async def test_studio_generate_without_balance_returns_402(
    client, db_session, monkeypatch
):
    phase, mission, _, _ = await _studio_phase(db_session)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )

    monkeypatch.setattr(settings, "orchestrate_enabled", True)
    monkeypatch.setattr(settings, "orchestrate_url", "http://orchestrate.test")

    response = await client.post(
        "/api/v1/studio/generate",
        json={
            "format": "revisao",
            "phase_id": phase.id,
            "mission_id": mission.id,
        },
        headers=headers,
    )

    assert response.status_code == 402
    assert "insuficiente" in response.json()["error"]["message"]


async def test_studio_generate_happy_path_spends_and_saves(
    client, db_session, monkeypatch
):
    phase, mission, _, _ = await _studio_phase(db_session)
    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    points = (
        await db_session.execute(
            select(UserPoints).where(UserPoints.user_id == user.id)
        )
    ).scalar_one()
    points.coins = 100
    await db_session.flush()

    monkeypatch.setattr(settings, "orchestrate_enabled", True)
    monkeypatch.setattr(settings, "orchestrate_url", "http://orchestrate.test")

    async def fake_orchestrate(payload: dict) -> dict:
        return {
            "type": "flashcards",
            "cards": [
                {"front": "O que é reserva?", "back": "Dinheiro para imprevistos."}
            ],
        }

    monkeypatch.setattr(studio_mentor, "call_orchestrate", fake_orchestrate)

    generated = await client.post(
        "/api/v1/studio/generate",
        json={
            "format": "flashcards",
            "phase_id": phase.id,
            "mission_id": mission.id,
            "style_hint": "analogia com doces",
        },
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)
    library = await client.get("/api/v1/studio/library", headers=headers)

    assert generated.status_code == 200, generated.text
    assert generated.json()["status"] == "ready"
    assert generated.json()["phase_name"] == phase.name
    assert generated.json()["mission_name"] == mission.name
    assert generated.json()["style_hint"] == "analogia com doces"
    assert generated.json()["content"]["cards"][0]["front"] == "O que é reserva?"
    assert generated.json()["coins_spent"] == 20
    assert summary.json()["coins"] == 80
    assert library.json()["total"] == 1


async def test_studio_is_honest_without_orchestrate_and_does_not_charge(
    client, db_session
):
    phase, mission, _, _ = await _studio_phase(db_session)
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )

    response = await client.post(
        "/api/v1/studio/generate",
        json={
            "format": "flashcards",
            "phase_id": phase.id,
            "mission_id": mission.id,
        },
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert response.status_code == 503
    assert "estará disponível" in response.json()["error"]["message"]
    assert summary.json()["coins"] == 0


async def test_studio_exercise_feeds_analyst_and_rewards_completion(
    client, db_session
):
    phase, mission, competency, _ = await _studio_phase(db_session)
    user, tokens = await register_verified_user(client, db_session)
    _, other_tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    other_headers = auth_headers(other_tokens)

    generation = GeneratedContent(
        user_id=user.id,
        format="exercicios",
        phase_id=phase.id,
        mission_id=mission.id,
        style_hint="analogia com doces",
        content=_exercise_content(),
        coins_spent=25,
        status="ready",
    )
    db_session.add(generation)
    await db_session.flush()

    hidden = await client.get(
        f"/api/v1/studio/generate/{generation.id}", headers=headers
    )
    forbidden = await client.get(
        f"/api/v1/studio/generate/{generation.id}", headers=other_headers
    )
    assert hidden.status_code == 200
    assert "correct_answer" not in hidden.json()["content"]["questions"][0]
    assert forbidden.status_code == 404

    wrong = await client.post(
        f"/api/v1/studio/exercises/{generation.id}/submit",
        json={"question_index": 0, "response_data": {"selected_option": "a"}},
        headers=headers,
    )
    assert wrong.status_code == 200
    assert wrong.json()["is_correct"] is False
    assert wrong.json()["correct_answer"] == "b"
    assert wrong.json()["all_done"] is False
    assert wrong.json()["coins_earned"] == 0

    duplicate = await client.post(
        f"/api/v1/studio/exercises/{generation.id}/submit",
        json={"question_index": 0, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    assert duplicate.status_code == 409

    revealed = await client.get(
        f"/api/v1/studio/generate/{generation.id}", headers=headers
    )
    assert revealed.json()["content"]["questions"][0]["correct_answer"] == "b"

    last = await client.post(
        f"/api/v1/studio/exercises/{generation.id}/submit",
        json={"question_index": 1, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)
    competency_progress = (
        await db_session.execute(
            select(UserCompetencyProgress).where(
                UserCompetencyProgress.user_id == user.id,
                UserCompetencyProgress.competency_id == competency.id,
            )
        )
    ).scalar_one()
    responses = (
        await db_session.execute(
            select(UserResponse).where(
                UserResponse.user_id == user.id,
                UserResponse.mission_attempt == 0,
            )
        )
    ).scalars().all()

    assert last.status_code == 200
    assert last.json()["all_done"] is True
    assert last.json()["coins_earned"] == 5
    assert summary.json()["coins"] == 5
    assert competency_progress.correct_count == 1
    assert competency_progress.incorrect_count == 1
    assert len(responses) == 2
    assert all(item.mission_id is None and item.activity_id is None for item in responses)


async def test_studio_library_is_personal(client, db_session):
    phase, mission, _, _ = await _studio_phase(db_session)
    user, tokens = await register_verified_user(client, db_session)
    _, other_tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    other_headers = auth_headers(other_tokens)

    db_session.add(
        GeneratedContent(
            user_id=user.id,
            format="revisao",
            phase_id=phase.id,
            mission_id=mission.id,
            style_hint=None,
            content={
                "type": "revisao",
                "title": "Revisão",
                "sections": [{"title": "Seção", "body": "Conteúdo"}],
                "summary": ["Ponto"],
            },
            coins_spent=30,
            status="ready",
        )
    )
    await db_session.flush()

    mine = await client.get("/api/v1/studio/library", headers=headers)
    theirs = await client.get("/api/v1/studio/library", headers=other_headers)

    assert mine.status_code == 200
    assert mine.json()["total"] == 1
    assert mine.json()["items"][0]["format"] == "revisao"
    assert theirs.json()["total"] == 0
