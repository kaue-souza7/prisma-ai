"""Roteiros imersivos dos minicursos das Trilhas 1 a 6.

Cada missão existente é tratada como um minicurso. O roteiro referencia
itens de conteúdo e atividades já versionados, sem duplicar o conteúdo
pedagógico no banco.
"""

LESSON_FLOWS = {
    (1, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O dinheiro que chega não é o dinheiro que fica",
            "body": (
                "O primeiro salário costuma trazer uma sensação de conquista — e "
                "também a primeira surpresa: o valor que cai na conta é menor do "
                "que o combinado.\n\n"
                "Neste módulo, você vai acompanhar um contracheque de verdade, "
                "entender de onde vem essa diferença e calcular quanto realmente "
                "está disponível para planejar o mês."
            ),
            "highlights": [
                "Diferenciar salário bruto de líquido",
                "Reconhecer INSS, IRRF, vale-transporte e FGTS",
                "Calcular o valor que realmente cai na conta",
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
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Seu contracheque agora faz sentido",
            "body": (
                "Você aprendeu a olhar para o salário em camadas: o bruto combinado, "
                "os descontos e o líquido que realmente entra no orçamento. Também "
                "viu que o FGTS não reduz o que você recebe.\n\n"
                "O próximo passo é decidir o que fazer com esse valor antes que ele "
                "se misture aos gastos do mês."
            ),
            "highlights": [
                "Bruto é o valor combinado; líquido é o valor disponível.",
                "INSS, IRRF e vale-transporte podem reduzir o salário.",
                "FGTS é depósito do empregador, não desconto do trabalhador.",
            ],
        },
    ],
    (1, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Quando o dinheiro não dá para tudo",
            "body": (
                "Todo mês alguém precisa escolher o que pagar primeiro. A diferença "
                "entre uma decisão angustiante e uma decisão consciente está em "
                "reconhecer necessidades, desejos e consequências.\n\n"
                "Você vai analisar situações comuns da vida financeira e construir "
                "uma ordem de prioridade que caiba na sua realidade."
            ),
            "highlights": [
                "Separar necessidade de desejo",
                "Priorizar quando a renda é limitada",
                "Perceber como o contexto muda a classificação",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Prioridade não é proibição",
            "body": (
                "Organizar prioridades não significa abandonar tudo o que dá prazer. "
                "Significa proteger o essencial e escolher com clareza o que cabe "
                "agora, o que pode esperar e o que precisa virar objetivo.\n\n"
                "Na próxima missão, você vai transformar essas escolhas em um plano "
                "com valores e destinos."
            ),
            "highlights": [
                "Necessidade atende ao essencial; desejo pode esperar ou ser adaptado.",
                "O contexto e a consequência definem a classificação.",
                "Contas essenciais e dívidas com juros vêm antes dos desejos.",
            ],
        },
    ],
    (1, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Cada real precisa de um destino",
            "body": (
                "Um plano financeiro não é uma planilha complicada. É uma decisão "
                "sobre quanto vai para o essencial, para as dívidas, para os objetivos "
                "e para a reserva — antes de o dinheiro desaparecer.\n\n"
                "Você vai montar um plano com R$ 1.800 líquidos e decidir o que fazer "
                "quando um desejo compete com uma conta atrasada."
            ),
            "highlights": [
                "Distribuir a renda entre prioridades",
                "Justificar escolhas pelas consequências",
                "Separar reserva e objetivos no início do mês",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "scenario", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Seu primeiro plano, com critério",
            "body": (
                "Você transformou uma renda fictícia em decisões concretas: protegeu "
                "o essencial, evitou juros, manteve um objetivo importante e separou "
                "uma reserva. O plano cabe no valor disponível.\n\n"
                "Esse é o hábito que sustenta os próximos meses: dar destino ao "
                "dinheiro antes que ele seja gasto por impulso."
            ),
            "highlights": [
                "Essenciais primeiro; depois dívidas com juros.",
                "Objetivos e reserva fazem parte do plano, não do que sobra.",
                "Desejos entram com o que sobrar, sem comprometer o essencial.",
            ],
        },
    ],
    (2, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Pagar agora ou pagar depois?",
            "body": (
                "Pix, débito e crédito parecem apenas três botões no aplicativo. Na "
                "verdade, cada um muda o momento em que o dinheiro sai do seu bolso "
                "e o risco que você assume.\n\n"
                "Você vai comparar os meios de pagamento e escolher o mais adequado "
                "para compras pequenas, contas e decisões que comprometem meses "
                "seguintes."
            ),
            "highlights": [
                "Entender quando o dinheiro sai da conta",
                "Reconhecer a irreversibilidade do Pix",
                "Avaliar parcelamento e fatura com planejamento",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "question", "activity_order": 3},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O meio de pagamento certo para cada escolha",
            "body": (
                "Você comparou o que sai na hora com o que vira compromisso futuro. "
                "O crédito pode ser útil quando cabe no orçamento e a fatura é paga "
                "inteira, mas ele não cria dinheiro.\n\n"
                "Antes de confirmar, pergunte de onde o valor vai sair e quais serão "
                "as consequências se algo mudar."
            ),
            "highlights": [
                "Pix e débito usam dinheiro que já existe; crédito usa limite.",
                "Pix concluído não é cancelado como uma compra.",
                "Parcelar só faz sentido quando a parcela cabe no orçamento.",
            ],
        },
    ],
    (2, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O cartão tem regras — e datas",
            "body": (
                "Limite não é renda. A fatura não é um valor aleatório. E a diferença "
                "entre fechamento e vencimento pode mudar o mês em que a compra vai "
                "pesar no seu bolso.\n\n"
                "Você vai destrinchar o ciclo do cartão e entender por que pagar só "
                "uma parte da fatura cria uma dívida que cresce."
            ),
            "highlights": [
                "Diferenciar limite, fatura, fechamento e vencimento",
                "Prever em qual fatura uma compra entra",
                "Entender o custo de pagar só o mínimo",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O cartão deixou de ser uma caixa-preta",
            "body": (
                "Você agora sabe que o limite é um teto, que a fatura reúne um ciclo "
                "de compras e que o fechamento define quando a compra entra. Também "
                "viu que o valor não pago não fica congelado: ele vira dívida com "
                "encargos.\n\n"
                "Olhar as duas datas antes de comprar é uma forma simples de escolher "
                "de qual mês sairá o dinheiro."
            ),
            "highlights": [
                "Limite é teto de uso, não renda.",
                "Compra após o fechamento entra na fatura seguinte.",
                "Pagar o total evita juros; pagar parte gera dívida.",
            ],
        },
    ],
    (2, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O clique que pode custar caro",
            "body": (
                "Pagamentos digitais são rápidos, e é justamente essa velocidade que "
                "exige atenção. Um nome diferente na tela, um link com desconto "
                "exagerado ou a pressa de uma mensagem podem ser os últimos avisos "
                "antes de uma perda.\n\n"
                "Você vai praticar conferências, reconhecer sinais de fraude e decidir "
                "o que fazer quando algo dá errado."
            ),
            "highlights": [
                "Conferir recebedor, valor e origem",
                "Reconhecer pressão, link e desconto como sinais de risco",
                "Saber acionar o banco e registrar ocorrência",
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
            "title": "Segurança é um hábito, não um clique",
            "body": (
                "Você treinou o que fazer antes, durante e depois de um pagamento "
                "digital: conferir os dados, desconfiar de pedidos que chegam com "
                "pressa e agir rápido se perceber um golpe.\n\n"
                "Nenhuma conferência é exagero quando o dinheiro não volta "
                "automaticamente. O tempo de alguns segundos protege meses de trabalho."
            ),
            "highlights": [
                "Confira nome do recebedor, valor e origem antes de pagar.",
                "Pressa, link desconhecido e desconto exagerado pedem cautela.",
                "Suspeitou? Conteste no banco e registre boletim de ocorrência.",
            ],
        },
    ],
    (3, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Desejo ou meta?",
            "body": (
                "Querer guardar dinheiro é um começo, mas não é um plano. Uma meta "
                "precisa de valor e prazo para virar ação.\n\n"
                "Neste módulo, você vai transformar um objetivo em uma conta "
                "simples e descobrir o que fazer quando o valor mensal não cabe no "
                "orçamento."
            ),
            "highlights": [
                "Diferenciar desejo de meta",
                "Calcular quanto guardar por mês",
                "Ajustar a meta sem comprometer o essencial",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Uma meta que cabe na vida real",
            "body": (
                "Você aprendeu a dar nome, valor e prazo ao objetivo e a calcular "
                "o esforço mensal. Também viu que ajustar prazo ou valor é melhor "
                "do que comprometer o essencial ou entrar em dívida.\n\n"
                "Na próxima missão, esse valor vai disputar espaço com os outros "
                "gastos do mês."
            ),
            "highlights": [
                "Meta é objetivo, valor e prazo.",
                "O valor mensal é a meta dividida pelo número de meses.",
                "Se não couber, ajuste o prazo ou o valor — não o essencial.",
            ],
        },
    ],
    (3, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Guardar sem viver no limite",
            "body": (
                "Poupar não é cortar tudo. É decidir antes de gastar, proteger o "
                "essencial e dar um limite claro para o lazer.\n\n"
                "Você vai equilibrar um orçamento apertado, encontrar pequenos "
                "gastos que se repetem e escolher uma estratégia que se sustente "
                "no mês seguinte."
            ),
            "highlights": [
                "Equilibrar essenciais, poupança e lazer",
                "Enxergar o peso dos gastos recorrentes",
                "Escolher uma economia realista e segura",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Um plano que cabe no mês inteiro",
            "body": (
                "Você viu que pequenos gastos recorrentes somam e que a economia "
                "mais segura vem de ajustes realistas, não de cortar alimentação "
                "ou usar crédito. Separar a meta no início do mês protege o "
                "plano.\n\n"
                "Agora falta preparar o plano para o que não estava previsto."
            ),
            "highlights": [
                "Poupar é decidir, não eliminar o lazer.",
                "Assinaturas e delivery se acumulam ao longo do ano.",
                "Separe a meta no início do mês, antes dos outros gastos.",
            ],
        },
    ],
    (3, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Quando o plano encontra o imprevisto",
            "body": (
                "Nenhum orçamento está pronto para tudo. A diferença está em ter "
                "um dinheiro separado, seguro e de fácil acesso quando algo "
                "urgente acontece.\n\n"
                "Você vai entender a reserva de emergência, separar imprevisto de "
                "desejo e decidir como agir quando a geladeira quebra."
            ),
            "highlights": [
                "Entender o papel da reserva de emergência",
                "Distinguir imprevisto de desejo",
                "Calcular uma reserva inicial",
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
            "title": "Proteção para o que você não controla",
            "body": (
                "Você entendeu que a reserva existe para imprevistos, não para "
                "promoções, e que segurança e acesso importam mais que rendimento. "
                "Também calculou quanto ela pode alcançar e viu como repor depois "
                "de usar.\n\n"
                "Esse é o primeiro passo para lidar com imprevistos sem "
                "transformar um problema em dívida."
            ),
            "highlights": [
                "A reserva cobre o urgente que não estava no plano.",
                "Segurança e acesso rápido vêm antes do rendimento.",
                "Usou a reserva? Reponha assim que puder.",
            ],
        },
    ],
    (4, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O tempo muda o valor do dinheiro",
            "body": (
                "Juros não são um detalhe de contrato: são o preço do tempo. Eles "
                "podem trabalhar a seu favor ou transformar uma dívida em uma bola "
                "de neve.\n\n"
                "Você vai comparar juros simples e compostos e acompanhar quanto "
                "R$ 1.000 se tornam ao longo de alguns anos."
            ),
            "highlights": [
                "Entender juros como preço do dinheiro no tempo",
                "Diferenciar juros simples de compostos",
                "Estimar o efeito dos juros compostos",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O tempo é parte da conta",
            "body": (
                "Você viu que juros são o preço do dinheiro no tempo e que os "
                "compostos crescem sobre os juros anteriores. A diferença parece "
                "pequena no começo, mas aumenta com o prazo.\n\n"
                "Antes de aceitar qualquer parcela ou aplicação, pergunte a taxa e "
                "o período."
            ),
            "highlights": [
                "Juros podem estar a favor ou contra você.",
                "Juros compostos incidem sobre juros acumulados.",
                "Taxa e prazo mudam completamente o resultado.",
            ],
        },
    ],
    (4, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A parcela esconde o preço",
            "body": (
                "Uma parcela de R$ 190 pode parecer leve. Mas o preço de uma "
                "compra é o total que sai do seu bolso, não o valor que cabe no "
                "mês.\n\n"
                "Você vai calcular o custo total de um parcelamento, comparar com "
                "o preço à vista e avaliar o que os meses seguintes perdem."
            ),
            "highlights": [
                "Calcular o custo total de uma compra parcelada",
                "Comparar com o preço à vista",
                "Perceber o comprometimento dos meses seguintes",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "O preço está no total",
            "body": (
                "Você aprendeu a multiplicar parcela por número de parcelas, "
                "comparar com o preço à vista e identificar o custo do crédito. "
                "Também viu que caber no orçamento não basta.\n\n"
                "A próxima missão olha para o que acontece quando a parcela não é "
                "paga ou quando só o mínimo da fatura é quitado."
            ),
            "highlights": [
                "Custo total = parcela × número de parcelas.",
                "A diferença para o preço à vista é o custo do crédito.",
                "Parcela que cabe não significa compra vantajosa.",
            ],
        },
    ],
    (4, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "A dívida que cresce sozinha",
            "body": (
                "Atraso e pagamento mínimo não congelam uma dívida: eles a "
                "alimentam. Multa, juros e encargos fazem o saldo crescer mesmo "
                "sem novas compras.\n\n"
                "Você vai entender o efeito bola de neve, conhecer o limite legal "
                "dos encargos e escolher por qual dívida começar."
            ),
            "highlights": [
                "Entender atraso, mínimo e juros compostos",
                "Reconhecer o teto legal e seu limite",
                "Priorizar dívidas e negociar",
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
            "title": "Sair da dívida exige ordem",
            "body": (
                "Você viu que o rotativo e o atraso encarecem a dívida, que o "
                "teto legal não a torna barata e que priorizar os juros mais "
                "altos é a decisão mais eficiente. Negociar antes do vencimento "
                "abre mais caminhos.\n\n"
                "O próximo passo é comparar alternativas antes de assumir novas "
                "parcelas."
            ),
            "highlights": [
                "Pagar só o mínimo faz o saldo crescer com juros.",
                "O teto de 100% protege, mas dobrar a dívida ainda é caro.",
                "Juros mais altos primeiro; negocie antes de atrasar.",
            ],
        },
    ],
    (5, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O dinheiro compra menos?",
            "body": (
                "Um preço que sobe não é só um número maior: é uma parte do seu "
                "poder de compra que desaparece. E isso muda o que significa "
                "guardar dinheiro.\n\n"
                "Você vai entender a inflação, calcular seu efeito sobre um preço "
                "e comparar rendimento nominal com rendimento real."
            ),
            "highlights": [
                "Entender inflação e poder de compra",
                "Calcular o efeito da inflação",
                "Distinguir rendimento nominal de real",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Rendimento também se mede em poder de compra",
            "body": (
                "Você viu que inflação é o aumento geral dos preços e que o mesmo "
                "dinheiro passa a comprar menos. Um rendimento só é real quando "
                "supera a inflação.\n\n"
                "Na próxima missão, você vai decidir entre guardar para a reserva "
                "e investir em busca de rendimento."
            ),
            "highlights": [
                "Inflação reduz o poder de compra.",
                "Rendimento nominal é em reais; real desconta a inflação.",
                "Rendimento abaixo da inflação significa perda real.",
            ],
        },
    ],
    (5, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Nem todo dinheiro guardado tem o mesmo objetivo",
            "body": (
                "A reserva precisa estar disponível. Um objetivo distante pode "
                "aceitar mais prazo. Confundir os dois é o que transforma "
                "segurança em risco.\n\n"
                "Você vai diferenciar guardar de investir, reconhecer promessas "
                "impossíveis e escolher características conforme o prazo do "
                "objetivo."
            ),
            "highlights": [
                "Diferenciar reserva de investimento",
                "Reconhecer risco e promessas exageradas",
                "Associar prazo do objetivo à aplicação",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Segurança primeiro, rendimento depois",
            "body": (
                "Você entendeu que a reserva prioriza segurança e liquidez, "
                "enquanto investir envolve aceitar prazo ou risco por rendimento "
                "potencial. Também viu que ganho alto e garantido é sinal de "
                "golpe.\n\n"
                "A última missão compara alternativas fictícias com quatro "
                "características explícitas."
            ),
            "highlights": [
                "Reserva: segurança e acesso rápido.",
                "Investir: prazo ou risco em troca de rendimento potencial.",
                "Promessa de ganho alto e garantido é sinal de alerta.",
            ],
        },
    ],
    (5, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Rendimento não é a única pergunta",
            "body": (
                "Duas aplicações podem render de forma diferente e servir a "
                "objetivos diferentes. Prazo, liquidez, risco e rendimento "
                "precisam ser lidos juntos.\n\n"
                "Você vai comparar alternativas fictícias, entender o papel do "
                "FGC e distribuir o dinheiro entre reserva e viagem."
            ),
            "highlights": [
                "Comparar rendimento, prazo, liquidez e risco",
                "Escolher conforme o objetivo",
                "Entender o que o FGC cobre",
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
            "title": "A escolha depende do objetivo",
            "body": (
                "Você viu que mais rendimento costuma exigir mais prazo ou risco "
                "e que liquidez é decisiva para uma reserva. Também entendeu o "
                "que o FGC cobre e o que fica de fora.\n\n"
                "Agora seu olhar sobre o dinheiro inclui tempo, risco e acesso — "
                "não apenas o saldo."
            ),
            "highlights": [
                "Não existe aplicação com rendimento máximo, liquidez total e risco zero.",
                "Reserva pede liquidez; objetivos longos podem aceitar prazo.",
                "FGC cobre depósitos e alguns títulos, não ações nem Tesouro Direto.",
            ],
        },
    ],
    (6, 1): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "O golpe começa com uma mensagem",
            "body": (
                "Urgência, ameaça e um link: três elementos que aparecem nas "
                "tentativas de phishing todos os dias. Reconhecer o padrão é o "
                "primeiro passo para não cair.\n\n"
                "Você vai analisar mensagens, identificar sinais de alerta e "
                "aprender a verificar tudo por um canal oficial."
            ),
            "highlights": [
                "Reconhecer sinais de phishing",
                "Verificar a origem por um canal oficial",
                "Evitar cliques e respostas de risco",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "Reconhecer é a melhor proteção",
            "body": (
                "Você aprendeu a desconfiar de urgência, ameaça, pedido de dados "
                "e links recebidos. A conferência por aplicativo ou telefone "
                "oficial interrompe o golpe antes do clique.\n\n"
                "A próxima missão aplica essa atenção ao momento de enviar um Pix."
            ),
            "highlights": [
                "Urgência e ameaça são armas do golpista.",
                "Não clique no link: verifique pelo canal oficial.",
                "Bancos não pedem senha nem códigos por mensagem.",
            ],
        },
    ],
    (6, 2): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Antes de tocar em enviar",
            "body": (
                "O Pix sai na hora e não volta como um cartão. É justamente essa "
                "velocidade que exige uma pausa para confirmar quem está pedindo "
                "e para onde o dinheiro vai.\n\n"
                "Você vai reconhecer falsos parentes, falsos bancos e o golpe do "
                "Pix por engano, além de montar um checklist de confirmação."
            ),
            "highlights": [
                "Diferenciar pedido legítimo de suspeito",
                "Reconhecer golpes comuns com Pix",
                "Confirmar antes de enviar",
            ],
        },
        {"type": "reading", "content_type": "explanation", "content_order": 1},
        {"type": "question", "activity_order": 1},
        {"type": "reading", "content_type": "example", "content_order": 2},
        {"type": "question", "activity_order": 2},
        {"type": "reading", "content_type": "tip", "content_order": 3},
        {"type": "question", "activity_order": 3},
        {"type": "question", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A confirmação vem antes do Pix",
            "body": (
                "Você viu que números novos, pressa, segredo e pedidos para pagar "
                "terceiros são sinais de alerta. Confirmar a identidade por outro "
                "canal e conferir o recebedor evita o envio.\n\n"
                "Proteger os dados é o próximo passo para fechar o cerco."
            ),
            "highlights": [
                "Confirme a identidade por outro canal.",
                "O banco nunca pede transferência para uma \"conta segura\".",
                "Pix por engano: confira e use a função \"Devolver\".",
            ],
        },
    ],
    (6, 3): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Seus dados são a chave",
            "body": (
                "Senha, código de verificação e dados do cartão abrem a porta do "
                "seu dinheiro. Nenhum atendente legítimo precisa deles.\n\n"
                "Você vai analisar pedidos de código, práticas de proteção de "
                "contas e ofertas boas demais para ser verdade."
            ),
            "highlights": [
                "Proteger senhas e códigos",
                "Adotar hábitos de segurança digital",
                "Avaliar sites e ofertas antes de pagar",
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
            "title": "Segurança é hábito",
            "body": (
                "Você viu que códigos nunca devem ser compartilhados, que senhas "
                "diferentes e verificação em duas etapas protegem as contas e que "
                "preço, site e forma de pagamento revelam golpes.\n\n"
                "O desafio integrador vai juntar essas decisões às das fases "
                "anteriores."
            ),
            "highlights": [
                "Nunca compartilhe códigos de verificação.",
                "Senhas longas e diferentes + duas etapas.",
                "Preço muito baixo e Pix para pessoa física pedem cautela.",
            ],
        },
    ],
    (6, 4): [
        {
            "type": "intro",
            "agent": "catalyst",
            "title": "Quatro decisões, uma jornada",
            "body": (
                "A Lara tem R$ 2.000 por mês, uma fatura para pagar, um curso, uma "
                "reserva e uma vontade de comprar um notebook. Depois, um "
                "imprevisto e uma mensagem suspeita testam o plano.\n\n"
                "Você vai atravessar quatro decisões que combinam orçamento, "
                "crédito, reserva e segurança digital."
            ),
            "highlights": [
                "Organizar a renda sem gerar dívida",
                "Comparar propostas de crédito pelo total",
                "Usar a reserva e reconhecer um golpe",
            ],
        },
        {"type": "scenario", "activity_order": 1},
        {"type": "scenario", "activity_order": 2},
        {"type": "scenario", "activity_order": 3},
        {"type": "scenario", "activity_order": 4},
        {
            "type": "summary",
            "agent": "analyst",
            "title": "A jornada inteira em quatro escolhas",
            "body": (
                "Você organizou o orçamento sem passar da renda, comparou "
                "propostas de crédito pelo total e pelo tamanho da parcela, usou "
                "a reserva para um imprevisto e ignorou uma mensagem de golpe.\n\n"
                "Essas quatro decisões resumem a jornada: dar destino ao dinheiro, "
                "comparar antes de assumir dívida, proteger o essencial e "
                "desconfiar do que chega com pressa."
            ),
            "highlights": [
                "Cada real tem um destino; a soma não passa da renda.",
                "Compare o custo total e o tamanho da parcela.",
                "Reserva para imprevistos; desconfie de urgência e links.",
            ],
        },
    ],
}
