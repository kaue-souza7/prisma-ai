"""Trilha 5 — Metas e reserva.

phase_number: 5 (existente — NÃO inserir nova fase)
Fonte editorial: docs/trilhas/trilha-05.md

Missões 1 e 3 são expansões (upsert sobre phase_3_v1.py missões 1 e 3).
Missões 2 e 4 são novas.
"""

TRAIL_5_V1 = {
    "phase_number": 5,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 5.1 — Por que poupar? (expansão sobre phase_3_v1 missão 1)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Por que poupar?",
            "description": (
                "Entenda a diferença entre reserva de emergência e meta financeira, "
                "e por que imprevistos acontecem com todo mundo."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.1.1",
                    "name": "Distinguir reserva de emergência de objetivo financeiro",
                    "description": (
                        "Explica que a reserva é para imprevistos (acesso imediato, "
                        "sem prazo definido) e o objetivo é para metas planejadas "
                        "(prazo e valor definidos)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.1.2",
                    "name": "Identificar por que imprevistos financeiros são inevitáveis",
                    "description": (
                        "Reconhece que eventos não planejados (desemprego, saúde, "
                        "equipamento quebrado) ocorrem independentemente de planejamento, "
                        "e que a reserva é a ferramenta de proteção."
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
                        "prompt": "Qual é a diferença entre reserva de emergência e meta financeira?",
                        "competency_codes": ["5.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "São a mesma coisa — qualquer dinheiro guardado "
                                    "serve para os dois fins."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Reserva é para imprevistos (acesso imediato, sem prazo); "
                                    "meta financeira é para objetivos planejados (valor e prazo definidos)."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Meta financeira é mais importante que a reserva — "
                                    "ela deve ser priorizada."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A reserva é segurança imediata — não tem data para usar, "
                            "mas precisa estar disponível a qualquer momento. "
                            "A meta financeira é planejada com valor e prazo (ex.: R$ 5.000 "
                            "em 10 meses). Os dois são importantes, mas a reserva vem primeiro."
                        ),
                        "feedback_incorrect": (
                            "Reserva e meta têm finalidades diferentes. "
                            "A reserva protege contra imprevistos — precisa estar acessível. "
                            "A meta é para objetivos planejados. "
                            "Misturar os dois cria problemas: se usar a meta para um imprevisto, "
                            "perde o objetivo; se usar a reserva para uma meta, fica vulnerável."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "A reserva de emergência deve ser usada para quê?",
                        "competency_codes": ["5.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Para aproveitar oportunidades de investimento.",
                            },
                            {
                                "value": "b",
                                "label": "Para gastos não planejados com consequências graves (saúde, desemprego, reparo urgente).",
                            },
                            {
                                "value": "c",
                                "label": "Para compras desejadas que o orçamento não cobre no mês.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A reserva existe para proteger o essencial "
                            "quando o inesperado acontece. Não é para investimento "
                            "(perderia liquidez) nem para desejos (esvazia a proteção)."
                        ),
                        "feedback_incorrect": (
                            "A reserva é para imprevistos com consequências graves — "
                            "não para oportunidades nem desejos. "
                            "Usar a reserva para desejos ou investimentos "
                            "deixa você sem proteção no próximo imprevisto."
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
                            "Ana tem R$ 2.000 guardados, mas está num parcelamento "
                            "de R$ 300/mês com juros. O que ela deveria priorizar? "
                            "(Situação fictícia.)"
                        ),
                        "competency_codes": ["5.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Manter a reserva intacta — segurança sempre primeiro.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Usar parte da reserva para quitar o parcelamento — "
                                    "os juros custam mais do que a reserva rende."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Não fazer nada — manter os dois em paralelo.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Com parcelamento com juros, quitar é mais eficiente "
                            "do que manter a reserva. Os juros que você paga superam "
                            "qualquer rendimento conservador da reserva. "
                            "Após quitar, recomponha a reserva gradualmente."
                        ),
                        "feedback_incorrect": (
                            "Quando há dívida com juros, quitar é prioridade — "
                            "você ganha o equivalente à taxa de juros ao se livrar dela. "
                            "Manter reserva enquanto paga juros altos é ineficiente. "
                            "Após quitar, reconstrua a reserva."
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
                            "Qual das situações abaixo justifica usar a reserva de emergência?"
                        ),
                        "competency_codes": ["5.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Viagem de férias planejada há 3 meses.",
                            },
                            {
                                "value": "b",
                                "label": "Conserto urgente do carro necessário para ir ao trabalho.",
                            },
                            {
                                "value": "c",
                                "label": "Compra de eletrônico em promoção.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O conserto do carro necessário para o trabalho "
                            "é um imprevisto com consequência grave — sem ele, "
                            "a renda pode ser comprometida. "
                            "A viagem e a promoção são planejáveis ou adiáveis."
                        ),
                        "feedback_incorrect": (
                            "A reserva é para imprevistos urgentes e essenciais. "
                            "Viagem planejada deve ser financiada por poupança programada. "
                            "Promoção de eletrônico é desejo, não emergência. "
                            "O conserto do carro (necessário para o trabalho) sim — "
                            "é um imprevisto com consequência direta na renda."
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
                            "Por que guardar o dinheiro da reserva em uma conta separada "
                            "da conta corrente é mais eficaz?"
                        ),
                        "competency_codes": ["5.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Porque a conta separada rende mais.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Porque separar cria uma barreira psicológica — "
                                    "o dinheiro não está disponível para gasto cotidiano."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Não faz diferença onde o dinheiro fica.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A separação física cria uma barreira psicológica. "
                            "Dinheiro na conta corrente convida ao gasto. "
                            "Dinheiro em conta separada exige ação deliberada para acessar "
                            "— o que reduz o gasto impulsivo da reserva."
                        ),
                        "feedback_incorrect": (
                            "A principal vantagem não é o rendimento — é a separação mental. "
                            "Manter a reserva na conta corrente facilita usá-la "
                            "para gastos do dia a dia sem perceber. "
                            "Uma conta separada cria uma barreira intencional."
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
                            "Explique a diferença entre reserva de emergência e objetivo "
                            "financeiro com um exemplo pessoal ou fictício. "
                            "Por que misturar os dois pode causar problemas?"
                        ),
                        "competency_codes": ["5.1.1"],
                        "feedback_static": (
                            "Exemplo esperado: 'Minha reserva é R$ 3.000 para emergências. "
                            "Meu objetivo é juntar R$ 5.000 para uma viagem em 12 meses. "
                            "Se eu usar a reserva para a viagem e aparecer um conserto "
                            "de carro inesperado, ficaria sem proteção e teria que usar "
                            "o crédito — com juros.'"
                        ),
                        "evaluation_criteria": [
                            "Distingue os dois conceitos com características corretas.",
                            "Usa um exemplo concreto (fictício ou real).",
                            "Explica a consequência de misturar os dois.",
                        ],
                        "max_length": 600,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "A diferença entre reserva de emergência e objetivo financeiro",
                    "order": 1,
                    "body": (
                        "**Reserva de emergência:** dinheiro guardado para situações "
                        "não planejadas e urgentes — desemprego, doença, conserto "
                        "urgente. Não tem prazo para usar, mas precisa estar disponível "
                        "imediatamente quando necessário.\n\n"
                        "**Objetivo financeiro:** dinheiro guardado para uma meta "
                        "específica com valor e prazo definidos — viagem, troca de "
                        "celular, entrada para imóvel.\n\n"
                        "**Por que separar:** misturar os dois significa que um imprevisto "
                        "pode destruir um objetivo, e usar o objetivo para emergência "
                        "deixa você sem proteção."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Por que imprevistos acontecem — e por que o dinheiro desaparece",
                    "order": 2,
                    "body": (
                        "Imprevistos financeiros são estatisticamente inevitáveis. "
                        "Não é questão de 'se', mas de 'quando'. Estudos de orçamento "
                        "familiar mostram que a maioria das famílias enfrenta pelo menos "
                        "um gasto não planejado relevante por ano.\n\n"
                        "**Por que o dinheiro desaparece:** sem separação clara, "
                        "o dinheiro 'disponível' tende a ser usado para gastos "
                        "do cotidiano antes que o imprevisto chegue. "
                        "Resultado: quando a emergência vem, o dinheiro não está mais lá."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O carro da Camila quebrou: quem está protegido e quem não está",
                    "order": 3,
                    "body": (
                        "**Camila A** tem R$ 3.500 de reserva em conta separada. "
                        "O carro dela precisou de R$ 1.200 de conserto urgente. "
                        "Ela pagou da reserva, continuou trabalhando e começou "
                        "a recompor a reserva nos meses seguintes. "
                        "*(Situação fictícia.)*\n\n"
                        "**Camila B** não tem reserva — tudo que ganhou foi gasto "
                        "no mês. Ela precisou pedir empréstimo pessoal de R$ 1.200 "
                        "com juros de 3%/mês. Em 6 meses, pagou R$ 1.200 + R$ 240 "
                        "de juros = R$ 1.440 no total.\n\n"
                        "**Diferença:** R$ 240 a mais — e meses de estresse financeiro."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A reserva não é investimento: ela é segurança",
                    "order": 4,
                    "body": (
                        "Um erro comum é tentar 'rentabilizar' a reserva em "
                        "investimentos de longo prazo ou com liquidez restrita.\n\n"
                        "**A reserva precisa de:**\n"
                        "- **Liquidez imediata:** disponível sem carência.\n"
                        "- **Segurança:** sem risco de perda do valor principal.\n"
                        "- **Separação:** conta diferente da corrente.\n\n"
                        "**Onde colocar:** conta de rendimento diário (CDB com liquidez "
                        "diária, fundo DI, conta remunerada). O rendimento é "
                        "secundário — o que importa é estar disponível quando "
                        "você precisar."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Quanto tempo falta para uma emergência sem reserva?",
                    "order": 5,
                    "body": (
                        "Sem reserva, um imprevisto força uma das escolhas:\n\n"
                        "1. **Usar o crédito** (cartão ou empréstimo) — paga juros altos.\n"
                        "2. **Não pagar essenciais** — risco de negativação e despejo.\n"
                        "3. **Pedir dinheiro emprestado** — impacta relacionamentos.\n\n"
                        "Cada uma dessas escolhas custa mais caro do que teria custado "
                        "guardar R$ 200 por mês durante 12 meses (R$ 2.400).\n\n"
                        "A reserva não elimina o problema — ela elimina o custo extra "
                        "de lidar com ele sem planejamento."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois perfis: com reserva e sem reserva no mesmo imprevisto",
                    "order": 6,
                    "body": (
                        "**Imprevisto:** geladeira quebrou, conserto R$ 800. "
                        "*(Valores fictícios.)*\n\n"
                        "| | Com reserva (R$ 4.000) | Sem reserva |\n"
                        "|---|---|---|\n"
                        "| Ação | Paga da reserva | Usa cartão de crédito |\n"
                        "| Custo total | R$ 800 | R$ 800 + juros do rotativo |\n"
                        "| Tempo para resolver | Imediato | Meses pagando parcelas |\n"
                        "| Impacto no orçamento | Recompõe gradualmente | Compromete renda futura |\n\n"
                        "**Conclusão:** a reserva não economiza no valor do imprevisto — "
                        "economiza nos juros e no estresse de resolver sem planejamento."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 5.2 — Calculando a reserva de emergência (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Calculando a reserva de emergência",
            "description": (
                "Calcule o tamanho ideal da sua reserva de emergência com base "
                "nas despesas essenciais, na estabilidade da renda e no número "
                "de dependentes, e descubra quanto guardar por mês para formá-la."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.2.1",
                    "name": "Calcular o tamanho ideal da reserva de emergência",
                    "description": (
                        "Multiplica as despesas essenciais mensais pelo número "
                        "de meses recomendado para obter o valor-alvo da reserva."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.2.2",
                    "name": "Ajustar o número de meses conforme renda e dependentes",
                    "description": (
                        "Identifica que trabalhadores CLT precisam de menos meses "
                        "de reserva do que autônomos ou quem tem renda irregular, "
                        "e que dependentes aumentam o tamanho recomendado."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.2.3",
                    "name": "Determinar o aporte mensal para formar a reserva",
                    "description": (
                        "Divide o valor-alvo da reserva pelo número de meses "
                        "disponíveis para calcular o aporte mensal necessário."
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
                            "João é CLT, sem dependentes, com despesas essenciais de "
                            "R$ 2.500 por mês. Qual é a faixa de reserva de emergência "
                            "recomendada para ele?"
                        ),
                        "competency_codes": ["5.2.1", "5.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "R$ 2.500 (1 mês de essenciais).",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "R$ 7.500 a R$ 15.000 "
                                    "(3 a 6 meses de essenciais)."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "R$ 15.000 a R$ 30.000 "
                                    "(6 a 12 meses de essenciais)."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "R$ 5.000 (valor fixo recomendado para CLT).",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Para um trabalhador CLT sem dependentes, "
                            "a recomendação é de 3 a 6 meses de despesas essenciais: "
                            "3 × R$ 2.500 = R$ 7.500 e 6 × R$ 2.500 = R$ 15.000. "
                            "A renda CLT é mais estável, o que justifica um intervalo menor."
                        ),
                        "feedback_incorrect": (
                            "A faixa recomendada para CLT sem dependentes é de 3 a 6 meses "
                            "de despesas essenciais. Com R$ 2.500 de essenciais: "
                            "3 × 2.500 = R$ 7.500 (mínimo) e 6 × 2.500 = R$ 15.000 (máximo). "
                            "A renda CLT é mais previsível, então o intervalo é menor."
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
                            "Marina é freelancer com renda irregular e tem dois filhos "
                            "dependentes. Suas despesas essenciais somam R$ 3.000 por mês. "
                            "Quantos meses de reserva ela deve buscar, comparado a um "
                            "CLT sem dependentes?"
                        ),
                        "competency_codes": ["5.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "O mesmo número de meses — o perfil não importa.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Menos meses, pois freelancers gastam menos "
                                    "com transporte."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Mais meses — renda irregular e dependentes "
                                    "aumentam o número recomendado (6 a 12 meses)."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Menos meses, porque freelancers têm mais "
                                    "liberdade para cortar gastos."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! Renda irregular aumenta o risco de ficar sem entrada, "
                            "e dependentes ampliam as despesas essenciais que precisam "
                            "ser cobertas. Por isso, para Marina, a recomendação sobe para "
                            "6 a 12 meses: entre R$ 18.000 e R$ 36.000."
                        ),
                        "feedback_incorrect": (
                            "O perfil importa muito. Renda irregular significa que os meses "
                            "sem receita podem se estender, e dependentes tornam as despesas "
                            "maiores e mais difíceis de cortar em crise. "
                            "Para Marina, a recomendação é 6 a 12 meses de essenciais."
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
                            "João (CLT, sem dependentes, R$ 2.500 de essenciais) quer "
                            "formar a reserva mínima recomendada (R$ 7.500) em 15 meses. "
                            "Quanto ele precisa guardar por mês?"
                        ),
                        "competency_codes": ["5.2.3"],
                        "options": [
                            {"value": "a", "label": "R$ 250 por mês."},
                            {"value": "b", "label": "R$ 750 por mês."},
                            {"value": "c", "label": "R$ 500 por mês."},
                            {"value": "d", "label": "R$ 625 por mês."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! R$ 7.500 ÷ 15 meses = R$ 500 por mês. "
                            "Se quiser chegar ao máximo da faixa CLT (R$ 15.000) em 30 meses, "
                            "o aporte é o mesmo: R$ 15.000 ÷ 30 = R$ 500 por mês."
                        ),
                        "feedback_incorrect": (
                            "A conta é simples: valor-alvo ÷ meses disponíveis = aporte mensal. "
                            "R$ 7.500 ÷ 15 = R$ 500 por mês. "
                            "Para chegar ao teto (R$ 15.000) em 30 meses, o aporte é igual."
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
                            "Dois trabalhadores têm as mesmas despesas essenciais: R$ 2.000 "
                            "por mês. Pedro é CLT com carteira assinada há 3 anos; "
                            "Caio é autônomo com renda que varia bastante todo mês. "
                            "Qual dos dois precisa de uma reserva maior?"
                        ),
                        "competency_codes": ["5.2.2"],
                        "options": [
                            {"value": "a", "label": "Pedro, porque tem mais responsabilidade."},
                            {
                                "value": "b",
                                "label": (
                                    "Caio, porque renda irregular aumenta o risco "
                                    "de meses sem entrada."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Os dois precisam da mesma reserva.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pedro, porque CLT tem mais despesas "
                                    "com transporte."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A renda irregular do Caio pode ficar zerando em meses "
                            "ruins, então ele precisa de uma rede de segurança maior — "
                            "entre 6 e 12 meses de essenciais. Pedro, com renda CLT estável, "
                            "pode trabalhar com 3 a 6 meses."
                        ),
                        "feedback_incorrect": (
                            "O principal fator é a estabilidade da renda. "
                            "Caio, autônomo com renda variável, corre mais risco de ficar "
                            "sem entrada por meses seguidos. Por isso precisa de uma reserva "
                            "maior: 6 a 12 meses de essenciais, contra 3 a 6 de Pedro."
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
                            "Estime as suas próprias despesas essenciais mensais "
                            "(aluguel ou moradia, alimentação, transporte, saúde e "
                            "contas básicas). Com base no seu perfil de renda "
                            "(CLT, autônomo, estudante etc.) e no número de pessoas "
                            "que dependem de você, quantos meses de reserva você "
                            "acha que deveria ter? Calcule o valor-alvo e o aporte "
                            "mensal necessário para chegar lá em 24 meses."
                        ),
                        "competency_codes": ["5.2.1", "5.2.2", "5.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado.\n\n"
                            "Exemplo de cálculo esperado:\n"
                            "- Despesas essenciais: R$ X por mês\n"
                            "- Número de meses recomendado: Y (3–6 para CLT, "
                            "6–12 para autônomo/irregular)\n"
                            "- Valor-alvo: R$ X × Y\n"
                            "- Aporte mensal para 24 meses: valor-alvo ÷ 24"
                        ),
                        "evaluation_criteria": [
                            "Estima as despesas essenciais mensais com alguma especificação.",
                            (
                                "Justifica o número de meses com base no perfil "
                                "de renda e/ou dependentes."
                            ),
                            (
                                "Calcula o valor-alvo corretamente "
                                "(despesas × meses)."
                            ),
                            (
                                "Calcula o aporte mensal dividindo o valor-alvo "
                                "pelo prazo desejado."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Três perfis, três reservas. Leia cada perfil e escolha "
                            "a faixa de reserva e o aporte mensal corretos para todos."
                        ),
                        "competency_codes": ["5.2.1", "5.2.2", "5.2.3"],
                        "scenario": (
                            "**Perfil A — Ana:** CLT, sem dependentes, "
                            "despesas essenciais R$ 1.800/mês. Quer formar a reserva "
                            "mínima em 18 meses.\n\n"
                            "**Perfil B — Bruno:** Freelancer, renda irregular, sem "
                            "dependentes, despesas essenciais R$ 1.800/mês. Quer "
                            "formar a reserva mínima em 18 meses.\n\n"
                            "**Perfil C — Carla:** Autônoma, 2 filhos dependentes, "
                            "despesas essenciais R$ 1.800/mês. Quer formar a reserva "
                            "mínima em 18 meses.\n\n"
                            "(Valores fictícios, para fins didáticos.)"
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Ana: reserva mínima R$ 5.400 (3 meses), "
                                    "aporte R$ 300/mês. "
                                    "Bruno: reserva mínima R$ 10.800 (6 meses), "
                                    "aporte R$ 600/mês. "
                                    "Carla: reserva mínima R$ 10.800 (6 meses), "
                                    "aporte R$ 600/mês."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Ana: reserva mínima R$ 5.400 (3 meses), "
                                    "aporte R$ 300/mês. "
                                    "Bruno: reserva mínima R$ 10.800 (6 meses), "
                                    "aporte R$ 600/mês. "
                                    "Carla: reserva mínima R$ 21.600 (12 meses), "
                                    "aporte R$ 1.200/mês."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ana: reserva mínima R$ 10.800 (6 meses), "
                                    "aporte R$ 600/mês. "
                                    "Bruno: reserva mínima R$ 5.400 (3 meses), "
                                    "aporte R$ 300/mês. "
                                    "Carla: reserva mínima R$ 10.800 (6 meses), "
                                    "aporte R$ 600/mês."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Os três têm as mesmas despesas essenciais, "
                                    "então a reserva e o aporte são iguais para todos."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Muito bem! Ana (CLT, sem dependentes) fica na faixa de 3 a 6 meses: "
                            "mínimo R$ 5.400 → aporte R$ 300/mês em 18 meses. "
                            "Bruno (freelancer, sem dependentes) precisa de 6 a 12 meses: "
                            "mínimo R$ 10.800 → aporte R$ 600/mês. "
                            "Carla (autônoma, 2 dependentes) também precisa de 6 a 12 meses: "
                            "mínimo R$ 10.800 → aporte R$ 600/mês. "
                            "Os dependentes aumentam o número recomendado, mas o ponto de "
                            "partida para autônomos já é 6 meses — e o máximo sobe para 12."
                        ),
                        "feedback_incorrect": (
                            "Revise os perfis. "
                            "CLT sem dependentes: 3 a 6 meses de essenciais. "
                            "Autônomo/freelancer sem dependentes: 6 a 12 meses. "
                            "Autônoma com dependentes: 6 a 12 meses (e o máximo pode ser maior). "
                            "O aporte mensal é sempre: valor-alvo ÷ meses disponíveis."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como calcular o tamanho da sua reserva de emergência",
                    "order": 1,
                    "body": (
                        "A reserva de emergência não tem um valor fixo universal. "
                        "Ela depende de três fatores:\n\n"
                        "**1. Despesas essenciais mensais**\n"
                        "Calcule apenas o que você *precisa* pagar para manter o básico: "
                        "moradia, alimentação, transporte, saúde e contas essenciais. "
                        "Gastos variáveis e lazer ficam de fora desse cálculo.\n\n"
                        "**2. Estabilidade da renda**\n"
                        "- **CLT (carteira assinada):** renda previsível, aviso-prévio garantido "
                        "em caso de demissão → recomendação: **3 a 6 meses** de essenciais.\n"
                        "- **Autônomo ou renda irregular:** os meses ruins podem zerar "
                        "a entrada → recomendação: **6 a 12 meses** de essenciais.\n\n"
                        "**3. Número de dependentes**\n"
                        "Cada dependente adiciona despesas que não podem ser cortadas "
                        "em crise. Quem tem filhos ou outros dependentes deve caminhar "
                        "para o teto superior da faixa recomendada.\n\n"
                        "**Fórmula:**\n"
                        "valor-alvo = despesas essenciais × número de meses recomendado\n\n"
                        "**Aporte mensal:**\n"
                        "aporte = valor-alvo ÷ meses disponíveis para formar a reserva"
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois perfis, dois cálculos",
                    "order": 2,
                    "body": (
                        "**Perfil 1 — João (CLT, sem dependentes)**\n"
                        "- Despesas essenciais: R$ 2.500/mês\n"
                        "- Faixa recomendada: 3 a 6 meses\n"
                        "- Reserva mínima: 3 × R$ 2.500 = **R$ 7.500**\n"
                        "- Reserva ideal: 6 × R$ 2.500 = **R$ 15.000**\n"
                        "- Guardando R$ 500/mês: chega ao mínimo em 15 meses "
                        "e ao ideal em 30 meses.\n\n"
                        "**Perfil 2 — Marina (freelancer, 2 dependentes)**\n"
                        "- Despesas essenciais: R$ 2.500/mês\n"
                        "- Faixa recomendada: 6 a 12 meses\n"
                        "- Reserva mínima: 6 × R$ 2.500 = **R$ 15.000**\n"
                        "- Reserva ideal: 12 × R$ 2.500 = **R$ 30.000**\n"
                        "- Guardando R$ 500/mês: chega ao mínimo em 30 meses "
                        "e ao ideal em 60 meses.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Onde guardar a reserva de emergência",
                    "order": 3,
                    "body": (
                        "A reserva de emergência tem três requisitos que vêm antes "
                        "de qualquer rentabilidade:\n\n"
                        "1. **Liquidez:** você precisa conseguir resgatar o dinheiro "
                        "rapidamente — de preferência no mesmo dia ou no dia seguinte.\n"
                        "2. **Segurança:** o valor não pode ficar exposto a risco de "
                        "perda. Oscilações de mercado não cabem na reserva.\n"
                        "3. **Acessibilidade:** o dinheiro precisa estar disponível "
                        "a qualquer momento, inclusive em feriados ou fins de semana.\n\n"
                        "Escolha o lugar onde guardar com base nessas três "
                        "características — não apenas na taxa de retorno. "
                        "Uma pequena diferença de rendimento não vale se você não "
                        "conseguir acessar o dinheiro quando mais precisar."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 5.3 — Atingindo a meta (expansão sobre phase_3_v1 missão 3)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Atingindo a meta",
            "description": (
                "Formule uma meta financeira com valor e prazo, calcule o aporte "
                "mensal necessário e saiba como revisar o plano quando a vida muda."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.3.1",
                    "name": "Formular uma meta financeira com valor e prazo",
                    "description": (
                        "Define uma meta com valor-alvo numérico e prazo em meses, "
                        "tornando o objetivo concreto e mensurável."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.3.2",
                    "name": "Calcular o aporte mensal necessário para atingir a meta",
                    "description": (
                        "Aplica a fórmula aporte = meta / meses e ajusta conforme "
                        "o orçamento disponível."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.4.2",
                    "name": "Revisar e atualizar a meta conforme a vida muda",
                    "description": (
                        "Reconhece quando e como ajustar uma meta (valor, prazo "
                        "ou aporte) diante de mudanças de renda ou prioridade."
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
                            "Para juntar R$ 6.000 em 12 meses, "
                            "qual aporte mensal é necessário? (Valores fictícios.)"
                        ),
                        "competency_codes": ["5.3.1", "5.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 400/mês."},
                            {"value": "b", "label": "R$ 500/mês."},
                            {"value": "c", "label": "R$ 600/mês."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! R$ 6.000 ÷ 12 meses = R$ 500/mês. "
                            "Se o orçamento não comportar R$ 500, você pode aumentar "
                            "o prazo (ex.: R$ 400/mês × 15 meses) ou reduzir a meta."
                        ),
                        "feedback_incorrect": (
                            "A fórmula é simples: meta ÷ meses = aporte. "
                            "R$ 6.000 ÷ 12 = R$ 500/mês. "
                            "Se não couber no orçamento, ajuste o prazo ou o valor da meta."
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
                            "Ana guardou R$ 1.800 dos R$ 3.000 planejados para os "
                            "próximos 6 meses. A meta original era juntar tudo em 10 meses "
                            "com R$ 300/mês. Ela ainda pode manter a meta? (Situação fictícia.)"
                        ),
                        "competency_codes": ["5.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Sim — faltam R$ 1.200 e ainda há 4 meses (R$ 300/mês).",
                            },
                            {
                                "value": "b",
                                "label": "Não — a meta falhou, deve ser cancelada.",
                            },
                            {
                                "value": "c",
                                "label": "Sim, mas precisará aumentar o aporte ou o prazo.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Com R$ 1.800 guardados e 4 meses restantes, "
                            "Ana precisa de R$ 1.200 mais — exatamente R$ 300/mês. "
                            "A meta original ainda é factível se ela manter o aporte."
                        ),
                        "feedback_incorrect": (
                            "A meta não falhou — ela está no prazo. "
                            "R$ 1.800 em 6 meses = R$ 300/mês (correto). "
                            "Faltam R$ 1.200 em 4 meses = R$ 300/mês. "
                            "A meta original ainda pode ser atingida."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos quer juntar R$ 4.800 para trocar o notebook. "
                            "Renda líquida: R$ 2.200/mês. "
                            "Despesas essenciais: R$ 1.500/mês. "
                            "Sobra: R$ 700/mês.\n\n"
                            "Como Carlos deve estruturar sua meta? (Valores fictícios.)"
                        ),
                        "competency_codes": ["5.3.1", "5.3.2"],
                        "scenario": (
                            "Carlos, renda R$ 2.200, sobra R$ 700/mês após essenciais. "
                            "Sem reserva ainda. Situação fictícia."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Guardar R$ 400/mês para a reserva e R$ 300/mês para "
                                    "o notebook. Atingirá os R$ 4.800 em 16 meses."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Guardar R$ 700/mês só para o notebook. "
                                    "Atingirá os R$ 4.800 em ~7 meses."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não guardar nada — esperar a renda aumentar."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Boa decisão! Dividir a sobra entre reserva e meta "
                            "é a abordagem mais equilibrada. "
                            "Carlos constrói proteção (reserva) ao mesmo tempo "
                            "que avança na meta. Em 16 meses tem o notebook "
                            "e em paralelo vai acumulando a reserva."
                        ),
                        "feedback_incorrect": (
                            "Guardar tudo para o notebook deixa Carlos sem proteção. "
                            "Se aparecer um imprevisto nos 7 meses, ele usaria o "
                            "dinheiro do notebook e perderia o progresso. "
                            "A opção A é mais prudente: constrói reserva e meta em paralelo."
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
                            "Qual é a melhor ação quando o orçamento não permite "
                            "mais o aporte planejado para a meta?"
                        ),
                        "competency_codes": ["5.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Abandonar a meta — não funciona mais.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Ajustar o aporte para o valor possível e "
                                    "estender o prazo da meta."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Usar crédito para continuar no ritmo original."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Ajustar é sempre melhor do que abandonar ou usar crédito. "
                            "Uma meta com prazo estendido ainda é uma meta — "
                            "e sem a dívida que o crédito criaria."
                        ),
                        "feedback_incorrect": (
                            "Abandonar desperdiça o progresso. Usar crédito cria custo extra. "
                            "A melhor opção é ajustar o aporte e estender o prazo — "
                            "a meta continua existindo, apenas em ritmo diferente."
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
                            "Crie uma meta financeira pessoal ou fictícia. "
                            "Defina: o que quer, quanto custa, em quantos meses "
                            "quer atingir e qual seria o aporte mensal. "
                            "Verifique se o aporte cabe no orçamento fictício "
                            "de R$ 2.000 líquidos com R$ 1.400 de despesas essenciais."
                        ),
                        "competency_codes": ["5.3.1", "5.3.2"],
                        "feedback_static": (
                            "Uma boa meta tem: objetivo claro (ex.: notebook R$ 2.400), "
                            "prazo definido (ex.: 8 meses) e aporte calculado "
                            "(R$ 2.400 ÷ 8 = R$ 300/mês). "
                            "Com sobra de R$ 600, cabe no orçamento."
                        ),
                        "evaluation_criteria": [
                            "Define objetivo com valor numérico.",
                            "Define prazo em meses.",
                            "Calcula o aporte mensal corretamente.",
                            "Verifica se o aporte cabe no orçamento.",
                        ],
                        "max_length": 600,
                    },
                },
                {
                    "order": 6,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Por que revisar a meta periodicamente é mais saudável "
                            "do que abandoná-la quando a vida muda?"
                        ),
                        "competency_codes": ["5.4.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Porque uma meta não pode ser mudada após criada.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Porque ajustar preserva o progresso já feito e "
                                    "adapta o plano à realidade atual, sem perder o objetivo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Porque revisar sempre resulta numa meta maior.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Revisar é adaptar — não desistir. "
                            "O progresso já feito continua valendo. "
                            "A meta ajustada ao contexto atual é mais sustentável "
                            "do que uma meta original que se tornou impossível."
                        ),
                        "feedback_incorrect": (
                            "Metas podem e devem ser ajustadas quando a vida muda. "
                            "Abandonar perde tudo; manter o original pode ser impossível. "
                            "Revisar adapta sem desperdiçar o progresso."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como definir uma meta: valor, prazo e objetivo",
                    "order": 1,
                    "body": (
                        "Uma boa meta financeira tem três elementos:\n\n"
                        "**1. Objetivo claro:** o que você quer? "
                        "(Ex.: trocar o notebook, fazer uma viagem, quitar uma dívida)\n\n"
                        "**2. Valor:** quanto custa? Pesquise o valor atual — "
                        "metas sem número são desejos vagos.\n\n"
                        "**3. Prazo:** em quantos meses quer atingir?\n\n"
                        "Com esses três, você calcula o aporte: **aporte = valor ÷ meses**.\n\n"
                        "Exemplo: R$ 3.000 em 10 meses = R$ 300/mês. "
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Aporte mensal: fórmula e ajuste pelo orçamento",
                    "order": 2,
                    "body": (
                        "**Fórmula:** aporte = meta ÷ prazo\n\n"
                        "Se o aporte não cabe no orçamento, você tem duas opções:\n\n"
                        "1. **Aumentar o prazo:** guardar menos por mês, por mais tempo.\n"
                        "   Ex.: R$ 300/mês × 10 meses → R$ 200/mês × 15 meses\n\n"
                        "2. **Reduzir a meta:** aceitar uma versão menor do objetivo.\n"
                        "   Ex.: notebook de R$ 3.000 → notebook de R$ 2.000\n\n"
                        "O que você NÃO deve fazer: usar crédito para compensar "
                        "um aporte impossível de pagar."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A meta da Ana: R$ 3.000 em 10 meses",
                    "order": 3,
                    "body": (
                        "**Ana** quer tirar férias e precisa de R$ 3.000. "
                        "Prazo: 10 meses. *(Fictício, para fins didáticos.)*\n\n"
                        "Aporte: R$ 3.000 ÷ 10 = **R$ 300/mês**.\n\n"
                        "Ana separa os R$ 300 no dia do recebimento do salário, "
                        "antes de qualquer outro gasto.\n\n"
                        "**Mês 6:** Ana recebeu uma conta inesperada e só conseguiu "
                        "guardar R$ 150. Ela ajustou o prazo:\n\n"
                        "Saldo atual: R$ 1.650 (R$ 300×5 + R$ 150). "
                        "Faltam R$ 1.350. Novo prazo: R$ 1.350 ÷ R$ 300 = 4,5 meses — "
                        "arredondando para 5 meses.\n\n"
                        "Ana não desistiu — ajustou o prazo em 1 mês."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "O que fazer quando a meta parece impossível",
                    "order": 4,
                    "body": (
                        "Se em algum mês você não conseguir fazer o aporte completo, "
                        "não abandone a meta. Tente estas estratégias:\n\n"
                        "1. **Guarde o que puder** — mesmo R$ 50 mantém o hábito.\n\n"
                        "2. **Revise o prazo** — estender 1 ou 2 meses é melhor "
                        "do que zerar tudo.\n\n"
                        "3. **Reduza outra categoria** — lazer pode ceder temporariamente "
                        "para manter a meta.\n\n"
                        "4. **Não use crédito** — financiar uma meta transforma "
                        "um objetivo em dívida."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Revisão semestral da meta: quando mudar o plano",
                    "order": 5,
                    "body": (
                        "Revise a meta quando:\n\n"
                        "- **A renda mudou** (aumento, redução, novo emprego)\n"
                        "- **O custo do objetivo mudou** (produto ficou mais caro ou barato)\n"
                        "- **A prioridade mudou** (surgiu algo mais urgente)\n\n"
                        "Revisão semestral é uma boa cadência para a maioria das metas. "
                        "Na revisão, recalcule: valor atualizado ÷ meses restantes = "
                        "novo aporte.\n\n"
                        "Uma meta revisada ainda é uma meta — não é fracasso."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O que acontece quando a meta muda no meio do caminho",
                    "order": 6,
                    "body": (
                        "**Pedro** queria juntar R$ 5.000 para uma viagem em 12 meses "
                        "(R$ 417/mês). No mês 8, ele guardou R$ 3.336 "
                        "quando surgiu uma oportunidade de emprego melhor, mas "
                        "precisaria investir R$ 800 em cursos para qualificação. "
                        "*(Situação fictícia.)*\n\n"
                        "**Opções:**\n"
                        "A) Usar parte da meta (R$ 800) e estender o prazo → viagem "
                        "em 15 meses em vez de 12.\n"
                        "B) Abandonar a meta → perde R$ 3.336 de progresso.\n"
                        "C) Não fazer o curso → perde a oportunidade.\n\n"
                        "**Pedro escolheu A:** usou R$ 800 da meta para o curso, "
                        "ficou com R$ 2.536, e ajustou o prazo da viagem para 6 meses "
                        "mais (total 18 meses desde o início). "
                        "Investiu na carreira sem perder o objetivo."
                    ),
                },
            ],
        },

        # ──────────────────────────────────────────────────────────────────
        # Missão 5.4 — Usando e revisando a reserva (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Usando e revisando a reserva",
            "description": (
                "Aprenda a distinguir emergências reais de desejos, a recompor "
                "a reserva depois de usá-la e a revisá-la quando sua vida financeira "
                "mudar."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.4.1",
                    "name": "Distinguir situações que justificam usar a reserva",
                    "description": (
                        "Diferencia imprevistos urgentes e não planejados de "
                        "desejos e gastos planejáveis, usando a reserva apenas "
                        "para os primeiros."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.4.2",
                    "name": "Planejar a recomposição da reserva após uso",
                    "description": (
                        "Calcula o prazo para recompor a reserva após uso parcial "
                        "ou total, ajustando o aporte mensal conforme necessário."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.4.3",
                    "name": "Revisar o tamanho da reserva diante de mudanças",
                    "description": (
                        "Reconhece que mudanças na renda, nos gastos essenciais ou "
                        "na composição familiar exigem recalcular o valor-alvo da reserva."
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
                            "Qual das situações abaixo justifica usar a reserva "
                            "de emergência?"
                        ),
                        "competency_codes": ["5.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Aproveitar uma promoção de passagem aérea "
                                    "para uma viagem de lazer."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Comprar um presente de aniversário que "
                                    "será daqui a duas semanas."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Cobrir as despesas essenciais após perder "
                                    "o emprego inesperadamente."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pagar a primeira parcela de um curso que "
                                    "você planejou fazer."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Perder o emprego sem aviso é um imprevisto real: "
                            "a renda para e as despesas essenciais continuam. "
                            "A reserva existe exatamente para cobrir esse tipo de situação. "
                            "Promoção, presente e curso são gastos que podem (e devem) "
                            "ser planejados separadamente."
                        ),
                        "feedback_incorrect": (
                            "A reserva é para imprevistos urgentes e não planejados. "
                            "Promoção é um desejo; presente e curso são gastos planejáveis. "
                            "A única situação que justifica a reserva é o imprevisto real: "
                            "perda de emprego que interrompe a renda sem aviso."
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
                            "Rafaela tinha uma reserva de R$ 6.000 e usou R$ 2.400 "
                            "(40%) para consertar o carro, que quebrou de forma "
                            "inesperada e era essencial para o trabalho. "
                            "Ela pode guardar R$ 300 por mês. "
                            "Em quantos meses ela repõe os R$ 2.400?"
                        ),
                        "competency_codes": ["5.4.2"],
                        "options": [
                            {"value": "a", "label": "4 meses."},
                            {"value": "b", "label": "6 meses."},
                            {"value": "c", "label": "8 meses."},
                            {"value": "d", "label": "12 meses."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! R$ 2.400 ÷ R$ 300/mês = 8 meses para recompor "
                            "o valor usado. Rafaela usou a reserva da forma certa — "
                            "agora é hora de repô-la antes de qualquer outro gasto "
                            "não essencial."
                        ),
                        "feedback_incorrect": (
                            "A conta é simples: valor usado ÷ aporte mensal = meses para recompor. "
                            "R$ 2.400 ÷ R$ 300 = 8 meses. "
                            "Até lá, Rafaela está com a reserva reduzida — "
                            "repor deve ser a prioridade."
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
                            "Felipe tinha uma reserva adequada como CLT. Ele se "
                            "tornou autônomo e suas despesas essenciais também "
                            "aumentaram 20% com a chegada de um filho. "
                            "O que ele deve fazer com a reserva?"
                        ),
                        "competency_codes": ["5.4.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Manter a reserva como está — "
                                    "o valor já é suficiente."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Recalcular o valor-alvo com base nas novas "
                                    "despesas essenciais e no novo perfil de renda, "
                                    "e ampliar a reserva."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Usar parte da reserva para cobrir as novas "
                                    "despesas do filho."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Reduzir a reserva, pois autônomos ganham mais."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! Quando a renda muda de CLT para autônoma, "
                            "o número de meses recomendado sobe de 3–6 para 6–12. "
                            "Com despesas maiores por causa do filho, o valor-alvo "
                            "aumenta ainda mais. Felipe precisa recalcular e ampliar a reserva."
                        ),
                        "feedback_incorrect": (
                            "Mudanças na renda e na composição familiar sempre pedem "
                            "uma revisão da reserva. Como autônomo com um dependente, "
                            "Felipe agora precisa de 6 a 12 meses de despesas essenciais — "
                            "e as despesas essenciais ficaram maiores. "
                            "A reserva antiga já não é mais suficiente."
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
                            "Pense em uma situação em que você (ou alguém próximo) "
                            "usou dinheiro reservado para algo que, na reflexão, "
                            "era um desejo e não uma emergência. "
                            "O que você faria diferente hoje? "
                            "Como separaria o que é imprevisto real do que é desejo?"
                        ),
                        "competency_codes": ["5.4.1"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            "Descreve uma situação concreta de uso do dinheiro reservado.",
                            (
                                "Identifica se o gasto era um imprevisto real "
                                "ou um desejo."
                            ),
                            (
                                "Propõe uma alternativa — como separar os "
                                "dois tipos de situação ou criar uma conta "
                                "separada para desejos."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 5,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Rafaela usou 40% da reserva. Ajude-a a decidir como "
                            "recompor mais rápido."
                        ),
                        "competency_codes": ["5.4.2", "5.4.3"],
                        "scenario": (
                            "Rafaela é CLT, sem dependentes. "
                            "Ela tinha R$ 6.000 na reserva (equivalente a ~3 meses "
                            "de essenciais de R$ 2.000). Usou R$ 2.400 para consertar "
                            "o carro. Sobram R$ 3.600 na reserva.\n\n"
                            "Renda líquida atual: R$ 2.800/mês.\n"
                            "Despesas essenciais: R$ 2.000/mês.\n"
                            "Despesas não essenciais atuais: R$ 480/mês "
                            "(streaming R$ 80, delivery R$ 200, academia R$ 120, "
                            "roupas R$ 80).\n"
                            "Aporte atual para recompor a reserva: R$ 300/mês "
                            "(sobra após essenciais e não essenciais).\n\n"
                            "A Rafaela quer recompor os R$ 2.400 o mais rápido possível "
                            "sem comprometer o essencial.\n\n"
                            "(Valores fictícios, para fins didáticos.)"
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Manter tudo como está e recompor com R$ 300/mês "
                                    "em 8 meses. Não cortar nenhum gasto não essencial."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Suspender temporariamente delivery (R$ 200) e roupas (R$ 80), "
                                    "realocar para a reserva: aporte sobe para R$ 580/mês. "
                                    "Recompõe R$ 2.400 em ~4 meses."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Cortar toda a alimentação fora de casa e "
                                    "cancelar a academia para recompor em 3 meses. "
                                    "Total realocado: R$ 320 + outros."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pegar um empréstimo pessoal de R$ 2.400 para "
                                    "repor a reserva imediatamente e pagar em parcelas."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! Suspender temporariamente delivery e roupas — "
                            "gastos não essenciais — libera R$ 280/mês adicionais. "
                            "O aporte sobe de R$ 300 para R$ 580/mês, e Rafaela recompõe "
                            "os R$ 2.400 em pouco mais de 4 meses, sem comprometer o essencial "
                            "e sem criar uma nova dívida. Depois de recompor, ela pode "
                            "voltar a ter lazer com o orçamento recalibrado."
                        ),
                        "feedback_incorrect": (
                            "Revise as opções. "
                            "Manter tudo funciona, mas é o caminho mais lento (8 meses). "
                            "Cortar a alimentação compromete o essencial — não é seguro. "
                            "Pegar empréstimo para repor reserva cria dívida com juros: "
                            "você estaria pagando mais para ter de volta o que já tinha. "
                            "O melhor equilíbrio é suspender temporariamente os gastos "
                            "não essenciais e aumentar o aporte até recompor a reserva."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Quando usar — e quando não usar — a reserva",
                    "order": 1,
                    "body": (
                        "A reserva de emergência é para **imprevistos urgentes e "
                        "não planejados** — situações em que a renda para ou surge "
                        "uma despesa essencial impossível de evitar. Exemplos:\n\n"
                        "✔ Perda de emprego ou queda brusca de renda\n"
                        "✔ Conserto urgente de algo essencial (carro usado para trabalho, "
                        "geladeira, computador de trabalho)\n"
                        "✔ Despesa de saúde inesperada\n\n"
                        "A reserva **não é para:**\n\n"
                        "✘ Promoções e oportunidades de compra\n"
                        "✘ Presentes, viagens ou lazer planejáveis\n"
                        "✘ Entrada de bens que você decidiu comprar\n"
                        "✘ Complementar o salário de um mês de gastos excessivos\n\n"
                        "Uma pergunta útil antes de mexer na reserva:\n"
                        "*\"Isso é urgente, inesperado e essencial?\"* "
                        "Se a resposta for sim para os três, a reserva pode ser usada. "
                        "Se não, procure outra solução."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como recompor a reserva após o uso",
                    "order": 2,
                    "body": (
                        "Usar a reserva não é um fracasso — é ela cumprindo o papel para "
                        "o qual foi criada. Mas depois de usar, **recompor é a prioridade**.\n\n"
                        "**Passo a passo para recompor:**\n\n"
                        "1. Calcule o valor usado: reserva anterior − reserva atual.\n"
                        "2. Reveja os gastos não essenciais do mês: quais podem ser "
                        "suspensos temporariamente para acelerar a recomposição?\n"
                        "3. Defina um aporte mensal de recomposição: "
                        "valor usado ÷ meses desejados = aporte necessário.\n"
                        "4. Mantenha esse ritmo até a reserva estar completa.\n\n"
                        "Enquanto a reserva não estiver recomposta, evite assumir "
                        "novos gastos não essenciais. Uma reserva incompleta "
                        "aumenta a vulnerabilidade diante do próximo imprevisto."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Quando e como revisar o tamanho da sua reserva",
                    "order": 3,
                    "body": (
                        "O valor-alvo da reserva não é fixo para sempre. "
                        "Revise sempre que algo mudar:\n\n"
                        "- **Mudança de emprego ou regime de trabalho:** "
                        "de CLT para autônomo, o número de meses recomendado sobe.\n"
                        "- **Novo dependente:** um filho ou outro familiar que passa "
                        "a depender da sua renda aumenta as despesas essenciais.\n"
                        "- **Aumento ou queda de renda:** se as despesas essenciais "
                        "mudaram, o valor-alvo muda junto.\n"
                        "- **Mudança de moradia:** aluguel ou prestação nova "
                        "altera o cálculo base.\n\n"
                        "Faça essa revisão pelo menos uma vez por ano, "
                        "ou toda vez que perceber uma mudança relevante "
                        "na sua vida financeira."
                    ),
                },
            ],
        },
    ],
}
