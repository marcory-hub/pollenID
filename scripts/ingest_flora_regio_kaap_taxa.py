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


def _clean_gallery_val(v: Any) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    if s in ("", "-", "null", "None"):
        return ""
    return s


def _gallery_size_line(entry: Dict[str, Any], size_class: Optional[str]) -> str:
    from pollen_display import canonicalize_delport_size_class, entry_size_strings

    ss, ls = entry_size_strings(entry) if entry else (None, None)
    if ss and ls:
        if ss == ls:
            return ss
        small_num = re.sub(r"\s*µm$", "", ss, flags=re.I)
        return f"{small_num}-{ls}" if ls.lower().endswith("µm") else f"{small_num}-{ls} µm"
    if ss or ls:
        return ss or ls or ""
    cls = canonicalize_delport_size_class(size_class) if size_class else None
    labels = {
        "zeer klein": "zeer klein (<10 µm)",
        "klein": "klein (10-25 µm)",
        "middelgroot": "middelgroot (26-50 µm)",
        "groot": "groot (51-100 µm)",
        "zeer groot": "zeer groot (>100 µm)",
    }
    return labels.get(cls or "", "")


def _gallery_block_sort_key(item: Dict[str, Any]) -> Tuple[int, float, str]:
    from pollen_display import (
        _DELPORT_SIZE_CLASS_UM,
        canonicalize_delport_size_class,
        json_entry_size_sort_key,
        parse_max_um_from_size_strings,
    )

    grootte = item.get("grootte") or ""
    latin = (item.get("latin") or item.get("pk") or "").strip().lower()
    um = parse_max_um_from_size_strings(grootte, None) if grootte and "to be verified" not in grootte else None
    if um:
        return (0, um, latin)
    syn = {
        "size": item.get("size") or {},
        "pollen-note": item.get("pollen_note") or "",
        "latin": latin,
    }
    key = json_entry_size_sort_key(syn, latin)
    if key[0] == 0:
        return key
    cls = canonicalize_delport_size_class(item.get("size_class"))
    if cls:
        return (0, _DELPORT_SIZE_CLASS_UM[cls], latin)
    return (1, 0.0, latin)


def update_gallery(taxa: List[dict], yaml_data: Optional[Dict[str, Any]] = None) -> str:
    """Rewrite gallery-non-eu.md in easy-page format, sorted by size."""
    from fill_pollen_yaml_from_delport import collect_bundles
    from pollen_display import entry_dutch, entry_family, entry_feature, entry_latin

    data = yaml_data if isinstance(yaml_data, dict) else {}
    bundles = collect_bundles()
    tbv = "[to be verified]"
    items: List[Dict[str, Any]] = [
        {
            "pk": "coffea_arabica",
            "heading": "*Coffea arabica* (koffie)",
            "latin": "Coffea arabica",
        }
    ]
    for rec in taxa:
        pk = rec["pollen_key"]
        latin = rec["latin_name"]
        items.append({"pk": pk, "heading": f"*{latin}*", "latin": latin})

    blocks: List[Dict[str, Any]] = []
    for it in items:
        pk = it["pk"]
        entry = data.get(pk) if isinstance(data.get(pk), dict) else {}
        bundle = bundles.get(pk)
        aperture = _clean_gallery_val(entry_feature(entry, "aperture") if entry else None)
        shape = _clean_gallery_val(entry_feature(entry, "shape") if entry else None)
        sculpture = _clean_gallery_val(entry_feature(entry, "sculpture") if entry else None)
        size_class = getattr(bundle, "size_class", None) if bundle else None
        if bundle:
            if not aperture:
                aperture = _clean_gallery_val(getattr(bundle, "aperture", None))
            if not shape:
                shape = _clean_gallery_val(getattr(bundle, "shape", None))
            if not sculpture:
                sculpture = _clean_gallery_val(getattr(bundle, "sculpture", None))
        grootte = _gallery_size_line(entry, size_class)
        latin = (entry_latin(entry) if entry else None) or it["latin"]
        dutch = entry_dutch(entry) if entry else None
        voorbeeld = f"*{latin}*" + (f" ({dutch})" if dutch else "")
        familie = entry_family(entry) if entry else ""
        if not familie:
            fam = ""
            if isinstance(entry, dict):
                clas = entry.get("classification")
                if isinstance(clas, dict):
                    fam = _clean_gallery_val(clas.get("family_latin"))
            if not fam:
                rec = next((r for r in taxa if r.get("pollen_key") == pk), None)
                fam = (rec or {}).get("family_latin") or ""
            fd = FAMILY_DUTCH.get(fam, "")
            familie = f"{fam} ({fd})" if fam and fd else fam
        blocks.append(
            {
                **it,
                "grootte": grootte or tbv,
                "size": (entry or {}).get("size") or {},
                "pollen_note": entry_feature(entry, "pollen-note") if entry else "",
                "size_class": size_class,
                "aperture": aperture or tbv,
                "shape": shape or tbv,
                "sculpture": sculpture or tbv,
                "voorbeeld": voorbeeld,
                "familie": familie or tbv,
            }
        )
    blocks.sort(key=_gallery_block_sort_key)
    lines = ["# Buiten EU", ""]
    for b in blocks:
        lines += [
            f"### {b['heading']}",
            "",
            f'{{{{ gallery("{b["pk"]}") }}}}',
            "",
            f"- Pollenklasse: {b['aperture']}",
            f"- Vorm: {b['shape']}",
            f"- Grootte: {b['grootte']}",
            f"- Structuur: {b['sculpture']}",
            f"- Voorbeeld: {b['voorbeeld']}",
            f"- Familie: {b['familie']}",
            "",
        ]
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

    gallery_text = update_gallery(taxa, data)

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
