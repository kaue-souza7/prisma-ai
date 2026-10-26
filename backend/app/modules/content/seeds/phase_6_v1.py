"""Conteúdo versionado da Fase 6 — Proteção digital.

Este módulo é a fonte da migration 0008 e dos testes de contrato. Alterações
editoriais posteriores devem gerar uma nova versão/migração, preservando a
reprodutibilidade do histórico.

Os nomes, valores, mensagens e sites usados nos exemplos e nas simulações são
fictícios. A missão 6.4 é o desafio integrador da jornada.
"""
from app.modules.content.seeds._text import md

PHASE_6_V1 = {
    "phase_number": 6,
    "missions": [
        {
            "number": 1,
            "name": "A mensagem suspeita",
            "description": (
                "Reconheça sinais de phishing e verifique a origem de uma "
                "mensagem por um canal oficial."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.1.1",
                    "name": "Reconhecer sinais de phishing",
                    "description": (
                        "Identifica urgência, ameaça, pedido de dados, links "
                        "estranhos e outros sinais em mensagens, e-mails e "
                        "ligações."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.1.2",
                    "name": "Verificar a origem por um canal oficial",
                    "description": (
                        "Confere a informação abrindo o aplicativo oficial ou "
                        "usando um telefone obtido fora da mensagem recebida."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.1.3",
                    "name": "Evitar ações de risco ao receber mensagens",
                    "description": (
                        "Sabe que não deve clicar no link, responder nem "
                        "compartilhar dados ao receber uma mensagem suspeita."
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
                            "Qual das mensagens abaixo tem mais sinais de "
                            "phishing?"
                        ),
                        "competency_codes": ["6.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "\"Seu extrato de outubro já está disponível "
                                    "no aplicativo do seu banco.\""
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "\"Sua conta será bloqueada em 1 hora. "
                                    "Atualize seus dados agora neste link.\""
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "\"Seu pedido foi entregue. Avalie a compra "
                                    "no aplicativo da loja.\""
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "\"Lembrete: sua fatura vence em 3 dias. "
                                    "Consulte os detalhes no aplicativo.\""
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! Urgência, ameaça de bloqueio e pedido para "
                            "atualizar dados por link são sinais clássicos de "
                            "phishing."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A mensagem com mais sinais de risco "
                            "é a que cria urgência (\"em 1 hora\"), ameaça "
                            "bloquear a conta e pede dados por um link. As outras "
                            "mandam você consultar o aplicativo oficial."
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
                            "Você recebe uma mensagem dizendo ser do seu banco, "
                            "avisando de uma compra suspeita e trazendo um link. "
                            "Qual é a melhor forma de verificar?"
                        ),
                        "competency_codes": ["6.1.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Clicar no link para ver os detalhes da "
                                    "compra."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Responder à mensagem pedindo mais "
                                    "informações."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ignorar o link e abrir o aplicativo oficial "
                                    "do banco, ou ligar para o número do verso do "
                                    "cartão."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Encaminhar a mensagem para amigos "
                                    "perguntando o que acham."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! A verificação deve ser feita por um canal "
                            "oficial que você mesmo abre, como o aplicativo do "
                            "banco ou o número do verso do cartão, nunca pelo "
                            "link recebido."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Clicar no link ou responder à "
                            "mensagem pode entregar seus dados. O correto é "
                            "verificar por um canal oficial que você mesmo abre, "
                            "como o aplicativo do banco ou o número do verso do "
                            "cartão."
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
                            "Ao receber uma mensagem suspeita, qual atitude você "
                            "deve evitar?"
                        ),
                        "competency_codes": ["6.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Clicar no link \"só para ver se é verdade\"."
                                ),
                            },
                            {
                                "value": "b",
                                "label": "Não responder e apagar a mensagem.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Denunciar a mensagem como spam ou golpe."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Conferir a informação por um canal oficial."
                                ),
                            },
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Clicar no link, mesmo \"só para ver\", pode "
                            "levar a um site falso ou instalar algo malicioso. As "
                            "outras atitudes são seguras."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A atitude a evitar é clicar no link "
                            "\"só para ver\". Não responder, denunciar e conferir "
                            "por um canal oficial são atitudes seguras."
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
                            "Você recebe uma mensagem dizendo \"seu CPF será "
                            "bloqueado hoje, regularize neste link\". Descreva, "
                            "passo a passo, o que você faria e quais sinais de "
                            "alerta notou."
                        ),
                        "competency_codes": ["6.1.1", "6.1.2", "6.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Identifica pelo menos dois sinais de alerta, como "
                                "urgência, ameaça, link ou remetente "
                                "desconhecido."
                            ),
                            (
                                "Afirma que não clicaria no link."
                            ),
                            (
                                "Explica que verificaria a informação por um canal "
                                "oficial."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é phishing e como reconhecer",
                    "order": 1,
                    "body": md(
                        """
                        **Phishing** é a tentativa de enganar alguém, passando-se
                        por banco, loja, órgão público ou empresa conhecida, para
                        obter dados, senhas, códigos ou dinheiro.

                        Os principais sinais de alerta:

                        - **Urgência ou ameaça:** "sua conta será bloqueada hoje",
                          "regularize em 1 hora".
                        - **Pedido de dados sigilosos:** senha, código de
                          verificação, número completo do cartão, CVV.
                        - **Link estranho ou encurtado**, ou endereço parecido
                          com o oficial, mas com letras trocadas.
                        - **Remetente desconhecido**, erros de escrita e linguagem
                          estranha.
                        - **Oferta boa demais para ser verdade.**
                        - **Pedido para instalar um aplicativo** ou liberar acesso
                          ao seu celular.

                        Bancos e empresas sérias **não pedem sua senha nem códigos
                        de verificação** por mensagem, ligação ou e-mail.

                        **Como verificar:** não clique no link. Abra o aplicativo
                        oficial ou digite você mesmo o endereço do site. Se for
                        preciso ligar, use o número que está no verso do cartão ou
                        no site oficial, e não o que veio na mensagem.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "A mensagem do \"CPF bloqueado\"",
                    "order": 2,
                    "body": md(
                        """
                        Mensagem fictícia: *"URGENTE: seu CPF será bloqueado hoje.
                        Regularize agora em [link encurtado]."*

                        Sinais de alerta presentes:

                        1. **Urgência** ("hoje", "agora").
                        2. **Ameaça** (bloqueio do CPF).
                        3. **Link encurtado**, que esconde o endereço verdadeiro.
                        4. **Remetente desconhecido**, sem identificação clara.

                        O caminho seguro é não clicar e, se tiver dúvida, procurar
                        o órgão pelos canais oficiais.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Pare, respire, confira",
                    "order": 3,
                    "body": md(
                        """
                        A urgência é a principal arma do golpista: ela tenta
                        impedir que você pense. Antes de agir, pare, respire e
                        confira por um canal oficial.
                        """
                    ),
                },
            ],
        },
        {
            "number": 2,
            "name": "Antes de enviar um Pix",
            "description": (
                "Diferencie pedidos de Pix legítimos de suspeitos e aplique um "
                "procedimento de confirmação antes de enviar."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.2.1",
                    "name": "Diferenciar pedido de Pix legítimo de suspeito",
                    "description": (
                        "Reconhece pedidos que combinam com o contexto e "
                        "desconfia dos que chegam com pressa, segredo ou por "
                        "número novo."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.2.2",
                    "name": "Reconhecer golpes comuns com Pix",
                    "description": (
                        "Identifica falsos parentes, falsos funcionários do banco, "
                        "Pix por engano e comprovantes falsos."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.2.3",
                    "name": "Aplicar um procedimento de confirmação",
                    "description": (
                        "Confirma a identidade por outro canal e confere o nome "
                        "do recebedor e o valor antes de enviar o Pix."
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
                        "prompt": "Qual dos pedidos abaixo é o mais suspeito?",
                        "competency_codes": ["6.2.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Um amigo que você encontra toda semana pede "
                                    "para dividir uma pizza que vocês acabaram de "
                                    "comer juntos."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Alguém que diz ser do banco liga e pede para "
                                    "você transferir seu saldo para uma \"conta "
                                    "segura\"."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Você paga o aluguel ao proprietário que você "
                                    "conhece, depois de conferir o nome do "
                                    "recebedor."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Você paga a padaria usando o QR Code do "
                                    "próprio caixa, na sua frente."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! O banco nunca pede para você transferir seu "
                            "dinheiro para uma \"conta segura\". Esse é um golpe "
                            "clássico."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. O pedido mais suspeito é o da "
                            "ligação do suposto banco, que pede para transferir o "
                            "saldo para uma \"conta segura\". O banco nunca faz "
                            "esse pedido. Nas outras situações, você conhece a "
                            "pessoa ou o local e confere os dados."
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
                            "Você recebe uma mensagem de um número desconhecido: "
                            "\"Oi mãe, troquei de número. Pode pagar esse boleto "
                            "de R$ 800 por Pix pra mim? Depois te explico.\" O que "
                            "fazer?"
                        ),
                        "competency_codes": ["6.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Pagar logo, porque a mensagem parece vir de "
                                    "um filho."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pagar metade do valor e pedir o resto "
                                    "depois."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Responder pedindo o comprovante da dívida."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Ligar para o número antigo ou falar "
                                    "pessoalmente com a pessoa antes de enviar "
                                    "qualquer valor."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Correto! Esse é o golpe do falso parente. Confirmar "
                            "a identidade por outro canal, como o número antigo, é "
                            "o que protege você."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Esse é o golpe do falso parente. O "
                            "caminho seguro é confirmar a identidade por outro "
                            "canal, ligando para o número antigo ou falando "
                            "pessoalmente, antes de enviar qualquer valor."
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
                            "Uma pessoa diz que fez um Pix para você por engano e "
                            "pede devolução. O que você deve fazer?"
                        ),
                        "competency_codes": ["6.2.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Fazer um novo Pix para a conta que ela "
                                    "passar, o mais rápido possível."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Conferir no seu aplicativo se o valor "
                                    "realmente entrou e, se entrou, usar a função "
                                    "\"Devolver\" da própria transação."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Devolver o dobro, para evitar problemas."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Ignorar e bloquear a pessoa, mesmo que o "
                                    "valor tenha entrado."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Muito bem! Primeiro confira se o valor entrou. Se "
                            "entrou, a função \"Devolver\" do aplicativo refaz o "
                            "caminho da transação original e evita que você envie "
                            "dinheiro para outra conta indicada por um golpista."
                        ),
                        "feedback_incorrect": (
                            "Revise o procedimento. Primeiro confira se o valor "
                            "entrou. Se entrou, use a função \"Devolver\" ligada à "
                            "transação original, em vez de fazer um novo Pix para "
                            "uma conta que a pessoa informe."
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
                            "Escreva as 3 perguntas que você faria a si mesmo "
                            "antes de enviar um Pix a alguém que acabou de pedir "
                            "dinheiro por mensagem."
                        ),
                        "competency_codes": ["6.2.1", "6.2.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Inclui confirmar a identidade da pessoa por outro "
                                "canal."
                            ),
                            (
                                "Inclui observar urgência, pressão ou pedido de "
                                "segredo."
                            ),
                            (
                                "Inclui conferir o nome do recebedor ou o valor."
                            ),
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Golpes comuns com Pix",
                    "order": 1,
                    "body": md(
                        """
                        Alguns golpes que se repetem:

                        - **Falso parente ou amigo:** uma mensagem de um número
                          novo diz "mudei de número, pode pagar uma conta para
                          mim?".
                        - **Falso funcionário do banco:** alguém liga dizendo que
                          sua conta está em risco e pede para você transferir o
                          saldo para uma "conta segura". O banco **nunca** pede
                          isso.
                        - **"Pix por engano":** alguém diz que fez um Pix para
                          você por engano e pede devolução. Antes de qualquer
                          coisa, confira no seu aplicativo se o valor realmente
                          entrou. Se entrou, use a função **"Devolver"** ligada
                          àquela transação, dentro do próprio aplicativo, e não
                          faça um novo Pix manual.
                        - **Falso comprovante de pagamento:** um comprovante falso
                          é enviado para convencer o vendedor a entregar o
                          produto.
                        - **Anúncio ou oferta boa demais**, que exige Pix
                          imediato.

                        **Checklist antes de enviar:**

                        1. **Quem está pedindo?** Consigo confirmar por **outro
                           canal** (ligação para o número antigo, conversa
                           pessoal)?
                        2. Existe **urgência**, pressão ou pedido de segredo?
                        3. O **nome do recebedor** na tela de confirmação bate com
                           quem eu espero?
                        4. Se algo não fecha, **não envie**.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "\"Oi mãe, mudei de número\"",
                    "order": 2,
                    "body": md(
                        """
                        Mensagem fictícia, de um número desconhecido: *"Oi mãe,
                        troquei de número e o antigo não funciona mais. Pode pagar
                        esse boleto de R$ 800 por Pix pra mim? Depois te
                        explico."*

                        Sinais de alerta: número novo, urgência, valor alto,
                        pedido para pagar para terceiros e "depois te explico". O
                        caminho seguro é **ligar para o número antigo** ou falar
                        pessoalmente com a pessoa antes de enviar qualquer valor.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Combine uma pergunta-teste",
                    "order": 3,
                    "body": md(
                        """
                        Combine com a família uma pergunta que só vocês saberiam
                        responder. Se alguém pedir dinheiro em nome de um parente,
                        faça a pergunta antes de qualquer Pix.
                        """
                    ),
                },
            ],
        },
        {
            "number": 3,
            "name": "Protegendo meus dados",
            "description": (
                "Proteja senhas, códigos e dados pessoais e avalie links e "
                "ofertas antes de informar dados ou pagar."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.3.1",
                    "name": "Proteger senhas, códigos e dados pessoais",
                    "description": (
                        "Não compartilha senhas, códigos de verificação nem "
                        "dados do cartão com ninguém que os solicite."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "6.3.2",
                    "name": "Adotar hábitos de segurança digital",
                    "description": (
                        "Usa senhas longas e diferentes, verificação em duas "
                        "etapas e aplicativos das lojas oficiais."
                    ),
                    "is_essential": False,
                },
                {
                    "code": "6.3.3",
                    "name": "Avaliar links, ofertas e sites suspeitos",
                    "description": (
                        "Observa preço, endereço, informações da empresa e forma "
                        "de pagamento antes de comprar ou informar dados."
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
                            "Uma pessoa que diz ser \"atendente do banco\" pede o "
                            "código de verificação que chegou por SMS para "
                            "\"cancelar uma compra suspeita\". O que fazer?"
                        ),
                        "competency_codes": ["6.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Passar o código, porque ela é do banco.",
                            },
                            {
                                "value": "b",
                                "label": "Passar só metade do código.",
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pedir que ela envie o código por e-mail."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Não passar o código, encerrar a conversa e "
                                    "ligar para o número oficial do banco."
                                ),
                            },
                        ],
                        "correct_answer": "d",
                        "feedback_correct": (
                            "Exato! Nenhum atendente legítimo pede código de "
                            "verificação. Encerrar e ligar pelo número oficial é "
                            "o caminho seguro."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. Códigos de verificação são pessoais e "
                            "nunca devem ser passados a ninguém. O correto é "
                            "encerrar a conversa e entrar em contato pelo número "
                            "oficial do banco."
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
                            "Qual prática protege melhor as suas contas "
                            "importantes?"
                        ),
                        "competency_codes": ["6.3.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Usar a mesma senha em todas as contas, para "
                                    "não esquecer."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Anotar a senha em uma mensagem no celular, "
                                    "para ter à mão."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Usar senhas longas e diferentes e ativar a "
                                    "verificação em duas etapas."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Compartilhar a senha apenas com amigos de "
                                    "confiança."
                                ),
                            },
                        ],
                        "correct_answer": "c",
                        "feedback_correct": (
                            "Correto! Senhas longas e diferentes, junto com a "
                            "verificação em duas etapas, protegem melhor: se uma "
                            "senha vazar, as outras contas continuam seguras."
                        ),
                        "feedback_incorrect": (
                            "Não exatamente. A melhor proteção é combinar senhas "
                            "longas e diferentes em cada conta importante com a "
                            "verificação em duas etapas. Repetir ou compartilhar "
                            "senhas aumenta o risco."
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
                            "Um site desconhecido, aberto por um link recebido "
                            "por mensagem, vende um celular por R$ 400 (o preço "
                            "normal é cerca de R$ 2.000) e aceita só Pix para "
                            "conta de pessoa física. O que fazer?"
                        ),
                        "competency_codes": ["6.3.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Comprar rápido, antes que o estoque acabe."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não comprar: o preço muito abaixo do mercado "
                                    "e o pagamento só por Pix para pessoa física "
                                    "são sinais de golpe."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Fazer um Pix de valor pequeno só para "
                                    "testar."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Comprar e pedir o dinheiro de volta ao banco "
                                    "se der errado."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Muito bem! Preço muito abaixo do mercado, site aberto "
                            "por link recebido por mensagem e pagamento só por Pix "
                            "para pessoa física são sinais clássicos de golpe."
                        ),
                        "feedback_incorrect": (
                            "Revise os sinais. Preço muito abaixo do mercado, link "
                            "recebido por mensagem e pagamento só por Pix para "
                            "pessoa física indicam golpe. O caminho seguro é não "
                            "comprar. A devolução do Pix não é garantida."
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
                            "Liste 3 hábitos que você adotaria para proteger seus "
                            "dados e suas contas financeiras e explique por que "
                            "cada um ajuda."
                        ),
                        "competency_codes": ["6.3.1", "6.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. O Mentor vai analisá-la "
                            "e dar um retorno personalizado."
                        ),
                        "evaluation_criteria": [
                            (
                                "Menciona três hábitos coerentes, como não "
                                "compartilhar senhas e códigos, usar senhas "
                                "diferentes ou ativar verificação em duas etapas."
                            ),
                            (
                                "Apresenta uma justificativa para cada hábito."
                            ),
                            (
                                "Inclui cuidados com senhas ou códigos e hábitos "
                                "mais amplos de segurança digital."
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
                        "prompt": "O que você faz diante da ligação?",
                        "scenario": (
                            "Você recebe um SMS: \"Banco: compra de R$ 1.890 "
                            "detectada no seu cartão. Se não foi você, ligue "
                            "agora para o número abaixo.\" Você liga. Quem atende "
                            "diz ser do \"setor de segurança\", pede os dados do "
                            "seu cartão e o código que acabou de chegar por SMS, "
                            "\"para cancelar a compra\". Depois diz que, para "
                            "proteger seu dinheiro, você precisa transferir o "
                            "saldo por Pix para uma \"conta segura\". O que você "
                            "faz?"
                        ),
                        "competency_codes": ["6.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Passo os dados do cartão e o código para "
                                    "cancelar a compra rapidamente."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Desligo, abro o aplicativo oficial do banco "
                                    "(ou ligo para o número do verso do cartão), "
                                    "verifico se existe a compra e, se não existir, "
                                    "registro a contestação, sem passar dados, "
                                    "código nem fazer Pix."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Faço o Pix para a \"conta segura\" e depois "
                                    "falo com o banco."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Respondo o SMS pedindo mais informações sobre "
                                    "a compra."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Excelente! Você percebeu os sinais: telefone vindo de "
                            "uma mensagem, pedido de dados e de código, e a "
                            "transferência para uma \"conta segura\". Verificar "
                            "por um canal oficial que você mesmo abre é o que "
                            "protege você."
                        ),
                        "feedback_incorrect": (
                            "Revise a sequência. O banco nunca pede dados do "
                            "cartão, códigos de verificação nem transferência para "
                            "uma \"conta segura\". O caminho seguro é encerrar a "
                            "ligação e verificar a compra no aplicativo oficial ou "
                            "pelo número do verso do cartão."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Seus dados são a chave do seu dinheiro",
                    "order": 1,
                    "body": md(
                        """
                        Senhas, códigos de verificação e dados do cartão são
                        **pessoais**: não compartilhe com ninguém, nem com alguém
                        que diga ser "atendente" ou "do suporte".

                        Hábitos que protegem:

                        - Use **senhas longas e diferentes** para contas
                          importantes, como e-mail e banco. Um gerenciador de
                          senhas ajuda.
                        - Ative a **verificação em duas etapas** (código extra
                          além da senha) em todas as contas que permitirem.
                        - Mantenha o **celular e os aplicativos atualizados** e
                          instale apps só das **lojas oficiais**.
                        - Evite fazer operações financeiras em **Wi-Fi público**.

                        Antes de comprar em um site ou aceitar uma oferta,
                        observe:

                        - **Preço muito abaixo do mercado.**
                        - **Endereço do site** com letras trocadas ou estranhas.
                        - **Falta de informações da empresa**, como CNPJ e canais
                          de contato.
                        - **Pagamento só por Pix, para conta de pessoa física.**
                        - **Link recebido por mensagem**, em vez de um site que
                          você mesmo procurou.
                        """
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O celular de R$ 400",
                    "order": 2,
                    "body": md(
                        """
                        Um site desconhecido, aberto por um link recebido por
                        mensagem, vende um celular por R$ 400, quando o preço
                        normal é cerca de R$ 2.000. O site aceita só Pix, para uma
                        conta de pessoa física, e não mostra CNPJ nem canais de
                        contato.

                        Sinais de alerta: preço muito abaixo do mercado, link
                        recebido por mensagem, pagamento só por Pix para pessoa
                        física e falta de informações da empresa. O caminho seguro
                        é **não comprar**.
                        """
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Algo deu errado? Aja rápido",
                    "order": 3,
                    "body": md(
                        """
                        Se você acha que passou dados para um golpista: troque as
                        senhas, avise o banco, bloqueie os cartões envolvidos e
                        registre um boletim de ocorrência. Quanto mais rápido,
                        menor o estrago.
                        """
                    ),
                },
            ],
        },
        {
            "number": 4,
            "name": "Desafio integrador",
            "description": (
                "Combine orçamento, crédito, imprevisto e segurança digital em "
                "quatro decisões da mesma história."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "6.4.1",
                    "name": "Integrar as competências da jornada",
                    "description": (
                        "Toma decisões coerentes de orçamento, crédito, "
                        "imprevisto e segurança digital em uma situação que "
                        "combina as seis fases."
                    ),
                    "is_essential": True,
                },
            ],
            "activities": [
                {
                    "order": 1,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual plano fecha a conta da Lara?",
                        "scenario": (
                            "A Lara recebe R$ 2.000 líquidos por mês. As despesas "
                            "essenciais somam R$ 1.200. Ela tem uma fatura de "
                            "cartão de R$ 200, de compras já feitas, que vence "
                            "este mês. Ela também paga um curso de R$ 150 por mês e "
                            "quer separar R$ 100 para a reserva de emergência. O "
                            "que sobra é para o lazer. Qual plano fecha a conta sem "
                            "passar da renda e sem gerar dívida?"
                        ),
                        "competency_codes": ["6.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Paga as essenciais e só o mínimo da fatura "
                                    "(R$ 40), para ter mais dinheiro para o lazer."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Paga as essenciais e o lazer (R$ 800) e "
                                    "deixa a fatura e a reserva para quando "
                                    "sobrar."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Paga as essenciais (R$ 1.200), a fatura "
                                    "inteira (R$ 200), o curso (R$ 150), separa "
                                    "R$ 100 para a reserva e usa R$ 350 para o "
                                    "lazer."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Corta o curso e a reserva para ter R$ 600 de "
                                    "lazer."
                                ),
                            },
                        ],
                        "correct_choice": "c",
                        "feedback_correct": (
                            "Ótimo plano! 1.200 + 200 + 150 + 100 + 350 = "
                            "R$ 2.000. A Lara pagou o essencial, quitou a fatura "
                            "inteira (sem juros), manteve o curso, começou a "
                            "reserva e ainda tem lazer."
                        ),
                        "feedback_incorrect": (
                            "Revise o plano. Pagar só o mínimo da fatura gera "
                            "juros, deixar a fatura e a reserva \"para quando "
                            "sobrar\" quase nunca funciona, e cortar o curso e a "
                            "reserva compromete o futuro. O plano que fecha é: "
                            "1.200 + 200 + 150 + 100 + 350 = R$ 2.000."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Qual proposta a Lara escolhe?",
                        "scenario": (
                            "A Lara precisa de um notebook para o curso, que custa "
                            "R$ 2.400 à vista, valor que ela não tem. Depois do "
                            "orçamento do mês, ela pode destinar até R$ 300 por mês "
                            "ao notebook, saindo do lazer, sem tocar nas despesas "
                            "essenciais, no curso nem na reserva. Três propostas "
                            "fictícias. Proposta X: 12 parcelas de R$ 250. "
                            "Proposta Y: 6 parcelas de R$ 480. Proposta Z: 24 "
                            "parcelas de R$ 150. Qual proposta ela escolhe?"
                        ),
                        "competency_codes": ["6.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Proposta Y, porque tem o menor valor total "
                                    "(R$ 2.880)."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Proposta X: o total (R$ 3.000) é o menor "
                                    "entre as que cabem nos R$ 300 por mês."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Proposta Z, porque tem a menor parcela "
                                    "(R$ 150)."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Nenhuma; usa o rotativo do cartão para pagar "
                                    "à vista."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Boa decisão! Os totais são: X = R$ 3.000, Y = "
                            "R$ 2.880 e Z = R$ 3.600. A proposta Y é a mais "
                            "barata, mas a parcela de R$ 480 passa dos R$ 300 que "
                            "a Lara pode pagar. Entre as que cabem (X e Z), a X "
                            "custa menos no total."
                        ),
                        "feedback_incorrect": (
                            "Revise a comparação. Calcule o total de cada proposta "
                            "(X: 12 × 250 = R$ 3.000; Y: 6 × 480 = R$ 2.880; Z: "
                            "24 × 150 = R$ 3.600) e verifique se a parcela cabe "
                            "nos R$ 300. A Y não cabe; entre X e Z, a X custa "
                            "menos. O rotativo do cartão costuma ser uma das "
                            "dívidas mais caras."
                        ),
                    },
                },
                {
                    "order": 3,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que a Lara faz com o celular quebrado?",
                        "scenario": (
                            "Um mês depois, o celular da Lara quebra, e ela precisa "
                            "dele para trabalhar. O conserto custa R$ 450. Ela tem "
                            "R$ 400 de reserva de emergência e ainda tem R$ 50 do "
                            "lazer do mês, depois de pagar a parcela do notebook. O "
                            "que ela faz?"
                        ),
                        "competency_codes": ["6.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Usa a reserva (R$ 400), completa os R$ 50 "
                                    "com o lazer do mês, mantém as parcelas do "
                                    "notebook e volta a repor a reserva nos meses "
                                    "seguintes."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Pega um empréstimo com uma financeira que "
                                    "libera o dinheiro na hora, com juros altos."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Deixa de pagar uma conta essencial neste mês "
                                    "para pagar o conserto."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Parcela o conserto no rotativo do cartão e "
                                    "deixa a reserva intocada."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Boa decisão! Era para isso que a reserva existia. A "
                            "Lara cobriu o imprevisto (400 + 50 = R$ 450), "
                            "manteve as parcelas e vai repor a reserva, sem entrar "
                            "em dívida."
                        ),
                        "feedback_incorrect": (
                            "Revise a escolha. O conserto é um imprevisto, e a "
                            "reserva existe para ele. Pegar empréstimo com juros "
                            "altos, deixar uma conta essencial de lado ou usar o "
                            "rotativo cria dívida ou problemas maiores do que o "
                            "próprio conserto."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "simulation",
                    "points_value": 20,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Como a Lara reage à mensagem?",
                        "scenario": (
                            "Na mesma semana, a Lara recebe uma mensagem de um "
                            "número desconhecido: \"Seu reembolso de R$ 900 está "
                            "liberado! Para receber, pague a taxa de R$ 90 por Pix "
                            "neste link em até 30 minutos.\" Ela não esperava "
                            "nenhum reembolso. O que ela faz?"
                        ),
                        "competency_codes": ["6.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Paga logo, porque R$ 90 por R$ 900 "
                                    "compensa."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Responde à mensagem pedindo mais detalhes "
                                    "sobre o reembolso."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Clica no link só para ver a página, sem "
                                    "pagar nada."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Ignora a mensagem e o link, não paga nada, e "
                                    "se quiser conferir procura o assunto pelos "
                                    "canais oficiais, que ela mesma abre."
                                ),
                            },
                        ],
                        "correct_choice": "d",
                        "feedback_correct": (
                            "Excelente! A mensagem tem vários sinais de golpe: "
                            "número desconhecido, reembolso que ela não esperava, "
                            "taxa para receber, link e pressa de 30 minutos. "
                            "Ignorar e conferir por canais oficiais é o caminho "
                            "seguro."
                        ),
                        "feedback_incorrect": (
                            "Revise os sinais. Um reembolso inesperado que exige "
                            "taxa por Pix, em um link recebido de número "
                            "desconhecido, com prazo curto, é um golpe clássico. "
                            "Pagar, responder ou clicar no link coloca você em "
                            "risco. O caminho seguro é ignorar e, se tiver "
                            "dúvida, conferir por canais oficiais."
                        ),
                    },
                },
            ],
            "content_items": [],
        },
    ],
}
