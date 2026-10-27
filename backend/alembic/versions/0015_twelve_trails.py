"""twelve trails — reorganização curricular de 6 fases para 12 trilhas

Revision ID: 0015
Revises: 0014
Create Date: 2026-10-24 00:00:00.000000

Esta migration:
1. Insere 6 novas fases (trilhas 7–12, numbers 7–12).
2. Semeia o conteúdo das trilhas 7–12 via seeds dedicados.

As fases 1–6 (trilhas 1–6) são preservadas intactas. Suas missões existentes
permanecem com os mesmos IDs. O conteúdo expandido das trilhas 1–6 entra via
seeds separados chamados nesta mesma migration.

Compatibilidade: progresso de usuários (user_mission_progress,
user_competency_progress) não é alterado. Novas missões entram como 'locked'
para usuários existentes, o que é o comportamento correto do sistema.

Reversão: o downgrade remove apenas os dados inseridos nesta migration.
"""
import sqlalchemy as sa
from alembic import op

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 0. Renomear phases 1–6 para os nomes das novas trilhas temáticas ───
    #
    # As phases 1–6 existentes correspondem, respectivamente, às trilhas 1–6.
    # A fase 1 do banco já tem o conteúdo correto e apenas recebe nome novo.
    # As fases 2–6 são renomeadas para refletir a nova organização pedagógica.
    # Os IDs e mission_ids NÃO mudam — preserva progresso de usuários.
    bind_pre = op.get_bind()
    rename_map = {
        1: ("Meu primeiro salário",
            "Compreenda o holerite, o salário líquido, o INSS, o IRRF e os direitos "
            "trabalhistas como 13º e férias."),
        2: ("Orçamento na prática",
            "Organize o orçamento mensal, identifique gastos invisíveis e mantenha "
            "o controle das suas despesas."),
        3: ("Pagamentos do dia a dia",
            "Compare Pix, débito, crédito e carteiras digitais e escolha o meio "
            "certo para cada compra."),
        4: ("Cartão e fatura",
            "Entenda o ciclo do cartão de crédito, a fatura, o pagamento mínimo e "
            "as consequências do crédito rotativo."),
        5: ("Metas e reserva",
            "Formule metas financeiras e calcule o tamanho ideal da sua reserva de "
            "emergência com base no seu perfil."),
        6: ("Guardar sem perder o controle",
            "Aplique a estratégia de separar o dinheiro no recebimento e adapte o "
            "método para qualquer perfil de renda."),
    }
    for phase_number, (new_name, new_desc) in rename_map.items():
        bind_pre.execute(
            sa.text(
                "UPDATE phases SET name = :name, description = :desc "
                "WHERE number = :num"
            ).bindparams(name=new_name, desc=new_desc, num=phase_number)
        )

    # ── 1. Inserir fases 7–12 (trilhas novas) ──────────────────────────────
    op.bulk_insert(
        sa.table(
            "phases",
            sa.column("number", sa.Integer),
            sa.column("name", sa.String),
            sa.column("description", sa.Text),
            sa.column("order", sa.Integer),
            sa.column("is_active", sa.Boolean),
        ),
        [
            {
                "number": 7,
                "name": "Juros e parcelas",
                "description": (
                    "Calcule o custo real do crédito, interprete o CET e avalie "
                    "ofertas de parcelamento com senso crítico."
                ),
                "order": 7,
                "is_active": True,
            },
            {
                "number": 8,
                "name": "Dívida que cresce",
                "description": (
                    "Interprete o crescimento de dívidas, calcule o impacto do "
                    "pagamento mínimo e trace estratégias de saída."
                ),
                "order": 8,
                "is_active": True,
            },
            {
                "number": 9,
                "name": "Inflação e poder de compra",
                "description": (
                    "Compreenda o IPCA, calcule o impacto da inflação no seu "
                    "orçamento e aprenda a diferença entre rendimento nominal e real."
                ),
                "order": 9,
                "is_active": True,
            },
            {
                "number": 10,
                "name": "Onde o dinheiro rende",
                "description": (
                    "Conheça os fundamentos da renda fixa, o FGC e a tributação "
                    "para comparar produtos e tomar decisões de investimento informadas."
                ),
                "order": 10,
                "is_active": True,
            },
            {
                "number": 11,
                "name": "Golpes e proteção de dados",
                "description": (
                    "Reconheça fraudes digitais, proteja seus dados e saiba como "
                    "agir corretamente após um golpe financeiro."
                ),
                "order": 11,
                "is_active": True,
            },
            {
                "number": 12,
                "name": "Desafio integrador",
                "description": (
                    "Aplique as competências de todas as trilhas anteriores em "
                    "cenários reais de decisão financeira. Esta é a culminação da jornada."
                ),
                "order": 12,
                "is_active": True,
            },
        ],
    )

    # ── 2. Inserir conquistas para as novas trilhas ─────────────────────────
    op.execute(
        """
        INSERT INTO achievements
            (key, name, description, condition_type, condition_value, is_active)
        VALUES
            ('trilha_juros', 'Custo real', 'Concluiu a trilha Juros e parcelas.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 7}'::jsonb, TRUE),
            ('trilha_divida', 'Plano de saída', 'Concluiu a trilha Dívida que cresce.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 8}'::jsonb, TRUE),
            ('trilha_inflacao', 'Poder de compra', 'Concluiu a trilha Inflação e poder de compra.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 9}'::jsonb, TRUE),
            ('trilha_rendimentos', 'Onde rende', 'Concluiu a trilha Onde o dinheiro rende.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 10}'::jsonb, TRUE),
            ('trilha_seguranca', 'Bem protegido', 'Concluiu a trilha Golpes e proteção de dados.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 11}'::jsonb, TRUE),
            ('desafio_integrador', 'Jornada concluída', 'Concluiu o Desafio integrador.',
             'phase_complete'::achievementconditiontype, '{"phase_number": 12}'::jsonb, TRUE)
        """
    )

    # ── 3. Semear conteúdo das trilhas 7–12 ────────────────────────────────
    # Os seeds são importados e chamados dentro da migration para que o
    # conteúdo seja idempotente (mesmas chaves naturais) e versionado.
    from app.modules.content.seeds.trail_7_v1 import TRAIL_7_V1
    from app.modules.content.seeds.trail_8_v1 import TRAIL_8_V1
    from app.modules.content.seeds.trail_9_v1 import TRAIL_9_V1
    from app.modules.content.seeds.trail_10_v1 import TRAIL_10_V1
    from app.modules.content.seeds.trail_11_v1 import TRAIL_11_V1
    from app.modules.content.seeds.trail_12_v1 import TRAIL_12_V1
    from app.modules.content.seeds.seeder import seed_phase_content

    bind = op.get_bind()
    for data, tag in [
        (TRAIL_7_V1, "seed:trail_7_v1"),
        (TRAIL_8_V1, "seed:trail_8_v1"),
        (TRAIL_9_V1, "seed:trail_9_v1"),
        (TRAIL_10_V1, "seed:trail_10_v1"),
        (TRAIL_11_V1, "seed:trail_11_v1"),
        (TRAIL_12_V1, "seed:trail_12_v1"),
    ]:
        seed_phase_content(bind, data, tag)

    # ── 4. Semear conteúdo expandido das trilhas 1–6 ───────────────────────
    from app.modules.content.seeds.trail_1_v2 import TRAIL_1_V2
    from app.modules.content.seeds.trail_2_v1 import TRAIL_2_V1
    from app.modules.content.seeds.trail_3_v1 import TRAIL_3_V1
    from app.modules.content.seeds.trail_4_v1 import TRAIL_4_V1
    from app.modules.content.seeds.trail_5_v1 import TRAIL_5_V1
    from app.modules.content.seeds.trail_6_v1 import TRAIL_6_V1

    for data, tag in [
        (TRAIL_1_V2, "seed:trail_1_v2"),
        (TRAIL_2_V1, "seed:trail_2_v1"),
        (TRAIL_3_V1, "seed:trail_3_v1"),
        (TRAIL_4_V1, "seed:trail_4_v1"),
        (TRAIL_5_V1, "seed:trail_5_v1"),
        (TRAIL_6_V1, "seed:trail_6_v1"),
    ]:
        seed_phase_content(bind, data, tag)


def downgrade() -> None:
    # Remove apenas o conteúdo inserido por esta migration.
    # O progresso de usuários NÃO é removido (chave estrangeira ON DELETE CASCADE
    # protege integridade; mas remover fases remove as missões e o progresso
    # associado — por isso este downgrade é destrutivo e não deve ser executado
    # em produção sem backup).
    bind = op.get_bind()

    # Remover missões das novas trilhas (phase numbers 7–12)
    # As missões das trilhas 1–6 expandidas permanecem (são atualizações, não inserções)
    bind.execute(
        sa.text(
            """
            DELETE FROM missions WHERE phase_id IN (
                SELECT id FROM phases WHERE number >= 7
            )
            """
        )
    )
    bind.execute(
        sa.text("DELETE FROM phases WHERE number >= 7")
    )
    bind.execute(
        sa.text(
            """
            DELETE FROM achievements WHERE key IN (
                'trilha_juros', 'trilha_divida', 'trilha_inflacao',
                'trilha_rendimentos', 'trilha_seguranca', 'desafio_integrador'
            )
            """
        )
    )
