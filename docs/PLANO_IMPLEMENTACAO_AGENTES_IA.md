# Plano de Implementação — Agentes de IA no watsonx Orchestrate

**Data:** 28/10/2026  
**Status:** pronto para execução  
**Escopo:** integração real dos agentes Mentor, Catalisador e Analista; conteúdo e frontend necessários para a experiência completa  
**Substitui:** o status de integração do `agents-implementation-plan.md` e as afirmações otimistas de conclusão em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`

---

## Status de execução (28/10/2026)

| Fase | Status | Observação |
|---|---|---|
| 0 — Configuração | ✅ Concluída | UUIDs no `.env`, migrations 0017/0018 aplicadas, backend recriado |
| 1 — Cliente Orchestrate | ✅ Concluída | `backend/app/core/orchestrate_client.py` com IAM, retry, timeout, circuit breaker |
| 2 — Parsing | ✅ Concluída | `backend/app/core/orchestrate_parser.py` + testes |
| 3 — Mentor | ✅ Concluída | `status=available`, `source=orchestrate` validado via API |
| 4 — Catalisador | ✅ Concluída | Onboarding, next_step e celebrate validados; agente atualizado no Orchestrate |
| 5 — Analista | ✅ Concluída | Agente criado, insight com IA/cache, síntese persistida em `trail_syntheses` |
| 6 — Orquestração/latência | ✅ Concluída | Cache de recomendação, insight em background, síntese com sessão própria |
| 7 — Conteúdo/dados | ⚠️ Parcial | Conjuntos 2/3 gerados nas 12 trilhas via variantes; `question_set=4` ainda não existe |
| 8 — Frontend | ✅ Concluída | Síntese, celebração, selo, modos e onboarding conversacional com 10 fixas + até 8 adaptativas |
| 9 — Testes/segurança | ✅ Concluída | Suíte verde, contrato ao vivo e 10/10 cenários D8 sem violação |

### Pendências conhecidas

1. **Conteúdo:** os conjuntos 2 e 3 das Trilhas 2–12 foram gerados como **variantes** por `backend/scripts/backfill_question_sets.py` (alternativas embaralhadas, mesma pergunta-base). O time de conteúdo deve substituí-los por perguntas autorais. `question_set=4` (reforço do modo `full`) segue pendente.
2. **Onboarding conversacional:** implementado com as 10 perguntas fixas, até 8 perguntas adaptativas geradas pelo Catalisador e envio do histórico completo. A curadoria das perguntas adaptativas pode evoluir com o piloto.
3. **Teste de contrato ao vivo:** implementado em `backend/tests/test_orchestrate_live.py` (`ORCHESTRATE_LIVE_TEST=1`) e no workflow manual `.github/workflows/agents-live.yml`; basta configurar os secrets no GitHub.
4. **Segurança D8:** executada em 28/10/2026 (10/10 sem violação, em `docs/RELATORIO_SEGURANCA_D8.md`); repetir o harness a cada mudança de instruções do agente.
5. **Estúdio:** implementado com o agente `prisma_studio` (`ORCHESTRATE_STUDIO_AGENT_ID`). Gera `revisao`, `flashcards` e `exercicios` com validação de estrutura e fallback de refund. A qualidade pedagógica do conteúdo gerado deve ser revisada antes do piloto.

---

## 1. Objetivo

Colocar os três agentes de produto em operação real no watsonx Orchestrate, preservando as seguintes garantias:

1. O backend continua sendo a única autoridade sobre pontos, desbloqueios, conclusão de missão e conquistas.
2. Toda chamada de IA tem fallback determinístico quando o Orchestrate está desligado, indisponível, lento ou devolve resposta inválida.
3. O sistema funciona de ponta a ponta antes, durante e depois da integração.
4. Nenhum segredo é versionado no repositório.
5. A latência e o custo das chamadas de LLM são controlados por cache e por limites explícitos.

---

## 2. Diagnóstico de partida

O código já tem boa parte da estrutura, mas a integração com o Orchestrate está quebrada nos pontos fundamentais.

| Item | Estado real |
|---|---|
| Agente Mentor | Existe no Orchestrate e responde quando chamado corretamente |
| Agente Catalisador | Existe no Orchestrate, mas só tem instruções de onboarding |
| Agente Analista | **Não existe** no Orchestrate |
| Endpoint usado pelo backend | Errado (`/v1/chat`); o correto é `/v1/orchestrate/{uuid}/chat/completions` |
| Autenticação | Errada: envia a IBM Cloud API key crua como Bearer; falta troca por token IAM |
| Identificação do agente | Errada: usa nome; a API exige UUID no path |
| Parsing das respostas | Incompatível com `choices[0].message.content` e com JSON cercado por ```json``` |
| Container do backend | Rodando com `ORCHESTRATE_ENABLED=false` e sem URL/chave |
| Migração 0017 | Pendente (banco em 0016, head 0017) |
| Conjuntos de perguntas | Só a Trilha 1 tem os conjuntos 1, 2 e 3 |
| Modo `express` | Não filtra atividades; funciona como `standard` |
| Modo `full` | Não tem `question_set=4` semeado |
| Testes | 224 passed, 1 failed |
| Frontend | Não exibe `trail_modes`, selo de auto-conclusão, síntese de trilha nem celebração |
| Agentes versionados no repo | Não; `agents/` está vazio |
| Estúdio | `call_orchestrate()` ainda não implementado |

### Contrato real confirmado do Orchestrate

- Base: `ORCHESTRATE_URL` (URL da instância, sem `/v1`).
- Chat: `POST {ORCHESTRATE_URL}/v1/orchestrate/{agent_uuid}/chat/completions`.
- Auth: `Authorization: Bearer <token IAM>`.
- Corpo: `{"stream": false, "messages": [{"role": "user", "content": "<payload JSON>"}]}`.
- Resposta: texto em `choices[0].message.content`; `thread_id` no topo.
- O conteúdo pode vir como JSON puro, JSON interno ou JSON cercado por ```json ... ```.

---

## 3. Princípios de implementação

1. **Backend como autoridade:** agentes só produzem texto/estrutura; nunca escrevem no banco, nunca concedem pontos e nunca alteram progresso.
2. **Fallback sempre:** qualquer falha de IA devolve o comportamento determinístico atual.
3. **Cliente único:** um só módulo faz auth, chamada, timeout, retry e logging. Os três adaptadores não duplicam HTTP.
4. **Segredos fora do repo:** `ORCHESTRATE_API_KEY` fica apenas no `.env`; nunca em YAML, código, docs ou testes.
5. **Agentes versionados:** exportar YAMLs para `agents/` e manter um script de import/deploy.
6. **Custo e latência controlados:** nada de LLM em `GET` crítico sem cache; síntese e análise rodam em background.
7. **Segurança D8 em duas camadas:** instruções no agente + validação/limites no backend.

---

## 4. Fases de implementação

### Fase 0 — Preparação e configuração (0,5 dia)

- [ ] Confirmar os UUIDs dos agentes com `orchestrate agents list -v`.
- [ ] Adicionar ao `.env` e ao `.env.example`:
  - `ORCHESTRATE_AGENT_MENTOR_ID=<uuid>`
  - `ORCHESTRATE_CATALYST_AGENT_ID=<uuid>`
  - `ORCHESTRATE_ANALYST_AGENT_ID=<uuid>` (após criar o Analista)
- [ ] Manter `ORCHESTRATE_ENABLED=false` como padrão no `.env.example`.
- [ ] Aplicar a migração pendente: `docker compose exec backend alembic upgrade head`.
- [ ] Recriar o backend para carregar o `.env` atual: `docker compose up -d --force-recreate backend`.
- [ ] Confirmar que o container vê `ORCHESTRATE_ENABLED`, URL, chave e IDs.
- [ ] Criar as flags por agente (recomendado):
  - `ORCHESTRATE_MENTOR_ENABLED`
  - `ORCHESTRATE_CATALYST_ENABLED`
  - `ORCHESTRATE_ANALYST_ENABLED`
  - Cada uma com fallback para `ORCHESTRATE_ENABLED`.

**Critério de saída:** o backend sobe com Orchestrate desligado e a suíte atual continua passando (exceto o teste já quebrado, tratado na Fase 7).

---

### Fase 1 — Cliente Orchestrate único (1–2 dias)

Criar um módulo compartilhado, por exemplo `backend/app/modules/agents/orchestrate_client.py` (ou `backend/app/core/orchestrate.py`).

- [ ] Implementar troca de IBM Cloud API key por token IAM:
  - `POST https://iam.cloud.ibm.com/identity/token`
  - `grant_type=urn:ibm:params:oauth:grant-type:apikey`
  - Cache em memória com expiração e margem de renovação (ex.: 5 min).
- [ ] Implementar `chat_completion(agent_id, payload, thread_id=None) -> dict`:
  - Monta `messages` com o payload serializado em JSON.
  - Usa `/v1/orchestrate/{agent_id}/chat/completions`.
  - Envia `stream: false`.
  - Devolve o JSON bruto da resposta.
- [ ] Implementar tratamento de erros:
  - `401` → renova o token e tenta uma vez.
  - `429`/`5xx` → retry com backoff limitado.
  - timeout → erro tipado para o fallback.
  - resposta sem `choices` → erro `empty_response`.
- [ ] Adicionar logging estruturado: agente, status HTTP, latência, `trace_id`, tipo de erro (sem conteúdo sensível).
- [ ] Adicionar health check opcional do Orchestrate para o endpoint de contexto do Mentor.
- [ ] Substituir as três implementações duplicadas de HTTP por esse cliente.

**Contrato interno sugerido:**

```python
async def chat_completion(
    *,
    agent_id: str,
    payload: dict,
    thread_id: str | None = None,
    timeout: float | None = None,
) -> dict:
    ...
```

**Critério de saída:** um teste unitário com mock HTTP prova auth, URL, corpo e tratamento de erros sem chamar a rede real.

---

### Fase 2 — Extração e validação de resposta (1 dia)

Criar um extrator único, por exemplo `extract_agent_content(response) -> str | None` e `extract_agent_json(response) -> dict | None`.

- [ ] Ler `choices[0].message.content`.
- [ ] Aceitar também `content`, `output` e `response` no topo, para compatibilidade.
- [ ] Remover cercas markdown (```json ... ```).
- [ ] Extrair JSON quando houver texto antes/depois.
- [ ] Expandir JSON interno quando o conteúdo for uma string JSON.
- [ ] Devolver `None` quando não houver conteúdo utilizável.
- [ ] Atualizar os parsers:
  - `conversations/orchestrate.py` → `_extract_text` (Mentor)
  - `agents/catalyst.py` → `_parse_catalyst_response`, `build_recommendation`, `celebrate_trail_completion`
  - `agents/analyst.py` → `_request_analyst_insight`, `generate_trail_synthesis`
- [ ] Validar o schema de cada resposta antes de persistir ou exibir:
  - Mentor: `content` string e `suggestions` lista.
  - Catalisador onboarding: `phase_order`, `trail_modes`, `trail_1_auto_concluded`, `rationale`, `next_message`, `focus_areas`.
  - Catalisador next_step: `tipo`, `mensagem`, `missao_id`, `rationale`.
  - Catalisador celebrate: `celebration_message`, `next_step_message`, `badge_label`.
  - Analista insight: `severity`, `action`, `competencies`, `message`.
  - Analista síntese: `short`, `full`.
- [ ] Em qualquer schema inválido, cair no fallback e registrar o motivo.

**Critério de saída:** testes cobrem JSON puro, JSON cercado, texto antes/depois, resposta vazia e resposta inválida.

---

### Fase 3 — Mentor (0,5–1 dia)

- [ ] Ligar `request_mentor_reply()` ao cliente único.
- [ ] Expandir o JSON interno do Mentor (`content` + `suggestions`).
- [ ] Garantir `status` correto:
  - `preparing` quando desligado.
  - `available` quando a resposta tem conteúdo válido.
  - `unavailable` em erro/timeout/resposta vazia.
- [ ] Manter a janela de mensagens e o `mission_id` como estão.
- [ ] Adicionar `thread_id` opcional para multi-turn (recomendado).
- [ ] Testar:
  - chat geral;
  - chat com missão;
  - missão inexistente;
  - Orchestrate desligado;
  - 401, 404, timeout e resposta vazia;
  - fallback persistido no histórico.

**Critério de saída:** `POST /api/v1/conversations/mentor` retorna `status=available` e `source=orchestrate` com o agente real, e continua funcionando com o Orchestrate desligado.

---

### Fase 4 — Catalisador (2–3 dias)

#### 4.1 Instruções do agente

- [ ] Completar as instruções vivas do `prisma_catalyst` com os formatos de resposta para:
  - `action: onboarding` (já existe);
  - `action: next_step`;
  - `action: celebrate_trail`.
- [ ] Definir explicitamente os tipos de recomendação: `start`, `continue`, `review`, `celebrate`, `trail_1_review`.
- [ ] Definir que o agente nunca concede pontos/desbloqueios e nunca inventa dados de progresso.
- [ ] Exportar o YAML para `agents/prisma_catalyst.yaml`.

#### 4.2 Onboarding

- [ ] Adicionar `conversation_history` ao schema `OnboardingComplete` e ao router `POST /users/me/onboarding`.
- [ ] Fazer `conduct_onboarding()` usar o cliente único e o extrator único.
- [ ] Persistir `trail_modes`, `trail_1_auto_concluded`, `rationale`, `next_message` e `focus_areas`.
- [ ] Garantir que `apply_generated_trail()` valide a ordem contra as fases ativas.
- [ ] Aplicar a migração 0017 e garantir 50 XP + conquista quando `trail_1_auto_concluded=true`.
- [ ] Decidir se o onboarding conversacional completo entra no MVP:
  - **Se sim:** criar a UI de conversa com as perguntas fixas + adaptativas e enviar o histórico.
  - **Se não:** manter o formulário atual e documentar que o onboarding é “assistido”, não conversacional.

#### 4.3 Próximo passo e celebração

- [ ] Fazer `build_recommendation()` usar o cliente único e o parser único.
- [ ] Adicionar cache de recomendação por usuário/trilha/missão com TTL curto, ou gerar em eventos (conclusão de missão) e ler do cache no overview.
- [ ] Acionar `celebrate_trail_completion()` quando a trilha for concluída pela primeira vez.
- [ ] Incluir a celebração no `GET /journey/overview` ou no retorno de conclusão da missão.
- [ ] Garantir que `trail_1_review` apareça também no fallback determinístico.
- [ ] Exportar o agente e testar os três fluxos.

**Critério de saída:** onboarding, recomendação e celebração retornam `source=ai` quando ligados e fallback quando desligados; a Home não fica bloqueada esperando LLM.

---

### Fase 5 — Analista (2–3 dias)

- [ ] Criar o agente `prisma_analyst` no Orchestrate com instruções para:
  - `action: insight` (formato D14: 1 frase de dificuldade + 1 de ação);
  - `action: trail_synthesis` (formato D-A1: `short` + `full`);
  - regras D8 e limites pedagógicos.
- [ ] Exportar para `agents/prisma_analyst.yaml`.
- [ ] Registrar o UUID em `ORCHESTRATE_ANALYST_AGENT_ID`.
- [ ] Ligar `mission_insight()` e `overall_insight()` à versão assíncrona com IA.
- [ ] Implementar cache/persistência da síntese:
  - Opção A: nova tabela leve `trail_synthesis` (`user_id`, `trail_id`, `short`, `full`, `source`, `generated_at`).
  - Opção B: JSONB em `user_mission_progress` da última missão da trilha.
  - A opção A é mais limpa e evita acoplamento.
- [ ] Gerar a síntese apenas na primeira conclusão da trilha.
- [ ] Rodar a geração em background com **sessão de banco própria**, não com a sessão do request.
- [ ] Nunca chamar LLM dentro de `GET /progress/summary`; ler apenas o cache.
- [ ] Expor `trail_synthesis` no summary.
- [ ] Testar insight com/sem reforço, síntese, cache e fallback.

**Critério de saída:** o Analista de IA participa dos insights e da síntese, mas o painel de progresso continua rápido e funciona sem Orchestrate.

---

### Fase 6 — Orquestração, latência e resiliência (1–2 dias)

- [ ] Revisar todos os pontos que chamam LLM em caminho de request:
  - `GET /journey/overview` → cache ou evento.
  - `GET /progress/summary` → cache.
  - `POST /journey/missions/{id}/submit` → apenas o necessário; análise em background.
  - `POST /users/me/onboarding` → chamada única aceitável.
  - `POST /conversations/mentor` → chamada única aceitável.
- [ ] Definir timeouts por tipo:
  - chat do Mentor: 15s;
  - onboarding: 20s;
  - recomendação: 5–8s com cache;
  - análise/síntese: background.
- [ ] Adicionar fallback explícito para cada agente.
- [ ] Adicionar circuit breaker simples ou limite de falhas consecutivas (opcional, mas recomendado).
- [ ] Garantir que nenhuma chamada de IA seja feita quando a flag do agente está desligada.
- [ ] Adicionar logs/métricas de latência e taxa de fallback.

**Critério de saída:** nenhum `GET` crítico depende de LLM; o sistema se mantém responsivo com o Orchestrate lento ou fora.

---

### Fase 7 — Conteúdo, dados e testes quebrados (3–5 dias)

- [ ] Aplicar a migração 0017 e confirmar a conquista `trilha_1_dominada_onboarding`.
- [ ] Corrigir o teste `test_phase_achievement_requires_all_three_seeded_missions`:
  - buscar o conjunto ativo da tentativa;
  - obter as respostas corretas do conjunto;
  - não assumir ordem fixa.
- [ ] Criar os conjuntos `question_set=2` e `3` para as trilhas 2–12 (hoje só a Trilha 1 tem).
- [ ] Definir se o modo `full` terá `question_set=4`:
  - **Se sim:** semear atividades de reforço.
  - **Se não:** documentar que `full` = `standard` por enquanto e remover a expectativa do contrato.
- [ ] Corrigir o modo `express` para filtrar de verdade:
  - obter os `competency_codes` essenciais da missão;
  - manter apenas atividades cujo `content.competency_codes` intersecta os essenciais;
  - se o filtro esvaziar a missão, cair para `standard`.
- [ ] Garantir que a rotação registre `user_mission_attempts` também quando houver um único conjunto (ou documentar a exceção).
- [ ] Rodar os 6 cenários de rotação da especificação.
- [ ] Confirmar que refazer missão não duplica pontos.

**Critério de saída:** rotação, modos e conquistas funcionam em todas as trilhas; a suíte fica verde.

---

### Fase 8 — Frontend (3–5 dias)

- [ ] Atualizar `frontend/src/types/student.ts`:
  - `Trail`: `trail_modes`, `trail_1_auto_concluded`, `next_message`.
  - `ProgressSummary`: `trail_synthesis`.
  - `CatalystRecommendation`: tipos `celebrate` e `trail_1_review` e campos de celebração.
- [ ] Onboarding:
  - se conversacional: criar a UI de conversa e enviar `conversation_history`;
  - se não: exibir `next_message` e o selo de auto-conclusão.
- [ ] Progresso:
  - renderizar o card “O que você demonstrou saber” com `trail_synthesis.full`;
  - exibir o selo “Dominada no onboarding”.
- [ ] Home/Jornada:
  - renderizar celebração quando `kind=celebrate`;
  - renderizar `trail_1_review` com CTA para revisar a Trilha 1;
  - exibir o modo da trilha (express/standard/full) quando útil.
- [ ] Ajustar mocks/testes do frontend para os novos campos.
- [ ] Garantir que o fallback visual continue funcionando quando o status for `preparing`/`unavailable`.

**Critério de saída:** todas as saídas novas dos agentes têm representação visual; nada quebra quando o Orchestrate está desligado.

---

### Fase 9 — Testes, segurança e rollout (2–3 dias)

- [ ] Adicionar testes de adaptador com `httpx.MockTransport`/`respx`:
  - 200 com `choices` e JSON puro;
  - 200 com JSON cercado;
  - 401 → renovação de token;
  - 404, 500, timeout e resposta vazia → fallback;
  - resposta sem `suggestions` → sugestões padrão.
- [ ] Adicionar teste de contrato opt-in (`ORCHESTRATE_LIVE_TEST=1`) que chama os três agentes reais.
- [ ] Executar os 10 cenários de segurança D8 do Mentor e documentar em `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.
- [ ] Testar o Mentor em missões da Trilha 1 com respostas corretas, incorretas e ambíguas (mínimo 20 casos).
- [ ] Simular indisponibilidade do Orchestrate e validar fallback dos três agentes.
- [ ] Verificar que nenhum agente altera pontos, desbloqueios ou conclusão.
- [ ] Rodar `pytest -q` e o build do frontend.
- [ ] Atualizar a documentação para refletir o estado real.
- [ ] Fazer rollout gradual: Mentor → Catalisador onboarding → Catalisador recomendação/celebração → Analista.

**Critério de saída:** suíte verde, D8 documentado, agentes versionados e rollback por flag disponível.

---

## 5. Ordem de execução e dependências

```text
Fase 0 (config + migration)
  └── Fase 1 (cliente Orchestrate)
        └── Fase 2 (parsing)
              ├── Fase 3 (Mentor)
              ├── Fase 4 (Catalisador)
              └── Fase 5 (Analista)
                    └── Fase 6 (orquestração/latência)
                          ├── Fase 7 (conteúdo/dados)
                          └── Fase 8 (frontend)
                                └── Fase 9 (testes/segurança/rollout)
```

Paralelizações possíveis:

- Fase 7 (conteúdo) pode começar em paralelo à Fase 4/5.
- Fase 8 (frontend) pode começar depois que os contratos de API estiverem estáveis (final da Fase 4/5).
- Fase 9 depende de todas as anteriores.

---

## 6. Definition of Done

- [ ] `POST /api/v1/conversations/mentor` retorna `status=available` e `source=orchestrate` com o agente real.
- [ ] Onboarding retorna `source=ai`, `trail_modes`, `trail_1_auto_concluded` e `next_message`.
- [ ] `trail_1_auto_concluded=true` concede 50 XP e a conquista correspondente.
- [ ] `GET /journey/overview` retorna recomendação `start`, `continue`, `review`, `celebrate` ou `trail_1_review` sem bloquear por LLM.
- [ ] `GET /progress/summary` retorna `trail_synthesis` cacheada e não chama LLM a cada request.
- [ ] Celebração de trilha é acionada uma única vez.
- [ ] Fallback funciona com `ORCHESTRATE_ENABLED=false` e com falha simulada.
- [ ] Nenhum agente altera progresso/pontos/desbloqueios.
- [ ] Agentes exportados em `agents/*.yaml` e importáveis.
- [ ] `pytest -q` verde.
- [ ] Testes de segurança D8 documentados.
- [ ] Frontend exibe os novos campos e continua funcionando em fallback.

---

## 7. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Token IAM expirar em produção | Chamadas falham após 1h | Cache + renovação automática + retry no 401 |
| Agente responder formato inesperado | Fallback constante | Extrator tolerante + validação de schema + testes de contrato |
| Latência alta no overview | Home lenta | Cache por evento/TTL + timeout curto |
| Custo alto de LLM no progresso | Muitas chamadas por usuário | Síntese persistida e gerada só na conclusão |
| Sessão de banco fechada em background | Task falha silenciosamente | Sessão própria + tratamento de exceção |
| Instruções do agente divergirem do backend | Regressão funcional | YAML versionado + teste de contrato opt-in |
| Conteúdo incompleto nas trilhas 2–12 | Rotação não funciona | Semear conjuntos ou documentar limitação |
| Segurança D8 insuficiente | Risco pedagógico/reputacional | Instruções no agente + validação no backend + 10 cenários |
| Rollout tudo-ou-nada | Falha afeta todos os agentes | Flags por agente |

---

## 8. Comandos de verificação

```bash
# Ambiente e agentes
orchestrate env list
orchestrate agents list -v

# Banco
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current

# Backend
docker compose up -d --force-recreate backend
docker compose exec backend pytest -q

# Frontend
docker compose exec frontend npm test -- --run
docker compose exec frontend npm run build

# Logs
docker compose logs -f backend
```

---

## 9. Decisões pendentes antes da execução

1. **Onboarding conversacional entra no MVP?**
   - Se sim, a Fase 4 e a Fase 8 crescem bastante.
   - Se não, manter o formulário atual e documentar o escopo.
2. **Um agente Catalisador com múltiplas ações ou agentes separados?**
   - Um agente com instruções por ação é mais simples de operar.
   - Agentes separados reduzem risco de confusão de formato.
3. **Onde persistir a síntese de trilha?**
   - Recomendado: nova tabela leve.
4. **O modo `full` terá atividades de reforço (`question_set=4`)?**
   - Se não, remover a promessa do contrato por enquanto.
5. **O Mentor de Estúdio entra neste ciclo?**
   - Hoje ele quebra quando o Orchestrate é ligado; se ficar fora, manter o Estúdio bloqueado de forma explícita.

---

## 10. Fora de escopo

- Redesign de frontend além dos campos necessários.
- Novos fluxos de autenticação.
- Open Finance.
- Áudio.
- Reengajamento por inatividade.
- Avaliação semântica de respostas abertas pelo Mentor.

---

## 11. Mascotes 3D (integração concluída)

- Os três GLBs (`catalisador.glb`, `mentor.glb`, `analista.glb`) e o `manifest.json` ficam em `backend/app/static/mascotes/` e são servidos por `GET /static/mascotes/*` no FastAPI existente.
- O frontend usa `frontend/src/features/mascots/Mascot3D.tsx`, que carrega o viewer Three.js sob demanda e usa o `PrismMascot` como fallback sem WebGL/testes.
- Integrações ativas: landing page (cards dos três agentes), Onboarding, Home, Mentor, introdução/feedback/resumo da aula e painel de progresso.
- O piso escuro do demo foi desativado (`showFloor=false`) para o mascote aparecer transparente no tema do app.
- Documentação: `docs/mascotes-3d/INTEGRACAO_APP.md`, `INVENTARIO_ANIMACOES.md`, `INTEGRACAO.md` e `THIRD_PARTY_NOTICES.md`.
