#!/usr/bin/env python3
"""Verify pollen YAML image paths exist under docs/. Optionally rebuild generated data and run mkdocs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

import yaml

from pollen_asset_lib import DOCS_DIR, POLLEN_YAML, REPO_ROOT, yaml_image_paths

BUILD_DATA = REPO_ROOT / "scripts" / "build_docs_data.py"


def broken_yaml_paths(data: dict) -> List[str]:
    broken: List[str] = []
    for _key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        for rel in yaml_image_paths(entry):
            posix = rel.replace("\\", "/")
            if posix.startswith("../") or posix.startswith("/"):
                continue
            if not (DOCS_DIR / posix).is_file():
                broken.append(posix)
    return sorted(set(broken))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--rebuild-data",
        action="store_true",
        help="Run scripts/build_docs_data.py before checks",
    )
    ap.add_argument(
        "--mkdocs-build",
        action="store_true",
        help="Run mkdocs build after YAML checks pass",
    )
    args = ap.parse_args()

    if args.rebuild_data:
        r = subprocess.run([sys.executable, str(BUILD_DATA)], cwd=REPO_ROOT)
        if r.returncode != 0:
            return r.returncode

    raw = yaml.safe_load(POLLEN_YAML.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print("pollen.yaml: invalid top-level", file=sys.stderr)
        return 1

    bad_paths = broken_yaml_paths(raw)
    if bad_paths:
        print(f"Broken YAML image paths ({len(bad_paths)}):", file=sys.stderr)
        for bp in bad_paths[:50]:
            print(f"  {bp}", file=sys.stderr)
        if len(bad_paths) > 50:
            print(f"  ... and {len(bad_paths) - 50} more", file=sys.stderr)
        return 1

    if args.mkdocs_build:
        mkdocs = REPO_ROOT / ".venv" / "bin" / "mkdocs"
        cmd = [str(mkdocs), "build"] if mkdocs.is_file() else ["mkdocs", "build"]
        r2 = subprocess.run(cmd, cwd=REPO_ROOT)
        return r2.returncode

    print("validate_pollen_site: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
