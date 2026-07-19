from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

from extract_key_paths import render_paths_markdown
from pollen_display import (
    entry_dutch,
    entry_family,
    entry_feature,
    entry_latin,
    entry_size_strings,
    entry_visibility,
    format_morph_with_visibility,
    resolve_pollen_field,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
NL_DIR = DOCS_DIR / "pollen" / "species"
POLLEN_YAML = REPO_ROOT / "data" / "pollen.yaml"
INDEX_MD = NL_DIR / "_index.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load_pollen() -> Dict[str, Any]:
    return yaml.safe_load(_read_text(POLLEN_YAML)) or {}


def _extract_gallery_keys(index_text: str) -> List[str]:
    keys = re.findall(r'\{\{\s*gallery\(\s*"([^"]+)"\s*\)\s*\}\}', index_text)
    out: List[str] = []
    for k in keys:
        k = k.strip()
        if k and k not in out:
            out.append(k)
    return out


def _title(entry: Dict[str, Any], key: str) -> str:
    latin = entry_latin(entry) or ""
    dutch = entry_dutch(entry) or ""
    latin_txt = f"*{latin}*" if latin else f"*{key}*"
    if dutch:
        return f"# {latin_txt} ({dutch})"
    return f"# {latin_txt}"


def _iter_scalar_fields(entry: Dict[str, Any]) -> Iterable[Tuple[str, str]]:
    skip_top = {"images", "name", "classification", "pollen_features", "value", "note", "size", "links", "flowering_time"}
    for k, v in entry.items():
        if k in skip_top:
            continue
        if isinstance(v, (str, int, float)) and str(v).strip():
            yield (k, str(v).strip())


def _format_size(entry: Dict[str, Any]) -> str:
    a, b = entry_size_strings(entry)
    a = (a or "").strip()
    b = (b or "").strip()
    if a and b and a != b:
        return f"{a}-{b}"
    return a or b


def _yaml_overview_table(entry: Dict[str, Any], key: str) -> str:
    rows: List[Tuple[str, str]] = []

    latin = entry_latin(entry) or ""
    dutch = entry_dutch(entry) or ""
    if latin:
        rows.append(("Latijn", latin))
    if dutch:
        rows.append(("Nederlands", dutch))

    fam = entry_family(entry) or ""
    if fam:
        rows.append(("Familie", fam))

    size = _format_size(entry)
    if size:
        rows.append(("Grootte", size))

    for fld, label in [
        ("shape", "Vorm"),
        ("polarity", "Polariteit"),
        ("pe_ratio", "P/E"),
        ("aperture", "Apertuur"),
        ("sculpture", "Sculptuur"),
        ("ornamentation", "Ornamentatie"),
    ]:
        if fld in ("aperture", "sculpture", "ornamentation"):
            val = format_morph_with_visibility(
                entry_feature(entry, fld), entry_visibility(entry, fld)
            )
        else:
            val = str(entry_feature(entry, fld) or "").strip()
        if val:
            rows.append((label, val))

    bloei = entry.get("flowering_time")
    if isinstance(bloei, dict):
        s = str(bloei.get("start") or "").strip()
        e = str(bloei.get("end") or "").strip()
        if s or e:
            rows.append(("Bloeitijd", f"{s}-{e}".strip("-")))

    nv = str(resolve_pollen_field(entry, "nectar_value") or "").strip()
    if nv:
        rows.append(("Nectarwaarde", nv))
    pv = str(resolve_pollen_field(entry, "pollen_value") or "").strip()
    if pv:
        rows.append(("Pollenwaarde", pv))
    for freq_fld, freq_label in [
        ("frequency_in_dutch_honey", "Frequentie in NL-honing"),
        ("frequency_in_eu_honey", "Frequentie in EU-honing"),
        ("frequency_in_non_eu_honey", "Frequentie in niet-EU-honing"),
    ]:
        fr = str(entry.get(freq_fld) or "").strip()
        if fr:
            rows.append((freq_label, fr))

    note = entry.get("note")
    if isinstance(note, dict):
        for nk, nlbl in [
            ("note_plant", "Plantnotitie"),
            ("note_honey", "Honingnotitie"),
            ("note_pollen", "Pollennotitie"),
        ]:
            nv2 = str(note.get(nk) or "").strip()
            if nv2:
                rows.append((nlbl, nv2))

    # Append any remaining scalar fields not covered above
    covered = {
        "latin",
        "dutch",
        "family",
        "size",
        "shape",
        "polarity",
        "pe_ratio",
        "aperture",
        "aperture_visibility",
        "sculpture",
        "sculpture_visibility",
        "ornamentation",
        "ornamentation_visibility",
        "flowering_time",
        "nectar_value",
        "pollen_value",
        "frequency_in_dutch_honey",
        "frequency_in_eu_honey",
        "frequency_in_non_eu_honey",
        "links",
        "pollen_class_beug",
        "name",
        "classification",
        "pollen_features",
        "value",
        "note",
    }
    for k2, v2 in _iter_scalar_fields(entry):
        if k2 in covered:
            continue
        rows.append((k2, v2))

    if not rows:
        return ""

    # Tight markdown table
    out = ["| Veld | Waarde |", "|---|---|"]
    out.extend([f"| {a} | {b} |" for a, b in rows])
    return "\n".join(out)


def _links_section(entry: Dict[str, Any]) -> str:
    links = entry.get("links")
    if not isinstance(links, dict):
        return ""
    items: List[str] = []
    for k, v in links.items():
        if isinstance(v, str) and v.strip().startswith(("http://", "https://")):
            items.append(f"- {k}: {v.strip()}")
    if not items:
        return ""
    return "## Online databases\n\n" + "\n".join(items)

def _yaml_sot_block(key: str, entry: Dict[str, Any]) -> str:
    # Full SoT snapshot for this key, as stored in data/pollen.yaml.
    payload = {key: entry}
    dumped = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip()
    return "### SoT (`data/pollen.yaml`)\n\n```yaml\n" + dumped + "\n```"


def render_taxon_page(key: str, entry: Dict[str, Any]) -> str:
    parts: List[str] = []
    parts.append(_title(entry, key))
    parts.append("")
    parts.append('{{ gallery("' + key + '") }}')
    parts.append("")
    parts.append("## Kenmerken")
    parts.append("")
    table = _yaml_overview_table(entry, key)
    if table:
        parts.append(table)
    else:
        parts.append("[to be verified]")
    parts.append("")
    parts.append(_yaml_sot_block(key, entry))
    parts.append("")
    parts.append("## Determinatiesleutels")
    parts.append("")
    parts.append(render_paths_markdown(key).strip() or "[to be verified]")
    parts.append("")
    links = _links_section(entry)
    if links:
        parts.append(links)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    pollen = _load_pollen()
    idx = _read_text(INDEX_MD)
    keys = _extract_gallery_keys(idx)
    if not keys:
        raise SystemExit("No gallery keys found in _index.md")

    missing: List[str] = []
    for k in keys:
        entry = pollen.get(k)
        if not isinstance(entry, dict):
            missing.append(k)
            continue
        md_path = NL_DIR / f"{k}.md"
        _write_text(md_path, render_taxon_page(k, entry))

    if missing:
        raise SystemExit(f"Missing {len(missing)} keys in pollen.yaml: {missing[:30]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

