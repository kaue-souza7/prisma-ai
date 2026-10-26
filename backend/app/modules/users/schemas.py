from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TrailPhaseOut(BaseModel):
    number: int
    name: str
    description: Optional[str] = None


class TrailOut(BaseModel):
    source: str
    version: int = 1
    goal_category: Optional[str] = None
    phase_order: list[int]
    rationale: str
    focus_areas: list[str] = []
    pace: str = "steady"
    knowledge_level: Optional[str] = None
    life_context: Optional[str] = None
    urgency: Optional[str] = None
    generated_at: Optional[str] = None
    phases: list[TrailPhaseOut] = []


class ProfileOut(BaseModel):
    personal_goal: Optional[str]
    knowledge_level: Optional[str]
    onboarding_completed: bool
    consent_given: bool
    preferences: Optional[dict]
    trail: Optional[dict] = None

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    personal_goal: Optional[str] = None
    knowledge_level: Optional[str] = None
    preferences: Optional[dict] = None


class OnboardingComplete(BaseModel):
    personal_goal: str
    knowledge_level: str
    consent_version: str
    preferences: Optional[dict] = None
    life_context: Optional[str] = None
    urgency: Optional[str] = None


class OnboardingOut(BaseModel):
    message: str
    trail: Optional[TrailOut] = None


class TrailPreferenceRequest(BaseModel):
    mode: str  # personalized | standard


class MeResponse(BaseModel):
    user: UserOut
    profile: Optional[ProfileOut]

    model_config = {"from_attributes": True}
