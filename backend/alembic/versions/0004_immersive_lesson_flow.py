"""immersive lesson flow

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-21 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

from app.modules.content.lesson_flows import LESSON_FLOWS

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("missions", sa.Column("lesson_flow", JSONB, nullable=True))
    op.add_column(
        "user_mission_progress",
        sa.Column("current_step", sa.Integer, nullable=False, server_default="0"),
    )
    op.add_column(
        "user_mission_progress",
        sa.Column(
            "completed_steps",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )

    bind = op.get_bind()
    phases = sa.table(
        "phases",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("number", sa.Integer),
    )
    missions = sa.table(
        "missions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("phase_id", sa.Integer),
        sa.Column("number", sa.Integer),
        sa.Column("lesson_flow", JSONB),
    )

    for (phase_number, mission_number), flow in LESSON_FLOWS.items():
        phase_id = bind.execute(
            sa.select(phases.c.id).where(phases.c.number == phase_number)
        ).scalar_one_or_none()
        if phase_id is None:
            continue
        bind.execute(
            sa.update(missions)
            .where(
                missions.c.phase_id == phase_id,
                missions.c.number == mission_number,
            )
            .values(lesson_flow=flow)
        )


def downgrade() -> None:
    op.drop_column("user_mission_progress", "completed_steps")
    op.drop_column("user_mission_progress", "current_step")
    op.drop_column("missions", "lesson_flow")
