"""Wrapper client per comandi Tailscale CLI e API."""

import subprocess
from typing import List

from config_loader import Device


class TailscaleError(Exception):
    """Errore durante l'interazione con Tailscale."""

    pass


class TailscaleClient:
    """Client per eseguire comandi Tailscale CLI e chiamate API."""

    def __init__(self, auth_key: str, dry_run: bool = False) -> None:
        self.auth_key = auth_key
        self.dry_run = dry_run

    def _build_argv_list(self, device: Device) -> List[List[str]]:
        """Costruisce i comandi 'tailscale up' come liste di argomenti
        (nessuna interpolazione in stringhe di shell)."""
        cmd = ["tailscale", "up", "--authkey", self.auth_key]

        if device.advertise_routes:
            cmd.extend(["--advertise-routes", ",".join(device.advertise_routes)])

        if device.advertise_exit_node:
            cmd.append("--advertise-exit-node")

        if device.hostname:
            cmd.extend(["--hostname", device.hostname])

        if not device.ssh:
            cmd.append("--ssh=false")

        return [cmd]

    def generate_commands(self, device: Device) -> List[str]:
        """Genera i comandi 'tailscale up' per un dispositivo, in forma
        di stringa leggibile (solo per log/anteprima, non per l'esecuzione)."""
        return [" ".join(argv) for argv in self._build_argv_list(device)]

    def apply(self, device: Device) -> None:
        """Esegue il provisioning del dispositivo tramite Tailscale CLI."""
        argv_list = self._build_argv_list(device)
        for argv in argv_list:
            if self.dry_run:
                continue
            result = subprocess.run(
                argv,
                shell=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise TailscaleError(
                    f"Comando fallito per {device.name}: {result.stderr.strip()}"
                )
