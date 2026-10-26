from sqlalchemy import select

from app.shared.models import Activity, Mission, Phase
from tests.conftest import auth_headers, register_verified_user


async def create_test_mission(db_session, *, number: int, correct_answer: str = "b"):
    phase_result = await db_session.execute(select(Phase).order_by(Phase.order).limit(1))
    phase = phase_result.scalar_one()

    mission = Mission(
        phase_id=phase.id,
        number=number,
        name="Missão de teste",
        description="Missão criada apenas no teste de integração.",
        order=number,
        # Não marca a fase inteira como concluída, pois o conteúdo real da
        # Fase 1 ainda não foi inserido.
        is_required=False,
        passing_score=70,
    )
    db_session.add(mission)
    await db_session.flush()

    activity = Activity(
        mission_id=mission.id,
        order=1,
        activity_type="multiple_choice",
        content={
            "prompt": "Qual alternativa está correta?",
            "options": [
                {"value": "a", "label": "Alternativa A"},
                {"value": "b", "label": "Alternativa B"},
            ],
            "correct_answer": correct_answer,
            "feedback_correct": "Muito bem!",
            "feedback_incorrect": "Revise o conceito e tente novamente.",
        },
        points_value=10,
        is_active=True,
    )
    db_session.add(activity)
    await db_session.flush()
    return mission, activity


async def test_journey_completion_after_retry_awards_70(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission, activity = await create_test_mission(db_session, number=901)

    start = await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    detail = await client.get(f"/api/v1/journey/missions/{mission.id}", headers=headers)
    wrong = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "a"}},
        headers=headers,
    )
    duplicate = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    correct = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert start.status_code == 200
    assert start.json()["status"] == "in_progress"
    assert detail.status_code == 200
    assert "correct_answer" not in detail.json()["activities"][0]["content"]
    assert wrong.status_code == 200
    assert wrong.json()["is_correct"] is False
    assert wrong.json()["correct_answer"] == "b"
    assert wrong.json()["mission_completed"] is False
    assert wrong.json()["attempt_finished"] is True
    assert wrong.json()["score_percent"] == 0
    assert wrong.json()["passed"] is False
    assert wrong.json()["must_retry"] is True
    assert wrong.json()["can_retry_optionally"] is False
    assert duplicate.status_code == 409
    assert retry.status_code == 200
    assert retry.json()["attempts"] == 2
    assert retry.json()["status"] == "in_progress"
    assert correct.status_code == 200
    assert correct.json()["is_correct"] is True
    assert correct.json()["mission_completed"] is True
    assert correct.json()["points_earned"] == 70
    assert correct.json()["score_percent"] == 100
    assert correct.json()["passed"] is True
    assert correct.json()["must_retry"] is False
    assert correct.json()["can_retry_optionally"] is True
    assert "Sem dúvidas" not in correct.json()["new_achievements"]
    assert summary.json()["total_points"] == 70
    assert summary.json()["missions_completed"] == 1


async def test_first_attempt_awards_100_and_achievement(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission, activity = await create_test_mission(db_session, number=902)

    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    result = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert result.json()["points_earned"] == 100
    assert result.json()["score_percent"] == 100
    assert result.json()["passed"] is True
    assert result.json()["can_retry_optionally"] is True
    assert "Sem dúvidas" in result.json()["new_achievements"]
    assert summary.json()["total_points"] == 100


async def test_voluntary_retry_does_not_award_points_twice(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission, activity = await create_test_mission(db_session, number=903)

    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    first = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    duplicate = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )

    forbidden_retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": True},
        headers=headers,
    )
    second = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )
    summary = await client.get("/api/v1/progress/summary", headers=headers)

    assert first.json()["points_earned"] == 100
    assert duplicate.status_code == 409
    assert forbidden_retry.status_code == 403
    assert retry.status_code == 200
    assert retry.json()["attempts"] == 2
    assert second.json()["mission_completed"] is True
    assert second.json()["points_earned"] == 0
    assert summary.json()["total_points"] == 100


async def test_retry_unattempted_mission_returns_409(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission, _ = await create_test_mission(db_session, number=906)

    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )

    assert retry.status_code == 409
    assert "ainda não foi iniciado" in retry.json()["error"]["message"]


async def test_activity_must_belong_to_mission(client, db_session):
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission_a, _ = await create_test_mission(db_session, number=904)
    _, activity_b = await create_test_mission(db_session, number=905)

    response = await client.post(
        f"/api/v1/journey/missions/{mission_a.id}/submit",
        json={"activity_id": activity_b.id, "response_data": {"selected_option": "b"}},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Atividade não encontrada."
