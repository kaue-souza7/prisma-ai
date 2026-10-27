"""Trilha 3 — Pagamentos do dia a dia (missões novas + expansões).

phase_number: 3 (existente — não inserir nova fase)
Fonte editorial: docs/trilhas/trilha-03.md

Missões 1 e 3 são expansões (upsert sobre as existentes de phase_2_v1.py).
Missões 3 e 4 são novas.
O seeder usa upsert por chave natural — não duplica conteúdo existente.
"""

TRAIL_3_V1 = {
    "phase_number": 3,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 3.1 — Como vou pagar? (expansão sobre phase_2_v1 missão 1)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Como vou pagar?",
            "description": (
                "Compare Pix, débito e crédito: entenda o impacto de cada meio "
                "no saldo e no orçamento futuro."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.1.1",
                    "name": "Distinguir débito, crédito, Pix e pagamento por carteira digital",
                    "description": (
                        "Descreve o funcionamento de cada meio de pagamento: "
                        "Pix (instantâneo, irreversível), débito (sai imediatamente), "
                        "crédito (paga depois na fatura)."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.1.2",
                    "name": "Identificar o impacto de cada meio no saldo disponível e no orçamento",
                    "description": (
                        "Explica como cada meio afeta o saldo atual e o orçamento futuro: "
                        "débito e Pix reduzem o saldo imediatamente; "
                        "crédito compromete a renda futura na fatura."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.1.3",
                    "name": "Comparar prazo de compensação dos diferentes meios",
                    "description": (
                        "Identifica que Pix e débito compensam imediatamente, "
                        "enquanto boleto pode levar até 3 dias úteis."
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
                        "prompt": "Qual meio de pagamento desconta o dinheiro imediatamente da conta corrente?",
                        "competency_codes": ["3.1.1"],
                        "options": [
                            {"value": "a", "label": "Cartão de crédito."},
                            {"value": "b", "label": "Boleto bancário."},
                            {"value": "c", "label": "Débito."},
                            {"value": "d", "label": "Parcelamento no crédito."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O débito desconta imediatamente da conta corrente — "
                            "você precisa ter o saldo disponível. "
                            "O crédito só é cobrado na fatura (dias ou semanas depois). "
                            "O boleto pode levar até 3 dias úteis."
                        ),
                        "feedback_incorrect": (
                            "O débito desconta na hora. O crédito compromete a renda futura "
                            "(você paga na fatura). O boleto pode levar dias. "
                            "Saber a diferença ajuda a planejar o saldo."
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
                            "Ana pagou R$ 200 em roupas usando o cartão de crédito. "
                            "Quando o dinheiro sai da conta dela? (Situação fictícia.)"
                        ),
                        "competency_codes": ["3.1.2"],
                        "options": [
                            {"value": "a", "label": "Imediatamente após a compra."},
                            {
                                "value": "b",
                                "label": "Na data de vencimento da fatura do cartão.",
                            },
                            {"value": "c", "label": "Em 3 dias úteis."},
                            {"value": "d", "label": "No dia do fechamento da fatura."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Com crédito, a cobrança aparece na fatura e é "
                            "debitada no vencimento. O fechamento é quando a fatura "
                            "é 'cortada'; o vencimento é quando você paga."
                        ),
                        "feedback_incorrect": (
                            "Com crédito, o dinheiro NÃO sai na hora. "
                            "A compra vai para a fatura e é cobrada no vencimento. "
                            "Isso é diferente do débito (sai na hora) e do Pix (instantâneo)."
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
                            "Pix tem limite por transação? Qual é a regra geral?\n\n"
                            "(Nota: limites variam por banco e horário — consulte o "
                            "seu aplicativo para valores exatos.)"
                        ),
                        "competency_codes": ["3.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Não tem limite — qualquer valor pode ser enviado a qualquer hora.",
                            },
                            {
                                "value": "b",
                                "label": "Sim, cada banco define limites, que podem variar por horário.",
                            },
                            {
                                "value": "c",
                                "label": "O limite é sempre R$ 5.000 por transação, fixo pelo Banco Central.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Os limites do Pix são definidos por cada instituição "
                            "e podem variar conforme o horário (limite noturno é menor "
                            "por segurança). Sempre verifique no aplicativo do seu banco."
                        ),
                        "feedback_incorrect": (
                            "O Pix tem limites definidos por cada banco (não fixos). "
                            "Limites noturnos costumam ser menores por questões de segurança. "
                            "Consulte o aplicativo do seu banco para os valores vigentes."
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
                            "Pedro tem R$ 300 em conta e quer pagar uma conta de R$ 350. "
                            "Qual meio ele NÃO pode usar? (Situação fictícia.)"
                        ),
                        "competency_codes": ["3.1.2"],
                        "options": [
                            {"value": "a", "label": "Débito."},
                            {"value": "b", "label": "Pix."},
                            {"value": "c", "label": "Crédito."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Débito exige saldo disponível. "
                            "Com R$ 300 e conta de R$ 350, o débito seria recusado. "
                            "O Pix também exige saldo — portanto Pix também não funcionaria. "
                            "O crédito usa o limite do cartão, não o saldo da conta."
                        ),
                        "feedback_incorrect": (
                            "Débito exige saldo. Com saldo de R$ 300 e conta de "
                            "R$ 350, o débito seria recusado. O crédito usa o limite "
                            "do cartão — mas lembre que a fatura terá que ser paga depois."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual meio de pagamento tem compensação mais demorada?",
                        "competency_codes": ["3.1.3"],
                        "options": [
                            {"value": "a", "label": "Pix."},
                            {"value": "b", "label": "Débito."},
                            {"value": "c", "label": "Boleto bancário."},
                            {"value": "d", "label": "Todos compensam na hora."},
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! O boleto pode levar até 3 dias úteis para compensar. "
                            "Pix é instantâneo (24h, incluindo fins de semana). "
                            "Débito também é imediato."
                        ),
                        "feedback_incorrect": (
                            "Boleto bancário tem a compensação mais demorada — até 3 dias úteis. "
                            "Pix e débito compensam imediatamente."
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
                            "Descreva a diferença entre Pix, débito e crédito "
                            "como se fosse explicar para alguém que nunca usou banco. "
                            "Use exemplos concretos de compras do dia a dia."
                        ),
                        "competency_codes": ["3.1.1"],
                        "feedback_static": (
                            "Pix: você envia dinheiro na hora, de qualquer banco, "
                            "sem taxa, e o destinatário recebe imediatamente. "
                            "Débito: o dinheiro sai da sua conta no momento da compra — "
                            "você precisa ter saldo. "
                            "Crédito: o banco paga a compra agora e você paga depois, "
                            "na fatura — mas se não pagar tudo, paga juros altos."
                        ),
                        "evaluation_criteria": [
                            "Distingue os três meios com características corretas.",
                            "Usa exemplos concretos (não só definições abstratas).",
                            "Menciona o impacto no saldo ou na fatura de pelo menos dois meios.",
                        ],
                        "max_length": 600,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Pix: como funciona, limites e horários",
                    "order": 1,
                    "body": (
                        "O **Pix** é um sistema de pagamento instantâneo do Banco Central. "
                        "Principais características:\n\n"
                        "- **Instantâneo:** o destinatário recebe em segundos, "
                        "24 horas por dia, 7 dias por semana.\n"
                        "- **Chaves Pix:** CPF/CNPJ, e-mail, telefone ou chave aleatória.\n"
                        "- **Gratuito** para pessoa física na maioria das instituições.\n"
                        "- **Irreversível:** uma vez enviado, a devolução depende "
                        "do destinatário ou do MED.\n"
                        "- **Limites:** definidos por cada banco, com limite reduzido "
                        "à noite por segurança.\n\n"
                        "⚠️ **Atenção:** confira sempre os dados do destinatário antes "
                        "de confirmar."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Débito: saldo necessário, compensação imediata",
                    "order": 2,
                    "body": (
                        "O **cartão de débito** debita o valor da sua conta corrente "
                        "no momento da compra.\n\n"
                        "- **Precisa de saldo:** sem saldo, a transação é recusada.\n"
                        "- **Compensação imediata:** o valor sai na hora.\n"
                        "- **Sem juros:** você só gasta o que tem.\n\n"
                        "**Quando usar:** compras do dia a dia, mercado, transporte — "
                        "quando você quer saber exatamente quanto saiu."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Crédito: diferença de débito, impacto no orçamento futuro",
                    "order": 3,
                    "body": (
                        "No **cartão de crédito**, o banco paga a compra e você "
                        "reembolsa na data de vencimento da fatura.\n\n"
                        "- **Não precisa de saldo imediato:** usa o limite do cartão.\n"
                        "- **Cada compra no crédito compromete a renda do mês seguinte.**\n"
                        "- **Parcelamento:** divide o valor em parcelas mensais na fatura.\n\n"
                        "**Risco principal:** usar o crédito sem controle da fatura "
                        "resulta em dívida com juros entre os mais altos do mercado."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Fatura e parcelamento: visão geral",
                    "order": 4,
                    "body": (
                        "A **fatura** é o extrato do cartão de crédito — lista todas as "
                        "compras do período entre os fechamentos.\n\n"
                        "**Data de fechamento:** quando a fatura é 'cortada'. "
                        "Compras depois do fechamento entram na fatura seguinte.\n\n"
                        "**Data de vencimento:** quando você paga a fatura.\n\n"
                        "**Parcelamento:** divide uma compra grande em parcelas mensais. "
                        "Cada parcela entra na fatura do mês correspondente.\n\n"
                        "Os detalhes sobre fatura, pagamento mínimo e rotativo "
                        "são o tema central da **Trilha 4**."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Quando usar cada meio: um guia rápido",
                    "order": 5,
                    "body": (
                        "| Situação | Meio recomendado | Por quê |\n"
                        "|---|---|---|\n"
                        "| Pagar aluguel ou conta fixa | Pix ou débito | Instantâneo, sem taxa |\n"
                        "| Compra no mercado | Débito ou Pix | Desconta do saldo imediatamente |\n"
                        "| Compra grande parcelada | Crédito (sem juros) | Distribui o impacto |\n"
                        "| Emergência sem saldo | Crédito (com cuidado) | Último recurso |\n\n"
                        "Não há meio 'certo' para todas as situações — há o meio "
                        "mais adequado ao contexto."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Ana paga 4 contas de formas diferentes",
                    "order": 6,
                    "body": (
                        "**Ana** tem as seguintes contas neste mês *(fictício)*:\n\n"
                        "1. **Aluguel R$ 700** → Pix (proprietário aceita só Pix).\n\n"
                        "2. **Conta de luz R$ 110** → Débito, para descontar imediatamente.\n\n"
                        "3. **Supermercado R$ 380** → Débito.\n\n"
                        "4. **Geladeira R$ 1.200 em 4×** → Crédito parcelado. "
                        "Ela calculou que as 4 parcelas de R$ 300 cabem no orçamento.\n\n"
                        "**Resultado:** Ana usou o meio certo para cada situação. "
                        "O crédito só entrou onde o parcelamento fazia sentido. "
                        "*(Situação fictícia, para fins didáticos.)*"
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 3.3 — Antes de confirmar (expansão sobre phase_2_v1 missão 3)
        # Upsert: atualiza nome, descrição, competências e atividades
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Antes de confirmar",
            "description": (
                "Aplique a checagem antes de confirmar qualquer pagamento, "
                "identifique sinais de fraude e saiba o que fazer após uma "
                "transação errada."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.3.1",
                    "name": "Aplicar checagem antes de confirmar qualquer pagamento",
                    "description": (
                        "Verifica destinatário, valor, tipo e data antes de confirmar "
                        "qualquer transferência ou pagamento."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.3.2",
                    "name": "Identificar sinais de fraude em telas de pagamento e comprovantes",
                    "description": (
                        "Reconhece comprovantes falsos, QR Codes adulterados e "
                        "situações de pressão para confirmar pagamentos rapidamente."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.3.3",
                    "name": "Conhecer o MED e quando acionar",
                    "description": (
                        "Explica o que é o Mecanismo Especial de Devolução (MED), "
                        "seus critérios de acionamento e limitações."
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
                            "Antes de confirmar um Pix de R$ 800 para um vendedor online, "
                            "quais dados você deve verificar no aplicativo?"
                        ),
                        "competency_codes": ["3.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Apenas o valor — o banco valida o destinatário automaticamente.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Nome do destinatário, instituição, chave Pix usada e valor — "
                                    "antes de clicar em confirmar."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Apenas a chave Pix — se o banco aceitar, está certo.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Sempre confirme: nome completo do destinatário, "
                            "instituição, chave usada e valor. Uma digitação errada "
                            "pode enviar o dinheiro para outra pessoa. O banco valida "
                            "apenas se a chave existe — não se é a pessoa certa."
                        ),
                        "feedback_incorrect": (
                            "O banco confirma apenas se a chave existe — "
                            "não valida se é a pessoa certa. "
                            "Você precisa conferir nome, instituição e valor antes de confirmar."
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
                            "Marina enviou R$ 500 para o número de telefone errado "
                            "por engano. Qual é a primeira ação correta? (Situação fictícia.)"
                        ),
                        "competency_codes": ["3.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Aguardar — a pessoa deve devolver por conta própria.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Contatar o banco imediatamente e solicitar "
                                    "a devolução via protocolo de transferência errada."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Acionar o MED — é um golpe.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Erro de transferência não é golpe — o MED é para "
                            "fraudes confirmadas. O procedimento correto é: "
                            "contatar o banco imediatamente, solicitar devolução "
                            "ao destinatário e registrar BO se necessário."
                        ),
                        "feedback_incorrect": (
                            "Aguardar passivamente é a pior estratégia. "
                            "O MED é para fraudes, não para erros de digitação. "
                            "Para erro de transferência: contate o banco imediatamente."
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
                            "Um golpista manda um comprovante de Pix falso de R$ 1.000. "
                            "O comerciante entrega o produto sem conferir no app. "
                            "O que ele deveria ter feito?"
                        ),
                        "competency_codes": ["3.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Aceitar o comprovante — parecia legítimo.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Verificar no aplicativo do banco se o valor "
                                    "foi creditado no extrato antes de entregar o produto."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Pedir um segundo comprovante por e-mail.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Comprovantes são fáceis de falsificar. "
                            "A única confirmação válida é ver o crédito no extrato. "
                            "Pix é instantâneo — se não apareceu, não foi pago."
                        ),
                        "feedback_incorrect": (
                            "Comprovantes podem ser falsificados. Um segundo comprovante "
                            "externo pode ser igualmente falso. Verifique sempre "
                            "no aplicativo do seu banco se o valor apareceu no extrato."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O MED garante a devolução de qualquer Pix enviado por engano?",
                        "competency_codes": ["3.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Sim — qualquer Pix pode ser devolvido pelo MED.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não — o MED é para fraudes confirmadas; "
                                    "erros de transferência têm processo diferente."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Sim, mas só dentro de 24 horas.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O MED existe para casos de fraude confirmada. "
                            "Transferência para conta errada por erro do usuário não "
                            "aciona o MED automaticamente. Nesses casos, o processo "
                            "é de devolução voluntária pelo destinatário."
                        ),
                        "feedback_incorrect": (
                            "O MED não é um mecanismo de estorno geral — é para fraudes. "
                            "Para erros de transferência, o banco pode solicitar "
                            "a devolução ao destinatário, sem garantia automática. "
                            "Conferir antes de enviar é a única proteção efetiva."
                        ),
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual sinal indica que um QR Code pode ter sido adulterado por golpistas?",
                        "competency_codes": ["3.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "O QR Code está impresso em papel comum.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Ao escanear, o nome do beneficiário não corresponde "
                                    "ao estabelecimento onde você está."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "O valor já aparece preenchido no QR Code.",
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Sempre verifique o nome do beneficiário após escanear. "
                            "Um QR Code adulterado parece idêntico ao original mas "
                            "redireciona para uma conta fraudulenta. Se o nome não bater "
                            "com o estabelecimento, não confirme."
                        ),
                        "feedback_incorrect": (
                            "O sinal mais importante é o nome do beneficiário após escanear. "
                            "Golpistas substituem QR Codes legítimos por códigos "
                            "que apontam para contas fraudulentas."
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
                            "Descreva um procedimento de conferência passo a passo "
                            "antes de confirmar um pagamento Pix de R$ 800 "
                            "para um vendedor online que você nunca usou antes."
                        ),
                        "competency_codes": ["3.3.1", "3.3.2"],
                        "feedback_static": (
                            "Um bom procedimento inclui: verificar o nome completo "
                            "e CPF/CNPJ do destinatário, conferir o valor digitado, "
                            "confirmar o banco destinatário, e após enviar, verificar "
                            "se apareceu no extrato antes de entregar produto ou serviço."
                        ),
                        "evaluation_criteria": [
                            "Lista ao menos 3 itens a verificar antes de confirmar.",
                            "Menciona a verificação no extrato após o envio.",
                            "Identifica ao menos um risco específico de fraude.",
                        ],
                        "max_length": 600,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Por que conferir antes de confirmar salva dinheiro",
                    "order": 1,
                    "body": (
                        "O Pix é irreversível: uma vez enviado, o dinheiro chegou "
                        "ao destino. Por isso, **conferir antes de confirmar** é o "
                        "único mecanismo de proteção efetivo:\n\n"
                        "1. Verifique o nome e CPF/CNPJ do destinatário.\n"
                        "2. Confirme o valor digitado.\n"
                        "3. Verifique o tipo de chave usado.\n"
                        "4. Se necessário, ligue para o destinatário para confirmar.\n\n"
                        "10 segundos de verificação podem evitar uma perda impossível "
                        "de recuperar."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O que verificar: destinatário, valor, tipo e data",
                    "order": 2,
                    "body": (
                        "Antes de confirmar qualquer pagamento Pix:\n\n"
                        "**1. Destinatário:** nome completo e CPF/CNPJ devem bater "
                        "com quem você negociou.\n\n"
                        "**2. Valor:** confirme o valor, especialmente em transações altas.\n\n"
                        "**3. Tipo de chave:** certifique-se de que usou a chave correta.\n\n"
                        "**4. Instituição:** banco ou fintech do destinatário.\n\n"
                        "Se qualquer dado não bater: cancele e contate o destinatário "
                        "por outro canal."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A transferência errada da Marina",
                    "order": 3,
                    "body": (
                        "**Marina** queria pagar R$ 500 ao Rafael por um notebook. "
                        "Ela digitou o número de telefone errado e enviou para outra "
                        "pessoa. *(Situação fictícia, para fins didáticos.)*\n\n"
                        "O que aconteceu:\n"
                        "1. O Pix compensou instantaneamente para a pessoa errada.\n"
                        "2. Marina percebeu o erro ao ligar para Rafael.\n"
                        "3. Ela contatou o banco e iniciou pedido de devolução.\n"
                        "4. A outra pessoa não devolveu imediatamente.\n\n"
                        "**Lição:** 10 segundos de verificação teriam evitado tudo isso."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Comprovante falso: como identificar",
                    "order": 4,
                    "body": (
                        "Comprovantes de Pix podem ser falsificados facilmente.\n\n"
                        "**Como se proteger:**\n\n"
                        "1. **Nunca aceite comprovante como única confirmação.** "
                        "Verifique no seu aplicativo se o valor creditou.\n\n"
                        "2. **Pix é instantâneo.** Se não apareceu no extrato em segundos, "
                        "não foi pago.\n\n"
                        "3. **Desconfie de urgência.** Golpistas criam pressa "
                        "para você não verificar.\n\n"
                        "4. **Em vendas:** só entregue o produto após confirmar "
                        "o crédito no extrato, não no comprovante."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O MED: o que é, quando se aplica, limitações",
                    "order": 5,
                    "body": (
                        "O **Mecanismo Especial de Devolução (MED)** é um processo "
                        "do Banco Central para casos de fraude confirmada com Pix.\n\n"
                        "**Quando se aplica:** fraude ou falha operacional da instituição.\n\n"
                        "**Quando NÃO se aplica:**\n"
                        "- Transferência para conta errada por erro do usuário.\n"
                        "- Arrependimento após compra.\n\n"
                        "**Limitações:**\n"
                        "- O dinheiro precisa ainda estar na conta destino.\n"
                        "- O processo tem prazo definido.\n"
                        "- Não é garantia de devolução em todos os casos.\n\n"
                        "Para erros de transferência sem fraude, o processo é devolução "
                        "voluntária via banco — sem acionamento do MED."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "O que fazer imediatamente após perceber uma transação errada",
                    "order": 6,
                    "body": (
                        "Se você percebeu que enviou um Pix para a pessoa errada:\n\n"
                        "1. **Aja imediatamente.** Quanto antes, maiores as chances.\n\n"
                        "2. **Contate o seu banco** — informe o erro e registre o pedido.\n\n"
                        "3. **Guarde todos os comprovantes** — chave usada, data e valor.\n\n"
                        "4. **Registre um Boletim de Ocorrência** se necessário.\n\n"
                        "5. **Considere ação judicial** se necessário.\n\n"
                        "Aguardar passivamente é sempre a pior opção."
                    ),
                },
            ],
        },

        # ──────────────────────────────────────────────────────────────────
        # Missão 3.2 — Carteiras digitais e pagamentos no celular (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Carteiras digitais e pagamentos no celular",
            "description": (
                "Entenda o que são carteiras digitais, como diferenciá-las do Pix "
                "e do débito, e como usar esses meios com segurança."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.2.1",
                    "name": "Explicar o que são carteiras digitais e como funcionam",
                    "description": (
                        "Descreve o funcionamento de carteiras digitais (Google Pay, "
                        "Apple Pay, Samsung Pay etc.) e como elas armazenam dados de "
                        "pagamento para transações por NFC ou QR Code."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.2.2",
                    "name": "Identificar diferenças entre carteira digital, Pix e débito",
                    "description": (
                        "Distingue carteira digital, transferência Pix e pagamento "
                        "no débito convencional em termos de fluxo, prazo e requisitos."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.2.3",
                    "name": "Reconhecer riscos de segurança no uso de carteiras digitais",
                    "description": (
                        "Identifica práticas que aumentam ou reduzem o risco ao "
                        "utilizar carteiras digitais, como bloqueio de tela, autenticação "
                        "biométrica e uso em redes Wi-Fi públicas."
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
                            "O que é uma carteira digital (ex.: Google Pay, Apple Pay)?"
                        ),
                        "competency_codes": ["3.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Um aplicativo que armazena dados de cartões e "
                                    "permite pagar por aproximação (NFC) ou QR Code, "
                                    "sem precisar portar o cartão físico."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Um tipo de conta bancária digital sem tarifas, "
                                    "como as oferecidas por fintechs."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Um cartão de crédito virtual emitido pelo banco.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Um sistema de transferência instantânea criado "
                                    "pelo Banco Central, como o Pix."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A carteira digital armazena dados de um ou mais "
                            "cartões (crédito, débito ou pré-pago) e permite pagar "
                            "por aproximação via NFC ou por QR Code, sem o cartão "
                            "físico na mão."
                        ),
                        "feedback_incorrect": (
                            "Carteira digital não é conta bancária nem cartão virtual "
                            "em si — é um cofre seguro de dados de cartão no celular. "
                            "Ela usa NFC ou QR Code para efetuar o pagamento no lugar "
                            "do cartão físico."
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
                            "Qual é a principal diferença entre pagar com carteira "
                            "digital e pagar com Pix?"
                        ),
                        "competency_codes": ["3.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "A carteira digital usa dados de cartão cadastrado "
                                    "e passa pela rede da bandeira; o Pix é uma "
                                    "transferência instantânea diretamente entre contas, "
                                    "sem bandeira."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "O Pix só funciona entre pessoas físicas; a carteira "
                                    "digital funciona também para comércios."
                                ),
                            },
                            {
                                "value": "c",
                                "label": "Não há diferença — ambos debitam da mesma forma.",
                            },
                            {
                                "value": "d",
                                "label": (
                                    "A carteira digital é mais segura porque usa senha "
                                    "bancária, enquanto o Pix não exige autenticação."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Exato! A carteira digital processa o pagamento pela rede "
                            "da bandeira do cartão cadastrado (Visa, Mastercard etc.). "
                            "O Pix é uma infraestrutura do Banco Central que transfere "
                            "valores diretamente entre contas, sem bandeira, em segundos."
                        ),
                        "feedback_incorrect": (
                            "O Pix funciona para pessoas físicas, jurídicas e governo. "
                            "A diferença central é o fluxo: carteira digital passa pela "
                            "bandeira do cartão cadastrado; Pix é transferência direta "
                            "entre contas pelo sistema do Banco Central."
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
                            "Qual prática AUMENTA o risco ao usar carteira digital?"
                        ),
                        "competency_codes": ["3.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Usar bloqueio de tela com biometria no celular."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar em redes Wi-Fi públicas sem VPN e com "
                                    "o celular desbloqueado por padrão."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ativar notificações de transação em tempo real."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Cadastrar apenas um cartão e remover os que não usa."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Wi-Fi público sem VPN expõe o tráfego a "
                            "interceptações. Celular desbloqueado por padrão permite "
                            "que qualquer pessoa use a carteira digital em caso de roubo. "
                            "Sempre bloqueie a tela e prefira dados móveis para pagamentos."
                        ),
                        "feedback_incorrect": (
                            "Biometria, notificações em tempo real e manter poucos "
                            "cartões cadastrados são boas práticas de segurança. "
                            "O maior risco é usar Wi-Fi público sem VPN com o "
                            "celular desbloqueado — isso facilita interceptação e acesso."
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
                            "Mariana tem pressa e vai pagar o almoço no restaurante. "
                            "O estabelecimento aceita cartão por aproximação (NFC) "
                            "e Pix. Ela tem ambos disponíveis no celular.\n\n"
                            "Explique quando faz mais sentido usar a carteira digital "
                            "com NFC e quando faz mais sentido usar Pix, considerando "
                            "velocidade, segurança e controle do orçamento."
                        ),
                        "competency_codes": ["3.2.1", "3.2.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Pontos esperados na resposta:\n"
                            "- NFC (carteira digital) é rápido e conveniente para "
                            "valores pequenos do dia a dia; pode ser crédito ou débito.\n"
                            "- Pix debita imediatamente da conta — maior controle do "
                            "saldo em tempo real, sem faturas futuras.\n"
                            "- Para quem controla melhor os gastos evitando crédito, "
                            "Pix ou débito são preferíveis.\n"
                            "- Para acumular pontos em programas de fidelidade, "
                            "a carteira digital com cartão de crédito pode ser vantajosa "
                            "se o saldo for pago integralmente no vencimento."
                        ),
                        "evaluation_criteria": [
                            "Diferencia carteira digital de Pix de forma correta.",
                            "Menciona ao menos um critério de escolha (velocidade, controle, crédito vs. débito).",
                            "Demonstra entendimento de que NFC pode ser crédito ou débito.",
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
                            "Escolha o meio de pagamento correto para cada situação."
                        ),
                        "scenario": (
                            "João está em um dia agitado e precisa realizar três "
                            "pagamentos seguidos. Em cada situação há uma restrição "
                            "diferente. Analise e escolha o meio mais adequado:\n\n"
                            "**Situação 1:** Padaria aceita apenas Pix ou dinheiro. "
                            "O celular de João está com 3% de bateria.\n"
                            "**Situação 2:** Supermercado aceita cartão por aproximação "
                            "(NFC), débito e crédito. João não tem sinal de internet.\n"
                            "**Situação 3:** Loja online aceita cartão de crédito ou "
                            "boleto. João quer parcelar sem juros e acumular pontos.\n\n"
                            "Qual sequência de meios de pagamento João deve usar?"
                        ),
                        "competency_codes": ["3.2.1", "3.2.2", "3.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Situação 1: Pix pelo celular. "
                                    "Situação 2: NFC pela carteira digital (requer internet). "
                                    "Situação 3: Boleto para evitar cartão."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Situação 1: Dinheiro (bateria insuficiente para Pix). "
                                    "Situação 2: NFC pela carteira digital (não precisa de "
                                    "internet — usa token local). "
                                    "Situação 3: Cartão de crédito para parcelar sem juros "
                                    "e acumular pontos."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Situação 1: Pix pelo celular. "
                                    "Situação 2: Débito convencional (mais seguro sem internet). "
                                    "Situação 3: Boleto para controlar o orçamento."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Situação 1: Dinheiro. "
                                    "Situação 2: Débito convencional (não precisa de internet "
                                    "igual ao NFC). "
                                    "Situação 3: Cartão de crédito para parcelar e pontuar."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Ótima análise! Situação 1: com 3% de bateria, abrir o app "
                            "de Pix pode não completar a transação — dinheiro é mais "
                            "seguro. Situação 2: carteiras digitais modernas geram um "
                            "token criptografado local para NFC, sem precisar de internet "
                            "ativa durante a transação. Situação 3: cartão de crédito "
                            "permite parcelamento sem juros e acúmulo de pontos — desde "
                            "que o saldo seja pago integral no vencimento."
                        ),
                        "feedback_incorrect": (
                            "Revise cada restrição:\n"
                            "- 3% de bateria não garante conclusão do Pix — use dinheiro.\n"
                            "- NFC por carteira digital funciona sem internet (token local); "
                            "débito convencional também funciona, mas a questão pedia o "
                            "meio que combina segurança e conveniência sem internet.\n"
                            "- Para parcelar sem juros e acumular pontos, cartão de crédito "
                            "é o meio certo — boleto não parcela nem acumula pontos."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que são carteiras digitais e como funcionam",
                    "order": 1,
                    "body": (
                        "Uma **carteira digital** (digital wallet) é um aplicativo "
                        "no celular que armazena, de forma criptografada, os dados "
                        "de um ou mais cartões (crédito, débito ou pré-pago).\n\n"
                        "**Como funciona o pagamento:**\n"
                        "1. O cartão é cadastrado na carteira (ex.: Google Pay, Apple Pay, "
                        "Samsung Pay, Mercado Pago).\n"
                        "2. No momento da compra, o app gera um **token** — um código "
                        "temporário que representa o cartão sem expor os dados reais.\n"
                        "3. Esse token é enviado à maquininha via **NFC** (aproximação) "
                        "ou lido como **QR Code**.\n"
                        "4. A bandeira do cartão valida o token e conclui a transação.\n\n"
                        "**Vantagem de segurança:** como o número real do cartão nunca "
                        "é transmitido, mesmo que alguém intercepte o token, ele não "
                        "pode ser reutilizado."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Carteira digital × Pix × débito: comparativo",
                    "order": 2,
                    "body": (
                        "| Característica | Carteira digital | Pix | Débito convencional |\n"
                        "|---|---|---|---|\n"
                        "| O que movimenta | Dados do cartão cadastrado | Saldo em conta | Saldo em conta |\n"
                        "| Infraestrutura | Rede da bandeira (Visa, Master…) | Banco Central | Rede da bandeira |\n"
                        "| Precisa de internet no pagamento? | Não (NFC usa token local) | Sim | Não |\n"
                        "| Confirma no celular? | Sim (biometria/PIN) | Sim (app) | Não (PIN na maquininha) |\n"
                        "| Prazo de débito na conta | Conforme modalidade do cartão | Imediato | Imediato |\n\n"
                        "*(Comparativo simplificado para fins didáticos. "
                        "Fluxos podem variar por instituição.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como usar carteiras digitais com mais segurança",
                    "order": 3,
                    "body": (
                        "Adotar carteiras digitais é prático, mas exige cuidados:\n\n"
                        "- **Ative o bloqueio de tela** com biometria ou PIN — "
                        "sem ele, quem pegar o celular pode pagar com a sua carteira.\n"
                        "- **Evite pagar em Wi-Fi público** sem VPN ativa.\n"
                        "- **Ative notificações de transação** no app do banco — "
                        "você perceberá cobranças indevidas em segundos.\n"
                        "- **Cadastre apenas os cartões que usa** — "
                        "menos cartões = menos superfície de risco.\n"
                        "- **Se perder o celular:** bloqueie imediatamente o cartão "
                        "cadastrado pelo app do banco e informe a operadora."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 3.4 — Comparando meios de pagamento (nova)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Comparando meios de pagamento",
            "description": (
                "Compare custo, prazo e conveniência de diferentes meios de pagamento "
                "e escolha o mais adequado para cada perfil de compra e momento financeiro."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "3.4.1",
                    "name": "Comparar custo, prazo e conveniência de diferentes meios de pagamento",
                    "description": (
                        "Analisa dimensões práticas de Pix, débito, crédito e carteira "
                        "digital — incluindo tarifas, prazos de liquidação e "
                        "facilidade de uso em diferentes contextos."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.4.2",
                    "name": "Avaliar o impacto no orçamento da escolha do meio de pagamento",
                    "description": (
                        "Relaciona a escolha do meio de pagamento ao fluxo de caixa "
                        "pessoal — especialmente o impacto do crédito parcelado e "
                        "dos juros no orçamento futuro."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "3.4.3",
                    "name": "Escolher o meio adequado para cada perfil de compra",
                    "description": (
                        "Seleciona o meio de pagamento mais vantajoso considerando "
                        "tipo de compra, situação financeira do momento e "
                        "objetivos de curto e médio prazo."
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
                            "Qual meio de pagamento geralmente NÃO cobra tarifa "
                            "para o pagador pessoa física em transações entre "
                            "contas no Brasil?"
                        ),
                        "competency_codes": ["3.4.1"],
                        "options": [
                            {"value": "a", "label": "TED (Transferência Eletrônica Disponível)."},
                            {"value": "b", "label": "Pix."},
                            {"value": "c", "label": "Boleto bancário."},
                            {"value": "d", "label": "DOC (Documento de Ordem de Crédito)."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O Banco Central determina que o Pix é gratuito "
                            "para pessoas físicas em transferências. TED, DOC e boleto "
                            "podem ter tarifas cobradas pelas instituições financeiras, "
                            "dependendo do contrato e do canal usado."
                        ),
                        "feedback_incorrect": (
                            "O Pix é gratuito para pessoas físicas nas transferências, "
                            "por determinação do Banco Central. TED e DOC costumam ter "
                            "tarifas, especialmente via caixa eletrônico ou agência. "
                            "Boleto também pode ter custo de emissão ou pagamento fora "
                            "da rede credenciada."
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
                            "Ana vai comprar um notebook de R$ 3.000. Ela tem o "
                            "dinheiro disponível na conta. Qual afirmação sobre "
                            "o impacto no orçamento está correta?"
                        ),
                        "competency_codes": ["3.4.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar no débito ou Pix retira R$ 3.000 da conta "
                                    "imediatamente; parcelar no crédito sem juros "
                                    "distribui o impacto, mas compromete renda futura."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Parcelar no crédito sempre é melhor porque preserva "
                                    "o saldo da conta, independentemente dos juros."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pagar à vista no crédito e parcelar no débito "
                                    "têm o mesmo impacto no orçamento."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "O crédito não afeta o orçamento porque o dinheiro "
                                    "já está na conta."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Débito/Pix: impacto imediato e total no saldo. "
                            "Crédito parcelado sem juros: preserva o saldo agora, mas "
                            "cada parcela reduzirá a renda disponível nos meses seguintes. "
                            "A escolha depende do fluxo de caixa e da disciplina para "
                            "não gastar o saldo 'preservado' em outra coisa."
                        ),
                        "feedback_incorrect": (
                            "Parcelar no crédito sem juros pode ser vantajoso, mas "
                            "sempre compromete renda futura — cada parcela é um "
                            "compromisso no orçamento dos próximos meses. "
                            "Ter o dinheiro na conta não significa que o crédito "
                            "não afeta o orçamento futuro."
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
                            "Pedro quer pagar uma conta de luz de R$ 180. "
                            "Ele está com o orçamento apertado este mês. "
                            "Qual meio é mais adequado considerando custo e controle?"
                        ),
                        "competency_codes": ["3.4.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Cartão de crédito parcelado em 3x para aliviar "
                                    "o mês atual."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pix ou débito — debita imediatamente, sem gerar "
                                    "dívida futura nem juros."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Boleto com vencimento no mês seguinte para ganhar tempo."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Carteira digital com crédito para acumular pontos "
                                    "e pagar depois."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Para uma conta de valor fixo com orçamento apertado, "
                            "Pix ou débito são os mais adequados: sem juros, sem "
                            "comprometimento de renda futura, sem risco de esquecer a "
                            "fatura do cartão. Parcelar R$ 180 no crédito cria um "
                            "compromisso nos próximos meses — que continuarão apertados."
                        ),
                        "feedback_incorrect": (
                            "Parcelar ou adiar uma conta de valor pequeno no crédito "
                            "cria compromisso futuro e pode gerar juros se a fatura "
                            "não for paga integral. Com orçamento apertado, "
                            "o ideal é quitar agora via Pix ou débito — sem criar "
                            "dívida que pesará nos meses seguintes."
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
                            "Qual afirmação sobre o crédito à vista (sem parcelamento) "
                            "está correta?"
                        ),
                        "competency_codes": ["3.4.1", "3.4.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O débito é debitado na hora; o crédito à vista "
                                    "só é debitado na data do vencimento da fatura, "
                                    "dando um prazo de até ~40 dias."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Crédito à vista e débito têm o mesmo prazo de "
                                    "impacto no saldo bancário."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pagar no crédito à vista gera juros automaticamente "
                                    "se não for pago até o vencimento."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Crédito à vista sempre cobra mais do que o débito."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O crédito à vista difere do débito no prazo: "
                            "o débito sai da conta na hora; o crédito só sai no "
                            "vencimento da fatura — podendo dar um prazo de alguns dias "
                            "a semanas. A alternativa C está parcialmente certa: "
                            "juros só incidem se a fatura não for paga integralmente "
                            "no vencimento."
                        ),
                        "feedback_incorrect": (
                            "O crédito à vista não debita imediatamente — ele vai para "
                            "a fatura do mês. O débito sai na hora. Não há cobrança de "
                            "juros no crédito à vista se a fatura for paga integral "
                            "no vencimento. A diferença-chave é o prazo de impacto "
                            "no saldo bancário."
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
                            "Fernanda ganha R$ 2.500 líquidos por mês e quer comprar "
                            "um celular de R$ 1.200. Ela tem R$ 1.400 na conta e "
                            "R$ 300 de reserva de emergência separada.\n\n"
                            "Compare pelo menos dois meios de pagamento (ex.: débito, "
                            "crédito à vista, crédito parcelado sem juros, Pix) e "
                            "recomende o mais adequado para o perfil de Fernanda, "
                            "justificando sua escolha com base no impacto no orçamento."
                        ),
                        "competency_codes": ["3.4.1", "3.4.2", "3.4.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada.\n\n"
                            "Pontos esperados:\n"
                            "- Débito/Pix à vista: retira R$ 1.200 imediatamente, "
                            "deixando apenas R$ 200 livres (mais reserva de R$ 300). "
                            "Arriscado — qualquer imprevisto compromete o orçamento.\n"
                            "- Crédito parcelado sem juros (ex.: 4x R$ 300): "
                            "preserva o saldo da conta, mas compromete R$ 300/mês "
                            "por 4 meses — o que é 12% da renda mensal.\n"
                            "- Recomendação razoável: crédito parcelado sem juros, "
                            "se Fernanda tiver disciplina para não gastar o saldo "
                            "preservado e pagar a fatura integralmente todo mês.\n"
                            "- Alternativa prudente: esperar mais 1–2 meses para "
                            "aumentar a reserva antes de comprar."
                        ),
                        "evaluation_criteria": [
                            "Compara ao menos dois meios de pagamento distintos.",
                            "Menciona o impacto no saldo ou nas parcelas futuras.",
                            "Justifica a recomendação com base no contexto financeiro de Fernanda.",
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
                            "Analise as quatro opções de pagamento e escolha a mais "
                            "vantajosa para a restrição financeira apresentada."
                        ),
                        "scenario": (
                            "Rafael vai comprar uma geladeira de R$ 2.400. "
                            "O vendedor oferece quatro formas de pagamento:\n\n"
                            "| Opção | Meio | Condição |\n"
                            "|---|---|---|\n"
                            "| A | Pix à vista | 5% de desconto → R$ 2.280 |\n"
                            "| B | Débito | Sem desconto → R$ 2.400 |\n"
                            "| C | Crédito 12x sem juros | R$ 200/mês, sem desconto |\n"
                            "| D | Crédito 12x com juros (2% a.m.) | ~R$ 224/mês |\n\n"
                            "**Restrição:** Rafael tem R$ 2.600 na conta corrente, "
                            "R$ 1.800 de despesas fixas mensais e renda de R$ 2.500/mês. "
                            "Sua reserva de emergência está zerada.\n\n"
                            "Qual opção Rafael deve escolher?"
                        ),
                        "competency_codes": ["3.4.1", "3.4.2", "3.4.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Opção A — Pix à vista com 5% de desconto (R$ 2.280). "
                                    "Menor custo total."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Opção B — Débito à vista (R$ 2.400). "
                                    "Mais simples e sem fatura futura."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Opção C — Crédito 12x sem juros (R$ 200/mês). "
                                    "Preserva o saldo da conta e cabe no orçamento."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Opção D — Crédito 12x com juros (≈ R$ 224/mês). "
                                    "Parcelas menores do que pagar tudo agora."
                                ),
                            },
                        ],
                        "correct_choice": "c",
                        "feedback_correct": (
                            "Boa análise! Rafael tem R$ 2.600 na conta e R$ 1.800 de "
                            "despesas fixas — sobram apenas R$ 700/mês livres. "
                            "Pagar R$ 2.280 ou R$ 2.400 à vista zeraria praticamente "
                            "toda a conta, deixando-o sem reserva de emergência alguma. "
                            "A opção C (12x R$ 200 sem juros) usa R$ 200/mês — "
                            "28% do valor livre — e mantém o saldo da conta intacto "
                            "para reconstruir a reserva. A opção D tem juros desnecessários. "
                            "Regra: quando não há reserva, evite comprometer todo o saldo "
                            "de uma vez."
                        ),
                        "feedback_incorrect": (
                            "Analise a restrição: com R$ 2.600 na conta e R$ 1.800 de "
                            "despesas fixas, pagar à vista (A ou B) deixaria Rafael sem "
                            "nenhuma reserva de emergência — qualquer imprevisto viraria "
                            "dívida. A opção C parcela sem juros em R$ 200/mês — "
                            "valor que cabe no orçamento e preserva o saldo. "
                            "A opção D tem juros evitáveis. Quando a reserva está zerada, "
                            "preservar liquidez é prioritário."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Custo, prazo e conveniência: como comparar meios de pagamento",
                    "order": 1,
                    "body": (
                        "Ao escolher como pagar, avalie três dimensões:\n\n"
                        "**1. Custo direto**\n"
                        "- Pix: gratuito para PF.\n"
                        "- Débito: sem juros; pode haver tarifa em alguns canais.\n"
                        "- Crédito à vista: sem juros se pagar a fatura integral; "
                        "juros altos se não pagar.\n"
                        "- Crédito parcelado com juros: CET (Custo Efetivo Total) "
                        "pode dobrar o preço final.\n"
                        "- Boleto: pode ter taxa de emissão ou pagamento fora da rede.\n\n"
                        "**2. Prazo de impacto no saldo**\n"
                        "- Pix e débito: imediato.\n"
                        "- Crédito: no vencimento da fatura (dias a semanas depois).\n\n"
                        "**3. Conveniência**\n"
                        "- Carteira digital/NFC: rápido, sem contato.\n"
                        "- Pix: disponível 24h, inclusive fins de semana.\n"
                        "- Boleto: útil quando não há cartão ou conta."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Mesma compra, quatro meios: o que muda no orçamento",
                    "order": 2,
                    "body": (
                        "**Compra fictícia: tênis de R$ 300**\n\n"
                        "| Meio | Valor final | Impacto imediato | Impacto futuro |\n"
                        "|---|---|---|---|\n"
                        "| Pix à vista (5% desc.) | R$ 285 | − R$ 285 na hora | Nenhum |\n"
                        "| Débito | R$ 300 | − R$ 300 na hora | Nenhum |\n"
                        "| Crédito à vista (fatura) | R$ 300 | 0 na hora | − R$ 300 no vencimento |\n"
                        "| Crédito 3x sem juros | R$ 300 | 0 na hora | − R$ 100/mês × 3 |\n"
                        "| Crédito 3x com 3% a.m. | ≈ R$ 327 | 0 na hora | − R$ 109/mês × 3 |\n\n"
                        "Pix com desconto tem o menor custo total. "
                        "Crédito com juros paga R$ 27 a mais pelo mesmo tênis.\n\n"
                        "*(Valores fictícios para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como escolher o meio certo para cada compra",
                    "order": 3,
                    "body": (
                        "Use este guia rápido na hora de decidir:\n\n"
                        "- **Tem desconto no Pix?** Se sim e o saldo permite, "
                        "Pix geralmente é o mais barato.\n"
                        "- **Orçamento apertado este mês?** Prefira Pix ou débito "
                        "para não criar compromisso futuro.\n"
                        "- **Compra grande e reserva sólida?** Crédito parcelado "
                        "sem juros pode ser vantajoso — distribui o impacto sem custo extra.\n"
                        "- **Quer acumular pontos?** Cartão de crédito com programa "
                        "de fidelidade faz sentido — desde que a fatura seja paga "
                        "integralmente no vencimento.\n"
                        "- **Nunca parcele com juros** se tiver alternativa: "
                        "os juros do crédito rotativo e do parcelado com juros "
                        "estão entre os mais altos do mercado brasileiro."
                    ),
                },
            ],
        },
    ],
}
