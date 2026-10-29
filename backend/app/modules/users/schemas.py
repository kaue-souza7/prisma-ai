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
    version: int = 2
    goal_category: Optional[str] = None
    phase_order: list[int]
    trail_modes: Optional[dict] = None
    trail_1_auto_concluded: Optional[bool] = None
    rationale: str
    focus_areas: list[str] = []
    pace: str = "steady"
    next_message: Optional[str] = None
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
    # Histórico do onboarding conversacional (perguntas adaptativas).
    conversation_history: Optional[list[dict]] = None
    # Respostas estruturadas das 10 perguntas fixas.
    fixed_answers: Optional[dict] = None


class AdaptiveQuestionsRequest(BaseModel):
    fixed_answers: dict
    conversation_history: list[dict] = []


class AdaptiveQuestionsOut(BaseModel):
    questions: list[str]
    source: str = "fallback"


class OnboardingOut(BaseModel):
    message: str
    trail: Optional[TrailOut] = None


class TrailPreferenceRequest(BaseModel):
    mode: str  # personalized | standard


class MeResponse(BaseModel):
    user: UserOut
    profile: Optional[ProfileOut]

    model_config = {"from_attributes": True}
