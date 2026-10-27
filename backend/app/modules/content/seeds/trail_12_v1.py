"""Conteúdo versionado da Trilha 12 — Desafio integrador.

phase_number: 12 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-12.md

Apenas simulações. Avalia aplicação integrada de competências das trilhas 1–11.
Os cenários são fictícios. Não incentivam exposição de dados reais.
"""

TRAIL_12_V1 = {
    "phase_number": 12,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 12.1 — Cenário: primeiro salário
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Cenário: primeiro salário",
            "description": (
                "Lucas recebeu seu primeiro salário. Confira o contracheque, "
                "calcule o líquido real e distribua o orçamento com critério."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "12.1.1",
                    "name": "Aplicar competências das trilhas 1 e 2 em cenário integrado",
                    "description": (
                        "Verifica o contracheque, calcula o salário líquido e "
                        "organiza o orçamento a partir do valor correto."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Lucas começou a trabalhar com salário bruto de R$ 2.000,00. "
                            "Seu contracheque mostra:\n\n"
                            "- Salário bruto: R$ 2.000,00\n"
                            "- INSS: R$ 155,68\n"
                            "- IRRF: R$ 0,00\n"
                            "- Vale-transporte: R$ 120,00\n"
                            "- FGTS (informativo): R$ 160,00\n\n"
                            "O gerente disse a Lucas que seu salário líquido é R$ 1.844,32. "
                            "Está correto?"
                        ),
                        "competency_codes": ["12.1.1"],
                        "scenario": (
                            "Lucas, 20 anos, primeiro emprego. "
                            "Contracheque fictício com valores baseados nas faixas INSS 2026. "
                            "Valores para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Sim, R$ 1.844,32 está correto — o gerente calculou direito."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não. O correto é R$ 1.724,32. O gerente não descontou "
                                    "o vale-transporte: 2.000 − 155,68 − 0 − 120 = R$ 1.724,32."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não. O FGTS também deve ser descontado: "
                                    "2.000 − 155,68 − 160 − 120 = R$ 1.564,32."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Correto! O líquido real é R$ 1.724,32: "
                            "2.000 − 155,68 (INSS) − 0 (IRRF) − 120 (VT) = R$ 1.724,32. "
                            "O gerente esqueceu do vale-transporte. "
                            "O FGTS não é desconto — é depositado pelo empregador "
                            "em conta separada. Lucas deve questionar o cálculo."
                        ),
                        "feedback_incorrect": (
                            "Verifique o cálculo: 2.000 − 155,68 − 0 − 120 = R$ 1.724,32. "
                            "R$ 1.844,32 seria se o vale-transporte não fosse descontado. "
                            "O FGTS não reduz o salário líquido — é um benefício depositado "
                            "pelo empregador em conta vinculada ao trabalhador."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Lucas tem R$ 1.724,32 líquidos. Ele precisa distribuir:\n\n"
                            "- Aluguel (dividido com amigo): R$ 500\n"
                            "- Alimentação: R$ 400\n"
                            "- Transporte (já descontado): R$ 0 extra\n"
                            "- Celular (indispensável para o trabalho): R$ 60\n"
                            "- Reserva de emergência: quer guardar algo\n"
                            "- Compra de um tênis: R$ 280\n\n"
                            "Qual é a melhor distribuição?"
                        ),
                        "competency_codes": ["12.1.1"],
                        "scenario": (
                            "Orçamento de Lucas com renda de R$ 1.724,32. "
                            "Valores fictícios, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Aluguel R$ 500 + alimentação R$ 400 + celular R$ 60 "
                                    "+ tênis R$ 280 + reserva R$ 484,32. "
                                    "Total: R$ 1.724,32."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Aluguel R$ 500 + alimentação R$ 400 + celular R$ 60 "
                                    "+ reserva R$ 764,32. O tênis fica para quando a "
                                    "reserva estiver construída. Total: R$ 1.724,32."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Tênis R$ 280 + aluguel R$ 500 + alimentação R$ 400 "
                                    "+ celular R$ 60 + reserva R$ 484,32. "
                                    "Prioridade ao tênis por ser novo."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! Essenciais primeiro: aluguel, alimentação e celular "
                            "somam R$ 960. O restante (R$ 764,32) vai para a reserva. "
                            "O tênis é um desejo — pode esperar até a reserva estar formada. "
                            "Lucas protege o orçamento e constrói segurança financeira."
                        ),
                        "feedback_incorrect": (
                            "A ordem correta é: essenciais (aluguel, alimentação, celular) → "
                            "reserva → desejos. O tênis é um desejo — "
                            "não compromete nada se ficar para depois. "
                            "Guardar R$ 764 de uma vez é um ótimo começo para a reserva."
                        ),
                    },
                },
            ],
            "content_items": [],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 12.2 — Cenário: decisão de pagamento
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Cenário: decisão de pagamento",
            "description": (
                "Ana precisa pagar 4 contas e usou o cartão para uma compra "
                "parcelada. Escolha o meio correto para cada situação e "
                "avalie o impacto no orçamento."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "12.2.1",
                    "name": "Aplicar competências das trilhas 3 e 4 em cenário integrado",
                    "description": (
                        "Escolhe o meio de pagamento adequado e calcula o "
                        "comprometimento de renda de um parcelamento."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Ana tem 4 pagamentos para fazer agora:\n\n"
                            "1. Aluguel: R$ 700 — proprietário aceita só Pix ou transferência\n"
                            "2. Conta de luz: R$ 120 — tem código de barras\n"
                            "3. Ingresso show: R$ 150 — site aceita débito, crédito ou Pix\n"
                            "4. Mercadinho perto de casa: R$ 95 — aceita débito, crédito ou Pix\n\n"
                            "Qual é a melhor estratégia de pagamento?"
                        ),
                        "competency_codes": ["12.2.1"],
                        "scenario": (
                            "Ana, orçamento organizado, precisa pagar 4 contas. "
                            "Ela tem saldo suficiente em conta. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Todos no crédito — mais fácil e concentra tudo na fatura."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Aluguel: Pix (obrigatório). Luz: débito/boleto. "
                                    "Show: Pix ou débito (saída imediata do orçamento). "
                                    "Mercado: débito ou Pix."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Aluguel: Pix. Luz: crédito. Show: crédito. Mercado: crédito. "
                                    "Guardo o dinheiro na conta."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa estratégia! Aluguel em Pix (obrigatório pelo proprietário). "
                            "Conta de luz em débito/boleto para sair do saldo corrente. "
                            "Show e mercado em Pix ou débito — os valores são claros e "
                            "Ana tem saldo. Usar crédito para despesas do mês compromete "
                            "a fatura futura desnecessariamente quando há saldo disponível."
                        ),
                        "feedback_incorrect": (
                            "O crédito para todas as contas compromete a fatura futura "
                            "sem necessidade — Ana tem saldo disponível. "
                            "Para contas mensais fixas com saldo disponível, "
                            "Pix ou débito é a escolha mais simples e transparente."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Ana parcelou uma compra de R$ 900 em 3 × de R$ 300 no cartão. "
                            "Ela já tinha 1 parcela de R$ 150 em andamento. "
                            "Sua renda mensal é R$ 1.724,32. "
                            "Qual é o comprometimento de renda com parcelas nos próximos 2 meses?"
                        ),
                        "competency_codes": ["12.2.1"],
                        "scenario": (
                            "Ana, mesma situação do cenário anterior. "
                            "Parcela existente: R$ 150/mês (1 mês restante). "
                            "Nova parcela: R$ 300/mês por 3 meses. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Mês 1: R$ 450 (R$ 150 + R$ 300). "
                                    "Mês 2: R$ 300 (só a nova parcela). "
                                    "Mês 3: R$ 300. "
                                    "Comprometimento: 26% da renda no mês 1."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "R$ 300 em todos os meses — só a nova parcela.",
                            },
                            {
                                "value": "c",
                                "label": "R$ 150 em todos os meses — só a parcela antiga.",
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Correto! No mês 1, Ana paga R$ 150 (parcela antiga) + R$ 300 "
                            "(nova) = R$ 450 de parcelas — 26% da renda de R$ 1.724. "
                            "A partir do mês 2, só R$ 300. Planejar as parcelas futuras "
                            "evita surpresas no orçamento."
                        ),
                        "feedback_incorrect": (
                            "Parcelas simultâneas somam. No mês 1: R$ 150 + R$ 300 = R$ 450. "
                            "A partir do mês 2: só R$ 300. "
                            "Verificar o total de parcelas em andamento é essencial "
                            "antes de assumir um novo compromisso."
                        ),
                    },
                },
            ],
            "content_items": [],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 12.3 — Cenário: crise financeira
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Cenário: crise financeira",
            "description": (
                "Carlos perdeu o emprego. Com reserva parcial, duas dívidas "
                "e uma oferta de crédito, tome decisões fundamentadas."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "12.3.1",
                    "name": "Aplicar competências das trilhas 5, 7 e 8 em cenário integrado",
                    "description": (
                        "Usa a reserva de emergência, prioriza dívidas e avalia "
                        "uma oferta de crédito com senso crítico."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos ficou desempregado. Ele tem:\n\n"
                            "- Reserva de emergência: R$ 2.400\n"
                            "- Gastos essenciais mensais: R$ 1.800\n"
                            "- Dois meses para encontrar emprego (estimativa)\n\n"
                            "Ele deve usar a reserva para pagar as contas enquanto "
                            "procura emprego?"
                        ),
                        "competency_codes": ["12.3.1"],
                        "scenario": (
                            "Carlos, 28 anos, desempregado. Reserva parcial cobrindo "
                            "1,3 meses de despesas. Situação fictícia."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Sim — a reserva foi criada exatamente para isso. "
                                    "Usar para pagar essenciais enquanto procura emprego "
                                    "é o uso correto. Mas deve recompor quando voltar a trabalhar."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não — deve preservar a reserva e pagar essenciais "
                                    "no crédito."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Não — a reserva é só para emergências médicas."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Correto! Perda de emprego é exatamente a situação para a "
                            "qual a reserva existe. R$ 2.400 cobre 1,3 meses de "
                            "despesas essenciais (R$ 1.800/mês). Carlos deve ser seletivo "
                            "nos gastos, buscar emprego ativamente e recompor a reserva "
                            "quando estiver trabalhando. Usar crédito para essenciais "
                            "criaria uma dívida cara desnecessariamente."
                        ),
                        "feedback_incorrect": (
                            "A reserva de emergência existe para situações como esta. "
                            "Usar crédito para pagar essenciais quando a reserva existe "
                            "gera custo extra. A reserva é para ser usada — "
                            "e recomposta depois."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Carlos conseguiu emprego temporário gerando R$ 800/mês. "
                            "Tem duas dívidas:\n\n"
                            "- Dívida A: R$ 800, 6%/mês\n"
                            "- Dívida B: R$ 2.000, 1,5%/mês\n\n"
                            "Seus essenciais custam R$ 1.200. Ele tem R$ 800 − R$ 1.200 = "
                            "déficit de R$ 400. Ele também recebe FGTS (R$ 2.500 a receber).\n\n"
                            "Com o FGTS, qual dívida Carlos quita primeiro?"
                        ),
                        "competency_codes": ["12.3.1"],
                        "scenario": (
                            "Carlos com renda de R$ 800 temporário e déficit mensal. "
                            "FGTS a receber: R$ 2.500. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Dívida A (R$ 800, 6%/mês) — menor saldo e "
                                    "maior taxa. Quita totalmente com R$ 800 do FGTS "
                                    "e economiza juros altos."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Dívida B (R$ 2.000, 1,5%/mês) — maior saldo, "
                                    "reduz o total mais. Paga R$ 2.000 e fica com R$ 500."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Divide o FGTS entre as duas dívidas igualmente."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Ótima decisão! A avalanche prioriza a dívida mais cara (6%/mês). "
                            "Com R$ 2.500 de FGTS: quita A (R$ 800) completamente e "
                            "usa R$ 1.700 para reduzir B. "
                            "Eliminar A primeiro remove a maior fonte de custo futuro."
                        ),
                        "feedback_incorrect": (
                            "A estratégia da avalanche prioriza a dívida de maior taxa: "
                            "dívida A (6%/mês >> 1,5%/mês da B). "
                            "Com R$ 2.500 de FGTS: quita A completamente (R$ 800) "
                            "e usa o restante (R$ 1.700) para reduzir B."
                        ),
                    },
                },
            ],
            "content_items": [],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 12.4 — Cenário: alerta de fraude
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "Cenário: alerta de fraude",
            "description": (
                "Camila recebeu um comprovante falso e uma mensagem de phishing. "
                "Identifique as ameaças e tome as decisões corretas."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "12.4.1",
                    "name": "Aplicar competências das trilhas 11 e 3 em cenário integrado",
                    "description": (
                        "Identifica golpe em situação realista e toma a decisão "
                        "correta incluindo os procedimentos pós-golpe."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Camila está vendendo um celular por R$ 600. O comprador "
                            "manda um comprovante de Pix pelo WhatsApp e pede para "
                            "ela enviar o aparelho amanhã de manhã. "
                            "Ela abre o aplicativo do banco e vê que o saldo não mudou.\n\n"
                            "O que Camila faz?"
                        ),
                        "competency_codes": ["12.4.1"],
                        "scenario": (
                            "Venda online de celular. Comprovante externo recebido. "
                            "Saldo bancário não alterado. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Enviar o celular amanhã cedo — o Pix pode demorar."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Aguardar até o crédito aparecer no extrato. "
                                    "Como o saldo não mudou, o Pix não foi feito. "
                                    "Informar o comprador e não entregar o aparelho."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pedir um segundo comprovante por e-mail para confirmar."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Decisão correta! Pix é instantâneo — se o saldo não mudou, "
                            "o pagamento não foi feito. O comprovante foi falsificado. "
                            "Camila não deve entregar nada sem ver o crédito no extrato. "
                            "Pode informar o comprador que aguardará a confirmação."
                        ),
                        "feedback_incorrect": (
                            "Pix compensa em segundos. Se o saldo não mudou, "
                            "o pagamento não foi realizado. O comprovante é falso. "
                            "Nunca entregue produto antes de ver o crédito no extrato. "
                            "Segundo comprovante externo pode ser igualmente falsificado."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "simulation",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Mais tarde, Camila percebe que enviou R$ 600 para uma "
                            "conta errada por distração (digitou o número de chave Pix errado). "
                            "Ela quer recuperar o dinheiro.\n\n"
                            "Quais são as próximas ações corretas, em ordem?"
                        ),
                        "competency_codes": ["12.4.1"],
                        "scenario": (
                            "Camila enviou R$ 600 para conta errada por engano. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "1. Contatar o banco imediatamente para informar o erro. "
                                    "2. Solicitar devolução voluntária ao destinatário via banco. "
                                    "3. Registrar boletim de ocorrência se necessário. "
                                    "4. Guardar todos os comprovantes."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Acionar o MED imediatamente — é um erro de transferência."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Aguardar o destinatário perceber o erro e devolver."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Correto! Erro de transferência não aciona o MED automaticamente "
                            "(MED é para fraude confirmada). O processo é: "
                            "contatar o banco → solicitar devolução voluntária pelo destinatário "
                            "→ registrar BO se necessário → aguardar resposta. "
                            "Se o destinatário não devolver, pode ser necessária ação judicial."
                        ),
                        "feedback_incorrect": (
                            "Erro de transferência ≠ fraude. O MED é para fraudes confirmadas. "
                            "Para erro de transferência, o processo é: contatar o banco, "
                            "solicitar devolução voluntária ao destinatário e, se necessário, "
                            "registrar BO e considerar ação judicial. "
                            "Aguardar passivamente é a pior estratégia."
                        ),
                    },
                },
            ],
            "content_items": [],
        },
    ],
}
