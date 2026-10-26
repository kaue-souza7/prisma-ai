"""prism economy and studio library

Revision ID: 0013
Revises: 0012
Create Date: 2026-10-23 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Prismas são uma moeda separada dos pontos de progressão.
    op.add_column(
        "user_points",
        sa.Column("coins", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "generated_contents",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("format", sa.String(length=30), nullable=False),
        sa.Column(
            "phase_id",
            sa.Integer(),
            sa.ForeignKey("phases.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "mission_id",
            sa.Integer(),
            sa.ForeignKey("missions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("style_hint", sa.Text(), nullable=True),
        sa.Column(
            "content",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "coins_spent",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="generating",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_generated_contents_user_created",
        "generated_contents",
        ["user_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_generated_contents_user_created",
        table_name="generated_contents",
    )
    op.drop_table("generated_contents")
    op.drop_column("user_points", "coins")
