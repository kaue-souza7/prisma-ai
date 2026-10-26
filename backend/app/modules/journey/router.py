from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.shared.models import User, UserResponse
from app.modules.journey import service
from app.modules.journey.schemas import (
    PhaseOut, MissionDetailOut, UserMissionProgressOut,
    SubmitResponseRequest, SubmitResponseOut, LessonOut,
    LessonStepProgressRequest, LessonStepProgressOut, PhaseProgressOut,
    JourneyOverviewOut, RetryMissionRequest,
)
from typing import List

router = APIRouter()

# Chaves que nunca devem ser enviadas ao estudante antes do envio da resposta.
# O gabarito e o critério de avaliação permanecem exclusivamente no backend.
PRIVATE_ACTIVITY_KEYS = {
    "correct_answer",
    "correct_choice",
    "evaluation_criteria",
    # Feedbacks de acerto/erro podem revelar o gabarito antes da submissão.
    # Eles são devolvidos somente na resposta do POST /submit.
    "feedback_correct",
    "feedback_incorrect",
}


def _sanitize_activity_content(content: dict) -> dict:
    return {key: value for key, value in content.items() if key not in PRIVATE_ACTIVITY_KEYS}


@router.get("/phases", response_model=List[PhaseOut])
async def list_phases(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    phases = await service.get_all_phases(db)
    return phases


@router.get("/phases/my-progress", response_model=List[PhaseProgressOut])
async def my_journey(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await service.get_phases_with_user_progress(db, current_user.id)
    return data


@router.get("/overview", response_model=JourneyOverviewOut)
async def journey_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.get_journey_overview(db, current_user.id)


@router.get("/missions/{mission_id}", response_model=MissionDetailOut)
async def get_mission(
    mission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mission = await service.get_mission_detail(db, mission_id)
    progress = await service.get_mission_progress(db, current_user.id, mission_id)
    is_unlocked = await service.is_mission_unlocked(db, current_user.id, mission)

    public_mission = MissionDetailOut.model_validate(mission)
    if progress and progress.status.value in {"in_progress", "completed"}:
        public_mission.user_status = progress.status.value
    else:
        public_mission.user_status = "available" if is_unlocked else "locked"
    public_mission.is_unlocked = is_unlocked
    public_mission.user_progress = (
        UserMissionProgressOut.model_validate(progress) if progress else None
    )

    current_attempt = max(progress.attempts or 0, 1) if progress else 1
    responses_result = await db.execute(
        select(UserResponse).where(
            UserResponse.user_id == current_user.id,
            UserResponse.mission_id == mission_id,
            UserResponse.mission_attempt == current_attempt,
        )
    )
    responses = responses_result.scalars().all()
    completed_activity_ids = []
    for activity in mission.activities:
        if any(response.activity_id == activity.id for response in responses):
            completed_activity_ids.append(activity.id)
    public_mission.completed_activity_ids = completed_activity_ids

    for activity in public_mission.activities:
        activity.content = _sanitize_activity_content(activity.content)
    return public_mission


@router.get("/missions/{mission_id}/lesson", response_model=LessonOut)
async def get_mission_lesson(
    mission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.get_lesson(db, current_user.id, mission_id)


@router.post(
    "/missions/{mission_id}/lesson/progress",
    response_model=LessonStepProgressOut,
)
async def save_lesson_step(
    mission_id: int,
    body: LessonStepProgressRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.update_lesson_progress(
        db, current_user.id, mission_id, body.step_index
    )


@router.post("/missions/{mission_id}/start", response_model=UserMissionProgressOut)
async def start_mission(
    mission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.start_mission(db, current_user.id, mission_id)


@router.post("/missions/{mission_id}/submit", response_model=SubmitResponseOut)
async def submit_response(
    mission_id: int,
    body: SubmitResponseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.submit_activity_response(
        db, current_user.id, mission_id, body.activity_id, body.response_data
    )


@router.post("/missions/{mission_id}/retry", response_model=UserMissionProgressOut)
async def retry_mission(
    mission_id: int,
    body: RetryMissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.retry_mission(
        db, current_user.id, mission_id, voluntary=body.voluntary
    )
