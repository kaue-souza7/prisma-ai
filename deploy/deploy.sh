#!/usr/bin/env bash
#
# Deploy do Prisma.AI no IBM Cloud Code Engine.
#
# Uso:
#   cp deploy/.env.deploy.example deploy/.env.deploy
#   # edite deploy/.env.deploy
#   ./deploy/deploy.sh
#
# Pré-requisitos:
#   - ibmcloud CLI com os plugins code-engine, container-registry e cloud-databases
#   - docker com BuildKit
#   - jq e python3
#   - conta IBM Cloud com permissão para criar Code Engine, ICR e Databases
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="${DEPLOY_ENV_FILE:-$SCRIPT_DIR/.env.deploy}"
SECRETS_DIR="$SCRIPT_DIR/.secrets"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

export PATH="$HOME/.local/bin:$PATH"

log() { printf '\n==> %s\n' "$*"; }
die() { printf '\nERRO: %s\n' "$*" >&2; exit 1; }
get_app_url() {
  ibmcloud ce app get -n "$1" -o url 2>/dev/null | tr -d '\r' | tail -n 1 | xargs
}

if [[ -z "${IBMCLOUD_API_KEY:-}" && -n "${IBMCLOUD_API_KEY_FILE:-}" ]]; then
  if [[ "$IBMCLOUD_API_KEY_FILE" != /* ]]; then
    IBMCLOUD_API_KEY_FILE="$ROOT_DIR/$IBMCLOUD_API_KEY_FILE"
  fi
  [[ -f "$IBMCLOUD_API_KEY_FILE" ]] || die "IBMCLOUD_API_KEY_FILE não encontrado: $IBMCLOUD_API_KEY_FILE"
  IBMCLOUD_API_KEY="$(tr -d '\r\n' < "$IBMCLOUD_API_KEY_FILE")"
fi

command -v ibmcloud >/dev/null 2>&1 || die "ibmcloud CLI não encontrada. Rode: ./deploy/install-ibmcloud-cli.sh"
command -v docker >/dev/null 2>&1 || die "docker não encontrado."
command -v jq >/dev/null 2>&1 || die "jq não encontrado."
command -v python3 >/dev/null 2>&1 || die "python3 não encontrado."

# ── Configuração ─────────────────────────────────────────────
IBMCLOUD_REGION="${IBMCLOUD_REGION:-br-sao}"
IBMCLOUD_RESOURCE_GROUP="${IBMCLOUD_RESOURCE_GROUP:-Default}"

ICR_NAMESPACE="${ICR_NAMESPACE:-}"
CE_PROJECT="${CE_PROJECT:-prisma-ai}"
API_APP_NAME="${API_APP_NAME:-prisma-ai-api}"
WEB_APP_NAME="${WEB_APP_NAME:-prisma-ai-web}"
MIGRATION_JOB_NAME="${MIGRATION_JOB_NAME:-prisma-ai-migrate}"

DB_INSTANCE_NAME="${DB_INSTANCE_NAME:-prisma-ai-postgres}"
DB_SERVICE="${DB_SERVICE:-databases-for-postgresql}"
DB_PLAN="${DB_PLAN:-standard}"
DB_HOST_FLAVOR="${DB_HOST_FLAVOR:-multitenant}"
DB_SERVICE_ENDPOINTS="${DB_SERVICE_ENDPOINTS:-public}"
DB_KEY_NAME="${DB_KEY_NAME:-prisma-ai-postgres-key}"

REGISTRY_HOST="${REGISTRY_HOST:-icr.io}"
API_IMAGE_REPO="${API_IMAGE_REPO:-prisma-ai-api}"
WEB_IMAGE_REPO="${WEB_IMAGE_REPO:-prisma-ai-web}"
REGISTRY_SECRET_NAME="${REGISTRY_SECRET_NAME:-prisma-ai-icr}"

APP_SECRET_NAME="${APP_SECRET_NAME:-prisma-ai-app}"
DB_CA_SECRET_NAME="${DB_CA_SECRET_NAME:-prisma-ai-db-ca}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"

API_CPU="${API_CPU:-1}"
API_MEMORY="${API_MEMORY:-2G}"
API_MIN_SCALE="${API_MIN_SCALE:-0}"
API_MAX_SCALE="${API_MAX_SCALE:-3}"

WEB_CPU="${WEB_CPU:-0.25}"
WEB_MEMORY="${WEB_MEMORY:-0.5G}"
WEB_MIN_SCALE="${WEB_MIN_SCALE:-0}"
WEB_MAX_SCALE="${WEB_MAX_SCALE:-2}"

ENVIRONMENT="${ENVIRONMENT:-production}"
REQUIRE_EMAIL_VERIFICATION="${REQUIRE_EMAIL_VERIFICATION:-false}"
MAIL_ENABLED="${MAIL_ENABLED:-false}"

[[ -n "$ICR_NAMESPACE" ]] || die "Defina ICR_NAMESPACE em $ENV_FILE (o namespace do Container Registry é único na conta/região)."
[[ "$ICR_NAMESPACE" != *SEUNOME* ]] || die "Troque ICR_NAMESPACE no $ENV_FILE por um nome único."

if [[ -z "${IMAGE_TAG:-}" ]]; then
  if git -C "$ROOT_DIR" rev-parse --short HEAD >/dev/null 2>&1; then
    IMAGE_TAG="$(git -C "$ROOT_DIR" rev-parse --short HEAD)"
  else
    IMAGE_TAG="$(date +%Y%m%d%H%M%S)"
  fi
fi

mkdir -p "$SECRETS_DIR"
chmod 700 "$SECRETS_DIR"

APP_ENV_FILE="$SECRETS_DIR/app.env"
DB_CA_FILE="$SECRETS_DIR/postgres-ca.crt"
SECRET_KEY_FILE="$SECRETS_DIR/secret_key"

# ── 1. Autenticação e target ─────────────────────────────────
log "1/10 Autenticando e selecionando região/grupo"

if [[ -n "${IBMCLOUD_API_KEY:-}" ]]; then
  ibmcloud login --apikey "$IBMCLOUD_API_KEY" \
    -r "$IBMCLOUD_REGION" \
    -g "$IBMCLOUD_RESOURCE_GROUP" \
    -q
else
  ibmcloud account show >/dev/null 2>&1 || die "Você não está autenticado. Rode 'ibmcloud login --sso' ou defina IBMCLOUD_API_KEY."
  ibmcloud target -r "$IBMCLOUD_REGION" -g "$IBMCLOUD_RESOURCE_GROUP" -q
fi

# ── 2. Code Engine project ───────────────────────────────────
log "2/10 Garantindo projeto do Code Engine: $CE_PROJECT"

if ibmcloud ce project get -n "$CE_PROJECT" >/dev/null 2>&1; then
  ibmcloud ce project select -n "$CE_PROJECT" -q
else
  ibmcloud ce project create -n "$CE_PROJECT" -q
  ibmcloud ce project select -n "$CE_PROJECT" -q
fi

# ── 3. Container Registry ────────────────────────────────────
log "3/10 Garantindo namespace e credencial do Container Registry"

if ! ibmcloud cr namespace-list 2>/dev/null | grep -qw "$ICR_NAMESPACE"; then
  ibmcloud cr namespace-add "$ICR_NAMESPACE"
fi

ibmcloud cr login

if ! ibmcloud ce registry get -n "$REGISTRY_SECRET_NAME" >/dev/null 2>&1; then
  [[ -n "${IBMCLOUD_API_KEY:-}" ]] || die "Para criar o segredo do registry, defina IBMCLOUD_API_KEY (uma API key da conta) ou crie o segredo '$REGISTRY_SECRET_NAME' manualmente."
  ibmcloud ce registry create \
    -n "$REGISTRY_SECRET_NAME" \
    --server "$REGISTRY_HOST" \
    --username iamapikey \
    --password "$IBMCLOUD_API_KEY"
fi

# ── 4. Banco de dados ────────────────────────────────────────
log "4/10 Garantindo Databases for PostgreSQL: $DB_INSTANCE_NAME"

if ibmcloud resource service-instance "$DB_INSTANCE_NAME" -g "$IBMCLOUD_RESOURCE_GROUP" >/dev/null 2>&1; then
  log "Banco já existe; aguardando estado ativo"
else
  log "Criando banco (pode levar alguns minutos)"
  ibmcloud resource service-instance-create \
    "$DB_INSTANCE_NAME" \
    "$DB_SERVICE" \
    "$DB_PLAN" \
    "$IBMCLOUD_REGION" \
    -g "$IBMCLOUD_RESOURCE_GROUP" \
    -p "{\"members_host_flavor\":\"$DB_HOST_FLAVOR\"}" \
    --service-endpoints "$DB_SERVICE_ENDPOINTS"
fi

DB_STATE=""
for _ in $(seq 1 120); do
  DB_STATE="$(
    ibmcloud resource service-instance "$DB_INSTANCE_NAME" \
      -g "$IBMCLOUD_RESOURCE_GROUP" \
      --output json 2>/dev/null \
      | jq -r 'if type == "array" then .[0].state else .state end' 2>/dev/null \
      || true
  )"
  [[ "$DB_STATE" == "active" ]] && break
  sleep 10
done
[[ "$DB_STATE" == "active" ]] || die "O banco não ficou ativo (estado atual: ${DB_STATE:-desconhecido})."

log "Obtendo credenciais do banco"

if ibmcloud resource service-key "$DB_KEY_NAME" -g "$IBMCLOUD_RESOURCE_GROUP" >/dev/null 2>&1; then
  DB_KEY_JSON="$(ibmcloud resource service-key "$DB_KEY_NAME" -g "$IBMCLOUD_RESOURCE_GROUP" --output json)"
else
  DB_KEY_JSON="$(
    ibmcloud resource service-key-create \
      "$DB_KEY_NAME" \
      Administrator \
      --instance-name "$DB_INSTANCE_NAME" \
      -g "$IBMCLOUD_RESOURCE_GROUP" \
      --output json
  )"
fi

PG_JSON="$(
  printf '%s' "$DB_KEY_JSON" \
    | jq -c 'if type == "array" then .[0] else . end
             | .credentials.connection.postgres
               // .credentials.connection.postgresql
               // empty'
)"

[[ -n "$PG_JSON" ]] || die "Não encontrei a conexão PostgreSQL no service key. Verifique o painel do banco."

DB_HOST="$(printf '%s' "$PG_JSON" | jq -r 'if (.hosts | type) == "array" then .hosts[0].hostname else .hosts.hostname end')"
DB_PORT="$(printf '%s' "$PG_JSON" | jq -r 'if (.hosts | type) == "array" then .hosts[0].port else .hosts.port end')"
DB_USER="$(printf '%s' "$PG_JSON" | jq -r '.authentication.username // .username // empty')"
DB_PASS="$(printf '%s' "$PG_JSON" | jq -r '.authentication.password // .password // empty')"
DB_NAME="$(printf '%s' "$PG_JSON" | jq -r '.database // .path // "ibmclouddb"' | sed 's#^/##')"
DB_CERT_B64="$(printf '%s' "$PG_JSON" | jq -r '.certificate.certificate_base64 // .certificate.base64 // empty')"

[[ -n "$DB_HOST" && -n "$DB_PORT" && -n "$DB_USER" && -n "$DB_PASS" && -n "$DB_NAME" ]] \
  || die "Credenciais do banco incompletas."

DB_USER_ENC="$(jq -nr --arg v "$DB_USER" '$v | @uri')"
DB_PASS_ENC="$(jq -nr --arg v "$DB_PASS" '$v | @uri')"
DB_NAME_ENC="$(jq -nr --arg v "$DB_NAME" '$v | @uri')"

if [[ -n "$DB_CERT_B64" ]]; then
  python3 -c 'import base64, sys; sys.stdout.buffer.write(base64.b64decode(sys.argv[1]))' \
    "$DB_CERT_B64" > "$DB_CA_FILE"
  chmod 600 "$DB_CA_FILE"
  DB_SSL_QUERY="sslmode=verify-full&sslrootcert=/certs/postgres.crt"
else
  DB_SSL_QUERY="sslmode=require"
fi

DATABASE_URL="postgresql+asyncpg://${DB_USER_ENC}:${DB_PASS_ENC}@${DB_HOST}:${DB_PORT}/${DB_NAME_ENC}?${DB_SSL_QUERY}"

# ── 5. Segredos da aplicação ─────────────────────────────────
log "5/10 Criando/atualizando segredos da aplicação"

if [[ -n "${SECRET_KEY:-}" ]]; then
  JWT_SECRET="$SECRET_KEY"
elif [[ -f "$SECRET_KEY_FILE" ]]; then
  JWT_SECRET="$(cat "$SECRET_KEY_FILE")"
else
  JWT_SECRET="$(openssl rand -hex 32)"
  printf '%s' "$JWT_SECRET" > "$SECRET_KEY_FILE"
  chmod 600 "$SECRET_KEY_FILE"
fi

write_app_env() {
  local allowed_origins="$1"
  : > "$APP_ENV_FILE"
  chmod 600 "$APP_ENV_FILE"

  {
    printf 'DATABASE_URL=%s\n' "$DATABASE_URL"
    printf 'SECRET_KEY=%s\n' "$JWT_SECRET"
    printf 'ENVIRONMENT=%s\n' "$ENVIRONMENT"
    printf 'ALLOWED_ORIGINS=%s\n' "$allowed_origins"
    printf 'REQUIRE_EMAIL_VERIFICATION=%s\n' "$REQUIRE_EMAIL_VERIFICATION"
    printf 'MAIL_ENABLED=%s\n' "$MAIL_ENABLED"
    printf 'MAIL_TLS=%s\n' "${MAIL_TLS:-true}"
    printf 'ORCHESTRATE_ENABLED=%s\n' "${ORCHESTRATE_ENABLED:-false}"
    printf 'ORCHESTRATE_STUDIO_ENABLED=%s\n' "${ORCHESTRATE_STUDIO_ENABLED:-false}"
    printf 'ORCHESTRATE_TIMEOUT_SECONDS=%s\n' "${ORCHESTRATE_TIMEOUT_SECONDS:-15}"

    [[ -n "${MAIL_FROM:-}" ]] && printf 'MAIL_FROM=%s\n' "$MAIL_FROM" || true
    [[ -n "${MAIL_SERVER:-}" ]] && printf 'MAIL_SERVER=%s\n' "$MAIL_SERVER" || true
    [[ -n "${MAIL_PORT:-}" ]] && printf 'MAIL_PORT=%s\n' "$MAIL_PORT" || true
    [[ -n "${MAIL_USERNAME:-}" ]] && printf 'MAIL_USERNAME=%s\n' "$MAIL_USERNAME" || true
    [[ -n "${MAIL_PASSWORD:-}" ]] && printf 'MAIL_PASSWORD=%s\n' "$MAIL_PASSWORD" || true

    [[ -n "${ORCHESTRATE_URL:-}" ]] && printf 'ORCHESTRATE_URL=%s\n' "$ORCHESTRATE_URL" || true
    [[ -n "${ORCHESTRATE_API_KEY:-}" ]] && printf 'ORCHESTRATE_API_KEY=%s\n' "$ORCHESTRATE_API_KEY" || true
    [[ -n "${ORCHESTRATE_AGENT_MENTOR_ID:-}" ]] && printf 'ORCHESTRATE_AGENT_MENTOR_ID=%s\n' "$ORCHESTRATE_AGENT_MENTOR_ID" || true
    [[ -n "${ORCHESTRATE_CATALYST_AGENT_ID:-}" ]] && printf 'ORCHESTRATE_CATALYST_AGENT_ID=%s\n' "$ORCHESTRATE_CATALYST_AGENT_ID" || true
    [[ -n "${ORCHESTRATE_ANALYST_AGENT_ID:-}" ]] && printf 'ORCHESTRATE_ANALYST_AGENT_ID=%s\n' "$ORCHESTRATE_ANALYST_AGENT_ID" || true
    [[ -n "${ORCHESTRATE_STUDIO_AGENT_ID:-}" ]] && printf 'ORCHESTRATE_STUDIO_AGENT_ID=%s\n' "$ORCHESTRATE_STUDIO_AGENT_ID" || true
    [[ -n "${ORCHESTRATE_MENTOR_ENABLED:-}" ]] && printf 'ORCHESTRATE_MENTOR_ENABLED=%s\n' "$ORCHESTRATE_MENTOR_ENABLED" || true
    [[ -n "${ORCHESTRATE_CATALYST_ENABLED:-}" ]] && printf 'ORCHESTRATE_CATALYST_ENABLED=%s\n' "$ORCHESTRATE_CATALYST_ENABLED" || true
    [[ -n "${ORCHESTRATE_ANALYST_ENABLED:-}" ]] && printf 'ORCHESTRATE_ANALYST_ENABLED=%s\n' "$ORCHESTRATE_ANALYST_ENABLED" || true
  } >> "$APP_ENV_FILE"
}

# CORS inicial: será ajustado depois que a URL do frontend existir.
INITIAL_ORIGINS="http://localhost:5173"
[[ -n "${ALLOWED_ORIGINS_EXTRA:-}" ]] && INITIAL_ORIGINS="$INITIAL_ORIGINS,$ALLOWED_ORIGINS_EXTRA"
write_app_env "$INITIAL_ORIGINS"

if ibmcloud ce secret get -n "$APP_SECRET_NAME" >/dev/null 2>&1; then
  ibmcloud ce secret update -n "$APP_SECRET_NAME" --from-env-file "$APP_ENV_FILE" -q
else
  ibmcloud ce secret create -n "$APP_SECRET_NAME" --from-env-file "$APP_ENV_FILE" -q
fi

if [[ -f "$DB_CA_FILE" ]]; then
  if ibmcloud ce secret get -n "$DB_CA_SECRET_NAME" >/dev/null 2>&1; then
    ibmcloud ce secret update -n "$DB_CA_SECRET_NAME" --from-file "postgres.crt=$DB_CA_FILE" -q
  else
    ibmcloud ce secret create -n "$DB_CA_SECRET_NAME" --from-file "postgres.crt=$DB_CA_FILE" -q
  fi
fi

# ── 6. Imagem do backend ─────────────────────────────────────
log "6/10 Construindo e enviando imagem do backend"

API_IMAGE="$REGISTRY_HOST/$ICR_NAMESPACE/$API_IMAGE_REPO:$IMAGE_TAG"
docker build \
  --platform "$DOCKER_PLATFORM" \
  -f "$ROOT_DIR/backend/Dockerfile" \
  -t "$API_IMAGE" \
  "$ROOT_DIR/backend"
docker push "$API_IMAGE"

# ── 7. Migração ──────────────────────────────────────────────
log "7/10 Executando migrações (alembic upgrade head)"

JOB_ARGS=(
  --name "$MIGRATION_JOB_NAME"
  --image "$API_IMAGE"
  --command alembic
  --argument upgrade
  --argument head
  --env-from-secret "$APP_SECRET_NAME"
  --cpu 1
  --memory 2G
)
[[ -f "$DB_CA_FILE" ]] && JOB_ARGS+=(--mount-secret "/certs=$DB_CA_SECRET_NAME")

if ibmcloud ce job get -n "$MIGRATION_JOB_NAME" >/dev/null 2>&1; then
  ibmcloud ce job update "${JOB_ARGS[@]}" -q
else
  ibmcloud ce job create "${JOB_ARGS[@]}" -q
fi

JOBRUN_NAME="${MIGRATION_JOB_NAME}-$(date +%Y%m%d%H%M%S)"
ibmcloud ce jobrun submit \
  --job "$MIGRATION_JOB_NAME" \
  --name "$JOBRUN_NAME" \
  --wait \
  --wait-timeout 900

# ── 8. App do backend ────────────────────────────────────────
log "8/10 Criando/atualizando aplicação do backend"

API_APP_ARGS=(
  --name "$API_APP_NAME"
  --image "$API_IMAGE"
  --port 8000
  --registry-secret "$REGISTRY_SECRET_NAME"
  --env-from-secret "$APP_SECRET_NAME"
  --env "APP_REVISION=$IMAGE_TAG"
  --cpu "$API_CPU"
  --memory "$API_MEMORY"
  --min-scale "$API_MIN_SCALE"
  --max-scale "$API_MAX_SCALE"
  --wait-timeout 600
)
[[ -f "$DB_CA_FILE" ]] && API_APP_ARGS+=(--mount-secret "/certs=$DB_CA_SECRET_NAME")

if ibmcloud ce app get -n "$API_APP_NAME" >/dev/null 2>&1; then
  ibmcloud ce app update "${API_APP_ARGS[@]}" -q
else
  ibmcloud ce app create "${API_APP_ARGS[@]}" -q
fi

if [[ -n "${API_PUBLIC_URL:-}" ]]; then
  API_URL="$API_PUBLIC_URL"
else
  API_URL="$(get_app_url "$API_APP_NAME")"
fi

# ── 9. Frontend ──────────────────────────────────────────────
log "9/10 Construindo e publicando o frontend para $API_URL"

WEB_IMAGE="$REGISTRY_HOST/$ICR_NAMESPACE/$WEB_IMAGE_REPO:$IMAGE_TAG"
docker build \
  --platform "$DOCKER_PLATFORM" \
  -f "$ROOT_DIR/frontend/Dockerfile.prod" \
  --build-arg "VITE_API_BASE_URL=$API_URL" \
  -t "$WEB_IMAGE" \
  "$ROOT_DIR/frontend"
docker push "$WEB_IMAGE"

WEB_APP_ARGS=(
  --name "$WEB_APP_NAME"
  --image "$WEB_IMAGE"
  --port 8080
  --registry-secret "$REGISTRY_SECRET_NAME"
  --env "APP_REVISION=$IMAGE_TAG"
  --cpu "$WEB_CPU"
  --memory "$WEB_MEMORY"
  --min-scale "$WEB_MIN_SCALE"
  --max-scale "$WEB_MAX_SCALE"
  --wait-timeout 600
)

if ibmcloud ce app get -n "$WEB_APP_NAME" >/dev/null 2>&1; then
  ibmcloud ce app update "${WEB_APP_ARGS[@]}" -q
else
  ibmcloud ce app create "${WEB_APP_ARGS[@]}" -q
fi

if [[ -n "${WEB_PUBLIC_URL:-}" ]]; then
  WEB_URL="$WEB_PUBLIC_URL"
else
  WEB_URL="$(get_app_url "$WEB_APP_NAME")"
fi

# ── 10. CORS definitivo ──────────────────────────────────────
log "10/10 Ajustando CORS do backend para $WEB_URL"

ALLOWED_ORIGINS="$WEB_URL"
[[ -n "${ALLOWED_ORIGINS_EXTRA:-}" ]] && ALLOWED_ORIGINS="$ALLOWED_ORIGINS,$ALLOWED_ORIGINS_EXTRA"
write_app_env "$ALLOWED_ORIGINS"

ibmcloud ce secret update -n "$APP_SECRET_NAME" --from-env-file "$APP_ENV_FILE" -q
ibmcloud ce app update -n "$API_APP_NAME" --env "APP_REVISION=${IMAGE_TAG}-cors" -q

# ── Verificação ──────────────────────────────────────────────
log "Verificando saúde da API"

HEALTH_OK=false
for _ in $(seq 1 30); do
  if curl -fsS "$API_URL/health" >/dev/null 2>&1; then
    HEALTH_OK=true
    break
  fi
  sleep 5
done

[[ "$HEALTH_OK" == "true" ]] || die "A API não respondeu em $API_URL/health. Veja os logs: ibmcloud ce app logs -n $API_APP_NAME"

printf '\n============================================================\n'
printf ' Deploy concluído\n'
printf '============================================================\n'
printf ' Frontend: %s\n' "$WEB_URL"
printf ' API:      %s\n' "$API_URL"
printf ' Health:   %s/health\n' "$API_URL"
printf ' Região:   %s\n' "$IBMCLOUD_REGION"
printf ' Projeto:  %s\n' "$CE_PROJECT"
printf '============================================================\n'
printf '\nPróximos passos:\n'
printf '  - Abra o frontend e conclua o onboarding.\n'
printf '  - Para logs: ibmcloud ce app logs -n %s\n' "$API_APP_NAME"
printf '  - Para atualizar: ./deploy/deploy.sh\n'
