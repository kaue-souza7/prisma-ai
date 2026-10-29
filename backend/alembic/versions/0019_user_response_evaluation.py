"""Avaliação imediata de respostas abertas

Revision ID: 0019
Revises: 0018
Create Date: 2026-10-29 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user_responses",
        sa.Column("feedback", sa.Text(), nullable=True),
    )
    op.add_column(
        "user_responses",
        sa.Column("evaluation_status", sa.String(length=20), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_responses", "evaluation_status")
    op.drop_column("user_responses", "feedback")
