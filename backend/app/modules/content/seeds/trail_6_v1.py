"""Trilha 6 — Guardar sem perder o controle.

phase_number: 6 (existente — não insere nova fase)
Fonte editorial: docs/trilhas/trilha-06.md

Missão 1 é expansão (upsert sobre phase_3_v1.py missão 2).
Missões 2 e 3 são novas.
O seeder usa upsert por chave natural — não duplica conteúdo existente.
"""

TRAIL_6_V1 = {
    "phase_number": 6,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 6.1 — Separar primeiro (expansão sobre phase_3_v1 missão 2)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Separar primeiro",
            "description": (
                "Aplique o método de pagar a si mesmo primeiro: separe a reserva "
                "no momento do recebimento, antes de qualquer gasto."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.1.1",
                    "name": "Aplicar o método de separar primeiro no recebimento",
                    "description": (
                        "Transfere o valor destinado à reserva ou meta no mesmo dia "
                        "em que o salário cai na conta, antes de qualquer gasto."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.1.2",
                    "name": "Calcular quanto separar por categoria no recebimento",
                    "description": (
                        "Determina o valor a separar para reserva e metas como "
                        "percentual ou valor fixo da renda líquida."
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
                            "Por que separar o dinheiro da reserva no dia do recebimento "
                            "funciona melhor do que guardar o que sobra no fim do mês?"
                        ),
                        "competency_codes": ["6.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Porque o banco cobra menos tarifas no início do mês.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Porque o dinheiro que sai primeiro não está disponível "
                                    "para gasto — elimina a tentação e garante que a reserva acontece."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Porque rende mais investindo por mais dias.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O princípio é simples: você não gasta o que não vê. "
                            "Separar no recebimento trata a reserva como despesa obrigatória — "
                            "não como sobra opcional. Guardar o que sobra raramente funciona "
                            "porque as despesas tendem a consumir tudo disponível."
                        ),
                        "feedback_incorrect": (
                            "O motivo não é tarifa nem rendimento — é psicologia. "
                            "Dinheiro disponível na conta convida ao gasto. "
                            "Dinheiro separado logo no recebimento 'desaparece' antes "
                            "que você tenha a oportunidade de gastá-lo."
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
                            "Ana recebe R$ 1.800 e quer separar 10% para a reserva. "
                            "Quanto ela transfere antes de qualquer gasto? (Situação fictícia.)"
                        ),
                        "competency_codes": ["6.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 90."},
                            {"value": "b", "label": "R$ 180."},
                            {"value": "c", "label": "R$ 280."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 10% de R$ 1.800 = R$ 180. "
                            "Esse valor vai para a conta da reserva no dia do recebimento, "
                            "antes de pagar qualquer conta ou fazer qualquer compra."
                        ),
                        "feedback_incorrect": (
                            "10% de R$ 1.800 = R$ 180. "
                            "Lembre: o percentual é calculado sobre a renda líquida "
                            "(o que cai na conta), não sobre o bruto."
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
                            "Qual é a principal vantagem de ter uma conta separada "
                            "para a reserva, diferente da conta corrente?"
                        ),
                        "competency_codes": ["6.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "A conta separada sempre rende mais juros.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "O dinheiro fica fora do alcance cotidiano — "
                                    "você não o vê no saldo da conta corrente."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Facilita o empréstimo bancário.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Conta separada = barreira psicológica. "
                            "O dinheiro não aparece no saldo da conta corrente, "
                            "reduzindo a tentação de usá-lo em gastos do dia a dia."
                        ),
                        "feedback_incorrect": (
                            "A principal vantagem não é o rendimento — é a separação mental. "
                            "Dinheiro fora da conta corrente fica protegido de gastos impulsivos."
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
                            "Descreva como você aplicaria o método de separar primeiro "
                            "com a sua renda atual ou fictícia. "
                            "Quanto separaria, para onde o dinheiro iria e em qual dia?"
                        ),
                        "competency_codes": ["6.1.1", "6.1.2"],
                        "feedback_static": (
                            "Uma boa resposta descreve: o valor ou percentual a separar, "
                            "a conta de destino (reserva, meta), o dia de transferência "
                            "(preferencialmente o dia do recebimento) e a forma "
                            "(transferência manual ou programada)."
                        ),
                        "evaluation_criteria": [
                            "Define o valor ou percentual a separar.",
                            "Menciona o dia de recebimento como momento ideal.",
                            "Descreve a conta de destino.",
                        ],
                        "max_length": 500,
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Se Ana separa R$ 200/mês para a reserva e R$ 100/mês "
                            "para uma meta de viagem, qual é o total que ela "
                            "transfere no dia do recebimento? (Situação fictícia.)"
                        ),
                        "competency_codes": ["6.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 100."},
                            {"value": "b", "label": "R$ 200."},
                            {"value": "c", "label": "R$ 300."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! R$ 200 (reserva) + R$ 100 (meta) = R$ 300 totais "
                            "no dia do recebimento. Ambos saem antes de qualquer outro gasto."
                        ),
                        "feedback_incorrect": (
                            "Reserva e meta são separadas simultaneamente: "
                            "R$ 200 + R$ 100 = R$ 300. "
                            "Ambas saem no dia do recebimento, não em momentos diferentes."
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
                            "O que Ana deve fazer no mês em que a renda foi "
                            "menor do que o esperado?"
                        ),
                        "competency_codes": ["6.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Pular o mês — não separar nada.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Separar um valor proporcional ao que recebeu, "
                                    "mesmo que seja menos do que o planejado."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Usar crédito para compensar a diferença da reserva.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Separar menos é melhor do que não separar nada. "
                            "Pular um mês quebra o hábito; usar crédito para alimentar "
                            "a reserva não faz sentido financeiro."
                        ),
                        "feedback_incorrect": (
                            "Pular o mês quebra o hábito. Usar crédito para alimentar "
                            "a reserva é contraditório — você paga juros para guardar. "
                            "O correto é separar proporcionalmente ao que recebeu."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Pagar-se primeiro: a lógica por trás do método",
                    "order": 1,
                    "body": (
                        "O método 'pague-se primeiro' ('pay yourself first') é simples:\n\n"
                        "**Antes de pagar qualquer conta, antes de qualquer compra, "
                        "você transfere uma parte da renda para a sua reserva ou meta.**\n\n"
                        "Por que funciona:\n"
                        "1. A reserva não compete com outros gastos — ela sai primeiro.\n"
                        "2. Você se acostuma a viver com o restante.\n"
                        "3. Elimina a decisão mensal de 'quanto vou guardar' — "
                        "o valor já está definido.\n\n"
                        "Não é sobre disciplina — é sobre design do sistema."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como aplicar: no dia do recebimento, antes de qualquer gasto",
                    "order": 2,
                    "body": (
                        "**Passo a passo:**\n\n"
                        "1. Defina o valor a separar (ex.: 10% da renda ou R$ 200 fixos).\n"
                        "2. No dia em que o salário cai na conta:\n"
                        "   - Abra o aplicativo do banco.\n"
                        "   - Transfira o valor para a conta da reserva.\n"
                        "   - Só então pague as contas e faça compras.\n\n"
                        "**Dica:** configure a transferência como automática "
                        "para o dia seguinte ao recebimento — assim acontece "
                        "mesmo que você esqueça."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Ana recebe na quinta e separa R$ 200 antes de pagar qualquer conta",
                    "order": 3,
                    "body": (
                        "**Ana**, renda líquida R$ 1.800/mês, recebe toda quinta-feira. "
                        "*(Situação fictícia.)*\n\n"
                        "**Rotina dela:**\n\n"
                        "1. Quinta de manhã: salário cai.\n"
                        "2. 10 minutos depois: transfere R$ 180 (10%) para a conta da reserva.\n"
                        "3. Paga o aluguel, alimentação e demais contas com os R$ 1.620 restantes.\n\n"
                        "**Resultado em 12 meses:** R$ 2.160 de reserva. "
                        "Sem esforço extra, sem revisão mensal da decisão."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Conta separada para reserva: por que funciona melhor",
                    "order": 4,
                    "body": (
                        "Manter a reserva na mesma conta corrente é o principal erro.\n\n"
                        "**Problemas:**\n"
                        "- O saldo parece maior — tentação de gastar.\n"
                        "- É difícil saber o que é reserva e o que é para gastos.\n\n"
                        "**Solução:** conta separada, diferente da corrente. Pode ser:\n"
                        "- Conta de rendimento diário no mesmo banco.\n"
                        "- Conta em outro banco ou fintech.\n"
                        "- Carteira de investimentos com liquidez diária (CDB, fundo DI).\n\n"
                        "O objetivo não é o rendimento — é a separação visual e psicológica."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Quanto separar: percentuais de referência",
                    "order": 5,
                    "body": (
                        "Não existe um percentual único correto. "
                        "Use como referência:\n\n"
                        "| Situação | Percentual de referência |\n"
                        "|---|---|\n"
                        "| Sem reserva ainda, início da jornada | 5–10% da renda |\n"
                        "| Com dívidas | Quitá-las primeiro, depois guardar |\n"
                        "| Reserva em construção (3–6 meses de despesas) | 10–20% |\n"
                        "| Reserva formada, guardando para metas | 10–30% |\n\n"
                        "**O mais importante:** comece com qualquer valor, mesmo R$ 50. "
                        "O hábito importa mais do que o percentual no início."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O mês em que Ana quase gastou a reserva sem perceber",
                    "order": 6,
                    "body": (
                        "**Ana** mantinha a reserva na mesma conta corrente. "
                        "Em novembro, ela viu o saldo alto e pensou que tinha sobrado dinheiro. "
                        "Comprou roupas por R$ 320 — que eram exatamente a reserva do mês. "
                        "*(Situação fictícia.)*\n\n"
                        "**O que ela fez:** em dezembro, abriu uma conta separada "
                        "no mesmo banco e passou a transferir a reserva imediatamente "
                        "ao receber o salário.\n\n"
                        "**Resultado:** o saldo da conta corrente agora reflete apenas "
                        "o dinheiro disponível para o mês — sem confusão com a reserva."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 6.2 — Separar o dinheiro no recebimento (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Separar o dinheiro no recebimento",
            "description": (
                "Aplique a estratégia de pagar a si mesmo primeiro, configure "
                "transferências programadas e organize o orçamento por categorias "
                "logo que a renda chegar."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.2.1",
                    "name": "Aplicar a estratégia de separar o dinheiro no momento do recebimento",
                    "description": (
                        "Entende e aplica o princípio de destinar o valor da poupança "
                        "imediatamente ao receber a renda, antes de qualquer gasto."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.2.2",
                    "name": "Configurar transferências programadas para automatizar a separação",
                    "description": (
                        "Descreve como usar transferências automáticas para separar "
                        "a poupança no dia do recebimento, reduzindo a dependência de "
                        "decisões manuais mensais."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.2.3",
                    "name": "Organizar o orçamento por categorias após a separação da poupança",
                    "description": (
                        "Distribui o valor restante entre categorias de despesas fixas, "
                        "variáveis e lazer depois de separar o valor da meta de poupança."
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
                            "Qual é a principal diferença entre a estratégia "
                            "\"guardar o que sobra\" e a estratégia \"pagar-se primeiro\"?"
                        ),
                        "competency_codes": ["6.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Quem guarda o que sobra separa a poupança no final do "
                                    "mês; quem se paga primeiro separa logo ao receber, "
                                    "antes de gastar."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não há diferença prática — o valor guardado no final "
                                    "do mês costuma ser o mesmo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pagar-se primeiro significa gastar com lazer antes de "
                                    "pagar as contas."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Guardar o que sobra é mais eficiente porque evita "
                                    "mexer no dinheiro duas vezes."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A diferença está no momento: quem tenta guardar o que "
                            "sobra raramente consegue, porque as despesas e os imprevistos "
                            "consomem tudo antes. Pagar-se primeiro garante que a poupança "
                            "acontece antes de qualquer gasto."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. A estratégia 'pagar-se primeiro' separa a "
                            "poupança imediatamente ao receber a renda, antes de gastar com "
                            "qualquer outra coisa. Guardar o que sobra tende a resultar em "
                            "nada guardado, porque os gastos preenchem o espaço disponível."
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
                            "Caio recebe todo dia 5 e quer guardar R$ 250 por mês. "
                            "Como ele pode usar uma transferência programada para aplicar "
                            "o método pagar-se primeiro?"
                        ),
                        "competency_codes": ["6.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Programar uma transferência de R$ 250 para o dia 6, "
                                    "logo após o recebimento, para uma conta ou reserva separada."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Programar a transferência para o dia 30, para ver "
                                    "primeiro quanto sobrou durante o mês."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Fazer a transferência manualmente sempre que lembrar, "
                                    "para manter flexibilidade."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não usar transferência programada — guardar em espécie "
                                    "em casa é mais seguro."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! Programar a transferência para o dia seguinte ao recebimento "
                            "automatiza a separação e elimina a tentação de gastar esse valor. "
                            "A poupança acontece antes de qualquer outro gasto do mês."
                        ),
                        "feedback_incorrect": (
                            "O objetivo da transferência programada é agir logo ao receber, "
                            "não ao final do mês. Esperando o dia 30, os gastos do mês "
                            "costumam consumir o valor que seria guardado. "
                            "A chave é automatizar no início, não no final."
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
                            "Ana trabalha como freelancer e recebe valores diferentes a "
                            "cada mês. Em meses de renda mais baixa, o valor programado "
                            "para guardar pode comprometer os essenciais. "
                            "Qual ajuste é mais indicado?"
                        ),
                        "competency_codes": ["6.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Cancelar a transferência programada nos meses de renda "
                                    "baixa e não guardar nada."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Manter sempre o mesmo valor, independentemente da renda "
                                    "do mês."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Definir um valor mínimo fixo para meses ruins e aumentar "
                                    "a separação nos meses de renda mais alta."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Guardar tudo em meses bons e não guardar nada em meses ruins."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Boa estratégia! Um valor mínimo garantido nos meses de renda baixa "
                            "mantém o hábito ativo. Nos meses de renda alta, guardar mais "
                            "compensa os períodos menores. Consistência importa mais do que "
                            "valor alto em alguns meses."
                        ),
                        "feedback_incorrect": (
                            "Não guardar nada nos meses ruins quebra o hábito e pode "
                            "comprometer a meta. O ideal é definir um valor mínimo sustentável "
                            "para os meses de menor renda e ampliar nos meses de maior renda — "
                            "mantendo o método ativo o ano todo."
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
                            "Após separar a poupança, qual é a ordem correta para "
                            "distribuir o valor restante?"
                        ),
                        "competency_codes": ["6.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Lazer primeiro, depois despesas fixas, depois variáveis."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Despesas fixas essenciais → despesas variáveis essenciais "
                                    "→ lazer com o que sobrar."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não importa a ordem — qualquer sequência chega ao "
                                    "mesmo resultado."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Dividir igualmente entre todas as categorias."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Depois de separar a poupança, o essencial vem primeiro: "
                            "aluguel, contas fixas, alimentação, transporte. "
                            "Com o restante garantido para o básico, o lazer fica no que sobrar, "
                            "sem comprometer o orçamento."
                        ),
                        "feedback_incorrect": (
                            "A ordem faz diferença. Depois de separar a poupança, "
                            "as despesas essenciais (fixas e variáveis) devem ser cobertas antes "
                            "do lazer. Reservar o lazer para o que sobrar garante que o "
                            "essencial nunca fique descoberto."
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
                            "Imagine que você recebe R$ 1.800 por mês e quer guardar R$ 200. "
                            "Descreva como você organizaria o recebimento usando a estratégia "
                            "pagar-se primeiro: quando separaria a poupança, como dividiria o "
                            "restante e o que faria para não depender de decisões manuais "
                            "todos os meses."
                        ),
                        "competency_codes": ["6.2.1", "6.2.2", "6.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado.\n\n"
                            "Referência esperada:\n"
                            "- Separar R$ 200 assim que o salário cair (ou no dia seguinte)\n"
                            "- Configurar uma transferência programada para automatizar\n"
                            "- Distribuir o restante (R$ 1.600) entre essenciais e lazer\n"
                            "- Não depender de lembrar manualmente — o sistema trabalha por você"
                        ),
                        "evaluation_criteria": [
                            "Indica que a poupança é separada antes dos demais gastos.",
                            "Menciona transferência programada ou automação da separação.",
                            "Descreve como distribuir o valor restante por categorias.",
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
                            "Caio recebe R$ 2.200 líquidos no dia 5. Ele quer aplicar "
                            "o método pagar-se primeiro com meta de guardar R$ 300. "
                            "Como ele deve distribuir o restante (R$ 1.900)?\n\n"
                            "Despesas do mês de Caio:\n"
                            "- Aluguel: R$ 700\n"
                            "- Conta de energia + água: R$ 130\n"
                            "- Alimentação (mercado): R$ 400\n"
                            "- Transporte: R$ 150\n"
                            "- Celular: R$ 60\n"
                            "- Streaming e lazer: R$ ?\n\n"
                            "Qual distribuição aplica corretamente o método?"
                        ),
                        "competency_codes": ["6.2.1", "6.2.3"],
                        "scenario": (
                            "Caio, 24 anos, salário fixo de R$ 2.200 líquidos. "
                            "Meta de poupança: R$ 300 por mês. Valores fictícios, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Separar R$ 300 de poupança no dia 5. "
                                    "Com os R$ 1.900 restantes: aluguel R$ 700, energia+água R$ 130, "
                                    "alimentação R$ 400, transporte R$ 150, celular R$ 60, "
                                    "lazer R$ 460. Total: R$ 2.200."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar todas as contas primeiro (R$ 1.440) e depois "
                                    "guardar R$ 300 e usar R$ 460 para lazer. "
                                    "Total: R$ 2.200."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Gastar R$ 700 em lazer antes de separar a poupança, "
                                    "depois pagar as contas e ver o que sobra para guardar."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não separar nada de poupança este mês — pagar todas "
                                    "as contas e usar o restante (R$ 760) para lazer."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Perfeito! Caio aplicou o método corretamente: separou R$ 300 "
                            "de poupança logo ao receber, depois distribuiu os R$ 1.900 "
                            "restantes entre essenciais (R$ 1.440) e lazer (R$ 460). "
                            "A poupança foi garantida antes de qualquer gasto."
                        ),
                        "feedback_incorrect": (
                            "No método pagar-se primeiro, a poupança é separada imediatamente "
                            "ao receber — não ao final. Depois de reservar R$ 300, Caio "
                            "distribui os R$ 1.900 entre essenciais e lazer: "
                            "aluguel R$ 700 + energia+água R$ 130 + alimentação R$ 400 "
                            "+ transporte R$ 150 + celular R$ 60 = R$ 1.440 essenciais, "
                            "sobrando R$ 460 para lazer."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Pagar-se primeiro: a lógica da separação imediata",
                    "order": 1,
                    "body": (
                        "A maioria das pessoas tenta guardar o que sobra no fim do mês. "
                        "O problema é que quase nunca sobra nada — os gastos expandem "
                        "para preencher o espaço disponível.\n\n"
                        "A estratégia **pagar-se primeiro** inverte essa lógica:\n\n"
                        "1. Ao receber a renda, separe imediatamente o valor da poupança\n"
                        "2. Só então distribua o restante entre despesas e lazer\n\n"
                        "Essa sequência funciona porque retira o valor da poupança do "
                        "'dinheiro disponível para gastar' antes que qualquer decisão "
                        "de gasto aconteça. O que não está na conta corrente, não é gasto.\n\n"
                        "**Por que automação potencializa o método:**\n"
                        "Uma transferência programada para o dia seguinte ao recebimento "
                        "elimina a necessidade de decidir todo mês — e elimina também a "
                        "tentação de 'usar só desta vez'."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Caio separa logo ao receber",
                    "order": 2,
                    "body": (
                        "Caio recebe R$ 2.200 todo dia 5. Sua meta é guardar R$ 300 por mês.\n\n"
                        "**Antes (guardar o que sobra):**\n"
                        "Caio pagava as contas, comprava o que precisava e, no fim do mês, "
                        "sempre havia algo novo para gastar. Resultado: R$ 0 guardados.\n\n"
                        "**Depois (pagar-se primeiro):**\n"
                        "No dia 6, uma transferência automática move R$ 300 para uma conta "
                        "separada. Caio distribui os R$ 1.900 restantes entre as contas e "
                        "o lazer. Como o dinheiro da poupança já saiu, ele nem o conta como "
                        "disponível.\n\n"
                        "Resultado após 6 meses: R$ 1.800 guardados — sem esforço extra, "
                        "só mudando o momento da separação.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como configurar uma transferência programada",
                    "order": 3,
                    "body": (
                        "A maioria dos aplicativos bancários permite criar transferências "
                        "automáticas recorrentes. O fluxo geral é:\n\n"
                        "1. Acesse a área de transferências ou Pix no seu aplicativo\n"
                        "2. Escolha 'agendar' ou 'programar'\n"
                        "3. Defina o valor, a conta de destino e a data (preferencialmente "
                        "1 dia após o recebimento)\n"
                        "4. Selecione a recorrência (mensal)\n\n"
                        "Ao separar para uma conta diferente da sua conta corrente principal, "
                        "o valor fica visualmente separado e você evita usá-lo por impulso.\n\n"
                        "*(Verifique as funcionalidades disponíveis no aplicativo do seu banco.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 6.3 — Adaptando o método para diferentes rendas (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Adaptando o método para diferentes rendas",
            "description": (
                "Aprenda a manter o hábito de poupar com renda fixa, variável ou "
                "irregular — usando percentuais e um fundo de nivelamento."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.3.1",
                    "name": "Adaptar a estratégia de poupança para renda fixa",
                    "description": (
                        "Aplica o método pagar-se primeiro com valor fixo mensal para "
                        "quem tem renda previsível (CLT, servidor público etc.)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.3.2",
                    "name": "Criar um método de separação proporcional para renda variável",
                    "description": (
                        "Define um percentual fixo de poupança a ser aplicado sobre "
                        "cada recebimento, independentemente do valor, para quem tem "
                        "renda variável (comissão, freelance)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.3.3",
                    "name": "Desenvolver um plano de poupança sustentável para renda irregular",
                    "description": (
                        "Estrutura um fundo de nivelamento para uniformizar a renda "
                        "mensal e aplica poupança sobre o excedente em períodos de "
                        "maior recebimento."
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
                            "Marcos tem salário CLT fixo de R$ 2.600 líquidos e quer "
                            "guardar 10% por mês. Qual é o valor mensal e qual é a "
                            "vantagem do seu tipo de renda para aplicar esse método?"
                        ),
                        "competency_codes": ["6.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "R$ 260 por mês. A previsibilidade da renda fixa "
                                    "permite programar a transferência automaticamente "
                                    "e manter o mesmo valor todos os meses."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "R$ 260 por mês. Mas renda fixa é desvantagem — "
                                    "não dá para guardar mais em bons meses."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "R$ 520 por mês (20%). Quem tem renda fixa deve "
                                    "sempre guardar o dobro do percentual."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "R$ 130 por mês (5%). Com renda fixa, o percentual "
                                    "recomendado é sempre 5%."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 10% de R$ 2.600 = R$ 260. A renda fixa facilita "
                            "porque o valor é sempre o mesmo — uma transferência "
                            "programada resolve sem necessidade de recalcular todo mês."
                        ),
                        "feedback_incorrect": (
                            "10% de R$ 2.600 = R$ 260. A vantagem da renda fixa é a "
                            "previsibilidade: o valor guardado é igual todos os meses, "
                            "o que facilita a automação. Não existe percentual 'correto' "
                            "fixo para todos — o importante é ser consistente com "
                            "o percentual que cabe no orçamento."
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
                            "Juliana trabalha com vendas por comissão. Nos últimos "
                            "3 meses recebeu: R$ 1.600, R$ 3.100 e R$ 2.200. "
                            "Ela decidiu guardar 12% de cada recebimento. "
                            "Quanto ela guardou no total nesses 3 meses?"
                        ),
                        "competency_codes": ["6.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 264,00."},
                            {"value": "b", "label": "R$ 372,00 + R$ 264,00 = R$ 636,00."},
                            {
                                "value": "c",
                                "label": (
                                    "R$ 192,00 + R$ 372,00 + R$ 264,00 = R$ 828,00."
                                ),
                            },
                            {"value": "d", "label": "R$ 744,00."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! 12% de R$ 1.600 = R$ 192; 12% de R$ 3.100 = R$ 372; "
                            "12% de R$ 2.200 = R$ 264. Total: R$ 828. "
                            "O percentual fixo garante que Juliana guarda mais nos meses "
                            "de renda alta e menos nos meses de renda baixa — "
                            "sem jamais comprometer o orçamento."
                        ),
                        "feedback_incorrect": (
                            "Aplique o percentual sobre cada recebimento separadamente:\n"
                            "- R$ 1.600 × 12% = R$ 192\n"
                            "- R$ 3.100 × 12% = R$ 372\n"
                            "- R$ 2.200 × 12% = R$ 264\n"
                            "Total: R$ 828. O método proporcional se ajusta automaticamente "
                            "à variação da renda."
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
                            "Rafael tem renda irregular: vende artesanato em feiras e "
                            "faz bicos esporádicos. Seus recebimentos são imprevisíveis "
                            "e às vezes chegam todos de uma vez. "
                            "Qual estratégia é mais adequada para ele manter um plano "
                            "de poupança sustentável?"
                        ),
                        "competency_codes": ["6.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Guardar tudo que receber além do mínimo para cobrir "
                                    "os essenciais e não poupar nos meses sem renda."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Criar um fundo de nivelamento: acumular os recebimentos "
                                    "em conta separada e retirar um valor fixo mensal para "
                                    "cobrir os essenciais, poupando o que exceder esse valor "
                                    "nos meses de maior entrada."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não poupar enquanto a renda for irregular — esperar "
                                    "ter um emprego fixo para começar."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Guardar um valor fixo alto todo mês, independentemente "
                                    "de quanto recebeu."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Boa estratégia! O fundo de nivelamento funciona como um "
                            "reservatório: nos meses de maior entrada, o excedente fica "
                            "acumulado. Nos meses fracos, Rafael retira o valor necessário "
                            "para cobrir o mínimo. Isso suaviza a irregularidade e ainda "
                            "permite separar uma parte para a poupança."
                        ),
                        "feedback_incorrect": (
                            "Renda irregular não impede a poupança — exige uma adaptação. "
                            "O fundo de nivelamento é uma conta-tampão: acumule recebimentos "
                            "irregulares e use-a para 'pagar' um salário fixo a si mesmo "
                            "todo mês. O excedente vai para a poupança. "
                            "Esperar ter renda fixa para começar significa adiar "
                            "indefinidamente um hábito que pode ser desenvolvido agora."
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
                            "Descreva como é a sua renda hoje (fixa, variável ou irregular) "
                            "e como você adaptaria a estratégia pagar-se primeiro para o "
                            "seu perfil. Se a renda varia, qual percentual você usaria e "
                            "como decidiria quanto guardar em cada mês?"
                        ),
                        "competency_codes": ["6.3.1", "6.3.2", "6.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado.\n\n"
                            "Referências esperadas:\n"
                            "- Renda fixa: definir valor ou percentual fixo e automatizar\n"
                            "- Renda variável: escolher um percentual (ex.: 10–15%) aplicado "
                            "a cada recebimento\n"
                            "- Renda irregular: criar um fundo de nivelamento e poupar "
                            "o excedente nos meses de maior entrada"
                        ),
                        "evaluation_criteria": [
                            "Identifica corretamente o tipo de renda (fixa, variável ou irregular).",
                            (
                                "Propõe uma estratégia adequada ao tipo de renda descrito, "
                                "com percentual ou valor definido."
                            ),
                            (
                                "Menciona como lidar com a variação de renda ou como "
                                "automatizar a separação."
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
                            "Bruno é freelancer e recebeu valores diferentes nos últimos "
                            "3 meses:\n\n"
                            "- Mês 1: R$ 3.500\n"
                            "- Mês 2: R$ 1.800\n"
                            "- Mês 3: R$ 4.200\n\n"
                            "Suas despesas essenciais mínimas somam R$ 1.600 por mês. "
                            "Ele decidiu guardar 10% de cada recebimento. "
                            "Qual resultado o método proporcional produz ao longo dos 3 meses?"
                        ),
                        "competency_codes": ["6.3.2", "6.3.3"],
                        "scenario": (
                            "Bruno, freelancer, 27 anos. Renda variável mensal. "
                            "Despesas essenciais mínimas: R$ 1.600/mês. "
                            "Estratégia: 10% de poupança sobre cada recebimento. "
                            "Valores fictícios, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Mês 1: guarda R$ 350 (10% de R$ 3.500). "
                                    "Mês 2: guarda R$ 180 (10% de R$ 1.800) — o essencial "
                                    "fica coberto com os R$ 1.620 restantes. "
                                    "Mês 3: guarda R$ 420 (10% de R$ 4.200). "
                                    "Total guardado: R$ 950."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Guardar R$ 350 somente no mês 1 e nada nos demais "
                                    "meses, porque no mês 2 a renda foi baixa."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Guardar R$ 350 nos 3 meses (valor fixo do mês 1), "
                                    "totalizando R$ 1.050."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não guardar nada — com renda variável é impossível "
                                    "manter um método de poupança."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Correto! O método proporcional funciona assim:\n"
                            "- Mês 1: R$ 3.500 × 10% = R$ 350 poupados; R$ 3.150 para gastos\n"
                            "- Mês 2: R$ 1.800 × 10% = R$ 180 poupados; R$ 1.620 para gastos "
                            "(acima do mínimo de R$ 1.600)\n"
                            "- Mês 3: R$ 4.200 × 10% = R$ 420 poupados; R$ 3.780 para gastos\n"
                            "Total poupado: R$ 950. O percentual fixo garante que Bruno sempre "
                            "guarda algo, mas nunca compromete o essencial."
                        ),
                        "feedback_incorrect": (
                            "O método proporcional aplica o percentual sobre cada recebimento:\n"
                            "- Mês 1: 10% × R$ 3.500 = R$ 350\n"
                            "- Mês 2: 10% × R$ 1.800 = R$ 180 (ainda cobre o essencial "
                            "de R$ 1.600 com os R$ 1.620 restantes)\n"
                            "- Mês 3: 10% × R$ 4.200 = R$ 420\n"
                            "Total: R$ 950 guardados em 3 meses. "
                            "Renda variável não impede a poupança — o percentual "
                            "ajusta o valor ao que chegou."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Três perfis de renda, três adaptações",
                    "order": 1,
                    "body": (
                        "O método pagar-se primeiro funciona para qualquer tipo de renda — "
                        "o que muda é a forma de aplicá-lo:\n\n"
                        "**Renda fixa (CLT, servidor público):**\n"
                        "O valor guardado é o mesmo todo mês. Use um valor absoluto "
                        "(ex.: R$ 300) ou um percentual fixo (ex.: 10%). "
                        "Configure uma transferência automática e esqueça — ela trabalha "
                        "por você.\n\n"
                        "**Renda variável (comissão, freelance):**\n"
                        "Substitua o valor fixo por um percentual. A cada recebimento, "
                        "separe imediatamente o percentual definido (ex.: 12%). "
                        "Meses de renda alta geram mais poupança; meses fracos geram menos — "
                        "mas sempre algo é guardado.\n\n"
                        "**Renda irregular (bicos, trabalhos sazonais, múltiplas fontes):**\n"
                        "Crie um **fundo de nivelamento**: uma conta separada onde todos "
                        "os recebimentos entram. Defina um 'salário' mensal para si mesmo "
                        "baseado no mínimo necessário para os essenciais. "
                        "O excedente fica no fundo — parte como reserva, parte como poupança."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois trabalhadores, dois métodos",
                    "order": 2,
                    "body": (
                        "**Fernanda — CLT, renda fixa de R$ 2.400:**\n"
                        "Escolheu guardar R$ 240 por mês (10%). "
                        "Configurou uma transferência no dia 6 (recebe no dia 5). "
                        "Ao longo do ano, acumula R$ 2.880 sem nenhuma decisão mensal.\n\n"
                        "**Bruno — freelancer, renda variável:**\n"
                        "Escolheu o percentual de 10% sobre cada recebimento.\n\n"
                        "| Mês | Recebimento | Poupado (10%) | Disponível |\n"
                        "|-----|-------------|--------------|------------|\n"
                        "| Jan | R$ 3.500 | R$ 350 | R$ 3.150 |\n"
                        "| Fev | R$ 1.800 | R$ 180 | R$ 1.620 |\n"
                        "| Mar | R$ 4.200 | R$ 420 | R$ 3.780 |\n\n"
                        "Total poupado em 3 meses: R$ 950. "
                        "Mesmo no mês fraco (R$ 1.800), Bruno cobriu os essenciais "
                        "(R$ 1.600) com os R$ 1.620 disponíveis.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Fundo de nivelamento: como montar o seu",
                    "order": 3,
                    "body": (
                        "O fundo de nivelamento é especialmente útil para quem tem "
                        "renda irregular. A ideia é simples:\n\n"
                        "1. **Abra uma conta separada** só para este fim\n"
                        "2. **Deposite todos os recebimentos irregulares** nessa conta\n"
                        "3. **Defina um 'salário mensal'** para si mesmo — "
                        "o valor mínimo para cobrir os essenciais\n"
                        "4. **Transfira esse valor fixo** para a conta principal no "
                        "início de cada mês\n"
                        "5. **O excedente** que sobrar no fundo, acima do necessário "
                        "para os próximos meses, pode ser direcionado para a poupança\n\n"
                        "Esse mecanismo suaviza a variação da renda e permite planejar "
                        "com previsibilidade, mesmo sem um emprego fixo."
                    ),
                },
            ],
        },
    ],
}
