#!/usr/bin/env python3
"""Strip duplicated taxon payloads from VD-style keys and Kerkvliet rows when pollen.yaml has the slug.

- van der Ham: terminal `choices[].id` becomes `{ "pollen_key", "note"? }`; removes name/size/source/text/images/image.
  Also removes `choices[].image` / `choices[].images` on terminal branches with a resolved slug (images come from pollen.json).
  Branching rows (`next` set) keep choice-level thumbnails.
- Kerkvliet: rows with a valid pollen_key shrink to `{ "section", "pollen_key" }`.

Run after changes to pollen.yaml entries; requires matching keys in YAML.

Usage:
  ./.venv/bin/python scripts/slim_pollen_key_endpoints.py \\
    docs/keys/vanderham/vanderham-pollentabel.json \\
    docs/keys/kerkvliet/kerkvliet-determinatietabel.json
"""
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"


def valid_slugs() -> Set[str]:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return set()
    return {k for k in data if isinstance(k, str)}


def norm_pk(v):
    if not isinstance(v, str):
        return ""
    s = v.strip()
    return "" if not s or s == "-" else s


def slim_id(ep: Dict, slugs: Set[str]) -> Optional[Dict]:
    pk = norm_pk(ep.get("pollen_key"))
    if pk not in slugs:
        return None
    out: Dict = {"pollen_key": pk}
    note = ep.get("note")
    if isinstance(note, str) and note.strip():
        out["note"] = note.strip()
    if ep.get("incomplete") is True:
        out["incomplete"] = True
    return out


def slim_vdh(path: Path, slugs: Set[str]) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for step in (data.get("steps") or {}).values():
        if not isinstance(step, dict):
            continue
        for ch in step.get("choices") or []:
            if not isinstance(ch, dict):
                continue
            ep = ch.get("id")
            new_id = None
            if isinstance(ep, dict):
                new_id = slim_id(ep, slugs)
                if new_id is not None:
                    ch["id"] = new_id
                    n += 1

            terminal = not ch.get("next")
            pk_ok = isinstance(ch.get("id"), dict) and norm_pk(ch["id"].get("pollen_key")) in slugs
            if terminal and pk_ok:
                ch.pop("image", None)
                ch.pop("images", None)
                # drop legacy lone image fields duplicated on endpoints
                if isinstance(ch.get("id"), dict):
                    pass

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return n


def slim_kerk(path: Path, slugs: Set[str]) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("rows")
    if not isinstance(rows, list):
        return 0
    n = 0
    new_rows = []
    for row in rows:
        if not isinstance(row, dict):
            new_rows.append(row)
            continue
        pk = norm_pk(row.get("pollen_key"))
        if pk in slugs and isinstance(row.get("section"), str):
            new_rows.append({"section": row["section"], "pollen_key": pk})
            n += 1
        else:
            new_rows.append(row)
    data["rows"] = new_rows
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return n


def main() -> int:
    raw_paths = [Path(p) for p in sys.argv[1:]]
    paths = [(ROOT / p).resolve() if not p.is_absolute() else p for p in raw_paths]
    if len(paths) < 1:
        print("Provide one or more JSON paths", file=sys.stderr)
        return 2
    slugs = valid_slugs()
    for p in paths:
        if not p.exists():
            print(f"skip missing {p}", file=sys.stderr)
            continue
        if "kerkvliet-determinatietabel" in p.name:
            c = slim_kerk(p, slugs)
            print(f"{p.relative_to(ROOT)}\tKerckv rows slimmed: {c}")
        else:
            c = slim_vdh(p, slugs)
            print(f"{p.relative_to(ROOT)}\tEndpoints slimmed: {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
