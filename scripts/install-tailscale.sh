#!/usr/bin/env bash
# Installa Tailscale su sistemi Linux (Debian/Ubuntu, Fedora, Arch)
# Uso: ./install-tailscale.sh

set -euo pipefail

echo "=== Installazione Tailscale ==="

if command -v apt-get &>/dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
elif command -v dnf &>/dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
elif command -v pacman &>/dev/null; then
    sudo pacman -S tailscale
else
    echo "Gestore pacchetti non supportato. Visita https://tailscale.com/download"
    exit 1
fi

echo "Tailscale installato. Avvia con: sudo tailscale up --authkey \$TAILSCALE_AUTH_KEY"
