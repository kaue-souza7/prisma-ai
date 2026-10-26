"""Módulo de conversas — chat do Mentor.

A persistência e o contrato do chat já são reais. A resposta do Mentor usa o
adaptador do Orchestrate; sem integração, o fallback é explícito e nunca
simula uma resposta de IA.
"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.shared.models import User
from app.modules.conversations import service

router = APIRouter()


class MessageIn(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    mission_id: Optional[int] = None


class MessageOut(BaseModel):
    role: str  # user | assistant
    content: str
    timestamp: str
    status: str = "preparing"  # available | preparing | unavailable
    suggestions: List[str] = []
    source: str = "fallback"


class ConversationOut(BaseModel):
    id: int
    agent: str
    mission_id: Optional[int]
    messages: List[dict]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MentorContextOut(BaseModel):
    mission_id: Optional[int] = None
    mission_name: Optional[str] = None
    phase_number: Optional[int] = None
    phase_name: Optional[str] = None
    opening_message: str
    suggestions: List[str] = []
    status: str
    personal_goal: Optional[str] = None
    reinforcement_topics: List[str] = []


@router.post("/mentor", response_model=MessageOut)
async def chat_with_mentor(
    body: MessageIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.send_mentor_message(
        db, current_user, body.content, body.mission_id
    )


@router.get("/mentor/context", response_model=MentorContextOut)
async def mentor_context(
    mission_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_mentor_context(db, current_user.id, mission_id)


@router.get("/mentor/history", response_model=List[ConversationOut])
async def get_mentor_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_mentor_history(db, current_user.id)
