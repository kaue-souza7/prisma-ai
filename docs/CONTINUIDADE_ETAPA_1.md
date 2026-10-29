# CONTINUIDADE — Etapa 1 do Protótipo ELL IBM

**Arquivo:** `docs/CONTINUIDADE_ETAPA_1.md`  
**Gerado em:** Sessão de implementação da Etapa 1  
**Última atualização:** 22/10/2026 — conteúdo das Trilhas 3 a 6  
**Propósito:** Permitir que uma nova sessão de LLM retome o trabalho exatamente de onde parou, sem reabrir decisões já aprovadas, sem recriar arquivos existentes e sem presumir integrações indisponíveis.

> **Atualização de 23/10/2026 (prevalece sobre o histórico abaixo):** foram
> antecipadas, sem Orchestrate, a trilha personalizada determinística, o chat
> funcional do Mentor com fallback honesto, os insights do Analista nos fluxos,
> o Catalisador visível na Home/Jornada/Perfil e o onboarding com contexto de
> vida e urgência. A migration `0010` adiciona `profiles.trail`. Ver seção 14 e
> `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.
>
> **Atualização de 22/10/2026:** as Trilhas 3, 4, 5 e 6 receberam conteúdo
> completo no mesmo modelo das Trilhas 1 e 2: seeds versionados, loaders
> idempotentes, migrations `0005`–`0009`, roteiros imersivos, conquistas de fase
> e testes de contrato. A Fase 6 inclui a missão 6.4 — Desafio integrador. O
> estado verificado no Compose é de **101 testes de backend e 29 de frontend
> passando**, com build aprovado e migrations até `0009`. Ver
> `docs/MINICURSOS_TRILHAS_3_6.md` e a seção 13.

> **Atualização de 21/10/2026 (prevalece sobre o histórico abaixo):** foram
> antecipadas, sem IA e sem Orchestrate, as frentes de conteúdo da Fase 1,
> contrato JSONB, critérios de domínio, desbloqueio sequencial, onboarding,
> telas de jornada/missão/progresso e testes de frontend. O conteúdo da Fase 1
> está na migration `0002_phase_1_content.py`; o contrato está em
> `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md`; os critérios estão em
> `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`. A integração de IA continua
> bloqueada por D7. As migrations `0002`–`0004` foram aplicadas no Compose e o fluxo vertical
> foi validado por API em PostgreSQL real; falta o E2E em navegador.
>
> **Atualização visual:** a landing pública e as telas de autenticação do Prisma.AI foram implementadas com identidade dark premium, efeitos Motion/React Bits-inspired e fluxos reais preservados. Ver seção 9.

---

## Resumo executivo para retomada rápida

| Campo | Estado |
|---|---|
| **Objetivo atual** | Seis fases ponta a ponta **sem IA**: conteúdo real, onboarding com trilha, minicursos, chat com fallback, progresso e desbloqueio determinístico. |
| **Estado geral** | **Frentes sem IA implementadas e validadas no Compose.** Migrations `0002`–`0010` aplicadas; 108 testes de backend e 37 de frontend passando; fluxo vertical de API e novas telas verificados em Chrome headless. Falta E2E automatizado de interação e revisão de produto/LGPD. |
| **Último marco concluído** | Trilha personalizada determinística, chat funcional do Mentor, insights do Analista, Catalisador visível e preparação do adaptador Orchestrate. Backend: 108 testes passando no Compose. |
| **Tarefa em andamento** | Revisão de produto do conteúdo/critérios, E2E automatizado e validação da trilha personalizada. |
| **Próxima ação exata** | Validar a trilha personalizada com produto/pedagogia; automatizar a jornada completa em navegador; revisar conteúdo e critérios; validar LGPD. |
| **Principais bloqueadores** | (1) watsonx Orchestrate sem acesso — bloqueia apenas a integração de IA. (2) Revisão editorial/produto do conteúdo e dos critérios. (3) Base legal LGPD sem validação jurídica. |
| **Documentos a ler primeiro** | Este arquivo → `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md` → `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md` → `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md` → `docs/GUIA_PRODUCAO_CONTEUDO.md` → `docs/MINICURSOS_TRILHAS_3_6.md` → `docs/Arquitetura_Tecnica_ELL_IBM.md` → `docs/PRD_ELL_IBM.md` |

---

## 1. Contexto e objetivo da Etapa 1

### 1.1 Objetivo

Criar a base técnica local do projeto ELL IBM com todos os serviços operacionais via Docker Compose. Ao final desta etapa, deve ser possível:

1. Clonar o repositório.
2. Copiar `.env.example` para `.env` e preencher os valores obrigatórios.
3. Executar `docker compose up`.
4. Aplicar a migração: `docker compose exec backend alembic upgrade head`.
5. Acessar o frontend em `http://localhost:5173`.
6. Cadastrar um usuário, verificar o e-mail (mock em desenvolvimento — token impresso no log), fazer login.
7. Ver a estrutura das 6 fases e o painel de progresso.
8. Acessar a documentação da API em `http://localhost:8000/docs`.

### 1.2 Arquitetura

- **Monólito modular:** um único backend FastAPI organizado por módulos com responsabilidades separadas. Extrair microserviços apenas se houver justificativa concreta.
- **Backend como autoridade:** toda regra de negócio, pontuação, desbloqueio e validação vive no backend. A IA nunca altera estado persistente diretamente.
- **Gamificação determinística:** pontos e conquistas calculados por regras explícitas, sem participação da IA.
- **Espaços reservados para IA:** o módulo `conversations` já tem chat funcional, histórico persistido e fallback honesto; a resposta real depende do adaptador do Orchestrate. A estrutura de dados e o contrato estão prontos para a Etapa 2.

### 1.3 Stack tecnológica

| Camada | Tecnologia | Status |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Aprovado e implementado |
| Banco de dados | PostgreSQL 16 | Aprovado e configurado |
| ORM / Migrações | SQLAlchemy 2 (async) + Alembic | Implementado |
| Autenticação | JWT (python-jose) + bcrypt (passlib) | Implementado e validado end-to-end |
| Frontend | React 18 + Vite + TypeScript | Aprovado e implementado |
| Estado de sessão | Zustand (persist) | Implementado |
| HTTP client | Axios | Implementado |
| Roteamento | React Router v6 | Implementado |
| Execução local | Docker Compose v2 | Validado end-to-end em 20/10/2026 |
| IA — Etapa 2 | IBM watsonx Orchestrate + Granite | Aprovado, sem acesso ainda |
| Banco vetorial / RAG | Não adotar inicialmente | Excluído |
| Áudio | Adiado formalmente (D3) | Excluído do MVP |

### 1.4 Princípios e restrições

- Segredos nunca no código-fonte nem no controle de versão.
- Logs nunca expõem senhas, tokens ou dados sensíveis.
- Dois papéis: `student` e `admin`. Autorização verificada no backend em todas as rotas protegidas.
- Isolamento de dados: usuário A não acessa dados do usuário B.
- Sem ranking público.
- Sem integração bancária ou execução de transações.
- Mobile-first no frontend.

### 1.5 Status de conclusão da Etapa 1

| Critério estrutural da Etapa 1 | Evidência |
|---|---|
| Ambiente local e Docker Compose | `postgres`, `backend` e `frontend` sobem com `docker compose up`; healthcheck do banco ativo |
| FastAPI + React/Vite/TypeScript + PostgreSQL | Serviços operacionais; `/health`, `/docs` e frontend respondendo |
| Autenticação inicial | Cadastro, verificação de e-mail, login, refresh e recuperação de senha validados |
| Estrutura modular e contratos iniciais | Routers por módulo; OpenAPI com 25 rotas; respostas tipadas |
| Migração e seed | `alembic upgrade head` aplicado; 6 fases e 3 conquistas confirmadas no banco |
| Testes e validação | 38 testes de backend, 2 de frontend, build e E2E no navegador aprovados |

**Fora do escopo original da Etapa 1:** onboarding completo no frontend, telas do estudante além do Início e qualquer integração real de IA. Em 21/10/2026, as frentes sem IA foram antecipadas (onboarding, jornada, missão, progresso, conteúdo e critérios); a integração de IA continua fora de escopo até D7.

### 1.6 Preparação para a Etapa 2 (IA)

Os seguintes elementos foram desenhados para receber a IA sem reescrever a base:

- **Tabela `conversations`:** estrutura no banco pronta (campo `messages` JSONB, associação a `user_id` e `mission_id`).
- **Módulo `conversations`:** endpoints existem e retornam placeholder claro. Quando o Orchestrate estiver disponível, apenas a implementação do `service` muda — o router e a estrutura de dados permanecem.
- **Payload do Mentor já especificado:** definido na Decisão 4 do Documento 4. O backend já sabe o que enviar (fase, missão, objetivo, últimas 5 mensagens, dificuldades recorrentes, meta pessoal).
- **Motor de regras separado da IA:** `progress/service.py` nunca chama a IA. Pontos e conquistas são calculados independentemente.
- **Fallback educativo:** quando o Orchestrate estiver indisponível, o sistema apresenta conteúdo estático da missão. Esse conteúdo está modelado em `content_items` e a Fase 1 já tem 10 itens publicados pela migration `0002`; as telas `LessonPlayerPage` exibem esse conteúdo antes e depois da integração.

---

## 2. Decisões técnicas relevantes

### D1 — Número de fases: 6
**Status: Aprovado**  
Fases: Primeiro salário / Seu dinheiro no digital / Por que poupar / Juros: a favor e contra você / Onde o dinheiro rende / Proteção digital.  
Seed inserido na migration `0001_initial_schema.py`.

### D2 — MVP iterativo por fase
**Status: Aprovado**  
O piloto começa com a Fase 1 completa. A expansão para as fases seguintes depende dos resultados de cada piloto.

### D3 — Áudio adiado
**Status: Aprovado**  
Fora dos critérios de aceite do MVP. Não há nenhuma implementação de áudio no código atual.

### D4 — 2 agentes de IA no MVP
**Status: Aprovado**  
- **Mentor** (IA, tempo real) — espaço reservado no módulo `conversations`.
- **Analista de Progresso** (IA, background) — espaço reservado; regras determinísticas de detecção de dificuldade implementadas em `progress/service.py` (lógica de `incorrect_count`).
- **Catalisador** (backend determinístico) — implementado como lógica em `progress/service.py` e `journey/service.py`.

### D5 — Documento 4 parcialmente aprovado
**Status: Aprovado (18 decisões)**  
Ver `docs/Especificacao_Agentes_IA_ELL_IBM.md` v0.2. As demais 31 decisões estão adiadas para pós-piloto.

### D6 — Sistema de gamificação
**Status: Aprovado e implementado**  
- Missão na 1ª tentativa: 100 pts.
- Missão após reforço: 70 pts.
- Onboarding: 50 pts (bônus único).
- 5 níveis: Iniciante (0) / Consciente (300) / Planejador (700) / Estrategista (1200) / Autônomo (1800).
- Implementado em: `backend/app/modules/progress/service.py` — funções `calculate_level`, `add_points`, `grant_achievement`, `apply_mission_completion`.
- Testado: 16 testes unitários + testes de integração de conclusão, reforço e não duplicação de pontos.

### D7 — Spike Orchestrate bloqueado
**Status: Bloqueado — sem acesso ao ambiente**  
Checklist do spike registrado em `docs/Arquitetura_Tecnica_ELL_IBM.md` §22. A Etapa 1 não depende do Orchestrate.

### D8 — Conteúdo produzido pelo responsável do produto
**Status: Aprovado**  
O responsável do produto produzirá o conteúdo das missões em Markdown. O formato exato será definido quando o conteúdo for inserido. A tabela `content_items` e o endpoint `GET /api/v1/content/missions/{mission_id}` estão prontos para receber.

### D9 — Base legal LGPD
**Status: Proposto — validação jurídica pendente antes do lançamento**  
Onboarding coleta consentimento explícito (`consent_given`, `consent_version`, `consent_given_at` na tabela `profiles`). Campos implementados, fluxo de UI pendente.

### Decisão técnica: `asyncpg` + SQLAlchemy async
**Status: Adotado na implementação**  
Justificativa: consistência com o padrão assíncrono do FastAPI. Todas as queries usam `AsyncSession`. Consequência: as migrations do Alembic também precisam ser assíncronas (implementado em `alembic/env.py`).

### Decisão técnica: Modelos SQLAlchemy em `shared/models.py`
**Status: Adotado na implementação**  
Todos os modelos ORM centralizados em um único arquivo para evitar imports circulares entre módulos. Os módulos importam os modelos de `app.shared.models`. Consequência: o arquivo crescerá conforme novas entidades forem adicionadas — avaliar separação por grupo lógico se ultrapassar ~400 linhas.

### Decisão técnica: JWT stateless (sem revogação)
**Status: Adotado na implementação**  
Refresh token persiste no localStorage via Zustand. Não há blacklist de tokens. Consequência: logout no frontend apenas limpa o estado local — o token permanece válido até expirar. Risco aceitável para o MVP local; implementar revogação antes de produção.

### Decisão técnica: template completo do Alembic
**Status: Corrigido e verificado em 20/10/2026**  
`backend/alembic/script.py.mako` agora contém o template padrão. A geração de uma revisão de teste foi executada e produziu um arquivo válido; o arquivo de teste foi removido em seguida.

### Decisão técnica: SQL echo opt-in
**Status: Adotado e implementado**  
O engine não registra mais todas as queries SQL e seus parâmetros em desenvolvimento. `SQL_ECHO=false` é o padrão; ativar somente para depuração local pontual. Isso evita exposição de e-mails, hashes e outros parâmetros em logs.

### Decisão técnica: testes de integração com transação revertida
**Status: Adotado e implementado**  
Os testes de API usam o PostgreSQL real do Compose, com uma transação externa revertida ao final de cada teste e sessões de aplicação em savepoints. Isso valida queries, constraints e migrações sem deixar dados de teste no banco.

### Decisão técnica: pontuação de missão por histórico de erros
**Status: Adotado e implementado**  
Uma missão vale 100 pontos somente se nenhuma resposta incorreta tiver sido registrada para ela. Qualquer erro caracteriza reforço/nova tentativa e reduz a recompensa para 70 pontos. Respostas abertas não são avaliadas deterministicamente na Etapa 1 e não penalizam a pontuação.

### Decisão técnica: gabarito não vai ao cliente antes da resposta
**Status: Adotado e implementado**  
`GET /api/v1/journey/missions/{id}` remove `correct_answer`, `correct_choice`, `evaluation_criteria`, `feedback_correct` e `feedback_incorrect` do conteúdo das atividades antes de retornar ao estudante. O gabarito permanece no backend para avaliação determinística e o feedback chega apenas na resposta da submissão.

---

## 3. O que já foi feito

### 3.1 Arquivos criados

#### Raiz do projeto
```
docker-compose.yml       — 3 serviços: postgres, backend, frontend
.env.example             — todas as variáveis documentadas, sem valores reais
README.md                — instruções de setup e execução local
```

#### Backend (`backend/`)
```
Dockerfile
requirements.txt         — 14 dependências com versões fixadas
alembic.ini
alembic/env.py           — configurado para async com SQLAlchemy
alembic/versions/0001_initial_schema.py  — schema completo + seed de 6 fases + 3 conquistas
pytest.ini

app/__init__.py
app/main.py              — FastAPI app, CORS, routers registrados, handlers de erro
app/core/config.py       — Settings via pydantic-settings, lê .env
app/core/database.py     — engine async, AsyncSession, Base declarativa, get_db
app/core/security.py     — hash_password, verify_password, create_access_token,
                           create_refresh_token, decode_token, get_current_user, require_admin
app/core/exceptions.py   — error_response, validation_exception_handler, http_exception_handler
app/core/logging.py      — setup_logging, logger

app/shared/models.py     — todos os modelos ORM:
                           User, Profile, Phase, Mission, Competency, Activity,
                           UserMissionProgress, UserCompetencyProgress, UserPoints,
                           Achievement, UserAchievement, UserResponse, Conversation, ContentItem
                           + Enums: UserRole, MissionStatus, CompetencyStatus, AchievementConditionType

app/modules/auth/
  schemas.py             — RegisterRequest (com validação de senha), LoginRequest,
                           TokenResponse, RefreshRequest, PasswordResetRequest,
                           PasswordResetConfirm, MessageResponse
  service.py             — register_user, verify_email, login_user, refresh_tokens,
                           request_password_reset, confirm_password_reset,
                           _send_verification_email (mock em dev), _send_password_reset_email
  router.py              — POST /register, GET /verify-email, POST /login,
                           POST /refresh, POST /password-reset/request,
                           POST /password-reset/confirm

app/modules/users/
  schemas.py             — UserOut, ProfileOut, ProfileUpdate, OnboardingComplete, MeResponse
  service.py             — get_user_by_id, get_profile, update_profile, complete_onboarding
  router.py              — GET /me, PATCH /me/profile, POST /me/onboarding

app/modules/journey/
  schemas.py             — PhaseOut, MissionOut, CompetencyOut, ActivityOut, MissionDetailOut,
                           PhaseWithMissionsOut, UserMissionProgressOut,
                           UserCompetencyProgressOut, SubmitResponseRequest, SubmitResponseOut
  service.py             — get_all_phases, get_phases_with_user_progress, get_mission_detail,
                           start_mission, submit_activity_response, _evaluate_response
  router.py              — GET /phases, GET /phases/my-progress, GET /missions/{id},
                           POST /missions/{id}/start, POST /missions/{id}/submit

app/modules/progress/
  service.py             — calculate_level, add_points, grant_achievement,
                           grant_onboarding_bonus, calculate_mission_score,
                           apply_mission_completion, _check_phase_completion,
                           get_user_progress_summary, _level_name, _next_level_threshold
                           + constantes: LEVEL_THRESHOLDS, POINTS_FIRST_ATTEMPT,
                           POINTS_AFTER_REINFORCEMENT, POINTS_ONBOARDING, REINFORCEMENT_THRESHOLD
  router.py              — GET /summary

app/modules/content/
  router.py              — GET /missions/{id} (conteúdo publicado),
                           POST / (admin), PATCH /{id}/publish (admin)

app/modules/conversations/
  router.py              — POST /mentor (placeholder), GET /mentor/history
                           [PLACEHOLDER — retorna mensagem informando que o Mentor chegará na Etapa 2]

tests/
  test_gamification.py   — 16 testes: níveis, pontuação, nomes, progressão máxima
  test_auth_schemas.py   — 5 testes: validação de registro, e-mail, senha
```

#### Frontend (`frontend/`)
```
Dockerfile
package.json             — React 18, Vite, TypeScript, React Router v6, Zustand, Axios
vite.config.ts           — alias @/, proxy /api → backend, vitest config
tsconfig.json
index.html               — fonts Space Grotesk + Inter via Google Fonts

src/main.tsx             — entry point, monta <App />, importa tokens.css
src/App.tsx              — BrowserRouter, rotas: / → /student, /login, /register,
                           /student/* (protegido por ProtectedRoute)
src/test-setup.ts

src/design-system/
  tokens.css             — CSS custom properties: paleta completa, tipografia, espaçamento,
                           raios, sombras, transições, tema claro e escuro ([data-theme='dark'])
  Button.tsx + Button.module.css   — variantes: primary, secondary, ghost, danger
                                     tamanhos: sm, md, lg; loading spinner; acessível
  Input.tsx + Input.module.css     — label, hint, error, aria-invalid, aria-describedby
  index.ts               — re-exporta Button e Input

src/api/
  client.ts              — instância axios, interceptor de token (Authorization header),
                           interceptor de 401 (limpa sessão, redireciona /login)
  index.ts               — authApi, usersApi, journeyApi, progressApi, conversationsApi

src/store/
  session.ts             — Zustand + persist: user, accessToken, refreshToken,
                           isAuthenticated, setSession, clearSession, setUser

src/shared/
  ProtectedRoute.tsx     — verifica isAuthenticated e role, redireciona se não autorizado

src/areas/auth/
  LoginPage.tsx          — formulário de login, chama authApi.login + usersApi.getMe,
                           chama setSession, redireciona /student
  RegisterPage.tsx       — formulário de cadastro, exibe mensagem de sucesso
  Auth.module.css

src/areas/student/
  StudentLayout.tsx      — sidebar (desktop) + bottom nav (mobile), logout
  StudentLayout.module.css — responsivo: sidebar some em ≤768px, bottom nav aparece
  StudentHome.tsx        — carrega summary + phases/my-progress, exibe stats e mapa de fases
  Student.module.css
```

### 3.2 Documentos atualizados em `docs/`

| Arquivo | Alterações |
|---|---|
| `PRD_ELL_IBM.md` | Versão 1.1: 6 fases, MVP iterativo, agentes, gamificação com regras numéricas, áudio adiado, privacidade com base legal, critérios de aceite e pendências atualizados |
| `Arquitetura_Tecnica_ELL_IBM.md` | 6 fases, D4 (Catalisador determinístico), checklist do spike Orchestrate |
| `Especificacao_Agentes_IA_ELL_IBM.md` | Versão 0.2: 18 decisões aprovadas, 31 adiadas formalmente |

### 3.3 Testes executados na sessão 1 (histórico)

```
Comando: cd backend && python3 -m pytest tests/ -v
Resultado: 21 passed in 0.42s (executado e verificado na sessão 1)

Cobertura:
  test_auth_schemas.py   — 5 testes: validação de registro (Pydantic)
  test_gamification.py   — 16 testes: lógica de pontos e níveis (D6)
```

Na sessão 1, os testes de integração abaixo ainda não existiam. Eles foram criados e executados na sessão 2.

### 3.4 Seed de dados na migration

A migration `0001_initial_schema.py` insere automaticamente ao aplicar `alembic upgrade head`:

**6 fases:**
- Fase 1 — Primeiro salário
- Fase 2 — Seu dinheiro no digital
- Fase 3 — Por que poupar
- Fase 4 — Juros: a favor e contra você
- Fase 5 — Onde o dinheiro rende
- Fase 6 — Proteção digital

**3 conquistas:**
- `primeiro_passo` — concluir o onboarding
- `planejador_iniciante` — concluir as 3 missões da Fase 1
- `sem_duvidas` — concluir uma missão sem intervenção do Mentor

### 3.5 Sessão 2 — correções, testes e conclusão

#### Arquivos criados

| Arquivo | Finalidade |
|---|---|
| `.gitignore` | Impedir versionamento de `.env`, caches, `node_modules`, builds e artefatos locais |
| `backend/.dockerignore` / `frontend/.dockerignore` | Reduzir contexto de build e evitar copiar caches/segredos para imagens |
| `backend/tests/conftest.py` | Fixtures de API, banco real e transação revertida |
| `backend/tests/test_api_auth.py` | Integração de cadastro, verificação, login, onboarding idempotente, reset e refresh |
| `backend/tests/test_isolation.py` | Isolamento entre usuários, autorização e tokens inválidos |
| `backend/tests/test_journey_api.py` | Início, submissão, pontuação, gabarito protegido e não duplicação |
| `backend/tests/test_conversations_api.py` | Persistência do placeholder do Mentor e isolamento do histórico |
| `frontend/src/areas/auth/VerifyEmailPage.tsx` | Tratamento do link de verificação de e-mail |
| `frontend/src/areas/auth/ForgotPasswordPage.tsx` | Solicitação de recuperação de senha |
| `frontend/src/areas/auth/ResetPasswordPage.tsx` | Definição de nova senha |
| `frontend/src/vite-env.d.ts` | Tipos do Vite e de CSS Modules para o build TypeScript |
| `frontend/src/store/session.test.ts` | Testes do estado de sessão |
| `frontend/package-lock.json` | Lockfile reproduzível; Dockerfile passou a usar `npm ci` |

#### Arquivos alterados

| Arquivo | Alteração |
|---|---|
| `backend/requirements.txt` | Incluídos `email-validator` e `bcrypt==4.0.1` (compatibilidade com passlib) |
| `backend/alembic/versions/0001_initial_schema.py` | Enums sem duplicação e seed de conquistas com cast explícito |
| `backend/alembic/script.py.mako` | Template completo do Alembic |
| `backend/app/core/config.py`, `database.py` | `SQL_ECHO` opt-in; logs SQL deixam de expor parâmetros por padrão |
| `backend/app/modules/users/service.py` | Onboarding idempotente, sem duplicar 50 pontos |
| `backend/app/modules/progress/service.py` | Pontuação considera erros anteriores; corrigida consulta com múltiplas respostas |
| `backend/app/modules/journey/router.py` | Remoção de gabarito, critérios e feedbacks privados da resposta ao estudante |
| `backend/app/modules/conversations/router.py` | Persistência correta de mensagens JSONB e `updated_at` |
| `backend/pytest.ini` | Escopo padrão de fixtures assíncronas definido |
| `docker-compose.yml` | Porta do host configurável via `POSTGRES_HOST_PORT` |
| `.env.example` | Incluídos `POSTGRES_HOST_PORT`, `SQL_ECHO` e aviso sobre `DATABASE_URL` |
| `frontend/Dockerfile` | `npm ci` em vez de `npm install` |
| `frontend/src/api/client.ts` | 401 limpa o store, não apenas o localStorage |
| `frontend/src/api/index.ts`, `LoginPage.tsx` | Token enviado explicitamente no `/users/me` imediatamente após o login |
| `frontend/src/areas/student/StudentHome.tsx` | Tratamento de erro, retry e estado vazio |
| `frontend/src/App.tsx`, `Auth.module.css` | Rotas e estados visuais de verificação/recuperação |
| `README.md` | Portas, teste, migração, `DATABASE_URL` e solução de conflito de porta |

#### Testes executados na sessão 2

```
docker compose exec backend pytest -q
→ 38 passed, 28 warnings

docker compose exec frontend npm test -- --run
→ 2 passed (1 arquivo)

docker compose exec frontend npm run build
→ tsc -b && vite build concluídos

cd backend && python3 -m pytest -q
→ 21 passed, 17 skipped (integração sem PostgreSQL local)

docker compose exec backend alembic check
→ No new upgrade operations detected
```

O E2E foi executado em Chrome headless, viewport mobile (390×844), contra os containers:

```
cadastro: ok
verificação de e-mail: ok
login: ok
fases renderizadas: 6
progresso: 0 pontos / Nível 1 / Iniciante
recarga preservando sessão: ok
recuperação de senha: ok
login com nova senha: ok
recursos com erro no browser: nenhum
```

O harness E2E residiu em diretório temporário fora do repositório e não adicionou dependência ao projeto.

#### Validações adicionais

- `pip check` → `No broken requirements found`.
- `python -m compileall -q app` → sem erros.
- `docker compose config --quiet` → configuração válida.
- Serviços finais: backend em `:8000`, frontend em `:5173`, PostgreSQL em `:5433` neste ambiente (conflito com PostgreSQL local na `5432`).
- Usuários criados durante os testes automatizados foram revertidos com as transações. O banco local mantém **1 conta de teste verificada**, criada apenas para acesso manual pelo navegador; as credenciais não fazem parte do código nem do `.env`.

---

## 4. Onde o trabalho parou

- **Etapa 1:** concluída no escopo estrutural definido pela Arquitetura.
- **Frentes sem IA da Etapa 2:** antecipadas em 21/10/2026 (ver seção 10).
- **Última tarefa concluída:** conteúdo da Fase 1, contrato JSONB, critérios de domínio, regras de desbloqueio, onboarding e telas do estudante.
- **Tarefa em andamento:** revisão pedagógica do conteúdo/critérios e E2E automatizado de interação.
- **Última verificação executada nesta sessão:**
  ```
  docker compose exec backend alembic upgrade head
  → 0002 (head)

  docker compose exec backend pytest -q
  → 53 passed

  docker compose exec frontend npm test -- --run
  → 29 passed (11 arquivos)

  docker compose exec frontend npm run build
  → tsc -b && vite build aprovados
  ```
- **Fluxo de API validado no Compose:** cadastro → verificação → login → onboarding → missão 1.1 → desbloqueio da 1.2 → progresso. O gabarito, os critérios e os feedbacks de acerto/erro não aparecem antes da submissão.
- **Não executado nesta sessão:** E2E em navegador real; a validação de API cobriu o fluxo vertical sem interface.
- **Ambiente local:** `.env` criado com segredos gerados (não versionado); `POSTGRES_HOST_PORT=5433` por conflito com um PostgreSQL já ativo na máquina.
- **Próxima ação:** validar o fluxo completo em navegador automatizado e revisar pedagogicamente os minicursos; a integração de IA segue bloqueada por D7. Ver seção 7.

---

## 5. Estado das tarefas da Etapa 1

### P0 — Bloqueadores

| Item | Estado | Evidência |
|---|---|---|
| **Validação Docker end-to-end** | Concluída | 3 containers saudáveis; `localhost:5173`, `localhost:8000/health` e `/docs` respondem |
| **Migração aplicada** | Concluída | `alembic current` = `0001 (head)`; 6 fases e 3 conquistas verificadas |

### P1 — Essenciais

| Item | Estado | Evidência |
|---|---|---|
| **Fluxo de cadastro → login funcional** | Concluída | Playwright: cadastro, verificação, login, home, reload e recuperação de senha |
| **Template do Alembic** | Concluída | Template padrão instalado; geração de revisão de teste funcionou |
| **Testes de integração API** | Concluída | 17 testes de integração com PostgreSQL real |
| **Testes de isolamento** | Concluída | `backend/tests/test_isolation.py`, incluindo autorização de admin e tokens |
| **Frontend compilando** | Concluída | `tsc -b && vite build` aprovados |

### P2 — Importantes

| Item | Estado | Observação |
|---|---|---|
| **Páginas do estudante além do Home** | Concluída em 21/10/2026 | `JourneyPage`, `MissionPage`, `ProgressPage` e `ProfilePage`; conteúdo via API real |
| **Fluxo de onboarding no frontend** | Concluído em 21/10/2026 | Wizard de 3 passos, gate de onboarding e consentimento LGPD; endpoint real |
| **Página de verificação de e-mail** | Concluída | `VerifyEmailPage.tsx` |
| **Páginas de recuperação de senha** | Concluída | `ForgotPasswordPage.tsx` e `ResetPasswordPage.tsx` |
| **`.gitignore`** | Concluída | `.env`, caches, dependências e builds cobertos |
| **`VITE_API_BASE_URL` no Docker** | Verificada | O cliente usa a URL absoluta configurada; CORS e login validados no browser. O proxy Vite não é usado pelo cliente atual. |
| **Tratamento de erro no Home** | Concluída | Estado de erro com retry e estado vazio |
| **Testes de componente/fluxo no frontend** | Concluída em 21/10/2026 | 29 testes: store, landing, auth, ProtectedRoute, OnboardingGate, Home, Jornada, Minicurso, Progresso, Mentor e Onboarding |

### P3 — Pós-MVP ou etapas futuras (adiados intencionalmente)

| Item | Motivo do adiamento |
|---|---|
| Integração watsonx Orchestrate (Mentor + Analista) | Sem acesso ao ambiente — spike obrigatório antes |
| Áudio | Decisão D3: adiado formalmente |
| Painel administrativo | Implementado após o sistema principal do estudante |
| Narrativa contínua com personagens | Aguarda validação do engajamento real |
| Quizzes gerados por LLM | Aguarda integração com Orchestrate |
| Desafio integrador | Aguarda conclusão de todas as 6 fases |
| Ações práticas opcionais fora do app | Aguarda validação do núcleo pedagógico |
| Notificações e lembretes | Aguarda dados de uso real |
| RAG / banco vetorial | Não necessário inicialmente |
| Hospedagem produtiva | Fora do escopo do MVP local |

---

## 6. Pendências e riscos

### 6.1 Bloqueante externo
- **watsonx Orchestrate sem acesso:** o responsável do produto não tem acesso ao ambiente. Nenhuma implementação de agente de IA pode ser feita até o spike ser concluído. Checklist completo em `docs/Arquitetura_Tecnica_ELL_IBM.md` §22.

### 6.2 Pendências de produto
- **Conteúdo das missões produzido e carregado:** as 3 missões da Fase 1 estão em `backend/app/modules/content/seeds/phase_1_v1.py` e na migration `0002`; a referência editorial é `docs/fase-1-primeiro-salario.md`. Falta revisão final de produto/pedagógico.
- **Critérios de domínio documentados e implementados:** ver `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`. Os limiares de reforço ainda precisam de validação com o piloto.
- **Contrato JSONB formalizado:** `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md` e `backend/app/modules/content/activity_schema.py`.
- **Guia de produção:** `docs/GUIA_PRODUCAO_CONTEUDO.md`.

### 6.3 Segurança e privacidade
- **Base legal LGPD não validada juridicamente:** proposta registrada no PRD §10.4. Não lançar o piloto sem essa validação.
- **JWT sem revogação:** aceitável para MVP local, mas deve ser resolvido antes de qualquer ambiente compartilhado ou produção. O frontend também não renova o token automaticamente; ao expirar, o usuário precisa entrar novamente.
- **Verificação de e-mail e reset como mock:** em desenvolvimento, os tokens são apenas logados no terminal. Isso é correto para dev, mas exige configuração SMTP real para qualquer piloto com usuários reais.
- **`.env` e segredos:** `.env` local foi criado com credenciais geradas, tem permissão `600` e está coberto pelo `.gitignore`. Nenhum segredo foi adicionado ao código ou à documentação.
- **Logs:** o `SQL_ECHO` passou a ser opt-in (`false` por padrão), evitando registrar parâmetros de queries. Logs de aplicação continuam sem senha; o token de verificação/reset aparece apenas no mock de e-mail de desenvolvimento.
- **Dependências frontend:** `npm audit --omit=dev` reporta 2 vulnerabilidades moderadas em `react-router`/`react-router-dom` 6.30.6. O fix disponível exige upgrade major para React Router 7.18.4. O conjunto completo (incluindo dev) reporta 8 vulnerabilidades (2 críticas em Vitest/Tinypool, 1 alta em Vite e 5 moderadas). Não houve upgrade forçado nesta etapa; a decisão de migrar para React Router 7 precisa ser autorizada e validada com os testes de fluxo.

### 6.4 Riscos técnicos
- **Migration `0002` ainda não aplicada neste ambiente:** o conteúdo está versionado e os testes de contrato passam, mas a carga em PostgreSQL real precisa ser validada com o Compose.
- **Conclusão de fase:** `_check_phase_completion` considera todas as missões obrigatórias existentes no banco. O seed tem exatamente 3 missões obrigatórias na Fase 1; qualquer conteúdo futuro deve preservar essa validação (coberta por `test_content_schema.py`).
- **Cobertura de frontend ampliada:** 29 testes cobrem store, landing, auth, `ProtectedRoute`, `OnboardingGate`, Home, Jornada, Minicurso, Progresso, Mentor e Onboarding. Ainda faltam testes E2E e de acessibilidade automatizada.
- **Regras de desbloqueio:** implementadas de forma sequencial e cobertas por teste de integração que será executado quando houver PostgreSQL. Os limiares pedagógicos continuam como proposta a validar.
- **Respostas abertas:** continuam sem avaliação semântica; contam para conclusão e não penalizam pontos. A avaliação por IA só entra após D7.
- **`npm test` no host:** a suíte frontend exige `node_modules` e `jsdom`; o caminho reproduzível é via container. O `package-lock.json` foi criado e o Dockerfile usa `npm ci`.
- **Porta local:** neste ambiente, o PostgreSQL do host ocupa `5432`; o Compose foi configurado com `POSTGRES_HOST_PORT=5433`. O valor padrão do `.env.example` continua `5432`.

### 6.5 Divergências e dívidas documentais identificadas
- **PRD §14 e §18 corrigidos em 21/10/2026:** o texto agora reflete a arquitetura aprovada/implementada e o estado do conteúdo. A frase do §13 sobre o diagrama lógico também foi ajustada.
- **Documento 5 §2.3:** ainda menciona como pendente a atualização do PRD/Arquitetura para seis fases, já realizada. Não é bloqueante.
- **Git:** o diretório não é um repositório Git. Não foi possível verificar diffs, branches ou commits. `.gitignore` foi criado, mas a inicialização do repositório e o primeiro commit não foram executados por não fazerem parte do escopo solicitado.
- Nenhuma nova divergência de escopo D1–D9 foi encontrada no código.

---

## 7. Instruções para a próxima LLM

### Passo a passo obrigatório antes de qualquer ação

1. **Leia este documento na íntegra** antes de abrir qualquer arquivo de código.
2. **Inspecione a estrutura atual:**
   ```bash
   find backend/app frontend/src -type f | sort
   ```
3. **Verifique os containers e os testes existentes:**
   ```bash
   docker compose ps
   docker compose exec backend pytest -q
   # Esperado: 38 passed
   docker compose exec frontend npm test -- --run
   # Esperado: 2 passed
   ```
   Fora do Docker, `cd backend && pytest` executa 21 unitários e marca os 17 de integração como `skipped` se não houver PostgreSQL acessível.
4. **Consulte os documentos de referência na ordem:**
   - `docs/CONTINUIDADE_ETAPA_1.md` (este arquivo)
   - `docs/Arquitetura_Tecnica_ELL_IBM.md`
   - `docs/PRD_ELL_IBM.md`
   - `docs/Especificacao_Agentes_IA_ELL_IBM.md` (se trabalhar com agentes)

5. **Não reinicie a Etapa 1.** Verifique o estado antes de alterar qualquer arquivo.

### Regras operacionais

- **Não recriar** arquivos ou funcionalidades que já existem. Verifique antes de criar.
- **Não reabrir** decisões D1–D9 sem identificar uma contradição concreta e documentada.
- **Não presumir** que o watsonx Orchestrate está disponível. Nenhuma implementação de IA real antes do spike.
- **Não inventar** endpoints, campos de banco, regras de desbloqueio ou comportamentos não especificados.
- **Não implementar a Etapa 2** sem autorização e sem cumprir D7.
- **Manter o backend como autoridade** sobre pontos, desbloqueios, persistência e integridade.
- **Implementar incrementalmente:** uma tarefa por vez, testar, confirmar, avançar.
- **Atualizar este documento** ao final de cada marco relevante, mantendo-o fiel ao estado real.

### Como iniciar o projeto localmente

```bash
# 1. Criar o arquivo de variáveis de ambiente
cp .env.example .env

# 2. Editar .env — obrigatório antes de subir:
#    SECRET_KEY=<gere com: python3 -c "import secrets; print(secrets.token_hex(32))">
#    POSTGRES_PASSWORD=<escolha uma senha>
#    DATABASE_URL=<mesma senha e usuário na URL asyncpg>
#    POSTGRES_HOST_PORT=5433  # somente se 5432 já estiver ocupada no host
#    SQL_ECHO=false

# 3. Subir os serviços
docker compose up -d --build

# 4. Aplicar migrações (primeira vez)
docker compose exec backend alembic upgrade head

# 5. Validar
curl http://localhost:8000/health
docker compose exec backend pytest -q
docker compose exec frontend npm test -- --run
docker compose exec frontend npm run build

# 6. Acessar
# Frontend:  http://localhost:5173
# API docs:  http://localhost:8000/docs
# API redoc: http://localhost:8000/redoc

# 7. Verificar tokens de e-mail/reset (mock em dev)
docker compose logs backend | grep "MOCK EMAIL"
```

### Próxima ação autorizada

As frentes sem IA já foram antecipadas. O trabalho de IA continua bloqueado por D7.

1. **Validar as migrations `0002`–`0004` em ambiente limpo:**
   ```bash
   docker compose up -d --build
   docker compose exec backend alembic upgrade head
   docker compose exec backend pytest -q
   docker compose exec frontend npm test -- --run
   docker compose exec frontend npm run build
   ```
2. **Revisar produto/pedagógico:** conteúdo das 3 missões, contrato JSONB e
   critérios de domínio/reforço.
3. **Validar o fluxo vertical no navegador:** cadastro → onboarding → missão 1.1
   → desbloqueio da 1.2 → progresso.
4. **Obter acesso ao Orchestrate** e executar o checklist do spike em
   `docs/Arquitetura_Tecnica_ELL_IBM.md` §22.
5. **Validar a base legal LGPD** antes de qualquer piloto com usuários reais.
6. Somente depois do spike, iniciar a integração de IA.

A integração de IA não deve ser simulada com um LLM fake local. O módulo
`conversations` mantém o contrato atual e o fallback estático é o conteúdo das
missões, já disponível em `content_items`.

---

## 8. Estado dos arquivos críticos (checksums não disponíveis — verificar existência)

Os seguintes arquivos são críticos para o funcionamento do sistema. Verifique a existência antes de assumir que estão presentes:

| Arquivo | Função crítica |
|---|---|
| `backend/app/shared/models.py` | Todos os modelos ORM — base de tudo |
| `backend/app/core/security.py` | Hash, JWT, autenticação |
| `backend/app/modules/progress/service.py` | Motor de gamificação, competências e reforço |
| `backend/app/modules/content/activity_schema.py` | Contrato do JSONB de atividades |
| `backend/app/modules/content/seeds/phase_1_v1.py` | Conteúdo versionado da Fase 1 |
| `backend/alembic/versions/0001_initial_schema.py` | Schema completo + seed |
| `backend/alembic/versions/0002_phase_1_content.py` | Códigos de competência + conteúdo da Fase 1 |
| `frontend/src/store/session.ts` | Estado de sessão e perfil persistidos |
| `frontend/src/api/client.ts` | Interceptors de autenticação e limpeza de sessão |
| `frontend/src/shared/OnboardingGate.tsx` | Bloqueio de acesso antes do onboarding |
| `frontend/src/areas/student/MissionPage.tsx` | Experiência de missão e submissão |
| `frontend/src/areas/student/JourneyPage.tsx` | Mapa de fases e missões |
| `frontend/src/areas/auth/VerifyEmailPage.tsx` | Tratamento do link de verificação |
| `frontend/src/areas/auth/ForgotPasswordPage.tsx` | Solicitação de recuperação |
| `frontend/src/areas/auth/ResetPasswordPage.tsx` | Definição de nova senha |
| `backend/tests/conftest.py` | Fixtures de integração com transação revertida |
| `backend/tests/test_api_auth.py` | Cobertura de autenticação e onboarding |
| `backend/tests/test_isolation.py` | Cobertura de isolamento e autorização |
| `backend/tests/test_journey_api.py` | Cobertura de missões e pontuação |
| `backend/tests/test_conversations_api.py` | Cobertura do placeholder do Mentor |
| `.env.example` | Referência de todas as variáveis necessárias |
| `docker-compose.yml` | Orquestração dos 3 serviços |

---

## 9. Camada visual Prisma.AI — landing e autenticação

**Status:** implementada e validada em 20/10/2026.

### Landing pública

- Rota pública: `/`.
- Componentes em `frontend/src/areas/landing/`.
- Seções: navbar sticky, hero com prisma e preview de produto, solução em bento, como funciona, agentes, experiência interativa, autonomia, CTA final e footer.
- Efeitos: partículas em canvas, gradientes animados, spotlight cards, tilt 3D, parallax, reveals e botões magnéticos, com suporte a `prefers-reduced-motion`.
- Motion/Framer Motion é a única dependência de animação adicionada; os efeitos são equivalentes próprios inspirados em React Bits (Particles, SpotlightCard, TiltedCard, SplitText e efeitos de fundo), sem WebGL.
- CTAs usam rotas reais existentes: `/login`, `/register`, `/forgot-password` e âncoras internas.
- Páginas jurídicas permanecem identificadas como “em breve”, sem links falsos.

### Autenticação

- Login, cadastro, verificação de e-mail, recuperação e redefinição de senha compartilham `AuthShell`, `AuthVisuals`, `AuthField`, `PasswordStrength` e tokens de marca.
- `LoginPage`: validação por campo, foco no primeiro erro, feedback de API, revelar/ocultar senha e sessão real.
- `RegisterPage`: regras de senha em tempo real, medidor de força, estado de sucesso e instrução de verificação.
- Componentes de marca compartilhados: `design-system/Icons.tsx` e `design-system/brand/` (`Logo`, `PrismArt`, `ParticleField`, `brand.css`).
- Visual desktop dividido; em telas menores a composição visual é ocultada e o formulário recebe prioridade.
- Nenhuma integração foi simulada: os handlers chamam `authApi`/`usersApi` existentes.

### Testes executados

```text
docker compose exec frontend npm test -- --run
→ 13 passed (store, landing e 8 fluxos de autenticação)

docker compose exec frontend npm run build
→ tsc -b && vite build aprovados

docker compose exec backend pytest -q
→ 38 passed
```

Validação E2E em Chrome headless:

```text
login: validação, erro de API, revelar senha e navegação para /student
cadastro: validação, força de senha, sucesso e e-mail exibido
verificação de e-mail real: ok
login após verificação: ok
recuperação e redefinição de senha: ok
login com nova senha: ok
larguras 320/360/390/768/1024/1440: sem overflow horizontal
erros de console: nenhum
```

---

## 10. Sessão 3 — frentes sem IA (21/10/2026)

### 10.1 O que foi implementado

**Conteúdo e banco**

- `backend/app/modules/content/activity_schema.py`: contrato Pydantic versionado
  para `activities.content`, com validação de alternativas, gabarito,
  competências e critérios de resposta aberta.
- `backend/app/modules/content/seeds/phase_1_v1.py`: 3 missões, 9 competências,
  12 atividades e 10 itens de conteúdo da Fase 1.
- `backend/app/modules/content/seeds/phase_1.py`: upsert idempotente por chave
  natural.
- `backend/alembic/versions/0002_phase_1_content.py`: adiciona
  `competencies.code` e carrega a Fase 1.
- `backend/tests/test_content_schema.py`: valida o contrato, a cobertura de
  competências e as 3 missões obrigatórias.

**Domínio, gamificação e desbloqueio**

- `progress/service.py`: registro de evidência por competência, status
  `not_started` / `developing` / `demonstrated`, contagem de acertos/erros e
  sinal de reforço determinístico.
- `progress/service.py`: `GET /progress/summary` agora inclui competências,
  `current_level_points` e o indicador de reforço.
- `journey/service.py`: desbloqueio sequencial de missões e fases, status
  calculado no mapa e bloqueio de `start`/`submit` com 403.
- `journey/router.py`: `evaluation_criteria`, `feedback_correct` e
  `feedback_incorrect` também são removidos da resposta ao estudante; a missão inclui `user_status`, `is_unlocked` e `progress`.
- `backend/tests/test_progression_api.py`: cobertura de bloqueio, evidência de
  competência e reforço (integração).

**Frontend**

- `OnboardingPage` + `OnboardingGate`: wizard de 3 passos, coleta de objetivo,
  nível e consentimento LGPD, com gate antes da jornada.
- `JourneyPage`: mapa de fases e missões com status e bloqueio.
- `MissionPage`: conteúdo educacional, início explícito da missão, múltipla
  escolha, simulação, resposta aberta, feedback e conclusão.
- `ProgressPage`: nível, pontos, competências e conquistas.
- `ProfilePage`: dados de conta, objetivo e consentimento.
- `RichText`: renderização segura de Markdown básico, sem `innerHTML`.
- `types/student.ts`: contratos tipados da área do estudante.
- 29 testes de frontend em 11 arquivos, incluindo Home, Jornada, Minicurso, Progresso, Mentor,
  Onboarding e `ProtectedRoute`.

**Documentação**

- `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md`
- `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`
- `docs/GUIA_PRODUCAO_CONTEUDO.md`
- PRD §13, §14, §16, §17 e §18 atualizados.

### 10.2 Verificações executadas

```text
docker compose exec backend alembic upgrade head
→ 0002 (head)

docker compose exec backend pytest -q
→ 53 passed

docker compose exec frontend npm test -- --run
→ 29 passed (11 arquivos)

docker compose exec frontend npm run build
→ tsc -b && vite build aprovados

docker compose exec backend alembic check
→ No new upgrade operations detected

# banco vazio → 0001 → 0002
alembic upgrade head
→ 3 missões, 9 competências, 12 atividades, 10 itens publicados
```

Fluxo de API verificado em PostgreSQL real: cadastro, verificação, login,
onboarding, leitura da missão sem gabarito, submissão, pontuação, competência
demonstrada e desbloqueio da missão 2.

Não executado nesta sessão: E2E em navegador real. O fluxo vertical foi
validado por API e pelos testes de componente.

### 10.3 Pendências imediatas

1. Revisar produto/pedagógico do conteúdo e dos critérios.
2. Validar o fluxo no navegador (onboarding → missão 1.1 → 1.2 → progresso).
3. Validar LGPD e textos de consentimento.
4. Manter a integração de IA bloqueada até o spike D7.

### 10.4 O que não foi feito de propósito

- Nenhum LLM fake, mock de Mentor ou simulação de Orchestrate.
- Nenhuma alteração no contrato do módulo `conversations`.
- Nenhuma migração forçada para React Router 7.
- Nenhuma fase 2–6 inventada sem conteúdo/revisão.

---

## 11. Redesign visual da área do estudante (21/10/2026)

### 11.1 Direção implementada

- Tema claro com canvas lavanda, cartões de vidro, tipografia Space Grotesk/Inter e acentos violeta, azul, mint e coral.
- Sidebar escura premium com identidade Prisma.AI, navegação por ícones, cartão do Mentor e perfil.
- Navegação móvel flutuante, com safe area e cinco áreas.
- Personagem/mascote prismático em SVG, sem dependência de imagens externas.
- Identidade visual própria para os três agentes, com avatares e cores oficiais.
- Sistema de ilustrações por fase (`PhaseArt`) e anéis de progresso.
- Microinterações e animações com `prefers-reduced-motion`.
- Rotas com code splitting (`React.lazy`), eliminando o chunk único acima de 500 kB.

### 11.2 Telas redesenhadas

| Tela | Arquivos principais |
|---|---|
| Shell e navegação | `StudentLayout.tsx`, `StudentLayout.module.css`, `student-theme.css` |
| Início | `StudentHome.tsx`, `Home.module.css` |
| Jornada | `JourneyPage.tsx`, `Journey.module.css` |
| Missão | `MissionPage.tsx`, `Mission.module.css` |
| Progresso | `ProgressPage.tsx`, `Progress.module.css` |
| Perfil | `ProfilePage.tsx`, `Profile.module.css` |
| Mentor e agentes | `MentorPage.tsx`, `Mentor.module.css` |
| Onboarding | `OnboardingPage.tsx`, `Onboarding.module.css` |
| Componentes visuais | `components/StudentVisuals.tsx` e CSS module |

### 11.3 Funcionalidades preservadas

- Todos os dados continuam vindo das APIs reais; nenhum valor foi inventado.
- Regras de desbloqueio, pontuação, competências e conquistas permanecem no backend.
- O contrato do módulo `conversations` não foi alterado.
- O Mentor continua apresentando indisponibilidade honesta, sem simular IA.
- O fallback estático aponta para o conteúdo real das missões.
- Formulários, onboarding, consentimento e submissão de atividades seguem funcionando.

### 11.4 Verificação visual executada

Capturas em Chrome headless com dados reais de um usuário de teste:

- desktop 1440×1000: Início, Jornada, Missão em andamento, Missão concluída, Progresso, Mentor, Perfil e Onboarding;
- tablet 768×1024: Início;
- mobile 390×844: Início, Missão, Jornada e Onboarding;
- larguras 320, 360, 390, 768, 1024, 1440 e 1920: sem overflow horizontal;
- console do navegador: nenhum erro;
- títulos de página corretos por rota.

### 11.5 Pendências visuais

- Revisão humana de contraste e testes com leitores de tela.
- Testes E2E de interação (login → onboarding → missão → progresso) em navegador automatizado.
- Validação das referências visuais externas, que não estavam anexadas ao repositório nesta sessão.

---

## 12. Minicursos imersivos das Trilhas 1 e 2 (21/10/2026)

**Status:** implementado e validado no Compose e em Chrome headless.  
**Documento de referência:** `docs/MINICURSOS_TRILHAS_1_2.md`.

### 12.1 Arquitetura

- `missions.lesson_flow` (JSONB) define o roteiro imersivo.
- Cada missão existente é um minicurso; não foram criadas tabelas paralelas.
- O roteiro referencia `content_items` e `activities` já versionados.
- `user_mission_progress.current_step` e `completed_steps` persistem a retomada.
- Migration `0004_immersive_lesson_flow.py` adiciona os campos e os roteiros.
- `GET /journey/missions/{id}/lesson` devolve etapas, feedback anterior, progresso
  e próximo minicurso.
- `POST /journey/missions/{id}/lesson/progress` marca a etapa e avança o cursor.
- O envio de resposta continua usando o endpoint existente; a etapa só avança
  depois do feedback.
- Respostas incorretas exigem nova tentativa e não marcam a etapa como concluída.

### 12.2 Experiência

- Rota `/student/learn/{mission_id}` fora do `StudentLayout`: sem sidebar, menu
  ou abas inferiores.
- Uma etapa por tela: introdução, leitura, questão, cenário, síntese.
- Topbar com saída, progresso, etapa atual e controle de efeitos.
- Saída com confirmação; progresso já salvo é preservado.
- Retomada restaura a etapa e o feedback confirmado.
- Tela final com pontos, competências, próximas etapas e retomada da jornada.
- Som via Web Audio API, vibração via `navigator.vibrate`, ambos opcionais e
  desativados por padrão; preferência persistida localmente.
- Confete no desktop; oculto no mobile para preservar leitura.

### 12.3 Conteúdo

- Trilha 1: 3 minicursos, 9–10 etapas cada, ~18 min no total.
- Trilha 2: 3 minicursos, 9–10 etapas cada, ~19 min no total.
- Conteúdo existente preservado e complementado por telas de introdução,
  contexto e síntese com objetivos e competências.

### 12.4 Testes

```text
docker compose exec backend pytest -q
→ 53 passed

docker compose exec frontend npm test -- --run
→ 29 passed (11 arquivos)

docker compose exec frontend npm run build
→ build aprovado
```

Validação em Chrome headless: introdução, leitura, questão, feedback, retomada
e resumo em desktop; introdução e etapa atual em mobile; ausência de navegação
principal; um único grupo de opções por tela; sem overflow e sem erros de
console.

---

*Documento atualizado em 21/10/2026. Estado verificado no Docker Compose: migrations `0002`–`0004` aplicadas; 53 testes de backend (26 unitários + 27 de integração) e 29 de frontend passando; build aprovado. Minicursos imersivos das Trilhas 1 e 2 validados em Chrome headless em desktop e mobile. A revisão pedagógica/LGPD e o E2E automatizado de interação permanecem como próxima ação. A integração de IA segue bloqueada por D7.*

---

## 13. Conteúdo das Trilhas 3 a 6 (22/10/2026)

**Status:** implementado e validado no Compose.  
**Documento de referência:** `docs/MINICURSOS_TRILHAS_3_6.md`.

### 13.1 O que foi implementado

| Arquivo | Finalidade |
|---|---|
| `backend/app/modules/content/seeds/phase_3_v1.py` | 3 missões, 9 competências, 13 atividades e 9 itens de conteúdo da Fase 3 |
| `backend/app/modules/content/seeds/phase_4_v1.py` | 3 missões, 9 competências, 13 atividades e 9 itens de conteúdo da Fase 4 |
| `backend/app/modules/content/seeds/phase_5_v1.py` | 3 missões, 9 competências, 13 atividades e 9 itens de conteúdo da Fase 5 |
| `backend/app/modules/content/seeds/phase_6_v1.py` | 4 missões, 10 competências, 17 atividades e 9 itens de conteúdo da Fase 6 |
| `backend/app/modules/content/seeds/seeder.py` | Upsert idempotente compartilhado pelas Fases 3–6 |
| `backend/app/modules/content/seeds/phase_3.py` a `phase_6.py` | Loaders por fase |
| `backend/app/modules/content/lesson_flows.py` | Roteiros imersivos das Trilhas 3–6 |
| `backend/alembic/versions/0005`–`0009` | Conteúdo, conquistas e roteiros |
| `backend/tests/test_content_phases_3_6.py` | Contrato, competências, conteúdo e roteiros |
| `docs/MINICURSOS_TRILHAS_3_6.md` | Referência pedagógica e técnica |

### 13.2 Conteúdo

- Trilha 3: metas, equilíbrio do orçamento e reserva de emergência.
- Trilha 4: juros simples e compostos, custo de parcelamentos e dívidas.
- Trilha 5: inflação, poder de compra, reserva, investimento, liquidez e FGC.
- Trilha 6: phishing, golpes com Pix, proteção de dados e desafio integrador.
- A missão 6.4 — Desafio integrador encerra a jornada com quatro simulações.

### 13.3 Verificações executadas

```text
docker compose exec backend alembic upgrade head
→ 0009 (head)

docker compose exec backend pytest -q
→ 101 passed

docker compose exec backend alembic check
→ No new upgrade operations detected

docker compose exec frontend npm test -- --run
→ 29 passed (11 arquivos)

docker compose exec frontend npm run build
→ tsc -b && vite build aprovados
```

Contagens confirmadas no PostgreSQL: Fases 3–5 com 3 missões, 9 competências,
13 atividades e 9 conteúdos cada; Fase 6 com 4 missões, 10 competências,
17 atividades e 9 conteúdos. Todas as 13 missões têm `lesson_flow` preenchido.

### 13.4 Pendências mantidas

- Revisão pedagógica e de produto do conteúdo das seis trilhas.
- E2E automatizado de interação no navegador para a jornada completa.
- Validação LGPD antes de piloto com usuários reais.
- Integração de IA continua bloqueada por D7.


---

## 14. Preparação dos agentes sem Orchestrate (23/10/2026)

**Status:** implementado e verificado no Compose.  
**Documento de referência:** `docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.

### 14.1 O que foi antecipado

| Frente | Implementação |
|---|---|
| Trilha personalizada | `profiles.trail` (migration `0010`), regras do Catalisador, onboarding com contexto de vida/urgência e etapa de prévia da trilha |
| Desbloqueio por trilha | `is_phase_unlocked()` lê a ordem da trilha; missões continuam sequenciais dentro da fase |
| Home e Jornada | `GET /journey/overview` entrega trilha, fases na ordem personalizada e recomendação do Catalisador |
| Perfil | card “Minha trilha” com ordem, justificativa e troca entre personalizada/padrão |
| Chat do Mentor | UI real em `/student/mentor`, histórico persistido, contexto por `?mission=ID` e modal dentro do minicurso |
| Fallback honesto | `preparing` / `unavailable` explícitos; nenhuma simulação de IA |
| Analista | `mission_insight` no resumo, `reinforcement` após erro repetido e `analyst_insight` no painel |
| Infraestrutura | `conversations/orchestrate.py`, variáveis `ORCHESTRATE_*`, timeout e fallback |
| Seam de IA | `catalyst.apply_generated_trail()` valida a trilha antes de persistir |

### 14.2 Arquivos principais

| Arquivo | Finalidade |
|---|---|
| `backend/app/modules/agents/catalyst.py` | Regras de trilha, recomendação e seam do Catalisador IA |
| `backend/app/modules/agents/analyst.py` | Recomendações determinísticas do Analista |
| `backend/app/modules/conversations/orchestrate.py` | Adaptador único do Mentor para o Orchestrate |
| `backend/app/modules/conversations/service.py` | Persistência, contexto e payload do chat |
| `backend/alembic/versions/0010_personalized_trail.py` | Campo `profiles.trail` |
| `backend/tests/test_agents_preparation.py` | Trilha, desbloqueio, chat, fallback e reforço |
| `frontend/src/areas/student/components/MentorChat.tsx` | Chat reutilizável (página e modal) |
| `frontend/src/areas/student/MentorPage.tsx` | Página dos agentes com chat real |
| `frontend/src/areas/student/OnboardingPage.tsx` | Coleta ampliada e prévia da trilha |
| `frontend/src/types/student.ts` | Contratos de trilha, recomendação, insight e chat |

### 14.3 Verificações executadas

```text
docker compose exec backend alembic upgrade head
→ 0010 (head)

docker compose exec backend pytest -q
→ 108 passed

docker compose exec frontend npm test -- --run
→ 37 passed (12 arquivos)

docker compose exec frontend npm run build
→ tsc -b && vite build aprovados

docker compose exec backend alembic check
→ No new upgrade operations detected
```

### 14.4 Correção incluída

`_check_phase_completion()` passou a mapear a conquista da Fase 2 para
`digital_consciente` (antes procurava `fase_2_concluida`, que não existia).

### 14.5 O que continua bloqueado

- Chamada real ao Mentor e ao Analista via watsonx Orchestrate (D7).
- Geração de trilha por IA — o seam existe, mas a fonte atual é `rules`.
- Calibração dos limiares pedagógicos com dados reais do piloto.
- Revisão editorial/LGPD e E2E automatizado em navegador.

### 14.6 Próxima ação

1. Executar o spike do Orchestrate (§22 da Arquitetura).
2. Ajustar somente o mapeamento de `orchestrate.py` ao contrato real.
3. Ativar `ORCHESTRATE_ENABLED=true` em ambiente controlado.
4. Comparar os insights determinísticos do Analista com a análise do agente.
5. Conectar o Catalisador IA via `apply_generated_trail()` e validar a trilha
   antes de exibi-la.

---

## 15. Reorganização e implementação das 12 trilhas (23/10/2026)

### 15.1 Objetivo

Expandir as trilhas 1–6 (antes limitadas a 2–3 missões cada) e criar as trilhas
7–12 do zero, completando o currículo de 12 trilhas × 3–4 missões conforme o
contrato curricular `docs/CONTRATO_CURRICULAR_TRILHAS.md`.

### 15.2 Mapeamento phase/trilha

| Phase | Trilha | Nome |
|---|---|---|
| 1 | Trilha 1 | Meu primeiro salário |
| 2 | Trilha 2 | Orçamento na prática |
| 3 | Trilha 3 | Pagamentos do dia a dia |
| 4 | Trilha 4 | Cartão e fatura |
| 5 | Trilha 5 | Metas e reserva |
| 6 | Trilha 6 | Guardar sem perder o controle |
| 7–12 | Trilhas 7–12 | Juros e parcelas, dívida, inflação, investimentos, golpes e desafio integrador |

As fases 1–6 já existiam na base. Não foram inseridas novas phases para elas —
os seeds usam upsert por chave natural `(phase_id, mission.number)`.

### 15.3 Seeds criados/modificados

| Arquivo | Missões novas/expandidas |
|---|---|
| `trail_1_v2.py` | Missões 1.2 e 1.3 (expansão) |
| `trail_2_v1.py` | Missões 2.1 e 2.2 (expansão) |
| `trail_3_v1.py` | Missões 3.1 e 3.3 (expansão); 3.2 renumerada (era 3 → 2) |
| `trail_4_v1.py` | Missão 4.1 (expansão) |
| `trail_5_v1.py` | Missões 5.1 e 5.3 (expansão) |
| `trail_6_v1.py` | Missão 6.1 (expansão) |
| `trail_7_v1.py` a `trail_12_v1.py` | Todas as missões (novas fases) |

### 15.4 Lesson flows

`lesson_flows_trails.py` centraliza os roteiros das missões da reestruturação.
Flows adicionados nesta sessão:

- `(2, 1)`, `(2, 2)` — Trilha 2 expansões
- `(3, 1)`, `(3, 3)` — Trilha 3 expansões; `(3, 2)` renomeado
- `(4, 1)` — Trilha 4 expansão
- `(5, 1)`, `(5, 3)` — Trilha 5 expansões
- `(6, 1)` — Trilha 6 expansão

Cada flow segue o padrão: `intro → reading/question interleaved → summary`.
Atividades do tipo `simulation` usam `{"type": "scenario"}` no flow.

### 15.5 Correção incluída

`trail_3_v1.py` tinha "Carteiras digitais" registrada como `mission.number = 3`
(conflito com a missão 3.3 do contrato). Foi corrigida para `number = 2`,
`order = 2`, e os códigos de competência atualizados de `3.3.x` para `3.2.x`.

### 15.6 Estado final dos testes

```
211 passed (PostgreSQL ativo)
```

Sem banco disponível, os 50 testes de integração são marcados como `skipped`.
Todos os testes do módulo `test_content_trails_v2.py` passam, incluindo
`test_lesson_flows_cover_all_new_missions` e
`test_lesson_flow_structure_for_new_missions`.

### 15.7 Próximas ações

1. Revisão pedagógica e editorial de todo o conteúdo das 12 trilhas.
2. Executar o spike do Orchestrate (§22 da Arquitetura).
3. Ativar `ORCHESTRATE_ENABLED=true` em ambiente controlado.
4. Conectar o Catalisador IA via `apply_generated_trail()` e validar.
