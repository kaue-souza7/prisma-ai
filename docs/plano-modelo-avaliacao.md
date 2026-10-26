# Plano — Novo modelo de avaliação dos módulos

**Status:** implementado  
**Escopo:** backend (regras de avaliação e conclusão), frontend (QuestionStep e SummaryStep) e contrato de tipos  
**Restrições respeitadas:**
- Sem mudança de schema de banco de dados além do estritamente necessário
- Regras de negócio permanecem no backend; frontend só exibe resultado
- A IA não concede pontos nem desbloqueios
- Sem punição permanente por inatividade ou por repetir módulo

---

## Visão geral

O modelo atual permite que o usuário erre, tente novamente na mesma questão e avance mesmo sem passar por todas as questões corretamente. O novo modelo funciona como uma **avaliação por módulo**:

1. O usuário escolhe uma alternativa e confirma — **não pode trocar** depois de confirmar.
2. Ao errar, vê qual era a correta e uma explicação, sem poder tentar a mesma questão de novo.
3. Avança para a próxima questão normalmente.
4. Ao final, o backend calcula o **percentual de acerto** da tentativa completa:
   - **≥ 90%** → passou com excelência; pode refazer por vontade própria, mas não é obrigado.
   - **≥ 70% e < 90%** → passou; pode avançar para o próximo módulo.
   - **< 70%** → não passou; deve refazer o módulo inteiro para desbloquear o próximo.
5. Refazer o módulo reseta as respostas da tentativa (nova tentativa) mas preserva o histórico de tentativas anteriores.

---

## Terminologia adotada

| Hoje | Novo nome |
|---|---|
| Minicurso | Módulo |
| Trilha | Fase (já era fase no backend) |

A renomeação é apenas visual (strings no frontend e textos das UIs). O campo `lesson_flow`, as rotas e os tipos de banco **não mudam**.

---

## Sub-tarefas

---

### Sub-tarefa 1 — Backend: modo "uma tentativa por questão"

**Status:** `[x] done`

**Intent:**  
Impedir que o usuário submeta uma segunda resposta para a mesma atividade dentro da mesma tentativa de módulo. Hoje `submit_activity_response` aceita N submissões para a mesma `activity_id`. O novo comportamento bloqueia a segunda submissão enquanto a tentativa do módulo ainda está em andamento.

**Expected Outcomes:**
- `POST /journey/missions/{id}/submit` retorna 409 se o usuário já respondeu aquela atividade na tentativa atual.
- O histórico de tentativas anteriores (de tentativas passadas do módulo inteiro) continua acessível.
- Refazer o módulo (nova tentativa) permite responder todas as atividades novamente.

**Todo List:**
1. Definir o conceito de "tentativa de módulo": um `attempt_number` no nível da missão, não da atividade. Usar `user_mission_progress.attempts` já existente como contador de tentativas do módulo.
2. Em `submit_activity_response`, antes de registrar, verificar se já existe `UserResponse` com `user_id`, `activity_id` e `mission_attempt = current_attempt`. Se sim, retornar 409 com mensagem clara.
3. Adicionar campo `mission_attempt: int` a `UserResponse` — valor padrão 1, preenchido com o valor atual de `user_mission_progress.attempts` (ou 1 se ainda não iniciada).
4. Criar migration adicionando coluna `mission_attempt INTEGER NOT NULL DEFAULT 1` em `user_responses`.
5. Ajustar `_evaluate_response` para expor a resposta correta no retorno quando `is_correct = False` — campo `correct_answer` (somente nesse momento, nunca antes da submissão).
6. Ajustar `apply_mission_completion` para calcular `score_percent` (acertos / total de atividades objetivas) em vez de só verificar se todas estão corretas.
7. Atualizar o retorno de `submit_activity_response` para incluir `correct_answer` quando errar e `score_percent` quando a missão for concluída.

**Relevant Context:**
- `backend/app/modules/journey/service.py` — `submit_activity_response()`, `_evaluate_response()`, `apply_mission_completion()`
- `backend/app/modules/progress/service.py` — `apply_mission_completion()`, `calculate_mission_score()`
- `backend/alembic/versions/` — nova migration necessária para `mission_attempt`
- `backend/app/shared/models.py` — modelo `UserResponse`

---

### Sub-tarefa 2 — Backend: regras de aprovação por percentual

**Status:** `[x] done`

**Intent:**  
Substituir a lógica binária de conclusão (todas corretas = passou) pelo modelo percentual. A missão é concluída se o usuário atingiu ≥ 70% de acerto nas atividades objetivas da tentativa atual. Open_text continua contando para conclusão sem penalizar a nota.

**Expected Outcomes:**
- Missão concluída quando `score_percent >= 70`.
- Campo `passed` no retorno do submit: `True` se ≥ 70%, `False` se abaixo.
- Campo `can_retry_optionally` no retorno: `True` se ≥ 90% (passou, mas pode refazer por vontade).
- Campo `must_retry` no retorno: `True` se < 70% (obrigado a refazer para avançar).
- Pontuação: 100 pts se ≥ 90% na primeira tentativa, 70 pts se entre 70–89%, sem pontos se < 70%.
- Desbloqueio da próxima missão: só ocorre se `passed = True`.

**Todo List:**
1. Em `apply_mission_completion`, calcular `correct_count / total_objective_activities` como `score_percent`.
2. Definir constantes `PASS_THRESHOLD = 70` e `EXCELLENCE_THRESHOLD = 90` em `progress/service.py`.
3. A missão só é marcada como `completed` se `score_percent >= PASS_THRESHOLD`.
4. Pontuação: `100` se `score_percent >= EXCELLENCE_THRESHOLD` e `attempt == 1`; `70` se passou mas não excelência ou não primeira tentativa.
5. Novo campo `score_percent` em `UserMissionProgress` — migration simples, nullable, float.
6. Retornar no submit: `{ score_percent, passed, must_retry, can_retry_optionally }`.
7. Atualizar `is_mission_unlocked` para checar `score_percent >= PASS_THRESHOLD` em vez de só `status == completed`.

**Relevant Context:**
- `backend/app/modules/progress/service.py` — `apply_mission_completion()`, `calculate_mission_score()`
- `backend/app/modules/journey/service.py` — `is_mission_unlocked()`
- `backend/alembic/versions/` — nova migration para `score_percent` em `user_mission_progress`

---

### Sub-tarefa 3 — Backend: endpoint de nova tentativa do módulo

**Status:** `[x] done`

**Intent:**  
Criar um endpoint que redefine o estado da missão para `in_progress` e incrementa o contador de tentativas, permitindo que o usuário responda todas as atividades novamente. O histórico de tentativas anteriores é preservado — apenas o `current_step` e `completed_steps` são resetados.

**Expected Outcomes:**
- `POST /journey/missions/{id}/retry` disponível e funcionando.
- Incrementa `user_mission_progress.attempts`.
- Reseta `current_step` para 0 e `completed_steps` para `[]`.
- Não apaga `UserResponse` anteriores — eles ficam marcados com `mission_attempt` anterior.
- Retorna 403 se a missão não pode ser refeita (ex: `can_retry_optionally = False` e `passed = True` — neste caso, o usuário não pode ser forçado a refazer).
- Retorna 409 se a missão não foi tentada ainda.

**Todo List:**
1. Criar `async def retry_mission(db, user_id, mission_id)` em `journey/service.py`.
2. Verificar que `user_mission_progress` existe e que `attempts >= 1`.
3. Se `score_percent >= PASS_THRESHOLD`: só permite retry se o frontend indicar que é voluntário (parâmetro `voluntary: bool` no body).
4. Incrementar `attempts`, resetar `current_step = 0`, `completed_steps = []`, `status = in_progress`.
5. Adicionar rota `POST /journey/missions/{id}/retry` em `journey/router.py`.
6. Adicionar `retryMission(id)` na camada de API do frontend (`api/index.ts`).

**Relevant Context:**
- `backend/app/modules/journey/service.py` — `start_mission()` como referência de padrão
- `backend/app/modules/journey/router.py`
- `frontend/src/api/index.ts`

---

### Sub-tarefa 4 — Frontend: QuestionStep — uma tentativa por questão

**Status:** `[x] done`

**Intent:**  
Remover o botão "Tentar novamente" do `QuestionStep`. Ao errar, mostrar a alternativa correta destacada, o feedback do Mentor e dois botões: "Continuar" e "Pedir ajuda ao Mentor". O usuário não pode mudar a resposta depois de confirmar.

**Expected Outcomes:**
- Após confirmar, todas as opções ficam `disabled` (já ocorre, mantido).
- Ao errar: a opção escolhida fica marcada como errada (vermelho) e a opção correta é revelada com destaque (verde) usando `correct_answer` retornado pelo backend.
- Bloco de feedback do Mentor exibido normalmente.
- Botão "Tentar novamente" removido.
- Botão "Continuar" presente sempre após confirmar (acerto ou erro).
- Botão "Pedir ajuda ao Mentor" presente sempre após confirmar.
- Barra de progresso do topo reflete questões respondidas (acerto + erro), não só acertos.

**Todo List:**
1. Em `SubmitResult`, adicionar campo `correct_answer?: string | null`.
2. Em `QuestionStep`, remover a função `retry()` e o botão associado.
3. Ao receber resultado com `is_correct = False`, ler `result.correct_answer` e aplicar CSS `optionCorrect` na opção correspondente.
4. Remover condicional que impedia "Continuar" após erro — sempre mostrar "Continuar" após confirmar.
5. Garantir que `onContinue` seja chamado independente de acerto ou erro.
6. Em `handleActivityResult` no `LessonPlayerPage`, remover a condição que só adicionava step aos `completed_steps` quando correto — todo step respondido conta como "feito" na barra de progresso.

**Relevant Context:**
- `frontend/src/areas/student/LessonPlayerPage.tsx` — `QuestionStep`, `handleActivityResult`
- `frontend/src/areas/student/LessonPlayer.module.css` — classes `optionCorrect`, `optionWrong`

---

### Sub-tarefa 5 — Frontend: SummaryStep — resultado percentual e retry

**Status:** `[x] done`

**Intent:**  
O `SummaryStep` precisa mostrar o resultado da avaliação com clareza: percentual de acerto, se passou ou não, e os botões corretos para cada situação. Quando `must_retry = True`, bloquear a navegação para o próximo módulo e mostrar apenas "Refazer módulo". Quando `passed = True`, mostrar próximo módulo e oferecer opcionalmente "Refazer".

**Expected Outcomes:**
- Exibir percentual de acerto em destaque: "Você acertou 8 de 10 questões (80%)".
- Exibir status: "Aprovado ✓" ou "Refaça para avançar ✗".
- Se `must_retry = True`: botão principal "Refazer módulo", sem link para próximo módulo.
- Se `passed = True` e `can_retry_optionally = True`: botão principal "Próximo módulo" + botão secundário "Refazer por vontade".
- Se `passed = True` e `can_retry_optionally = False` (70–89%): botão principal "Próximo módulo" + botão secundário "Refazer" (opcional).
- Ao clicar em "Refazer": chamar `journeyApi.retryMission(id)` e navegar para `stepIndex = 0` (recarregar o lesson).
- Manter o insight do Analista e o bloco de conquistas.

**Todo List:**
1. Atualizar `SubmitResult` e `Lesson` com os novos campos: `score_percent`, `passed`, `must_retry`, `can_retry_optionally`.
2. Atualizar `SummaryStep` para ler esses campos de `completion` ou `lesson`.
3. Implementar lógica de exibição condicional dos botões.
4. Implementar `handleRetry` no `LessonPlayerPage`: chama `retryMission`, reseta `stepIndex` para 0, recarrega os dados do lesson.
5. Passar `onRetry` como prop para `SummaryStep`.
6. Renomear "Minicurso" para "Módulo" em todas as strings visíveis ao usuário no `LessonPlayerPage`.

**Relevant Context:**
- `frontend/src/areas/student/LessonPlayerPage.tsx` — `SummaryStep`, `LessonPlayerPage`
- `frontend/src/types/student.ts` — `SubmitResult`, `Lesson`, `LessonStep`

---

### Sub-tarefa 6 — Frontend: renomear "Minicurso" → "Módulo" nas UIs

**Status:** `[x] done`

**Intent:**  
Atualizar todas as strings visíveis ao usuário que usam "minicurso" para "módulo". Não alterar nomes de rotas, campos de banco, chaves de API nem nomes de componentes — apenas texto na interface.

**Expected Outcomes:**
- Nenhuma ocorrência de "Minicurso" visível ao usuário nas páginas do estudante.
- Rotas, tipos TypeScript, nomes de componentes e campos de banco inalterados.

**Todo List:**
1. Buscar todas as ocorrências de "minicurso" (case-insensitive) nos arquivos `.tsx` e `.css` da área do estudante.
2. Substituir textos visíveis: "Minicurso concluído" → "Módulo concluído", "Preparando seu minicurso" → "Preparando seu módulo", etc.
3. Atualizar `useDocumentTitle` onde houver "Minicurso".
4. Atualizar a documentação `docs/MINICURSOS_TRILHAS_1_2.md` e `docs/MINICURSOS_TRILHAS_3_6.md` para refletir o novo nome (sem alterar o conteúdo técnico).
5. Atualizar as mensagens do backend que aparecem na UI (erros de módulo bloqueado e abertura do Mentor). A migration `0012` renomeia a cópia já publicada dentro de `lesson_flow`, sem alterar sua estrutura.

**Relevant Context:**
- `frontend/src/areas/student/LessonPlayerPage.tsx`
- `frontend/src/areas/student/JourneyPage.tsx`
- `frontend/src/areas/student/StudentHome.tsx`
- `docs/MINICURSOS_TRILHAS_1_2.md`

---

### Sub-tarefa 7 — Testes

**Status:** `[x] done`

**Intent:**  
Garantir que as novas regras de avaliação estejam cobertas por testes automatizados antes de considerar a implementação concluída.

**Todo List:**
1. Atualizar `backend/tests/test_progression_api.py`: testar que segunda submissão para mesma atividade retorna 409.
2. Adicionar teste: `score_percent < 70` → `passed = False`, `must_retry = True`, próxima missão bloqueada.
3. Adicionar teste: `score_percent` entre 70–89 → `passed = True`, `must_retry = False`, `can_retry_optionally = False`.
4. Adicionar teste: `score_percent >= 90` → `passed = True`, `can_retry_optionally = True`.
5. Adicionar teste: `POST /retry` incrementa `attempts` e reseta `current_step` e `completed_steps`.
6. Adicionar teste: refazer missão já aprovada voluntariamente não duplica pontos.
7. Atualizar testes de frontend (`LessonPlayerPage.test.tsx`) para refletir novo comportamento do `QuestionStep`.

**Relevant Context:**
- `backend/tests/test_progression_api.py`
- `frontend/src/areas/student/LessonPlayerPage.test.tsx`

---

## Ordem de execução recomendada

```
Sub-tarefa 1 → Sub-tarefa 2 → Sub-tarefa 3
                                    ↓
              Sub-tarefa 4 → Sub-tarefa 5 → Sub-tarefa 6 → Sub-tarefa 7
```

As sub-tarefas 1, 2 e 3 são de backend e devem ser feitas juntas (compartilham a migration). As sub-tarefas 4 e 5 dependem dos novos campos retornados pelo backend. A 6 é independente e pode ser feita a qualquer momento. A 7 fecha tudo.

---

## Campos novos no contrato de API

### `POST /journey/missions/{id}/submit` — resposta atualizada

```json
{
  "is_correct": false,
  "correct_answer": "b",
  "score": 0,
  "feedback": "O bruto ainda não sofreu os descontos...",
  "feedback_agent": "mentor",
  "attempt_number": 1,
  "reinforcement": null,
  "mission_completed": false,
  "attempt_finished": true,
  "points_earned": 0,
  "new_achievements": [],
  "score_percent": 0,
  "passed": false,
  "must_retry": true,
  "can_retry_optionally": false,
  "mission_insight": null,
  "next_step": null
}
```

`score_percent`, `passed`, `must_retry` e `can_retry_optionally` ficam não-nulos quando a tentativa termina (`attempt_finished = true`), isto é, quando todas as atividades da tentativa atual foram respondidas. `mission_completed` só é `true` quando a tentativa foi aprovada (`>= 70%`); por isso um módulo reprovado retorna os campos de avaliação com `mission_completed = false`, permitindo que a UI mostre o resultado e o botão de refazer.

`correct_answer` só é preenchido quando `is_correct = false`. O gabarito nunca aparece antes da submissão.

### `POST /journey/missions/{id}/retry` — body e resposta

```json
// body
{ "voluntary": false }

// resposta — igual ao UserMissionProgressOut existente
{ "mission_id": 1, "status": "in_progress", "score": null, "score_percent": 60, "attempts": 2, ... }
```

Regras de retry:
- Módulo reprovado (`must_retry = true`): sempre pode refazer.
- Módulo aprovado: só refaz com `voluntary = true`; retry não duplica pontos nem bloqueia novamente o próximo módulo.
- Módulo nunca iniciado: `409`.
- Respostas antigas permanecem no banco com o `mission_attempt` da tentativa a que pertencem.
