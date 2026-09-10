"""Configurazione pytest a livello di repo.

I moduli applicativi vivono sotto ``src/`` e vengono importati nei test
come pacchetti top-level (es. ``from tailscale_client import ...``),
coerentemente con il modo in cui li importa ``src/provisioner.py``.
Aggiungiamo quindi ``src/`` a ``sys.path`` prima della raccolta dei test.
"""

import sys
from pathlib import Path

SRC_PATH = str(Path(__file__).parent / "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
