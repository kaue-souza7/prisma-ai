"""phase 6 content

Revision ID: 0008
Revises: 0007
Create Date: 2026-10-22 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

from app.modules.content.seeds.phase_6 import seed_phase_6

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    seed_phase_6(op.get_bind())

    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('fase_6_concluida',
             'Guardião digital',
             'Concluiu as 4 missões da Fase 6, incluindo o desafio integrador.',
             'phase_complete'::achievementconditiontype,
             '{"phase_number": 6}'::jsonb,
             TRUE)
        ON CONFLICT (key) DO NOTHING
        """
    )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM content_items WHERE created_by = 'seed:phase_6_v1'")
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM missions
            WHERE phase_id = (SELECT id FROM phases WHERE number = 6)
              AND number IN (1, 2, 3, 4)
            """
        )
    )
    bind.execute(
        sa.text("DELETE FROM achievements WHERE key = 'fase_6_concluida'")
    )
