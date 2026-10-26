"""evaluation model

Revision ID: 0011
Revises: 0010
Create Date: 2026-10-23 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Cada resposta passa a pertencer a uma tentativa do módulo. Respostas
    # antigas são tratadas como pertencentes à primeira tentativa.
    op.add_column(
        "user_responses",
        sa.Column(
            "mission_attempt",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )
    # Percentual de acerto da melhor tentativa aprovada do módulo. É nullable
    # para preservar registros anteriores ao novo modelo de avaliação.
    op.add_column(
        "user_mission_progress",
        sa.Column("score_percent", sa.Float(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_mission_progress", "score_percent")
    op.drop_column("user_responses", "mission_attempt")
