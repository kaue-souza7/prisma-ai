"""Conteúdo versionado da Fase 4 — Juros: a favor e contra você.

Este módulo é a fonte da migration 0006 e dos testes de contrato. Alterações
editoriais posteriores devem gerar uma nova versão/migração, preservando a
reprodutibilidade do histórico.

As taxas e os valores usados nos exemplos são fictícios e servem apenas para
ilustrar o conceito. Não representam taxas reais do mercado.
"""
from app.modules.content.seeds._text import md

PHASE_4_V1 = {
    "phase_number": 4,
    "missions": [
        {
            "number": 1,
            "name": "O tempo e os juros",
            "description": (
                "Entenda o que são juros, diferencie juros simples de compostos "
                "e estime como um valor cresce com o tempo."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.1.1",
                    "name": "Explicar juros como preço do dinheiro no tempo",
                    "description": (
                        "Reconhece que juros são o preço do uso do dinheiro ao "
                        "longo do tempo, cobrados por quem empresta e recebidos "
                        "por quem investe."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.1.2",
                    "name": "Diferenciar juros simples de compostos",
                    "description": (
                        "Distingue o cálculo sobre o valor inicial do cálculo "
                        "sobre o valor inicial mais os juros acumulados."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.1.3",
                    "name": "Estimar crescimento com juros compostos",
                    "description": (
                        "Calcula o valor acumulado em poucos períodos aplicando "
                        "a taxa sobre o saldo do período anterior."
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
                        "prompt": "O que são juros?",
                        "competency_codes": ["4.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Um valor que o banco dá de presente a quem "
                                    "tem conta."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "O preço pelo uso do dinheiro ao longo do "
                                    "tempo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Um imposto cobrado só de quem tem dívida."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "O valor mínimo que se paga em qualquer "
                                    "compra."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! Juros são o preço do dinheiro no tempo: quem "
                            "empresta cobra, e quem investe recebe."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Juros são o preço pelo uso do "
                            "dinheiro ao longo do tempo. Quem empresta cobra "
                            "juros; quem investe recebe juros."
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
                            "Qual alternativa descreve melhor os juros "
                            "compostos?"
                        ),
                        "competency_codes": ["4.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Juros calculados sempre só sobre o valor "
                                    "inicial."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Juros que diminuem a cada período.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Juros calculados sobre o valor inicial mais "
                                    "os juros já acumulados."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "Juros que só existem em dívidas.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Nos juros compostos, os juros de cada "
                            "período incidem também sobre os juros anteriores, "
                            "por isso o valor cresce cada vez mais rápido."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Juros compostos são calculados "
                            "sobre o valor inicial mais os juros já acumulados, "
                            "o famoso \"juros sobre juros\". Calculados só sobre "
                            "o valor inicial são os juros simples."
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
                            "Você aplica R$ 1.000 a 10% ao ano, com juros "
                            "compostos. Quanto terá ao final de 2 anos?"
                        ),
                        "competency_codes": ["4.1.3"],
                        "options": [
                            {"value": "a", "label": "R$ 1.100."},
                            {"value": "b", "label": "R$ 1.200."},
                            {"value": "c", "label": "R$ 1.210."},
                            {"value": "d", "label": "R$ 1.331."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! No primeiro ano, 1.000 vira 1.100. No "
                            "segundo, os 10% incidem sobre 1.100 e o valor "
                            "chega a R$ 1.210."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Ano 1: 1.000 + 10% = R$ 1.100. "
                            "Ano 2: 1.100 + 10% = R$ 1.210. R$ 1.200 seria o "
                            "resultado com juros simples."
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
                            "Explique com as suas palavras por que os juros "
                            "compostos podem ser ótimos para quem investe e "
                            "ruins para quem está devendo."
                        ),
                        "competency_codes": ["4.1.1", "4.1.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Explica que os juros compostos incidem sobre os "
                                "juros anteriores, o \"juros sobre juros\"."
                            ),
                            (
                                "Relaciona o efeito do tempo ao crescimento cada "
                                "vez mais rápido."
                            ),
                            (
                                "Contrasta investir, quando o valor cresce a "
                                "favor, com dever, quando a dívida cresce contra "
                                "a pessoa."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que são juros",
                    "order": 1,
                    "body": md(
                        """
                        **Juros** são o preço do uso do dinheiro ao longo do
                        tempo. Quem **empresta** dinheiro cobra juros; quem
                        **investe** dinheiro recebe juros. Por isso os juros
                        podem estar a seu favor (quando você guarda ou investe)
                        ou contra você (quando você deve).

                        Existem dois jeitos principais de calcular:

                        - **Juros simples:** calculados sempre sobre o **valor
                          inicial**. O valor dos juros é o mesmo em todo
                          período.
                        - **Juros compostos:** calculados sobre o valor inicial
                          **mais os juros já acumulados**. É o famoso "juros
                          sobre juros": o valor cresce cada vez mais rápido.

                        Na vida real, a maioria dos produtos financeiros
                        (investimentos e dívidas) usa juros compostos.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "R$ 1.000 a 10% ao ano, por 3 anos",
                    "order": 2,
                    "body": md(
                        """
                        Taxa fictícia, só para ilustrar.

                        - **Início:** R$ 1.000 nos dois cálculos.
                        - **Ano 1:** R$ 1.100 com juros simples e R$ 1.100 com
                          juros compostos.
                        - **Ano 2:** R$ 1.200 com juros simples e R$ 1.210 com
                          juros compostos.
                        - **Ano 3:** R$ 1.300 com juros simples e R$ 1.331 com
                          juros compostos.

                        Nos juros simples, são sempre R$ 100 por ano (10% de
                        R$ 1.000). Nos compostos, o 10% do segundo ano incide
                        sobre R$ 1.100, e o do terceiro sobre R$ 1.210. A
                        diferença parece pequena em 3 anos, mas cresce muito com
                        o passar do tempo.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Sempre pergunte a taxa e o prazo",
                    "order": 3,
                    "body": md(
                        """
                        Quando alguém falar em juros, pergunte: "essa taxa é por
                        mês ou por ano? E por quanto tempo?". Uma taxa de 2% ao
                        mês é muito diferente de 2% ao ano.
                        """
                    ),
                },
            ],
        },
        {
            "number": 2,
            "name": "Parcelas não contam a história inteira",
            "description": (
                "Calcule o custo total de compras parceladas e compare com o "
                "preço à vista."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.2.1",
                    "name": "Calcular o custo total de uma compra parcelada",
                    "description": (
                        "Multiplica o valor da parcela pelo número de parcelas "
                        "para obter o total pago."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.2.2",
                    "name": "Comparar à vista e parcelado",
                    "description": (
                        "Subtrai o preço à vista do total parcelado e identifica "
                        "o custo do crédito."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.2.3",
                    "name": "Avaliar o impacto da parcela no orçamento",
                    "description": (
                        "Reconhece que caber no orçamento não basta: é preciso "
                        "olhar o total e o comprometimento dos meses seguintes."
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
                            "Um notebook é vendido em 12x de R$ 250. Qual é o "
                            "custo total da compra?"
                        ),
                        "competency_codes": ["4.2.1"],
                        "options": [
                            {"value": "a", "label": "R$ 250."},
                            {"value": "b", "label": "R$ 2.500."},
                            {"value": "c", "label": "R$ 3.250."},
                            {"value": "d", "label": "R$ 3.000."},
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Correto! 12 × 250 = R$ 3.000."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. O custo total é a parcela "
                            "multiplicada pelo número de parcelas: "
                            "12 × 250 = R$ 3.000."
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
                            "O mesmo notebook custa R$ 2.400 à vista ou 12x de "
                            "R$ 250. Quanto o parcelamento custa a mais?"
                        ),
                        "competency_codes": ["4.2.2"],
                        "options": [
                            {"value": "a", "label": "R$ 250."},
                            {"value": "b", "label": "R$ 400."},
                            {"value": "c", "label": "R$ 600."},
                            {"value": "d", "label": "R$ 3.000."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! O parcelado custa 12 × 250 = R$ 3.000, e o "
                            "à vista custa R$ 2.400. A diferença é R$ 600, o "
                            "custo do crédito."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Calcule o total parcelado "
                            "(12 × 250 = R$ 3.000) e subtraia o preço à vista "
                            "(R$ 2.400): a diferença é R$ 600."
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
                            "A Ana diz: \"A parcela de R$ 190 cabe no meu "
                            "orçamento, então a compra vale a pena.\" Qual é a "
                            "melhor resposta?"
                        ),
                        "competency_codes": ["4.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Está certa: se a parcela cabe no "
                                    "orçamento, a compra sempre vale a pena."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Caber no orçamento é só uma parte: é "
                                    "preciso comparar o total pago com o preço à "
                                    "vista e ver se a parcela compromete os "
                                    "meses seguintes."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Está errada: parcelar nunca compensa.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não importa o valor total, só o número de "
                                    "parcelas."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Muito bem! Caber no orçamento é necessário, mas não "
                            "basta. É preciso olhar o custo total, a diferença "
                            "para o preço à vista e o impacto nos meses "
                            "seguintes."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Caber no orçamento é só parte da "
                            "análise. É preciso comparar o custo total com o "
                            "preço à vista e ver o impacto da parcela nos meses "
                            "seguintes."
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
                            "Você já viu uma oferta do tipo \"parcela que cabe "
                            "no bolso\"? Como você avaliaria se ela compensa?"
                        ),
                        "competency_codes": ["4.2.1", "4.2.2", "4.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Calcula o custo total multiplicando a parcela "
                                "pelo número de parcelas."
                            ),
                            (
                                "Compara o total parcelado com o preço à vista."
                            ),
                            (
                                "Considera o impacto da parcela nos meses "
                                "seguintes ou no orçamento."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O valor da parcela não é o preço da compra",
                    "order": 1,
                    "body": md(
                        """
                        Para saber quanto uma compra parcelada realmente custa:

                        **custo total = valor da parcela × número de parcelas**

                        Depois, compare com o **preço à vista**. A diferença entre
                        os dois é o **custo do crédito**: o que você paga a mais
                        por ter pago depois.

                        "Cabe no bolso" é só uma parte da análise. As perguntas
                        mais importantes são: **qual é o valor total?** e **vale a
                        pena pagar essa diferença?** Além disso, cada parcela
                        compromete a renda dos meses seguintes, reduzindo o que
                        sobra para essenciais, metas e imprevistos.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O celular da Ana",
                    "order": 2,
                    "body": md(
                        """
                        Um celular custa **R$ 1.500 à vista** ou **10x de
                        R$ 190**.

                        - Custo total parcelado: 10 × 190 = **R$ 1.900**
                        - Diferença: 1.900 − 1.500 = **R$ 400** a mais
                        - Em proporção: 400 ÷ 1.500 ≈ 26,7% a mais que o preço à
                          vista.

                        A parcela de R$ 190 parece leve, mas a Ana pagaria R$ 400
                        a mais por parcelar.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Duas perguntas antes de parcelar",
                    "order": 3,
                    "body": md(
                        """
                        Pergunte sempre: "qual é o valor total?" e "tem desconto
                        à vista?". Em financiamentos e empréstimos, peça também o
                        **CET (Custo Efetivo Total)**, que reúne os juros e as
                        tarifas em um só número e facilita a comparação.
                        """
                    ),
                },
            ],
        },
        {
            "number": 3,
            "name": "O que acontece quando a dívida cresce?",
            "description": (
                "Entenda como atraso e pagamento mínimo fazem a dívida crescer "
                "e escolha estratégias para sair dela."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "4.3.1",
                    "name": "Explicar como a dívida cresce",
                    "description": (
                        "Relaciona atraso, multa, juros e pagamento mínimo ao "
                        "aumento do saldo devedor."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "4.3.2",
                    "name": "Reconhecer o teto de juros do rotativo",
                    "description": (
                        "Sabe que juros e encargos do rotativo são limitados a "
                        "100% do valor original e que a dívida continua cara."
                    ),
                    "is_essential": False,
                },
                {
                    "code": "4.3.3",
                    "name": "Escolher uma estratégia para sair da dívida",
                    "description": (
                        "Prioriza dívidas com juros mais altos, negocia com o "
                        "credor e evita novas dívidas."
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
                            "O que acontece com o saldo restante quando você "
                            "paga só o mínimo da fatura do cartão?"
                        ),
                        "competency_codes": ["4.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "É perdoado pelo banco.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "É financiado com juros, e a dívida continua "
                                    "crescendo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Fica congelado, sem custo, por um ano."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "É descontado automaticamente do seu "
                                    "salário."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O que não foi pago é financiado com juros, "
                            "e a dívida continua crescendo enquanto não for "
                            "quitada."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O saldo que sobra depois do "
                            "pagamento mínimo é financiado com juros, e a dívida "
                            "continua crescendo. Não há perdão nem congelamento "
                            "sem custo."
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
                            "Pela regra legal em vigor, até quanto a soma de "
                            "juros e encargos do rotativo do cartão pode chegar, "
                            "em relação ao valor original da dívida?"
                        ),
                        "competency_codes": ["4.3.2"],
                        "options": [
                            {"value": "a", "label": "10%."},
                            {"value": "b", "label": "50%."},
                            {"value": "c", "label": "Não há limite."},
                            {"value": "d", "label": "100%."},
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Correto! O teto é de 100% do valor original. Uma "
                            "dívida de R$ 1.000 pode chegar a, no máximo, "
                            "R$ 2.000 por efeito de juros e encargos. Mesmo "
                            "assim, dobrar a dívida continua sendo muito caro."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. A lei limita juros e encargos do "
                            "rotativo a 100% do valor original da dívida. O teto "
                            "ajuda, mas ainda permite que a dívida dobre, o que é "
                            "muito caro."
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
                            "Você tem duas dívidas: R$ 400 no rotativo do cartão "
                            "(com juros altos) e R$ 400 com um parente (sem "
                            "juros). Este mês só dá para pagar R$ 400. Qual é a "
                            "escolha mais eficiente?"
                        ),
                        "competency_codes": ["4.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar o parente primeiro, porque é mais "
                                    "educado."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Dividir os R$ 400 igualmente entre as duas "
                                    "dívidas."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não pagar nenhuma e esperar o mês seguinte."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pagar a dívida do cartão primeiro e "
                                    "combinar um prazo com o parente."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Muito bem! A dívida com juros altos cresce mais "
                            "rápido, então ela deve ser a prioridade. Combinar um "
                            "prazo com o parente evita o desgaste e não gera "
                            "juros."
                        ),
                        "feedback_incorrect": (
                            "Revise a estratégia. A dívida com juros mais altos "
                            "é a que mais cresce, então deve ser paga primeiro. A "
                            "dívida sem juros pode ser negociada com mais calma."
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
                            "Imagine que um amigo está com a fatura do cartão "
                            "atrasada. Que 3 conselhos você daria a ele para sair "
                            "dessa situação?"
                        ),
                        "competency_codes": ["4.3.1", "4.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Sugere procurar o credor para negociar."
                            ),
                            (
                                "Recomenda listar as dívidas ou priorizar a de "
                                "juros mais altos."
                            ),
                            (
                                "Recomenda evitar novas dívidas ou evitar pagar "
                                "só o mínimo."
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
                        "prompt": "Qual proposta de crédito você escolhe?",
                        "scenario": (
                            "Você precisa de R$ 2.000 para consertar o notebook "
                            "que usa no trabalho. Três propostas fictícias de "
                            "crédito chegaram. Proposta A: 10 parcelas de "
                            "R$ 230. Proposta B: 12 parcelas de R$ 215. Proposta "
                            "C: 5 parcelas de R$ 450. Depois das despesas "
                            "essenciais e da sua meta, sua folga mensal é de "
                            "R$ 400. Qual proposta você escolhe?"
                        ),
                        "competency_codes": ["4.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Proposta C, porque tem o menor valor total "
                                    "(R$ 2.250)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Proposta A: o total (R$ 2.300) é o menor "
                                    "entre as que cabem na minha folga de "
                                    "R$ 400."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Proposta B, porque tem a menor parcela "
                                    "(R$ 215)."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Nenhuma delas; uso o rotativo do cartão, "
                                    "porque assim não preciso decidir agora."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! Os totais são: A = R$ 2.300, B = "
                            "R$ 2.580 e C = R$ 2.250. A proposta C é a mais "
                            "barata, mas a parcela de R$ 450 passa da sua folga "
                            "de R$ 400 e levaria a atrasos. Entre as que cabem, a "
                            "A é a que custa menos no total."
                        ),
                        "feedback_incorrect": (
                            "Revise a comparação. Calcule o total de cada "
                            "proposta (A: 10 × 230 = R$ 2.300; B: 12 × 215 = "
                            "R$ 2.580; C: 5 × 450 = R$ 2.250) e verifique se a "
                            "parcela cabe na folga de R$ 400. A C não cabe; entre "
                            "A e B, a A custa menos no total. O rotativo do "
                            "cartão costuma ser uma das dívidas mais caras."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Atraso, pagamento mínimo e bola de neve",
                    "order": 1,
                    "body": md(
                        """
                        Quando você **atrasa** uma conta, em geral paga multa e
                        juros de atraso, e pode ter o nome negativado. Quando você
                        paga **só o mínimo da fatura do cartão**, o restante é
                        financiado com juros (no rotativo ou no parcelamento da
                        fatura). Como os juros são compostos, a dívida cresce cada
                        vez mais rápido.

                        Desde 2024, uma lei limita a soma de **juros e encargos**
                        do rotativo e do parcelamento da fatura a **100% do valor
                        original** da dívida. Ou seja, uma dívida de R$ 1.000 pode
                        chegar, no máximo, a R$ 2.000 por efeito de juros e
                        encargos. O teto protege, mas **dobrar a dívida continua
                        sendo muito caro**.

                        Para sair de uma dívida:

                        1. **Liste** todas as dívidas, com valor e juros.
                        2. **Priorize** a dívida de juros mais altos.
                        3. **Negocie** com o credor, mostrando quanto você
                           consegue pagar.
                        4. **Evite novas dívidas** enquanto estiver quitando as
                           atuais.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A bola de neve",
                    "order": 2,
                    "body": md(
                        """
                        Imagine uma dívida de R$ 1.000 com juros de 10% ao mês
                        (taxa fictícia, só para ilustrar), sem nenhum pagamento:

                        - Mês 1: R$ 1.100
                        - Mês 2: R$ 1.210
                        - Mês 3: R$ 1.331

                        Em 3 meses, a dívida cresceu R$ 331 sem que nenhuma compra
                        nova tivesse sido feita. Quanto mais tempo passa, mais
                        rápido ela cresce.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Negocie antes de atrasar",
                    "order": 3,
                    "body": md(
                        """
                        Se você percebeu que não vai conseguir pagar, procure o
                        credor **antes** do vencimento. Mostrar quanto você
                        consegue pagar por mês costuma abrir mais opções de acordo
                        do que esperar a dívida crescer.
                        """
                    ),
                },
            ],
        },
    ],
}
