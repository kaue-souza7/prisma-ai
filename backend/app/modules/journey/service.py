from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.shared.models import (
    Phase, Mission, Activity, ContentItem, UserMissionProgress, UserResponse, MissionStatus
)
from app.modules.progress.service import (
    COINS_CORRECT_ANSWER,
    EXCELLENCE_THRESHOLD,
    add_coins,
    apply_mission_completion,
    mission_has_passed,
    mission_passed_sql,
    record_competency_evidence,
)
from app.modules.agents import analyst, catalyst


async def get_all_phases(db: AsyncSession) -> list[Phase]:
    result = await db.execute(
        select(Phase).where(Phase.is_active == True).order_by(Phase.order)
    )
    return result.scalars().all()


async def get_phases_with_user_progress(db: AsyncSession, user_id: int) -> list[dict]:
    phases = await get_all_phases(db)
    phase_order = await catalyst.get_phase_order(db, user_id, phases)
    by_number = {phase.number: phase for phase in phases}
    ordered_phases = [by_number[number] for number in phase_order if number in by_number]
    # Se uma fase nova for criada depois da trilha, ela entra no fim em vez de
    # desaparecer do mapa.
    ordered_phases.extend(phase for phase in phases if phase not in ordered_phases)

    progress_result = await db.execute(
        select(UserMissionProgress).where(UserMissionProgress.user_id == user_id)
    )
    progress_by_mission = {
        progress.mission_id: progress for progress in progress_result.scalars().all()
    }

    result = []
    for position, phase in enumerate(ordered_phases, start=1):
        missions_result = await db.execute(
            select(Mission).where(Mission.phase_id == phase.id).order_by(Mission.order)
        )
        missions = missions_result.scalars().all()
        phase_unlocked = await is_phase_unlocked(db, user_id, phase, phase_order)
        previous_required_completed = True
        missions_out = []

        for mission in missions:
            progress = progress_by_mission.get(mission.id)
            mission_unlocked = phase_unlocked and (
                not mission.is_required or previous_required_completed
            )
            status = _resolve_mission_status(progress, mission_unlocked)

            missions_out.append({
                "mission": mission,
                "progress": progress,
                "status": status,
                "is_unlocked": status != MissionStatus.locked.value,
            })

            if mission.is_required:
                previous_required_completed = (
                    previous_required_completed and _is_completed(progress)
                )

        required = [mission for mission in missions if mission.is_required]
        phase_completed = bool(required) and all(
            _is_completed(progress_by_mission.get(mission.id)) for mission in required
        )
        phase_started = any(mission.id in progress_by_mission for mission in missions)

        if phase_completed:
            phase_status = "completed"
        elif not phase_unlocked:
            phase_status = "locked"
        elif phase_started:
            phase_status = "in_progress"
        else:
            phase_status = "available"

        result.append({
            "phase": phase,
            "status": phase_status,
            "is_unlocked": phase_unlocked,
            "trail_position": position,
            "trail_size": len(ordered_phases),
            "missions": missions_out,
        })
    return result


def _is_completed(progress: UserMissionProgress | None) -> bool:
    """Um módulo aprovado continua liberando o próximo mesmo durante um retry."""
    return mission_has_passed(progress)


def _resolve_mission_status(
    progress: UserMissionProgress | None, unlocked: bool
) -> str:
    if progress and progress.status in {
        MissionStatus.completed,
        MissionStatus.in_progress,
    }:
        return progress.status.value
    return (
        MissionStatus.available.value
        if unlocked
        else MissionStatus.locked.value
    )


async def is_phase_unlocked(
    db: AsyncSession,
    user_id: int,
    phase: Phase,
    phase_order: list[int] | None = None,
) -> bool:
    """A primeira fase da trilha começa disponível; as demais dependem de
    todas as fases anteriores da trilha estarem concluídas.

    A trilha vem do perfil (personalizada) ou da ordem canônica (fallback).
    O backend valida a trilha antes de usá-la; uma ordem inválida nunca
    desbloqueia fases por acidente.
    """
    order = phase_order or await catalyst.get_phase_order(db, user_id)
    if phase.number not in order:
        return False

    position = order.index(phase.number)
    if position == 0:
        return True

    prior_numbers = order[:position]
    prior_result = await db.execute(
        select(Phase).where(
            Phase.is_active == True,
            Phase.number.in_(prior_numbers),
        )
    )
    prior_phases = {item.number: item for item in prior_result.scalars().all()}
    if set(prior_phases) != set(prior_numbers):
        return False

    for prior in prior_phases.values():
        required_result = await db.execute(
            select(Mission.id).where(
                Mission.phase_id == prior.id,
                Mission.is_required == True,
            )
        )
        required_ids = list(required_result.scalars().all())
        if not required_ids:
            # Uma fase sem missões obrigatórias não pode ser considerada
            # concluída; por segurança, ela bloqueia as seguintes.
            return False

        completed_result = await db.execute(
            select(UserMissionProgress.mission_id).where(
                UserMissionProgress.user_id == user_id,
                UserMissionProgress.mission_id.in_(required_ids),
                mission_passed_sql(),
            )
        )
        completed_ids = set(completed_result.scalars().all())
        if not all(mission_id in completed_ids for mission_id in required_ids):
            return False

    return True


async def is_mission_unlocked(
    db: AsyncSession, user_id: int, mission: Mission
) -> bool:
    phase_result = await db.execute(
        select(Phase).where(Phase.id == mission.phase_id, Phase.is_active == True)
    )
    phase = phase_result.scalar_one_or_none()
    if not phase or not await is_phase_unlocked(db, user_id, phase):
        return False

    # Missões opcionais não bloqueiam nem são bloqueadas pela sequência.
    if not mission.is_required:
        return True

    previous_result = await db.execute(
        select(Mission).where(
            Mission.phase_id == mission.phase_id,
            Mission.is_required == True,
            Mission.order < mission.order,
        )
    )
    previous_missions = previous_result.scalars().all()
    if not previous_missions:
        return True

    completed_result = await db.execute(
        select(UserMissionProgress.mission_id).where(
            UserMissionProgress.user_id == user_id,
            UserMissionProgress.mission_id.in_(
                [previous.id for previous in previous_missions]
            ),
            mission_passed_sql(),
        )
    )
    completed_ids = set(completed_result.scalars().all())
    return all(previous.id in completed_ids for previous in previous_missions)


async def get_mission_progress(
    db: AsyncSession, user_id: int, mission_id: int
) -> UserMissionProgress | None:
    result = await db.execute(
        select(UserMissionProgress).where(
            UserMissionProgress.user_id == user_id,
            UserMissionProgress.mission_id == mission_id,
        )
    )
    return result.scalar_one_or_none()


async def get_mission_detail(db: AsyncSession, mission_id: int) -> Mission:
    result = await db.execute(
        select(Mission)
        .where(Mission.id == mission_id)
        .options(selectinload(Mission.competencies), selectinload(Mission.activities))
    )
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Missão não encontrada.")
    return mission


async def get_next_mission(
    db: AsyncSession, user_id: int, mission: Mission
) -> Mission | None:
    """Próxima missão na trilha do estudante, respeitando os desbloqueios."""
    phases = await catalyst.get_active_phases(db)
    order = await catalyst.get_phase_order(db, user_id, phases)
    by_number = {phase.number: phase for phase in phases}
    ordered_phases = [by_number[number] for number in order if number in by_number]
    ordered_phases.extend(phase for phase in phases if phase not in ordered_phases)

    current_result = await db.execute(select(Phase).where(Phase.id == mission.phase_id))
    current_phase = current_result.scalar_one_or_none()
    if not current_phase:
        return None

    # Primeiro, a próxima missão da mesma fase.
    next_result = await db.execute(
        select(Mission)
        .where(
            Mission.phase_id == mission.phase_id,
            Mission.order > mission.order,
        )
        .order_by(Mission.order)
        .limit(1)
    )
    same_phase = next_result.scalar_one_or_none()
    if same_phase and await is_mission_unlocked(db, user_id, same_phase):
        return same_phase

    # Depois, a primeira missão da próxima fase da trilha que esteja liberada.
    try:
        current_position = ordered_phases.index(current_phase)
    except ValueError:
        current_position = len(ordered_phases) - 1

    for phase in ordered_phases[current_position + 1:]:
        if not await is_phase_unlocked(db, user_id, phase, order):
            break
        candidate_result = await db.execute(
            select(Mission)
            .where(Mission.phase_id == phase.id)
            .order_by(Mission.order)
            .limit(1)
        )
        candidate = candidate_result.scalar_one_or_none()
        if candidate:
            return candidate if await is_mission_unlocked(db, user_id, candidate) else None

    return None


async def start_mission(db: AsyncSession, user_id: int, mission_id: int) -> UserMissionProgress:
    mission = await get_mission_detail(db, mission_id)
    if not await is_mission_unlocked(db, user_id, mission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conclua as missões anteriores para desbloquear esta missão.",
        )

    if not mission.activities:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta missão ainda não possui atividades disponíveis.",
        )

    prog_result = await db.execute(
        select(UserMissionProgress).where(
            UserMissionProgress.user_id == user_id,
            UserMissionProgress.mission_id == mission_id,
        )
    )
    prog = prog_result.scalar_one_or_none()

    if prog and prog.status == MissionStatus.completed:
        return prog

    if not prog:
        prog = UserMissionProgress(
            user_id=user_id,
            mission_id=mission_id,
            status=MissionStatus.in_progress,
            attempts=1,
            started_at=datetime.now(timezone.utc),
        )
        db.add(prog)
    else:
        prog.status = MissionStatus.in_progress
        # `attempts` é o número da tentativa atual. Registros antigos podem
        # estar com 0; nesse caso a primeira tentativa é a 1.
        prog.attempts = max(prog.attempts or 0, 1)
        if not prog.started_at:
            prog.started_at = datetime.now(timezone.utc)

    await db.flush()
    return prog


async def retry_mission(
    db: AsyncSession,
    user_id: int,
    mission_id: int,
    *,
    voluntary: bool = False,
) -> UserMissionProgress:
    """Abre uma nova tentativa do módulo sem apagar o histórico.

    O retry de um módulo já aprovado é opcional: só acontece quando o próprio
    estudante pede (`voluntary=True`). Em ambos os casos, as respostas antigas
    permanecem no banco com o `mission_attempt` anterior.
    """
    await get_mission_detail(db, mission_id)  # 404 se o módulo não existir
    progress = await get_mission_progress(db, user_id, mission_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este módulo ainda não foi iniciado.",
        )

    if mission_has_passed(progress) and not voluntary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Você já foi aprovado neste módulo. Refazer é opcional "
                "e precisa ser solicitado pelo estudante."
            ),
        )

    # Registros anteriores ao novo modelo podem ter `attempts = 0` mesmo com
    # respostas já gravadas na tentativa 1. Nesse caso a próxima é a 2.
    progress.attempts = max(progress.attempts or 0, 1) + 1
    progress.status = MissionStatus.in_progress
    progress.current_step = 0
    progress.completed_steps = []
    progress.completed_at = None
    if not progress.started_at:
        progress.started_at = datetime.now(timezone.utc)

    await db.flush()
    return progress


async def build_next_step_recommendation(
    db: AsyncSession,
    user_id: int,
    next_mission: Mission | None,
) -> dict:
    """Mensagem do Catalisador para o próximo passo, com base na trilha."""
    trail = await catalyst.get_trail_view(db, user_id)
    reinforcement_topics = await analyst.reinforcement_topics(db, user_id)

    if not next_mission:
        return catalyst.build_recommendation(
            trail=trail,
            mission_name=None,
            mission_id=None,
            phase_number=None,
            phase_name=None,
            is_in_progress=False,
            has_mission=False,
            reinforcement_topics=reinforcement_topics,
            trail_size=len(trail["phase_order"]) if trail else 6,
        )

    phase_result = await db.execute(select(Phase).where(Phase.id == next_mission.phase_id))
    phase = phase_result.scalar_one_or_none()
    progress = await get_mission_progress(db, user_id, next_mission.id)
    order = trail["phase_order"] if trail else list(catalyst.DEFAULT_PHASE_ORDER)
    position = order.index(phase.number) + 1 if phase and phase.number in order else None

    return catalyst.build_recommendation(
        trail=trail,
        mission_name=next_mission.name,
        mission_id=next_mission.id,
        phase_number=phase.number if phase else None,
        phase_name=phase.name if phase else None,
        is_in_progress=bool(progress and progress.status == MissionStatus.in_progress),
        has_mission=True,
        reinforcement_topics=reinforcement_topics,
        trail_position=position,
        trail_size=len(order),
    )


async def submit_activity_response(
    db: AsyncSession,
    user_id: int,
    mission_id: int,
    activity_id: int,
    response_data: dict,
) -> dict:
    mission = await get_mission_detail(db, mission_id)
    if not await is_mission_unlocked(db, user_id, mission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conclua as missões anteriores para responder a esta missão.",
        )

    # Verificar que a atividade pertence à missão
    act_result = await db.execute(
        select(Activity).where(Activity.id == activity_id, Activity.mission_id == mission_id)
    )
    activity = act_result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atividade não encontrada.")

    progress = await get_mission_progress(db, user_id, mission_id)
    current_attempt = max(progress.attempts or 0, 1) if progress else 1

    # Uma atividade só pode ser respondida uma vez por tentativa do módulo.
    # Refazer o módulo abre uma nova tentativa e mantém o histórico anterior.
    existing_result = await db.execute(
        select(UserResponse.id).where(
            UserResponse.user_id == user_id,
            UserResponse.activity_id == activity_id,
            UserResponse.mission_attempt == current_attempt,
        ).limit(1)
    )
    if existing_result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Você já respondeu esta atividade nesta tentativa. "
                "Refaça o módulo para responder novamente."
            ),
        )

    # Contar tentativas anteriores nesta atividade (histórico entre módulos).
    prev_result = await db.execute(
        select(UserResponse).where(
            UserResponse.user_id == user_id,
            UserResponse.activity_id == activity_id,
        )
    )
    previous = prev_result.scalars().all()
    attempt_number = len(previous) + 1

    # Avaliar resposta (determinístico)
    is_correct, feedback, correct_answer = evaluate_response(activity, response_data)
    score = activity.points_value if is_correct else 0

    # Prismas por acerto valem apenas na primeira vez que a atividade é
    # acertada. Refazer um módulo já aprovado não pode virar farm de moedas.
    first_correct = (
        is_correct is True
        and activity.activity_type != "open_text"
        and not any(item.is_correct is True for item in previous)
    )

    response = UserResponse(
        user_id=user_id,
        mission_id=mission_id,
        activity_id=activity_id,
        response_data=response_data,
        is_correct=is_correct,
        score=score,
        attempt_number=attempt_number,
        mission_attempt=current_attempt,
        created_at=datetime.now(timezone.utc),
    )
    db.add(response)
    await db.flush()

    coins_earned = 0
    if first_correct:
        await add_coins(db, user_id, COINS_CORRECT_ANSWER)
        coins_earned += COINS_CORRECT_ANSWER

    await record_competency_evidence(db, user_id, activity, is_correct)
    await mark_activity_step_completed(db, user_id, mission, activity)

    # Avaliar a tentativa completa do módulo.
    completion = await apply_mission_completion(db, user_id, mission_id)
    mission_completed = completion["mission_completed"]
    points_earned = completion["points_earned"]
    coins_earned += completion["coins_earned"]
    new_achievements = completion["new_achievements"]

    # O feedback de uma primeira tentativa é do Mentor (fallback estático do
    # conteúdo). Quando o erro se repete ou a competência já tinha sido
    # sinalizada, o Analista aparece com uma recomendação estruturada.
    reinforcement = None
    if is_correct is False:
        codes = activity.content.get("competency_codes") or []
        names = await analyst.competency_names_for_codes(db, mission_id, codes)
        recurring = [
            name
            for name in names
            if name in await analyst.reinforcement_topics(db, user_id)
        ]
        # O selo de reforço só aparece quando a regra determinística já
        # sinalizou a competência (2 atividades distintas ou 3 tentativas).
        if recurring:
            reinforcement = analyst.build_reinforcement_insight(
                recurring, max(attempt_number, 2)
            )

    feedback_agent = "analyst" if reinforcement else "mentor"

    mission_insight = None
    next_step = None
    if mission_completed:
        mission_insight = await analyst.mission_insight(db, user_id, mission_id)
        next_mission = await get_next_mission(db, user_id, mission)
        next_step = await build_next_step_recommendation(db, user_id, next_mission)

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer if is_correct is False else None,
        "score": score,
        "feedback": feedback,
        "feedback_agent": feedback_agent,
        "attempt_number": attempt_number,
        "reinforcement": reinforcement,
        "mission_completed": mission_completed,
        "attempt_finished": completion["attempt_finished"],
        "points_earned": points_earned,
        "coins_earned": coins_earned,
        "new_achievements": new_achievements,
        "score_percent": completion["score_percent"],
        "passed": completion["passed"],
        "must_retry": completion["must_retry"],
        "can_retry_optionally": completion["can_retry_optionally"],
        "mission_insight": mission_insight,
        "next_step": next_step,
    }


def evaluate_response(
    activity: Activity, response_data: dict
) -> tuple[bool | None, str, str | None]:
    """
    Avaliação determinística por tipo de atividade.

    Retorna (is_correct, feedback, correct_answer). O gabarito só é devolvido
    quando a resposta está incorreta — nunca antes da submissão.
    """
    activity_type = activity.activity_type
    content = activity.content

    if activity_type == "multiple_choice":
        selected = response_data.get("selected_option")
        correct = content.get("correct_answer")
        if selected is None or correct is None:
            return None, content.get("feedback_neutral", "Resposta registrada."), None
        is_correct = str(selected) == str(correct)
        feedback = content.get("feedback_correct") if is_correct else content.get("feedback_incorrect", "Revise sua resposta.")
        return is_correct, feedback or "Obrigado pela resposta.", None if is_correct else str(correct)

    if activity_type == "simulation":
        selected = response_data.get("choice")
        correct = content.get("correct_choice")
        if selected is None or correct is None:
            return None, content.get("feedback_neutral", "Escolha registrada."), None
        is_correct = str(selected) == str(correct)
        feedback = content.get("feedback_correct") if is_correct else content.get("feedback_incorrect", "Revise sua escolha.")
        return is_correct, feedback or "Escolha registrada.", None if is_correct else str(correct)

    # open_text — avaliação pela IA na Etapa 2; por ora retorna feedback estático
    if activity_type == "open_text":
        feedback = content.get("feedback_static", "Sua resposta foi registrada. O Mentor irá analisá-la.")
        return None, feedback, None

    return None, "Resposta registrada.", None


# ─────────────────────────────────────────────
# Experiência imersiva de módulo
# ─────────────────────────────────────────────

def _fallback_flow(content_items: list[ContentItem], activities: list[Activity]) -> list[dict]:
    flow = [
        {
            "type": "reading",
            "content_type": item.content_type,
            "content_order": item.order,
        }
        for item in content_items
    ]
    flow.extend(
        {
            "type": "scenario" if activity.activity_type == "simulation" else "question",
            "activity_order": activity.order,
        }
        for activity in activities
    )
    return flow


def _estimated_minutes(flow: list[dict]) -> int:
    total = 0.0
    for step in flow:
        step_type = step.get("type")
        if step_type == "reading":
            total += 0.65
        elif step_type == "question":
            total += 0.75
        elif step_type == "scenario":
            total += 1.2
        else:
            total += 0.25
    return max(5, min(20, round(total)))


async def get_lesson(db: AsyncSession, user_id: int, mission_id: int) -> dict:
    mission = await get_mission_detail(db, mission_id)
    if not await is_mission_unlocked(db, user_id, mission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conclua as missões anteriores para abrir este módulo.",
        )

    phase_result = await db.execute(select(Phase).where(Phase.id == mission.phase_id))
    phase = phase_result.scalar_one_or_none()
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trilha não encontrada.")

    content_result = await db.execute(
        select(ContentItem)
        .where(
            ContentItem.mission_id == mission_id,
            ContentItem.is_published == True,
        )
        .order_by(ContentItem.order)
    )
    content_items = content_result.scalars().all()

    flow = mission.lesson_flow or _fallback_flow(content_items, mission.activities)
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este módulo ainda não possui um roteiro disponível.",
        )

    progress = await get_mission_progress(db, user_id, mission_id)
    completed_steps = sorted(set((progress.completed_steps or []) if progress else []))
    current_step = progress.current_step if progress else 0
    current_attempt = max(progress.attempts or 0, 1) if progress else 1
    if progress and progress.status == MissionStatus.completed:
        summary_index = next(
            (index for index, step in enumerate(flow) if step.get("type") == "summary"),
            len(flow) - 1,
        )
        current_step = summary_index
    current_step = max(0, min(current_step, len(flow) - 1))

    responses_result = await db.execute(
        select(UserResponse).where(
            UserResponse.user_id == user_id,
            UserResponse.mission_id == mission_id,
            UserResponse.mission_attempt == current_attempt,
        )
    )
    responses = responses_result.scalars().all()
    responses_by_activity: dict[int, list[UserResponse]] = {}
    for response in responses:
        responses_by_activity.setdefault(response.activity_id, []).append(response)

    content_by_key = {
        (item.content_type, item.order): item for item in content_items
    }
    activities_by_order = {activity.order: activity for activity in mission.activities}
    steps = []

    for index, step in enumerate(flow):
        step_type = step.get("type", "reading")
        title = step.get("title")
        body = step.get("body")
        content_type = step.get("content_type")
        activity = None
        user_response = None

        if step_type == "reading":
            item = content_by_key.get(
                (step.get("content_type"), step.get("content_order"))
            )
            if not item:
                continue
            title = item.title
            body = item.body
            content_type = item.content_type
        elif step_type in {"question", "scenario"}:
            activity = activities_by_order.get(step.get("activity_order"))
            if not activity:
                continue
            title = title or activity.content.get("prompt", "Atividade")
            activity_responses = responses_by_activity.get(activity.id, [])
            if activity_responses:
                latest = max(activity_responses, key=lambda item: item.created_at)
                is_correct, feedback, correct_answer = evaluate_response(
                    activity, latest.response_data
                )
                user_response = {
                    "is_correct": is_correct,
                    "feedback": feedback,
                    "attempt_number": latest.attempt_number,
                    "response_data": latest.response_data,
                    # A resposta correta só aparece depois da submissão e
                    # apenas quando o estudante errou.
                    "correct_answer": correct_answer,
                }
                # Toda atividade respondida conta como etapa feita na barra de
                # progresso, independentemente de acerto ou erro.
                if index not in completed_steps:
                    completed_steps.append(index)
            activity_public = {
                "id": activity.id,
                "order": activity.order,
                "activity_type": activity.activity_type,
                "content": _public_activity_content(activity.content),
                "points_value": activity.points_value,
            }
        else:
            activity_public = None

        steps.append({
            "index": index,
            "type": step_type,
            "title": title or "",
            "body": body,
            "agent": step.get("agent"),
            "content_type": content_type,
            "highlights": step.get("highlights") or [],
            "activity": activity_public if step_type in {"question", "scenario"} else None,
            "user_response": user_response,
            "completed": index in completed_steps,
        })

    completed_steps = sorted(set(completed_steps))
    next_candidate = await get_next_mission(db, user_id, mission)
    next_mission = None
    if next_candidate:
        next_mission = {
            "id": next_candidate.id,
            "number": next_candidate.number,
            "name": next_candidate.name,
        }

    is_unlocked = True
    status_value = _resolve_mission_status(progress, is_unlocked)
    mission_completed = bool(progress and progress.status == MissionStatus.completed)

    answered_activity_ids = {response.activity_id for response in responses}
    active_activities = [activity for activity in mission.activities if activity.is_active]
    all_answered = bool(active_activities) and all(
        activity.id in answered_activity_ids for activity in active_activities
    )
    score_percent = progress.score_percent if progress else None
    passed = mission_completed or mission_has_passed(progress)
    attempt_finished = bool(progress and all_answered)
    must_retry = attempt_finished and not passed
    can_retry_optionally = passed and (
        score_percent is None or score_percent >= EXCELLENCE_THRESHOLD
    )

    mission_insight = None
    next_step = None
    if mission_completed:
        mission_insight = await analyst.mission_insight(db, user_id, mission_id)
        next_step = await build_next_step_recommendation(db, user_id, next_candidate)

    return {
        "mission": mission,
        "phase": phase,
        "competencies": mission.competencies,
        "steps": steps,
        "current_step": current_step,
        "completed_steps": completed_steps,
        "estimated_minutes": _estimated_minutes(flow),
        "status": status_value,
        "progress": progress,
        "score_percent": score_percent,
        "passed": passed if attempt_finished else None,
        "attempt_finished": attempt_finished,
        "must_retry": must_retry if attempt_finished else None,
        "can_retry_optionally": can_retry_optionally if attempt_finished else None,
        "next_mission": next_mission,
        "mission_insight": mission_insight,
        "next_step": next_step,
    }


def _public_activity_content(content: dict) -> dict:
    private_keys = {
        "correct_answer",
        "correct_choice",
        "evaluation_criteria",
        "feedback_correct",
        "feedback_incorrect",
    }
    return {key: value for key, value in content.items() if key not in private_keys}


async def update_lesson_progress(
    db: AsyncSession,
    user_id: int,
    mission_id: int,
    step_index: int,
) -> dict:
    mission = await get_mission_detail(db, mission_id)
    if not await is_mission_unlocked(db, user_id, mission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conclua as missões anteriores para continuar este módulo.",
        )

    content_result = await db.execute(
        select(ContentItem).where(
            ContentItem.mission_id == mission_id,
            ContentItem.is_published == True,
        )
    )
    content_items = content_result.scalars().all()
    flow = mission.lesson_flow or _fallback_flow(content_items, mission.activities)
    if step_index < 0 or step_index >= len(flow):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa do módulo inválida.",
        )

    progress = await get_mission_progress(db, user_id, mission_id)
    if not progress:
        progress = await start_mission(db, user_id, mission_id)

    completed_steps = sorted(set(progress.completed_steps or []))
    if step_index > progress.current_step and step_index not in completed_steps:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Avance uma etapa por vez.",
        )

    if step_index not in completed_steps:
        completed_steps.append(step_index)
    progress.completed_steps = sorted(set(completed_steps))
    progress.current_step = max(
        progress.current_step,
        min(step_index + 1, len(flow) - 1),
    )

    if progress.status != MissionStatus.completed:
        progress.status = MissionStatus.in_progress
    await db.flush()

    return {
        "current_step": progress.current_step,
        "completed_steps": progress.completed_steps,
        "mission_completed": progress.status == MissionStatus.completed,
    }


async def mark_activity_step_completed(
    db: AsyncSession,
    user_id: int,
    mission: Mission,
    activity: Activity,
) -> None:
    """Marca a etapa respondida, sem avançar automaticamente o cursor.

    Acerto e erro contam igualmente como etapa feita: a avaliação do módulo
    acontece no fim da tentativa, não na barra de progresso.
    """
    if not mission.lesson_flow:
        return
    step_index = next(
        (
            index
            for index, step in enumerate(mission.lesson_flow)
            if step.get("type") in {"question", "scenario"}
            and step.get("activity_order") == activity.order
        ),
        None,
    )
    if step_index is None:
        return

    progress = await get_mission_progress(db, user_id, mission.id)
    if not progress:
        return

    completed = set(progress.completed_steps or [])
    completed.add(step_index)
    progress.completed_steps = sorted(completed)
    await db.flush()


async def get_journey_overview(db: AsyncSession, user_id: int) -> dict:
    """Mapa da jornada + trilha + próximo passo em uma única resposta.

    É o contrato que a UI usa para apresentar o Catalisador sem duplicar
    regras no frontend. O endpoint antigo `/phases/my-progress` permanece
    disponível para compatibilidade.
    """
    phases_data = await get_phases_with_user_progress(db, user_id)
    trail = await catalyst.get_trail_view(db, user_id)

    next_mission = None
    for phase in phases_data:
        for item in phase["missions"]:
            if item["status"] in {
                MissionStatus.in_progress.value,
                MissionStatus.available.value,
            }:
                next_mission = item["mission"]
                break
        if next_mission:
            break

    recommendation = await build_next_step_recommendation(db, user_id, next_mission)
    return {
        "trail": trail,
        "phases": phases_data,
        "recommendation": recommendation,
    }
