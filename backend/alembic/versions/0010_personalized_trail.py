"""personalized trail

Revision ID: 0010
Revises: 0009
Create Date: 2026-10-23 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # A trilha é um dado do perfil, não uma regra fixa de código. O backend
    # continua sendo a autoridade: só persiste trilhas que passam na validação
    # de fases existentes e ordem completa.
    op.add_column("profiles", sa.Column("trail", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("profiles", "trail")
