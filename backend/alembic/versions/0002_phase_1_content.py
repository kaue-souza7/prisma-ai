"""phase 1 content

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-21 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

from app.modules.content.seeds.phase_1 import seed_phase_1

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "competencies",
        sa.Column("code", sa.String(20), nullable=True),
    )
    op.create_unique_constraint(
        "uq_competencies_mission_code",
        "competencies",
        ["mission_id", "code"],
    )

    seed_phase_1(op.get_bind())


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text(
            """
            DELETE FROM content_items
            WHERE created_by = 'seed:phase_1_v1'
            """
        )
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM missions
            WHERE phase_id = (SELECT id FROM phases WHERE number = 1)
              AND number IN (1, 2, 3)
            """
        )
    )
    op.drop_constraint(
        "uq_competencies_mission_code",
        "competencies",
        type_="unique",
    )
    op.drop_column("competencies", "code")
