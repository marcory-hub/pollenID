#!/usr/bin/env python3
"""Regenerate docs site data artifacts from data/pollen.yaml.

Order: export pollen.json (+ taxa detail) -> species pages -> build manifests
-> morph neighbours JSON for PalynoQuest name-MCQ.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT = REPO / "scripts" / "export_pollen_json.py"
RENDER = REPO / "scripts" / "render_taxon_pages_from_sot.py"
MANIFESTS = REPO / "scripts" / "build_manifests.py"
MORPH_NEIGHBOURS = REPO / "scripts" / "morph_lookalike_cluster.py"


def main() -> int:
    r1 = subprocess.run([sys.executable, str(EXPORT)], cwd=REPO, check=False)
    if r1.returncode != 0:
        return r1.returncode
    r1b = subprocess.run(
        [sys.executable, str(RENDER), "--build-all-species"],
        cwd=REPO,
        check=False,
    )
    if r1b.returncode != 0:
        return r1b.returncode
    r2 = subprocess.run([sys.executable, str(MANIFESTS)], cwd=REPO, check=False)
    if r2.returncode != 0:
        return r2.returncode
    r3 = subprocess.run([sys.executable, str(MORPH_NEIGHBOURS)], cwd=REPO, check=False)
    return r3.returncode


if __name__ == "__main__":
    raise SystemExit(main())
