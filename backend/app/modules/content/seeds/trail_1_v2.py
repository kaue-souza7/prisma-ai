"""Conteúdo expandido da Trilha 1 — Meu primeiro salário (v2).

phase_number: 1 (existente — apenas adiciona missões 2 e 3)
Fonte editorial: docs/trilhas/trilha-01.md

As missões 1.2 e 1.3 são novas. A missão 1.1 já existe via phase_1_v1.py.
O seeder usa upsert por chave natural — não duplica conteúdo existente.
Faixas INSS 2026: verificar vigência antes de publicar atualizações.

Conjuntos de perguntas (question_set):
- question_set=1: perguntas originais (preservadas para não quebrar progresso)
- question_set=2: variações — mesma competência, texto e opções diferentes
- question_set=3: variações — mesma competência, contexto diferente
"""

TRAIL_1_V2 = {
    "phase_number": 1,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 1.2 — Holerite linha a linha
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Holerite linha a linha",
            "description": (
                "Interprete cada linha do contracheque, calcule o INSS progressivo "
                "por faixas e entenda adiantamentos e benefícios."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "1.2.1",
                    "name": "Interpretar cada linha do contracheque",
                    "description": (
                        "Identifica a função de cada linha do holerite: "
                        "vencimentos, descontos e informativos."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.2.2",
                    "name": "Calcular INSS progressivo por faixas",
                    "description": (
                        "Aplica a tabela progressiva do INSS para calcular o "
                        "desconto correto sobre cada faixa salarial."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.2.3",
                    "name": "Reconhecer benefícios que não reduzem o salário",
                    "description": (
                        "Diferencia benefícios depositados pelo empregador "
                        "(FGTS, ticket pago pela empresa) de descontos do salário."
                    ),
                    "is_essential": False,
                },
            ],
            "activities": [
                # ── question_set=1 (original) ───────────────────────────
                {
                    "order": 1,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Um salário de R$ 2.800,00 está em qual faixa INSS 2026? "
                            "(Faixas hipotéticas baseadas em 2026 para fins didáticos.)\n\n"
                            "Faixas de referência:\n"
                            "- Até R$ 1.518: 7,5%\n"
                            "- R$ 1.518,01 a R$ 2.793,88: 9%\n"
                            "- R$ 2.793,89 a R$ 4.190,83: 12%"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Totalmente na faixa de 9% (até R$ 2.793,88).",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Parte na faixa de 9% e parte na faixa de 12% — "
                                    "R$ 2.793,88 na faixa de 9% e R$ 6,12 na faixa de 12%."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Totalmente na faixa de 12%.",
                            },
                            {
                                "value": "d",
                                "label": "Totalmente na faixa de 7,5%.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! R$ 2.800 supera o limite da 2ª faixa (R$ 2.793,88). "
                            "Até R$ 2.793,88: alíquota de 9%. Os R$ 6,12 acima: alíquota de 12%. "
                            "O sistema é progressivo — cada faixa paga sua própria alíquota."
                        ),
                        "feedback_incorrect": (
                            "O INSS é progressivo: não existe uma alíquota única sobre "
                            "o salário inteiro. R$ 2.800 cruza duas faixas: "
                            "até R$ 2.793,88 (alíquota 9%) e R$ 6,12 acima (alíquota 12%). "
                            "Verifique as faixas vigentes em 2026 antes de usar em produção."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Usando as faixas de referência 2026, qual é o INSS "
                            "aproximado de quem ganha R$ 2.000,00 bruto?\n\n"
                            "- Faixa 1: até R$ 1.518 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n"
                            "(Valores para fins didáticos.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {"value": "a", "label": "R$ 113,85 + R$ 43,38 = R$ 157,23."},
                            {"value": "b", "label": "R$ 180,00 (9% sobre R$ 2.000)."},
                            {"value": "c", "label": "R$ 150,00 (7,5% sobre R$ 2.000)."},
                            {"value": "d", "label": "R$ 155,68."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Progressivo:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 2.000 − R$ 1.518) × 9% = R$ 482 × 9% = R$ 43,38\n"
                            "- Total: R$ 157,23\n\n"
                            "*(Valores didáticos. Verifique tabela vigente.)*"
                        ),
                        "feedback_incorrect": (
                            "Progressivo, não alíquota única:\n"
                            "Faixa 1: 1.518 × 7,5% = R$ 113,85\n"
                            "Faixa 2: (2.000 − 1.518) × 9% = 482 × 9% = R$ 43,38\n"
                            "Total: R$ 157,23\n\n"
                            "*(Valores didáticos. Tabela muda anualmente.)*"
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Um adiantamento de R$ 500 recebido no dia 15 aparece no "
                            "holerite do dia 30. Como ele aparece?"
                        ),
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Como desconto — o valor já foi pago antes e é "
                                    "abatido do salário do mês."
                                ),
                            },
                            {"value": "b", "label": "Como crédito adicional ao salário."},
                            {"value": "c", "label": "Não aparece no holerite."},
                            {"value": "d", "label": "Como FGTS do mês."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O adiantamento aparece como desconto no holerite "
                            "do dia 30, porque você já recebeu esse valor antes. "
                            "O salário bruto é o mesmo — mas o líquido é reduzido "
                            "pelo valor já adiantado."
                        ),
                        "feedback_incorrect": (
                            "O adiantamento foi pago no dia 15 — já está na sua conta. "
                            "No holerite do dia 30, ele aparece como desconto para "
                            "que o saldo final esteja correto. "
                            "Salário bruto inalterado; adiantamento abatido no líquido."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é a PLR no contracheque?",
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Participação nos Lucros e Resultados — "
                                    "valor pago pela empresa conforme acordo coletivo, "
                                    "geralmente anual ou semestral."
                                ),
                            },
                            {"value": "b", "label": "Um desconto obrigatório de previdência."},
                            {"value": "c", "label": "Um tipo de vale-refeição."},
                            {"value": "d", "label": "Plano de Licença Remunerada."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! PLR (Participação nos Lucros e Resultados) é "
                            "um benefício opcional negociado em acordo coletivo. "
                            "Aparece como crédito no holerite e tem tributação específica."
                        ),
                        "feedback_incorrect": (
                            "PLR = Participação nos Lucros e Resultados. É um crédito — "
                            "não um desconto. Empresas que adotam pagam ao trabalhador "
                            "um valor extra conforme metas ou resultados, geralmente "
                            "anual ou semestral."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 1,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos recebe R$ 3.500,00 brutos. Usando as faixas de "
                            "referência INSS 2026 abaixo, calcule o INSS dele:\n\n"
                            "- Faixa 1: até R$ 1.518,00 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n"
                            "- Faixa 3: R$ 2.793,89 a R$ 4.190,83 → 12%\n\n"
                            "Mostre o cálculo de cada faixa e o total.\n"
                            "(Faixas para fins didáticos — verificar vigência.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Cálculo esperado:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 2.793,88 − R$ 1.518) × 9% = R$ 1.275,88 × 9% = R$ 114,83\n"
                            "- Faixa 3: (R$ 3.500 − R$ 2.793,88) × 12% = R$ 706,12 × 12% = R$ 84,73\n"
                            "- Total INSS: R$ 313,41\n\n"
                            "*(Valores didáticos. Verifique faixas vigentes.)*"
                        ),
                        "evaluation_criteria": [
                            "Calcula cada faixa separadamente.",
                            "Aplica a alíquota correta a cada faixa.",
                            "Soma os valores das três faixas.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual informação NÃO costuma aparecer em um contracheque?"
                        ),
                        "competency_codes": ["1.2.3"],
                        "options": [
                            {"value": "a", "label": "Salário bruto."},
                            {"value": "b", "label": "INSS descontado."},
                            {"value": "c", "label": "Saldo da conta corrente do trabalhador."},
                            {"value": "d", "label": "FGTS depositado pela empresa."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O contracheque mostra salário, descontos e "
                            "informativos do vínculo empregatício. O saldo da conta "
                            "corrente do trabalhador é informação privada do banco — "
                            "não aparece no holerite."
                        ),
                        "feedback_incorrect": (
                            "O contracheque mostra informações do vínculo de trabalho: "
                            "salário, descontos, FGTS (informativo) etc. "
                            "O saldo bancário do trabalhador é dado do banco — "
                            "não tem relação com o holerite."
                        ),
                    },
                },
                # ── question_set=2 ──────────────────────────────────────
                {
                    "order": 1,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Um salário de R$ 1.600,00 está em qual situação "
                            "em relação às faixas INSS 2026?\n\n"
                            "Faixas de referência:\n"
                            "- Até R$ 1.518: 7,5%\n"
                            "- R$ 1.518,01 a R$ 2.793,88: 9%\n"
                            "(Valores para fins didáticos.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {"value": "a", "label": "Totalmente na faixa de 7,5%."},
                            {
                                "value": "b",
                                "label": (
                                    "Parte na faixa de 7,5% e parte na faixa de 9% — "
                                    "R$ 1.518 na faixa de 7,5% e R$ 82 na faixa de 9%."
                                ),
                            },
                            {"value": "c", "label": "Totalmente na faixa de 9%."},
                            {"value": "d", "label": "Na faixa de 12%."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! R$ 1.600 supera o limite da 1ª faixa (R$ 1.518). "
                            "Até R$ 1.518: alíquota de 7,5%. Os R$ 82 acima: alíquota de 9%. "
                            "O sistema é progressivo — cada faixa incide apenas sobre a "
                            "parte do salário que está dentro dela."
                        ),
                        "feedback_incorrect": (
                            "O INSS é progressivo: R$ 1.600 cruza duas faixas. "
                            "Até R$ 1.518 → 7,5%. Os R$ 82 restantes → 9%. "
                            "Não existe uma alíquota única sobre o salário inteiro."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual é o INSS aproximado de quem ganha R$ 1.600,00 bruto?\n\n"
                            "- Faixa 1: até R$ 1.518 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n"
                            "(Valores para fins didáticos.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {"value": "a", "label": "R$ 113,85 + R$ 7,38 = R$ 121,23."},
                            {"value": "b", "label": "R$ 144,00 (9% sobre R$ 1.600)."},
                            {"value": "c", "label": "R$ 120,00 (7,5% sobre R$ 1.600)."},
                            {"value": "d", "label": "R$ 128,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Progressivo:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 1.600 − R$ 1.518) × 9% = R$ 82 × 9% = R$ 7,38\n"
                            "- Total: R$ 121,23\n\n"
                            "*(Valores didáticos. Verifique tabela vigente.)*"
                        ),
                        "feedback_incorrect": (
                            "Progressivo, não alíquota única:\n"
                            "Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "Faixa 2: R$ 82 × 9% = R$ 7,38\n"
                            "Total: R$ 121,23\n\n"
                            "*(Valores didáticos.)*"
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Ana recebeu vale-refeição de R$ 400 no cartão de benefícios, "
                            "pago integralmente pela empresa. Como esse valor aparece no holerite?"
                        ),
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {"value": "a", "label": "Não aparece — é benefício externo ao holerite."},
                            {
                                "value": "b",
                                "label": (
                                    "Aparece como crédito informativo — não é desconto, "
                                    "pois a empresa paga 100%."
                                ),
                            },
                            {"value": "c", "label": "Aparece como desconto do salário líquido."},
                            {"value": "d", "label": "Aparece como parte do FGTS."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Quando a empresa paga 100% do vale-refeição, "
                            "o valor aparece como informativo (crédito) no holerite — "
                            "não reduz o salário líquido."
                        ),
                        "feedback_incorrect": (
                            "Se a empresa paga integralmente o benefício, não há desconto. "
                            "O valor aparece no holerite como crédito informativo, "
                            "mostrando o benefício recebido sem reduzir o líquido."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O FGTS aparece no holerite como desconto do salário?",
                        "competency_codes": ["1.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Não — o FGTS é pago pelo empregador e aparece "
                                    "como informativo, sem reduzir o salário líquido."
                                ),
                            },
                            {"value": "b", "label": "Sim — é descontado diretamente do salário bruto."},
                            {"value": "c", "label": "Depende: para salários acima de R$ 3.000, é descontado."},
                            {"value": "d", "label": "Não aparece no holerite."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O FGTS (8% do salário bruto) é pago pelo empregador "
                            "diretamente na conta vinculada do trabalhador. "
                            "Aparece no holerite como informativo — não reduz o salário líquido."
                        ),
                        "feedback_incorrect": (
                            "O FGTS não sai do salário do trabalhador. "
                            "É uma obrigação do empregador — ele deposita 8% do salário bruto "
                            "na conta vinculada do trabalhador. Aparece como informativo no holerite."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 2,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Mariana ganha R$ 4.000,00 brutos. Usando as faixas de "
                            "referência INSS 2026 abaixo, calcule o INSS dela:\n\n"
                            "- Faixa 1: até R$ 1.518,00 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n"
                            "- Faixa 3: R$ 2.793,89 a R$ 4.190,83 → 12%\n\n"
                            "Mostre o cálculo de cada faixa e o total.\n"
                            "(Faixas para fins didáticos — verificar vigência.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Cálculo esperado:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 2.793,88 − R$ 1.518) × 9% = R$ 1.275,88 × 9% = R$ 114,83\n"
                            "- Faixa 3: (R$ 4.000 − R$ 2.793,88) × 12% = R$ 1.206,12 × 12% = R$ 144,73\n"
                            "- Total INSS: R$ 373,41\n\n"
                            "*(Valores didáticos. Verifique faixas vigentes.)*"
                        ),
                        "evaluation_criteria": [
                            "Calcula cada faixa separadamente.",
                            "Aplica a alíquota correta a cada faixa.",
                            "Soma os valores das três faixas.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual das opções abaixo NÃO é considerada desconto no holerite?"
                        ),
                        "competency_codes": ["1.2.3"],
                        "options": [
                            {"value": "a", "label": "INSS."},
                            {"value": "b", "label": "Vale-transporte (parte do trabalhador)."},
                            {
                                "value": "c",
                                "label": (
                                    "FGTS — é depósito do empregador, "
                                    "não desconto do salário."
                                ),
                            },
                            {"value": "d", "label": "Adiantamento salarial."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O FGTS não é desconto — é depositado pelo empregador "
                            "na conta vinculada do trabalhador. INSS, vale-transporte "
                            "(parte do trabalhador) e adiantamentos são descontos do salário."
                        ),
                        "feedback_incorrect": (
                            "INSS, vale-transporte e adiantamentos são descontos do salário. "
                            "O FGTS não é desconto: é pago pelo empregador, não sai "
                            "do salário do trabalhador."
                        ),
                    },
                },
                # ── question_set=3 ──────────────────────────────────────
                {
                    "order": 1,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Pedro ganha R$ 3.200,00 brutos. Quantas faixas do INSS 2026 "
                            "são atingidas pelo seu salário?\n\n"
                            "Faixas de referência:\n"
                            "- Faixa 1: até R$ 1.518\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88\n"
                            "- Faixa 3: R$ 2.793,89 a R$ 4.190,83\n"
                            "(Valores para fins didáticos.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {"value": "a", "label": "Uma faixa (a de 9%)."},
                            {"value": "b", "label": "Duas faixas (7,5% e 9%)."},
                            {"value": "c", "label": "Três faixas (7,5%, 9% e 12%)."},
                            {"value": "d", "label": "Quatro faixas."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! R$ 3.200 ultrapassa os limites da 1ª e da 2ª faixa, "
                            "atingindo a 3ª faixa (12%). As três faixas são atingidas — "
                            "cada uma incide apenas sobre a parte do salário dentro dela."
                        ),
                        "feedback_incorrect": (
                            "R$ 3.200 > R$ 2.793,88 (teto da 2ª faixa), portanto "
                            "as três primeiras faixas são atingidas: 7,5%, 9% e 12%. "
                            "O INSS progressivo aplica cada alíquota somente ao trecho "
                            "do salário dentro daquela faixa."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual é o INSS aproximado de quem ganha R$ 2.400,00 bruto?\n\n"
                            "- Faixa 1: até R$ 1.518 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n"
                            "(Valores para fins didáticos.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {"value": "a", "label": "R$ 113,85 + R$ 78,50 = R$ 192,35."},
                            {"value": "b", "label": "R$ 216,00 (9% sobre R$ 2.400)."},
                            {"value": "c", "label": "R$ 180,00 (7,5% sobre R$ 2.400)."},
                            {"value": "d", "label": "R$ 200,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Progressivo:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 2.400 − R$ 1.518) × 9% = R$ 882 × 9% = R$ 79,38\n"
                            "Aproximado: R$ 192,35 a R$ 193,23 dependendo do arredondamento.\n\n"
                            "*(Valores didáticos. Verifique tabela vigente.)*"
                        ),
                        "feedback_incorrect": (
                            "Progressivo, não alíquota única:\n"
                            "Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "Faixa 2: (R$ 2.400 − R$ 1.518) × 9% = R$ 882 × 9% ≈ R$ 79,38\n"
                            "Total ≈ R$ 193,23\n\n"
                            "*(Valores didáticos.)*"
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "João recebeu vale-transporte de R$ 200. A empresa desconta "
                            "até 6% do salário bruto do trabalhador. O salário de João "
                            "é R$ 2.000. Quanto é descontado no holerite de vale-transporte?"
                        ),
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 200 (valor total do VT)."},
                            {"value": "b", "label": "R$ 120 (6% de R$ 2.000)."},
                            {
                                "value": "c",
                                "label": (
                                    "R$ 120 — pois 6% de R$ 2.000 = R$ 120, "
                                    "que é menor que o VT recebido (R$ 200)."
                                ),
                            },
                            {"value": "d", "label": "Nada — VT é gratuito."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O desconto máximo de VT é 6% do salário bruto. "
                            "6% de R$ 2.000 = R$ 120. Como R$ 120 < R$ 200 (custo real), "
                            "desconta-se apenas R$ 120. A diferença (R$ 80) é custeada pela empresa."
                        ),
                        "feedback_incorrect": (
                            "O desconto de VT é limitado a 6% do salário bruto do trabalhador. "
                            "6% de R$ 2.000 = R$ 120. Mesmo que o VT custe R$ 200, "
                            "o desconto no holerite é apenas R$ 120."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual é a diferença entre 'vencimentos' e 'descontos' "
                            "em um holerite?"
                        ),
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Vencimentos são créditos (o que a empresa paga ao trabalhador); "
                                    "descontos são débitos (o que é abatido do salário)."
                                ),
                            },
                            {"value": "b", "label": "São sinônimos — significam o mesmo no holerite."},
                            {"value": "c", "label": "Vencimentos são apenas o salário base; descontos incluem tudo."},
                            {"value": "d", "label": "Descontos são pagamentos extras da empresa."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Vencimentos = o que entra (salário base, horas extras, PLR). "
                            "Descontos = o que sai (INSS, IRRF, VT, adiantamentos). "
                            "Líquido = total vencimentos − total descontos."
                        ),
                        "feedback_incorrect": (
                            "Vencimentos são todos os créditos: salário base, horas extras, PLR etc. "
                            "Descontos são todos os débitos: INSS, IRRF, VT, adiantamentos etc. "
                            "O salário líquido é a diferença entre os dois totais."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 3,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Roberta ganha R$ 2.600,00 brutos. Usando as faixas de "
                            "referência INSS 2026 abaixo, calcule o INSS dela:\n\n"
                            "- Faixa 1: até R$ 1.518,00 → 7,5%\n"
                            "- Faixa 2: R$ 1.518,01 a R$ 2.793,88 → 9%\n\n"
                            "Mostre o cálculo de cada faixa e o total.\n"
                            "(Faixas para fins didáticos — verificar vigência.)"
                        ),
                        "competency_codes": ["1.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Cálculo esperado:\n"
                            "- Faixa 1: R$ 1.518 × 7,5% = R$ 113,85\n"
                            "- Faixa 2: (R$ 2.600 − R$ 1.518) × 9% = R$ 1.082 × 9% = R$ 97,38\n"
                            "- Total INSS: R$ 211,23\n\n"
                            "*(Valores didáticos. Verifique faixas vigentes.)*"
                        ),
                        "evaluation_criteria": [
                            "Calcula cada faixa separadamente.",
                            "Aplica a alíquota correta a cada faixa.",
                            "Soma os valores das duas faixas.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Um trabalhador recebe plano de saúde onde a empresa "
                            "paga 70% e ele paga 30% (R$ 90). Como aparece no holerite?"
                        ),
                        "competency_codes": ["1.2.3"],
                        "options": [
                            {"value": "a", "label": "Aparece como desconto de R$ 90 no salário."},
                            {"value": "b", "label": "Não aparece — benefício externo."},
                            {"value": "c", "label": "Aparece como desconto do valor total do plano."},
                            {"value": "d", "label": "Aparece como FGTS adicional."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Apenas a parte paga pelo trabalhador (R$ 90) "
                            "aparece como desconto no holerite. "
                            "A parte da empresa (70%) é custo dela — não sai do seu salário."
                        ),
                        "feedback_incorrect": (
                            "Quando há coparticipação, apenas a parte do trabalhador "
                            "é descontada do salário. A parte da empresa não aparece "
                            "como desconto — é custo dela, não seu."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é um holerite e como lê-lo",
                    "order": 1,
                    "body": (
                        "O **holerite** (ou contracheque) é o documento que detalha "
                        "o salário do trabalhador: o que foi creditado, o que foi "
                        "descontado e o valor líquido resultante.\n\n"
                        "**Principais seções:**\n"
                        "1. **Identificação:** nome, cargo, empresa, período de referência\n"
                        "2. **Vencimentos:** salário base, horas extras, adicionais, PLR\n"
                        "3. **Descontos:** INSS, IRRF, vale-transporte, adiantamentos\n"
                        "4. **Informativos:** FGTS (não é desconto), bases de cálculo\n"
                        "5. **Totais:** total de vencimentos, total de descontos, "
                        "**salário líquido**\n\n"
                        "Verifique o holerite todo mês. Se algo não fizer sentido, "
                        "pergunte ao RH."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Tabela INSS 2026: faixas e alíquotas",
                    "order": 2,
                    "body": (
                        "O INSS usa um sistema **progressivo por faixas** — "
                        "semelhante ao Imposto de Renda:\n\n"
                        "| Faixa | Alíquota | Referência 2026 |\n"
                        "|---|---|---|\n"
                        "| 1ª | 7,5% | Até R$ 1.518,00 |\n"
                        "| 2ª | 9% | R$ 1.518,01 a R$ 2.793,88 |\n"
                        "| 3ª | 12% | R$ 2.793,89 a R$ 4.190,83 |\n"
                        "| 4ª | 14% | R$ 4.190,84 a R$ 8.157,41 |\n\n"
                        "Cada faixa incide apenas sobre a parte do salário "
                        "dentro daquela faixa — **não existe alíquota única "
                        "sobre o salário inteiro**.\n\n"
                        "*(Faixas de referência 2026. Verifique o Diário Oficial "
                        "antes de usar em conteúdo publicado.)*"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Cálculo do INSS por faixas — salário R$ 2.800",
                    "order": 3,
                    "body": (
                        "**Salário bruto fictício: R$ 2.800,00**\n\n"
                        "| Faixa | Base | Alíquota | Valor |\n"
                        "|---|---|---|---|\n"
                        "| 1ª | R$ 1.518,00 | 7,5% | R$ 113,85 |\n"
                        "| 2ª | R$ 1.275,88 | 9% | R$ 114,83 |\n"
                        "| 3ª | R$ 6,12 | 12% | R$ 0,73 |\n"
                        "| **Total INSS** | | | **R$ 229,41** |\n\n"
                        "R$ 2.800 = R$ 1.518 (1ª faixa) + R$ 1.275,88 (2ª faixa) + "
                        "R$ 6,12 (3ª faixa)\n\n"
                        "*(Valores didáticos baseados em faixas 2026.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Adiantamento e PLR: o que são",
                    "order": 4,
                    "body": (
                        "**Adiantamento salarial:**\n"
                        "Parte do salário paga antes do fechamento do mês "
                        "(geralmente no dia 15 ou 20). No holerite do dia 30, "
                        "o adiantamento aparece como **desconto**, pois você "
                        "já recebeu aquele valor antes.\n\n"
                        "**PLR — Participação nos Lucros e Resultados:**\n"
                        "Benefício opcional, negociado em acordo coletivo. "
                        "Quando a empresa atinge metas, paga um valor extra "
                        "ao trabalhador. Aparece como crédito no holerite, "
                        "geralmente anual ou semestral. Tem tributação específica."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Benefícios que o empregador paga sem descontar do salário",
                    "order": 5,
                    "body": (
                        "Alguns benefícios aparecem no holerite mas **não são "
                        "descontados do salário líquido**:\n\n"
                        "- **FGTS (8%):** depositado pelo empregador em conta "
                        "vinculada ao trabalhador. Aparece como informativo.\n"
                        "- **Ticket-alimentação/refeição pago pela empresa:** "
                        "se o empregador paga 100%, não há desconto. Se o trabalhador "
                        "paga parte, apenas essa parte é descontada.\n"
                        "- **Plano de saúde subsidiado:** quando a empresa paga "
                        "parte, apenas a parte do trabalhador é descontada.\n\n"
                        "Esses valores são benefícios reais — aparecem no holerite "
                        "para transparência, não para descontar."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Contracheque completo com adiantamento e PLR (fictício)",
                    "order": 6,
                    "body": (
                        "**Carlos — salário R$ 3.500, PLR semestral R$ 1.200 (fictício)**\n\n"
                        "**Vencimentos:**\n"
                        "- Salário base: R$ 3.500,00\n"
                        "- PLR (semestral): R$ 1.200,00\n"
                        "- **Total vencimentos: R$ 4.700,00**\n\n"
                        "**Descontos:**\n"
                        "- INSS: R$ 313,41 (calculado sobre salário + PLR separadamente)\n"
                        "- Adiantamento recebido no dia 15: − R$ 700,00\n"
                        "- Vale-transporte: − R$ 105,00\n"
                        "- **Total descontos: R$ 1.118,41**\n\n"
                        "**Salário líquido: R$ 3.581,59**\n\n"
                        "**Informativo:** FGTS depositado pela empresa: R$ 280,00\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como guardar o histórico dos contracheques",
                    "order": 7,
                    "body": (
                        "Guarde todos os contracheques — físicos ou digitais:\n\n"
                        "- São necessários para comprovar renda em financiamentos e "
                        "cadastros\n"
                        "- Servem como prova em disputas trabalhistas\n"
                        "- Permitem verificar o INSS acumulado para a aposentadoria\n\n"
                        "Se o holerite for digital, baixe o PDF mensalmente e "
                        "armazene em local seguro (nuvem ou HD)."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Por que o IRRF pode ser R$ 0,00 no primeiro salário",
                    "order": 8,
                    "body": (
                        "Desde janeiro de 2026 (Lei 14.848/2024), trabalhadores que "
                        "recebem até R$ 5.000 por mês têm o Imposto de Renda Retido "
                        "na Fonte (IRRF) **zerado**.\n\n"
                        "Por isso, para quem está começando com um salário de "
                        "R$ 1.800–R$ 3.000, o IRRF aparece como R$ 0,00 no holerite.\n\n"
                        "Para salários acima de R$ 5.000, o IRRF passa a incidir "
                        "com alíquotas progressivas. Mas para a maioria dos primeiros "
                        "empregos, esse desconto é zero.\n\n"
                        "*(Verifique o limite de isenção vigente no site da Receita Federal.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 1.3 — 13º salário e férias
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "13º salário e férias",
            "description": (
                "Calcule o 13º salário e as férias com adicional constitucional "
                "de 1/3 e entenda por que o líquido é diferente do bruto."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "1.3.1",
                    "name": "Calcular o 13º salário bruto",
                    "description": (
                        "Calcula o 13º proporcional ao tempo de serviço no ano."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.3.2",
                    "name": "Calcular férias com adicional de 1/3",
                    "description": (
                        "Calcula o valor bruto das férias incluindo o adicional "
                        "constitucional de 1/3."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.3.3",
                    "name": "Diferenciar bruto e líquido em 13º e férias",
                    "description": (
                        "Explica por que o valor líquido do 13º e das férias "
                        "é menor que o bruto."
                    ),
                    "is_essential": False,
                },
            ],
            "activities": [
                # ── question_set=1 (original) ───────────────────────────
                {
                    "order": 1,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Salário bruto R$ 2.400,00, trabalhado 12 meses completos. "
                            "Qual é o 13º salário bruto integral?"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 2.400,00 (salário de 1 mês completo)."},
                            {"value": "b", "label": "R$ 1.200,00 (metade do salário)."},
                            {"value": "c", "label": "R$ 3.200,00 (mais adicional)."},
                            {"value": "d", "label": "R$ 200,00 (1/12 do salário)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O 13º integral é igual a 1 mês de salário bruto. "
                            "Para 12 meses completos: 12/12 × R$ 2.400 = R$ 2.400."
                        ),
                        "feedback_incorrect": (
                            "O 13º integral é 1/12 do salário × meses trabalhados. "
                            "Para 12 meses completos: (12/12) × R$ 2.400 = R$ 2.400. "
                            "É o valor de 1 mês completo de salário bruto."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Uma trabalhadora foi admitida em julho. "
                            "Em dezembro, ela tem direito a quanto de 13º? "
                            "(Salário bruto: R$ 1.800; trabalhados: 6 meses — julho a dezembro.)"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 1.800,00 (integral)."},
                            {"value": "b", "label": "R$ 900,00 (6/12 do salário)."},
                            {"value": "c", "label": "R$ 300,00 (1/6 do salário)."},
                            {"value": "d", "label": "R$ 1.500,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 13º proporcional = salário bruto × (meses trabalhados/12). "
                            "R$ 1.800 × (6/12) = R$ 1.800 × 0,5 = **R$ 900,00**."
                        ),
                        "feedback_incorrect": (
                            "13º proporcional = salário × meses/12. "
                            "6 meses de 12 = 50%. "
                            "R$ 1.800 × 50% = R$ 900,00."
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "O adicional constitucional de férias é de quanto "
                            "sobre o salário de férias?"
                        ),
                        "competency_codes": ["1.3.2"],
                        "options": [
                            {"value": "a", "label": "1/3 do salário de férias (CF/88, art. 7º, XVII)."},
                            {"value": "b", "label": "1/2 do salário de férias."},
                            {"value": "c", "label": "10% do salário de férias."},
                            {"value": "d", "label": "O mesmo valor do salário mensal (dobro)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A Constituição Federal (art. 7º, XVII) garante "
                            "o adicional de 1/3 do salário de férias. "
                            "Se o salário de férias é R$ 1.800, o adicional é R$ 600."
                        ),
                        "feedback_incorrect": (
                            "O adicional constitucional de férias é de 1/3. "
                            "CF/88, art. 7º, XVII: 'gozo de férias anuais remuneradas "
                            "com, pelo menos, um terço a mais do que o salário normal'."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos ganha R$ 1.800,00 brutos. Qual é o valor bruto "
                            "das suas férias de 30 dias com adicional de 1/3?"
                        ),
                        "competency_codes": ["1.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 2.400,00 (1.800 + 1/3 de 1.800 = 1.800 + 600)."},
                            {"value": "b", "label": "R$ 1.800,00 (apenas o salário)."},
                            {"value": "c", "label": "R$ 3.600,00 (salário dobrado)."},
                            {"value": "d", "label": "R$ 2.100,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Férias brutas = salário + 1/3 do salário. "
                            "R$ 1.800 + (R$ 1.800 / 3) = R$ 1.800 + R$ 600 = **R$ 2.400**."
                        ),
                        "feedback_incorrect": (
                            "Férias brutas = salário de férias + adicional de 1/3. "
                            "1.800 + (1.800 ÷ 3) = 1.800 + 600 = R$ 2.400."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 1,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Pedro vai tirar férias. Seu salário bruto é R$ 2.200,00.\n\n"
                            "1. Calcule o valor bruto das férias com adicional de 1/3.\n"
                            "2. Explique por que o valor líquido que Pedro vai receber "
                            "será menor do que o bruto calculado."
                        ),
                        "competency_codes": ["1.3.1", "1.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "1. Bruto: R$ 2.200 + (R$ 2.200/3) = R$ 2.200 + R$ 733,33 = R$ 2.933,33\n\n"
                            "2. O líquido é menor porque:\n"
                            "- INSS incide sobre as férias\n"
                            "- IRRF pode incidir se o total superar a faixa de isenção\n"
                            "- O salário de férias tem descontos calculados separadamente "
                            "das contribuições do mês normal."
                        ),
                        "evaluation_criteria": [
                            "Calcula o bruto corretamente (R$ 2.933,33).",
                            "Menciona que INSS e/ou IR incidem sobre férias.",
                            "Explica que bruto ≠ líquido.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 1,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Por que o IRRF sobre o 13º pode ser diferente do IRRF "
                            "do salário mensal?"
                        ),
                        "competency_codes": ["1.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O 13º é calculado com uma tabela específica da "
                                    "Receita Federal — diferente do salário mensal."
                                ),
                            },
                            {"value": "b", "label": "O 13º nunca paga IR."},
                            {"value": "c", "label": "O 13º sempre paga mais IR do que o salário."},
                            {"value": "d", "label": "Não há diferença — o cálculo é idêntico."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O 13º salário tem tabela de IRRF exclusiva "
                            "(não é somado ao salário mensal para o cálculo). "
                            "A Receita Federal determina como o 13º é tributado "
                            "separadamente do rendimento mensal."
                        ),
                        "feedback_incorrect": (
                            "O 13º tem regras próprias de tributação definidas pela "
                            "Receita Federal. Ele não é somado ao salário do mês "
                            "para calcular o IR — usa uma tabela específica."
                        ),
                    },
                },
                # ── question_set=2 ──────────────────────────────────────
                {
                    "order": 1,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Lucas foi admitido em março. Em dezembro, "
                            "quantos avos de 13º ele terá?\n"
                            "(Admissão em março = meses trabalhados: março a dezembro = 10 meses.)"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "12/12 (integral)."},
                            {"value": "b", "label": "10/12 (proporcional a 10 meses)."},
                            {"value": "c", "label": "9/12 (proporcional a 9 meses)."},
                            {"value": "d", "label": "3/12 (apenas o trimestre final)."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Mês conta se trabalhado mais de 15 dias. "
                            "De março a dezembro = 10 meses. "
                            "13º = salário × (10/12)."
                        ),
                        "feedback_incorrect": (
                            "De março a dezembro são 10 meses completos. "
                            "13º proporcional = salário × (meses/12) = salário × (10/12)."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Fernanda foi admitida em outubro. Em dezembro, "
                            "qual é o 13º bruto dela? (Salário: R$ 2.400; 3 meses trabalhados.)"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 2.400,00 (integral)."},
                            {"value": "b", "label": "R$ 600,00 (3/12 de R$ 2.400)."},
                            {"value": "c", "label": "R$ 800,00."},
                            {"value": "d", "label": "R$ 1.200,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 13º proporcional = R$ 2.400 × (3/12) = R$ 2.400 × 0,25 = **R$ 600**."
                        ),
                        "feedback_incorrect": (
                            "3 meses de 12 = 25%. "
                            "R$ 2.400 × (3/12) = R$ 600."
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Qual é o valor bruto das férias de Marcos, "
                            "que ganha R$ 2.100,00 brutos, com o adicional de 1/3?"
                        ),
                        "competency_codes": ["1.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 2.800,00 (R$ 2.100 + R$ 700)."},
                            {"value": "b", "label": "R$ 2.100,00 (apenas o salário)."},
                            {"value": "c", "label": "R$ 4.200,00 (salário dobrado)."},
                            {"value": "d", "label": "R$ 2.310,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Férias brutas = R$ 2.100 + (R$ 2.100/3) = "
                            "R$ 2.100 + R$ 700 = **R$ 2.800**."
                        ),
                        "feedback_incorrect": (
                            "Férias brutas = salário + 1/3 do salário. "
                            "R$ 2.100 + (R$ 2.100 ÷ 3) = R$ 2.100 + R$ 700 = R$ 2.800."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Patrícia ganha R$ 3.000 brutos e vai tirar férias. "
                            "O INSS incidirá sobre as férias dela?"
                        ),
                        "competency_codes": ["1.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Sim — o INSS incide sobre o valor bruto das férias, "
                                    "reduzindo o líquido recebido."
                                ),
                            },
                            {"value": "b", "label": "Não — férias são isentas de INSS."},
                            {"value": "c", "label": "Apenas se o valor superar R$ 5.000."},
                            {"value": "d", "label": "Apenas na 2ª parcela das férias."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O INSS incide sobre o valor bruto das férias. "
                            "Por isso o líquido recebido é menor do que o bruto calculado."
                        ),
                        "feedback_incorrect": (
                            "As férias não são isentas de INSS. "
                            "O INSS é calculado sobre o valor bruto das férias, "
                            "assim como sobre o salário mensal."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 2,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Roberto foi admitido em abril e ganha R$ 3.000,00 brutos.\n\n"
                            "1. Quantos meses ele terá trabalhado até dezembro?\n"
                            "2. Qual é o valor bruto do 13º proporcional?\n"
                            "3. O valor líquido será igual ao bruto? Por quê?"
                        ),
                        "competency_codes": ["1.3.1", "1.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "1. Abril a dezembro = 9 meses.\n\n"
                            "2. 13º bruto = R$ 3.000 × (9/12) = R$ 3.000 × 0,75 = **R$ 2.250**.\n\n"
                            "3. Não — o líquido será menor pois INSS e possivelmente IRRF "
                            "incidem sobre o 13º."
                        ),
                        "evaluation_criteria": [
                            "Conta corretamente os meses (9).",
                            "Calcula o 13º proporcional (R$ 2.250).",
                            "Explica que INSS/IR reduzem o líquido.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "O 13º salário é somado ao salário do mês de dezembro "
                            "para o cálculo do IRRF?"
                        ),
                        "competency_codes": ["1.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Não — o 13º tem tabela de IRRF própria e "
                                    "é tributado separadamente do salário mensal."
                                ),
                            },
                            {"value": "b", "label": "Sim — é somado ao salário de dezembro."},
                            {"value": "c", "label": "Sim — mas apenas a 2ª parcela é somada."},
                            {"value": "d", "label": "O 13º nunca paga IRRF."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A Receita Federal determina que o 13º tem base "
                            "de cálculo do IRRF própria — não é somado ao salário mensal. "
                            "Isso pode resultar em tributação diferente."
                        ),
                        "feedback_incorrect": (
                            "O 13º não é somado ao salário de dezembro para o IR. "
                            "Ele tem tabela de IRRF exclusiva definida pela Receita Federal."
                        ),
                    },
                },
                # ── question_set=3 ──────────────────────────────────────
                {
                    "order": 1,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carla ganha R$ 1.500,00 brutos e foi admitida em janeiro. "
                            "Qual é o 13º bruto integral em dezembro?"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 1.500,00 (12 meses completos)."},
                            {"value": "b", "label": "R$ 750,00 (metade do salário)."},
                            {"value": "c", "label": "R$ 125,00 (1/12 do salário)."},
                            {"value": "d", "label": "R$ 2.000,00 (com adicional de 1/3)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 12 meses completos = 12/12 × R$ 1.500 = **R$ 1.500**. "
                            "O 13º integral equivale a 1 mês de salário bruto."
                        ),
                        "feedback_incorrect": (
                            "Para 12 meses completos: 13º = salário × (12/12) = salário inteiro. "
                            "R$ 1.500 × 1 = R$ 1.500."
                        ),
                    },
                },
                {
                    "order": 2,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Thiago foi admitido em setembro. Em dezembro, "
                            "qual é o 13º bruto? (Salário: R$ 2.200; 4 meses trabalhados.)"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 2.200,00 (integral)."},
                            {"value": "b", "label": "R$ 733,33 (4/12 de R$ 2.200)."},
                            {"value": "c", "label": "R$ 550,00 (1/4 de R$ 2.200)."},
                            {"value": "d", "label": "R$ 880,00."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 13º proporcional = R$ 2.200 × (4/12) = "
                            "R$ 2.200 × 0,333... = **R$ 733,33**."
                        ),
                        "feedback_incorrect": (
                            "4 meses de 12: R$ 2.200 × (4/12) = R$ 733,33."
                        ),
                    },
                },
                {
                    "order": 3,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "O adicional de 1/3 de férias incide sobre qual base?"
                        ),
                        "competency_codes": ["1.3.2"],
                        "options": [
                            {"value": "a", "label": "Sobre o salário bruto mensal normal."},
                            {"value": "b", "label": "Sobre o salário líquido (já com descontos)."},
                            {"value": "c", "label": "Sobre o 13º salário."},
                            {"value": "d", "label": "Sobre as horas extras do mês."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O adicional de 1/3 é calculado sobre o salário bruto "
                            "das férias (= salário mensal bruto). "
                            "Férias brutas = salário + 1/3 do salário."
                        ),
                        "feedback_incorrect": (
                            "O adicional de 1/3 incide sobre o salário bruto das férias, "
                            "não sobre o líquido ou sobre o 13º."
                        ),
                    },
                },
                {
                    "order": 4,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Sandra ganha R$ 2.700,00 brutos. Qual é o adicional "
                            "constitucional de férias dela?"
                        ),
                        "competency_codes": ["1.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 900,00 (1/3 de R$ 2.700)."},
                            {"value": "b", "label": "R$ 1.350,00 (1/2 de R$ 2.700)."},
                            {"value": "c", "label": "R$ 270,00 (10% de R$ 2.700)."},
                            {"value": "d", "label": "R$ 2.700,00 (salário dobrado)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Adicional de férias = 1/3 do salário. "
                            "R$ 2.700 / 3 = **R$ 900,00**. "
                            "Total férias brutas = R$ 2.700 + R$ 900 = R$ 3.600."
                        ),
                        "feedback_incorrect": (
                            "Adicional de férias = 1/3 do salário bruto. "
                            "R$ 2.700 ÷ 3 = R$ 900."
                        ),
                    },
                },
                {
                    "order": 5,
                    "question_set": 3,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Ana ganha R$ 2.500,00 brutos e tem 12 meses trabalhados.\n\n"
                            "1. Qual é o valor bruto das férias com adicional de 1/3?\n"
                            "2. Qual é o 13º bruto integral?\n"
                            "3. Se os dois fossem pagos no mesmo mês, por que o Ana "
                            "não deve somar os dois valores brutos para planejar gastos?"
                        ),
                        "competency_codes": ["1.3.2", "1.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "1. Férias brutas = R$ 2.500 + (R$ 2.500/3) = R$ 2.500 + R$ 833,33 = **R$ 3.333,33**\n\n"
                            "2. 13º bruto = R$ 2.500 (12/12 = integral)\n\n"
                            "3. Porque ambos têm INSS e possivelmente IRRF incidindo. "
                            "O planejamento deve usar os valores líquidos, não os brutos."
                        ),
                        "evaluation_criteria": [
                            "Calcula férias brutas corretamente (R$ 3.333,33).",
                            "Calcula 13º bruto corretamente (R$ 2.500).",
                            "Menciona que INSS/IR incidem e que se deve usar o líquido.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "question_set": 3,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Quando as férias são pagas (prazo legal)?"
                        ),
                        "competency_codes": ["1.3.3"],
                        "options": [
                            {"value": "a", "label": "Até 2 dias antes do início do período de descanso."},
                            {"value": "b", "label": "No primeiro dia das férias."},
                            {"value": "c", "label": "No último dia do mês anterior às férias."},
                            {"value": "d", "label": "Junto com o salário do mês em que as férias terminam."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A CLT determina que o pagamento das férias deve ocorrer "
                            "até 2 dias antes do início do período de descanso. "
                            "Isso garante que o trabalhador tenha o dinheiro disponível "
                            "antes de sair de férias."
                        ),
                        "feedback_incorrect": (
                            "A lei trabalhista (CLT) exige que as férias sejam pagas "
                            "até 2 dias antes do início do descanso — "
                            "não no dia do início nem no mês seguinte."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é o 13º salário e quando é pago",
                    "order": 1,
                    "body": (
                        "O **13º salário** (ou gratificação natalina) é um direito "
                        "trabalhista previsto na Lei 4.090/1962 e na CF/88.\n\n"
                        "**Quem tem direito:** todo trabalhador com carteira assinada "
                        "e que tenha trabalhado pelo menos 15 dias no mês.\n\n"
                        "**Quando é pago:**\n"
                        "- 1ª parcela: até 30 de novembro\n"
                        "- 2ª parcela: até 20 de dezembro\n\n"
                        "**Cálculo:** 1/12 do salário bruto por mês trabalhado no ano. "
                        "Para 12 meses completos = 1 salário inteiro."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como calcular o 13º bruto proporcional",
                    "order": 2,
                    "body": (
                        "**Fórmula:** 13º bruto = salário bruto × (meses trabalhados / 12)\n\n"
                        "Considera-se mês completo quando trabalhado mais de 15 dias.\n\n"
                        "**Exemplos fictícios:**\n"
                        "- Admitido em janeiro → 12 meses → 12/12 × salário = salário inteiro\n"
                        "- Admitido em julho → 6 meses → 6/12 × salário = metade do salário\n"
                        "- Admitido em outubro → 3 meses → 3/12 × salário = 1/4 do salário\n\n"
                        "O 13º é bruto — INSS e IR incidem sobre ele, "
                        "então o líquido será menor."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "13º da Ana: admitida em março (fictício)",
                    "order": 3,
                    "body": (
                        "**Ana, salário bruto R$ 2.400, admitida em março:**\n\n"
                        "Meses trabalhados até dezembro: 10 (março a dezembro)\n\n"
                        "13º bruto = R$ 2.400 × (10/12) = R$ 2.400 × 0,8333 = **R$ 2.000,00**\n\n"
                        "Sobre esse valor, incidirão INSS e possivelmente IRRF.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Férias: direito, prazo e o adicional de 1/3",
                    "order": 4,
                    "body": (
                        "Todo trabalhador com carteira assinada tem direito a 30 dias "
                        "de férias remuneradas após cada 12 meses de trabalho (período aquisitivo).\n\n"
                        "**Adicional constitucional:** a CF/88 (art. 7º, XVII) garante "
                        "1/3 a mais do salário normal como adicional de férias.\n\n"
                        "**Total bruto de férias:**\n"
                        "Salário de férias + 1/3 do salário de férias\n\n"
                        "**Exemplo:** salário R$ 1.800:\n"
                        "- Salário de férias: R$ 1.800\n"
                        "- Adicional 1/3: R$ 600\n"
                        "- **Total bruto: R$ 2.400**"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Férias do Carlos com adicional de 1/3 (fictício)",
                    "order": 5,
                    "body": (
                        "**Carlos, salário bruto R$ 2.400:**\n\n"
                        "Férias brutas = R$ 2.400 + (R$ 2.400 / 3) = "
                        "R$ 2.400 + R$ 800 = **R$ 3.200,00 brutos**\n\n"
                        "Sobre esses R$ 3.200, incidirão:\n"
                        "- INSS (calculado sobre as férias)\n"
                        "- Possivelmente IRRF (se superar a faixa de isenção)\n\n"
                        "**Estimativa do líquido:**\n"
                        "Com INSS de ~R$ 300 e IRRF R$ 0 (abaixo de R$ 5.000): "
                        "líquido ≈ R$ 2.900\n\n"
                        "*(Valores fictícios. Tributação varia conforme tabelas vigentes.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Por que 13º e férias têm INSS e IR calculados separadamente",
                    "order": 6,
                    "body": (
                        "O 13º e as férias não são somados ao salário do mês para "
                        "o cálculo do INSS e do IR. Eles têm bases de cálculo próprias, "
                        "definidas pela Receita Federal e pelo INSS.\n\n"
                        "Isso significa que:\n"
                        "- O INSS sobre o 13º é calculado sobre o valor bruto do 13º\n"
                        "- O IR sobre o 13º usa uma tabela específica da Receita Federal\n"
                        "- O mesmo se aplica às férias\n\n"
                        "Por isso, ao planejar os meses em que o 13º ou as férias "
                        "caem na conta, considere sempre o **valor líquido** — "
                        "não o bruto anunciado."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como planejar os meses do 13º e das férias",
                    "order": 7,
                    "body": (
                        "13º e férias são salário diferido — você trabalhou o ano "
                        "inteiro para recebê-los. Não são 'dinheiro extra' inesperado.\n\n"
                        "**Dicas de planejamento:**\n"
                        "- Saiba com antecedência quando o 13º será pago (1ª parcela "
                        "até novembro, 2ª até dezembro)\n"
                        "- Estime o valor líquido (não o bruto) para o planejamento\n"
                        "- Use o 13º para quitar dívidas ou aumentar a reserva — "
                        "antes de fazer compras\n"
                        "- Não conte com o 13º para cobrir despesas mensais fixas"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Férias: planejar antes de gastar",
                    "order": 8,
                    "body": (
                        "O pagamento das férias deve acontecer até 2 dias antes "
                        "do início do período de descanso.\n\n"
                        "Receber as férias 'tudo de uma vez' pode dar a impressão "
                        "de que há muito dinheiro disponível. "
                        "Mas lembre-se: o salário do mês das férias + o valor das férias "
                        "precisam cobrir o mês de descanso **e** o mês seguinte "
                        "(quando você não receberá o valor adicional).\n\n"
                        "Planeje antes de gastar."
                    ),
                },
            ],
        },
    ],
}
