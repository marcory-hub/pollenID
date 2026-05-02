#!/usr/bin/env python3
"""
Set `pollen_key` on key JSON payloads where we can tie an endpoint row to data/pollen.yaml.

- VD steps JSON (Beug / van der Ham / Eide / Reitsma / …): fills `choices[].id.pollen_key` and/or
  `choices[].outcome.pollen_key` using an existing YAML slug match, or derives a slug from a Latin binomial.
- Kerkvliet determinatietabel: adds `pollen_key` next to existing `latin` when the slug matches YAML.

Leaves unknown taxa untouched (existing '-' placeholders are stripped when no YAML match exists).

Usage:
  python3 scripts/inject_pollen_keys_into_key_json.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Set

import yaml


ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
import merge_pollen as mp  # noqa: E402


def load_valid_slugs() -> Set[str]:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return set()
    return {k for k in data.keys() if isinstance(k, str)}


def normalized_pollen_slug(v: Any) -> str:
    if not isinstance(v, str):
        return ""
    s = mp._normalize_spaces(v)
    return "" if not s or s == "-" else s


def resolve_endpoint_slug(ep: Dict[str, Any], valid: Set[str]) -> Optional[str]:
    cand = normalized_pollen_slug(ep.get("pollen_key"))
    if cand and cand in valid:
        return cand

    latin: Optional[str] = None

    txt = ep.get("text")
    name = ep.get("name")

    latin_a, _ = mp._extract_latin_and_dutch_from_name(str(name)) if isinstance(name, str) else (
        None,
        None,
    )
    if latin_a:
        latin = latin_a
    elif isinstance(txt, str) and txt.strip() and txt.strip() != "-":
        latin_b, _ = mp._extract_latin_and_dutch_from_name(str(txt))
        if latin_b:
            latin = latin_b

    if not latin:
        return None

    slug = mp.latin_to_id(latin)
    return slug if slug in valid else None


def apply_to_endpoint(ep: Dict[str, Any], valid: Set[str]) -> bool:
    if not isinstance(ep, dict):
        return False
    had = ep.get("pollen_key")

    slug = resolve_endpoint_slug(ep, valid)
    dirty = False
    if slug:
        if ep.get("pollen_key") != slug:
            ep["pollen_key"] = slug
            dirty = True
    else:
        if isinstance(had, str) and mp._normalize_spaces(had) in ("", "-") and "pollen_key" in ep:
            del ep["pollen_key"]
            dirty = True
    return dirty


def mutate_vdh(data: Dict[str, Any], valid: Set[str]) -> int:
    n = 0
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return 0

    for step in steps.values():
        for choice in step.get("choices") or []:
            if not isinstance(choice, dict):
                continue
            for blob in ("id", "outcome"):
                ep = choice.get(blob)
                if isinstance(ep, dict):
                    if apply_to_endpoint(ep, valid):
                        n += 1
    return n


def mutate_kerkvliet(rows: Any, valid: Set[str]) -> int:
    n = 0
    if not isinstance(rows, list):
        return 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        latin_raw = row.get("latin")
        if not isinstance(latin_raw, str):
            continue
        latin = mp._normalize_spaces(mp._strip_md_links(latin_raw))
        slug = mp.latin_to_id(latin)
        if slug in valid:
            if row.get("pollen_key") != slug:
                row["pollen_key"] = slug
                n += 1
    return n


def process_file(path: Path, valid: Set[str], dry_run: bool) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    mutations = 0

    rows = data.get("rows")
    sections = data.get("sections")

    if isinstance(rows, list) and isinstance(sections, list):
        mutations += mutate_kerkvliet(rows, valid)
    elif isinstance(data.get("steps"), dict):
        mutations += mutate_vdh(data, valid)

    if mutations and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return mutations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count mutations without writing JSON files.",
    )
    args = parser.parse_args()

    valid = load_valid_slugs()
    keys_dir = ROOT / "docs" / "keys"
    total_changes = 0
    touched_files = 0

    for path in sorted(keys_dir.rglob("*.json")):
        delta = process_file(path, valid, dry_run=args.dry_run)
        if delta > 0:
            touched_files += 1
            total_changes += delta
            msg = "Would update" if args.dry_run else "Updated"
            print(f"{msg} {delta} endpoints/rows\t{path.relative_to(ROOT)}", file=sys.stderr)

    print(f"pollen_yaml_slugs_valid={len(valid)} JSON_files_modified={touched_files} mutations={total_changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
