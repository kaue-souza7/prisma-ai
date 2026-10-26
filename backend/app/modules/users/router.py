from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.shared.models import User
from app.modules.users import service
from app.modules.users.schemas import (
    MeResponse,
    ProfileUpdate,
    OnboardingComplete,
    OnboardingOut,
    ProfileOut,
    TrailOut,
    TrailPreferenceRequest,
    UserOut,
)

router = APIRouter()


@router.get("/me", response_model=MeResponse)
async def get_me(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await service.get_profile(db, current_user.id)
    if not profile:
        return {"user": current_user, "profile": None}

    payload = ProfileOut.model_validate(profile).model_dump()
    trail = await service.get_trail(db, current_user.id)
    if trail:
        # Mantém /me consistente com /me/trail: a UI recebe as fases já
        # enriquecidas, não apenas a ordem bruta persistida.
        payload["trail"] = trail
    return {"user": current_user, "profile": payload}


@router.patch("/me/profile", response_model=ProfileOut)
async def update_profile(
    body: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await service.update_profile(db, current_user.id, body.model_dump(exclude_none=True))
    return profile


@router.post("/me/onboarding", response_model=OnboardingOut)
async def complete_onboarding(
    body: OnboardingComplete,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await service.complete_onboarding(
        db,
        current_user.id,
        body.personal_goal,
        body.knowledge_level,
        body.consent_version,
        body.preferences,
        body.life_context,
        body.urgency,
    )
    trail = await service.get_trail(db, current_user.id)
    return {"message": "Onboarding concluído com sucesso.", "trail": trail}


@router.get("/me/trail", response_model=Optional[TrailOut])
async def get_my_trail(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_trail(db, current_user.id)


@router.post("/me/trail/preference", response_model=TrailOut)
async def set_trail_preference(
    body: TrailPreferenceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.set_trail_preference(db, current_user.id, body.mode)
