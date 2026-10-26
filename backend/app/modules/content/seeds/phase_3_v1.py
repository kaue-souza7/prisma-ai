"""Conteúdo versionado da Fase 3 — Por que poupar.

Este módulo é a fonte da migration 0005 e dos testes de contrato. Alterações
editoriais posteriores devem gerar uma nova versão/migração, preservando a
reprodutibilidade do histórico.
"""
from app.modules.content.seeds._text import md

PHASE_3_V1 = {
    "phase_number": 3,
    "missions": [
        {
            "number": 1,
            "name": "Um objetivo que faz sentido",
            "description": (
                "Defina uma meta com valor e prazo e calcule quanto precisa "
                "guardar por mês para alcançá-la."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.1.1",
                    "name": "Definir uma meta financeira específica",
                    "description": (
                        "Descreve uma meta com objetivo, valor e prazo, em vez de "
                        "um desejo genérico."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.1.2",
                    "name": "Calcular quanto guardar por mês",
                    "description": (
                        "Divide o valor da meta pelo número de meses para obter "
                        "o valor mensal necessário, sem considerar rendimento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.1.3",
                    "name": "Avaliar se a meta cabe no orçamento",
                    "description": (
                        "Compara o valor mensal necessário com o que sobra no "
                        "orçamento e ajusta prazo ou valor quando não couber."
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
                            "Qual das frases abaixo é uma meta financeira bem "
                            "definida?"
                        ),
                        "competency_codes": ["3.1.1"],
                        "options": [
                            {"value": "a", "label": "Quero juntar dinheiro."},
                            {
                                "value": "b",
                                "label": "Quero guardar mais este ano.",
                            },
                            {
                                "value": "c",
                                "label": "Quero comprar um notebook um dia.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Quero juntar R$ 1.200 para um notebook "
                                    "usado em 8 meses."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Exato! Uma boa meta diz para quê, quanto e até "
                            "quando. Com valor e prazo, dá para saber quanto "
                            "guardar por mês."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Uma meta bem definida tem objetivo, "
                            "valor e prazo. Só a opção \"juntar R$ 1.200 para um "
                            "notebook usado em 8 meses\" tem os três."
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
                            "Você quer juntar R$ 1.800 em 9 meses. Sem "
                            "considerar rendimento, quanto precisa guardar por "
                            "mês?"
                        ),
                        "competency_codes": ["3.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 150."},
                            {"value": "b", "label": "R$ 180."},
                            {"value": "c", "label": "R$ 250."},
                            {"value": "d", "label": "R$ 200."},
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Correto! 1.800 ÷ 9 = R$ 200 por mês."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Para saber quanto guardar por "
                            "mês, divida o valor da meta pelo número de meses: "
                            "1.800 ÷ 9 = R$ 200."
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
                            "Sua meta é juntar R$ 1.200 em 6 meses, o que exige "
                            "R$ 200 por mês. Mas, depois das despesas essenciais, "
                            "só sobram R$ 120 por mês. Qual é a melhor decisão?"
                        ),
                        "competency_codes": ["3.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Cortar parte do dinheiro da alimentação "
                                    "para fechar a conta."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Usar o limite do cartão para completar o "
                                    "valor que falta."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ajustar a meta: aumentar o prazo para 10 "
                                    "meses ou reduzir o valor para R$ 720."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Manter a meta como está e torcer para "
                                    "sobrar mais dinheiro."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Boa decisão! Com R$ 120 por mês, em 10 meses você "
                            "chega a R$ 1.200, ou em 6 meses chega a R$ 720. "
                            "Ajustar a meta é melhor do que comprometer o "
                            "essencial ou entrar em dívida."
                        ),
                        "feedback_incorrect": (
                            "Revise a decisão. Cortar o essencial ou usar "
                            "crédito para guardar não faz sentido. Quando a meta "
                            "não cabe, ajuste o prazo (1.200 ÷ 120 = 10 meses) "
                            "ou o valor (120 × 6 = R$ 720)."
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
                            "Escreva uma meta financeira sua em uma frase, com "
                            "valor e prazo, e calcule quanto você precisaria "
                            "guardar por mês. Essa quantia caberia no seu "
                            "orçamento?"
                        ),
                        "competency_codes": ["3.1.1", "3.1.2", "3.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona um objetivo, um valor e um prazo para "
                                "a meta."
                            ),
                            (
                                "Apresenta um cálculo coerente, dividindo o valor "
                                "da meta pelo número de meses."
                            ),
                            (
                                "Avalia se o valor mensal cabe no orçamento ou "
                                "explica como ajustar prazo, valor ou renda."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Uma meta precisa de valor e prazo",
                    "order": 1,
                    "body": md(
                        """
                        "Quero juntar dinheiro" é um desejo. "Quero juntar
                        **R$ 1.200** para um notebook usado em **8 meses**" é uma
                        **meta**. Uma boa meta financeira responde a três
                        perguntas:

                        1. **Para quê?** (o objetivo)
                        2. **Quanto?** (o valor)
                        3. **Até quando?** (o prazo)

                        Com valor e prazo, a conta fica simples:

                        **valor da meta ÷ número de meses = quanto guardar por
                        mês**

                        Se o valor mensal não couber no orçamento, você tem três
                        caminhos: **aumentar o prazo**, **reduzir o valor da
                        meta** ou **aumentar a renda**.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A meta da Bia",
                    "order": 2,
                    "body": md(
                        """
                        A Bia quer um notebook usado de R$ 1.200 em 8 meses. A
                        conta: 1.200 ÷ 8 = **R$ 150 por mês**.

                        Mas, depois das despesas essenciais, só sobram R$ 100 por
                        mês para ela. Então a meta, do jeito que está, não cabe.
                        A Bia pode:

                        - aumentar o prazo para 12 meses (1.200 ÷ 12 = R$ 100 por
                          mês); ou
                        - escolher um modelo de R$ 800 e manter os 8 meses
                          (800 ÷ 8 = R$ 100 por mês).
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Metas curtas dão ritmo",
                    "order": 3,
                    "body": md(
                        """
                        Quando a meta é grande, divida em etapas. Chegar a
                        "R$ 300 até o fim do trimestre" é mais fácil de
                        acompanhar do que esperar um ano para ver o resultado.
                        """
                    ),
                },
            ],
        },
        {
            "number": 2,
            "name": "Guardar sem perder o controle",
            "description": (
                "Equilibre poupança, despesas essenciais e lazer, e escolha "
                "estratégias realistas de economia."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.2.1",
                    "name": "Equilibrar poupança, essenciais e lazer",
                    "description": (
                        "Distribui a renda entre despesas essenciais, poupança "
                        "e lazer sem ultrapassar o valor disponível."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.2.2",
                    "name": "Identificar pequenos gastos recorrentes",
                    "description": (
                        "Reconhece assinaturas e compras pequenas que se repetem "
                        "e pesam no orçamento quando somadas."
                    ),
                    "is_essential": False,
                },
                {
                    "code": "3.2.3",
                    "name": "Escolher estratégias de economia realistas",
                    "description": (
                        "Propõe reduções que liberam valor sem comprometer "
                        "despesas essenciais nem criar dívidas."
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
                            "A Maria recebe R$ 1.600 líquidos por mês. As "
                            "despesas essenciais dela somam R$ 1.000. Ela quer "
                            "guardar R$ 200 e ter um valor para lazer. Qual "
                            "divisão fecha a conta sem passar da renda?"
                        ),
                        "competency_codes": ["3.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Guardar R$ 300 e lazer de R$ 400.",
                            },
                            {
                                "value": "b",
                                "label": "Guardar R$ 200 e lazer de R$ 500.",
                            },
                            {
                                "value": "c",
                                "label": "Guardar R$ 200 e lazer de R$ 400.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não guardar nada e lazer de R$ 700."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! 1.000 (essenciais) + 200 (poupança) + 400 "
                            "(lazer) = R$ 1.600, exatamente a renda dela."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. A soma de essenciais, poupança e "
                            "lazer não pode passar de R$ 1.600. A única opção "
                            "que fecha é 1.000 + 200 + 400 = R$ 1.600."
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
                            "O Davi paga R$ 29,90 de streaming, R$ 19,90 de "
                            "música e pede delivery 6 vezes por mês, a R$ 15 "
                            "cada. Quanto esses gastos somam por mês?"
                        ),
                        "competency_codes": ["3.2.2"],
                        "options": [
                            {"value": "a", "label": "R$ 49,80."},
                            {"value": "b", "label": "R$ 90,00."},
                            {"value": "c", "label": "R$ 139,80."},
                            {"value": "d", "label": "R$ 169,80."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! 29,90 + 19,90 + (6 × 15 = 90) = R$ 139,80 "
                            "por mês. Pequenos gastos recorrentes pesam quando "
                            "somados."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Some tudo: assinaturas (29,90 + "
                            "19,90 = 49,80) mais delivery (6 × 15 = 90) dá "
                            "R$ 139,80 por mês."
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
                            "Você quer guardar R$ 150 por mês. Qual estratégia "
                            "é mais realista e segura?"
                        ),
                        "competency_codes": ["3.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Reduzir o mercado pela metade.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Rever assinaturas e delivery e separar os "
                                    "R$ 150 assim que o salário cair."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Usar o limite do cartão para fechar o mês."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Deixar de pagar uma conta essencial por "
                                    "alguns meses."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Boa estratégia! Revisar gastos recorrentes e "
                            "separar o valor logo no início protege o essencial "
                            "e a meta."
                        ),
                        "feedback_incorrect": (
                            "Revise a estratégia. Cortar a alimentação, usar "
                            "crédito ou deixar contas essenciais de lado cria "
                            "problemas maiores. O caminho seguro é rever gastos "
                            "recorrentes e separar a meta no início do mês."
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
                            "Quais gastos pequenos e recorrentes você tem hoje? "
                            "Quais você reduziria sem prejudicar o essencial, e "
                            "quanto isso renderia por mês?"
                        ),
                        "competency_codes": ["3.2.2", "3.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona um ou mais gastos pequenos e "
                                "recorrentes."
                            ),
                            (
                                "Propõe uma redução que não compromete o "
                                "essencial."
                            ),
                            (
                                "Estima quanto a redução liberaria por mês."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Poupar não é cortar tudo, é decidir",
                    "order": 1,
                    "body": md(
                        """
                        Guardar dinheiro não significa viver sem lazer. Significa
                        **decidir** para onde o dinheiro vai, antes de gastar.
                        Algumas estratégias que funcionam:

                        - **Separar logo no início do mês** o valor da meta,
                          antes de gastar com outras coisas.
                        - **Rever gastos recorrentes:** assinaturas, delivery,
                          pequenas compras que se repetem. Pequenos valores,
                          somados, pesam.
                        - **Definir um limite de lazer**, para se divertir sem
                          culpa e sem estourar o orçamento.

                        Cuidado com o extremo oposto: cortar o essencial (como
                        alimentação) para guardar mais costuma fazer o plano ruir
                        em poucas semanas.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Os gastos pequenos do Davi",
                    "order": 2,
                    "body": md(
                        """
                        O Davi paga R$ 29,90 por mês de streaming e R$ 19,90 de
                        música, e pede delivery 6 vezes por mês, a R$ 15 cada.

                        - Assinaturas: 29,90 + 19,90 = R$ 49,80
                        - Delivery: 6 × 15 = R$ 90,00
                        - **Total: R$ 139,80 por mês**, ou mais de R$ 1.600 por
                          ano.

                        Ele não precisa cortar tudo. Manter uma assinatura e
                        reduzir o delivery pela metade já libera uma boa parte
                        desse valor para a meta.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A regra das 24 horas",
                    "order": 3,
                    "body": md(
                        """
                        Antes de uma compra por impulso (que não é uma
                        necessidade), espere 24 horas. Se depois desse tempo você
                        ainda quiser e a compra couber no plano, tudo bem. Muitas
                        vezes a vontade passa.
                        """
                    ),
                },
            ],
        },
        {
            "number": 3,
            "name": "E se acontecer algo inesperado?",
            "description": (
                "Entenda o que é reserva de emergência, distinga imprevisto de "
                "desejo e calcule uma reserva inicial."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.3.1",
                    "name": "Explicar a reserva de emergência",
                    "description": (
                        "Entende que a reserva é um dinheiro separado, seguro e "
                        "de fácil acesso para cobrir imprevistos."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.3.2",
                    "name": "Distinguir imprevisto de desejo",
                    "description": (
                        "Classifica como imprevisto o gasto não planejado e "
                        "urgente, diferenciando-o de promoções e gastos "
                        "planejados."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.3.3",
                    "name": "Calcular o valor-alvo de uma reserva",
                    "description": (
                        "Multiplica as despesas essenciais pelo número de meses "
                        "desejado para obter o valor da reserva."
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
                            "Qual é a principal função de uma reserva de "
                            "emergência?"
                        ),
                        "competency_codes": ["3.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Render o máximo possível, mesmo com risco."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Pagar compras em promoção.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Servir de entrada para financiar um bem."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Cobrir imprevistos, com dinheiro seguro e "
                                    "de fácil acesso."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Exato! A reserva existe para imprevistos e precisa "
                            "ser segura e de fácil acesso."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A reserva de emergência é um "
                            "dinheiro separado, seguro e de fácil acesso, para "
                            "cobrir imprevistos. Não é para promoções nem para "
                            "correr risco por rendimento."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual dos itens abaixo é um imprevisto?",
                        "competency_codes": ["3.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A geladeira quebrar e precisar de conserto "
                                    "urgente."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "A TV em promoção na Black Friday."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "A passagem de uma viagem planejada para o "
                                    "ano que vem."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "O presente de aniversário de um amigo, no "
                                    "mês que vem."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Um conserto urgente é um imprevisto: não "
                            "estava planejado e não dá para esperar. Os outros "
                            "itens são desejos ou gastos que dá para planejar."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Imprevisto é o que não estava no "
                            "plano e não dá para esperar, como o conserto "
                            "urgente da geladeira. Promoção, viagem e presente "
                            "são desejos ou gastos que podem ser planejados."
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
                            "Suas despesas essenciais somam R$ 1.300 por mês. "
                            "Qual é o valor de uma reserva de emergência de 3 "
                            "meses?"
                        ),
                        "competency_codes": ["3.3.3"],
                        "options": [
                            {"value": "a", "label": "R$ 1.300."},
                            {"value": "b", "label": "R$ 2.600."},
                            {"value": "c", "label": "R$ 3.900."},
                            {"value": "d", "label": "R$ 5.200."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! 3 × 1.300 = R$ 3.900."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. A reserva de 3 meses é o valor "
                            "das despesas essenciais multiplicado por 3: "
                            "3 × 1.300 = R$ 3.900."
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
                            "Se a sua renda parasse por 1 mês, o que aconteceria "
                            "com as suas contas? O que uma reserva de emergência "
                            "mudaria nessa situação?"
                        ),
                        "competency_codes": ["3.3.1", "3.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Identifica quais despesas essenciais ficariam "
                                "em risco."
                            ),
                            (
                                "Explica o papel da reserva em cobrir essas "
                                "despesas."
                            ),
                            (
                                "Menciona uma noção de valor ou meta para a "
                                "reserva, como 1 mês de despesas."
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
                        "prompt": "O que você faz quando a geladeira quebra?",
                        "scenario": (
                            "Você recebe R$ 1.800 líquidos por mês. As despesas "
                            "essenciais somam R$ 1.100. Sua meta é juntar R$ 600 "
                            "em 6 meses para um curso (R$ 100 por mês), e você já "
                            "tem uma reserva de R$ 300. No terceiro mês, a "
                            "geladeira quebra e o conserto custa R$ 350. O que "
                            "você faz?"
                        ),
                        "competency_codes": ["3.3.1", "3.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Uso os R$ 300 que já guardei para o curso e "
                                    "deixo a reserva intocada."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Parcelo o conserto no cartão e deixo de "
                                    "guardar nos próximos meses."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Peço dinheiro emprestado com juros altos "
                                    "para não mexer em nada."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Uso a reserva (R$ 300), completo os R$ 50 "
                                    "com o dinheiro livre do mês, mantenho a meta "
                                    "do curso e volto a repor a reserva nos meses "
                                    "seguintes."
                                ),
                            },
                        ],
                        "correct_choice": "d",
                        "feedback_correct": (
                            "Boa decisão! Era exatamente para isso que a reserva "
                            "existia. Você cobriu o imprevisto (300 + 50 = "
                            "R$ 350), manteve a meta do curso e vai repor a "
                            "reserva nos próximos meses, sem entrar em dívida."
                        ),
                        "feedback_incorrect": (
                            "Revise suas escolhas. A reserva existe para "
                            "imprevistos como esse. Usar o dinheiro da meta, "
                            "parcelar no cartão ou pegar empréstimo com juros "
                            "altos desorganiza o plano ou cria dívida. O caminho "
                            "é usar a reserva, completar o que faltar com o "
                            "dinheiro livre do mês e repor depois."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Reserva de emergência",
                    "order": 1,
                    "body": md(
                        """
                        **Reserva de emergência** é um dinheiro separado, de
                        fácil acesso, para cobrir **imprevistos**: perda de
                        renda, um conserto urgente, uma despesa de saúde. Ela não
                        é para desejos, promoções ou viagens.

                        Duas características importam mais do que o rendimento:
                        **segurança** (você não pode correr risco de perder esse
                        dinheiro) e **acesso rápido** (você precisa conseguir
                        usá-lo quando precisar).

                        Uma referência comum é juntar de **3 a 6 meses de
                        despesas essenciais**. Para quem está começando, um bom
                        primeiro passo é chegar a **1 mês** de essenciais e ir
                        aumentando aos poucos.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A reserva do Gui",
                    "order": 2,
                    "body": md(
                        """
                        As despesas essenciais do Gui somam R$ 1.100 por mês.

                        - Reserva de 1 mês: R$ 1.100
                        - Reserva de 3 meses: 3 × 1.100 = **R$ 3.300**

                        Guardando R$ 100 por mês, o Gui chega a 1 mês de reserva
                        em 11 meses. Parece devagar, mas cada R$ 100 guardado já o
                        protege de um imprevisto.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Usou? Reponha",
                    "order": 3,
                    "body": md(
                        """
                        A reserva existe para ser usada nos imprevistos. Se você
                        precisar dela, **volte a repô-la** assim que puder. E não
                        use a reserva para promoções: promoção é desejo, não
                        emergência.
                        """
                    ),
                },
            ],
        },
    ],
}
