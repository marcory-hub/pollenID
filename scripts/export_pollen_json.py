#!/usr/bin/env python3
"""Export data/pollen.yaml to docs/assets/data/pollen.json for runtime use.

Writes a minimal, deterministic JSON index so `docs/javascripts/vdh-pollentabel.js`
can resolve endpoint info (latin, dutch, family, size, images) from the SoT without
macros running in JSON files.

Usage: python3 scripts/export_pollen_json.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import yaml


REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
JSON_PATH = REPO / "docs" / "assets" / "data" / "pollen.json"

FIELDS_SIZE = ("smallest_size", "largest_size")


def _clean_scalar(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s in ("", "-", "null", "None"):
            return None
        return s
    return v


def _build_entry(src: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    latin = _clean_scalar(src.get("latin"))
    dutch = _clean_scalar(src.get("dutch"))
    family = _clean_scalar(src.get("family"))

    if latin is not None:
        out["latin"] = latin
    if dutch is not None:
        out["dutch"] = dutch
    if family is not None:
        out["family"] = family

    size_src = src.get("size") or {}
    if isinstance(size_src, dict):
        size_out: Dict[str, Any] = {}
        for key in FIELDS_SIZE:
            val = _clean_scalar(size_src.get(key))
            if val is not None:
                size_out[key] = val
        if size_out:
            out["size"] = size_out

    images_src = src.get("images")
    if isinstance(images_src, list) and images_src:
        images_out = []
        for im in images_src:
            if not isinstance(im, dict):
                continue
            path = _clean_scalar(im.get("path"))
            if not path:
                continue
            item: Dict[str, Any] = {"path": path}
            kind = _clean_scalar(im.get("kind"))
            source = _clean_scalar(im.get("source"))
            if kind is not None:
                item["kind"] = kind
            if source is not None:
                item["source"] = source
            images_out.append(item)
        if images_out:
            out["images"] = images_out

    return out


def main() -> int:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Unexpected top-level YAML type: {type(data).__name__}")

    exported: Dict[str, Dict[str, Any]] = {}
    for key in sorted(data.keys()):
        entry = data.get(key)
        if not isinstance(entry, dict):
            continue
        exported[key] = _build_entry(entry)

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(exported, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH.relative_to(REPO)} ({len(exported)} entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
