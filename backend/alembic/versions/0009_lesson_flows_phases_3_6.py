"""lesson flows for phases 3 to 6

Revision ID: 0009
Revises: 0008
Create Date: 2026-10-22 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

from app.modules.content.lesson_flows import LESSON_FLOWS

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
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
        if phase_number < 3:
            continue
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

    for phase_number in (3, 4, 5, 6):
        phase_id = bind.execute(
            sa.select(phases.c.id).where(phases.c.number == phase_number)
        ).scalar_one_or_none()
        if phase_id is None:
            continue
        bind.execute(
            sa.update(missions)
            .where(missions.c.phase_id == phase_id)
            .values(lesson_flow=None)
        )
