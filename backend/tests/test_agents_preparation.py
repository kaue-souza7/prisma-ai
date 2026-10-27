from sqlalchemy import select

from app.modules.agents import analyst, catalyst
from app.modules.progress.service import PHASE_ACHIEVEMENT_KEYS
from app.shared.models import Mission, MissionStatus, Phase, UserMissionProgress
from tests.conftest import auth_headers, register_verified_user


def test_trail_rules_are_explicit_and_goal_specific():
    # Após a reestruturação de 12 trilhas, os phase_order passam a ter 12 elementos.
    debt = catalyst.build_trail(
        personal_goal="Sair das dívidas",
        goal_category="dividas",
        knowledge_level="intermediate",
    )
    assert debt["phase_order"] == [7, 8, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]
    assert "juros" in debt["rationale"].lower()

    reserve = catalyst.build_trail(
        personal_goal="Criar uma reserva",
        goal_category="reserva",
        knowledge_level="beginner",
    )
    assert reserve["phase_order"] == [5, 6, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12]
    assert reserve["pace"] == "supported"

    advanced = catalyst.build_trail(
        personal_goal="Aprender a investir",
        goal_category="investimentos",
        knowledge_level="advanced",
    )
    assert advanced["phase_order"] == [5, 6, 7, 9, 10, 1, 2, 3, 4, 8, 11, 12]
    assert advanced["pace"] == "accelerated"
    # Trilha 12 (Desafio integrador) deve ser sempre a última
    assert advanced["phase_order"][-1] == 12


def test_trail_validation_rejects_incomplete_or_duplicated_orders():
    assert catalyst.validate_phase_order(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    ) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # Ordens incompletas (6 elementos onde são esperados 12 no DEFAULT) são aceitas
    # somente se passarem um available_numbers explícito compatível.
    assert catalyst.validate_phase_order(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        available_numbers={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
    ) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert catalyst.validate_phase_order([1, 2, 3, 4, 5]) is None
    assert catalyst.validate_phase_order([1, 2, 3, 4, 5, 5]) is None
    assert catalyst.validate_phase_order([1, 2, 3, 4, 5, 9]) is None
    assert catalyst.validate_phase_order("1,2,3,4,5,6") is None


def test_phase_achievement_keys_match_seeded_achievements():
    assert PHASE_ACHIEVEMENT_KEYS[1] == "planejador_iniciante"
    assert PHASE_ACHIEVEMENT_KEYS[2] == "digital_consciente"
    assert PHASE_ACHIEVEMENT_KEYS[6] == "fase_6_concluida"


def test_analyst_builds_short_actionable_recommendations():
    insight = analyst.build_insight_from_competencies([
        {
            "name": "Distinguir salário bruto de líquido",
            "status": "developing",
            "reinforcement_suggested": True,
        }
    ])
    assert insight is not None
    assert insight["severity"] == "attention"
    assert insight["action"] == "review"
    assert "revisar" in insight["message"]

    positive = analyst.build_insight_from_competencies([
        {
            "name": "Distinguir salário bruto de líquido",
            "status": "demonstrated",
            "reinforcement_suggested": False,
        }
    ])
    assert positive is not None
    assert positive["severity"] == "positive"


async def _mission(db_session, phase_number: int, mission_number: int) -> Mission | None:
    result = await db_session.execute(
        select(Mission)
        .join(Phase, Mission.phase_id == Phase.id)
        .where(Phase.number == phase_number, Mission.number == mission_number)
    )
    return result.scalar_one_or_none()


async def _user_id(client, headers) -> int:
    response = await client.get("/api/v1/users/me", headers=headers)
    return response.json()["user"]["id"]


async def test_onboarding_generates_a_personalized_trail_and_orders_the_journey(
    client, db_session
):
    # Após a reestruturação para 12 trilhas, a categoria "dividas" inicia por
    # trilhas 7 (Juros e parcelas) e 8 (Dívida que cresce). O skip ocorre se
    # as trilhas 1 e 7 não estiverem no banco — o que é normal em ambientes
    # onde a migration 0015 ainda não foi aplicada.
    mission_7 = await _mission(db_session, 7, 1)
    mission_1 = await _mission(db_session, 1, 1)
    if not mission_7 or not mission_1:
        import pytest

        pytest.skip("Conteúdo das trilhas 1 e 7 não aplicado neste banco (migration 0015 necessária).")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    response = await client.post(
        "/api/v1/users/me/onboarding",
        json={
            "personal_goal": "Sair das dívidas",
            "knowledge_level": "intermediate",
            "consent_version": "2026-10-21",
            "preferences": {"goal_category": "dividas"},
            "life_context": "ja_trabalho",
            "urgency": "agora_preciso",
        },
        headers=headers,
    )
    assert response.status_code == 200
    trail = response.json()["trail"]
    assert trail["phase_order"] == [7, 8, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]
    assert trail["phases"][0]["number"] == 7
    assert trail["source"] == "rules"

    trail_response = await client.get("/api/v1/users/me/trail", headers=headers)
    assert trail_response.status_code == 200
    assert trail_response.json()["phase_order"] == [7, 8, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]

    me = await client.get("/api/v1/users/me", headers=headers)
    assert me.json()["profile"]["trail"]["phases"][0]["number"] == 7

    overview = await client.get("/api/v1/journey/overview", headers=headers)
    assert overview.status_code == 200
    data = overview.json()
    assert data["trail"]["phase_order"] == [7, 8, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]
    assert data["phases"][0]["phase"]["number"] == 7
    assert data["phases"][0]["is_unlocked"] is True
    assert data["phases"][1]["phase"]["number"] == 8
    assert data["phases"][1]["is_unlocked"] is False
    assert data["recommendation"]["mission_id"] == mission_7.id
    assert data["recommendation"]["trail_position"] == 1

    # A segunda trilha só abre após concluir a primeira.
    user_id = await _user_id(client, headers)
    required = await db_session.execute(
        select(Mission).where(Mission.phase_id == mission_7.phase_id, Mission.is_required == True)
    )
    for mission in required.scalars().all():
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

    unlocked = await client.get("/api/v1/journey/overview", headers=headers)
    phases = unlocked.json()["phases"]
    assert phases[0]["status"] == "completed"
    assert phases[1]["phase"]["number"] == 8
    assert phases[1]["is_unlocked"] is True

    standard = await client.post(
        "/api/v1/users/me/trail/preference",
        json={"mode": "standard"},
        headers=headers,
    )
    assert standard.status_code == 200
    assert standard.json()["phase_order"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    standard_overview = await client.get("/api/v1/journey/overview", headers=headers)
    assert standard_overview.json()["phases"][0]["phase"]["number"] == 1

    # Seam para a futura trilha gerada por IA: o backend valida antes de
    # persistir e rejeita qualquer ordem incompleta.
    ai_trail = await catalyst.apply_generated_trail(
        db_session,
        user_id,
        {
            "phase_order": [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "rationale": "Trilha sugerida pelo agente para o seu momento.",
            "focus_areas": ["Meios de pagamento"],
            "pace": "steady",
        },
    )
    assert ai_trail["source"] == "ai"
    assert ai_trail["phase_order"] == [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    try:
        await catalyst.apply_generated_trail(
            db_session, user_id, {"phase_order": [1, 2, 3]}
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Uma trilha incompleta deveria ser rejeitada.")


async def test_mentor_chat_persists_context_and_returns_honest_fallback(client, db_session):
    mission = await _mission(db_session, 1, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)

    context = await client.get(
        f"/api/v1/conversations/mentor/context?mission_id={mission.id}",
        headers=headers,
    )
    assert context.status_code == 200
    assert context.json()["mission_name"] == mission.name
    assert context.json()["status"] == "preparing"
    assert context.json()["suggestions"]

    reply = await client.post(
        "/api/v1/conversations/mentor",
        json={"content": "Por que o salário líquido é menor?", "mission_id": mission.id},
        headers=headers,
    )
    assert reply.status_code == 200
    assert reply.json()["status"] == "preparing"
    assert reply.json()["source"] == "fallback"
    assert "preparação" in reply.json()["content"].lower()

    history = await client.get("/api/v1/conversations/mentor/history", headers=headers)
    assert history.status_code == 200
    conversation = next(item for item in history.json() if item["mission_id"] == mission.id)
    assert conversation["messages"][0]["role"] == "user"
    assert conversation["messages"][1]["role"] == "assistant"


async def test_repeated_error_returns_analyst_reinforcement(client, db_session):
    mission = await _mission(db_session, 1, 1)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    detail = await client.get(f"/api/v1/journey/missions/{mission.id}", headers=headers)
    activity = next(
        item for item in detail.json()["activities"] if item["activity_type"] == "multiple_choice"
    )
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)

    first = await client.post(
        f"/api/v1/journey/missions/{mission.id}/submit",
        json={"activity_id": activity["id"], "response_data": {"selected_option": "a"}},
        headers=headers,
    )
    assert first.json()["feedback_agent"] == "mentor"
    assert first.json()["reinforcement"] is None

    third = first
    for _ in range(2):
        retry = await client.post(
            f"/api/v1/journey/missions/{mission.id}/retry",
            json={"voluntary": False},
            headers=headers,
        )
        assert retry.status_code == 200
        third = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={"activity_id": activity["id"], "response_data": {"selected_option": "a"}},
            headers=headers,
        )
    assert third.json()["feedback_agent"] == "analyst"
    assert third.json()["reinforcement"]["action"] == "review"
    assert third.json()["reinforcement"]["message"]
