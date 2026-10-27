"""Conteúdo versionado da Trilha 8 — Dívida que cresce.

phase_number: 8 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-08.md

As taxas nos exemplos são hipotéticas e identificadas como tal.
Este módulo é imutável após publicação.
"""

TRAIL_8_V1 = {
    "phase_number": 8,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 8.1 — Como a dívida cresce
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Como a dívida cresce",
            "description": (
                "Entenda o que compõe uma dívida, calcule seu crescimento "
                "com juros compostos e reconheça por que ignorar é o pior "
                "caminho."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "8.1.1",
                    "name": "Distinguir saldo devedor, juros e encargos",
                    "description": (
                        "Identifica o que é capital original, juro contratual, "
                        "IOF, multa e mora numa dívida."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "8.1.2",
                    "name": "Calcular o crescimento de uma dívida com juros compostos",
                    "description": (
                        "Aplica M = C(1+i)^n para estimar o saldo de uma dívida "
                        "após n períodos sem pagamento."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é o saldo devedor de uma dívida?",
                        "competency_codes": ["8.1.1"],
                        "options": [
                            {"value": "a", "label": "Apenas os juros acumulados."},
                            {
                                "value": "b",
                                "label": (
                                    "O valor total que você ainda deve: capital restante "
                                    "mais juros e encargos acumulados até o momento."
                                ),
                            },
                            {"value": "c", "label": "Só o valor original emprestado."},
                            {"value": "d", "label": "O valor das parcelas pagas até agora."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O saldo devedor é o total que você ainda deve: "
                            "capital restante + juros e encargos acumulados. "
                            "Ele cresce conforme o tempo passa sem pagamento."
                        ),
                        "feedback_incorrect": (
                            "O saldo devedor é o valor total em aberto: capital original "
                            "(ou parte dele, se houve pagamentos) mais juros e encargos "
                            "acumulados. É esse valor que serve de base para o próximo "
                            "cálculo de juros compostos."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual é a diferença entre juros contratuais e multa de mora?",
                        "competency_codes": ["8.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Juros são o custo do crédito ao longo do tempo. "
                                    "Multa de mora é uma penalidade pelo atraso no pagamento."
                                ),
                            },
                            {"value": "b", "label": "São a mesma coisa com nomes diferentes."},
                            {"value": "c", "label": "Multa é sempre maior do que os juros."},
                            {"value": "d", "label": "Juros incidem somente uma vez; multa é mensal."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Juros são o custo contratual do crédito, cobrados "
                            "ao longo do prazo. Multa de mora é uma penalidade adicional "
                            "por atraso no pagamento — geralmente limitada a 2% pelo CDC."
                        ),
                        "feedback_incorrect": (
                            "São encargos distintos: juros remuneratórios são o custo do "
                            "crédito (previstos em contrato). Multa de mora e juros de mora "
                            "são penalidades por atraso. Ambos somam-se ao saldo devedor, "
                            "mas têm origens e regras diferentes."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Dívida de R$ 800,00 a 10% ao mês (composto). "
                            "Sem nenhum pagamento, qual é o saldo em 3 meses? "
                            "(1,10)^3 ≈ 1,331. (Taxa hipotética, para fins didáticos.)"
                        ),
                        "competency_codes": ["8.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 1.064,80."},
                            {"value": "b", "label": "R$ 1.040,00."},
                            {"value": "c", "label": "R$ 1.100,00."},
                            {"value": "d", "label": "R$ 880,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! M = 800 × (1,10)^3 = 800 × 1,331 = R$ 1.064,80. "
                            "Em 3 meses sem pagamento, a dívida cresceu R$ 264,80 — "
                            "33% acima do valor original."
                        ),
                        "feedback_incorrect": (
                            "M = C × (1+i)^n = 800 × (1,10)^3 ≈ 800 × 1,331 = R$ 1.064,80. "
                            "Nos juros compostos, cada mês os juros incidem sobre um "
                            "saldo maior — por isso cresce mais rápido do que o simples."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "R$ 1.200,00 no rotativo do cartão a 15% ao mês (hipotético). "
                            "Dois meses sem nenhum pagamento. "
                            "(1,15)^2 ≈ 1,3225. Qual o saldo aproximado?"
                        ),
                        "competency_codes": ["8.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 1.587,00."},
                            {"value": "b", "label": "R$ 1.560,00."},
                            {"value": "c", "label": "R$ 1.400,00."},
                            {"value": "d", "label": "R$ 1.200,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! M = 1.200 × (1,15)^2 ≈ 1.200 × 1,3225 ≈ R$ 1.587,00. "
                            "Em apenas 2 meses, a dívida cresceu R$ 387 — 32% a mais. "
                            "Isso ilustra por que o rotativo do cartão é considerado "
                            "um dos créditos mais caros."
                        ),
                        "feedback_incorrect": (
                            "M = 1.200 × (1,15)^2 ≈ 1.587. Em 2 meses a 15%/mês "
                            "(hipotético), a dívida cresceu mais de R$ 387. "
                            "O rotativo cobra juros sobre o novo saldo a cada mês."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Explique por que uma dívida no cartão de crédito pode "
                            "ser mais perigosa do que um empréstimo pessoal para o "
                            "mesmo valor, mesmo que o saldo inicial seja idêntico."
                        ),
                        "competency_codes": ["8.1.1", "8.1.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Pontos esperados: (1) a taxa do rotativo costuma ser mais alta "
                            "do que a de empréstimos pessoais; (2) no empréstimo, o prazo e "
                            "as parcelas são fixas e previsíveis; (3) no rotativo, o saldo "
                            "pode crescer indefinidamente se só o mínimo for pago."
                        ),
                        "evaluation_criteria": [
                            "Menciona que a taxa do rotativo tende a ser mais alta.",
                            "Explica que o saldo do rotativo cresce mês a mês se não pago integralmente.",
                            "Compara com a previsibilidade do empréstimo pessoal.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Entre pagar R$ 300,00 hoje numa dívida com 8% ao mês "
                            "ou esperar 3 meses para pagar os mesmos R$ 300,00, "
                            "qual é melhor financeiramente?"
                        ),
                        "competency_codes": ["8.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar hoje — porque cada mês de atraso aumenta o "
                                    "saldo devedor sobre o qual os juros incidem."
                                ),
                            },
                            {"value": "b", "label": "Esperar — os R$ 300 ficam disponíveis por mais tempo."},
                            {"value": "c", "label": "São equivalentes — R$ 300 é R$ 300."},
                            {"value": "d", "label": "Depende da taxa de juros do mês."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Cada mês sem pagamento, os juros incidem sobre um "
                            "saldo maior. Pagar hoje reduz o saldo devedor imediatamente "
                            "e evita que os juros cresçam sobre aquele valor."
                        ),
                        "feedback_incorrect": (
                            "Pagar hoje é sempre melhor numa dívida com juros. "
                            "Esperando 3 meses, o saldo que seus R$ 300 poderiam "
                            "amortizar terá crescido com juros — e seu pagamento "
                            "liquidará menos do que liquidaria hoje."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Saldo devedor: o que é e por que cresce",
                    "order": 1,
                    "body": (
                        "O **saldo devedor** é o valor total que você ainda deve numa "
                        "dívida: capital original (ou o restante dele) mais juros e "
                        "encargos acumulados até o momento da consulta.\n\n"
                        "Enquanto a dívida não é paga, os juros compostos fazem o "
                        "saldo crescer a cada período — mesmo que você não faça "
                        "novas compras ou saques.\n\n"
                        "Por isso, **ignorar uma dívida é sempre a pior estratégia**: "
                        "quanto mais tempo passa, maior é o valor a ser quitado."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Juros, multa e encargos: as diferenças",
                    "order": 2,
                    "body": (
                        "Numa dívida em atraso, podem incidir:\n\n"
                        "- **Juros remuneratórios:** o custo contratual do crédito, "
                        "definido em contrato (ex.: 3% ao mês).\n"
                        "- **Juros de mora:** penalidade pelo atraso, limitada em "
                        "muitos contratos a 1% ao mês.\n"
                        "- **Multa contratual:** aplicada uma vez, geralmente ao "
                        "primeiro atraso (CDC limita a 2%).\n"
                        "- **IOF:** imposto federal sobre operações financeiras.\n\n"
                        "Todos esses valores somam-se ao saldo devedor. No extrato, "
                        "verifique quais estão sendo cobrados e se as taxas batem "
                        "com o contrato."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dívida de R$ 1.000 ao longo do tempo (hipotético)",
                    "order": 3,
                    "body": (
                        "**Taxa hipotética de 8% ao mês (composto)**\n\n"
                        "| Meses sem pagamento | Saldo devedor |\n"
                        "|---|---|\n"
                        "| 0 | R$ 1.000,00 |\n"
                        "| 1 | R$ 1.080,00 |\n"
                        "| 3 | R$ 1.259,71 |\n"
                        "| 6 | R$ 1.586,87 |\n"
                        "| 12 | R$ 2.518,17 |\n\n"
                        "Em 12 meses sem pagar, a dívida mais do que dobrou.\n\n"
                        "*(Taxa hipotética. Use para entender o mecanismo, "
                        "não como referência de taxa real de mercado.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O crédito rotativo do cartão",
                    "order": 4,
                    "body": (
                        "O **crédito rotativo** entra quando você paga menos do que "
                        "o total da fatura. O saldo restante é financiado automaticamente "
                        "pelo banco com taxas que costumam ser muito altas.\n\n"
                        "A resolução CMN nº 4.906/2021 estabeleceu o pagamento mínimo "
                        "obrigatório de 15% da fatura. Qualquer valor abaixo do total "
                        "aciona o rotativo sobre o restante.\n\n"
                        "Por isso, o pagamento integral da fatura é sempre a melhor "
                        "decisão — evita completamente o rotativo."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A dívida que você ignora é a que mais cresce",
                    "order": 5,
                    "body": (
                        "Muitas pessoas evitam abrir o extrato porque têm medo do "
                        "que vão encontrar. Mas quanto mais tempo passa, maior fica "
                        "o saldo — e mais difícil fica de sair.\n\n"
                        "Saber exatamente o que você deve é o primeiro passo para "
                        "resolver. Ignorar aumenta o problema."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Rotativo vs. empréstimo pessoal: mesmo valor, custo diferente",
                    "order": 6,
                    "body": (
                        "**Situação hipotética:** saldo de R$ 500 em aberto\n\n"
                        "| Opção | Taxa | 3 meses | Diferença |\n"
                        "|---|---|---|---|\n"
                        "| Rotativo (hipotético 15%/mês) | 15%/mês | R$ 760,06 | +R$ 260 |\n"
                        "| Empréstimo pessoal (hipotético 4%/mês) | 4%/mês | R$ 562,43 | +R$ 62 |\n\n"
                        "Mesmo sendo o mesmo valor inicial, o rotativo pode custar "
                        "R$ 198 a mais do que um empréstimo pessoal em apenas 3 meses.\n\n"
                        "*(Taxas hipotéticas. Taxas reais variam por produto e instituição.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 8.2 — Cálculo do rotativo
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Cálculo do rotativo",
            "description": (
                "Calcule o impacto do pagamento mínimo no saldo da dívida "
                "e compare cenários de pagamento para entender o custo real."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "8.2.1",
                    "name": "Calcular o impacto do pagamento mínimo",
                    "description": (
                        "Calcula o saldo devedor após um mês com pagamento mínimo "
                        "e identifica sobre qual valor o rotativo incide."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "8.2.2",
                    "name": "Comparar cenários de pagamento",
                    "description": (
                        "Compara mínimo, parcela fixa e quitação pelo custo total "
                        "e pelo prazo de liquidação."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Ana tem fatura de R$ 2.000,00. O pagamento mínimo é 15% "
                            "(R$ 300,00). Ela paga o mínimo. Sobre qual valor "
                            "o rotativo incide no próximo mês?"
                        ),
                        "competency_codes": ["8.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 300,00."},
                            {"value": "b", "label": "R$ 1.700,00."},
                            {"value": "c", "label": "R$ 2.000,00."},
                            {"value": "d", "label": "R$ 0,00 — pagou o mínimo, então não há rotativo."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Após pagar R$ 300, restam R$ 1.700. O rotativo "
                            "incide sobre esses R$ 1.700 no próximo mês. Mesmo pagando "
                            "o mínimo, a dívida continua crescendo sobre o saldo restante."
                        ),
                        "feedback_incorrect": (
                            "O rotativo incide sobre o saldo não pago: R$ 2.000 − R$ 300 = "
                            "R$ 1.700. Pagar o mínimo não elimina o rotativo — "
                            "apenas reduz um pouco o saldo sobre o qual ele incide."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Saldo de R$ 1.700 com taxa hipotética de 10%/mês. "
                            "Qual é o saldo após 1 mês sem nenhum pagamento adicional?"
                        ),
                        "competency_codes": ["8.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 1.870,00."},
                            {"value": "b", "label": "R$ 1.700,00."},
                            {"value": "c", "label": "R$ 1.750,00."},
                            {"value": "d", "label": "R$ 1.800,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 1.700 × 1,10 = R$ 1.870. "
                            "Os R$ 170 de juros somam-se ao saldo e viram base "
                            "para o próximo cálculo."
                        ),
                        "feedback_incorrect": (
                            "1.700 × (1 + 0,10) = 1.700 × 1,10 = R$ 1.870,00. "
                            "O juro de R$ 170 é adicionado ao saldo devedor."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos pode pagar o mínimo de R$ 150/mês ou R$ 500/mês "
                            "numa dívida de R$ 1.000. Qual reduz mais o saldo total "
                            "no fim de 6 meses? (Taxa hipotética 8%/mês.)"
                        ),
                        "competency_codes": ["8.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "R$ 500/mês — porque cada pagamento maior reduz mais o saldo "
                                    "sobre o qual os juros incidem."
                                ),
                            },
                            {"value": "b", "label": "São iguais — qualquer pagamento liquida a dívida."},
                            {"value": "c", "label": "R$ 150/mês — porque preserva mais dinheiro no curto prazo."},
                            {"value": "d", "label": "Depende da data de vencimento."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Com R$ 500/mês, Carlos quita a dívida em aproximadamente "
                            "2–3 meses e paga menos total. Com R$ 150/mês, a dívida pode "
                            "não diminuir e continuar crescendo se os juros superarem o pagamento."
                        ),
                        "feedback_incorrect": (
                            "Pagar mais por mês é sempre melhor no total: reduz o saldo "
                            "devedor mais rápido, diminui a base para o cálculo dos juros "
                            "seguintes e elimina a dívida em menos tempo."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Calcule o custo total de uma dívida de R$ 1.200,00 em "
                            "três cenários (use taxa hipotética de 8% ao mês):\n\n"
                            "a) Pagar só o mínimo (15%) por 6 meses\n"
                            "b) Pagar R$ 400/mês\n"
                            "c) Quitar tudo agora\n\n"
                            "Qual é a diferença de custo entre os três cenários? "
                            "O que você conclui sobre a estratégia de pagamento mínimo?"
                        ),
                        "competency_codes": ["8.2.1", "8.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Cenário c: R$ 1.200 (sem custo adicional)\n"
                            "Cenário b: pagar R$ 400/mês × 3 meses + juros ≈ total ≈ R$ 1.300\n"
                            "Cenário a: com mínimo de 15% e 8%/mês, em 6 meses a dívida "
                            "pode crescer antes de diminuir — custo total muito maior.\n\n"
                            "O pagamento mínimo é o mais caro no longo prazo. "
                            "Pagar mais cedo e mais do que o mínimo economiza significativamente."
                        ),
                        "evaluation_criteria": [
                            "Calcula o custo do cenário b corretamente (ou de forma aproximada).",
                            "Reconhece que o mínimo de 15% pode não cobrir todos os juros em taxas altas.",
                            "Conclui que o pagamento mínimo é a estratégia mais cara.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Por que pagar só o mínimo por muitos meses pode resultar "
                            "em pagar mais do que o dobro do valor original?"
                        ),
                        "competency_codes": ["8.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Porque o pagamento mínimo pode ser menor do que os "
                                    "juros mensais, fazendo o saldo crescer mesmo com pagamentos."
                                ),
                            },
                            {"value": "b", "label": "Porque o banco cobra multa toda vez que você paga o mínimo."},
                            {"value": "c", "label": "Porque o mínimo é sempre menor do que os juros."},
                            {"value": "d", "label": "Porque a fatura aumenta com o tempo por outros motivos."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Se a taxa mensal gera mais juros do que o valor do "
                            "mínimo pago, o saldo cresce mesmo com pagamentos. Isso pode "
                            "acontecer em taxas altas — o mínimo não cobre o custo do crédito."
                        ),
                        "feedback_incorrect": (
                            "Em taxas altas, o mínimo (15% da fatura) pode ser menor "
                            "do que os juros mensais. Nessa situação, o saldo cresce mesmo "
                            "com pagamentos — e o total pago ao longo do tempo supera "
                            "muito o valor original."
                        ),
                    },
                },
                {
                    "order": 6,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você tem R$ 3.000,00 de dívida no cartão e pode pagar "
                            "diferentes valores por mês (taxa hipotética 10%/mês). "
                            "Qual estratégia você escolhe?"
                        ),
                        "competency_codes": ["8.2.2"],
                        "scenario": (
                            "Dívida: R$ 3.000. Taxa: 10%/mês (hipotética). "
                            "Você tem R$ 600/mês disponível para quitar dívidas. "
                            "Valores hipotéticos, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar o mínimo (R$ 450/mês = 15%): preserva dinheiro agora, "
                                    "mas o saldo pode crescer além do mínimo com taxa de 10%."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar R$ 600/mês: quita a dívida em aproximadamente 6 meses "
                                    "e minimiza o custo total."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pagar R$ 300/mês: parcela menor, mas com 10%/mês o saldo "
                                    "vai crescer — essa estratégia não quita a dívida."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! Com R$ 600/mês e taxa de 10%/mês (hipotética), "
                            "a dívida é quitada em aproximadamente 6 meses. "
                            "Pagar o máximo possível é sempre a estratégia mais econômica "
                            "em dívidas com juros altos."
                        ),
                        "feedback_incorrect": (
                            "Com taxa de 10%/mês (hipotética), os juros mensais sobre "
                            "R$ 3.000 são R$ 300. Pagar menos do que R$ 300/mês faz o "
                            "saldo crescer — a dívida nunca é quitada. "
                            "Pagar R$ 600 (máximo disponível) é a decisão mais eficiente."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O efeito do pagamento mínimo mês a mês",
                    "order": 1,
                    "body": (
                        "O pagamento mínimo obrigatório é de 15% do valor da fatura "
                        "(Resolução CMN 4.906/2021). O saldo restante é financiado pelo "
                        "crédito rotativo.\n\n"
                        "O problema: em taxas altas, o juro mensal pode representar mais "
                        "do que o mínimo pago. Nesses casos, o saldo **cresce** mesmo com pagamentos.\n\n"
                        "**Exemplo hipotético:**\n"
                        "- Fatura: R$ 2.000\n"
                        "- Mínimo (15%): R$ 300\n"
                        "- Saldo após pagamento: R$ 1.700\n"
                        "- Juro de 10%/mês (hipotético) sobre R$ 1.700: R$ 170\n"
                        "- Novo saldo: R$ 1.870 — maior do que R$ 1.700!"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Fatura de R$ 1.500: pagamento mínimo por 6 meses",
                    "order": 2,
                    "body": (
                        "**Taxa hipotética: 12%/mês**\n\n"
                        "| Mês | Saldo | Mínimo pago (15%) | Juro 12% | Novo saldo |\n"
                        "|---|---|---|---|---|\n"
                        "| 0 | R$ 1.500 | — | — | R$ 1.500 |\n"
                        "| 1 | R$ 1.500 | R$ 225 | R$ 153 | R$ 1.428 |\n"
                        "| 2 | R$ 1.428 | R$ 214 | R$ 146 | R$ 1.360 |\n"
                        "| 3 | R$ 1.360 | R$ 204 | R$ 139 | R$ 1.295 |\n\n"
                        "Total pago em 3 meses: R$ 643. Saldo ainda em aberto: R$ 1.295.\n\n"
                        "*(Taxa hipotética. A dívida reduz, mas lentamente e com custo alto.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Comparando cenários: mínimo, fixo e quitação",
                    "order": 3,
                    "body": (
                        "Para a mesma dívida inicial, os resultados são muito diferentes:\n\n"
                        "**Dívida fictícia de R$ 1.000 a 8%/mês (hipotético)**\n\n"
                        "| Estratégia | Prazo | Total pago |\n"
                        "|---|---|---|\n"
                        "| Quitar agora | Imediato | R$ 1.000 |\n"
                        "| Pagar R$ 400/mês | ~3 meses | ~R$ 1.100 |\n"
                        "| Pagar R$ 200/mês | ~6+ meses | ~R$ 1.250+ |\n"
                        "| Pagar só o mínimo | Meses/anos | Muito mais |\n\n"
                        "*(Valores aproximados, hipotéticos. A tabela ilustra o mecanismo.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Pagar mais do que o mínimo: o impacto prático",
                    "order": 4,
                    "body": (
                        "Dobrar o pagamento mínimo pode reduzir o prazo de liquidação "
                        "de meses para semanas — e o custo total pode cair pela metade.\n\n"
                        "Se você não tem como pagar tudo de uma vez, pague o máximo "
                        "que o orçamento permitir — sempre acima do mínimo."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Quando o mínimo não cobre os juros",
                    "order": 5,
                    "body": (
                        "Em taxas muito altas (como algumas do rotativo), pode acontecer "
                        "que o juro mensal seja **maior** do que o mínimo pago. "
                        "Nesse caso, o saldo cresce mesmo pagando regularmente.\n\n"
                        "**Sinal de alerta:** se você paga o mínimo há meses e o saldo "
                        "não diminui, verifique se o juro supera o que você paga. "
                        "Essa é uma situação que exige uma ação mais urgente — "
                        "como negociar, buscar crédito mais barato ou quitar de uma vez."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 8.3 — Estratégias de saída
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Estratégias de saída",
            "description": (
                "Priorize dívidas, avalie propostas de renegociação e conheça "
                "alternativas para sair da dívida de forma mais eficiente."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "8.3.1",
                    "name": "Priorizar dívidas pelo custo",
                    "description": (
                        "Ordena o pagamento de dívidas pela taxa de juros mais alta "
                        "primeiro (estratégia da avalanche)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "8.3.2",
                    "name": "Avaliar proposta de renegociação",
                    "description": (
                        "Compara prazo, taxa, custo total e condições de uma proposta "
                        "de renegociação antes de aceitar."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "8.3.3",
                    "name": "Reconhecer quando a portabilidade pode ser vantajosa",
                    "description": (
                        "Identifica situações em que transferir a dívida para uma "
                        "instituição com taxa menor reduz o custo total."
                    ),
                    "is_essential": False,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos tem dívida A: R$ 500 a 5%/mês e dívida B: R$ 1.200 a "
                            "2%/mês. Tem R$ 400 disponíveis. Pela estratégia da avalanche, "
                            "qual ele paga primeiro?"
                        ),
                        "competency_codes": ["8.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Dívida A — porque tem a maior taxa (5%/mês), "
                                    "que gera mais custo por real em aberto."
                                ),
                            },
                            {"value": "b", "label": "Dívida B — porque tem o maior saldo."},
                            {"value": "c", "label": "Divide igualmente entre as duas."},
                            {"value": "d", "label": "A mais antiga."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A estratégia da avalanche prioriza a dívida com "
                            "maior taxa de juros — a que gera mais custo por real em "
                            "aberto. A dívida A cobra 5%/mês, mais do que o dobro da B."
                        ),
                        "feedback_incorrect": (
                            "Na avalanche, a prioridade é a dívida mais cara (maior taxa). "
                            "A dívida A cobra 5%/mês — mais que o dobro da B (2%/mês). "
                            "Liquidar A primeiro elimina o custo maior mais rápido."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Um credor oferece renegociação com desconto de 50% nos "
                            "juros acumulados, mas alongando o prazo de 6 para 24 meses. "
                            "Qual é o impacto mais importante a verificar?"
                        ),
                        "competency_codes": ["8.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O custo total: o desconto nos juros acumulados pode ser "
                                    "menor do que os novos juros que incidirão por 24 meses."
                                ),
                            },
                            {"value": "b", "label": "O nome do credor na proposta."},
                            {"value": "c", "label": "O número de parcelas apenas."},
                            {"value": "d", "label": "Se há multa de rescisão."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O desconto imediato parece atraente, mas o prazo "
                            "maior significa mais meses com juros incidindo. "
                            "O que importa é o custo total da renegociação comparado "
                            "com o saldo atual."
                        ),
                        "feedback_incorrect": (
                            "O foco correto é o custo total. Um desconto nos juros "
                            "acumulados pode ser pequeno se o prazo longo gera novos "
                            "juros por 24 meses. Compare: valor total a pagar na "
                            "renegociação vs. saldo atual."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que verificar antes de aceitar uma proposta de renegociação?",
                        "competency_codes": ["8.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Custo total após a renegociação, nova taxa, prazo, "
                                    "valor das parcelas e condições de quitação antecipada."
                                ),
                            },
                            {"value": "b", "label": "Apenas o valor da primeira parcela."},
                            {"value": "c", "label": "O desconto percentual oferecido, sem calcular o total."},
                            {"value": "d", "label": "O prazo — quanto maior, melhor sempre."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Antes de assinar, verifique: nova taxa de juros, "
                            "custo total (n × parcela), se cabe no orçamento e "
                            "se há custo para quitar antecipadamente."
                        ),
                        "feedback_incorrect": (
                            "Uma renegociação precisa ser avaliada pelo custo total, "
                            "não apenas pelo desconto ou pela parcela. A taxa nova pode "
                            "ser alta, o prazo longo demais ou as condições desfavoráveis."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Portabilidade de crédito significa:"
                        ),
                        "competency_codes": ["8.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Transferir uma dívida de uma instituição para outra "
                                    "com taxa menor, mantendo o saldo devedor."
                                ),
                            },
                            {"value": "b", "label": "Cancelar a dívida e abrir uma nova em outro banco."},
                            {"value": "c", "label": "Transferir a dívida para o nome de outra pessoa."},
                            {"value": "d", "label": "Pagar a dívida com o cartão de crédito."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A portabilidade permite transferir o saldo devedor "
                            "para outra instituição que ofereça taxa menor. "
                            "É regulamentada pelo Banco Central e pode reduzir o custo total."
                        ),
                        "feedback_incorrect": (
                            "Portabilidade de crédito é a transferência do saldo devedor "
                            "de uma instituição para outra com condições melhores "
                            "(taxa menor). O saldo permanece o mesmo — apenas a "
                            "instituição credora muda."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você tem duas dívidas fictícias:\n"
                            "- Dívida X: R$ 1.500, 6%/mês\n"
                            "- Dívida Y: R$ 3.000, 2%/mês\n\n"
                            "Você tem R$ 600/mês disponível para quitação. "
                            "Qual estratégia de pagamento você escolhe e por quê? "
                            "Considere a avalanche, a bola de neve e qualquer outra abordagem."
                        ),
                        "competency_codes": ["8.3.1", "8.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Avalanche: X tem taxa maior (6%/mês) — paga-se primeiro. "
                            "Pague o mínimo de Y e concentre o restante em X até quitar. "
                            "Depois redireciona tudo para Y.\n\n"
                            "Bola de neve: X tem saldo menor — fica mais próxima de ser quitada. "
                            "Liquidar X mais rápido libera o valor para Y.\n\n"
                            "Neste caso, a avalanche é mais econômica (6%/mês >> 2%/mês)."
                        ),
                        "evaluation_criteria": [
                            "Identifica a estratégia da avalanche (maior taxa primeiro).",
                            "Justifica com base na taxa e no custo gerado.",
                            "Menciona que o dinheiro liberado vai para a próxima dívida.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual é a primeira coisa a fazer ao perceber que você "
                            "não vai conseguir pagar a fatura do cartão integralmente?"
                        ),
                        "competency_codes": ["8.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Contatar o banco proativamente para negociar parcelamento "
                                    "ou renegociação antes do vencimento."
                                ),
                            },
                            {"value": "b", "label": "Pagar o mínimo e esperar o próximo mês."},
                            {"value": "c", "label": "Não pagar e ver o que acontece."},
                            {"value": "d", "label": "Usar outro cartão para pagar a fatura."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Negociar proativamente antes do vencimento dá mais "
                            "opções: parcelamento da fatura com taxa menor que o rotativo, "
                            "prazo mais longo ou desconto. Esperar piora a situação."
                        ),
                        "feedback_incorrect": (
                            "Negociar proativamente é sempre melhor do que deixar vencer. "
                            "O banco tem mais opções antes do vencimento. Pagar o mínimo "
                            "aciona o rotativo (custo alto). Usar outro cartão apenas "
                            "transfere e possivelmente amplia o problema."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Priorização de dívidas: avalanche vs. bola de neve",
                    "order": 1,
                    "body": (
                        "Quando há múltiplas dívidas, duas estratégias principais:\n\n"
                        "**Avalanche (maior taxa primeiro):**\n"
                        "- Pague o mínimo de todas as dívidas\n"
                        "- Concentre o restante na dívida de maior taxa\n"
                        "- Quando quitar, redirecione tudo para a próxima mais cara\n"
                        "- **Resultado:** menor custo total\n\n"
                        "**Bola de neve (menor saldo primeiro):**\n"
                        "- Pague o mínimo de todas as dívidas\n"
                        "- Concentre o restante na dívida de menor saldo\n"
                        "- Quando quitar, redirecione tudo para a próxima\n"
                        "- **Resultado:** satisfação psicológica de eliminar dívidas rápido\n\n"
                        "Para quem quer minimizar o custo financeiro: **avalanche**."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Carlos e a estratégia de avalanche",
                    "order": 2,
                    "body": (
                        "**Carlos tem:**\n"
                        "- Dívida A: R$ 500 a 5%/mês\n"
                        "- Dívida B: R$ 1.200 a 2%/mês\n"
                        "- Disponível por mês: R$ 400\n\n"
                        "**Estratégia avalanche:**\n"
                        "1. Paga o mínimo de B (ex.: R$ 50)\n"
                        "2. Concentra os R$ 350 restantes em A (mais cara)\n"
                        "3. A dívida A (R$ 500) é quitada em ~2 meses\n"
                        "4. Redirecionada para B: R$ 400/mês → quitada em ~3 meses\n\n"
                        "**Total:** ~5 meses para quitar ambas, com menor custo total.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como avaliar uma proposta de renegociação",
                    "order": 3,
                    "body": (
                        "Antes de aceitar qualquer renegociação, calcule:\n\n"
                        "1. **Custo total:** n × parcela nova\n"
                        "2. **Compare:** custo total da renegociação vs. saldo atual\n"
                        "3. **Verifique a nova taxa:** é menor que a atual?\n"
                        "4. **Cabe no orçamento?** a parcela nova não pode comprometer essenciais\n"
                        "5. **Quitação antecipada:** há multa para quitar antes do prazo?\n\n"
                        "Um desconto nos juros acumulados pode parecer ótimo, mas se o prazo "
                        "for muito longo, você pode pagar mais no total."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Portabilidade de crédito",
                    "order": 4,
                    "body": (
                        "A **portabilidade de crédito** permite transferir o saldo devedor "
                        "de uma instituição para outra que ofereça taxa menor.\n\n"
                        "**Como funciona:**\n"
                        "1. Você solicita uma proposta a outro banco\n"
                        "2. Se a nova taxa for menor, o banco novo paga o banco atual\n"
                        "3. Você passa a dever ao banco novo, com as novas condições\n\n"
                        "**Regulamentação:** Resolução CMN 4.292/2013\n\n"
                        "**Atenção:** verifique o CET da portabilidade e se há custos "
                        "adicionais. Só vale a pena se o custo total cair de fato."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Negociar é sempre melhor do que ignorar",
                    "order": 5,
                    "body": (
                        "Credores preferem negociar do que não receber nada. "
                        "Ao perceber que não vai conseguir pagar no prazo:\n\n"
                        "1. Entre em contato proativamente\n"
                        "2. Explique a situação honestamente\n"
                        "3. Peça condições de parcelamento ou prazo maior\n"
                        "4. Compare a proposta com o custo do rotativo\n\n"
                        "Isso evita o rotativo automático e pode resultar em condições "
                        "significativamente melhores."
                    ),
                },
            ],
        },
    ],
}
