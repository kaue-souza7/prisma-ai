# Trilha 9 — Inflação e poder de compra

**phase_number:** 9  
**Origem:** Fase 5, missão 5.1 → realocada + expandida  
**Seeds:** `trail_9_v1.py`  
**Data:** 2026-10-24

---

## 1. Objetivo geral e justificativa pedagógica

A inflação corrói o poder de compra silenciosamente. Esta trilha desenvolve a
capacidade de entender o que é o IPCA, calcular o impacto real da inflação no
orçamento e distinguir rendimento nominal de rendimento real.

---

## 2. Competências e resultados de aprendizagem

| Código | Competência | Essencial |
|---|---|:---:|
| 9.1.1 | Explicar o que é inflação e como o IPCA mede | sim |
| 9.1.2 | Calcular o reajuste de um preço pela inflação acumulada | sim |
| 9.1.3 | Distinguir inflação oficial (IPCA) e inflação percebida | não |
| 9.2.1 | Calcular rendimento real usando a fórmula de Fisher | sim |
| 9.2.2 | Identificar quando um rendimento nominal está acima ou abaixo da inflação | sim |
| 9.3.1 | Aplicar o impacto da inflação a contratos e reajustes | sim |
| 9.3.2 | Comparar poder de compra de dois momentos no tempo | sim |

---

## 4. Mapa de conteúdo

### Missão 9.1 — O que é inflação? (migrada da fase 5, missão 5.1 — expandida)

#### Conteúdo educacional
1. `[explanation]` O que é inflação e por que preços sobem
2. `[explanation]` O IPCA: o que mede, quem calcula (IBGE) e como é divulgado
3. `[example]` Cesta de compras da Ana: quanto custava e quanto custa agora (fictício, inflação hipotética)
4. `[explanation]` Inflação percebida: por que parece mais alta do que o índice
5. `[tip]` Como consultar o IPCA acumulado no site do IBGE
6. `[example]` Dois perfis com inflações diferentes: família com criança vs. aposentado
7. `[explanation]` Deflação: quando os preços caem (conceito breve)
8. `[explanation]` INPC vs. IPCA: diferença de público e uso

#### Atividades
1. MC: O IPCA é calculado por qual instituição? *(9.1.1)*
2. MC: Um produto custava R$ 50 há 1 ano. Com inflação de 6% no período, quanto custa hoje? *(9.1.2)*
3. MC: Qual é a diferença entre inflação oficial e inflação percebida? *(9.1.3)*
4. MC: Por que a inflação de uma família pode ser diferente do IPCA oficial? *(9.1.3)*
5. MC: Se o IPCA acumulado no ano foi 5%, um produto de R$ 100 em janeiro deve custar quanto em dezembro? *(9.1.2)*
6. Aberto: Descreva o que é inflação usando um exemplo de produto do dia a dia e explique por que o IPCA pode não refletir a inflação que você sente *(9.1.1, 9.1.3)*

---

### Missão 9.2 — Rendimento real *(nova)*

#### Competências: 9.2.1, 9.2.2

#### Conteúdo educacional
1. `[explanation]` Rendimento nominal vs. rendimento real: a diferença
2. `[explanation]` A fórmula de Fisher: (1 + r_real) = (1 + r_nominal) / (1 + inflação)
3. `[example]` Poupança rende 6% ao ano, inflação é 5%. Qual é o ganho real? (valores hipotéticos)
4. `[example]` Investimento rende 8%, inflação é 9%. Você ganhou ou perdeu?
5. `[tip]` Quando o rendimento nominal "ganhou da inflação" — como verificar
6. `[explanation]` Rendimento real negativo: quando guardar dinheiro empobrece

#### Atividades
1. MC: Rendimento nominal de 7% ao ano e inflação de 4%. Qual é o rendimento real aproximado? *(9.2.1)*
2. MC: Aplicação que rende 6%/ano com inflação de 7%. O investidor ganhou ou perdeu poder de compra? *(9.2.2)*
3. MC: Usando a fórmula exata de Fisher: (1+0,08)/(1+0,05) − 1 = ? *(9.2.1)*
4. MC: O que significa rentabilidade real negativa? *(9.2.2)*
5. Aberto: Uma poupança rende 6% ao ano em um período com inflação de 5%. Calcule o rendimento real e explique o que significa para o poder de compra *(9.2.1, 9.2.2)*
6. MC: Carlos deixou R$ 10.000 numa aplicação que rendeu 3% no ano, mas a inflação foi 6%. Quanto perdeu em poder de compra (aproximado)? *(9.2.2)*

---

### Missão 9.3 — Inflação e decisões *(nova)*

#### Competências: 9.3.1, 9.3.2

#### Conteúdo educacional
1. `[explanation]` Como a inflação afeta contratos de aluguel e serviços
2. `[example]` Reajuste do aluguel: IGP-M acumulado 10% em um aluguel de R$ 1.200 (fictício)
3. `[explanation]` Comparar poder de compra de dois momentos: tabela e cálculo
4. `[tip]` Por que guardar dinheiro "no colchão" é perder dinheiro

#### Atividades
1. MC: O aluguel da Ana é de R$ 1.200 e será reajustado em 8% pelo contrato. Qual é o novo valor? *(9.3.1)*
2. MC: R$ 10.000 guardados há 3 anos com inflação média de 5%/ano têm poder de compra equivalente a quanto hoje? *(9.3.2)*
3. MC: Qual a desvantagem de manter dinheiro em conta corrente sem rendimento num período de inflação? *(9.3.2)*
4. Aberto: Explique por que poupar em uma aplicação que rende abaixo da inflação pode ser pior do que parece à primeira vista *(9.2.2, 9.3.2)*

---

## 5. Referências e fontes

| Tema | Fonte | Data de consulta |
|---|---|---|
| IPCA — metodologia | IBGE — Índice Nacional de Preços ao Consumidor Amplo | 2026-10-24 |
| Fórmula de Fisher | Conceito padrão de matemática financeira | 2026-10-24 |
| INPC vs. IPCA | IBGE | 2026-10-24 |

> **Atenção:** Os valores do IPCA mudam mensalmente. Não inclua valores
> específicos de inflação como se fossem dados atuais. Use sempre valores
> fictícios ou peça ao usuário que consulte o IBGE.

---

## 7. Relações com outras trilhas

- **Trilha 7**: os juros compostos desta trilha são usados no cálculo do rendimento real.
- **Trilha 10**: a inflação é o parâmetro para avaliar se um investimento rende de verdade.
