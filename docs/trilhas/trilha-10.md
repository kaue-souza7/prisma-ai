# Trilha 10 — Onde o dinheiro rende

**phase_number:** 10  
**Origem:** Fase 5, missões 5.2 e 5.3 → realocadas + expandidas  
**Seeds:** `trail_10_v1.py`  
**Data:** 2026-10-24

---

## 1. Objetivo geral e justificativa pedagógica

Antes de investir, é preciso entender as características básicas dos produtos
disponíveis: risco, liquidez, prazo e tributação. Esta trilha apresenta os
fundamentos da renda fixa, explica o FGC com precisão e desenvolve a capacidade
de comparar produtos pela rentabilidade líquida real.

---

## 2. Competências e resultados de aprendizagem

| Código | Competência | Essencial |
|---|---|:---:|
| 10.1.1 | Distinguir risco, liquidez e prazo em investimentos | sim |
| 10.1.2 | Classificar um investimento por perfil de risco | não |
| 10.2.1 | Descrever características de CDB, LCI, LCA, Tesouro Direto e poupança | sim |
| 10.2.2 | Identificar vantagens e desvantagens de cada produto | sim |
| 10.3.1 | Explicar o que o FGC cobre e o que não cobre | sim |
| 10.3.2 | Calcular a cobertura do FGC para um investimento específico | sim |
| 10.3.3 | Aplicar as regras de IOF e IR por prazo em renda fixa | sim |
| 10.4.1 | Calcular a rentabilidade líquida após IR e IOF | sim |
| 10.4.2 | Comparar dois produtos pelo rendimento real líquido | sim |

---

## 4. Mapa de conteúdo

### Missão 10.1 — Fundamentos (migrada da fase 5, missão 5.2 — expandida)

#### Conteúdo educacional
1. `[explanation]` Risco: o que é e por que existe no investimento
2. `[explanation]` Liquidez: facilidade de resgatar sem perda
3. `[explanation]` Prazo: impacto no rendimento e nos impostos
4. `[example]` Comparando a poupança com um CDB de 90 dias
5. `[tip]` A reserva de emergência precisa de alta liquidez acima de tudo
6. `[explanation]` Risco de crédito: o que acontece se a instituição quebrar?

#### Atividades
1. MC: O que é liquidez em um investimento? *(10.1.1)*
2. MC: Um CDB com carência de 1 ano tem maior ou menor liquidez do que a poupança? *(10.1.1)*
3. MC: Qual produto é mais adequado para a reserva de emergência: CDB diário ou CDB com carência de 2 anos? *(10.1.1)*
4. MC: O que é risco de crédito? *(10.1.2)*
5. Aberto: Explique com suas palavras a relação entre prazo, liquidez e rendimento. Por que investimentos de maior prazo tendem a render mais? *(10.1.1)*
6. MC: Liquidez diária significa que você pode resgatar quando quiser. Em qual situação isso é mais importante? *(10.1.1)*

---

### Missão 10.2 — Produtos de renda fixa *(nova)*

#### Competências: 10.2.1, 10.2.2

#### Conteúdo educacional
1. `[explanation]` Poupança: como funciona, regras de rendimento (Taxa Referencial)
2. `[explanation]` CDB: o que é, como funciona, variações (CDI, prefixado, IPCA+)
3. `[explanation]` LCI e LCA: isenção de IR para pessoa física, prazos mínimos
4. `[explanation]` Tesouro Direto: o que é, principais títulos (Selic, prefixado, IPCA+)
5. `[example]` Comparando 4 produtos para R$ 5.000 no prazo de 1 ano (valores hipotéticos)
6. `[tip]` Onde consultar as condições atuais de cada produto (instituição + Tesouro Nacional)

#### Atividades
1. MC: LCI tem qual vantagem tributária para pessoa física? *(10.2.1)*
2. MC: Tesouro Selic acompanha qual indicador? *(10.2.1)*
3. MC: Qual produto tem maior risco de crédito: CDB de grande banco ou CDB de financeira pequena? *(10.2.2)*
4. MC: Poupança tem isenção de IR. Um CDB de 105% do CDI paga IR. Com inflação alta, qual pode render mais no líquido? *(10.2.2)*
5. Aberto: Compare CDB e poupança para uma aplicação de R$ 3.000 no prazo de 1 ano, considerando liquidez e tributação *(10.2.1, 10.2.2)*
6. MC: LCI e LCA são isentas de IR. Isso significa que sempre rendem mais que CDB? *(10.2.2)*

---

### Missão 10.3 — FGC e tributação (migrada da fase 5, missão 5.3 — expandida)

**Importante:** O FGC é garantia de crédito (devolução do principal + rendimentos até o limite),
não garantia de rentabilidade. Não confundir os dois.

#### Conteúdo educacional
1. `[explanation]` O que é o FGC e quem está por trás dele
2. `[explanation]` O que o FGC cobre: produtos e limites (R$ 250 mil por CPF por IF, R$ 1 milhão no total)
3. `[explanation]` O que o FGC NÃO cobre: fundos de investimento, ações, LCI de alguns bancos (verificar)
4. `[example]` Carlos tem R$ 200.000 em CDB do banco A e R$ 100.000 no banco B. O que está coberto?
5. `[explanation]` IR sobre renda fixa: tabela regressiva de prazo
6. `[explanation]` IOF: incide nos primeiros 30 dias, tabela regressiva diária
7. `[example]` Cálculo do imposto em um CDB de 90 dias e de 360 dias

#### Atividades
1. MC: Qual é o limite de cobertura do FGC por CPF por instituição? *(10.3.1)*
2. MC: Fundo de ações tem garantia do FGC? *(10.3.1)*
3. MC: Carlos tem R$ 300.000 num único banco coberto pelo FGC. Quanto está protegido? *(10.3.2)*
4. MC: Qual é a alíquota de IR para renda fixa resgatada depois de 2 anos? *(10.3.3)*
5. MC: Se você resgata um CDB no 15º dia, paga IOF? *(10.3.3)*
6. Aberto: Explique a diferença entre garantia do FGC e garantia de rentabilidade. Por que elas são conceitos distintos? *(10.3.1)*

---

### Missão 10.4 — Comparando produtos *(nova)*

#### Competências: 10.4.1, 10.4.2

#### Conteúdo educacional
1. `[explanation]` Como calcular o rendimento líquido (após IR): fórmula
2. `[example]` CDB 12% ao ano vs. LCI 10% ao ano por 1 ano: qual rende mais no líquido?
3. `[explanation]` Comparando rentabilidade real (após inflação e IR)
4. `[tip]` Simuladores dos bancos e do Tesouro Direto: como usar

#### Atividades
1. MC: CDB rende 13%/ano, IR de 15%. Qual é o rendimento líquido? *(10.4.1)*
2. MC: LCI rende 11%/ano (isenta de IR). CDB rende 13%/ano (IR 15%). Qual rende mais no líquido? *(10.4.2)*
3. Simulação: compare 3 produtos hipotéticos para uma aplicação de R$ 5.000 por 1 ano *(10.4.1, 10.4.2)*
4. Aberto: Explique a diferença entre rendimento bruto e rendimento líquido e por que você deve sempre comparar pelo líquido *(10.4.1)*

---

## 5. Referências e fontes

| Tema | Fonte | Data de consulta |
|---|---|---|
| FGC — limites e cobertura | FGC — fgc.org.br | 2026-10-24 |
| IR renda fixa — tabela regressiva | RIR/2018 + Lei 11.033/2004 | 2026-10-24 |
| IOF — tabela regressiva | Decreto 6.306/2007 | 2026-10-24 |
| Tesouro Direto | tesouredireto.com.br | 2026-10-24 |

> **Atenção:** Os limites do FGC, as taxas Selic e CDI mudam. Não apresente
> valores específicos como atuais sem data e fonte explícita. Use valores
> hipotéticos nos exemplos pedagógicos.

---

## 6. Decisões editoriais

| Decisão | Justificativa |
|---|---|
| Não recomendar produtos específicos de instituições | Educação financeira ≠ consultoria de investimentos |
| Apresentar o FGC com limitações explícitas | Precisão informacional; muitos materiais tratam FGC como garantia universal |
| Rendimento real = comparar com inflação | Conexão direta com trilha 9 |

---

## 7. Relações com outras trilhas

- **Trilha 9**: a inflação da trilha 9 é necessária para calcular rendimento real aqui.
- **Trilha 5 e 6**: onde guardar a reserva de emergência (liquidez diária, CDB ou poupança).
