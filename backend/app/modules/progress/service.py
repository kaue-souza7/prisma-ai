import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, or_, select

from app.core.config import settings
from app.core.logging import logger

from app.shared.models import (
    UserPoints, UserAchievement, Achievement, UserMissionProgress,
    UserResponse, MissionStatus, Mission, Phase,
    Activity, Competency, CompetencyStatus, UserCompetencyProgress,
)
from app.modules.agents import analyst

# ─────────────────────────────────────────────
# Regras de gamificação (D6)
# ─────────────────────────────────────────────

LEVEL_THRESHOLDS = {
    1: 0,
    2: 300,
    3: 700,
    4: 1200,
    5: 1800,
}

POINTS_FIRST_ATTEMPT = 100
POINTS_AFTER_REINFORCEMENT = 70
POINTS_ONBOARDING = 50

# Prismas: moeda do Estúdio.
COINS_CORRECT_ANSWER = 2
COINS_MODULE_PASS = 15
COINS_MODULE_EXCELLENCE = 25
COINS_PHASE_COMPLETION = 50
COINS_ONBOARDING = 20
COINS_STUDIO_EXERCISES_COMPLETION = 5

# Modelo de avaliação por módulo: 70% aprova, 90% indica excelência.
PASS_THRESHOLD = 70.0
EXCELLENCE_THRESHOLD = 90.0

REINFORCEMENT_THRESHOLD = 2  # erros na mesma competência para sugerir reforço

PHASE_ACHIEVEMENT_KEYS = {
    1: "planejador_iniciante",
    2: "digital_consciente",
    3: "fase_3_concluida",
    4: "fase_4_concluida",
    5: "fase_5_concluida",
    6: "fase_6_concluida",
    # Trilhas 7–12 (adicionadas na reestruturação de 12 trilhas — migration 0015)
    7: "trilha_juros",
    8: "trilha_divida",
    9: "trilha_inflacao",
    10: "trilha_rendimentos",
    11: "trilha_seguranca",
    12: "desafio_integrador",
}


def calculate_level(total_points: int) -> int:
    level = 1
    for lvl, threshold in sorted(LEVEL_THRESHOLDS.items(), reverse=True):
        if total_points >= threshold:
            level = lvl
            break
    return level


async def add_points(db: AsyncSession, user_id: int, points: int) -> UserPoints:
    result = await db.execute(select(UserPoints).where(UserPoints.user_id == user_id))
    user_points = result.scalar_one_or_none()

    if not user_points:
        user_points = UserPoints(
            user_id=user_id,
            total_points=0,
            level=1,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(user_points)

    user_points.total_points += points
    user_points.level = calculate_level(user_points.total_points)
    user_points.updated_at = datetime.now(timezone.utc)
    await db.flush()
    return user_points


async def get_coins(db: AsyncSession, user_id: int) -> int:
    """Retorna o saldo de Prismas do usuário (0 se ainda não houver registro)."""
    result = await db.execute(
        select(UserPoints.coins).where(UserPoints.user_id == user_id)
    )
    return result.scalar_one_or_none() or 0


async def add_coins(db: AsyncSession, user_id: int, amount: int) -> int:
    """Credita Prismas e devolve o novo saldo."""
    if amount < 0:
        raise ValueError("valor_invalido")

    result = await db.execute(
        select(UserPoints).where(UserPoints.user_id == user_id).with_for_update()
    )
    user_points = result.scalar_one_or_none()
    if not user_points:
        user_points = UserPoints(
            user_id=user_id,
            total_points=0,
            coins=0,
            level=1,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(user_points)
        await db.flush()

    user_points.coins = (user_points.coins or 0) + amount
    user_points.updated_at = datetime.now(timezone.utc)
    await db.flush()
    return user_points.coins


async def spend_coins(db: AsyncSession, user_id: int, amount: int) -> int:
    """Debita Prismas; levanta ValueError("saldo_insuficiente") se faltar saldo."""
    if amount < 0:
        raise ValueError("valor_invalido")

    result = await db.execute(
        select(UserPoints).where(UserPoints.user_id == user_id).with_for_update()
    )
    user_points = result.scalar_one_or_none()
    if not user_points or (user_points.coins or 0) < amount:
        raise ValueError("saldo_insuficiente")

    user_points.coins -= amount
    user_points.updated_at = datetime.now(timezone.utc)
    await db.flush()
    return user_points.coins


async def grant_achievement(db: AsyncSession, user_id: int, achievement_key: str) -> str | None:
    """Concede uma conquista ao usuário. Retorna o nome da conquista ou None se já possuída."""
    ach_result = await db.execute(
        select(Achievement).where(Achievement.key == achievement_key, Achievement.is_active == True)
    )
    achievement = ach_result.scalar_one_or_none()
    if not achievement:
        return None

    existing = await db.execute(
        select(UserAchievement).where(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement.id,
        )
    )
    if existing.scalar_one_or_none():
        return None  # Já possui

    db.add(UserAchievement(
        user_id=user_id,
        achievement_id=achievement.id,
        earned_at=datetime.now(timezone.utc),
    ))
    await db.flush()
    return achievement.name


async def grant_onboarding_bonus(db: AsyncSession, user_id: int) -> None:
    """Concede pontos, Prismas e conquista do onboarding."""
    await add_points(db, user_id, POINTS_ONBOARDING)
    await add_coins(db, user_id, COINS_ONBOARDING)
    await grant_achievement(db, user_id, "primeiro_passo")


async def grant_trail_1_auto_concluded_bonus(db: AsyncSession, user_id: int) -> None:
    """Concede 50 XP e achievement quando o Catalisador reconhece a Trilha 1 no onboarding.

    Idempotente: se o achievement já foi concedido, nenhum XP adicional é dado.
    Fonte: "catalyst_onboarding" — distingue da pontuação normal de missão.
    """
    # grant_achievement já é idempotente (retorna None se já possuído).
    already_granted = await grant_achievement(db, user_id, "trilha_1_dominada_onboarding")
    if already_granted is None:
        # já possuída — não duplicar pontos
        return
    await add_points(db, user_id, 50)


def calculate_mission_score(
    score_percent: float,
    attempt_number: int,
    *,
    already_awarded: bool = False,
) -> tuple[int, bool]:
    """Calcula a pontuação de uma tentativa concluída do módulo.

    - 100 pontos: excelência (>= 90%) na primeira tentativa.
    - 70 pontos: aprovação (>= 70%) em qualquer outra situação.
    - 0 pontos: reprovação ou módulo que já havia sido aprovado antes
      (refazer por vontade própria nunca duplica pontos).

    Retorna também se a tentativa é a primeira aprovação com excelência, usado
    para a conquista "Sem dúvidas".
    """
    if already_awarded or score_percent < PASS_THRESHOLD:
        return 0, False

    is_first_attempt = attempt_number == 1
    if is_first_attempt and score_percent >= EXCELLENCE_THRESHOLD:
        return POINTS_FIRST_ATTEMPT, True

    return POINTS_AFTER_REINFORCEMENT, False


def mission_has_passed(progress: UserMissionProgress | None) -> bool:
    """Indica se o módulo já foi aprovado alguma vez.

    `score` é preenchido somente quando o módulo é aprovado. Mantê-lo após um
    retry garante que refazer um módulo já aprovado não bloqueie novamente as
    próximas missões.
    """
    if not progress:
        return False
    if progress.score is not None:
        return True
    return progress.status == MissionStatus.completed and (
        progress.score_percent is None
        or progress.score_percent >= PASS_THRESHOLD
    )


def mission_passed_sql():
    """Condição SQL equivalente a `mission_has_passed`."""
    return or_(
        UserMissionProgress.score.is_not(None),
        and_(
            UserMissionProgress.status == MissionStatus.completed,
            or_(
                UserMissionProgress.score_percent.is_(None),
                UserMissionProgress.score_percent >= PASS_THRESHOLD,
            ),
        ),
    )


async def _apply_competency_evidence(
    db: AsyncSession,
    user_id: int,
    competencies: list[Competency],
    is_correct: bool | None,
) -> None:
    """Atualiza contadores e status para um conjunto de competências."""
    for competency in competencies:
        progress_result = await db.execute(
            select(UserCompetencyProgress).where(
                UserCompetencyProgress.user_id == user_id,
                UserCompetencyProgress.competency_id == competency.id,
            )
        )
        progress = progress_result.scalar_one_or_none()
        if not progress:
            progress = UserCompetencyProgress(
                user_id=user_id,
                competency_id=competency.id,
                status=CompetencyStatus.not_started,
                incorrect_count=0,
                correct_count=0,
                reinforcement_suggested=False,
                updated_at=datetime.now(timezone.utc),
            )
            db.add(progress)

        if is_correct is True:
            progress.correct_count += 1
        elif is_correct is False:
            progress.incorrect_count += 1

        progress.status = await _calculate_competency_status(
            db, user_id, competency, competency.mission_id
        )
        progress.reinforcement_suggested = (
            progress.status != CompetencyStatus.demonstrated
            and await _should_suggest_reinforcement(
                db, user_id, competency, competency.mission_id
            )
        )
        progress.updated_at = datetime.now(timezone.utc)

    await db.flush()


async def record_competency_evidence(
    db: AsyncSession,
    user_id: int,
    activity: Activity,
    is_correct: bool | None,
) -> None:
    """
    Registra a evidência de aprendizagem da atividade nas competências ligadas
    por `content.competency_codes`.

    O status e o sinal de reforço são recalculados a partir de todo o histórico,
    nunca a partir de uma única resposta. Respostas abertas registram evidência
    de participação, mas não contam como acerto/erro enquanto a avaliação por
    IA não estiver disponível.
    """
    codes = activity.content.get("competency_codes") or []
    if not codes:
        return

    result = await db.execute(
        select(Competency).where(
            Competency.mission_id == activity.mission_id,
            Competency.code.in_(codes),
        )
    )
    await _apply_competency_evidence(
        db, user_id, list(result.scalars().all()), is_correct
    )


async def record_studio_competency_evidence(
    db: AsyncSession,
    user_id: int,
    codes: list[str],
    is_correct: bool | None,
    *,
    phase_id: int | None = None,
    mission_id: int | None = None,
) -> None:
    """Evidência de Exercícios Extras, que não têm atividade no currículo.

    O vínculo é feito pelo código da competência. Quando a geração é de uma
    fase inteira, todas as competências daquela fase são consideradas; quando é
    de um módulo, apenas as competências daquele módulo.
    """
    if not codes:
        return

    query = select(Competency).where(Competency.code.in_(codes))
    if mission_id is not None:
        query = query.where(Competency.mission_id == mission_id)
    elif phase_id is not None:
        query = query.join(
            Mission, Competency.mission_id == Mission.id
        ).where(Mission.phase_id == phase_id)

    result = await db.execute(query)
    await _apply_competency_evidence(
        db, user_id, list(result.scalars().all()), is_correct
    )


async def _linked_activities(
    db: AsyncSession, competency_code: str, mission_id: int
) -> list[Activity]:
    result = await db.execute(
        select(Activity)
        .where(Activity.mission_id == mission_id, Activity.is_active == True)
        .order_by(Activity.order)
    )
    return [
        activity
        for activity in result.scalars().all()
        if competency_code in (activity.content.get("competency_codes") or [])
    ]


async def _calculate_competency_status(
    db: AsyncSession,
    user_id: int,
    competency: Competency,
    mission_id: int,
) -> CompetencyStatus:
    linked = await _linked_activities(db, competency.code, mission_id)
    if not linked:
        return CompetencyStatus.not_started

    # A rotação usa um conjunto por tentativa. A competência é considerada
    # demonstrada quando TODAS as atividades de PELO MENOS UM conjunto têm
    # evidência válida; não é necessário responder às três variantes.
    activities_by_set: dict[int, list[Activity]] = {}
    for activity in linked:
        activities_by_set.setdefault(activity.question_set, []).append(activity)

    has_any_response = False
    for activities in activities_by_set.values():
        all_evidence = True
        for activity in activities:
            query = select(UserResponse.id).where(
                UserResponse.user_id == user_id,
                UserResponse.activity_id == activity.id,
            )
            if activity.activity_type != "open_text":
                query = query.where(UserResponse.is_correct == True)

            response = (await db.execute(query.limit(1))).scalar_one_or_none()
            if response is None:
                all_evidence = False
            else:
                has_any_response = True
        if all_evidence:
            return CompetencyStatus.demonstrated

    if has_any_response:
        return CompetencyStatus.developing
    return CompetencyStatus.not_started


async def _should_suggest_reinforcement(
    db: AsyncSession,
    user_id: int,
    competency: Competency,
    mission_id: int,
) -> bool:
    """
    Regra determinística do MVP:

    - 2 atividades objetivas diferentes com erro na mesma competência; ou
    - 3 tentativas incorretas na mesma atividade, quando a competência tem
      apenas uma evidência objetiva disponível.

    A regra fica sujeita à validação de produto documentada em
    `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`.
    """
    linked = await _linked_activities(db, competency.code, mission_id)
    objective = [a for a in linked if a.activity_type != "open_text"]
    if not objective:
        return False

    objective_by_set: dict[int, list[Activity]] = {}
    for activity in objective:
        objective_by_set.setdefault(activity.question_set, []).append(activity)

    result = await db.execute(
        select(
            Activity.question_set,
            UserResponse.activity_id,
            func.count(UserResponse.id),
        )
        .join(Activity, UserResponse.activity_id == Activity.id)
        .where(
            UserResponse.user_id == user_id,
            UserResponse.activity_id.in_([a.id for a in objective]),
            UserResponse.is_correct == False,
        )
        .group_by(Activity.question_set, UserResponse.activity_id)
    )

    errors_by_set: dict[int, dict[int, int]] = {}
    for question_set, activity_id, count in result.all():
        errors_by_set.setdefault(question_set, {})[activity_id] = count

    for question_set, errors in errors_by_set.items():
        # 2 atividades objetivas diferentes do mesmo conjunto com erro.
        if len(errors) >= 2:
            return True
        # 3 erros na mesma atividade quando o conjunto só tem uma objetiva.
        activities_in_set = objective_by_set.get(question_set, [])
        if len(activities_in_set) == 1 and sum(errors.values()) >= 3:
            return True

    return False


async def apply_mission_completion(
    db: AsyncSession, user_id: int, mission_id: int
) -> dict:
    """Avalia a tentativa atual do módulo como um todo.

    A tentativa só termina quando todas as atividades ativas possuem resposta
    registrada. O percentual considera apenas as atividades objetivas; respostas
    abertas contam para a conclusão, mas não penalizam a nota. Abaixo de 70% o
    módulo continua em andamento e precisa ser refeito; a partir de 70% ele é
    aprovado e libera o próximo módulo.
    """
    from app.modules.journey.service import get_attempt_activities, get_mission_detail

    mission = await get_mission_detail(db, mission_id)
    required_activities = await get_attempt_activities(db, user_id, mission)

    prog_result = await db.execute(
        select(UserMissionProgress).where(
            UserMissionProgress.user_id == user_id,
            UserMissionProgress.mission_id == mission_id,
        )
    )
    prog = prog_result.scalar_one_or_none()
    current_attempt = max(prog.attempts or 0, 1) if prog else 1

    base_result = {
        "mission_completed": False,
        "attempt_finished": False,
        "points_earned": 0,
        "coins_earned": 0,
        "new_achievements": [],
        "score_percent": None,
        "passed": None,
        "must_retry": None,
        "can_retry_optionally": None,
    }
    if not required_activities:
        return base_result

    responses_result = await db.execute(
        select(UserResponse).where(
            UserResponse.user_id == user_id,
            UserResponse.mission_id == mission_id,
            UserResponse.mission_attempt == current_attempt,
        )
    )
    responses = responses_result.scalars().all()
    latest_by_activity: dict[int, UserResponse] = {}
    for response in responses:
        current = latest_by_activity.get(response.activity_id)
        if current is None or response.created_at > current.created_at:
            latest_by_activity[response.activity_id] = response

    # A tentativa só pode ser avaliada quando todas as atividades foram
    # respondidas. Como o backend bloqueia a segunda resposta por atividade,
    # isso equivale a "uma resposta por atividade nesta tentativa".
    if any(activity.id not in latest_by_activity for activity in required_activities):
        return base_result

    objective = [
        activity for activity in required_activities
        if activity.activity_type != "open_text"
    ]
    if objective:
        correct_count = sum(
            1
            for activity in objective
            if latest_by_activity[activity.id].is_correct is True
        )
        score_percent = round((correct_count / len(objective)) * 100, 2)
    else:
        # Módulo somente com respostas abertas: conclusão não é penalizada.
        score_percent = 100.0

    was_passed_before = mission_has_passed(prog)
    previous_percent = (
        prog.score_percent
        if prog and prog.score_percent is not None
        else (100.0 if was_passed_before else 0.0)
    )
    best_percent = max(score_percent, previous_percent)
    passed = was_passed_before or score_percent >= PASS_THRESHOLD
    must_retry = not passed
    can_retry_optionally = passed and best_percent >= EXCELLENCE_THRESHOLD

    now = datetime.now(timezone.utc)
    if not prog:
        prog = UserMissionProgress(
            user_id=user_id,
            mission_id=mission_id,
            status=MissionStatus.in_progress,
            attempts=1,
            current_step=0,
            completed_steps=[],
            started_at=now,
        )
        db.add(prog)
        await db.flush()

    points_earned = 0
    coins_earned = 0
    new_achievements: list[str] = []

    if passed:
        if not was_passed_before:
            points, is_first_excellent_attempt = calculate_mission_score(
                score_percent,
                current_attempt,
                already_awarded=False,
            )
            if points:
                prog.score = points
                await add_points(db, user_id, points)
                points_earned = points

            if is_first_excellent_attempt:
                name = await grant_achievement(db, user_id, "sem_duvidas")
                if name:
                    new_achievements.append(name)

            module_coins = (
                COINS_MODULE_EXCELLENCE
                if score_percent >= EXCELLENCE_THRESHOLD
                else COINS_MODULE_PASS
            )
            await add_coins(db, user_id, module_coins)
            coins_earned += module_coins

        prog.status = MissionStatus.completed
        prog.completed_at = prog.completed_at or now
        prog.score_percent = best_percent
    else:
        prog.status = MissionStatus.in_progress
        prog.score_percent = score_percent
        prog.completed_at = None

    prog.attempts = max(prog.attempts or 0, 1)
    prog.started_at = prog.started_at or now
    await db.flush()

    completed_phase = None
    if passed:
        # Novas evidências invalidam a síntese antiga da trilha.
        await analyst.invalidate_trail_synthesis(db, user_id, mission.phase_id)
        phase_achievement, phase_coins, completed_phase = await _check_phase_completion(
            db, user_id, mission.phase_id
        )
        if phase_achievement:
            new_achievements.append(phase_achievement)
        coins_earned += phase_coins

    return {
        "mission_completed": passed,
        "attempt_finished": True,
        "points_earned": points_earned,
        "coins_earned": coins_earned,
        "new_achievements": new_achievements,
        "score_percent": best_percent if passed else score_percent,
        "passed": passed,
        "must_retry": must_retry,
        "can_retry_optionally": can_retry_optionally,
        "completed_trail_id": completed_phase.id if completed_phase else None,
        "completed_trail_name": completed_phase.name if completed_phase else None,
    }


_SYNTHESIS_TASKS: set[asyncio.Task] = set()
_SYNTHESIS_INFLIGHT: set[tuple[int, int]] = set()


async def _run_synthesis_in_background(user_id: int, phase_id: int) -> None:
    """Gera a síntese com uma sessão própria, fora do request."""
    from app.core.database import AsyncSessionLocal

    try:
        async with AsyncSessionLocal() as session:
            await analyst.generate_trail_synthesis(
                session, user_id, phase_id, use_cache=False
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001 — background nunca derruba o fluxo
        logger.warning(
            "Síntese de trilha em background falhou user=%s trail=%s: %s",
            user_id,
            phase_id,
            exc.__class__.__name__,
        )
    finally:
        _SYNTHESIS_INFLIGHT.discard((user_id, phase_id))


def _spawn_trail_synthesis(user_id: int, phase_id: int) -> None:
    """Dispara a síntese uma única vez por usuário/trilha."""
    key = (user_id, phase_id)
    if key in _SYNTHESIS_INFLIGHT:
        return
    _SYNTHESIS_INFLIGHT.add(key)
    task = asyncio.create_task(_run_synthesis_in_background(user_id, phase_id))
    _SYNTHESIS_TASKS.add(task)
    task.add_done_callback(_SYNTHESIS_TASKS.discard)


async def _completed_phase_records(
    db: AsyncSession,
    mission_progress: list[UserMissionProgress],
) -> list[Phase]:
    """Retorna apenas as trilhas com todas as missões obrigatórias concluídas."""
    completed_ids = {
        progress.mission_id
        for progress in mission_progress
        if progress.status == MissionStatus.completed
    }
    if not completed_ids:
        return []

    phases_result = await db.execute(select(Phase).where(Phase.is_active == True))
    phases = phases_result.scalars().all()
    completed_phases: list[Phase] = []
    for phase in phases:
        required_result = await db.execute(
            select(Mission.id).where(
                Mission.phase_id == phase.id,
                Mission.is_required == True,
            )
        )
        required_ids = list(required_result.scalars().all())
        if required_ids and all(mission_id in completed_ids for mission_id in required_ids):
            completed_phases.append(phase)
    return completed_phases


async def _check_phase_completion(
    db: AsyncSession, user_id: int, phase_id: int
) -> tuple[str | None, int, Phase | None]:
    """Verifica a conclusão da fase e, na primeira vez, concede a conquista e
    as Prismas do marco. Retorna (nome_da_conquista, prismas_creditadas, phase).

    A `Phase` retornada permite ao chamador gerar a síntese e a celebração
    com os dados recém-gravados na mesma sessão.
    """
    missions_result = await db.execute(
        select(Mission).where(Mission.phase_id == phase_id, Mission.is_required == True)
    )
    required_missions = missions_result.scalars().all()

    if not required_missions:
        return None, 0, None

    for mission in required_missions:
        prog_result = await db.execute(
            select(UserMissionProgress.id).where(
                UserMissionProgress.user_id == user_id,
                UserMissionProgress.mission_id == mission.id,
                mission_passed_sql(),
            )
        )
        if not prog_result.scalar_one_or_none():
            return None, 0, None

    # Todas concluídas — verificar qual conquista de fase conceder
    phase_result = await db.execute(select(Phase).where(Phase.id == phase_id))
    phase = phase_result.scalar_one_or_none()
    if not phase:
        return None, 0, None

    achievement_key = PHASE_ACHIEVEMENT_KEYS.get(
        phase.number, f"fase_{phase.number}_concluida"
    )
    name = await grant_achievement(db, user_id, achievement_key)
    if not name:
        # Já concluída antes — não duplica síntese.
        return None, 0, None

    await add_coins(db, user_id, COINS_PHASE_COMPLETION)

    # A síntese é gerada no fluxo de conclusão da missão (com a sessão do
    # request, para enxergar os dados recém-gravados) e usada na celebração.
    # O painel de progresso apenas lê o cache.
    return name, COINS_PHASE_COMPLETION, phase


async def get_user_progress_summary(db: AsyncSession, user_id: int) -> dict:
    points_result = await db.execute(select(UserPoints).where(UserPoints.user_id == user_id))
    user_points = points_result.scalar_one_or_none()

    achievements_result = await db.execute(
        select(UserAchievement, Achievement)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .where(UserAchievement.user_id == user_id)
        .order_by(UserAchievement.earned_at.desc())
    )
    achievements = achievements_result.all()

    mission_progress_result = await db.execute(
        select(UserMissionProgress).where(UserMissionProgress.user_id == user_id)
    )
    mission_progress = mission_progress_result.scalars().all()

    competencies_result = await db.execute(
        select(UserCompetencyProgress, Competency)
        .join(Competency, UserCompetencyProgress.competency_id == Competency.id)
        .where(UserCompetencyProgress.user_id == user_id)
        .order_by(Competency.code)
    )
    competencies = competencies_result.all()

    # Expõe apenas a síntese de trilhas realmente concluídas.
    # O painel nunca espera o LLM: usa cache ou fallback imediato e atualiza
    # a versão com IA em background.
    completed_phases = await _completed_phase_records(db, mission_progress)
    trail_synthesis_list: list[dict] = []
    for phase in completed_phases:
        synthesis = await analyst.get_cached_trail_synthesis(db, user_id, phase.id)
        if not synthesis:
            synthesis = await analyst.generate_trail_synthesis(
                db,
                user_id,
                phase.id,
                use_cache=True,
                allow_ai=False,
                save=False,
            )
            if settings.analyst_enabled:
                _spawn_trail_synthesis(user_id, phase.id)
        elif synthesis.source == "fallback" and settings.analyst_enabled:
            # Tenta melhorar o cache com a versão do Analista IA.
            _spawn_trail_synthesis(user_id, phase.id)
        trail_synthesis_list.append({
            "trail_id": phase.id,
            "trail_number": phase.number,
            "trail_name": phase.name,
            "short": synthesis.short,
            "full": {
                "competencies_demonstrated": synthesis.full.competencies_demonstrated,
                "competencies_with_difficulty": synthesis.full.competencies_with_difficulty,
                "summary": synthesis.full.summary,
                "reinforcement_suggestion": synthesis.full.reinforcement_suggestion,
            },
            "source": synthesis.source,
        })

    return {
        "total_points": user_points.total_points if user_points else 0,
        "coins": user_points.coins if user_points else 0,
        "level": user_points.level if user_points else 1,
        "level_name": _level_name(user_points.level if user_points else 1),
        "current_level_points": LEVEL_THRESHOLDS.get(
            user_points.level if user_points else 1, 0
        ),
        "next_level_points": _next_level_threshold(user_points.level if user_points else 1),
        "achievements": [
            {"key": a.Achievement.key, "name": a.Achievement.name, "earned_at": a.UserAchievement.earned_at}
            for a in achievements
        ],
        "competencies": [
            {
                "code": row.Competency.code,
                "name": row.Competency.name,
                "status": row.UserCompetencyProgress.status.value,
                "correct_count": row.UserCompetencyProgress.correct_count,
                "incorrect_count": row.UserCompetencyProgress.incorrect_count,
                "reinforcement_suggested": row.UserCompetencyProgress.reinforcement_suggested,
            }
            for row in competencies
        ],
        "missions_completed": sum(1 for m in mission_progress if m.status == MissionStatus.completed),
        "missions_in_progress": sum(1 for m in mission_progress if m.status == MissionStatus.in_progress),
        "analyst_insight": await analyst.overall_insight(db, user_id),
        "trail_synthesis": trail_synthesis_list,
    }


def _level_name(level: int) -> str:
    names = {1: "Iniciante", 2: "Consciente", 3: "Planejador", 4: "Estrategista", 5: "Autônomo"}
    return names.get(level, "Iniciante")


def _next_level_threshold(level: int) -> int | None:
    return LEVEL_THRESHOLDS.get(level + 1)
