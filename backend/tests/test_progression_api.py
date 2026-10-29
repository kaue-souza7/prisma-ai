from sqlalchemy import func, select

from app.shared.models import (
    Activity,
    Mission,
    MissionStatus,
    Phase,
    UserMissionProgress,
    UserResponse,
)
from tests.conftest import auth_headers, register_verified_user


async def _seeded_mission(db_session, number: int) -> Mission | None:
    result = await db_session.execute(
        select(Mission)
        .join(Phase, Mission.phase_id == Phase.id)
        .where(Phase.number == 1, Mission.number == number)
    )
    return result.scalar_one_or_none()


async def _test_phase(db_session) -> Phase:
    """Fase isolada para testar desbloqueios sem depender do conteúdo real."""
    phase = Phase(
        number=99,
        name="Fase de avaliação",
        description="Criada apenas nos testes.",
        order=0,
        is_active=True,
    )
    db_session.add(phase)
    await db_session.flush()
    return phase


async def _mission_with_activities(
    db_session,
    phase: Phase,
    *,
    number: int,
    activity_count: int,
    is_required: bool = True,
) -> tuple[Mission, list[Activity]]:
    mission = Mission(
        phase_id=phase.id,
        number=number,
        name=f"Módulo de teste {number}",
        description="Criado apenas nos testes.",
        order=number,
        is_required=is_required,
        passing_score=70,
    )
    db_session.add(mission)
    await db_session.flush()

    activities = []
    for order in range(1, activity_count + 1):
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
            },
            points_value=10,
            is_active=True,
        )
        db_session.add(activity)
        activities.append(activity)

    await db_session.flush()
    return mission, activities


async def _answer_mission(
    client,
    headers,
    mission: Mission,
    activities: list[Activity],
    *,
    correct_count: int,
):
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
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


async def test_second_mission_is_locked_until_the_first_is_completed(client, db_session):
    mission_1 = await _seeded_mission(db_session, 1)
    mission_2 = await _seeded_mission(db_session, 2)
    if not mission_1 or not mission_2:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    locked = await client.post(
        f"/api/v1/journey/missions/{mission_2.id}/start", headers=headers
    )
    assert locked.status_code == 403

    db_session.add(
        UserMissionProgress(
            user_id=(await _user_id(client, headers)),
            mission_id=mission_1.id,
            status=MissionStatus.completed,
            score=100,
            attempts=1,
        )
    )
    await db_session.flush()

    unlocked = await client.post(
        f"/api/v1/journey/missions/{mission_2.id}/start", headers=headers
    )
    assert unlocked.status_code == 200
    assert unlocked.json()["status"] == "in_progress"


async def _user_id(client, headers) -> int:
    response = await client.get("/api/v1/users/me", headers=headers)
    return response.json()["user"]["id"]


async def test_seeded_mission_hides_private_keys_and_publishes_support_content(
    client, db_session
):
    mission = await _seeded_mission(db_session, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    detail = await client.get(f"/api/v1/journey/missions/{mission.id}", headers=headers)
    assert detail.status_code == 200
    for activity in detail.json()["activities"]:
        assert "correct_answer" not in activity["content"]
        assert "correct_choice" not in activity["content"]
        assert "evaluation_criteria" not in activity["content"]
        assert "feedback_correct" not in activity["content"]
        assert "feedback_incorrect" not in activity["content"]

    content = await client.get(
        f"/api/v1/content/missions/{mission.id}", headers=headers
    )
    assert content.status_code == 200
    assert len(content.json()) == 4
    assert all(item["is_published"] for item in content.json())


async def test_map_exposes_sequential_unlock_status(client, db_session):
    mission_1 = await _seeded_mission(db_session, 1)
    if not mission_1:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    response = await client.get("/api/v1/journey/phases/my-progress", headers=headers)
    assert response.status_code == 200
    phase = response.json()[0]
    statuses = {
        item["mission"]["number"]: item["status"] for item in phase["missions"]
    }
    assert statuses == {1: "available", 2: "locked", 3: "locked"}


async def test_second_submission_to_same_activity_returns_409(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=2, is_required=False
    )
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    first = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": activities[0].id,
            "response_data": {"selected_option": "a"},
        },
        headers=headers,
    )
    duplicate = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": activities[0].id,
            "response_data": {"selected_option": "b"},
        },
        headers=headers,
    )
    other = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": activities[1].id,
            "response_data": {"selected_option": "b"},
        },
        headers=headers,
    )

    assert first.status_code == 200
    assert first.json()["correct_answer"] == "b"
    assert duplicate.status_code == 409
    assert other.status_code == 200


async def test_score_at_or_above_90_passes_with_excellence(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=10
    )
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    result = await _answer_mission(
        client, headers, mission, activities, correct_count=9
    )

    lesson = await client.get(
        f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
    )

    assert result.json()["score_percent"] == 90
    assert result.json()["passed"] is True
    assert result.json()["mission_completed"] is True
    assert result.json()["must_retry"] is False
    assert result.json()["can_retry_optionally"] is True
    assert result.json()["points_earned"] == 100
    assert lesson.json()["attempt_finished"] is True
    assert lesson.json()["score_percent"] == 90
    assert lesson.json()["passed"] is True
    assert lesson.json()["can_retry_optionally"] is True


async def test_score_exactly_70_passes(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=10
    )
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    result = await _answer_mission(
        client, headers, mission, activities, correct_count=7
    )

    assert result.json()["score_percent"] == 70
    assert result.json()["passed"] is True
    assert result.json()["must_retry"] is False
    assert result.json()["can_retry_optionally"] is False


async def test_score_between_70_and_89_passes_without_excellence(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=10
    )
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    result = await _answer_mission(
        client, headers, mission, activities, correct_count=8
    )

    assert result.json()["score_percent"] == 80
    assert result.json()["passed"] is True
    assert result.json()["must_retry"] is False
    assert result.json()["can_retry_optionally"] is False
    assert result.json()["points_earned"] == 70


async def test_score_below_70_requires_retry_and_blocks_next_module(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=10
    )
    next_mission, _ = await _mission_with_activities(
        db_session, phase, number=2, activity_count=1
    )
    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    result = await _answer_mission(
        client, headers, mission, activities, correct_count=6
    )
    blocked = await client.post(
        f"/api/v1/journey/missions/{next_mission.id}/start", headers=headers
    )
    lesson = await client.get(
        f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
    )

    assert result.json()["score_percent"] == 60
    assert result.json()["passed"] is False
    assert result.json()["must_retry"] is True
    assert result.json()["mission_completed"] is False
    assert result.json()["points_earned"] == 0
    assert blocked.status_code == 403
    assert lesson.json()["attempt_finished"] is True
    assert lesson.json()["score_percent"] == 60
    assert lesson.json()["passed"] is False
    assert lesson.json()["must_retry"] is True
    assert lesson.json()["can_retry_optionally"] is False


async def test_retry_resets_progress_without_deleting_history(client, db_session):
    phase = await _test_phase(db_session)
    mission, activities = await _mission_with_activities(
        db_session, phase, number=1, activity_count=2
    )
    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    for activity in activities:
        await client.post(
            f"/api/v1/journey/missions/{mission.id}/start", headers=headers
        )
        await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": activity.id,
                "response_data": {"selected_option": "a"},
            },
            headers=headers,
        )

    progress = (
        await db_session.execute(
            select(UserMissionProgress).where(
                UserMissionProgress.user_id == user.id,
                UserMissionProgress.mission_id == mission.id,
            )
        )
    ).scalar_one()
    progress.current_step = 4
    progress.completed_steps = [0, 1, 2, 3]
    await db_session.flush()

    responses_before = (
        await db_session.execute(
            select(func.count(UserResponse.id)).where(
                UserResponse.user_id == user.id,
                UserResponse.mission_id == mission.id,
            )
        )
    ).scalar_one()

    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    await db_session.refresh(progress)
    responses_after = (
        await db_session.execute(
            select(func.count(UserResponse.id)).where(
                UserResponse.user_id == user.id,
                UserResponse.mission_id == mission.id,
            )
        )
    ).scalar_one()

    assert retry.status_code == 200
    assert retry.json()["attempts"] == 2
    assert retry.json()["status"] == "in_progress"
    assert progress.current_step == 0
    assert progress.completed_steps == []
    assert responses_before == 2
    assert responses_after == responses_before


async def test_competency_is_demonstrated_only_after_all_linked_evidence(client, db_session):
    mission = await _seeded_mission(db_session, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    detail = await client.get(f"/api/v1/journey/missions/{mission.id}", headers=headers)
    activities = detail.json()["activities"]
    mc_1 = next(a for a in activities if a["activity_type"] == "multiple_choice")
    open_text = next(a for a in activities if a["activity_type"] == "open_text")

    stored_mc = (
        await db_session.execute(select(Activity).where(Activity.id == mc_1["id"]))
    ).scalar_one()
    correct = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": mc_1["id"],
            "response_data": {
                "selected_option": stored_mc.content.get("correct_answer")
            },
        },
        headers=headers,
    )
    assert correct.status_code == 200

    refreshed = await client.get(
        f"/api/v1/journey/missions/{mission.id}", headers=headers
    )
    assert mc_1["id"] in refreshed.json()["completed_activity_ids"]

    summary = await client.get("/api/v1/progress/summary", headers=headers)
    competency = next(
        c for c in summary.json()["competencies"] if c["code"] == "1.1.1"
    )
    assert competency["status"] == "developing"
    assert competency["correct_count"] == 1

    await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={
            "activity_id": open_text["id"],
            "response_data": {"text": "O bruto é o combinado e o líquido é o que cai na conta."},
        },
        headers=headers,
    )

    refreshed = await client.get(
        f"/api/v1/journey/missions/{mission.id}", headers=headers
    )
    completed_ids = set(refreshed.json()["completed_activity_ids"])
    assert {mc_1["id"], open_text["id"]} <= completed_ids

    summary = await client.get("/api/v1/progress/summary", headers=headers)
    competency = next(
        c for c in summary.json()["competencies"] if c["code"] == "1.1.1"
    )
    assert competency["status"] == "demonstrated"


async def test_phase_achievement_requires_all_three_seeded_missions(client, db_session):
    mission_1 = await _seeded_mission(db_session, 1)
    mission_2 = await _seeded_mission(db_session, 2)
    mission_3 = await _seeded_mission(db_session, 3)
    if not mission_1 or not mission_2 or not mission_3:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    user_id = await _user_id(client, headers)

    for mission in (mission_1, mission_2):
        db_session.add(
            UserMissionProgress(
                user_id=user_id,
                mission_id=mission.id,
                status=MissionStatus.completed,
                score=100,
                attempts=1,
            )
        )
    await db_session.flush()

    await client.post(f"/api/v1/journey/missions/{mission_3.id}/start", headers=headers)

    # Descobre o question_set da tentativa ativa diretamente no banco
    from sqlalchemy import select as sa_select
    from app.shared.models import Activity as ActivityModel, UserMissionAttempt
    attempt_row = await db_session.execute(
        sa_select(UserMissionAttempt.question_set_used)
        .where(
            UserMissionAttempt.user_id == user_id,
            UserMissionAttempt.mission_id == mission_3.id,
        )
        .order_by(UserMissionAttempt.id.desc())
        .limit(1)
    )
    active_set = attempt_row.scalar_one_or_none() or 1

    # Busca todas as atividades do conjunto ativo para obter as respostas corretas
    act_rows = await db_session.execute(
        sa_select(ActivityModel)
        .where(
            ActivityModel.mission_id == mission_3.id,
            ActivityModel.question_set == active_set,
            ActivityModel.is_active == True,
        )
        .order_by(ActivityModel.order)
    )
    active_activities = list(act_rows.scalars().all())

    last = None
    for activity in active_activities:
        content = activity.content
        if activity.activity_type == "multiple_choice":
            response_data = {"selected_option": content.get("correct_answer", "a")}
        else:
            response_data = {"text": "Aprovado — resposta de avaliação do teste."}
        last = await client.post(
            f"/api/v1/journey/missions/{mission_3.id}/submit",
            json={"activity_id": activity.id, "response_data": response_data},
            headers=headers,
        )
        assert last.status_code == 200, f"Submit falhou para atividade {activity.id}: {last.json()}"

    assert last.json()["mission_completed"] is True
    assert "Planejador iniciante" in last.json()["new_achievements"]

    summary = await client.get("/api/v1/progress/summary", headers=headers)
    assert "planejador_iniciante" in [
        achievement["key"] for achievement in summary.json()["achievements"]
    ]


async def test_repeated_errors_request_reinforcement(client, db_session):
    mission = await _seeded_mission(db_session, 2)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission_1 = await _seeded_mission(db_session, 1)
    if mission_1:
        db_session.add(
            UserMissionProgress(
                user_id=user.id,
                mission_id=mission_1.id,
                status=MissionStatus.completed,
                score=100,
                score_percent=100,
                attempts=1,
            )
        )
        await db_session.flush()
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)
    detail = await client.get(f"/api/v1/journey/missions/{mission.id}", headers=headers)
    activities = [
        item
        for item in detail.json()["activities"]
        if item["activity_type"] in {"multiple_choice", "simulation"}
    ]

    pair = None
    for index, first_item in enumerate(activities):
        first_codes = set(first_item["content"].get("competency_codes") or [])
        for second_item in activities[index + 1:]:
            second_codes = set(second_item["content"].get("competency_codes") or [])
            if "1.2.2" in (first_codes & second_codes):
                pair = (first_item, second_item)
                break
        if pair:
            break
    if not pair:
        import pytest

        pytest.skip("Não há duas atividades objetivas da competência 1.2.2.")

    rows = await db_session.execute(
        select(Activity).where(Activity.id.in_([pair[0]["id"], pair[1]["id"]]))
    )
    by_id = {activity.id: activity for activity in rows.scalars().all()}

    for item in pair:
        stored = by_id[item["id"]]
        correct = stored.content.get("correct_answer")
        wrong = next(
            option["value"]
            for option in stored.content.get("options", [])
            if str(option["value"]) != str(correct)
        )
        response = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": item["id"],
                "response_data": {"selected_option": wrong},
            },
            headers=headers,
        )
        assert response.status_code == 200, response.text

    summary = await client.get("/api/v1/progress/summary", headers=headers)
    competency = next(
        c for c in summary.json()["competencies"] if c["code"] == "1.2.2"
    )
    assert competency["incorrect_count"] >= 2
    assert competency["reinforcement_suggested"] is True
