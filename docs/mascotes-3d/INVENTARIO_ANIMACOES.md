# Inventário de animações — Mascotes ELL

**Versão dos ativos:** 1.0  
**Fonte de verdade:** `ESPECIFICACAO_ANIMACOES_MASCOTES.md`  
**Escopo implementado:** 30 de 30 animações do catálogo (20 P1, 7 P2 e 3 P3).

> **Critério de conclusão:** uma animação só é considerada concluída aqui se o clipe existe no GLB, foi reproduzido pelo controlador real na demo, avançou no `AnimationMixer` e foi inspecionado visualmente. A evidência automatizada está em `docs/validation/report.json`; os frames-chave estão em `docs/validation/poses/` e no contact sheet `docs/validation/contact-sheet.png`.

## Resumo

| Prioridade MVP | Total | Concluídas | Pendentes do catálogo |
|---|---:|---:|---:|
| P1 (MVP obrigatório) | 20 | 20 | 0 |
| P2 (pós-MVP) | 7 | 7 | 0 |
| P3 (backlog) | 3 | 3 | 0 |
| **Total** | **30** | **30** | **0** |

- **Prioridade MVP (`P1/P2/P3`)** é a classificação de entrega da especificação.
- **Prioridade de estado** é o número usado pela máquina de estados; **menor = mais alta**.
- Estados com **lock** não podem ser interrompidos depois de iniciados (`C-05`, `C-12`, `A-07`).
- `M-08` e `C-06` são apresentações contínuas; `M-08` protege explicitamente o texto ativo.
- Todos os clipes estão embutidos nos GLBs. Não há dependência de clipes externos.

## P1 — MVP

| ID | Mascote | Animação | Clipe no GLB | Tipo | Duração | Prioridade de estado | Proteção | Validação |
|---|---|---|---|---|---|---:|---|---|
| **M-01** | Mentor | Ocioso | `MENTOR_M01_IDLE` | Loop contínuo | 12,0 s | 5 | — | Execução + captura |
| **M-02** | Mentor | Saudação | `MENTOR_M02_GREETING` | Reação curta | 1,8 s | 4 | — | Execução + captura |
| **M-03** | Mentor | Pensativo | `MENTOR_M03_THINKING` | Loop contínuo | 2,5 s | 4 | — | Execução + captura |
| **M-06** | Mentor | Preocupado | `MENTOR_M06_CONCERNED` | Reação curta | 2,4 s | 4 | — | Execução + captura |
| **M-07** | Mentor | Encorajador | `MENTOR_M07_ENCOURAGING` | Reação curta | 1,5 s | 1 | — | Execução + captura |
| **M-08** | Mentor | Explicando | `MENTOR_M08_EXPLAINING` | Loop contínuo | 2,0 s | 3 | Texto ativo | Execução + captura |
| **M-10** | Mentor | Aprovando | `MENTOR_M10_APPROVING` | Reação curta | 1,2 s | 2 | — | Execução + captura |
| **A-01** | Analista | Ocioso | `ANALISTA_A01_IDLE` | Loop contínuo | 12,0 s | 4 | — | Execução + captura |
| **A-02** | Analista | Apresentando dados | `ANALISTA_A02_PRESENTING` | Apresentação | 2,5 s | 3 | — | Execução + captura |
| **A-03** | Analista | Identificando padrão | `ANALISTA_A03_PATTERN` | Apresentação | 2,4 s | 2 | — | Execução + captura |
| **C-01** | Catalisador | Ocioso | `CATALISADOR_C01_IDLE` | Loop contínuo | 10,0 s | 6 | — | Execução + captura |
| **C-02** | Catalisador | Saudação de onboarding | `CATALISADOR_C02_WELCOME` | Reação curta | 2,0 s | 4 | — | Execução + captura |
| **C-03** | Catalisador | Ouvindo | `CATALISADOR_C03_LISTENING` | Loop contínuo | 3,0 s | 5 | — | Execução + captura |
| **C-04** | Catalisador | Celebrando resposta | `CATALISADOR_C04_CELEBRATE_ANSWER` | Reação curta | 1,0 s | 3 | — | Execução + captura |
| **C-05** | Catalisador | Revelação de trilha | `CATALISADOR_C05_TRAIL_REVEAL` | Celebração | 2,5 s | 3 | Lock | Execução + captura |
| **C-06** | Catalisador | Explicando | `CATALISADOR_C06_EXPLAINING` | Loop contínuo | 4,0 s | 5 | — | Execução + captura |
| **C-07** | Catalisador | Incentivando | `CATALISADOR_C07_NEXT_MISSION` | Reação curta | 1,5 s | 4 | — | Execução + captura |
| **C-08** | Catalisador | Acolhimento após inatividade | `CATALISADOR_C08_WELCOME_BACK` | Reação curta | 1,8 s | 4 | — | Execução + captura |
| **C-10** | Catalisador | Encorajando após dificuldade | `CATALISADOR_C10_ENCOURAGING` | Reação curta | 1,5 s | 4 | — | Execução + captura |
| **C-11** | Catalisador | Celebrando conquista | `CATALISADOR_C11_MISSION_COMPLETE` | Celebração | 2,2 s | 2 | — | Execução + captura |

## P2 — pós-MVP

| ID | Mascote | Animação | Clipe no GLB | Tipo | Duração | Prioridade de estado | Proteção | Validação |
|---|---|---|---|---|---|---:|---|---|
| **M-04** | Mentor | Curioso | `MENTOR_M04_CURIOUS` | Loop contínuo | 4,0 s | 4 | — | Execução + captura |
| **M-09** | Mentor | Verificando compreensão | `MENTOR_M09_CHECKING` | Loop contínuo | 3,0 s | 4 | — | Execução + captura |
| **M-11** | Mentor | Incentivando | `MENTOR_M11_ENCOURAGING_NEXT` | Reação curta | 1,8 s | 4 | — | Execução + captura |
| **A-04** | Analista | Reflexivo | `ANALISTA_A04_REFLECTING` | Loop contínuo | 2,0 s | 3 | — | Execução + captura |
| **A-05** | Analista | Confiante | `ANALISTA_A05_CONFIDENT` | Reação curta | 1,5 s | 2 | — | Execução + captura |
| **A-07** | Analista | Celebração analítica | `ANALISTA_A07_CELEBRATION` | Celebração | 2,0 s | 1 | Lock | Execução + captura |
| **C-12** | Catalisador | Celebração de trilha | `CATALISADOR_C12_TRAIL_COMPLETE` | Celebração | 3,5 s | 1 | Lock | Execução + captura |

## P3 — backlog

| ID | Mascote | Animação | Clipe no GLB | Tipo | Duração | Prioridade de estado | Proteção | Validação |
|---|---|---|---|---|---|---:|---|---|
| **M-05** | Mentor | Surpreso | `MENTOR_M05_SURPRISED` | Reação curta | 1,2 s | 2 | — | Execução + captura |
| **A-06** | Analista | Organizando | `ANALISTA_A06_ORGANIZING` | Reação curta | 1,2 s | 3 | — | Execução + captura |
| **C-09** | Catalisador | Surpreso positivo | `CATALISADOR_C09_SURPRISED_POSITIVE` | Reação curta | 1,5 s | 2 | — | Execução + captura |

## Regras de prioridade implementadas

### Mentor

| Prioridade | Tipo | Animação | Regra implementada |
|---:|---|---|---|
| 1 | Reação a erro | M-07 | Interrompe qualquer estado não bloqueado; obrigatória após erro. |
| 2 | Reação a acerto | M-10 | Pode substituir o idle e loops; uma reação curta aguarda o fim. |
| 3 | Explicando | M-08 | Assume quando o texto começa; reações aguardam o fim do texto. |
| 4 | Transições | M-02, M-03, M-04, M-06, M-09, M-11 | Interrompem o idle e podem ser enfileiradas. |
| 5 | Ociosidade | M-01 | Só entra quando a fila está vazia. |

### Analista de Progresso

| Prioridade | Tipo | Animação | Regra implementada |
|---:|---|---|---|
| 1 | Celebração de trilha | A-07 | Lock; não é interrompida. |
| 2 | Confiança / padrão | A-03, A-05 | A-05 é bloqueada por `recommendationActive`; A-03 é bloqueada por `positiveProgressActive`. |
| 3 | Apresentação / reflexão | A-02, A-04, A-06 | Interrompem o idle; A-02 e A-06 retornam ao idle. |
| 4 | Ociosidade | A-01 | Só entra quando a fila está vazia. |

### Catalisador

| Prioridade | Tipo | Animação | Regra implementada |
|---:|---|---|---|
| 1 | Celebração de trilha | C-12 | Lock; prioridade absoluta; C-11 é bloqueada se C-12 estiver ativa. |
| 2 | Celebração de missão | C-11 | Interrompe idle, escuta, explicação e próximo passo; não é executada junto de C-12. |
| 3 | Onboarding especial | C-05 | Lock; não é interrompida. |
| 4 | Suporte / onboarding | C-02, C-07, C-08, C-10 | Interrompem o idle e são enfileiradas se necessário. |
| 5 | Explicando / escutando | C-03, C-06 | Loops de presença. |
| 6 | Ociosidade | C-01 | Só entra quando a fila está vazia. |

## Adaptações de duração e continuidade

| ID | Especificação | Implementação | Motivo |
|---|---|---|---|
| M-01 | Loop; balanço 3 s, respiração 4 s | Clipe de 12 s | Menor múltiplo comum para loop contínuo sem emenda. |
| A-01 | Loop; ciclo de respiração 4 s; mão ao mento ~10 s | Clipe de 12 s | Inclui o gesto de análise uma vez por ciclo e mantém a emenda contínua. |
| C-01 | Loop; balanço 2,5 s, pulso 2 s | Clipe de 10 s | Menor múltiplo comum para balanço e pulso sem emenda. |
| M-06 | “2+ s” | 2,4 s | Valor dentro do mínimo, com ataque/saída suaves. |
| A-03 | “2+ s” | 2,4 s | Valor dentro do mínimo; o controlador pode mantê-la em cena por contexto. |
| C-07 | 1,5 s + postura inclinada em loop | Clipe de 1,5 s e retorno ao idle | O “hold” contínuo deve ser coordenado pela interface, não pelo clipe atômico. |
| M-05 | “O” por 300 ms e depois sorriso | 1,2 s com transição interna | Mantém a sequência e o retorno. |
| M-08 / C-06 | Loop enquanto texto ativo; encerra 500/600 ms depois | Loops de 2 s / 4 s com `textEndDelay` de 0,5 s / 0,6 s | O encerramento é feito por `endText()`/evento textual e respeita o atraso documentado. |

## Pendências de produção (não são animações ausentes)

| Lacuna | Status | Observação |
|---|---|---|
| L-02 — 3–4 variações de C-04 | Pendente | A animação base C-04 está pronta; o pool de variações deve ser produzido com o time de animação para evitar repetição no onboarding. |
| Lip-sync/TTS | Fora do MVP | A boca usa animação genérica de fala; não há fonemas. |
| C-12 → A-07 em telas simultâneas | Orquestração pendente | Ambos os clipes existem e são validados; a sincronização entre agentes é responsabilidade da integração. |
| Tema claro | Não validado | Lacuna L-06; o palco foi validado em tema escuro. |
| Layout por breakpoint do site | Não validado | Lacuna L-07; a demo tem breakpoints próprios, não os do site. |
| Variações de intensidade “Normal/Reduzido/Desativado” | Parcial | `setReducedMotion` cobre “Normal” e “Reduzido”. “Desativado” pode ser implementado com `setReducedMotion(true)` + idle estático. |
| Frequência por sessão/missão/trilha | Responsabilidade da integração | O backend/site deve impedir repetições como M-02 1×/sessão, M-05 1×/missão, C-05 1×/usuário, C-12 1×/trilha; o controlador genérico não conhece esses IDs de contexto. |
| Validação em celular físico | Pendente | Foram usados Chromium headless e emulação mobile; falta medir FPS/térmica em aparelho de referência. |

## Evidência de validação

- **30/30 clipes** executados pelo controlador real no navegador; `docs/validation/report.json` contém ID, clipe, duração e progresso amostrado.
- **Contact sheet** dos 30 frames-chave: `docs/validation/contact-sheet.png`.
- **Capturas individuais**: `docs/validation/poses/<ID>.png`.
- **Regras de estado**: testes de M-08 em texto, exclusão A-03/A-05, prioridade C-12/C-11, fila, locks, reduced motion e pausa fora da viewport.
- **Instruções de reprodução**: `docs/VALIDACAO.md`.
