#!/usr/bin/env python3
"""Refresh monofloral page pollen feature tables from data/pollen.yaml."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parents[1]
MONOFLORAL_MD_DIR = REPO / "docs" / "monoflorale-honing-pollen"
POLLEN_YAML_PATH = REPO / "data" / "pollen.yaml"

BY_TAXON_RE = re.compile(r"by-taxon/([a-z0-9_]+)/", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ATLAS_URL_RE = re.compile(
    r"\[([^\]]+)\]\((https?://(?:[^)]*pollenx\.eu|[^)]*pollen\.tstebler\.ch|[^)]*paldat\.org)[^)]*)\)",
    re.I,
)

REMOVE_HEADINGS = {
    "pollenkenmerken",
    "pollenafmeting en vorm",
    "vorm, afmeting en apertuur",
    "pollenklasse",
    "ornamentatie en structuur",
    "externe determinatiebronnen",
}

FALLBACK_PAGE_KEYS = {
    "lindehoning.md": "tilia_type_linde_species",
    "paardenbloemhoning.md": "taraxacum_officinale",
}

FIELDS = [
    ("Latijn", "latin"),
    ("Nederlands", "dutch"),
    ("Familie", "family"),
    ("Grootte", "size"),
    ("Vorm", "shape"),
    ("Sculptuur", "sculpture"),
    ("Apertuur", "aperture"),
    ("Ornamentatie", "ornamentation"),
    ("Polariteit", "polarity"),
    ("P/E-ratio", "pe_ratio"),
    ("Bloeitijd", "bloeitijd"),
    ("Nectarwaarde", "nectar_value"),
    ("Pollenwaarde", "pollen_value"),
    ("Frequentie in honing", "frequency_in_honey"),
    ("Links", "links"),
]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        stripped = value.strip()
        return "" if stripped in {"", "-", "None", "null"} else stripped
    return str(value).strip()


def _format_size(size: Any) -> str:
    if not isinstance(size, dict):
        return ""
    small = _clean(size.get("smallest_size"))
    large = _clean(size.get("largest_size"))
    if small and large:
        if small == large:
            return small
        small_num = re.sub(r"\s*µm$", "", small, flags=re.I)
        large_num = re.sub(r"\s*µm$", "", large, flags=re.I)
        return f"{small_num}-{large_num} µm"
    return small or large


def _format_bloeitijd(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    start = _clean(value.get("start"))
    end = _clean(value.get("end"))
    if start and end:
        return start if start == end else f"{start}-{end}"
    return start or end


def _format_links(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    labels = {
        "pollenx": "PollenX",
        "pollenX": "PollenX",
        "tstebler": "Pollen-Wiki",
        "paldat": "PalDat",
    }
    parts: list[str] = []
    seen: set[str] = set()
    for key in ("pollenx", "pollenX", "tstebler", "paldat"):
        url = _clean(value.get(key))
        if not url or url in seen:
            continue
        seen.add(url)
        parts.append(f"[{labels[key]}]({url})")
    return "<br>".join(parts)


def _format_value(entry: dict[str, Any], field: str) -> str:
    if field == "size":
        return _format_size(entry.get("size"))
    if field == "bloeitijd":
        return _format_bloeitijd(entry.get("bloeitijd"))
    if field == "links":
        return _format_links(entry.get("links"))
    return _clean(entry.get(field))


def _table_for_entry(entry: dict[str, Any]) -> str:
    rows = ["## Pollenkenmerken", "", "| Kenmerk | Waarde |", "| --- | --- |"]
    for label, field in FIELDS:
        value = _format_value(entry, field).replace("|", r"\|")
        rows.append(f"| **{label}** | {value} |")
    return "\n".join(rows)


def _heading_title(line: str) -> tuple[int, str] | None:
    match = HEADING_RE.match(line)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip().lower()


def _remove_generated_sections(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        heading = _heading_title(lines[i])
        if heading and heading[1] in REMOVE_HEADINGS:
            level = heading[0]
            i += 1
            while i < len(lines):
                next_heading = _heading_title(lines[i])
                if next_heading and next_heading[0] <= level:
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return out


def _strip_atlas_links(text: str) -> str:
    text = ATLAS_URL_RE.sub(r"\1", text)
    return re.sub(
        r"(?m)^\s*-\s*(?:\*\*)?(?:PollenX|Pollen-Wiki|PalDat)(?:\*\*)?:?\s*$\n?",
        "",
        text,
    )


def _insert_after_opening_gallery(lines: list[str], section: str) -> list[str]:
    insert_at = 1
    in_gallery = False
    depth = 0
    for idx, line in enumerate(lines[1:], start=1):
        stripped = line.strip()
        if stripped.startswith('<div class="pid-scale-gallery"'):
            in_gallery = True
            depth = 1
            continue
        if in_gallery:
            depth += stripped.count("<div")
            depth -= stripped.count("</div>")
            if depth <= 0:
                insert_at = idx + 1
                break
        elif stripped:
            insert_at = idx
            break

    return lines[:insert_at] + ["", section, ""] + lines[insert_at:]


def _primary_key_for_page(md_path: Path, text: str, pollen_data: dict[str, Any]) -> str | None:
    counts = Counter(BY_TAXON_RE.findall(text))
    for key, _count in counts.most_common():
        if key in pollen_data:
            return key
    fallback = FALLBACK_PAGE_KEYS.get(md_path.name)
    if fallback in pollen_data:
        return fallback
    return None


def update_page(md_path: Path, entry: dict[str, Any]) -> None:
    text = md_path.read_text(encoding="utf-8")
    text = _strip_atlas_links(text)
    lines = _remove_generated_sections(text.splitlines())
    lines = _insert_after_opening_gallery(lines, _table_for_entry(entry))
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    md_path.write_text(text, encoding="utf-8")


def main() -> int:
    pollen_data = yaml.safe_load(POLLEN_YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(pollen_data, dict):
        raise SystemExit(f"Unexpected YAML root type: {type(pollen_data).__name__}")

    changed = 0
    skipped: list[str] = []
    for md_path in sorted(MONOFLORAL_MD_DIR.glob("*.md")):
        if md_path.name == "_index.md":
            continue
        before = md_path.read_text(encoding="utf-8")
        key = _primary_key_for_page(md_path, before, pollen_data)
        entry = pollen_data.get(key) if key else None
        if isinstance(entry, dict):
            update_page(md_path, entry)
            changed += 1
        else:
            skipped.append(md_path.name)

    print(f"Updated {changed} monofloral pages.")
    if skipped:
        print("Skipped without pollen.yaml match: " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
