"""Conteúdo versionado da Trilha 9 — Inflação e poder de compra.

phase_number: 9 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-09.md

Valores de inflação nos exemplos são hipotéticos. IPCA real deve ser
consultado no IBGE antes de publicar atualizações.
"""

TRAIL_9_V1 = {
    "phase_number": 9,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 9.1 — O que é inflação?
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "O que é inflação?",
            "description": (
                "Entenda o que é inflação, como o IPCA mede a variação de preços "
                "e por que a inflação que você sente pode diferir do índice oficial."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "9.1.1",
                    "name": "Explicar o que é inflação e como o IPCA mede",
                    "description": (
                        "Descreve inflação como elevação geral dos preços e o IPCA "
                        "como índice calculado pelo IBGE sobre uma cesta de consumo."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "9.1.2",
                    "name": "Calcular o reajuste de um preço pela inflação",
                    "description": (
                        "Aplica a variação percentual do IPCA para calcular o novo "
                        "preço de um produto após a inflação."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "9.1.3",
                    "name": "Distinguir inflação oficial e inflação percebida",
                    "description": (
                        "Explica por que a inflação sentida por cada família pode "
                        "diferir do IPCA agregado."
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
                        "prompt": "O IPCA é calculado por qual instituição?",
                        "competency_codes": ["9.1.1"],
                        "options": [
                            {"value": "a", "label": "Banco Central do Brasil."},
                            {"value": "b", "label": "IBGE (Instituto Brasileiro de Geografia e Estatística)."},
                            {"value": "c", "label": "Receita Federal."},
                            {"value": "d", "label": "Ministério da Economia."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O IPCA é calculado pelo IBGE, que pesquisa os preços "
                            "em uma cesta de produtos e serviços consumidos por famílias "
                            "de renda de 1 a 40 salários mínimos nas principais cidades."
                        ),
                        "feedback_incorrect": (
                            "O IPCA é calculado pelo IBGE (Instituto Brasileiro de "
                            "Geografia e Estatística). O Banco Central usa o IPCA como "
                            "referência para a política monetária, mas não o calcula."
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
                            "Um produto custava R$ 50,00. A inflação acumulada no "
                            "período foi de 6%. Qual é o novo preço? "
                            "(Valor hipotético.)"
                        ),
                        "competency_codes": ["9.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 53,00."},
                            {"value": "b", "label": "R$ 56,00."},
                            {"value": "c", "label": "R$ 50,60."},
                            {"value": "d", "label": "R$ 56,30."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Novo preço = 50 × (1 + 0,06) = 50 × 1,06 = R$ 53,00. "
                            "Um aumento de 6% sobre R$ 50 é R$ 3, totalizando R$ 53."
                        ),
                        "feedback_incorrect": (
                            "Novo preço = preço original × (1 + taxa). "
                            "50 × 1,06 = R$ 53,00. "
                            "A inflação de 6% representa R$ 3 de aumento sobre R$ 50."
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
                            "Qual é a diferença entre inflação oficial e inflação percebida?"
                        ),
                        "competency_codes": ["9.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Não há diferença — o IPCA mede exatamente o que cada "
                                    "família paga."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "O IPCA mede a variação média de uma cesta ampla. "
                                    "Cada família sente a inflação de acordo com seu "
                                    "padrão de consumo específico."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "A inflação percebida é sempre maior do que o IPCA.",
                            },
                            {
                                "value": "d",
                                "label": "A inflação percebida é uma opinião, sem base factual.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O IPCA é uma média de uma cesta com muitos produtos. "
                            "Uma família que gasta mais em alimentação sentirá mais a "
                            "inflação em períodos de alta nos alimentos — mesmo que o IPCA "
                            "geral suba pouco por conta de outros itens."
                        ),
                        "feedback_incorrect": (
                            "O IPCA é uma média de variação de preços em uma cesta ampla. "
                            "Como cada família tem um padrão diferente de consumo, a "
                            "inflação que ela sente pode ser maior ou menor que o índice."
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
                            "Por que a inflação de uma família pode ser diferente do IPCA oficial?"
                        ),
                        "competency_codes": ["9.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Porque o IPCA usa uma cesta de consumo média; "
                                    "uma família que gasta mais em transporte, por exemplo, "
                                    "sente mais o impacto quando combustíveis sobem."
                                ),
                            },
                            {"value": "b", "label": "Porque o IBGE erra o cálculo com frequência."},
                            {"value": "c", "label": "Porque a inflação de cada cidade é a mesma."},
                            {"value": "d", "label": "Porque o IPCA mede apenas alimentos."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! A cesta do IPCA é uma média. Famílias com padrão "
                            "diferente (mais gastos em saúde, educação ou transporte) "
                            "sentem de forma distinta as variações em cada categoria."
                        ),
                        "feedback_incorrect": (
                            "O IPCA é calculado corretamente, mas sobre uma cesta média. "
                            "Famílias têm padrões de consumo diferentes, então cada uma "
                            "tem uma 'inflação pessoal' que pode ser maior ou menor "
                            "do que o índice agregado."
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
                            "O IPCA acumulado no ano foi de 5% (hipotético). "
                            "Um produto de R$ 100 em janeiro deve custar quanto em dezembro?"
                        ),
                        "competency_codes": ["9.1.2"],
                        "options": [
                            {"value": "a", "label": "R$ 105,00."},
                            {"value": "b", "label": "R$ 100,50."},
                            {"value": "c", "label": "R$ 110,00."},
                            {"value": "d", "label": "R$ 100,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 100 × 1,05 = R$ 105,00. "
                            "Com inflação de 5% no ano, o produto custa R$ 5 a mais — "
                            "5% de R$ 100."
                        ),
                        "feedback_incorrect": (
                            "Novo preço = 100 × (1 + 0,05) = R$ 105,00. "
                            "A inflação acumulada de 5% representa R$ 5 de aumento "
                            "sobre o preço original de R$ 100."
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
                            "Descreva o que é inflação usando um exemplo de produto "
                            "do dia a dia. Em seguida, explique por que o IPCA oficial "
                            "pode não refletir exatamente a inflação que uma família "
                            "específica sente no mês."
                        ),
                        "competency_codes": ["9.1.1", "9.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Pontos esperados: definição de inflação como aumento "
                            "geral e contínuo dos preços; exemplo concreto (como pão, "
                            "aluguel ou gasolina); explicação de que o IPCA é uma média "
                            "e cada família tem um padrão de consumo diferente."
                        ),
                        "evaluation_criteria": [
                            "Define inflação como elevação geral de preços.",
                            "Usa um exemplo concreto de produto ou serviço.",
                            "Explica que o IPCA é uma média e famílias têm cestas diferentes.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é inflação e por que preços sobem",
                    "order": 1,
                    "body": (
                        "**Inflação** é o aumento generalizado e contínuo dos preços "
                        "de bens e serviços ao longo do tempo. Quando há inflação, "
                        "o mesmo dinheiro compra menos do que antes.\n\n"
                        "Os preços sobem por diferentes razões:\n"
                        "- **Demanda alta:** mais pessoas querendo o mesmo produto\n"
                        "- **Custos de produção maiores:** insumos, energia, transporte\n"
                        "- **Emissão de moeda:** mais dinheiro circulando sem aumento "
                        "proporcional de produção\n\n"
                        "Uma inflação pequena e estável é considerada normal em "
                        "economias saudáveis. O problema é quando ela é alta ou "
                        "imprevisível — corrói o poder de compra das pessoas."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O IPCA: o que mede, quem calcula e como consultar",
                    "order": 2,
                    "body": (
                        "O **IPCA (Índice Nacional de Preços ao Consumidor Amplo)** é "
                        "o indicador oficial de inflação no Brasil.\n\n"
                        "- **Quem calcula:** IBGE (Instituto Brasileiro de Geografia "
                        "e Estatística)\n"
                        "- **O que mede:** variação de preços de uma cesta de produtos "
                        "e serviços para famílias com renda de 1 a 40 salários mínimos "
                        "nas principais regiões metropolitanas\n"
                        "- **Frequência:** divulgado mensalmente\n"
                        "- **Como consultar:** site do IBGE (ibge.gov.br)\n\n"
                        "O IPCA é usado como meta de inflação pelo Banco Central e "
                        "como indexador de contratos, reajustes de salário mínimo e "
                        "títulos do Tesouro (Tesouro IPCA+)."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Cesta de compras: antes e depois da inflação",
                    "order": 3,
                    "body": (
                        "**Cesta fictícia da Ana em janeiro:**\n\n"
                        "| Item | Preço | Com 6% de inflação anual (hipotético) |\n"
                        "|---|---|---|\n"
                        "| Pão (kg) | R$ 12,00 | R$ 12,72 |\n"
                        "| Aluguel | R$ 800,00 | R$ 848,00 |\n"
                        "| Transporte (mês) | R$ 200,00 | R$ 212,00 |\n"
                        "| **Total** | **R$ 1.012,00** | **R$ 1.072,72** |\n\n"
                        "Com inflação de 6%, Ana precisa de R$ 60,72 a mais por mês "
                        "para manter o mesmo padrão de consumo.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Inflação percebida vs. IPCA oficial",
                    "order": 4,
                    "body": (
                        "O IPCA é uma **média de uma cesta ampla**. Cada família "
                        "tem um padrão de consumo diferente — e por isso cada uma "
                        "sente a inflação de forma distinta.\n\n"
                        "**Exemplos:**\n"
                        "- Uma família que vai de carro sente mais quando a gasolina sobe\n"
                        "- Uma família com criança sente mais quando materiais escolares "
                        "e plano de saúde sobem\n"
                        "- Um aposentado que gasta muito em saúde sente mais quando "
                        "remédios ficam mais caros\n\n"
                        "Isso não significa que o IPCA está errado — apenas que é uma "
                        "média. A inflação que você sente é a sua 'inflação pessoal'."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como consultar o IPCA acumulado",
                    "order": 5,
                    "body": (
                        "O IPCA acumulado (anual, semestral ou mensal) está disponível "
                        "no site do IBGE: **ibge.gov.br → IPCA**.\n\n"
                        "Para comparar o rendimento de um investimento com a inflação, "
                        "você precisa do IPCA acumulado no mesmo período do investimento.\n\n"
                        "Valores mudam todo mês — consulte sempre a fonte atualizada."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Deflação: quando os preços caem",
                    "order": 6,
                    "body": (
                        "**Deflação** é o fenômeno oposto: os preços caem ao longo do tempo.\n\n"
                        "Parece bom, mas deflação persistente pode ser um sinal "
                        "de economia fraca: as pessoas e empresas adiam compras "
                        "esperando preços menores, o que reduz a produção e o emprego.\n\n"
                        "No Brasil, deflações pontuais acontecem em períodos específicos "
                        "(quedas de energia, por exemplo), mas não são a regra histórica."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "IPCA vs. INPC: qual a diferença?",
                    "order": 7,
                    "body": (
                        "| Índice | Público-alvo | Uso principal |\n"
                        "|---|---|---|\n"
                        "| IPCA | Famílias de 1 a 40 SM | Meta de inflação, contratos, investimentos |\n"
                        "| INPC | Famílias de 1 a 5 SM | Reajuste do salário mínimo e benefícios |\n\n"
                        "Para o trabalhador de baixa renda, o INPC pode ser mais "
                        "representativo da sua inflação real, pois a cesta é mais "
                        "focada em alimentação e serviços básicos.\n\n"
                        "Ambos são calculados pelo IBGE."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois perfis com inflações diferentes",
                    "order": 8,
                    "body": (
                        "**IPCA hipotético do período: 5%**\n\n"
                        "**Família A** (com criança em escola particular):\n"
                        "- Educação subiu 12% no período\n"
                        "- Educação representa 30% do orçamento\n"
                        "- Inflação pessoal estimada: acima de 5%\n\n"
                        "**Família B** (aposentado sem filhos):\n"
                        "- Educação não consome nada do orçamento\n"
                        "- Gastos concentrados em saúde e alimentação\n"
                        "- Depende da variação nesses setores\n\n"
                        "Mesma economia, inflações diferentes para cada família.\n\n"
                        "*(Valores hipotéticos, para fins didáticos.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 9.2 — Rendimento real
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Rendimento real",
            "description": (
                "Calcule o rendimento real de um investimento usando a fórmula "
                "de Fisher e identifique quando um rendimento perde para a inflação."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "9.2.1",
                    "name": "Calcular rendimento real pela fórmula de Fisher",
                    "description": (
                        "Aplica (1+r_real) = (1+r_nominal)/(1+inflação) − 1 para "
                        "calcular o rendimento real de um investimento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "9.2.2",
                    "name": "Identificar quando rendimento nominal perde para a inflação",
                    "description": (
                        "Reconhece quando o rendimento nominal é menor que a inflação "
                        "e o que isso significa para o poder de compra."
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
                            "Rendimento nominal de 7% ao ano e inflação de 4% ao ano "
                            "(hipotéticos). Qual é o rendimento real aproximado "
                            "(cálculo simplificado)?"
                        ),
                        "competency_codes": ["9.2.1"],
                        "options": [
                            {"value": "a", "label": "≈ 3%."},
                            {"value": "b", "label": "≈ 11%."},
                            {"value": "c", "label": "≈ 1,75%."},
                            {"value": "d", "label": "= 7%."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Aproximação simples: 7% − 4% ≈ 3%. "
                            "Pela fórmula exata: (1,07/1,04) − 1 ≈ 2,88%. "
                            "O rendimento real é o ganho efetivo de poder de compra."
                        ),
                        "feedback_incorrect": (
                            "Rendimento real ≈ rendimento nominal − inflação = 7% − 4% = 3%. "
                            "Para precisão: usar a fórmula de Fisher: (1+0,07)/(1+0,04)−1 ≈ 2,88%."
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
                            "Uma aplicação rende 6% ao ano (nominal). A inflação no "
                            "período foi 7% (hipotéticos). O investidor ganhou ou "
                            "perdeu poder de compra?"
                        ),
                        "competency_codes": ["9.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Perdeu — o rendimento nominal (6%) foi menor do que "
                                    "a inflação (7%), então o poder de compra diminuiu."
                                ),
                            },
                            {"value": "b", "label": "Ganhou — recebeu 6% de rendimento."},
                            {"value": "c", "label": "Ficou igual — inflação e rendimento se cancelam."},
                            {"value": "d", "label": "Ganhou, porque a poupança é segura."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Quando o rendimento nominal é menor que a inflação, "
                            "o rendimento real é negativo — você perdeu poder de compra. "
                            "Ter mais dinheiro não significa comprar mais."
                        ),
                        "feedback_incorrect": (
                            "Rendimento real = (1,06/1,07) − 1 ≈ −0,93%. "
                            "O saldo cresceu nominalmente (6%), mas os preços "
                            "subiram mais (7%). Com o dinheiro rendido, você compra "
                            "menos do que comprava antes."
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
                            "Usando a fórmula exata de Fisher: "
                            "(1 + 0,08) / (1 + 0,05) − 1 = ? "
                            "(Valores hipotéticos.)"
                        ),
                        "competency_codes": ["9.2.1"],
                        "options": [
                            {"value": "a", "label": "≈ 2,86%."},
                            {"value": "b", "label": "= 3%."},
                            {"value": "c", "label": "= 13%."},
                            {"value": "d", "label": "≈ 1,6%."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 1,08 / 1,05 = 1,02857... → − 1 = 0,02857 ≈ 2,86%. "
                            "A fórmula exata dá 2,86%, não 3% (8%−5%). "
                            "A diferença parece pequena, mas importa em prazos longos."
                        ),
                        "feedback_incorrect": (
                            "1,08 ÷ 1,05 = 1,02857 → rendimento real = 2,86%. "
                            "A subtração simples (8%−5%=3%) é uma aproximação. "
                            "A fórmula de Fisher dá o valor exato."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que significa rentabilidade real negativa?",
                        "competency_codes": ["9.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O investimento rendeu menos do que a inflação: "
                                    "você tem mais dinheiro, mas pode comprar menos do que antes."
                                ),
                            },
                            {"value": "b", "label": "O investimento perdeu dinheiro nominal."},
                            {"value": "c", "label": "O rendimento foi zero."},
                            {"value": "d", "label": "O investimento cobrou taxa de custódia."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Rentabilidade real negativa significa que o rendimento "
                            "nominal foi menor que a inflação. O saldo cresceu em reais, "
                            "mas compra menos — o poder de compra diminuiu."
                        ),
                        "feedback_incorrect": (
                            "Real negativo ≠ nominal negativo. Você pode ter mais reais "
                            "do que antes (rendimento nominal positivo) mas ainda assim "
                            "perder poder de compra se a inflação subiu mais do que seu "
                            "investimento rendeu."
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
                            "Uma poupança fictícia rende 6% ao ano em um período com "
                            "inflação de 5% ao ano (valores hipotéticos).\n\n"
                            "1. Calcule o rendimento real usando a fórmula de Fisher.\n"
                            "2. O que esse resultado significa para o poder de compra "
                            "de quem investiu R$ 10.000?"
                        ),
                        "competency_codes": ["9.2.1", "9.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Rendimento real = (1,06/1,05) − 1 ≈ 0,95%\n"
                            "R$ 10.000 × 1,06 = R$ 10.600 (nominal)\n"
                            "Para manter o poder de compra com 5% de inflação: "
                            "10.000 × 1,05 = R$ 10.500\n"
                            "Ganho real ≈ R$ 100 — o investidor compra um pouco mais "
                            "do que antes, mas muito menos do que os R$ 600 nominais "
                            "sugerem."
                        ),
                        "evaluation_criteria": [
                            "Aplica a fórmula de Fisher corretamente: (1,06/1,05)−1.",
                            "Calcula o ganho real em reais sobre os R$ 10.000.",
                            "Distingue rendimento nominal de rendimento real.",
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
                            "Carlos deixou R$ 10.000 numa aplicação que rendeu 3% "
                            "no ano, mas a inflação foi 6% (hipotéticos). "
                            "Quanto perdeu aproximadamente em poder de compra?"
                        ),
                        "competency_codes": ["9.2.2"],
                        "options": [
                            {"value": "a", "label": "≈ R$ 291 de poder de compra."},
                            {"value": "b", "label": "Nada — teve R$ 300 de rendimento."},
                            {"value": "c", "label": "R$ 600 exatos."},
                            {"value": "d", "label": "R$ 300."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Para manter o poder de compra com 6% de inflação: "
                            "10.000 × 1,06 = R$ 10.600. O saldo real foi 10.000 × 1,03 = "
                            "R$ 10.300. Diferença: R$ 300 — mas em poder de compra real, "
                            "a perda é: (1,03/1,06)−1 ≈ −2,83% → ≈ R$ 283−291 de poder "
                            "de compra perdido."
                        ),
                        "feedback_incorrect": (
                            "Para manter o poder de compra: 10.000 × 1,06 = R$ 10.600. "
                            "Carlos teve R$ 10.300 — R$ 300 a menos do que precisaria. "
                            "O rendimento nominal foi positivo, mas o real foi negativo."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Rendimento nominal vs. rendimento real",
                    "order": 1,
                    "body": (
                        "**Rendimento nominal:** o percentual que o investimento rende "
                        "em moeda corrente, sem descontar a inflação. É o número que "
                        "o banco mostra.\n\n"
                        "**Rendimento real:** o ganho efetivo de poder de compra — "
                        "o quanto a mais você consegue comprar depois do investimento "
                        "em comparação com o começo.\n\n"
                        "Ter mais dinheiro não significa necessariamente ter mais poder "
                        "de compra: se a inflação subiu mais do que o rendimento, "
                        "você tem mais reais, mas pode comprar menos."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "A fórmula de Fisher: como calcular o rendimento real",
                    "order": 2,
                    "body": (
                        "A fórmula exata para calcular o rendimento real:\n\n"
                        "**(1 + r_real) = (1 + r_nominal) ÷ (1 + inflação)**\n\n"
                        "Ou: **r_real = (1 + r_nominal) / (1 + inflação) − 1**\n\n"
                        "**Exemplo fictício:**\n"
                        "- Rendimento nominal: 8%/ano (r_nominal = 0,08)\n"
                        "- Inflação: 5%/ano (inflação = 0,05)\n"
                        "- r_real = (1,08 / 1,05) − 1 ≈ 0,0286 = **2,86%**\n\n"
                        "**Aproximação simples:** r_real ≈ r_nominal − inflação\n"
                        "- 8% − 5% = 3% (próximo, mas não exato)\n\n"
                        "Use a fórmula exata quando precisão for importante."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Poupança vs. inflação: três cenários hipotéticos",
                    "order": 3,
                    "body": (
                        "**R$ 10.000 investidos por 1 ano (todos hipotéticos)**\n\n"
                        "| Cenário | Rend. nominal | Inflação | Rend. real | Poder de compra |\n"
                        "|---|---|---|---|---|\n"
                        "| A | 6%/ano | 4%/ano | ≈ 1,9% | Ganhou |\n"
                        "| B | 5%/ano | 5%/ano | ≈ 0% | Manteve |\n"
                        "| C | 3%/ano | 6%/ano | ≈ -2,8% | Perdeu |\n\n"
                        "No cenário C, o saldo vai de R$ 10.000 para R$ 10.300, "
                        "mas o investidor perdeu poder de compra — "
                        "porque os preços subiram mais do que o dinheiro rendeu.\n\n"
                        "*(Valores hipotéticos, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Sempre compare pelo rendimento real",
                    "order": 4,
                    "body": (
                        "Ao avaliar um investimento, pergunte: **o rendimento supera "
                        "a inflação do período?**\n\n"
                        "Se a resposta for não, você está perdendo poder de compra "
                        "mesmo tendo mais dinheiro na conta.\n\n"
                        "Para comparar, consulte:\n"
                        "- Rendimento do investimento: extrato da aplicação\n"
                        "- Inflação do período: IPCA no site do IBGE"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Rendimento real negativo: quando guardar empobrece",
                    "order": 5,
                    "body": (
                        "Se o rendimento nominal for menor que a inflação, o "
                        "rendimento real é **negativo**. Isso acontece quando:\n\n"
                        "- O dinheiro fica em conta corrente sem rendimento\n"
                        "- A poupança rende menos que o IPCA\n"
                        "- O investimento tem taxa muito baixa em período de inflação alta\n\n"
                        "Guardar dinheiro sem rendimento é diferente de perder dinheiro "
                        "nominalmente — mas o efeito prático é o mesmo: "
                        "cada dia que passa, aquele dinheiro compra menos."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O dinheiro no 'colchão': o custo invisível",
                    "order": 6,
                    "body": (
                        "R$ 5.000 guardados em espécie por 1 ano com inflação de 5% "
                        "(hipotético):\n\n"
                        "- Valor nominal: R$ 5.000 (não muda)\n"
                        "- Poder de compra equivalente no fim do ano: R$ 4.762\n"
                        "- Perda de poder de compra: R$ 238\n\n"
                        "Guardar dinheiro sem rendimento não é 'neutro' — "
                        "é perda garantida quando há inflação.\n\n"
                        "*(Valor hipotético, para fins didáticos.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 9.3 — Inflação e decisões
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Inflação e decisões",
            "description": (
                "Aplique a inflação em reajustes de contratos e compare o poder "
                "de compra em momentos diferentes no tempo."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "9.3.1",
                    "name": "Aplicar o impacto da inflação a contratos e reajustes",
                    "description": (
                        "Calcula o novo valor de um contrato após reajuste pelo "
                        "índice acumulado no período."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "9.3.2",
                    "name": "Comparar poder de compra em dois momentos no tempo",
                    "description": (
                        "Calcula quanto um valor do passado equivale no presente "
                        "após a inflação acumulada."
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
                            "O aluguel da Ana é R$ 1.200 e será reajustado em 8% "
                            "pelo contrato (índice hipotético). Qual é o novo valor?"
                        ),
                        "competency_codes": ["9.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 1.296,00."},
                            {"value": "b", "label": "R$ 1.280,00."},
                            {"value": "c", "label": "R$ 1.208,00."},
                            {"value": "d", "label": "R$ 1.300,00."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! 1.200 × 1,08 = R$ 1.296. "
                            "O reajuste de 8% sobre R$ 1.200 é R$ 96, totalizando R$ 1.296."
                        ),
                        "feedback_incorrect": (
                            "Novo valor = 1.200 × (1 + 0,08) = 1.200 × 1,08 = R$ 1.296,00."
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
                            "R$ 10.000 guardados há 3 anos com inflação média de 5%/ano "
                            "(hipotética). Qual é o poder de compra equivalente hoje? "
                            "(1,05)^3 ≈ 1,1576."
                        ),
                        "competency_codes": ["9.3.2"],
                        "options": [
                            {"value": "a", "label": "≈ R$ 11.576 é o que valeria hoje."},
                            {"value": "b", "label": "R$ 10.000 — o dinheiro não muda."},
                            {"value": "c", "label": "R$ 11.500."},
                            {"value": "d", "label": "R$ 9.500."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Para ter o mesmo poder de compra de R$ 10.000 "
                            "de 3 anos atrás, você precisaria hoje de "
                            "10.000 × (1,05)^3 ≈ R$ 11.576. "
                            "Se seu dinheiro não cresceu esse valor, perdeu poder de compra."
                        ),
                        "feedback_incorrect": (
                            "Com inflação de 5%/ano por 3 anos (hipotético), R$ 10.000 "
                            "de então equivalem a 10.000 × (1,05)^3 ≈ R$ 11.576 hoje. "
                            "O dinheiro parado perde poder de compra."
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
                            "Qual é a desvantagem de manter dinheiro em conta corrente "
                            "sem rendimento num período de inflação de 5% ao ano?"
                        ),
                        "competency_codes": ["9.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O dinheiro perde poder de compra: no fim do ano, "
                                    "você compra menos com o mesmo valor."
                                ),
                            },
                            {"value": "b", "label": "O banco pode reter o dinheiro."},
                            {"value": "c", "label": "A conta corrente cobra juros sobre o saldo."},
                            {"value": "d", "label": "Nenhuma — conta corrente é sempre segura."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Com 5% de inflação, R$ 1.000 em conta corrente sem "
                            "rendimento valem aproximadamente R$ 952 em poder de compra "
                            "no fim do ano — uma perda real de R$ 48."
                        ),
                        "feedback_incorrect": (
                            "Conta corrente não paga rendimento (ou paga muito pouco). "
                            "Com inflação, o dinheiro parado perde poder de compra. "
                            "Não é uma perda nominal — o saldo continua R$ 1.000 — "
                            "mas é uma perda real."
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
                            "Explique por que poupar em uma aplicação que rende 3% ao "
                            "ano em um período com inflação de 6% ao ano pode ser pior "
                            "do que parece à primeira vista. "
                            "Use cálculos para ilustrar a resposta. (Valores hipotéticos.)"
                        ),
                        "competency_codes": ["9.3.1", "9.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Exemplo para R$ 10.000:\n"
                            "- Saldo após 1 ano: R$ 10.300 (nominal)\n"
                            "- Para manter poder de compra: 10.000 × 1,06 = R$ 10.600\n"
                            "- Perda de poder de compra: ≈ R$ 300\n"
                            "- Rendimento real ≈ (1,03/1,06) − 1 ≈ −2,83%\n\n"
                            "Ter R$ 10.300 parece bom, mas você precisaria de R$ 10.600 "
                            "para comprar o mesmo que comprava antes."
                        ),
                        "evaluation_criteria": [
                            "Calcula o saldo nominal correto (R$ 10.300 para R$ 10.000).",
                            "Calcula o valor necessário para manter poder de compra (R$ 10.600).",
                            "Conclui que o rendimento real é negativo.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Inflação em contratos: reajuste pelo índice",
                    "order": 1,
                    "body": (
                        "Muitos contratos incluem cláusulas de reajuste pelo índice "
                        "de inflação acumulado num período:\n\n"
                        "- **Aluguel residencial:** geralmente reajustado pelo IGPM, "
                        "IPCA ou outro índice acordado\n"
                        "- **Mensalidades escolares:** reajuste normalmente pelo IPCA "
                        "ou INPC do período\n"
                        "- **Planos de saúde:** regulados pela ANS, com índice próprio\n\n"
                        "**Como calcular:**\n"
                        "Novo valor = valor atual × (1 + índice acumulado)\n\n"
                        "Antes de renovar qualquer contrato, verifique qual índice "
                        "será usado e qual foi o acumulado no período."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Reajuste de aluguel pelo IGP-M",
                    "order": 2,
                    "body": (
                        "**Aluguel fictício: R$ 1.200/mês**\n"
                        "**IGP-M hipotético acumulado: 10%**\n\n"
                        "Novo aluguel = 1.200 × 1,10 = **R$ 1.320/mês**\n\n"
                        "Impacto anual: R$ 120/mês a mais × 12 = R$ 1.440 a mais por ano.\n\n"
                        "Se a renda de Ana cresceu apenas 5% no mesmo período, "
                        "o aluguel passou a representar uma fatia maior do seu orçamento.\n\n"
                        "*(Valores fictícios. IGP-M e IPCA variam — consulte sempre "
                        "o índice acordado no contrato.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Poder de compra: comparando momentos no tempo",
                    "order": 3,
                    "body": (
                        "Para comparar o poder de compra de um valor em dois momentos:\n\n"
                        "**Valor presente equivalente = valor passado × (1 + inflação)^anos**\n\n"
                        "**Exemplo hipotético:**\n"
                        "- R$ 10.000 guardados há 3 anos\n"
                        "- Inflação média: 5%/ano\n"
                        "- Equivalente hoje: 10.000 × (1,05)^3 ≈ R$ 11.576\n\n"
                        "Se o dinheiro ficou parado e não rendeu nada, você tem "
                        "R$ 10.000 — mas esses R$ 10.000 compram apenas o que "
                        "R$ 10.000 / 1,1576 ≈ R$ 8.638 compravam 3 anos atrás."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Dinheiro parado perde dinheiro real",
                    "order": 4,
                    "body": (
                        "Guardar dinheiro em conta corrente ou embaixo do colchão "
                        "não é uma decisão neutra. Em qualquer período com inflação "
                        "positiva, o poder de compra daquele dinheiro diminui.\n\n"
                        "A solução não é necessariamente investir em aplicações "
                        "complexas — mas sim garantir que o dinheiro guardado "
                        "renda pelo menos o equivalente à inflação."
                    ),
                },
            ],
        },
    ],
}
