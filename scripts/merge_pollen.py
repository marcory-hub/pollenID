#!/usr/bin/env python3
from __future__ import annotations

"""
Usage (after running this script):

- Text field in Markdown:
  {{ pollen("taraxacum_officinale", "size.largest_size") }}

- YAML-backed gallery:
  {{ pollen_gallery("taraxacum_officinale") }}
- Height-scaled single image in Markdown:
  {{ pollen_img("taraxacum_officinale", "assets/images/by-taxon/taraxacum_officinale/taraxacum_officinale_4.png", alt="Taraxacum officinale") }}
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


RE_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
RE_SIZE_NUM = re.compile(r"(?P<num>\d+(?:[.,]\d+)?)\s*(?:[µμu]m)?", re.IGNORECASE)
RE_RANGE_SEP = re.compile(r"\s*(?:-|–|to|tot)\s*")


MONTHS_NL = {
    "januari": 1,
    "februari": 2,
    "maart": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "augustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "december": 12,
}


FIELD_ORDER = [
    "name",
    "classification",
    "size",
    "pollen_class_beug",
    "pollen_features",
    "flowering_time",
    "value",
    "note",
    "frequency_in_dutch_honey",
    "frequency_in_eu_honey",
    "frequency_in_non_eu_honey",
    "links",
    "images",
]


def _strip_md_links(s: str) -> str:
    return RE_MD_LINK.sub(r"\1", s).strip()


def _normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def latin_to_id(latin: str) -> str:
    latin = _strip_md_links(latin)
    latin = latin.replace("×", "x")
    latin = latin.strip()
    latin = re.sub(r"[()]", "", latin)
    latin = _normalize_spaces(latin)
    latin = latin.lower().replace(" ", "_")
    latin = re.sub(r"[^a-z0-9_]+", "_", latin)
    latin = re.sub(r"_+", "_", latin).strip("_")
    return latin


def _first_nonempty(*values: Optional[str]) -> Optional[str]:
    for v in values:
        if v is None:
            continue
        v2 = _normalize_spaces(str(v))
        if v2:
            return v2
    return None


def _parse_um_numbers(text: str) -> List[float]:
    nums: List[float] = []
    for m in RE_SIZE_NUM.finditer(text):
        raw = m.group("num").replace(",", ".")
        try:
            nums.append(float(raw))
        except ValueError:
            continue
    return nums


def parse_size_to_small_large(size_raw: str) -> Tuple[Optional[str], Optional[str], Optional[float]]:
    """
    Returns (smallest_size_str, largest_size_str, largest_um_float).
    Keep size strings human-readable, but expose numeric largest for height computation.
    """
    s0 = _normalize_spaces(size_raw.replace("μm", "µm"))
    # Many sources append citations after the size; restrict parsing to the size segment.
    cut = None
    idx = s0.lower().find("µm")
    if idx != -1:
        cut = idx + 2
    else:
        idx2 = s0.lower().find("um")
        if idx2 != -1:
            cut = idx2 + 2
    s = s0[:cut] if cut else s0
    s = _normalize_spaces(s.replace("um", "µm"))
    nums = _parse_um_numbers(s)
    if not nums:
        return (None, None, None)
    smallest = min(nums)
    largest = max(nums)
    smallest_str = f"{_format_um(smallest)}"
    largest_str = f"{_format_um(largest)}"
    return (smallest_str, largest_str, largest)


def _format_um(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return f"{int(round(value))} µm"
    return f"{value:.1f} µm"


def parse_bloom_months(text: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Best-effort parse for bloom month ranges.
    Accepts:
    - numeric ranges like '3-6' or '3 - 6'
    - Dutch month ranges like 'maart-juni'
    - single month like 'mei'
    """
    t = _normalize_spaces(text.lower())

    m = re.search(r"\b(1[0-2]|[1-9])\b\s*[-/]\s*\b(1[0-2]|[1-9])\b", t)
    if m:
        return (int(m.group(1)), int(m.group(2)))

    for name, num in MONTHS_NL.items():
        t = re.sub(rf"\b{name}\b", str(num), t)

    m2 = re.search(r"\b(1[0-2]|[1-9])\b\s*[-/]\s*\b(1[0-2]|[1-9])\b", t)
    if m2:
        return (int(m2.group(1)), int(m2.group(2)))

    m3 = re.search(r"\b(1[0-2]|[1-9])\b", t)
    if m3:
        n = int(m3.group(1))
        return (n, n)

    return (None, None)


def compute_height_px(largest_um: Optional[float]) -> Optional[int]:
    if largest_um is None:
        return None
    return int(round(largest_um * 2.5))


def _set_if_better(
    dst: Dict[str, Any],
    key: str,
    value: Any,
    conflicts: List[str],
    *,
    source_label: str,
) -> None:
    if value is None:
        return
    if isinstance(value, str) and not value.strip():
        return

    if key not in dst or dst[key] is None or dst[key] == "" or dst[key] == {}:
        dst[key] = value
        return

    if dst[key] == value:
        return

    conflicts.append(f"{source_label}: conflict field '{key}': keeping '{dst[key]}' over '{value}'")


def _init_entry() -> Dict[str, Any]:
    return {
        "name": {"latin_name": None, "dutch_name": None},
        "classification": {
            "order": None,
            "family_latin": None,
            "family_dutch": None,
            "tribe": None,
            "genus": None,
        },
        "size": {"size_smallest": None, "size_largest": None, "height_px": None},
        "pollen_class_beug": None,
        "pollen_features": {
            "shape": None,
            "sculpture": None,
            "sculpture_visibility": None,
            "aperture": None,
            "aperture_visibility": None,
            "ornamentation": None,
            "ornamentation_visibility": None,
            "polarity": None,
            "pe_ratio": None,
            "pollen-note": None,
        },
        "flowering_time": {"start": None, "end": None},
        "value": {"nectar_value": None, "pollen_value": None},
        "note": {"note_plant": None, "note_honey": None, "note_pollen": None},
        "frequency_in_dutch_honey": None,
        "frequency_in_eu_honey": None,
        "frequency_in_non_eu_honey": None,
        "links": {},
        "images": [],
    }


def _ordered_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    ordered: Dict[str, Any] = {}
    for k in FIELD_ORDER:
        ordered[k] = entry.get(k)
    return ordered


def _feat(entry: Dict[str, Any]) -> Dict[str, Any]:
    feats = entry.setdefault("pollen_features", {})
    if not isinstance(feats, dict):
        feats = {}
        entry["pollen_features"] = feats
    return feats


def merge_kerkvliet(path: Path, out: Dict[str, Dict[str, Any]], conflicts: List[str]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("rows", [])
    for row in rows:
        latin_raw = row.get("latin")
        if not latin_raw:
            continue
        latin = _normalize_spaces(_strip_md_links(str(latin_raw)))
        key = latin_to_id(latin)
        entry = out.setdefault(key, _init_entry())

        _set_if_better(entry["name"], "latin_name", latin, conflicts, source_label="kerkvliet")
        dutch = row.get("dutch")
        if dutch:
            _set_if_better(
                entry["name"],
                "dutch_name",
                _normalize_spaces(_strip_md_links(str(dutch))),
                conflicts,
                source_label="kerkvliet",
            )

        size_raw = row.get("grootte")
        if size_raw:
            smallest, largest, largest_um = parse_size_to_small_large(str(size_raw))
            _set_if_better(entry["size"], "size_smallest", smallest, conflicts, source_label="kerkvliet")
            _set_if_better(entry["size"], "size_largest", largest, conflicts, source_label="kerkvliet")
            if entry["size"].get("height_px") in (None, ""):
                entry["size"]["height_px"] = compute_height_px(largest_um)

        vorm = row.get("vorm")
        if vorm:
            _set_if_better(_feat(entry), "shape", _normalize_spaces(str(vorm)), conflicts, source_label="kerkvliet")

        oppervlak = row.get("oppervlak")
        if oppervlak:
            _set_if_better(
                _feat(entry),
                "ornamentation",
                _normalize_spaces(str(oppervlak)),
                conflicts,
                source_label="kerkvliet",
            )

        opmerkingen = row.get("opmerkingen")
        if opmerkingen:
            # best-effort: store the aperture phrase if present
            opm = _normalize_spaces(str(opmerkingen))
            m = re.search(r"\b(\d+)\s*-\s*(colporaat|colpaat|por(a|)aat|inaperturaat|tricolpaat|tricolporaat)\b", opm, re.IGNORECASE)
            if m:
                _set_if_better(_feat(entry), "aperture", m.group(0), conflicts, source_label="kerkvliet")


RE_LATIN_BINOMIAL = re.compile(r"\b([A-Z][a-z]+)\s+([a-z][a-z-]+)\b")


def _extract_latin_and_dutch_from_name(name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Endpoint names often look like:
    - 'Sanguisorba minor (kleine pimpernel)'
    - '[Onagraceae](...) (teunisbloemfamilie) - Epilobium ( ... )' (no binomial)
    """
    raw = _normalize_spaces(_strip_md_links(name))

    m = RE_LATIN_BINOMIAL.search(raw)
    latin = None
    if m:
        latin = f"{m.group(1)} {m.group(2)}"

    dutch = None
    m2 = re.search(r"\(([^)]+)\)\s*$", raw)
    if m2 and latin:
        dutch = _normalize_spaces(m2.group(1))

    return latin, dutch


def merge_vdh_style_key(path: Path, out: Dict[str, Dict[str, Any]], conflicts: List[str], *, source_label: str) -> None:
    """
    pollentabel style JSON: steps -> choices -> either 'next' or endpoint 'id' object.
    We only merge endpoints where a Latin binomial can be extracted.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    steps = data.get("steps", {})
    for step in steps.values():
        for choice in step.get("choices", []):
            endpoint = choice.get("id")
            if not isinstance(endpoint, dict):
                continue
            name = endpoint.get("name")
            if not name:
                continue

            latin, dutch = _extract_latin_and_dutch_from_name(str(name))
            if not latin:
                continue

            key = latin_to_id(latin)
            entry = out.setdefault(key, _init_entry())

            _set_if_better(entry["name"], "latin_name", latin, conflicts, source_label=source_label)
            _set_if_better(entry["name"], "dutch_name", dutch, conflicts, source_label=source_label)

            size_raw = endpoint.get("size")
            if size_raw and str(size_raw).strip() not in {"-", ""}:
                smallest, largest, largest_um = parse_size_to_small_large(str(size_raw))
                _set_if_better(entry["size"], "size_smallest", smallest, conflicts, source_label=source_label)
                _set_if_better(entry["size"], "size_largest", largest, conflicts, source_label=source_label)
                if entry["size"].get("height_px") in (None, ""):
                    entry["size"]["height_px"] = compute_height_px(largest_um)

            # Best-effort: use the choice label as a morphological hint if entry lacks it.
            label = choice.get("label")
            if isinstance(label, str):
                lab = label.lower()
                feats = _feat(entry)
                if feats.get("aperture") in (None, ""):
                    if any(k in lab for k in ["tricolpaat", "tricolporaat", "triporaat", "inaperturaat", "por"]):
                        _set_if_better(feats, "aperture", _normalize_spaces(label), conflicts, source_label=source_label)
                if feats.get("ornamentation") in (None, ""):
                    if any(k in lab for k in ["psilaat", "scabraat", "echinaat", "striaat", "reticulaat", "rugulaat"]):
                        _set_if_better(feats, "ornamentation", _normalize_spaces(label), conflicts, source_label=source_label)
                if feats.get("shape") in (None, ""):
                    if any(k in lab for k in ["oblaat", "prolaat", "globulair", "sferoid", "rond"]):
                        _set_if_better(feats, "shape", _normalize_spaces(label), conflicts, source_label=source_label)


def _extract_md_tables(md: str) -> Dict[str, str]:
    """
    Extract key-value pairs from Markdown tables of the form:
    | **Label** | Value |
    """
    kv: Dict[str, str] = {}
    for line in md.splitlines():
        line = line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        k = parts[0]
        v = parts[1]
        k = re.sub(r"[*_`]+", "", k).strip().lower()
        v = re.sub(r"\s+", " ", v).strip()
        if not k or not v:
            continue
        kv[k] = v
    return kv


def _extract_frequency_in_honey(md: str) -> Optional[str]:
    m = re.search(r"\bkomt voor in\s+(\d+(?:[.,]\d+)?)%\b", md, re.IGNORECASE)
    if not m:
        return None
    return f"{m.group(1).replace(',', '.')}%"


def merge_markdown_pages(base_dir: Path, pattern: str, out: Dict[str, Dict[str, Any]], conflicts: List[str], *, source: str) -> None:
    for path in sorted(base_dir.glob(pattern)):
        md = path.read_text(encoding="utf-8")

        latin = None
        h1 = next((ln.strip() for ln in md.splitlines() if ln.strip().startswith("# ")), None)
        if h1:
            # Examples:
            # "# paardenbloemhoning (Taraxacum officinale)"
            # "# *Calluna vulgaris* (struikheide)"
            m = re.search(r"\(([^)]+)\)", h1)
            if m:
                latin = m.group(1)
            else:
                m2 = re.search(r"\*\s*([^*]+?)\s*\*", h1)
                if m2:
                    latin = m2.group(1)

        if not latin:
            continue

        latin = _normalize_spaces(latin)
        key = latin_to_id(latin)
        entry = out.setdefault(key, _init_entry())

        _set_if_better(entry["name"], "latin_name", latin, conflicts, source_label=source)

        kv = _extract_md_tables(md)

        # Dutch common name is often in the H1 (second parentheses) but is inconsistent; prefer existing.
        # If there's an explicit 'nederlands' label in admonitions, we leave it for future parsing.

        size_val = kv.get("pollenkorrelgrootte") or kv.get("grootte (µm)") or kv.get("grootte (um)")
        if size_val:
            smallest, largest, largest_um = parse_size_to_small_large(size_val)
            _set_if_better(entry["size"], "size_smallest", smallest, conflicts, source_label=source)
            _set_if_better(entry["size"], "size_largest", largest, conflicts, source_label=source)
            if entry["size"].get("height_px") in (None, ""):
                entry["size"]["height_px"] = compute_height_px(largest_um)

        feats = _feat(entry)
        shape_val = kv.get("vorm")
        if shape_val:
            _set_if_better(feats, "shape", shape_val, conflicts, source_label=source)

        pol_val = kv.get("polariteit")
        if pol_val:
            _set_if_better(feats, "polarity", pol_val, conflicts, source_label=source)

        pe_val = kv.get("p/e-ratio") or kv.get("p/e ratio")
        if pe_val:
            _set_if_better(feats, "pe_ratio", pe_val, conflicts, source_label=source)

        ap_val = kv.get("aperturen") or kv.get("aperturen ")
        if ap_val:
            _set_if_better(feats, "aperture", ap_val, conflicts, source_label=source)

        orn_val = kv.get("ornamentatie") or kv.get("oppervlak")
        if orn_val:
            _set_if_better(feats, "ornamentation", orn_val, conflicts, source_label=source)

        bloom_val = kv.get("bloeitijd")  # Dutch source label from page tables
        if bloom_val:
            start, end = parse_bloom_months(bloom_val)
            _set_if_better(
                entry["flowering_time"], "start", start, conflicts, source_label=source
            )
            _set_if_better(
                entry["flowering_time"], "end", end, conflicts, source_label=source
            )

        freq = _extract_frequency_in_honey(md)
        if freq:
            _set_if_better(
                entry, "frequency_in_dutch_honey", freq, conflicts, source_label=source
            )


def write_yaml(path: Path, data: Dict[str, Dict[str, Any]]) -> None:
    sorted_keys = sorted(data.keys())
    ordered_top: Dict[str, Any] = {}
    for k in sorted_keys:
        ordered_top[k] = _ordered_entry(data[k])

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            ordered_top,
            f,
            sort_keys=False,
            allow_unicode=True,
            width=120,
            default_flow_style=False,
        )


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Merge project pollen data sources into data/pollen.yaml.",
    )
    p.add_argument("--out", default="data/pollen.yaml", help="Output YAML path (default: data/pollen.yaml).")
    p.add_argument(
        "--report",
        default=None,
        help="Optional path to write a conflict report (otherwise printed to stderr).",
    )
    args = p.parse_args(argv)

    conflicts: List[str] = []
    merged: Dict[str, Dict[str, Any]] = {}

    repo_root = Path(__file__).resolve().parents[1]
    kerkvliet = repo_root / "docs/keys/kerkvliet/kerkvliet-determinatietabel.json"
    if kerkvliet.exists():
        merge_kerkvliet(kerkvliet, merged, conflicts)
    else:
        conflicts.append(f"missing source: {kerkvliet}")

    merge_markdown_pages(repo_root / "docs/monoflorale-honing-pollen", "*.md", merged, conflicts, source="monoflorale_md")
    merge_markdown_pages(repo_root / "docs/pollen/species", "*.md", merged, conflicts, source="pollen_species_md")

    other_keys = [
        (repo_root / "docs/keys/eide/rosaceae-eide.json", "eide"),
        (repo_root / "docs/keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json", "feagri_iversen"),
        (repo_root / "docs/keys/vanderham/vanderham-pollentabel.json", "vanderham"),
    ]
    for path, label in other_keys:
        if not path.exists():
            conflicts.append(f"missing source: {path}")
            continue
        merge_vdh_style_key(path, merged, conflicts, source_label=label)

    out_path = repo_root / args.out
    write_yaml(out_path, merged)

    report_text = "\n".join(conflicts).strip() + ("\n" if conflicts else "")
    if args.report:
        report_path = repo_root / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
    else:
        if report_text:
            sys.stderr.write(report_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

