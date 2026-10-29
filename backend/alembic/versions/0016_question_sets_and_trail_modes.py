"""question_sets e user_mission_attempts — rotação de conjuntos de perguntas

Revision ID: 0016
Revises: 0015
Create Date: 2026-10-25 00:00:00.000000

Esta migration:
1. Adiciona coluna `question_set INTEGER DEFAULT 1 NOT NULL` em `activities`.
2. Cria tabela `user_mission_attempts` com as colunas necessárias para
   registrar a tentativa e o conjunto usado por cada usuário em cada missão.

Idempotência: usuários existentes não perdem progresso. O campo `question_set`
assume default 1 para todas as atividades existentes. Os campos `trail_modes`
e `trail_1_auto_concluded` vivem dentro do JSONB `profiles.trail` — nenhuma
coluna nova em `profiles` é necessária.
"""
import sqlalchemy as sa
from alembic import op

revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Adicionar question_set em activities ─────────────────────────────
    op.add_column(
        "activities",
        sa.Column(
            "question_set",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    # ── 2. Criar tabela user_mission_attempts ───────────────────────────────
    op.create_table(
        "user_mission_attempts",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "mission_id",
            sa.BigInteger(),
            sa.ForeignKey("missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("question_set_used", sa.Integer(), nullable=False),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_index(
        "ix_user_mission_attempts_user_mission",
        "user_mission_attempts",
        ["user_id", "mission_id"],
    )

    # ── 3. Semear conjuntos 2 e 3 da Trilha 1 ──────────────────────────────
    from app.modules.content.seeds.trail_1_v2 import TRAIL_1_V2
    from app.modules.content.seeds.seeder import seed_phase_content

    bind = op.get_bind()
    seed_phase_content(bind, TRAIL_1_V2, "seed:trail_1_v2:0016")


def downgrade() -> None:
    op.drop_index(
        "ix_user_mission_attempts_user_mission",
        table_name="user_mission_attempts",
    )
    op.drop_table("user_mission_attempts")
    op.drop_column("activities", "question_set")
