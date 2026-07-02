"""Parsing e validazione del file YAML dei dispositivi."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


class ConfigValidationError(Exception):
    """Errore di validazione della configurazione."""

    pass


@dataclass
class Device:
    """Rappresenta un dispositivo IoT da provisionare."""

    name: str
    hostname: str
    role: str
    advertise_routes: List[str] = field(default_factory=list)
    advertise_exit_node: bool = False
    tags: List[str] = field(default_factory=list)
    ssh: bool = True


class ConfigLoader:
    """Carica e valida il file YAML di configurazione dei dispositivi."""

    REQUIRED_FIELDS = {"name", "hostname", "role"}
    VALID_ROLES = {"hub", "iot", "gateway", "exit-node"}

    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self) -> List[Device]:
        """Carica e valida il file YAML, restituisce la lista di Device."""
        if not self.path.exists():
            raise FileNotFoundError(self.path)

        with self.path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "devices" not in data:
            raise ConfigValidationError("Il file YAML deve contenere una chiave 'devices'")

        devices = []
        for idx, item in enumerate(data["devices"]):
            devices.append(self._parse_device(item, idx))

        return devices

    def _parse_device(self, item: dict, idx: int) -> Device:
        """Valida e converte un dizionario in un oggetto Device."""
        if not isinstance(item, dict):
            raise ConfigValidationError(f"Dispositivo {idx}: deve essere un dizionario")

        missing = self.REQUIRED_FIELDS - item.keys()
        if missing:
            raise ConfigValidationError(
                f"Dispositivo {idx}: campi obbligatori mancanti: {missing}"
            )

        role = item.get("role", "")
        if role not in self.VALID_ROLES:
            raise ConfigValidationError(
                f"Dispositivo {idx}: ruolo '{role}' non valido. "
                f"Ruoli supportati: {self.VALID_ROLES}"
            )

        routes = item.get("advertise_routes", [])
        if not isinstance(routes, list):
            raise ConfigValidationError(
                f"Dispositivo {idx}: 'advertise_routes' deve essere una lista"
            )

        return Device(
            name=item["name"],
            hostname=item["hostname"],
            role=role,
            advertise_routes=routes,
            advertise_exit_node=item.get("advertise_exit_node", False),
            tags=item.get("tags", []),
            ssh=item.get("ssh", True),
        )
