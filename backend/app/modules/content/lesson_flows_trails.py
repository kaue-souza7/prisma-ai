"""Roteiros dos minicursos para as trilhas 1–12 (missões novas da reestruturação).

Complementa lesson_flows.py, que cobre as missões originais das phases 1–6.
As chaves são (phase_number, mission_number), que correspondem a (trilha, missão).

Gerado em: 2026-10
Fonte editorial: seeds trail_1_v2 a trail_12_v1
"""

LESSON_FLOWS_TRAILS: dict[tuple, list] = {

    # ── Trilha 1 — Meu primeiro salário ──────────────────────────────────────
    (1, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cada linha do holerite tem um motivo",
            "body": (
                "O holerite lista vencimentos e descontos em linhas separadas — "
                "mas poucos param para entender cada uma. Saber o que cada item "
                "significa é o primeiro passo para conferir se o desconto está "
                "correto.\n\n"
                "Você vai destrinchar um contracheque fictício, calcular o INSS "
                "progressivo e entender o que o empregador deposita sem descontar "
                "do salário."
            ),
            "highlights": [
                "Identificar vencimentos, descontos e informativos",
                "Calcular o INSS progressivo por faixas",
                "Diferenciar FGTS e benefícios de descontos",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O holerite não tem mais segredos",
            "body": (
                "Você aprendeu a distinguir vencimentos (o que entra) de descontos "
                "(o que sai) e informativos (como o FGTS). Também calculou o INSS "
                "progressivo por faixas — o desconto muda conforme a faixa do salário.\n\n"
                "Com isso, você pode conferir seu próprio contracheque assim que ele "
                "chegar."
            ),
            "highlights": [
                "Vencimentos entram; descontos saem; informativos apenas informam.",
                "INSS progressivo: cada faixa salarial tem sua alíquota.",
                "FGTS é depósito do empregador — não aparece como desconto.",
            ],
        },
    ],

    (1, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Benefícios que chegam uma vez por ano",
            "body": (
                "O 13º salário e as férias parecem bônus, mas são direitos garantidos "
                "por lei — e o valor que cai na conta não é sempre o que parece.\n\n"
                "Você vai aprender quando cada um é pago, como o adicional de férias "
                "é calculado e por que o líquido é diferente do bruto."
            ),
            "highlights": [
                "Entender 13º salário: parcelas e prazo",
                "Calcular o adicional constitucional de férias (⅓)",
                "Diferenciar bruto e líquido nos dois benefícios",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Benefícios planejados são dinheiro certo",
            "body": (
                "Você calculou o 13º bruto e líquido, entendeu o adicional de ⅓ das "
                "férias e viu que os prazos importam para o planejamento.\n\n"
                "Com esses valores no horizonte, dá para planejar o fim do ano ou a "
                "viagem de férias sem surpresas na conta."
            ),
            "highlights": [
                "13º = um salário bruto dividido em 2 parcelas.",
                "Férias: salário + ⅓ constitucional — sujeito a INSS e IRRF.",
                "O líquido é o que cai na conta; planeje pelo líquido.",
            ],
        },
    ],

    # ── Trilha 2 — Orçamento na prática ──────────────────────────────────────
    (2, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O que sai sem você perceber",
            "body": (
                "Alguns gastos se tornam invisíveis porque são cobrados todo mês "
                "de forma automática — assinaturas que você esqueceu, serviços que "
                "não usa mais, pequenas cobranças que somam centenas por ano.\n\n"
                "Você vai revisar um extrato fictício, identificar os gastos "
                "invisíveis e calcular o quanto eles custam no ano."
            ),
            "highlights": [
                "Identificar gastos que passam despercebidos",
                "Calcular o impacto acumulado no orçamento",
                "Decidir o que manter e o que cancelar",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O que estava se escondendo no extrato",
            "body": (
                "Você encontrou os gastos que passavam sem ser notados e calculou "
                "o custo real deles no mês e no ano. Cancelar ou ajustar esses "
                "gastos libera espaço no orçamento sem cortar o que você realmente "
                "valoriza.\n\n"
                "A próxima missão usa esse olhar para acompanhar o orçamento mês a mês."
            ),
            "highlights": [
                "Gastos invisíveis se acumulam — revise o extrato todo mês.",
                "Pequenas cobranças mensais viram grandes valores no ano.",
                "Cancele o que não usa; mantenha o que agrega valor real.",
            ],
        },
    ],

    (2, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O que você planejou versus o que aconteceu",
            "body": (
                "Fazer um orçamento é a primeira parte. Acompanhar se ele está sendo "
                "cumprido é a segunda — e a mais reveladora.\n\n"
                "Você vai comparar um orçamento planejado com o realizado, "
                "identificar em quais categorias o gasto passou do limite e "
                "propor ajustes realistas para o mês seguinte."
            ),
            "highlights": [
                "Registrar e categorizar despesas reais",
                "Identificar desvios entre planejado e realizado",
                "Propor ajustes sem comprometer o essencial",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O orçamento como ferramenta, não punição",
            "body": (
                "Você identificou os desvios, entendeu suas causas e propôs ajustes "
                "que preservam o essencial. Controlar o orçamento não é cortar tudo "
                "— é fazer escolhas conscientes para o próximo mês.\n\n"
                "Com esse hábito, cada mês começa com mais clareza."
            ),
            "highlights": [
                "Compare planejado com realizado ao final do mês.",
                "Desvio pequeno em muitas categorias some antes de ser notado.",
                "Ajuste uma categoria por vez — mudanças abruptas não duram.",
            ],
        },
    ],

    # ── Trilha 3 — Pagamentos do dia a dia ───────────────────────────────────
    (3, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Pagar com o celular: mais opções, mesma atenção",
            "body": (
                "Carteiras digitais, NFC e pagamentos por aproximação tornaram as "
                "compras mais rápidas — mas também trouxeram novas formas de risco.\n\n"
                "Você vai entender como as carteiras digitais funcionam, o que as "
                "diferencia do Pix e do débito, e quais cuidados precisam acompanhar "
                "a conveniência."
            ),
            "highlights": [
                "Entender o que são carteiras digitais",
                "Comparar com Pix e débito",
                "Reconhecer riscos de segurança",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "scenario", "activity_order": 5},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Conveniência com consciência",
            "body": (
                "Você entendeu que carteiras digitais funcionam como intermediárias "
                "entre o cartão e o pagamento, e que os cuidados com segurança não "
                "diminuem porque o processo parece invisível.\n\n"
                "Na próxima missão, você vai comparar todos os meios e escolher o "
                "mais adequado para cada situação."
            ),
            "highlights": [
                "Carteiras digitais tokenizam o cartão — não expõem os dados diretamente.",
                "NFC e Pix têm comportamentos diferentes em falha ou golpe.",
                "Celular desbloqueado e Wi-Fi público aumentam os riscos.",
            ],
        },
    ],

    (3, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Qual o melhor jeito de pagar?",
            "body": (
                "Custo, prazo, conveniência e impacto no orçamento: cada meio de "
                "pagamento tem características próprias que fazem mais sentido em "
                "contextos diferentes.\n\n"
                "Você vai comparar as opções disponíveis, avaliar o impacto de "
                "cada uma no orçamento e escolher o meio certo para cada perfil "
                "de compra."
            ),
            "highlights": [
                "Comparar custo, prazo e conveniência",
                "Avaliar impacto no orçamento de cada meio",
                "Escolher o meio adequado ao perfil da compra",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A escolha do meio é parte da decisão financeira",
            "body": (
                "Você comparou os meios de pagamento em três dimensões — custo, "
                "prazo e conveniência — e viu que a melhor opção depende do contexto "
                "e da saúde financeira no momento.\n\n"
                "Escolher bem o meio de pagamento é parte do mesmo hábito de "
                "perguntar: esse dinheiro eu tenho agora?"
            ),
            "highlights": [
                "Débito e Pix: dinheiro que já existe.",
                "Crédito: compromisso futuro — use quando a parcela cabe no orçamento.",
                "Carteiras digitais: conveniência com os mesmos cuidados do cartão.",
            ],
        },
    ],

    # ── Trilha 4 — Cartão e fatura ───────────────────────────────────────────
    (4, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Uma compra, várias faturas",
            "body": (
                "Quando você parcela uma compra, ela se distribui por meses — e "
                "cada parcela aparece em uma fatura diferente. Entender isso é "
                "essencial para saber quanto do seu limite futuro já está comprometido.\n\n"
                "Você vai interpretar uma fatura com múltiplas compras e parcelas, "
                "rastrear quando cada uma aparece e calcular seu comprometimento total."
            ),
            "highlights": [
                "Interpretar uma fatura de cartão com detalhes",
                "Rastrear parcelas distribuídas por meses",
                "Calcular o comprometimento futuro da renda",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O limite não está sozinho — as parcelas estão",
            "body": (
                "Você aprendeu a ler uma fatura com várias compras, calcular o total "
                "futuro comprometido e decidir se uma nova compra cabe no orçamento "
                "real — não apenas no limite disponível.\n\n"
                "Limite disponível e renda disponível são coisas diferentes. Sempre "
                "calcule o comprometimento total antes de parcelar."
            ),
            "highlights": [
                "Fatura é o resumo do ciclo — parcelas futuras ficam fora dela.",
                "Comprometimento futuro = soma de todas as parcelas em aberto.",
                "Limite livre ≠ dinheiro disponível no orçamento.",
            ],
        },
    ],

    (4, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O mínimo parece pouco e custa muito",
            "body": (
                "O pagamento mínimo do cartão é regulamentado por lei desde 2024, "
                "mas mesmo a versão legal pode fazer uma dívida durar anos.\n\n"
                "Você vai calcular o mínimo de uma fatura, projetar o crescimento "
                "da dívida com taxa hipotética e comparar alternativas."
            ),
            "highlights": [
                "Calcular o pagamento mínimo legal",
                "Projetar o crescimento da dívida com juros",
                "Comparar pagamento mínimo, parcial e integral",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Pagar o mínimo é começar uma dívida nova",
            "body": (
                "Você calculou o impacto de pagar só o mínimo e comparou com cenários "
                "de pagamento parcial e integral. A lição é clara: o valor não pago "
                "vira dívida com juros — e o crédito rotativo é um dos mais caros.\n\n"
                "Quando não for possível pagar o integral, pague o máximo possível e "
                "busque alternativas com custo menor do que o rotativo."
            ),
            "highlights": [
                "Mínimo legal: juros + encargos + 1% do principal.",
                "Pagar o mínimo mal reduz o saldo — os juros consomem quase tudo.",
                "Rotativo: avalie empréstimo ou negociação como alternativa mais barata.",
            ],
        },
    ],

    # ── Trilha 5 — Metas e reserva ───────────────────────────────────────────
    (5, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Quantos meses de reserva você precisa?",
            "body": (
                "A resposta depende do seu perfil: tipo de vínculo de trabalho, "
                "estabilidade da renda, número de dependentes e capacidade de "
                "poupar todo mês.\n\n"
                "Você vai usar um método de cálculo para chegar a um número "
                "adequado ao seu momento de vida."
            ),
            "highlights": [
                "Calcular o tamanho ideal com base nas despesas essenciais",
                "Ajustar conforme estabilidade da renda e dependentes",
                "Definir o aporte mensal para chegar à meta",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Sua reserva tem nome, valor e prazo",
            "body": (
                "Você calculou a reserva ideal para diferentes perfis e definiu "
                "o aporte mensal necessário para chegar lá. CLT com renda estável "
                "precisa de menos meses; autônomos e quem tem dependentes precisam "
                "de mais.\n\n"
                "Na próxima missão, você vai aprender a usar e revisar a reserva "
                "quando a vida mudar."
            ),
            "highlights": [
                "Reserva = N meses de despesas essenciais (3 a 12, conforme o perfil).",
                "Renda variável ou dependentes aumentam o número de meses necessários.",
                "Aporte mensal = valor total da reserva ÷ prazo em meses.",
            ],
        },
    ],

    (5, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A reserva foi usada — e agora?",
            "body": (
                "Usar a reserva é exatamente para isso que ela existe. Mas depois "
                "de usá-la, o trabalho é repô-la antes do próximo imprevisto.\n\n"
                "Você vai decidir quando a reserva se justifica, planejar a "
                "recomposição e revisar o tamanho necessário quando a vida mudar."
            ),
            "highlights": [
                "Distinguir emergência real de desejo",
                "Planejar a recomposição da reserva",
                "Revisar o tamanho necessário quando o perfil muda",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "scenario", "activity_order": 5},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A reserva que se renova",
            "body": (
                "Você viu que a reserva existe para emergências reais, não para "
                "desejos, e que recompô-la é tão importante quanto construí-la. "
                "Mudanças de renda ou de dependentes exigem revisão do tamanho.\n\n"
                "Uma reserva em dia significa dormir com menos preocupação."
            ),
            "highlights": [
                "Use a reserva para emergências — não para oportunidades.",
                "Repor a reserva é a primeira prioridade após usá-la.",
                "Mudou de emprego ou teve um dependente? Recalcule o tamanho.",
            ],
        },
    ],

    # ── Trilha 6 — Guardar sem perder o controle ─────────────────────────────
    (6, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Guarde antes de gastar",
            "body": (
                "Guardar o que sobra é uma estratégia que raramente funciona. A "
                "que funciona é outra: separar o que você quer guardar assim que "
                "o dinheiro chegar — antes de qualquer gasto.\n\n"
                "Você vai configurar a separação automática, organizar as categorias "
                "do que sobra e entender por que automatizar é mais eficaz do que "
                "depender da força de vontade."
            ),
            "highlights": [
                "Aplicar a estratégia de guardar antes de gastar",
                "Configurar transferências programadas",
                "Organizar o orçamento por categorias após a separação",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A separação automática fecha o ciclo",
            "body": (
                "Você entendeu por que guardar primeiro funciona melhor do que guardar "
                "o que sobra, e como uma transferência programada torna o hábito "
                "automático — e mais resistente às tentações do mês.\n\n"
                "Na próxima missão, você adapta esse método para rendas que variam."
            ),
            "highlights": [
                "Guardar o que sobra raramente funciona — separe antes.",
                "Transferência programada: automatize o hábito.",
                "Categorize o restante para saber onde o dinheiro vai.",
            ],
        },
    ],

    (6, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Guardar com renda que muda todo mês",
            "body": (
                "Salário fixo facilita o planejamento. Mas e quando a renda varia "
                "por comissão, freelance ou trabalho sazonal?\n\n"
                "Você vai adaptar o método de separação para cada perfil: o CLT "
                "usa percentual fixo; o autônomo usa proporcional; quem tem renda "
                "irregular precisa de um fundo de nivelamento."
            ),
            "highlights": [
                "Adaptar a poupança para renda fixa",
                "Criar separação proporcional para renda variável",
                "Desenvolver um plano para renda irregular",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "scenario", "activity_order": 5},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Um método para cada tipo de renda",
            "body": (
                "Você viu que guardar uma porcentagem de cada recebimento é mais "
                "realista do que um valor fixo quando a renda varia. O fundo de "
                "nivelamento transforma receitas irregulares em um 'salário "
                "autoimposto' mais previsível.\n\n"
                "Com esses ajustes, o hábito de poupar pode funcionar para qualquer "
                "perfil de renda."
            ),
            "highlights": [
                "Percentual fixo é mais resiliente do que valor fixo.",
                "Guardar proporcional ao que entrou funciona para autônomos.",
                "Fundo de nivelamento: acumula nos meses bons, sustenta nos ruins.",
            ],
        },
    ],

    # ── Trilha 7 — Juros e parcelas ──────────────────────────────────────────
    (7, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O preço do tempo",
            "body": (
                "Juros não são um custo arbitrário: são o preço do dinheiro ao "
                "longo do tempo. Entender a diferença entre simples e compostos "
                "explica por que o mesmo valor pode custar muito mais do que parece.\n\n"
                "Você vai calcular os dois tipos e observar como a diferença "
                "cresce com o tempo."
            ),
            "highlights": [
                "Entender juros como preço do tempo",
                "Calcular juros simples e compostos",
                "Perceber o efeito do prazo nos compostos",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {"type": "question", "activity_order": 7},
        {"type": "question", "activity_order": 8},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O tempo muda tudo no cálculo",
            "body": (
                "Você calculou o crescimento com juros simples e compostos e viu "
                "que, nos compostos, os juros incidem sobre os juros anteriores. "
                "No curto prazo parece pouca diferença — no longo prazo, é enorme.\n\n"
                "Esse efeito pode trabalhar a seu favor (em investimentos) ou contra "
                "você (em dívidas). Entender o mecanismo é o primeiro passo."
            ),
            "highlights": [
                "Simples: taxa sobre o capital inicial. Compostos: taxa sobre o montante.",
                "O efeito dos compostos cresce com o prazo.",
                "Mesma lógica em investimentos e em dívidas — sentidos opostos.",
            ],
        },
    ],

    (7, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O custo real da parcela",
            "body": (
                "Uma parcela pequena não significa um crédito barato. O Custo "
                "Efetivo Total (CET) reúne todos os encargos — e é o número que "
                "permite comparar propostas de verdade.\n\n"
                "Você vai calcular o custo total de parcelamentos e interpretar "
                "o CET de contratos fictícios."
            ),
            "highlights": [
                "Calcular o custo total de um parcelamento",
                "Interpretar o CET como ferramenta de comparação",
                "Identificar encargos além da taxa de juros",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Parcela pequena não é crédito barato",
            "body": (
                "Você aprendeu que o CET inclui todos os encargos, não apenas a "
                "taxa de juros, e que comparar pelo CET anual é a forma mais "
                "precisa de avaliar propostas de crédito.\n\n"
                "Na próxima missão, você vai analisar o chamado parcelamento 'sem juros' "
                "e entender o que essa promessa esconde."
            ),
            "highlights": [
                "Custo total = parcela × n. Compare com o preço à vista.",
                "CET reúne todos os encargos — use-o para comparar propostas.",
                "Taxas mensais e anuais seguem regras diferentes de conversão.",
            ],
        },
    ],

    (7, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "\"Sem juros\" — o que isso realmente significa?",
            "body": (
                "Parcelamento sem juros é uma das ofertas mais comuns no varejo "
                "brasileiro. Mas 'sem juros' nem sempre significa 'sem custo'.\n\n"
                "Você vai comparar o preço à vista com o parcelado, analisar "
                "as condições reais da oferta e entender quando o parcelamento "
                "faz sentido — e quando não faz."
            ),
            "highlights": [
                "Comparar preço à vista e parcelado",
                "Identificar custos embutidos no parcelamento",
                "Avaliar o comprometimento futuro da renda",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "tip", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Sem juros pode ter custo — depende da oferta",
            "body": (
                "Você analisou as condições reais de parcelamentos sem juros e "
                "entendeu que nem sempre o custo é zero: pode haver diferença de "
                "preço, comprometimento de limite e ausência de desconto à vista.\n\n"
                "A pergunta certa não é 'tem juros?' — é 'qual o custo total e "
                "o que isso representa no meu orçamento?'"
            ),
            "highlights": [
                "Sem juros ≠ sem custo. Verifique se há desconto à vista.",
                "Parcelar compromete o limite por meses — mesmo sem juros.",
                "Compare o total pago, não apenas o valor da parcela.",
            ],
        },
    ],

    (7, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Comparando ofertas de crédito",
            "body": (
                "Você recebeu três propostas de crédito para o mesmo objetivo. "
                "Taxa, prazo, parcela, total e CET são diferentes em cada uma.\n\n"
                "Neste módulo você vai usar o que aprendeu para comparar as "
                "propostas e escolher a mais adequada para o seu momento."
            ),
            "highlights": [
                "Comparar propostas usando CET e custo total",
                "Avaliar o impacto de prazo e parcela no orçamento",
                "Justificar a escolha com base nos dados",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 1},
        {"type": "question", "activity_order": 2},
        {"type": "scenario", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A melhor proposta é a que você entende",
            "body": (
                "Você comparou propostas usando CET, custo total e impacto no "
                "orçamento — e não apenas a parcela mensal. Esse é o método para "
                "qualquer decisão de crédito.\n\n"
                "Na próxima trilha, você vai ver o que acontece quando a dívida "
                "não é quitada no prazo."
            ),
            "highlights": [
                "CET compara o custo real, não apenas a taxa nominal.",
                "Prazo menor costuma significar menos custo total.",
                "Parcela que cabe no orçamento é condição necessária, não suficiente.",
            ],
        },
    ],

    # ── Trilha 8 — Dívida que cresce ─────────────────────────────────────────
    (8, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A bola de neve começa pequena",
            "body": (
                "Uma dívida que parece controlável pode dobrar em poucos meses se "
                "os juros não forem pagos. Entender como o saldo cresce é o primeiro "
                "passo para interromper o ciclo.\n\n"
                "Você vai calcular o crescimento de uma dívida com taxa hipotética "
                "e ver como o atraso muda tudo."
            ),
            "highlights": [
                "Calcular o crescimento de uma dívida ao longo do tempo",
                "Distinguir saldo devedor, juros e encargos",
                "Entender o efeito do atraso",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O saldo não para de crescer sozinho",
            "body": (
                "Você calculou como juros compostos fazem o saldo crescer sobre "
                "si mesmo — e viu que atraso e pagamento mínimo alimentam a bola "
                "de neve.\n\n"
                "Na próxima missão, você vai calcular especificamente o rotativo "
                "do cartão, que é um dos créditos mais caros do mercado."
            ),
            "highlights": [
                "Saldo devedor + juros compostos = crescimento exponencial.",
                "Pagar menos do que os juros faz a dívida crescer mesmo pagando.",
                "Atraso adiciona multa e mora sobre os juros já acumulados.",
            ],
        },
    ],

    (8, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O rotativo é o crédito mais caro do cartão",
            "body": (
                "Quando você paga menos do que o total da fatura, o saldo restante "
                "entra no crédito rotativo. A taxa é alta — e o efeito é rápido.\n\n"
                "Você vai calcular quanto uma fatura cresce com o rotativo e "
                "comparar o custo com alternativas."
            ),
            "highlights": [
                "Calcular o crescimento com a taxa do rotativo",
                "Comparar o custo com alternativas de crédito",
                "Entender por que o pagamento mínimo não resolve",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Rotativo: saia antes de entrar",
            "body": (
                "Você calculou o custo real do rotativo com taxa hipotética e "
                "comparou com alternativas. A conclusão é clara: o rotativo é "
                "emergencial, não planejado.\n\n"
                "Se entrar no rotativo, saia o mais rápido possível — "
                "preferencialmente com um crédito de custo menor."
            ),
            "highlights": [
                "Rotativo: taxa alta, efeito imediato.",
                "Parcelamento da fatura pode ser mais barato que o rotativo.",
                "Empréstimo pessoal pode sair mais barato — compare o CET.",
            ],
        },
    ],

    (8, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Por qual dívida você começa?",
            "body": (
                "Quando há mais de uma dívida, a ordem importa. Começar pela de "
                "maior taxa reduz o custo total; começar pela menor pode dar "
                "motivação imediata.\n\n"
                "Você vai conhecer as duas estratégias, avaliar propostas de "
                "renegociação e entender quando a portabilidade de crédito faz sentido."
            ),
            "highlights": [
                "Comparar as estratégias avalanche e bola de neve",
                "Avaliar propostas de renegociação",
                "Entender portabilidade de crédito",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Prioridade e negociação: as duas ferramentas",
            "body": (
                "Você aprendeu a priorizar dívidas pela taxa (avalanche) ou pelo "
                "saldo (bola de neve), a avaliar uma proposta de renegociação "
                "pelo CET total e a entender quando a portabilidade ajuda.\n\n"
                "Sair da dívida exige método — e o método mais importante é "
                "nunca deixar de pagar o essencial para honrar uma dívida."
            ),
            "highlights": [
                "Avalanche: pague a maior taxa primeiro.",
                "Bola de neve: pague a menor dívida primeiro para ganhar motivação.",
                "Renegociação: compare o CET, não apenas a parcela.",
            ],
        },
    ],

    # ── Trilha 9 — Inflação e poder de compra ────────────────────────────────
    (9, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Quando os preços sobem, o dinheiro encolhe",
            "body": (
                "Inflação não é apenas preço mais alto: é o seu poder de compra "
                "ficando menor. E o IPCA — índice oficial do Brasil — mede exatamente "
                "isso.\n\n"
                "Você vai entender como a inflação é calculada, por que ela afeta "
                "famílias de formas diferentes e como calcular reajustes."
            ),
            "highlights": [
                "Entender o que é inflação e o IPCA",
                "Calcular o impacto da inflação em um preço",
                "Perceber como diferentes famílias são afetadas",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O IPCA não é o seu IPCA",
            "body": (
                "Você aprendeu que o IPCA mede a inflação de uma cesta representativa "
                "de bens e que famílias com perfis diferentes sentem inflações "
                "diferentes. Reajustar um valor pelo IPCA preserva o poder de compra.\n\n"
                "Na próxima missão, você vai usar isso para calcular o rendimento real "
                "de uma aplicação."
            ),
            "highlights": [
                "IPCA: variação de uma cesta representativa de bens e serviços.",
                "Famílias diferentes têm inflações percebidas diferentes.",
                "Reajuste pelo IPCA preserva o poder de compra — não aumenta.",
            ],
        },
    ],

    (9, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O que o rendimento realmente comprou para você?",
            "body": (
                "Um rendimento de 5% ao ano parece bom. Mas se a inflação foi de "
                "6%, você perdeu poder de compra.\n\n"
                "Você vai calcular o rendimento real, entender a fórmula exata "
                "e usá-la para comparar situações."
            ),
            "highlights": [
                "Calcular o rendimento real",
                "Diferenciar nominal de real com a fórmula correta",
                "Comparar situações de ganho e perda real",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Rendimento real: o número que importa",
            "body": (
                "Você calculou o rendimento real usando a fórmula de Fisher e "
                "viu como uma aplicação pode parecer lucrativa nominalmente mas "
                "representar uma perda real.\n\n"
                "Na próxima missão, você vai usar esse conceito para tomar "
                "decisões financeiras comparando alternativas."
            ),
            "highlights": [
                "Rendimento real ≈ nominal − inflação (para taxas pequenas).",
                "Fórmula exata: (1 + nominal) / (1 + inflação) − 1.",
                "Rendimento abaixo da inflação = perda de poder de compra.",
            ],
        },
    ],

    (9, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A inflação e as suas decisões",
            "body": (
                "Agora que você entende inflação e rendimento real, chegou a hora "
                "de usar esses conceitos para comparar alternativas e tomar "
                "decisões mais fundamentadas.\n\n"
                "Você vai analisar cenários que combinam inflação, rendimento e "
                "escolhas do dia a dia."
            ),
            "highlights": [
                "Aplicar rendimento real em comparações",
                "Avaliar quando a inflação muda a melhor decisão",
                "Interpretar dados de inflação para o orçamento",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Inflação muda o que vale a pena",
            "body": (
                "Você aplicou o conceito de rendimento real em decisões concretas "
                "e viu como a inflação muda o que é vantajoso guardar, investir "
                "ou gastar.\n\n"
                "Esse olhar vai ser fundamental na próxima trilha, onde você "
                "compara produtos de renda fixa."
            ),
            "highlights": [
                "Compare aplicações pelo rendimento real, não nominal.",
                "IPCA varia — consulte a fonte oficial para valores atuais.",
                "Inflação afeta decisões de compra, salário e investimento.",
            ],
        },
    ],

    # ── Trilha 10 — Onde o dinheiro rende ────────────────────────────────────
    (10, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Por que investir — e por onde começar",
            "body": (
                "Guardar dinheiro em conta corrente pode fazer o valor encolher "
                "com a inflação. Investir é o caminho para preservar e aumentar "
                "o poder de compra.\n\n"
                "Você vai entender a relação entre risco, liquidez e rendimento, "
                "e por que não existe aplicação perfeita."
            ),
            "highlights": [
                "Entender risco, liquidez e rendimento",
                "Perceber que mais rendimento costuma exigir mais prazo ou risco",
                "Reconhecer o papel do objetivo na escolha da aplicação",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Não existe aplicação perfeita",
            "body": (
                "Você aprendeu que rendimento, liquidez e risco formam um triângulo "
                "onde melhorar um lado costuma piorar outro. O objetivo do investimento "
                "é o que determina qual equilíbrio faz mais sentido.\n\n"
                "Na próxima missão, você vai conhecer os principais produtos de renda fixa."
            ),
            "highlights": [
                "Risco, liquidez e rendimento formam um triângulo de equilíbrio.",
                "Mais rendimento: aceite mais prazo ou mais risco.",
                "O objetivo define qual equilíbrio é o adequado.",
            ],
        },
    ],

    (10, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Os produtos de renda fixa",
            "body": (
                "CDB, LCI, LCA, Tesouro Direto: cada produto tem características "
                "próprias de rentabilidade, liquidez, prazo e cobertura pelo FGC.\n\n"
                "Você vai aprender o que diferencia cada um para poder comparar "
                "com critério."
            ),
            "highlights": [
                "Conhecer as características dos principais produtos",
                "Comparar liquidez, prazo e rentabilidade",
                "Identificar o que o FGC cobre e o que fica de fora",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Cada produto serve a um objetivo",
            "body": (
                "Você conheceu os produtos de renda fixa mais comuns e suas "
                "características. O produto certo não é o de maior rendimento "
                "— é o que combina com o prazo, a liquidez necessária e o perfil "
                "de risco do seu objetivo.\n\n"
                "Na próxima missão, você vai entender o FGC e a tributação em detalhe."
            ),
            "highlights": [
                "CDB: emitido por bancos, tributação IR regressiva.",
                "LCI/LCA: isentos de IR para PF, exigem prazo mínimo.",
                "Tesouro Direto: emissor federal, liquidez diária, vários indexadores.",
            ],
        },
    ],

    (10, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "FGC e tributação: dois fatores que mudam tudo",
            "body": (
                "O Fundo Garantidor de Créditos protege parte dos seus investimentos "
                "em caso de quebra da instituição. E o IR regressivo sobre renda "
                "fixa significa que prazo mais longo costuma ser mais eficiente.\n\n"
                "Você vai entender o que o FGC cobre, até que limite, e como a "
                "tributação afeta o rendimento líquido."
            ),
            "highlights": [
                "Entender a cobertura do FGC e seus limites",
                "Calcular o rendimento líquido após IR",
                "Diferenciar produtos cobertos e não cobertos",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "FGC protege — mas tem limites",
            "body": (
                "Você aprendeu que o FGC cobre depósitos e alguns títulos até "
                "determinado limite por instituição, e que o Tesouro Direto não "
                "precisa do FGC — tem o emissor federal como garantidor.\n\n"
                "A tributação regressiva do IR incentiva investimentos de prazo "
                "mais longo — isso muda o rendimento líquido real."
            ),
            "highlights": [
                "FGC: limite por CPF e por instituição — consulte o site oficial.",
                "Tesouro Direto: garantia do governo federal, não do FGC.",
                "IR regressivo: quanto maior o prazo, menor a alíquota.",
            ],
        },
    ],

    (10, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Hora de comparar e escolher",
            "body": (
                "Você tem R$ 10.000 e dois objetivos: uma reserva de emergência "
                "e uma viagem em 2 anos. Quatro opções estão disponíveis, com "
                "características diferentes de liquidez, prazo, cobertura e "
                "rendimento.\n\n"
                "Este módulo integra tudo o que você aprendeu na Trilha 10."
            ),
            "highlights": [
                "Comparar produtos com critérios múltiplos",
                "Distribuir entre objetivo de curto e longo prazo",
                "Justificar a escolha com dados",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 1},
        {"type": "question", "activity_order": 2},
        {"type": "scenario", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A escolha certa depende do objetivo certo",
            "body": (
                "Você distribuiu recursos entre objetivos de curto e longo prazo "
                "considerando liquidez, cobertura do FGC, tributação e rendimento.\n\n"
                "Este é o processo que acompanha qualquer decisão de onde guardar "
                "ou investir dinheiro: entender o objetivo antes de escolher o produto."
            ),
            "highlights": [
                "Reserva: liquidez diária, cobertura pelo FGC.",
                "Objetivo de médio prazo: prazo compatível, tributação menor.",
                "Compare sempre o rendimento líquido — depois do IR e da inflação.",
            ],
        },
    ],

    # ── Trilha 11 — Golpes e proteção de dados ───────────────────────────────
    (11, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Como os golpistas pensam",
            "body": (
                "Phishing, engenharia social, falsa central, falso parente: cada "
                "golpe usa uma mecânica diferente, mas todos exploram pressa, "
                "emoção e falta de verificação.\n\n"
                "Você vai conhecer os tipos mais comuns para reconhecê-los antes "
                "de se tornar uma vítima."
            ),
            "highlights": [
                "Reconhecer os principais tipos de golpe",
                "Identificar as táticas usadas pelos golpistas",
                "Aprender a verificar antes de agir",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Reconhecer é a primeira linha de defesa",
            "body": (
                "Você aprendeu os padrões de golpe mais frequentes e viu que "
                "urgência, pressão e pedido de segredo são sinais universais "
                "de fraude.\n\n"
                "Na próxima missão, você vai focar nos golpes que envolvem Pix — "
                "por onde a maioria das fraudes digitais passa hoje."
            ),
            "highlights": [
                "Urgência + pedido de dados ou dinheiro = sinal de alerta.",
                "Golpistas imitam bancos, familiares e autoridades.",
                "Verifique sempre por um canal que você iniciou.",
            ],
        },
    ],

    (11, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Os golpes que chegam pelo Pix",
            "body": (
                "O Pix é instantâneo e irreversível — o que o torna alvo preferido "
                "de golpistas. Comprovante falso, falso parente, falsa devolução: "
                "cada variante usa a velocidade do Pix contra a vítima.\n\n"
                "Você vai reconhecer os golpes mais comuns e o MED — Mecanismo "
                "Especial de Devolução para golpes."
            ),
            "highlights": [
                "Reconhecer golpes que usam o Pix",
                "Entender o MED e seus critérios",
                "Saber o que o MED não cobre",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "tip", "content_order": 6},
        {"type": "scenario", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O Pix não volta — o MED pode tentar",
            "body": (
                "Você entendeu que o Pix concluído não é cancelado como um cartão "
                "e que o MED existe para casos de golpe — não para erro do pagador. "
                "Acionar rápido e documentar tudo aumenta as chances de recuperação.\n\n"
                "A proteção dos seus dados é o tema da próxima missão."
            ),
            "highlights": [
                "Pix concluído é irreversível — o MED não é garantia de devolução.",
                "MED cobre golpes; erro do pagador não é elegível automaticamente.",
                "Acione o banco imediatamente e documente tudo.",
            ],
        },
    ],

    (11, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A senha que você não vai compartilhar",
            "body": (
                "Roubo de credenciais, código de verificação repassado por engano, "
                "contas laranja: a proteção dos seus dados é a última linha de "
                "defesa antes do golpe acontecer.\n\n"
                "Você vai aprender hábitos de segurança digital e entender "
                "o que são contas laranja."
            ),
            "highlights": [
                "Proteger senhas e dados de acesso",
                "Adotar hábitos de segurança em dispositivos e redes",
                "Entender o que são contas laranja e seus riscos",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Seus dados são a chave — proteja-os",
            "body": (
                "Você aprendeu que senhas fortes e únicas, verificação em duas "
                "etapas e cuidado em redes públicas formam uma barreira real. "
                "Também viu que usar sua conta para terceiros (conta laranja) "
                "tem consequências penais.\n\n"
                "Na próxima missão, você vai saber o que fazer depois que um golpe acontece."
            ),
            "highlights": [
                "Nunca compartilhe códigos de verificação.",
                "Senhas diferentes por serviço + verificação em duas etapas.",
                "Conta laranja é crime — mesmo sem saber que está participando.",
            ],
        },
    ],

    (11, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Caiu no golpe — o que fazer agora",
            "body": (
                "Reconhecer que foi vítima de golpe é difícil. Mas agir rápido "
                "pode fazer diferença na recuperação do dinheiro.\n\n"
                "Você vai aprender o passo a passo: contato com o banco, "
                "registro das evidências, comunicação às autoridades e "
                "acompanhamento do caso."
            ),
            "highlights": [
                "Agir imediatamente após perceber o golpe",
                "Registrar evidências e boletim de ocorrência",
                "Entender o que pode e o que não pode ser recuperado",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Rápido e documentado: as duas regras",
            "body": (
                "Você aprendeu que velocidade e documentação são os dois fatores "
                "que mais influenciam a chance de recuperação. Contate o banco, "
                "registre evidências, faça o boletim e acompanhe.\n\n"
                "A última missão coloca em prática o reconhecimento rápido em "
                "cenários simulados."
            ),
            "highlights": [
                "Contate o banco imediatamente — cada minuto conta.",
                "Documente tudo: capturas de tela, conversas, dados do golpista.",
                "Boletim de ocorrência é necessário para o MED e para processos legais.",
            ],
        },
    ],

    (11, 5): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Treinamento de reconhecimento",
            "body": (
                "Esta é a missão final da Trilha 11. Você vai enfrentar cenários "
                "simulados de tentativa de golpe e treinar o reconhecimento rápido "
                "— a habilidade mais importante para se proteger.\n\n"
                "Leia cada cenário, identifique os sinais e tome a decisão correta."
            ),
            "highlights": [
                "Identificar tentativas de golpe em cenários realistas",
                "Tomar a decisão certa sob pressão simulada",
                "Consolidar os hábitos de proteção da trilha",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {"type": "question", "activity_order": 5},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Você reconheceu os sinais",
            "body": (
                "Você treinou o reconhecimento rápido em cenários que imitam "
                "golpes reais. Cada acerto reforça o hábito de parar, verificar "
                "e só então agir.\n\n"
                "A Trilha 12 — o Desafio integrador — vai testar todas as "
                "competências das 11 trilhas anteriores em cenários combinados."
            ),
            "highlights": [
                "Urgência + pedido de dados ou dinheiro = não aja sem verificar.",
                "Verifique sempre por um canal que você iniciou.",
                "Um segundo de pausa pode evitar meses de prejuízo.",
            ],
        },
    ],

    # ── Trilha 12 — Desafio integrador ───────────────────────────────────────
    (12, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cenário 1: o primeiro salário chegou",
            "body": (
                "A Luana recebeu o primeiro salário. Ela tem contas essenciais, "
                "uma dívida pequena, uma meta de reserva e um desejo. A renda "
                "não dá para tudo.\n\n"
                "Você vai tomar as decisões por ela — e ver as consequências."
            ),
            "highlights": [
                "Organizar o orçamento do primeiro salário",
                "Priorizar sem comprometer o essencial",
                "Calcular quanto sobra para meta e lazer",
            ],
        },
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O primeiro salário organizado",
            "body": (
                "Você distribui a renda da Luana entre essenciais, dívida, reserva "
                "e lazer — sem ultrapassar o que ela tem. Cada decisão foi uma "
                "aplicação do que você aprendeu nas Trilhas 1 e 2.\n\n"
                "No próximo cenário, o dinheiro no digital entra em cena."
            ),
            "highlights": [
                "Essenciais primeiro; dívidas com juros antes de lazer.",
                "Reserva é prioridade, mesmo pequena no começo.",
                "O que sobra é lazer — não o que você não planejou.",
            ],
        },
    ],

    (12, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cenário 2: pagamentos e cartão",
            "body": (
                "A Luana precisa pagar o aluguel, fazer uma compra parcelada e "
                "decidir entre Pix e cartão. Ela também recebeu uma fatura com "
                "surpresas.\n\n"
                "Você vai navegar pelas decisões de pagamento e cartão com tudo "
                "o que aprendeu nas Trilhas 3 e 4."
            ),
            "highlights": [
                "Escolher o meio de pagamento adequado",
                "Interpretar a fatura e suas consequências",
                "Calcular o comprometimento futuro com parcelas",
            ],
        },
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Cada pagamento é uma decisão",
            "body": (
                "Você escolheu os meios de pagamento e interpretou a fatura da "
                "Luana. As Trilhas 3 e 4 ficaram evidentes: o meio certo e "
                "o comprometimento futuro são inseparáveis da decisão.\n\n"
                "O próximo cenário envolve crédito, dívida e inflação."
            ),
            "highlights": [
                "Pix é irreversível — confirme antes.",
                "Fatura: comprometimento futuro importa mais do que o limite disponível.",
                "Parcelamento sem juros pode ter custo embutido — compare.",
            ],
        },
    ],

    (12, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cenário 3: um imprevisto e uma proposta de crédito",
            "body": (
                "A reserva da Luana foi parcialmente usada em um imprevisto. "
                "Agora ela precisa de crédito para um objetivo e recebeu três "
                "propostas com taxas e prazos diferentes.\n\n"
                "Você vai ajudá-la a comparar as propostas e reconstruir a reserva."
            ),
            "highlights": [
                "Comparar propostas de crédito usando CET",
                "Planejar a recomposição da reserva",
                "Calcular o rendimento real após inflação",
            ],
        },
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Crédito com critério, reserva reposta",
            "body": (
                "Você escolheu a proposta de crédito com melhor CET e planejou "
                "a recomposição da reserva da Luana. As Trilhas 7, 8 e 9 foram "
                "acionadas para chegar às melhores decisões.\n\n"
                "O último cenário fecha a jornada com um teste de segurança digital."
            ),
            "highlights": [
                "CET compara o custo real, não apenas a taxa anunciada.",
                "Reserva usada: reponha antes de assumir novos objetivos.",
                "Rendimento real = quanto o dinheiro cresceu acima da inflação.",
            ],
        },
    ],

    (12, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cenário 4: alerta de fraude",
            "body": (
                "A Luana recebeu uma mensagem urgente dizendo que sua conta foi "
                "invadida. O 'atendente' pede que ela transfira o dinheiro para "
                "uma 'conta segura' e informe o token.\n\n"
                "Este é o cenário final. Você vai reconhecer o golpe e tomar as "
                "decisões corretas."
            ),
            "highlights": [
                "Reconhecer o golpe da falsa central",
                "Tomar as ações corretas imediatamente",
                "Proteger dados e evitar a transferência",
            ],
        },
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A jornada completa em quatro cenários",
            "body": (
                "Você atravessou a jornada completa da Luana: organizou o primeiro "
                "salário, gerenciou pagamentos e fatura, comparou crédito e planejou "
                "a reserva, e reconheceu um golpe na hora certa.\n\n"
                "As 12 trilhas estão conectadas: cada decisão financeira usa "
                "conhecimentos de mais de uma delas. Parabéns — você concluiu a "
                "jornada."
            ),
            "highlights": [
                "Banco legítimo nunca pede transferência para 'conta segura'.",
                "Token é seu — nunca compartilhe com ninguém.",
                "A jornada completa conecta salário, orçamento, crédito e segurança.",
            ],
        },
    ],

    # ── Expansões das trilhas 2 e 3 (missões existentes expandidas) ──────────
    (2, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Necessidade ou desejo? A pergunta que muda as suas prioridades",
            "body": (
                "Nem todo gasto é igual. Alguns não podem esperar — sem eles, "
                "a saúde, o trabalho ou a moradia ficam em risco. "
                "Outros melhoram a vida, mas podem ser adiados.\n\n"
                "Você vai aprender a distinguir os dois e, principalmente, "
                "a priorizar com base na consequência de não pagar."
            ),
            "highlights": [
                "Necessidade: ausência gera dano imediato",
                "Desejo: pode esperar sem consequência grave",
                "Contexto importa: o mesmo item pode ser os dois",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "tip", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {"type": "question", "activity_order": 7},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Prioridades claras, decisões mais fáceis",
            "body": (
                "Você aprendeu a distinguir necessidade de desejo pelo contexto e "
                "pela consequência de não pagar. Aluguel, alimentação e transporte "
                "vêm antes — não porque você prefere, mas porque as consequências "
                "de não pagá-los são imediatas e graves.\n\n"
                "Com isso, fica mais fácil dizer 'não' a um gasto sem sentir culpa: "
                "você está protegendo o que realmente importa."
            ),
            "highlights": [
                "Pergunte: 'O que acontece se eu não pagar isso?'",
                "Consequência grave = necessidade; sem consequência imediata = desejo.",
                "O contexto muda a classificação — o mesmo item pode ser os dois.",
            ],
        },
    ],

    (2, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O dinheiro tem destino — ou desaparece",
            "body": (
                "Sem um plano, o salário entra e some. Com um orçamento simples, "
                "você direciona cada real para onde ele precisa ir antes que "
                "apareça uma oportunidade de gastá-lo em outra coisa.\n\n"
                "Você vai montar um orçamento básico, entender a ordem correta "
                "de prioridades e saber o que fazer quando o dinheiro não fecha."
            ),
            "highlights": [
                "Ordem: essenciais → dívidas → reserva → desejos",
                "Separar a reserva no início do mês garante que acontece",
                "Déficit? Corte uma categoria não essencial, não o essencial",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "scenario", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "example", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "explanation", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {"type": "question", "activity_order": 7},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Orçamento montado, controle nas mãos",
            "body": (
                "Você aprendeu a distribuir a renda na ordem certa: "
                "essenciais primeiro, dívidas depois, reserva antes dos desejos. "
                "E quando o orçamento fecha negativo, a solução é cortar o não essencial, "
                "não ignorar o problema.\n\n"
                "Guardar no início do mês é a estratégia mais simples e eficaz — "
                "o dinheiro que não se vê não se gasta."
            ),
            "highlights": [
                "Essenciais → dívidas → reserva → desejos.",
                "Guardar primeiro é mais eficaz do que guardar o que sobra.",
                "Déficit = cortar lazer, não comprometer moradia ou saúde.",
            ],
        },
    ],

    (3, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O meio certo para cada compra",
            "body": (
                "Pix, débito, crédito, boleto — cada meio de pagamento tem "
                "características diferentes. Escolher o errado pode custar dinheiro, "
                "criar dívida ou simplesmente não funcionar quando você precisa.\n\n"
                "Você vai entender como cada um funciona e quando usá-lo."
            ),
            "highlights": [
                "Débito e Pix: saldo na hora",
                "Crédito: compromete a renda futura na fatura",
                "Boleto: compensação mais lenta — até 3 dias úteis",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "explanation", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "tip", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Cada real no lugar certo",
            "body": (
                "Você agora distingue os principais meios de pagamento: "
                "débito e Pix debitam na hora, crédito compromete a fatura futura "
                "e boleto pode demorar dias para compensar.\n\n"
                "Com esse mapa, você escolhe o meio mais adequado para cada situação "
                "sem comprometer o saldo ou criar dívida desnecessária."
            ),
            "highlights": [
                "Débito e Pix: saída imediata — precisa ter saldo.",
                "Crédito: paga depois — controle a fatura.",
                "Boleto: use quando o prazo não for urgente.",
            ],
        },
    ],

    (3, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Conferir antes de confirmar: o único escudo que funciona",
            "body": (
                "O Pix é instantâneo e irreversível. Um erro de digitação, "
                "um comprovante falso ou um QR Code adulterado — e o dinheiro foi.\n\n"
                "Você vai aprender o que verificar antes de confirmar qualquer "
                "pagamento e o que fazer se algo der errado."
            ),
            "highlights": [
                "Verifique nome, chave, valor e banco antes de confirmar",
                "Comprovante não é prova — verifique no extrato",
                "MED é para fraudes; erro de transferência tem processo diferente",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "explanation", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "tip", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Conferir é o seu escudo",
            "body": (
                "Você aprendeu a checagem antes de confirmar e a identificar "
                "comprovantes falsos e QR Codes adulterados. "
                "O MED não resolve tudo — o hábito de verificar é a única "
                "proteção confiável.\n\n"
                "Para erros de transferência: contate o banco imediatamente. "
                "Para fraudes: aja rápido, guarde comprovantes e registre BO."
            ),
            "highlights": [
                "Verifique nome e CPF do destinatário antes de confirmar.",
                "Extrato, não comprovante externo, é a confirmação válida.",
                "MED = fraude confirmada; erro = devolução voluntária.",
            ],
        },
    ],

    # ── Trilha 4 — Cartão e fatura (missão 4.1 — expansão) ───────────────────
    (4, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O cartão não é seu dinheiro",
            "body": (
                "Limite de crédito não é saldo disponível — é um empréstimo "
                "pré-aprovado que você paga depois, com ou sem juros.\n\n"
                "Você vai entender como o ciclo de fechamento e vencimento "
                "determina quando cada compra precisa ser paga e o que "
                "acontece se a fatura não for quitada integralmente."
            ),
            "highlights": [
                "Distinguir limite de crédito de dinheiro disponível",
                "Entender o ciclo fechamento/vencimento do cartão",
                "Calcular quando uma compra entra em qual fatura",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Limite é crédito — use como se fosse dívida",
            "body": (
                "Você aprendeu que o limite do cartão não é seu dinheiro: "
                "é crédito do banco que você paga na fatura. Entendeu o "
                "ciclo fechamento/vencimento e como calcular quando uma "
                "compra entra em qual fatura.\n\n"
                "Com isso, você pode usar o cartão de forma estratégica — "
                "e evitar o rotativo, um dos créditos mais caros do mercado."
            ),
            "highlights": [
                "Limite ≠ dinheiro seu — é crédito a ser pago na fatura.",
                "Compra antes do fechamento: fatura atual. Depois: próxima fatura.",
                "Não pagou o total? Rotativo incide sobre o saldo em aberto.",
            ],
        },
    ],

    # ── Trilha 5 — Metas e reserva (missão 5.1 — expansão) ───────────────────
    (5, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Para que serve o dinheiro guardado?",
            "body": (
                "Há uma diferença fundamental entre guardar para imprevistos "
                "e guardar para objetivos planejados — e misturá-los é o "
                "erro mais comum em finanças pessoais.\n\n"
                "Você vai aprender a distinguir reserva de emergência de meta "
                "financeira e entender por que imprevistos são inevitáveis "
                "para todo mundo."
            ),
            "highlights": [
                "Distinguir reserva de emergência de objetivo financeiro",
                "Entender por que imprevistos acontecem com todo mundo",
                "Reconhecer o custo de não ter reserva",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Reserva e meta: funções diferentes, contas separadas",
            "body": (
                "Você distinguiu reserva de emergência (acesso imediato, sem prazo) "
                "de objetivo financeiro (valor e prazo definidos). Viu que misturar "
                "os dois deixa você sem proteção quando o imprevisto chegar.\n\n"
                "Na próxima missão, você vai calcular o tamanho ideal da reserva "
                "para o seu perfil."
            ),
            "highlights": [
                "Reserva: para imprevistos. Meta: para objetivos planejados.",
                "Imprevistos acontecem — a reserva elimina o custo extra de lidar com eles.",
                "Misturar os dois deixa você sem proteção.",
            ],
        },
    ],

    # ── Trilha 5 — Metas e reserva (missão 5.3 — expansão) ───────────────────
    (5, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Meta sem número é desejo",
            "body": (
                "Uma meta financeira precisa de três elementos: o que você quer, "
                "quanto custa e em quantos meses quer chegar lá.\n\n"
                "Você vai formular metas com valor e prazo, calcular o aporte "
                "mensal necessário e aprender a revisar o plano quando algo muda "
                "no meio do caminho."
            ),
            "highlights": [
                "Formular uma meta com valor e prazo definidos",
                "Calcular o aporte mensal: meta ÷ prazo",
                "Revisar a meta quando a vida mudar",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "scenario", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Metas concretas chegam — desejos vagos não",
            "body": (
                "Você formulou metas com valor e prazo, calculou o aporte mensal "
                "com a fórmula meta ÷ meses e viu que, quando algo muda, revisar "
                "o prazo é melhor do que abandonar a meta.\n\n"
                "Uma meta revisada ainda é uma meta — não é fracasso."
            ),
            "highlights": [
                "Meta = objetivo + valor + prazo. Sem número, é desejo.",
                "Aporte mensal = meta ÷ meses restantes.",
                "Revise o prazo; não abandone a meta.",
            ],
        },
    ],

    # ── Trilha 6 — Guardar sem perder o controle (missão 6.1 — expansão) ─────
    (6, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Guardar o que sobra nunca funciona",
            "body": (
                "Quando você espera sobrar dinheiro para guardar, quase nunca sobra. "
                "O método que funciona é o inverso: separar primeiro, antes de "
                "qualquer gasto.\n\n"
                "Você vai entender a lógica do 'pague-se primeiro', configurar "
                "a separação e aprender por que ter uma conta separada para "
                "a reserva é mais eficaz do que disciplina."
            ),
            "highlights": [
                "Aplicar o método 'pague-se primeiro'",
                "Configurar a separação antes de qualquer gasto",
                "Manter a reserva em conta separada",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "explanation", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "example", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 4},
        {"type": "question", "activity_order": 4},
        {"type": "reading", "content_type": "explanation", "content_order": 5},
        {"type": "question", "activity_order": 5},
        {"type": "reading", "content_type": "example", "content_order": 6},
        {"type": "question", "activity_order": 6},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Separação automática: o hábito que não depende da vontade",
            "body": (
                "Você viu que guardar o que sobra raramente funciona — "
                "e que separar primeiro, antes de qualquer gasto, transforma "
                "o hábito em automático. Uma conta separada elimina a tentação "
                "de usar a reserva sem perceber.\n\n"
                "Na próxima missão, você aplica esse método para rendas variáveis."
            ),
            "highlights": [
                "Separe primeiro — não espere sobrar.",
                "Transferência automática elimina a decisão mensal.",
                "Conta separada: a reserva fica visível e protegida.",
            ],
        },
    ],
}
