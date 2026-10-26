"""initial schema

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enums
    op.execute("CREATE TYPE userrole AS ENUM ('student', 'admin')")
    op.execute("CREATE TYPE missionstatus AS ENUM ('locked', 'available', 'in_progress', 'completed')")
    op.execute("CREATE TYPE competencystatus AS ENUM ('not_started', 'developing', 'demonstrated')")
    op.execute("CREATE TYPE achievementconditiontype AS ENUM ('onboarding_complete', 'mission_complete', 'phase_complete', 'mission_first_attempt', 'points_threshold')")

    # users
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", postgresql.ENUM("student", "admin", name="userrole", create_type=False), default="student", nullable=False),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("verification_token", sa.String(255), nullable=True),
        sa.Column("password_reset_token", sa.String(255), nullable=True),
        sa.Column("password_reset_expires", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # profiles
    op.create_table(
        "profiles",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("personal_goal", sa.String(500), nullable=True),
        sa.Column("knowledge_level", sa.String(50), nullable=True),
        sa.Column("onboarding_completed", sa.Boolean, default=False, nullable=False),
        sa.Column("consent_given", sa.Boolean, default=False, nullable=False),
        sa.Column("consent_version", sa.String(20), nullable=True),
        sa.Column("consent_given_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("preferences", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # phases
    op.create_table(
        "phases",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("number", sa.Integer, unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
    )

    # missions
    op.create_table(
        "missions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("phase_id", sa.Integer, sa.ForeignKey("phases.id", ondelete="CASCADE"), nullable=False),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("is_required", sa.Boolean, default=True, nullable=False),
        sa.Column("passing_score", sa.Integer, default=70, nullable=False),
        sa.UniqueConstraint("phase_id", "number"),
    )

    # competencies
    op.create_table(
        "competencies",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_essential", sa.Boolean, default=True, nullable=False),
    )

    # activities
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("activity_type", sa.String(50), nullable=False),
        sa.Column("content", JSONB, nullable=False),
        sa.Column("points_value", sa.Integer, default=0, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
    )

    # user_mission_progress
    op.create_table(
        "user_mission_progress",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", postgresql.ENUM("locked", "available", "in_progress", "completed", name="missionstatus", create_type=False), default="locked", nullable=False),
        sa.Column("score", sa.Integer, nullable=True),
        sa.Column("attempts", sa.Integer, default=0, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "mission_id"),
    )

    # user_competency_progress
    op.create_table(
        "user_competency_progress",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("competency_id", sa.Integer, sa.ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", postgresql.ENUM("not_started", "developing", "demonstrated", name="competencystatus", create_type=False), default="not_started", nullable=False),
        sa.Column("incorrect_count", sa.Integer, default=0, nullable=False),
        sa.Column("correct_count", sa.Integer, default=0, nullable=False),
        sa.Column("reinforcement_suggested", sa.Boolean, default=False, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "competency_id"),
    )

    # user_points
    op.create_table(
        "user_points",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("total_points", sa.Integer, default=0, nullable=False),
        sa.Column("level", sa.Integer, default=1, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # achievements
    op.create_table(
        "achievements",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(100), unique=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("condition_type", postgresql.ENUM("onboarding_complete", "mission_complete", "phase_complete", "mission_first_attempt", "points_threshold", name="achievementconditiontype", create_type=False), nullable=False),
        sa.Column("condition_value", JSONB, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
    )

    # user_achievements
    op.create_table(
        "user_achievements",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("achievement_id", sa.Integer, sa.ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("earned_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "achievement_id"),
    )

    # user_responses
    op.create_table(
        "user_responses",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("activity_id", sa.Integer, sa.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("response_data", JSONB, nullable=False),
        sa.Column("is_correct", sa.Boolean, nullable=True),
        sa.Column("score", sa.Integer, default=0, nullable=False),
        sa.Column("attempt_number", sa.Integer, default=1, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # conversations
    op.create_table(
        "conversations",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("agent", sa.String(50), nullable=False),
        sa.Column("messages", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # content_items
    op.create_table(
        "content_items",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mission_id", sa.Integer, sa.ForeignKey("missions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("content_type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(300), nullable=True),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("order", sa.Integer, default=0, nullable=False),
        sa.Column("is_published", sa.Boolean, default=False, nullable=False),
        sa.Column("created_by", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # Seed: 6 fases
    op.bulk_insert(
        sa.table(
            "phases",
            sa.column("number", sa.Integer),
            sa.column("name", sa.String),
            sa.column("description", sa.Text),
            sa.column("order", sa.Integer),
            sa.column("is_active", sa.Boolean),
        ),
        [
            {"number": 1, "name": "Primeiro salário", "description": "Compreender renda, prioridades e organização inicial do dinheiro.", "order": 1, "is_active": True},
            {"number": 2, "name": "Seu dinheiro no digital", "description": "Compreender meios de pagamento digitais, débito, crédito e cuidados com transações.", "order": 2, "is_active": True},
            {"number": 3, "name": "Por que poupar", "description": "Desenvolver compreensão de objetivos financeiros, planejamento e preparação para imprevistos.", "order": 3, "is_active": True},
            {"number": 4, "name": "Juros: a favor e contra você", "description": "Compreender como juros, tempo, atrasos e condições de crédito afetam o valor total de uma decisão financeira.", "order": 4, "is_active": True},
            {"number": 5, "name": "Onde o dinheiro rende", "description": "Introduzir a relação entre inflação, poder de compra, poupança e características básicas de alternativas de investimento.", "order": 5, "is_active": True},
            {"number": 6, "name": "Proteção digital", "description": "Desenvolver a capacidade de reconhecer riscos digitais e tomar decisões seguras diante de possíveis fraudes financeiras.", "order": 6, "is_active": True},
        ],
    )

    # Seed: conquistas da Fase 1
    # Os valores do enum são literais fixos; o CAST explícito evita que o
    # PostgreSQL receba o parâmetro como VARCHAR em uma coluna ENUM.
    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('primeiro_passo', 'Primeiro passo', 'Concluiu o onboarding.',
             'onboarding_complete'::achievementconditiontype, NULL, TRUE),
            ('planejador_iniciante', 'Planejador iniciante', 'Concluiu as 3 missões da Fase 1.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 1}'::jsonb, TRUE),
            ('sem_duvidas', 'Sem dúvidas', 'Concluiu uma missão sem intervenção do Mentor.',
             'mission_first_attempt'::achievementconditiontype, NULL, TRUE)
        """
    )


def downgrade() -> None:
    op.drop_table("content_items")
    op.drop_table("conversations")
    op.drop_table("user_responses")
    op.drop_table("user_achievements")
    op.drop_table("achievements")
    op.drop_table("user_points")
    op.drop_table("user_competency_progress")
    op.drop_table("user_mission_progress")
    op.drop_table("activities")
    op.drop_table("competencies")
    op.drop_table("missions")
    op.drop_table("phases")
    op.drop_table("profiles")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS achievementconditiontype")
    op.execute("DROP TYPE IF EXISTS competencystatus")
    op.execute("DROP TYPE IF EXISTS missionstatus")
    op.execute("DROP TYPE IF EXISTS userrole")
