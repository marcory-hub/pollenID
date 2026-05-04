#!/usr/bin/env python3
"""Verify pollen YAML image paths exist under docs/. Optionally rebuild generated data and run mkdocs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List

import yaml

from pollen_asset_lib import DOCS_DIR, POLLEN_YAML, REPO_ROOT, yaml_image_paths

BUILD_DATA = REPO_ROOT / "scripts" / "build_docs_data.py"
POLLEN_JSON = DOCS_DIR / "data" / "pollen.json"


LEGACY_IMAGE_PREFIXES = (
    "assets/images/pollenwiki/",
    "assets/images/persano_oddo/",
    "assets/images/paldat/",
    "assets/images/placeholder/",
)


def legacy_yaml_paths(data: dict) -> List[str]:
    bad: List[str] = []
    for _key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        for rel in yaml_image_paths(entry):
            posix = rel.replace("\\", "/")
            if any(posix.startswith(p) for p in LEGACY_IMAGE_PREFIXES):
                bad.append(posix)
            if posix.startswith("assets/images/") and not posix.startswith("assets/images/by-taxon/"):
                if not posix.startswith("assets/images/non-pollen/"):
                    bad.append(posix)
    return sorted(set(bad))


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


def check_pollen_json_links() -> List[str]:
    """Fail entries with a binomial latin name but no exported atlas URLs."""
    errs: List[str] = []
    if not POLLEN_JSON.is_file():
        errs.append("missing docs/data/pollen.json (run scripts/build_docs_data.py)")
        return errs
    try:
        payload = json.loads(POLLEN_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"docs/data/pollen.json: invalid JSON ({e})"]
    if not isinstance(payload, dict):
        return ["docs/data/pollen.json: top-level must be an object"]

    atlas_keys = ("pollenx", "tstebler", "paldat")
    for key, rec in sorted(payload.items(), key=lambda x: x[0]):
        if not isinstance(rec, dict):
            continue
        lat = rec.get("latin")
        if not isinstance(lat, str) or len(lat.strip().split()) < 2:
            continue
        links = rec.get("links")
        if not isinstance(links, dict) or not any(
            isinstance(links.get(k), str) and links[k].strip() for k in atlas_keys
        ):
            errs.append(f"{key}: binomial latin but no links (expected one of {atlas_keys})")
    return errs


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
    ap.add_argument(
        "--enforce-asset-layout",
        action="store_true",
        help="Fail if pollen image paths are not under assets/images/by-taxon/ (except non-pollen/)",
    )
    ap.add_argument(
        "--images",
        action="store_true",
        help="Alias for --enforce-asset-layout (canonical pollen image paths in YAML)",
    )
    ap.add_argument(
        "--links",
        action="store_true",
        help="Verify docs/data/pollen.json has atlas links for binomial taxa",
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

    enforce_layout = args.enforce_asset_layout or args.images
    if enforce_layout:
        legacy = legacy_yaml_paths(raw)
        if legacy:
            print(f"Non-canonical YAML image paths ({len(legacy)}):", file=sys.stderr)
            for p in legacy[:80]:
                print(f"  {p}", file=sys.stderr)
            if len(legacy) > 80:
                print(f"  ... and {len(legacy) - 80} more", file=sys.stderr)
            return 1

    if args.links:
        link_issues = check_pollen_json_links()
        if link_issues:
            print("pollen.json link check failed:", file=sys.stderr)
            for line in link_issues[:80]:
                print(f"  {line}", file=sys.stderr)
            if len(link_issues) > 80:
                print(f"  ... and {len(link_issues) - 80} more", file=sys.stderr)
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
