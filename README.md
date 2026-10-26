<p align="center">
  <img src="docs/assets/banner.svg" alt="Prisma.AI — aprender finanças é praticar o próximo passo" width="100%" />
</p>

<h1 align="center">Prisma.AI</h1>

<p align="center">
  <strong>Sua jornada. Suas escolhas. Seu futuro.</strong><br />
  Educação financeira para jovens adultos que aprendem praticando — com seis fases,
  missões reais e uma camada de agentes preparada para IA.
</p>

<p align="center">
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" />
  <img alt="PostgreSQL 16" src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" />
  <img alt="React 18" src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=0B0B0F" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white" />
  <img alt="Vite" src="https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white" />
  <img alt="Docker Compose" src="https://img.shields.io/badge/Docker_Compose-2-2496ED?logo=docker&logoColor=white" />
</p>

<p align="center">
  <a href="#o-problema-que-nos-move">Problema</a> ·
  <a href="#diferenciais">Diferenciais</a> ·
  <a href="#funcionalidades">Funcionalidades</a> ·
  <a href="#experiência-do-produto">Experiência</a> ·
  <a href="#como-funciona-por-dentro">Arquitetura</a> ·
  <a href="#inteligência-artificial-e-agentes">IA e agentes</a> ·
  <a href="#qualidade-técnica">Qualidade</a> ·
  <a href="#como-executar">Executar</a>
</p>

> **Status:** MVP local funcional. Autenticação, onboarding, jornada, avaliação,
> gamificação, chat do Mentor e a experiência do Estúdio de Prismas já têm
> implementação no repositório. A geração real de conteúdo pelo Estúdio e as
> respostas do Mentor dependem do IBM watsonx Orchestrate, cuja integração está
> preparada, mas **desativada por padrão** (`ORCHESTRATE_ENABLED=false`).

> **Em 30 segundos:** o Prisma.AI transforma educação financeira em uma jornada
> de seis fases com missões práticas, feedback contextual e progressão por
> evidências. O backend é a autoridade sobre pontos e desbloqueios; os agentes
> orientam o estudante, mas nunca decidem sozinhos.

> O projeto também aparece na documentação de descoberta como **ELL IBM**, o
> codinome usado antes da definição da marca Prisma.AI.

---

## O problema que nos move

Aprender finanças não deveria começar com uma planilha ou uma lista de termos
técnicos. O primeiro salário, o primeiro cartão, um Pix urgente, uma parcela
que parecia pequena, uma mensagem suspeita: decisões financeiras chegam cedo —
e costumam vir acompanhadas de pouca prática.

O Prisma.AI parte de uma proposta simples: **aproximar o aprendizado da decisão
real**. Em vez de só apresentar conteúdo, o estudante enfrenta situações,
escolhe um caminho, recebe feedback e constrói evidências de que compreendeu o
conceito.

**Público principal:** jovens adultos de 18 a 24 anos, em diferentes níveis de
conhecimento financeiro e de familiaridade digital. A experiência é mobile-first
e não exige conhecimento prévio de finanças.

**O que o produto não é:** o Prisma.AI não é banco, não conecta contas, não
executa transações e não recomenda investimentos personalizados. O foco é
educacional e seguro.

### A jornada em seis fases

| Fase | Tema | O que o estudante desenvolve |
|---|---|---|
| 01 | Primeiro salário | Renda, descontos, prioridades e organização do dinheiro |
| 02 | Seu dinheiro no digital | Meios de pagamento, cartão, crédito e cuidados nas transações |
| 03 | Por que poupar | Objetivos, planejamento, reserva e imprevistos |
| 04 | Juros: a favor e contra você | Tempo, crédito, parcelamento e custo total |
| 05 | Onde o dinheiro rende | Inflação, poder de compra, risco, prazo e liquidez |
| 06 | Proteção digital | Golpes, Pix, dados pessoais e decisões seguras |

São **19 missões** e **81 atividades** carregadas por migrações versionadas,
incluindo o desafio integrador da Fase 6.

---

## Diferenciais

### Aprender fazendo, não assistindo

Cada módulo combina introdução, leitura, questões, cenário e resumo. O estudante
avança por etapas e responde atividades que geram evidências de aprendizagem.
O objetivo não é completar telas, mas tomar decisões e explicar o raciocínio.

### Personalização com regras explícitas

O onboarding coleta objetivo, nível de conhecimento, contexto de vida e urgência.
O Catalisador, uma camada determinística do backend, monta uma ordem de fases
adequada a esse contexto e a persiste em `profiles.trail`. O estudante pode
aceitar a trilha personalizada ou voltar à ordem padrão.

Não há caixa-preta: as regras estão no código, a ordem é validada contra as fases
existentes e nenhuma trilha altera pontos ou desbloqueios por conta própria.

### Avaliação por evidências, não por clique

A avaliação é por módulo: o estudante responde uma vez por questão dentro da
tentativa, recebe o gabarito apenas depois de enviar e vê o percentual ao final.
**70%** aprova; **90%** indica excelência. Abaixo de 70%, é necessário refazer o
módulo para avançar. Refazer preserva o histórico das tentativas anteriores.

### IA com limites claros

O backend é a autoridade sobre o estado do estudante. Nenhum agente concede
pontos, cria conquistas ou desbloqueia fases diretamente. O Catalisador e o
Analista já operam com regras determinísticas; o Mentor tem interface,
persistência e contrato prontos para o Orchestrate, com fallback explícito
enquanto a integração não está ativa.

### Duas moedas, dois propósitos

**XP** mede progressão: níveis, conquistas e desbloqueios. **Prismas (◆)** são
uma moeda separada, acumulada por acertos e conclusões, usada para gerar revisões
no Estúdio. Não há compra de Prismas, ranking público ou vantagem paga.

### Conteúdo e ambiente reproduzíveis

As seis fases, missões, atividades e conquistas são carregadas por migrations
Alembic e seeds versionados. O ambiente sobe com Docker Compose, e a suíte de
testes usa PostgreSQL real com transações revertidas ao final.

---

## Funcionalidades

**Legenda:** **Implementado** funciona no código atual · **Em preparação** tem
base pronta, mas depende de uma integração externa · **Planejado** está
documentado e ainda não foi construído.

| Funcionalidade | O que o estudante consegue fazer | Status |
|---|---|---|
| **Onboarding e trilha** | Informar objetivo, nível, contexto e urgência; receber uma ordem de fases personalizada; voltar à ordem padrão. | **Implementado** (regras determinísticas) |
| **Jornada de aprendizagem** | Navegar por seis fases, missões e desbloqueios sequenciais; retomar de onde parou. | **Implementado** |
| **Aulas imersivas** | Percorrer introdução, leitura, questões, cenário e resumo com progresso por etapa. | **Implementado** |
| **Avaliação por módulo** | Responder uma vez por questão, ver o gabarito após o envio, obter percentual e refazer o módulo quando necessário. | **Implementado** |
| **Gamificação** | Acumular XP, subir de nível e conquistar marcos por desempenho. | **Implementado** (5 níveis) |
| **Prismas** | Ganhar a moeda ao acertar atividades e concluir módulos, fases e onboarding. | **Implementado** |
| **Estúdio de Prismas** | Escolher fase, módulo e formato (revisão, flashcards ou exercícios), consultar a biblioteca e responder exercícios extras. | **Em preparação** (a geração real depende do Orchestrate) |
| **Mentor** | Conversar sobre conceitos, receber sugestões e manter histórico por missão. | **Interface implementada; IA em preparação** |
| **Analista de Progresso** | Receber insights de reforço após dificuldades recorrentes e no painel de progresso. | **Implementado** (determinístico) |
| **Catalisador** | Ver a trilha e a recomendação de próximo passo na Home, na Jornada e no Perfil. | **Implementado** (determinístico) |
| **Perfil e progresso** | Consultar competências demonstradas, conquistas, XP, Prismas e preferências. | **Implementado** |
| **Autenticação** | Cadastrar, verificar e-mail, entrar e redefinir senha. | **Implementado** (e-mail mock em desenvolvimento) |
| **Painel administrativo** | Criar e publicar conteúdo com autorização de administrador. | **Planejado** (há endpoints-base, sem UI) |
| **Áudio** | — | **Fora do MVP** |

### Uma trilha que começa pelo seu contexto

No onboarding, o estudante informa o que quer alcançar, quanto já sabe e qual é
o seu momento de vida. O backend combina essas informações com regras explícitas
para sugerir uma sequência — por exemplo, começar por juros quando a prioridade é
sair das dívidas, ou por reserva quando o objetivo é criar segurança.

A trilha fica salva no perfil, é exibida na Home, na Jornada e no Perfil, e pode
ser trocada por uma ordem padrão. O backend valida a ordem antes de persistir e
continua sendo responsável por desbloqueios e pontuação.

**Onde está:** `backend/app/modules/agents/catalyst.py`, `backend/app/modules/users/` e
`backend/alembic/versions/0010_personalized_trail.py`.

### Aprender fazendo, com consequência

O player de aula organiza o conteúdo em etapas. Em questões objetivas, o
estudante confirma a resposta e não pode trocá-la na mesma tentativa. Se errar,
vê a alternativa correta e uma explicação; ao final, o backend calcula o
percentual da tentativa.

O resultado não é só uma nota: ele atualiza competências, XP, Prismas e
conquistas. Se o desempenho ficar abaixo de 70%, o próximo módulo permanece
bloqueado até uma nova tentativa. Se ficar entre 70% e 89%, o estudante passa e
pode refazer por vontade própria; a partir de 90%, recebe o bônus de excelência.

**Onde está:** `backend/app/modules/journey/service.py`,
`backend/app/modules/progress/service.py`,
`backend/alembic/versions/0011_evaluation_model.py` e
`frontend/src/areas/student/LessonPlayerPage.tsx`.

### Duas moedas, dois propósitos

O XP responde à pergunta “quanto eu já avancei?”. As Prismas respondem a outra:
“o que eu quero revisar agora?”. Elas são acumuladas por acertos e conclusões,
não podem ser compradas e são gastas no Estúdio.

| Evento | XP | Prismas |
|---|---|---:|
| Onboarding concluído | +50 | +20 |
| Resposta correta em atividade objetiva | conforme a missão | +2 (primeira vez) |
| Módulo aprovado (70–89%) | +70 | +15 |
| Módulo com excelência (≥ 90%) | +100 na 1ª tentativa | +25 |
| Fase concluída | — | +50 |

O Estúdio oferece revisão narrativa (30), flashcards (20) e exercícios extras
(25). Com o Orchestrate desativado, a geração retorna uma mensagem honesta e
**não cobra Prismas**; a biblioteca e a economia já estão implementadas.

**Onde está:** `backend/app/modules/progress/service.py`,
`backend/app/modules/studio/service.py`,
`backend/app/modules/agents/studio_mentor.py` e
`backend/alembic/versions/0013_prism_economy.py`.

### Agentes que orientam, mas não decidem

O Catalisador sugere próximo passo com base em regras. O Analista transforma
evidências de competências em uma recomendação curta de reforço ou avanço. O
Mentor tem contexto da missão, sugestões e histórico persistido; quando o
Orchestrate não está ativo, responde com um fallback explícito em vez de simular
uma IA.

Nenhum desses papéis altera pontos, conquistas ou desbloqueios. O backend monta
o contexto, valida a resposta e persiste o estado. Essa separação é o que permite
trocar a camada de IA sem reescrever a jornada.

---

## Experiência do produto

As imagens abaixo foram capturadas da aplicação em execução local, com uma conta
de demonstração e dados de exemplo. Não são mockups.

![Landing pública do Prisma.AI — proposta de valor e prévia do produto](docs/assets/screenshots/landing.webp)

**Landing pública.** A proposta de valor, a identidade visual e uma prévia da
experiência do estudante antes do cadastro.

![Início do estudante — próximo passo, trilha, XP, nível e Prismas](docs/assets/screenshots/student-home.webp)

**Início.** O estudante vê o próximo passo, a fase atual, a trilha personalizada,
o nível, o XP e o saldo de Prismas.

![Minha jornada — seis fases, missões e desbloqueios](docs/assets/screenshots/student-journey.webp)

**Minha jornada.** As seis fases aparecem na ordem da trilha, com progresso,
missões concluídas, disponíveis e bloqueadas.

![Player de aula — leitura com destaque de conceitos e progresso por etapa](docs/assets/screenshots/student-lesson.webp)

**Aula imersiva.** Conteúdo em etapas, progresso visível e acesso ao Mentor
durante a missão.

![Estúdio de Prismas — formatos de revisão, custos e biblioteca](docs/assets/screenshots/student-studio.webp)

**Estúdio de Prismas.** Formatos de revisão, custos em Prismas e biblioteca
pessoal. O estado exibido é real: a geração de IA só é liberada quando o
Orchestrate estiver ativo.

---

## Como funciona por dentro

O Prisma.AI é um **monólito modular**: um backend FastAPI concentra autenticação,
regras de negócio, persistência e integração com IA; o frontend React consome uma
API REST versionada em `/api/v1`. PostgreSQL guarda usuários, conteúdo, respostas,
progresso, competências, conversas e conteúdo gerado.

```mermaid
flowchart TB
    subgraph FE["Frontend"]
        UI["React + Vite + TypeScript<br/>landing, autenticação e área do estudante"]
    end

    subgraph BE["Backend FastAPI — monólito modular"]
        AUTH["auth · usuários"]
        JOURNEY["journey · aulas · avaliação"]
        PROGRESS["progress · XP · conquistas"]
        CONTENT["content · seeds versionados"]
        STUDIO["studio · Prismas"]
        CHAT["conversations · Mentor"]
        AGENTS["agents · Catalisador e Analista"]
    end

    DB[("PostgreSQL 16<br/>JSONB · migrações Alembic")]
    ORCH["IBM watsonx Orchestrate<br/>integração preparada"]

    UI --> AUTH
    UI --> JOURNEY
    UI --> STUDIO
    UI --> CHAT
    AUTH --> DB
    JOURNEY --> DB
    JOURNEY --> PROGRESS
    JOURNEY --> AGENTS
    CONTENT --> DB
    PROGRESS --> DB
    STUDIO --> DB
    CHAT --> DB
    STUDIO -.->|quando ativo| ORCH
    CHAT -.->|quando ativo| ORCH
    AGENTS --> DB
```

### O fluxo de uma resposta

```mermaid
sequenceDiagram
    autonumber
    actor E as Estudante
    participant F as Frontend
    participant B as FastAPI
    participant DB as PostgreSQL
    E->>F: responde uma atividade
    F->>B: POST /api/v1/journey/missions/{id}/submit
    B->>DB: valida a tentativa e persiste a resposta
    B->>B: avalia com regra determinística
    B->>DB: atualiza competência, XP, Prismas e conquistas
    B-->>F: feedback, percentual e próximo passo
    F-->>E: resultado e desbloqueio
```

### Decisões que sustentam o produto

- **Backend como autoridade:** pontos, níveis, conquistas e desbloqueios são
  calculados por regras explícitas. A IA nunca escreve estado persistente.
- **Contratos tipados:** Pydantic valida entradas e saídas; o frontend consome
  tipos TypeScript e não replica regras críticas.
- **Conteúdo versionado:** as fases são carregadas por migrations idempotentes,
  preservando IDs de atividades já respondidas.
- **Gabarito protegido:** chaves como `correct_answer` e critérios de avaliação
  são removidos das respostas antes do envio da resposta.
- **Sessão segura:** JWT de acesso curto, refresh token, hash bcrypt e proteção
  de rotas por papel no backend.
- **Persistência relacional:** PostgreSQL com JSONB para conteúdo flexível,
  trilha e mensagens, mantendo integridade e relacionamentos no banco.
- **Ambiente reproduzível:** Docker Compose, `.env.example`, Alembic e testes
  contra PostgreSQL real.

---

## Inteligência artificial e agentes

> **Importante:** neste estágio, o Prisma.AI **não opera agentes autônomos com
> LLM em produção**. O que existe é uma arquitetura de agentes com papéis,
> contratos e pontos de extensão definidos. Catalisador e Analista são camadas
> determinísticas; o Mentor tem adapter para o IBM watsonx Orchestrate, mas
> responde com fallback enquanto a integração não está habilitada.

### Papéis e estado atual

| Papel | Responsabilidade | Hoje no código | Ponto de extensão |
|---|---|---|---|
| **Catalisador** | Personalizar a ordem das fases e sugerir o próximo passo | Regras determinísticas implementadas e visíveis na Home, Jornada e Perfil | `backend/app/modules/agents/catalyst.py` |
| **Mentor** | Explicar conceitos, acompanhar o raciocínio e responder dúvidas | Chat, histórico, contexto de missão e fallback implementados | `backend/app/modules/conversations/orchestrate.py` |
| **Analista de Progresso** | Identificar dificuldades recorrentes e recomendar reforço ou avanço | Insights determinísticos no feedback, resumo e painel | `backend/app/modules/agents/analyst.py` |
| **Mentor do Estúdio** | Montar o contexto e validar conteúdo gerado para o Estúdio | Contrato, payload, validação e falha com reembolso implementados | `backend/app/modules/agents/studio_mentor.py` |

```mermaid
flowchart LR
    B["Backend valida contexto e permissões"] --> C["Catalisador<br/>trilha e próximo passo"]
    B --> A["Analista<br/>evidências e reforço"]
    B --> M["Adapter do Mentor"]
    C --> R["Resposta validada e persistida"]
    A --> R
    M -.->|quando ativo| O["IBM watsonx Orchestrate"]
    O -.-> R
```

### O que está ativo hoje

- **Catalisador:** trilha por objetivo e contexto, recomendação de próximo passo
  e leitura da ordem persistida.
- **Analista:** recomendações curtas a partir de competências, erros recorrentes
  e evidências já calculadas pelo backend.
- **Mentor:** interface de chat, sugestões, contexto da missão, histórico e
  mensagens persistidas. Sem Orchestrate, a resposta é um fallback explícito.
- **Estúdio:** economia de Prismas, biblioteca, formatos e submissão de exercícios
  extras. A geração retorna `503` e não cobra quando o Orchestrate está inativo.

### O que muda quando o Orchestrate for ativado

1. O adapter do Mentor passa a chamar o endpoint configurado, com timeout e
   fallback em caso de erro.
2. O Analista pode rodar em background e substituir os insights determinísticos
   mantendo o mesmo contrato.
3. O Catalisador pode receber uma trilha sugerida por IA, validada pelo backend
   antes de ser persistida.
4. O Estúdio pode gerar revisões, flashcards e exercícios, sempre passando por
   validação estrutural antes de consumir Prismas.

A configuração fica em `.env` (`ORCHESTRATE_ENABLED`, `ORCHESTRATE_URL`,
`ORCHESTRATE_API_KEY`, `ORCHESTRATE_AGENT_ID` e `ORCHESTRATE_TIMEOUT_SECONDS`).
Nenhuma credencial real está versionada.

### Por que essa separação importa

Ela permite evoluir a inteligência sem entregar ao modelo decisões que precisam
ser auditáveis. O estudante pode receber uma resposta melhor do Mentor sem que
isso mude seus pontos, desbloqueie uma fase indevidamente ou altere o histórico
de aprendizagem.

---

## Tecnologias

| Camada | Tecnologias | Papel no projeto |
|---|---|---|
| **Frontend** | React 18, TypeScript 5, Vite 6, React Router 6 | Landing, autenticação, área do estudante e rotas protegidas |
| **Estado e HTTP** | Zustand 5, Axios, Framer Motion | Sessão persistida, chamadas à API e movimento da interface |
| **UI** | CSS Modules, design system próprio, Vitest + Testing Library | Componentes, tokens de marca e testes de interface |
| **Backend** | Python 3.12, FastAPI 0.115, Pydantic 2 | API REST, validação, regras de negócio e OpenAPI |
| **Dados** | SQLAlchemy 2 async, asyncpg, PostgreSQL 16, Alembic | Persistência, JSONB, migrações e seeds |
| **Segurança** | JWT com python-jose, passlib + bcrypt | Autenticação, refresh e hash de senhas |
| **IA e integração** | IBM watsonx Orchestrate (adapter preparado), httpx | Ponto de extensão do Mentor, Analista e Estúdio |
| **Infraestrutura** | Docker Compose, Uvicorn | Ambiente local reproduzível e servidor ASGI |
| **Qualidade** | pytest, pytest-asyncio, pytest-cov, Vitest, Testing Library, jsdom | Testes unitários, integração e componentes |

> O Orchestrate não é uma dependência ativa para executar o projeto. Ele só é
> necessário para habilitar respostas reais de IA e geração no Estúdio.

---

## Qualidade técnica

O projeto foi construído para ser compreensível, testável e extensível, não apenas
para demonstrar uma tela.

### Evidências verificáveis

- **14 migrações Alembic** (`0001` a `0014`) cobrem schema, conteúdo, aulas,
  avaliação, trilha, Prismas e Estúdio.
- **6 fases, 19 missões e 81 atividades** carregadas por seeds versionados.
- **127 testes de backend** passando, incluindo integração com PostgreSQL real.
- **42 testes de frontend** passando em 13 arquivos.
- **Build de produção do frontend** aprovado com `tsc -b && vite build`.
- **`docker compose config`** validado com o `.env.example`.

### Organização e segurança

- **Monólito modular:** `auth`, `users`, `journey`, `progress`, `content`,
  `conversations`, `studio` e `agents` têm responsabilidades separadas.
- **Contratos e erros consistentes:** schemas Pydantic, respostas tipadas,
  envelope de erro e tratamento centralizado de validação e HTTP.
- **Autorização no backend:** rotas protegidas com JWT e verificação de papel;
  testes de isolamento impedem que um estudante acesse dados de outro.
- **Gabarito não vaza:** o conteúdo enviado ao cliente remove respostas corretas,
  critérios e feedbacks antes da submissão.
- **Transações:** a dependência de banco faz commit ou rollback por requisição; os
  testes revertem a transação ao final.
- **Conteúdo idempotente:** seeds usam chaves naturais para preservar IDs de
  atividades já respondidas.
- **Frontend protegido:** rotas por papel, gate de onboarding, sessão persistida,
  estados de carregamento/erro e componentes reutilizáveis.
- **Acessibilidade de base:** foco visível, skip links, rótulos ARIA e respeito a
  `prefers-reduced-motion` nas animações principais.

### Limites atuais

- A integração real de IA depende do acesso ao IBM watsonx Orchestrate e de um
  spike técnico; até lá, o Mentor usa fallback e o Estúdio não gera conteúdo.
- O envio de e-mail é mock em desenvolvimento (`MAIL_ENABLED=false`); não há
  provedor SMTP configurado.
- O painel administrativo ainda não tem interface; existem endpoints de criação
  e publicação de conteúdo no backend.
- Não há deploy de produção, observabilidade externa ou política de backup
  documentada neste repositório.
- A validação jurídica de LGPD e a revisão editorial/pedagógica do conteúdo
  continuam como pendências de produto.
- Não há suíte E2E dedicada em navegador; a cobertura atual é de API,
  componentes e fluxos de interface, complementada por validação manual/headless.

---

## Um projeto com espaço para crescer

A arquitetura foi organizada para que a próxima evolução não exija reescrever a
jornada. Abaixo, uma separação honesta entre próximos passos, expansões e
possibilidades de longo prazo.

### Próximos passos

- **Ativar o Orchestrate** no Mentor, no Analista, no Catalisador e no Estúdio,
  com o spike de contrato, timeout, fallback e validação já previstos.
- **Integrar e-mail real** para verificação e recuperação de senha, mantendo o
  mock local como opção de desenvolvimento.
- **Construir o painel administrativo** sobre os endpoints de conteúdo já
  existentes: rascunho, revisão, publicação e gestão de usuários.
- **Definir operação de produção:** deploy, observabilidade, backups, rate
  limiting e política de retenção de dados.
- **Revisar LGPD, acessibilidade e conteúdo** com as áreas responsáveis antes de
  um piloto real.

### Expansões naturais

- Novos módulos e trilhas usando o contrato JSONB de atividades e o pipeline de
  seeds/migrações já existente.
- Geração de revisões, flashcards e exercícios no Estúdio, com biblioteca pessoal
  e devolutiva do Analista.
- Exportação ou compartilhamento de revisões e conquistas.
- PWA/mobile instalável, mantendo a experiência mobile-first.
- Novos formatos de feedback do Mentor e do Analista, sempre mediados pelo
  backend.

### Longo prazo

- Aprendizagem adaptativa com mais evidências ao longo das seis fases.
- Novos agentes especializados, com contratos e limites definidos.
- Painéis para instituições de ensino e organizações parceiras.
- Expansão de idioma e de repertório cultural, preservando a curadoria
  pedagógica.

Integrações bancárias, execução de transações e recomendação personalizada de
investimentos permanecem **fora do escopo** atual. A base modular, os contratos
tipados, as migrações e o adapter de IA reduzem o custo de evolução, mas não
garantem escalabilidade ou sucesso de produto por si só.

---

## Como executar

### Pré-requisitos

- Docker e Docker Compose v2+
- Git
- Portas livres: `5173` (frontend), `8000` (API) e `5432` (PostgreSQL; ou outra
  porta definida em `POSTGRES_HOST_PORT`)

### 1. Configurar o ambiente

```bash
git clone <url-do-repositorio>
cd prisma-ai
cp .env.example .env
```

Edite `.env` e ajuste, no mínimo:

| Variável | O que fazer |
|---|---|
| `POSTGRES_USER` | Definir o usuário do banco |
| `POSTGRES_PASSWORD` | Definir uma senha forte |
| `POSTGRES_DB` | Definir o nome do banco |
| `DATABASE_URL` | Usar o mesmo usuário, senha e banco; dentro do Compose, o host é `postgres` |
| `SECRET_KEY` | Gerar uma chave aleatória com 32+ caracteres |
| `POSTGRES_HOST_PORT` | Usar `5433` se `5432` já estiver ocupada no host |
| `ALLOWED_ORIGINS` | Manter `http://localhost:5173` no ambiente local |
| `ORCHESTRATE_ENABLED` | Manter `false` para o fluxo sem IA |

Gere a chave secreta com:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> A senha em `POSTGRES_PASSWORD` e a senha dentro de `DATABASE_URL` precisam ser
> idênticas. Se a senha tiver caracteres especiais, codifique-os na URL. O `.env`
> é ignorado pelo Git.

### 2. Subir os serviços

```bash
docker compose up -d --build
docker compose ps
```

Aguarde o PostgreSQL ficar saudável e o backend responder em
`http://localhost:8000/health`.

### 3. Aplicar as migrações e carregar o conteúdo

```bash
docker compose exec backend alembic upgrade head
```

As migrations `0002`–`0009` carregam as seis fases, os módulos e as atividades.
Não há comando separado de seed para o currículo inicial.

### 4. Acessar

| Serviço | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API — Swagger | http://localhost:8000/docs |
| API — ReDoc | http://localhost:8000/redoc |
| Health check | http://localhost:8000/health |
| PostgreSQL | `localhost:${POSTGRES_HOST_PORT}` (padrão `5432`) |

### 5. Primeiro acesso

1. Abra `http://localhost:5173/register` e crie uma conta.
2. Com `MAIL_ENABLED=false`, o token de verificação é impresso no log:

   ```bash
   docker compose logs backend | grep "MOCK EMAIL"
   ```

3. Abra `http://localhost:5173/verify-email?token=TOKEN` substituindo `TOKEN`
   pelo valor exibido no log.
4. Entre, conclua o onboarding e comece a jornada.

O fluxo de recuperação de senha segue a mesma lógica: o token é registrado no log
e pode ser usado em `http://localhost:5173/reset-password?token=TOKEN`.

### 6. Executar os testes

Com o ambiente no ar e as migrações aplicadas:

```bash
# Backend — unitários + integração com PostgreSQL
docker compose exec backend pytest -q

# Frontend — execução única
docker compose exec frontend npm test -- --run

# Frontend — type-check + build de produção
docker compose exec frontend npm run build
```

Na validação deste README: **127 testes de backend** e **42 testes de frontend**
passaram, e o build do frontend foi concluído com sucesso.

### 7. Rodar sem Docker (opcional)

O caminho recomendado é o Compose. Para desenvolvimento local, você precisa de um
PostgreSQL acessível e das variáveis de ambiente configuradas.

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+asyncpg://usuario:senha@localhost:5432/ell_ibm"
export SECRET_KEY="uma-chave-com-32-caracteres-ou-mais"
alembic upgrade head
uvicorn app.main:app --reload

# Frontend, em outro terminal
cd frontend
npm ci
npm run dev
```

Fora do Docker, os testes de integração são marcados como `skipped` se o
PostgreSQL não estiver acessível; os testes unitários continuam executando.

### 8. Parar o ambiente

```bash
docker compose down
```

Para apagar também os dados locais do PostgreSQL, use `docker compose down -v`
com consciência de que o volume será removido.

### Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `env file .env not found` | `.env` não foi criado | `cp .env.example .env` e preencher |
| Backend não conecta ao banco | Senha/usuário divergentes entre `POSTGRES_*` e `DATABASE_URL` | Igualar os valores e recriar os containers |
| Porta `5432` ocupada | PostgreSQL local já em execução | Definir `POSTGRES_HOST_PORT=5433` e subir novamente |
| Frontend recebe `401` | Sessão expirada ou conta não verificada | Fazer login novamente e conferir a verificação do e-mail |
| Nenhum e-mail chega | `MAIL_ENABLED=false` | Ler o token no log do backend |
| Estúdio retorna `503` | Orchestrate desativado | Comportamento esperado; nenhuma Prisma é cobrada |
| Migrações ausentes | `alembic upgrade head` não foi executado | Rodar o comando dentro do backend |

---

## Estrutura do repositório

```text
prisma-ai/
├── backend/
│   ├── app/
│   │   ├── core/                 # Config, banco, segurança, logs e erros
│   │   ├── modules/
│   │   │   ├── auth/             # Cadastro, verificação, login e reset
│   │   │   ├── users/            # Perfil, onboarding e trilha
│   │   │   ├── journey/          # Fases, missões, aulas e avaliação
│   │   │   ├── progress/         # XP, níveis, conquistas e Prismas
│   │   │   ├── content/          # Contrato, seeds e conteúdo das fases
│   │   │   ├── conversations/    # Chat do Mentor e adapter Orchestrate
│   │   │   ├── studio/           # Estúdio de Prismas e biblioteca
│   │   │   └── agents/           # Catalisador, Analista e Mentor do Estúdio
│   │   └── shared/models.py      # Modelos SQLAlchemy compartilhados
│   ├── alembic/versions/         # Schema, conteúdo e evolução do banco
│   └── tests/                    # Unitários + integração PostgreSQL
├── frontend/
│   └── src/
│       ├── areas/                # landing, auth e student
│       ├── api/                  # Cliente HTTP e contratos de API
│       ├── design-system/        # Tokens, marca e componentes base
│       ├── shared/               # Guards, hooks e rich text
│       ├── store/                # Sessão persistida com Zustand
│       └── types/                # Tipos TypeScript do domínio
├── docs/
│   ├── assets/                   # Banner e capturas de tela
│   └── fases/                    # Referências editoriais das seis fases
├── docker-compose.yml
├── .env.example
└── README.md
```

> O painel administrativo ainda não tem pasta de frontend; ele está planejado
> sobre os endpoints de conteúdo existentes no backend.

---

## Documentação

A documentação de descoberta, produto e implementação está em `docs/`:

- [PRD — requisitos do produto](docs/PRD_ELL_IBM.md) — visão, público, jornada,
  requisitos e limites de escopo.
- [Arquitetura técnica](docs/Arquitetura_Tecnica_ELL_IBM.md) — decisões,
  monólito modular, dados, agentes e integração.
- [Conteúdo e jornada de aprendizagem](docs/Conteudo_e_Jornada_de_Aprendizagem.md) —
  princípios pedagógicos, fases, missões e avaliação.
- [Especificação dos agentes de IA](docs/Especificacao_Agentes_IA_ELL_IBM.md) —
  papéis, entradas, saídas e limites dos agentes.
- [Design system e UX/UI](docs/Design_System_UX_UI_ELL_IBM.md) — identidade,
  princípios visuais e experiência.
- [Integração com o Orchestrate](docs/AGENTES_INTEGRACAO_ORCHESTRATE.md) —
  contratos, fallback, trilha, chat e preparação para a IA real.
- [Modelo de avaliação](docs/plano-modelo-avaliacao.md) — aprovação, excelência,
  tentativas e histórico.
- [Estúdio de Prismas](docs/plano-estudio-prismas.md) — economia, formatos,
  biblioteca e integração futura.
- [Esquema de conteúdo das atividades](docs/ESQUEMA_CONTEUDO_ATIVIDADES.md) —
  contrato JSONB usado pelas atividades.
- [Guia de produção de conteúdo](docs/GUIA_PRODUCAO_CONTEUDO.md) — como escrever,
  revisar e publicar missões.
- [Critérios de domínio e progressão](docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md) —
  regras de reforço, desbloqueio e conclusão.
- [Referência editorial da Fase 1](docs/fases/fase-1-primeiro-salario.md) —
  exemplo de conteúdo completo.
- [Continuidade da Etapa 1](docs/CONTINUIDADE_ETAPA_1.md) — histórico técnico,
  decisões e pendências do protótipo.

---

## Encerramento

O Prisma.AI já tem o essencial de um produto educacional funcionando ponta a
ponta: o estudante entra, conta o que quer aprender, recebe uma trilha, percorre
missões, responde atividades, vê seu progresso e acumula Prismas para revisar.
A camada de IA está desenhada para entrar sem substituir a autoridade do backend.

O que torna o projeto interessante não é apenas a interface — é a combinação de
**aprendizagem prática, avaliação por evidências, gamificação determinística e
uma arquitetura de agentes com limites claros**. O que falta está explícito:
ativar a IA real, concluir o painel administrativo, integrar e-mail e preparar
operação de produção.

**Explore o código:** [funcionalidades](#funcionalidades) ·
[arquitetura](#como-funciona-por-dentro) ·
[agentes](#inteligência-artificial-e-agentes) ·
[execução](#como-executar) ·
[documentação](#documentação).

> Sua jornada. Suas escolhas. Seu futuro.
