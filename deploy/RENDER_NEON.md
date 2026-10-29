# Deploy no Render + Neon

Arquitetura recomendada para o Prisma.AI fora da IBM Cloud:

- **Render**: backend FastAPI (Docker) + frontend React/Vite (site estático)
- **Neon**: PostgreSQL gerenciado no plano gratuito
- **Custo**: US$ 0 para demonstração
- **Limitações**: o backend free do Render hiberna após 15 minutos sem tráfego (cold start); o Neon free tem 0,5 GB e acorda na primeira conexão.

## 1. Criar o PostgreSQL no Neon

1. Acesse <https://neon.com> e crie um projeto.
2. Escolha a região **AWS us-east-1** (Virginia) para ficar próxima do Render.
3. Copie a connection string do banco.
4. Converta o início da URL para o driver async do projeto:

```text
postgresql+asyncpg://USUARIO:SENHA@HOST/BANCO?sslmode=require
```

> O backend usa SQLAlchemy com `asyncpg`. Se a URL vier como `postgresql://`, troque para `postgresql+asyncpg://`.

Guarde essa URL; ela será o secret `DATABASE_URL` no Render.

## 2. Conectar o repositório no Render

1. Crie uma conta em <https://render.com>.
2. Conecte sua conta do GitHub.
3. Selecione o repositório `kaue-souza7/prisma-ai`.
4. O Render deve detectar o `render.yaml` na raiz e propor o Blueprint com os dois serviços:
   - `prisma-ai-api-kaue` (backend Docker)
   - `prisma-ai-web-kaue` (frontend estático)
5. Aplique o Blueprint.

Se os nomes `prisma-ai-api-kaue` e `prisma-ai-web-kaue` já estiverem em uso, o Render pode gerar URLs com sufixo. Nesse caso, ajuste depois:

- `ALLOWED_ORIGINS` no backend para a URL real do frontend;
- `VITE_API_BASE_URL` no frontend para a URL real da API.

## 3. Configurar o banco

No serviço `prisma-ai-api-kaue` → **Environment**:

1. Adicione `DATABASE_URL` com a URL do Neon.
2. Confirme que `SECRET_KEY` foi gerada pelo Render (`generateValue`).
3. Salve e faça o deploy.

O comando de start do backend executa `alembic upgrade head` antes de subir o Uvicorn. As seeds de conteúdo estão dentro das migrations, então o banco novo já sobe com o currículo.

## 4. Validar

Backend:

```bash
curl https://prisma-ai-api-kaue.onrender.com/health
# {"status":"ok","version":"0.1.0"}
```

Frontend:

```text
https://prisma-ai-web-kaue.onrender.com
```

Se o backend estiver hibernando, a primeira requisição pode demorar ~50 segundos.

## 5. Atualizações

O Blueprint usa `autoDeployTrigger: commit`. Basta fazer push na branch configurada:

```bash
git push origin main
```

O Render reconstrói backend e frontend. O backend roda as migrations no start.

## 6. Se quiser usar o PostgreSQL do próprio Render

Para simplificar e ter tudo em um provedor:

1. No Render, crie um **Postgres** no plano free.
2. Use a connection string interna no `DATABASE_URL` do backend.
3. Ajuste o esquema para `postgresql+asyncpg://`.

Atenção: o PostgreSQL free do Render expira **30 dias após a criação**. Para uma demo curta serve; para manter o projeto, use Neon ou um plano pago.

## 7. Custos e limites

| Recurso | Free | Limite |
|---|---|---|
| Render Web Service | US$ 0 | 512 MB RAM, 0,1 CPU, hiberna após 15 min |
| Render Static Site | US$ 0 | 100 GB de banda/mês |
| Neon Postgres | US$ 0 | 0,5 GB de storage, 100 CU-hours/mês |

Para uma demo de hackathon, o conjunto atende. Para uso contínuo sem cold start, o próximo passo natural é o Render Starter (US$ 7/mês por web service) ou Railway (~US$ 5/mês).

## 8. Variáveis opcionais

Para ligar os agentes de IA, adicione no backend:

```text
ORCHESTRATE_ENABLED=true
ORCHESTRATE_URL=...
ORCHESTRATE_API_KEY=...
ORCHESTRATE_AGENT_MENTOR_ID=...
ORCHESTRATE_CATALYST_AGENT_ID=...
ORCHESTRATE_ANALYST_AGENT_ID=...
ORCHESTRATE_STUDIO_AGENT_ID=...
```

Para e-mail real, configure `MAIL_ENABLED=true` e as variáveis `MAIL_*` com um SMTP externo (SendGrid, Mailgun etc.).
