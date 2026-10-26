"""Conteúdo versionado da Fase 2 — Seu dinheiro no digital.

Fonte editorial: docs/fases/fase-2-seu-dinheiro-no-digital.md
Migration: 0003_phase_2_content.py
"""

PHASE_2_V1 = {
    "phase_number": 2,
    "missions": [
        # ─────────────────────────────────────────────
        # Missão 2.1 — Como vou pagar?
        # ─────────────────────────────────────────────
        {
            "number": 1,
            "name": "Como vou pagar?",
            "description": (
                "Compare Pix, débito e crédito e escolha o meio de pagamento "
                "mais adequado para cada situação."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.1.1",
                    "name": "Explicar como funcionam Pix, débito e crédito",
                    "description": (
                        "Descreve as diferenças entre os três meios de pagamento: "
                        "Pix (instantâneo, irreversível), débito (sai na hora) e "
                        "crédito (paga depois, na fatura)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.1.2",
                    "name": "Escolher o meio de pagamento adequado à situação",
                    "description": (
                        "Avalia o meio de pagamento considerando o valor, o orçamento "
                        "disponível e as consequências de cada escolha."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.1.3",
                    "name": "Reconhecer que o Pix concluído não pode ser cancelado",
                    "description": (
                        "Entende que o Pix é irreversível e que a devolução depende "
                        "do recebedor, diferentemente de uma contestação de cartão."
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
                        "prompt": "Qual alternativa descreve melhor o cartão de crédito?",
                        "competency_codes": ["2.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "O valor da compra sai direto da sua conta, na hora.",
                            },
                            {
                                "value": "b",
                                "label": "É dinheiro extra que o banco dá de presente.",
                            },
                            {
                                "value": "c",
                                "label": "O banco paga a compra agora e você paga depois, na fatura.",
                            },
                            {
                                "value": "d",
                                "label": "Só funciona para compras parceladas.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! No crédito, o banco paga a loja e você paga depois, "
                            "na fatura. Por isso ele não é dinheiro extra: é uma compra "
                            "que você vai pagar no futuro."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. No crédito, o banco paga a compra agora e "
                            "você paga depois, na fatura. O valor só sai direto da conta "
                            "no débito e no Pix."
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
                            "Você fez um Pix de R$ 80 para a chave errada, por distração. "
                            "O que é verdade?"
                        ),
                        "competency_codes": ["2.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Dá para cancelar o Pix pelo aplicativo em até 24 horas.",
                            },
                            {
                                "value": "b",
                                "label": "O banco é obrigado a devolver o valor sempre.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "O Pix concluído não se cancela como uma compra; a "
                                    "devolução depende do recebedor, e o mecanismo de "
                                    "devolução para golpes não vale para erro do próprio pagador."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "O Pix errado é devolvido automaticamente em alguns dias.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Um Pix concluído não pode ser cancelado. Quando o "
                            "erro foi seu, a devolução depende de o recebedor aceitar "
                            "devolver. Por isso é tão importante conferir antes de confirmar."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O Pix concluído não pode ser cancelado, e "
                            "não há devolução automática. Quando o erro é do próprio "
                            "pagador, a devolução depende do recebedor."
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
                            "Uma loja vende uma geladeira por R$ 1.200 à vista ou em "
                            "4x de R$ 300 sem juros. Depois das despesas essenciais, "
                            "sobram R$ 700 por mês para você, e sua fatura de cartão "
                            "hoje está zerada. Qual análise é mais adequada?"
                        ),
                        "competency_codes": ["2.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Parcelar em 4x é razoável: a parcela de R$ 300 cabe "
                                    "no que sobra e não há juros, desde que eu pague a "
                                    "fatura inteira todo mês."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Parcelar é sempre pior do que pagar à vista.",
                            },
                            {
                                "value": "c",
                                "label": "Não importa o valor da parcela, desde que seja sem juros.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "O ideal é pagar só o mínimo da fatura para sobrar "
                                    "mais dinheiro."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Boa análise! Sem juros e com a parcela cabendo no orçamento, "
                            "o parcelamento é razoável. O cuidado é pagar a fatura inteira, "
                            "sempre."
                        ),
                        "feedback_incorrect": (
                            "Revise a análise. Sem juros e com a parcela cabendo no "
                            "orçamento, parcelar é razoável. Mas a parcela precisa caber "
                            "no que sobra, e a fatura deve ser paga por inteiro: pagar só "
                            "o mínimo gera juros."
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
                            "Pense nas últimas compras que você fez. Que meio de pagamento "
                            "você usou em cada uma (Pix, débito ou crédito) e por quê? "
                            "Você escolheria diferente hoje?"
                        ),
                        "competency_codes": ["2.1.1", "2.1.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado quando a integração de IA estiver "
                            "disponível. Enquanto isso, reflita se você identificou a "
                            "diferença entre pagar agora (Pix e débito) e pagar depois "
                            "(crédito)."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona um meio de pagamento e o motivo da escolha "
                                "(conveniência, controle do gasto, prazo etc.)."
                            ),
                            (
                                "Reconhece que o crédito é pagar depois e exige "
                                "planejamento."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Três jeitos de pagar",
                    "order": 1,
                    "body": (
                        "- **Pix:** transferência instantânea, que funciona 24 horas "
                        "por dia, todos os dias, e em geral sem custo para pessoas "
                        "físicas. O dinheiro sai da sua conta e chega à conta do "
                        "recebedor em segundos. Depois de confirmado, **não dá para "
                        "cancelar**.\n"
                        "- **Débito:** o valor da compra sai da sua conta na hora. "
                        "Você só gasta o que tem.\n"
                        "- **Crédito:** o banco paga a loja agora e **você paga "
                        "depois**, na fatura do cartão. Dá para parcelar. Se você "
                        "pagar a fatura inteira no vencimento, não há juros; se não "
                        "pagar, a dívida cresce.\n\n"
                        "O crédito não é dinheiro extra: é um **compromisso futuro** "
                        "que vai sair do seu orçamento dos próximos meses."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Três situações do dia a dia",
                    "order": 2,
                    "body": (
                        "1. **Padaria, R$ 18:** débito ou Pix. É um valor pequeno, "
                        "que já cabe no dinheiro que você tem na conta hoje.\n"
                        "2. **Geladeira de R$ 1.200, em 4x de R$ 300 sem juros:** "
                        "o crédito pode fazer sentido se a parcela de R$ 300 couber "
                        "no orçamento dos próximos 4 meses e você pagar a fatura "
                        "inteira todo mês.\n"
                        "3. **Aluguel pago ao proprietário:** Pix, conferindo o nome "
                        "do recebedor antes de confirmar. Se o Pix for para a pessoa "
                        "errada, a devolução depende de quem recebeu."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Antes de escolher, pergunte",
                    "order": 3,
                    "body": (
                        "\"Eu tenho esse dinheiro agora? Se não tenho, de onde ele vai "
                        "sair nos próximos meses?\" Essa pergunta ajuda a diferenciar "
                        "o que cabe no seu bolso hoje do que só parece caber."
                    ),
                },
            ],
        },
        # ─────────────────────────────────────────────
        # Missão 2.2 — Entendendo o cartão
        # ─────────────────────────────────────────────
        {
            "number": 2,
            "name": "Entendendo o cartão",
            "description": (
                "Entenda limite, fechamento, vencimento e fatura, e saiba o que "
                "acontece quando você paga só uma parte."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.2.1",
                    "name": "Explicar limite, fatura, fechamento e vencimento",
                    "description": (
                        "Define corretamente cada conceito: limite (teto de uso), "
                        "fatura (soma do ciclo), fechamento (fim do ciclo) e "
                        "vencimento (prazo de pagamento)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.2.2",
                    "name": "Prever em qual fatura uma compra vai cair",
                    "description": (
                        "Identifica se uma compra entra na fatura atual ou na "
                        "seguinte com base na data de fechamento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.2.3",
                    "name": "Reconhecer as consequências de pagar só parte da fatura",
                    "description": (
                        "Entende que o valor não pago vira dívida com juros e "
                        "encargos, e não há período sem custo para o restante."
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
                        "prompt": "O que é o limite do cartão de crédito?",
                        "competency_codes": ["2.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Um valor extra de renda que o banco oferece todo mês.",
                            },
                            {
                                "value": "b",
                                "label": "O valor máximo que o emissor permite você usar no cartão.",
                            },
                            {
                                "value": "c",
                                "label": "O valor mínimo que você precisa pagar na fatura.",
                            },
                            {
                                "value": "d",
                                "label": "O dinheiro que você já tem guardado no banco.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! O limite é o teto do que você pode usar. Ele não é "
                            "renda nem dinheiro seu: tudo o que você usar vai ter que "
                            "ser pago na fatura."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O limite é o valor máximo que o emissor "
                            "permite você usar. Não é renda extra: o que você gastar "
                            "precisa ser pago depois."
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
                            "Seu cartão fecha dia 10 e vence dia 17. Você faz uma compra "
                            "no dia 12 de outubro. Em qual vencimento ela será cobrada?"
                        ),
                        "competency_codes": ["2.2.2"],
                        "options": [
                            {"value": "a", "label": "17 de outubro."},
                            {"value": "b", "label": "17 de novembro."},
                            {"value": "c", "label": "10 de novembro."},
                            {"value": "d", "label": "12 de novembro."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A fatura de outubro fechou dia 10. A compra do "
                            "dia 12 entra na fatura que fecha em 10 de novembro e vence "
                            "em 17 de novembro."
                        ),
                        "feedback_incorrect": (
                            "Não foi dessa vez. Compras feitas depois do fechamento "
                            "(dia 10) entram na fatura seguinte. A compra do dia 12 de "
                            "outubro vence só em 17 de novembro."
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
                            "Sua fatura de R$ 800 vence hoje e você só consegue pagar "
                            "R$ 200. O que acontece com os R$ 600 restantes?"
                        ),
                        "competency_codes": ["2.2.3"],
                        "options": [
                            {"value": "a", "label": "São perdoados pelo banco."},
                            {
                                "value": "b",
                                "label": "Ficam congelados, sem custo, até o mês seguinte.",
                            },
                            {
                                "value": "c",
                                "label": "São descontados do limite, sem juros.",
                            },
                            {
                                "value": "d",
                                "label": "Viram dívida com juros e encargos, que fazem o valor crescer.",
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Isso mesmo! O que sobra da fatura vira dívida com juros e "
                            "encargos. Mesmo com o teto legal para esses juros, o custo "
                            "é alto e o valor cresce."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O valor que não foi pago vira dívida com "
                            "juros e encargos. Não existe perdão nem período sem custo "
                            "para a parte não paga."
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
                            "Explique com as suas palavras a diferença entre o fechamento "
                            "e o vencimento da fatura, e por que conhecer as duas datas "
                            "ajuda a planejar suas compras."
                        ),
                        "competency_codes": ["2.2.1", "2.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado quando a integração de IA estiver "
                            "disponível. Enquanto isso, confira se você mencionou que o "
                            "fechamento define em qual fatura a compra entra e o "
                            "vencimento é o prazo de pagamento."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona que o fechamento é o fim do ciclo e define "
                                "em qual fatura a compra entra."
                            ),
                            "Menciona que o vencimento é a data-limite de pagamento.",
                            (
                                "Cita algum efeito no planejamento, como saber de qual "
                                "mês sairá o dinheiro."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Limite, fatura, fechamento e vencimento",
                    "order": 1,
                    "body": (
                        "- **Limite:** o valor máximo que o emissor do cartão permite "
                        "você usar. Ele **não é renda** e não é dinheiro seu.\n"
                        "- **Fatura:** a soma das compras feitas dentro de um ciclo.\n"
                        "- **Fechamento:** a data em que o ciclo termina. Compras feitas "
                        "depois dessa data entram na fatura seguinte.\n"
                        "- **Vencimento:** a data-limite para pagar a fatura.\n\n"
                        "Pagando o **valor total** até o vencimento, não há juros. "
                        "Pagando só uma parte, o restante vira dívida com juros e "
                        "encargos (rotativo ou parcelamento da fatura)."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Em qual fatura essa compra entra?",
                    "order": 2,
                    "body": (
                        "O cartão do Caio **fecha dia 10** e **vence dia 17**.\n\n"
                        "- Compra no **dia 8**: entra na fatura que fecha no dia 10 e "
                        "vence no dia 17 do mesmo mês.\n"
                        "- Compra no **dia 12**: o ciclo já fechou. Ela entra na fatura "
                        "que fecha no dia 10 do mês seguinte e vence no dia 17 do mês "
                        "seguinte.\n\n"
                        "Saber isso ajuda a planejar: a mesma compra pode sair do "
                        "orçamento deste mês ou do próximo."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Olhe o fechamento, não só o vencimento",
                    "order": 3,
                    "body": (
                        "Muita gente olha só o dia do vencimento. A data de fechamento "
                        "é que decide em qual fatura a compra cai. Conferir as duas "
                        "datas ajuda a evitar surpresas."
                    ),
                },
            ],
        },
        # ─────────────────────────────────────────────
        # Missão 2.3 — Antes de confirmar
        # ─────────────────────────────────────────────
        {
            "number": 3,
            "name": "Antes de confirmar",
            "description": (
                "Confira os dados antes de pagar e reconheça sinais de risco "
                "em pagamentos digitais."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "2.3.1",
                    "name": "Conferir recebedor, valor e origem antes de confirmar",
                    "description": (
                        "Verifica o nome do recebedor, o valor e se a solicitação "
                        "de pagamento partiu de si mesmo antes de confirmar."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.3.2",
                    "name": "Reconhecer sinais de risco em cobranças digitais",
                    "description": (
                        "Identifica sinais como pressa, link de número desconhecido, "
                        "desconto exagerado e pedido para pagar fora da plataforma."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "2.3.3",
                    "name": "Saber o que fazer ao suspeitar de fraude em Pix",
                    "description": (
                        "Conhece o procedimento de contestação no aplicativo do banco "
                        "e o registro de boletim de ocorrência."
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
                            "Você vai fazer um Pix para pagar o conserto de um aparelho. "
                            "Na tela de confirmação, o nome do recebedor é diferente do "
                            "nome da pessoa com quem você combinou o serviço. O que fazer?"
                        ),
                        "competency_codes": ["2.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Confirmar mesmo assim, porque a chave foi enviada por mensagem.",
                            },
                            {
                                "value": "b",
                                "label": "Confirmar e avisar a pessoa depois.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não confirmar e conferir os dados com a pessoa, "
                                    "por outro canal, antes de pagar."
                                ),
                            },
                            {
                                "value": "d",
                                "label": "Fazer um Pix de valor pequeno para testar.",
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Exato! Se o nome não bate, não confirme. Como o Pix não "
                            "pode ser cancelado, a conferência é a sua proteção."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Se o nome do recebedor não bate com o que "
                            "você esperava, não confirme. Confira os dados com a pessoa "
                            "por outro canal, porque depois de concluído o Pix não pode "
                            "ser cancelado."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual das situações abaixo tem mais sinais de risco?",
                        "competency_codes": ["2.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar a conta de luz com o código de barras "
                                    "dentro do aplicativo do seu banco."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar uma 'taxa de liberação de pacote' por um "
                                    "link enviado em mensagem de número desconhecido, "
                                    "com prazo de 1 hora."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Pagar uma compra em um site cujo endereço você mesmo digitou.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pagar a mensalidade da escola usando os dados do "
                                    "boleto que você recebeu em mãos."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Mensagem de número desconhecido, link de pagamento "
                            "e pressa de 1 hora são sinais clássicos de golpe."
                        ),
                        "feedback_incorrect": (
                            "Revise os sinais. Cobrança por link enviado por número "
                            "desconhecido, com prazo curto, é um sinal clássico de golpe. "
                            "As outras situações partem de você ou de dados que você já "
                            "conhece."
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
                            "Você percebeu que caiu em um golpe e fez um Pix há 1 hora. "
                            "Qual é a melhor atitude agora?"
                        ),
                        "competency_codes": ["2.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Esperar alguns dias para ver se o dinheiro volta sozinho.",
                            },
                            {
                                "value": "b",
                                "label": "Pedir ao golpista, pela conversa, que devolva o valor.",
                            },
                            {
                                "value": "c",
                                "label": "Apagar as mensagens para não ficar com raiva.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Acionar imediatamente o banco pelo aplicativo, "
                                    "contestar o Pix e registrar um boletim de ocorrência."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Muito bem! Agir rápido aumenta as chances de bloqueio. O "
                            "prazo para pedir o MED é de até 80 dias, mas não há garantia "
                            "de devolução, então cada hora conta."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O correto é avisar o banco na hora, usando a "
                            "contestação do Pix no aplicativo, e registrar um boletim de "
                            "ocorrência. Esperar ou negociar com o golpista só diminui as "
                            "chances de recuperar o dinheiro."
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
                            "Descreva um pagamento digital que você fez (ou faria). "
                            "Que conferências faria antes de confirmar?"
                        ),
                        "competency_codes": ["2.3.1", "2.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la e dar "
                            "um retorno personalizado quando a integração de IA estiver "
                            "disponível. Enquanto isso, confira se você mencionou pelo "
                            "menos duas verificações: nome do recebedor, valor e origem "
                            "do pedido."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona pelo menos duas conferências: nome do recebedor, "
                                "valor ou origem do pedido."
                            ),
                            (
                                "Reconhece que o Pix não pode ser cancelado depois de "
                                "confirmado."
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
                        "prompt": "Qual plano é o mais seguro para o mês?",
                        "scenario": (
                            "Você começa o mês com R$ 1.500 na conta. Até o fim do mês "
                            "precisa pagar o aluguel (R$ 600, por Pix, vence dia 5), o "
                            "mercado (R$ 300) e a fatura do cartão (R$ 250, vence dia 17). "
                            "No meio do mês, uma amiga chama você para jantar (R$ 120) e "
                            "você recebe, de um número desconhecido, um link com um fone "
                            "de R$ 200 e a mensagem 'Pix hoje com 40% de desconto'."
                        ),
                        "competency_codes": ["2.3.1", "2.3.2", "2.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pago o aluguel por Pix conferindo o recebedor, o "
                                    "mercado no débito e a fatura inteira no vencimento; "
                                    "janto no débito e ignoro o link do fone."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pago só o mínimo da fatura para sobrar mais e compro "
                                    "o fone pelo link, aproveitando o desconto."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pago o aluguel e o mercado no crédito para ganhar "
                                    "prazo e deixo a fatura para o mês seguinte."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Pago tudo, incluindo o fone pelo link, e deixo o "
                                    "jantar para outro mês."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Ótimo plano! Você conferiu o recebedor antes do Pix, pagou "
                            "a fatura inteira (sem juros) e ignorou uma oferta que chegou "
                            "por link de número desconhecido. Ao final do mês ainda "
                            "sobraram R$ 230 (1.500 − 600 − 300 − 250 − 120)."
                        ),
                        "feedback_incorrect": (
                            "Revise o plano. Pagar só o mínimo da fatura gera juros, "
                            "empurrar contas para o mês seguinte acumula dívida, e pagar "
                            "uma oferta enviada por link de número desconhecido é um sinal "
                            "clássico de golpe. O caminho seguro é pagar o essencial por "
                            "inteiro, conferir antes de confirmar e ignorar o link."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que conferir antes de confirmar",
                    "order": 1,
                    "body": (
                        "Como o Pix é imediato, a conferência acontece **antes** do "
                        "toque em \"confirmar\". Na tela de confirmação, olhe:\n\n"
                        "1. **O nome do recebedor:** bate com a pessoa ou empresa que "
                        "você quer pagar?\n"
                        "2. **O valor:** está correto?\n"
                        "3. **A origem do pedido:** foi você quem iniciou esse "
                        "pagamento, ou chegou uma mensagem pedindo?\n\n"
                        "Sinais de risco: pressa (\"só hoje\", \"em 30 minutos\"), "
                        "mensagem de número desconhecido, link pedindo pagamento, "
                        "desconto exagerado, pedido para pagar \"por fora\" da "
                        "plataforma, QR Code que parece colado sobre outro. E nunca "
                        "informe senha, código de verificação ou CVV a ninguém."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "\"Fiz um Pix por engano, pode devolver?\"",
                    "order": 2,
                    "body": (
                        "Você recebe uma mensagem: \"Fiz um Pix de R$ 500 para você "
                        "por engano, pode devolver?\"\n\n"
                        "O que fazer: primeiro, **confira no seu aplicativo** se o "
                        "valor realmente entrou. Se não entrou, ignore. Se entrou, "
                        "use a função **\"Devolver\"** ligada àquela transação, dentro "
                        "do próprio aplicativo do banco, em vez de fazer um novo Pix "
                        "manual para outra conta. Golpistas usam esse tipo de pedido "
                        "para tentar receber dinheiro por outro caminho."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Caiu em um golpe? Aja rápido",
                    "order": 3,
                    "body": (
                        "Se você fez um Pix e percebeu que era golpe, entre no "
                        "aplicativo do banco o quanto antes e use a opção de "
                        "contestação, para pedir a abertura do Mecanismo Especial de "
                        "Devolução (MED). O prazo para pedir é de até 80 dias, mas "
                        "quanto mais cedo, maiores as chances de o dinheiro ainda estar "
                        "disponível para bloqueio. Registre também um boletim de "
                        "ocorrência. Não há garantia de devolução."
                    ),
                },
            ],
        },
    ],
}
