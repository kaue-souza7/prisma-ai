"""Testes de rotação de conjuntos de perguntas (D-Q1).

Cobre os 6 cenários obrigatórios da tabela em
docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md seção 5.4:

 1. 1ª tentativa — conjunto sorteado aleatoriamente entre os 3.
 2. 2ª tentativa — conjunto diferente do usado na 1ª.
 3. 3ª tentativa — conjunto diferente dos usados na 1ª e 2ª.
 4. 4ª tentativa — qualquer conjunto (repetição permitida).
 5. Duas tentativas com mesmo conjunto nas 3 primeiras — nunca deve ocorrer.
 6. Ordem das perguntas entre tentativas do mesmo conjunto — deve variar.
"""

from sqlalchemy import select

from app.modules.journey.service import (
    _get_used_sets,
    _select_set,
    get_active_activities_for_attempt,
    get_current_attempt_set,
)
from app.shared.models import Activity, Mission, Phase, UserMissionAttempt
from tests.conftest import auth_headers, register_verified_user


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────


async def _make_phase(db_session) -> Phase:
    phase = Phase(
        number=98,
        name="Fase rotação",
        description="Criada apenas nos testes de rotação.",
        order=0,
        is_active=True,
    )
    db_session.add(phase)
    await db_session.flush()
    return phase


async def _make_mission_with_sets(
    db_session,
    phase: Phase,
    *,
    number: int,
    num_sets: int = 3,
    activities_per_set: int = 2,
) -> tuple[Mission, list[Activity]]:
    """Cria uma missão com `num_sets` conjuntos de `activities_per_set` atividades cada."""
    mission = Mission(
        phase_id=phase.id,
        number=number,
        name=f"Módulo rotação {number}",
        description="Criado apenas nos testes de rotação.",
        order=number,
        is_required=False,
        passing_score=70,
    )
    db_session.add(mission)
    await db_session.flush()

    all_activities: list[Activity] = []
    for q_set in range(1, num_sets + 1):
        for order in range(1, activities_per_set + 1):
            activity = Activity(
                mission_id=mission.id,
                order=order,
                activity_type="multiple_choice",
                question_set=q_set,
                content={
                    "prompt": f"Questão conjunto {q_set} ordem {order}",
                    "options": [
                        {"value": "a", "label": "Incorreta"},
                        {"value": "b", "label": "Correta"},
                    ],
                    "correct_answer": "b",
                    "feedback_correct": "Certo!",
                    "feedback_incorrect": "Errado.",
                },
                points_value=10,
                is_active=True,
            )
            db_session.add(activity)
            all_activities.append(activity)

    await db_session.flush()
    return mission, all_activities


async def _get_user_id(client, headers) -> int:
    response = await client.get("/api/v1/users/me", headers=headers)
    return response.json()["user"]["id"]


# ─────────────────────────────────────────────
# Testes unitários de _select_set (sem banco)
# ─────────────────────────────────────────────


def test_select_set_first_attempt_picks_from_all():
    """1ª tentativa (used=[]) — pool é [1,2,3]."""
    available = [1, 2, 3]
    results = {_select_set([], available) for _ in range(50)}
    assert results.issubset({1, 2, 3})


def test_select_set_second_attempt_avoids_used():
    """2ª tentativa — nunca repete o conjunto da 1ª."""
    available = [1, 2, 3]
    for first_set in available:
        for _ in range(30):
            chosen = _select_set([first_set], available)
            assert chosen != first_set, (
                f"2ª tentativa escolheu {chosen}, mas {first_set} já foi usado."
            )


def test_select_set_third_attempt_avoids_both_used():
    """3ª tentativa — usa o único conjunto restante."""
    available = [1, 2, 3]
    for a in available:
        for b in available:
            if a == b:
                continue
            remaining = [s for s in available if s not in (a, b)]
            for _ in range(20):
                chosen = _select_set([a, b], available)
                assert chosen in remaining, (
                    f"3ª tentativa escolheu {chosen}, mas restava {remaining}."
                )


def test_select_set_fourth_attempt_allows_any():
    """4ª tentativa (len(used) >= 3) — qualquer conjunto é válido."""
    available = [1, 2, 3]
    results = {_select_set([1, 2, 3], available) for _ in range(50)}
    assert results.issubset({1, 2, 3})


def test_select_set_no_duplicate_in_first_three():
    """Cenário 5: em 100 sequências de 3 tentativas, nunca há duplicata."""
    available = [1, 2, 3]
    for _ in range(100):
        used: list[int] = []
        for _ in range(3):
            chosen = _select_set(used, available)
            assert chosen not in used, (
                f"Duplicata detectada: escolheu {chosen} com used={used}."
            )
            used.append(chosen)
        assert sorted(used) == [1, 2, 3]


def test_select_set_fallback_when_only_one_available():
    """Fallback: se só existe um conjunto possível, usa ele."""
    available = [1]
    result = _select_set([], available)
    assert result == 1


# ─────────────────────────────────────────────
# Testes de integração via HTTP (banco real, FK satisfeita)
# ─────────────────────────────────────────────


async def test_first_attempt_registers_attempt_record(client, db_session):
    """Cenário 1: 1ª tentativa (POST /start) cria registro em user_mission_attempts."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, _ = await _make_mission_with_sets(db_session, phase, number=1)

    resp = await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    assert resp.status_code == 200, resp.text

    result = await db_session.execute(
        select(UserMissionAttempt).where(
            UserMissionAttempt.user_id == user_id,
            UserMissionAttempt.mission_id == mission.id,
        )
    )
    attempts = result.scalars().all()
    assert len(attempts) == 1
    assert attempts[0].attempt_number == 1
    assert attempts[0].question_set_used in {1, 2, 3}


async def test_second_attempt_uses_different_set(client, db_session):
    """Cenário 2: 2ª tentativa (POST /retry) usa conjunto diferente do da 1ª."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(db_session, phase, number=2)

    # Inicia a 1ª tentativa
    await client.post(f"/api/v1/journey/missions/{mission.id}/start", headers=headers)

    first_set = await get_current_attempt_set(db_session, user_id, mission.id)

    # Responde todas as atividades do conjunto para poder pedir retry
    qs1_activities = [a for a in activities if a.question_set == first_set]
    for act in qs1_activities:
        await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={"activity_id": act.id, "response_data": {"selected_option": "a"}},
            headers=headers,
        )

    # Retry obrigatório (falhou)
    retry_resp = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    assert retry_resp.status_code == 200, retry_resp.text

    second_set = await get_current_attempt_set(db_session, user_id, mission.id)
    assert second_set != first_set, (
        f"2ª tentativa usou o mesmo conjunto {second_set} da 1ª."
    )


async def test_third_attempt_covers_all_three_sets(client, db_session):
    """Cenário 3: as 3 primeiras tentativas cobrem todos os 3 conjuntos."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(db_session, phase, number=3)

    for attempt_num in range(3):
        if attempt_num == 0:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/start", headers=headers
            )
        else:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/retry",
                json={"voluntary": False},
                headers=headers,
            )

        current_set = await get_current_attempt_set(db_session, user_id, mission.id)
        qs_activities = [a for a in activities if a.question_set == current_set]
        for act in qs_activities:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/submit",
                json={"activity_id": act.id, "response_data": {"selected_option": "a"}},
                headers=headers,
            )

    used = await _get_used_sets(db_session, user_id, mission.id)
    assert sorted(used) == [1, 2, 3], (
        f"Após 3 tentativas os conjuntos usados foram {sorted(used)}, esperado [1,2,3]."
    )


async def test_fourth_attempt_allows_any_set(client, db_session):
    """Cenário 4: 4ª tentativa pode repetir qualquer conjunto."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(db_session, phase, number=4)

    # 3 tentativas para cobrir todos os conjuntos
    for attempt_num in range(3):
        if attempt_num == 0:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/start", headers=headers
            )
        else:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/retry",
                json={"voluntary": False},
                headers=headers,
            )

        current_set = await get_current_attempt_set(db_session, user_id, mission.id)
        qs_activities = [a for a in activities if a.question_set == current_set]
        for act in qs_activities:
            await client.post(
                f"/api/v1/journey/missions/{mission.id}/submit",
                json={"activity_id": act.id, "response_data": {"selected_option": "a"}},
                headers=headers,
            )

    # 4ª tentativa — qualquer conjunto é válido
    retry_resp = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    assert retry_resp.status_code == 200, retry_resp.text

    used = await _get_used_sets(db_session, user_id, mission.id)
    assert len(used) == 4
    assert used[3] in {1, 2, 3}


async def test_activity_order_is_randomized_across_calls(client, db_session):
    """Cenário 6: a ordem das atividades varia entre chamadas para o mesmo conjunto.

    Usa um conjunto único com muitas atividades e verifica que em 20 chamadas
    ao menos uma diferença de ordem ocorre — confirma que random.shuffle() está ativo.
    """
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    user_id = await _get_user_id(client, auth_headers(tokens))

    phase = await _make_phase(db_session)
    mission, _ = await _make_mission_with_sets(
        db_session, phase, number=5, num_sets=1, activities_per_set=6
    )

    orders_seen: set[tuple[int, ...]] = set()
    for _ in range(20):
        activities = await get_active_activities_for_attempt(
            db_session, user_id, mission.id
        )
        order_tuple = tuple(a.order for a in activities)
        orders_seen.add(order_tuple)

    assert len(orders_seen) > 1, (
        "A ordem das atividades nunca variou em 20 chamadas — "
        "random.shuffle pode não estar funcionando."
    )


async def test_fallback_single_set_mission_no_attempt_record(client, db_session):
    """Missões com apenas question_set=1 retornam esse conjunto sem criar tentativa."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, _ = await _make_mission_with_sets(
        db_session, phase, number=6, num_sets=1, activities_per_set=2
    )

    # start_mission chama get_active_activities_for_attempt internamente
    resp = await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    assert resp.status_code == 200, resp.text

    # Para conjunto único: fallback não cria registro de tentativa
    used = await _get_used_sets(db_session, user_id, mission.id)
    assert used == [], (
        "Fallback de conjunto único não deve registrar tentativa em user_mission_attempts."
    )

    # O GET deve ainda mostrar as atividades (fallback para set=1)
    detail_resp = await client.get(
        f"/api/v1/journey/missions/{mission.id}", headers=headers
    )
    assert detail_resp.status_code == 200
    assert len(detail_resp.json()["activities"]) == 2


async def test_get_current_attempt_set_fallback_no_attempts(client, db_session):
    """Sem tentativa registrada, get_current_attempt_set retorna 1."""
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, _ = await _make_mission_with_sets(db_session, phase, number=7)

    current = await get_current_attempt_set(db_session, user_id, mission.id)
    assert current == 1


async def test_express_mode_keeps_only_essential_activities(client, db_session):
    """Modo express: filtra atividades que não tocam competências essenciais."""
    from app.shared.models import Competency

    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(
        db_session, phase, number=3, num_sets=1, activities_per_set=2
    )

    activities[0].content = {
        **activities[0].content,
        "competency_codes": ["E.1"],
    }
    activities[1].content = {
        **activities[1].content,
        "competency_codes": ["N.1"],
    }
    db_session.add(
        Competency(
            mission_id=mission.id,
            code="E.1",
            name="Competência essencial",
            description="Teste",
            is_essential=True,
        )
    )
    db_session.add(
        Competency(
            mission_id=mission.id,
            code="N.1",
            name="Competência não essencial",
            description="Teste",
            is_essential=False,
        )
    )
    await db_session.flush()

    selected = await get_active_activities_for_attempt(
        db_session, user_id, mission.id, trail_mode="express"
    )
    assert [activity.id for activity in selected] == [activities[0].id]


async def test_lesson_serves_activities_from_current_attempt_set(client, db_session):
    """O módulo deve exibir as perguntas do conjunto sorteado para a tentativa.

    Regressão: o fluxo da lição usa `activity_order` e, quando havia três
    conjuntos com a mesma ordem, o backend servia perguntas de outro conjunto.
    O estudante respondia tudo o que via, mas a tentativa nunca fechava e o
    botão "Refazer módulo" não aparecia.
    """
    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(
        db_session, phase, number=8, activities_per_set=3
    )
    mission.lesson_flow = [
        {"type": "question", "activity_order": order}
        for order in range(1, 4)
    ]
    await db_session.flush()

    started = await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    assert started.status_code == 200, started.text

    current_set = await get_current_attempt_set(db_session, user_id, mission.id)
    expected_ids = {
        activity.id for activity in activities if activity.question_set == current_set
    }

    lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    served_ids = {
        step["activity"]["id"]
        for step in lesson["steps"]
        if step["activity"] is not None
    }
    assert served_ids == expected_ids, (
        f"Tentativa usa o conjunto {current_set}, mas a lição exibiu "
        f"atividades de outro conjunto: {served_ids} != {expected_ids}."
    )

    last_result = None
    for step in lesson["steps"]:
        if step["activity"] is None:
            continue
        answer = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": step["activity"]["id"],
                "response_data": {"selected_option": "a"},
            },
            headers=headers,
        )
        assert answer.status_code == 200, answer.text
        last_result = answer.json()

    assert last_result is not None
    assert last_result["attempt_finished"] is True
    assert last_result["passed"] is False
    assert last_result["must_retry"] is True, (
        "Ao terminar a tentativa com erro, o backend deve exigir nova tentativa."
    )

    retry = await client.post(
        f"/api/v1/journey/missions/{mission.id}/retry",
        json={"voluntary": False},
        headers=headers,
    )
    assert retry.status_code == 200, retry.text

    second_set = await get_current_attempt_set(db_session, user_id, mission.id)
    assert second_set != current_set
    second_expected_ids = {
        activity.id for activity in activities if activity.question_set == second_set
    }
    second_lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    second_served_ids = {
        step["activity"]["id"]
        for step in second_lesson["steps"]
        if step["activity"] is not None
    }
    assert second_served_ids == second_expected_ids


async def test_fallback_lesson_serves_only_current_attempt_set(client, db_session):
    """Missões sem `lesson_flow` também não podem misturar conjuntos."""
    from app.shared.models import UserMissionAttempt

    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(
        db_session, phase, number=9, activities_per_set=2
    )

    # Fixa o conjunto da tentativa para não depender do sorteio.
    db_session.add(
        UserMissionAttempt(
            user_id=user_id,
            mission_id=mission.id,
            attempt_number=1,
            question_set_used=2,
        )
    )
    await db_session.flush()

    lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()
    served_ids = [
        step["activity"]["id"]
        for step in lesson["steps"]
        if step["activity"] is not None
    ]
    expected_ids = {
        activity.id for activity in activities if activity.question_set == 2
    }
    assert set(served_ids) == expected_ids
    assert len(served_ids) == len(expected_ids), (
        "O fluxo de fallback não deve repetir a mesma atividade de outro conjunto."
    )


async def test_lesson_repairs_progress_stuck_on_summary_with_pending_questions(
    client, db_session
):
    """Dados antigos presos no resumo devem voltar para a pergunta pendente.

    Reproduz o estado deixado pela mistura de conjuntos: o estudante respondeu
    perguntas de outro conjunto, o cursor chegou ao resumo, mas a tentativa
    atual ainda tem atividades sem resposta.
    """
    from datetime import datetime, timezone

    from app.shared.models import MissionStatus, UserMissionProgress, UserResponse

    _, tokens = await register_verified_user(client, db_session, password="Senha123")
    headers = auth_headers(tokens)
    user_id = await _get_user_id(client, headers)

    phase = await _make_phase(db_session)
    mission, activities = await _make_mission_with_sets(
        db_session, phase, number=10, activities_per_set=3
    )
    mission.lesson_flow = [
        *[
            {"type": "question", "activity_order": order}
            for order in range(1, 4)
        ],
        {"type": "summary", "title": "Resumo", "body": "Fim do módulo."},
    ]
    await db_session.flush()

    started = await client.post(
        f"/api/v1/journey/missions/{mission.id}/start", headers=headers
    )
    assert started.status_code == 200, started.text

    current_set = await get_current_attempt_set(db_session, user_id, mission.id)
    wrong_set = next(value for value in {1, 2, 3} if value != current_set)
    for activity in activities:
        if activity.question_set != wrong_set:
            continue
        db_session.add(
            UserResponse(
                user_id=user_id,
                mission_id=mission.id,
                activity_id=activity.id,
                response_data={"selected_option": "a"},
                is_correct=False,
                score=0,
                attempt_number=1,
                mission_attempt=1,
                created_at=datetime.now(timezone.utc),
            )
        )

    progress = (
        await db_session.execute(
            select(UserMissionProgress).where(
                UserMissionProgress.user_id == user_id,
                UserMissionProgress.mission_id == mission.id,
            )
        )
    ).scalar_one()
    progress.status = MissionStatus.in_progress
    progress.current_step = 3  # índice do resumo no lesson_flow
    progress.completed_steps = [0, 1, 2, 3]
    await db_session.flush()

    lesson = (
        await client.get(
            f"/api/v1/journey/missions/{mission.id}/lesson", headers=headers
        )
    ).json()

    assert lesson["current_step"] == 0, (
        "O estudante deve voltar para a primeira pergunta ainda sem resposta."
    )
    served_ids = {
        step["activity"]["id"]
        for step in lesson["steps"]
        if step["activity"] is not None
    }
    expected_ids = {
        activity.id for activity in activities if activity.question_set == current_set
    }
    assert served_ids == expected_ids
    assert not any(
        step["completed"] for step in lesson["steps"] if step["activity"] is not None
    ), "Perguntas não respondidas não podem aparecer como concluídas."

    last_result = None
    for step in lesson["steps"]:
        if step["activity"] is None:
            continue
        answer = await client.post(
            f"/api/v1/journey/missions/{mission.id}/submit",
            json={
                "activity_id": step["activity"]["id"],
                "response_data": {"selected_option": "a"},
            },
            headers=headers,
        )
        assert answer.status_code == 200, answer.text
        last_result = answer.json()

    assert last_result is not None
    assert last_result["attempt_finished"] is True
    assert last_result["must_retry"] is True
