#!/usr/bin/env python3
"""Export data/pollen.yaml to docs/data/pollen.json for runtime use.

Writes a deterministic JSON index so `docs/javascripts/pollentabel.js`
and MkDocs macros can resolve taxon info from the SoT.

Each exported taxon includes:
  - pollen_key, latin, dutch, family, shape, sculpture, ornamentation, aperture, size
  - optional polarity, pe_ratio, pollen-note (curated herkennen macro fields)
  - optional sculpture_visibility / aperture_visibility / ornamentation_visibility
    (lm_clear | lm_poor | em_only) when set in YAML
  - monofloral_honey_page — optional docs-relative path when inferred from monoflorale markdown
  - learning_priority_rank — optional int from YAML (Level 2 PalynoQuest priority)
  - controlled — optional coarse LM codes (sculptuur/apertuur/vorm/grootteband) for Kenmerken-drill
  - lookalikes — optional confirmed pairs + group slugs when set in YAML
  - has_taxon_page — true when monofloral_honey_page is set or slug is listed in
    data/species_page_slugs.txt (or a species MD exists on disk); false otherwise.
  - display_width_px — round(max_um * 2.5) from YAML size strings, else 125 (50 µm default)
  - images[] — path, optional kind/source, width_px (per-image override or display_width_px)

Atlas links (pollenx, tstebler, paldat, waarneming) are written to
``docs/data/taxa/<slug>.json`` (leaf/build detail), not the widget index.

Usage: python3 scripts/export_pollen_json.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from pollen_display import (
    display_width_px_for_yaml_entry,
    entry_dutch,
    entry_family,
    entry_feature,
    entry_latin,
    entry_size_strings,
    entry_visibility,
    merge_links_yaml_defaults,
    per_image_width_px,
)

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
JSON_PATH = REPO / "docs" / "data" / "pollen.json"
TAXA_DETAIL_DIR = REPO / "docs" / "data" / "taxa"
MONOFLORAL_MD_DIR = REPO / "docs" / "monoflorale-honing-pollen"
SPECIES_MD_DIR = REPO / "docs" / "pollen" / "species"
SPECIES_SLUGS_FILE = REPO / "data" / "species_page_slugs.txt"
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


def _species_page_slugs_set() -> set[str]:
    """pollen_key slugs listed in data/species_page_slugs.txt (+ any on-disk species MD)."""
    slugs: set[str] = set()
    if SPECIES_SLUGS_FILE.is_file():
        for line in SPECIES_SLUGS_FILE.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith("#") and s != "_index":
                slugs.add(s)
    if SPECIES_MD_DIR.is_dir():
        for p in SPECIES_MD_DIR.glob("*.md"):
            if p.name != "_index.md":
                slugs.add(p.stem)
    return slugs


def _clean_scalar(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s in ("", "-", "null", "None"):
            return None
        return s
    return v


def _build_links_detail(pollen_key_slug: str, src: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Per-slug detail payload (links only for now). None when empty."""
    latin = _clean_scalar(entry_latin(src))
    latin_s = latin if isinstance(latin, str) else ""
    merged = merge_links_yaml_defaults(latin_s, src.get("links"))
    links_out: Dict[str, str] = {}
    for lk, url in merged.items():
        if isinstance(url, str) and url.strip():
            links_out[lk] = url.strip()
    if not links_out:
        return None
    return {"pollen_key": pollen_key_slug, "links": links_out}


def _build_index_entry(
    pollen_key_slug: str, src: Dict[str, Any], species_slugs: set[str]
) -> Dict[str, Any]:
    """Build one widget-index JSON object (no links)."""
    out: Dict[str, Any] = {}

    latin = _clean_scalar(entry_latin(src))
    dutch = _clean_scalar(entry_dutch(src))
    family = _clean_scalar(entry_family(src))

    out["pollen_key"] = pollen_key_slug

    if latin is not None:
        out["latin"] = latin
    if dutch is not None:
        out["dutch"] = dutch
    if family is not None:
        out["family"] = family

    for morph in ("shape", "sculpture", "ornamentation", "aperture"):
        mv = _clean_scalar(entry_feature(src, morph))
        if mv is not None:
            out[morph] = mv

    for extra in ("polarity", "pe_ratio"):
        ev = _clean_scalar(entry_feature(src, extra))
        if ev is not None:
            out[extra] = ev

    pnote = _clean_scalar(
        entry_feature(src, "pollen-note") or entry_feature(src, "pollen_note")
    )
    if pnote is not None:
        out["pollen-note"] = pnote

    for vis in (
        "sculpture_visibility",
        "aperture_visibility",
        "ornamentation_visibility",
    ):
        vv = _clean_scalar(entry_visibility(src, vis.replace("_visibility", "")))
        if vv is not None:
            out[vis] = vv

    # Controlled LM codes for Kenmerken-drill (see data/feature_vocab.yaml).
    feats = src.get("pollen_features")
    if isinstance(feats, dict):
        controlled = feats.get("controlled")
        if isinstance(controlled, dict):
            ctrl_out: Dict[str, str] = {}
            for ck in ("sculptuur", "apertuur", "vorm", "grootteband", "source_slug"):
                cv = _clean_scalar(controlled.get(ck))
                if cv is not None:
                    ctrl_out[ck] = str(cv)
            if ctrl_out:
                out["controlled"] = ctrl_out

    ss, ls = entry_size_strings(src)
    size_out: Dict[str, Any] = {}
    if _clean_scalar(ss) is not None:
        size_out["smallest_size"] = _clean_scalar(ss)
    if _clean_scalar(ls) is not None:
        size_out["largest_size"] = _clean_scalar(ls)
    if size_out:
        out["size"] = size_out

    display_w = display_width_px_for_yaml_entry(src)
    out["display_width_px"] = display_w

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

    look = src.get("lookalikes")
    if isinstance(look, dict):
        la_out: Dict[str, Any] = {}
        pairs_src = look.get("pairs")
        if isinstance(pairs_src, list) and pairs_src:
            pairs_out: List[Dict[str, Any]] = []
            for item in pairs_src:
                if not isinstance(item, dict):
                    continue
                partner = _clean_scalar(item.get("partner"))
                status = _clean_scalar(item.get("status"))
                if not partner or status != "confirmed":
                    continue
                row: Dict[str, Any] = {"partner": str(partner), "status": "confirmed"}
                note = _clean_scalar(item.get("note"))
                if note is not None:
                    row["note"] = str(note)
                difficulty = _clean_scalar(item.get("difficulty"))
                if difficulty is not None:
                    row["difficulty"] = str(difficulty)
                pairs_out.append(row)
            if pairs_out:
                la_out["pairs"] = pairs_out
        groups_src = look.get("groups")
        if isinstance(groups_src, list) and groups_src:
            groups_out = [
                str(g).strip()
                for g in groups_src
                if isinstance(g, str) and g.strip()
            ]
            if groups_out:
                la_out["groups"] = groups_out
        if la_out:
            out["lookalikes"] = la_out

    return out


def main() -> int:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Unexpected top-level YAML type: {type(data).__name__}")

    monofloral_pages = _build_monofloral_primary_slug_map()
    species_slugs = _species_page_slugs_set()
    exported: Dict[str, Dict[str, Any]] = {}
    detail_count = 0
    if TAXA_DETAIL_DIR.is_dir():
        for old in TAXA_DETAIL_DIR.glob("*.json"):
            old.unlink()
    TAXA_DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    for key in sorted(data.keys()):
        entry = data.get(key)
        if not isinstance(entry, dict):
            continue
        slug = str(key)
        built = _build_index_entry(slug, entry, species_slugs)
        detail = _build_links_detail(slug, entry)
        if detail:
            detail_path = TAXA_DETAIL_DIR / f"{slug}.json"
            detail_path.write_text(
                json.dumps(detail, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                encoding="utf-8",
            )
            detail_count += 1
        mf = monofloral_pages.get(slug)
        if mf:
            built["monofloral_honey_page"] = mf
        rank = entry.get("learning_priority_rank")
        if isinstance(rank, int) and rank > 0:
            built["learning_priority_rank"] = rank
        elif isinstance(rank, str) and rank.strip().isdigit():
            built["learning_priority_rank"] = int(rank.strip())
        # Runtime taxon-page link resolution (pollentabel.js, kerkvliet-determinatietabel.js)
        # defaults to pollen/species/<pollen_key>.md when no monofloral page is set.
        # Flag entries with neither so the JS can skip the link instead of pointing at a 404.
        built["has_taxon_page"] = bool(mf) or slug in species_slugs
        exported[key] = built

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(exported, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH.relative_to(REPO)} ({len(exported)} entries).")
    print(f"Wrote {TAXA_DETAIL_DIR.relative_to(REPO)}/ ({detail_count} detail files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
