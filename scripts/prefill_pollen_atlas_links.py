#!/usr/bin/env python3
"""Fill empty pollenX / tstebler / paldat / waarneming slots in data/pollen.yaml from latin binomial.

Only writes URLs into empty (null/blank) link fields; does not overwrite custom URLs.
Use explicit null in YAML to suppress a default atlas link (see update-pollen-yaml skill).

Usage:
  python scripts/prefill_pollen_atlas_links.py --dry-run
  python scripts/prefill_pollen_atlas_links.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from pollen_display import default_external_links, entry_latin  # noqa: E402

YAML_LINK_KEYS = ("pollenX", "tstebler", "paldat", "waarneming")
JSON_TO_YAML = {
    "pollenx": "pollenX",
    "tstebler": "tstebler",
    "paldat": "paldat",
    "waarneming": "waarneming",
}


def _link_empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
        return True
    return False


def prefill_entry(entry: Dict[str, Any]) -> Tuple[int, bool]:
    """Return (slots_filled, changed)."""
    latin = entry_latin(entry)
    if not isinstance(latin, str) or not latin.strip():
        return 0, False
    defaults = default_external_links(latin.strip())
    if not defaults:
        return 0, False

    links = entry.get("links")
    if not isinstance(links, dict):
        links = {}
        entry["links"] = links

    filled = 0
    for json_key, yaml_key in JSON_TO_YAML.items():
        url = defaults.get(json_key)
        if not url:
            continue
        current = links.get(yaml_key)
        if links.get("pollenx") and yaml_key == "pollenX" and _link_empty(current):
            current = links.get("pollenx")
        if not _link_empty(current):
            continue
        links[yaml_key] = url
        if yaml_key == "pollenX" and "pollenx" in links:
            del links["pollenx"]
        filled += 1
    return filled, filled > 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--path", type=Path, default=YAML_PATH)
    args = parser.parse_args()

    data = yaml.safe_load(args.path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        print(f"{args.path}: invalid root", file=sys.stderr)
        return 1

    taxa_changed = 0
    slots_filled = 0
    no_latin = 0
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        latin = entry_latin(entry)
        if not isinstance(latin, str) or not latin.strip():
            no_latin += 1
            continue
        n, changed = prefill_entry(entry)
        if changed:
            taxa_changed += 1
            slots_filled += n

    print(f"taxa: {len(data)}")
    print(f"no latin: {no_latin}")
    print(f"taxa updated: {taxa_changed}")
    print(f"link slots filled: {slots_filled}")

    if args.dry_run:
        print("dry-run: no file written")
        return 0

    from ruamel.yaml import YAML

    ry = YAML()
    ry.preserve_quotes = True
    ry.default_flow_style = False
    ry.width = 4096
    ry.indent(mapping=2, sequence=4, offset=2)
    with args.path.open("w", encoding="utf-8") as fh:
        ry.dump(data, fh)
    print(f"wrote {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
