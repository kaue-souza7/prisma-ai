from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.shared.models import User, Profile
from app.modules.agents import catalyst


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_profile(db: AsyncSession, user_id: int) -> Profile | None:
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    return result.scalar_one_or_none()


async def update_profile(db: AsyncSession, user_id: int, data: dict) -> Profile:
    profile = await get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")

    for key, value in data.items():
        if value is not None:
            if key == "preferences":
                profile.preferences = {**(profile.preferences or {}), **value}
            else:
                setattr(profile, key, value)
    await db.flush()
    return profile


def _trail_from_profile(profile: Profile) -> dict:
    preferences = profile.preferences or {}
    return catalyst.build_trail(
        personal_goal=profile.personal_goal,
        goal_category=preferences.get("goal_category"),
        knowledge_level=profile.knowledge_level,
        preferences=preferences,
    )


async def complete_onboarding(
    db: AsyncSession,
    user_id: int,
    personal_goal: str,
    knowledge_level: str,
    consent_version: str,
    preferences: dict | None = None,
    life_context: str | None = None,
    urgency: str | None = None,
) -> Profile:
    profile = await get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")

    merged_preferences = {**(profile.preferences or {}), **(preferences or {})}
    if life_context:
        merged_preferences["life_context"] = life_context
    if urgency:
        merged_preferences["urgency"] = urgency

    # O endpoint pode ser reenviado por retry de rede. Não conceder o bônus
    # de onboarding mais de uma vez — mas garanta que um perfil antigo, sem
    # trilha, receba a trilha na primeira oportunidade.
    if profile.onboarding_completed:
        if not profile.trail:
            profile.trail = catalyst.build_trail(
                personal_goal=profile.personal_goal,
                goal_category=merged_preferences.get("goal_category"),
                knowledge_level=profile.knowledge_level,
                preferences=merged_preferences,
            )
            await db.flush()
        return profile

    profile.personal_goal = personal_goal
    profile.knowledge_level = knowledge_level
    profile.consent_given = True
    profile.consent_version = consent_version
    profile.consent_given_at = datetime.now(timezone.utc)
    profile.onboarding_completed = True
    profile.preferences = merged_preferences
    profile.trail = catalyst.build_trail(
        personal_goal=personal_goal,
        goal_category=merged_preferences.get("goal_category"),
        knowledge_level=knowledge_level,
        preferences=merged_preferences,
    )

    await db.flush()

    # Conceder conquista e pontos do onboarding
    from app.modules.progress.service import grant_onboarding_bonus
    await grant_onboarding_bonus(db, user_id)

    return profile


async def set_trail_preference(
    db: AsyncSession, user_id: int, mode: str
) -> dict:
    """Permite ao estudante aceitar a trilha sugerida ou voltar à ordem padrão."""
    profile = await get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")

    if mode == "standard":
        trail = catalyst.build_standard_trail()
    elif mode == "personalized":
        trail = _trail_from_profile(profile)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Modo de trilha inválido. Use 'personalized' ou 'standard'.",
        )

    profile.trail = trail
    await db.flush()
    return await catalyst.get_trail_view(db, user_id) or trail


async def get_trail(db: AsyncSession, user_id: int) -> dict | None:
    return await catalyst.get_trail_view(db, user_id)
