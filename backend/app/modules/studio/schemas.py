from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    format: Literal["revisao", "flashcards", "exercicios"]
    phase_id: int
    mission_id: Optional[int] = None
    style_hint: Optional[str] = Field(default=None, max_length=500)


class GenerationOut(BaseModel):
    id: int
    format: str
    phase_id: Optional[int] = None
    phase_name: Optional[str] = None
    mission_id: Optional[int] = None
    mission_name: Optional[str] = None
    style_hint: Optional[str] = None
    content: dict
    status: str
    coins_spent: int
    created_at: datetime


class LibraryOut(BaseModel):
    items: list[GenerationOut]
    total: int


class SubmitExerciseRequest(BaseModel):
    question_index: int
    response_data: dict


class SubmitExerciseOut(BaseModel):
    is_correct: Optional[bool]
    correct_answer: Optional[str] = None
    feedback: str
    all_done: bool
    coins_earned: int = 0
