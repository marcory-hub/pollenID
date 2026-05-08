from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

from extract_key_paths import render_paths_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
NL_DIR = DOCS_DIR / "nederlandse-honing-pollen"
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
    keys = re.findall(r'\{\{\s*pollen_gallery\(\s*"([^"]+)"\s*\)\s*\}\}', index_text)
    out: List[str] = []
    for k in keys:
        k = k.strip()
        if k and k not in out:
            out.append(k)
    return out


def _title(entry: Dict[str, Any], key: str) -> str:
    latin = str(entry.get("latin") or "").strip()
    dutch = str(entry.get("dutch") or "").strip()
    latin_txt = f"*{latin}*" if latin else f"*{key}*"
    if dutch:
        return f"# {latin_txt} ({dutch})"
    return f"# {latin_txt}"


def _iter_scalar_fields(entry: Dict[str, Any]) -> Iterable[Tuple[str, str]]:
    skip_top = {"images", "sources"}
    for k, v in entry.items():
        if k in skip_top:
            continue
        if isinstance(v, (str, int, float)) and str(v).strip():
            yield (k, str(v).strip())


def _format_size(entry: Dict[str, Any]) -> str:
    size = entry.get("size")
    if not isinstance(size, dict):
        return ""
    a = str(size.get("smallest_size") or "").strip()
    b = str(size.get("largest_size") or "").strip()
    if a and b and a != b:
        return f"{a}-{b}"
    return a or b


def _yaml_overview_table(entry: Dict[str, Any], key: str) -> str:
    rows: List[Tuple[str, str]] = []

    latin = str(entry.get("latin") or "").strip()
    dutch = str(entry.get("dutch") or "").strip()
    if latin:
        rows.append(("Latijn", latin))
    if dutch:
        rows.append(("Nederlands", dutch))

    fam = str(entry.get("family") or "").strip()
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
        val = str(entry.get(fld) or "").strip()
        if val:
            rows.append((label, val))

    bloei = entry.get("bloeitijd")
    if isinstance(bloei, dict):
        s = str(bloei.get("start") or "").strip()
        e = str(bloei.get("end") or "").strip()
        if s or e:
            rows.append(("Bloeitijd", f"{s}-{e}".strip("-")))

    nv = str(entry.get("nectar_value") or "").strip()
    if nv:
        rows.append(("Nectarwaarde", nv))
    pv = str(entry.get("pollen_value") or "").strip()
    if pv:
        rows.append(("Pollenwaarde", pv))
    fr = str(entry.get("frequency_in_honey") or "").strip()
    if fr:
        rows.append(("In honing", fr))

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
        "sculpture",
        "ornamentation",
        "bloeitijd",
        "nectar_value",
        "pollen_value",
        "frequency_in_honey",
        "links",
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
    parts.append('{{ pollen_gallery("' + key + '") }}')
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
        raise SystemExit("No pollen_gallery keys found in _index.md")

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

