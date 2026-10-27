"""Conteúdo versionado da Trilha 10 — Onde o dinheiro rende.

phase_number: 10 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-10.md

Valores de rentabilidade são hipotéticos. FGC: verificar limites vigentes.
"""

TRAIL_10_V1 = {
    "phase_number": 10,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 10.1 — Fundamentos
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Fundamentos do investimento",
            "description": (
                "Compreenda risco, liquidez e prazo — os três pilares que "
                "definem qualquer investimento."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "10.1.1",
                    "name": "Distinguir risco, liquidez e prazo em investimentos",
                    "description": (
                        "Define risco (possibilidade de perda), liquidez (facilidade "
                        "de resgate) e prazo e explica como se relacionam."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "10.1.2",
                    "name": "Classificar um investimento por perfil de risco",
                    "description": (
                        "Identifica se um investimento é conservador, moderado ou "
                        "arrojado com base nas características descritas."
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
                        "prompt": "O que é liquidez em um investimento?",
                        "competency_codes": ["10.1.1"],
                        "options": [
                            {"value": "a", "label": "A rentabilidade garantida."},
                            {
                                "value": "b",
                                "label": (
                                    "A facilidade e velocidade de transformar o investimento "
                                    "em dinheiro disponível sem perda significativa."
                                ),
                            },
                            {"value": "c", "label": "O prazo mínimo do investimento."},
                            {"value": "d", "label": "O risco de crédito da instituição."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Liquidez é a facilidade de resgatar o investimento "
                            "rapidamente e sem grandes perdas. Poupança e Tesouro Selic "
                            "têm alta liquidez; imóveis têm baixa liquidez."
                        ),
                        "feedback_incorrect": (
                            "Liquidez mede o quão fácil é converter o investimento em "
                            "dinheiro quando você precisar. Alta liquidez = resgate rápido "
                            "e sem perda significativa."
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
                            "Um CDB com carência de 1 ano tem maior ou menor liquidez "
                            "do que a poupança?"
                        ),
                        "competency_codes": ["10.1.1"],
                        "options": [
                            {"value": "a", "label": "Maior — CDB rende mais."},
                            {
                                "value": "b",
                                "label": (
                                    "Menor — a carência impede o resgate por 1 ano sem perda."
                                ),
                            },
                            {"value": "c", "label": "Igual — ambos são renda fixa."},
                            {"value": "d", "label": "Depende do banco."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Carência significa que você não pode resgatar "
                            "antes do prazo sem perda. CDB com carência de 1 ano tem "
                            "liquidez menor do que a poupança, que pode ser resgatada "
                            "a qualquer momento."
                        ),
                        "feedback_incorrect": (
                            "Liquidez não é o mesmo que rendimento. Com carência, "
                            "você não pode resgatar quando quiser — isso é baixa liquidez."
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
                            "Para a reserva de emergência, qual produto é mais adequado: "
                            "CDB com liquidez diária ou CDB com carência de 2 anos?"
                        ),
                        "competency_codes": ["10.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "CDB com liquidez diária — emergências exigem acesso "
                                    "imediato ao dinheiro."
                                ),
                            },
                            {"value": "b", "label": "CDB com carência de 2 anos — rende mais."},
                            {"value": "c", "label": "São equivalentes para reserva."},
                            {"value": "d", "label": "Nenhum — poupança é melhor."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A reserva de emergência precisa estar acessível "
                            "imediatamente. Um produto com carência, por maior rendimento "
                            "que tenha, não serve para emergência — você não pode resgatar "
                            "quando precisar."
                        ),
                        "feedback_incorrect": (
                            "Para reserva de emergência, liquidez é mais importante "
                            "do que rentabilidade. Se a emergência acontecer, você "
                            "precisa do dinheiro imediatamente — não em 2 anos."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é risco de crédito num investimento?",
                        "competency_codes": ["10.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A possibilidade de a instituição emissora não honrar "
                                    "o pagamento do principal ou dos juros."
                                ),
                            },
                            {"value": "b", "label": "A variação do rendimento ao longo do tempo."},
                            {"value": "c", "label": "O risco de perder dinheiro na Bolsa."},
                            {"value": "d", "label": "O risco de inflação superar o rendimento."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Risco de crédito é o risco de o emissor do título "
                            "(banco, empresa ou governo) não conseguir pagar o que deve. "
                            "O FGC existe justamente para mitigar esse risco em alguns "
                            "produtos bancários."
                        ),
                        "feedback_incorrect": (
                            "Risco de crédito é a possibilidade de o emissor não pagar. "
                            "Uma financeira pequena tem risco de crédito maior que um "
                            "grande banco, por exemplo."
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
                            "Explique com suas palavras a relação entre prazo, liquidez "
                            "e rendimento. Por que investimentos de maior prazo tendem "
                            "a oferecer mais rendimento?"
                        ),
                        "competency_codes": ["10.1.1"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Pontos esperados: maior prazo = menor liquidez; "
                            "quem aceita esperar mais tempo recebe uma compensação "
                            "em forma de juros maiores; o rendimento adicional é o "
                            "'prêmio pelo prazo'."
                        ),
                        "evaluation_criteria": [
                            "Explica que maior prazo implica menor liquidez.",
                            "Relaciona prazo maior com tendência de rendimento maior.",
                            "Menciona que o rendimento maior é uma compensação pelo tempo de espera.",
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
                            "Liquidez diária significa que você pode resgatar quando "
                            "quiser. Em qual situação isso é mais importante?"
                        ),
                        "competency_codes": ["10.1.1"],
                        "options": [
                            {"value": "a", "label": "Para objetivos de longo prazo."},
                            {
                                "value": "b",
                                "label": (
                                    "Para a reserva de emergência ou qualquer dinheiro "
                                    "que você pode precisar a qualquer momento."
                                ),
                            },
                            {"value": "c", "label": "Para maximizar o rendimento."},
                            {"value": "d", "label": "Para investimentos de risco moderado."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A liquidez diária é essencial para dinheiro que "
                            "pode ser necessário a qualquer momento — como a reserva "
                            "de emergência. Para objetivos de longo prazo, você pode "
                            "aceitar liquidez menor em troca de rendimento maior."
                        ),
                        "feedback_incorrect": (
                            "Liquidez diária importa quando você não pode prever "
                            "quando vai precisar do dinheiro. A reserva de emergência "
                            "é o exemplo mais claro."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Os três pilares de qualquer investimento",
                    "order": 1,
                    "body": (
                        "Todo investimento é analisado por três dimensões:\n\n"
                        "**1. Risco:** probabilidade de não receber o que foi prometido "
                        "(ou de perder parte do capital). Quanto maior o potencial de "
                        "ganho, geralmente maior o risco.\n\n"
                        "**2. Liquidez:** facilidade de transformar o investimento em "
                        "dinheiro disponível. Alta liquidez = resgate rápido e sem perda. "
                        "Baixa liquidez = dinheiro 'preso' por um prazo.\n\n"
                        "**3. Prazo:** por quanto tempo o dinheiro ficará investido. "
                        "Em geral, prazos maiores oferecem rendimentos maiores — "
                        "como compensação pela espera.\n\n"
                        "O **triângulo impossível:** não existe investimento com alto "
                        "rendimento, alta liquidez e baixo risco ao mesmo tempo. "
                        "Há sempre uma compensação."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Risco de crédito: quem pode não pagar",
                    "order": 2,
                    "body": (
                        "Em renda fixa, o principal risco é o **risco de crédito**: "
                        "a instituição emissora do título pode não ter condições de "
                        "pagar o que deve.\n\n"
                        "- **Tesouro Nacional (Governo Federal):** risco de crédito "
                        "considerado o menor do mercado doméstico.\n"
                        "- **Grandes bancos:** risco de crédito baixo, mas não zero.\n"
                        "- **Pequenas financeiras:** risco de crédito maior — "
                        "por isso oferecem taxas maiores.\n\n"
                        "Para proteger o investidor, o FGC (Fundo Garantidor de Créditos) "
                        "garante alguns produtos bancários dentro de certos limites."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A reserva de emergência precisa de alta liquidez",
                    "order": 3,
                    "body": (
                        "Para a reserva de emergência, a prioridade é **liquidez**, "
                        "não rendimento. O dinheiro precisa estar disponível imediatamente "
                        "quando uma emergência acontecer.\n\n"
                        "Produtos com liquidez diária e baixo risco são os mais adequados:\n"
                        "- CDB com liquidez diária\n"
                        "- Tesouro Selic\n"
                        "- Poupança (como opção de acesso fácil)\n\n"
                        "Para objetivos de longo prazo, você pode aceitar menos liquidez "
                        "em troca de rendimento maior."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "A relação entre risco, liquidez e prazo",
                    "order": 4,
                    "body": (
                        "| Característica | Impacto no rendimento |\n"
                        "|---|---|\n"
                        "| Risco alto | Tende a oferecer rendimento maior |\n"
                        "| Liquidez baixa | Tende a oferecer rendimento maior |\n"
                        "| Prazo longo | Tende a oferecer rendimento maior |\n\n"
                        "Isso não é uma regra absoluta — mas é o padrão geral. "
                        "Quando alguém oferece alto rendimento com baixo risco "
                        "e alta liquidez, é sinal de alerta: provavelmente há algo "
                        "que não está sendo dito."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 10.2 — Produtos de renda fixa
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Produtos de renda fixa",
            "description": (
                "Conheça as características de CDB, LCI, LCA, Tesouro Direto "
                "e poupança para comparar e escolher com fundamento."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "10.2.1",
                    "name": "Descrever características dos principais produtos de renda fixa",
                    "description": (
                        "Explica as características básicas de CDB, LCI, LCA, "
                        "Tesouro Direto e poupança."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "10.2.2",
                    "name": "Identificar vantagens e desvantagens de cada produto",
                    "description": (
                        "Compara produtos de renda fixa por liquidez, risco, "
                        "tributação e adequação para diferentes objetivos."
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
                        "prompt": "LCI tem qual vantagem tributária para pessoa física?",
                        "competency_codes": ["10.2.1"],
                        "options": [
                            {"value": "a", "label": "Isenção de IOF."},
                            {"value": "b", "label": "Isenção de Imposto de Renda sobre o rendimento."},
                            {"value": "c", "label": "Garantia de rentabilidade mínima."},
                            {"value": "d", "label": "Liquidez diária garantida."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! LCI (Letra de Crédito Imobiliário) e LCA "
                            "(Letra de Crédito do Agronegócio) são isentas de Imposto "
                            "de Renda para pessoa física. Por isso, mesmo com taxa "
                            "nominal menor, podem render mais no líquido."
                        ),
                        "feedback_incorrect": (
                            "A vantagem fiscal da LCI/LCA é a isenção de IR para "
                            "pessoa física. Isso significa que o rendimento declarado "
                            "já é o líquido — sem desconto de imposto."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O Tesouro Selic acompanha qual indicador?",
                        "competency_codes": ["10.2.1"],
                        "options": [
                            {"value": "a", "label": "IPCA."},
                            {"value": "b", "label": "Taxa Selic (taxa básica de juros definida pelo COPOM)."},
                            {"value": "c", "label": "CDI."},
                            {"value": "d", "label": "IGP-M."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O Tesouro Selic rende a taxa Selic acumulada "
                            "no período. É um dos produtos mais indicados para a "
                            "reserva de emergência: liquidez diária e baixo risco de "
                            "marcação a mercado."
                        ),
                        "feedback_incorrect": (
                            "O Tesouro Selic rende a taxa Selic — a taxa básica de "
                            "juros definida pelo COPOM. CDI e Selic são índices próximos, "
                            "mas distintos: CDBs geralmente são indexados ao CDI."
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
                            "Qual produto tem maior risco de crédito: CDB de grande "
                            "banco ou CDB de financeira pequena?"
                        ),
                        "competency_codes": ["10.2.2"],
                        "options": [
                            {"value": "a", "label": "CDB de grande banco — porque rende menos."},
                            {
                                "value": "b",
                                "label": (
                                    "CDB de financeira pequena — maior risco de a instituição "
                                    "não honrar o pagamento."
                                ),
                            },
                            {"value": "c", "label": "São iguais em risco de crédito."},
                            {"value": "d", "label": "Nenhum — o FGC cobre todos os CDBs sem limite."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Instituições menores têm maior risco de crédito — "
                            "por isso oferecem taxas mais altas para atrair investidores. "
                            "O FGC cobre até R$ 250 mil por CPF por IF, então o risco "
                            "acima desse limite permanece."
                        ),
                        "feedback_incorrect": (
                            "Financeiras menores têm risco de crédito maior e por isso "
                            "precisam oferecer taxas mais altas. O FGC mitiga parte do "
                            "risco dentro dos limites — mas não elimina completamente."
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
                            "Poupança é isenta de IR. Um CDB de 105% do CDI paga IR. "
                            "Com inflação alta, qual pode render mais no líquido?"
                        ),
                        "competency_codes": ["10.2.2"],
                        "options": [
                            {"value": "a", "label": "Sempre a poupança — isenção de IR."},
                            {
                                "value": "b",
                                "label": (
                                    "Depende da taxa. Com CDI alto, o CDB de 105% CDI pode "
                                    "render mais no líquido mesmo após o IR."
                                ),
                            },
                            {"value": "c", "label": "Sempre o CDB — taxa maior."},
                            {"value": "d", "label": "São sempre iguais."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A isenção de IR da poupança é uma vantagem, mas "
                            "quando o CDI está alto, o CDB de 105% CDI pode render "
                            "mais no líquido mesmo após o desconto do IR. "
                            "Compare sempre pelo rendimento líquido no período."
                        ),
                        "feedback_incorrect": (
                            "Isenção de IR não garante maior rendimento — o CDI (base "
                            "do CDB) pode render mais que a poupança mesmo após o IR. "
                            "Compare pelo rendimento líquido, não pelo bruto."
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
                            "Compare CDB e poupança para uma aplicação de R$ 3.000,00 "
                            "no prazo de 1 ano, considerando liquidez e tributação. "
                            "Use as informações conceituais aprendidas (sem valores "
                            "reais de taxa, pois variam)."
                        ),
                        "competency_codes": ["10.2.1", "10.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Comparação esperada: "
                            "Poupança: isenção de IR, liquidez alta, rendimento limitado. "
                            "CDB: sujeito a IR e IOF (< 30 dias), pode ter liquidez diária "
                            "ou com carência, rendimento depende do % do CDI. "
                            "Para 1 ano, CDB de boa financeira pode superar poupança no líquido. "
                            "Ambos cobertos pelo FGC dentro dos limites."
                        ),
                        "evaluation_criteria": [
                            "Menciona a isenção de IR da poupança.",
                            "Menciona a incidência de IR no CDB.",
                            "Compara liquidez dos dois produtos.",
                            "Conclui que a comparação depende das taxas vigentes.",
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
                            "LCI e LCA são isentas de IR. Isso significa que sempre "
                            "rendem mais que CDB?"
                        ),
                        "competency_codes": ["10.2.2"],
                        "options": [
                            {"value": "a", "label": "Sim — isenção de IR garante rendimento maior."},
                            {
                                "value": "b",
                                "label": (
                                    "Não — LCI/LCA têm prazo mínimo e podem ter taxa bruta "
                                    "menor. Compare sempre pelo rendimento líquido."
                                ),
                            },
                            {"value": "c", "label": "Sim — são os melhores investimentos de renda fixa."},
                            {"value": "d", "label": "Depende só da instituição."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! LCI/LCA são isentas de IR, mas têm prazo mínimo "
                            "(geralmente 90 dias para LCI, 90 dias para LCA) e podem "
                            "ter taxa bruta menor do que um CDB. Compare sempre o "
                            "rendimento líquido (após IR) no mesmo prazo."
                        ),
                        "feedback_incorrect": (
                            "A isenção de IR é uma vantagem, mas não garante rendimento "
                            "maior que CDB. LCI/LCA têm prazo mínimo e podem oferecer "
                            "taxa bruta menor. A comparação correta é pelo líquido."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Poupança: o produto mais simples e mais popular",
                    "order": 1,
                    "body": (
                        "**Poupança:**\n"
                        "- Rendimento: quando a Selic está acima de 8,5% ao ano, "
                        "rende 0,5% ao mês + TR. Abaixo de 8,5%, rende 70% da Selic + TR.\n"
                        "- Isenta de IR para pessoa física\n"
                        "- Liquidez alta (resgate a qualquer momento, mas rende só "
                        "nos 'aniversários' mensais)\n"
                        "- Cobertura do FGC\n\n"
                        "Vantagem: simplicidade e isenção de IR. Desvantagem: "
                        "rendimento pode ser baixo em relação ao CDI."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "CDB: Certificado de Depósito Bancário",
                    "order": 2,
                    "body": (
                        "**CDB:**\n"
                        "- O banco capta dinheiro do investidor e paga juros\n"
                        "- Rendimento: % do CDI (ex.: 100% CDI, 110% CDI) ou prefixado "
                        "ou indexado ao IPCA+\n"
                        "- Tributação: IR tabela regressiva (22,5% a 15%); IOF nos "
                        "primeiros 30 dias\n"
                        "- Liquidez: varia — diária ou com carência\n"
                        "- Cobertura do FGC: sim, dentro dos limites\n\n"
                        "Vantagem: variedade de opções e taxas. "
                        "Desvantagem: sujeito a IR e IOF."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "LCI e LCA: isentas de IR",
                    "order": 3,
                    "body": (
                        "**LCI (Letra de Crédito Imobiliário) e LCA (Agronegócio):**\n"
                        "- Captação para financiar os setores imobiliário e do agronegócio\n"
                        "- Isentas de IR para pessoa física\n"
                        "- Prazo mínimo: LCI — 90 dias; LCA — 90 dias (verificar "
                        "regulamentação vigente)\n"
                        "- Cobertura do FGC: sim, dentro dos limites\n\n"
                        "Vantagem: isenção de IR torna a comparação favorável em "
                        "muitos cenários. Desvantagem: prazo mínimo reduz liquidez."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Tesouro Direto: o governo como devedor",
                    "order": 4,
                    "body": (
                        "**Tesouro Direto:**\n"
                        "- Você empresta dinheiro ao governo federal\n"
                        "- Principais títulos:\n"
                        "  - **Tesouro Selic:** rende a Selic acumulada; baixo risco "
                        "de marcação a mercado; ideal para reserva\n"
                        "  - **Tesouro Prefixado:** taxa definida no momento da compra\n"
                        "  - **Tesouro IPCA+:** IPCA acumulado + taxa prefixada; "
                        "protege o poder de compra\n"
                        "- Tributação: IR tabela regressiva; IOF nos primeiros 30 dias\n"
                        "- Risco: menor risco de crédito no mercado doméstico\n\n"
                        "Acesse: tesourodireto.gov.br"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Onde consultar as condições atuais",
                    "order": 5,
                    "body": (
                        "As taxas dos produtos de renda fixa mudam constantemente. "
                        "Não use taxas específicas sem verificar a data:\n\n"
                        "- **CDB/LCI/LCA:** plataformas do banco ou corretora\n"
                        "- **Tesouro Direto:** tesourodireto.gov.br\n"
                        "- **Taxa Selic/CDI:** bacen.gov.br\n\n"
                        "O que não muda são as características estruturais: "
                        "isenção de IR para LCI/LCA, cobertura do FGC, etc."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Comparação de 4 produtos para R$ 5.000 por 1 ano",
                    "order": 6,
                    "body": (
                        "**Exemplo hipotético — taxas fictícias**\n\n"
                        "| Produto | Taxa bruta | IR (15%) | Rend. líquido |\n"
                        "|---|---|---|---|\n"
                        "| Poupança | 6%/ano | Isento | 6,0% |\n"
                        "| CDB 100% CDI | 10%/ano | 1,5% | 8,5% |\n"
                        "| LCI 8,5%/ano | 8,5%/ano | Isento | 8,5% |\n"
                        "| Tesouro Selic | 10%/ano | 1,5% | 8,5% |\n\n"
                        "*(Valores hipotéticos, para fins didáticos. "
                        "Taxas reais mudam diariamente.)*\n\n"
                        "Neste exemplo, CDB, LCI e Tesouro Selic têm o mesmo "
                        "rendimento líquido. A poupança fica abaixo. "
                        "A diferença está na liquidez e no risco de crédito."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 10.3 — FGC e tributação
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "FGC e tributação",
            "description": (
                "Entenda a cobertura real do FGC, seus limites e limitações, "
                "e aprenda a calcular o imposto sobre renda fixa."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "10.3.1",
                    "name": "Explicar o que o FGC cobre e o que não cobre",
                    "description": (
                        "Descreve os produtos cobertos, os limites por CPF por "
                        "instituição e o que o FGC não cobre."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "10.3.2",
                    "name": "Calcular a cobertura do FGC para um investimento",
                    "description": (
                        "Determina quanto de um investimento está coberto e quanto "
                        "ultrapassa o limite de proteção."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "10.3.3",
                    "name": "Aplicar as regras de IOF e IR por prazo",
                    "description": (
                        "Calcula o imposto devido sobre um resgate de renda fixa "
                        "considerando o prazo e a tabela regressiva."
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
                            "Qual é o limite de cobertura do FGC por CPF por instituição "
                            "financeira? (Verificar vigência em fgc.org.br)"
                        ),
                        "competency_codes": ["10.3.1"],
                        "options": [
                            {"value": "a", "label": "R$ 100.000."},
                            {"value": "b", "label": "R$ 250.000 por CPF por instituição."},
                            {"value": "c", "label": "R$ 500.000."},
                            {"value": "d", "label": "Não existe limite — o FGC cobre tudo."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O limite é R$ 250.000 por CPF por instituição "
                            "financeira associada ao FGC. Há ainda um teto global de "
                            "R$ 1.000.000 por CPF a cada 4 anos. "
                            "Verifique sempre em fgc.org.br."
                        ),
                        "feedback_incorrect": (
                            "O limite atual é R$ 250.000 por CPF por instituição, "
                            "com teto global de R$ 1.000.000 por CPF a cada 4 anos. "
                            "Confirme sempre no site oficial do FGC."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Fundo de ações tem garantia do FGC?",
                        "competency_codes": ["10.3.1"],
                        "options": [
                            {"value": "a", "label": "Sim — qualquer produto financeiro é coberto."},
                            {
                                "value": "b",
                                "label": (
                                    "Não — o FGC cobre depósitos e títulos bancários específicos. "
                                    "Fundos de investimento não estão cobertos."
                                ),
                            },
                            {"value": "c", "label": "Sim — se o banco quebrar, o fundo é coberto."},
                            {"value": "d", "label": "Depende do tipo de fundo."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O FGC cobre: conta corrente, poupança, CDB, LCI, "
                            "LCA, LC (Letras de Câmbio) e outros depósitos bancários. "
                            "Fundos de investimento, ações e debêntures não são cobertos."
                        ),
                        "feedback_incorrect": (
                            "O FGC tem escopo limitado. Ele cobre depósitos e títulos "
                            "emitidos pelas instituições associadas (CDB, LCI, poupança). "
                            "Fundos de investimento têm patrimônio separado do banco, "
                            "mas não têm cobertura do FGC."
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
                            "Carlos tem R$ 300.000 em CDB num único banco coberto "
                            "pelo FGC. Quanto está protegido?"
                        ),
                        "competency_codes": ["10.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 300.000 — o FGC cobre tudo."},
                            {
                                "value": "b",
                                "label": "R$ 250.000 — o limite por CPF por instituição.",
                            },
                            {"value": "c", "label": "R$ 0 — acima do limite, nada é coberto."},
                            {"value": "d", "label": "Depende do banco."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O FGC cobre até R$ 250.000 por CPF por instituição. "
                            "Os R$ 50.000 acima do limite não têm cobertura. "
                            "Para proteger R$ 300.000 integralmente, Carlos deveria "
                            "dividir entre dois bancos diferentes."
                        ),
                        "feedback_incorrect": (
                            "O limite é R$ 250.000 por CPF por IF. "
                            "R$ 50.000 ficam descobertos. Para cobrir R$ 300.000, "
                            "é necessário usar pelo menos dois bancos diferentes."
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
                            "Qual é a alíquota de IR para renda fixa resgatada "
                            "depois de 2 anos (720 dias ou mais)?"
                        ),
                        "competency_codes": ["10.3.3"],
                        "options": [
                            {"value": "a", "label": "22,5%."},
                            {"value": "b", "label": "20%."},
                            {"value": "c", "label": "15%."},
                            {"value": "d", "label": "Isento."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! A tabela regressiva de IR para renda fixa:\n"
                            "- Até 180 dias: 22,5%\n"
                            "- De 181 a 360 dias: 20%\n"
                            "- De 361 a 720 dias: 17,5%\n"
                            "- Acima de 720 dias: 15%\n\n"
                            "Quanto maior o prazo, menor a alíquota — incentivo ao "
                            "investimento de longo prazo."
                        ),
                        "feedback_incorrect": (
                            "A tabela regressiva de IR termina em 15% para prazos "
                            "acima de 720 dias. A alíquota diminui quanto maior o prazo."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Se você resgata um CDB no 15º dia, paga IOF?",
                        "competency_codes": ["10.3.3"],
                        "options": [
                            {"value": "a", "label": "Não — IOF só incide no primeiro dia."},
                            {
                                "value": "b",
                                "label": (
                                    "Sim — IOF incide sobre o rendimento nos primeiros "
                                    "30 dias, com alíquota decrescente."
                                ),
                            },
                            {"value": "c", "label": "Não — IOF só é cobrado em operações de câmbio."},
                            {"value": "d", "label": "Sim, sempre 1% fixo."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O IOF incide sobre o rendimento nos primeiros "
                            "30 dias, com alíquota decrescente: 96% no 1º dia até "
                            "0% no 30º dia. Depois do 30º dia, não há mais IOF."
                        ),
                        "feedback_incorrect": (
                            "O IOF em renda fixa segue uma tabela regressiva: incide "
                            "sobre o rendimento nos primeiros 30 dias, começando em "
                            "96% (1º dia) e chegando a 0% no 30º dia. "
                            "No 15º dia, a alíquota ainda é considerável."
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
                            "Explique a diferença entre 'garantia do FGC' e "
                            "'garantia de rentabilidade'. Por que esses são conceitos "
                            "distintos e qual erro comum esse conceito evita?"
                        ),
                        "competency_codes": ["10.3.1"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Pontos esperados: "
                            "FGC = garante devolução do principal + rendimentos "
                            "caso a IF quebre, dentro dos limites; "
                            "não garante que o investimento vai render bem; "
                            "o erro comum é confundir: 'tem FGC, então é seguro "
                            "investir em qualquer taxa' — o FGC cobre a quebra da IF, "
                            "não a rentabilidade nem o risco de mercado."
                        ),
                        "evaluation_criteria": [
                            "Explica que FGC cobre crédito (quebra da IF), não rentabilidade.",
                            "Distingue risco de crédito de risco de rentabilidade.",
                            "Menciona o limite de cobertura.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é o FGC e quem está por trás",
                    "order": 1,
                    "body": (
                        "O **Fundo Garantidor de Créditos (FGC)** é uma entidade "
                        "privada sem fins lucrativos mantida pelas instituições "
                        "financeiras associadas.\n\n"
                        "**Função:** proteger os depositantes e investidores em caso "
                        "de intervenção, liquidação ou falência de uma instituição "
                        "financeira associada.\n\n"
                        "**O FGC garante:** a devolução do principal + rendimentos "
                        "dentro dos limites estabelecidos.\n\n"
                        "**O FGC NÃO garante:** que o investimento vai render bem, "
                        "que a taxa será cumprida ou que não haverá perda por "
                        "marcação a mercado."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O que o FGC cobre e o que não cobre",
                    "order": 2,
                    "body": (
                        "**Produtos cobertos (principais):**\n"
                        "- Conta corrente e poupança\n"
                        "- CDB, RDB\n"
                        "- LCI, LCA\n"
                        "- Letras de Câmbio (LC)\n"
                        "- Depósitos a prazo\n\n"
                        "**Produtos NÃO cobertos:**\n"
                        "- Fundos de investimento\n"
                        "- Ações e ETFs\n"
                        "- Debêntures\n"
                        "- CRI e CRA\n"
                        "- Investimentos no exterior\n\n"
                        "Sempre verifique em **fgc.org.br** a lista atualizada "
                        "e os limites vigentes."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "IR em renda fixa: tabela regressiva",
                    "order": 3,
                    "body": (
                        "O Imposto de Renda sobre renda fixa segue uma tabela "
                        "**regressiva**: quanto maior o prazo, menor a alíquota.\n\n"
                        "| Prazo | Alíquota IR |\n"
                        "|---|---|\n"
                        "| Até 180 dias | 22,5% |\n"
                        "| 181 a 360 dias | 20% |\n"
                        "| 361 a 720 dias | 17,5% |\n"
                        "| Acima de 720 dias | 15% |\n\n"
                        "O IR incide sobre o **rendimento**, não sobre o capital. "
                        "É retido na fonte pela instituição."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "IOF: o imposto dos primeiros 30 dias",
                    "order": 4,
                    "body": (
                        "O **IOF** incide sobre o rendimento nos primeiros 30 dias "
                        "de aplicação. A alíquota diminui a cada dia:\n\n"
                        "- Dia 1: 96% do rendimento\n"
                        "- Dia 15: cerca de 50% do rendimento\n"
                        "- Dia 30: 0%\n\n"
                        "Após 30 dias: **sem IOF**.\n\n"
                        "Por isso, resgatar antes de 30 dias pode custar caro. "
                        "Se você sabe que pode precisar do dinheiro em menos de "
                        "30 dias, evite produtos de renda fixa — use conta remunerada "
                        "ou poupança, que não têm IOF."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Cálculo de IR e IOF em um CDB",
                    "order": 5,
                    "body": (
                        "**CDB hipotético: R$ 10.000 a 10%/ano**\n\n"
                        "**Cenário A: resgate em 90 dias**\n"
                        "- Rendimento bruto (hipotético): ≈ R$ 244\n"
                        "- IR: 22,5% → R$ 55\n"
                        "- IOF: R$ 0 (> 30 dias)\n"
                        "- Rendimento líquido: ≈ R$ 189\n\n"
                        "**Cenário B: resgate em 360 dias**\n"
                        "- Rendimento bruto (hipotético): ≈ R$ 1.000\n"
                        "- IR: 20% → R$ 200\n"
                        "- IOF: R$ 0\n"
                        "- Rendimento líquido: ≈ R$ 800\n\n"
                        "*(Valores hipotéticos, para fins didáticos.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 10.4 — Comparando produtos
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Comparando produtos",
            "description": (
                "Calcule o rendimento líquido de dois produtos e compare pelo "
                "resultado real, não pelo rendimento bruto."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "10.4.1",
                    "name": "Calcular a rentabilidade líquida após IR",
                    "description": (
                        "Aplica a alíquota de IR sobre o rendimento bruto para "
                        "obter o rendimento líquido de uma aplicação de renda fixa."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "10.4.2",
                    "name": "Comparar dois produtos pelo rendimento real líquido",
                    "description": (
                        "Determina qual produto oferece maior rendimento líquido "
                        "comparando CDB tributado com produto isento de IR."
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
                            "CDB rende 13%/ano (bruto). IR de 15% (prazo > 720 dias). "
                            "Qual é o rendimento líquido? (Valores hipotéticos.)"
                        ),
                        "competency_codes": ["10.4.1"],
                        "options": [
                            {"value": "a", "label": "≈ 11,05%/ano."},
                            {"value": "b", "label": "13%/ano."},
                            {"value": "c", "label": "1,95%/ano."},
                            {"value": "d", "label": "15%/ano."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Líquido = 13% × (1 − 0,15) = 13% × 0,85 = 11,05%. "
                            "O IR de 15% incide sobre o rendimento (não sobre o capital)."
                        ),
                        "feedback_incorrect": (
                            "Rendimento líquido = bruto × (1 − alíquota IR). "
                            "13% × (1 − 0,15) = 13% × 0,85 = 11,05%."
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
                            "LCI rende 11%/ano (isenta de IR). CDB rende 13%/ano "
                            "(IR 15%). Qual rende mais no líquido? (Valores hipotéticos.)"
                        ),
                        "competency_codes": ["10.4.2"],
                        "options": [
                            {"value": "a", "label": "CDB — taxa bruta maior."},
                            {
                                "value": "b",
                                "label": (
                                    "LCI — rende 11% líquido contra 11,05% do CDB. "
                                    "Neste caso, são praticamente iguais."
                                ),
                            },
                            {"value": "c", "label": "CDB — 11,05% líquido contra 11% da LCI."},
                            {"value": "d", "label": "LCI sempre rende mais — isenção de IR."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! CDB líquido: 13% × 0,85 = 11,05%. LCI líquido: 11%. "
                            "Neste cenário específico, o CDB rende 0,05% a mais no líquido. "
                            "A diferença é pequena, mas ilustra que a comparação deve ser "
                            "sempre pelo líquido."
                        ),
                        "feedback_incorrect": (
                            "Compare pelo líquido: CDB = 13% × (1 − 0,15) = 11,05%. "
                            "LCI = 11% (isenta). O CDB rende ligeiramente mais neste "
                            "cenário hipotético. Isenção de IR não garante sempre "
                            "o maior rendimento líquido."
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
                            "Compare 3 produtos hipotéticos para R$ 5.000,00 por 1 ano:\n\n"
                            "- Produto A: CDB 12%/ano, IR 17,5% (361–720 dias)\n"
                            "- Produto B: LCI 10%/ano, isenta de IR\n"
                            "- Produto C: Poupança 7%/ano, isenta de IR\n\n"
                            "Qual tem maior rendimento líquido?"
                        ),
                        "competency_codes": ["10.4.1", "10.4.2"],
                        "scenario": (
                            "Aplicação de R$ 5.000 por 1 ano. "
                            "Taxas hipotéticas, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": "Produto A (CDB): líquido ≈ 9,9%/ano (12% × 0,825).",
                            },
                            {
                                "value": "b",
                                "label": "Produto B (LCI): líquido = 10%/ano (isenta).",
                            },
                            {
                                "value": "c",
                                "label": "Produto C (poupança): líquido = 7%/ano (isenta).",
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Correto! LCI com 10% líquido supera CDB com 9,9% líquido "
                            "(12% × (1−17,5%) = 12% × 0,825 = 9,9%) e poupança com 7%. "
                            "Neste cenário hipotético, a LCI é a melhor escolha no líquido."
                        ),
                        "feedback_incorrect": (
                            "Compare os rendimentos líquidos:\n"
                            "A: 12% × (1 − 0,175) = 9,9%\n"
                            "B: 10% (isenta)\n"
                            "C: 7% (isenta)\n"
                            "Produto B (LCI) tem maior rendimento líquido."
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
                            "Explique a diferença entre rendimento bruto e rendimento "
                            "líquido em renda fixa. Por que você sempre deve comparar "
                            "produtos pelo rendimento líquido, nunca pelo bruto?"
                        ),
                        "competency_codes": ["10.4.1"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Pontos esperados: bruto = taxa antes do IR/IOF; "
                            "líquido = bruto menos os impostos devidos; "
                            "comparar pelo bruto pode levar a escolher um produto "
                            "com maior taxa nominal mas menor rendimento efetivo "
                            "(ex.: CDB 13% bruto vs. LCI 11% isenta)."
                        ),
                        "evaluation_criteria": [
                            "Define rendimento bruto (sem IR/IOF).",
                            "Define rendimento líquido (após IR/IOF).",
                            "Explica por que comparar pelo bruto pode ser enganoso.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Rendimento bruto vs. rendimento líquido",
                    "order": 1,
                    "body": (
                        "**Rendimento bruto:** a taxa nominal antes dos impostos "
                        "(IR e IOF). É o número que o banco geralmente anuncia.\n\n"
                        "**Rendimento líquido:** o ganho efetivo depois de descontar "
                        "IR e IOF. É o que importa na comparação.\n\n"
                        "**Fórmula:**\n"
                        "Rend. líquido = rend. bruto × (1 − alíquota IR)\n\n"
                        "Para LCI/LCA (isentas de IR):\n"
                        "Rend. líquido = rend. bruto (são iguais)\n\n"
                        "Nunca compare um produto tributado com um isento pelo "
                        "rendimento bruto — você vai fazer a escolha errada."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "CDB vs. LCI: quem vence no líquido?",
                    "order": 2,
                    "body": (
                        "**Cenário hipotético — prazo: 1 ano, IR: 17,5%**\n\n"
                        "| Produto | Bruto | IR | Líquido |\n"
                        "|---|---|---|---|\n"
                        "| CDB 12%/ano | 12% | 2,1% | 9,9% |\n"
                        "| LCI 10%/ano | 10% | 0% | 10% |\n"
                        "| Poupança 7%/ano | 7% | 0% | 7% |\n\n"
                        "Neste exemplo, a LCI (10% isenta) supera o CDB (9,9% líquido) "
                        "mesmo com taxa bruta menor. A poupança fica atrás dos dois.\n\n"
                        "*(Valores hipotéticos. Compare com as taxas vigentes.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Simuladores: use sempre antes de decidir",
                    "order": 3,
                    "body": (
                        "Antes de investir, compare os produtos usando simuladores:\n\n"
                        "- **Tesouro Direto:** tesourodireto.gov.br (simulador próprio)\n"
                        "- **Banco/Corretora:** plataformas geralmente têm calculadora "
                        "de rendimento líquido\n"
                        "- **IPCA como referência:** verifique se o rendimento líquido "
                        "supera a inflação do período\n\n"
                        "Simuladores automatizam o cálculo de IR e IOF — "
                        "use-os, mas verifique as premissas."
                    ),
                },
            ],
        },
    ],
}
