#!/usr/bin/env python3
"""
Append placeholder taxa to data/pollen.yaml for pollen slugs referenced in docs/keys
(Kerkvliet, van der Ham, Beug, overige sleutels) die nog niet in YAML staan.

Regels:
1) Elke niet-lege `pollen_key` string onder docs/keys/**/*.json wordt verzameld (recursief).
2) Kerkvliet-rijen ZONDER `pollen_key` maar mét `latin`: slug uit eerste deel vóór de komma
   (binomium of genus + eerste epitheton), geen VD/Beug-tekstparsing.

Daarna: python scripts/build_docs_data.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"
KEYS_DIR = ROOT / "docs" / "keys"

sys.path.insert(0, str(ROOT / "scripts"))
import merge_pollen as mp  # noqa: E402


def label_for_json(path: Path) -> str:
    rel = path.as_posix()
    if "/beug/" in rel:
        return "beug"
    if "kerkvliet-determinatietabel" in rel:
        return "kerkvliet"
    if "vanderham" in rel:
        return "vanderham"
    if "/reitsma/" in rel:
        return "reitsma"
    if "/eide/" in rel:
        return "eide"
    if "feagri-iversen" in rel:
        return "feagri-iversen"
    try:
        return path.relative_to(KEYS_DIR).parts[0]
    except ValueError:
        return "keys"


def abs_source_path(rel_posix: str) -> str:
    """Absolute path voor YAML sources-regel."""
    return (ROOT / rel_posix.strip("/")).resolve().as_posix()


def valid_slug(s: Optional[str]) -> Optional[str]:
    if not isinstance(s, str):
        return None
    t = mp._normalize_spaces(s)
    if not t or t in ("-", "null", "_"):
        return None
    if not re.match(r"^[a-z][a-z0-9_]*\Z", t):
        return None
    if len(t) < 2:
        return None
    return t


def collect_recursive_pollen_keys(obj: Any, out: Set[str]) -> None:
    if isinstance(obj, dict):
        pk = obj.get("pollen_key")
        vs = valid_slug(pk) if isinstance(pk, str) else None
        if vs:
            out.add(vs)
        for v in obj.values():
            collect_recursive_pollen_keys(v, out)
    elif isinstance(obj, list):
        for it in obj:
            collect_recursive_pollen_keys(it, out)


def latin_display_from_kerkrliet(latin_raw: str) -> str:
    seg = latin_raw.split(",")[0].strip()
    seg = mp._strip_md_links(seg)
    low = seg.lower()
    for token in (
        " pollenwiki",
        " paldat",
        " alleen em",
        " alleen sem",
    ):
        i = low.find(token)
        if i != -1:
            seg = seg[:i].strip()
            low = seg.lower()
    return mp._normalize_spaces(seg)


def slug_from_kerkrliet_latin_only(latin_raw: str) -> Optional[str]:
    """Alleen gebruikt als een Kerkvliet-rij geen pollen_key heeft."""
    if not isinstance(latin_raw, str):
        return None
    if "Bronscan" in latin_raw or "drukwerk" in latin_raw:
        return None
    s = latin_display_from_kerkrliet(latin_raw)
    if not s:
        return None
    parts = re.split(r"\s+", s)
    if len(parts) >= 2 and re.match(r"^[A-Z]", parts[0]) and parts[1].strip():
        epi = parts[1].split(";")[0].strip()
        if re.match(r"^[a-z0-9*-]+\Z", epi, re.I):
            slug = mp.latin_to_id(f"{parts[0]} {epi}")
            return valid_slug(slug)
    if len(parts) == 1 and re.match(r"^[A-Z]", parts[0]):
        slug = mp.latin_to_id(parts[0])
        return valid_slug(slug)
    return None


def iter_kerk_latin_fallback(data: Dict[str, Any]) -> Iterator[Tuple[str, str]]:
    rows = data.get("rows")
    sections = data.get("sections")
    if not isinstance(rows, list) or not isinstance(sections, list):
        return

    for row in rows:
        if not isinstance(row, dict):
            continue
        if valid_slug(row.get("pollen_key")):
            continue
        latin_raw = row.get("latin")
        if not isinstance(latin_raw, str):
            continue
        slug = slug_from_kerkrliet_latin_only(latin_raw)
        if slug:
            yield slug, latin_display_from_kerkrliet(latin_raw)


def latin_from_slug(slug: str) -> str:
    parts = slug.split("_")
    if len(parts) >= 2:
        return f"{parts[0].capitalize()} {parts[1].replace('_', ' ')}"
    return parts[0].capitalize() if parts else slug


@dataclass
class Pending:
    slug: str
    latin: str
    dutch: Optional[str]
    sources: Dict[str, Set[str]] = field(default_factory=dict)

    def add_sources(self, label: str, abs_paths: List[str]) -> None:
        b = self.sources.setdefault(label, set())
        b.update(abs_paths)


def nl_line(val: Optional[str]) -> str:
    if val is None:
        return ""
    s = mp._normalize_spaces(str(val))
    return s


def flatten_sources(p: Pending) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for lbl in sorted(p.sources.keys()):
        for frag in sorted(p.sources[lbl]):
            out.append((lbl, frag))
    return out


def format_placeholder_block(
    slug: str, latin: str, dutch: Optional[str], sources: List[Tuple[str, str]]
) -> str:
    dutch_yaml = nl_line(dutch)
    lat_esc = latin.replace('"', "'")
    sources_lines = [
        f"    - source: {lbl}\n      path: \n        {frag}" for lbl, frag in sorted(sources)
    ]
    sources_block = "\n".join(sources_lines)
    return (
        f"{slug}:\n"
        f"  latin: {lat_esc}\n"
        f"  dutch: {dutch_yaml}\n"
        f"  family:\n"
        f"  size:\n"
        f"    smallest_size:\n"
        f"    largest_size:\n"
        f"  shape:\n"
        f"  polarity:\n"
        f"  pe_ratio:\n"
        f"  aperture:\n"
        f"  ornamentation:\n"
        f"  image:\n"
        f"    height_px:\n"
        f"  bloeitijd:\n"
        f"    start:\n"
        f"    end:\n"
        f"  nectar_value:\n"
        f"  pollen_value:\n"
        f"  frequency_in_honey:\n"
        f"  sources:\n"
        f"{sources_block}\n"
    )


def collect_pending(existing: Set[str]) -> Dict[str, Pending]:
    pending: Dict[str, Pending] = {}

    def add(slug: str, latin: str, nl: Optional[str], label: str, path_abs: str) -> None:
        if slug in existing:
            return
        p = pending.get(slug)
        if p is None:
            pending[slug] = Pending(
                slug=slug,
                latin=latin or latin_from_slug(slug),
                dutch=nl,
            )
            p = pending[slug]
            p.add_sources(label, [path_abs])
        else:
            if latin and len(latin) >= len(p.latin):
                p.latin = latin
            if nl and not nl_line(p.dutch):
                p.dutch = nl
            p.add_sources(label, [path_abs])

    for jp in sorted(KEYS_DIR.rglob("*.json")):
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        rel = jp.relative_to(ROOT).as_posix()
        path_abs = abs_source_path(rel)
        label = label_for_json(jp)

        keys_here: Set[str] = set()
        collect_recursive_pollen_keys(data, keys_here)

        rows = data.get("rows")
        sections = data.get("sections")
        if isinstance(rows, list) and isinstance(sections, list):
            for row in rows:
                if isinstance(row, dict):
                    vn = row.get("dutch")
                    nl_clean = vn if isinstance(vn, str) and nl_line(vn) else None
                    pk_raw = row.get("pollen_key")
                    latin_raw = row.get("latin")

                    pv = valid_slug(pk_raw)
                    if pv:
                        latin_disp = latin_from_slug(pv)
                        if isinstance(latin_raw, str):
                            latin_disp = latin_display_from_kerkrliet(latin_raw)
                        add(pv, latin_disp, nl_clean, label, path_abs)
            for slug, lat_disp in iter_kerk_latin_fallback(data):
                add(slug, lat_disp, None, label, path_abs)

        else:
            for pk in sorted(keys_here):
                add(pk, latin_from_slug(pk), None, label, path_abs)

    return pending


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    import yaml

    current = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(current, dict):
        print("pollen.yaml: invalid root", file=sys.stderr)
        return 1

    existing = {k for k in current.keys() if isinstance(k, str)}
    pending_map = collect_pending(existing)

    if not pending_map:
        print("Geen ontbrekende sleuteltaxa.")
        return 0

    blocks = [format_placeholder_block(p.slug, p.latin, p.dutch, flatten_sources(p)) for p in (pending_map[s] for s in sorted(pending_map.keys()))]

    print(f"Nieuwe placeholdertaxa: {len(blocks)}", file=sys.stderr)
    if args.dry_run:
        for slug in sorted(pending_map.keys())[:45]:
            print(f"  {slug}", file=sys.stderr)
        if len(pending_map) > 45:
            print(f"  ... (+{len(pending_map) - 45})", file=sys.stderr)
        return 0

    sep = "\n# --- placeholders: toegevoegd vanuit docs/keys (aanvullen met data en afbeeldingen) ---\n\n"
    appendix = sep + "\n".join(blocks)
    txt = YAML_PATH.read_text(encoding="utf-8")
    if txt and not txt.endswith("\n"):
        appendix = "\n" + appendix

    YAML_PATH.write_text(txt + appendix, encoding="utf-8", newline="\n")

    print(f"Toegevoegd aan {YAML_PATH.relative_to(ROOT)}: {len(blocks)} blokken.")
    print("Voer uit: python scripts/build_docs_data.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
