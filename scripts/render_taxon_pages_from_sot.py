from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

from extract_key_paths import render_paths_markdown
from pollen_display import (
    display_width_px_for_json_entry,
    entry_dutch,
    entry_family,
    entry_feature,
    entry_latin,
    entry_size_strings,
    entry_visibility,
    format_morph_with_visibility,
    per_image_width_px,
    resolve_pollen_field,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
NL_DIR = DOCS_DIR / "pollen" / "species"
POLLEN_YAML = REPO_ROOT / "data" / "pollen.yaml"
POLLEN_JSON = DOCS_DIR / "data" / "pollen.json"
TAXA_DETAIL_DIR = DOCS_DIR / "data" / "taxa"
SPECIES_SLUGS_FILE = REPO_ROOT / "data" / "species_page_slugs.txt"
INDEX_MD = NL_DIR / "_index.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load_pollen_yaml() -> Dict[str, Any]:
    return yaml.safe_load(_read_text(POLLEN_YAML)) or {}


def _load_display_index() -> Dict[str, Any]:
    if not POLLEN_JSON.is_file():
        return {}
    payload = json.loads(_read_text(POLLEN_JSON))
    return payload if isinstance(payload, dict) else {}


def _load_detail(slug: str) -> Optional[Dict[str, Any]]:
    path = TAXA_DETAIL_DIR / f"{slug}.json"
    if not path.is_file():
        return None
    payload = json.loads(_read_text(path))
    return payload if isinstance(payload, dict) else None


def _species_page_slugs() -> List[str]:
    """Slugs with a generated leaf page (manifest + any on-disk MD)."""
    slugs: set[str] = set()
    if SPECIES_SLUGS_FILE.is_file():
        for line in _read_text(SPECIES_SLUGS_FILE).splitlines():
            s = line.strip()
            if s and not s.startswith("#") and s != "_index":
                slugs.add(s)
    if NL_DIR.is_dir():
        for p in NL_DIR.glob("*.md"):
            if p.name != "_index.md":
                slugs.add(p.stem)
    return sorted(slugs)


def _extract_gallery_keys(index_text: str) -> List[str]:
    keys = re.findall(r'\{\{\s*gallery\(\s*"([^"]+)"\s*\)\s*\}\}', index_text)
    out: List[str] = []
    for k in keys:
        k = k.strip()
        if k and k not in out:
            out.append(k)
    return out


def _title_from_index(index_entry: Dict[str, Any], key: str) -> str:
    latin = index_entry.get("latin")
    dutch = index_entry.get("dutch")
    latin_s = latin.strip() if isinstance(latin, str) else key
    latin_txt = f"*{latin_s}*"
    if isinstance(dutch, str) and dutch.strip():
        return f"# {latin_txt} ({dutch.strip()})"
    return f"# {latin_txt}"


def _format_size_from_index(index_entry: Dict[str, Any]) -> str:
    size = index_entry.get("size")
    if not isinstance(size, dict):
        return ""
    a = str(size.get("smallest_size") or "").strip()
    b = str(size.get("largest_size") or "").strip()
    if a and b and a != b:
        return f"{a}-{b}"
    return a or b


def _iter_scalar_fields(entry: Dict[str, Any]) -> Iterable[Tuple[str, str]]:
    skip_top = {
        "images",
        "name",
        "classification",
        "pollen_features",
        "value",
        "note",
        "size",
        "links",
        "flowering_time",
    }
    for k, v in entry.items():
        if k in skip_top:
            continue
        if isinstance(v, (str, int, float)) and str(v).strip():
            yield (k, str(v).strip())


def _overview_table(
    key: str,
    index_entry: Dict[str, Any],
    yaml_entry: Dict[str, Any],
) -> str:
    rows: List[Tuple[str, str]] = []

    latin = index_entry.get("latin")
    if isinstance(latin, str) and latin.strip():
        rows.append(("Latijn", latin.strip()))
    dutch = index_entry.get("dutch")
    if isinstance(dutch, str) and dutch.strip():
        rows.append(("Nederlands", dutch.strip()))

    fam = index_entry.get("family")
    if isinstance(fam, str) and fam.strip():
        rows.append(("Familie", fam.strip()))
    elif yaml_entry:
        yfam = entry_family(yaml_entry) or ""
        if yfam:
            rows.append(("Familie", yfam))

    size = _format_size_from_index(index_entry)
    if size:
        rows.append(("Grootte", size))

    morph_map = [
        ("shape", "Vorm"),
        ("polarity", "Polariteit"),
        ("pe_ratio", "P/E"),
        ("aperture", "Apertuur"),
        ("sculpture", "Sculptuur"),
        ("ornamentation", "Ornamentatie"),
    ]
    for fld, label in morph_map:
        if fld in ("aperture", "sculpture", "ornamentation"):
            text = index_entry.get(fld)
            vis = index_entry.get(f"{fld}_visibility")
            val = format_morph_with_visibility(text, vis)
        elif yaml_entry and fld in ("polarity", "pe_ratio"):
            val = str(entry_feature(yaml_entry, fld) or "").strip()
        else:
            val = str(index_entry.get(fld) or "").strip()
        if val:
            rows.append((label, val))

    bloei = yaml_entry.get("flowering_time") if yaml_entry else None
    if isinstance(bloei, dict):
        s = str(bloei.get("start") or "").strip()
        e = str(bloei.get("end") or "").strip()
        if s or e:
            rows.append(("Bloeitijd", f"{s}-{e}".strip("-")))

    if yaml_entry:
        nv = str(resolve_pollen_field(yaml_entry, "nectar_value") or "").strip()
        if nv:
            rows.append(("Nectarwaarde", nv))
        pv = str(resolve_pollen_field(yaml_entry, "pollen_value") or "").strip()
        if pv:
            rows.append(("Pollenwaarde", pv))
        pnote = str(
            entry_feature(yaml_entry, "pollen-note")
            or entry_feature(yaml_entry, "pollen_note")
            or ""
        ).strip()
        if pnote:
            rows.append(("pollen-note", pnote))
        for freq_fld, freq_label in [
            ("frequency_in_dutch_honey", "Frequentie in NL-honing"),
            ("frequency_in_eu_honey", "Frequentie in EU-honing"),
            ("frequency_in_non_eu_honey", "Frequentie in niet-EU-honing"),
        ]:
            fr = str(yaml_entry.get(freq_fld) or "").strip()
            if fr:
                rows.append((freq_label, fr))

        note = yaml_entry.get("note")
        if isinstance(note, dict):
            for nk, nlbl in [
                ("note_plant", "Plantnotitie"),
                ("note_honey", "Honingnotitie"),
                ("note_pollen", "Pollennotitie"),
            ]:
                nv2 = str(note.get(nk) or "").strip()
                if nv2:
                    rows.append((nlbl, nv2))

        covered = {
            "latin",
            "dutch",
            "family",
            "size",
            "shape",
            "polarity",
            "pe_ratio",
            "aperture",
            "sculpture",
            "ornamentation",
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
        for k2, v2 in _iter_scalar_fields(yaml_entry):
            if k2 in covered:
                continue
            rows.append((k2, v2))

    if not rows:
        return ""

    out = ["| Veld | Waarde |", "|---|---|"]
    out.extend([f"| {a} | {b} |" for a, b in rows])
    return "\n".join(out)


def _static_gallery_html(key: str, index_entry: Dict[str, Any]) -> str:
    latin = index_entry.get("latin")
    latin_s = latin.strip() if isinstance(latin, str) else key
    default_w = display_width_px_for_json_entry(index_entry)
    imgs = index_entry.get("images")
    if not isinstance(imgs, list) or not imgs:
        return ""

    figures: List[str] = []
    for im in imgs:
        if not isinstance(im, dict):
            continue
        raw_path = im.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue
        canon = raw_path.strip().replace("\\", "/").lstrip("./")
        if not canon.startswith("assets/"):
            continue
        rel = "../../" + canon
        iw = per_image_width_px(im, default_w)
        fname = Path(canon).name
        safe_src = escape(rel, quote=True)
        safe_alt = escape(f"{latin_s} ({fname})", quote=True)
        style = f' style="width: {iw}px; height: auto;"' if iw > 0 else ""
        figures.append(
            f'<figure class="pid-scale-item"><img src="{safe_src}"{style} alt="{safe_alt}"></figure>'
        )

    if not figures:
        return ""

    inner = "".join(figures)
    return (
        '<div class="pid-scale-gallery">'
        '<div class="pid-scale-row pid-scale-row--snug">'
        f"{inner}"
        "</div></div>"
    )


def _links_section_from_detail(detail: Optional[Dict[str, Any]]) -> str:
    if not detail:
        return ""
    links = detail.get("links")
    if not isinstance(links, dict):
        return ""
    labels = (
        ("pollenx", "pollenX"),
        ("tstebler", "tstebler"),
        ("paldat", "paldat"),
        ("waarneming", "waarneming"),
    )
    items: List[str] = []
    for lk, label in labels:
        url = links.get(lk)
        if isinstance(url, str) and url.strip().startswith(("http://", "https://")):
            items.append(f"- {label}: {url.strip()}")
    if not items:
        return ""
    return "## Online databases\n\n" + "\n".join(items)


def _yaml_sot_block(key: str, entry: Dict[str, Any]) -> str:
    payload = {key: entry}
    dumped = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip()
    return "### SoT (`data/pollen.yaml`)\n\n```yaml\n" + dumped + "\n```"


def render_taxon_page_from_display(
    key: str,
    index_entry: Dict[str, Any],
    detail_entry: Optional[Dict[str, Any]],
    yaml_entry: Dict[str, Any],
) -> str:
    parts: List[str] = []
    parts.append(_title_from_index(index_entry, key))
    parts.append("")
    gallery = _static_gallery_html(key, index_entry)
    if gallery:
        parts.append(gallery)
    parts.append("")
    parts.append("## Kenmerken")
    parts.append("")
    table = _overview_table(key, index_entry, yaml_entry)
    if table:
        parts.append(table)
    else:
        parts.append("[to be verified]")
    parts.append("")
    if yaml_entry:
        parts.append(_yaml_sot_block(key, yaml_entry))
        parts.append("")
    parts.append("## Determinatiesleutels")
    parts.append("")
    parts.append(render_paths_markdown(key).strip() or "[to be verified]")
    parts.append("")
    links = _links_section_from_detail(detail_entry)
    if links:
        parts.append(links)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_taxon_page(key: str, entry: Dict[str, Any]) -> str:
    """Legacy YAML+macro render for add_taxon --render-pages when index missing."""
    latin = entry_latin(entry) or ""
    dutch = entry_dutch(entry) or ""
    latin_txt = f"*{latin}*" if latin else f"*{key}*"
    title = f"# {latin_txt} ({dutch})" if dutch else f"# {latin_txt}"
    idx_stub = {"latin": latin, "dutch": dutch}
    parts = [
        title,
        "",
        f'{{{{ gallery("{key}") }}}}',
        "",
        "## Kenmerken",
        "",
        _overview_table(key, idx_stub, entry) or "[to be verified]",
        "",
        _yaml_sot_block(key, entry),
        "",
        "## Determinatiesleutels",
        "",
        render_paths_markdown(key).strip() or "[to be verified]",
        "",
    ]
    detail = _load_detail(key)
    links = _links_section_from_detail(detail)
    if links:
        parts.append(links)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def build_all_species_pages() -> int:
    """Regenerate docs/pollen/species/<slug>.md for every existing species stem."""
    index = _load_display_index()
    yaml_data = _load_pollen_yaml()
    slugs = _species_page_slugs()
    if not slugs:
        print("No species pages to regenerate.")
        return 0

    missing_index: List[str] = []
    written = 0
    for slug in slugs:
        idx_entry = index.get(slug)
        if not isinstance(idx_entry, dict):
            missing_index.append(slug)
            continue
        yaml_entry = yaml_data.get(slug)
        if not isinstance(yaml_entry, dict):
            yaml_entry = {}
        detail = _load_detail(slug)
        md_path = NL_DIR / f"{slug}.md"
        _write_text(
            md_path,
            render_taxon_page_from_display(slug, idx_entry, detail, yaml_entry),
        )
        written += 1

    print(f"Regenerated {written} species pages under docs/pollen/species/.")
    if missing_index:
        print(
            f"Warning: {len(missing_index)} slugs missing from pollen.json index "
            f"(first: {missing_index[:5]})"
        )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--build-all-species",
        action="store_true",
        help="Regenerate all existing docs/pollen/species/<slug>.md from display JSON",
    )
    args = ap.parse_args()

    if args.build_all_species:
        return build_all_species_pages()

    pollen = _load_pollen_yaml()
    idx = _read_text(INDEX_MD)
    keys = _extract_gallery_keys(idx)
    if not keys:
        raise SystemExit("No gallery keys found in _index.md")

    display_index = _load_display_index()
    missing: List[str] = []
    for k in keys:
        entry = pollen.get(k)
        if not isinstance(entry, dict):
            missing.append(k)
            continue
        idx_entry = display_index.get(k)
        if isinstance(idx_entry, dict):
            detail = _load_detail(k)
            md_path = NL_DIR / f"{k}.md"
            _write_text(
                md_path,
                render_taxon_page_from_display(k, idx_entry, detail, entry),
            )
        else:
            md_path = NL_DIR / f"{k}.md"
            _write_text(md_path, render_taxon_page(k, entry))

    if missing:
        raise SystemExit(f"Missing {len(missing)} keys in pollen.yaml: {missing[:30]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
