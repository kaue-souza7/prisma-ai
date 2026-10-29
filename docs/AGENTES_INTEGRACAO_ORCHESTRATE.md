# Preparação dos agentes para o watsonx Orchestrate

**Status:** integração real ativa — Mentor, Catalisador e Analista criados no Orchestrate e validados via API.
**Objetivo:** deixar trilha, chat, recomendações e contratos prontos para que a
chegada do Orchestrate seja uma substituição de adaptador — não uma reescrita.

> Com `ORCHESTRATE_ENABLED=true` e os UUIDs dos agentes configurados, o adaptador
> chama o agente real. Quando desativado ou em caso de falha, o fallback honesto continua ativo.

---

## Estado real da integração (28/10/2026)

- **Cliente único:** `backend/app/core/orchestrate_client.py` faz troca de API key por token IAM, cache/renovação, retry, timeout e circuit breaker.
- **Parsing único:** `backend/app/core/orchestrate_parser.py` lê `choices[0].message.content`, JSON puro e JSON cercado por markdown.
- **Agentes no Orchestrate:** `prisma_mentor`, `prisma_catalyst`, `prisma_analyst` e `prisma_studio` existem e foram validados com chamadas reais.
- **Configuração:** os UUIDs ficam em `ORCHESTRATE_AGENT_MENTOR_ID`, `ORCHESTRATE_CATALYST_AGENT_ID`, `ORCHESTRATE_ANALYST_AGENT_ID` e `ORCHESTRATE_STUDIO_AGENT_ID` no `.env`. Nunca versionar a API key.
- **Analista:** insight de missão/geral com IA + cache, e síntese de trilha persistida em `trail_syntheses` (migration 0018).
- **Celebração:** o Catalisador gera a celebração na primeira conclusão de trilha; o campo `trail_celebration` aparece no submit da missão.
- **Fallback:** continua ativo e coberto por testes; a suíte desliga o Orchestrate por padrão (`ORCHESTRATE_LIVE_TEST=1` para teste ao vivo).

### Pendências conhecidas

- Conjuntos `question_set=2/3` foram gerados como variantes nas 12 trilhas por `backend/scripts/backfill_question_sets.py`; ainda não são perguntas autorais.
- `question_set=4` (reforço do modo `full`) não existe.
- O onboarding implementa as 10 perguntas fixas + até 8 perguntas adaptativas geradas pelo Catalisador, com `conversation_history` completo enviado ao backend.
- Cenários de segurança D8 ainda precisam ser executados e documentados.
- O Estúdio agora usa o agente `prisma_studio` (`ORCHESTRATE_STUDIO_AGENT_ID`) para gerar `revisao`, `flashcards` e `exercicios`, com validação de estrutura e refund em caso de falha. A qualidade do conteúdo gerado deve ser revisada antes do piloto.

---

## Spike D7 — Agente Mentor no Orchestrate

**Concluído em:** Sub-tarefa 3 do plano de implementação de agentes.

### Agente criado

| Campo | Valor |
|---|---|
| Nome (API) | `prisma_mentor` |
| ID | `c0c9e92a-ed73-4310-8f57-6967012e84dd` |
| Ambiente | `ca-tor-d893bf93` — IBM Cloud Toronto |
| LLM | `groq/openai/gpt-oss-120b` |
| Style | `react_intrinsic` |
| Decisões cobertas | D7, D8, D9, D14, D30, D32, D33, D36 |

> **Nota de nomenclatura:** o Orchestrate não aceita hífens em nomes de agentes.
> O nome de API é `prisma_mentor`; o campo `ORCHESTRATE_AGENT_MENTOR_ID` usa esse valor.

### Contrato de resposta confirmado

O agente `prisma_mentor` retorna no campo `response` da API um **JSON string** com:

```json
{
  "content": "<resposta textual, 2-4 parágrafos curtos>",
  "suggestions": ["<pergunta de acompanhamento>", ...]
}
```

**Campo textual:** `response` → JSON string → campo `content` (extração via `_extract_text` com expansão de JSON interno).
**Sugestões:** propagadas via `data["_suggestions"]` pelo extrator.

O adaptador em `conversations/orchestrate.py` cobre todos os formatos:
- `content` / `output` / `response` como string plana
- `content` / `output` / `response` como JSON string (formato atual do agente)
- `choices[0].message.content` (OpenAI-compat)

### Resultado do teste de mensagem simples

**Pergunta:** "Por que a dívida no cartão de crédito cresce tão rápido?"

**Resposta (trecho):** "A dívida do cartão de crédito costuma crescer rápido porque ele tem juros muito altos e, além disso, as parcelas de juros são cobradas diariamente. Quando você deixa de pagar o total da fatura, o saldo que fica pendente entra no próximo mês já com juros compostos..."

**Verificação de segurança (D8):** pedido de recomendação de investimento respondeu com recusa correta e redirecionamento para educação — zero violações.

### Configuração ativada

```env
ORCHESTRATE_ENABLED=true
ORCHESTRATE_URL=https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/d596b027-b5a4-4614-be7c-cab5d12a8c03
ORCHESTRATE_API_KEY=<sua chave IBM Cloud>
ORCHESTRATE_AGENT_MENTOR_ID=prisma_mentor
ORCHESTRATE_TIMEOUT_SECONDS=15
```

### Suite de testes

`pytest -q` — **266 passed, 3 skipped** (os 3 skips são o contrato ao vivo,
executado com `ORCHESTRATE_LIVE_TEST=1`).

---


## 1. O que foi antecipado

| Frente | Estado agora | Ponto de entrada da IA |
|---|---|---|
| Trilha personalizada | Gerada por regras no onboarding e persistida em `profiles.trail` | `agents.catalyst.apply_generated_trail()` |
| Chat do Mentor | UI real, histórico persistido, contexto da missão e fallback honesto | `conversations.orchestrate.request_mentor_reply()` |
| Analista no fluxo | Insight no resumo da missão, no feedback de erro repetido e no painel | `agents.analyst` (substituível por análise em background) |
| Catalisador visível | Mensagem de próximo passo na Home, na Jornada e no resumo | `agents.catalyst.build_recommendation()` |
| Onboarding conversacional | Conduzido pelo Catalisador IA: 10 fixas + até 8 adaptativas | `agents.catalyst.conduct_onboarding()` |
| Síntese de trilha | Gerada pelo Analista ao concluir trilha — frase curta + card no painel | `agents.analyst.generate_trail_synthesis()` |
| Infraestrutura | Configuração, timeout, fallback, logs e testes | `.env` + `orchestrate.py` |

---

## 2. Trilha personalizada

### 2.1 Modelo persistido

`profiles.trail` (JSONB, migration `0010`) guarda:

```json
{
  "source": "ai",
  "version": 2,
  "goal_category": "dividas",
  "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  "trail_modes": {
    "1": "express",
    "2": "standard",
    "3": "full",
    "4": "full"
  },
  "trail_1_auto_concluded": true,
  "rationale": "Com 3 anos de CLT e objetivo de sair das dívidas, os juros são onde o impacto é mais imediato para você.",
  "focus_areas": ["Juros compostos", "Custo de parcelamentos"],
  "pace": "steady",
  "knowledge_level": "intermediate",
  "life_context": "ja_trabalho",
  "urgency": "agora_preciso",
  "generated_at": "2026-10-23T..."
}
```

> **Nota:** `phase_order` mantém sempre `[1..12]` — a ordem nunca muda.
> `trail_modes` define o modo de profundidade por trilha: `express`, `standard` ou `full`.
> `trail_1_auto_concluded: true` indica que a Trilha 1 foi reconhecida no onboarding (50 XP, selo "Dominada no onboarding").

A API enriquece o objeto com `phases` (número, nome e descrição) para a UI.

Perfis criados antes da migration `0010`, sem `trail`, continuam na ordem
canônica e podem criar uma trilha personalizada no Perfil (ou voltar à ordem
padrão). Nenhum usuário existente é desbloqueado ou pontuado de forma diferente
até a trilha ser persistida.

### 2.2 Regras determinísticas atuais

| Objetivo | Ordem das fases |
|---|---|
| Primeiro salário | 1 → 2 → 3 → 4 → 5 → 6 |
| Sair das dívidas / crédito e juros | 4 → 1 → 2 → 3 → 5 → 6 |
| Criar reserva | 3 → 1 → 2 → 4 → 5 → 6 |
| Investir melhor | 3 → 4 → 5 → 1 → 2 → 6 |
| Proteção digital | 6 → 2 → 1 → 3 → 4 → 5 |
| Outro | Ordem padrão, ajustada por contexto de vida e urgência |

Contextos de vida podem alterar a ordem quando o objetivo é genérico:
renda variável começa por dinheiro digital e reserva; estudante sem renda começa
por metas e reserva. `knowledge_level=advanced` muda o ritmo para
`accelerated`, mas **não pula missões**.

### 2.3 Regra de desbloqueio

- A primeira fase da trilha começa disponível.
- Cada fase seguinte exige **todas as missões obrigatórias de todas as fases
  anteriores da trilha**.
- Dentro de uma fase, as missões obrigatórias continuam sequenciais.
- Pontos, conquistas e conclusão continuam no backend (`progress/service.py`).
- Uma ordem inválida (fase faltando, duplicada ou inexistente) é rejeitada; o
  backend usa a ordem canônica como fallback.

### 2.4 Contratos

| Método | Rota | Uso |
|---|---|---|
| `POST` | `/api/v1/users/me/onboarding/adaptive-questions` | Gera até 8 perguntas adaptativas a partir das 10 respostas fixas |
| `POST` | `/api/v1/users/me/onboarding` | Gera a trilha e devolve `trail` com fases |
| `GET` | `/api/v1/users/me/trail` | Lê a trilha atual |
| `POST` | `/api/v1/users/me/trail/preference` | `{ "mode": "personalized" \| "standard" }` |
| `GET` | `/api/v1/journey/overview` | Fases na ordem da trilha + recomendação do Catalisador |

### 2.5 Seam para a IA

Quando o Catalisador IA estiver disponível, ele deve devolver algo como:

```json
{
  "phase_order": [4, 1, 2, 3, 5, 6],
  "rationale": "Você quer resolver dívidas agora; juros vem primeiro.",
  "focus_areas": ["Juros compostos", "Rotativo"],
  "pace": "steady"
}
```

O backend chama `apply_generated_trail()`, valida a ordem contra as fases ativas
e só então persiste com `source: "ai"`. O agente nunca escreve no banco
diretamente e nunca concede desbloqueios.

---

## 3. Chat do Mentor

### 3.1 O que já é real

- `POST /api/v1/conversations/mentor` persiste mensagens do usuário e do Mentor.
- `GET /api/v1/conversations/mentor/history` devolve as conversas.
- `GET /api/v1/conversations/mentor/context?mission_id=` devolve:
  - missão, fase e competências;
  - mensagem de abertura;
  - sugestões de perguntas;
  - tópicos de reforço identificados pelo Analista;
  - `status`: `preparing`, `available` ou `unavailable`.
- A UI existe na página `/student/mentor` e em um modal dentro do minicurso.
- A página aceita `?mission=ID` e pré-carrega o contexto da missão.
- O resumo da missão tem o botão “Conversar com o Mentor sobre esta missão”.

### 3.2 Status honestos

| Status | Significado | Comportamento |
|---|---|---|
| `preparing` | `ORCHESTRATE_ENABLED=false` | Fallback explícito; mensagens salvas |
| `available` | Orchestrate respondeu | Conteúdo do agente |
| `unavailable` | Erro, timeout ou resposta vazia | Fallback; chat não quebra |

### 3.3 Payload enviado ao Orchestrate

```json
{
  "agent": "mentor",
  "conversation_id": 12,
  "user_context": {
    "personal_goal": "Sair das dívidas",
    "knowledge_level": "intermediate"
  },
  "learning_context": {
    "mission_id": 10,
    "mission_name": "O tempo e os juros",
    "phase_number": 4,
    "phase_name": "Juros: a favor e contra você",
    "competencies": [{"code": "4.1.1", "name": "Explicar juros..."}],
    "reinforcement_topics": ["Juros compostos"]
  },
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "message": "Por que a dívida cresce tão rápido?"
}
```

O adaptador aceita `content`, `output` ou `response` como campo textual e usa
as `suggestions` devolvidas pelo agente, se existirem. O mapeamento final será
ajustado no spike, sem mudar o restante do sistema.

### 3.4 Configuração

```env
ORCHESTRATE_ENABLED=true
ORCHESTRATE_URL=https://api.<região>.watson-orchestrate.cloud.ibm.com/instances/<id>
ORCHESTRATE_API_KEY=<IBM Cloud API key>
ORCHESTRATE_AGENT_MENTOR_ID=<uuid>
ORCHESTRATE_CATALYST_AGENT_ID=<uuid>
ORCHESTRATE_ANALYST_AGENT_ID=<uuid>
ORCHESTRATE_TIMEOUT_SECONDS=15
```

Os UUIDs são obtidos com `orchestrate agents list -v`. A API key nunca deve ser
versionada; o cliente troca por um token IAM de curta duração em runtime.

---

## 4. Analista de Progresso

O Analista continua em background no MVP, mas suas recomendações já aparecem
nos pontos certos:

| Ponto | Dado exibido |
|---|---|
| Feedback de erro | `reinforcement` após erro recorrente, com ação `review` |
| Resumo da missão | `mission_insight` com 1 frase de evidência + 1 ação |
| Painel de progresso | `analyst_insight` no `/progress/summary` |
| Contexto do Mentor | `reinforcement_topics` no payload |
| Celebração de trilha (via Catalisador) | `trail_synthesis.short` — 1 frase gerada pelo Analista, entregue pelo Catalisador |
| Card no painel de progresso | `trail_synthesis.full` — card "O que você demonstrou saber" (D-A1) |

Formato aprovado em D14: uma frase sobre a dificuldade + uma frase de ação. O
estudante nunca vê a análise bruta.

### Contrato de síntese de trilha (D-A1)

A futura chamada de IA deve substituir `generate_trail_synthesis()`, mantendo o contrato:

```json
{
  "agent": "analyst",
  "trail_id": 3,
  "short": "Você agora consegue calcular o custo real de uma parcela antes de assinar.",
  "full": {
    "competencies_demonstrated": ["3.1.1", "3.2.1"],
    "competencies_with_difficulty": ["3.1.2"],
    "summary": "Nas atividades desta trilha, você demonstrou saber...",
    "reinforcement_suggestion": null
  }
}
```

A futura chamada de IA deve também substituir a função que monta o insight de missão,
mantendo o mesmo contrato `{agent, severity, action, competencies, message}`.

---

## 5. Catalisador como agente de IA

O Catalisador foi promovido de lógica determinística a agente de IA (D-C1 a D-C14).
Os contratos abaixo definem os pontos de substituição no backend.

### 5.1 Onboarding conversacional

**Fluxo atual:**
1. O frontend conduz as **10 perguntas fixas**.
2. Chama `POST /api/v1/users/me/onboarding/adaptive-questions` com `fixed_answers` + histórico.
3. O Catalisador devolve até **8 perguntas adaptativas** (`{"questions": [...]}`).
4. O frontend pergunta as adaptativas (com opção de pular) e envia tudo em `POST /api/v1/users/me/onboarding`.

**Ponto de entrada da IA:** `agents.catalyst.conduct_onboarding()` e `agents.catalyst.generate_adaptive_questions()`

**Payload enviado ao Catalisador:**
```json
{
  "agent": "catalyst",
  "action": "onboarding",
  "fixed_answers": {
    "objetivo": "sair_dividas",
    "life_context": "ja_trabalho",
    "anos_trabalho": "3",
    "urgency": "agora_preciso",
    "knowledge_level_declared": "intermediate"
  },
  "conversation_history": [
    {"role": "assistant", "content": "Que legal que você já trabalha! Há quanto tempo?"},
    {"role": "user", "content": "3 anos com carteira assinada"}
  ]
}
```

**Resposta do Catalisador:**
```json
{
  "phase_order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  "trail_modes": {
    "1": "express",
    "2": "standard",
    "3": "full"
  },
  "trail_1_auto_concluded": true,
  "rationale": "Com 3 anos de CLT e foco em sair das dívidas, os juros são onde o impacto é mais imediato para você.",
  "next_message": "Sua jornada está pronta! Você já domina o básico do contracheque — vamos direto para o que vai fazer diferença agora.",
  "focus_areas": ["Juros compostos", "Custo de parcelamentos"]
}
```

O backend chama `apply_generated_trail()`, valida `phase_order` (sempre `[1..12]`),
aplica `trail_modes`, concede 50 XP se `trail_1_auto_concluded: true`, e persiste com `source: "ai"`.

### 5.2 Presença contínua — próximo passo

**Endpoint atual:** `GET /api/v1/journey/overview`
**Ponto de entrada da IA:** `agents.catalyst.build_recommendation()`

**Payload enviado ao Catalisador:**
```json
{
  "agent": "catalyst",
  "action": "next_step",
  "user_context": {
    "personal_goal": "Sair das dívidas",
    "trail_modes": {"1": "express", "2": "standard"},
    "trail_1_auto_concluded": true
  },
  "progress": {
    "completed_trails": [1],
    "current_trail": 2,
    "current_mission": 5,
    "last_session_hours_ago": 48
  },
  "analyst_signals": [
    {"competencia": "1.1.1", "nivel_dificuldade": "low", "tipo_reforco_sugerido": null}
  ]
}
```

**Resposta do Catalisador:**
```json
{
  "tipo": "continue",
  "trilha_id": 2,
  "missao_id": 5,
  "mensagem": "Bem-vindo de volta! Você estava no orçamento — vamos continuar de onde parou.",
  "rationale": "Orçamento é o próximo passo natural depois de entender o salário."
}
```

**Tipos de recomendação:** `start` | `continue` | `review` | `celebrate` | `trail_1_review`

Para `trail_1_review` (quando Analista detecta dificuldade em competências da Trilha 1):
```json
{
  "tipo": "trail_1_review",
  "trilha_id": 1,
  "mensagem": "Percebi algumas dificuldades com contracheque — quer dar uma olhada rápida na Trilha 1?",
  "rationale": "Competência 1.1.1 com dificuldade recorrente detectada pelo Analista."
}
```

### 5.3 Celebração de conclusão de trilha

**Ponto de entrada da IA:** `agents.catalyst.celebrate_trail_completion()`

**Payload enviado:**
```json
{
  "agent": "catalyst",
  "action": "celebrate_trail",
  "trail_id": 2,
  "trail_name": "Orçamento na prática",
  "analyst_synthesis": {
    "short": "Você agora consegue montar um orçamento real com sua renda líquida.",
    "competencies_demonstrated": ["2.1.1", "2.2.1"]
  },
  "next_trail": {"id": 3, "name": "Pagamentos do dia a dia"}
}
```

**Resposta do Catalisador:**
```json
{
  "celebration_message": "Você agora consegue montar um orçamento real com sua renda líquida — isso já é mais do que a maioria das pessoas faz.",
  "next_step_message": "Agora vem uma parte prática: como os pagamentos do dia a dia afetam esse orçamento que você acabou de montar.",
  "badge_label": "Orçamento na prática — concluída"
}
```

### 5.4 Configuração

```env
ORCHESTRATE_ENABLED=true
ORCHESTRATE_CATALYST_AGENT_ID=<uuid>
ORCHESTRATE_TIMEOUT_SECONDS=15
```

Com `ORCHESTRATE_ENABLED=false` (ou `ORCHESTRATE_CATALYST_ENABLED=false`),
`conduct_onboarding()`, `build_recommendation()` e `celebrate_trail_completion()`
usam as regras determinísticas atuais como fallback, mantendo o mesmo contrato
de entrada e saída.

---

## 6. Ordem de integração quando o acesso chegar

1. Executar o spike do §22 da Arquitetura.
2. Confirmar o contrato real de entrada/saída do agente Mentor.
3. Ajustar apenas o mapeamento em `conversations/orchestrate.py`.
4. Ativar `ORCHESTRATE_ENABLED=true` e validar:
   - resposta com contexto de missão;
   - timeout e fallback;
   - persistência do histórico;
   - nenhuma alteração de pontos/desbloqueios pela IA.
5. Conectar o Analista em background e comparar com os insights determinísticos.
6. Conectar o Catalisador IA:
   - ativar `conduct_onboarding()` e validar `trail_modes` + `trail_1_auto_concluded`;
   - ativar `build_recommendation()` e validar os 5 tipos de recomendação;
   - ativar `celebrate_trail_completion()` e validar síntese do Analista integrada.
7. Rodar os cenários de segurança da D8 antes de qualquer piloto.

---

## 7. Verificação

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/backfill_question_sets.py  # conjuntos 2/3 (variantes)
docker compose exec backend pytest -q
docker compose exec backend pytest tests/test_orchestrate_live.py -q  # com ORCHESTRATE_LIVE_TEST=1
# CI: workflow manual .github/workflows/agents-live.yml (requer secrets do Orchestrate)
docker compose exec frontend npm test -- --run
docker compose exec frontend npm run build
docker compose exec backend alembic check
```

Cobertura adicionada em `backend/tests/test_agents_preparation.py`:
trilha por objetivo, validação de ordem, recomendação do Analista, onboarding
com trilha, desbloqueio fora da ordem canônica, contexto/histórico do Mentor,
fallback honesto, celebração, cache de síntese e reforço após erro repetido.

### Segurança D8

O harness `backend/scripts/check_mentor_safety.py` executa os 10 cenários
obrigatórios contra o Mentor real. O resultado de 28/10/2026 está em
[`docs/RELATORIO_SEGURANCA_D8.md`](RELATORIO_SEGURANCA_D8.md): 10/10 sem violação.
Repita o harness sempre que as instruções do agente mudarem.

```bash
docker compose exec -T backend python scripts/check_mentor_safety.py > docs/RELATORIO_SEGURANCA_D8.md
```
