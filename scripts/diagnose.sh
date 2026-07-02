#!/usr/bin/env bash
# Script di diagnostica per la mesh Tailscale
# Uso: ./diagnose.sh

set -euo pipefail

echo "=== Diagnostica Mesh Tailscale ==="
echo

echo "--- Stato Tailscale ---"
tailscale status || true
echo

echo "--- IP Tailscale ---"
tailscale ip -4 || true
echo

echo "--- Route pubblicizzate ---"
tailscale debug prefs | grep -i route || true
echo

echo "--- Connessione API Tailscale ---"
if [ -n "${TAILSCALE_API_TOKEN:-}" ]; then
    curl -s -o /dev/null -w "HTTP %{http_code}\n" \
        -H "Authorization: Bearer $TAILSCALE_API_TOKEN" \
        "https://api.tailscale.com/api/v2/tailnet/-/devices" || true
else
    echo "TAILSCALE_API_TOKEN non impostato"
fi
echo

echo "=== Diagnostica completata ==="
