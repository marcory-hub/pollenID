#!/usr/bin/env python3
"""Export data/pollen.yaml to docs/data/pollen.json for runtime use.

Writes a deterministic JSON index so `docs/javascripts/vdh-pollentabel.js`
and MkDocs macros can resolve taxon info from the SoT.

Each exported taxon includes:
  - pollen_key, latin, dutch, family, shape, sculpture, ornamentation, aperture, size
  - monofloral_honey_page — optional docs-relative path when inferred from monoflorale markdown
  - display_width_px — round(max_um * 2.5) from YAML size strings, else 125 (50 µm default)
  - links — optional pollenx, tstebler, paldat URLs (YAML `links` overrides)
  - images[] — path, optional kind/source, width_px (per-image override or display_width_px)

Usage: python3 scripts/export_pollen_json.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from pollen_display import display_width_px_for_yaml_entry, merge_links_yaml_defaults, per_image_width_px

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
JSON_PATH = REPO / "docs" / "data" / "pollen.json"
MONOFLORAL_MD_DIR = REPO / "docs" / "monoflorale-honing-pollen"
BY_TAXON_REF_RE = re.compile(r"by-taxon/([a-z0-9_]+)/", re.I)


def _build_monofloral_primary_slug_map() -> Dict[str, str]:
    """pollen_key slug -> docs-relative path to monofloral honey page.

    Each ``*.md`` under ``docs/monoflorale-honing-pollen/`` (except ``_index.md``)
    is scanned for ``by-taxon/<slug>/`` image paths; the most frequent slug wins.
    First file in sorted path order wins if two pages share the same dominant slug.
    """
    out: Dict[str, str] = {}
    if not MONOFLORAL_MD_DIR.is_dir():
        return out
    for md_path in sorted(MONOFLORAL_MD_DIR.glob("*.md")):
        if md_path.name == "_index.md":
            continue
        text = md_path.read_text(encoding="utf-8")
        counts: Counter[str] = Counter(m.group(1) for m in BY_TAXON_REF_RE.finditer(text))
        if not counts:
            continue
        primary = counts.most_common(1)[0][0]
        rel = f"monoflorale-honing-pollen/{md_path.name}"
        out.setdefault(primary, rel)
    return out


def _clean_scalar(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s in ("", "-", "null", "None"):
            return None
        return s
    return v


def _build_entry(pollen_key_slug: str, src: Dict[str, Any]) -> Dict[str, Any]:
    """Build one JSON object keyed by pollen_key_slug elsewhere."""
    out: Dict[str, Any] = {}

    latin = _clean_scalar(src.get("latin"))
    dutch = _clean_scalar(src.get("dutch"))
    family = _clean_scalar(src.get("family"))

    out["pollen_key"] = pollen_key_slug

    if latin is not None:
        out["latin"] = latin
    if dutch is not None:
        out["dutch"] = dutch
    if family is not None:
        out["family"] = family

    for morph in ("shape", "sculpture", "ornamentation", "aperture"):
        mv = _clean_scalar(src.get(morph))
        if mv is not None:
            out[morph] = mv

    size_src = src.get("size") or {}
    if isinstance(size_src, dict):
        size_out: Dict[str, Any] = {}
        for key in ("smallest_size", "largest_size"):
            val = _clean_scalar(size_src.get(key))
            if val is not None:
                size_out[key] = val
        if size_out:
            out["size"] = size_out

    display_w = display_width_px_for_yaml_entry(src)
    out["display_width_px"] = display_w

    latin_s = latin if isinstance(latin, str) else ""
    merged = merge_links_yaml_defaults(latin_s, src.get("links"))
    links_out: Dict[str, str] = {}
    for lk, url in merged.items():
        if isinstance(url, str) and url.strip():
            links_out[lk] = url.strip()
    if links_out:
        out["links"] = links_out

    images_src = src.get("images")
    if isinstance(images_src, list) and images_src:
        images_out: List[Dict[str, Any]] = []
        for im in images_src:
            if not isinstance(im, dict):
                continue
            path = _clean_scalar(im.get("path"))
            if not path:
                continue
            item: Dict[str, Any] = {"path": str(path)}
            kind = _clean_scalar(im.get("kind"))
            source = _clean_scalar(im.get("source"))
            if kind is not None:
                item["kind"] = kind
            if source is not None:
                item["source"] = source
            wp = per_image_width_px(im, display_w)
            item["width_px"] = wp
            item["height_px"] = wp
            images_out.append(item)
        if images_out:
            out["images"] = images_out

    return out


def main() -> int:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Unexpected top-level YAML type: {type(data).__name__}")

    monofloral_pages = _build_monofloral_primary_slug_map()
    exported: Dict[str, Dict[str, Any]] = {}
    for key in sorted(data.keys()):
        entry = data.get(key)
        if not isinstance(entry, dict):
            continue
        built = _build_entry(str(key), entry)
        mf = monofloral_pages.get(str(key))
        if mf:
            built["monofloral_honey_page"] = mf
        exported[key] = built

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(exported, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH.relative_to(REPO)} ({len(exported)} entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
