"""Conteúdo versionado da Trilha 11 — Golpes e proteção de dados.

phase_number: 11 (novo registro, inserido pela migration 0015)
Fonte editorial: docs/trilhas/trilha-11.md

Os nomes, mensagens e situações são fictícios. O MED tem critérios e
limitações específicos — não prometer devolução garantida de valores.
"""

TRAIL_11_V1 = {
    "phase_number": 11,
    "missions": [
        # ──────────────────────────────────────────────────────────────────
        # Missão 11.1 — Tipos de golpe
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 1,
            "name": "Tipos de golpe",
            "description": (
                "Reconheça os principais tipos de golpe financeiro digital: "
                "phishing, engenharia social, falsa central e falso parente."
            ),
            "order": 1,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "11.1.1",
                    "name": "Reconhecer sinais de phishing",
                    "description": (
                        "Identifica urgência, ameaça, pedido de dados, links "
                        "suspeitos e outros sinais em mensagens, e-mails e ligações."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.1.2",
                    "name": "Identificar golpes de engenharia social",
                    "description": (
                        "Reconhece técnicas de manipulação emocional como falsa "
                        "central de atendimento e falso parente."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.1.3",
                    "name": "Aplicar protocolo de verificação por canal oficial",
                    "description": (
                        "Sabe que não deve clicar no link, responder nem compartilhar "
                        "dados sem verificar por canal oficial independente."
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
                            "Qual das mensagens abaixo tem mais sinais de phishing?"
                        ),
                        "competency_codes": ["11.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": '"Seu extrato de outubro está disponível no aplicativo."',
                            },
                            {
                                "value": "b",
                                "label": (
                                    '"Sua conta será bloqueada em 1 hora. '
                                    'Clique aqui para atualizar seus dados."'
                                ),
                            },
                            {
                                "value": "c",
                                "label": '"Seu pedido foi entregue. Avalie no aplicativo da loja."',
                            },
                            {
                                "value": "d",
                                "label": '"Sua fatura vence em 3 dias. Consulte no aplicativo."',
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A mensagem 'b' tem urgência artificial ('1 hora'), "
                            "ameaça ('bloqueio') e pedido de ação imediata ('clique aqui "
                            "para atualizar dados'). São os três sinais mais comuns "
                            "de phishing. Nunca clique no link — verifique pelo app oficial."
                        ),
                        "feedback_incorrect": (
                            "A mensagem 'b' combina três sinais clássicos de phishing: "
                            "urgência ('1 hora'), ameaça ('será bloqueada') e solicitação "
                            "de dados por link externo. As outras mensagens são normais: "
                            "não pedem dados e direcionam para o aplicativo oficial."
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
                            "Você recebe uma ligação de 'alguém do banco' dizendo que "
                            "detectou uma fraude na sua conta e pedindo sua senha "
                            "para cancelar. O que fazer?"
                        ),
                        "competency_codes": ["11.1.2"],
                        "options": [
                            {"value": "a", "label": "Fornecer a senha para cancelar a fraude rapidamente."},
                            {
                                "value": "b",
                                "label": (
                                    "Desligar e ligar para o banco pelo número do cartão "
                                    "ou do aplicativo oficial para confirmar."
                                ),
                            },
                            {"value": "c", "label": "Transferir o dinheiro para uma 'conta segura' indicada."},
                            {"value": "d", "label": "Seguir as instruções se o número parecer legítimo."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Bancos jamais pedem senhas por telefone. "
                            "Desligue e ligue pelo número oficial do cartão ou do "
                            "aplicativo. Esse é o golpe da falsa central — um dos "
                            "mais comuns e eficazes porque usa o nome real do banco."
                        ),
                        "feedback_incorrect": (
                            "Nunca forneça senha ou transfira dinheiro por solicitação "
                            "telefônica. Bancos não pedem senhas por telefone. "
                            "O número exibido pode ser clonado (spoofing). "
                            "A ação correta é desligar e ligar pelo canal oficial."
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
                            "O que é a 'regra dos 3 não' ao receber mensagem suspeita?"
                        ),
                        "competency_codes": ["11.1.3"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Não clique no link. Não responda com dados. "
                                    "Não faça transferência antes de verificar pelo canal oficial."
                                ),
                            },
                            {"value": "b", "label": "Não leia, não responda, não delete."},
                            {"value": "c", "label": "Não ligue, não transfira, não denuncie."},
                            {"value": "d", "label": "Não ignore — sempre responda para confirmar a identidade."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Ao receber qualquer mensagem suspeita:\n"
                            "1. Não clique no link\n"
                            "2. Não responda com dados pessoais ou financeiros\n"
                            "3. Não transfira dinheiro antes de verificar pelo canal oficial\n\n"
                            "Sempre confirme por um canal que você mesmo iniciou."
                        ),
                        "feedback_incorrect": (
                            "Os 3 'não' corretos: não clique no link da mensagem, "
                            "não responda com dados, não transfira dinheiro. "
                            "Após esses 'não', verifique pelo canal oficial."
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
                            "Qual característica distingue o spear phishing do "
                            "phishing genérico?"
                        ),
                        "competency_codes": ["11.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "O spear phishing é personalizado com dados reais "
                                    "da vítima (nome, empresa, transação recente), "
                                    "tornando-o mais convincente."
                                ),
                            },
                            {"value": "b", "label": "O spear phishing é enviado por SMS, não por e-mail."},
                            {"value": "c", "label": "O phishing genérico é mais difícil de identificar."},
                            {"value": "d", "label": "São a mesma coisa com nomes diferentes."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O spear phishing usa informações reais da vítima "
                            "(obtidas em redes sociais ou vazamentos de dados) para "
                            "criar mensagens mais convincentes e difíceis de identificar."
                        ),
                        "feedback_incorrect": (
                            "O spear phishing é personalizado: usa nome real, empresa, "
                            "cargo ou transação recente para parecer mais legítimo. "
                            "O phishing genérico é o mesmo e-mail enviado para milhões "
                            "de pessoas — menos personalizado, mais fácil de identificar."
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
                            "Uma mensagem diz: 'Responda agora ou perde tudo'. "
                            "Qual é o principal sinal de golpe?"
                        ),
                        "competency_codes": ["11.1.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Urgência artificial — criar pressa é a técnica central "
                                    "para impedir que a vítima pense antes de agir."
                                ),
                            },
                            {"value": "b", "label": "O tamanho da mensagem."},
                            {"value": "c", "label": "O horário do envio."},
                            {"value": "d", "label": "O canal utilizado (SMS, e-mail ou WhatsApp)."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Urgência artificial é o mecanismo central dos golpes: "
                            "o atacante quer que você aja sem pensar. Comunicações legítimas "
                            "de bancos não usam esse tipo de linguagem para decisões "
                            "que envolvem dados ou dinheiro."
                        ),
                        "feedback_incorrect": (
                            "A urgência artificial ('agora', 'perde tudo', 'última chance') "
                            "é o sinal mais importante. Ela visa eliminar o tempo que "
                            "a vítima usaria para verificar a informação. Desconfie sempre "
                            "de mensagens que criam pressão de tempo."
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
                            "Você recebe uma mensagem de texto dizendo: 'Sua conta foi "
                            "bloqueada por atividade suspeita. Clique em [link] para "
                            "desbloquear em até 2 horas ou perca o acesso permanentemente.'\n\n"
                            "Descreva passo a passo o que você faria."
                        ),
                        "competency_codes": ["11.1.2", "11.1.3"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Passos esperados: (1) não clicar no link; "
                            "(2) não responder à mensagem; "
                            "(3) ligar para o banco pelo número do verso do cartão "
                            "ou acessar o aplicativo diretamente; "
                            "(4) verificar se a conta realmente está bloqueada; "
                            "(5) se for golpe, deletar a mensagem e relatar ao banco."
                        ),
                        "evaluation_criteria": [
                            "Não clicar no link da mensagem.",
                            "Verificar pelo canal oficial (app ou telefone do cartão).",
                            "Não fornecer dados pessoais ou financeiros.",
                        ],
                        "max_length": 2000,
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que é phishing e como funciona",
                    "order": 1,
                    "body": (
                        "**Phishing** é uma tentativa de obter dados pessoais, "
                        "senhas ou dinheiro se passando por uma entidade legítima "
                        "(banco, governo, loja).\n\n"
                        "**Canais mais comuns:**\n"
                        "- E-mail (phishing clássico)\n"
                        "- SMS (smishing)\n"
                        "- Ligação (vishing)\n"
                        "- WhatsApp e redes sociais\n\n"
                        "**Sinais de alerta:**\n"
                        "- Urgência: 'sua conta será bloqueada em X horas'\n"
                        "- Ameaça: 'você perderá tudo se não agir agora'\n"
                        "- Pedido de dados: senha, token, número de cartão\n"
                        "- Link suspeito: URL diferente do site oficial\n"
                        "- Erros de ortografia ou formatação diferente do normal"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Engenharia social: manipulação emocional",
                    "order": 2,
                    "body": (
                        "**Engenharia social** é a manipulação psicológica para obter "
                        "informações ou ações da vítima. Não explora falhas técnicas — "
                        "explora comportamento humano.\n\n"
                        "**Golpe da falsa central:**\n"
                        "Ligação de 'funcionário do banco' informando fraude e pedindo "
                        "confirmação de dados ou transferência para conta segura. "
                        "O número exibido pode ser clonado.\n\n"
                        "**Golpe do falso parente:**\n"
                        "Mensagem de 'filho(a)/parente' com número novo pedindo "
                        "dinheiro urgente. Usa o gatilho emocional do cuidado familiar.\n\n"
                        "**Proteção:** verifique sempre por um contato independente "
                        "(ligue para o número que você já tem; não use o número da mensagem)."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O golpe da falsa central (fictício)",
                    "order": 3,
                    "body": (
                        "**Situação fictícia:**\n\n"
                        "Carlos recebe uma ligação. O número exibido parece ser do banco.\n\n"
                        "Atendente: 'Carlos, identificamos uma compra suspeita de R$ 3.200 "
                        "em seu nome. Para cancelar, preciso confirmar sua senha para "
                        "autenticar a operação.'\n\n"
                        "**O que o Carlos deveria fazer:**\n"
                        "1. Desligar o telefone\n"
                        "2. Ligar para o banco pelo número do verso do cartão\n"
                        "3. Verificar se há de fato uma compra suspeita\n"
                        "4. Nunca fornecer senha por telefone\n\n"
                        "*(Nome e situação fictícios. Bancos nunca pedem senha por telefone.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Como verificar pelo canal oficial",
                    "order": 4,
                    "body": (
                        "**Regra dos 3 'não':**\n\n"
                        "1. **Não clique** no link da mensagem suspeita\n"
                        "2. **Não responda** com dados pessoais ou financeiros\n"
                        "3. **Não transfira** dinheiro sem verificar\n\n"
                        "**Após os 3 'não':**\n"
                        "- Abra o aplicativo do banco diretamente (sem seguir link)\n"
                        "- Ligue para o número que está no verso do cartão\n"
                        "- Use o número de contato que você já tem, não o da mensagem\n\n"
                        "Se o banco realmente precisar de você, ele pode ser contactado "
                        "por esses canais. Se não puder ser confirmado por canal oficial, "
                        "é golpe."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Smishing, vishing e spear phishing",
                    "order": 5,
                    "body": (
                        "| Tipo | Canal | Característica |\n"
                        "|---|---|---|\n"
                        "| Phishing | E-mail | Mensagem genérica para muitas pessoas |\n"
                        "| Smishing | SMS | Mesmo mecanismo via SMS |\n"
                        "| Vishing | Ligação | Golpe por voz, geralmente falsa central |\n"
                        "| Spear phishing | Qualquer | Personalizado com dados reais da vítima |\n\n"
                        "O spear phishing é o mais perigoso porque usa informações reais "
                        "(nome, empresa, transação recente) obtidas em redes sociais "
                        "ou vazamentos de dados — tornando a mensagem muito mais convincente."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "E-mail de phishing: análise linha a linha (fictício)",
                    "order": 6,
                    "body": (
                        "**E-mail fictício analisado:**\n\n"
                        "'De: seguranca@banco-seguro-br.com ← domínio diferente do banco real'\n"
                        "'Assunto: URGENTE — Confirme sua identidade em 2 horas'\n\n"
                        "'Prezado cliente, ← sem nome'\n"
                        "'Detectamos atividade suspeita. ← urgência'\n"
                        "'Clique AQUI para confirmar seus dados ← link não oficial'\n"
                        "'ou sua conta será suspensa. ← ameaça'\n\n"
                        "**Sinais identificados:**\n"
                        "- Domínio diferente do banco real\n"
                        "- Urgência artificial\n"
                        "- Ameaça de perda\n"
                        "- Link externo\n"
                        "- Ausência do nome do cliente\n\n"
                        "*(Fictício, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Urgência e medo: os gatilhos dos golpistas",
                    "order": 7,
                    "body": (
                        "Golpistas criam urgência e medo para eliminar o tempo de "
                        "verificação. Quanto menos você pensa, mais você age por impulso.\n\n"
                        "**A regra mais simples:** se a mensagem cria urgência ou medo, "
                        "pare. Respire. Verifique por canal oficial antes de qualquer ação.\n\n"
                        "Uma mensagem legítima do banco pode esperar a sua verificação. "
                        "Uma fraude não pode — por isso cria pressão."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Informações que NUNCA devem ser compartilhadas",
                    "order": 8,
                    "body": (
                        "Independentemente de quem pede ou qual o pretexto:\n\n"
                        "- **Senha do banco** (acesso ao app ou internet banking)\n"
                        "- **Token de autenticação** (código enviado por SMS ou gerado no app)\n"
                        "- **CVV do cartão** (3 dígitos no verso)\n"
                        "- **Código de desbloqueio do celular**\n"
                        "- **Senha do cartão** (4 a 6 dígitos)\n\n"
                        "Bancos, operadoras e instituições legítimas **nunca pedem** "
                        "essas informações por telefone, SMS, e-mail ou WhatsApp."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 11.2 — Golpes com Pix
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 2,
            "name": "Golpes com Pix",
            "description": (
                "Reconheça golpes específicos com Pix: comprovante falso, "
                "QR Code adulterado e contas laranja."
            ),
            "order": 2,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "11.2.1",
                    "name": "Reconhecer golpes específicos com Pix",
                    "description": (
                        "Identifica comprovante falso de Pix, QR Code adulterado "
                        "e como verificar o recebimento no aplicativo."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.2.2",
                    "name": "Identificar características de contas laranja",
                    "description": (
                        "Explica o que são contas laranja, os riscos para quem "
                        "aceita receber e repassar valores."
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
                            "Um comprovante de Pix chegou pelo WhatsApp antes de "
                            "você entregar o produto. Você deve confiar nele?"
                        ),
                        "competency_codes": ["11.2.1"],
                        "options": [
                            {"value": "a", "label": "Sim — comprovante do WhatsApp é oficial."},
                            {
                                "value": "b",
                                "label": (
                                    "Não — comprovante pode ser editado. Verifique o "
                                    "recebimento no seu aplicativo bancário."
                                ),
                            },
                            {"value": "c", "label": "Sim — se o valor e a data estiverem corretos."},
                            {"value": "d", "label": "Depende do banco do comprador."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Comprovantes de Pix podem ser editados com "
                            "aplicativos simples. A única confirmação confiável é "
                            "ver o crédito no extrato do seu aplicativo bancário. "
                            "Nunca entregue produtos ou serviços antes de confirmar."
                        ),
                        "feedback_incorrect": (
                            "Comprovantes enviados por WhatsApp podem ser falsificados. "
                            "A confirmação real é ver o valor creditado no seu extrato. "
                            "Abra o aplicativo do banco e verifique antes de qualquer ação."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é uma conta laranja?",
                        "competency_codes": ["11.2.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Uma conta bancária de alta rentabilidade.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Uma conta usada por terceiros para receber e "
                                    "repassar valores de origem ilícita, "
                                    "expondo o titular a responsabilidade criminal."
                                ),
                            },
                            {"value": "c", "label": "Uma conta poupança de banco digital."},
                            {"value": "d", "label": "Um tipo de conta conjunta."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Conta laranja é usada para 'lavar' dinheiro de golpes. "
                            "O titular da conta pode ser responsabilizado criminalmente, "
                            "mesmo que não saiba da origem dos valores — o que é difícil "
                            "de provar depois."
                        ),
                        "feedback_incorrect": (
                            "Conta laranja é aquela cujo titular cede o acesso ou "
                            "aceita receber valores para repassar para terceiros. "
                            "Isso caracteriza participação em lavagem de dinheiro, "
                            "com risco de responsabilidade criminal."
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
                            "Pedro foi solicitado via WhatsApp para receber R$ 1.000 "
                            "e repassar R$ 900 para outra conta, ficando com R$ 100 "
                            "por isso. O que ele deve fazer?"
                        ),
                        "competency_codes": ["11.2.2"],
                        "options": [
                            {"value": "a", "label": "Aceitar — ganhar R$ 100 por nada parece bom."},
                            {
                                "value": "b",
                                "label": (
                                    "Recusar — essa é a forma clássica de recrutar "
                                    "contas laranja. Pedro pode ser responsabilizado."
                                ),
                            },
                            {"value": "c", "label": "Aceitar se conhecer quem está pedindo."},
                            {"value": "d", "label": "Perguntar a origem do dinheiro primeiro."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Receber e repassar dinheiro de pessoas desconhecidas "
                            "é o funcionamento típico de conta laranja. Pedro pode ser "
                            "investigado e responsabilizado criminalmente — "
                            "mesmo não sendo o autor do golpe original."
                        ),
                        "feedback_incorrect": (
                            "Receber dinheiro para repassar configura participação em "
                            "esquema de lavagem. Mesmo sem saber a origem, Pedro "
                            "pode responder criminalmente. A resposta correta é sempre "
                            "recusar e denunciar ao banco se necessário."
                        ),
                    },
                },
                {
                    "order": 4,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "Como verificar se um Pix foi realmente recebido?",
                        "competency_codes": ["11.2.1"],
                        "options": [
                            {"value": "a", "label": "Pelo comprovante enviado pelo WhatsApp."},
                            {"value": "b", "label": "Pelo extrato no aplicativo bancário oficial."},
                            {"value": "c", "label": "Pelo comprovante impresso apresentado pelo pagador."},
                            {"value": "d", "label": "Perguntando ao gerente."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! A única forma confiável de confirmar o recebimento "
                            "de um Pix é verificar o extrato no seu próprio aplicativo "
                            "bancário oficial. Comprovantes externos podem ser falsificados."
                        ),
                        "feedback_incorrect": (
                            "Só o extrato no seu aplicativo bancário comprova o recebimento. "
                            "Comprovantes enviados por WhatsApp, impressos ou por e-mail "
                            "podem ser falsificados."
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
                            "Você está vendendo um produto por R$ 400 online. O comprador "
                            "envia um comprovante de Pix pelo WhatsApp e pede para você "
                            "enviar o produto imediatamente.\n\n"
                            "Descreva como você identificaria se o comprovante é "
                            "legítimo e o que você faria antes de enviar o produto."
                        ),
                        "competency_codes": ["11.2.1"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Passos corretos: (1) não confiar no comprovante do WhatsApp; "
                            "(2) abrir o aplicativo do banco; "
                            "(3) verificar o extrato para confirmar o crédito; "
                            "(4) só enviar o produto após ver R$ 400 creditados; "
                            "(5) se não aparecer, avisar o comprador e aguardar."
                        ),
                        "evaluation_criteria": [
                            "Não confia no comprovante enviado externamente.",
                            "Verifica o extrato no aplicativo bancário oficial.",
                            "Aguarda a confirmação do crédito antes de agir.",
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
                            "Você está vendendo um produto online. O comprador manda um "
                            "comprovante de Pix de R$ 300 pelo WhatsApp. O que você faz?"
                        ),
                        "competency_codes": ["11.2.1"],
                        "scenario": (
                            "Venda online de produto por R$ 300. Comprador manda "
                            "comprovante via WhatsApp e pede entrega imediata. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Conferir o extrato do banco para ver se R$ 300 "
                                    "foram creditados. Só então combinar a entrega."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Aceitar o comprovante do WhatsApp como confirmação "
                                    "e entregar o produto imediatamente."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pedir um segundo comprovante por e-mail "
                                    "para confirmar."
                                ),
                            },
                        ],
                        "correct_choice": "a",
                        "feedback_correct": (
                            "Decisão correta! Verificar no extrato bancário é a única "
                            "confirmação segura. Comprovantes de WhatsApp ou e-mail "
                            "podem ser falsificados com facilidade."
                        ),
                        "feedback_incorrect": (
                            "Apenas o extrato no seu aplicativo bancário confirma o "
                            "recebimento. Um segundo comprovante externo pode ser "
                            "igualmente falsificado. Espere sempre o crédito aparecer "
                            "no seu extrato antes de entregar."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Comprovante falso de Pix: como funciona e como detectar",
                    "order": 1,
                    "body": (
                        "O comprovante falso é um dos golpes mais simples e eficazes "
                        "com Pix. O golpista:\n\n"
                        "1. Edita um comprovante real com valores e dados alterados\n"
                        "2. Envia para o vendedor antes de fazer qualquer transferência\n"
                        "3. Pressiona por entrega imediata\n\n"
                        "**Como se proteger:**\n"
                        "Nunca entregue produto ou serviço antes de ver o crédito "
                        "no seu próprio extrato. Comprovantes externos não têm "
                        "valor probatório antes da confirmação no banco."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "QR Code adulterado: cuidado com impressões e adesivos",
                    "order": 2,
                    "body": (
                        "Em locais físicos, golpistas trocam QR Codes legítimos "
                        "por QR Codes falsos que redirecionam para outra conta:\n\n"
                        "- Colocam adesivos com QR Code falso sobre o original\n"
                        "- Trocam o material impresso com o QR Code\n\n"
                        "**Como se proteger:**\n"
                        "- Sempre confirme o nome do destinatário na tela antes de confirmar\n"
                        "- Se o nome não for o esperado, cancele e verifique\n"
                        "- Desconfie de QR Codes impressos em papel com aparência improvisada"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Contas laranja: o risco para quem aceita participar",
                    "order": 3,
                    "body": (
                        "**Conta laranja** é uma conta bancária usada para receber "
                        "e movimentar dinheiro de origem ilícita — geralmente proveniente "
                        "de golpes.\n\n"
                        "**Como você pode ser abordado:**\n"
                        "- Oferta de 'trabalho' para receber e repassar dinheiro\n"
                        "- Pedido de empréstimo da conta com promessa de comissão\n"
                        "- Colega ou 'amigo' pedindo que você receba por ele\n\n"
                        "**Consequências para o titular:**\n"
                        "- Investigação por lavagem de dinheiro\n"
                        "- Bloqueio da conta\n"
                        "- Responsabilidade criminal, mesmo sem conhecer a origem\n\n"
                        "Recuse sempre. Denuncie ao banco se for abordado."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Sempre confira o destinatário antes de confirmar",
                    "order": 4,
                    "body": (
                        "Antes de confirmar qualquer Pix:\n\n"
                        "1. Verifique o **nome completo** do destinatário na tela\n"
                        "2. Confirme o **valor** antes de clicar\n"
                        "3. Verifique se a **instituição** é a esperada\n"
                        "4. Só então confirme\n\n"
                        "Esses 10 segundos de conferência evitam a maioria dos "
                        "erros e golpes com QR Code adulterado."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O golpe do QR Code na loja (fictício)",
                    "order": 5,
                    "body": (
                        "**Situação fictícia:**\n\n"
                        "Camila vai ao estabelecimento 'Loja Fictícia' pagar R$ 50. "
                        "O balconista mostra um cartaz com QR Code. Ela escaneia, "
                        "confirma sem ler o destinatário e paga.\n\n"
                        "Na semana seguinte, ela descobre que o QR Code era um "
                        "adesivo colocado sobre o original — o dinheiro foi para "
                        "uma conta desconhecida.\n\n"
                        "**O erro:** não verificar o nome do destinatário antes de confirmar.\n\n"
                        "*(Situação fictícia, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Como confirmar que o Pix chegou (para quem vende)",
                    "order": 6,
                    "body": (
                        "Se você recebe Pix como vendedor:\n\n"
                        "1. **Abra seu aplicativo bancário** — não dependa do "
                        "comprovante externo\n"
                        "2. **Vá ao extrato** e procure o crédito no valor esperado\n"
                        "3. **Confirme o horário** — Pix é instantâneo (segundos)\n"
                        "4. **Só então confirme** a entrega ou o serviço\n\n"
                        "Se o crédito não aparecer em até 1–2 minutos, "
                        "o pagamento provavelmente não foi feito."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 11.3 — Proteção de dados
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 3,
            "name": "Proteção de dados",
            "description": (
                "Proteja seus dados pessoais e financeiros com senhas fortes, "
                "autenticação e cuidados nas redes sociais."
            ),
            "order": 3,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "11.3.1",
                    "name": "Aplicar práticas de proteção de dados",
                    "description": (
                        "Usa senhas fortes, autenticação em dois fatores e "
                        "evita compartilhar dados sensíveis."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.3.2",
                    "name": "Reconhecer exposição inadequada em redes sociais",
                    "description": (
                        "Identifica quais informações em redes sociais podem "
                        "facilitar golpes personalizados."
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
                            "Qual informação jamais deve ser compartilhada, nem com "
                            "funcionário do banco?"
                        ),
                        "competency_codes": ["11.3.1"],
                        "options": [
                            {"value": "a", "label": "Nome completo."},
                            {"value": "b", "label": "Senha do aplicativo bancário."},
                            {"value": "c", "label": "Número da agência."},
                            {"value": "d", "label": "CPF."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Senha é sempre pessoal e intransferível. "
                            "Funcionários do banco não pedem e não precisam da sua senha "
                            "para realizar operações. Se alguém pedir, é golpe."
                        ),
                        "feedback_incorrect": (
                            "A senha é o único item da lista que jamais deve ser "
                            "compartilhado. CPF, nome e agência são dados de identificação "
                            "que a instituição já tem. Senha é pessoal e intransferível."
                        ),
                    },
                },
                {
                    "order": 2,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": "O que é autenticação em dois fatores (2FA)?",
                        "competency_codes": ["11.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Uma segunda camada de segurança além da senha: "
                                    "código enviado por SMS, e-mail ou gerado por app "
                                    "para confirmar o acesso."
                                ),
                            },
                            {"value": "b", "label": "Usar duas senhas diferentes no mesmo acesso."},
                            {"value": "c", "label": "Confirmar o CPF e a senha em sequência."},
                            {"value": "d", "label": "Usar biometria e PIN ao mesmo tempo."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O 2FA adiciona uma segunda camada: mesmo que sua "
                            "senha seja descoberta, o atacante ainda precisaria do "
                            "segundo fator (código SMS, app autenticador ou e-mail) "
                            "para acessar a conta."
                        ),
                        "feedback_incorrect": (
                            "2FA é uma segunda camada de verificação além da senha. "
                            "Geralmente é um código temporário enviado por SMS, e-mail "
                            "ou gerado por um app autenticador. Torna o acesso muito "
                            "mais difícil para quem roubou apenas a senha."
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
                            "Uma senha de 8 caracteres com maiúsculas, minúsculas, "
                            "números e símbolos é mais segura do que uma com "
                            "12 letras minúsculas simples?"
                        ),
                        "competency_codes": ["11.3.1"],
                        "options": [
                            {"value": "a", "label": "Sim — variedade de caracteres é o mais importante."},
                            {
                                "value": "b",
                                "label": (
                                    "Depende: comprimento maior geralmente gera mais combinações. "
                                    "O ideal é combinar comprimento e variedade."
                                ),
                            },
                            {"value": "c", "label": "Não — comprimento sempre supera a variedade."},
                            {"value": "d", "label": "Ambas têm o mesmo nível de segurança."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Comprimento e variedade ambos importam. "
                            "Uma senha longa com variedade de caracteres é mais "
                            "resistente a ataques de força bruta. Use pelo menos "
                            "12 caracteres com maiúsculas, minúsculas, números e símbolos."
                        ),
                        "feedback_incorrect": (
                            "O ideal é combinar comprimento e variedade. "
                            "Uma frase longa (12+ caracteres) com variações é "
                            "geralmente mais forte do que uma curta com muitos tipos. "
                            "Evite palavras comuns, datas de nascimento e sequências."
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
                            "Liste 3 informações pessoais que você não deve publicar "
                            "em redes sociais e explique como cada uma pode ser "
                            "usada em golpes personalizados."
                        ),
                        "competency_codes": ["11.3.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Exemplos esperados: "
                            "(1) Data de nascimento — usada para confirmar identidade ou "
                            "criar mensagens personalizadas; "
                            "(2) Cidade e endereço — localiza a vítima para golpes físicos "
                            "ou fornece contexto para spear phishing; "
                            "(3) Nome do banco ou empresa — golpista se passa por essas "
                            "instituições para criar abordagem convincente."
                        ),
                        "evaluation_criteria": [
                            "Lista 3 tipos de informação com risco de exposição.",
                            "Explica como cada uma pode ser usada em golpe específico.",
                            "Demonstra entendimento de que informações públicas facilitam personalização.",
                        ],
                        "max_length": 2000,
                    },
                },
                {
                    "order": 5,
                    "activity_type": "multiple_choice",
                    "points_value": 10,
                    "content": {
                        "schema_version": 1,
                        "prompt": (
                            "Você recebeu um SMS com código de verificação que "
                            "você não solicitou. O que você deve fazer?"
                        ),
                        "competency_codes": ["11.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Ignorar e, se houver tentativas repetidas, trocar "
                                    "a senha imediatamente."
                                ),
                            },
                            {"value": "b", "label": "Fornecer o código se alguém ligar pedindo."},
                            {"value": "c", "label": "Encaminhar o código para confirmar que é seu."},
                            {"value": "d", "label": "Aguardar o código expirar."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Um código de verificação não solicitado significa "
                            "que alguém tentou usar suas credenciais. Troque sua senha "
                            "imediatamente. Nunca compartilhe o código — mesmo que "
                            "alguém ligue dizendo que enviou 'por engano'."
                        ),
                        "feedback_incorrect": (
                            "Código de verificação não solicitado = tentativa de acesso "
                            "por outra pessoa. Troque a senha imediatamente. Nunca "
                            "compartilhe o código — quem ligar pedindo está tentando "
                            "acessar sua conta."
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
                            "O que a LGPD (Lei Geral de Proteção de Dados) garante "
                            "ao cidadão em relação aos próprios dados?"
                        ),
                        "competency_codes": ["11.3.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Direito de saber quais dados uma empresa tem, "
                                    "corrigir dados incorretos e solicitar exclusão "
                                    "em determinados casos."
                                ),
                            },
                            {"value": "b", "label": "Garantia de que seus dados nunca serão usados por empresas."},
                            {"value": "c", "label": "Isenção de publicidade direcionada."},
                            {"value": "d", "label": "Apenas o direito de cancelar cadastros."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! A LGPD (Lei 13.709/2018) garante direitos como: "
                            "acesso aos dados, correção, exclusão, portabilidade e "
                            "revogação de consentimento. Você pode solicitar que uma "
                            "empresa informe quais dados seus ela possui."
                        ),
                        "feedback_incorrect": (
                            "A LGPD não proíbe o uso de dados — ela regula como podem "
                            "ser usados. Garante ao titular: saber quais dados existem, "
                            "corrigir erros, solicitar exclusão em alguns casos e "
                            "revogar o consentimento de uso."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Dados que nunca devem ser compartilhados",
                    "order": 1,
                    "body": (
                        "Independentemente do canal ou do pretexto:\n\n"
                        "❌ **Senha bancária** — de acesso ao app ou internet banking\n"
                        "❌ **Token/código de verificação** — enviado por SMS ou gerado no app\n"
                        "❌ **CVV do cartão** — 3 dígitos no verso\n"
                        "❌ **Senha do cartão** — PIN de 4 a 6 dígitos\n"
                        "❌ **Código de desbloqueio do celular**\n\n"
                        "Bancos, operadoras e qualquer instituição legítima **nunca pedem** "
                        "esses dados por telefone, SMS, e-mail, WhatsApp ou redes sociais."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Autenticação em dois fatores: por que usar",
                    "order": 2,
                    "body": (
                        "O 2FA adiciona uma segunda camada de segurança além da senha.\n\n"
                        "**Como funciona:** além de senha, você precisar de um código "
                        "temporário (SMS, e-mail ou app autenticador) para concluir o login.\n\n"
                        "**Por que protege:** mesmo que sua senha seja roubada "
                        "(em phishing ou vazamento), o atacante não consegue acessar "
                        "sem o segundo fator.\n\n"
                        "**Ative em:** bancos, e-mails, redes sociais, plataformas "
                        "de pagamento e qualquer serviço que ofereça a opção.\n\n"
                        "**Atenção:** nunca compartilhe o código 2FA com ninguém — "
                        "ele tem validade de segundos e é pessoal."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Senhas fortes: comprimento + variedade",
                    "order": 3,
                    "body": (
                        "Uma senha forte tem:\n\n"
                        "- **Comprimento:** mínimo 12 caracteres\n"
                        "- **Variedade:** maiúsculas, minúsculas, números e símbolos\n"
                        "- **Exclusividade:** diferente para cada serviço\n"
                        "- **Sem padrões óbvios:** nada de datas, nomes de parentes "
                        "ou sequências (123, abc)\n\n"
                        "**Dica prática:** use uma frase que só você sabe e substitua "
                        "algumas letras por símbolos e números.\n\n"
                        "**Gerenciador de senhas:** aplicativos como bitwarden.com, "
                        "1Password ou o gerenciador do navegador guardam senhas "
                        "diferentes para cada site — você precisa lembrar apenas uma."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Redes sociais e exposição de dados",
                    "order": 4,
                    "body": (
                        "Golpistas usam informações públicas para personalizar abordagens "
                        "(spear phishing). Cuidado com o que você publica:\n\n"
                        "- **Data de nascimento:** usada para confirmar identidade ou "
                        "criar urgência personalizada\n"
                        "- **Nome do banco:** golpista pode fingir ser funcionário do "
                        "seu banco específico\n"
                        "- **Cidade e rotina:** facilita abordagem no golpe do falso parente\n"
                        "- **Viagens:** indica quando você está ausente\n"
                        "- **Número do celular completo:** facilita smishing direcionado\n\n"
                        "Revise as configurações de privacidade nas redes sociais "
                        "e limite quem pode ver suas informações."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "O token que Carlos compartilhou (fictício)",
                    "order": 5,
                    "body": (
                        "**Situação fictícia:**\n\n"
                        "Carlos recebe uma ligação: 'Aqui é o suporte do banco. "
                        "Vamos enviar um código para confirmar sua identidade.'\n\n"
                        "Ele recebe um SMS com um código e fornece ao 'suporte'.\n\n"
                        "Resultado: o código era o token de autenticação para alterar "
                        "a senha do banco. O atacante usou o código para acessar "
                        "a conta de Carlos.\n\n"
                        "**O erro:** compartilhar o token. Esse código nunca deve "
                        "ser fornecido a ninguém, em nenhuma circunstância.\n\n"
                        "*(Situação fictícia, para fins didáticos.)*"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "LGPD: seus direitos básicos sobre seus dados",
                    "order": 6,
                    "body": (
                        "A **Lei Geral de Proteção de Dados (Lei 13.709/2018)** "
                        "garante ao cidadão:\n\n"
                        "- **Acesso:** saber quais dados uma empresa tem sobre você\n"
                        "- **Correção:** corrigir dados incompletos ou incorretos\n"
                        "- **Exclusão:** solicitar apagamento em determinados casos\n"
                        "- **Portabilidade:** transferir dados para outra empresa\n"
                        "- **Revogação de consentimento:** retirar a autorização de uso\n"
                        "- **Informação sobre compartilhamento:** saber com quem seus "
                        "dados são compartilhados\n\n"
                        "Para exercer esses direitos, entre em contato com o encarregado "
                        "de dados (DPO) da empresa ou use os canais de atendimento."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 11.4 — O que fazer depois
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 4,
            "name": "O que fazer depois",
            "description": (
                "Saiba agir corretamente após um golpe financeiro: acionar a "
                "instituição, entender o MED e registrar evidências."
            ),
            "order": 4,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "11.4.1",
                    "name": "Descrever os procedimentos corretos após um golpe",
                    "description": (
                        "Enumera as ações prioritárias: contato imediato com a IF, "
                        "registro de evidências e boletim de ocorrência."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.4.2",
                    "name": "Conhecer o MED, seus critérios e limitações",
                    "description": (
                        "Explica o que é o MED, quando se aplica, suas limitações "
                        "e a diferença entre fraude e erro de transferência."
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
                            "Qual é a primeira ação ao perceber que você foi vítima "
                            "de um golpe financeiro com Pix?"
                        ),
                        "competency_codes": ["11.4.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Contatar imediatamente o banco para solicitar "
                                    "o acionamento do MED e bloqueio do golpista."
                                ),
                            },
                            {"value": "b", "label": "Aguardar até o próximo dia útil para ligar."},
                            {"value": "c", "label": "Primeiro registrar o boletim de ocorrência."},
                            {"value": "d", "label": "Postar nas redes sociais para alertar outros."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O tempo é crítico. Contate o banco imediatamente — "
                            "quanto antes o MED for acionado, maior a chance de o valor "
                            "ainda estar disponível na conta de destino. "
                            "O boletim de ocorrência pode ser feito depois."
                        ),
                        "feedback_incorrect": (
                            "A prioridade é contatar o banco imediatamente. "
                            "O MED tem prazo e depende de o dinheiro ainda estar "
                            "disponível na conta de destino. Aguardar reduz as chances. "
                            "O boletim de ocorrência é importante, mas pode ser feito depois."
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
                            "O MED garante a devolução de qualquer Pix enviado "
                            "para golpistas?"
                        ),
                        "competency_codes": ["11.4.2"],
                        "options": [
                            {"value": "a", "label": "Sim — o MED devolve sempre o valor integral."},
                            {
                                "value": "b",
                                "label": (
                                    "Não — o MED tem critérios específicos e depende de "
                                    "o dinheiro ainda estar disponível na conta de destino."
                                ),
                            },
                            {"value": "c", "label": "Sim — desde que o boletim seja registrado."},
                            {"value": "d", "label": "Não — o MED só funciona para valores acima de R$ 1.000."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O MED não garante devolução automática. "
                            "Depende de: fraude confirmada segundo os critérios do BCB, "
                            "saldo disponível na conta de destino e prazo de acionamento. "
                            "Não prometa devolução garantida."
                        ),
                        "feedback_incorrect": (
                            "O MED tem limitações importantes: exige critérios de fraude "
                            "confirmados, depende de saldo na conta de destino e tem prazo. "
                            "Se o golpista já sacou o dinheiro, não há o que devolver. "
                            "O acionamento rápido aumenta as chances, mas não garante."
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
                            "Qual é a diferença entre acionar o MED por fraude e "
                            "solicitar devolução por erro de transferência?"
                        ),
                        "competency_codes": ["11.4.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "MED por fraude: aciona bloqueio automático da conta "
                                    "do golpista suspeito. Erro de transferência: pedido "
                                    "de devolução voluntária ao destinatário — não aciona "
                                    "o mesmo mecanismo de bloqueio."
                                ),
                            },
                            {"value": "b", "label": "São o mesmo processo com nomes diferentes."},
                            {"value": "c", "label": "Erro de transferência tem resposta mais rápida."},
                            {"value": "d", "label": "O MED cobre erros de transferência também."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! O MED é um mecanismo específico para fraude — "
                            "pode bloquear a conta suspeita e iniciar processo de "
                            "devolução. Um erro de transferência (enviou para a pessoa "
                            "errada por engano) é tratado como pedido de devolução "
                            "voluntária pelo destinatário — processo diferente."
                        ),
                        "feedback_incorrect": (
                            "São situações distintas: MED por fraude aciona bloqueio "
                            "automático. Erro de transferência depende da boa vontade "
                            "do destinatário ou de medida judicial — não há bloqueio "
                            "automático só porque você enviou para o número errado."
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
                            "Em quanto tempo após o golpe você deve acionar o banco "
                            "para maximizar as chances de recuperação?"
                        ),
                        "competency_codes": ["11.4.1"],
                        "options": [
                            {"value": "a", "label": "Imediatamente — quanto antes, melhor."},
                            {"value": "b", "label": "Em até 5 dias úteis."},
                            {"value": "c", "label": "Em até 30 dias."},
                            {"value": "d", "label": "O prazo não importa."},
                        ],
                        "correct_answer": "a",
                        "feedback_correct": (
                            "Correto! Quanto mais rápido, maior a chance de o dinheiro "
                            "ainda estar na conta de destino. Golpistas movem os valores "
                            "rapidamente — minutos ou horas depois do recebimento."
                        ),
                        "feedback_incorrect": (
                            "Tempo é crítico. Golpistas movem dinheiro em minutos. "
                            "Acionar o banco imediatamente — pelo aplicativo ou telefone — "
                            "é a ação com maior impacto para a recuperação."
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
                            "Você percebeu que foi vítima de um golpe de Pix agora. "
                            "Descreva as ações que você tomaria nas próximas 24 horas, "
                            "em ordem de prioridade."
                        ),
                        "competency_codes": ["11.4.1", "11.4.2"],
                        "feedback_static": (
                            "Sua resposta foi registrada. "
                            "Ordem esperada: (1) acionar o banco imediatamente — "
                            "chat/telefone/app — solicitando MED; "
                            "(2) guardar todas as evidências (prints, mensagens, "
                            "número de protocolo do atendimento); "
                            "(3) registrar boletim de ocorrência (pode ser online); "
                            "(4) acompanhar o andamento do caso junto ao banco; "
                            "(5) comunicar às autoridades se necessário (Delegacia "
                            "de Crimes Cibernéticos)."
                        ),
                        "evaluation_criteria": [
                            "Prioriza o contato imediato com o banco.",
                            "Menciona a coleta e guarda de evidências.",
                            "Menciona o boletim de ocorrência.",
                            "Demonstra entendimento das limitações do MED.",
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
                            "Registrar boletim de ocorrência policial é obrigatório "
                            "para acionar o MED?"
                        ),
                        "competency_codes": ["11.4.2"],
                        "options": [
                            {"value": "a", "label": "Sim — sem BO o MED não é aceito."},
                            {
                                "value": "b",
                                "label": (
                                    "Não — o MED é acionado pelo banco. O BO é importante "
                                    "para a investigação, mas não é pré-requisito obrigatório "
                                    "para o acionamento inicial."
                                ),
                            },
                            {"value": "c", "label": "Sim — em todos os casos."},
                            {"value": "d", "label": "Apenas para valores acima de R$ 5.000."},
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! O BO não é pré-requisito para acionar o MED pelo banco. "
                            "O banco pode iniciar o processo com o relato da vítima. "
                            "O BO é importante para a investigação policial e fortalece "
                            "o caso, mas não deve ser feito antes do acionamento bancário."
                        ),
                        "feedback_incorrect": (
                            "O MED é acionado pelo banco com base no relato da vítima. "
                            "O BO fortalece o caso e é recomendável, mas não é "
                            "obrigatório como primeiro passo. Priorize o banco primeiro."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "O que fazer imediatamente após um golpe",
                    "order": 1,
                    "body": (
                        "**Ordem de ações após perceber um golpe financeiro:**\n\n"
                        "1. **Acionar o banco imediatamente**\n"
                        "   - Pelo app, chat ou telefone (número do cartão)\n"
                        "   - Solicitar acionamento do MED\n"
                        "   - Anotar o número de protocolo\n\n"
                        "2. **Guardar todas as evidências**\n"
                        "   - Screenshots da conversa, e-mail ou mensagem\n"
                        "   - Comprovante da transação fraudulenta\n"
                        "   - Número do protocolo do banco\n\n"
                        "3. **Registrar boletim de ocorrência**\n"
                        "   - Pode ser feito online (delegacia virtual de cada estado)\n"
                        "   - Fortalece o caso e é exigido em alguns processos judiciais\n\n"
                        "4. **Acompanhar o caso**\n"
                        "   - Monitorar o status junto ao banco\n"
                        "   - Se necessário, acionar o Banco Central (reclame.bcb.gov.br)"
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "O MED: o que é, critérios e limitações",
                    "order": 2,
                    "body": (
                        "O **Mecanismo Especial de Devolução (MED)** é um processo "
                        "do ecossistema Pix para facilitar a devolução de valores "
                        "em casos de fraude.\n\n"
                        "**Quando se aplica:**\n"
                        "- Fraude confirmada segundo os critérios do Banco Central\n"
                        "- Envio de Pix a conta suspeita de uso fraudulento\n\n"
                        "**Limitações importantes:**\n"
                        "- Depende de o dinheiro ainda estar disponível na conta de destino\n"
                        "- Tem prazo para acionamento\n"
                        "- Não é garantia de devolução\n"
                        "- Erro de transferência (número errado) não aciona o mesmo processo\n\n"
                        "Fonte: Resolução BCB nº 128/2021 e atualizações. "
                        "Consulte sempre o BCB para critérios vigentes."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "MED por fraude vs. erro de transferência",
                    "order": 3,
                    "body": (
                        "| Situação | Processo | Chance de devolução |\n"
                        "|---|---|---|\n"
                        "| Fraude confirmada | MED — bloqueio automático | Depende do saldo |\n"
                        "| Erro de transferência | Pedido de devolução voluntária | Baixa sem acordo |\n\n"
                        "**Fraude:** você foi enganado para fazer a transferência "
                        "(golpe do comprovante falso, falsa central etc.).\n\n"
                        "**Erro:** você transferiu para o destinatário errado por "
                        "equívoco seu. O destinatário não é obrigado a devolver — "
                        "pode ser necessária medida judicial.\n\n"
                        "**Importante:** não afirme que todo Pix fraudulento será "
                        "devolvido. O MED é um mecanismo, não uma garantia."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "Guarde evidências: elas valem muito depois",
                    "order": 4,
                    "body": (
                        "Logo após perceber o golpe, antes de apagar qualquer coisa:\n\n"
                        "- **Captura de tela** da conversa no WhatsApp, SMS ou e-mail\n"
                        "- **Foto do número** de telefone do golpista\n"
                        "- **Print do extrato** com a transação fraudulenta\n"
                        "- **Número de protocolo** do atendimento bancário\n\n"
                        "Essas evidências são necessárias para o boletim de ocorrência, "
                        "para o processo no banco e em eventual ação judicial."
                    ),
                },
                {
                    "content_type": "explanation",
                    "title": "Canais para buscar ajuda e denunciar",
                    "order": 5,
                    "body": (
                        "| Canal | Quando usar |\n"
                        "|---|---|\n"
                        "| Banco (app/telefone) | Primeiro passo — MED e bloqueio |\n"
                        "| Delegacia virtual do estado | Boletim de ocorrência |\n"
                        "| Banco Central (reclame.bcb.gov.br) | Se o banco não responder |\n"
                        "| Procon | Questões de consumo |\n"
                        "| Delegacia de Crimes Cibernéticos | Para investigação policial |\n\n"
                        "Para fraudes com Pix, o banco é o primeiro canal — "
                        "ele tem acesso ao MED e às informações da conta de destino."
                    ),
                },
            ],
        },
        # ──────────────────────────────────────────────────────────────────
        # Missão 11.5 — Reconhecimento rápido (apenas simulações)
        # ──────────────────────────────────────────────────────────────────
        {
            "number": 5,
            "name": "Reconhecimento rápido",
            "description": (
                "Aplique as competências de proteção em cenários simulados "
                "de tentativa de golpe."
            ),
            "order": 5,
            "is_required": True,
            "passing_score": 70,
            "competencies": [
                {
                    "code": "11.5.1",
                    "name": "Identificar tentativa de golpe em cenário simulado",
                    "description": (
                        "Reconhece os sinais de golpe em uma situação apresentada "
                        "de forma realista."
                    ),
                    "is_essential": True,
                },
                {
                    "code": "11.5.2",
                    "name": "Tomar a decisão correta diante de uma tentativa de golpe",
                    "description": (
                        "Escolhe a ação adequada ao identificar um golpe, "
                        "sem agir por impulso ou pressão."
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
                            "Você recebe uma mensagem de texto: 'Seu acesso ao banco "
                            "foi temporariamente suspenso. Para reativar, acesse: "
                            "www.seubanco-atendimento-urgente.com e confirme seus dados. "
                            "Prazo: 2 horas.' O que você faz?"
                        ),
                        "competency_codes": ["11.5.1", "11.5.2"],
                        "scenario": (
                            "Mensagem de texto recebida no celular. URL diferente "
                            "do site oficial do banco. Urgência artificial. "
                            "Situação fictícia, para fins didáticos."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Acessar o link, pois a urgência indica situação real."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Não acessar o link. Abrir o aplicativo oficial do banco "
                                    "diretamente para verificar se há algum alerta real."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Responder à mensagem pedindo mais informações."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Decisão correta! A mensagem tem todos os sinais de phishing: "
                            "urgência artificial ('2 horas'), ameaça ('suspenso') e URL "
                            "diferente do site oficial do banco. Verificar pelo app "
                            "oficial — que você mesmo abre, sem seguir o link — é "
                            "a única ação segura."
                        ),
                        "feedback_incorrect": (
                            "Essa mensagem é um phishing clássico: urgência, ameaça "
                            "e URL suspeita. Acessar o link ou responder expõe seus dados. "
                            "A ação correta é abrir o aplicativo oficial diretamente "
                            "e verificar se há algum alerta na conta."
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
                            "Um contato no WhatsApp com número desconhecido escreve: "
                            "'Oi mãe/pai, troquei de número. Estou com uma emergência "
                            "e preciso de R$ 500 agora. Você pode mandar para este Pix?' "
                            "O que você faz?"
                        ),
                        "competency_codes": ["11.5.1", "11.5.2"],
                        "scenario": (
                            "Mensagem no WhatsApp com número desconhecido. "
                            "Pedido de dinheiro urgente. "
                            "Situação fictícia (golpe do falso parente)."
                        ),
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Transferir imediatamente — é meu familiar."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Antes de qualquer ação, ligar para o familiar "
                                    "pelo número que você já tem para confirmar "
                                    "se é realmente ele."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Pedir mais provas, como uma foto."
                                ),
                            },
                        ],
                        "correct_choice": "b",
                        "feedback_correct": (
                            "Decisão correta! Ligar para o familiar pelo número que você "
                            "já conhece é a única forma de confirmar. "
                            "O golpe do falso parente usa o gatilho emocional do cuidado "
                            "para pressionar pela transferência rápida. "
                            "Fotos podem ser falsificadas — a ligação é o único teste."
                        ),
                        "feedback_incorrect": (
                            "Esse é o golpe do falso parente: número novo + urgência + "
                            "pedido de dinheiro. Pedir foto não é suficiente "
                            "(pode ser falsificada). A única verificação confiável é "
                            "ligar para o familiar pelo número que você já tem."
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
                            "Qual das seguintes situações tem MENOS sinais de golpe?"
                        ),
                        "competency_codes": ["11.5.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "E-mail com urgência pedindo que você clique em "
                                    "link para confirmar senha."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Notificação do próprio aplicativo do banco "
                                    "informando uma transferência que você mesmo fez."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Ligação de número desconhecido alegando ser "
                                    "do banco e pedindo seu token."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Mensagem de WhatsApp com número novo pedindo "
                                    "dinheiro urgente."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Notificação do próprio aplicativo sobre uma "
                            "transferência que você fez é o comportamento esperado "
                            "do sistema. As outras opções têm sinais clássicos: "
                            "urgência + link externo, pedido de token por ligação, "
                            "e número novo + pedido de dinheiro."
                        ),
                        "feedback_incorrect": (
                            "Revise. A notificação do aplicativo sobre ação que você "
                            "mesmo realizou é esperada e não tem sinais de golpe. "
                            "As outras situações têm urgência, link externo, pedido "
                            "de token ou número desconhecido — todos sinais de alerta."
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
                            "Você recebeu um Pix 'por engano' de R$ 200 de um "
                            "desconhecido, que logo em seguida pede que você devolva "
                            "R$ 400 porque 'precisa de troco'. O que está acontecendo?"
                        ),
                        "competency_codes": ["11.5.1"],
                        "options": [
                            {
                                "value": "a",
                                "label": "Um erro genuíno que merece ajuda imediata.",
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Uma tentativa de golpe: o Pix recebido pode ser "
                                    "fraudulento, e o pedido de 'troco' faz você pagar "
                                    "mais do que recebeu."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Uma confusão bancária que o banco vai resolver "
                                    "automaticamente."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Exato! Esse é o golpe do 'Pix errado com troco': "
                            "o valor recebido pode ter origem fraudulenta e você "
                            "ainda pagaria mais do que recebeu. "
                            "Nunca devolva valores fora do mecanismo oficial de "
                            "devolução do banco."
                        ),
                        "feedback_incorrect": (
                            "Cuidado! Esse é um golpe conhecido: enviam um valor "
                            "e pedem que você devolva mais. O Pix recebido pode "
                            "ter origem suspeita. Nunca faça transferência fora do "
                            "mecanismo de devolução oficial do banco."
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
                            "Qual atitude reduz MAIS o risco de cair em um golpe "
                            "de engenharia social?"
                        ),
                        "competency_codes": ["11.5.2"],
                        "options": [
                            {
                                "value": "a",
                                "label": (
                                    "Atender ligações apenas de números conhecidos."
                                ),
                            },
                            {
                                "value": "b",
                                "label": (
                                    "Verificar qualquer pedido urgente de dinheiro "
                                    "ou dados por um canal que você iniciou, "
                                    "independentemente de quem parece estar pedindo."
                                ),
                            },
                            {
                                "value": "c",
                                "label": (
                                    "Nunca usar o celular para operações bancárias."
                                ),
                            },
                            {
                                "value": "d",
                                "label": (
                                    "Compartilhar informações apenas com pessoas "
                                    "que você conhece pessoalmente."
                                ),
                            },
                        ],
                        "correct_answer": "b",
                        "feedback_correct": (
                            "Correto! Verificar por um canal que você iniciou "
                            "(ligar pelo número oficial, abrir o aplicativo direto) "
                            "é a defesa mais eficaz — independentemente de como "
                            "a solicitação chegou."
                        ),
                        "feedback_incorrect": (
                            "A atitude mais eficaz é verificar todo pedido urgente "
                            "por um canal que você controlou — você ligou, você "
                            "abriu o app. Não basta conhecer o número ou conhecer "
                            "a pessoa: golpistas imitam ambos."
                        ),
                    },
                },
            ],
            "content_items": [
                {
                    "content_type": "explanation",
                    "title": "Como funciona o reconhecimento rápido",
                    "order": 1,
                    "body": (
                        "Nesta missão você vai treinar o **reconhecimento rápido**: "
                        "diante de uma situação suspeita, você tem poucos segundos para "
                        "decidir — e é exatamente aí que os golpistas contam com a "
                        "pressa e a emoção.\n\n"
                        "O exercício é simples: leia o cenário, identifique os sinais "
                        "de alerta e escolha a ação correta. Cada decisão certa "
                        "reforça o hábito de parar antes de agir."
                    ),
                },
                {
                    "content_type": "example",
                    "title": "Padrão dos golpes mais comuns",
                    "order": 2,
                    "body": (
                        "A maioria dos golpes compartilha pelo menos um destes elementos:\n\n"
                        "1. **Urgência artificial:** 'precisa ser agora', 'última chance', "
                        "'sua conta será bloqueada'\n"
                        "2. **Pedido de sigilo:** 'não conta para ninguém', 'só você pode "
                        "resolver'\n"
                        "3. **Solicitação de dado sensível:** senha, token, código por SMS\n"
                        "4. **Contato de canal não oficial:** número desconhecido, link "
                        "encaminhado, e-mail com domínio estranho\n"
                        "5. **Pressão emocional:** 'seu filho está em apuros', 'você foi "
                        "sorteado', 'há uma fraude na sua conta'\n\n"
                        "Identificar qualquer um desses elementos é sinal para parar "
                        "e verificar por um canal que você já conhece."
                    ),
                },
                {
                    "content_type": "tip",
                    "title": "A regra dos 5 segundos",
                    "order": 3,
                    "body": (
                        "Antes de qualquer ação que envolva dinheiro ou dados pessoais, "
                        "pergunte a si mesmo:\n\n"
                        "1. Eu iniciei este contato, ou ele veio até mim?\n"
                        "2. Há pressa ou pressão para decidir agora?\n"
                        "3. Estou sendo pedido a fornecer uma senha, código ou "
                        "transferência?\n\n"
                        "Se a resposta for 'não' à primeira e 'sim' a qualquer das outras, "
                        "**não prossiga**. Ligue para a instituição pelo número oficial "
                        "antes de fazer qualquer coisa."
                    ),
                },
            ],
        },
    ],
}
