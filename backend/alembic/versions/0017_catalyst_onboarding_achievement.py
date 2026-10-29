"""achievement trilha_1_dominada_onboarding — Catalisador reconhece Trilha 1 no onboarding

Revision ID: 0017
Revises: 0016
Create Date: 2026-10-26 00:00:00.000000

Adiciona o achievement concedido quando o Catalisador reconhece que o usuário
já domina os conteúdos da Trilha 1 durante o onboarding conversacional (D-C5,
D-C6, D-C7). Condição: `onboarding_complete` — concedido imediatamente após
o onboarding, apenas quando `trail_1_auto_concluded=true`.
"""
from alembic import op

revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            (
                'trilha_1_dominada_onboarding',
                'Meu primeiro salário — Dominada no onboarding',
                'O Catalisador reconheceu seu conhecimento de contracheque antes mesmo de começar.',
                'onboarding_complete'::achievementconditiontype,
                '{"trail_1_auto_concluded": true}'::jsonb,
                TRUE
            )
        ON CONFLICT (key) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM achievements WHERE key = 'trilha_1_dominada_onboarding'
        """
    )
