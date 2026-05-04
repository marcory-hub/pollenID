#!/usr/bin/env python3
"""Append confidently mapped image files that are missing from data/pollen.yaml.

Uses the same stem resolution as scripts/audit_pollen_assets.py.
Skips assets/images/placeholder and files already under assets/images/by-taxon/.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from pollen_asset_lib import (
    DOCS_DIR,
    IMAGES_DIR,
    POLLEN_YAML,
    build_pollen_indexes,
    image_file_to_docs_path,
    is_under_by_taxon,
    iter_image_files,
    load_pollen_yaml_dict,
    normalize_image_stem,
    resolve_pollen_key_for_stem,
    yaml_image_paths,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def folder_kind_source(rel: str) -> tuple[str, str]:
    parts = rel.replace("\\", "/").split("/")
    if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "images":
        folder = parts[2]
        return folder, folder
    return "unknown", "unknown"


def collect_by_taxon_additions(data: dict) -> list[tuple[str, str, str, str]]:
    """PNG paths under assets/images/by-taxon/<pollen_key>/ when <pollen_key> is a YAML entry.

    MkDocs/Kerkvliet resolve thumbnails from pollen.json, which comes only from these lists;
    raster files alone are invisible until appended here."""
    root = DOCS_DIR / "assets" / "images" / "by-taxon"
    if not root.is_dir():
        return []
    additions: list[tuple[str, str, str, str]] = []
    for taxon_dir in sorted(root.iterdir()):
        if not taxon_dir.is_dir():
            continue
        pollen_key = taxon_dir.name
        if pollen_key not in data or not isinstance(data[pollen_key], dict):
            continue
        for png in sorted(taxon_dir.glob("*.png"), key=lambda p: p.name.lower()):
            rel = image_file_to_docs_path(png).replace("\\", "/")
            additions.append((pollen_key, rel, "by_taxon", "by_taxon"))
    return additions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--include-by-taxon",
        action="store_true",
        help="Also append PNGs under assets/images/by-taxon/<pollen_key>/ missing from YAML (folder name must match pollen key)",
    )
    ap.add_argument(
        "--only-by-taxon",
        action="store_true",
        help="Only append by-taxon/ PNGs (skip pollenwiki/paldat confident path scan)",
    )
    args = ap.parse_args()

    yload = YAML()
    yload.preserve_quotes = True
    yload.indent(mapping=2, sequence=4, offset=2)
    yload.allow_duplicate_keys = True

    data = yload.load(POLLEN_YAML.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("pollen.yaml top level must be mapping")

    slug_to_key, stem_to_keys = build_pollen_indexes(load_pollen_yaml_dict())

    additions: list[tuple[str, str, str, str]] = []  # key, path, kind, source

    if args.only_by_taxon:
        additions.extend(collect_by_taxon_additions(data))
    else:
        for p in iter_image_files(IMAGES_DIR):
            rel = image_file_to_docs_path(p).replace("\\", "/")
            low = rel.lower()
            if "placeholder" in low or "no_image_found" in low:
                continue
            if is_under_by_taxon(rel):
                continue

            stem = normalize_image_stem(p.stem)
            status, keys = resolve_pollen_key_for_stem(
                stem, stem_to_keys=stem_to_keys, slug_to_key=slug_to_key
            )
            if status != "confident" or len(keys) != 1:
                continue
            pollen_key = keys[0]
            entry = data.get(pollen_key)
            if not isinstance(entry, dict):
                continue

            seen = set(yaml_image_paths(entry))
            if rel in seen:
                continue

            kind, source = folder_kind_source(rel)
            additions.append((pollen_key, rel, kind, source))

        if args.include_by_taxon:
            additions.extend(collect_by_taxon_additions(data))

    if not additions:
        print("No confident image paths to add.")
        return 0

    by_key: dict[str, list[tuple[str, str, str]]] = {}
    for pk, rel, kind, source in additions:
        by_key.setdefault(pk, []).append((rel, kind, source))

    changed = 0
    for pollen_key, rows in sorted(by_key.items()):
        entry = data[pollen_key]
        assert isinstance(entry, dict)
        imgs = entry.get("images")
        if imgs is None:
            entry["images"] = []
            imgs = entry["images"]
        if not isinstance(imgs, list):
            continue
        existing = {p for p in yaml_image_paths(entry)}
        for rel, kind, source in sorted(rows, key=lambda t: t[0].lower()):
            if rel in existing:
                continue
            item = CommentedMap()
            item["path"] = rel
            item["kind"] = kind
            item["source"] = source
            imgs.append(item)
            existing.add(rel)
            changed += 1
            print(f"+ {pollen_key}: {rel}")

    if changed and not args.dry_run:
        with POLLEN_YAML.open("w", encoding="utf-8", newline="\n") as f:
            yload.dump(data, f)

    print(f"Added {changed} image entr(y/ies) across {len(by_key)} taxa (dry_run={args.dry_run})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
