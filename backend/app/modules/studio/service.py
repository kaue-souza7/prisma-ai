"""Regras de negócio do Estúdio de Prismas.

O Estúdio permite trocar Prismas por conteúdo personalizado. O backend valida
o acesso ao módulo/fase, cobra as Prismas, monta o payload e só persiste
conteúdo que passou na validação estrutural. A IA nunca acessa o banco.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from types import SimpleNamespace

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.modules.agents import studio_mentor
from app.modules.journey.service import evaluate_response
from app.modules.progress.service import (
    COINS_STUDIO_EXERCISES_COMPLETION,
    add_coins,
    get_coins,
    record_studio_competency_evidence,
    spend_coins,
)
from app.shared.models import (
    Competency,
    ContentItem,
    GeneratedContent,
    Mission,
    Phase,
    Profile,
    User,
    UserCompetencyProgress,
    UserMissionProgress,
    UserResponse,
)

STUDIO_COSTS = {
    "revisao": 30,
    "flashcards": 20,
    "exercicios": 25,
}

LIBRARY_PAGE_SIZE = 20


async def _get_phase(db: AsyncSession, phase_id: int) -> Phase:
    result = await db.execute(select(Phase).where(Phase.id == phase_id))
    phase = result.scalar_one_or_none()
    if not phase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trilha não encontrada.",
        )
    return phase


async def _get_mission(db: AsyncSession, mission_id: int) -> Mission:
    result = await db.execute(select(Mission).where(Mission.id == mission_id))
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo não encontrado.",
        )
    return mission


async def _has_coursed_phase(db: AsyncSession, user_id: int, phase_id: int) -> bool:
    result = await db.execute(
        select(UserMissionProgress.id)
        .join(Mission, UserMissionProgress.mission_id == Mission.id)
        .where(
            UserMissionProgress.user_id == user_id,
            Mission.phase_id == phase_id,
        )
        .limit(1)
    )
    return result.scalar_one_or_none() is not None


async def _has_coursed_mission(db: AsyncSession, user_id: int, mission_id: int) -> bool:
    result = await db.execute(
        select(UserMissionProgress.id).where(
            UserMissionProgress.user_id == user_id,
            UserMissionProgress.mission_id == mission_id,
        ).limit(1)
    )
    return result.scalar_one_or_none() is not None


async def _build_context(
    db: AsyncSession,
    user_id: int,
    phase: Phase,
    mission: Mission | None,
) -> tuple[list[dict], list[dict], Profile | None]:
    """Competências, conteúdo aprovado e perfil usados no payload."""
    mission_query = select(Mission.id).where(Mission.phase_id == phase.id)
    if mission is not None:
        mission_query = mission_query.where(Mission.id == mission.id)
    else:
        # Revisão da fase inteira considera apenas os módulos que o estudante
        # já começou, para não expor conteúdo ainda bloqueado.
        mission_query = mission_query.join(
            UserMissionProgress,
            UserMissionProgress.mission_id == Mission.id,
        ).where(UserMissionProgress.user_id == user_id)
    mission_ids = list((await db.execute(mission_query)).scalars().all())
    if not mission_ids:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta trilha ainda não possui módulos disponíveis para o Estúdio.",
        )

    competencies_result = await db.execute(
        select(Competency)
        .where(Competency.mission_id.in_(mission_ids))
        .order_by(Competency.code)
    )
    competencies = list(competencies_result.scalars().all())

    progress_result = await db.execute(
        select(UserCompetencyProgress).where(
            UserCompetencyProgress.user_id == user_id,
            UserCompetencyProgress.competency_id.in_(
                [item.id for item in competencies]
            ),
        )
    )
    progress_by_competency = {
        item.competency_id: item for item in progress_result.scalars().all()
    }
    competency_payload = [
        {
            "code": item.code,
            "name": item.name,
            "status": (
                progress_by_competency[item.id].status.value
                if item.id in progress_by_competency
                else "not_started"
            ),
        }
        for item in competencies
    ]

    content_result = await db.execute(
        select(ContentItem)
        .where(
            ContentItem.mission_id.in_(mission_ids),
            ContentItem.is_published == True,
        )
        .order_by(ContentItem.order)
    )
    content_payload = [
        {"title": item.title, "body": item.body}
        for item in content_result.scalars().all()
    ]

    profile_result = await db.execute(
        select(Profile).where(Profile.user_id == user_id)
    )
    return competency_payload, content_payload, profile_result.scalar_one_or_none()


async def create_generation(
    db: AsyncSession,
    user_id: int,
    format: str,
    phase_id: int,
    mission_id: int | None,
    style_hint: str | None,
    coins_spent: int,
) -> GeneratedContent:
    generation = GeneratedContent(
        user_id=user_id,
        format=format,
        phase_id=phase_id,
        mission_id=mission_id,
        style_hint=style_hint,
        content={},
        coins_spent=coins_spent,
        status="generating",
    )
    db.add(generation)
    await db.flush()
    return generation


async def _load_generation(
    db: AsyncSession, user_id: int, generation_id: int
) -> GeneratedContent:
    result = await db.execute(
        select(GeneratedContent)
        .where(
            GeneratedContent.id == generation_id,
            GeneratedContent.user_id == user_id,
        )
        .options(
            selectinload(GeneratedContent.phase),
            selectinload(GeneratedContent.mission),
        )
    )
    generation = result.scalar_one_or_none()
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado.",
        )
    return generation


async def set_generation_ready(
    db: AsyncSession, generation_id: int, content: dict
) -> GeneratedContent:
    result = await db.execute(
        select(GeneratedContent)
        .where(GeneratedContent.id == generation_id)
        .options(
            selectinload(GeneratedContent.phase),
            selectinload(GeneratedContent.mission),
        )
    )
    generation = result.scalar_one_or_none()
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado.",
        )
    generation.content = content
    generation.status = "ready"
    await db.flush()
    return generation


async def set_generation_failed(
    db: AsyncSession, generation_id: int
) -> GeneratedContent:
    result = await db.execute(
        select(GeneratedContent).where(GeneratedContent.id == generation_id)
    )
    generation = result.scalar_one_or_none()
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado.",
        )
    if generation.status == "failed":
        return generation

    generation.status = "failed"
    if generation.coins_spent:
        await add_coins(db, generation.user_id, generation.coins_spent)
    await db.flush()
    return generation


async def list_library(
    db: AsyncSession, user_id: int, limit: int = LIBRARY_PAGE_SIZE, offset: int = 0
) -> tuple[list[GeneratedContent], int]:
    conditions = (
        GeneratedContent.user_id == user_id,
        GeneratedContent.status == "ready",
    )
    total_result = await db.execute(
        select(func.count(GeneratedContent.id)).where(*conditions)
    )
    total = total_result.scalar_one()

    result = await db.execute(
        select(GeneratedContent)
        .where(*conditions)
        .options(
            selectinload(GeneratedContent.phase),
            selectinload(GeneratedContent.mission),
        )
        .order_by(GeneratedContent.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def get_generation(
    db: AsyncSession, user_id: int, generation_id: int
) -> GeneratedContent:
    return await _load_generation(db, user_id, generation_id)


async def generate_studio_content(
    db: AsyncSession,
    user: User,
    *,
    format: str,
    phase_id: int,
    mission_id: int | None,
    style_hint: str | None,
) -> GeneratedContent:
    if format not in STUDIO_COSTS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de conteúdo inválido.",
        )

    phase = await _get_phase(db, phase_id)
    mission = None
    if mission_id is not None:
        mission = await _get_mission(db, mission_id)
        if mission.phase_id != phase.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O módulo não pertence à trilha selecionada.",
            )

    if mission is not None:
        if not await _has_coursed_mission(db, user.id, mission.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você ainda não cursou este módulo.",
            )
    elif not await _has_coursed_phase(db, user.id, phase.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você ainda não cursou esta trilha.",
        )

    # Sem Orchestrate ativo, o Estúdio é honesto: não gera, não cobra. Essa
    # checagem vem antes do saldo para que o estudante veja a mensagem de
    # preparação, e não um erro de saldo, enquanto a IA não está disponível.
    if not settings.orchestrate_enabled or not settings.orchestrate_url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=studio_mentor.STUDIO_UNAVAILABLE_MESSAGE,
        )

    cost = STUDIO_COSTS[format]
    balance = await get_coins(db, user.id)
    if balance < cost:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                "Saldo de Prismas insuficiente para esta geração. "
                "Conclua atividades e módulos para ganhar mais."
            ),
        )

    competencies, content_items, profile = await _build_context(
        db, user.id, phase, mission
    )
    payload = studio_mentor.build_studio_payload(
        format=format,
        phase=phase,
        mission=mission,
        style_hint=style_hint,
        competencies=competencies,
        content_items=content_items,
        profile=profile,
    )

    try:
        await spend_coins(db, user.id, cost)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Saldo de Prismas insuficiente.",
        ) from None

    generation = await create_generation(
        db,
        user.id,
        format,
        phase.id,
        mission.id if mission else None,
        style_hint,
        cost,
    )

    try:
        content = await studio_mentor.call_orchestrate(payload)
        content = studio_mentor.validate_generated_content(format, content)
    except Exception as exc:  # noqa: BLE001 — falha de IA nunca some sem refund
        studio_mentor.log_orchestrate_failure(exc)
        await set_generation_failed(db, generation.id)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Não foi possível gerar o conteúdo agora. "
                "Suas Prismas foram devolvidas."
            ),
        ) from None

    return await set_generation_ready(db, generation.id, content)


def public_generation_content(generation: GeneratedContent) -> dict:
    """Remove gabaritos de questões ainda não respondidas."""
    content = deepcopy(generation.content or {})
    if generation.format != "exercicios":
        return content

    for question in content.get("questions", []):
        if question.get("user_response") is not None:
            continue
        question.pop("correct_answer", None)
        question.pop("feedback_correct", None)
        question.pop("feedback_incorrect", None)
    return content


def generation_to_dict(generation: GeneratedContent) -> dict:
    return {
        "id": generation.id,
        "format": generation.format,
        "phase_id": generation.phase_id,
        "phase_name": generation.phase.name if generation.phase else None,
        "mission_id": generation.mission_id,
        "mission_name": generation.mission.name if generation.mission else None,
        "style_hint": generation.style_hint,
        "content": public_generation_content(generation),
        "status": generation.status,
        "coins_spent": generation.coins_spent,
        "created_at": generation.created_at,
    }


async def submit_studio_exercise(
    db: AsyncSession,
    user_id: int,
    generation_id: int,
    question_index: int,
    response_data: dict,
) -> dict:
    generation = await _load_generation(db, user_id, generation_id)
    if generation.format != "exercicios":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta geração não é um conjunto de exercícios.",
        )
    if generation.status != "ready":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este conteúdo ainda não está pronto.",
        )

    content = dict(generation.content or {})
    questions = list(content.get("questions") or [])
    if question_index < 0 or question_index >= len(questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questão inválida.",
        )

    question = dict(questions[question_index])
    if question.get("user_response") is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já respondeu esta questão.",
        )

    activity_type = "multiple_choice" if question.get("options") else "open_text"
    synthetic_activity = SimpleNamespace(
        activity_type=activity_type,
        content=question,
    )
    is_correct, feedback, correct_answer = evaluate_response(
        synthetic_activity, response_data
    )

    response = UserResponse(
        user_id=user_id,
        mission_id=None,
        activity_id=None,
        response_data={
            **response_data,
            "generation_id": generation.id,
            "question_index": question_index,
        },
        is_correct=is_correct,
        score=0,
        attempt_number=1,
        mission_attempt=0,
        created_at=datetime.now(timezone.utc),
    )
    db.add(response)
    await db.flush()

    await record_studio_competency_evidence(
        db,
        user_id,
        question.get("competency_codes") or [],
        is_correct,
        phase_id=generation.phase_id,
        mission_id=generation.mission_id,
    )

    question["user_response"] = response_data
    question["is_correct"] = is_correct
    question["feedback"] = feedback
    questions[question_index] = question
    content["questions"] = questions

    all_done = all(item.get("user_response") is not None for item in questions)
    coins_earned = 0
    if all_done and not content.get("coins_rewarded"):
        await add_coins(db, user_id, COINS_STUDIO_EXERCISES_COMPLETION)
        content["coins_rewarded"] = True
        coins_earned = COINS_STUDIO_EXERCISES_COMPLETION

    generation.content = content
    await db.flush()

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "feedback": feedback,
        "all_done": all_done,
        "coins_earned": coins_earned,
    }
