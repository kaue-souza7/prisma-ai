# Permissões necessárias no IBM Cloud

Conta: `<conta-IBM-Cloud>`
Usuário: `<seu-email-IBM-Cloud>`
Grupo de acesso: `watsonx-Hackathon-Access`
Região desejada: `br-sao` (São Paulo)

## Situação atual

O grupo `watsonx-Hackathon-Access` tem:

- **Code Engine:** funções de serviço *Viewer* e *Manager* (não tem função de plataforma *Editor*);
- **Container Registry:** *Viewer* e *Manager*;
- **Object Storage:** *Administrator* e *Manager*;
- **watsonx Orchestrate:** *Editor*;
- **Cloudant:** *Administrator* e *Manager*;
- **grupo de recursos Default:** *Viewer*.

Com isso, o login e o Container Registry funcionam, mas:

- criar projeto no Code Engine retorna **“Esta ação é proibida”**;
- criar Databases for PostgreSQL retorna **erro de catálogo global** (`RC-GlobalCatalogErrorResponse`).

## O que precisa ser liberado

### 1. Code Engine

Conceder ao usuário/grupo a função de plataforma **Editor** (ou **Administrator**) para o serviço **Code Engine**.

> A função *Manager* atual é de serviço; para criar projetos é necessário *Editor* ou *Administrator* de plataforma.

### 2. Databases for PostgreSQL

Conceder ao usuário/grupo:

- função de plataforma **Editor** (ou **Administrator**) para **Databases for PostgreSQL**;
- função de serviço **Manager** (ou **Writer**) para o banco.

Alternativa: o administrador pode criar o banco e entregar as credenciais:

- serviço: `databases-for-postgresql`
- plano: `standard`
- região: `br-sao`
- hosting model: Shared Compute (`members_host_flavor = multitenant`)
- endpoints: `public`
- nome sugerido: `prisma-ai-postgres`
- service key sugerida: `prisma-ai-postgres-key` com função `Administrator`

### 3. Grupo de recursos

Para criar os recursos, o usuário/grupo precisa de **Editor** no grupo de recursos `Default` (ou em um grupo dedicado ao projeto), além das funções de serviço acima.

## Recursos que serão criados

| Recurso | Nome |
|---|---|
| Projeto Code Engine | `prisma-ai` |
| App da API | `prisma-ai-api` |
| App do frontend | `prisma-ai-web` |
| Job de migração | `prisma-ai-migrate` |
| Banco PostgreSQL | `prisma-ai-postgres` |
| Namespace ICR | `prisma-ai-kaues` (já criado) |

## Observações

- O namespace `prisma-ai-kaues` já foi criado no Container Registry com sucesso.
- O watsonx Orchestrate já está disponível na conta; os agentes podem ser ligados depois, sem bloquear o deploy.
- Nenhum recurso cobrável foi criado até agora (o projeto Code Engine e o banco não chegaram a ser provisionados).
