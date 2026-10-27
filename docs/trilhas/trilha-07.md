# Trilha 7 — Juros e parcelas

**phase_number:** 7  
**Origem:** Fase 4, missões 4.1 e 4.2 → realocadas + expandidas  
**Seeds:** `trail_7_v1.py`  
**Data:** 2026-10-24

---

## 1. Objetivo geral e justificativa pedagógica

O crédito é uma ferramenta poderosa quando usada com conhecimento e perigosa
quando usada sem. Esta trilha desenvolve a capacidade de calcular o custo real
de qualquer operação de crédito, interpretar o CET e avaliar se o "parcelamento
sem juros" realmente não tem custo.

---

## 2. Competências e resultados de aprendizagem

| Código | Competência | Essencial |
|---|---|:---:|
| 7.1.1 | Calcular juros simples sobre um capital por um período | sim |
| 7.1.2 | Distinguir juros simples de juros compostos | sim |
| 7.1.3 | Calcular juros compostos com a fórmula M = C(1+i)^n | sim |
| 7.2.1 | Calcular o custo total de um parcelamento | sim |
| 7.2.2 | Interpretar o CET (Custo Efetivo Total) de uma oferta | sim |
| 7.2.3 | Comparar preço à vista e parcelado considerando o CET | sim |
| 7.3.1 | Analisar uma oferta de parcelamento sem juros com senso crítico | sim |
| 7.3.2 | Identificar diferenças de preço entre à vista e parcelado | sim |
| 7.3.3 | Avaliar o comprometimento futuro de renda em parcelamentos sem juros | sim |
| 7.4.1 | Comparar duas ofertas de crédito pelo custo total | sim |
| 7.4.2 | Tomar decisão de crédito baseada em custo total e capacidade de pagamento | sim |

---

## 4. Mapa de conteúdo

### Missão 7.1 — Juros simples e compostos (migrada da fase 4, missão 4.1 — expandida)

#### Conteúdo educacional
1. `[explanation]` O que são juros e por que existem
2. `[explanation]` Juros simples: fórmula J = C × i × n
3. `[example]` Empréstimo de R$ 1.000 a 5% ao mês por 3 meses — juros simples
4. `[explanation]` Juros compostos: "juros sobre juros", fórmula M = C(1+i)^n
5. `[example]` Os mesmos R$ 1.000 com juros compostos: quanto a diferença importa?
6. `[tip]` O tempo é o maior aliado ou inimigo: quanto antes você paga, menos você paga
7. `[explanation]` Por que a maioria dos créditos usa juros compostos (não simples)
8. `[example]` Comparação visual: R$ 1.000 a 5%/mês em 1, 3, 6 e 12 meses (simples vs. compostos)

#### Atividades
1. MC: Qual é o juro simples de R$ 500 a 3%/mês por 4 meses? *(7.1.1)*
2. MC: Qual é a diferença entre juros simples e compostos? *(7.1.2)*
3. MC: M = 1.000 × (1,05)^3. Qual é o montante? *(7.1.3)*
4. MC: Depois de 12 meses, R$ 1.000 a 5% compostos ao mês resulta em quanto? *(7.1.3)*
5. Aberto: Explique com suas palavras por que os juros compostos crescem mais rápido e o que isso significa para uma dívida não paga *(7.1.2, 7.1.3)*
6. MC: Uma dívida de R$ 800 acumulou R$ 120 de juros em 3 meses. Qual a taxa mensal (simples)? *(7.1.1)*
7. MC: Por que é importante pagar uma dívida com juros compostos o mais cedo possível? *(7.1.3)*
8. Aberto: Calcule e compare uma dívida de R$ 1.000 a 8%/mês em 6 meses com juros simples e com juros compostos *(7.1.1, 7.1.3)*

---

### Missão 7.2 — Parcelamento e CET (migrada da fase 4, missão 4.2 — expandida)

#### Conteúdo educacional
1. `[explanation]` O que é o CET e onde encontrá-lo
2. `[explanation]` Como calcular o custo total de um parcelamento
3. `[example]` Notebook de R$ 3.000: à vista vs. 12× de R$ 290
4. `[explanation]` O que entra no CET além dos juros nominais
5. `[tip]` Sempre peça o CET antes de assinar qualquer contrato de crédito
6. `[explanation]` Tarifa de abertura de crédito, seguro e outros custos embutidos

#### Atividades
1. MC: Um empréstimo de R$ 2.000 parcelado em 10× de R$ 240. Qual é o custo total? *(7.2.1)*
2. MC: O que é o CET? *(7.2.2)*
3. MC: Produto à vista R$ 1.200 ou 6× de R$ 230. Qual custa mais? *(7.2.3)*
4. MC: Dois bancos oferecem R$ 5.000: banco A a 3%/mês, banco B com CET de 45% ao ano. Qual é mais barato? *(7.2.2)*
5. Aberto: Compare duas ofertas de financiamento para o mesmo produto: calcule e explique qual você escolheria e por quê *(7.2.2, 7.2.3)*
6. MC: Qual dos itens abaixo NÃO costuma entrar no cálculo do CET? *(7.2.2)*

---

### Missão 7.3 — "Sem juros" existe? *(nova)*

**Importante:** Esta missão não afirma que todo parcelamento sem juros tem custo zero
nem que sempre há custo. Explica o que pode e não pode ser concluído sem mais informações.

#### Competências: 7.3.1, 7.3.2, 7.3.3

#### Conteúdo educacional
1. `[explanation]` O que significa "parcelamento sem juros" na prática
2. `[explanation]` Desconto à vista vs. preço parcelado sem juros: quando há diferença
3. `[example]` Loja A: R$ 900 à vista ou 6× de R$ 150. Loja B: R$ 1.000 à vista ou 6× de R$ 150. O que é diferente? (fictício)
4. `[explanation]` Comprometimento futuro de renda: parcelar "sem juros" não significa gratuito no orçamento
5. `[tip]` Perguntas a fazer antes de parcelar sem juros
6. `[explanation]` Quando o parcelamento sem juros pode fazer sentido (e quando não faz)

#### Atividades
1. MC: Uma loja oferece um produto por R$ 600 à vista ou 6× de R$ 100 "sem juros". Há alguma diferença de custo financeiro direto? *(7.3.1)*
2. MC: Loja A cobra R$ 800 à vista e R$ 1.000 parcelado. Loja B cobra o mesmo preço nas duas formas. Em qual situação o "sem juros" tem custo implícito? *(7.3.2)*
3. MC: Parcelar uma compra em 12× sem juros compromete sua renda por quanto tempo? *(7.3.3)*
4. MC: Carlos quer comprar uma televisão de R$ 1.800 em 12× sem juros. Cada parcela é R$ 150. O que ele deve considerar antes de fechar? *(7.3.3)*
5. Aberto: Analise a seguinte oferta fictícia: "R$ 1.200 à vista ou 10× de R$ 130 sem juros". O que você concluiria sobre o custo real da compra e o impacto no orçamento? *(7.3.1, 7.3.2, 7.3.3)*
6. MC: Em qual situação parcelar sem juros faz mais sentido do que pagar à vista? *(7.3.1)*

---

### Missão 7.4 — Comparando ofertas *(nova)*

#### Competências: 7.4.1, 7.4.2

#### Conteúdo educacional
1. `[explanation]` Como comparar duas ofertas de crédito: passo a passo
2. `[example]` Carlos compara 3 opções de crédito pessoal para o mesmo valor
3. `[tip]` Além do custo, considere o prazo e o impacto mensal no orçamento
4. `[explanation]` Quando não contratar crédito é a melhor decisão

#### Atividades
1. MC: Oferta 1: R$ 3.000 em 12× de R$ 295. Oferta 2: R$ 3.000 em 24× de R$ 160. Qual tem maior custo total? *(7.4.1)*
2. MC: O custo total de dois empréstimos é igual, mas um tem parcela menor. Qual deles compromete menos o orçamento mensal? *(7.4.2)*
3. Simulação: você precisa de R$ 5.000 e tem 3 ofertas. Calcule o custo total e escolha a melhor para o seu orçamento *(7.4.1, 7.4.2)*
4. Aberto: Quando a decisão correta é recusar todas as ofertas de crédito disponíveis? Descreva uma situação *(7.4.2)*

---

## 5. Referências e fontes

| Tema | Fonte | Data de consulta |
|---|---|---|
| CET — definição e componentes | Resolução CMN nº 3.517/2007 | 2026-10-24 |
| Juros compostos — conceito | Matemática financeira — padrão acadêmico | 2026-10-24 |

> **Atenção:** As taxas usadas nos exemplos são fictícias e didáticas. Identificar
> claramente nos seeds que se trata de valores hipotéticos.

---

## 6. Decisões editoriais

| Decisão | Justificativa |
|---|---|
| Missão 7.3 não afirma que "parcelamento sem juros tem custo" como verdade universal | Correto: depende se há diferença de preço à vista. A missão ensina a verificar, não a concluir sem dados. |
| Juros compostos com fórmula explícita | Nível de competência adequado para aplicação prática; simplificação pedagógica identificada como tal |

---

## 7. Relações com outras trilhas

- **Trilha 4**: cartão de crédito introduzido lá; CET desenvolvido aqui.
- **Trilha 8**: o crescimento de dívidas usa os juros compostos desta trilha.
- **Trilha 10**: a rentabilidade de investimentos usa o mesmo raciocínio de juros compostos.
