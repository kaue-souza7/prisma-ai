"""phase 4 content

Revision ID: 0006
Revises: 0005
Create Date: 2026-10-22 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

from app.modules.content.seeds.phase_4 import seed_phase_4

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    seed_phase_4(op.get_bind())

    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('fase_4_concluida',
             'Mestre dos juros',
             'Concluiu as 3 missões da Fase 4.',
             'phase_complete'::achievementconditiontype,
             '{"phase_number": 4}'::jsonb,
             TRUE)
        ON CONFLICT (key) DO NOTHING
        """
    )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM content_items WHERE created_by = 'seed:phase_4_v1'")
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM missions
            WHERE phase_id = (SELECT id FROM phases WHERE number = 4)
              AND number IN (1, 2, 3)
            """
        )
    )
    bind.execute(
        sa.text("DELETE FROM achievements WHERE key = 'fase_4_concluida'")
    )
