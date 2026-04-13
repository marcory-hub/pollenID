#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import re


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


def humanize_next_token(token: str) -> str:
    """
    Turn internal 'next' tokens (that are not step ids) into a readable endpoint name.
    Examples:
      beug_..._223151_pisum_sativum_sub -> Pisum sativum
      ..._viburnum_opulus_type_sub -> Viburnum opulus-type
      ..._vicia_type_s_str_sub -> Vicia type s. str.
    """
    if not isinstance(token, str) or not token:
        return "-"
    t = token.strip()
    t = re.sub(r"_sub$", "", t)
    # drop leading prefixes up to last numeric chunk
    m = re.search(r"(?:^|_)(\d{3,})(?:_|$)", t)
    if m:
        t = t[m.end() :]
    t = t.strip("_")
    if not t:
        return "-"
    t = t.replace("_type", "-type")
    t = t.replace("_groep", "-groep")
    t = t.replace("_s_str", " s. str.")
    t = t.replace("_s_l", " s. l.")
    parts = [p for p in t.split("_") if p]
    if not parts:
        return "-"
    parts[0] = parts[0][:1].upper() + parts[0][1:]
    return " ".join(parts)


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
            # If a choice points to an external token (next not in steps), convert to endpoint id.
            nxt = ch.get("next")
            if isinstance(nxt, str) and nxt and nxt not in steps and not isinstance(ch.get("id"), dict):
                ch["id"] = {"name": humanize_next_token(nxt)}
                ch.pop("next", None)
                ident = ch["id"]
                changed = True

            if isinstance(ident, dict):
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

