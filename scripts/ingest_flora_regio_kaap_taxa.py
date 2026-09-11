#!/usr/bin/env python3
"""Insert or refresh Delport flora-regio-kaap taxa in data/pollen.yaml.

Reads docs/keys/flora-regio-kaap/taxa-index.json and by-taxon PNGs.
New slugs get a full nested YAML skeleton; existing slugs only gain Delport
image paths (via sync) and a note_pollen attribution if missing.

Does not invent morphology. Atlas links are constructed from the Latin name
(Wiki / PalDat title form); HTTP status is not checked here. After ``--apply``,
runs ``fill_pollen_yaml_from_delport.py --apply`` unless ``--skip-fill``.

Examples::

    ./.venv/bin/python scripts/ingest_flora_regio_kaap_taxa.py --dry-run
    ./.venv/bin/python scripts/ingest_flora_regio_kaap_taxa.py --apply
    ./.venv/bin/python scripts/ingest_flora_regio_kaap_taxa.py --apply --skip-fill
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from ruamel.yaml import YAML as RuamelYAML
from ruamel.yaml.comments import CommentedMap

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "docs" / "keys" / "flora-regio-kaap" / "taxa-index.json"
YAML_PATH = REPO / "data" / "pollen.yaml"
SLUGS_PATH = REPO / "data" / "species_page_slugs.txt"
BY_TAXON = REPO / "docs" / "assets" / "images" / "by-taxon"
GALLERY = REPO / "docs" / "gallerie" / "gallery-non-eu.md"
FILL_SCRIPT = REPO / "scripts" / "fill_pollen_yaml_from_delport.py"

# Dutch vernaculars only for families already used elsewhere in this repo's YAML.
FAMILY_DUTCH = {
    "Amaranthaceae": "amarantenfamilie",
    "Anacardiaceae": "cashewbomenfamilie",
    "Apiaceae": "schermbloemenfamilie",
    "Apocynaceae": "oleanderfamilie",
    "Asparagaceae": "aspergefamilie",
    "Asphodelaceae": "affodilfamilie",
    "Asteraceae": "composietenfamilie",
    "Boraginaceae": "ruwbladigenfamilie",
    "Brassicaceae": "kruisbloemenfamilie",
    "Campanulaceae": "klokjesfamilie",
    "Caprifoliaceae": "kamperfoeliefamilie",
    "Caryophyllaceae": "anjerfamilie",
    "Convolvulaceae": "haagwindefamilie",
    "Cucurbitaceae": "komkommerfamilie",
    "Cyperaceae": "cypergrassenfamilie",
    "Droseraceae": "zonnedauwfamilie",
    "Ericaceae": "heidefamilie",
    "Fabaceae": "vlinderbloemenfamilie",
    "Lamiaceae": "lipbloemenfamilie",
    "Malvaceae": "kaasjeskruidfamilie",
    "Oleaceae": "olijffamilie",
    "Orchidaceae": "orchideeënfamilie",
    "Orobanchaceae": "bremraapfamilie",
    "Oxalidaceae": "klaverzuringfamilie",
    "Plumbaginaceae": "strandkruidfamilie",
    "Poaceae": "grassenfamilie",
    "Polygonaceae": "duizendknoopfamilie",
    "Rhamnaceae": "wegedoornfamilie",
    "Rosaceae": "rozenfamilie",
    "Rubiaceae": "sterbladigenfamilie",
    "Salicaceae": "wilgenfamilie",
    "Sapindaceae": "zeepboomfamilie",
    "Scrophulariaceae": "helmkruidfamilie",
    "Solanaceae": "nachtschadefamilie",
}


def wiki_title(latin: str) -> str:
    """Pollen-Wiki / PalDat title form (Genus_species or Genus_species_ssp._epithet)."""
    s = re.sub(r"\s+", " ", latin.replace("\n", " ")).strip()
    s = (
        s.replace(" ssp. ", "_ssp._")
        .replace(" subsp. ", "_subsp._")
        .replace(" var. ", "_var._")
        .replace(" cf. ", "_")
    )
    return s.replace(" ", "_")


def empty_entry(latin: str, family: Optional[str], plate: str, method: str) -> CommentedMap:
    genus = latin.split()[0] if latin else None
    title = wiki_title(latin)
    note = (
        f"Delport et al. 2025 GCFR atlas: plate {plate}; "
        f"processing {method} (A=acetolysed; NA,S=non-acetolysed stained)"
    )
    cm = CommentedMap()
    cm["name"] = CommentedMap(
        [("latin_name", latin), ("dutch_name", None)]
    )
    cm["classification"] = CommentedMap(
        [
            ("order", None),
            ("family_latin", family),
            ("family_dutch", FAMILY_DUTCH.get(family) if family else None),
            ("tribe", None),
            ("genus", genus),
        ]
    )
    cm["size"] = CommentedMap(
        [("size_smallest", None), ("size_largest", None), ("height_px", None)]
    )
    cm["pollen_class_beug"] = None
    cm["beug_key_paths"] = None
    cm["pollen_features"] = CommentedMap(
        [
            ("shape", None),
            ("sculpture", None),
            ("sculpture_visibility", None),
            ("aperture", None),
            ("aperture_visibility", None),
            ("ornamentation", None),
            ("ornamentation_visibility", None),
            ("polarity", None),
            ("pe_ratio", None),
            ("pollen-note", note),
        ]
    )
    cm["flowering_time"] = CommentedMap([("start", None), ("end", None)])
    cm["value"] = CommentedMap([("nectar_value", None), ("pollen_value", None)])
    cm["note"] = CommentedMap(
        [
            ("note_plant", None),
            ("note_honey", "Greater Cape Floristic Region (Delport et al. 2025)"),
            ("note_pollen", note),
        ]
    )
    cm["frequency_in_dutch_honey"] = None
    cm["frequency_in_eu_honey"] = None
    cm["frequency_in_non_eu_honey"] = None
    cm["learning_priority_rank"] = None
    cm["lookalikes"] = None
    cm["is_secondary_contributor"] = None
    cm["links"] = CommentedMap(
        [
            ("pollenX", "not in the database"),
            (
                "tstebler",
                f"https://pollen.tstebler.ch/MediaWiki/index.php?title={title}",
            ),
            ("paldat", f"https://www.paldat.org/pub/{title}"),
            (
                "waarneming",
                f"https://waarneming.nl/search/?q={latin.replace(' ', '+')}",
            ),
        ]
    )
    cm["images"] = []
    return cm


def collect_images(pollen_key: str) -> List[CommentedMap]:
    folder = BY_TAXON / pollen_key
    if not folder.is_dir():
        return []
    out: List[CommentedMap] = []
    for png in sorted(folder.glob("*.png"), key=lambda p: p.name.lower()):
        item = CommentedMap()
        item["path"] = f"assets/images/by-taxon/{pollen_key}/{png.name}"
        item["kind"] = "by_taxon"
        item["source"] = "by_taxon"
        out.append(item)
    return out


def merge_images(existing: Any, new_imgs: List[CommentedMap]) -> List[Any]:
    paths = set()
    merged: List[Any] = []
    if isinstance(existing, list):
        for it in existing:
            if isinstance(it, dict) and it.get("path"):
                paths.add(it["path"])
                merged.append(it)
    for it in new_imgs:
        if it["path"] not in paths:
            merged.append(it)
            paths.add(it["path"])
    return merged


def ensure_delport_note(entry: CommentedMap, plate: str, method: str) -> None:
    note = (
        f"Delport et al. 2025 GCFR atlas: plate {plate}; "
        f"processing {method} (A=acetolysed; NA,S=non-acetolysed stained)"
    )
    features = entry.get("pollen_features")
    if not isinstance(features, dict):
        features = CommentedMap()
        entry["pollen_features"] = features
    pn = features.get("pollen-note")
    if not pn:
        features["pollen-note"] = note
    elif "Delport" not in str(pn):
        features["pollen-note"] = f"{pn}; {note}"
    notes = entry.get("note")
    if not isinstance(notes, dict):
        notes = CommentedMap()
        entry["note"] = notes
    if not notes.get("note_honey"):
        notes["note_honey"] = "Greater Cape Floristic Region (Delport et al. 2025)"
    np = notes.get("note_pollen")
    if not np:
        notes["note_pollen"] = note
    elif "Delport" not in str(np):
        notes["note_pollen"] = f"{np}; {note}"


def unique_taxa(records: List[dict]) -> List[dict]:
    """One row per pollen_key; keep first plate, list all plates."""
    by_key: Dict[str, dict] = {}
    for rec in records:
        pk = rec["pollen_key"]
        if pk not in by_key:
            by_key[pk] = {
                **rec,
                "plates": [rec["plate"]],
            }
        else:
            by_key[pk]["plates"].append(rec["plate"])
    return list(by_key.values())


def update_gallery(taxa: List[dict]) -> str:
    """Rewrite gallery-non-eu.md: keep Coffea block, append Delport taxa."""
    lines = [
        "# Buiten EU",
        "",
        "| Label | Referentie | Opmerking |",
        "| :--- | :--- | :--- |",
        "| *Coffea* | [*Coffea arabica*](../pollen/species/coffea_arabica.md) | koffie; [koffiebloesemhoning](../monoflorale-honing-pollen/koffiebloesemhoning.md) |",
        "| Flora regio Kaap | [taxa-index](../keys/flora-regio-kaap/taxa-index.md) | Delport et al. 2025; Greater Cape Floristic Region |",
    ]
    # table rows for each unique key (sorted by latin)
    for rec in sorted(taxa, key=lambda r: r["latin_name"].lower()):
        pk = rec["pollen_key"]
        latin = rec["latin_name"]
        fam = rec.get("family_latin") or ""
        lines.append(
            f"| *{latin}* | [*{latin}*](../pollen/species/{pk}.md) | {fam}; Delport plate {', '.join(rec['plates'])} |"
        )
    lines += [
        "",
        "### *Coffea arabica* (koffie)",
        "",
        '{{ gallery("coffea_arabica") }}',
        "",
        "- Voorbeeld: *Coffea arabica* (koffie)",
        "- Familie: Rubiaceae (sterbladigenfamilie)",
        "",
        "### Flora regio Kaap (Delport et al. 2025)",
        "",
    ]
    for rec in sorted(taxa, key=lambda r: r["latin_name"].lower()):
        pk = rec["pollen_key"]
        latin = rec["latin_name"]
        fam = rec.get("family_latin") or ""
        fd = FAMILY_DUTCH.get(fam, "")
        fam_line = f"{fam}" + (f" ({fd})" if fd else "")
        lines.append(f"### *{latin}*")
        lines.append("")
        lines.append(f'{{{{ gallery("{pk}") }}}}')
        lines.append("")
        lines.append(f"- *{latin}*")
        if fam_line.strip():
            lines.append(f"- Familie: {fam_line}")
        lines.append(f"- Bronplaat: {', '.join(rec['plates'])} (Delport et al. 2025)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Write pollen.yaml, slugs, gallery")
    ap.add_argument("--dry-run", action="store_true", help="Report only (default if no --apply)")
    ap.add_argument("--skip-gallery", action="store_true")
    ap.add_argument(
        "--skip-fill",
        action="store_true",
        help="Do not run fill_pollen_yaml_from_delport.py after apply",
    )
    args = ap.parse_args()
    dry = not args.apply

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    records = index["taxa"]
    taxa = unique_taxa(records)

    ry = RuamelYAML()
    ry.preserve_quotes = True
    ry.default_flow_style = False
    ry.width = 100
    ry.indent(mapping=2, sequence=4, offset=2)
    data = ry.load(YAML_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("invalid pollen.yaml", file=sys.stderr)
        return 1

    created = 0
    updated = 0
    missing_imgs = 0
    for rec in taxa:
        pk = rec["pollen_key"]
        imgs = collect_images(pk)
        if not imgs:
            missing_imgs += 1
        if pk not in data:
            entry = empty_entry(
                rec["latin_name"],
                rec.get("family_latin"),
                ",".join(rec["plates"]),
                rec.get("method") or "",
            )
            entry["images"] = imgs
            data[pk] = entry
            created += 1
        else:
            entry = data[pk]
            if not isinstance(entry, dict):
                continue
            ensure_delport_note(entry, ",".join(rec["plates"]), rec.get("method") or "")
            entry["images"] = merge_images(entry.get("images"), imgs)
            # ensure family if empty
            clas = entry.get("classification")
            if isinstance(clas, dict) and not clas.get("family_latin") and rec.get("family_latin"):
                clas["family_latin"] = rec["family_latin"]
                if not clas.get("family_dutch"):
                    clas["family_dutch"] = FAMILY_DUTCH.get(rec["family_latin"])
            updated += 1

    # species_page_slugs
    slugs = []
    if SLUGS_PATH.is_file():
        slugs = [ln.strip() for ln in SLUGS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    slug_set = set(slugs)
    added_slugs = []
    for rec in taxa:
        pk = rec["pollen_key"]
        if pk not in slug_set:
            slugs.append(pk)
            slug_set.add(pk)
            added_slugs.append(pk)

    gallery_text = update_gallery(taxa)

    print(
        f"taxa={len(taxa)} created={created} updated={updated} "
        f"new_slugs={len(added_slugs)} missing_image_folders={missing_imgs}"
    )
    if dry:
        print("dry-run: no writes")
        return 0

    # Sort? Keep ruamel insertion order; new keys appended at end is OK for bulk.
    buf = ry.dump_to_string(data) if hasattr(ry, "dump_to_string") else None
    if buf is None:
        from io import StringIO

        stream = StringIO()
        ry.dump(data, stream)
        buf = stream.getvalue()
    YAML_PATH.write_text(buf, encoding="utf-8")
    SLUGS_PATH.write_text("\n".join(slugs) + "\n", encoding="utf-8")
    if not args.skip_gallery:
        GALLERY.write_text(gallery_text, encoding="utf-8")
    print(f"wrote {YAML_PATH}")
    print(f"wrote {SLUGS_PATH}")
    if not args.skip_gallery:
        print(f"wrote {GALLERY}")

    if not args.skip_fill and FILL_SCRIPT.is_file():
        cmd = [sys.executable, str(FILL_SCRIPT), "--apply"]
        print("running", " ".join(cmd))
        rc = subprocess.call(cmd, cwd=str(REPO))
        if rc != 0:
            print(f"fill_pollen_yaml_from_delport failed: {rc}", file=sys.stderr)
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
