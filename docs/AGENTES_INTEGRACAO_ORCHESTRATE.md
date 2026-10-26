# Preparação dos agentes para o watsonx Orchestrate

**Status:** implementado sem IA em 23/10/2026.  
**Objetivo:** deixar trilha, chat, recomendações e contratos prontos para que a
chegada do Orchestrate seja uma substituição de adaptador — não uma reescrita.

> A integração real continua bloqueada por D7. Nenhum endpoint deste documento
> chama um LLM enquanto `ORCHESTRATE_ENABLED=false`. O fallback é explícito.

---

## 1. O que foi antecipado

| Frente | Estado agora | Ponto de entrada da IA |
|---|---|---|
| Trilha personalizada | Gerada por regras no onboarding e persistida em `profiles.trail` | `agents.catalyst.apply_generated_trail()` |
| Chat do Mentor | UI real, histórico persistido, contexto da missão e fallback honesto | `conversations.orchestrate.request_mentor_reply()` |
| Analista no fluxo | Insight no resumo da missão, no feedback de erro repetido e no painel | `agents.analyst` (substituível por análise em background) |
| Catalisador visível | Mensagem de próximo passo na Home, na Jornada e no resumo | `agents.catalyst.build_recommendation()` |
| Onboarding | Coleta contexto de vida e urgência, mostra a trilha e permite ajustar | Mesmo contrato de trilha |
| Infraestrutura | Configuração, timeout, fallback, logs e testes | `.env` + `orchestrate.py` |

---

## 2. Trilha personalizada

### 2.1 Modelo persistido

`profiles.trail` (JSONB, migration `0010`) guarda:

```json
{
  "source": "rules",
  "version": 1,
  "goal_category": "dividas",
  "phase_order": [4, 1, 2, 3, 5, 6],
  "rationale": "Como seu objetivo é sair das dívidas, começar por juros...",
  "focus_areas": ["Juros compostos", "Custo de parcelamentos"],
  "pace": "steady",
  "knowledge_level": "intermediate",
  "life_context": "ja_trabalho",
  "urgency": "agora_preciso",
  "generated_at": "2026-10-23T..."
}
```

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
ORCHESTRATE_ENABLED=false
ORCHESTRATE_URL=
ORCHESTRATE_API_KEY=
ORCHESTRATE_AGENT_ID=
ORCHESTRATE_TIMEOUT_SECONDS=15
```

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

Formato aprovado em D14: uma frase sobre a dificuldade + uma frase de ação. O
estudante nunca vê a análise bruta.

A futura chamada de IA deve substituir a função que monta o insight, mantendo o
mesmo contrato `{agent, severity, action, competencies, message}`.

---

## 5. Catalisador

- `GET /journey/overview` devolve a recomendação pronta para a Home e a Jornada.
- A mensagem é determinística e cobre: começar, continuar, revisar ou concluir.
- Se houver reforço sugerido, a mensagem prioriza revisão — sem bloquear o
  avanço.
- A trilha e a recomendação são exibidas na Home, na Jornada e no Perfil.
- A IA futura pode substituir `build_recommendation()` desde que devolva o mesmo
  contrato e o backend valide a missão sugerida.

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
6. Conectar o Catalisador IA via `apply_generated_trail()` e `build_recommendation()`.
7. Rodar os cenários de segurança da D8 antes de qualquer piloto.

---

## 7. Verificação

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend pytest -q
docker compose exec frontend npm test -- --run
docker compose exec frontend npm run build
docker compose exec backend alembic check
```

Cobertura adicionada em `backend/tests/test_agents_preparation.py`:
trilha por objetivo, validação de ordem, recomendação do Analista, onboarding
com trilha, desbloqueio fora da ordem canônica, contexto/histórico do Mentor,
fallback honesto e reforço após erro repetido.
