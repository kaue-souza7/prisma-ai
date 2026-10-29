# Relatório detalhado dos agentes — Prisma.AI

**Data:** 28/10/2026  
**Escopo:** comportamento real dos agentes no código atual (`backend/app`), pontos de acionamento, cenários normais e de exceção, limites e diferenças em relação à especificação.  
**Método:** leitura do código de backend, rotas, serviços, testes e telas do frontend que consomem as saídas dos agentes.

---

## 1. Resumo executivo

O produto tem **três agentes de produto** e **um agente auxiliar de geração de conteúdo**:

| Agente | Tipo no código atual | Estado real | Onde vive |
|---|---|---|---|
| **Catalisador** | Lógica determinística, síncrona | Implementado | `backend/app/modules/agents/catalyst.py` |
| **Analista de Progresso** | Lógica determinística, calculada sob demanda | Implementado (sem IA e sem job em background) | `backend/app/modules/agents/analyst.py` |
| **Mentor** | Adaptador para o watsonx Orchestrate + fallback | Chat e persistência reais; IA depende do Orchestrate | `backend/app/modules/conversations/` |
| **Mentor de Estúdio** | Contrato de geração de conteúdo | Contrato pronto; geração real não implementada | `backend/app/modules/agents/studio_mentor.py` |

### O que isso significa na prática

1. **Nenhum agente é autônomo.** Não existe loop, fila, scheduler, worker ou chamada em background. Todo agente é acionado por uma requisição HTTP do usuário ou por uma leitura de tela.
2. **O backend é a autoridade.** Nenhum agente escreve no banco diretamente, concede pontos, desbloqueia fases ou altera progresso. O Catalisador e o Analista são funções do backend; o Mentor só produz texto.
3. **O Catalisador é 100% determinístico.** Ele não usa IA, mesmo com `ORCHESTRATE_ENABLED=true`.
4. **O Analista também é 100% determinístico no MVP.** Ele é recalculado a cada resposta/consulta, não “roda em background”.
5. **O Mentor é o único que pode fazer chamada externa.** Ele usa `ORCHESTRATE_URL` e `ORCHESTRATE_API_KEY`; sem integração, devolve fallback honesto.
6. **O Estúdio nunca gera conteúdo hoje.** `call_orchestrate()` levanta `NotImplementedError` de forma incondicional. Com Orchestrate “ligado”, a requisição falha, devolve as Prismas e retorna 502.

> Os diretórios `agents/`, `tools/`, `connections/`, `knowledge-bases/`, `models/` e `toolkits/` na raiz estão vazios. Eles são apenas a estrutura do workspace do watsonx Orchestrate ADK (`workspace_config.yaml`); não há definição de agente importada neles.

---

## 2. Modelo de execução

### 2.1 Fluxo geral

```
Usuário → Frontend → Rota FastAPI → Serviço do backend
                                      ├── Catalisador (regras)
                                      ├── Analista (regras)
                                      ├── Mentor (adaptador Orchestrate)
                                      └── Mentor de Estúdio (contrato, sem chamada real)

Backend valida, persiste estado, calcula pontos/desbloqueios e devolve a resposta.
```

### 2.2 Regras transversais

- O backend monta todo o contexto enviado aos agentes; nenhum agente consulta o banco.
- O backend decide **quando** cada agente é chamado.
- O Mentor não participa de pontuação, desbloqueio, conclusão de missão ou conquistas.
- O Catalisador não concede desbloqueios: ele sugere/ordena; o backend valida e aplica.
- O Analista não altera estado: ele lê evidências já registradas e produz um parecer.
- Não há comunicação direta Mentor ↔ Analista. O backend agrega os dados.
- Falhas de IA não devem derrubar o fluxo: o chat tem fallback; o Estúdio devolve Prismas.

### 2.3 Estado da configuração no ambiente atual

O arquivo `.env` está com:

```env
ORCHESTRATE_ENABLED=true
ORCHESTRATE_URL=https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/...
ORCHESTRATE_API_KEY=<preenchida>
ORCHESTRATE_AGENT_ID=
```

Porém, o container `ell_ibm_backend` em execução foi criado com a configuração anterior e hoje reporta:

```env
ORCHESTRATE_ENABLED=false
ORCHESTRATE_URL=
ORCHESTRATE_API_KEY=
```

Consequências:

- **Agora**, o Mentor responde com status `preparing` e o Estúdio devolve 503 sem cobrar Prismas.
- **Após recriar o container** (`docker compose up -d --force-recreate backend`), o comportamento muda: o Mentor passa a tentar a chamada real e o Estúdio passa a cobrar e falhar com 502/refund, porque `call_orchestrate()` ainda não foi implementado.
- `ORCHESTRATE_AGENT_ID` existe na configuração, mas **não é usado em nenhum lugar do código**.

---

## 3. Catalisador

### 3.1 Papel

Personalizar a trilha, ordenar as fases, explicar o próximo passo, sugerir revisão quando o Analista sinaliza dificuldade e reconhecer progresso. No código atual, ele não celebra conclusão de trilha nem gera síntese.

### 3.2 Onde é acionado

| Evento | Função | O que faz |
|---|---|---|
| Conclusão do onboarding | `users.service.complete_onboarding()` → `catalyst.build_trail()` | Gera e persiste a trilha inicial |
| Reenvio do onboarding | `users.service.complete_onboarding()` | Se já concluído e sem trilha, faz backfill; se já tem trilha, não altera nada |
| Alteração de preferência de trilha | `users.service.set_trail_preference()` | Reconstrói a trilha personalizada ou volta à ordem padrão |
| Leitura da trilha | `GET /users/me/trail`, `GET /users/me` | Enriquece a trilha com nome/descrição das fases |
| Home | `GET /journey/overview` | Devolve `recommendation` |
| Jornada | `GET /journey/overview` e `/journey/phases/my-progress` | Ordena fases e verifica desbloqueios |
| Abertura de missão/aula | `journey.service` | Usa a ordem da trilha para verificar desbloqueio |
| Conclusão de missão | `journey.service.submit_activity_response()` | Calcula `next_step` |
| Retomada de aula concluída | `GET /journey/missions/{id}/lesson` | Devolve `next_step` e `mission_insight` |
| Perfil | `GET /users/me` | Devolve a trilha enriquecida |

### 3.3 Regras de geração da trilha

#### Categorias de objetivo

| `goal_category` | Ordem inicial |
|---|---|
| `primeiro_salario` | `[1,2,3,4,5,6,7,8,9,10,11,12]` |
| `dividas` | `[7,8,1,2,3,4,5,6,9,10,11,12]` |
| `credito_juros` | `[7,8,4,1,2,3,5,6,9,10,11,12]` |
| `reserva` | `[5,6,1,2,3,4,7,8,9,10,11,12]` |
| `investimentos` | `[5,6,7,9,10,1,2,3,4,8,11,12]` |
| `protecao_digital` | `[11,3,4,1,2,5,6,7,8,9,10,12]` |
| `outro` ou ausente/inválida | `[1..12]` |

#### Ajustes por contexto de vida

Só se aplicam quando a categoria é `primeiro_salario` ou `outro`:

| `life_context` | Ordem |
|---|---|
| `primeiro_emprego` | `[1..12]` |
| `ja_trabalho` | `[1..12]` |
| `autonomo_freelancer` | `[2,6,3,1,5,4,7,8,9,10,11,12]` |
| `estudante_sem_renda` | `[5,6,1,2,3,4,7,8,9,10,11,12]` |

#### Ajuste por urgência

Se `urgency == "agora_preciso"` e a categoria é `outro` ou `primeiro_salario`, e a primeira fase atual não é 5, 6, 7 ou 8, a ordem vira:

```
[5,6,1,2,3,4,7,8,9,10,11,12]
```

A fase 12 permanece sempre por último.

#### Ritmo

| `knowledge_level` | `pace` |
|---|---|
| `beginner` ou ausente | `supported` |
| `intermediate` | `steady` |
| `advanced` | `accelerated` (+ frase no rationale) |

#### Formato persistido

```json
{
  "source": "rules",
  "version": 1,
  "goal_category": "dividas",
  "phase_order": [7,8,1,2,3,4,5,6,9,10,11,12],
  "rationale": "...",
  "focus_areas": ["..."],
  "pace": "steady",
  "knowledge_level": "intermediate",
  "life_context": "ja_trabalho",
  "urgency": "agora_preciso",
  "generated_at": "..."
}
```

> Observação: a especificação fala em `version: 2`, `trail_modes` e `trail_1_auto_concluded`, mas o código atual não gera nenhum desses campos.

### 3.4 Regras de desbloqueio

- A primeira fase da trilha começa liberada.
- Cada fase seguinte exige **todas as missões obrigatórias de todas as fases anteriores**.
- Missões opcionais não bloqueiam.
- Uma fase sem missões obrigatórias é tratada como não concluída e bloqueia as seguintes.
- Se a ordem persistida for inválida, o backend usa a ordem padrão das fases ativas (normalmente `[1..12]`).
- Se uma fase existir no banco mas não estiver na trilha persistida, ela fica bloqueada.
- Fases novas criadas depois da trilha são anexadas ao fim da lista visual, mas continuam bloqueadas até a trilha ser regerada.

### 3.5 Recomendação de próximo passo

A função `build_recommendation()` decide nesta ordem:

| # | Condição | `kind` | Mensagem |
|---|---|---|---|
| 1 | Não há próxima missão | `complete` | “Você concluiu o que está disponível nesta trilha...” |
| 2 | Existe tópico de reforço do Analista | `review` | “Antes de avançar, vale revisar...” (até 2 tópicos) |
| 3 | Missão está em andamento | `continue` | “Retome ‘X’ de onde parou...” |
| 4 | Trilha personalizada e primeira posição | `start` | “Sua trilha começa por X. <rationale>” |
| 5 | Há fase/missão | `start` | “O próximo passo é ‘X’, na trilha N...” |
| 6 | Fallback | `start` | “Seu próximo passo está pronto...” |

**Precedência importante:** `review` vence `continue`; `complete` vence todos. O `complete` também aparece quando a próxima fase existe, mas está bloqueada ou sem conteúdo.

### 3.6 Cenários do Catalisador

| ID | Cenário | Comportamento |
|---|---|---|
| CAT-01 | Onboarding com categoria válida | Gera ordem específica da categoria |
| CAT-02 | Categoria ausente, nula ou inválida | Usa `outro` e ordem canônica |
| CAT-03 | `life_context` válido com categoria `primeiro_salario`/`outro` | Sobrescreve a ordem pelo contexto |
| CAT-04 | `life_context` com categoria específica (`dividas`, etc.) | Ignora o contexto de vida |
| CAT-05 | `urgency=agora_preciso` + categoria `outro`/`primeiro_salario` | Força início por 5/6, se ainda não começar por 5–8 |
| CAT-06 | `urgency=aprendizado_continuo` | Não altera a ordem |
| CAT-07 | `knowledge_level=advanced` | `pace=accelerated` + frase de ritmo |
| CAT-08 | `knowledge_level=beginner` | `pace=supported` |
| CAT-09 | Objetivo personalizado (`outro`) | Acrescenta o texto do objetivo ao rationale |
| CAT-10 | Onboarding reenviado após concluído, com trilha | Não altera perfil, trilha nem bônus |
| CAT-11 | Onboarding reenviado após concluído, sem trilha | Cria a trilha, mas **não** concede o bônus novamente |
| CAT-12 | Usuário escolhe `standard` | Volta à ordem `[1..12]`, `source=standard` |
| CAT-13 | Usuário escolhe `personalized` | Reconstrói a trilha com as preferências atuais |
| CAT-14 | Modo inválido | HTTP 400 |
| CAT-15 | Trilha persistida válida | Devolve ordem + fases enriquecidas |
| CAT-16 | Trilha persistida inválida | `get_trail_view()` devolve `None`; Jornada/desbloqueios usam a ordem padrão das fases ativas, mas `GET /users/me` ainda pode devolver o objeto bruto do perfil |
| CAT-17 | Fase fora da trilha | Bloqueada |
| CAT-18 | Fase nova após a trilha | Aparece no fim, mas bloqueada |
| CAT-19 | Primeira missão disponível | Recomendação `start` com rationale da trilha |
| CAT-20 | Missão em andamento | Recomendação `continue` |
| CAT-21 | Tópico de reforço sinalizado | Recomendação `review` (mesmo se houver missão em andamento) |
| CAT-22 | Todas as missões concluídas | Recomendação `complete` |
| CAT-23 | Conclusão de missão com próxima missão liberada | `next_step` aponta para a próxima |
| CAT-24 | Conclusão da última missão da fase | `next_step` aponta para a primeira missão da fase seguinte, se liberada |
| CAT-25 | Conclusão sem próxima missão | `next_step.kind=complete` |
| CAT-26 | Ordem de trilha gerada por IA incompleta/duplicada/inexistente | `apply_generated_trail()` rejeita com `ValueError` |
| CAT-27 | Ordem de trilha gerada por IA válida | Persiste com `source=ai` |
| CAT-28 | Alteração de perfil após onboarding | **Não** regenera a trilha automaticamente; só o endpoint de preferência regenera |
| CAT-29 | Troca de trilha com progresso existente | Mantém progresso; muda apenas a ordem/desbloqueios |
| CAT-30 | Usuário sem trilha | Ordem padrão das fases ativas |
| CAT-31 | Usuário sem trilha e sem próxima missão | `build_next_step_recommendation()` usa `trail_size=6`, embora existam 12 fases — inconsistência de exibição |
| CAT-32 | Celebração de trilha / `trail_1_review` / `celebrate` | **Não implementado**; só existe na especificação |
| CAT-33 | `trail_modes` (express/standard/full) | **Não implementado**; não é gerado nem aplicado |
| CAT-34 | Trilha 1 auto-concluída + 50 XP | **Não implementado** |
| CAT-35 | Síntese de trilha pelo Analista | **Não implementado** |

### 3.7 Limites do Catalisador

- Não escreve no banco diretamente; só devolve dados para o serviço persistir.
- Não concede pontos, moedas, conquistas ou desbloqueios.
- Não usa LLM no MVP.
- Não adapta a ordem em tempo real durante as missões.
- Não reage a inatividade; não há job de reengajamento.
- Não gera mensagem de celebração ao concluir trilha.

---

## 4. Analista de Progresso

### 4.1 Papel

Interpretar evidências de aprendizagem e produzir recomendações curtas de reforço, além de alimentar o painel de progresso e o contexto do Mentor. No código atual, ele é **determinístico e calculado sob demanda**, não um agente de IA em background.

### 4.2 Pipeline de evidência

```
Resposta do usuário
  → record_competency_evidence()
  → atualiza UserCompetencyProgress
  → recalcula status e reinforcement_suggested
  → Analista pode aparecer no feedback, no resumo, no painel ou no contexto do Mentor
```

### 4.3 Status de competência

Uma competência é avaliada pelas atividades vinculadas via `content.competency_codes`:

| Status | Condição |
|---|---|
| `not_started` | Nenhuma evidência registrada |
| `developing` | Há alguma evidência, mas não todas |
| `demonstrated` | Todas as atividades vinculadas têm evidência válida |

Para atividades objetivas, “evidência válida” exige acerto (`is_correct=true`). Para `open_text`, basta ter resposta registrada. Isso significa que uma competência composta só de respostas abertas pode virar `demonstrated` apenas por participação.

### 4.4 Regra de reforço

O sinal `reinforcement_suggested` fica `true` quando o status **não** é `demonstrated` e ocorre uma das condições:

1. **2 atividades objetivas diferentes** da mesma competência com pelo menos um erro cada; ou
2. **3 tentativas incorretas na mesma atividade**, quando a competência tem apenas uma atividade objetiva vinculada.

Erros são contados em todo o histórico, inclusive entre tentativas do módulo.

### 4.5 Onde o Analista aparece

| Ponto | Dado | Quando |
|---|---|---|
| Feedback de resposta | `reinforcement` | Apenas em resposta incorreta de competência já sinalizada |
| Resumo da missão | `mission_insight` | Quando a missão é concluída |
| Painel de progresso | `analyst_insight` | Ao abrir `GET /progress/summary` |
| Cartão de competências | `reinforcement_suggested` por competência | Ao abrir o painel |
| Contexto do Mentor | `reinforcement_topics` | Ao abrir/consultar o chat |
| Payload do Mentor | `learning_context.reinforcement_topics` | Em cada mensagem enviada ao Orchestrate |
| Recomendação do Catalisador | `review` | Quando há tópicos sinalizados |
| Exercícios do Estúdio | Contadores de acerto/erro | Ao responder exercício gerado; **não** recalculam status nem reforço hoje |

### 4.6 Formato das mensagens

O Analista prioriza:

1. **Reforço** (`severity=attention`, `action=review`) se qualquer competência estiver sinalizada.
2. **Positivo** (`severity=positive`, `action=advance`) se houver competência `demonstrated`.
3. **Neutro** (`severity=neutral`, `action=continue`) se houver competência `developing`.
4. `None` se não houver competências.

A mensagem mostra no máximo **2 nomes** de competências.

### 4.7 Cenários do Analista

| ID | Cenário | Comportamento |
|---|---|---|
| ANA-01 | Nenhuma resposta registrada | Nenhum insight (`None`) |
| ANA-02 | Primeiro erro em competência com várias atividades | Status `developing`; reforço ainda não sinalizado |
| ANA-03 | Erro em 2 atividades objetivas diferentes | Reforço sinalizado |
| ANA-04 | 3 erros na mesma atividade, competência com uma única atividade | Reforço sinalizado |
| ANA-05 | 3 erros na mesma atividade, mas competência com 2+ atividades | Reforço **não** sinalizado pela regra atual |
| ANA-06 | Acerto em todas as atividades vinculadas | Status `demonstrated`; reforço removido |
| ANA-07 | Acertos parciais | Status `developing`; mensagem neutra |
| ANA-08 | Uma competência sinalizada + várias demonstradas | Mensagem de reforço prevalece |
| ANA-09 | Competência só com resposta aberta | Pode virar `demonstrated` por participação |
| ANA-10 | Resposta aberta sem avaliação | `is_correct=null`; não conta como erro nem acerto |
| ANA-11 | Resposta objetiva sem alternativa selecionada | `is_correct=null`; feedback neutro; sem reforço |
| ANA-12 | Resposta incorreta em competência já sinalizada | `feedback_agent=analyst` + `reinforcement` |
| ANA-13 | Primeira resposta incorreta sem sinalização | `feedback_agent=mentor`; feedback é o texto estático da atividade |
| ANA-14 | Resposta correta | `feedback_agent=mentor`; feedback estático de acerto |
| ANA-15 | Missão concluída com competências demonstradas | `mission_insight` positivo |
| ANA-16 | Missão concluída com competência em desenvolvimento | `mission_insight` neutro |
| ANA-17 | Missão concluída com competência sinalizada | `mission_insight` de reforço |
| ANA-18 | Missão sem competências vinculadas | `mission_insight=None` |
| ANA-19 | Painel de progresso com histórico geral | `analyst_insight` considera todas as competências |
| ANA-20 | Contexto do Mentor com tópicos sinalizados | Lista `reinforcement_topics`; abertura cita o primeiro |
| ANA-21 | Refez módulo e melhorou | Status/flag recalculados com todo o histórico |
| ANA-22 | Refez módulo e piorou | Erros antigos continuam contando |
| ANA-23 | Exercício do Estúdio respondido | Incrementa `correct_count`/`incorrect_count`, mas o status e o reforço continuam baseados apenas nas atividades do currículo (`activity_id=null`) |
| ANA-24 | Exercício aberto do Estúdio | Não altera contadores nem status; a resposta fica registrada sem vínculo com atividade |
| ANA-25 | Exercício de fase inteira | Mesmo comportamento: contadores por competência, sem impacto no status/reforço |
| ANA-26 | Nenhuma competência no banco | Nenhum insight |
| ANA-27 | Síntese de trilha (D-A1) | **Não implementado** |
| ANA-28 | Análise em background | **Não existe**; é cálculo síncrono sob demanda |
| ANA-29 | “Uma recomendação por sessão por competência” | **Não implementado**; a mensagem pode reaparecer a cada consulta/resposta |
| ANA-30 | Limite de 2 intervenções por missão | **Não implementado** no Analista; a regra de reforço é por histórico |

### 4.8 Limites do Analista

- Não vê o texto de respostas abertas para avaliar conteúdo; só registra participação.
- Não usa LLM.
- Não altera pontuação, desbloqueio, status de missão ou conquistas.
- Não “rotula” o aluno; trabalha por competência.
- Não recomenda repetir a fase inteira; a mensagem sugere revisão de conceito.
- Não impede o avanço.
- Não gera a síntese de trilha prometida na especificação.

---

## 5. Mentor

### 5.1 Papel

Conversar com o estudante, explicar conceitos, apoiar o raciocínio e responder dúvidas durante as missões. A integração real é feita por um adaptador único para o watsonx Orchestrate.

### 5.2 Onde é acionado

| Evento | Rota | Comportamento |
|---|---|---|
| Abrir a página do Mentor | `GET /conversations/mentor/context` | Monta abertura, sugestões e tópicos do Analista |
| Enviar mensagem no chat | `POST /conversations/mentor` | Persiste, chama o Orchestrate e persiste a resposta |
| Abrir modal dentro da aula | `POST /conversations/mentor` com `mission_id` | Usa o contexto da missão |
| Consultar histórico | `GET /conversations/mentor/history` | Últimas 10 conversas |
| Abrir aula concluída | `GET /journey/.../lesson` | Fornece `mission_insight` e `next_step` para os botões de ajuda |

### 5.3 Contexto devolvido ao frontend

- Missão, fase e competências (quando há `mission_id`).
- Mensagem de abertura.
- Sugestões de perguntas.
- Tópicos de reforço do Analista.
- `status`: no endpoint de contexto, apenas `preparing` ou `available`; `unavailable` aparece na resposta do chat quando a chamada falha.
- Meta pessoal e nível de conhecimento.

### 5.4 Payload enviado ao Orchestrate

```json
{
  "agent": "mentor",
  "conversation_id": 12,
  "user_context": {
    "personal_goal": "...",
    "knowledge_level": "..."
  },
  "learning_context": {
    "mission_id": 10,
    "mission_name": "...",
    "phase_number": 4,
    "phase_name": "...",
    "competencies": [{"code": "4.1.1", "name": "..."}],
    "reinforcement_topics": ["..."]
  },
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "message": "..."
}
```

**Detalhes importantes:**

- A janela é de até 5 mensagens, mas o código adiciona a mensagem atual antes de montar o payload. Na prática, entram até 4 mensagens anteriores + a atual.
- A mensagem atual aparece **duas vezes**: dentro de `messages` e no campo `message`.
- `mission_id` inválido não gera erro: o contexto cai no modo geral.
- As competências vêm da missão, não do nível de domínio.
- O payload não inclui dados financeiros, renda, saldo ou dados bancários.
- Não há “system prompt” do Mentor neste repositório; a instrução de comportamento deve estar configurada no agente do Orchestrate.

### 5.5 Cenários do Mentor

| ID | Cenário | Comportamento |
|---|---|---|
| MEN-01 | Chat geral sem missão | Contexto genérico + sugestões gerais |
| MEN-02 | Chat com missão válida | Contexto da missão/fase/competências |
| MEN-03 | Chat com `mission_id` inexistente | Cai no contexto geral, sem 404 |
| MEN-04 | Primeira mensagem | Cria conversa para o par (usuário, agente, missão) |
| MEN-05 | Mensagens seguintes | Reutiliza a mesma conversa da missão |
| MEN-06 | Mensagem vazia | HTTP 400 |
| MEN-07 | Mensagem > 2000 caracteres | HTTP 400 |
| MEN-08 | Múltiplas conversas (geral + missões) | Histórico separado por missão |
| MEN-09 | `ORCHESTRATE_ENABLED=false` | `preparing` + fallback; mensagem salva |
| MEN-10 | `ORCHESTRATE_URL` vazio | `preparing` + fallback |
| MEN-11 | Enabled + URL + resposta 2xx com `content` | `available`, `source=orchestrate` |
| MEN-12 | Resposta 2xx com `output` | `available` |
| MEN-13 | Resposta 2xx com `response` | `available` |
| MEN-14 | Resposta 2xx sem texto utilizável | `unavailable`, `detail=empty_response` |
| MEN-15 | Resposta 2xx com texto vazio/só espaços | `unavailable` |
| MEN-16 | HTTP 4xx/5xx | `unavailable` + fallback |
| MEN-17 | Timeout (15 s padrão) | `unavailable` + fallback |
| MEN-18 | Erro de rede/DNS | `unavailable` + fallback |
| MEN-19 | JSON inválido | `unavailable` + fallback |
| MEN-20 | Resposta sem `suggestions` | Usa sugestões padrão |
| MEN-21 | Falha do Orchestrate | Mensagem do usuário e fallback são persistidos |
| MEN-22 | Histórico | Últimas 10 conversas, ordenadas por atualização |
| MEN-23 | Nova mensagem após falha | Tenta o Orchestrate novamente, sem circuit breaker |
| MEN-24 | Resposta do Mentor | Não altera pontos, progresso ou desbloqueio |
| MEN-25 | Intervenção proativa em erro | **Não implementada**; o “Mentor” do feedback é apenas rótulo do feedback estático |
| MEN-26 | Avaliação de resposta aberta pelo Mentor | **Não implementada** |
| MEN-27 | Geração de quiz pelo Mentor | **Não implementada** |
| MEN-28 | Pedido de esclarecimento em resposta ambígua | **Não implementado no backend** |
| MEN-29 | Filtro de segurança D8 no código | **Não existe**; depende do agente configurado no Orchestrate |
| MEN-30 | Status `available` no contexto | Reflete apenas flags de configuração, não health check real |
| MEN-31 | `ORCHESTRATE_AGENT_ID` | Ignorado pelo código |
| MEN-32 | URL raiz da instância | O adaptador faz `POST` na URL como está; não monta caminho por agente |

### 5.6 Fallback

O fallback é explícito e não simula uma resposta de IA:

> “O Mentor ainda está em preparação — a integração com a IA não foi ativada. Sua mensagem foi salva. Enquanto isso, o conteúdo de apoio de cada missão continua disponível nas etapas de leitura.”

Ele devolve sugestões padrão e não quebra o chat. O progresso do usuário não é afetado.

### 5.7 Limites do Mentor

- Não altera estado acadêmico.
- Não acessa banco.
- Não vê histórico completo; só a janela enviada.
- Não recebe renda, saldo ou dados bancários.
- Não faz chamadas a fontes externas.
- Não tem retry/backoff.
- Não há garantia de aderência às regras D8 no backend; isso precisa ser garantido no agente do Orchestrate.
- Não substitui o conteúdo aprovado; a especificação exige hierarquia de fontes, mas o código não a impõe.

---

## 6. Mentor de Estúdio

### 6.1 Papel

Gerar conteúdo personalizado no Estúdio em três formatos: `revisao`, `flashcards` e `exercicios`, usando conteúdo aprovado e competências do usuário.

### 6.2 Onde é acionado

| Evento | Rota | Comportamento |
|---|---|---|
| Gerar conteúdo | `POST /studio/generate` | Valida acesso, saldo, monta payload e tenta gerar |
| Consultar geração | `GET /studio/generate/{id}` | Devolve conteúdo do próprio usuário |
| Biblioteca | `GET /studio/library` | Lista apenas conteúdos `ready` do usuário |
| Responder exercício | `POST /studio/exercises/{id}/submit` | Avalia, registra evidência e recompensa |

### 6.3 Custos em Prismas

| Formato | Custo |
|---|---|
| `revisao` | 30 |
| `flashcards` | 20 |
| `exercicios` | 25 |

### 6.4 Ordem de validação

1. Formato válido.
2. Fase existe.
3. Missão existe (se informada).
4. Missão pertence à fase.
5. Usuário já cursou a missão/fase.
6. Orchestrate habilitado e com URL.
7. Saldo suficiente.
8. Debita Prismas.
9. Cria registro de geração.
10. Chama `call_orchestrate()`.
11. Valida estrutura.
12. Marca `ready`.

### 6.5 Cenários do Estúdio

| ID | Cenário | Comportamento |
|---|---|---|
| STU-01 | Formato inválido | 422 |
| STU-02 | Fase inexistente | 404 |
| STU-03 | Missão inexistente | 404 |
| STU-04 | Missão de outra fase | 400 |
| STU-05 | Missão não cursada | 403 |
| STU-06 | Fase não cursada (geração de fase) | 403 |
| STU-07 | Fase sem missões disponíveis | 409 |
| STU-08 | Orchestrate desligado | 503, sem cobrança |
| STU-09 | Saldo insuficiente | 402, sem cobrança |
| STU-10 | Orchestrate ligado (configuração aplicada) | Debita, chama função não implementada, falha, devolve Prismas, 502 |
| STU-11 | Futuro: resposta válida | Conteúdo `ready`, custo mantido |
| STU-12 | Futuro: resposta inválida | Falha, devolve Prismas, 502 |
| STU-13 | Biblioteca | Só conteúdos `ready` do próprio usuário |
| STU-14 | Geração de outro usuário | 404 |
| STU-15 | Exercício em geração que não é `exercicios` | 400 |
| STU-16 | Exercício em geração não `ready` | 409 |
| STU-17 | Índice de questão inválido | 400 |
| STU-18 | Questão já respondida | 409 |
| STU-19 | Questão objetiva | Avalia e devolve feedback/gabarito quando aplicável |
| STU-20 | Questão aberta | `is_correct=null`; feedback estático |
| STU-21 | Todas as questões respondidas | 5 Prismas, uma única vez |
| STU-22 | Exercício respondido | Incrementa contadores, mas não altera status/reforço do Analista |
| STU-23 | Geração de fase inteira | Considera apenas módulos já iniciados |
| STU-24 | Resposta do exercício | Não concede pontos de progressão, só Prismas |

### 6.6 Limites do Estúdio

- `call_orchestrate()` não está implementado; nenhum conteúdo real é gerado hoje.
- O payload já está pronto e validado.
- A validação de estrutura existe para os três formatos.
- O conteúdo gerado nunca é escrito diretamente pela IA; o backend valida antes de persistir.
- Exercícios alimentam os contadores de acerto/erro do Analista, mas **não** recalculam `status` nem `reinforcement_suggested`, porque a resposta do Estúdio é gravada com `activity_id=null` e o cálculo de status só olha atividades do currículo.
- Não substituem atividades oficiais do currículo.

---

## 7. Fluxos completos entre agentes

### 7.1 Onboarding

```
Usuário preenche objetivo, nível, contexto de vida, urgência e consentimento
  → POST /users/me/onboarding
  → Catalisador gera trilha
  → Backend persiste perfil + trilha
  → Backend concede bônus de onboarding (50 pontos, 20 Prismas, conquista "primeiro_passo")
  → Frontend mostra prévia da trilha
```

Agentes envolvidos: **Catalisador**.  
Mentor e Analista não participam.

### 7.2 Home e Jornada

```
GET /journey/overview
  → Catalisador lê a trilha e ordena as fases
  → Backend calcula desbloqueios
  → Analista fornece tópicos de reforço
  → Catalisador monta a recomendação
  → Frontend mostra o cartão “Catalisador”
```

### 7.3 Responder uma atividade

```
POST /journey/missions/{id}/submit
  → Backend avalia deterministicamente
  → Analista atualiza evidência de competência
  → Se erro e competência já sinalizada: feedback do Analista
  → Caso contrário: feedback estático rotulado como Mentor
  → Se a missão foi aprovada: Analista gera mission_insight e Catalisador gera next_step
  → Se a tentativa terminou reprovada: nenhum insight de conclusão; o aluno precisa refazer
```

**Atenção:** o “feedback do Mentor” nesse fluxo **não é uma chamada ao Mentor**. É o texto `feedback_correct`/`feedback_incorrect` da própria atividade.

### 7.4 Concluir uma missão

```
Todas as atividades respondidas
  → apply_mission_completion()
  → pontos, Prismas, conquistas e status
  → Analista: mission_insight
  → Catalisador: next_step
  → Frontend: resumo com insight + próximo passo
```

### 7.5 Refazer uma missão

```
POST /journey/missions/{id}/retry
  → abre nova tentativa
  → não apaga respostas antigas
  → erros antigos continuam contando para o Analista
  → respostas novas geram novas evidências
```

### 7.6 Painel de progresso

```
GET /progress/summary
  → Analista lê todas as competências do usuário
  → Gera analyst_insight (reforço, positivo ou neutro)
  → Frontend exibe o card do Analista
```

### 7.7 Chat do Mentor

```
POST /conversations/mentor
  → Backend persiste mensagem do usuário
  → Analista fornece tópicos de reforço
  → Backend monta payload com missão, competências, meta e últimas mensagens
  → Mentor chama Orchestrate (ou fallback)
  → Backend persiste resposta
  → Frontend exibe
```

### 7.8 Estúdio

```
POST /studio/generate
  → Backend valida acesso e saldo
  → Debita Prismas
  → Mentor de Estúdio monta payload
  → call_orchestrate() (não implementado)
  → Falha: devolve Prismas e retorna 502
```

### 7.9 Onde cada agente aparece na interface

| Tela | Agentes visíveis | O que o usuário vê |
|---|---|---|
| Landing | Catalisador, Mentor, Analista (marketing) | Descrição dos papéis; não há chamada real |
| Onboarding | Catalisador | Prévia da trilha gerada ao concluir |
| Home | Catalisador + Analista (indireto) | Cartão do próximo passo; a recomendação pode virar revisão por tópico do Analista |
| Jornada | Catalisador | Trilha personalizada + linha de recomendação |
| Aula/missão | Mentor + Analista | Feedback estático rotulado como Mentor; insight e reforço do Analista; modal do Mentor |
| Progresso | Analista | Card “Analista de Progresso”, tópicos de reforço e competências |
| Mentor e agentes | Mentor + Analista | Chat e tópicos de reforço no contexto |
| Estúdio | Mentor de Estúdio + Analista | Geração (indisponível) e exercícios que alimentam o Analista |
| Perfil | Catalisador | Trilha e opção de voltar à ordem padrão |

---

## 8. Cobertura real vs. especificação

| Item especificado | Estado no código | Observação |
|---|---|---|
| Catalisador determinístico | ✅ Implementado | `catalyst.py` |
| Onboarding com 10 perguntas fixas + 8 adaptativas | ✅ Implementado | Frontend conversacional + endpoint de perguntas adaptativas + histórico no backend |
| Trilha por objetivo/contexto/urgência | ✅ Implementado | Regras explícitas |
| `trail_modes` (express/standard/full) | ❌ Não implementado | Não é gerado nem aplicado |
| Trilha 1 auto-concluída | ❌ Não implementado | Sem selo e sem 50 XP específicos |
| Celebração de conclusão de trilha | ❌ Não implementado | Sem `celebrate_trail_completion()` |
| Tipos de recomendação `celebrate` e `trail_1_review` | ❌ Não implementado | Só `complete`, `start`, `continue`, `review` |
| Síntese de trilha do Analista (D-A1) | ❌ Não implementado | Sem `generate_trail_synthesis()` |
| Analista determinístico | ✅ Implementado | Regras 2 atividades/3 tentativas |
| Analista em background | ❌ Não é background | Cálculo sob demanda |
| Mentor com chat persistido | ✅ Implementado | Conversas por missão |
| Mentor com IA real | ⚠️ Adaptador pronto | Depende de configuração e endpoint válidos |
| Contexto do Mentor (missão, competências, meta, 5 mensagens) | ✅ Implementado | Com duplicação da mensagem atual |
| Intervenções proativas do Mentor | ❌ Não implementado | Feedback é estático |
| Avaliação de resposta aberta | ❌ Não implementado | `open_text` fica neutro |
| Geração de quizzes pelo Mentor | ❌ Não implementado | — |
| Segurança D8 no backend | ❌ Não implementado | Deve estar no agente do Orchestrate |
| Mentor de Estúdio (contrato) | ✅ Implementado | Payload e validação |
| Mentor de Estúdio (geração real) | ❌ Não implementado | `call_orchestrate()` sempre falha |
| Exercícios do Estúdio alimentam o Analista | ⚠️ Parcial | Incrementa contadores, mas não altera status/reforço (resposta com `activity_id=null`) |
| Backend como autoridade | ✅ Implementado | Nenhum agente altera estado diretamente |

---

## 9. Riscos e pontos de atenção

### 9.1 Configuração

1. **`.env` e container divergem.** O arquivo está com Orchestrate ligado; o container em execução está com desligado. Ao recriar, o comportamento muda.
2. **`ORCHESTRATE_AGENT_ID` é ignorado.** Se o Orchestrate exigir um agente específico no caminho/URL, a chamada falhará.
3. **URL raiz.** O adaptador faz `POST` exatamente em `ORCHESTRATE_URL`; não monta `/agents/{id}` nem usa o `agent` do payload para roteamento local.
4. **Estúdio com Orchestrate ligado.** A validação de saldo passa, as Prismas são debitadas e a geração falha em seguida. O refund existe, mas o usuário vê um erro 502.

### 9.2 Comportamento

5. **“Feedback do Mentor” é estático.** A UI pode dar a impressão de participação do Mentor, mas não há chamada de IA nesse ponto.
6. **Analista não é background.** A especificação fala em análise em background; o código recalcula a cada resposta/consulta.
7. **Mensagem atual duplicada no payload do Mentor.** Pode causar respostas repetidas ou confusão no agente.
8. **`trail_size=6` no fallback.** Quando não há trilha, a recomendação usa 6, mas o sistema tem 12 fases.
9. **Fase nova após a trilha fica bloqueada.** A fase é anexada ao fim da lista, mas não entra na ordem validada.
10. **Competência só com resposta aberta pode ficar `demonstrated`.** A regra considera participação, não compreensão.
11. **Sinal de reforço global domina a recomendação.** Um tópico antigo sinalizado pode transformar a Home em “review” mesmo com uma missão em andamento.
12. **Sem limite de intervenções por sessão.** A recomendação do Analista pode reaparecer em várias telas/consultas.
13. **Exercícios do Estúdio não afetam o status do Analista.** Eles incrementam contadores, mas `_calculate_competency_status()` e `_should_suggest_reinforcement()` só enxergam respostas vinculadas a atividades do currículo. Na prática, o Estúdio ainda não influencia os insights do Analista.

### 9.3 Lacunas de produto

14. Onboarding conversacional adaptativo implementado; a curadoria das perguntas adaptativas segue em evolução.
15. Não há modos de profundidade por trilha.
16. Não há trilha 1 auto-concluída.
17. Não há celebração de trilha.
18. Não há síntese de trilha.
19. Não há reengajamento por inatividade.
20. Não há avaliação de respostas abertas.
21. Não há testes de segurança D8 no backend.

---

## 10. Mapa rápido de endpoints por agente

| Endpoint | Catalisador | Analista | Mentor | Estúdio |
|---|---|---|---|---|
| `POST /api/v1/users/me/onboarding` | ✅ | — | — | — |
| `POST /api/v1/users/me/trail/preference` | ✅ | — | — | — |
| `GET /api/v1/users/me/trail` | ✅ | — | — | — |
| `GET /api/v1/users/me` | ✅ | — | — | — |
| `GET /api/v1/journey/overview` | ✅ | ✅ | — | — |
| `GET /api/v1/journey/phases/my-progress` | ✅ | — | — | — |
| `GET /api/v1/journey/missions/{id}` | ✅ | — | — | — |
| `GET /api/v1/journey/missions/{id}/lesson` | ✅ | ✅ | — | — |
| `POST /api/v1/journey/missions/{id}/start` | ✅ | — | — | — |
| `POST /api/v1/journey/missions/{id}/submit` | ✅ | ✅ | ⚠️ rótulo estático | — |
| `POST /api/v1/journey/missions/{id}/retry` | — | — | — | — |
| `GET /api/v1/progress/summary` | — | ✅ | — | — |
| `GET /api/v1/conversations/mentor/context` | — | ✅ | ✅ | — |
| `POST /api/v1/conversations/mentor` | — | ✅ | ✅ | — |
| `GET /api/v1/conversations/mentor/history` | — | — | ✅ | — |
| `POST /api/v1/studio/generate` | — | — | — | ✅ |
| `GET /api/v1/studio/generate/{id}` | — | — | — | ✅ |
| `GET /api/v1/studio/library` | — | — | — | ✅ |
| `POST /api/v1/studio/exercises/{id}/submit` | — | ✅ | — | ✅ |

Legenda: ✅ participa; ⚠️ apenas rótulo/feedback estático; — não participa.

---

## 11. Conclusão

O sistema atual tem uma base sólida de **regras determinísticas** e um **contrato de integração bem definido**, mas ainda não tem os agentes de IA em operação plena:

- **Catalisador** é o agente mais “completo” em comportamento, mas é 100% baseado em regras e não cobre as decisões mais recentes (modos de trilha, auto-conclusão, celebração, síntese).
- **Analista** já entrega recomendações úteis e integradas a várias telas, mas é síncrono, determinístico e não faz análise semântica de respostas abertas.
- **Mentor** tem chat, histórico e contexto prontos; falta a chamada real funcionando de ponta a ponta e as regras de segurança/comportamento precisam estar no agente do Orchestrate.
- **Mentor de Estúdio** tem o contrato e a validação, mas a geração real está deliberadamente bloqueada.

O ponto mais urgente antes de qualquer piloto com IA é alinhar a configuração do Orchestrate (URL/agente), implementar o `call_orchestrate()` do Estúdio e decidir se as regras D8 serão aplicadas no backend ou no próprio agente.
