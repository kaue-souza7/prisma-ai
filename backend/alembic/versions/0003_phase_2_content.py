"""phase 2 content

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-21 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

from app.modules.content.seeds.phase_2 import seed_phase_2

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    seed_phase_2(op.get_bind())

    # Conquistas da Fase 2
    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('digital_consciente',
             'Digital consciente',
             'Concluiu as 3 missões da Fase 2.',
             'phase_complete'::achievementconditiontype,
             '{"phase_number": 2}'::jsonb,
             TRUE)
        ON CONFLICT (key) DO NOTHING
        """
    )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text(
            "DELETE FROM content_items WHERE created_by = 'seed:phase_2_v1'"
        )
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM missions
            WHERE phase_id = (SELECT id FROM phases WHERE number = 2)
              AND number IN (1, 2, 3)
            """
        )
    )
    bind.execute(
        sa.text("DELETE FROM achievements WHERE key = 'digital_consciente'")
    )
