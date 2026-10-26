# Plano — Estúdio de Prismas

**Status:** implementado  
**Decisões fechadas:**
- Moeda separada dos XP: **Prismas** (símbolo: ◆)
- Sem limite de gerações por dia
- Saldo não expira
- Exercícios extras entram no painel do Analista
- Biblioteca pessoal permanente

**Dependência:** o backend já tem `UserPoints` com `total_points` e `level`. As Prismas entram como coluna `coins` nessa mesma tabela.

---

## Visão geral

O Estúdio de Prismas é uma tela nova onde o usuário gasta Prismas acumuladas para pedir à IA que gere conteúdo personalizado de revisão baseado nos módulos que já cursou. Três formatos disponíveis: Revisão Narrativa, Flashcards e Exercícios Extras. O conteúdo gerado é salvo em uma biblioteca pessoal acessível a qualquer momento.

```
XP (total_points) → Progressão: níveis, conquistas, desbloqueio de fases
Prismas (coins)   → Combustível: gera conteúdo personalizado com a IA
```

---

## Onde Prismas são ganhas

| Evento | Prismas | Regra |
|---|---|---|
| Resposta correta em questão objetiva | +2 | Por questão, imediato; apenas na primeira vez que a atividade é acertada |
| Concluir módulo com 70–89% | +15 | Por conclusão aprovada; apenas na primeira aprovação |
| Concluir módulo com ≥ 90% | +25 | Bônus de excelência; apenas na primeira aprovação |
| Concluir uma fase inteira | +50 | Marco de fase, uma vez por fase |
| Onboarding concluído | +20 | Bônus único |

## Onde Prismas são gastas

| Formato | Custo |
|---|---|
| Revisão Narrativa | 30 Prismas |
| Flashcards | 20 Prismas |
| Exercícios Extras | 25 Prismas |

Ao concluir um conjunto de Exercícios Extras gerados, o usuário recebe +5 Prismas de volta.

---

## Sub-tarefas

---

### Sub-tarefa 1 — Backend: coluna `coins` e funções de Prismas

**Status:** `[x] done`

**Intent:**
Adicionar o campo `coins` à tabela `user_points` e criar as funções de crédito/débito que todos os outros módulos vão usar.

**Expected Outcomes:**
- `UserPoints.coins` existe no banco com padrão 0.
- `add_coins(db, user_id, amount)` credita Prismas e persiste.
- `spend_coins(db, user_id, amount)` debita Prismas; levanta `ValueError` se saldo insuficiente.
- `get_coins(db, user_id)` retorna saldo atual.
- `coins` aparece no retorno de `GET /progress/summary`.

**Todo List:**
1. Criar migration `0013_prism_economy.py`: `ALTER TABLE user_points ADD COLUMN coins INTEGER NOT NULL DEFAULT 0` e criação da tabela `generated_contents`.
2. Atualizar `UserPoints` em `shared/models.py` com o campo `coins`.
3. Criar `add_coins(db, user_id, amount)` em `progress/service.py`.
4. Criar `spend_coins(db, user_id, amount)` em `progress/service.py` — levanta `ValueError("saldo_insuficiente")` se `coins < amount`.
5. Atualizar `get_user_progress_summary` para incluir `coins` no retorno.
6. Atualizar `ProgressSummary` em `frontend/src/types/student.ts` com campo `coins: number`.

**Relevant Context:**
- `backend/app/shared/models.py` — modelo `UserPoints`
- `backend/app/modules/progress/service.py` — padrão de `add_points`
- `backend/alembic/versions/` — migration nova
- `frontend/src/types/student.ts` — interface `ProgressSummary`

---

### Sub-tarefa 2 — Backend: crédito de Prismas nos eventos existentes

**Status:** `[x] done`

**Intent:**
Conectar `add_coins` aos eventos que já existem: resposta correta, conclusão de módulo, conclusão de fase e onboarding. As Prismas seguem os mesmos pontos de controle que o XP — nenhuma lógica nova de negócio, apenas chamadas adicionais.

**Expected Outcomes:**
- Resposta correta em questão objetiva credita +2 Prismas imediatamente na resposta do submit.
- Conclusão de módulo com 70–89% credita +15; com ≥ 90% credita +25.
- Conclusão de fase credita +50.
- Onboarding credita +20.
- Os novos campos `coins_earned` e `coins` aparecem nos retornos de `submit` e `progress/summary`.
- Anti-farm: +2 só na primeira vez que a atividade é acertada; +15/+25 só na primeira aprovação do módulo. Refazer módulo já aprovado não duplica Prismas.

**Todo List:**
1. Em `submit_activity_response` (`journey/service.py`): após registrar resposta correta, chamar `add_coins(db, user_id, 2)`. Incluir `coins_earned` no retorno.
2. Em `apply_mission_completion` (`progress/service.py`): após calcular `score_percent`, chamar `add_coins` com 25 (excelência) ou 15 (aprovação). Incluir `coins_earned` no retorno da tupla.
3. Em `_check_phase_completion` (`progress/service.py`): chamar `add_coins(db, user_id, 50)` quando fase for concluída.
4. Em `grant_onboarding_bonus` (`progress/service.py`): chamar `add_coins(db, user_id, 20)`.
5. Atualizar `SubmitResponseOut` schema para incluir `coins_earned: int`.
6. Atualizar `SubmitResult` em `frontend/src/types/student.ts` com `coins_earned: number`.

**Relevant Context:**
- `backend/app/modules/journey/service.py` — `submit_activity_response`, `apply_mission_completion`
- `backend/app/modules/progress/service.py` — `_check_phase_completion`, `grant_onboarding_bonus`
- `backend/app/modules/journey/schemas.py` — `SubmitResponseOut`

---

### Sub-tarefa 3 — Backend: tabela e modelo de `GeneratedContent`

**Status:** `[x] done`

**Intent:**
Criar a tabela que persiste todo conteúdo gerado pelo Estúdio, servindo como biblioteca pessoal do usuário. O conteúdo em si é JSONB — flexível o suficiente para os três formatos sem precisar de tabelas separadas.

**Expected Outcomes:**
- Tabela `generated_contents` existe no banco.
- `GeneratedContent` mapeado como modelo SQLAlchemy.
- CRUD básico: criar, listar por usuário, buscar por id (com verificação de dono).

**Todo List:**
1. Criar a tabela na migration `0013_prism_economy.py` (a migration `0014_studio_responses.py` complementa o modelo liberando `mission_id` e `activity_id` nulos em `user_responses`):
   ```sql
   CREATE TABLE generated_contents (
     id          BIGSERIAL PRIMARY KEY,
     user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
     format      VARCHAR(30) NOT NULL,   -- revisao | flashcards | exercicios
     phase_id    INTEGER REFERENCES phases(id) ON DELETE SET NULL,
     mission_id  INTEGER REFERENCES missions(id) ON DELETE SET NULL,
     style_hint  TEXT,
     content     JSONB NOT NULL,
     coins_spent INTEGER NOT NULL DEFAULT 0,
     status      VARCHAR(20) NOT NULL DEFAULT 'generating',  -- generating | ready | failed
     created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
   );
   CREATE INDEX ON generated_contents (user_id, created_at DESC);
   ```
2. Criar modelo `GeneratedContent` em `shared/models.py`.
3. Criar `backend/app/modules/studio/` com `__init__.py` e `service.py`.
4. Implementar `create_generation(db, user_id, format, phase_id, mission_id, style_hint, coins_spent)` — cria com `status="generating"`, retorna o id.
5. Implementar `set_generation_ready(db, generation_id, content)` — salva o conteúdo e muda para `status="ready"`.
6. Implementar `set_generation_failed(db, generation_id)` — muda para `status="failed"` e devolve as Prismas.
7. Implementar `list_library(db, user_id, limit, offset)` — retorna biblioteca paginada.
8. Implementar `get_generation(db, user_id, generation_id)` — retorna item com verificação de dono.

**Relevant Context:**
- `backend/app/shared/models.py` — padrão de modelos existentes
- `backend/app/modules/agents/catalyst.py` — padrão de módulo de agente
- `backend/alembic/versions/` — migrations existentes como referência

---

### Sub-tarefa 4 — Backend: módulo do agente Mentor de Estúdio

**Status:** `[x] done`

**Intent:**
Criar `backend/app/modules/agents/studio_mentor.py` — o agente responsável por montar o payload para o Orchestrate e processar a resposta para cada formato. No MVP sem Orchestrate: retorna conteúdo de fallback estruturado e honesto, nunca simula uma resposta de IA.

**Expected Outcomes:**
- `build_studio_payload(format, phase, mission, style_hint, competencies, content_items, profile)` monta o payload completo para o Orchestrate.
- `build_fallback_content(format, phase_name, mission_name)` retorna conteúdo de fallback por formato, com mensagem clara de que a IA está em preparação.
- Interface pronta para substituição por chamada real ao Orchestrate.

**Todo List:**
1. Criar `backend/app/modules/agents/studio_mentor.py`.
2. Implementar `build_studio_payload(...)` → dict com campos:
   - `format`, `phase_number`, `mission_number` (nullable), `style_hint`
   - `competencies`: lista de `{code, name, status}` extraída do banco
   - `content_items`: lista de `{title, body}` dos itens publicados da missão/fase
   - `user_goal`, `knowledge_level`
3. Implementar `build_fallback_content(format, phase_name, mission_name)` → dict com estrutura válida por formato:
   - `revisao`: `{ type: "revisao", sections: [], summary: [] }`
   - `flashcards`: `{ type: "flashcards", cards: [] }`
   - `exercicios`: `{ type: "exercicios", questions: [] }`
   - Mensagem visível: "O Estúdio estará disponível assim que o Mentor for ativado."
4. Implementar `call_orchestrate(payload)` → `NotImplementedError` agora; substituído na Etapa 2.
5. Documentar no módulo o contrato exato esperado do Orchestrate por formato.

**Relevant Context:**
- `backend/app/modules/agents/catalyst.py` — padrão de módulo de agente
- `backend/app/modules/conversations/service.py` — padrão de chamada ao Orchestrate (fallback)
- `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md` — estrutura do conteúdo educacional

---

### Sub-tarefa 5 — Backend: router do Estúdio

**Status:** `[x] done`

**Intent:**
Expor os endpoints que o frontend precisa: solicitar geração, verificar status, acessar biblioteca e visualizar item gerado.

**Expected Outcomes:**
- `POST /studio/generate` — valida acesso/saldo, debita Prismas e retorna o conteúdo já pronto (geração síncrona no MVP). Com o Orchestrate indisponível, retorna `503` com a mensagem honesta e **não cobra** Prismas.
- `GET /studio/generate/{id}` — retorna item com `status` e `content` (quando ready).
- `GET /studio/library` — retorna lista paginada da biblioteca do usuário.
- Todos os endpoints exigem autenticação.
- Se saldo insuficiente: 402 com mensagem clara.
- Se fase/missão não cursada pelo usuário: 403.

**Todo List:**
1. Criar `backend/app/modules/studio/router.py`.
2. Criar schema `GenerateRequest`: `{ format, phase_id, mission_id (optional), style_hint (optional) }`.
3. Criar schema `GenerationOut`: `{ id, format, phase_name, mission_name, style_hint, content, status, coins_spent, created_at }`.
4. Criar schema `LibraryOut`: lista paginada com `{ items: GenerationOut[], total: int }`.
5. Implementar `POST /studio/generate`:
   - Verificar que o usuário cursou a fase/missão solicitada.
   - Verificar saldo de Prismas (`spend_coins` — levanta 402 se insuficiente).
   - Criar registro com `status="generating"`.
   - Chamar `studio_mentor.build_studio_payload` → `studio_mentor.call_orchestrate` → `validate_generated_content` → `set_generation_ready`.
   - Se o Orchestrate estiver desativado, retornar `503` antes de debitar qualquer Prisma.
   - Retornar o conteúdo gerado diretamente (geração síncrona no MVP).
6. Implementar `GET /studio/library`.
7. Implementar `GET /studio/generate/{id}`.
8. Registrar o router em `backend/app/main.py` sob `/api/v1/studio`.

**Relevant Context:**
- `backend/app/modules/journey/router.py` — padrão de router
- `backend/app/modules/studio/service.py` — funções criadas na sub-tarefa 3

---

### Sub-tarefa 6 — Backend: Exercícios Extras entram no Analista

**Status:** `[x] done`

**Intent:**
Quando o usuário responde Exercícios Extras gerados pelo Estúdio, as respostas devem alimentar `UserCompetencyProgress` — exatamente como atividades normais. Isso permite que o Analista leve essas evidências em conta no painel de progresso.

**Expected Outcomes:**
- `POST /studio/exercises/{generation_id}/submit` recebe resposta do usuário para cada questão gerada.
- O backend avalia a resposta (a questão gerada tem gabarito interno), registra `UserResponse` com `mission_attempt = 0` (sentinela para "exercício extra"), `mission_id` e `activity_id` nulos (migration `0014`) e chama a evidência de competência via código.
- Ao concluir todas as questões do conjunto, credita +5 Prismas.
- As competências vinculadas aparecem atualizadas no `GET /progress/summary`.

**Todo List:**
1. Definir contrato JSONB para questões de Exercícios Extras dentro de `content.questions`:
   ```json
   { "prompt": "...", "options": [...], "correct_answer": "b",
     "feedback_correct": "...", "feedback_incorrect": "...",
     "competency_codes": ["3.2.1"] }
   ```
2. Criar `POST /studio/exercises/{generation_id}/submit` no router.
3. Implementar `submit_studio_exercise(db, user_id, generation_id, question_index, response_data)` em `studio/service.py`.
4. Avaliar resposta com a mesma lógica de `_evaluate_response` (múltipla escolha).
5. Registrar `UserResponse` com `mission_id = NULL` e `mission_attempt = 0`.
6. Chamar `record_competency_evidence` com a atividade sintética.
7. Ao concluir todas as questões, chamar `add_coins(db, user_id, 5)`.
8. Retornar `{ is_correct, correct_answer, feedback, all_done, coins_earned }`.

**Relevant Context:**
- `backend/app/modules/journey/service.py` — `_evaluate_response`, `submit_activity_response`
- `backend/app/modules/progress/service.py` — `record_competency_evidence`
- `backend/app/shared/models.py` — `UserResponse` (verificar nullable de `mission_id`)

---

### Sub-tarefa 7 — Frontend: saldo de Prismas na topbar e `ProgressPage`

**Status:** `[x] done`

**Intent:**
Tornar as Prismas visíveis em dois lugares: na topbar do app (para o usuário sempre saber seu saldo) e na `ProgressPage` junto ao XP.

**Expected Outcomes:**
- Topbar do `StudentLayout` exibe `◆ {coins}` ao lado do nível do usuário.
- `ProgressPage` exibe saldo de Prismas com link "Ir para o Estúdio".
- `LessonPlayerPage` exibe `+2 ◆` em animação breve ao acertar uma questão.
- O contador de Prismas na topbar atualiza sem recarregar a página após cada acerto.

**Todo List:**
1. Atualizar `ProgressSummary` em `student.ts` com `coins: number` (sub-tarefa 1 já faz isso).
2. Criar componente `CoinsDisplay` em `design-system` ou `student/components`: recebe `coins: number`, exibe `◆ {coins}` com a cor coral/laranja do Catalisador (`#FCA048`).
3. Adicionar `CoinsDisplay` ao `StudentLayout` na topbar, lendo `coins` do store de sessão.
4. Em `LessonPlayerPage`, ao receber `coins_earned > 0` no resultado do submit, exibir animação `+{coins_earned} ◆` por 2s.
5. Atualizar `ProgressPage` para exibir o saldo de Prismas junto ao card de nível.
6. Adicionar ao store de sessão (`store/session.ts`) o campo `coins` e a ação `addCoins(n)`.

**Relevant Context:**
- `frontend/src/areas/student/StudentLayout.tsx`
- `frontend/src/areas/student/LessonPlayerPage.tsx`
- `frontend/src/areas/student/ProgressPage.tsx`
- `frontend/src/store/session.ts`
- `frontend/src/design-system/` — padrão de componentes

---

### Sub-tarefa 8 — Frontend: tela do Estúdio

**Status:** `[x] done`

**Intent:**
Criar `frontend/src/areas/student/StudioPage.tsx` — a tela principal do Estúdio onde o usuário escolhe módulo/fase, formato e estilo, vê o conteúdo gerado e acessa a biblioteca.

**Expected Outcomes:**
- Rota `/student/studio` registrada e protegida.
- Link "Estúdio" visível na navegação do `StudentLayout` (após "Mentor e agentes").
- Tela com três seções: formulário de geração, conteúdo gerado (resultado imediato), biblioteca pessoal.
- Estado de loading durante geração com mensagem do Mentor.
- Estado de saldo insuficiente com mensagem clara e link para a jornada.
- Fallback explícito quando Orchestrate indisponível: mostra mensagem e não consome Prismas.

**Todo List:**
1. Criar `StudioPage.tsx` com três abas ou seções: "Criar", "Minha Biblioteca".
2. Formulário de criação:
   - Dropdown: fases cursadas pelo usuário (filtradas do `GET /journey/overview`).
   - Dropdown: módulos da fase selecionada (opcional — pode pedir revisão da fase inteira).
   - Radio: formato (Revisão ◆30 / Flashcards ◆20 / Exercícios ◆25).
   - Input de texto: "Personalize o estilo" (placeholder: "ex.: analogia com doces, linguagem de games...").
   - Botão "Gerar" com saldo atual visível e custo destacado.
3. Ao submeter: loading state → exibir resultado inline.
4. Renderizadores por formato:
   - `RevisaoView`: seções com título e corpo, tópicos de resumo.
   - `FlashcardsView`: cards viraveis (frente/verso), contador, botão de avançar.
   - `ExerciciosView`: questões sequenciais com a lógica de avaliação do `QuestionStep` adaptada.
5. Biblioteca: lista de `GenerationOut` com tipo, fase, estilo e data, clicáveis para reabrir.
6. Registrar rota em `App.tsx` e adicionar ao `StudentLayout`.
7. Criar `frontend/src/api/studio.ts` com `generate()`, `getGeneration()`, `getLibrary()`, `submitExercise()`.

**Relevant Context:**
- `frontend/src/areas/student/MentorPage.tsx` — padrão de tela de agente
- `frontend/src/areas/student/LessonPlayerPage.tsx` — `QuestionStep` como referência para `ExerciciosView`
- `frontend/src/areas/student/StudentLayout.tsx` — navegação
- `frontend/src/api/index.ts` — padrão de camada de API

---

### Sub-tarefa 9 — Testes

**Status:** `[x] done`

**Intent:**
Cobrir as regras de negócio críticas: crédito/débito de Prismas, geração com saldo insuficiente, exercícios extras alimentando o Analista e não permitir gerar conteúdo de fase não cursada.

**Todo List:**
1. Teste unitário: `add_coins` e `spend_coins` — saldo insuficiente levanta `ValueError`.
2. Teste de integração: resposta correta no submit credita +2 Prismas no banco.
3. Teste de integração: conclusão de módulo credita Prismas corretas por faixa de score.
4. Teste de integração: `POST /studio/generate` com saldo insuficiente retorna 402.
5. Teste de integração: `POST /studio/generate` para fase não cursada retorna 403.
6. Teste de integração: exercício extra avaliado atualiza `UserCompetencyProgress`.
7. Teste de integração: concluir exercícios extras credita +5 Prismas.
8. Teste de integração: Prismas não são duplicadas ao refazer módulo já aprovado.

**Relevant Context:**
- `backend/tests/test_progression_api.py` — padrão de testes de integração existentes
- `backend/tests/test_gamification.py` — testes unitários de gamificação

---

## Ordem de execução recomendada

```
Sub-tarefa 1 (coins no banco)
        ↓
Sub-tarefa 2 (crédito nos eventos)
        ↓
Sub-tarefa 3 (tabela GeneratedContent)
Sub-tarefa 4 (agente studio_mentor)   ← paralelas
        ↓
Sub-tarefa 5 (router do Estúdio)
Sub-tarefa 6 (exercícios → Analista)  ← paralelas
        ↓
Sub-tarefa 7 (Prismas no frontend — topbar)
Sub-tarefa 8 (tela do Estúdio)        ← paralelas
        ↓
Sub-tarefa 9 (testes)
```

---

## Contrato de conteúdo gerado por formato (JSONB)

> O gabarito e os feedbacks de correção ficam armazenados no JSONB, mas a API
> remove esses campos de questões ainda não respondidas. Eles só aparecem
> depois da submissão do exercício extra.

### Revisão Narrativa
```json
{
  "type": "revisao",
  "title": "Revisão do Módulo 3 — analogia com doces",
  "sections": [
    { "title": "O orçamento como uma caixa de bombons", "body": "..." },
    { "title": "Reserva de emergência: o chocolate guardado", "body": "..." }
  ],
  "summary": ["Ponto 1", "Ponto 2", "Ponto 3"]
}
```

### Flashcards
```json
{
  "type": "flashcards",
  "cards": [
    { "front": "O que é reserva de emergência?", "back": "É o valor guardado para cobrir imprevistos sem comprometer o orçamento mensal." },
    { "front": "Quantos meses de gastos a reserva deve cobrir?", "back": "Entre 3 e 6 meses, dependendo da estabilidade da renda." }
  ]
}
```

### Exercícios Extras
```json
{
  "type": "exercicios",
  "questions": [
    {
      "prompt": "Qual desses gastos entra como necessidade no orçamento?",
      "options": [
        { "value": "a", "label": "Assinatura de streaming" },
        { "value": "b", "label": "Conta de luz" }
      ],
      "correct_answer": "b",
      "feedback_correct": "Correto. A conta de luz é um gasto essencial.",
      "feedback_incorrect": "A conta de luz é uma necessidade; streaming é um desejo.",
      "competency_codes": ["3.1.2"]
    }
  ]
}
```

---

## Payload para o Orchestrate (referência para Etapa 2)

```python
{
  "format": "flashcards",
  "phase_number": 3,
  "mission_number": 2,           # None = fase inteira
  "style_hint": "analogias a doces",
  "competencies": [
    { "code": "3.2.1", "name": "Reserva de emergência", "status": "developing" }
  ],
  "content_items": [
    { "title": "Por que poupar?", "body": "..." }
  ],
  "user_goal": "criar uma reserva para imprevistos",
  "knowledge_level": "beginner"
}
```

**Regra:** o backend controla tudo que entra no payload. O Orchestrate nunca acessa o banco diretamente.
