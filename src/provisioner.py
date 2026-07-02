#!/usr/bin/env python3
"""
Auto-Provisioner Mesh IoT con Tailscale

Script principale che orchestra il provisioning automatico
di dispositivi IoT su una mesh VPN Tailscale.
"""

import argparse
import os
import sys
from pathlib import Path

from config_loader import ConfigLoader, ConfigValidationError
from tailscale_client import TailscaleClient, TailscaleError
from acl_manager import ACLManager


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Provisioning automatico dispositivi IoT su Tailscale mesh VPN"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="devices.yaml",
        help="Percorso al file YAML di configurazione dei dispositivi",
    )
    parser.add_argument(
        "--apply-acl",
        action="store_true",
        help="Applica le ACL policies tramite Tailscale API",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula le operazioni senza applicare modifiche",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Abilita output dettagliato",
    )

    args = parser.parse_args()

    auth_key = os.environ.get("TAILSCALE_AUTH_KEY")
    api_token = os.environ.get("TAILSCALE_API_TOKEN")

    if not auth_key:
        print("ERRORE: impostare la variabile d'ambiente TAILSCALE_AUTH_KEY", file=sys.stderr)
        return 1

    try:
        loader = ConfigLoader(args.config)
        devices = loader.load()
    except ConfigValidationError as e:
        print(f"ERRORE configurazione: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"ERRORE: file configurazione non trovato: {args.config}", file=sys.stderr)
        return 1

    client = TailscaleClient(auth_key=auth_key, dry_run=args.dry_run)

    for device in devices:
        print(f"Provisioning: {device.name} ({device.hostname})")
        try:
            commands = client.generate_commands(device)
            for cmd in commands:
                print(f"  $ {cmd}")
            if not args.dry_run:
                client.apply(device)
        except TailscaleError as e:
            print(f"  ERRORE: {e}", file=sys.stderr)
            return 1

    if args.apply_acl:
        if not api_token:
            print("ERRORE: impostare TAILSCALE_API_TOKEN per applicare le ACL", file=sys.stderr)
            return 1
        acl_manager = ACLManager(api_token=api_token, dry_run=args.dry_run)
        print("Applicazione ACL policies...")
        acl_manager.apply_from_devices(devices)

    print("Provisioning completato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
