#!/usr/bin/env bash
#
# Instala a IBM Cloud CLI e os plugins usados pelo deploy, sem sudo,
# em ~/.local/ibmcloud.
#
set -euo pipefail

IBMCLOUD_CLI_VERSION="${IBMCLOUD_CLI_VERSION:-2.48.1}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/ibmcloud}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

log() { printf '\n==> %s\n' "$*"; }
die() { printf '\nERRO: %s\n' "$*" >&2; exit 1; }

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$OS" in
  darwin)
    case "$ARCH" in
      arm64) PKG="IBM_Cloud_CLI_${IBMCLOUD_CLI_VERSION}_arm64.pkg" ;;
      x86_64) PKG="IBM_Cloud_CLI_${IBMCLOUD_CLI_VERSION}.pkg" ;;
      *) die "Arquitetura macOS não suportada: $ARCH" ;;
    esac
    URL="https://download.clis.cloud.ibm.com/ibm-cloud-cli-dn/${IBMCLOUD_CLI_VERSION}/${PKG}"

    log "Baixando IBM Cloud CLI para macOS ($ARCH)"
    curl -fsSL "$URL" -o "$TMP_DIR/cli.pkg"

    log "Extraindo pacote"
    pkgutil --expand-full "$TMP_DIR/cli.pkg" "$TMP_DIR/pkg"
    PAYLOAD="$TMP_DIR/pkg/Command_Line_Interface.pkg/Payload/usr/local/ibmcloud"
    [[ -d "$PAYLOAD" ]] || die "Payload do pacote não encontrado."
    ;;
  linux)
    case "$ARCH" in
      x86_64|amd64) ARCHIVE_ARCH="amd64" ;;
      aarch64|arm64) ARCHIVE_ARCH="arm64" ;;
      *) die "Arquitetura Linux não suportada: $ARCH" ;;
    esac
    URL="https://download.clis.cloud.ibm.com/ibm-cloud-cli-dn/${IBMCLOUD_CLI_VERSION}/IBM_Cloud_CLI_${IBMCLOUD_CLI_VERSION}_${ARCHIVE_ARCH}.tar.gz"

    log "Baixando IBM Cloud CLI para Linux ($ARCHIVE_ARCH)"
    curl -fsSL "$URL" -o "$TMP_DIR/cli.tar.gz"
    tar -xzf "$TMP_DIR/cli.tar.gz" -C "$TMP_DIR"
    PAYLOAD="$TMP_DIR/Bluemix_CLI"
    [[ -d "$PAYLOAD/bin" ]] || die "Binários do CLI não encontrados no pacote."
    ;;
  *)
    die "Sistema não suportado: $OS"
    ;;
esac

log "Instalando em $INSTALL_DIR"
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/bin" "$INSTALL_DIR/autocomplete"

if [[ -d "$PAYLOAD/bin" ]]; then
  cp -R "$PAYLOAD/bin/." "$INSTALL_DIR/bin/"
fi
if [[ -d "$PAYLOAD/autocomplete" ]]; then
  cp -R "$PAYLOAD/autocomplete/." "$INSTALL_DIR/autocomplete/"
fi

chmod +x "$INSTALL_DIR/bin/ibmcloud"

mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/bin/ibmcloud" "$BIN_DIR/ibmcloud"

export PATH="$BIN_DIR:$PATH"

log "Versão instalada"
ibmcloud version

log "Instalando plugins"
ibmcloud plugin install code-engine -f
ibmcloud plugin install container-registry -f
ibmcloud plugin install cloud-databases -f

printf '\nIBM Cloud CLI instalada em %s\n' "$BIN_DIR/ibmcloud"
printf 'Adicione ao seu PATH se ainda não estiver:\n'
printf '  export PATH="%s:$PATH"\n' "$BIN_DIR"
