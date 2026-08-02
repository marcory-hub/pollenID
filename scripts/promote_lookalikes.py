#!/usr/bin/env python3
"""Promote confirmed lookalike pairs from data/lookalike_review.yaml into data/pollen.yaml.

Writes bidirectional lookalikes.pairs (status: confirmed) and optional lookalikes.groups
slugs on both taxa. Does not invent partners; only status=confirmed rows are promoted.

Usage:
  ./.venv/bin/python scripts/promote_lookalikes.py --dry-run
  ./.venv/bin/python scripts/promote_lookalikes.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from ruamel.yaml import YAML

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
REVIEW_PATH = REPO / "data" / "lookalike_review.yaml"

# Group slug → members (training units). Confirmed when all listed pairs exist or
# when seed groups are referenced from review signals.group.
KNOWN_GROUPS: Dict[str, List[str]] = {
    "acer-prunus-pyrus": [
        "acer_platanoides",
        "prunus_pirus_typ",
        "malus_typ",
        "robinia_pseudoacacia",
    ],
    "rubus-prunus-vogelkers": [
        "rubus_typ",
        "prunus_padus",
        "prunus_serotina",
    ],
    "melilotus-trifolium-repens": [
        "trifolium_repens",
        "melilotus_officinalis",
        "aesculus_hippocastanum",
    ],
    "raphanus-brassica-sinapis-ligustrum": [
        "raphanus_typ",
        "brassica_typ",
        "sinapis_typ",
        "ligustrum_vulgare",
    ],
    "fraxinus-salix-cruciferae": [
        "salix_typ",
        "fraxinus_ornus",
        "brassica_typ",
    ],
    "umbelliferae-vicia": [
        "anthriscus_typ",
        "vicia_typ",
    ],
    "fenestraat-taraxacum": [
        "taraxacum_typ",
        "cichorium_intybus",
        "hieracium_typ",
        "hieracium_aurantiacum",
        "crepis_biennis",
        "tragopogon_typ",
        "sonchus_arvensis",
    ],
}


def _load_ruamel(path: Path) -> Any:
    y = YAML()
    y.preserve_quotes = True
    with path.open(encoding="utf-8") as fh:
        return y.load(fh)


def _write_ruamel(path: Path, data: Any) -> None:
    y = YAML()
    y.preserve_quotes = True
    y.default_flow_style = False
    y.width = 4096
    y.indent(mapping=2, sequence=4, offset=2)
    with path.open("w", encoding="utf-8") as fh:
        y.dump(data, fh)


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def _ensure_lookalikes(entry: Dict[str, Any]) -> Dict[str, Any]:
    block = entry.get("lookalikes")
    if not isinstance(block, dict):
        block = {}
        entry["lookalikes"] = block
    if not isinstance(block.get("pairs"), list):
        block["pairs"] = []
    if not isinstance(block.get("groups"), list):
        block["groups"] = []
    return block


def _upsert_pair(
    entry: Dict[str, Any],
    partner: str,
    *,
    status: str,
    note: Optional[str],
    difficulty: Optional[str] = None,
) -> bool:
    block = _ensure_lookalikes(entry)
    pairs: List[Any] = block["pairs"]
    for item in pairs:
        if isinstance(item, dict) and item.get("partner") == partner:
            changed = False
            if item.get("status") != status:
                item["status"] = status
                changed = True
            if note and item.get("note") != note:
                item["note"] = note
                changed = True
            if difficulty and item.get("difficulty") != difficulty:
                item["difficulty"] = difficulty
                changed = True
            return changed
    row: Dict[str, Any] = {"partner": partner, "status": status}
    if note:
        row["note"] = note
    if difficulty:
        row["difficulty"] = difficulty
    pairs.append(row)
    return True


def _upsert_group(entry: Dict[str, Any], group_slug: str) -> bool:
    block = _ensure_lookalikes(entry)
    groups: List[Any] = block["groups"]
    if group_slug in groups:
        return False
    groups.append(group_slug)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--review", type=Path, default=REVIEW_PATH)
    parser.add_argument("--yaml", type=Path, default=YAML_PATH)
    args = parser.parse_args()

    review = _load_ruamel(args.review)
    if not isinstance(review, list):
        raise SystemExit(f"{args.review}: expected a list of review rows")

    data = _load_ruamel(args.yaml)
    if not isinstance(data, dict):
        raise SystemExit(f"{args.yaml}: expected a mapping")

    confirmed_pairs: Set[Tuple[str, str]] = set()
    pair_notes: Dict[Tuple[str, str], Optional[str]] = {}
    pair_difficulty: Dict[Tuple[str, str], Optional[str]] = {}
    pair_groups: Dict[Tuple[str, str], Optional[str]] = {}
    missing: List[str] = []
    allowed_diff = {"easy", "moderate", "difficult"}

    for row in review:
        if not isinstance(row, dict):
            continue
        if row.get("status") != "confirmed":
            continue
        a = row.get("anchor")
        b = row.get("partner")
        if not isinstance(a, str) or not isinstance(b, str):
            continue
        if a not in data:
            missing.append(a)
            continue
        if b not in data:
            missing.append(b)
            continue
        pk = _pair_key(a, b)
        confirmed_pairs.add(pk)
        note = row.get("note")
        if isinstance(note, str) and note.strip():
            pair_notes[pk] = note.strip()
        diff = row.get("difficulty")
        if isinstance(diff, str) and diff.strip().lower() in allowed_diff:
            pair_difficulty[pk] = diff.strip().lower()
        signals = row.get("signals") if isinstance(row.get("signals"), dict) else {}
        g = signals.get("group")
        if isinstance(g, str) and g.strip():
            pair_groups[pk] = g.strip()

    if missing:
        uniq = sorted(set(missing))
        print(f"WARNING: missing pollen.yaml keys (skipped): {', '.join(uniq)}")

    # Groups referenced by confirmed pairs or fully covered known groups.
    groups_to_apply: Dict[str, Set[str]] = {}
    for pk, g in pair_groups.items():
        if not g:
            continue
        members = groups_to_apply.setdefault(g, set())
        members.update(pk)

    for g, members in KNOWN_GROUPS.items():
        # Apply group label to any confirmed member that appears in a confirmed pair of this group.
        touched = False
        for i, a in enumerate(members):
            for b in members[i + 1 :]:
                if _pair_key(a, b) in confirmed_pairs:
                    touched = True
                    break
            if touched:
                break
        if touched:
            groups_to_apply.setdefault(g, set()).update(
                m for m in members if m in data
            )

    changes = 0
    for a, b in sorted(confirmed_pairs):
        note = pair_notes.get((a, b))
        difficulty = pair_difficulty.get((a, b))
        if _upsert_pair(data[a], b, status="confirmed", note=note, difficulty=difficulty):
            changes += 1
        if _upsert_pair(data[b], a, status="confirmed", note=note, difficulty=difficulty):
            changes += 1

    for g, members in sorted(groups_to_apply.items()):
        # Prefer full known member list when available.
        apply_members = KNOWN_GROUPS.get(g, sorted(members))
        for slug in apply_members:
            if slug not in data:
                continue
            if _upsert_group(data[slug], g):
                changes += 1

    print(
        f"Confirmed pairs: {len(confirmed_pairs)}; groups: {len(groups_to_apply)}; "
        f"field upserts: {changes}"
    )
    if args.dry_run:
        print("Dry run: no write.")
        return 0

    _write_ruamel(args.yaml, data)
    print(f"Wrote {args.yaml.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
