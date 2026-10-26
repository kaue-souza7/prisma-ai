# Fase 4 — Juros: a favor e contra você

**number:** 4
**name:** Juros: a favor e contra você
**order:** 4
**description:** Veja como os juros e o tempo mudam o valor do dinheiro, a seu favor quando você investe e contra você quando você deve.

> Todos os itens de conteúdo educacional desta fase: `is_published: false` (o admin publica depois da revisão).
> Todas as missões: `is_required: true`, `passing_score: 70`.
> As taxas e os valores usados nos exemplos são fictícios e servem só para ilustrar o conceito. Não representam taxas reais do mercado.

---

## Missão 4.1 — O tempo e os juros

**number:** 1
**order:** 1
**Descrição:** O usuário entende o que são juros, diferencia juros simples de compostos e estima como um valor cresce com o tempo.
**passing_score:** 70
**is_required:** true

### Competências
1. Explicar o que são juros como o preço do dinheiro no tempo (is_essential: true)
2. Diferenciar juros simples de juros compostos (is_essential: true)
3. Estimar o crescimento de um valor com juros compostos em poucos períodos (is_essential: false)

### Conteúdo educacional

**[explanation] O que são juros** (order: 1)

**Juros** são o preço do uso do dinheiro ao longo do tempo. Quem **empresta** dinheiro cobra juros; quem **investe** dinheiro recebe juros. Por isso os juros podem estar a seu favor (quando você guarda ou investe) ou contra você (quando você deve).

Existem dois jeitos principais de calcular:

- **Juros simples:** calculados sempre sobre o **valor inicial**. O valor dos juros é o mesmo em todo período.
- **Juros compostos:** calculados sobre o valor inicial **mais os juros já acumulados**. É o famoso "juros sobre juros": o valor cresce cada vez mais rápido.

Na vida real, a maioria dos produtos financeiros (investimentos e dívidas) usa juros compostos.

**[example] R$ 1.000 a 10% ao ano, por 3 anos** (order: 2)

Taxa fictícia, só para ilustrar.

| Ano | Juros simples | Juros compostos |
|---|---|---|
| Início | R$ 1.000 | R$ 1.000 |
| 1 | R$ 1.100 | R$ 1.100 |
| 2 | R$ 1.200 | R$ 1.210 |
| 3 | R$ 1.300 | R$ 1.331 |

Nos juros simples, são sempre R$ 100 por ano (10% de R$ 1.000). Nos compostos, o 10% do segundo ano incide sobre R$ 1.100, e o do terceiro sobre R$ 1.210. A diferença parece pequena em 3 anos, mas cresce muito com o passar do tempo.

**[tip] Sempre pergunte a taxa e o prazo** (order: 3)

Quando alguém falar em juros, pergunte: "essa taxa é por mês ou por ano? E por quanto tempo?". Uma taxa de 2% ao mês é muito diferente de 2% ao ano.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 4.1.1
question: O que são juros?
options:
A: Um valor que o banco dá de presente a quem tem conta
B: O preço pelo uso do dinheiro ao longo do tempo
C: Um imposto cobrado só de quem tem dívida
D: O valor mínimo que se paga em qualquer compra
correct_answer: B
feedback_correct: Exato! Juros são o preço do dinheiro no tempo: quem empresta cobra, e quem investe recebe.
feedback_incorrect: Não exatamente. Juros são o preço pelo uso do dinheiro ao longo do tempo. Quem empresta cobra juros; quem investe recebe juros.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 4.1.2
question: Qual alternativa descreve melhor os juros compostos?
options:
A: Juros calculados sempre só sobre o valor inicial
B: Juros que diminuem a cada período
C: Juros calculados sobre o valor inicial mais os juros já acumulados
D: Juros que só existem em dívidas
correct_answer: C
feedback_correct: Correto! Nos juros compostos, os juros de cada período incidem também sobre os juros anteriores, por isso o valor cresce cada vez mais rápido.
feedback_incorrect: Não foi dessa vez. Juros compostos são calculados sobre o valor inicial mais os juros já acumulados, o famoso "juros sobre juros". Calculados só sobre o valor inicial são os juros simples.

**Atividade 3 — multiple_choice (10 pts)**
competencia: 4.1.3
question: Você aplica R$ 1.000 a 10% ao ano, com juros compostos. Quanto terá ao final de 2 anos?
options:
A: R$ 1.100
B: R$ 1.200
C: R$ 1.210
D: R$ 1.331
correct_answer: C
feedback_correct: Correto! No primeiro ano, 1.000 vira 1.100. No segundo, os 10% incidem sobre 1.100 e o valor chega a R$ 1.210.
feedback_incorrect: Não foi dessa vez. Ano 1: 1.000 + 10% = R$ 1.100. Ano 2: 1.100 + 10% = R$ 1.210. R$ 1.200 seria o resultado com juros simples.

**Atividade 4 — open_text (0 pts)**
competencia: 4.1.1 e 4.1.2
question: Explique com as suas palavras por que os juros compostos podem ser ótimos para quem investe e ruins para quem está devendo.
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) que os juros compostos incidem sobre juros anteriores ("juros sobre juros"); (2) o efeito do tempo (o valor cresce cada vez mais rápido); (3) o contraste entre investir (valor cresce a seu favor) e dever (a dívida cresce contra você). Ausência de (1) ou (2) indica lacuna na competência 4.1.2; ausência de (3) indica lacuna na competência 4.1.1.

---

## Missão 4.2 — Parcelas não contam a história inteira

**number:** 2
**order:** 2
**Descrição:** O usuário calcula o custo total de compras parceladas e compara com o preço à vista.
**passing_score:** 70
**is_required:** true

### Competências
1. Calcular o custo total de uma compra parcelada (is_essential: true)
2. Comparar o preço à vista com o parcelado e identificar o custo do crédito (is_essential: true)
3. Reconhecer que uma parcela que cabe no orçamento não significa que a compra é vantajosa (is_essential: false)

### Conteúdo educacional

**[explanation] O valor da parcela não é o preço da compra** (order: 1)

Para saber quanto uma compra parcelada realmente custa:

**custo total = valor da parcela × número de parcelas**

Depois, compare com o **preço à vista**. A diferença entre os dois é o **custo do crédito**: o que você paga a mais por ter pago depois.

"Cabe no bolso" é só uma parte da análise. As perguntas mais importantes são: **qual é o valor total?** e **vale a pena pagar essa diferença?** Além disso, cada parcela compromete a renda dos meses seguintes, reduzindo o que sobra para essenciais, metas e imprevistos.

**[example] O celular da Ana** (order: 2)

Um celular custa **R$ 1.500 à vista** ou **10x de R$ 190**.

- Custo total parcelado: 10 × 190 = **R$ 1.900**
- Diferença: 1.900 − 1.500 = **R$ 400** a mais
- Em proporção: 400 ÷ 1.500 ≈ 26,7% a mais que o preço à vista.

A parcela de R$ 190 parece leve, mas a Ana pagaria R$ 400 a mais por parcelar.

**[tip] Duas perguntas antes de parcelar** (order: 3)

Pergunte sempre: "qual é o valor total?" e "tem desconto à vista?". Em financiamentos e empréstimos, peça também o **CET (Custo Efetivo Total)**, que reúne os juros e as tarifas em um só número e facilita a comparação.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 4.2.1
question: Um notebook é vendido em 12x de R$ 250. Qual é o custo total da compra?
options:
A: R$ 250
B: R$ 2.500
C: R$ 3.250
D: R$ 3.000
correct_answer: D
feedback_correct: Correto! 12 × 250 = R$ 3.000.
feedback_incorrect: Não foi dessa vez. O custo total é a parcela multiplicada pelo número de parcelas: 12 × 250 = R$ 3.000.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 4.2.2
question: O mesmo notebook custa R$ 2.400 à vista ou 12x de R$ 250. Quanto o parcelamento custa a mais?
options:
A: R$ 250
B: R$ 400
C: R$ 600
D: R$ 3.000
correct_answer: C
feedback_correct: Exato! O parcelado custa 12 × 250 = R$ 3.000, e o à vista custa R$ 2.400. A diferença é R$ 600, o custo do crédito.
feedback_incorrect: Não foi dessa vez. Calcule o total parcelado (12 × 250 = R$ 3.000) e subtraia o preço à vista (R$ 2.400): a diferença é R$ 600.

**Atividade 3 — multiple_choice (10 pts)**
competencia: 4.2.3
question: A Ana diz: "A parcela de R$ 190 cabe no meu orçamento, então a compra vale a pena." Qual é a melhor resposta?
options:
A: Está certa: se a parcela cabe no orçamento, a compra sempre vale a pena
B: Caber no orçamento é só uma parte: é preciso comparar o total pago com o preço à vista e ver se a parcela compromete os meses seguintes
C: Está errada: parcelar nunca compensa
D: Não importa o valor total, só o número de parcelas
correct_answer: B
feedback_correct: Muito bem! Caber no orçamento é necessário, mas não basta. É preciso olhar o custo total, a diferença para o preço à vista e o impacto nos meses seguintes.
feedback_incorrect: Não exatamente. Caber no orçamento é só parte da análise. É preciso comparar o custo total com o preço à vista e ver o impacto da parcela nos meses seguintes.

**Atividade 4 — open_text (0 pts)**
competencia: 4.2.1, 4.2.2 e 4.2.3
question: Você já viu uma oferta do tipo "parcela que cabe no bolso"? Como você avaliaria se ela compensa?
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) o cálculo do custo total (parcela vezes número de parcelas); (2) a comparação com o preço à vista; (3) o impacto da parcela nos meses seguintes ou no orçamento. Ausência de (1) indica lacuna na competência 4.2.1; ausência de (2) indica lacuna na competência 4.2.2; ausência de (3) indica lacuna na competência 4.2.3.

---

## Missão 4.3 — O que acontece quando a dívida cresce?

**number:** 3
**order:** 3
**Descrição:** O usuário entende como atraso e pagamento mínimo fazem a dívida crescer e escolhe estratégias para sair dela.
**passing_score:** 70
**is_required:** true

### Competências
1. Explicar como o atraso e o pagamento mínimo fazem uma dívida crescer (is_essential: true)
2. Reconhecer o teto legal para juros e encargos do rotativo e por que a dívida continua cara (is_essential: false)
3. Escolher uma estratégia para sair de uma dívida (is_essential: true)

### Conteúdo educacional

**[explanation] Atraso, pagamento mínimo e bola de neve** (order: 1)

Quando você **atrasa** uma conta, em geral paga multa e juros de atraso, e pode ter o nome negativado. Quando você paga **só o mínimo da fatura do cartão**, o restante é financiado com juros (no rotativo ou no parcelamento da fatura). Como os juros são compostos, a dívida cresce cada vez mais rápido.

Desde 2024, uma lei limita a soma de **juros e encargos** do rotativo e do parcelamento da fatura a **100% do valor original** da dívida. Ou seja, uma dívida de R$ 1.000 pode chegar, no máximo, a R$ 2.000 por efeito de juros e encargos. O teto protege, mas **dobrar a dívida continua sendo muito caro**.

Para sair de uma dívida:

1. **Liste** todas as dívidas, com valor e juros.
2. **Priorize** a dívida de juros mais altos.
3. **Negocie** com o credor, mostrando quanto você consegue pagar.
4. **Evite novas dívidas** enquanto estiver quitando as atuais.

**[example] A bola de neve** (order: 2)

Imagine uma dívida de R$ 1.000 com juros de 10% ao mês (taxa fictícia, só para ilustrar), sem nenhum pagamento:

- Mês 1: R$ 1.100
- Mês 2: R$ 1.210
- Mês 3: R$ 1.331

Em 3 meses, a dívida cresceu R$ 331 sem que nenhuma compra nova tivesse sido feita. Quanto mais tempo passa, mais rápido ela cresce.

**[tip] Negocie antes de atrasar** (order: 3)

Se você percebeu que não vai conseguir pagar, procure o credor **antes** do vencimento. Mostrar quanto você consegue pagar por mês costuma abrir mais opções de acordo do que esperar a dívida crescer.

### Atividades

**Atividade 1 — multiple_choice (10 pts)**
competencia: 4.3.1
question: O que acontece com o saldo restante quando você paga só o mínimo da fatura do cartão?
options:
A: É perdoado pelo banco
B: É financiado com juros, e a dívida continua crescendo
C: Fica congelado, sem custo, por um ano
D: É descontado automaticamente do seu salário
correct_answer: B
feedback_correct: Correto! O que não foi pago é financiado com juros, e a dívida continua crescendo enquanto não for quitada.
feedback_incorrect: Não exatamente. O saldo que sobra depois do pagamento mínimo é financiado com juros, e a dívida continua crescendo. Não há perdão nem congelamento sem custo.

**Atividade 2 — multiple_choice (10 pts)**
competencia: 4.3.2
question: Pela regra legal em vigor, até quanto a soma de juros e encargos do rotativo do cartão pode chegar, em relação ao valor original da dívida?
options:
A: 10%
B: 50%
C: Não há limite
D: 100%
correct_answer: D
feedback_correct: Correto! O teto é de 100% do valor original. Uma dívida de R$ 1.000 pode chegar a, no máximo, R$ 2.000 por efeito de juros e encargos. Mesmo assim, dobrar a dívida continua sendo muito caro.
feedback_incorrect: Não foi dessa vez. A lei limita juros e encargos do rotativo a 100% do valor original da dívida. O teto ajuda, mas ainda permite que a dívida dobre, o que é muito caro.

**Atividade 3 — multiple_choice (10 pts)**
competencia: 4.3.3
question: Você tem duas dívidas: R$ 400 no rotativo do cartão (com juros altos) e R$ 400 com um parente (sem juros). Este mês só dá para pagar R$ 400. Qual é a escolha mais eficiente?
options:
A: Pagar o parente primeiro, porque é mais educado
B: Dividir os R$ 400 igualmente entre as duas dívidas
C: Não pagar nenhuma e esperar o mês seguinte
D: Pagar a dívida do cartão primeiro e combinar um prazo com o parente
correct_answer: D
feedback_correct: Muito bem! A dívida com juros altos cresce mais rápido, então ela deve ser a prioridade. Combinar um prazo com o parente evita o desgaste e não gera juros.
feedback_incorrect: Revise a estratégia. A dívida com juros mais altos é a que mais cresce, então deve ser paga primeiro. A dívida sem juros pode ser negociada com mais calma.

**Atividade 4 — open_text (0 pts)**
competencia: 4.3.1 e 4.3.3
question: Imagine que um amigo está com a fatura do cartão atrasada. Que 3 conselhos você daria a ele para sair dessa situação?
feedback_static: Sua resposta foi registrada. O Mentor vai analisá-la e dar um retorno personalizado.
evaluation_criteria: O usuário deve mencionar ao menos: (1) procurar o credor para negociar; (2) priorizar a dívida de juros mais altos ou listar as dívidas; (3) evitar novas dívidas e/ou evitar pagar só o mínimo. Ausência de (1) ou (2) indica lacuna na competência 4.3.3; ausência de (3) indica lacuna na competência 4.3.1.

**Atividade 5 (simulação da Fase 4) — simulation (20 pts)**
competencia: 4.2.1, 4.2.2 e 4.3.3
scenario: Você precisa de R$ 2.000 para consertar o notebook que usa no trabalho. Três propostas fictícias de crédito chegaram. Proposta A: 10 parcelas de R$ 230. Proposta B: 12 parcelas de R$ 215. Proposta C: 5 parcelas de R$ 450. Depois das despesas essenciais e da sua meta, sua folga mensal é de R$ 400. Qual proposta você escolhe?
options:
A: Proposta C, porque tem o menor valor total (R$ 2.250)
B: Proposta A: o total (R$ 2.300) é o menor entre as que cabem na minha folga de R$ 400
C: Proposta B, porque tem a menor parcela (R$ 215)
D: Nenhuma delas; uso o rotativo do cartão, porque assim não preciso decidir agora
correct_choice: B
feedback_correct: Boa decisão! Os totais são: A = R$ 2.300, B = R$ 2.580 e C = R$ 2.250. A proposta C é a mais barata, mas a parcela de R$ 450 passa da sua folga de R$ 400 e levaria a atrasos. Entre as que cabem, a A é a que custa menos no total.
feedback_incorrect: Revise a comparação. Calcule o total de cada proposta (A: 10 × 230 = R$ 2.300; B: 12 × 215 = R$ 2.580; C: 5 × 450 = R$ 2.250) e verifique se a parcela cabe na folga de R$ 400. A C não cabe; entre A e B, a A custa menos no total. O rotativo do cartão costuma ser uma das dívidas mais caras.
