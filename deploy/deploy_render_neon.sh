#!/usr/bin/env bash
#
# Deploy do Prisma.AI no Render + Neon.
#
# Pré-requisitos:
#   - conta no Render com o repositório conectado ao GitHub
#   - conta no Neon
#   - API key do Render em deploy/.secrets/render-api-key
#   - API key do Neon em deploy/.secrets/neon-api-key
#
# Uso:
#   ./deploy/deploy_render_neon.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SECRETS_DIR="$SCRIPT_DIR/.secrets"

log() { printf '\n==> %s\n' "$*"; }
die() { printf '\nERRO: %s\n' "$*" >&2; exit 1; }

command -v curl >/dev/null 2>&1 || die "curl não encontrado."
command -v jq >/dev/null 2>&1 || die "jq não encontrado."
command -v openssl >/dev/null 2>&1 || die "openssl não encontrado."

RENDER_API_KEY="${RENDER_API_KEY:-}"
NEON_API_KEY="${NEON_API_KEY:-}"
if [[ -z "$RENDER_API_KEY" && -f "$SECRETS_DIR/render-api-key" ]]; then
  RENDER_API_KEY="$(tr -d '\r\n' < "$SECRETS_DIR/render-api-key")"
fi
if [[ -z "$NEON_API_KEY" && -f "$SECRETS_DIR/neon-api-key" ]]; then
  NEON_API_KEY="$(tr -d '\r\n' < "$SECRETS_DIR/neon-api-key")"
fi

[[ -n "$RENDER_API_KEY" ]] || die "Defina RENDER_API_KEY ou crie deploy/.secrets/render-api-key."
[[ -n "$NEON_API_KEY" ]] || die "Defina NEON_API_KEY ou crie deploy/.secrets/neon-api-key."

REPO_URL="${REPO_URL:-https://github.com/kaue-souza7/prisma-ai}"
BRANCH="${BRANCH:-main}"
RENDER_REGION="${RENDER_REGION:-virginia}"
NEON_REGION="${NEON_REGION:-aws-us-east-1}"
API_NAME="${API_NAME:-prisma-ai-api-kaue}"
WEB_NAME="${WEB_NAME:-prisma-ai-web-kaue}"
NEON_PROJECT_NAME="${NEON_PROJECT_NAME:-prisma-ai}"

RENDER_API="https://api.render.com/v1"
NEON_API="https://console.neon.tech/api/v2"

render_api() {
  local method="$1" path="$2" data="${3:-}" response code body
  if [[ -n "$data" ]]; then
    response="$(curl -sS -X "$method" "$RENDER_API$path" \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      -H "Accept: application/json" \
      -H "Content-Type: application/json" \
      -d "$data" -w $'\n%{http_code}')"
  else
    response="$(curl -sS -X "$method" "$RENDER_API$path" \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      -H "Accept: application/json" \
      -w $'\n%{http_code}')"
  fi
  code="${response##*$'\n'}"
  body="${response%$'\n'*}"
  if [[ "$code" -ge 400 ]]; then
    printf 'Render API %s %s falhou (%s):\n%s\n' "$method" "$path" "$code" "$body" >&2
    exit 1
  fi
  printf '%s' "$body"
}

neon_api() {
  local method="$1" path="$2" data="${3:-}" response code body
  if [[ -n "$data" ]]; then
    response="$(curl -sS -X "$method" "$NEON_API$path" \
      -H "Authorization: Bearer $NEON_API_KEY" \
      -H "Accept: application/json" \
      -H "Content-Type: application/json" \
      -d "$data" -w $'\n%{http_code}')"
  else
    response="$(curl -sS -X "$method" "$NEON_API$path" \
      -H "Authorization: Bearer $NEON_API_KEY" \
      -H "Accept: application/json" \
      -w $'\n%{http_code}')"
  fi
  code="${response##*$'\n'}"
  body="${response%$'\n'*}"
  if [[ "$code" -ge 400 ]]; then
    printf 'Neon API %s %s falhou (%s):\n%s\n' "$method" "$path" "$code" "$body" >&2
    exit 1
  fi
  printf '%s' "$body"
}

normalize_database_url() {
  python3 - "$1" <<'PY'
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

url = sys.argv[1]
if url.startswith("postgres://"):
    url = "postgresql+asyncpg://" + url[len("postgres://"):]
elif url.startswith("postgresql://"):
    url = "postgresql+asyncpg://" + url[len("postgresql://"):]

parts = urlsplit(url)
query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() != "channel_binding"]
if not any(k == "sslmode" for k, _ in query):
    query.append(("sslmode", "require"))

print(urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)))
PY
}

mkdir -p "$SECRETS_DIR"
chmod 700 "$SECRETS_DIR"
chmod 600 "$SECRETS_DIR"/* 2>/dev/null || true

# ── Neon ─────────────────────────────────────────────────────
log "1/5 Obtendo/criando PostgreSQL no Neon"

if [[ -n "${DATABASE_URL:-}" ]]; then
  DATABASE_URL="$(normalize_database_url "$DATABASE_URL")"
  log "Usando DATABASE_URL fornecido no ambiente"
else
  NEON_PROJECTS="$(neon_api GET "/projects")"
  NEON_PROJECT_ID="$(printf '%s' "$NEON_PROJECTS" | jq -r --arg name "$NEON_PROJECT_NAME" '
    .projects[]? | select(.name == $name) | .id
  ' | head -n 1)"

  if [[ -n "$NEON_PROJECT_ID" ]]; then
    log "Projeto Neon já existe: $NEON_PROJECT_ID"
    NEON_URI_JSON="$(neon_api GET "/projects/$NEON_PROJECT_ID/connection_uri?database_name=neondb&role_name=neondb_owner")"
    RAW_URI="$(printf '%s' "$NEON_URI_JSON" | jq -r '.uri // .connection_uri // empty')"
  else
    NEON_ORGS="$(neon_api GET "/users/me/organizations")"
    NEON_ORG_ID="$(printf '%s' "$NEON_ORGS" | jq -r '.organizations[0].id // .organizations[0].org_id // empty')"

    NEON_PAYLOAD="$(jq -n \
      --arg name "$NEON_PROJECT_NAME" \
      --arg region "$NEON_REGION" \
      --arg org "$NEON_ORG_ID" \
      '{
        project: (
          {name: $name, region_id: $region, pg_version: 17}
          + (if $org != "" then {org_id: $org} else {} end)
        )
      }')"

    log "Criando projeto Neon $NEON_PROJECT_NAME em $NEON_REGION"
    NEON_CREATED="$(neon_api POST "/projects" "$NEON_PAYLOAD")"
    NEON_PROJECT_ID="$(printf '%s' "$NEON_CREATED" | jq -r '.project.id')"
    RAW_URI="$(printf '%s' "$NEON_CREATED" | jq -r '.connection_uris[0].connection_uri // empty')"
  fi

  [[ -n "$RAW_URI" ]] || die "Não foi possível obter a connection string do Neon."
  DATABASE_URL="$(normalize_database_url "$RAW_URI")"
fi

# ── Render: owner ────────────────────────────────────────────
log "2/5 Identificando workspace do Render"

OWNERS="$(render_api GET "/owners?limit=20")"
OWNER_ID="${RENDER_OWNER_ID:-}"
if [[ -z "$OWNER_ID" ]]; then
  OWNER_ID="$(printf '%s' "$OWNERS" | jq -r '
    if type == "array" then (.[0].owner.id // .[0].id)
    else (.owners[0].id // .[0].id)
    end
  ')"
fi
[[ -n "$OWNER_ID" && "$OWNER_ID" != "null" ]] || die "Não foi possível identificar o ownerId do Render."

# ── Render: backend ──────────────────────────────────────────
log "3/5 Criando/atualizando backend no Render"

SECRET_KEY_FILE="$SECRETS_DIR/render-secret-key"
if [[ -n "${SECRET_KEY:-}" ]]; then
  JWT_SECRET="$SECRET_KEY"
elif [[ -f "$SECRET_KEY_FILE" ]]; then
  JWT_SECRET="$(cat "$SECRET_KEY_FILE")"
else
  JWT_SECRET="$(openssl rand -hex 32)"
  printf '%s' "$JWT_SECRET" > "$SECRET_KEY_FILE"
  chmod 600 "$SECRET_KEY_FILE"
fi

SERVICES="$(render_api GET "/services?limit=100")"
API_SERVICE_ID="$(printf '%s' "$SERVICES" | jq -r --arg name "$API_NAME" '
  .[]? | (.service // .) | select(.name == $name) | .id
' | head -n 1)"

DOCKER_COMMAND='sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"'

API_ENV_INITIAL="$(jq -n \
  --arg db "$DATABASE_URL" \
  --arg secret "$JWT_SECRET" \
  '[
    {key: "DATABASE_URL", value: $db},
    {key: "SECRET_KEY", value: $secret},
    {key: "ENVIRONMENT", value: "production"},
    {key: "ALLOWED_ORIGINS", value: "http://localhost:5173"},
    {key: "REQUIRE_EMAIL_VERIFICATION", value: "false"},
    {key: "MAIL_ENABLED", value: "false"},
    {key: "ORCHESTRATE_ENABLED", value: "false"},
    {key: "ORCHESTRATE_STUDIO_ENABLED", value: "false"}
  ]')"

if [[ -z "$API_SERVICE_ID" ]]; then
  API_PAYLOAD="$(jq -n \
    --arg name "$API_NAME" \
    --arg owner "$OWNER_ID" \
    --arg repo "$REPO_URL" \
    --arg branch "$BRANCH" \
    --arg region "$RENDER_REGION" \
    --arg command "$DOCKER_COMMAND" \
    --argjson env "$API_ENV_INITIAL" \
    '{
      type: "web_service",
      name: $name,
      ownerId: $owner,
      repo: $repo,
      branch: $branch,
      rootDir: "backend",
      autoDeployTrigger: "commit",
      serviceDetails: {
        runtime: "docker",
        plan: "free",
        region: $region,
        healthCheckPath: "/health",
        envSpecificDetails: {
          dockerCommand: $command,
          dockerContext: ".",
          dockerfilePath: "./Dockerfile"
        }
      },
      envVars: $env
    }')"

  log "Criando serviço $API_NAME"
  API_CREATED="$(render_api POST "/services" "$API_PAYLOAD")"
  API_SERVICE_ID="$(printf '%s' "$API_CREATED" | jq -r '.service.id')"
  API_URL="$(printf '%s' "$API_CREATED" | jq -r '.service.serviceDetails.url // empty')"
else
  log "Serviço $API_NAME já existe: $API_SERVICE_ID"
  API_DETAILS="$(render_api GET "/services/$API_SERVICE_ID")"
  API_URL="$(printf '%s' "$API_DETAILS" | jq -r '.serviceDetails.url // .service.serviceDetails.url // empty')"
fi

[[ -n "$API_URL" ]] || die "Não foi possível obter a URL do backend."
API_URL="${API_URL%/}"

# ── Render: frontend ─────────────────────────────────────────
log "4/5 Criando/atualizando frontend no Render"

WEB_ENV="$(jq -n --arg api "$API_URL" '[{key: "VITE_API_BASE_URL", value: $api}]')"

WEB_PAYLOAD="$(jq -n \
  --arg name "$WEB_NAME" \
  --arg owner "$OWNER_ID" \
  --arg repo "$REPO_URL" \
  --arg branch "$BRANCH" \
  --argjson env "$WEB_ENV" \
  '{
    type: "static_site",
    name: $name,
    ownerId: $owner,
    repo: $repo,
    branch: $branch,
    rootDir: "frontend",
    autoDeployTrigger: "commit",
    serviceDetails: {
      buildCommand: "npm ci && npm run build",
      staticPublishPath: "./dist",
      routes: [{type: "rewrite", source: "/*", destination: "/index.html"}]
    },
    envVars: $env
  }')"

WEB_SERVICE_ID="$(printf '%s' "$SERVICES" | jq -r --arg name "$WEB_NAME" '
  .[]? | (.service // .) | select(.name == $name) | .id
' | head -n 1)"

if [[ -z "$WEB_SERVICE_ID" ]]; then
  log "Criando site estático $WEB_NAME"
  WEB_CREATED="$(render_api POST "/services" "$WEB_PAYLOAD")"
  WEB_SERVICE_ID="$(printf '%s' "$WEB_CREATED" | jq -r '.service.id')"
  WEB_URL="$(printf '%s' "$WEB_CREATED" | jq -r '.service.serviceDetails.url // empty')"
else
  log "Site $WEB_NAME já existe: $WEB_SERVICE_ID"
  WEB_DETAILS="$(render_api GET "/services/$WEB_SERVICE_ID")"
  WEB_URL="$(printf '%s' "$WEB_DETAILS" | jq -r '.serviceDetails.url // .service.serviceDetails.url // empty')"
  render_api PUT "/services/$WEB_SERVICE_ID/env-vars" "$WEB_ENV" >/dev/null
  render_api POST "/services/$WEB_SERVICE_ID/deploys" '{"clearCache":"do_not_clear"}' >/dev/null || true
fi

[[ -n "$WEB_URL" ]] || die "Não foi possível obter a URL do frontend."
WEB_URL="${WEB_URL%/}"

# ── CORS definitivo ──────────────────────────────────────────
log "5/5 Ajustando CORS para $WEB_URL"

API_ENV_FINAL="$(jq -n \
  --arg db "$DATABASE_URL" \
  --arg secret "$JWT_SECRET" \
  --arg web "$WEB_URL" \
  '[
    {key: "DATABASE_URL", value: $db},
    {key: "SECRET_KEY", value: $secret},
    {key: "ENVIRONMENT", value: "production"},
    {key: "ALLOWED_ORIGINS", value: $web},
    {key: "REQUIRE_EMAIL_VERIFICATION", value: "false"},
    {key: "MAIL_ENABLED", value: "false"},
    {key: "ORCHESTRATE_ENABLED", value: "false"},
    {key: "ORCHESTRATE_STUDIO_ENABLED", value: "false"}
  ]')"

render_api PUT "/services/$API_SERVICE_ID/env-vars" "$API_ENV_FINAL" >/dev/null

# Força um novo deploy para o backend ler o CORS atualizado.
render_api POST "/services/$API_SERVICE_ID/deploys" '{"clearCache":"do_not_clear"}' >/dev/null || true

log "Aguardando a API responder em $API_URL/health"
HEALTH_OK=false
for _ in $(seq 1 90); do
  if curl -fsS "$API_URL/health" >/dev/null 2>&1; then
    HEALTH_OK=true
    break
  fi
  sleep 10
done

[[ "$HEALTH_OK" == "true" ]] || die "A API não respondeu. Veja os logs no dashboard do Render."

log "Aguardando o frontend responder em $WEB_URL"
WEB_OK=false
for _ in $(seq 1 60); do
  if curl -fsS "$WEB_URL" >/dev/null 2>&1; then
    WEB_OK=true
    break
  fi
  sleep 10
done
[[ "$WEB_OK" == "true" ]] || printf '\nAviso: o frontend ainda não respondeu; o build pode estar em andamento no Render.\n'

printf '\n============================================================\n'
printf ' Deploy concluído\n'
printf '============================================================\n'
printf ' Frontend: %s\n' "$WEB_URL"
printf ' API:      %s\n' "$API_URL"
printf ' Health:   %s/health\n' "$API_URL"
printf ' Neon:     %s\n' "$NEON_PROJECT_ID"
printf '============================================================\n'
printf '\nO backend free do Render hiberna após 15 min sem tráfego.\n'
printf 'A primeira requisição depois disso pode demorar ~50s.\n'
