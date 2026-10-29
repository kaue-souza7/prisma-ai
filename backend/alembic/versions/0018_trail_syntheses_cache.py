"""trail_syntheses — cache persistido da síntese do Analista (D-A1)

Revision ID: 0018
Revises: 0017
Create Date: 2026-10-28 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0018"
down_revision = "0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trail_syntheses",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "trail_id",
            sa.Integer(),
            sa.ForeignKey("phases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("short", sa.String(length=500), nullable=False),
        sa.Column("full", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False, server_default="fallback"),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("user_id", "trail_id", name="uq_trail_synthesis_user_trail"),
    )
    op.create_index(
        "ix_trail_syntheses_user_id", "trail_syntheses", ["user_id"]
    )
    op.create_index(
        "ix_trail_syntheses_trail_id", "trail_syntheses", ["trail_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_trail_syntheses_trail_id", table_name="trail_syntheses")
    op.drop_index("ix_trail_syntheses_user_id", table_name="trail_syntheses")
    op.drop_table("trail_syntheses")
