#!/usr/bin/env python3
"""
Sync Beug algorithm flow paths into data/pollen.yaml (compact form).

Field name: `beug_key_paths`

- Source of truth for the flow text/structure: scripts/extract_key_paths.py
  (Beug section), which reads `docs/keys/beug/*.json`.
- Write only when Beug extraction yields matches for the given pollen_key slug.
- When there are no matches for a slug, remove the field (no empty lists).

After writing, run:
  python scripts/normalize_pollen_yaml_schema.py
to enforce canonical top-level field ordering.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from extract_key_paths import extract_paths_for_taxon  # noqa: E402


def _first_nonempty_line(s: str) -> str:
    for ln in (s or "").splitlines():
        ln = ln.strip()
        if ln:
            return ln
    return ""


def _compact_path(pr: Any) -> Dict[str, Any]:
    # pr is PathRender from extract_key_paths.py
    chosen: List[str] = []
    for step in pr.steps:
        idx = getattr(step, "chosen_idx", None)
        choices = getattr(step, "choices", None)
        if isinstance(idx, int) and isinstance(choices, list) and 0 <= idx < len(choices):
            chosen.append(str(choices[idx]))
    return {
        "key_id": getattr(pr, "key_id", ""),
        "key_title": getattr(pr, "key_title", ""),
        "chosen": chosen,
        "outcome": _first_nonempty_line(getattr(pr, "outcome_label", "")),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--path",
        type=Path,
        default=YAML_PATH,
        help="Path to data/pollen.yaml (defaults to repo SoT).",
    )
    ap.add_argument(
        "--slug",
        action="append",
        default=[],
        help="Only sync one or more pollen_key slugs (repeatable).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Report only; do not write.",
    )
    args = ap.parse_args()

    if not args.path.is_file():
        raise SystemExit(f"Missing YAML: {args.path}")

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    data = yaml.load(args.path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{args.path}: expected mapping at top-level")

    slugs_all = [k for k in data.keys() if isinstance(k, str)]
    slugs = args.slug if args.slug else slugs_all

    changed = 0
    with_paths = 0
    without_paths = 0
    missing_yaml = 0

    for slug in slugs:
        entry = data.get(slug)
        if not isinstance(entry, dict):
            missing_yaml += 1
            continue

        paths = extract_paths_for_taxon(slug)
        beug_paths = paths.get("beug") or []

        if beug_paths:
            entry["beug_key_paths"] = [_compact_path(pr) for pr in beug_paths]
            changed += 1
            with_paths += 1
        else:
            if "beug_key_paths" in entry:
                del entry["beug_key_paths"]
                changed += 1
            without_paths += 1

    print(
        "sync_beug_key_paths:",
        f"slugs_scanned={len(slugs)}",
        f"changed_entries={changed}",
        f"with_paths={with_paths}",
        f"without_paths={without_paths}",
        f"missing_yaml={missing_yaml}",
    )

    if args.dry_run:
        return 0

    args.path.write_text(
        _yaml_dump(yaml, data),
        encoding="utf-8",
        newline="\n",
    )
    return 0


def _yaml_dump(yaml: YAML, data: Dict[str, Any]) -> str:
    import io

    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue()


if __name__ == "__main__":
    raise SystemExit(main())

