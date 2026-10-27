"""Conteúdo expandido da Trilha 2 — Orçamento na prática (v1).

phase_number: 2 (existente — NÃO inserir nova fase)
Fonte editorial: docs/trilhas/trilha-02.md

Missões 1 e 2 são expansões (upsert sobre as existentes de phase_1_v1.py).
Missões 3 e 4 são novas.
O seeder usa upsert por chave natural — não duplica conteúdo existente.
Todos os valores financeiros nos exemplos são fictícios e identificados como tal.
"""

TRAIL_2_V1 = {
    "phase_number": 2,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 2.1 — O que importa primeiro? (expansão sobre phase_1_v1)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "O que importa primeiro?",
            "description": (
                "Diferencie necessidades de desejos, priorize gastos com renda "
                "limitada e entenda as consequências de não pagar o essencial."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.1.1",
                    "name": "Diferenciar necessidades de desejos no contexto do próprio orçamento",
                    "description": (
                        "Classifica uma despesa como necessidade ou desejo levando em conta "
                        "o contexto pessoal (profissional, de saúde, dependentes) e não "
                        "apenas a categoria genérica do item."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.1.2",
                    "name": "Priorizar gastos com renda limitada",
                    "description": (
                        "Ordena as despesas pela consequência de não pagá-las, "
                        "garantindo que os essenciais com maior impacto sejam "
                        "cobertos primeiro."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.1.3",
                    "name": "Reconhecer que contexto e consequência mudam a classificação",
                    "description": (
                        "Explica que o mesmo item pode ser necessidade para uma pessoa "
                        "e desejo para outra, dependendo das consequências de não pagá-lo."
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
                        "prompt": "Qual dos itens abaixo é considerado uma necessidade básica?",
                        "competency_codes": ["2.1.1"],
                        "options": [
                            {"value": "a", "label": "Assinatura de streaming de vídeo."},
                            {"value": "b", "label": "Alimentação diária."},
                            {"value": "c", "label": "Roupas de grife."},
                            {"value": "d", "label": "Viagem de férias."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Alimentação é uma necessidade básica — sem ela, "
                            "há impacto direto na saúde e na capacidade de trabalhar. "
                            "Os demais itens são desejos ou confortos, não necessidades essenciais."
                        ),
                        "feedback_incorrect": (
                            "Alimentação diária é a única necessidade básica entre as opções. "
                            "Streaming, roupas de grife e viagens são desejos — podem ser "
                            "importantes para qualidade de vida, mas não são essenciais para "
                            "sobrevivência e trabalho."
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
                            "Marina é arquiteta e usa o celular para receber clientes e "
                            "acessar projetos. Pedro é estudante universitário e usa o "
                            "celular apenas para redes sociais e entretenimento.\n\n"
                            "Para quem o celular é necessidade e para quem é desejo?"
                        ),
                        "competency_codes": ["2.1.1", "2.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Para Marina é necessidade; para Pedro é desejo.",
                            },
                            {
                                "value": "b",
                                "label": "Para ambos é necessidade — todo mundo precisa de celular.",
                            },
                            {
                                "value": "c",
                                "label": "Para ambos é desejo — celular não é essencial.",
                            },
                            {
                                "value": "d",
                                "label": "Para Pedro é necessidade; para Marina é desejo.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O contexto importa. Para Marina, o celular é "
                            "ferramenta de trabalho — não tê-lo afeta sua renda diretamente. "
                            "Para Pedro, é principalmente entretenimento: pode ser substituído "
                            "ou reduzido sem impacto grave imediato."
                        ),
                        "feedback_incorrect": (
                            "A classificação depende do contexto, não do item. "
                            "Para Marina (arquiteta), o celular é ferramenta de trabalho — "
                            "necessidade. Para Pedro (estudante que usa para entretenimento), "
                            "é um desejo. O mesmo objeto pode ter classificações diferentes."
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
                            "Você recebeu R$ 900 e tem contas de R$ 800 (aluguel + alimentação). "
                            "Um amigo te convidou para um show que custa R$ 150.\n\n"
                            "O que você faz?"
                        ),
                        "competency_codes": ["2.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Paga as contas e não vai ao show: R$ 900 − R$ 800 = "
                                    "R$ 100 de folga, insuficiente para o show."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Vai ao show e paga metade do aluguel depois: "
                                    "o show é importante para o bem-estar."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pede emprestado R$ 50 para cobrir o show e "
                                    "paga todas as contas."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Com R$ 100 de folga e show custando R$ 150, "
                            "as contas têm prioridade absoluta. Não pagar o aluguel "
                            "ou a alimentação tem consequências mais graves "
                            "(despejo, saúde) do que perder o show."
                        ),
                        "feedback_incorrect": (
                            "Com R$ 900 e R$ 800 de contas essenciais, só sobram R$ 100. "
                            "O show não cabe neste mês. Pagar metade do aluguel cria "
                            "uma dívida com juros ou multa. Pegar emprestado para lazer "
                            "é uma armadilha — o empréstimo terá que ser pago com a "
                            "renda do próximo mês, que pode ser igual."
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
                            "Pense em uma compra que você fez ou considera fazer. "
                            "Era uma necessidade ou um desejo? "
                            "Justifique levando em conta o seu contexto atual."
                        ),
                        "competency_codes": ["2.1.1", "2.1.3"],
                        "feedback_static": (
                            "Não há resposta certa ou errada aqui — o que importa é "
                            "o raciocínio. Necessidade é o que, se não pago, gera "
                            "consequências graves para saúde, trabalho ou moradia. "
                            "Desejo é tudo que melhora a vida mas pode esperar ou "
                            "ser substituído sem impacto grave."
                        ),
                        "evaluation_criteria": [
                            "Cita o item específico e o classifica (necessidade ou desejo).",
                            "Justifica a classificação com base no contexto pessoal.",
                            "Menciona ao menos uma consequência de não pagar o item.",
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
                            "João tem R$ 1.600 líquidos. Suas despesas:\n\n"
                            "- Aluguel: R$ 700\n"
                            "- Alimentação: R$ 450\n"
                            "- Energia: R$ 90\n"
                            "- Streaming: R$ 40\n\n"
                            "Sobrou R$ 320. Qual compra cabe no orçamento?"
                            " (Valores fictícios, para fins didáticos.)"
                        ),
                        "competency_codes": ["2.1.1", "2.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Um tênis de R$ 280 para o trabalho — entra com R$ 40 de sobra.",
                            },
                            {
                                "value": "b",
                                "label": "Uma TV de R$ 1.200 em 4× de R$ 300 no crédito.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Um curso online de R$ 180 para progressão na carreira — "
                                    "entra com R$ 140 de folga."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "Nenhum — o ideal é guardar os R$ 320 como reserva.",
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Guardar os R$ 320 é a melhor decisão neste mês — "
                            "João ainda não tem reserva de emergência mencionada. "
                            "A TV parcelada compromete R$ 300/mês por 4 meses. "
                            "Tênis e curso podem entrar, mas a reserva tem prioridade "
                            "quando ela ainda não existe."
                        ),
                        "feedback_incorrect": (
                            "Com apenas R$ 320 de folga e sem reserva de emergência, "
                            "o ideal é guardar tudo. Parcelar a TV compromete a renda "
                            "futura por 4 meses. Tênis e curso são válidos, mas a "
                            "reserva é mais urgente — um imprevisto sem reserva "
                            "pode gerar dívida com juros altos."
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
                            "Qual consequência de não pagar o aluguel é mais grave "
                            "do que não renovar a assinatura de streaming?"
                        ),
                        "competency_codes": ["2.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Perder acesso a séries e filmes.",
                            },
                            {
                                "value": "b",
                                "label": "Risco de despejo e de perder a moradia.",
                            },
                            {
                                "value": "c",
                                "label": "Multa de cancelamento do streaming.",
                            },
                            {
                                "value": "d",
                                "label": "As duas consequências são igualmente graves.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Não pagar o aluguel pode resultar em despejo — "
                            "uma consequência que afeta diretamente a moradia e a "
                            "estabilidade. Perder o streaming é um inconveniente, "
                            "não uma ameaça à subsistência."
                        ),
                        "feedback_incorrect": (
                            "A gravidade da consequência define a prioridade. "
                            "Não pagar o aluguel pode levar ao despejo — impacto "
                            "na moradia e na estabilidade. Não renovar o streaming "
                            "gera no máximo um inconveniente de entretenimento. "
                            "Isso justifica pagar o aluguel primeiro, sempre."
                        ),
                    },
                },
                {
                    "order": 7,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Descreva uma situação em que você (ou alguém fictício) "
                            "precisaria escolher entre duas despesas. "
                            "Qual você pagaria primeiro e por quê?"
                        ),
                        "competency_codes": ["2.1.2", "2.1.3"],
                        "feedback_static": (
                            "A chave é pensar na consequência de NÃO pagar cada item. "
                            "A despesa cuja falta causa mais dano imediato "
                            "(perda de moradia, saúde, trabalho) deve ser paga primeiro, "
                            "independentemente do valor ou do desejo."
                        ),
                        "evaluation_criteria": [
                            "Descreve a situação com duas despesas específicas.",
                            "Indica qual pagaria primeiro.",
                            "Justifica pela consequência de não pagar, não apenas pelo valor.",
                        ],
                        "max_length": 600,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que são necessidades e o que são desejos?",
                    "order": 1,
                    "body": (
                        "**Necessidade** é tudo aquilo cuja ausência gera consequências "
                        "graves e imediatas — para a saúde, para o trabalho ou para "
                        "a moradia. Exemplos: aluguel, alimentação, transporte para o trabalho, "
                        "medicamento de uso contínuo.\n\n"
                        "**Desejo** é tudo que melhora a qualidade de vida, mas pode "
                        "ser adiado ou substituído sem dano imediato. Exemplos: "
                        "streaming, roupas de marca, viagens, eletrônicos novos.\n\n"
                        "**Atenção:** a classificação depende do contexto. "
                        "Um celular pode ser necessidade para um profissional autônomo "
                        "e desejo para quem usa apenas para lazer."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Marina e Pedro: o mesmo item, classificações diferentes",
                    "order": 2,
                    "body": (
                        "**Marina**, arquiteta freelancer, usa o celular para receber "
                        "clientes, enviar projetos e acessar o aplicativo do banco. "
                        "Sem celular, ela não trabalha. → **Necessidade**\n\n"
                        "**Pedro**, universitário, usa o celular para redes sociais "
                        "e entretenimento. Ele tem computador em casa para estudos. "
                        "Sem celular, sua vida muda, mas sem impacto grave imediato. "
                        "→ **Desejo**\n\n"
                        "*(Situação fictícia, para fins didáticos.)*\n\n"
                        "**Lição:** sempre pergunte: 'Qual é a consequência de não ter isso?'"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A pergunta que ajuda a decidir",
                    "order": 3,
                    "body": (
                        "Quando estiver em dúvida se algo é necessidade ou desejo, "
                        "faça esta pergunta:\n\n"
                        "**'O que acontece se eu não pagar isso este mês?'**\n\n"
                        "- Se a resposta envolver perda de moradia, saúde, trabalho "
                        "ou dívida com multa alta → **necessidade**.\n"
                        "- Se a resposta for 'fico sem o produto/serviço por um tempo' "
                        "→ **desejo**.\n\n"
                        "Essa pergunta simples reordena as prioridades sem precisar "
                        "de planilha ou cálculo."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Consequências de não pagar o essencial",
                    "order": 4,
                    "body": (
                        "Cada despesa essencial não paga gera uma consequência específica:\n\n"
                        "| Despesa | Consequência de não pagar |\n"
                        "|---|---|\n"
                        "| Aluguel | Multa, cobrança judicial, risco de despejo |\n"
                        "| Alimentação | Impacto na saúde e na produtividade |\n"
                        "| Energia elétrica | Corte, multa de religação |\n"
                        "| Transporte | Impossibilidade de trabalhar |\n"
                        "| Medicamento | Risco à saúde |\n\n"
                        "Conhecer essas consequências ajuda a priorizar com clareza, "
                        "sem depender de regras rígidas."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Renda de R$ 1.600: o que pagar primeiro quando falta dinheiro",
                    "order": 5,
                    "body": (
                        "**João** recebe R$ 1.600/mês e tem as seguintes despesas "
                        "*(fictício, para fins didáticos)*:\n\n"
                        "| Despesa | Valor | Classificação |\n"
                        "|---|---|---|\n"
                        "| Aluguel | R$ 700 | Necessidade (risco de despejo) |\n"
                        "| Alimentação | R$ 450 | Necessidade (saúde) |\n"
                        "| Energia | R$ 90 | Necessidade (corte imediato) |\n"
                        "| Streaming | R$ 40 | Desejo |\n\n"
                        "**Total essencial:** R$ 1.240. **Sobra:** R$ 360.\n\n"
                        "Se a renda cair para R$ 1.200 num mês difícil, "
                        "João paga os R$ 1.240 de essenciais (mesmo com déficit de R$ 40) "
                        "e cancela o streaming para cobrir a diferença. "
                        "Cortar o streaming primeiro é o movimento correto."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como lidar com a sensação de culpa ao dizer não a um desejo",
                    "order": 6,
                    "body": (
                        "Dizer não a um desejo não é punição — é uma escolha. "
                        "Lembre-se:\n\n"
                        "1. **Você está decidindo, não impedindo.** "
                        "A decisão está nas suas mãos, não nas circunstâncias.\n\n"
                        "2. **Adiado ≠ cancelado.** O show, o produto, a viagem "
                        "continuam existindo. Você os terá quando a situação permitir.\n\n"
                        "3. **Pagar o essencial primeiro é autocuidado financeiro.** "
                        "Você está protegendo sua estabilidade para poder desfrutar "
                        "os desejos sem dívida depois.\n\n"
                        "A sensação de privação passa. A dívida por desejo, não."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 2.2 — Meu primeiro plano (expansão sobre phase_1_v1)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Meu primeiro plano",
            "description": (
                "Distribua a renda entre prioridades, entenda a lógica do orçamento "
                "e saiba o que fazer quando o dinheiro não fecha."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.2.1",
                    "name": "Distribuir a renda entre prioridades",
                    "description": (
                        "Aloca a renda disponível nas categorias essenciais, "
                        "dívidas com juros, objetivos e reserva, nessa ordem de prioridade."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.2.2",
                    "name": "Justificar prioridades pelas consequências",
                    "description": (
                        "Explica por que cada prioridade antecede a seguinte, "
                        "com base no custo de não pagá-la."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.2.3",
                    "name": "Reconhecer o valor de separar a reserva no início",
                    "description": (
                        "Entende que guardar no início do mês é mais eficaz do que "
                        "guardar o que sobra no fim."
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
                            "Ao receber o salário, qual é a ordem correta de prioridades "
                            "para distribuir a renda?"
                        ),
                        "competency_codes": ["2.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Desejos → dívidas → essenciais → reserva.",
                            },
                            {
                                "value": "b",
                                "label": "Essenciais → dívidas → reserva → desejos.",
                            },
                            {
                                "value": "c",
                                "label": "Reserva → desejos → essenciais → dívidas.",
                            },
                            {
                                "value": "d",
                                "label": "Dívidas → desejos → reserva → essenciais.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A ordem é: essenciais primeiro (risco imediato de "
                            "não pagar), dívidas com juros (custo crescente), "
                            "reserva (proteção futura) e desejos por último. "
                            "Essa sequência protege o que mais importa."
                        ),
                        "feedback_incorrect": (
                            "A ordem correta é: essenciais → dívidas → reserva → desejos. "
                            "Essenciais têm prioridade porque a consequência de não "
                            "pagá-los é imediata (despejo, corte de energia, saúde). "
                            "Dívidas com juros crescem se não pagas. "
                            "Desejos são o último destino — não o primeiro."
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
                            "Ana tem dívida com juros de 5%/mês e também quer "
                            "guardar para a reserva de emergência. "
                            "O que ela deve priorizar?"
                        ),
                        "competency_codes": ["2.2.1", "2.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Guardar para a reserva — segurança vem primeiro.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar a dívida — juros de 5%/mês sobre o saldo restante "
                                    "custam mais do que qualquer rendimento da reserva."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Dividir igualmente entre os dois.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Uma dívida a 5%/mês cresce mais rápido do que "
                            "qualquer aplicação conservadora rende. Pagar a dívida "
                            "primeiro elimina um custo certo; guardar a reserva "
                            "sem quitar a dívida é economicamente ineficiente."
                        ),
                        "feedback_incorrect": (
                            "Quando há dívida com juros altos, quitá-la tem retorno "
                            "garantido (você deixa de pagar aqueles juros). "
                            "Guardar dinheiro enquanto paga 5%/mês de juros equivale "
                            "a investir com rentabilidade negativa. Quitar primeiro, "
                            "depois construir a reserva."
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
                            "Ana recebe R$ 2.200 líquidos por mês. "
                            "Despesas mensais:\n\n"
                            "- Aluguel: R$ 700\n"
                            "- Alimentação: R$ 400\n"
                            "- Transporte: R$ 150\n"
                            "- Prestação de empréstimo: R$ 200\n"
                            "- Contas de serviços (água, luz, net): R$ 180\n\n"
                            "Total essencial + dívida: R$ 1.630. Sobra: R$ 570.\n\n"
                            "Como Ana deve distribuir os R$ 570 restantes? "
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "competency_codes": ["2.2.1"],
                        "scenario": (
                            "Ana, renda R$ 2.200 líquidos, sem reserva constituída, "
                            "sem meta de curto prazo. Situação fictícia."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Reserva: R$ 300, lazer: R$ 200, outros: R$ 70. "
                                    "Guardar antes de gastar com lazer."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Lazer: R$ 400, reserva: R$ 100, outros: R$ 70. "
                                    "Merece relaxar depois de pagar tudo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Tudo para lazer e desejos: R$ 570. "
                                    "Essenciais já estão pagos."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Ótima distribuição! Com a reserva priorizada (R$ 300), "
                            "Ana constrói segurança antes de gastar com lazer. "
                            "Em 18 meses ela terá R$ 5.400 — equivalente a 3 meses "
                            "de despesas essenciais. O lazer (R$ 200) é suficiente "
                            "para qualidade de vida sem comprometer o futuro."
                        ),
                        "feedback_incorrect": (
                            "Com R$ 570 sobrando e sem reserva, a prioridade é "
                            "separar a reserva primeiro. A opção A é a mais equilibrada: "
                            "R$ 300 para a reserva e R$ 200 para lazer e outros. "
                            "Gastar tudo com lazer deixa Ana vulnerável a qualquer imprevisto."
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
                            "O orçamento de Rafael fechou com déficit de R$ 150 "
                            "este mês. Qual é a melhor estratégia?"
                            " (Valores fictícios.)"
                        ),
                        "competency_codes": ["2.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Usar o cartão de crédito para cobrir o déficit "
                                    "e pagar depois."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Reduzir R$ 150 de uma categoria não essencial "
                                    "(lazer, streaming, saídas) neste mês."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ignorar — o próximo mês provavelmente será melhor."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Reduzir uma categoria não essencial é a solução "
                            "sem custo futuro. Usar o crédito cria uma dívida nova "
                            "(com juros se não paga na íntegra). Ignorar o déficit "
                            "transforma um problema pontual em hábito."
                        ),
                        "feedback_incorrect": (
                            "Cobrir o déficit com crédito adiciona juros ao problema "
                            "original. Ignorar não resolve. A solução de menor custo "
                            "é cortar uma categoria não essencial neste mês específico — "
                            "não de forma permanente, só para equilibrar."
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
                            "Qual categoria do orçamento é mais fácil de reduzir "
                            "sem impacto grave na vida de quem precisa equilibrar as contas?"
                        ),
                        "competency_codes": ["2.2.2"],
                        "options": [
                            {"value": "a", "label": "Aluguel."},
                            {"value": "b", "label": "Alimentação básica."},
                            {"value": "c", "label": "Lazer e entretenimento."},
                            {"value": "d", "label": "Transporte para o trabalho."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Lazer e entretenimento são desejos — "
                            "reduzir ou eliminar temporariamente não gera "
                            "consequências graves. Aluguel, alimentação e transporte "
                            "para o trabalho têm impacto direto em moradia, "
                            "saúde e capacidade de gerar renda."
                        ),
                        "feedback_incorrect": (
                            "Aluguel, alimentação e transporte para o trabalho "
                            "são necessidades com consequências graves se não pagas. "
                            "Lazer é a categoria mais flexível: pode ser reduzida "
                            "temporariamente sem impacto direto em saúde, moradia "
                            "ou renda."
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
                            "Monte o orçamento fictício do Carlos: "
                            "renda líquida de R$ 2.000/mês. "
                            "Despesas fixas: aluguel R$ 600, alimentação R$ 350, "
                            "transporte R$ 130. "
                            "Como você distribuiria o restante? "
                            "Justifique a ordem das prioridades."
                        ),
                        "competency_codes": ["2.2.1"],
                        "feedback_static": (
                            "O restante seria R$ 920. "
                            "Uma boa distribuição começa pela reserva (prioridade), "
                            "depois dívidas se houver, e por último lazer e desejos. "
                            "Exemplo: reserva R$ 400, lazer R$ 200, outros R$ 320. "
                            "O critério é: quanto maior o custo de não pagar, "
                            "maior a prioridade."
                        ),
                        "evaluation_criteria": [
                            "Lista todas as categorias com valores somando R$ 2.000.",
                            "Justifica a ordem das prioridades.",
                            "Inclui a reserva como uma das categorias.",
                        ],
                        "max_length": 600,
                    },
                },
                {
                    "order": 7,
                    "activity_type": "open_text",
                    "points_value": 0,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Por que separar a reserva no início do mês "
                            "(no momento do recebimento) funciona melhor do que "
                            "guardar o que sobra no fim do mês?"
                        ),
                        "competency_codes": ["2.2.3"],
                        "feedback_static": (
                            "Guardar o que sobra raramente funciona porque "
                            "as despesas tendem a expandir para preencher a renda disponível. "
                            "Ao separar primeiro, você trata a reserva como despesa "
                            "obrigatória — ela sai antes que haja a oportunidade de gastá-la. "
                            "É o princípio de 'pagar a si mesmo primeiro'."
                        ),
                        "evaluation_criteria": [
                            "Explica por que guardar o que sobra não funciona.",
                            "Descreve o mecanismo de separar antes de gastar.",
                        ],
                        "max_length": 500,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como montar um orçamento simples",
                    "order": 1,
                    "body": (
                        "Um orçamento básico tem apenas três etapas:\n\n"
                        "**1. Calcule a renda líquida** — o que realmente cai na conta "
                        "(não o bruto).\n\n"
                        "**2. Liste todas as despesas** — fixas (não mudam: aluguel, "
                        "prestação) e variáveis (mudam: alimentação, lazer).\n\n"
                        "**3. Compare receita e despesa** — se a diferença for positiva, "
                        "distribua a sobra entre reserva e desejos. "
                        "Se for negativa, identifique o que cortar.\n\n"
                        "Não precisa ser perfeito no primeiro mês. "
                        "Um orçamento aproximado já é melhor do que nenhum."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O orçamento da Ana: R$ 1.724 líquidos distribuídos",
                    "order": 2,
                    "body": (
                        "**Ana**, 22 anos, renda líquida R$ 1.724/mês *(fictício)*:\n\n"
                        "| Categoria | Valor | Tipo |\n"
                        "|---|---|---|\n"
                        "| Aluguel (dividido) | R$ 500 | Fixo |\n"
                        "| Alimentação | R$ 400 | Variável |\n"
                        "| Transporte (incluso no VT) | R$ 0 | — |\n"
                        "| Celular | R$ 60 | Fixo |\n"
                        "| Reserva de emergência | R$ 400 | Objetivo |\n"
                        "| Lazer | R$ 200 | Desejo |\n"
                        "| Outros | R$ 164 | Variável |\n"
                        "| **Total** | **R$ 1.724** | |\n\n"
                        "Ana separa os R$ 400 da reserva no dia do recebimento "
                        "antes de qualquer outro gasto. Assim, a reserva é garantida "
                        "mesmo que o mês seja difícil."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Guarde sempre uma parte antes de gastar",
                    "order": 3,
                    "body": (
                        "A estratégia mais eficaz para guardar dinheiro é simples: "
                        "faça a transferência para a reserva no mesmo dia em que "
                        "o salário cair na conta, antes de qualquer gasto.\n\n"
                        "Por quê isso funciona?\n\n"
                        "- **Você não gasta o que não vê.** "
                        "O dinheiro separado fica fora da conta corrente.\n"
                        "- **Elimina a tentação de gastar primeiro.** "
                        "Guardar 'o que sobra' raramente funciona — "
                        "sempre aparecem gastos que consomem a sobra.\n"
                        "- **Transforma poupança em hábito automático.**\n\n"
                        "Comece com qualquer valor: R$ 50, R$ 100. "
                        "O hábito importa mais do que o montante inicial."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Categorias de orçamento: como organizar sem complicar",
                    "order": 4,
                    "body": (
                        "Um orçamento simples tem quatro categorias:\n\n"
                        "**1. Essenciais** — despesas cuja falta gera consequências graves. "
                        "Aluguel, alimentação, transporte para o trabalho, saúde, energia.\n\n"
                        "**2. Dívidas** — parcelas e créditos a pagar. "
                        "Quitá-las é prioridade porque têm custo de juros.\n\n"
                        "**3. Reserva / objetivos** — o 'salário para você'. "
                        "Transferir antes de gastar garante que acontece.\n\n"
                        "**4. Desejos** — o que sobra depois das três primeiras. "
                        "Não é errado gastar aqui — é o destino correto para esse dinheiro.\n\n"
                        "Não crie 20 subcategorias no início. "
                        "Quatro grupos são suficientes para começar."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Dois meses: com e sem planejamento",
                    "order": 5,
                    "body": (
                        "**Mês sem planejamento — Carla, R$ 2.000/mês** *(fictício)*:\n\n"
                        "Carla gasta conforme a vontade. No dia 20, já gastou R$ 1.900 "
                        "e ainda faltam 10 dias. Ela usa o cartão de crédito para "
                        "cobrir os últimos dias. Resultado: chega ao próximo mês "
                        "com R$ 300 de dívida no cartão e sem reserva.\n\n"
                        "**Mês com planejamento — mesma Carla:**\n\n"
                        "No dia do recebimento, Carla separa:\n"
                        "- Essenciais: R$ 1.200\n"
                        "- Reserva: R$ 300 (transferência imediata)\n"
                        "- Lazer: R$ 300\n"
                        "- Margem: R$ 200\n\n"
                        "No dia 20, ela sabe que tem R$ 200 de margem. "
                        "Usa R$ 150 e chega ao fim do mês sem dívida. "
                        "Em 12 meses, terá R$ 3.600 de reserva."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O que fazer quando o orçamento fecha no negativo",
                    "order": 6,
                    "body": (
                        "Se a soma das despesas supera a renda, há três caminhos:\n\n"
                        "**1. Reduzir despesas não essenciais** — cancelar assinaturas, "
                        "reduzir saídas, adiar compras. O mais recomendado.\n\n"
                        "**2. Aumentar a renda** — hora extra, serviço adicional, "
                        "venda de itens. Nem sempre é imediato.\n\n"
                        "**3. Usar crédito** — apenas como último recurso e para "
                        "necessidades, nunca para desejos. Cria custo futuro.\n\n"
                        "**O erro a evitar:** usar crédito para desejos quando "
                        "o orçamento já é negativo. "
                        "O déficit do mês se transforma em dívida com juros, "
                        "e o próximo mês começa ainda mais difícil."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 2.3 — Gastos invisíveis (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Gastos invisíveis",
            "description": (
                "Identifique cobranças recorrentes que passam despercebidas, "
                "calcule seu impacto acumulado e diferencie-as de gastos essenciais "
                "e discricionários."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.3.1",
                    "name": "Identificar gastos invisíveis no orçamento",
                    "description": (
                        "Reconhece cobranças recorrentes automáticas que passam "
                        "despercebidas no extrato bancário por serem de baixo valor "
                        "unitário ou por terem sido esquecidas após a contratação."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.3.2",
                    "name": "Calcular o impacto acumulado de pequenas despesas recorrentes",
                    "description": (
                        "Multiplica o valor mensal pelo número de meses para estimar "
                        "o custo anual de cada gasto invisível e o total do conjunto."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.3.3",
                    "name": "Diferenciar gastos invisíveis de gastos essenciais e discricionários",
                    "description": (
                        "Classifica cada despesa em essencial (moradia, alimentação, saúde), "
                        "discricionária (lazer, estilo de vida) ou invisível "
                        "(automática, esquecida ou subutilizada)."
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
                            "O que melhor define um 'gasto invisível' no orçamento pessoal?"
                        ),
                        "competency_codes": ["2.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Uma despesa recorrente e automática que passou a ser "
                                    "ignorada ou esquecida após a contratação."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Qualquer compra feita no débito em vez do crédito.",
                            },
                            {
                                "value": "c",
                                "label": "Gastos em dinheiro vivo que não aparecem no extrato.",
                            },
                            {
                                "value": "d",
                                "label": "Despesas essenciais como aluguel e alimentação.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Gastos invisíveis são cobranças automáticas "
                            "— assinaturas, anuidades, planos — que continuam debitando "
                            "mesmo depois que paramos de usar ou de notar o serviço. "
                            "Individualmente são pequenos, mas somados pesam no orçamento."
                        ),
                        "feedback_incorrect": (
                            "Gastos invisíveis não têm relação com a forma de pagamento "
                            "ou com a categoria do gasto. São despesas recorrentes "
                            "e automáticas que caem no esquecimento — como uma assinatura "
                            "de streaming que você não usa mais, ou uma anuidade de cartão "
                            "sub-rogada automaticamente todo ano."
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
                            "Marina paga R$ 29,90/mês por uma assinatura de revista digital "
                            "que não acessa há 8 meses. Qual foi o custo invisível acumulado "
                            "nesses 8 meses? (Valor fictício, para fins didáticos.)"
                        ),
                        "competency_codes": ["2.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 239,20 (R$ 29,90 × 8 meses)."},
                            {"value": "b", "label": "R$ 29,90 (apenas um mês)."},
                            {"value": "c", "label": "R$ 358,80 (R$ 29,90 × 12 meses)."},
                            {"value": "d", "label": "R$ 119,60 (R$ 29,90 × 4 meses)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! R$ 29,90 × 8 = R$ 239,20 gastos sem utilizar o serviço. "
                            "Multiplicar o valor mensal pelo período de não uso evidencia "
                            "o impacto real de um gasto esquecido."
                        ),
                        "feedback_incorrect": (
                            "O custo acumulado é simples: valor mensal × meses não utilizados. "
                            "R$ 29,90 × 8 = R$ 239,20. "
                            "Essa conta revela quanto dinheiro foi desperdiçado "
                            "enquanto a assinatura ficou ativa sem uso."
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
                            "Qual das alternativas abaixo é um exemplo típico de "
                            "gasto invisível — e NÃO de gasto essencial?"
                        ),
                        "competency_codes": ["2.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Anuidade de cartão de crédito cobrada automaticamente "
                                    "por um cartão que a pessoa raramente usa."
                                ),
                            },
                            {"value": "b", "label": "Conta de água e esgoto."},
                            {"value": "c", "label": "Plano de saúde familiar."},
                            {"value": "d", "label": "Aluguel do apartamento."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A anuidade de um cartão raramente usado é um gasto "
                            "invisível clássico: automático, esquecido e de baixo valor "
                            "unitário. Água, plano de saúde e aluguel são essenciais — "
                            "necessários à sobrevivência ou à qualidade de vida básica."
                        ),
                        "feedback_incorrect": (
                            "Água, plano de saúde e aluguel são gastos essenciais — "
                            "necessários e conscientes. A anuidade de cartão raramente usado "
                            "é invisível: cobrada automaticamente, muitas vezes sem que a "
                            "pessoa perceba que o serviço segue ativo."
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
                            "Pedro identificou 5 gastos invisíveis no extrato: "
                            "R$ 19,90 + R$ 29,90 + R$ 9,90 + R$ 34,90 + R$ 14,90 por mês. "
                            "Qual é o impacto anual total desses gastos? "
                            "(Valores fictícios, para fins didáticos.)"
                        ),
                        "competency_codes": ["2.3.2"],
                        "options": [
                            {"value": "a", "label": "R$ 1.312,80 (R$ 109,50 × 12 meses)."},
                            {"value": "b", "label": "R$ 109,50 (soma mensal apenas)."},
                            {"value": "c", "label": "R$ 656,40 (R$ 109,50 × 6 meses)."},
                            {"value": "d", "label": "R$ 1.194,00 (R$ 99,50 × 12 meses)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Soma mensal: 19,90 + 29,90 + 9,90 + 34,90 + 14,90 "
                            "= R$ 109,50. Anual: R$ 109,50 × 12 = **R$ 1.312,80**. "
                            "Mais de R$ 1.300 por ano em serviços potencialmente subutilizados."
                        ),
                        "feedback_incorrect": (
                            "Passo 1 — some os valores mensais: "
                            "19,90 + 29,90 + 9,90 + 34,90 + 14,90 = R$ 109,50/mês. "
                            "Passo 2 — multiplique por 12: "
                            "R$ 109,50 × 12 = R$ 1.312,80/ano. "
                            "Visualizar o custo anual torna o impacto muito mais evidente."
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
                            "Pense no seu próprio extrato bancário ou fatura de cartão. "
                            "Liste pelo menos dois serviços recorrentes que você suspeita "
                            "serem gastos invisíveis (ou pouco usados) e explique como "
                            "você decidiria se deve cancelá-los ou mantê-los."
                        ),
                        "competency_codes": ["2.3.1", "2.3.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Para decidir sobre um gasto recorrente, considere:\n"
                            "1. Você usou esse serviço nos últimos 30 dias?\n"
                            "2. O custo anual (mensal × 12) vale o benefício recebido?\n"
                            "3. Ele é essencial, discricionário ou realmente invisível?\n\n"
                            "Se for invisível e subutilizado, cancele. "
                            "Se for discricionário mas trouxer valor real, avalie se cabe no orçamento."
                        ),
                        "evaluation_criteria": [
                            "Identifica ao menos dois serviços recorrentes concretos.",
                            "Aplica algum critério de uso ou valor para justificar a decisão.",
                            "Diferencia conscientemente o que é útil do que é esquecido.",
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
                            "Você recebeu o extrato mensal de Camila e encontrou "
                            "8 cobranças recorrentes pequenas.\n\n"
                            "**Extrato de Camila (fictício):**\n"
                            "1. Streaming de vídeo A: R$ 39,90/mês — usa diariamente\n"
                            "2. Streaming de música B: R$ 21,90/mês — usa ocasionalmente\n"
                            "3. App de meditação C: R$ 19,90/mês — último acesso: 4 meses atrás\n"
                            "4. Anuidade cartão D: R$ 25,00/mês — cartão na gaveta há 6 meses\n"
                            "5. Backup em nuvem E: R$ 14,90/mês — nunca configurado\n"
                            "6. Jornal digital F: R$ 29,90/mês — lê toda semana\n"
                            "7. VPN G: R$ 17,90/mês — usada uma vez há 5 meses\n"
                            "8. Clube de descontos H: R$ 12,90/mês — nunca usou o app\n\n"
                            "Quais cobranças são claramente 'invisíveis' (esquecidas/subutilizadas) "
                            "e devem ser canceladas primeiro?"
                        ),
                        "competency_codes": ["2.3.1", "2.3.2", "2.3.3"],
                        "scenario": (
                            "Extrato mensal fictício de Camila com 8 cobranças recorrentes. "
                            "Algumas são utilizadas regularmente; outras estão ativas mas "
                            "esquecidas há meses. Objetivo: identificar os gastos invisíveis "
                            "prioritários para cancelamento e calcular a economia mensal resultante."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Cancelar app de meditação C, anuidade cartão D, "
                                    "backup em nuvem E, VPN G e clube de descontos H — "
                                    "todos sem uso recente. Economia: R$ 90,60/mês."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Cancelar apenas o streaming de música B (R$ 21,90) "
                                    "por ser de uso ocasional."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Cancelar streaming de vídeo A e jornal digital F "
                                    "para economizar mais, mesmo sendo usados regularmente."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não cancelar nada — o valor unitário de cada "
                                    "cobrança é pequeno demais para fazer diferença."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Excelente análise! Os 5 serviços sem uso recente "
                            "(app meditação, cartão na gaveta, backup não configurado, "
                            "VPN usada uma vez, clube nunca acessado) somam R$ 90,60/mês "
                            "= **R$ 1.087,20/ano** — dinheiro que sai sem retorno. "
                            "Streaming A e jornal F são usados regularmente: mantê-los é racional. "
                            "Streaming B (ocasional) pode ser reavaliado separadamente."
                        ),
                        "feedback_incorrect": (
                            "A chave é o critério de uso real, não o valor unitário. "
                            "Streaming A (diário) e jornal F (semanal) têm uso claro — mantenha. "
                            "App de meditação C (4 meses sem acesso), cartão D (na gaveta 6 meses), "
                            "backup E (nunca configurado), VPN G (usada uma vez há 5 meses) e "
                            "clube H (nunca acessou o app) são invisíveis clássicos. "
                            "Juntos: R$ 90,60/mês = R$ 1.087,20/ano em desperdício."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que são gastos invisíveis e por que eles crescem",
                    "order": 1,
                    "body": (
                        "**Gastos invisíveis** são cobranças recorrentes automáticas "
                        "que passaram a ser ignoradas depois que o serviço foi contratado. "
                        "São chamados de invisíveis porque:\n\n"
                        "- O débito ocorre todo mês sem ação do consumidor\n"
                        "- O valor unitário é pequeno (R$ 9 a R$ 50), dificultando "
                        "a percepção do impacto\n"
                        "- O serviço muitas vezes deixa de ser usado, mas a cobrança continua\n\n"
                        "**Exemplos comuns:**\n"
                        "- Assinaturas de streaming não utilizadas\n"
                        "- Anuidades de cartões pouco usados\n"
                        "- Apps com plano pago que caiu no esquecimento\n"
                        "- Planos de telefonia com recursos não utilizados\n"
                        "- Clubes de assinatura sem uso do app\n\n"
                        "O problema não é a existência desses gastos, mas a **ausência "
                        "de revisão periódica**. Uma vez identificados, é simples decidir "
                        "entre manter, renegociar ou cancelar."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Extrato de Renata: R$ 1.428/ano em gastos invisíveis (fictício)",
                    "order": 2,
                    "body": (
                        "**Renata revisou seu extrato e encontrou (valores fictícios):**\n\n"
                        "| Serviço | Valor/mês | Último uso | Decisão |\n"
                        "|---|---|---|---|\n"
                        "| Streaming de séries | R$ 45,90 | Hoje | Manter |\n"
                        "| App de academia virtual | R$ 39,90 | 5 meses atrás | **Cancelar** |\n"
                        "| Anuidade cartão extra | R$ 28,00 | Cartão na gaveta | **Cancelar** |\n"
                        "| Jornal digital | R$ 19,90 | Diariamente | Manter |\n"
                        "| VPN esquecida | R$ 17,90 | 7 meses atrás | **Cancelar** |\n"
                        "| Backup em nuvem | R$ 13,20 | Nunca acessou | **Cancelar** |\n\n"
                        "**Cancelamentos:** R$ 99,00/mês = **R$ 1.188,00/ano**\n\n"
                        "Com esse dinheiro, Renata poderia construir sua reserva de emergência "
                        "em menos de 6 meses.\n\n"
                        "*(Valores e serviços são fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como fazer uma faxina financeira de gastos invisíveis",
                    "order": 3,
                    "body": (
                        "Faça essa revisão a cada 3 meses:\n\n"
                        "1. **Baixe o extrato** bancário e a fatura do cartão do último mês\n"
                        "2. **Marque toda cobrança recorrente** — mesmo as pequenas\n"
                        "3. **Pergunte para cada uma:** 'Usei isso nos últimos 30 dias?'\n"
                        "4. **Calcule o custo anual** (mensal × 12) para visualizar o impacto real\n"
                        "5. **Classifique:** essencial, discricionário útil ou invisível\n"
                        "6. **Cancele ou negocie** os que são invisíveis\n\n"
                        "Aplicativos de gestão financeira (como Mobills, Organizze ou Guiabolso) "
                        "podem identificar padrões recorrentes automaticamente, facilitando a revisão."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 2.4 — Controle de despesas (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Controle de despesas",
            "description": (
                "Registre e categorize despesas mensais, compare o realizado com o "
                "planejado e identifique desvios para propor ajustes realistas no orçamento."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.4.1",
                    "name": "Registrar e categorizar despesas mensais",
                    "description": (
                        "Organiza os gastos reais do mês em categorias (moradia, "
                        "alimentação, transporte, lazer etc.) para ter uma visão "
                        "estruturada do que foi gasto."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.4.2",
                    "name": "Comparar despesas realizadas com o orçamento planejado",
                    "description": (
                        "Calcula a diferença entre o valor planejado e o realizado "
                        "em cada categoria, identificando superávits e déficits."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.4.3",
                    "name": "Identificar desvios e propor ajustes realistas",
                    "description": (
                        "Analisa as categorias com maior desvio positivo e sugere "
                        "ações concretas e viáveis para realinhar o orçamento."
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
                            "Por que categorizar as despesas mensais é importante "
                            "para o controle financeiro?"
                        ),
                        "competency_codes": ["2.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Permite identificar padrões de gasto, comparar com "
                                    "o planejado e encontrar onde há desperdício ou desvio."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "É exigido pelo banco para liberar crédito.",
                            },
                            {
                                "value": "c",
                                "label": "Reduz automaticamente os gastos sem nenhuma ação adicional.",
                            },
                            {
                                "value": "d",
                                "label": "Serve apenas para fins de declaração de imposto de renda.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Categorizar despesas transforma números soltos em "
                            "informação útil: você vê onde o dinheiro foi, compara com "
                            "o que planejou e decide onde ajustar. Sem categorização, "
                            "o orçamento é só uma intenção."
                        ),
                        "feedback_incorrect": (
                            "Categorizar despesas não é uma obrigação burocrática. "
                            "É uma ferramenta de análise: permite ver padrões, "
                            "comparar planejado × realizado e identificar onde há "
                            "desvio — sem isso, não há controle real."
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
                            "Julia planejou R$ 600 para alimentação e gastou R$ 780 no mês. "
                            "Como se classifica esse resultado na comparação orçado × realizado? "
                            "(Valores fictícios.)"
                        ),
                        "competency_codes": ["2.4.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Desvio positivo de R$ 180 — a categoria estourou o orçamento.",
                            },
                            {
                                "value": "b",
                                "label": "Superávit de R$ 180 — sobrou dinheiro na categoria.",
                            },
                            {
                                "value": "c",
                                "label": "Desvio neutro — a diferença é menor que 20%.",
                            },
                            {
                                "value": "d",
                                "label": "Não é possível calcular sem saber o salário.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! R$ 780 − R$ 600 = **R$ 180 de desvio positivo** "
                            "(gasto acima do planejado). A categoria alimentação estourou "
                            "o orçamento em 30%. Esse desvio precisa ser investigado: "
                            "foi eventual ou é recorrente?"
                        ),
                        "feedback_incorrect": (
                            "Desvio = realizado − planejado. "
                            "R$ 780 − R$ 600 = R$ 180 acima do orçado. "
                            "Quando o realizado supera o planejado, a categoria estourou — "
                            "isso não é superávit, é déficit na categoria."
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
                            "Ao revisar o orçamento de março, Luís percebeu que gastou "
                            "R$ 340 em lazer (planejado: R$ 200) e R$ 520 em "
                            "alimentação fora de casa (planejado: R$ 350). "
                            "Qual ajuste é mais realista para abril? "
                            "(Valores fictícios.)"
                        ),
                        "competency_codes": ["2.4.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Reduzir lazer de R$ 340 para R$ 250 e alimentação "
                                    "fora de R$ 520 para R$ 420 — ajustes graduais e viáveis."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Cortar lazer a R$ 0 e alimentação fora a R$ 0 "
                                    "para compensar o desvio de uma vez."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Não fazer nada — desvios acontecem todo mês.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Aumentar o orçamento dessas categorias para "
                                    "R$ 400 e R$ 600, respectivamente, sem revisar os hábitos."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Ótima escolha! Ajustes graduais são mais sustentáveis do que "
                            "cortes radicais. Reduzir lazer de R$ 340 para R$ 250 e "
                            "alimentação fora de R$ 520 para R$ 420 é exigente mas viável — "
                            "sem tornar o orçamento punitivo e abandonável."
                        ),
                        "feedback_incorrect": (
                            "Ajustes realistas são progressivos. Zerar uma categoria de "
                            "uma vez raramente funciona: a pressão leva ao abandono do orçamento. "
                            "Aumentar o orçado sem mudar hábitos apenas normaliza o desvio. "
                            "O caminho é reduzir gradualmente, chegando ao valor desejado em 2–3 meses."
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
                            "Fernanda tem renda de R$ 3.200/mês e planeja destinar "
                            "R$ 800 para poupança. No mês passado, as despesas somaram "
                            "R$ 2.900 — R$ 350 acima do planejado. "
                            "Qual é o impacto desse desvio na poupança? "
                            "(Valores fictícios.)"
                        ),
                        "competency_codes": ["2.4.2", "2.4.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A poupança cai de R$ 800 para R$ 300 — "
                                    "o desvio de R$ 350 sai diretamente do que sobra."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Nenhum — poupança e despesas são independentes.",
                            },
                            {
                                "value": "c",
                                "label": "A poupança aumenta, porque o desvio foi inevitável.",
                            },
                            {
                                "value": "d",
                                "label": "A poupança cai exatamente para zero.",
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Renda − despesas = sobra para poupança. "
                            "R$ 3.200 − R$ 2.900 = R$ 300 poupados em vez de R$ 800. "
                            "O desvio de R$ 350 nas despesas consumiu R$ 500 da poupança planejada. "
                            "Controlar despesas é, diretamente, proteger a poupança."
                        ),
                        "feedback_incorrect": (
                            "Poupança = renda − despesas. "
                            "Se as despesas sobem sem que a renda suba, a poupança cai. "
                            "R$ 3.200 − R$ 2.900 = R$ 300 — bem abaixo dos R$ 800 planejados. "
                            "O desvio nas despesas se converte diretamente em menos poupança."
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
                            "Imagine que você está no fim de um mês e percebeu que "
                            "gastou R$ 200 a mais do que planejou na categoria 'alimentação'.\n\n"
                            "1. Cite uma possível causa desse desvio.\n"
                            "2. Proponha um ajuste concreto e realista para o próximo mês "
                            "nessa categoria."
                        ),
                        "competency_codes": ["2.4.2", "2.4.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Causas comuns para desvio em alimentação:\n"
                            "- Refeições fora de casa mais frequentes do que o planejado\n"
                            "- Compras de supermercado sem lista, gerando itens desnecessários\n"
                            "- Delivery concentrado nos fins de semana\n\n"
                            "Ajustes realistas:\n"
                            "- Planejar o cardápio semanal antes de ir ao mercado\n"
                            "- Estabelecer um número máximo de refeições fora por semana\n"
                            "- Definir um limite de pedidos de delivery por mês\n\n"
                            "O importante é que o ajuste seja específico e viável — "
                            "não apenas 'gastar menos'."
                        ),
                        "evaluation_criteria": [
                            "Identifica uma causa plausível e específica para o desvio.",
                            "Propõe um ajuste concreto (não genérico como 'gastar menos').",
                            "O ajuste proposto é realista e compatível com a rotina.",
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
                            "Você é o consultor financeiro de Bruno. "
                            "Abaixo está o orçamento planejado e o realizado de março.\n\n"
                            "**Orçamento de Bruno — março (fictício):**\n\n"
                            "| Categoria | Planejado | Realizado | Desvio |\n"
                            "|---|---|---|---|\n"
                            "| Moradia (aluguel + cond.) | R$ 1.200 | R$ 1.200 | R$ 0 |\n"
                            "| Alimentação supermercado | R$ 500 | R$ 680 | +R$ 180 |\n"
                            "| Transporte | R$ 300 | R$ 310 | +R$ 10 |\n"
                            "| Refeições fora/delivery | R$ 250 | R$ 490 | +R$ 240 |\n"
                            "| Lazer/entretenimento | R$ 200 | R$ 370 | +R$ 170 |\n"
                            "| Roupas/beleza | R$ 150 | R$ 290 | +R$ 140 |\n"
                            "| Poupança planejada | R$ 400 | R$ 0 | −R$ 400 |\n\n"
                            "Renda mensal de Bruno: R$ 3.000.\n\n"
                            "Quais são as 3 categorias com maior desvio "
                            "e qual ação Bruno deve priorizar em abril?"
                        ),
                        "competency_codes": ["2.4.2", "2.4.3"],
                        "scenario": (
                            "Orçamento mensal fictício de Bruno com renda de R$ 3.000. "
                            "As despesas totalizaram R$ 3.340 — R$ 340 acima da renda — "
                            "zerando a poupança e gerando déficit. "
                            "Três categorias concentram os maiores desvios."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Refeições fora (+R$ 240), lazer (+R$ 170) e "
                                    "alimentação supermercado (+R$ 180) são as 3 maiores. "
                                    "Prioridade: limitar delivery a 2x/semana, "
                                    "definir teto de lazer em R$ 280 e fazer lista antes "
                                    "do mercado — economizando ~R$ 420/mês para retomar a poupança."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Cortar roupas/beleza a R$ 0 e lazer a R$ 0 — "
                                    "são os gastos mais 'supérfluos'."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Aumentar a renda de Bruno — os desvios são "
                                    "inevitáveis com o salário atual."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Eliminar a poupança do orçamento e redistribuir "
                                    "os R$ 400 entre as categorias que estouraram."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Análise certeira! As 3 maiores categorias em desvio são "
                            "refeições fora (+R$ 240), alimentação supermercado (+R$ 180) "
                            "e lazer (+R$ 170). Juntas somam R$ 590 de desvio. "
                            "Ajustes graduais nessas três — sem cortes radicais — "
                            "são suficientes para recuperar a poupança e fechar o mês no azul.\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                        "feedback_incorrect": (
                            "Cortar tudo de vez raramente é sustentável — o orçamento "
                            "vira uma punição e é abandonado. Eliminar a poupança do "
                            "orçamento normaliza o problema em vez de resolvê-lo.\n\n"
                            "As categorias prioritárias são as de maior desvio absoluto: "
                            "refeições fora (+R$ 240), supermercado (+R$ 180) e lazer (+R$ 170). "
                            "Ajustes graduais nessas três são suficientes para fechar o mês "
                            "sem déficit e retomar a poupança.\n\n"
                            "*(Valores fictícios, para fins didáticos.)*"
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Por que registrar despesas muda o comportamento financeiro",
                    "order": 1,
                    "body": (
                        "**Registrar despesas** é o primeiro passo do controle financeiro real. "
                        "Sem registro, o orçamento é apenas intenção.\n\n"
                        "**O que o registro permite:**\n"
                        "- Ver onde o dinheiro realmente foi — não onde você acha que foi\n"
                        "- Comparar o realizado com o planejado em cada categoria\n"
                        "- Identificar padrões recorrentes de desvio\n"
                        "- Tomar decisões baseadas em dados, não em impressões\n\n"
                        "**Como registrar:**\n"
                        "- Planilha simples (Excel, Google Sheets) com data, valor, categoria\n"
                        "- App de finanças pessoais (Mobills, Organizze, Minhas Economias)\n"
                        "- Revisão semanal do extrato bancário e da fatura do cartão\n\n"
                        "O hábito de registrar, mesmo por 15 minutos semanais, "
                        "transforma a relação com o dinheiro em poucas semanas."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Comparativo planejado × realizado de Carla — abril (fictício)",
                    "order": 2,
                    "body": (
                        "**Renda de Carla: R$ 2.800/mês (fictício)**\n\n"
                        "| Categoria | Planejado | Realizado | Desvio |\n"
                        "|---|---|---|---|\n"
                        "| Aluguel | R$ 900 | R$ 900 | R$ 0 |\n"
                        "| Alimentação | R$ 450 | R$ 510 | +R$ 60 |\n"
                        "| Transporte | R$ 250 | R$ 240 | −R$ 10 |\n"
                        "| Saúde | R$ 150 | R$ 150 | R$ 0 |\n"
                        "| Lazer | R$ 200 | R$ 320 | +R$ 120 |\n"
                        "| Outros | R$ 150 | R$ 190 | +R$ 40 |\n"
                        "| Poupança | R$ 300 | R$ 190 | −R$ 110 |\n\n"
                        "**Desvio total:** +R$ 210 acima do planejado → poupança caiu para R$ 190.\n\n"
                        "**Análise de Carla:** lazer (+R$ 120) foi o principal desvio. "
                        "Em maio, ela definiu um teto de R$ 250 para lazer "
                        "e planejou 2 saídas a menos no mês.\n\n"
                        "*(Valores fictícios, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Regra prática para desvios: ajuste gradual, não corte radical",
                    "order": 3,
                    "body": (
                        "Quando uma categoria estoura o orçamento, evite dois extremos:\n\n"
                        "❌ **Cortar para zero:** 'Não vou mais comer fora.' "
                        "Irrealista — dura poucos dias e gera culpa.\n\n"
                        "❌ **Ignorar:** 'Todo mês é assim.' "
                        "Normaliza o desvio e impede o crescimento financeiro.\n\n"
                        "✅ **Ajuste gradual:** reduza a categoria em 20–30% a cada mês "
                        "até atingir o valor desejado.\n\n"
                        "**Exemplo:** se você gastou R$ 490 em delivery e quer chegar a R$ 250:\n"
                        "- Mês 1: reduzir para R$ 380\n"
                        "- Mês 2: reduzir para R$ 310\n"
                        "- Mês 3: chegar a R$ 250\n\n"
                        "Esse ritmo é sustentável e transforma o hábito de forma permanente."
                    ),
                },
            ],
        },
    ],
}
