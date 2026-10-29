from sqlalchemy import select

from app.shared.models import Activity, Mission, Phase, UserMissionProgress, MissionStatus
from tests.conftest import auth_headers, register_verified_user


async def _seeded_mission(db_session, phase_number: int, mission_number: int):
    result = await db_session.execute(
        select(Mission)
        .join(Phase, Mission.phase_id == Phase.id)
        .where(Phase.number == phase_number, Mission.number == mission_number)
    )
    return result.scalar_one_or_none()


async def test_lesson_flow_is_ordered_and_hides_private_content(client, db_session):
    mission = await _seeded_mission(db_session, 1, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    response = await client.get(
        f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
    )
    assert response.status_code == 200
    data = response.json()

    assert data["steps"][0]["type"] == "intro"
    assert data["steps"][-1]["type"] == "summary"
    assert len(data["steps"]) >= 9
    assert data["current_step"] == 0
    assert data["completed_steps"] == []
    assert data["estimated_minutes"] >= 5

    question_steps = [step for step in data["steps"] if step["type"] != "reading"]
    assert any(step["type"] == "question" for step in question_steps)

    for step in data["steps"]:
        if step["activity"]:
            content = step["activity"]["content"]
            assert "correct_answer" not in content
            assert "correct_choice" not in content
            assert "evaluation_criteria" not in content


async def test_lesson_progress_saves_and_resumes_after_feedback(client, db_session):
    mission = await _seeded_mission(db_session, 1, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)

    lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    intro = lesson["steps"][0]
    saved = await client.post(
        f"/api/v1/journey/missions/{mission.id}/lesson/progress",
        json={"step_index": intro["index"]},
        headers=headers,
    )
    assert saved.status_code == 200
    assert saved.json()["current_step"] == 1
    assert saved.json()["completed_steps"] == [0]

    resumed = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    assert resumed["current_step"] == 1
    assert resumed["completed_steps"] == [0]

    reading_step = resumed["steps"][1]
    reading_saved = await client.post(
        f"/api/v1/journey/missions/{mission.id}/lesson/progress",
        json={"step_index": reading_step["index"]},
        headers=headers,
    )
    assert reading_saved.status_code == 200
    assert reading_saved.json()["current_step"] == 2

    question_step = next(
        step for step in resumed["steps"] if step["type"] == "question"
    )
    stored_activity = (
        await db_session.execute(
            select(Activity).where(Activity.id == question_step["activity"]["id"])
        )
    ).scalar_one()
    if stored_activity.activity_type == "multiple_choice":
        response_data = {
            "selected_option": stored_activity.content.get("correct_answer")
        }
    else:
        response_data = {"text": "Resposta de teste da lição."}

    answer = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": question_step["activity"]["id"],
            "response_data": response_data,
        },
        headers=headers,
    )
    assert answer.status_code == 200
    assert answer.json()["is_correct"] is True

    after_answer = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    assert after_answer["current_step"] == question_step["index"]
    assert question_step["index"] in after_answer["completed_steps"]
    restored = after_answer["steps"][question_step["index"]]["user_response"]
    assert restored["is_correct"] is True

    advanced = await client.post(
        f"/api/v1/journey/missions/{mission.id}/lesson/progress",
        json={"step_index": question_step["index"]},
        headers=headers,
    )
    assert advanced.status_code == 200
    assert advanced.json()["current_step"] == question_step["index"] + 1

    duplicate = await client.post(
        f"/api/v1/journey/missions/{mission.id}/lesson/progress",
        json={"step_index": question_step["index"]},
        headers=headers,
    )
    assert duplicate.status_code == 200
    assert duplicate.json()["completed_steps"].count(question_step["index"]) == 1


async def test_locked_mission_lesson_is_forbidden(client, db_session):
    mission = await _seeded_mission(db_session, 1, 2)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    response = await client.get(
        f"/api/v1/journey/missions/{mission.id}/lesson",
        headers=auth_headers(tokens),
    )
    assert response.status_code == 403


async def test_phase_2_lesson_flow_is_available_after_phase_1(client, db_session):
    mission_1 = await _seeded_mission(db_session, 1, 1)
    mission_2 = await _seeded_mission(db_session, 2, 1)
    if not mission_1 or not mission_2:
        import pytest

        pytest.skip("Conteúdo das Fases 1 e 2 não aplicado neste banco.")

    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    phase_1 = (
        await db_session.execute(
            select(Mission).where(Mission.phase_id == mission_1.phase_id)
        )
    ).scalars().all()
    for mission in phase_1:
        db_session.add(
            UserMissionProgress(
                user_id=user.id,
                mission_id=mission.id,
                status=MissionStatus.completed,
                score=100,
                attempts=1,
            )
        )
    await db_session.flush()

    response = await client.get(
        f"/api/v1/journey/missions/{mission_2.id}/lesson", headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["phase"]["number"] == 2
    assert data["steps"][0]["type"] == "intro"
    assert any(step["type"] == "question" for step in data["steps"])
    assert data["steps"][-1]["type"] == "summary"


async def _complete_previous_missions(db_session, user, target_mission):
    """Marca como concluídas as missões obrigatórias anteriores à missão-alvo."""
    target_phase = await db_session.get(Phase, target_mission.phase_id)
    missions = (await db_session.execute(select(Mission))).scalars().all()

    for candidate in missions:
        if not candidate.is_required:
            continue
        candidate_phase = await db_session.get(Phase, candidate.phase_id)
        is_previous = (
            candidate_phase.order < target_phase.order
            or (
                candidate_phase.order == target_phase.order
                and candidate.order < target_mission.order
            )
        )
        if not is_previous:
            continue

        existing = (
            await db_session.execute(
                select(UserMissionProgress).where(
                    UserMissionProgress.user_id == user.id,
                    UserMissionProgress.mission_id == candidate.id,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            db_session.add(
                UserMissionProgress(
                    user_id=user.id,
                    mission_id=candidate.id,
                    status=MissionStatus.completed,
                    score=100,
                    attempts=1,
                )
            )

    await db_session.flush()


async def test_phases_3_to_6_lesson_flows_are_available(client, db_session):
    targets = [(3, 1), (4, 1), (5, 1), (6, 1), (6, 4)]
    seeded = []
    for phase_number, mission_number in targets:
        mission = await _seeded_mission(db_session, phase_number, mission_number)
        if mission is None:
            import pytest

            pytest.skip("Conteúdo das Fases 3 a 6 não aplicado neste banco.")
        seeded.append((mission, mission_number))

    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    for mission, _ in seeded:
        await _complete_previous_missions(db_session, user, mission)

        response = await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["steps"][0]["type"] == "intro"
        assert data["steps"][-1]["type"] == "summary"
        assert len(data["steps"]) >= 6
        assert any(
            step["type"] in {"question", "scenario"} for step in data["steps"]
        )
        assert data["estimated_minutes"] >= 5

