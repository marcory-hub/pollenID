#!/usr/bin/env python3
"""Append pollen.yaml placeholders and source markers from prio list, images, docs, keys."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"
PRIO_PATH = ROOT / "notes" / "pollenID" / "prio pollen.md"
BY_TAXON = ROOT / "docs" / "assets" / "images" / "by-taxon"
KEYS_DIR = ROOT / "docs" / "keys"

DOC_DIRS = (
    "docs/nederlandse-honing-pollen",
    "docs/secundaire-inbreng",
    "docs/sporadische-eu-pollen",
)

sys.path.insert(0, str(ROOT / "scripts"))
import merge_pollen as mp  # noqa: E402
from sync_placeholder_taxa_from_keys import (  # noqa: E402
    abs_source_path,
    collect_pending as collect_keys_pending,
    label_for_json,
    latin_from_slug,
    valid_slug,
)

PRIO_TYPO = {
    "Brassica-Typ": "brassicaceae",
    "Prunus-/Pirus-Typ": "prunus_pirus_typ",
    "Rubus-Typ": "rubus_fruticosus",
    "Taraxacum-Typ": "taraxacum_officinale",
    "Vicia-Typ": "vicia_typ",
    "Anthriscus-Typ": "anthriscus_typ",
    "Ranunculus-Typ": "ranunculus_typ",
    "Raphanus-Typ": "raphanus_typ",
    "Lamium-Typ": "lamium_typ",
    "Genista-Typ": "genista_typ",
    "Sinapis-Typ": "sinapis_typ",
    "Allium-Typ": "allium_typ",
    "Achillea-Typ": "achillea_typ",
    "Aster-Solidago-Typ": "aster_solidago_typ",
    "Serratula-Typ": "serratula_typ",
    "Crataegus-Typ": "crataegus_typ",
    "Asparagus-Typ": "asparagus_typ",
    "Majoranus-Typ": "majoranus_typ",
    "Heracleum-Typ": "heracleum_typ",
    "Centaurea-Typ": "centaurea_typ",
    "Polygonum-Typ": "polygonum_typ",
    "Centaurea jacea-Typ": "centaurea_jacea_typ",
    "Helianthus-Typ": "helianthus_typ",
}

PRIO_GENUS = {
    "Rhamnus": "frangula_alnus",
    "Aesculus": "aesculus_hippocastanum",
    "Robinia": "robinia_pseudoacacia",
    "Salix": "salix_caprea",
    "Echium": "echium_vulgare",
    "Tilia": "tilia_platyphyllos",
    "Parthenocissus": "parthenocissus_tricuspidata",
    "Verbascum": "verbascum_nigrum",
    "Lotus": "lotus_corniculatus",
    "Myosotis": "myosotis_scorpioides",
    "Phacelia": "phacelia_tanacetifolia",
    "Ligustrum": "ligustrum_vulgare",
    "Ailanthus": "ailanthus_altissima",
    "Melilotus": "melilotus_officinalis",
    "Ononis": "ononis_spinosa",
    "Spiraea": "spiraea_japonica",
    "Populus": "populus_nigra",
    "Castanea": "castanea_sativa",
    "Hedera": "hedera_helix",
    "Rhus": "rhus_typhina",
    "Anchusa": "anchusa_officinalis",
    "Filipendula": "filipendula_ulmaria",
    "Fagopyrum": "fagopyrum_esculentum",
    "Fragaria": "fragaria_vesca",
    "Symphytum": "symphytum_officinale",
    "Symphoricarpus": "symphoricarpos_albus",
    "Vaccinium": "vaccinium_myrtillus",
    "Epilobium": "epilobium_angustifolium",
    "Ribes": "ribes_rubrum",
    "Cynoglossum": "cynoglossum_officinale",
    "Tradescantia": "tradescantia_andersoniana",
    "Jasione": "jasione_montana",
    "Fraxinus": "fraxinus_excelsior",
    "Potentilla": "potentilla_anserina",
    "Violaceae": "viola_odorata",
    "Eleagnaceae": "elaeagnus_angustifolia",
    "Hydrangeaceae": "hydrangea_macrophylla",
    "Buddlejaceae": "buddleja_davidii",
    "Brassicaceae": "brassicaceae",
    "Rosaceae": "rosaceae",
}


@dataclass
class TaxonRef:
    slug: str
    latin: str = ""
    dutch: str = ""
    markers: Dict[str, str] = field(default_factory=dict)

    def add(self, marker: str, path: str, latin: str = "", dutch: str = "") -> None:
        if latin and (not self.latin or len(latin) > len(self.latin)):
            self.latin = latin
        if dutch and not self.dutch:
            self.dutch = dutch
        self.markers.setdefault(marker, path)


def slug_from_md(name: str) -> Optional[str]:
    if name.startswith("_") or name in ("index.md",):
        return None
    if not name.endswith(".md"):
        return None
    slug = name[:-3].replace("-", "_")
    return valid_slug(slug)


def parse_prio_item(raw: str) -> Tuple[str, str]:
    m = re.match(r"^(.+?)\s*\((.+)\)\s*$", raw.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return raw.strip(), ""


def prio_slug(label: str) -> Optional[str]:
    if label in PRIO_TYPO:
        return PRIO_TYPO[label]
    if label in PRIO_GENUS:
        return PRIO_GENUS[label]
    slug = valid_slug(mp.latin_to_id(label))
    return slug


def collect_prio(refs: Dict[str, TaxonRef]) -> None:
    if not PRIO_PATH.is_file():
        return
    text = PRIO_PATH.read_text(encoding="utf-8").split("---")[-1]
    path = PRIO_PATH.relative_to(ROOT).as_posix()
    for line in text.splitlines():
        m = re.match(r"\d+\.\s+(.+)", line.strip())
        if not m:
            continue
        label, dutch = parse_prio_item(m.group(1))
        slug = prio_slug(label)
        if not slug:
            continue
        latin = label if re.search(r"[A-Za-z]+\s+[a-z]", label) else latin_from_slug(slug)
        ref = refs.setdefault(slug, TaxonRef(slug=slug))
        ref.add("prio pollen", path, latin=latin, dutch=dutch)


def collect_by_taxon(refs: Dict[str, TaxonRef]) -> None:
    if not BY_TAXON.is_dir():
        return
    for folder in sorted(BY_TAXON.iterdir()):
        if not folder.is_dir():
            continue
        slug = valid_slug(folder.name)
        if not slug:
            continue
        pngs = sorted(p for p in folder.glob("*.png") if "placeholder" not in p.name.lower())
        if not pngs:
            continue
        path = f"assets/images/by-taxon/{slug}/"
        ref = refs.setdefault(slug, TaxonRef(slug=slug, latin=latin_from_slug(slug)))
        ref.add("image", path)


def collect_docs(refs: Dict[str, TaxonRef], rel_dir: str) -> None:
    marker = Path(rel_dir).name
    base = ROOT / rel_dir
    if not base.is_dir():
        return
    for md in sorted(base.glob("*.md")):
        slug = slug_from_md(md.name)
        if not slug:
            continue
        path = md.relative_to(ROOT).as_posix()
        ref = refs.setdefault(slug, TaxonRef(slug=slug, latin=latin_from_slug(slug)))
        ref.add(marker, path)


def collect_keys(refs: Dict[str, TaxonRef]) -> None:
    from sync_placeholder_taxa_from_keys import collect_recursive_pollen_keys

    pending_map = collect_keys_pending(set())
    for slug, item in pending_map.items():
        ref = refs.setdefault(slug, TaxonRef(slug=slug, latin=item.latin, dutch=item.dutch or ""))
        for lbl in item.sources:
            for frag in item.sources[lbl]:
                ref.add(lbl, frag, latin=item.latin, dutch=item.dutch or "")

    import json

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
        for slug in keys_here:
            ref = refs.setdefault(slug, TaxonRef(slug=slug, latin=latin_from_slug(slug)))
            ref.add(label, path_abs)


def yaml_scalar(s: str) -> str:
    s = mp._normalize_spaces(s or "")
    if not s:
        return ""
    if re.search(r"[:#\[\]{}&*?|>-]", s) or s.strip() != s:
        return '"' + s.replace('"', "'") + '"'
    return s


def format_canonical_block(ref: TaxonRef) -> str:
    latin = yaml_scalar(ref.latin or latin_from_slug(ref.slug))
    dutch = yaml_scalar(ref.dutch)
    sources_lines = [
        f"    - source: {marker}\n      path: {path}"
        for marker, path in sorted(ref.markers.items())
    ]
    sources_block = "\n".join(sources_lines)
    slug = ref.slug
    by_taxon = BY_TAXON / slug
    image_lines: List[str] = []
    if by_taxon.is_dir():
        for png in sorted(by_taxon.glob("*.png")):
            if "placeholder" in png.name.lower():
                continue
            rel = f"assets/images/by-taxon/{slug}/{png.name}"
            image_lines.append(
                f"    - path: {rel}\n      kind: by_taxon\n      source: by_taxon"
            )
    images_block = "\n".join(image_lines) if image_lines else "  images: []"
    if image_lines:
        images_block = "  images:\n" + images_block

    return (
        f"{slug}:\n"
        f"  latin: {latin}\n"
        f"  dutch: {dutch}\n"
        f"  family:\n"
        f"  size:\n"
        f"    smallest_size:\n"
        f"    largest_size:\n"
        f"    height_px:\n"
        f"  pollen_class:\n"
        f"  shape:\n"
        f"  sculpture:\n"
        f"  aperture:\n"
        f"  ornamentation:\n"
        f"  polarity:\n"
        f"  pe_ratio:\n"
        f"  pollen-note:\n"
        f"  bloeitijd:\n"
        f"    start:\n"
        f"    end:\n"
        f"  nectar_value:\n"
        f"  pollen_value:\n"
        f"  frequency_in_honey:\n"
        f"  links:\n"
        f"    pollenX:\n"
        f"    tstebler:\n"
        f"    paldat:\n"
        f"  sources:\n"
        f"{sources_block}\n"
        f"{images_block}\n"
    )


def source_entry_exists(block: str, marker: str, path: str) -> bool:
    needle = f"source: {marker}"
    if needle not in block:
        return False
    return path in block


def patch_existing_block(block: str, ref: TaxonRef) -> str:
    changed = False
    for marker, path in sorted(ref.markers.items()):
        if source_entry_exists(block, marker, path):
            continue
        entry = f"    - source: {marker}\n      path: {path}\n"
        if re.search(r"^  sources:\n", block, re.M):
            block = re.sub(
                r"(^  sources:\n(?:    - source:.*\n      path:.*\n)*)",
                lambda m: m.group(1) + entry,
                block,
                count=1,
                flags=re.M,
            )
        else:
            block = re.sub(
                r"(^  images:)",
                f"  sources:\n{entry}\\1",
                block,
                count=1,
                flags=re.M,
            )
        changed = True
    return block if changed else ""


def split_yaml_blocks(text: str) -> List[Tuple[str, str]]:
    lines = text.splitlines(keepends=True)
    blocks: List[Tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^[a-z][a-z0-9_]*:\s*$", line):
            key = line.split(":", 1)[0]
            start = i
            i += 1
            while i < len(lines) and not re.match(r"^[a-z][a-z0-9_]*:\s*$", lines[i]):
                if lines[i].startswith("# --- placeholders"):
                    break
                i += 1
            blocks.append((key, "".join(lines[start:i])))
        else:
            i += 1
    return blocks


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
    refs: Dict[str, TaxonRef] = {}

    collect_prio(refs)
    collect_by_taxon(refs)
    for rel in DOC_DIRS:
        collect_docs(refs, rel)
    collect_keys(refs)

    to_create = {s: r for s, r in refs.items() if s not in existing}
    to_mark = {s: r for s, r in refs.items() if s in existing}

    print(f"Bronnen: {len(refs)} slugs ({len(to_create)} nieuw, {len(to_mark)} bestaand markeren)", file=sys.stderr)
    if args.dry_run:
        for slug in sorted(to_create.keys())[:40]:
            print(f"  + {slug} [{', '.join(sorted(to_create[slug].markers))}]", file=sys.stderr)
        if len(to_create) > 40:
            print(f"  ... (+{len(to_create) - 40} nieuw)", file=sys.stderr)
        return 0

    text = YAML_PATH.read_text(encoding="utf-8")
    blocks = split_yaml_blocks(text)
    out_parts: List[str] = []
    prefix = text
    if blocks:
        prefix_end = text.find(blocks[0][1])
        prefix = text[:prefix_end]

    patched = 0
    for key, body in blocks:
        if key in to_mark:
            new_body = patch_existing_block(body, to_mark[key])
            if new_body:
                out_parts.append(new_body)
                patched += 1
            else:
                out_parts.append(body)
        else:
            out_parts.append(body)

    appendix_blocks = [format_canonical_block(to_create[s]) for s in sorted(to_create.keys())]
    sep = "\n# --- placeholders: prio pollen, images, docs, keys (aanvullen) ---\n\n"
    appendix = sep + "\n".join(appendix_blocks) if appendix_blocks else ""

    tail = re.search(r"\n# --- placeholders:.*", text, re.S)
    if tail:
        text = text[: tail.start()]
    if blocks:
        text = prefix + "".join(out_parts)
    text = text.rstrip("\n") + appendix
    if not text.endswith("\n"):
        text += "\n"

    YAML_PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"Toegevoegd: {len(appendix_blocks)} placeholders; gemarkeerd: {patched} bestaande.")
    print("Voer uit: .venv/bin/python scripts/build_docs_data.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
