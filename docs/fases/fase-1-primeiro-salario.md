# Fase 1 — Primeiro salário

**number:** 1
**name:** Primeiro salário
**order:** 1
**description:** Entenda de onde vem o dinheiro, o que vem primeiro e como organizar a sua primeira renda.

> Este documento é a referência editorial em Markdown. O conteúdo executável está em
> `backend/app/modules/content/seeds/phase_1_v1.py` e é carregado pela migration
> `0002_phase_1_content.py`.
> Todos os itens de conteúdo educacional desta fase são inseridos como publicados;
> o admin pode despublicá-los depois de uma revisão.
> Todas as missões: `is_required: true`, `passing_score: 70`.
> Contrato dos campos: `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md`.
> Critérios de domínio e desbloqueio: `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`.
> Valores em reais de 2026 (INSS, IRRF, salário mínimo). Ver "Pontos para revisão" no final do arquivo.

---

## Missão 1.1 — De onde vem o dinheiro?

**number:** 1
**order:** 1
**Descrição:** O usuário diferencia salário bruto de líquido e reconhece os principais descontos de um contracheque.
**passing_score:** 70
**is_required:** true

### Competências
1. Distinguir salário bruto de salário líquido (is_essential: true)
2. Identificar os descontos obrigatórios de um contracheque e o que não é descontado, como o FGTS (is_essential: false)
3. Calcular o salário líquido a partir de um contracheque fictício (is_essential: true)

### Conteúdo educacional

**[explanation] O que é salário bruto e líquido** (order: 1)

Quando uma empresa diz "o salário é R$ 2.000", normalmente está falando do **salário bruto**: o valor combinado, **antes** de qualquer desconto.

O **salário líquido** é o que **realmente cai na sua conta**, depois dos descontos obrigatórios e de eventuais descontos que você autorizou.

Fórmula simples:

**salário líquido = salário bruto − descontos**

Por isso, ao receber uma proposta de emprego, vale perguntar: "esse valor é bruto ou líquido?". A diferença pode mudar bastante o seu planejamento.

**[explanation] Os principais descontos do contracheque** (order: 2)

Os descontos mais comuns para quem trabalha com carteira assinada:

- **INSS:** contribuição para a Previdência Social, que garante benefícios como aposentadoria, auxílio por doença e salário-maternidade. Em 2026, as alíquotas vão de 7,5% a 14% e são aplicadas **por faixa**: cada parte do salário paga a sua própria alíquota. Não existe uma alíquota única sobre o salário inteiro.
- **Imposto de Renda retido na fonte (IRRF):** desde janeiro de 2026, quem recebe até R$ 5.000 por mês tem o IRRF zerado. Por isso, em um primeiro salário, é comum que esse desconto seja R$ 0,00.
- **Vale-transporte:** se você optar por usar, a empresa pode descontar até 6% do seu salário-base.

E um item que **aparece no contracheque, mas não sai do seu bolso**:

- **FGTS:** o empregador deposita 8% do salário em uma conta vinculada ao seu nome. Não reduz o seu salário líquido.

**[example] O contracheque da Ana (fictício)** (order: 3)

A Ana começou a trabalhar com salário bruto de **R$ 2.000,00**. Veja o contracheque dela:

| Item | Valor |
|---|---|
| Salário bruto | R$ 2.000,00 |
| INSS | − R$ 155,68 |
| IRRF | R$ 0,00 |
| Vale-transporte | − R$ 120,00 |
| **Salário líquido** | **R$ 1.724,32** |
| FGTS (depositado pela empresa, não é desconto) | R$ 160,00 |

Como o INSS foi calculado por faixas: os primeiros R$ 1.621,00 pagam 7,5% (R$ 121,57) e os R$ 379,00 restantes pagam 9% (R$ 34,11).

Repare: a Ana combinou R$ 2.000, mas o que ela tem para gastar no mês é R$ 1.724,32. É sobre esse valor que ela precisa fazer o planejamento.

*(Valores fictícios e arredondados, para fins didáticos.)*

**[tip] Confira o seu contracheque todo mês** (order: 4)

Olhe sempre três linhas: **bruto**, **descontos** e **líquido**. Se alguma linha não fizer sentido, pergunte ao RH ou ao responsável pela folha de pagamento. Entender o contracheque é o primeiro passo para controlar o seu dinheiro.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 1.1.1
question: Uma proposta de emprego informa salário de R$ 2.000 bruto. O que isso significa?
options:
A: Que você receberá exatamente R$ 2.000 na conta
B: Que R$ 2.000 é o valor antes dos descontos; o que cai na conta normalmente será menor
C: Que R$ 2.000 é o valor depois de todos os descontos
D: Que R$ 2.000 é só o valor dos benefícios, sem contar o salário
correct_answer: B
feedback_correct: Exato! O salário bruto é o valor combinado antes dos descontos. O que você recebe de fato é o líquido, que normalmente é menor.
feedback_incorrect: Não exatamente. O salário bruto é o valor acordado antes de qualquer desconto. O líquido, que é o que cai na conta, normalmente é menor.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 1.1.2
question: Em um contracheque aparecem INSS, vale-transporte (quando o trabalhador opta por usar) e FGTS. Qual desses NÃO é descontado do salário do trabalhador?
options:
A: INSS
B: Vale-transporte
C: FGTS
D: Todos são descontados do salário
correct_answer: C
feedback_correct: Isso mesmo! O FGTS é depositado pelo empregador em uma conta em seu nome. Ele aparece no contracheque, mas não reduz o seu salário líquido.
feedback_incorrect: Quase! O INSS e o vale-transporte são descontados do salário. O FGTS é diferente: é o empregador que deposita, e o valor não sai do seu salário.

**Atividade 3 — multiple_choice (10 pts)**
competencia: 1.1.3
question: Um contracheque fictício mostra: salário bruto R$ 2.000,00; INSS R$ 155,68; IRRF R$ 0,00; vale-transporte R$ 120,00. Qual é o salário líquido?
options:
A: R$ 1.724,32
B: R$ 1.844,32
C: R$ 1.880,00
D: R$ 2.000,00
correct_answer: A
feedback_correct: Correto! 2.000,00 − 155,68 − 0,00 − 120,00 = R$ 1.724,32. É esse o valor que realmente cai na conta.
feedback_incorrect: Não foi dessa vez. O líquido é o bruto menos todos os descontos: 2.000,00 − 155,68 − 0,00 − 120,00 = R$ 1.724,32. Conferir se todos os descontos entraram na conta ajuda a evitar erros.

**Atividade 4 — open_text (0 pts)**
competencia: 1.1.1 e 1.1.2
question: Explique com as suas palavras, como se fosse para um amigo: por que o valor que cai na conta costuma ser diferente do valor combinado quando a pessoa é contratada?
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) que o salário bruto é o valor combinado antes dos descontos; (2) pelo menos um desconto, como INSS, imposto de renda ou vale-transporte; (3) que o salário líquido é o valor que de fato cai na conta. Ausência de (1) ou (3) indica lacuna na competência 1.1.1; ausência de (2) indica lacuna na competência 1.1.2.

---

## Missão 1.2 — O que importa primeiro?

**number:** 2
**order:** 2
**Descrição:** O usuário separa necessidades de desejos e define prioridades quando o dinheiro não dá para tudo.
**passing_score:** 70
**is_required:** true

### Competências
1. Diferenciar necessidades de desejos (is_essential: true)
2. Priorizar gastos quando a renda é limitada (is_essential: true)
3. Reconhecer que a mesma despesa pode ser necessidade ou desejo, dependendo do contexto (is_essential: false)

### Conteúdo educacional

**[explanation] Necessidade, desejo e prioridade** (order: 1)

**Necessidade** é o gasto de que você precisa para viver e cumprir suas obrigações: moradia, alimentação, contas básicas como água e luz, transporte para ir ao trabalho ou à escola, saúde.

**Desejo** é o que melhora a vida, mas pode esperar ou ser trocado por algo mais barato: streaming, roupa nova só por moda, delivery, passeios.

**Prioridade** é a ordem em que você paga as coisas quando o dinheiro não dá para tudo. Uma regra prática: o que traz consequências sérias se não for pago (aluguel, luz, dívidas com juros) vem **antes** dos desejos.

Desejo não é errado. A ideia é dar um espaço para ele **sem comprometer o essencial**.

**[example] O mesmo gasto, dois contextos** (order: 2)

A **Marina** usa o celular para receber os pedidos do trabalho. O aparelho quebrou. Para ela, ter um celular funcionando é uma **necessidade**, porque sem ele ela não trabalha. Mesmo assim, o que ela precisa é de um aparelho que funcione, e não necessariamente do modelo mais caro.

O **Pedro** tem um celular funcionando, mas quer trocar pelo último lançamento. Para ele, a troca é um **desejo**.

O mesmo item (um celular) pode ser necessidade para uma pessoa e desejo para outra. O que muda é o **contexto** e a **consequência** de não ter.

**[tip] A pergunta que ajuda a decidir** (order: 3)

Antes de comprar, pergunte: **"o que acontece se eu não comprar isso este mês?"** Se a resposta for "nada grave", provavelmente é um desejo. Ele pode esperar, ser trocado por uma opção mais barata ou virar um objetivo.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 1.2.1
question: Qual dos itens abaixo é uma necessidade básica?
options:
A: Assinatura de streaming
B: Conta de luz da casa
C: Tênis de marca novo
D: Ingresso para um show
correct_answer: B
feedback_correct: Exato! A conta de luz é uma despesa essencial: sem pagá-la, você perde um serviço básico. Os outros itens são desejos que podem esperar.
feedback_incorrect: Não exatamente. A conta de luz é essencial para morar. Streaming, tênis de marca e show são desejos: melhoram a vida, mas podem esperar.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 1.2.3
question: Marina usa o celular para receber pedidos do trabalho e o aparelho quebrou. Pedro tem um celular funcionando e quer trocar pelo último lançamento. Qual afirmação está correta?
options:
A: Para os dois, o celular é necessidade
B: Para os dois, o celular é desejo
C: Para Marina, ter um celular funcionando é necessidade; para Pedro, trocar pelo lançamento é desejo
D: Celular só é necessidade se for caro
correct_answer: C
feedback_correct: Muito bem! A classificação depende do contexto. Marina precisa do aparelho para trabalhar; Pedro já tem um que funciona e quer trocar por vontade.
feedback_incorrect: Não exatamente. A mesma despesa pode ser necessidade ou desejo, dependendo do contexto. Marina precisa de um celular para trabalhar. Pedro já tem um funcionando, então a troca é desejo.

**Atividade 3 — multiple_choice (10 pts)**
competencia: 1.2.2
question: Você tem R$ 900 até o fim do mês. Já está certo que vai pagar o aluguel (R$ 500) e o mercado (R$ 300). Um amigo chama você para um show, com ingresso de R$ 200. O que é mais sensato?
options:
A: Comprar o ingresso primeiro, porque pode esgotar
B: Pagar aluguel e mercado primeiro; o show só entra se couber no que sobrar (R$ 100) ou fica para depois
C: Dividir o dinheiro igualmente entre os três
D: Pagar o mercado e o show, e ver depois como fica o aluguel
correct_answer: B
feedback_correct: Boa decisão! Aluguel e mercado são essenciais e somam R$ 800. O show é desejo: só entra se couber no que sobrar, ou fica para outro momento.
feedback_incorrect: Revise suas prioridades. Aluguel e mercado (R$ 800) vêm antes do show (R$ 200). Com R$ 900, o show não cabe sem comprometer o essencial.

**Atividade 4 — open_text (0 pts)**
competencia: 1.2.1, 1.2.2 e 1.2.3
question: Pense em uma compra que você fez ou quer fazer. Ela é uma necessidade ou um desejo? O que você faria se o dinheiro só desse para esse gasto ou para uma conta essencial?
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) se a compra é necessidade ou desejo, com uma justificativa baseada em consequência ou contexto; (2) que, entre o gasto e a conta essencial, a conta essencial vem primeiro. Ausência de (1) indica lacuna nas competências 1.2.1 ou 1.2.3; ausência de (2) indica lacuna na competência 1.2.2.

---

## Missão 1.3 — Meu primeiro plano

**number:** 3
**order:** 3
**Descrição:** O usuário distribui uma renda fictícia entre despesas essenciais, dívidas, objetivos e reserva, e decide quando as demandas competem entre si.
**passing_score:** 70
**is_required:** true

### Competências
1. Distribuir uma renda líquida entre essenciais, dívidas, objetivos e reserva (is_essential: true)
2. Justificar uma ordem de prioridades com base nas consequências de cada escolha (is_essential: true)
3. Reconhecer por que separar uma parte da renda logo no início do mês (is_essential: false)

### Conteúdo educacional

**[explanation] Um plano simples para a sua renda** (order: 1)

Um plano financeiro não precisa ser complicado. Comece sempre pelo **salário líquido**, que é o dinheiro que realmente existe, e distribua em ordem de prioridade:

1. **Despesas essenciais:** moradia, alimentação, transporte, contas básicas.
2. **Dívidas e contas atrasadas:** especialmente as que geram multa e juros, porque crescem com o tempo.
3. **Objetivos e reserva:** uma parte para algo que você quer conquistar (um curso, um aparelho) e para imprevistos.
4. **Desejos e lazer:** com o que sobrar, sem culpa.

A soma de tudo **não pode passar da renda**. Se passar, é hora de rever as prioridades, e não de usar dinheiro que ainda não existe.

**[example] Do salário à divisão** (order: 2)

O Lucas recebeu R$ 1.500 líquidos no primeiro mês. Ele montou assim:

| Categoria | Valor |
|---|---|
| Essenciais (moradia, comida, transporte) | R$ 900 |
| Conta atrasada (com multa e juros) | R$ 150 |
| Objetivo (curso online) | R$ 150 |
| Reserva | R$ 100 |
| Lazer e desejos | R$ 200 |
| **Total** | **R$ 1.500** |

Repare que as essenciais ocupam 60% da renda, e isso é comum quando a renda ainda é baixa. O importante é que cada real tem um destino e a soma fecha em R$ 1.500.

**[tip] Separe antes de gastar** (order: 3)

Uma forma de proteger o seu objetivo e a sua reserva é separá-los **assim que o salário cai**, e não esperar ver o que sobra no fim do mês, porque quase nunca sobra. Existe uma referência popular chamada 50/30/20 (50% essenciais, 30% desejos, 20% objetivos e reserva), mas ela é só um ponto de partida: com renda menor, as essenciais costumam ocupar mais espaço, e tudo bem.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 1.3.1
question: Ao receber o salário, qual ordem de prioridades faz mais sentido?
options:
A: Despesas essenciais, dívidas com juros, objetivos e reserva, e por último os desejos
B: Desejos, depois essenciais, e dívidas só se sobrar
C: Reserva e objetivos só se sobrar dinheiro no fim do mês
D: Dívidas primeiro, mesmo que falte dinheiro para comer e morar
correct_answer: A
feedback_correct: Exato! O essencial vem primeiro, depois as dívidas que crescem com juros, depois o que constrói o seu futuro, e por último os desejos.
feedback_incorrect: Não exatamente. O essencial (moradia, comida, transporte) vem primeiro, depois as dívidas com juros, depois objetivos e reserva. Os desejos ficam para o que sobrar.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 1.3.3
question: Por que é uma boa ideia separar uma parte do salário para objetivos e reserva logo que o dinheiro cai?
options:
A: Porque assim o dinheiro rende juros automaticamente
B: Porque diminui o risco de gastar tudo e deixa o objetivo protegido antes dos outros gastos
C: Porque a reserva só pode ser feita no começo do mês
D: Porque não é preciso mais se preocupar com as despesas essenciais
correct_answer: B
feedback_correct: Boa! Separar logo no início protege o seu objetivo e a sua reserva, em vez de depender do que sobra no fim do mês.
feedback_incorrect: Revise a ideia. Separar logo no início protege o objetivo e a reserva: se você espera sobrar, o dinheiro quase sempre acaba antes.

**Atividade 3 — open_text (0 pts)**
competencia: 1.3.1 e 1.3.2
question: Imagine que você recebeu R$ 1.800 líquidos no seu primeiro salário. Como você dividiria esse valor? Escreva quanto iria para cada categoria (essenciais, objetivos, reserva, lazer, o que mais achar importante) e explique por quê.
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) despesas essenciais; (2) objetivos; (3) reserva. A soma dos valores informados não deve ultrapassar R$ 1.800. Deve haver alguma justificativa para a divisão. Ausência de qualquer categoria indica lacuna na competência 1.3.1; ausência de justificativa indica lacuna na competência 1.3.2.

**Atividade 4 (simulação da Fase 1) — simulation (20 pts)**
competencia: 1.3.1 e 1.3.2
scenario: Você recebeu seu primeiro salário: R$ 1.800 líquidos. Suas despesas essenciais somam R$ 1.100. Você tem uma conta atrasada de R$ 250 que está gerando multa e juros. Você também paga um curso de inglês de R$ 150 por mês, que é um objetivo importante para você. E há um tênis de R$ 400 que você quer muito. O que você faz?
options:
A: Pago as essenciais e a conta atrasada, mantenho o curso e guardo o restante (R$ 300); o tênis fica para quando eu juntar o valor
B: Pago as essenciais, compro o tênis e deixo a conta atrasada para o mês seguinte
C: Pago as essenciais, o tênis e o curso, e pago da conta atrasada só o que sobrar
D: Compro o tênis primeiro, porque está em promoção, e pago o que der das outras contas
correct_choice: A
feedback_correct: Boa decisão! Você pagou o essencial (R$ 1.100), quitou a conta que gerava juros (R$ 250), manteve o objetivo (R$ 150) e ainda guardou R$ 300. O tênis não foi cancelado: virou uma meta que você pode juntar aos poucos.
feedback_incorrect: Revise suas prioridades. Primeiro o essencial, depois a conta atrasada, que cresce com multa e juros a cada mês. Só então vêm o objetivo e a reserva, e por último o desejo. Fazendo isso: 1.100 + 250 + 150 = 1.500, e ainda sobram R$ 300.

---

## Pontos para revisão antes de publicar

Valores que dependem da legislação de 2026 e devem ser conferidos antes de publicar o conteúdo (e reconferidos a cada janeiro):

- Faixas do INSS para empregados: até R$ 1.621,00 (7,5%); até R$ 2.902,84 (9%); até R$ 4.354,27 (12%); até R$ 8.475,55 (14%). O salário mínimo de 2026 é R$ 1.621,00.
- IRRF: isenção para rendimentos tributáveis de até R$ 5.000,00 por mês (Lei 15.270/2025, em vigor desde 1º/01/2026).
- Vale-transporte: desconto de até 6% do salário-base.
- FGTS: depósito de 8% pelo empregador (não é desconto).
- Cálculo do contracheque da Ana: 1.621,00 × 7,5% = R$ 121,57; 379,00 × 9% = R$ 34,11; INSS total R$ 155,68.
