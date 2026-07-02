# Auto-Provisioner Mesh IoT con Tailscale

Provisioning automatico di dispositivi IoT su una mesh VPN sicura tramite Tailscale. Gestisce subnet routing, ACL policies e autenticazione senza configurazione manuale di firewall o port forwarding.

## Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                        Tailscale Cloud                       │
│                    (Control Plane / Coordination)           │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐           ┌────▼────┐           ┌────▼────┐
   │  Node   │◄─────────►│  Node   │◄─────────►│  Node   │
   │  Hub    │  WireGuard│  IoT-1  │  WireGuard│  IoT-2  │
   │(Linux)  │  tunnel   │(RPi/ESP)│  tunnel   │(RPi/ESP)│
   └────┬────┘           └────┬────┘           └────┬────┘
        │                     │                     │
   ┌────▼────┐           ┌────▼────┐           ┌────▼────┐
   │ Subnet  │           │ Subnet  │           │ Subnet  │
   │ Router  │           │ Client  │           │ Client  │
 └─────────────────────────────────────────────────────────────┘
                        Mesh VPN (Tailscale)
```

## Componenti

| File | Scopo |
|------|-------|
| `src/provisioner.py` | Script principale: legge YAML, genera comandi `tailscale up`, applica ACL |
| `src/acl_manager.py` | Gestione ACL via Tailscale API |
| `src/config_loader.py` | Parsing e validazione del file YAML dei dispositivi |
| `src/tailscale_client.py` | Wrapper client per comandi Tailscale CLI e API |
| `tests/` | Test unitari e di integrazione |
| `examples/` | File YAML di esempio per diversi scenari |
| `scripts/` | Script helper (installazione, diagnostica) |
| `docs/` | Documentazione aggiuntiva |

## Flusso di Provisioning

1. **Configurazione**: l'utente definisce i dispositivi in un file YAML (`devices.yaml`)
2. **Validazione**: lo script verifica che ogni dispositivo abbia i campi richiesti
3. **Generazione comandi**: per ogni dispositivo vengono generati i comandi `tailscale up` con i flag appropriati (`--advertise-routes`, `--advertise-exit-node`, ecc.)
4. **Applicazione ACL**: le policy di accesso vengono inviate alla Tailscale API
5. **Verifica**: test di connettività tra i nodi della mesh

## Requisiti

- Python >= 3.10
- Tailscale CLI installato su ogni nodo
- Auth key Tailscale (da impostare come variabile d'ambiente)
- Token API Tailscale per gestione ACL (da impostare come variabile d'ambiente)

## Installazione

```bash
pip install -r requirements.txt
```

## Configurazione

Copia il file di esempio e personalizzalo:

```bash
cp examples/devices.yaml.example devices.yaml
```

Imposta le variabili d'ambiente:

```bash
export TAILSCALE_AUTH_KEY="tskey-auth-..."
export TAILSCALE_API_TOKEN=[REDACTED]
```

## Uso

```bash
python src/provisioner.py --config devices.yaml --apply-acl
```

## Docker (Raspberry Pi / ESP32 gateway)

```bash
docker build -t auto-provisioner-mesh-iot .
docker run --env-file .env auto-provisioner-mesh-iot
```

## Licenza

MIT
