# Deploy no IBM Cloud — Code Engine

Este diretório contém o caminho de deploy do Prisma.AI para o IBM Cloud usando:

- **Code Engine** para o backend FastAPI e o frontend (nginx);
- **Container Registry (ICR)** para as imagens;
- **Databases for PostgreSQL** para o banco;
- **Secrets do Code Engine** para credenciais;
- **Code Engine Job** para rodar `alembic upgrade head`.

A região padrão é **São Paulo (`br-sao`)**.

## 1. Pré-requisitos

- Conta IBM Cloud com permissão para criar Code Engine, ICR e Databases.
- Docker em execução.
- `jq` e `python3`.
- IBM Cloud CLI com os plugins `code-engine`, `container-registry` e `cloud-databases`.

Se a CLI ainda não estiver instalada:

```bash
./deploy/install-ibmcloud-cli.sh
export PATH="$HOME/.local/bin:$PATH"
```

## 2. Autenticação

Recomendado: API key com permissões na conta.

```bash
export IBMCLOUD_API_KEY="sua-api-key"
```

Ou faça login interativo:

```bash
ibmcloud login --sso
ibmcloud target -r br-sao -g Default
```

> A API key também é usada para criar o segredo de pull do Container Registry. Se você autenticar apenas por SSO, crie o segredo `prisma-ai-icr` no projeto Code Engine manualmente ou defina `IBMCLOUD_API_KEY` só para o deploy.

## 3. Configuração

```bash
cp deploy/.env.deploy.example deploy/.env.deploy
```

Edite `deploy/.env.deploy` e ajuste pelo menos:

- `ICR_NAMESPACE`: namespace único do Container Registry;
- `IBMCLOUD_RESOURCE_GROUP`: normalmente `Default`;
- `DB_INSTANCE_NAME`, se quiser outro nome;
- `ORCHESTRATE_*`, se for ligar os agentes de IA;
- `MAIL_*`, se for habilitar e-mail real.

O arquivo `deploy/.env.deploy` contém segredos e está no `.gitignore`.

## 4. Executar

```bash
./deploy/deploy.sh
```

O script:

1. autentica e seleciona a região/grupo;
2. cria/seleciona o projeto Code Engine;
3. cria o namespace e o segredo do ICR;
4. cria o Databases for PostgreSQL e espera ficar ativo;
5. cria um service key e monta a `DATABASE_URL` com TLS;
6. cria os segredos da aplicação e o certificado CA do banco;
7. constrói e envia a imagem do backend;
8. roda `alembic upgrade head` como job;
9. cria/atualiza o app do backend e descobre a URL da API;
10. constrói o frontend com `VITE_API_BASE_URL` apontando para a API;
11. cria/atualiza o app do frontend e ajusta o CORS do backend.

No final ele imprime as URLs de frontend e API.

## 5. O que é criado

| Recurso | Nome padrão |
|---|---|
| Projeto Code Engine | `prisma-ai` |
| App da API | `prisma-ai-api` |
| App do frontend | `prisma-ai-web` |
| Job de migração | `prisma-ai-migrate` |
| Banco PostgreSQL | `prisma-ai-postgres` |
| Service key do banco | `prisma-ai-postgres-key` |
| Segredo da aplicação | `prisma-ai-app` |
| Segredo do certificado CA | `prisma-ai-db-ca` |
| Segredo de pull do ICR | `prisma-ai-icr` |

Os arquivos sensíveis gerados localmente ficam em `deploy/.secrets/`:

- `app.env`: variáveis da aplicação enviadas ao Code Engine;
- `postgres-ca.crt`: certificado do banco;
- `secret_key`: chave JWT gerada na primeira execução.

## 6. Atualizações

Depois de alterar o código:

```bash
./deploy/deploy.sh
```

O script reconstrói as imagens, roda as migrações e atualiza os dois apps. A tag padrão é o hash curto do Git; você pode fixar outra com `IMAGE_TAG=v1.2.3`.

## 7. Logs e diagnóstico

```bash
ibmcloud ce project select -n prisma-ai
ibmcloud ce app logs -n prisma-ai-api
ibmcloud ce app logs -n prisma-ai-web
ibmcloud ce jobrun list
ibmcloud ce jobrun logs -n <nome-do-jobrun>
```

Verificação rápida:

```bash
curl https://<url-da-api>/health
```

## 8. Domínio próprio

Por padrão, o Code Engine entrega URLs `*.codeengine.appdomain.cloud` com TLS.

Para usar domínio próprio:

1. crie o domínio em **IBM Cloud Internet Services (CIS)** ou no seu provedor de DNS;
2. crie um CNAME para o hostname do app no Code Engine;
3. configure o domínio no Code Engine (`Domain mappings`) com o segredo TLS;
4. preencha `API_PUBLIC_URL` e `WEB_PUBLIC_URL` no `deploy/.env.deploy`;
5. rode o deploy novamente.

## 9. Custo

- O Code Engine tem uma camada gratuita mensal; os apps podem escalar até zero.
- O Databases for PostgreSQL é o principal custo fixo. O menor plano Shared Compute fica em torno de **US$ 11,70/mês** (confira o valor atual no catálogo).
- O Container Registry tem limite gratuito de armazenamento; imagens antigas podem ser removidas.

## 10. Remoção

> Atenção: os comandos abaixo apagam recursos, inclusive o banco e os dados.

```bash
ibmcloud ce project select -n prisma-ai
ibmcloud ce app delete -n prisma-ai-api -f
ibmcloud ce app delete -n prisma-ai-web -f
ibmcloud ce job delete -n prisma-ai-migrate -f
ibmcloud ce project delete -n prisma-ai -f
ibmcloud resource service-instance-delete prisma-ai-postgres -g Default -f
```

Remova também as imagens do namespace `ICR_NAMESPACE` e o service key do banco, se não forem mais usados.

## 11. Orchestrate e e-mail

- **Orchestrate:** o deploy funciona com `ORCHESTRATE_ENABLED=false` e os fallbacks determinísticos. Para ligar os agentes, preencha `ORCHESTRATE_URL`, `ORCHESTRATE_API_KEY` e os IDs dos agentes.
- **E-mail:** o padrão é `MAIL_ENABLED=false` e `REQUIRE_EMAIL_VERIFICATION=false`. Para verificação real, configure um SMTP externo e mude as duas flags.
