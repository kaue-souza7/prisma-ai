from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PhaseOut(BaseModel):
    id: int
    number: int
    name: str
    description: Optional[str]
    order: int

    model_config = {"from_attributes": True}


class MissionOut(BaseModel):
    id: int
    phase_id: int
    number: int
    name: str
    description: Optional[str]
    order: int
    is_required: bool
    passing_score: int

    model_config = {"from_attributes": True}


class CompetencyOut(BaseModel):
    id: int
    code: Optional[str]
    name: str
    description: Optional[str]
    is_essential: bool

    model_config = {"from_attributes": True}


class ActivityOut(BaseModel):
    id: int
    order: int
    activity_type: str
    content: dict
    points_value: int
    question_set: int = 1

    model_config = {"from_attributes": True}


class UserMissionProgressOut(BaseModel):
    mission_id: int
    status: str
    score: Optional[int]
    score_percent: Optional[float] = None
    attempts: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class MissionDetailOut(MissionOut):
    competencies: List[CompetencyOut] = []
    activities: List[ActivityOut] = []
    user_status: str = "available"
    is_unlocked: bool = True
    user_progress: Optional[UserMissionProgressOut] = None
    completed_activity_ids: List[int] = []


class PhaseWithMissionsOut(PhaseOut):
    missions: List[MissionOut] = []


class MissionProgressItemOut(BaseModel):
    mission: MissionOut
    progress: Optional[UserMissionProgressOut] = None
    status: str
    is_unlocked: bool


class PhaseProgressOut(BaseModel):
    phase: PhaseOut
    status: str
    is_unlocked: bool
    trail_position: int = 0
    trail_size: int = 0
    missions: List[MissionProgressItemOut] = []


class UserCompetencyProgressOut(BaseModel):
    competency_id: int
    status: str
    incorrect_count: int
    correct_count: int
    reinforcement_suggested: bool

    model_config = {"from_attributes": True}


class AgentInsightOut(BaseModel):
    agent: str
    severity: str
    action: str
    competencies: List[str] = []
    message: str


class CatalystRecommendationOut(BaseModel):
    kind: str
    message: str
    mission_id: Optional[int] = None
    mission_name: Optional[str] = None
    phase_number: Optional[int] = None
    phase_name: Optional[str] = None
    trail_position: Optional[int] = None
    trail_size: Optional[int] = None
    rationale: Optional[str] = None
    # Campos de celebração (kind=celebrate)
    celebration_message: Optional[str] = None
    next_step_message: Optional[str] = None
    badge_label: Optional[str] = None
    source: Optional[str] = None


class JourneyOverviewOut(BaseModel):
    trail: Optional[dict] = None
    phases: List[PhaseProgressOut]
    recommendation: CatalystRecommendationOut


class SubmitResponseRequest(BaseModel):
    activity_id: int
    response_data: dict


class SubmitResponseOut(BaseModel):
    is_correct: Optional[bool]
    # Gabarito revelado somente quando a resposta está incorreta.
    correct_answer: Optional[str] = None
    score: int
    feedback: str
    feedback_agent: str = "mentor"
    evaluation_status: Optional[str] = None
    attempt_number: int
    reinforcement: Optional[AgentInsightOut] = None
    mission_completed: bool
    attempt_finished: bool = False
    points_earned: int
    coins_earned: int = 0
    new_achievements: List[str] = []
    score_percent: Optional[float] = None
    passed: Optional[bool] = None
    must_retry: Optional[bool] = None
    can_retry_optionally: Optional[bool] = None
    mission_insight: Optional[AgentInsightOut] = None
    next_step: Optional[CatalystRecommendationOut] = None
    # Presente apenas quando a missão concluiu uma trilha pela primeira vez.
    trail_celebration: Optional[CatalystRecommendationOut] = None


class RetryMissionRequest(BaseModel):
    voluntary: bool = False


class LessonStepOut(BaseModel):
    index: int
    type: str
    title: str
    body: Optional[str] = None
    agent: Optional[str] = None
    content_type: Optional[str] = None
    highlights: List[str] = []
    activity: Optional[ActivityOut] = None
    user_response: Optional[dict] = None
    completed: bool = False


class LessonNextMissionOut(BaseModel):
    id: int
    number: int
    name: str


class LessonOut(BaseModel):
    mission: MissionOut
    phase: PhaseOut
    competencies: List[CompetencyOut] = []
    steps: List[LessonStepOut]
    current_step: int
    completed_steps: List[int]
    estimated_minutes: int
    status: str
    progress: Optional[UserMissionProgressOut] = None
    score_percent: Optional[float] = None
    passed: Optional[bool] = None
    attempt_finished: bool = False
    must_retry: Optional[bool] = None
    can_retry_optionally: Optional[bool] = None
    next_mission: Optional[LessonNextMissionOut] = None
    mission_insight: Optional[AgentInsightOut] = None
    next_step: Optional[CatalystRecommendationOut] = None


class LessonStepProgressRequest(BaseModel):
    step_index: int


class LessonStepProgressOut(BaseModel):
    current_step: int
    completed_steps: List[int]
    mission_completed: bool
