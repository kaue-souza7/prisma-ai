import enum
from datetime import datetime, timezone
from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, Float, ForeignKey,
    Index, Integer, String, Text, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"


class MissionStatus(str, enum.Enum):
    locked = "locked"
    available = "available"
    in_progress = "in_progress"
    completed = "completed"


class CompetencyStatus(str, enum.Enum):
    not_started = "not_started"
    developing = "developing"
    demonstrated = "demonstrated"


class AchievementConditionType(str, enum.Enum):
    onboarding_complete = "onboarding_complete"
    mission_complete = "mission_complete"
    phase_complete = "phase_complete"
    mission_first_attempt = "mission_first_attempt"
    points_threshold = "points_threshold"


# ─────────────────────────────────────────────
# Usuários e autenticação
# ─────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.student, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    verification_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_reset_expires: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    points: Mapped["UserPoints"] = relationship("UserPoints", back_populates="user", uselist=False, cascade="all, delete-orphan")
    mission_progress: Mapped[list["UserMissionProgress"]] = relationship("UserMissionProgress", back_populates="user", cascade="all, delete-orphan")
    competency_progress: Mapped[list["UserCompetencyProgress"]] = relationship("UserCompetencyProgress", back_populates="user", cascade="all, delete-orphan")
    achievements: Mapped[list["UserAchievement"]] = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    responses: Mapped[list["UserResponse"]] = relationship("UserResponse", back_populates="user", cascade="all, delete-orphan")
    conversations: Mapped[list["Conversation"]] = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# Perfil
# ─────────────────────────────────────────────

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    personal_goal: Mapped[str | None] = mapped_column(String(500), nullable=True)
    knowledge_level: Mapped[str | None] = mapped_column(String(50), nullable=True)  # beginner | intermediate | advanced
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_version: Mapped[str | None] = mapped_column(String(20), nullable=True)
    consent_given_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    preferences: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # Trilha personalizada do estudante. Gerada por regras determinísticas no
    # MVP e preparada para receber uma trilha validada do Catalisador IA.
    trail: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profile")


# ─────────────────────────────────────────────
# Jornada de aprendizagem
# ─────────────────────────────────────────────

class Phase(Base):
    __tablename__ = "phases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    missions: Mapped[list["Mission"]] = relationship("Mission", back_populates="phase", order_by="Mission.order")


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phase_id: Mapped[int] = mapped_column(ForeignKey("phases.id", ondelete="CASCADE"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    passing_score: Mapped[int] = mapped_column(Integer, default=70, nullable=False)  # 70 ou 100
    lesson_flow: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    phase: Mapped["Phase"] = relationship("Phase", back_populates="missions")
    competencies: Mapped[list["Competency"]] = relationship("Competency", back_populates="mission", cascade="all, delete-orphan")
    activities: Mapped[list["Activity"]] = relationship("Activity", back_populates="mission", order_by="Activity.order", cascade="all, delete-orphan")
    progress: Mapped[list["UserMissionProgress"]] = relationship("UserMissionProgress", back_populates="mission")

    __table_args__ = (UniqueConstraint("phase_id", "number"),)


class Competency(Base):
    __tablename__ = "competencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str | None] = mapped_column(String(20), nullable=True)  # ex.: 1.1.1
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_essential: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    mission: Mapped["Mission"] = relationship("Mission", back_populates="competencies")
    user_progress: Mapped[list["UserCompetencyProgress"]] = relationship("UserCompetencyProgress", back_populates="competency")

    __table_args__ = (UniqueConstraint("mission_id", "code"),)


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # multiple_choice | open_text | simulation
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)  # enunciado, opções, resposta esperada, critério
    points_value: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    question_set: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    mission: Mapped["Mission"] = relationship("Mission", back_populates="activities")
    responses: Mapped[list["UserResponse"]] = relationship("UserResponse", back_populates="activity")


# ─────────────────────────────────────────────
# Progresso e gamificação
# ─────────────────────────────────────────────

class UserMissionProgress(Base):
    __tablename__ = "user_mission_progress"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), default=MissionStatus.locked, nullable=False)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_steps: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="mission_progress")
    mission: Mapped["Mission"] = relationship("Mission", back_populates="progress")

    __table_args__ = (UniqueConstraint("user_id", "mission_id"),)


class TrailSynthesisRecord(Base):
    """Cache persistido da síntese do Analista por usuário e trilha (D-A1)."""

    __tablename__ = "trail_syntheses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    trail_id: Mapped[int] = mapped_column(
        ForeignKey("phases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    short: Mapped[str] = mapped_column(String(500), nullable=False)
    full: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="fallback")
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )

    __table_args__ = (UniqueConstraint("user_id", "trail_id"),)


class UserCompetencyProgress(Base):
    __tablename__ = "user_competency_progress"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    competency_id: Mapped[int] = mapped_column(ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[CompetencyStatus] = mapped_column(Enum(CompetencyStatus), default=CompetencyStatus.not_started, nullable=False)
    incorrect_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reinforcement_suggested: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="competency_progress")
    competency: Mapped["Competency"] = relationship("Competency", back_populates="user_progress")

    __table_args__ = (UniqueConstraint("user_id", "competency_id"),)


class UserPoints(Base):
    __tablename__ = "user_points"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Prismas: moeda separada dos pontos de progressão. Gasta no Estúdio.
    coins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="points")


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_type: Mapped[AchievementConditionType] = mapped_column(Enum(AchievementConditionType), nullable=False)
    condition_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user_achievements: Mapped[list["UserAchievement"]] = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="achievements")
    achievement: Mapped["Achievement"] = relationship("Achievement", back_populates="user_achievements")

    __table_args__ = (UniqueConstraint("user_id", "achievement_id"),)


# ─────────────────────────────────────────────
# Respostas
# ─────────────────────────────────────────────

class UserResponse(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Exercícios extras do Estúdio não pertencem a uma missão/atividade do
    # currículo; por isso as duas referências são opcionais.
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), nullable=True)
    activity_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)
    response_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # Tentativa do módulo à qual esta resposta pertence. Cada atividade pode
    # ser respondida uma única vez por tentativa; o histórico fica preservado.
    mission_attempt: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="responses")
    mission: Mapped["Mission"] = relationship("Mission")
    activity: Mapped["Activity"] = relationship("Activity", back_populates="responses")


# ─────────────────────────────────────────────
# Tentativas de missão (rotação de conjuntos)
# ─────────────────────────────────────────────

class UserMissionAttempt(Base):
    __tablename__ = "user_mission_attempts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mission_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_set_used: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_user_mission_attempts_user_mission", "user_id", "mission_id"),
    )


# ─────────────────────────────────────────────
# Estúdio de Prismas
# ─────────────────────────────────────────────

class GeneratedContent(Base):
    """Conteúdo gerado pelo Estúdio e salvo na biblioteca pessoal."""

    __tablename__ = "generated_contents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    format: Mapped[str] = mapped_column(String(30), nullable=False)  # revisao | flashcards | exercicios
    phase_id: Mapped[int | None] = mapped_column(ForeignKey("phases.id", ondelete="SET NULL"), nullable=True)
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id", ondelete="SET NULL"), nullable=True)
    style_hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    coins_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="generating", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User")
    phase: Mapped["Phase"] = relationship("Phase")
    mission: Mapped["Mission"] = relationship("Mission")

    __table_args__ = (
        Index("ix_generated_contents_user_created", "user_id", "created_at"),
    )


# ─────────────────────────────────────────────
# Conversas (reservado para IA — Etapa 2)
# ─────────────────────────────────────────────

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id", ondelete="SET NULL"), nullable=True)
    agent: Mapped[str] = mapped_column(String(50), nullable=False)  # mentor | analyst
    messages: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="conversations")


# ─────────────────────────────────────────────
# Conteúdo educacional
# ─────────────────────────────────────────────

class ContentItem(Base):
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id", ondelete="SET NULL"), nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)  # explanation | example | tip
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
