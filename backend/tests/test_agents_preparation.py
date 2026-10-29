from sqlalchemy import select

from app.modules.agents import analyst, catalyst
from app.modules.progress.service import PHASE_ACHIEVEMENT_KEYS
from app.shared.models import Activity, Mission, MissionStatus, Phase, UserMissionProgress
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
    # D-C4: phase_order nunca muda — sempre [1..12]. O que varia é trail_modes.
    # O Catalisador conduz onboarding (com fallback determinístico quando
    # ORCHESTRATE_ENABLED=false) e produz trail_modes + trail_1_auto_concluded.
    mission_1 = await _mission(db_session, 1, 1)
    mission_2 = await _mission(db_session, 2, 1)
    if not mission_1 or not mission_2:
        import pytest

        pytest.skip("Conteúdo das trilhas 1 e 2 não aplicado neste banco (migration 0015 necessária).")

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
    # D-C4: A ordem das 12 trilhas NUNCA muda.
    assert trail["phase_order"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert trail["phases"][0]["number"] == 1
    # D-C5: life_context=ja_trabalho → Trilha 1 auto-concluída.
    assert trail["trail_1_auto_concluded"] is True
    # trail_modes contém todos os 12 modos.
    assert "trail_modes" in trail
    assert set(trail["trail_modes"].keys()) == {str(i) for i in range(1, 13)}
    # Fallback determinístico quando ORCHESTRATE_ENABLED=false.
    assert trail["source"] in {"fallback", "ai"}

    trail_response = await client.get("/api/v1/users/me/trail", headers=headers)
    assert trail_response.status_code == 200
    assert trail_response.json()["phase_order"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    me = await client.get("/api/v1/users/me", headers=headers)
    assert me.json()["profile"]["trail"]["phases"][0]["number"] == 1

    overview = await client.get("/api/v1/journey/overview", headers=headers)
    assert overview.status_code == 200
    data = overview.json()
    assert data["trail"]["phase_order"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert data["phases"][0]["phase"]["number"] == 1
    assert data["phases"][0]["is_unlocked"] is True
    assert data["phases"][1]["phase"]["number"] == 2
    assert data["phases"][1]["is_unlocked"] is False
    assert data["recommendation"]["mission_id"] == mission_1.id
    assert data["recommendation"]["trail_position"] == 1

    # A segunda trilha só abre após concluir todas as missões obrigatórias da primeira.
    user_id = await _user_id(client, headers)
    required = await db_session.execute(
        select(Mission).where(Mission.phase_id == mission_1.phase_id, Mission.is_required == True)
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
    assert phases[1]["phase"]["number"] == 2
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

    # Seam para trilha gerada por IA: o backend valida antes de persistir,
    # persiste trail_modes e rejeita qualquer ordem incompleta.
    ai_trail = await catalyst.apply_generated_trail(
        db_session,
        user_id,
        {
            "phase_order": [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "trail_modes": {"1": "express", "2": "standard", "3": "standard",
                            "4": "standard", "5": "standard", "6": "standard",
                            "7": "standard", "8": "standard", "9": "standard",
                            "10": "standard", "11": "standard", "12": "standard"},
            "trail_1_auto_concluded": True,
            "rationale": "Trilha sugerida pelo agente para o seu momento.",
            "focus_areas": ["Meios de pagamento"],
            "pace": "steady",
        },
    )
    assert ai_trail["source"] == "ai"
    assert ai_trail["phase_order"] == [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert ai_trail["trail_modes"]["1"] == "express"
    assert ai_trail["trail_1_auto_concluded"] is True

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
    mission = await _mission(db_session, 1, 2)
    if not mission:
        import pytest

        pytest.skip("Conteúdo da Fase 1 não aplicado neste banco.")

    user, tokens = await register_verified_user(client, db_session)
    headers = auth_headers(tokens)
    mission_1 = await _mission(db_session, 1, 1)
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
    if len(activities) < 2:
        import pytest

        pytest.skip("Missão não tem duas atividades objetivas no conjunto ativo.")

    # Escolhe duas atividades que compartilham uma competência para que o
    # segundo erro já sinalize reforço pela regra de 2 atividades distintas.
    pair = None
    for index, first_item in enumerate(activities):
        first_codes = set(first_item["content"].get("competency_codes") or [])
        for second_item in activities[index + 1:]:
            second_codes = set(second_item["content"].get("competency_codes") or [])
            if first_codes & second_codes:
                pair = (first_item, second_item)
                break
        if pair:
            break
    if not pair:
        import pytest

        pytest.skip("Não há duas atividades objetivas da mesma competência.")

    rows = await db_session.execute(
        select(Activity).where(Activity.id.in_([pair[0]["id"], pair[1]["id"]]))
    )
    by_id = {activity.id: activity for activity in rows.scalars().all()}

    last = None
    for index, item in enumerate(pair):
        stored = by_id[item["id"]]
        correct = stored.content.get("correct_answer")
        wrong = next(
            option["value"]
            for option in stored.content.get("options", [])
            if str(option["value"]) != str(correct)
        )
        last = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": item["id"],
                "response_data": {"selected_option": wrong},
            },
            headers=headers,
        )
        assert last.status_code == 200, last.text
        if index == 0:
            assert last.json()["feedback_agent"] == "mentor"
            assert last.json()["reinforcement"] is None

    assert last is not None
    assert last.json()["feedback_agent"] == "analyst"
    assert last.json()["reinforcement"]["action"] == "review"
    assert last.json()["reinforcement"]["message"]


async def test_celebrate_trail_completion_fallback_keeps_message_contract():
    # Mesmo com o Orchestrate desligado, o contrato de celebração precisa ter
    # `message` (usado pela UI) além dos campos específicos de celebração.
    result = await catalyst.celebrate_trail_completion(
        None, 1, 1, "Meu primeiro salário"
    )
    assert result["kind"] == "celebrate"
    assert result["message"]
    assert result["celebration_message"]
    assert result["badge_label"]
    assert result["source"] == "fallback"


async def test_trail_synthesis_is_persisted_and_read_from_cache(client, db_session):
    phase = (
        await db_session.execute(select(Phase).where(Phase.number == 1))
    ).scalar_one_or_none()
    if not phase:
        import pytest

        pytest.skip("Trilha 1 não aplicada neste banco.")

    _, tokens = await register_verified_user(client, db_session)
    user_id = await _user_id(client, auth_headers(tokens))

    synthesis = analyst.TrailSynthesis(
        short="Você demonstrou o básico do contracheque.",
        full=analyst.TrailSynthesisFull(
            competencies_demonstrated=["1.1.1"],
            competencies_with_difficulty=[],
            summary="Síntese de teste.",
            reinforcement_suggestion=None,
        ),
        source="ai",
    )
    await analyst.save_trail_synthesis(db_session, user_id, phase.id, synthesis)
    cached = await analyst.get_cached_trail_synthesis(db_session, user_id, phase.id)

    assert cached is not None
    assert cached.short == synthesis.short
    assert cached.source == "ai"
    assert cached.full.competencies_demonstrated == ["1.1.1"]


def test_fallback_recommendation_surfaces_trail_1_review_signal():
    result = catalyst._fallback_recommendation(
        trail=None,
        mission_name="Orçamento na prática",
        mission_id=5,
        phase_number=2,
        phase_name="Orçamento na prática",
        is_in_progress=False,
        has_mission=True,
        reinforcement_topics=[],
        trail_position=2,
        trail_size=12,
        analyst_signals=[{"tipo": "trail_1_review"}],
    )
    assert result["kind"] == "trail_1_review"
    assert "Trilha 1" in result["message"]


async def test_adaptive_questions_endpoint_returns_structured_fallback(
    client, db_session
):
    _, tokens = await register_verified_user(client, db_session)
    response = await client.post(
        "/api/v1/users/me/onboarding/adaptive-questions",
        headers=auth_headers(tokens),
        json={
            "fixed_answers": {
                "goal_category": "dividas",
                "goal_12m": "Guardar R$ 5.000",
                "main_difficulty": "cartão de crédito",
                "life_context": "ja_trabalho",
            },
            "conversation_history": [],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "fallback"
    assert 1 <= len(body["questions"]) <= 8
    assert all(isinstance(question, str) and question.strip() for question in body["questions"])
