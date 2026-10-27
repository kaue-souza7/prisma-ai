# Contrato Curricular — 12 Trilhas de Aprendizagem

**Status:** Aprovado — contrato de referência para implementação  
**Versão:** 1.0  
**Data:** 2026-10-24  
**Substitui:** estrutura de 6 fases descrita no PRD e em `Conteudo_e_Jornada_de_Aprendizagem.md`

> Este documento é a fonte de verdade pedagógica para a reorganização curricular.
> A correspondência entre fases antigas e trilhas novas é rastreável e explícita.
> Os identificadores técnicos das tabelas `phases`, `missions` e `competencies`
> são preservados quando possível; novos registros recebem novos identificadores.

---

## 1. Decisões arquiteturais registradas

| ID | Decisão |
|---|---|
| D-T1 | A tabela `phases` é expandida de 6 para 12 registros. Cada trilha nova corresponde a uma fase nova no banco. |
| D-T2 | As 19 missões existentes (incluindo o desafio integrador da Fase 6) são redistribuídas: cada missão mantém seu `phase_id`, `number` e `competency_codes` históricos. As trilhas que agregam múltiplas fases antigas recebem novas missões com códigos novos. |
| D-T3 | O Catalisador (`catalyst.py`) passa a trabalhar com `DEFAULT_PHASE_ORDER = [1..12]`. As regras de trilha personalizadas são atualizadas para 12 elementos. |
| D-T4 | O frontend exibe "trilha" em vez de "fase" no rótulo de navegação. O campo `phase.number` continua sendo o identificador técnico. |
| D-T5 | Os `competency_codes` das novas missões seguem o padrão `trilha.missão.competência` (ex.: `7.1.1` para trilha 7, missão 1, competência 1). |
| D-T6 | Seeds existentes (`phase_1_v1.py` … `phase_6_v1.py`) são imutáveis. A expansão cria seeds `trail_7_v1.py` … `trail_12_v1.py` para as trilhas novas e versões `_v2` para as expansões das trilhas 1–6. |
| D-T7 | A migration `0015_twelve_trails.py` insere as 6 fases novas (trilhas 7–12), realoca as missões das fases 1–6 para as trilhas correspondentes e semeia o conteúdo expandido. |
| D-T8 | Progresso de usuários existentes é preservado: `user_mission_progress` e `user_competency_progress` não são alterados retroativamente. |
| D-T9 | O Desafio integrador (trilha 12) usa apenas `simulation` como tipo de atividade, com cenários de decisão multietapa. |

---

## 2. Mapa de correspondência entre fases antigas e trilhas novas

| Trilha nova | Nome | Fases/módulos de origem | Fase no banco |
|---:|---|---|---:|
| 1 | Meu primeiro salário | Fase 1, missão 1.1 | **1** (mantida) |
| 2 | Orçamento na prática | Fase 1, missões 1.2 e 1.3 | **2** (nova, recebe missões da fase 1) |
| 3 | Pagamentos do dia a dia | Fase 2, missões 2.1 e 2.3 | **3** (mantida, = fase 2 antiga) |
| 4 | Cartão e fatura | Fase 2, missão 2.2 | **4** (nova, recebe missão 2.2) |
| 5 | Metas e reserva | Fase 3, missões 3.1 e 3.3 | **5** (nova, = fase 3 antiga expandida) |
| 6 | Guardar sem perder o controle | Fase 3, missão 3.2 | **6** (nova, recebe missão 3.2) |
| 7 | Juros e parcelas | Fase 4, missões 4.1 e 4.2 | **7** (nova, = fase 4 antiga expandida) |
| 8 | Dívida que cresce | Fase 4, missão 4.3 | **8** (nova, recebe missão 4.3) |
| 9 | Inflação e poder de compra | Fase 5, missão 5.1 | **9** (nova, = fase 5 antiga) |
| 10 | Onde o dinheiro rende | Fase 5, missões 5.2 e 5.3 | **10** (nova, recebe missões 5.2 e 5.3) |
| 11 | Golpes e proteção de dados | Fase 6, missões 6.1, 6.2 e 6.3 | **11** (nova, = fase 6 antiga expandida) |
| 12 | Desafio integrador | Fase 6, missão 6.4 | **12** (nova, recebe missão 6.4) |

> **Nota de implementação:** As fases antigas 2–6 recebem novos `number` (3–11)
> correspondentes à nova numeração de trilhas. As missões são atualizadas para
> apontar para o novo `phase_id`. A fase 1 mantém o `number = 1`.

---

## 3. Metas quantitativas por trilha

Metodologia: soma dos volumes de referência dos módulos de origem × 2.

| Trilha | Módulos de origem | MC (meta) | Abertos (meta) | Simulações (meta) | Leituras (meta) | Steps (meta) |
|---:|---|---:|---:|---:|---:|---:|
| 1 | 1.1 | 6 | 2 | 0 | 8 | 18 |
| 2 | 1.2 + 1.3 | 10 | 4 | 2 | 12 | 32 |
| 3 | 2.1 + 2.3 | 12 | 4 | 2 | 12 | 34 |
| 4 | 2.2 | 6 | 2 | 0 | 6 | 16 |
| 5 | 3.1 + 3.3 | 12 | 4 | 2 | 12 | 34 |
| 6 | 3.2 | 6 | 2 | 0 | 6 | 16 |
| 7 | 4.1 + 4.2 | 12 | 4 | 0 | 12 | 32 |
| 8 | 4.3 | 6 | 2 | 2 | 6 | 18 |
| 9 | 5.1 | 6 | 2 | 0 | 6 | 16 |
| 10 | 5.2 + 5.3 | 12 | 4 | 2 | 12 | 34 |
| 11 | 6.1 + 6.2 + 6.3 | 18 | 6 | 2 | 18 | 50 |
| 12 | 6.4 (Desafio integrador) | 0 | 0 | 8 | 0 | 12 |
| **Total** | | **106** | **36** | **20** | **110** | **312** |

> **Notas:**
> - Trilha 12 tem meta de simulações maior (8 vs. 4×2=8) por ser o Desafio integrador.
> - Steps = soma estimada de etapas de conteúdo + atividade no lesson_flow de cada missão.
> - A meta de leituras corresponde ao número de `content_items` distintos.
> - As metas são mínimos de planejamento, não autorizações para conteúdo repetitivo.

---

## 4. Estrutura de módulos por trilha

### Trilha 1 — Meu primeiro salário (phase_number: 1)

**Objetivo:** Compreender a remuneração, ler e conferir um contracheque e calcular o salário líquido.

| Missão | Nome | Conteúdo central | Tipo principal |
|---|---|---|---|
| 1.1 | De onde vem o dinheiro? | Bruto, líquido, descontos, FGTS (existente) | MC + aberto |
| 1.2 | Holerite linha a linha | INSS por faixas, IRRF, VT, ticket, PLR, adiantamento | MC + aberto |
| 1.3 | 13º salário e férias | Cálculo, parcelas, adicional constitucional 1/3, diferença bruto/líquido | MC + aberto |

**Competências adicionais (novas):**
- `1.2.1` Interpretar cada linha do contracheque
- `1.2.2` Calcular INSS progressivo por faixas
- `1.3.1` Calcular 13º salário bruto e líquido
- `1.3.2` Calcular férias com adicional de 1/3

---

### Trilha 2 — Orçamento na prática (phase_number: 2)

**Objetivo:** Organizar o orçamento pessoal, classificar despesas e controlar gastos.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 2.1 | O que importa primeiro? | Necessidades vs. desejos, priorização (existente) |
| 2.2 | Meu primeiro plano | Distribuição da renda, dívidas, objetivos (existente) |
| 2.3 | Gastos invisíveis | Assinaturas, parcelas esquecidas, débitos automáticos |
| 2.4 | Controle de despesas | Registro, categorias, ajuste quando renda é insuficiente |

---

### Trilha 3 — Pagamentos do dia a dia (phase_number: 3)

**Objetivo:** Usar meios de pagamento digitais com segurança e eficiência.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 3.1 | Como vou pagar? | Pix, débito, crédito, fatura, parcelamento (existente) |
| 3.2 | Carteiras digitais | Wallets, NFC, QR Code, diferenças de débito e crédito |
| 3.3 | Antes de confirmar | Conferência, sinais de fraude, MED (existente + expandido) |
| 3.4 | Comparando meios | Prazo, custo, segurança, impacto no orçamento |

---

### Trilha 4 — Cartão e fatura (phase_number: 4)

**Objetivo:** Compreender o funcionamento do cartão de crédito e evitar armadilhas da fatura.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 4.1 | Entendendo o cartão | Limite, fechamento, vencimento, rotativo (existente) |
| 4.2 | A fatura na prática | Leitura da fatura, fechamento vs. vencimento, compras em ciclos |
| 4.3 | Pagamento mínimo | Consequências, crédito rotativo, comprometimento futuro |

---

### Trilha 5 — Metas e reserva (phase_number: 5)

**Objetivo:** Formular metas financeiras e calcular a reserva de emergência necessária.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 5.1 | Por que poupar? | Objetivo, imprevistos, diferença entre reserva e meta (existente) |
| 5.2 | Calculando a reserva | Método: despesas essenciais × meses, estabilidade, dependentes |
| 5.3 | Atingindo a meta | Aportes, prazo, revisão da meta (existente + expandido) |
| 5.4 | Revisão e utilização | Quando usar a reserva, como recompor |

---

### Trilha 6 — Guardar sem perder o controle (phase_number: 6)

**Objetivo:** Criar e manter o hábito de separar dinheiro ao receber.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 6.1 | Separar primeiro | Pagar-se primeiro, transferências no dia do recebimento (existente) |
| 6.2 | Automatizando a poupança | TED/PIX programado, débito automático, contas separadas |
| 6.3 | Renda variável | Adaptação para renda irregular, freelancer, autônomo |

---

### Trilha 7 — Juros e parcelas (phase_number: 7)

**Objetivo:** Calcular o custo real do crédito e avaliar ofertas de parcelamento.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 7.1 | Juros simples e compostos | Fórmulas, comparação, impacto do tempo (existente) |
| 7.2 | Parcelamento e CET | Custo total, CET, diferença preço à vista e parcelado (existente + expandido) |
| 7.3 | "Sem juros" existe? | Parcelamento sem juros: análise, desconto à vista, compromisso futuro |
| 7.4 | Comparando ofertas | Simulação comparativa, escolha baseada em custo total |

---

### Trilha 8 — Dívida que cresce (phase_number: 8)

**Objetivo:** Interpretar o crescimento de dívidas e traçar estratégias de saída.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 8.1 | Como a dívida cresce | Rotativo, saldo devedor, encargos (existente) |
| 8.2 | Cálculo do rotativo | Impacto do pagamento mínimo, cenários de prazo |
| 8.3 | Estratégias de saída | Priorização, negociação, portabilidade, renegociação |

---

### Trilha 9 — Inflação e poder de compra (phase_number: 9)

**Objetivo:** Compreender inflação e calcular o impacto no poder de compra e nos rendimentos.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 9.1 | O que é inflação? | IPCA, cálculo de reajuste, inflação percebida (existente) |
| 9.2 | Rendimento real | Nominal vs. real, fórmula de Fisher, exemplos práticos |
| 9.3 | Inflação e decisões | Reajuste de contratos, poder de compra ao longo do tempo |

---

### Trilha 10 — Onde o dinheiro rende (phase_number: 10)

**Objetivo:** Conhecer as opções de renda fixa, compreender risco, liquidez e tributação.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 10.1 | Fundamentos (existente) | Risco, prazo, liquidez básica |
| 10.2 | Produtos de renda fixa | CDB, LCI, LCA, Tesouro Direto, poupança — características |
| 10.3 | FGC e tributação | Cobertura FGC, limites, IOF, IR por prazo (existente + expandido) |
| 10.4 | Comparando produtos | Rentabilidade bruta vs. líquida, decisão informada |

---

### Trilha 11 — Golpes e proteção de dados (phase_number: 11)

**Objetivo:** Reconhecer fraudes digitais e saber como reagir.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 11.1 | Tipos de golpe | Phishing, engenharia social, falsa central, falso parente (existente) |
| 11.2 | Golpes com Pix | Falso comprovante, QR Code adulterado, contas laranja (existente + expandido) |
| 11.3 | Proteção de dados | Senhas, autenticação, exposição em redes sociais (existente) |
| 11.4 | O que fazer depois | MED, procedimentos, contato com a instituição, autoridades |
| 11.5 | Reconhecimento rápido | Simulação de cenários de ataque |

---

### Trilha 12 — Desafio integrador (phase_number: 12)

**Objetivo:** Aplicar competências de todas as trilhas em cenários complexos de decisão financeira.

| Missão | Nome | Conteúdo central |
|---|---|---|
| 12.1 | Cenário: primeiro salário | Receber, conferir, organizar, pagar (competências 1 + 2) |
| 12.2 | Cenário: decisão de pagamento | Comparar meios, avaliar cartão, Pix ou débito (competências 3 + 4) |
| 12.3 | Cenário: crise financeira | Dívida, reserva, priorização e saída (competências 5 + 7 + 8) |
| 12.4 | Cenário: alerta de fraude | Identificar golpe, proteger dados, acionar MED (competências 11) |

---

## 5. Progressão e desbloqueio

- **Trilha 1** desbloqueada no início da jornada.
- **Trilhas 2–11** desbloqueiam sequencialmente; cada trilha exige conclusão da anterior.
- **Trilha 12** desbloqueada somente após a conclusão das trilhas 1–11.
- O Catalisador pode reorganizar a ordem 1–11 conforme o objetivo do usuário (mesmo mecanismo atual, expandido para 12 elementos).
- A trilha 12 (Desafio integrador) é sempre a última, independentemente da personalização.

---

## 6. Histórico de decisões editoriais

| Data | Decisão |
|---|---|
| 2026-10-24 | Missão 2.2 (cartão) separada para a trilha 4; justificativa: tema distinto de meios de pagamento do dia a dia. |
| 2026-10-24 | Missão 3.2 (separação do dinheiro) separada para a trilha 6; justificativa: hábito de poupança é competência distinta de metas. |
| 2026-10-24 | Trilha 12 usa apenas simulações; justificativa: avaliação de processo de decisão, não memorização. |
| 2026-10-24 | Códigos de competência das missões existentes preservados (ex.: `1.1.1`); novas missões usam esquema `trilha.missão.competência`. |
| 2026-10-24 | `phase_6_v1.py` contém a missão 6.4 (Desafio integrador antigo, 4 simulações); na nova estrutura ela migra para a trilha 12 e é expandida para 8 simulações em 4 missões. |
