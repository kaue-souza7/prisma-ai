"""phase 5 content

Revision ID: 0007
Revises: 0006
Create Date: 2026-10-22 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

from app.modules.content.seeds.phase_5 import seed_phase_5

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    seed_phase_5(op.get_bind())

    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('fase_5_concluida',
             'Investidor iniciante',
             'Concluiu as 3 missões da Fase 5.',
             'phase_complete'::achievementconditiontype,
             '{"phase_number": 5}'::jsonb,
             TRUE)
        ON CONFLICT (key) DO NOTHING
        """
    )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM content_items WHERE created_by = 'seed:phase_5_v1'")
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM missions
            WHERE phase_id = (SELECT id FROM phases WHERE number = 5)
              AND number IN (1, 2, 3)
            """
        )
    )
    bind.execute(
        sa.text("DELETE FROM achievements WHERE key = 'fase_5_concluida'")
    )
