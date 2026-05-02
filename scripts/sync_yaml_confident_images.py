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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
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
