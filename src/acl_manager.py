"""Gestione ACL via Tailscale API."""

import json
import os
from typing import List

import requests

from config_loader import Device


class ACLManager:
    """Gestisce le ACL policies tramite Tailscale API."""

    API_BASE = "https://api.tailscale.com/api/v2"

    def __init__(self, api_token: str, dry_run: bool = False) -> None:
        self.api_token = api_token
        self.dry_run = dry_run
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def apply_from_devices(self, devices: List[Device]) -> None:
        """Genera e applica le ACL policies in base ai ruoli dei dispositivi."""
        acl = self._build_acl(devices)
        if self.dry_run:
            print("[dry-run] ACL da applicare:")
            print(json.dumps(acl, indent=2))
            return
        self._push_acl(acl)

    def _build_acl(self, devices: List[Device]) -> dict:
        """Costruisce le ACL policies in base ai ruoli."""
        acls = []
        for device in devices:
            if device.role == "iot":
                acls.append({
                    "action": "accept",
                    "src": [f"tag:{device.tags[0]}" if device.tags else "*"],
                    "dst": ["tag:hub:*"],
                })
            elif device.role == "hub":
                acls.append({
                    "action": "accept",
                    "src": ["tag:hub"],
                    "dst": ["*:*"],
                })

        return {
            "acls": acls,
            "tagOwners": {
                "tag:hub": ["autogroup:admin"],
                "tag:iot": ["autogroup:admin"],
            },
        }

    def _push_acl(self, acl: dict) -> None:
        """Invia le ACL alla Tailscale API."""
        tailnet = os.environ.get("TAILSCALE_TAILNET", "")
        if not tailnet:
            raise RuntimeError("Impostare TAILSCALE_TAILNET per applicare le ACL")

        url = f"{self.API_BASE}/tailnet/{tailnet}/acl"
        response = requests.post(url, headers=self.headers, json=acl, timeout=30)
        response.raise_for_status()
