"""Conteúdo versionado da Fase 1.

Este módulo é a fonte da migration 0002 e dos testes de contrato. Alterações
editoriais posteriores devem gerar uma nova versão/migração, preservando a
reprodutibilidade do histórico.
"""

PHASE_1_V1 = {
    "phase_number": 1,
    "missions": [
        {
            "number": 1,
            "name": "De onde vem o dinheiro?",
            "description": (
                "Diferencie salário bruto de líquido e reconheça os principais "
                "descontos de um contracheque."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "1.1.1",
                    "name": "Distinguir salário bruto de salário líquido",
                    "description": (
                        "Reconhece que o bruto é o valor combinado antes dos "
                        "descontos e o líquido é o valor efetivamente recebido."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.1.2",
                    "name": "Identificar os descontos do contracheque",
                    "description": (
                        "Diferencia descontos que reduzem o salário (INSS, IRRF, "
                        "vale-transporte) de valores que não são descontados (FGTS)."
                    ),
                    "is_essential": False,
                },
                {
                    "code": "1.1.3",
                    "name": "Calcular o salário líquido",
                    "description": (
                        "Calcula o líquido a partir do bruto e dos descontos "
                        "informados em um contracheque."
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
                            "Uma proposta de emprego informa salário de R$ 2.000 "
                            "bruto. O que isso significa?"
                        ),
                        "competency_codes": ["1.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Que você receberá exatamente R$ 2.000 na conta.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Que R$ 2.000 é o valor antes dos descontos; "
                                    "o que cai na conta normalmente será menor."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Que R$ 2.000 é o valor depois de todos os descontos."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Que R$ 2.000 é só o valor dos benefícios, sem "
                                    "contar o salário."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! O salário bruto é o valor combinado antes dos "
                            "descontos. O que você recebe de fato é o líquido, que "
                            "normalmente é menor."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O salário bruto é o valor acordado "
                            "antes de qualquer desconto. O líquido, que é o que cai "
                            "na conta, normalmente é menor."
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
                            "Em um contracheque aparecem INSS, vale-transporte "
                            "(quando o trabalhador opta por usar) e FGTS. Qual "
                            "desses NÃO é descontado do salário do trabalhador?"
                        ),
                        "competency_codes": ["1.1.2"],
                        "options": [
                            {"value": "a", "label": "INSS."},
                            {"value": "b", "label": "Vale-transporte."},
                            {"value": "c", "label": "FGTS."},
                            {
                                "value": "d",
                                "label": "Todos são descontados do salário.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Isso mesmo! O FGTS é depositado pelo empregador em uma "
                            "conta em seu nome. Ele aparece no contracheque, mas não "
                            "reduz o seu salário líquido."
                        ),
                        "feedback_incorrect": (
                            "Quase! O INSS e o vale-transporte são descontados do "
                            "salário. O FGTS é diferente: é o empregador que deposita, "
                            "e o valor não sai do seu salário."
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
                            "Um contracheque fictício mostra: salário bruto "
                            "R$ 2.000,00; INSS R$ 155,68; IRRF R$ 0,00; "
                            "vale-transporte R$ 120,00. Qual é o salário líquido?"
                        ),
                        "competency_codes": ["1.1.3"],
                        "options": [
                            {"value": "a", "label": "R$ 1.724,32."},
                            {"value": "b", "label": "R$ 1.844,32."},
                            {"value": "c", "label": "R$ 1.880,00."},
                            {"value": "d", "label": "R$ 2.000,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 2.000,00 − 155,68 − 0,00 − 120,00 = "
                            "R$ 1.724,32. É esse o valor que realmente cai na conta."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. O líquido é o bruto menos todos os "
                            "descontos: 2.000,00 − 155,68 − 0,00 − 120,00 = "
                            "R$ 1.724,32. Conferir se todos os descontos entraram na "
                            "conta ajuda a evitar erros."
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
                            "Explique com as suas palavras, como se fosse para um "
                            "amigo: por que o valor que cai na conta costuma ser "
                            "diferente do valor combinado quando a pessoa é contratada?"
                        ),
                        "competency_codes": ["1.1.1", "1.1.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e "
                            "dar um retorno personalizado quando a integração de IA "
                            "estiver disponível. Enquanto isso, revise a diferença "
                            "entre bruto, descontos e líquido."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona que o salário bruto é o valor combinado "
                                "antes dos descontos."
                            ),
                            (
                                "Cita pelo menos um desconto, como INSS, imposto de "
                                "renda ou vale-transporte."
                            ),
                            (
                                "Explica que o salário líquido é o valor que de fato "
                                "cai na conta."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é salário bruto e líquido",
                    "order": 1,
                    "body": (
                        "Quando uma empresa diz \"o salário é R$ 2.000\", normalmente "
                        "está falando do **salário bruto**: o valor combinado, "
                        "**antes** de qualquer desconto.\n\n"
                        "O **salário líquido** é o que **realmente cai na sua conta**, "
                        "depois dos descontos obrigatórios e de eventuais descontos "
                        "que você autorizou.\n\n"
                        "Fórmula simples:\n\n"
                        "**salário líquido = salário bruto − descontos**\n\n"
                        "Por isso, ao receber uma proposta de emprego, vale perguntar: "
                        "\"esse valor é bruto ou líquido?\". A diferença pode mudar "
                        "bastante o seu planejamento."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Os principais descontos do contracheque",
                    "order": 2,
                    "body": (
                        "Os descontos mais comuns para quem trabalha com carteira "
                        "assinada:\n\n"
                        "- **INSS:** contribuição para a Previdência Social, que garante "
                        "benefícios como aposentadoria, auxílio por doença e "
                        "salário-maternidade. Em 2026, as alíquotas vão de 7,5% a 14% e "
                        "são aplicadas **por faixa**: cada parte do salário paga a sua "
                        "própria alíquota. Não existe uma alíquota única sobre o salário "
                        "inteiro.\n"
                        "- **Imposto de Renda retido na fonte (IRRF):** desde janeiro de "
                        "2026, quem recebe até R$ 5.000 por mês tem o IRRF zerado. Por "
                        "isso, em um primeiro salário, é comum que esse desconto seja "
                        "R$ 0,00.\n"
                        "- **Vale-transporte:** se você optar por usar, a empresa pode "
                        "descontar até 6% do seu salário-base.\n\n"
                        "E um item que **aparece no contracheque, mas não sai do seu "
                        "bolso**:\n\n"
                        "- **FGTS:** o empregador deposita 8% do salário em uma conta "
                        "vinculada ao seu nome. Não reduz o seu salário líquido."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O contracheque da Ana (fictício)",
                    "order": 3,
                    "body": (
                        "A Ana começou a trabalhar com salário bruto de **R$ 2.000,00**. "
                        "Veja como fica o contracheque dela:\n\n"
                        "- Salário bruto: R$ 2.000,00\n"
                        "- INSS: − R$ 155,68\n"
                        "- IRRF: R$ 0,00\n"
                        "- Vale-transporte: − R$ 120,00\n"
                        "- **Salário líquido: R$ 1.724,32**\n"
                        "- FGTS depositado pela empresa (não é desconto): R$ 160,00\n\n"
                        "Como o INSS foi calculado por faixas: os primeiros "
                        "R$ 1.621,00 pagam 7,5% (R$ 121,57) e os R$ 379,00 restantes "
                        "pagam 9% (R$ 34,11).\n\n"
                        "Repare: a Ana combinou R$ 2.000, mas o que ela tem para gastar "
                        "no mês é R$ 1.724,32. É sobre esse valor que ela precisa fazer "
                        "o planejamento.\n\n"
                        "*(Valores fictícios e arredondados, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Confira o seu contracheque todo mês",
                    "order": 4,
                    "body": (
                        "Olhe sempre três linhas: **bruto**, **descontos** e **líquido**. "
                        "Se alguma linha não fizer sentido, pergunte ao RH ou ao "
                        "responsável pela folha de pagamento. Entender o contracheque é "
                        "o primeiro passo para controlar o seu dinheiro."
                    ),
                },
            ],
        },
        {
            "number": 2,
            "name": "O que importa primeiro?",
            "description": (
                "Separe necessidades de desejos e defina prioridades quando o "
                "dinheiro não dá para tudo."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "1.2.1",
                    "name": "Diferenciar necessidades de desejos",
                    "description": (
                        "Classifica gastos considerando o que é essencial para viver "
                        "e cumprir obrigações."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.2.2",
                    "name": "Priorizar gastos com renda limitada",
                    "description": (
                        "Ordena pagamentos dando prioridade ao que evita consequências "
                        "sérias quando a renda não cobre tudo."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.2.3",
                    "name": "Reconhecer que contexto muda a classificação",
                    "description": (
                        "Entende que a mesma despesa pode ser necessidade ou desejo "
                        "dependendo do contexto e da consequência de não tê-la."
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
                        "prompt": "Qual dos itens abaixo é uma necessidade básica?",
                        "competency_codes": ["1.2.1"],
                        "options": [
                            {"value": "a", "label": "Assinatura de streaming."},
                            {"value": "b", "label": "Conta de luz da casa."},
                            {"value": "c", "label": "Tênis de marca novo."},
                            {"value": "d", "label": "Ingresso para um show."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! A conta de luz é uma despesa essencial: sem pagá-la, "
                            "você perde um serviço básico. Os outros itens são desejos "
                            "que podem esperar."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A conta de luz é essencial para morar. "
                            "Streaming, tênis de marca e show são desejos: melhoram a "
                            "vida, mas podem esperar."
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
                            "Marina usa o celular para receber pedidos do trabalho e o "
                            "aparelho quebrou. Pedro tem um celular funcionando e quer "
                            "trocar pelo último lançamento. Qual afirmação está correta?"
                        ),
                        "competency_codes": ["1.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Para os dois, o celular é necessidade.",
                            },
                            {
                                "value": "b",
                                "label": "Para os dois, o celular é desejo.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Para Marina, ter um celular funcionando é "
                                    "necessidade; para Pedro, trocar pelo lançamento é "
                                    "desejo."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "Celular só é necessidade se for caro.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Muito bem! A classificação depende do contexto. Marina "
                            "precisa do aparelho para trabalhar; Pedro já tem um que "
                            "funciona e quer trocar por vontade."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A mesma despesa pode ser necessidade ou "
                            "desejo, dependendo do contexto. Marina precisa de um "
                            "celular para trabalhar. Pedro já tem um funcionando, então "
                            "a troca é desejo."
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
                            "Você tem R$ 900 até o fim do mês. Já está certo que vai "
                            "pagar o aluguel (R$ 500) e o mercado (R$ 300). Um amigo "
                            "chama você para um show, com ingresso de R$ 200. O que é "
                            "mais sensato?"
                        ),
                        "competency_codes": ["1.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Comprar o ingresso primeiro, porque pode esgotar.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar aluguel e mercado primeiro; o show só entra "
                                    "se couber no que sobrar (R$ 100) ou fica para depois."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Dividir o dinheiro igualmente entre os três.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pagar o mercado e o show, e ver depois como fica o "
                                    "aluguel."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Boa decisão! Aluguel e mercado são essenciais e somam "
                            "R$ 800. O show é desejo: só entra se couber no que sobrar, "
                            "ou fica para outro momento."
                        ),
                        "feedback_incorrect": (
                            "Revise suas prioridades. Aluguel e mercado (R$ 800) vêm "
                            "antes do show (R$ 200). Com R$ 900, o show não cabe sem "
                            "comprometer o essencial."
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
                            "Pense em uma compra que você fez ou quer fazer. Ela é uma "
                            "necessidade ou um desejo? O que você faria se o dinheiro só "
                            "desse para esse gasto ou para uma conta essencial?"
                        ),
                        "competency_codes": ["1.2.1", "1.2.2", "1.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado quando a integração de IA estiver "
                            "disponível. Enquanto isso, confira se você justificou a "
                            "classificação pelo contexto e colocou a conta essencial "
                            "antes do desejo."
                        ),
                        "evaluation_criteria": [
                            (
                                "Classifica a compra como necessidade ou desejo com uma "
                                "justificativa baseada em consequência ou contexto."
                            ),
                            (
                                "Reconhece que, entre o gasto e uma conta essencial, a "
                                "conta essencial deve vir primeiro."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Necessidade, desejo e prioridade",
                    "order": 1,
                    "body": (
                        "**Necessidade** é o gasto de que você precisa para viver e "
                        "cumprir suas obrigações: moradia, alimentação, contas básicas "
                        "como água e luz, transporte para ir ao trabalho ou à escola, "
                        "saúde.\n\n"
                        "**Desejo** é o que melhora a vida, mas pode esperar ou ser "
                        "trocado por algo mais barato: streaming, roupa nova só por "
                        "moda, delivery, passeios.\n\n"
                        "**Prioridade** é a ordem em que você paga as coisas quando o "
                        "dinheiro não dá para tudo. Uma regra prática: o que traz "
                        "consequências sérias se não for pago (aluguel, luz, dívidas com "
                        "juros) vem **antes** dos desejos.\n\n"
                        "Desejo não é errado. A ideia é dar um espaço para ele **sem "
                        "comprometer o essencial**."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O mesmo gasto, dois contextos",
                    "order": 2,
                    "body": (
                        "A **Marina** usa o celular para receber os pedidos do trabalho. "
                        "O aparelho quebrou. Para ela, ter um celular funcionando é uma "
                        "**necessidade**, porque sem ele ela não trabalha. Mesmo assim, "
                        "o que ela precisa é de um aparelho que funcione, e não "
                        "necessariamente do modelo mais caro.\n\n"
                        "O **Pedro** tem um celular funcionando, mas quer trocar pelo "
                        "último lançamento. Para ele, a troca é um **desejo**.\n\n"
                        "O mesmo item (um celular) pode ser necessidade para uma pessoa "
                        "e desejo para outra. O que muda é o **contexto** e a "
                        "**consequência** de não ter."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A pergunta que ajuda a decidir",
                    "order": 3,
                    "body": (
                        "Antes de comprar, pergunte: **\"o que acontece se eu não comprar "
                        "isso este mês?\"** Se a resposta for \"nada grave\", "
                        "provavelmente é um desejo. Ele pode esperar, ser trocado por uma "
                        "opção mais barata ou virar um objetivo."
                    ),
                },
            ],
        },
        {
            "number": 3,
            "name": "Meu primeiro plano",
            "description": (
                "Distribua uma renda fictícia entre despesas essenciais, dívidas, "
                "objetivos e reserva, e decida quando as demandas competem entre si."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "1.3.1",
                    "name": "Distribuir a renda entre prioridades",
                    "description": (
                        "Organiza a renda líquida entre essenciais, dívidas, "
                        "objetivos e reserva sem ultrapassar o valor disponível."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.3.2",
                    "name": "Justificar prioridades pelas consequências",
                    "description": (
                        "Explica a ordem escolhida a partir das consequências de cada "
                        "decisão financeira."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "1.3.3",
                    "name": "Reconhecer o valor de separar a reserva no início",
                    "description": (
                        "Entende por que separar parte da renda logo que ela entra "
                        "protege objetivos e imprevistos."
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
                            "Ao receber o salário, qual ordem de prioridades faz mais "
                            "sentido?"
                        ),
                        "competency_codes": ["1.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Despesas essenciais, dívidas com juros, objetivos e "
                                    "reserva, e por último os desejos."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Desejos, depois essenciais, e dívidas só se sobrar."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Reserva e objetivos só se sobrar dinheiro no fim do "
                                    "mês."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Dívidas primeiro, mesmo que falte dinheiro para "
                                    "comer e morar."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! O essencial vem primeiro, depois as dívidas que "
                            "crescem com juros, depois o que constrói o seu futuro, e por "
                            "último os desejos."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O essencial (moradia, comida, transporte) "
                            "vem primeiro, depois as dívidas com juros, depois objetivos "
                            "e reserva. Os desejos ficam para o que sobrar."
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
                            "Por que é uma boa ideia separar uma parte do salário para "
                            "objetivos e reserva logo que o dinheiro cai?"
                        ),
                        "competency_codes": ["1.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Porque assim o dinheiro rende juros automaticamente.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Porque diminui o risco de gastar tudo e deixa o "
                                    "objetivo protegido antes dos outros gastos."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Porque a reserva só pode ser feita no começo do mês.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Porque não é preciso mais se preocupar com as "
                                    "despesas essenciais."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Boa! Separar logo no início protege o seu objetivo e a sua "
                            "reserva, em vez de depender do que sobra no fim do mês."
                        ),
                        "feedback_incorrect": (
                            "Revise a ideia. Separar logo no início protege o objetivo e "
                            "a reserva: se você espera sobrar, o dinheiro quase sempre "
                            "acaba antes."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Imagine que você recebeu R$ 1.800 líquidos no seu primeiro "
                            "salário. Como você dividiria esse valor? Escreva quanto iria "
                            "para cada categoria (essenciais, objetivos, reserva, lazer, "
                            "o que mais achar importante) e explique por quê."
                        ),
                        "competency_codes": ["1.3.1", "1.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado quando a integração de IA estiver "
                            "disponível. Enquanto isso, confira se a soma não passa de "
                            "R$ 1.800 e se você justificou as prioridades."
                        ),
                        "evaluation_criteria": [
                            "Menciona despesas essenciais.",
                            "Menciona objetivos.",
                            "Menciona reserva.",
                            "A soma dos valores informados não ultrapassa R$ 1.800.",
                            "Justifica a divisão escolhida.",
                        ],
                        "max_length": 3000,
                    },
                },
                {
                    "order": 4,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que você faz com o seu primeiro salário?",
                        "scenario": (
                            "Você recebeu seu primeiro salário: R$ 1.800 líquidos. Suas "
                            "despesas essenciais somam R$ 1.100. Você tem uma conta "
                            "atrasada de R$ 250 que está gerando multa e juros. Você "
                            "também paga um curso de inglês de R$ 150 por mês, que é um "
                            "objetivo importante para você. E há um tênis de R$ 400 que "
                            "você quer muito."
                        ),
                        "competency_codes": ["1.3.1", "1.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pago as essenciais e a conta atrasada, mantenho o "
                                    "curso e guardo o restante (R$ 300); o tênis fica para "
                                    "quando eu juntar o valor."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pago as essenciais, compro o tênis e deixo a conta "
                                    "atrasada para o mês seguinte."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pago as essenciais, o tênis e o curso, e pago da "
                                    "conta atrasada só o que sobrar."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Compro o tênis primeiro, porque está em promoção, e "
                                    "pago o que der das outras contas."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Boa decisão! Você pagou o essencial (R$ 1.100), quitou a "
                            "conta que gerava juros (R$ 250), manteve o objetivo "
                            "(R$ 150) e ainda guardou R$ 300. O tênis não foi cancelado: "
                            "virou uma meta que você pode juntar aos poucos."
                        ),
                        "feedback_incorrect": (
                            "Revise suas prioridades. Primeiro o essencial, depois a conta "
                            "atrasada, que cresce com multa e juros a cada mês. Só então "
                            "vêm o objetivo e a reserva, e por último o desejo. Fazendo "
                            "isso: 1.100 + 250 + 150 = 1.500, e ainda sobram R$ 300."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Um plano simples para a sua renda",
                    "order": 1,
                    "body": (
                        "Um plano financeiro não precisa ser complicado. Comece sempre "
                        "pelo **salário líquido**, que é o dinheiro que realmente existe, "
                        "e distribua em ordem de prioridade:\n\n"
                        "1. **Despesas essenciais:** moradia, alimentação, transporte, "
                        "contas básicas.\n"
                        "2. **Dívidas e contas atrasadas:** especialmente as que geram "
                        "multa e juros, porque crescem com o tempo.\n"
                        "3. **Objetivos e reserva:** uma parte para algo que você quer "
                        "conquistar (um curso, um aparelho) e para imprevistos.\n"
                        "4. **Desejos e lazer:** com o que sobrar, sem culpa.\n\n"
                        "A soma de tudo **não pode passar da renda**. Se passar, é hora de "
                        "rever as prioridades, e não de usar dinheiro que ainda não existe."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Do salário à divisão",
                    "order": 2,
                    "body": (
                        "O Lucas recebeu R$ 1.500 líquidos no primeiro mês. Ele montou "
                        "assim:\n\n"
                        "- Essenciais (moradia, comida, transporte): R$ 900\n"
                        "- Conta atrasada (com multa e juros): R$ 150\n"
                        "- Objetivo (curso online): R$ 150\n"
                        "- Reserva: R$ 100\n"
                        "- Lazer e desejos: R$ 200\n"
                        "- **Total: R$ 1.500**\n\n"
                        "Repare que as essenciais ocupam 60% da renda, e isso é comum "
                        "quando a renda ainda é baixa. O importante é que cada real tem um "
                        "destino e a soma fecha em R$ 1.500."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Separe antes de gastar",
                    "order": 3,
                    "body": (
                        "Uma forma de proteger o seu objetivo e a sua reserva é separá-los "
                        "**assim que o salário cai**, e não esperar ver o que sobra no fim "
                        "do mês, porque quase nunca sobra. Existe uma referência popular "
                        "chamada 50/30/20 (50% essenciais, 30% desejos, 20% objetivos e "
                        "reserva), mas ela é só um ponto de partida: com renda menor, as "
                        "essenciais costumam ocupar mais espaço, e tudo bem."
                    ),
                },
            ],
        },
    ],
}
