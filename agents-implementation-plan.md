# Plano de Implementação e Incorporação dos Agentes — Prisma.AI

## Visão geral

Integrar os três agentes de IA (Catalisador, Mentor, Analista de Progresso) ao IBM watsonx Orchestrate, substituindo os adaptadores determinísticos e fallbacks existentes por chamadas reais de LLM — sem reescrever a arquitetura de backend já construída.

**Escopo:** backend FastAPI + watsonx Orchestrate. Frontend e banco de dados mudam apenas onde necessário para suportar novos campos (`trail_modes`, `trail_1_auto_concluded`, `question_set`, `user_mission_attempts`).

**Abordagem:** cada sub-tarefa é uma substituição de adaptador ou uma adição de capacidade. O sistema funciona end-to-end com fallback determinístico antes, durante e depois de cada etapa.

**Não está no escopo deste plano:** redesign de frontend, novos fluxos de autenticação, Open Finance, áudio.

---

## Pré-requisito: Spike D7

Antes de qualquer sub-tarefa, o spike D7 deve ser concluído:
- Criar um agente Mentor básico no watsonx Orchestrate (via ADK ou UI).
- Confirmar o contrato real de entrada/saída (campos da resposta: `content`, `output` ou `response`; presença de `suggestions`).
- Ativar `ORCHESTRATE_ENABLED=true` em ambiente de desenvolvimento.
- Validar timeout (15s) e fallback.

O resultado do spike é registrado em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` (seção "Spike D7"), com o contrato confirmado.

---

## Sub-tarefa 1 — Migration e seeds: question_set e trail_modes

**Status:** [x] done

### Intent
Adicionar ao banco as estruturas necessárias para rotação de conjuntos de perguntas (D-Q1) e modos de profundidade de trilha (D-C10), sem quebrar dados existentes.

### Expected Outcomes
- Campo `question_set` (int, valores 1/2/3, default 1) em `activities`.
- Tabela `user_mission_attempts` com colunas: `user_id`, `mission_id`, `attempt_number`, `question_set_used`.
- Campo `trail_modes` (JSONB) em `profiles.trail` — o objeto `trail` já existe; apenas o novo campo interno é adicionado.
- Campo `trail_1_auto_concluded` (bool) em `profiles.trail`.
- Seeds das trilhas 1–12 atualizadas para incluir 3 conjuntos por missão (`question_set` 1, 2, 3) com perguntas diferentes em cada conjunto.
- Migration idempotente: usuários existentes não perdem progresso.

### Todo List
- [ ] Criar migration `0016_question_sets_and_trail_modes.py`:
  - Adicionar coluna `question_set INTEGER DEFAULT 1 NOT NULL` em `activities`.
  - Criar tabela `user_mission_attempts (id, user_id, mission_id, attempt_number, question_set_used, started_at)`.
- [ ] Atualizar modelo SQLAlchemy `Activity` com campo `question_set`.
- [ ] Criar modelo `UserMissionAttempt` em `backend/app/shared/models.py`.
- [ ] Atualizar seeds das trilhas (começando pela Trilha 1) para incluir 3 conjuntos por missão, prefixando conteúdo com `question_set=1/2/3`.
- [ ] Atualizar `seeder.py` para usar `(mission_id, order, question_set)` como chave natural de upsert.
- [ ] Verificar com `pytest backend/tests/test_content_trails_v2.py`.

### Relevant Context
- `backend/app/shared/models.py` — modelos SQLAlchemy existentes.
- `backend/alembic/versions/` — padrão de migrations existentes.
- `backend/app/modules/content/seeds/trail_1_v2.py` — exemplo de seed existente.
- `backend/app/modules/content/seeds/seeder.py` — lógica de upsert idempotente.
- `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md` seção 5.4 — especificação do campo e lógica.

---

## Sub-tarefa 2 — Backend: lógica de rotação de conjuntos de perguntas

**Status:** [x] done

### Intent
Implementar a função `get_active_activities_for_attempt()` que seleciona o conjunto correto de perguntas para cada tentativa do usuário, seguindo a regra D-Q1.

### Expected Outcomes
- Função `get_active_activities_for_attempt(db, user_id, mission_id)` em `backend/app/modules/journey/service.py`.
- Nas tentativas 1–3: conjunto sorteado aleatoriamente entre os não usados.
- Na tentativa 4+: qualquer conjunto sorteado livremente.
- Ordem interna das atividades do conjunto randomizada.
- Tentativa registrada em `user_mission_attempts` ao iniciar missão.
- Endpoint `POST /api/v1/journey/missions/{id}/start` usa a nova função.
- Testes unitários cobrindo os 6 cenários de rotação da tabela em `CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`.

### Todo List
- [ ] Implementar `get_active_activities_for_attempt(db, user_id, mission_id)` em `journey/service.py`.
- [ ] Implementar `_get_used_sets(db, user_id, mission_id) -> list[int]` — consulta `user_mission_attempts`.
- [ ] Implementar `_select_set(used: list[int]) -> int` — lógica de sorteio sem repetição nas 3 primeiras.
- [ ] Atualizar o endpoint de início de missão para registrar tentativa em `user_mission_attempts`.
- [ ] Adicionar casos de teste em `backend/tests/test_progression_api.py` ou arquivo específico.
- [ ] Verificar que `refazer missão concluída não duplica pontos` continua passando.

### Relevant Context
- `backend/app/modules/journey/service.py` — funções de jornada existentes.
- `backend/app/modules/journey/router.py` — endpoints de missão.
- `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md` seção 5.4 — regra de seleção por tentativa.
- `backend/tests/test_journey_api.py` — testes de integração existentes.

---

## Sub-tarefa 3 — Spike D7: primeiro agente Mentor no Orchestrate

**Status:** [x] done

### Intent
Criar o agente Mentor no watsonx Orchestrate, confirmar o contrato real de entrada/saída e ativar a integração no adaptador existente — sem alterar o restante do sistema.

### Expected Outcomes
- Agente Mentor criado no Orchestrate com instruções baseadas em `docs/Especificacao_Agentes_IA_ELL_IBM.md` (D7, D8, D9, D30, D32, D33, D36).
- `ORCHESTRATE_ENABLED=true` funcionando em desenvolvimento.
- `request_mentor_reply()` em `conversations/orchestrate.py` retornando `status: "available"` com conteúdo real.
- Contrato de resposta confirmado (campo textual e presença de `suggestions`).
- Fallback continua funcionando quando Orchestrate está indisponível (`status: "unavailable"`).
- Cenários de segurança da D8 testados manualmente (mínimo 10 cenários).

### Todo List
- [ ] Criar agente Mentor no Orchestrate via ADK (`orchestrate agent create`) com instruções de sistema baseadas nas decisões aprovadas.
- [ ] Registrar `ORCHESTRATE_AGENT_ID` (Mentor) no `.env`.
- [ ] Ajustar mapeamento de resposta em `conversations/orchestrate.py` conforme contrato real confirmado.
- [ ] Ativar `ORCHESTRATE_ENABLED=true` e executar testes de integração existentes.
- [ ] Executar manualmente os 10 cenários de segurança da D8 e documentar resultados em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.
- [ ] Verificar fallback: simular indisponibilidade e confirmar que progresso do usuário não é afetado.

### Relevant Context
- `backend/app/modules/conversations/orchestrate.py` — adaptador existente com MentorReply dataclass.
- `backend/app/modules/conversations/service.py` — send_mentor_message(), get_mentor_context().
- `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 3 — payload e configuração do Mentor.
- `backend/tests/test_conversations_api.py` e `test_agents_preparation.py` — testes existentes.
- `.env.example` — variáveis ORCHESTRATE_*.

---

## Sub-tarefa 4 — Catalisador como agente: onboarding conversacional

**Status:** [x] done

### Intent
Substituir o onboarding determinístico (`_trail_from_profile()` em `users/service.py`) pelo onboarding conversacional conduzido pelo Catalisador via Orchestrate, produzindo `trail_modes` e `trail_1_auto_concluded` além do `phase_order` já existente.

### Expected Outcomes
- Agente Catalisador criado no Orchestrate com instruções de onboarding (D-C1 a D-C4).
- Nova função `conduct_onboarding(payload) -> CatalystOnboardingReply` em `agents/catalyst.py`.
- `CatalystOnboardingReply` inclui `phase_order`, `trail_modes`, `trail_1_auto_concluded`, `rationale`, `next_message`.
- `apply_generated_trail()` atualizado para persistir `trail_modes` e `trail_1_auto_concluded`.
- Quando `trail_1_auto_concluded=true`: 50 XP concedidos via `progress/service.py`, conquista com selo "Dominada no onboarding".
- Fallback determinístico (`_trail_from_profile()`) continua ativo quando `ORCHESTRATE_ENABLED=false`.
- Payload do onboarding inclui `conversation_history` para perguntas adaptativas.
- Testes cobrem: trilha gerada com trail_modes, auto-conclusão da Trilha 1, fallback determinístico.

### Todo List
- [ ] Criar agente Catalisador no Orchestrate com instruções de onboarding (D-C1, D-C2, D-C3, D-C4).
- [ ] Registrar `ORCHESTRATE_CATALYST_AGENT_ID` no `.env` e em `core/config.py`.
- [ ] Criar dataclass `CatalystOnboardingReply` em `agents/catalyst.py`.
- [ ] Implementar `conduct_onboarding(payload) -> CatalystOnboardingReply` em `agents/catalyst.py` com fallback.
- [ ] Atualizar `apply_generated_trail()` para aceitar e persistir `trail_modes` e `trail_1_auto_concluded`.
- [ ] Atualizar `users/service.py: complete_onboarding()` para chamar `conduct_onboarding()` quando ativado.
- [ ] Atualizar `progress/service.py` para conceder 50 XP quando `trail_1_auto_concluded=true`.
- [ ] Adicionar `achievement_key = "trilha_1_dominada_onboarding"` em achievements.
- [ ] Atualizar testes em `test_agents_preparation.py`.

### Relevant Context
- `backend/app/modules/agents/catalyst.py` — funções existentes: `apply_generated_trail()`, `build_trail()`.
- `backend/app/modules/users/service.py` — `complete_onboarding()`, `_trail_from_profile()`.
- `backend/app/modules/progress/service.py` — `add_points()`, lógica de achievements.
- `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 5.1 — payload e resposta do Catalisador onboarding.
- `docs/Especificacao_Agentes_IA_ELL_IBM.md` seções D-C1 a D-C7.

---

## Sub-tarefa 5 — Catalisador como agente: presença contínua e celebração de trilha

**Status:** [x] done

### Intent
Substituir `build_recommendation()` determinístico pelo Catalisador via Orchestrate para próximo passo, e adicionar `celebrate_trail_completion()` para celebração de conclusão de trilha com síntese do Analista.

### Expected Outcomes
- `build_recommendation()` atualizado para chamar Orchestrate quando habilitado, com fallback determinístico.
- Resposta tipada com 5 tipos: `start | continue | review | celebrate | trail_1_review`.
- Nova função `celebrate_trail_completion(db, user_id, trail_id)` em `agents/catalyst.py`.
- Celebração inclui `celebration_message` (frase curta do Analista entregue pelo Catalisador) e `next_step_message`.
- Endpoint `GET /api/v1/journey/overview` retorna o novo formato de recomendação.
- Sinal `trail_1_review` disparado quando Analista detecta dificuldade em competências da Trilha 1 em usuários com `trail_1_auto_concluded=true`.

### Todo List
- [ ] Atualizar `build_recommendation()` em `agents/catalyst.py` para chamar Orchestrate e retornar 5 tipos.
- [ ] Implementar `celebrate_trail_completion(db, user_id, trail_id)` em `agents/catalyst.py`.
- [ ] Implementar lógica de `trail_1_review` em `analyst.py`: detecta dificuldade em competências de fase 1 para usuários com `trail_1_auto_concluded=true`.
- [ ] Atualizar `journey/router.py: GET /journey/overview` para incluir `celebrate` quando trilha for concluída.
- [ ] Atualizar testes em `test_agents_preparation.py` para os 5 tipos de recomendação.

### Relevant Context
- `backend/app/modules/agents/catalyst.py` — `build_recommendation()` existente (58 linhas).
- `backend/app/modules/agents/analyst.py` — `build_insight_from_competencies()`, `overall_insight()`.
- `backend/app/modules/journey/router.py` — endpoint overview.
- `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 5.2 e 5.3 — payloads e respostas.
- `docs/Especificacao_Agentes_IA_ELL_IBM.md` seções D-C11 a D-C13.

---

## Sub-tarefa 6 — Analista de Progresso como agente: análise em background e síntese de trilha

**Status:** [x] done

### Intent
Substituir os insights determinísticos do Analista por chamadas ao Orchestrate em background, e implementar `generate_trail_synthesis()` que produz a síntese de competências ao final de cada trilha (D-A1).

### Expected Outcomes
- Agente Analista criado no Orchestrate com instruções de análise pedagógica (D31, D8, D14).
- `build_insight_from_competencies()` atualizado para chamar Orchestrate em background com fallback.
- Nova função `generate_trail_synthesis(db, user_id, trail_id) -> TrailSynthesis` em `agents/analyst.py`.
- `TrailSynthesis` contém `short` (frase curta para Catalisador) e `full` (card do painel).
- `full` exposto via `GET /api/v1/progress/summary` como campo `trail_synthesis` por trilha concluída.
- Análise roda em background — não bloqueia resposta da atividade ao usuário.
- Testes cobrem: análise com reforço, análise sem reforço, síntese de trilha, fallback.

### Todo List
- [ ] Criar agente Analista no Orchestrate com instruções de análise pedagógica.
- [ ] Registrar `ORCHESTRATE_ANALYST_AGENT_ID` no `.env` e em `core/config.py`.
- [ ] Implementar chamada ao Orchestrate em `analyst.py: build_insight_from_competencies()` com fallback.
- [ ] Criar dataclass `TrailSynthesis` com campos `short: str` e `full: TrailSynthesisFull`.
- [ ] Implementar `generate_trail_synthesis(db, user_id, trail_id)` em `analyst.py`.
- [ ] Acionar `generate_trail_synthesis()` no evento de conclusão de trilha em `progress/service.py`.
- [ ] Persistir síntese em cache (campo JSONB `trail_synthesis` em `user_mission_progress` da última missão da trilha, ou nova tabela leve).
- [ ] Expor `trail_synthesis` no endpoint `GET /api/v1/progress/summary`.
- [ ] Atualizar testes relevantes.

### Relevant Context
- `backend/app/modules/agents/analyst.py` — funções existentes: `build_insight_from_competencies()`, `mission_insight()`, `overall_insight()`.
- `backend/app/modules/progress/service.py` — `apply_mission_completion()`, `record_competency_evidence()`.
- `backend/app/modules/conversations/orchestrate.py` — padrão de chamada ao Orchestrate com fallback.
- `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 4 — contrato de síntese de trilha.
- `docs/Especificacao_Agentes_IA_ELL_IBM.md` D-A1, D31.

---

## Sub-tarefa 7 — Modos de profundidade de trilha: Expresso / Padrão / Completo

**Status:** [x] done

### Intent
Implementar o filtro de atividades por modo de trilha (D-C10) — o backend usa `trail_modes` do perfil para exibir apenas as atividades relevantes para o modo daquela trilha (Expresso = só essenciais, Padrão = todas, Completo = todas + reforço).

### Expected Outcomes
- `get_active_activities_for_attempt()` (Sub-tarefa 2) respeita o `trail_mode` da trilha atual.
- Modo `express`: filtra apenas atividades ligadas a competências com `is_essential=true`.
- Modo `standard`: retorna todas as atividades (comportamento atual).
- Modo `full`: retorna todas as atividades + atividades de reforço (question_set=4, se existirem).
- Usuários sem `trail_modes` (perfis anteriores) usam `standard` como default.
- Testes cobrem os 3 modos e o fallback para `standard`.

### Todo List
- [ ] Criar função `get_trail_mode(profile, trail_id) -> str` em `agents/catalyst.py` — lê `trail_modes` do JSONB, default `"standard"`.
- [ ] Atualizar `get_active_activities_for_attempt()` para aceitar `trail_mode` e filtrar atividades.
- [ ] Para modo `express`: JOIN com `competencies` filtrando `is_essential=true`.
- [ ] Para modo `full`: incluir `question_set=4` se existir (seeds de reforço).
- [ ] Adicionar casos de teste para os 3 modos.

### Relevant Context
- `backend/app/modules/journey/service.py` — `get_active_activities_for_attempt()` (Sub-tarefa 2).
- `backend/app/shared/models.py` — `Activity`, `Competency` (campo `is_essential`), `Profile` (campo `trail` JSONB).
- `docs/Especificacao_Agentes_IA_ELL_IBM.md` D-C10 — definição dos 3 modos.

---

## Sub-tarefa 8 — Validação final e testes de segurança

**Status:** [ ] pending

### Intent
Executar todos os cenários de validação obrigatórios antes do piloto da Fase 1 (D10), garantindo segurança, confiabilidade pedagógica e integridade do sistema.

### Expected Outcomes
- Zero violações nos 10 cenários de segurança do Mentor (D8).
- Feedback do Mentor explica raciocínio e sugere próximo passo em ≥ 90% dos casos testados (D10).
- Fallback funciona: sistema apresenta conteúdo estático e não perde progresso quando Orchestrate cai.
- Rotação de conjuntos funciona: todos os 6 cenários da tabela em `CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md` passam.
- Suite de testes completa passa: `pytest -q` verde.

### Todo List
- [ ] Executar os 10 cenários de segurança do Mentor (pedidos de dados sensíveis, recomendações de investimento, dados desatualizados, etc.) e documentar em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.
- [ ] Testar o Mentor nas missões da Trilha 1 com respostas corretas, incorretas e ambíguas (mínimo 20 casos).
- [ ] Simular indisponibilidade do Orchestrate e verificar fallback para os 3 agentes.
- [ ] Verificar que nenhum agente altera pontos, desbloqueios ou registra conclusão diretamente.
- [ ] Executar `docker compose exec backend pytest -q` e confirmar suite verde.
- [ ] Executar `docker compose exec frontend npm run build` para confirmar build do frontend.
- [ ] Registrar resultado dos testes de segurança em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 7.

### Relevant Context
- `docs/Especificacao_Agentes_IA_ELL_IBM.md` D10 — critérios de avaliação.
- `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` seção 7 — checklist de verificação.
- `backend/tests/test_agents_preparation.py` — testes de preparação existentes.
- `docker-compose.yml` — comandos de verificação.

---

## Ordem de execução

```
Sub-tarefa 1 (migration) 
  └── Sub-tarefa 2 (rotação de perguntas)
        └── Sub-tarefa 3 (spike D7 — Mentor)
              ├── Sub-tarefa 4 (Catalisador onboarding)
              │     └── Sub-tarefa 5 (Catalisador presença contínua)
              └── Sub-tarefa 6 (Analista background + síntese)
                    └── Sub-tarefa 7 (modos de profundidade)
                          └── Sub-tarefa 8 (validação final)
```

Sub-tarefas 4, 5 e 6 podem começar em paralelo após Sub-tarefa 3. Sub-tarefa 7 depende das Sub-tarefas 1, 2 e 4.

---

## Contratos de variáveis de ambiente (adições ao .env.example)

```env
# Agentes Orchestrate (adicionados ao bloco existente)
ORCHESTRATE_CATALYST_AGENT_ID=
ORCHESTRATE_ANALYST_AGENT_ID=
# ORCHESTRATE_AGENT_ID existente passa a ser o Mentor
```
