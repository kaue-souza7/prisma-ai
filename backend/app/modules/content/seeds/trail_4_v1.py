"""Trilha 4 — Cartão e fatura.

phase_number: 4 (existente — não insere nova fase)
Fonte editorial: docs/trilhas/trilha-04.md

Missão 1 é expansão (upsert sobre phase_2_v1.py missão 2).
Missões 2 e 3 são novas.
O seeder usa upsert por chave natural — não duplica conteúdo existente.
Taxas são fictícias e usadas apenas para fins didáticos.
"""

TRAIL_4_V1 = {
    "phase_number": 4,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 4.1 — Entendendo o cartão (expansão sobre phase_2_v1 missão 2)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Entendendo o cartão",
            "description": (
                "Entenda o ciclo do cartão de crédito, a diferença entre limite e "
                "saldo, e o que acontece quando você não paga a fatura integralmente."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.1.1",
                    "name": "Distinguir limite disponível de dinheiro próprio",
                    "description": (
                        "Explica que o limite do cartão não é dinheiro do titular — "
                        "é crédito a ser pago depois, com possibilidade de juros."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.1.2",
                    "name": "Compreender o ciclo fechamento/vencimento do cartão",
                    "description": (
                        "Distingue a data de fechamento (quando a fatura é 'cortada') "
                        "da data de vencimento (quando você paga), e sabe calcular "
                        "quando uma compra entra em qual fatura."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.1.3",
                    "name": "Calcular quando uma compra entra em qual fatura",
                    "description": (
                        "Determina se uma compra feita antes ou depois do fechamento "
                        "entra na fatura atual ou na seguinte."
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
                            "Limite de R$ 2.000 no cartão significa que você tem "
                            "R$ 2.000 do seu próprio dinheiro para gastar?"
                        ),
                        "competency_codes": ["4.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Sim — o banco libera R$ 2.000 da sua conta.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não — é crédito do banco; você paga na fatura, "
                                    "com juros se não pagar integralmente."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Depende do banco — algumas operam diferente.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Limite de crédito é um empréstimo pré-aprovado. "
                            "Você usa o dinheiro do banco e paga depois na fatura. "
                            "Se não pagar o total, incide o crédito rotativo — "
                            "um dos juros mais altos do mercado."
                        ),
                        "feedback_incorrect": (
                            "O limite não é saldo em conta — é crédito do banco. "
                            "Você usa e paga depois na fatura. Se não pagar tudo, "
                            "o saldo restante vira dívida com juros."
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
                            "Fechamento dia 10, vencimento dia 25. "
                            "Uma compra feita no dia 12 entra em qual fatura? "
                            "(Situação fictícia.)"
                        ),
                        "competency_codes": ["4.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Na fatura atual, com vencimento no dia 25.",
                            },
                            {
                                "value": "b",
                                "label": "Na próxima fatura, com vencimento 30+ dias depois.",
                            },
                            {
                                "value": "c",
                                "label": "Depende do valor da compra.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A compra foi feita no dia 12, depois do fechamento "
                            "do dia 10. Portanto entra na próxima fatura — "
                            "você terá mais tempo para pagar."
                        ),
                        "feedback_incorrect": (
                            "Compras feitas DEPOIS do fechamento entram na PRÓXIMA fatura. "
                            "Compras feitas antes ou no dia do fechamento entram na fatura atual. "
                            "Compra no dia 12 com fechamento no dia 10 → próxima fatura."
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
                            "Uma compra feita no dia 9 (antes do fechamento no dia 10) "
                            "entra em qual fatura? Qual é a data de vencimento?"
                            " (Situação fictícia.)"
                        ),
                        "competency_codes": ["4.1.2", "4.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Fatura atual, vencimento dia 25 — você paga em ~16 dias."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Próxima fatura, vencimento ~45 dias depois."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Depende do banco.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Compra no dia 9, fechamento no dia 10 → "
                            "entra na fatura atual, com vencimento no dia 25. "
                            "Você tem ~16 dias para pagar."
                        ),
                        "feedback_incorrect": (
                            "Compras feitas ANTES do fechamento entram na fatura ATUAL. "
                            "Dia 9, fechamento dia 10 → fatura atual, vencimento dia 25."
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
                            "O que acontece com o crédito disponível quando você paga "
                            "a fatura integralmente?"
                        ),
                        "competency_codes": ["4.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "O limite aumenta automaticamente.",
                            },
                            {
                                "value": "b",
                                "label": "O limite utilizado é liberado — volta ao valor original.",
                            },
                            {
                                "value": "c",
                                "label": "Nada muda — o limite só é alterado pelo banco.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Ao pagar a fatura, o valor utilizado é creditado "
                            "de volta ao limite disponível. Se você usou R$ 800 "
                            "de um limite de R$ 2.000, após pagar terá R$ 2.000 disponíveis "
                            "novamente."
                        ),
                        "feedback_incorrect": (
                            "Pagar a fatura libera o crédito utilizado — "
                            "o limite volta ao valor original. O banco pode aumentar o "
                            "limite por iniciativa própria, mas isso é independente "
                            "do pagamento da fatura."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O crédito rotativo cobra juros sobre qual valor?",
                        "competency_codes": ["4.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Sobre o valor total da fatura original.",
                            },
                            {
                                "value": "b",
                                "label": "Sobre o saldo não pago após o vencimento.",
                            },
                            {
                                "value": "c",
                                "label": "Sobre o valor das novas compras do próximo mês.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O rotativo incide sobre o saldo que ficou em aberto "
                            "após o vencimento. Se você pagou R$ 500 de uma fatura de "
                            "R$ 1.000, o rotativo incide sobre os R$ 500 restantes. "
                            "As taxas do rotativo são das mais altas do mercado brasileiro."
                        ),
                        "feedback_incorrect": (
                            "O crédito rotativo incide sobre o saldo não pago — "
                            "não sobre o total original. Se pagou parcialmente, "
                            "os juros incidem só sobre o que ficou em aberto."
                        ),
                    },
                },
                {
                    "order": 6,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Explique para um amigo como funciona o ciclo do cartão "
                            "e por que é importante saber a data de fechamento. "
                            "Use um exemplo com datas fictícias."
                        ),
                        "competency_codes": ["4.1.1", "4.1.2"],
                        "feedback_static": (
                            "Um bom exemplo inclui: 'Meu fechamento é dia 10 e meu "
                            "vencimento é dia 25. Se eu compro no dia 8, pago no dia 25. "
                            "Se compro no dia 12, pago no dia 25 do próximo mês — "
                            "tenho mais tempo.' Saber isso ajuda a planejar compras grandes."
                        ),
                        "evaluation_criteria": [
                            "Distingue data de fechamento de data de vencimento.",
                            "Explica quando uma compra entra em qual fatura com exemplo.",
                            "Menciona pelo menos um benefício prático de conhecer o ciclo.",
                        ],
                        "max_length": 600,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Limite de crédito: o que é e o que não é",
                    "order": 1,
                    "body": (
                        "**Limite de crédito** é o valor máximo que o banco autoriza "
                        "você a usar no cartão. Mas atenção:\n\n"
                        "❌ **Não é seu dinheiro.** É um empréstimo pré-aprovado.\n"
                        "❌ **Não está na sua conta corrente.** Ele é uma linha de crédito "
                        "separada.\n"
                        "✅ **Você usa e paga depois**, na fatura.\n"
                        "✅ **Se pagar integral, sem juros.** Se pagar parcialmente, "
                        "incide o crédito rotativo.\n\n"
                        "O erro mais comum: confundir limite com saldo disponível e "
                        "gastar como se o dinheiro já estivesse no bolso."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Ciclo do cartão: data de fechamento e data de vencimento",
                    "order": 2,
                    "body": (
                        "Todo cartão de crédito tem dois marcos mensais:\n\n"
                        "**Data de fechamento:** o dia em que a fatura é 'cortada'. "
                        "Compras feitas antes do fechamento entram nessa fatura. "
                        "Compras depois do fechamento entram na fatura seguinte.\n\n"
                        "**Data de vencimento:** o dia em que você paga a fatura. "
                        "Normalmente entre 15 e 30 dias após o fechamento.\n\n"
                        "**Exemplo:** fechamento dia 10, vencimento dia 25.\n"
                        "- Compra dia 8 → paga no dia 25 (17 dias)\n"
                        "- Compra dia 12 → paga no dia 25 do próximo mês (~43 dias)\n\n"
                        "*(Datas fictícias, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A compra da Ana em diferentes datas",
                    "order": 3,
                    "body": (
                        "**Ana** tem cartão com fechamento dia 5 e vencimento dia 20. "
                        "*(Fictício, para fins didáticos.)*\n\n"
                        "| Compra | Data | Entra em qual fatura? | Paga quando? |\n"
                        "|---|---|---|---|\n"
                        "| Roupa R$ 150 | Dia 3 | Fatura atual | Dia 20 (17 dias) |\n"
                        "| Livros R$ 80 | Dia 5 | Fatura atual | Dia 20 (15 dias) |\n"
                        "| Tênis R$ 300 | Dia 7 | Próxima fatura | Dia 20 do mês seguinte |\n\n"
                        "A compra do tênis foi estratégica: Ana escolheu o dia 7 "
                        "(depois do fechamento) para ter mais tempo para pagar "
                        "sem comprometer o orçamento do mês atual."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "O erro mais comum: confundir limite com saldo disponível",
                    "order": 4,
                    "body": (
                        "Muitas pessoas gastam no cartão como se o limite fosse dinheiro "
                        "na conta. O resultado: fatura que não cabe no orçamento.\n\n"
                        "**Como evitar:**\n\n"
                        "1. **Trate o cartão como débito antecipado:** só gaste o que "
                        "você já tem ou vai ter até o vencimento.\n\n"
                        "2. **Monitore o limite utilizado**, não o disponível. "
                        "Se você usou R$ 1.200 de um limite de R$ 2.000, "
                        "o comprometimento é R$ 1.200 com a renda futura.\n\n"
                        "3. **Some as parcelas em andamento.** "
                        "O limite disponível pode ser ilusório se você tem muitas "
                        "parcelas futuras."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Crédito rotativo: a dívida que cobra juros altos",
                    "order": 5,
                    "body": (
                        "O **crédito rotativo** é acionado quando você não paga "
                        "o valor total da fatura até o vencimento.\n\n"
                        "O saldo não pago fica em aberto e passa a cobrar juros "
                        "mensais — entre os mais altos do sistema financeiro brasileiro.\n\n"
                        "**Consequência prática:** uma fatura de R$ 1.000 não paga "
                        "por 3 meses no rotativo pode se tornar R$ 1.400 ou mais, "
                        "dependendo da taxa.\n\n"
                        "*(Taxa fictícia, para fins didáticos. Consulte o contrato "
                        "do seu cartão para a taxa real.)*\n\n"
                        "**Alternativa:** se não puder pagar tudo, quite o mínimo para "
                        "evitar negativação, mas busque renegociar ou quitar o quanto "
                        "antes."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Calendário de um mês com compras antes e depois do fechamento",
                    "order": 6,
                    "body": (
                        "**Carlos**, fechamento dia 15, vencimento dia 30. "
                        "*(Fictício, para fins didáticos.)*\n\n"
                        "**Semana 1 (dias 1–15):** compras caem na fatura que vence dia 30.\n"
                        "- Dia 8: supermercado R$ 320\n"
                        "- Dia 12: academia R$ 80\n"
                        "- Dia 15: conta de celular R$ 60\n"
                        "**Total desta fatura:** R$ 460\n\n"
                        "**Semana 2+ (dias 16–30):** compras caem na próxima fatura.\n"
                        "- Dia 18: roupas R$ 250 → só paga daqui a ~42 dias\n"
                        "- Dia 25: eletrônico R$ 400 → paga junto com as roupas\n\n"
                        "Carlos planejou a compra do eletrônico para depois do fechamento "
                        "exatamente para não comprometer o orçamento do mês atual."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 4.2 — Fatura e ciclo de compras (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Fatura e ciclo de compras",
            "description": (
                "Entenda como o ciclo de faturamento funciona em detalhe: "
                "quando cada compra cai em qual fatura, como o parcelamento "
                "se distribui ao longo dos meses e como ler uma fatura completa."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.2.1",
                    "name": "Interpretar uma fatura de cartão de crédito",
                    "description": (
                        "Identifica cada linha da fatura — compras à vista, "
                        "parcelas abertas, encargos e saldo devedor."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.2.2",
                    "name": "Rastrear quando cada parcela de uma compra parcelada aparece na fatura",
                    "description": (
                        "Determina em quais faturas futuras cada parcela de uma "
                        "compra parcelada aparecerá, com base na data de fechamento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.2.3",
                    "name": "Calcular o comprometimento futuro da renda com parcelas em aberto",
                    "description": (
                        "Soma as parcelas futuras de todas as compras parceladas "
                        "para estimar o comprometimento da renda nos próximos meses."
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
                            "O fechamento do cartão de Maria é no dia 10. "
                            "Ela fez uma compra no dia 8 de março e outra no dia 12 de março. "
                            "Em qual fatura cada compra aparece?\n\n"
                            "(Considere que o mês de referência da fatura é determinado "
                            "pela data de fechamento.)"
                        ),
                        "competency_codes": ["4.2.1", "4.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Compra do dia 8: fatura de março (fechamento 10/03). "
                                    "Compra do dia 12: fatura de abril (fechamento 10/04)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "As duas compras aparecem na mesma fatura de março.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Compra do dia 8: fatura de abril. "
                                    "Compra do dia 12: fatura de março."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "As duas aparecem na fatura de fevereiro.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O fechamento do dia 10 é o limite. "
                            "Compras feitas até o dia 10/03 entram na fatura de março. "
                            "Compras feitas a partir do dia 11/03 entram na fatura seguinte (abril). "
                            "A compra do dia 8 fechou antes do dia 10 → fatura de março. "
                            "A do dia 12 ficou após o fechamento → fatura de abril."
                        ),
                        "feedback_incorrect": (
                            "O fechamento determina o corte da fatura. "
                            "Compras feitas até o dia do fechamento entram na fatura daquele mês. "
                            "Compras após o fechamento entram na fatura do mês seguinte. "
                            "Dia 8 < dia 10 → fatura de março. "
                            "Dia 12 > dia 10 → fatura de abril."
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
                            "João comprou um tênis por R$ 360,00 em 3x sem juros no dia 5 de janeiro. "
                            "O fechamento do cartão é no dia 20. "
                            "Em quantas faturas essa compra aparecerá e em quais meses?\n\n"
                            "(Compra realizada antes do fechamento de janeiro.)"
                        ),
                        "competency_codes": ["4.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "3 faturas: janeiro (1ª parcela R$ 120), "
                                    "fevereiro (2ª R$ 120) e março (3ª R$ 120)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Apenas na fatura de janeiro, com o total de R$ 360.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "3 faturas: fevereiro (1ª parcela), "
                                    "março (2ª) e abril (3ª)."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "2 faturas: janeiro e fevereiro.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Compra feita antes do fechamento (dia 5 < dia 20): "
                            "a 1ª parcela aparece na fatura de janeiro. "
                            "Cada parcela subsequente aparece na fatura do mês seguinte. "
                            "R$ 360 ÷ 3 = R$ 120 por parcela, em janeiro, fevereiro e março."
                        ),
                        "feedback_incorrect": (
                            "Em compras parceladas, cada parcela aparece em uma fatura diferente. "
                            "A 1ª parcela entra na fatura do mês em que a compra foi feita "
                            "(antes do fechamento). As demais aparecem nos meses seguintes. "
                            "3x: 1ª parcela em janeiro, 2ª em fevereiro, 3ª em março."
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
                            "Ana tem as seguintes parcelas em aberto no cartão "
                            "(valores fictícios para fins didáticos):\n\n"
                            "- Celular 12x R$ 80: ainda 8 parcelas restantes\n"
                            "- Notebook 6x R$ 150: ainda 4 parcelas restantes\n"
                            "- Curso 3x R$ 50: ainda 2 parcelas restantes\n\n"
                            "Qual é o comprometimento total de Ana com parcelas "
                            "nos próximos meses (valor total ainda a pagar)?"
                        ),
                        "competency_codes": ["4.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "R$ 1.340,00 "
                                    "(8×R$80 + 4×R$150 + 2×R$50 = R$640 + R$600 + R$100)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "R$ 280,00 (apenas o valor mensal somado: R$80+R$150+R$50).",
                            },
                            {
                                "value": "c",
                                "label": "R$ 960,00.",
                            },
                            {
                                "value": "d",
                                "label": "R$ 1.560,00.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Para calcular o comprometimento total, multiplique "
                            "o valor de cada parcela pelo número de parcelas restantes:\n"
                            "- Celular: 8 × R$ 80 = R$ 640\n"
                            "- Notebook: 4 × R$ 150 = R$ 600\n"
                            "- Curso: 2 × R$ 50 = R$ 100\n"
                            "- Total: R$ 1.340,00\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "feedback_incorrect": (
                            "O comprometimento futuro é a soma de todas as parcelas restantes, "
                            "não apenas as do próximo mês. Some o total restante de cada compra:\n"
                            "8 × R$ 80 = R$ 640 | 4 × R$ 150 = R$ 600 | 2 × R$ 50 = R$ 100\n"
                            "Total: R$ 1.340,00\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
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
                            "Uma fatura fictícia de Pedro mostra:\n\n"
                            "- Supermercado (à vista): R$ 320,00\n"
                            "- Parcela 2/6 da TV: R$ 180,00\n"
                            "- Parcela 1/3 do tênis: R$ 90,00\n"
                            "- Anuidade do cartão: R$ 30,00\n\n"
                            "Qual é o total desta fatura?"
                        ),
                        "competency_codes": ["4.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 620,00."},
                            {"value": "b", "label": "R$ 590,00."},
                            {"value": "c", "label": "R$ 500,00."},
                            {"value": "d", "label": "R$ 680,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Total = R$ 320 + R$ 180 + R$ 90 + R$ 30 = **R$ 620,00**.\n"
                            "A fatura soma todas as cobranças do período: compras à vista, "
                            "parcelas dos meses anteriores e encargos fixos como anuidade.\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "feedback_incorrect": (
                            "Some todos os itens da fatura:\n"
                            "R$ 320 + R$ 180 + R$ 90 + R$ 30 = R$ 620,00.\n"
                            "Cada parcela de uma compra parcelada aparece individualmente, "
                            "mas todas integram o total da fatura.\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
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
                            "Carla tem as seguintes compras parceladas no cartão "
                            "(valores fictícios para fins didáticos):\n\n"
                            "- Geladeira: 10x R$ 200 → já pagou 3 parcelas\n"
                            "- Passagem aérea: 4x R$ 130 → já pagou 1 parcela\n"
                            "- Livros: 2x R$ 45 → já pagou 0 parcelas\n\n"
                            "1. Qual é o comprometimento total ainda a pagar?\n"
                            "2. Quanto dessas parcelas aparecerá na próxima fatura?\n"
                            "3. Se a renda de Carla é R$ 3.000 e a recomendação é "
                            "não comprometer mais de 30% da renda com cartão, "
                            "ela está dentro do limite recomendado para o próximo mês?"
                        ),
                        "competency_codes": ["4.2.2", "4.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Cálculo esperado:\n\n"
                            "1. Comprometimento total restante:\n"
                            "   - Geladeira: (10 − 3) × R$ 200 = 7 × R$ 200 = R$ 1.400\n"
                            "   - Passagem: (4 − 1) × R$ 130 = 3 × R$ 130 = R$ 390\n"
                            "   - Livros: (2 − 0) × R$ 45 = 2 × R$ 45 = R$ 90\n"
                            "   - **Total: R$ 1.880,00**\n\n"
                            "2. Próxima fatura (1 parcela de cada):\n"
                            "   R$ 200 + R$ 130 + R$ 45 = **R$ 375,00**\n\n"
                            "3. 30% de R$ 3.000 = R$ 900,00.\n"
                            "   R$ 375 < R$ 900 → dentro do limite na próxima fatura.\n"
                            "   Porém, o comprometimento total de R$ 1.880 indica que "
                            "   o orçamento estará pressionado por vários meses.\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "evaluation_criteria": [
                            "Calcula o total restante de cada compra (parcelas pendentes × valor).",
                            "Identifica corretamente o valor da próxima fatura (R$ 375).",
                            "Compara o valor mensal com o limite de 30% da renda.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você recebeu sua fatura e precisa decidir se faz uma nova compra. "
                            "Analise a situação e tome a melhor decisão."
                        ),
                        "competency_codes": ["4.2.1", "4.2.2", "4.2.3"],
                        "scenario": (
                            "Sua fatura atual (valores fictícios para fins didáticos):\n"
                            "- Aluguel (débito automático): R$ 50,00\n"
                            "- Parcela 3/6 do notebook: R$ 160,00\n"
                            "- Parcela 1/4 do sofá: R$ 200,00\n"
                            "- Supermercado à vista: R$ 280,00\n"
                            "Total desta fatura: R$ 690,00 | Renda: R$ 2.500,00\n"
                            "Parcelas futuras já comprometidas: R$ 1.080,00\n\n"
                            "Uma loja oferece TV por R$ 900 em 3x de R$ 300. "
                            "Você tem limite disponível. Deve comprar agora?"
                        ),
                        "options": [
                            {
                                "value": "comprar",
                                "label": "Sim — comprar a TV agora em 3x de R$ 300.",
                            },
                            {
                                "value": "adiar",
                                "label": "Não agora — adiar até quitar parte das parcelas atuais.",
                            },
                            {
                                "value": "avaliar",
                                "label": "Calcular o comprometimento futuro antes de decidir.",
                            },
                        ],
                        "correct_choice": "adiar",
                        "feedback_correct": (
                            "Ótima decisão! Com as parcelas atuais + a TV:\n"
                            "- Próxima fatura estimada: R$ 690 + R$ 300 = R$ 990\n"
                            "- Compromisso da renda: ~40% (acima do recomendado de 30%)\n"
                            "- Total futuro comprometido: R$ 1.980\n\n"
                            "Adiar a compra até quitar parcelas é a escolha mais segura.\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "feedback_incorrect": (
                            "Atenção! Apesar de ter limite disponível, é preciso considerar "
                            "o comprometimento futuro da renda.\n\n"
                            "Com a TV incluída: fatura ~R$ 990 (39,6% da renda), "
                            "total futuro comprometido R$ 1.980. "
                            "Limite no cartão não é sinônimo de dinheiro disponível no orçamento.\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como o ciclo de faturamento funciona",
                    "order": 1,
                    "body": (
                        "O cartão de crédito funciona em **ciclos mensais** definidos "
                        "pela data de **fechamento** e pela data de **vencimento**.\n\n"
                        "**Data de fechamento:** último dia em que uma compra entra "
                        "na fatura atual. Qualquer compra feita após esse dia vai "
                        "para a fatura do mês seguinte.\n\n"
                        "**Data de vencimento:** data limite para pagar a fatura sem "
                        "entrar em atraso. Geralmente cai entre 7 e 14 dias após o fechamento.\n\n"
                        "**Exemplo:** fechamento dia 15, vencimento dia 25.\n"
                        "- Compra no dia 10 → entra na fatura deste mês.\n"
                        "- Compra no dia 18 → entra na fatura do próximo mês.\n\n"
                        "Conhecer essas datas ajuda a planejar grandes compras: "
                        "comprar logo após o fechamento dá até ~45 dias para pagar "
                        "sem custo adicional."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Como parcelas se distribuem nas faturas — exemplo com 3 compras",
                    "order": 2,
                    "body": (
                        "**Situação fictícia — fechamento no dia 20:**\n\n"
                        "| Compra | Valor | Parcelamento | Data da compra | 1ª parcela em |\n"
                        "|---|---|---|---|---|\n"
                        "| Tênis | R$ 240 | 3x R$ 80 | 05/jan | Janeiro |\n"
                        "| Celular | R$ 1.200 | 6x R$ 200 | 22/jan | Fevereiro |\n"
                        "| Livro | R$ 60 | à vista | 15/jan | Janeiro |\n\n"
                        "**Fatura de janeiro:** R$ 80 (tênis 1/3) + R$ 60 (livro) = **R$ 140**\n"
                        "**Fatura de fevereiro:** R$ 80 (tênis 2/3) + R$ 200 (celular 1/6) = **R$ 280**\n"
                        "**Fatura de março:** R$ 80 (tênis 3/3) + R$ 200 (celular 2/6) = **R$ 280**\n"
                        "**Fatura de abril a junho:** R$ 200 (celular) cada mês\n\n"
                        "O celular foi comprado no dia 22/jan (após o fechamento do dia 20), "
                        "por isso a 1ª parcela só aparece em fevereiro.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como controlar o comprometimento futuro com parcelas",
                    "order": 3,
                    "body": (
                        "Antes de fazer uma nova compra parcelada, calcule quanto "
                        "você já tem comprometido nos próximos meses:\n\n"
                        "1. Liste todas as parcelas em aberto.\n"
                        "2. Some o total restante de cada compra "
                        "(parcelas pendentes × valor da parcela).\n"
                        "3. Divida pela sua renda mensal para ver o percentual comprometido.\n\n"
                        "**Referência:** muitos especialistas recomendam não comprometer "
                        "mais de 30% da renda mensal com dívidas de curto prazo "
                        "(incluindo cartão de crédito).\n\n"
                        "Ter **limite disponível no cartão** não é o mesmo que ter "
                        "**espaço no orçamento** — sempre calcule o impacto nas faturas futuras."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 4.3 — Pagamento mínimo e suas consequências (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Pagamento mínimo e suas consequências",
            "description": (
                "Entenda como o pagamento mínimo é calculado, o que é o crédito "
                "rotativo e por que pagar apenas o mínimo pode multiplicar a dívida "
                "rapidamente."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.3.1",
                    "name": "Calcular o pagamento mínimo de uma fatura",
                    "description": (
                        "Aplica a regra legal do pagamento mínimo (juros + encargos "
                        "+ 1% do principal, ou o total se menor que R$ 100) para "
                        "calcular o valor mínimo exigido."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.3.2",
                    "name": "Comparar cenários de pagamento integral versus mínimo usando o total pago",
                    "description": (
                        "Calcula o total pago ao longo do tempo nos cenários de "
                        "pagamento integral e pagamento mínimo, e compara os resultados."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.3.3",
                    "name": "Reconhecer quando o crédito rotativo se torna mais caro que alternativas",
                    "description": (
                        "Identifica situações em que o crédito rotativo do cartão "
                        "é mais caro do que outras modalidades de crédito ou do que "
                        "negociar a dívida diretamente."
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
                            "Desde janeiro de 2024, qual é a regra legal do pagamento mínimo "
                            "do cartão de crédito no Brasil?\n\n"
                            "(Lei 14.690/2023 e Resolução CMN 4.855/2020, conforme atualização.)"
                        ),
                        "competency_codes": ["4.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "100% dos juros e encargos do período + 1% do valor "
                                    "principal da fatura (ou o total da fatura se for "
                                    "inferior a R$ 100)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Exatamente 15% do total da fatura, sempre.",
                            },
                            {
                                "value": "c",
                                "label": "Apenas os juros do período, sem abater o principal.",
                            },
                            {
                                "value": "d",
                                "label": "10% do saldo devedor total do cartão.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A regra vigente desde janeiro de 2024 exige que "
                            "o pagamento mínimo cubra, no mínimo:\n"
                            "- 100% dos juros e encargos do período\n"
                            "- + 1% do valor principal da fatura\n\n"
                            "Se a fatura total for inferior a R$ 100, o mínimo é o "
                            "valor integral da fatura. Isso garante que o devedor "
                            "sempre amortize ao menos 1% do principal por mês."
                        ),
                        "feedback_incorrect": (
                            "A regra vigente desde janeiro de 2024 determina que o mínimo "
                            "seja 100% dos juros + encargos + 1% do principal. "
                            "Não é um percentual fixo sobre o total — os juros precisam "
                            "ser pagos integralmente para que a dívida não cresça indefinidamente. "
                            "Se a fatura for menor que R$ 100, paga-se o total."
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
                            "Fatura fictícia de R$ 1.200,00. Dados para cálculo do mínimo "
                            "(taxa hipotética para fins didáticos — não representa taxa real):\n\n"
                            "- Juros e encargos do período: R$ 50,00\n"
                            "- 1% do principal (R$ 1.200): R$ 12,00\n\n"
                            "Qual é o pagamento mínimo desta fatura?"
                        ),
                        "competency_codes": ["4.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 62,00 (R$ 50 + R$ 12)."},
                            {"value": "b", "label": "R$ 120,00 (10% do total)."},
                            {"value": "c", "label": "R$ 50,00 (apenas os juros)."},
                            {"value": "d", "label": "R$ 180,00 (15% do total)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Mínimo = juros e encargos + 1% do principal:\n"
                            "R$ 50 + R$ 12 = **R$ 62,00**.\n\n"
                            "O saldo restante (R$ 1.200 − R$ 62 = R$ 1.138) entra no "
                            "crédito rotativo e sofrerá novos encargos no próximo período.\n\n"
                            "*(Taxa hipotética para fins didáticos.)*"
                        ),
                        "feedback_incorrect": (
                            "Mínimo = 100% dos juros/encargos + 1% do principal.\n"
                            "R$ 50 (juros) + R$ 12 (1% de R$ 1.200) = R$ 62,00.\n"
                            "O percentual fixo (10%, 15%) não é o critério da regra vigente.\n\n"
                            "*(Taxa hipotética para fins didáticos.)*"
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
                            "Com base no exemplo abaixo (todos os valores são fictícios "
                            "e usados apenas para fins didáticos), qual é o impacto de "
                            "pagar apenas o mínimo por 3 meses?\n\n"
                            "Fatura inicial: R$ 1.200,00\n"
                            "Taxa hipotética de juros rotativos: 12% ao mês\n"
                            "Pagamento mínimo mensal: R$ 150,00\n\n"
                            "Saldo após 3 meses (aproximado):\n"
                            "- Mês 1: (R$ 1.200 × 1,12) − R$ 150 = R$ 1.344 − R$ 150 = R$ 1.194\n"
                            "- Mês 2: (R$ 1.194 × 1,12) − R$ 150 = R$ 1.337,28 − R$ 150 = R$ 1.187,28\n"
                            "- Mês 3: (R$ 1.187,28 × 1,12) − R$ 150 ≈ R$ 1.329,75 − R$ 150 ≈ R$ 1.179,75\n\n"
                            "O que acontece com a dívida?"
                        ),
                        "competency_codes": ["4.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A dívida praticamente não diminui: após 3 meses pagando "
                                    "R$ 150/mês (total R$ 450), o saldo ainda está próximo "
                                    "de R$ 1.180 — quase o mesmo valor inicial."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "A dívida é quitada em 3 meses.",
                            },
                            {
                                "value": "c",
                                "label": "O saldo cai para zero se pagar o mínimo todo mês.",
                            },
                            {
                                "value": "d",
                                "label": "Os juros param de incidir após pagar o mínimo.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Pagou-se R$ 450 em 3 meses, mas a dívida caiu "
                            "apenas ~R$ 20 (de R$ 1.200 para ~R$ 1.180). "
                            "Isso acontece porque a taxa de juros consome quase todo "
                            "o pagamento mínimo — sobrando muito pouco para abater o principal.\n\n"
                            "*(Taxa de 12% a.m. é hipotética — usada apenas para fins "
                            "didáticos. Consulte as taxas reais do seu cartão.)*"
                        ),
                        "feedback_incorrect": (
                            "Com taxa hipotética de 12% a.m., os juros mensais sobre "
                            "R$ 1.200 são ~R$ 144. Um pagamento mínimo de R$ 150 abate "
                            "apenas ~R$ 6 do principal por mês. A dívida quase não cai.\n\n"
                            "*(Taxa de 12% a.m. é hipotética — usada apenas para fins "
                            "didáticos. Consulte as taxas reais do seu cartão.)*"
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
                            "O que é o crédito rotativo do cartão de crédito?"
                        ),
                        "competency_codes": ["4.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Uma modalidade de crédito automática acionada quando "
                                    "o titular não paga a fatura integralmente — o saldo "
                                    "restante fica sujeito a juros rotativos até ser quitado."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Um empréstimo pessoal solicitado na agência bancária.",
                            },
                            {
                                "value": "c",
                                "label": "Um desconto concedido pelo banco para bons pagadores.",
                            },
                            {
                                "value": "d",
                                "label": "O limite adicional disponível para compras parceladas.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O crédito rotativo é ativado automaticamente quando "
                            "o cliente não paga a fatura integralmente. O saldo não pago "
                            "vira uma dívida com juros rotativos — geralmente entre as "
                            "taxas mais altas do mercado de crédito. "
                            "Por lei, o rotativo só pode ser mantido por 30 dias consecutivos; "
                            "após isso, o banco deve oferecer parcelamento do saldo."
                        ),
                        "feedback_incorrect": (
                            "O crédito rotativo é uma modalidade de crédito automática: "
                            "quando você não paga a fatura inteira, o saldo restante "
                            "passa a ter juros rotativos cobrados pela operadora do cartão. "
                            "Não é um empréstimo solicitado — ocorre automaticamente "
                            "e costuma ter taxas muito elevadas."
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
                            "Fernanda tem uma fatura de R$ 800,00 e está pensando em "
                            "pagar apenas o mínimo de R$ 100,00.\n\n"
                            "Com base no que você aprendeu:\n"
                            "1. O que acontece com os R$ 700,00 restantes?\n"
                            "2. Por que pagar o mínimo pode ser uma armadilha financeira?\n"
                            "3. Que alternativas Fernanda poderia considerar se não "
                            "tiver os R$ 800 disponíveis agora?\n\n"
                            "(Não é necessário fazer cálculos exatos — explique o raciocínio.)"
                        ),
                        "competency_codes": ["4.3.2", "4.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Pontos esperados na resposta:\n\n"
                            "1. Os R$ 700 restantes entram no crédito rotativo e passam a "
                            "sofrer incidência de juros rotativos — geralmente as taxas mais "
                            "altas do mercado. A dívida cresce rapidamente.\n\n"
                            "2. A armadilha: os juros rotativos são tão altos que o mínimo "
                            "muitas vezes paga apenas (ou nem isso) os juros gerados — "
                            "o principal quase não diminui. A dívida pode ficar anos crescendo.\n\n"
                            "3. Alternativas possíveis:\n"
                            "   - Pedir parcelamento do saldo devedor (obrigatório pelo banco "
                            "     após 30 dias no rotativo)\n"
                            "   - Negociar diretamente com a operadora\n"
                            "   - Buscar empréstimo pessoal com taxa menor para quitar o cartão\n"
                            "   - Pagar o máximo possível (acima do mínimo) para reduzir o principal"
                        ),
                        "evaluation_criteria": [
                            "Explica que o saldo restante entra no crédito rotativo com juros altos.",
                            "Descreve por que pagar só o mínimo pode perpetuar a dívida.",
                            "Menciona ao menos uma alternativa ao rotativo.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você tem uma fatura de R$ 1.200,00 e precisa decidir quanto "
                            "pagar este mês. Veja as consequências de cada opção."
                        ),
                        "competency_codes": ["4.3.1", "4.3.2", "4.3.3"],
                        "scenario": (
                            "Fatura: R$ 1.200,00 | Renda: R$ 2.500,00 | Reserva: R$ 400,00\n"
                            "Taxa hipotética de juros rotativos: 10% a.m. (fictícia — fins didáticos)\n\n"
                            "Projeções:\n"
                            "- Mínimo (R$ 120): após 3 meses a dívida praticamente não caiu\n"
                            "- Parcial (R$ 600): saldo cai para R$ 600 → R$ 660 no mês seguinte\n"
                            "- Integral (R$ 1.200): dívida zerada, mas reserva vai a R$ 0\n\n"
                            "Qual valor você vai pagar?"
                        ),
                        "options": [
                            {
                                "value": "minimo",
                                "label": "Pagar apenas o mínimo de R$ 120,00.",
                            },
                            {
                                "value": "parcial",
                                "label": "Pagar R$ 600,00 (parcial — metade da fatura).",
                            },
                            {
                                "value": "integral",
                                "label": "Pagar R$ 1.200,00 (integral), zerando a reserva.",
                            },
                        ],
                        "correct_choice": "parcial",
                        "feedback_correct": (
                            "Boa decisão! Pagar R$ 600 reduz o principal pela metade e "
                            "mantém a reserva de R$ 400 intacta.\n\n"
                            "Com saldo de R$ 600 e taxa hipotética de 10% a.m., "
                            "os juros do próximo mês serão ~R$ 60 — muito menores "
                            "do que sobre os R$ 1.200 inteiros.\n"
                            "*(Taxa hipotética — verifique a real do seu cartão.)*"
                        ),
                        "feedback_incorrect": (
                            "Atenção à sua escolha:\n"
                            "- Mínimo (R$ 120): quase tudo vai para juros, dívida mal diminui.\n"
                            "- Integral (R$ 1.200): zera a dívida, mas também zera a reserva.\n\n"
                            "Pagar R$ 600 equilibra redução da dívida e preservação da reserva.\n"
                            "*(Taxa hipotética — consulte a real do seu cartão.)*"
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Pagamento mínimo: como é calculado desde 2024",
                    "order": 1,
                    "body": (
                        "Desde janeiro de 2024, a regra do pagamento mínimo do cartão "
                        "de crédito no Brasil é definida pela Lei 14.690/2023:\n\n"
                        "**Mínimo = 100% dos juros e encargos do período "
                        "+ 1% do valor principal da fatura**\n\n"
                        "Se a fatura total for inferior a R$ 100,00, o pagamento "
                        "mínimo é o valor integral da fatura.\n\n"
                        "**Por que isso importa:**\n"
                        "Antes, o mínimo era definido livremente pelas operadoras e "
                        "muitas vezes não cobria nem os juros — a dívida crescia mesmo "
                        "pagando o mínimo. A nova regra garante que o principal "
                        "sempre diminua ao menos 1% por mês.\n\n"
                        "**Atenção:** mesmo com a nova regra, pagar apenas o mínimo "
                        "faz a dívida durar muito tempo e gerar custo elevado."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Impacto de 3 meses pagando só o mínimo — exemplo fictício",
                    "order": 2,
                    "body": (
                        "**Todos os valores abaixo são fictícios e usados apenas "
                        "para fins didáticos. Não representam taxas reais.**\n\n"
                        "**Fatura inicial:** R$ 1.200,00\n"
                        "**Taxa hipotética de juros rotativos:** 12% a.m.\n"
                        "**Pagamento mínimo:** R$ 150,00/mês\n\n"
                        "| Mês | Saldo inicial | Juros (12%) | Após juros | Pago | Saldo final |\n"
                        "|---|---|---|---|---|---|\n"
                        "| 1 | R$ 1.200,00 | R$ 144,00 | R$ 1.344,00 | R$ 150,00 | R$ 1.194,00 |\n"
                        "| 2 | R$ 1.194,00 | R$ 143,28 | R$ 1.337,28 | R$ 150,00 | R$ 1.187,28 |\n"
                        "| 3 | R$ 1.187,28 | R$ 142,47 | R$ 1.329,75 | R$ 150,00 | R$ 1.179,75 |\n\n"
                        "**Resultado:** pagou R$ 450 em 3 meses, mas a dívida caiu "
                        "apenas ~R$ 20 (de R$ 1.200 para ~R$ 1.180).\n\n"
                        "R$ 429,75 dos R$ 450 pagos foram consumidos pelos juros.\n\n"
                        "*(Taxa de 12% a.m. é hipotética. Consulte a taxa real do seu cartão.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Crédito rotativo: o que é e por que é caro",
                    "order": 3,
                    "body": (
                        "O **crédito rotativo** é ativado automaticamente quando você "
                        "não paga a fatura integralmente. O saldo não pago se transforma "
                        "em uma dívida com juros rotativos cobrados pela operadora.\n\n"
                        "**Por que é caro:**\n"
                        "Os juros rotativos do cartão de crédito estão historicamente "
                        "entre as maiores taxas do mercado de crédito brasileiro.\n\n"
                        "**Limite do rotativo (regra vigente):**\n"
                        "O crédito rotativo só pode ser mantido por **30 dias** consecutivos. "
                        "Após esse prazo, o banco é obrigado a oferecer o parcelamento "
                        "do saldo devedor em condições mais acessíveis.\n\n"
                        "**Quando considerar alternativas ao rotativo:**\n"
                        "- Empréstimo pessoal com taxa menor (verifique e compare)\n"
                        "- Parcelamento do saldo (negociado com a operadora)\n"
                        "- Negociação direta da dívida com desconto\n\n"
                        "*(Consulte sempre as taxas reais do seu cartão e compare "
                        "com outras modalidades antes de decidir.)*"
                    ),
                },
            ],
        },
    ],
}
