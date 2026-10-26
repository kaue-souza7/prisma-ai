"""module copy

Revision ID: 0012
Revises: 0011
Create Date: 2026-10-23 00:00:00.000000

Renomeia a palavra "minicurso" no texto dos roteiros já publicados. A mudança
é somente de cópia: nenhuma chave, rota ou estrutura do `lesson_flow` muda.
"""
from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE missions
        SET lesson_flow = replace(lesson_flow::text, 'Neste minicurso', 'Neste módulo')::jsonb
        WHERE lesson_flow::text LIKE '%Neste minicurso%'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE missions
        SET lesson_flow = replace(lesson_flow::text, 'Neste módulo', 'Neste minicurso')::jsonb
        WHERE lesson_flow::text LIKE '%Neste módulo%'
        """
    )
