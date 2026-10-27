"""Conteúdo versionado da Trilha 7 — Juros e parcelas.

phase_number: 7 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-07.md

Este módulo é imutável após publicação. Expansões futuras criam trail_7_v2.py.
As taxas e valores nos exemplos são hipotéticos e identificados como fictícios.
"""

TRAIL_7_V1 = {
    "phase_number": 7,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 7.1 — Juros simples e compostos
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Juros simples e compostos",
            "description": (
                "Calcule juros simples e compostos e entenda por que o tempo "
                "amplia o impacto de qualquer taxa."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "7.1.1",
                    "name": "Calcular juros simples",
                    "description": "Aplica a fórmula J = C × i × n para calcular o juro simples.",
                    "is_essential": True,
                },
                {
                    "code": "7.1.2",
                    "name": "Distinguir juros simples de compostos",
                    "description": (
                        "Explica que no simples o juro incide sempre sobre o capital "
                        "original, enquanto no composto incide sobre o saldo acumulado."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.1.3",
                    "name": "Calcular montante com juros compostos",
                    "description": "Aplica a fórmula M = C(1+i)^n para calcular o montante.",
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
                            "Qual é o juro simples de R$ 500,00 emprestados a 3% ao mês "
                            "por 4 meses? (Valores fictícios, para fins didáticos.)"
                        ),
                        "competency_codes": ["7.1.1"],
                        "options": [
                            {"value": "a", "label": "R$ 15,00."},
                            {"value": "b", "label": "R$ 45,00."},
                            {"value": "c", "label": "R$ 60,00."},
                            {"value": "d", "label": "R$ 20,00."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! J = 500 × 0,03 × 4 = R$ 60,00. "
                            "No juro simples, a taxa incide sempre sobre o capital original."
                        ),
                        "feedback_incorrect": (
                            "Verifique o cálculo: J = C × i × n = 500 × 0,03 × 4 = R$ 60,00. "
                            "A taxa mensal de 3% incide sobre os R$ 500 por 4 meses."
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
                            "Qual é a diferença entre juros simples e compostos?"
                        ),
                        "competency_codes": ["7.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Nos simples, o juro incide sempre sobre o capital original. "
                                    "Nos compostos, incide sobre o saldo acumulado (juros sobre juros)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Simples é para empréstimos; compostos, para investimentos.",
                            },
                            {
                                "value": "c",
                                "label": "Simples cobra mais; compostos cobram menos.",
                            },
                            {
                                "value": "d",
                                "label": "São a mesma coisa, apenas com nomes diferentes.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! Nos juros simples, cada período soma a mesma quantia "
                            "ao capital original. Nos compostos, o juro do período anterior "
                            "passa a fazer parte da base de cálculo do próximo período."
                        ),
                        "feedback_incorrect": (
                            "A diferença fundamental é a base de cálculo: nos simples, "
                            "sempre o capital original; nos compostos, o saldo acumulado "
                            "(capital + juros anteriores). É isso que gera o crescimento exponencial."
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
                            "Usando a fórmula M = C(1+i)^n, calcule o montante de "
                            "R$ 1.000,00 a 5% ao mês por 3 meses. "
                            "(1,05)^3 ≈ 1,1576. (Taxa hipotética, para fins didáticos.)"
                        ),
                        "competency_codes": ["7.1.3"],
                        "options": [
                            {"value": "a", "label": "R$ 1.150,00."},
                            {"value": "b", "label": "R$ 1.157,63."},
                            {"value": "c", "label": "R$ 1.100,00."},
                            {"value": "d", "label": "R$ 1.050,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! M = 1.000 × (1,05)^3 = 1.000 × 1,1576 ≈ R$ 1.157,63. "
                            "Nos compostos, o juro do 1º mês vira parte da base do 2º, e assim por diante."
                        ),
                        "feedback_incorrect": (
                            "Verifique: M = 1.000 × (1,05)^3 ≈ 1.000 × 1,1576 ≈ R$ 1.157,63. "
                            "Não é 1.000 × (0,05 × 3) = 1.150 (que seria juro simples). "
                            "O composto é sempre maior porque 'cobra juros sobre juros'."
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
                            "R$ 1.000,00 a 5% ao mês (composto) por 12 meses. "
                            "(1,05)^12 ≈ 1,7959. Qual é o montante final? "
                            "(Taxa hipotética, para fins didáticos.)"
                        ),
                        "competency_codes": ["7.1.3"],
                        "options": [
                            {"value": "a", "label": "R$ 1.600,00."},
                            {"value": "b", "label": "R$ 1.795,86."},
                            {"value": "c", "label": "R$ 1.500,00."},
                            {"value": "d", "label": "R$ 2.000,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! M = 1.000 × (1,05)^12 ≈ R$ 1.795,86. "
                            "Perceba: 12 meses a 5% simples dariam R$ 600 de juro. "
                            "Com compostos, o juro é R$ 795,86 — quase o dobro!"
                        ),
                        "feedback_incorrect": (
                            "M = 1.000 × (1,05)^12 ≈ 1.000 × 1,7959 ≈ R$ 1.795,86. "
                            "Nos juros compostos, o montante cresce mais rápido conforme "
                            "o tempo passa porque cada período parte de uma base maior."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Uma dívida de R$ 800 acumulou R$ 120 de juros em 3 meses "
                            "com sistema simples. Qual é a taxa mensal?"
                        ),
                        "competency_codes": ["7.1.1"],
                        "options": [
                            {"value": "a", "label": "5% ao mês."},
                            {"value": "b", "label": "3% ao mês."},
                            {"value": "c", "label": "15% ao mês."},
                            {"value": "d", "label": "4% ao mês."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! J = C × i × n → 120 = 800 × i × 3 → i = 120/(800×3) = "
                            "0,05 = 5% ao mês."
                        ),
                        "feedback_incorrect": (
                            "Use J = C × i × n: 120 = 800 × i × 3 → i = 120 ÷ 2.400 = 0,05 → 5% ao mês."
                        ),
                    },
                },
                {
                    "order": 6,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Por que é importante pagar uma dívida com juros compostos "
                            "o mais cedo possível?"
                        ),
                        "competency_codes": ["7.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Porque nos juros compostos, o saldo devedor cresce "
                                    "cada vez mais rápido — quanto mais tempo passa, "
                                    "mais você paga."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Porque os juros compostos param de crescer depois de 6 meses.",
                            },
                            {
                                "value": "c",
                                "label": "Porque o banco pode cancelar a dívida se você esperar.",
                            },
                            {
                                "value": "d",
                                "label": "Porque o juro composto é sempre menor do que o simples.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! Nos juros compostos, o saldo acumulado vira a nova base "
                            "de cálculo. Quanto mais tempo passa, maior a base e maiores os "
                            "juros seguintes — crescimento exponencial."
                        ),
                        "feedback_incorrect": (
                            "A resposta correta é a 'a'. Nos juros compostos, os juros do "
                            "período anterior somam-se à dívida e passam a gerar juros "
                            "também. Por isso o crescimento acelera com o tempo."
                        ),
                    },
                },
                {
                    "order": 7,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Explique com suas palavras por que os juros compostos crescem "
                            "mais rápido do que os simples. O que isso significa para uma "
                            "dívida que não é paga por 6 meses?"
                        ),
                        "competency_codes": ["7.1.2", "7.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la. "
                            "Verifique se você mencionou: (1) que nos compostos o juro "
                            "incide sobre o saldo acumulado, não só sobre o capital; "
                            "(2) que o crescimento é exponencial; (3) o impacto prático "
                            "de deixar uma dívida crescer por meses."
                        ),
                        "evaluation_criteria": [
                            "Explica que nos compostos os juros incidem sobre o saldo acumulado (juros sobre juros).",
                            "Menciona que o crescimento é mais rápido do que no simples.",
                            "Relaciona com o impacto prático de uma dívida não paga por meses.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 8,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Calcule e compare: uma dívida de R$ 1.000,00 a 8% ao mês "
                            "em 6 meses usando (a) juros simples e (b) juros compostos. "
                            "(1,08)^6 ≈ 1,5869. Qual é a diferença? "
                            "(Taxa hipotética, para fins didáticos.)"
                        ),
                        "competency_codes": ["7.1.1", "7.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. Resultado esperado:\n"
                            "(a) Simples: J = 1.000 × 0,08 × 6 = R$ 480,00 → Total R$ 1.480,00\n"
                            "(b) Compostos: M = 1.000 × (1,08)^6 ≈ 1.000 × 1,5869 ≈ R$ 1.586,90\n"
                            "Diferença: R$ 106,90 a mais com juros compostos em apenas 6 meses."
                        ),
                        "evaluation_criteria": [
                            "Calcula corretamente o juro simples: J = 1.000 × 0,08 × 6 = 480.",
                            "Calcula corretamente o montante composto: M ≈ 1.586,90.",
                            "Apresenta a diferença entre os dois resultados.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que são juros e por que existem",
                    "order": 1,
                    "body": (
                        "**Juros** são o custo do crédito: quando alguém empresta dinheiro, "
                        "cobra um valor pelo tempo que esse dinheiro fica fora do seu bolso.\n\n"
                        "Para quem pede emprestado, o juro é um custo. Para quem investe, "
                        "é um rendimento. O mesmo mecanismo funciona dos dois lados.\n\n"
                        "A taxa de juros é expressa em percentual por período: 2% ao mês, "
                        "12% ao ano, etc. O período importa tanto quanto o percentual."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Juros simples: a fórmula J = C × i × n",
                    "order": 2,
                    "body": (
                        "Nos **juros simples**, o juro incide sempre sobre o **capital original** (C), "
                        "independentemente do tempo que passou.\n\n"
                        "**Fórmula:** J = C × i × n\n\n"
                        "Onde:\n"
                        "- C = capital (valor emprestado ou investido)\n"
                        "- i = taxa de juros (em decimal: 5% = 0,05)\n"
                        "- n = número de períodos\n\n"
                        "**Exemplo fictício:** R$ 500 a 3% ao mês por 4 meses\n"
                        "J = 500 × 0,03 × 4 = **R$ 60,00**\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Comparação: simples vs. compostos ao longo do tempo",
                    "order": 3,
                    "body": (
                        "**Dívida fictícia de R$ 1.000 a 5% ao mês (hipotético):**\n\n"
                        "| Meses | Simples | Compostos |\n"
                        "|---|---|---|\n"
                        "| 1 | R$ 1.050 | R$ 1.050 |\n"
                        "| 3 | R$ 1.150 | R$ 1.157,63 |\n"
                        "| 6 | R$ 1.300 | R$ 1.340,10 |\n"
                        "| 12 | R$ 1.600 | R$ 1.795,86 |\n\n"
                        "Nos primeiros meses a diferença parece pequena. Mas em 12 meses, "
                        "os compostos geram R$ 195,86 a mais do que os simples — "
                        "quase 30% acima.\n\n"
                        "*(Valores hipotéticos, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Juros compostos: M = C(1+i)^n",
                    "order": 4,
                    "body": (
                        "Nos **juros compostos**, o juro de cada período é incorporado "
                        "ao capital e passa a gerar juros no período seguinte. "
                        "É o famoso **'juros sobre juros'**.\n\n"
                        "**Fórmula:** M = C × (1 + i)^n\n\n"
                        "Onde:\n"
                        "- M = montante final (capital + juros)\n"
                        "- C = capital inicial\n"
                        "- i = taxa por período (em decimal)\n"
                        "- n = número de períodos\n\n"
                        "**Exemplo fictício:** R$ 1.000 a 5% ao mês por 3 meses\n"
                        "M = 1.000 × (1,05)^3 = 1.000 × 1,1576 ≈ **R$ 1.157,63**\n\n"
                        "*(Taxa hipotética, para fins didáticos.)*\n\n"
                        "A grande maioria dos empréstimos e financiamentos usa juros compostos."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "O tempo é o maior aliado ou inimigo",
                    "order": 5,
                    "body": (
                        "Nos **investimentos**, os juros compostos trabalham a seu favor: "
                        "quanto mais tempo o dinheiro fica aplicado, mais ele cresce.\n\n"
                        "Nas **dívidas**, acontece o contrário: quanto mais tempo você "
                        "espera para pagar, mais a dívida cresce.\n\n"
                        "Por isso, pagar uma dívida com juros o quanto antes reduz "
                        "significativamente o custo total."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Por que a maioria dos créditos usa juros compostos",
                    "order": 6,
                    "body": (
                        "Empréstimos, financiamentos, cartão de crédito rotativo e a maior "
                        "parte dos contratos de crédito no Brasil operam com **juros compostos**.\n\n"
                        "Isso significa que, se você não pagar a parcela no prazo, a dívida "
                        "cresce de forma exponencial — não linear.\n\n"
                        "Por isso é fundamental entender a fórmula e calcular o custo total "
                        "antes de contratar qualquer crédito."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "R$ 1.000 ao longo de 12 meses: onde chega?",
                    "order": 7,
                    "body": (
                        "**Com taxa hipotética de 5% ao mês (composto):**\n\n"
                        "- M = 1.000 × (1,05)^12 ≈ 1.000 × 1,7959 ≈ **R$ 1.795,86**\n\n"
                        "Em juros simples, o mesmo cenário daria:\n"
                        "- J = 1.000 × 0,05 × 12 = R$ 600 → Total **R$ 1.600,00**\n\n"
                        "A diferença de R$ 195,86 pode parecer pequena, mas represena 12% "
                        "a mais de custo — apenas pela diferença no método de cálculo.\n\n"
                        "*(Taxa hipotética. Use para entender o mecanismo, não como referência "
                        "de taxa real de mercado.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Calculadora de juros compostos",
                    "order": 8,
                    "body": (
                        "Você não precisa memorizar a fórmula para o dia a dia. "
                        "Use uma calculadora financeira ou o simulador do seu banco "
                        "para calcular o montante de qualquer operação de crédito.\n\n"
                        "O que você precisa saber é **o que está calculando**: "
                        "capital inicial, taxa ao período e número de períodos. "
                        "Com esses três dados, você pode calcular qualquer montante."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 7.2 — Parcelamento e CET
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Parcelamento e CET",
            "description": (
                "Calcule o custo total de um parcelamento e interprete o "
                "Custo Efetivo Total (CET) para comparar ofertas de crédito."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "7.2.1",
                    "name": "Calcular o custo total de um parcelamento",
                    "description": (
                        "Multiplica o número de parcelas pelo valor unitário e "
                        "subtrai o capital para obter o custo total do crédito."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.2.2",
                    "name": "Interpretar o CET",
                    "description": (
                        "Explica o que o CET representa e por que inclui mais do que "
                        "a taxa de juros nominal."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.2.3",
                    "name": "Comparar preço à vista e parcelado pelo CET",
                    "description": (
                        "Determina qual opção custa menos considerando o custo total "
                        "do crédito."
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
                            "Um empréstimo de R$ 2.000,00 é parcelado em 10 × de R$ 240,00. "
                            "Qual é o custo total do crédito?"
                        ),
                        "competency_codes": ["7.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 240,00."},
                            {"value": "b", "label": "R$ 400,00."},
                            {"value": "c", "label": "R$ 200,00."},
                            {"value": "d", "label": "R$ 2.400,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Total pago = 10 × 240 = R$ 2.400. "
                            "Custo do crédito = 2.400 − 2.000 = **R$ 400,00**."
                        ),
                        "feedback_incorrect": (
                            "Custo total = total pago − capital. "
                            "10 × 240 = 2.400 → 2.400 − 2.000 = R$ 400,00 de juros pagos."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é o CET (Custo Efetivo Total)?",
                        "competency_codes": ["7.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A taxa de juros nominal do empréstimo, sem outros custos."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "A taxa que representa o custo real da operação, incluindo "
                                    "juros, tarifas, seguros e outros encargos."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "O valor total das parcelas, sem desconto.",
                            },
                            {
                                "value": "d",
                                "label": "O mesmo que a taxa Selic.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O CET é obrigatório nos contratos de crédito "
                            "(Resolução CMN 3.517/2007) e representa a taxa que inclui "
                            "todos os custos: juros nominais, tarifas, seguros e IOF."
                        ),
                        "feedback_incorrect": (
                            "O CET vai além da taxa nominal. Ele inclui todos os custos "
                            "embutidos no crédito: juros, tarifas de abertura, seguros e IOF. "
                            "Por isso é a melhor forma de comparar duas ofertas."
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
                            "Um produto custa R$ 1.200,00 à vista ou 6 × de R$ 230,00 "
                            "no cartão. Qual opção custa menos?"
                        ),
                        "competency_codes": ["7.2.3"],
                        "options": [
                            {"value": "a", "label": "Parcelado, porque as parcelas são pequenas."},
                            {"value": "b", "label": "À vista, porque o total parcelado é R$ 1.380,00."},
                            {"value": "c", "label": "São iguais: o parcelamento sem juros não tem custo."},
                            {"value": "d", "label": "Parcelado, porque preserva o dinheiro na conta."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 6 × 230 = R$ 1.380. Diferença em relação ao à vista: "
                            "1.380 − 1.200 = **R$ 180,00** a mais no parcelado."
                        ),
                        "feedback_incorrect": (
                            "Compare o total: 6 × 230 = R$ 1.380 contra R$ 1.200 à vista. "
                            "O parcelado custa R$ 180 a mais. O argumento de 'preservar o "
                            "dinheiro' pode valer em alguns casos, mas o custo é maior."
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
                            "Banco A oferece R$ 5.000,00 a 3% ao mês. Banco B "
                            "oferece R$ 5.000,00 com CET de 42% ao ano. "
                            "Qual é mais barato? (3% ao mês ≈ 42,6% ao ano efetivo.)"
                        ),
                        "competency_codes": ["7.2.2"],
                        "options": [
                            {"value": "a", "label": "Banco A, porque a taxa mensal parece menor."},
                            {"value": "b", "label": "Banco B, porque o CET anual (42%) é menor que o do banco A (≈ 42,6% ao ano)."},
                            {"value": "c", "label": "São iguais — 3% ao mês e 42% ao ano são a mesma coisa."},
                            {"value": "d", "label": "Impossível comparar com informações diferentes."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! 3% ao mês em juros compostos = (1,03)^12 − 1 ≈ 42,6% ao ano. "
                            "O CET do banco B (42%) é levemente menor. O CET é a forma correta "
                            "de comparar operações expressas em períodos diferentes."
                        ),
                        "feedback_incorrect": (
                            "3% ao mês (composto) = aproximadamente 42,6% ao ano efetivo. "
                            "O CET do banco B é 42% ao ano — ligeiramente menor. "
                            "Sempre compare pelo CET, que padroniza os custos."
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
                            "Você precisa financiar R$ 3.000,00. Tem duas ofertas:\n"
                            "- Oferta A: 12 × de R$ 295,00\n"
                            "- Oferta B: 24 × de R$ 160,00\n\n"
                            "Calcule o custo total de cada oferta e explique qual "
                            "você escolheria e por quê, considerando custo total "
                            "e impacto mensal no orçamento."
                        ),
                        "competency_codes": ["7.2.1", "7.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n"
                            "Custo A: 12 × 295 = 3.540 → juros = R$ 540\n"
                            "Custo B: 24 × 160 = 3.840 → juros = R$ 840\n"
                            "A é mais barata no total. B tem parcela menor mas custa "
                            "R$ 300 a mais no total e compromete o orçamento por mais tempo."
                        ),
                        "evaluation_criteria": [
                            "Calcula o custo total de ambas as ofertas corretamente.",
                            "Compara pelo custo total, não apenas pela parcela.",
                            "Considera o impacto mensal no orçamento além do custo total.",
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
                            "Qual dos itens abaixo NÃO costuma entrar no cálculo do CET?"
                        ),
                        "competency_codes": ["7.2.2"],
                        "options": [
                            {"value": "a", "label": "Tarifa de abertura de crédito (TAC)."},
                            {"value": "b", "label": "IOF (Imposto sobre Operações Financeiras)."},
                            {"value": "c", "label": "Valor do produto comprado com o crédito."},
                            {"value": "d", "label": "Seguro contratado junto com o empréstimo."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O CET mede o custo da operação de crédito (juros, "
                            "tarifas, seguros, IOF), não o valor do bem financiado."
                        ),
                        "feedback_incorrect": (
                            "O CET inclui os custos da operação de crédito: juros, IOF, "
                            "tarifas (como TAC) e seguros. O valor do produto comprado não "
                            "entra — ele é o capital financiado, não um custo do crédito."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é o CET e onde encontrá-lo",
                    "order": 1,
                    "body": (
                        "O **Custo Efetivo Total (CET)** é a taxa que representa o "
                        "custo real de uma operação de crédito, incluindo:\n\n"
                        "- Juros nominais\n"
                        "- Tarifas (abertura de crédito, análise de cadastro etc.)\n"
                        "- IOF (Imposto sobre Operações Financeiras)\n"
                        "- Seguros obrigatórios vinculados ao crédito\n\n"
                        "O CET é **obrigatório nos contratos** de crédito no Brasil "
                        "(Resolução CMN 3.517/2007). Você encontra esse número no "
                        "contrato ou pode pedir ao banco antes de assinar.\n\n"
                        "**Sempre compare pelo CET**, não apenas pela taxa mensal anunciada."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como calcular o custo total de um parcelamento",
                    "order": 2,
                    "body": (
                        "A forma mais simples de calcular o custo total:\n\n"
                        "**Custo total = n × parcela − capital**\n\n"
                        "Onde:\n"
                        "- n = número de parcelas\n"
                        "- parcela = valor de cada prestação\n"
                        "- capital = valor original emprestado ou financiado\n\n"
                        "**Exemplo fictício:**\n"
                        "- Empréstimo: R$ 2.000,00\n"
                        "- Parcelas: 10 × R$ 240,00\n"
                        "- Total pago: 10 × 240 = R$ 2.400,00\n"
                        "- Custo do crédito: 2.400 − 2.000 = **R$ 400,00**\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Notebook: à vista vs. 12 parcelas",
                    "order": 3,
                    "body": (
                        "**Notebook fictício — preço à vista: R$ 3.000,00**\n\n"
                        "Opção parcelada: 12 × de R$ 290,00\n\n"
                        "| Item | Valor |\n"
                        "|---|---|\n"
                        "| Preço à vista | R$ 3.000,00 |\n"
                        "| Total parcelado | R$ 3.480,00 |\n"
                        "| Custo do crédito | R$ 480,00 |\n\n"
                        "Em 12 meses, você pagou **R$ 480,00 a mais** do que o preço à vista — "
                        "16% acima.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Sempre peça o CET antes de assinar",
                    "order": 4,
                    "body": (
                        "Antes de contratar qualquer crédito, peça o **CET ao ano**. "
                        "Com esse número, você pode comparar qualquer oferta, "
                        "independentemente da forma de apresentar as taxas "
                        "(mensais, diárias, anuais).\n\n"
                        "O CET está no contrato. Se o banco ou financeira não quiser "
                        "fornecê-lo antes da assinatura, isso é um sinal de alerta."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O que entra no CET além dos juros",
                    "order": 5,
                    "body": (
                        "Dois empréstimos podem ter a mesma taxa nominal e CETs "
                        "diferentes. Isso acontece porque o CET inclui custos que "
                        "a taxa nominal não mostra:\n\n"
                        "- **Tarifa de abertura de crédito (TAC):** cobrança única pelo "
                        "processamento do crédito.\n"
                        "- **Seguro prestamista:** garante o pagamento do crédito em caso "
                        "de morte ou invalidez. Aumenta o custo real.\n"
                        "- **IOF:** imposto obrigatório sobre operações de crédito, "
                        "calculado sobre o valor e o prazo.\n\n"
                        "Todos esses custos estão no CET — por isso compare sempre "
                        "pelo CET, e não apenas pela taxa mensal."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Duas ofertas, mesmo capital, CETs diferentes",
                    "order": 6,
                    "body": (
                        "**Capital: R$ 5.000,00**\n\n"
                        "| Oferta | Taxa mensal | CET ao ano | Total pago |\n"
                        "|---|---|---|---|\n"
                        "| Banco A | 3,0% | 42,6% | R$ 6.510,00 |\n"
                        "| Banco B | 2,8% | 39,5% | R$ 6.210,00 |\n\n"
                        "O banco A tem taxa mensal ligeiramente maior e CET mais alto. "
                        "Em 12 meses, você pagaria R$ 300 a mais no banco A.\n\n"
                        "*(Valores e taxas hipotéticos, para fins didáticos. "
                        "Taxas reais variam por banco e perfil do cliente.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 7.3 — "Sem juros" existe?
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": '"Sem juros" existe?',
            "description": (
                "Analise uma oferta de parcelamento sem juros com senso crítico: "
                "compare preços, avalie o comprometimento futuro e decida com base "
                "nos dados disponíveis."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "7.3.1",
                    "name": "Analisar oferta de parcelamento sem juros criticamente",
                    "description": (
                        "Entende que 'sem juros' não implica necessariamente custo zero "
                        "e verifica se há diferença de preço entre as formas de pagamento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.3.2",
                    "name": "Identificar diferença de preço entre à vista e parcelado",
                    "description": (
                        "Compara o preço à vista e o total parcelado para identificar "
                        "se há custo implícito no parcelamento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.3.3",
                    "name": "Avaliar comprometimento futuro da renda",
                    "description": (
                        "Calcula quantos meses o parcelamento vai comprometer a renda "
                        "e avalia se o orçamento suporta esse compromisso."
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
                            "Uma loja oferece um produto por R$ 600,00 à vista ou "
                            "6 × de R$ 100,00 'sem juros'. Há diferença de custo "
                            "financeiro direto nesse caso?"
                        ),
                        "competency_codes": ["7.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Não. O total é o mesmo (R$ 600), então não há custo extra."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Sim. Sempre há custo no parcelamento.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não há custo financeiro direto nesse exemplo, mas é "
                                    "preciso verificar se o preço à vista seria diferente "
                                    "com outro método de pagamento."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "O parcelamento tem juros escondidos sempre.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Quando o preço à vista e o total parcelado são iguais, "
                            "não há custo financeiro direto no parcelamento. "
                            "O que pode existir é uma diferença de preço se você pagasse "
                            "por outro meio — mas isso depende de cada loja e oferta."
                        ),
                        "feedback_incorrect": (
                            "Cuidado: não é correto afirmar que todo parcelamento sem juros "
                            "tem custo. Quando o preço à vista e o total parcelado são iguais "
                            "(R$ 600 nos dois casos), não há custo financeiro direto. "
                            "O que pode variar é se existiria um desconto à vista."
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
                            "Loja A: R$ 800,00 à vista ou R$ 1.000,00 parcelado em 10× de R$ 100. "
                            "Loja B: R$ 1.000,00 à vista ou R$ 1.000,00 parcelado em 10× de R$ 100. "
                            "Em qual situação o 'sem juros' tem custo implícito?"
                        ),
                        "competency_codes": ["7.3.2"],
                        "options": [
                            {"value": "a", "label": "Nas duas lojas."},
                            {"value": "b", "label": "Somente na loja A."},
                            {"value": "c", "label": "Somente na loja B."},
                            {"value": "d", "label": "Em nenhuma das lojas."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Na loja A, o preço à vista é R$ 800 e o parcelado "
                            "totaliza R$ 1.000 — uma diferença de R$ 200 que corresponde "
                            "ao custo implícito do parcelamento. Na loja B, o preço é o "
                            "mesmo em qualquer forma de pagamento."
                        ),
                        "feedback_incorrect": (
                            "Compare o preço à vista com o total parcelado. Loja A: "
                            "à vista R$ 800, parcelado R$ 1.000 — diferença de R$ 200. "
                            "Loja B: mesmos R$ 1.000 nos dois casos — sem custo implícito."
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
                            "Carlos quer comprar uma televisão de R$ 1.800,00 em "
                            "12 × de R$ 150,00 'sem juros'. Qual aspecto ele deve "
                            "considerar além do preço total?"
                        ),
                        "competency_codes": ["7.3.3"],
                        "options": [
                            {"value": "a", "label": "Nada mais. Como não há juros, o parcelamento é sempre vantajoso."},
                            {
                                "value": "b",
                                "label": (
                                    "O comprometimento de R$ 150 por mês durante 12 meses: "
                                    "se o orçamento suporta esse compromisso por 1 ano."
                                ),
                            },
                            {"value": "c", "label": "Apenas verificar se o preço é competitivo."},
                            {"value": "d", "label": "Se o cartão tem limite suficiente."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! Mesmo sem juros explícitos, parcelar em 12× compromete "
                            "R$ 150 do orçamento por 12 meses. Se surgir um imprevisto nesse "
                            "período, essa parcela continuará vencendo."
                        ),
                        "feedback_incorrect": (
                            "O comprometimento futuro da renda é tão importante quanto o "
                            "custo total. R$ 150/mês por 12 meses significa que esse valor "
                            "estará ocupado no orçamento por 1 ano, independentemente de "
                            "qualquer imprevisto."
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
                            "Em qual situação parcelar sem juros faz mais sentido do que "
                            "pagar à vista?"
                        ),
                        "competency_codes": ["7.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Quando o preço à vista é o mesmo que o parcelado e "
                                    "parcelar não compromete a reserva de emergência."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Quando você não tem o dinheiro à vista e precisa da compra.",
                            },
                            {
                                "value": "c",
                                "label": "Nunca — à vista é sempre melhor.",
                            },
                            {
                                "value": "d",
                                "label": "Quando o limite do cartão é alto.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Quando o preço é o mesmo nas duas formas e pagar à vista "
                            "comprometeria a reserva, parcelar sem juros pode ser a decisão mais "
                            "equilibrada — preserva a liquidez sem pagar mais."
                        ),
                        "feedback_incorrect": (
                            "A resposta mais equilibrada é a 'a'. Parcelar sem juros pode "
                            "fazer sentido quando o preço é igual e pagar à vista esvaziaria "
                            "a reserva de emergência. Mas 'preciso e não tenho o dinheiro' "
                            "é uma situação que exige mais cuidado com o orçamento futuro."
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
                            "Analise a seguinte oferta fictícia:\n\n"
                            "\"Smartphone por R$ 1.200,00 à vista ou 10 × de R$ 130,00 sem juros.\"\n\n"
                            "1. Calcule o total parcelado.\n"
                            "2. Há diferença de preço entre as formas de pagamento?\n"
                            "3. Qual é o comprometimento mensal e por quantos meses?\n"
                            "4. O que você concluiria sobre o custo real da compra e "
                            "o impacto no orçamento?"
                        ),
                        "competency_codes": ["7.3.1", "7.3.2", "7.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Total parcelado: 10 × 130 = R$ 1.300,00\n"
                            "Diferença: R$ 1.300 − R$ 1.200 = R$ 100 a mais no parcelado\n"
                            "Comprometimento: R$ 130/mês por 10 meses\n"
                            "Conclusão: há um custo implícito de R$ 100 (8,3% sobre o preço). "
                            "A decisão depende se preservar R$ 1.200 no curto prazo compensa "
                            "pagar R$ 100 a mais e comprometer R$ 130/mês por 10 meses."
                        ),
                        "evaluation_criteria": [
                            "Calcula o total parcelado corretamente (R$ 1.300).",
                            "Identifica a diferença de preço (R$ 100 a mais no parcelado).",
                            "Avalia o comprometimento mensal e o prazo (R$ 130 por 10 meses).",
                            "Relaciona a decisão com o contexto do orçamento disponível.",
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
                            "Qual pergunta você deve fazer antes de aceitar uma oferta "
                            "de parcelamento sem juros?"
                        ),
                        "competency_codes": ["7.3.1", "7.3.2"],
                        "options": [
                            {"value": "a", "label": "O preço à vista é o mesmo que o total parcelado?"},
                            {"value": "b", "label": "O produto tem garantia?"},
                            {"value": "c", "label": "O cartão tem limite?"},
                            {"value": "d", "label": "As parcelas são boleto ou cartão?"},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Se o preço à vista for diferente do total parcelado, "
                            "há um custo implícito no parcelamento — mesmo sem taxa de juros "
                            "explícita. Essa é a pergunta mais importante antes de aceitar."
                        ),
                        "feedback_incorrect": (
                            "A pergunta mais importante é comparar o preço à vista com o "
                            "total parcelado. Se forem diferentes, há custo implícito no "
                            "parcelamento, independentemente do que a oferta chama de 'sem juros'."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que significa 'parcelamento sem juros' na prática",
                    "order": 1,
                    "body": (
                        "**'Parcelamento sem juros'** significa que o valor total das "
                        "parcelas é igual ao preço do produto — sem acréscimo de taxa "
                        "de juros explícita.\n\n"
                        "Isso não significa, necessariamente, que não há custo. "
                        "O que precisa ser verificado:\n\n"
                        "1. **O preço à vista é o mesmo que o total parcelado?**\n"
                        "   - Se sim: não há custo implícito direto.\n"
                        "   - Se o preço à vista é menor: a diferença é o custo do parcelamento.\n\n"
                        "2. **Existe desconto para pagamento à vista que você está deixando de usar?**\n\n"
                        "3. **O parcelamento compromete sua renda por quantos meses?**\n\n"
                        "Sem mais informações, você não pode afirmar com certeza que "
                        "o parcelamento não tem custo — nem que tem."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois cenários: com e sem custo implícito",
                    "order": 2,
                    "body": (
                        "**Loja A — sem custo implícito:**\n"
                        "- À vista: R$ 600,00\n"
                        "- Parcelado: 6 × R$ 100,00 = R$ 600,00\n"
                        "- Conclusão: sem custo financeiro direto nesse exemplo.\n\n"
                        "**Loja B — com custo implícito:**\n"
                        "- À vista: R$ 500,00\n"
                        "- Parcelado: 6 × R$ 100,00 = R$ 600,00\n"
                        "- Conclusão: R$ 100 a mais no parcelado = 20% de custo implícito.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*\n\n"
                        "A diferença entre os dois cenários só aparece quando você "
                        "**compara o preço à vista com o total parcelado**."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Comprometimento futuro: o que o 'sem juros' não elimina",
                    "order": 3,
                    "body": (
                        "Mesmo quando o parcelamento não tem custo financeiro direto, "
                        "ele **compromete parte da sua renda por meses**.\n\n"
                        "Exemplo: R$ 1.800 em 12 × de R$ 150 'sem juros'.\n"
                        "- Você paga o mesmo valor total que pagaria à vista.\n"
                        "- Mas R$ 150 do seu orçamento estará comprometido por 12 meses.\n"
                        "- Se surgir um imprevisto nesse período, essa parcela vence do mesmo jeito.\n\n"
                        "**A decisão de parcelar deve considerar:**\n"
                        "1. Há diferença de preço entre as formas?\n"
                        "2. O orçamento suporta a parcela por todo o prazo?\n"
                        "3. Pagar à vista comprometeria a reserva de emergência?"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Perguntas a fazer antes de parcelar sem juros",
                    "order": 4,
                    "body": (
                        "1. O preço à vista é o mesmo que o total parcelado?\n"
                        "2. Existe desconto para pagamento no Pix ou débito?\n"
                        "3. A parcela cabe no orçamento mensal por todo o prazo?\n"
                        "4. Pagar à vista não vai comprometer a reserva de emergência?\n\n"
                        "Com essas respostas, você tem os dados para decidir."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Quando parcelar sem juros pode fazer sentido",
                    "order": 5,
                    "body": (
                        "Parcelar sem juros pode ser uma decisão equilibrada quando:\n\n"
                        "- O preço é o mesmo nas duas formas de pagamento\n"
                        "- Pagar à vista esvaziaria a reserva de emergência\n"
                        "- A parcela cabe confortavelmente no orçamento mensal\n"
                        "- O prazo do parcelamento é razoável (não compromete anos de renda)\n\n"
                        "Nessa situação, parcelar preserva liquidez sem custo adicional. "
                        "Mas se o preço à vista for menor, a economia vai para quem paga à vista."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Parcelamento acumulado: somando os compromissos",
                    "order": 6,
                    "body": (
                        "Cada parcelamento em andamento ocupa uma fatia do orçamento. "
                        "Se você tem 3 compras parceladas ao mesmo tempo, some todas as "
                        "parcelas mensais e verifique quanto do orçamento já está comprometido "
                        "antes de adicionar mais um parcelamento.\n\n"
                        "**Regra prática:** parcelas já contratadas + nova parcela "
                        "devem caber no orçamento sem comprometer essenciais nem a reserva."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 7.4 — Comparando ofertas
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Comparando ofertas",
            "description": (
                "Compare ofertas de crédito pelo custo total e tome decisões "
                "fundamentadas considerando custo e capacidade de pagamento."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "7.4.1",
                    "name": "Comparar duas ofertas de crédito pelo custo total",
                    "description": (
                        "Calcula e compara o custo total de duas ou mais ofertas de "
                        "crédito para o mesmo capital."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "7.4.2",
                    "name": "Tomar decisão de crédito fundamentada",
                    "description": (
                        "Escolhe uma oferta considerando o custo total, o impacto "
                        "mensal no orçamento e a capacidade de pagamento."
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
                            "Oferta 1: R$ 3.000,00 em 12 × de R$ 295,00. "
                            "Oferta 2: R$ 3.000,00 em 24 × de R$ 160,00. "
                            "Qual tem maior custo total?"
                        ),
                        "competency_codes": ["7.4.1"],
                        "options": [
                            {"value": "a", "label": "Oferta 1 — porque a parcela é maior."},
                            {
                                "value": "b",
                                "label": (
                                    "Oferta 2 — porque 24 × 160 = R$ 3.840 contra "
                                    "12 × 295 = R$ 3.540."
                                ),
                            },
                            {"value": "c", "label": "As duas têm o mesmo custo."},
                            {"value": "d", "label": "Oferta 1 — porque o prazo é menor."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Oferta 1: 12 × 295 = R$ 3.540 (juros = R$ 540). "
                            "Oferta 2: 24 × 160 = R$ 3.840 (juros = R$ 840). "
                            "Prazo maior quase sempre significa custo total maior."
                        ),
                        "feedback_incorrect": (
                            "Calcule: Oferta 1: 12 × 295 = R$ 3.540 (custo = R$ 540). "
                            "Oferta 2: 24 × 160 = R$ 3.840 (custo = R$ 840). "
                            "A oferta 2 custa R$ 300 a mais no total, apesar da parcela menor."
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
                            "O custo total de dois empréstimos é igual, mas um tem "
                            "parcela menor (prazo maior). Qual compromete menos o orçamento mensal?"
                        ),
                        "competency_codes": ["7.4.2"],
                        "options": [
                            {"value": "a", "label": "O de prazo menor, porque termina antes."},
                            {
                                "value": "b",
                                "label": (
                                    "O de parcela menor (prazo maior), porque libera mais "
                                    "espaço no orçamento mensal."
                                ),
                            },
                            {"value": "c", "label": "Ambos têm o mesmo impacto mensal."},
                            {"value": "d", "label": "Nenhum — crédito sempre compromete o orçamento igual."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Se o custo total é o mesmo, a parcela menor libera "
                            "mais dinheiro por mês, facilitando o orçamento. A desvantagem "
                            "é o comprometimento por mais tempo."
                        ),
                        "feedback_incorrect": (
                            "A parcela menor compromete menos o orçamento mensal. "
                            "Mas atenção: se o custo total for diferente, a opção de "
                            "menor parcela pode acabar custando muito mais no total."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você precisa de R$ 5.000,00 e tem três ofertas:\n\n"
                            "- Banco A: 12 × de R$ 490,00 (total: R$ 5.880)\n"
                            "- Banco B: 18 × de R$ 340,00 (total: R$ 6.120)\n"
                            "- Financeira C: 24 × de R$ 265,00 (total: R$ 6.360)\n\n"
                            "Seu orçamento suporta no máximo R$ 350/mês de compromisso "
                            "de crédito. Qual oferta você escolhe?"
                        ),
                        "competency_codes": ["7.4.1", "7.4.2"],
                        "scenario": (
                            "Capital necessário: R$ 5.000. Três ofertas disponíveis com "
                            "diferentes prazos e custos. Restrição de orçamento: máximo "
                            "R$ 350/mês. Bancos hipotéticos, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Banco A: menor custo total (R$ 5.880), mas a parcela "
                                    "de R$ 490 ultrapassa o limite de R$ 350. Inviável."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Banco B: parcela de R$ 340 (dentro do limite) e custo "
                                    "total de R$ 6.120. Menor custo entre as viáveis."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Financeira C: parcela de R$ 265 (dentro do limite), "
                                    "mas custo total de R$ 6.360 — maior de todas."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! O banco B tem a parcela dentro do limite do "
                            "orçamento (R$ 340 ≤ R$ 350) e o menor custo total entre as "
                            "opções viáveis (R$ 6.120). A financeira C é mais barata por "
                            "mês, mas custa R$ 240 a mais no total."
                        ),
                        "feedback_incorrect": (
                            "Considere duas restrições: a parcela não pode ultrapassar "
                            "R$ 350/mês e você quer minimizar o custo total. "
                            "O banco A tem menor custo, mas a parcela inviabiliza. "
                            "O banco B é a melhor opção viável: parcela dentro do limite "
                            "e menor custo total entre as que cabem no orçamento."
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
                            "Descreva uma situação em que a decisão correta é recusar "
                            "todas as ofertas de crédito disponíveis, mesmo precisando "
                            "do dinheiro. O que você faria em seguida?"
                        ),
                        "competency_codes": ["7.4.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Situações em que recusar o crédito é racional incluem: "
                            "(1) o custo total compromete mais do que o benefício; "
                            "(2) a parcela ultrapassa a capacidade de pagamento e criaria "
                            "uma nova dívida; (3) existe uma alternativa melhor (vender algo, "
                            "renegociar outro compromisso, aguardar com reserva parcial)."
                        ),
                        "evaluation_criteria": [
                            "Descreve uma situação em que o crédito criaria mais problemas do que resolve.",
                            "Propõe pelo menos uma alternativa ao crédito.",
                            "Demonstra raciocínio sobre custo de oportunidade.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como comparar duas ofertas de crédito: passo a passo",
                    "order": 1,
                    "body": (
                        "Para comparar duas ofertas de crédito para o mesmo valor:\n\n"
                        "1. **Calcule o custo total de cada uma:** n × parcela − capital\n"
                        "2. **Compare pelo CET ao ano** (padroniza periodicidades diferentes)\n"
                        "3. **Verifique o impacto mensal:** a parcela cabe no orçamento?\n"
                        "4. **Considere o prazo:** menor prazo = menor custo total (em geral), "
                        "mas maior parcela mensal\n\n"
                        "A melhor oferta é a que tem menor custo total **e** parcela "
                        "compatível com o orçamento."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Carlos compara 3 opções de empréstimo",
                    "order": 2,
                    "body": (
                        "**Capital: R$ 5.000,00 (valores hipotéticos)**\n\n"
                        "| Oferta | Parcelas | Valor/mês | Total | Custo crédito |\n"
                        "|---|---|---|---|---|\n"
                        "| Banco A | 12 | R$ 490 | R$ 5.880 | R$ 880 |\n"
                        "| Banco B | 18 | R$ 340 | R$ 6.120 | R$ 1.120 |\n"
                        "| Financeira C | 24 | R$ 265 | R$ 6.360 | R$ 1.360 |\n\n"
                        "Se o orçamento de Carlos suporta R$ 350/mês:\n"
                        "- Banco A: parcela acima do limite → inviável\n"
                        "- Banco B: dentro do limite, menor custo entre as viáveis → **melhor opção**\n"
                        "- Financeira C: cabe no orçamento, mas custa R$ 240 a mais que B\n\n"
                        "*(Valores hipotéticos, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Além do custo: prazo e impacto no orçamento",
                    "order": 3,
                    "body": (
                        "Um crédito de custo menor nem sempre é a melhor escolha se "
                        "a parcela ultrapassar a capacidade de pagamento. Da mesma forma, "
                        "um prazo menor pode ser ótimo no papel mas inviável na prática.\n\n"
                        "**Duas perguntas para qualquer oferta:**\n"
                        "1. Qual é o custo total?\n"
                        "2. A parcela mensal cabe confortavelmente no orçamento?"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Quando não contratar crédito é a melhor decisão",
                    "order": 4,
                    "body": (
                        "Nem sempre a melhor oferta disponível é a decisão certa. "
                        "Considere não contratar quando:\n\n"
                        "- O custo total é alto demais em relação ao benefício esperado\n"
                        "- Nenhuma parcela cabe no orçamento sem comprometer essenciais\n"
                        "- Há outra forma de resolver sem crédito (guardar por 2–3 meses, "
                        "vender algo que não usa, renegociar um compromisso)\n"
                        "- A compra pode esperar até você ter o dinheiro disponível\n\n"
                        "Recusar crédito quando o custo é alto é uma decisão financeira "
                        "racional — não uma derrota."
                    ),
                },
            ],
        },
    ],
}
