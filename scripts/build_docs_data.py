#!/usr/bin/env python3
"""Regenerate docs site data artifacts from data/pollen.yaml.

Order: export pollen.json -> build manifests (keys, images inventory, PalynoQuest).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT = REPO / "scripts" / "export_pollen_json.py"
MANIFESTS = REPO / "scripts" / "build_manifests.py"


def main() -> int:
    r1 = subprocess.run([sys.executable, str(EXPORT)], cwd=REPO, check=False)
    if r1.returncode != 0:
        return r1.returncode
    r2 = subprocess.run([sys.executable, str(MANIFESTS)], cwd=REPO, check=False)
    return r2.returncode


if __name__ == "__main__":
    raise SystemExit(main())
