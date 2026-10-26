"""studio responses without curriculum activity

Revision ID: 0014
Revises: 0013
Create Date: 2026-10-23 00:00:00.000000

Exercícios extras do Estúdio são evidências de prática: ficam em
`user_responses` com `mission_attempt = 0`, sem vínculo com uma missão ou
atividade do currículo.
"""
from alembic import op

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("user_responses", "mission_id", nullable=True)
    op.alter_column("user_responses", "activity_id", nullable=True)


def downgrade() -> None:
    # Remove apenas as respostas de exercícios extras; respostas curriculares
    # continuam íntegras para o downgrade das colunas.
    op.execute("DELETE FROM user_responses WHERE mission_attempt = 0")
    op.alter_column("user_responses", "mission_id", nullable=False)
    op.alter_column("user_responses", "activity_id", nullable=False)
