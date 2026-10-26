from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.shared.models import User
from app.modules.studio import service
from app.modules.studio.schemas import (
    GenerateRequest,
    GenerationOut,
    LibraryOut,
    SubmitExerciseOut,
    SubmitExerciseRequest,
)

router = APIRouter()


@router.post("/generate", response_model=GenerationOut)
async def generate_content(
    body: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    generation = await service.generate_studio_content(
        db,
        current_user,
        format=body.format,
        phase_id=body.phase_id,
        mission_id=body.mission_id,
        style_hint=body.style_hint,
    )
    return service.generation_to_dict(generation)


@router.get("/generate/{generation_id}", response_model=GenerationOut)
async def get_generated_content(
    generation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    generation = await service.get_generation(db, current_user.id, generation_id)
    return service.generation_to_dict(generation)


@router.get("/library", response_model=LibraryOut)
async def get_library(
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = await service.list_library(
        db, current_user.id, limit=limit, offset=offset
    )
    return {
        "items": [service.generation_to_dict(item) for item in items],
        "total": total,
    }


@router.post(
    "/exercises/{generation_id}/submit",
    response_model=SubmitExerciseOut,
)
async def submit_exercise(
    generation_id: int,
    body: SubmitExerciseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.submit_studio_exercise(
        db,
        current_user.id,
        generation_id,
        body.question_index,
        body.response_data,
    )
