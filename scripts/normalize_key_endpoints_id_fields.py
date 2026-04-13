#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYS_DIR = DOCS_DIR / "keys"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_id_obj(ident: Dict[str, Any]) -> Tuple[bool, int]:
    changed = False
    filled = 0
    for k in ("name", "size", "source"):
        if k not in ident or not isinstance(ident.get(k), str) or not ident.get(k).strip():
            ident[k] = "-"
            changed = True
            filled += 1

    # Reorder keys so images come last (stable diffs for authoring).
    desired_order = ["name", "size", "source", "text", "incomplete", "images", "image", "imageWidthPx"]
    out: Dict[str, Any] = {}
    for k in desired_order:
        if k in ident:
            out[k] = ident[k]
    for k, v in ident.items():
        if k not in out:
            out[k] = v
    if list(out.keys()) != list(ident.keys()):
        ident.clear()
        ident.update(out)
        changed = True
    return changed, filled


def migrate_key(path: Path) -> Tuple[bool, int]:
    data = read_json(path)
    if not isinstance(data, dict):
        return False, 0
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return False, 0

    changed = False
    filled_total = 0

    for _sid, step in steps.items():
        if not isinstance(step, dict):
            continue
        choices = step.get("choices")
        if not isinstance(choices, list):
            continue
        for ch in choices:
            if not isinstance(ch, dict):
                continue
            ident = ch.get("id")
            if not isinstance(ident, dict):
                continue
            c, f = normalize_id_obj(ident)
            if c:
                changed = True
                filled_total += f

    if changed:
        write_json(path, data)
    return changed, filled_total


def main() -> int:
    key_paths = sorted(KEYS_DIR.rglob("*.json"))
    changed_files = 0
    filled_fields = 0
    for kp in key_paths:
        changed, filled = migrate_key(kp)
        if changed:
            changed_files += 1
            filled_fields += filled
    print(f"changed_files={changed_files} filled_fields={filled_fields}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

