# Trilha 1 — Meu primeiro salário

**phase_number:** 1 (mantido da estrutura anterior)  
**Versão do conteúdo:** v2 (expansão sobre phase_1_v1, missão 1.1)  
**Seeds:** `trail_1_v2.py` (expansão da missão 1.1 + missões 1.2 e 1.3 novas)  
**Data:** 2026-10-24

---

## 1. Objetivo geral e justificativa pedagógica

O trabalhador brasileiro, especialmente em primeiro emprego, frequentemente não
sabe distinguir salário bruto de líquido, não reconhece os descontos do
contracheque e não tem base para planejar o orçamento sobre a renda real.

Esta trilha corrige esse déficit de forma imediata e prática: o estudante aprende
a ler um contracheque fictício, a calcular o líquido, a entender o 13º e as
férias, e a conferir se os valores estão corretos.

---

## 2. Público-alvo e pré-requisitos

- Pessoas em primeiro emprego formal ou prestes a ingressar no mercado.
- Sem pré-requisito de conhecimento financeiro.
- Pré-requisito de sistema: nenhum (é a primeira trilha da jornada).

---

## 3. Competências e resultados de aprendizagem

| Código | Competência | Essencial |
|---|---|:---:|
| 1.1.1 | Distinguir salário bruto de salário líquido | sim |
| 1.1.2 | Identificar os descontos do contracheque e o que não é descontado | não |
| 1.1.3 | Calcular o salário líquido a partir de um contracheque fictício | sim |
| 1.2.1 | Interpretar cada linha do contracheque com função e origem | sim |
| 1.2.2 | Calcular o desconto de INSS progressivo por faixas | sim |
| 1.2.3 | Reconhecer benefícios que não reduzem o salário (FGTS, ticket-alimentação pago pelo empregador) | não |
| 1.3.1 | Calcular o 13º salário bruto e estimar o líquido | sim |
| 1.3.2 | Calcular as férias com adicional constitucional de 1/3 | sim |
| 1.3.3 | Diferenciar valores brutos e líquidos em 13º e férias | não |

---

## 4. Mapa de conteúdo

### Missão 1.1 — De onde vem o dinheiro? (existente, expandida)

**Expansão:** 3 MC + 1 aberto → 6 MC + 2 abertos + 8 leituras

#### Subtemas
- Salário bruto: o que é, por que é diferente do combinado
- Descontos obrigatórios: INSS, IRRF (com isenção vigente), vale-transporte
- FGTS: o que é, quem paga, onde fica
- Cálculo do salário líquido: fórmula e prática

#### Conteúdo educacional (content_items)
1. `[explanation]` O que é salário bruto e líquido
2. `[explanation]` Os principais descontos do contracheque
3. `[example]` O contracheque da Ana (fictício, R$ 2.000 bruto)
4. `[tip]` Confira o seu contracheque todo mês
5. `[explanation]` O que é o FGTS e por que aparece no contracheque *(novo)*
6. `[example]` Contracheque com benefícios adicionais — ticket e PLR *(novo)*
7. `[tip]` Como perguntar sobre o seu contracheque sem constrangimento *(novo)*
8. `[explanation]` Por que o IRRF pode ser R$ 0,00 no seu primeiro salário *(novo)*

#### Atividades
1. MC: O que é salário bruto? (existente, competência 1.1.1)
2. MC: Qual item NÃO é descontado? FGTS (existente, competência 1.1.2)
3. MC: Calcule o líquido — R$ 2.000 bruto (existente, competência 1.1.3)
4. Aberto: Explique a diferença bruto/líquido para um amigo (existente)
5. MC: Ana recebe ticket-alimentação de R$ 300 pago pela empresa. O ticket sai do salário dela? *(novo, 1.1.2)*
6. MC: Por que o IRRF foi R$ 0,00 no contracheque da Ana? *(novo, 1.1.1)*
7. MC: Calcule o INSS por faixas — salário R$ 3.000 *(novo, 1.1.3)*
8. Aberto: Leia o contracheque fictício do Carlos e explique o que cada linha significa *(novo)*

---

### Missão 1.2 — Holerite linha a linha *(nova)*

**Foco:** leitura detalhada de contracheque, INSS progressivo, benefícios e adiantamentos.

#### Competências: 1.2.1, 1.2.2, 1.2.3

#### Conteúdo educacional
1. `[explanation]` O que é um holerite e como lê-lo
2. `[explanation]` Tabela INSS 2026: faixas e alíquotas
3. `[example]` Cálculo do INSS por faixas — passo a passo (salário R$ 2.800)
4. `[explanation]` Adiantamento salarial: o que é e como aparece no holerite
5. `[explanation]` PLR — participação nos lucros: breve introdução
6. `[example]` Contracheque completo com adiantamento e PLR (fictício)
7. `[tip]` Como guardar o histórico dos contracheques
8. `[explanation]` Benefícios que o empregador paga sem descontar do salário

#### Atividades
1. MC: Em qual faixa salarial fica um salário de R$ 2.800? *(1.2.2)*
2. MC: Qual é o INSS de quem ganha R$ 2.000? *(1.2.2)*
3. MC: O adiantamento de R$ 500 recebido no dia 15 aparece como crédito ou desconto no holerite do dia 30? *(1.2.1)*
4. MC: O que é a PLR no contracheque? *(1.2.1)*
5. Aberto: Calcule o INSS do Carlos com salário bruto de R$ 3.500 usando as faixas de 2026 *(1.2.2)*
6. MC: Qual informação NÃO costuma aparecer em um contracheque? *(1.2.3)*

---

### Missão 1.3 — 13º salário e férias *(nova)*

**Foco:** direitos trabalhistas, cálculo do 13º, férias, adicional de 1/3, bruto vs. líquido.

#### Competências: 1.3.1, 1.3.2, 1.3.3

#### Conteúdo educacional
1. `[explanation]` O que é o 13º salário e quando é pago
2. `[explanation]` Como calcular o 13º bruto (proporcional ao tempo de serviço)
3. `[example]` 13º da Ana: admitida em março, 10 meses de serviço (fictício)
4. `[explanation]` O que são as férias e o adicional constitucional de 1/3
5. `[example]` Férias do Carlos: cálculo bruto e estimativa do líquido (fictício)
6. `[explanation]` Por que o 13º e as férias têm INSS e IRRF calculados separadamente
7. `[tip]` Como planejar os meses em que o 13º cai na conta
8. `[tip]` Férias e 13º não são bônus: são salário diferido — planeje antes

#### Atividades
1. MC: Se o salário bruto é R$ 2.400 e o trabalhador trabalhou 12 meses, qual é o 13º bruto integral? *(1.3.1)*
2. MC: Uma trabalhadora admitida em julho tem direito a quanto de 13º neste ano? *(1.3.1)*
3. MC: O adicional de férias é de quanto sobre o salário de férias? *(1.3.2)*
4. MC: Qual é o valor bruto de férias + adicional para quem ganha R$ 1.800? *(1.3.2)*
5. Aberto: O Pedro vai receber férias + adicional. Estime o valor bruto e explique por que o líquido será menor. *(1.3.1, 1.3.3)*
6. MC: Por que o IRRF sobre o 13º pode ser diferente do IRRF do salário mensal? *(1.3.3)*

---

## 5. Referências e fontes

| Tema | Fonte | Data de consulta | Vigência |
|---|---|---|---|
| Tabela INSS progressiva 2026 | Portaria MPS — publicada Diário Oficial | 2026-10-24 | Jan 2026 |
| IRRF — isenção até R$ 5.000 | Lei 14.848/2024 | 2026-10-24 | Jan 2026 |
| FGTS — 8% sobre salário | Lei 8.036/1990, art. 15 | 2026-10-24 | Vigente |
| Adicional de férias 1/3 | CF/88, art. 7º, XVII | 2026-10-24 | Vigente |
| 13º salário | Lei 4.090/1962 | 2026-10-24 | Vigente |

> **Atenção:** As faixas e alíquotas da tabela INSS e o limite de isenção do IRRF
> são atualizados anualmente. Antes de publicar qualquer atualização do conteúdo,
> consulte o Diário Oficial e a Receita Federal para verificar os valores vigentes.

### Faixas INSS 2026 (referência para os seeds)

| Faixa salarial | Alíquota |
|---|---|
| Até R$ 1.518,00 | 7,5% |
| De R$ 1.518,01 a R$ 2.793,88 | 9% |
| De R$ 2.793,89 a R$ 4.190,83 | 12% |
| De R$ 4.190,84 a R$ 8.157,41 | 14% |

> Fonte: Portaria MPS de 2026. **Verificar vigência antes de publicar.**
> Os valores acima são referência para os exemplos didáticos. Cada faixa incide
> apenas sobre a parcela do salário dentro daquela faixa (sistema progressivo,
> semelhante ao IR).

---

## 6. Lacunas identificadas e status

| Lacuna | Status |
|---|---|
| Exemplos com salário mínimo 2026 | Pendente: verificar valor vigente antes de publicar |
| Cálculo de IRRF para salários acima de R$ 5.000 | Registrado — fora do foco da trilha (primeiro emprego); pode ser mencionado como nota |
| Holerite de trabalhador doméstico (Simples Doméstico) | Fora do escopo desta trilha |

---

## 7. Decisões editoriais

| Decisão | Justificativa |
|---|---|
| Usar salários fictícios próximos ao salário mínimo (R$ 1.800–R$ 3.500) | Representativo do público-alvo |
| Não detalhar cálculo do IRRF progressivo para salários altos | Fora do contexto de primeiro emprego; mencionar que existe sem desenvolver |
| Apresentar FGTS como benefício, não como desconto | Pedagogicamente correto e documentalmente preciso |
| Adicional de férias: usar termo "1/3 constitucional" | Alinha com a legislação (CF/88, art. 7º, XVII) |

---

## 8. Relações com outras trilhas

- **Trilha 2** usa o salário líquido calculado aqui como base do orçamento
- **Trilha 5** retoma o 13º como oportunidade para a reserva de emergência
- **Trilha 7** retoma o contracheque para comparar custo real do crédito com o salário líquido
