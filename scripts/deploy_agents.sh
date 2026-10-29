#!/usr/bin/env bash
# scripts/deploy_agents.sh — Importa/atualiza os agentes no watsonx Orchestrate.
#
# Uso:
#   ./scripts/deploy_agents.sh               # importa todos os 3 agentes
#   ./scripts/deploy_agents.sh mentor        # importa apenas o Mentor
#   ./scripts/deploy_agents.sh catalyst      # importa apenas o Catalisador
#   ./scripts/deploy_agents.sh analyst       # importa apenas o Analista
#
# Pré-requisito: CLI do Orchestrate autenticada (orchestrate env activate ...)

set -euo pipefail

AGENT=${1:-all}
AGENTS_DIR="$(dirname "$0")/../agents"

import_agent() {
    local name="$1"
    local file="$2"
    echo "→ Importando $name..."
    orchestrate agents import --file "$file"
    echo "  Sucesso. Obtenha o UUID com: orchestrate agents list -v | grep $name"
}

case "$AGENT" in
  mentor)
    import_agent "prisma_mentor" "$AGENTS_DIR/prisma_mentor.yaml"
    ;;
  catalyst)
    import_agent "prisma_catalyst" "$AGENTS_DIR/prisma_catalyst.yaml"
    ;;
  analyst)
    import_agent "prisma_analyst" "$AGENTS_DIR/prisma_analyst.yaml"
    ;;
  all)
    import_agent "prisma_mentor"   "$AGENTS_DIR/prisma_mentor.yaml"
    import_agent "prisma_catalyst" "$AGENTS_DIR/prisma_catalyst.yaml"
    import_agent "prisma_analyst"  "$AGENTS_DIR/prisma_analyst.yaml"
    ;;
  *)
    echo "Agente desconhecido: $AGENT. Use: mentor | catalyst | analyst | all"
    exit 1
    ;;
esac

echo ""
echo "Após importar, registre os UUIDs no .env:"
echo "  ORCHESTRATE_AGENT_MENTOR_ID=<uuid>"
echo "  ORCHESTRATE_CATALYST_AGENT_ID=<uuid>"
echo "  ORCHESTRATE_ANALYST_AGENT_ID=<uuid>"
