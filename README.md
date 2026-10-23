# Prisma.AI — Educação Financeira Personalizada

Aplicação web de educação financeira para jovens adultos, com landing page pública,
jornada de aprendizagem e uma visão de agentes de IA para apoiar a evolução do estudante.

**Stack:** FastAPI · PostgreSQL · React + Vite + TypeScript · Docker Compose

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose v2+
- [Git](https://git-scm.com/)

---

## Configuração inicial

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd OutOfThebox

# 2. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 3. Edite .env e substitua os valores obrigatórios:
#    - SECRET_KEY  → gere com: python -c "import secrets; print(secrets.token_hex(32))"
#    - POSTGRES_PASSWORD → escolha uma senha forte
#    - DATABASE_URL → use a MESMA senha e o MESMO usuário do PostgreSQL na URL
#      Ex.: postgresql+asyncpg://ell_user:SUA_SENHA@postgres:5432/ell_ibm
```

> A senha em `POSTGRES_PASSWORD` e a senha embutida em `DATABASE_URL` precisam ser
> idênticas. O arquivo `.env` é ignorado pelo Git e não deve ser versionado.

---

## Executar localmente

```bash
# Subir todos os serviços
docker compose up

# Subir em background
docker compose up -d

# Ver logs
docker compose logs -f

# Parar
docker compose down
```

Após subir:

| Serviço | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API (Swagger) | http://localhost:8000/docs |
| API (ReDoc) | http://localhost:8000/redoc |
| PostgreSQL | `localhost:${POSTGRES_HOST_PORT}` (padrão `5432`) |

Se a porta `5432` já estiver em uso na máquina, defina outra no `.env`, por exemplo
`POSTGRES_HOST_PORT=5433`, e execute `docker compose up -d` novamente. A porta
interna usada pelo backend continua sendo `5432`.

---

## Aplicar migrações do banco

```bash
# Dentro do container do backend
docker compose exec backend alembic upgrade head

# Ou localmente (com DATABASE_URL configurada)
cd backend
alembic upgrade head
```

---

## Executar testes

Aplique as migrações antes dos testes de integração:

```bash
docker compose exec backend alembic upgrade head

# Backend — unitários + integração real com PostgreSQL
docker compose exec backend pytest

# Com cobertura
docker compose exec backend pytest --cov=app --cov-report=term-missing

# Frontend — execução única
docker compose exec frontend npm test -- --run

# Frontend — type-check + build de produção
docker compose exec frontend npm run build
```

Os testes de integração usam o PostgreSQL do Compose e revertem cada transação ao
final. Fora do Docker, `cd backend && pytest` executa os testes unitários e marca os
testes de integração como `skipped` quando não há banco acessível.

Ao final do fluxo local, os e-mails de verificação e recuperação são registrados no log
do backend porque `MAIL_ENABLED=false`:

```bash
docker compose logs backend | grep "MOCK EMAIL"
```

---

## Estrutura do projeto

```
OutOfThebox/
├── docker-compose.yml
├── .env.example
├── docs/                    # Documentação do produto
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/             # Migrações do banco
│   └── app/
│       ├── main.py
│       ├── core/            # Config, segurança, banco de dados
│       ├── modules/
│       │   ├── auth/        # Autenticação e autorização
│       │   ├── users/       # Perfil e preferências
│       │   ├── journey/     # Fases, missões, competências
│       │   ├── progress/    # Pontos, níveis, conquistas
│       │   ├── content/     # Contrato, seeds e conteúdo das seis trilhas
│       │   └── conversations/ # Chat do Mentor e adaptador do Orchestrate
│       └── tests/           # Unitários + integração com PostgreSQL
└── frontend/
    ├── Dockerfile
    ├── package-lock.json
    └── src/
        ├── design-system/   # Tokens, componentes base
        ├── api/             # Camada de chamadas ao backend
        ├── store/           # Estado de sessão
        └── areas/
            ├── auth/        # Login, cadastro, verificação e reset
            └── student/     # Área do estudante
```

O painel administrativo ainda não possui diretório implementado; ele pertence à Etapa 4.

---

## Variáveis de ambiente obrigatórias

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta para JWT (mínimo 32 chars) |
| `POSTGRES_PASSWORD` | Senha do banco de dados |
| `POSTGRES_USER` | Usuário do banco |
| `POSTGRES_DB` | Nome do banco |
| `DATABASE_URL` | URL assíncrona do PostgreSQL, com usuário e senha iguais aos anteriores |
| `POSTGRES_HOST_PORT` | Porta opcional exposta no host (padrão `5432`) |
| `SQL_ECHO` | Log detalhado de SQL; mantenha `false` (padrão) |

Veja `.env.example` para a lista completa com descrições.

---

## Papéis de usuário

| Papel | Acesso |
|---|---|
| `student` | Jornada, missões, perfil, progresso |
| `admin` | Painel administrativo (implementado após o sistema principal) |

---

## Documentação de conteúdo e progressão

- [`docs/ESQUEMA_CONTEUDO_ATIVIDADES.md`](docs/ESQUEMA_CONTEUDO_ATIVIDADES.md) — contrato JSONB das atividades.
- [`docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`](docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md) — domínio, reforço e desbloqueio.
- [`docs/GUIA_PRODUCAO_CONTEUDO.md`](docs/GUIA_PRODUCAO_CONTEUDO.md) — como escrever e publicar missões.
- [`docs/MINICURSOS_TRILHAS_1_2.md`](docs/MINICURSOS_TRILHAS_1_2.md) — arquitetura e experiência dos minicursos das Trilhas 1 e 2.
- [`docs/MINICURSOS_TRILHAS_3_6.md`](docs/MINICURSOS_TRILHAS_3_6.md) — conteúdo e roteiros das Trilhas 3 a 6.
- [`docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`](docs/AGENTES_INTEGRACAO_ORCHESTRATE.md) — trilha personalizada, chat do Mentor, contratos e preparação para o Orchestrate.
- [`docs/fase-1-primeiro-salario.md`](docs/fase-1-primeiro-salario.md) — referência editorial da Fase 1.

As migrations `0002`–`0010` carregam as seis trilhas, os minicursos imersivos,
o desafio integrador e a trilha personalizada do perfil. Depois de
`alembic upgrade head`, o fluxo do estudante já funciona sem IA: onboarding com
trilha, missão, feedback determinístico, chat com fallback honesto, progresso e
desbloqueio pela ordem da trilha.

---

## Decisões técnicas aprovadas

Documentadas em [`docs/Arquitetura_Tecnica_ELL_IBM.md`](docs/Arquitetura_Tecnica_ELL_IBM.md).

- Monólito modular inicial (sem microserviços)
- Backend é autoridade sobre regras de negócio — IA nunca altera pontos ou desbloqueios diretamente
- Gamificação determinística: 100 pts (1ª tentativa) / 70 pts (após reforço) / 50 pts (onboarding)
- Áudio fora do escopo do MVP
- watsonx Orchestrate reservado para Etapa 2 (requer spike técnico)
