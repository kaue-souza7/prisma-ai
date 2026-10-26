"""Conteúdo versionado da Fase 5 — Onde o dinheiro rende.

Este módulo é a fonte da migration 0007 e dos testes de contrato. Alterações
editoriais posteriores devem gerar uma nova versão/migração, preservando a
reprodutibilidade do histórico.

A fase é educacional: as alternativas de guardar ou investir usadas nos exemplos
e nas simulações são fictícias e não constituem recomendação de investimento.
As taxas citadas não representam taxas reais do mercado.
"""
from app.modules.content.seeds._text import md

PHASE_5_V1 = {
    "phase_number": 5,
    "missions": [
        {
            "number": 1,
            "name": "O que meu dinheiro consegue comprar?",
            "description": (
                "Entenda inflação e poder de compra e distinga rendimento "
                "nominal de rendimento real."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.1.1",
                    "name": "Explicar inflação e poder de compra",
                    "description": (
                        "Entende que inflação é o aumento geral e contínuo dos "
                        "preços e que ela reduz o que o mesmo dinheiro compra."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.1.2",
                    "name": "Calcular o efeito da inflação sobre um preço",
                    "description": (
                        "Aplica uma taxa de inflação ao preço de um item para "
                        "estimar o valor no período seguinte."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.1.3",
                    "name": "Distinguir rendimento nominal de real",
                    "description": (
                        "Compara o rendimento do dinheiro com a inflação para "
                        "avaliar se o poder de compra aumentou ou diminuiu."
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
                        "prompt": "O que é inflação?",
                        "competency_codes": ["5.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Aumento geral e contínuo dos preços.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Queda dos preços de um único produto."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "O valor que o banco cobra por manter a "
                                    "conta."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "O rendimento do dinheiro guardado.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! Inflação é o aumento geral e contínuo dos "
                            "preços. Com ela, o mesmo dinheiro compra menos ao "
                            "longo do tempo."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Inflação é o aumento geral e "
                            "contínuo dos preços, e não a mudança no preço de um "
                            "único produto nem o rendimento do dinheiro."
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
                            "Uma cesta custa R$ 200 hoje. Com inflação de 5% ao "
                            "ano, quanto ela custará daqui a 1 ano?"
                        ),
                        "competency_codes": ["5.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 205."},
                            {"value": "b", "label": "R$ 210."},
                            {"value": "c", "label": "R$ 220."},
                            {"value": "d", "label": "R$ 195."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! 5% de R$ 200 são R$ 10, então a cesta "
                            "passa a custar R$ 210."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Calcule 5% de R$ 200 "
                            "(200 × 0,05 = R$ 10) e some ao preço atual: "
                            "200 + 10 = R$ 210."
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
                            "Seu dinheiro rendeu 4% no ano, e a inflação foi de "
                            "6% no mesmo período. O que aconteceu com o seu poder "
                            "de compra?"
                        ),
                        "competency_codes": ["5.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Aumentou, porque o dinheiro rendeu."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Ficou exatamente igual.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Só mudaria se a inflação fosse menor que "
                                    "1%."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Diminuiu, porque o rendimento ficou abaixo "
                                    "da inflação."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Correto! Você tem mais reais, mas os preços subiram "
                            "mais do que o seu dinheiro. O rendimento real foi "
                            "negativo e o poder de compra diminuiu."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Quando o rendimento (4%) fica abaixo "
                            "da inflação (6%), o dinheiro cresce em reais, mas "
                            "compra menos. O rendimento real foi negativo."
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
                            "Dê um exemplo do seu dia a dia em que você percebeu "
                            "que o dinheiro \"comprava menos\". Como a inflação "
                            "explica isso?"
                        ),
                        "competency_codes": ["5.1.1", "5.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Apresenta um exemplo concreto de preço que "
                                "subiu."
                            ),
                            (
                                "Relaciona o exemplo à inflação como aumento "
                                "geral de preços."
                            ),
                            (
                                "Explica que o mesmo dinheiro passou a comprar "
                                "menos, reduzindo o poder de compra."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Inflação e poder de compra",
                    "order": 1,
                    "body": md(
                        """
                        **Inflação** é o aumento geral e contínuo dos preços. No
                        Brasil, ela é medida por um índice oficial, o **IPCA**,
                        calculado pelo IBGE.

                        **Poder de compra** é o quanto você consegue comprar com
                        a mesma quantia de dinheiro. Quando os preços sobem, o
                        mesmo dinheiro compra menos.

                        Isso muda a forma de olhar para o dinheiro guardado. Se os
                        preços sobem 5% em um ano e o seu dinheiro rende só 3%,
                        você tem **mais** reais do que antes, mas consegue comprar
                        **menos**. Dizemos que o **rendimento real** foi negativo.

                        - **Rendimento nominal:** quanto o dinheiro cresceu em
                          reais.
                        - **Rendimento real:** quanto o dinheiro cresceu
                          **descontando a inflação**, ou seja, em poder de compra.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A cesta de R$ 100",
                    "order": 2,
                    "body": md(
                        """
                        Os números abaixo são fictícios. Uma cesta de compras
                        custa R$ 100 hoje. Com **inflação de 5% ao ano**, a mesma
                        cesta custará **R$ 105** daqui a um ano.

                        - Se o dinheiro ficou **parado** (R$ 100), compra só cerca
                          de 95% da cesta.
                        - Se o dinheiro **rendeu 3%** (R$ 103), ainda não alcança
                          os R$ 105: a pessoa tem mais dinheiro, mas compra um
                          pouco menos do que antes.
                        - Se o dinheiro **rendeu 6%** (R$ 106), passa dos R$ 105:
                          o poder de compra foi preservado e até aumentou um
                          pouco.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A sua inflação é a dos seus gastos",
                    "order": 3,
                    "body": md(
                        """
                        O IPCA é uma média. A inflação que você sente depende do
                        que mais pesa no seu orçamento, como comida e transporte.
                        Observar o preço dos itens que você mais compra ajuda a
                        perceber o efeito na prática.
                        """
                    ),
                },
            ],
        },
        {
            "number": 2,
            "name": "Guardar ou investir?",
            "description": (
                "Diferencie reserva de investimento, entenda que investir "
                "envolve risco e relacione o prazo do objetivo à aplicação."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.2.1",
                    "name": "Diferenciar guardar para reserva e investir",
                    "description": (
                        "Reconhece que a reserva prioriza segurança e acesso "
                        "rápido, enquanto investir aceita prazo ou risco em troca "
                        "de rendimento potencial."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.2.2",
                    "name": "Reconhecer risco e promessas exageradas",
                    "description": (
                        "Identifica que todo investimento envolve risco e que "
                        "ganho alto, garantido e sem risco é sinal de alerta."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.2.3",
                    "name": "Associar prazo do objetivo à aplicação",
                    "description": (
                        "Relaciona objetivos de curto prazo a segurança e "
                        "liquidez, e objetivos longos a prazos maiores."
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
                            "Qual é a principal prioridade de uma reserva de "
                            "emergência?"
                        ),
                        "competency_codes": ["5.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Render o máximo possível, mesmo com risco."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Ter segurança e acesso rápido ao dinheiro."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Ficar bloqueada por vários anos.",
                            },
                            {
                                "value": "d",
                                "label": "Ser indicada por alguém famoso.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! A reserva existe para imprevistos, então o "
                            "mais importante é que o dinheiro esteja seguro e "
                            "possa ser usado rapidamente."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A prioridade de uma reserva é "
                            "segurança e acesso rápido. Render mais, ficar "
                            "bloqueada ou ser indicada por alguém famoso não são "
                            "o que torna uma reserva adequada."
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
                            "Um anúncio promete \"ganho garantido de 10% ao mês, "
                            "sem nenhum risco\". O que isso indica?"
                        ),
                        "competency_codes": ["5.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Uma excelente oportunidade, porque é "
                                    "garantida."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Um produto oficial do governo.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Um sinal de alerta: retorno alto e "
                                    "garantido, sem risco, é uma promessa típica "
                                    "de golpe."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Um investimento ideal para a reserva de "
                                    "emergência."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Muito bem! Retorno alto, garantido e sem risco não "
                            "existe. Esse tipo de promessa é um sinal clássico de "
                            "golpe."
                        ),
                        "feedback_incorrect": (
                            "Revise o conceito. Todo investimento envolve algum "
                            "risco, e quanto maior o retorno prometido, maior "
                            "costuma ser o risco. Promessa de ganho alto e "
                            "garantido é sinal de alerta."
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
                            "Você vai precisar do dinheiro daqui a 3 meses para "
                            "pagar um curso. Qual característica é mais "
                            "importante na aplicação?"
                        ),
                        "competency_codes": ["5.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Rendimento mais alto possível, mesmo com "
                                    "risco de perda."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Liquidez e baixo risco.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Prazo de 5 anos para render mais."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Ter sido indicada por um influenciador."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Quando o dinheiro vai ser usado em pouco "
                            "tempo, o importante é ter acesso rápido e não correr "
                            "risco de perder parte dele."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Para um objetivo de curto prazo, o "
                            "mais importante é a liquidez (acesso rápido) e o "
                            "baixo risco. Um prazo longo ou um risco alto podem "
                            "atrapalhar o pagamento do curso."
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
                            "Para qual objetivo seu você guardaria dinheiro por "
                            "poucos meses, e para qual por muitos anos? Que "
                            "cuidado você teria em cada caso?"
                        ),
                        "competency_codes": ["5.2.1", "5.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona dois objetivos com prazos diferentes, "
                                "um curto e um longo."
                            ),
                            (
                                "Apresenta um cuidado coerente para o curto "
                                "prazo, como segurança ou acesso rápido."
                            ),
                            (
                                "Apresenta uma consideração coerente para o longo "
                                "prazo, como aceitar mais tempo ou variação."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Reserva e investimento têm objetivos diferentes",
                    "order": 1,
                    "body": md(
                        """
                        **Guardar dinheiro para reserva** tem como prioridade a
                        **segurança** e o **acesso rápido**. O objetivo não é
                        render o máximo, e sim ter o dinheiro disponível quando um
                        imprevisto aparecer.

                        **Investir** significa aceitar um prazo maior ou algum
                        risco em troca de um rendimento potencial maior. Por isso
                        a ordem costuma ser: **primeiro a reserva, depois os
                        investimentos**.

                        Alguns pontos importantes:

                        - **Todo investimento envolve algum risco.** Quanto maior
                          o rendimento prometido, em geral maior o risco ou o
                          prazo.
                        - **Rendimento passado não garante rendimento futuro.**
                        - **Prazo curto pede segurança e acesso rápido.** Para
                          objetivos de muitos anos, é possível aceitar mais
                          variação.
                        - **Desconfie de promessas de ganho alto e garantido**,
                          sem risco. Esse é um dos sinais mais comuns de golpe (a
                          Fase 6 volta a esse tema).
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O Léo e os dois objetivos",
                    "order": 2,
                    "body": md(
                        """
                        O Léo tem dois objetivos:

                        1. **Reserva de emergência (R$ 3.000):** ele pode
                           precisar do dinheiro a qualquer momento. O mais
                           importante é segurança e acesso rápido.
                        2. **Viagem daqui a 5 anos:** como ele não vai usar o
                           dinheiro por muito tempo, pode aceitar prazos maiores
                           na aplicação.

                        O mesmo Léo, para dois objetivos com prazos diferentes,
                        escolhe características diferentes. Não existe "a melhor
                        aplicação" para tudo: existe a mais adequada para cada
                        objetivo.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Se promete muito e sem risco, desconfie",
                    "order": 3,
                    "body": md(
                        """
                        Retorno alto, garantido e sem risco não existe. Se uma
                        oferta prometer isso, trate como sinal de alerta: pesquise
                        a empresa, pergunte onde o dinheiro será aplicado e
                        converse com alguém de confiança antes de decidir.
                        """
                    ),
                },
            ],
        },
        {
            "number": 3,
            "name": "Rendimento, prazo e liquidez",
            "description": (
                "Compare alternativas fictícias usando rendimento, prazo, "
                "liquidez e risco, e entenda o que o FGC cobre."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "5.3.1",
                    "name": "Explicar rendimento, prazo, liquidez e risco",
                    "description": (
                        "Diferencia as quatro características usadas para "
                        "comparar formas de guardar dinheiro."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.3.2",
                    "name": "Comparar alternativas fictícias",
                    "description": (
                        "Escolhe entre opções fictícias considerando rendimento, "
                        "prazo e liquidez para cada objetivo."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "5.3.3",
                    "name": "Reconhecer a cobertura do FGC",
                    "description": (
                        "Identifica quais produtos têm cobertura do FGC e quais "
                        "não têm."
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
                        "prompt": "O que é liquidez?",
                        "competency_codes": ["5.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O valor total que uma aplicação rende por "
                                    "ano."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "O risco de perder o dinheiro aplicado."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "A facilidade e a rapidez de transformar uma "
                                    "aplicação em dinheiro, sem perda relevante."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "O prazo máximo que o dinheiro pode ficar "
                                    "aplicado."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! Liquidez é a facilidade e a rapidez de "
                            "transformar a aplicação em dinheiro sem perda "
                            "relevante."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Liquidez é a facilidade e a rapidez "
                            "de transformar uma aplicação em dinheiro, sem perda "
                            "relevante. Rendimento, risco e prazo são outras "
                            "características."
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
                            "Duas alternativas fictícias. Opção X: rende 0,8% ao "
                            "mês, com resgate a qualquer dia. Opção Y: rende 1,0% "
                            "ao mês, com resgate só após 12 meses. Você precisa "
                            "de uma reserva para emergências, que pode ser usada a "
                            "qualquer momento. Qual escolher?"
                        ),
                        "competency_codes": ["5.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Opção Y, porque rende mais.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Opção X, porque tem liquidez para uso em "
                                    "emergências."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "As duas servem igualmente para reserva."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Nenhuma; é melhor guardar o dinheiro em "
                                    "casa."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Para uma reserva de emergência, o acesso "
                            "rápido é mais importante que um pequeno rendimento "
                            "extra. A Opção X atende a isso."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Uma reserva precisa estar disponível "
                            "a qualquer momento. A Opção Y, apesar de render mais, "
                            "prende o dinheiro por 12 meses, o que não combina com "
                            "emergências."
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
                            "Qual destes produtos NÃO tem cobertura do FGC?"
                        ),
                        "competency_codes": ["5.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "CDB emitido por um banco.",
                            },
                            {
                                "value": "b",
                                "label": "Caderneta de poupança.",
                            },
                            {
                                "value": "c",
                                "label": "Ações negociadas na bolsa.",
                            },
                            {
                                "value": "d",
                                "label": "LCI emitida por um banco.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Ações não têm cobertura do FGC. Já CDB, "
                            "poupança e LCI (de instituições participantes) têm, "
                            "dentro dos limites."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. O FGC cobre depósitos e alguns "
                            "títulos de instituições financeiras, como CDB, "
                            "poupança e LCI. Ações, fundos e Tesouro Direto não "
                            "têm essa cobertura."
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
                            "Escolha uma das alternativas fictícias da missão "
                            "(Opção X ou Opção Y) e explique, usando prazo, "
                            "rendimento e liquidez, se ela serviria para uma "
                            "reserva de emergência."
                        ),
                        "competency_codes": ["5.3.1", "5.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona ao menos duas das três características: "
                                "rendimento, prazo e liquidez."
                            ),
                            (
                                "Conecta as características ao objetivo de "
                                "reserva de emergência."
                            ),
                            (
                                "Conclui de forma coerente, reconhecendo que a "
                                "reserva precisa de liquidez."
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
                        "prompt": "Como você distribui o dinheiro?",
                        "scenario": (
                            "Você tem R$ 3.000 e dois objetivos. Objetivo 1: "
                            "manter R$ 2.000 como reserva de emergência, que pode "
                            "ser necessária a qualquer momento. Objetivo 2: juntar "
                            "R$ 1.000 para uma viagem daqui a 2 anos. Três "
                            "alternativas fictícias. Alternativa 1: resgate "
                            "imediato, rende 0,7% ao mês, baixo risco. "
                            "Alternativa 2: resgate só após 24 meses, rende 1,0% "
                            "ao mês, baixo risco. Alternativa 3: resgate imediato, "
                            "\"pode render muito, mas também pode perder\", sem "
                            "garantia, indicada por um influenciador. Como você "
                            "distribui o dinheiro?"
                        ),
                        "competency_codes": ["5.3.1", "5.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Tudo na Alternativa 3, para render o máximo "
                                    "possível."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Tudo na Alternativa 2, porque rende mais."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Reserva de R$ 2.000 na Alternativa 1 e "
                                    "viagem de R$ 1.000 na Alternativa 2."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Reserva na Alternativa 3 e viagem na "
                                    "Alternativa 1."
                                ),
                            },
                        ],
                        "correct_choice": "c",
                        "feedback_correct": (
                            "Ótima distribuição! A reserva precisa de liquidez e "
                            "baixo risco (Alternativa 1). A viagem, com prazo de "
                            "2 anos, combina com a Alternativa 2, que prende o "
                            "dinheiro por 24 meses e rende mais. Você também "
                            "evitou a Alternativa 3, que tem risco de perda e é "
                            "indicada só por um influenciador."
                        ),
                        "feedback_incorrect": (
                            "Revise a distribuição. A reserva precisa de acesso "
                            "rápido e baixo risco. Prender a reserva por 24 meses "
                            "(Alternativa 2) ou arriscá-la na Alternativa 3 não "
                            "combina com emergências. O prazo de 2 anos da viagem "
                            "combina com a Alternativa 2."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Quatro características para comparar",
                    "order": 1,
                    "body": md(
                        """
                        Para comparar formas de guardar dinheiro, olhe para
                        quatro características:

                        - **Rendimento:** quanto o dinheiro cresce.
                        - **Prazo:** por quanto tempo o dinheiro fica aplicado.
                        - **Liquidez:** a facilidade e a rapidez de transformar a
                          aplicação em dinheiro, sem perda relevante.
                        - **Risco:** a chance de o resultado ser diferente do
                          esperado, inclusive de perder parte do valor.

                        Em geral, **mais rendimento** costuma exigir **mais prazo
                        ou mais risco**. Não existe aplicação com rendimento
                        máximo, liquidez total e risco zero ao mesmo tempo.

                        Existe também o **FGC (Fundo Garantidor de Créditos)**,
                        uma proteção para parte dos depósitos e aplicações feitos
                        em instituições financeiras. Ele cobre até **R$ 250 mil
                        por CPF, por instituição financeira**, com um limite
                        global de **R$ 1 milhão a cada 4 anos**. Em geral, cobre
                        produtos como conta corrente, poupança, CDB, LCI e LCA.
                        **Não cobre** ações, fundos de investimento nem títulos do
                        Tesouro Direto. Antes de aplicar, confira sempre se o
                        produto é coberto.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Duas alternativas fictícias",
                    "order": 2,
                    "body": md(
                        """
                        - **Opção X:** rende 0,8% ao mês, o dinheiro pode ser
                          resgatado em qualquer dia, baixo risco.
                        - **Opção Y:** rende 1,0% ao mês, mas o dinheiro só pode
                          ser resgatado depois de 12 meses, baixo risco.

                        A Opção Y rende mais, mas tem **menos liquidez**. Para uma
                        **reserva de emergência**, a Opção X é mais adequada,
                        porque o dinheiro precisa estar disponível. Para um
                        **objetivo daqui a 2 anos**, a Opção Y pode ser
                        interessante.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Três perguntas antes de escolher",
                    "order": 3,
                    "body": md(
                        """
                        "Quando vou precisar desse dinheiro?", "posso aceitar
                        perder parte dele?" e "consigo resgatar sem prejuízo se
                        precisar?". As respostas ajudam a escolher entre
                        rendimento, prazo e liquidez.
                        """
                    ),
                },
            ],
        },
    ],
}
