#!/usr/bin/env python3
"""Fill images for *_typ pollen keys from genus-matching by-taxon folders.

For each pollen_key ending in ``_typ``, scans ``docs/assets/images/by-taxon/``
for species folders whose slug starts with the genus prefix (or hard-coded
double-genus prefixes). Selects up to 8 PNGs with balanced round-robin across
source species and image index, then shuffles deterministically (seed 42).

Writes the selected subset into ``data/pollen.yaml`` ``images`` lists.
Re-run after adding or removing by-taxon assets to refresh typ galleries.

Usage:
  ./.venv/bin/python scripts/fill_typ_images.py
  ./.venv/bin/python scripts/fill_typ_images.py --dry-run
"""

from __future__ import annotations

import argparse
import random
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from pollen_asset_lib import DOCS_DIR, POLLEN_YAML, image_file_to_docs_path

REPO = Path(__file__).resolve().parents[1]
BY_TAXON_DIR = DOCS_DIR / "assets" / "images" / "by-taxon"
MAX_IMAGES = 8
RNG_SEED = 42

# pollen_key -> folder slug prefixes (first path segment after by-taxon/)
DOUBLE_GENUS_PREFIXES: Dict[str, Tuple[str, ...]] = {
    "weigelia_diervilla_typ": ("weigela", "weigelia", "diervilla"),
    "aster_solidago_typ": ("aster", "solidago"),
    "prunus_pirus_typ": ("prunus", "pirus", "pyrus"),
}

_RE_IMAGE_NUM = re.compile(r"_(\d+)\.png$", re.IGNORECASE)


def _yaml_loader() -> YAML:
    yload = YAML()
    yload.preserve_quotes = True
    yload.indent(mapping=2, sequence=4, offset=2)
    yload.allow_duplicate_keys = True
    return yload


def genus_prefixes_for_typ(pollen_key: str) -> Tuple[str, ...]:
    """Return folder slug prefixes used to collect candidate images."""
    if pollen_key in DOUBLE_GENUS_PREFIXES:
        return DOUBLE_GENUS_PREFIXES[pollen_key]
    if not pollen_key.endswith("_typ"):
        return ()
    base = pollen_key[: -len("_typ")]
    parts = [p for p in base.split("_") if p]
    if not parts:
        return ()
    if len(parts) >= 2:
        return (parts[0], parts[1])
    return (parts[0],)


def folder_matches_prefixes(
    folder_name: str, prefixes: Sequence[str], typ_key: str
) -> bool:
    if folder_name.startswith("_") or folder_name == "_todo":
        return False
    if folder_name == typ_key:
        return True
    if folder_name.endswith("_typ"):
        return False
    for prefix in prefixes:
        if folder_name == prefix or folder_name.startswith(prefix + "_"):
            return True
    return False


def image_sort_key(path: Path) -> Tuple[int, str]:
    m = _RE_IMAGE_NUM.search(path.name)
    num = int(m.group(1)) if m else 10_000
    return (num, path.name.lower())


def collect_candidates(prefixes: Sequence[str], typ_key: str) -> Dict[str, List[str]]:
    """folder_name -> sorted docs-relative image paths."""
    out: Dict[str, List[str]] = defaultdict(list)
    if not BY_TAXON_DIR.is_dir():
        return out
    for taxon_dir in sorted(BY_TAXON_DIR.iterdir(), key=lambda p: p.name.lower()):
        if not taxon_dir.is_dir():
            continue
        folder = taxon_dir.name
        if not folder_matches_prefixes(folder, prefixes, typ_key):
            continue
        for png in sorted(taxon_dir.glob("*.png"), key=image_sort_key):
            rel = image_file_to_docs_path(png).replace("\\", "/")
            out[folder].append(rel)
    return dict(out)


def select_balanced(
    candidates_by_folder: Dict[str, List[str]], *, max_images: int
) -> List[str]:
    """Round-robin one image per species folder until max_images reached."""
    folders = sorted(candidates_by_folder.keys(), key=str.lower)
    if not folders:
        return []
    pools: Dict[str, List[str]] = {
        folder: list(paths) for folder, paths in candidates_by_folder.items()
    }
    selected: List[str] = []
    while len(selected) < max_images:
        progressed = False
        for folder in folders:
            if len(selected) >= max_images:
                break
            if pools[folder]:
                selected.append(pools[folder].pop(0))
                progressed = True
        if not progressed:
            break
    return selected


def build_image_items(paths: Sequence[str]) -> List[CommentedMap]:
    items: List[CommentedMap] = []
    for rel in paths:
        parts = rel.replace("\\", "/").split("/")
        folder = parts[3] if len(parts) >= 4 else "unknown"
        item = CommentedMap()
        item["path"] = rel
        item["kind"] = "atlas"
        item["source"] = folder
        items.append(item)
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Report without writing YAML")
    args = ap.parse_args()

    yload = _yaml_loader()
    data = yload.load(POLLEN_YAML.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("pollen.yaml top level must be mapping")

    typ_keys = sorted(k for k in data if isinstance(k, str) and k.endswith("_typ"))
    rng = random.Random(RNG_SEED)

    changed = 0
    filled = 0
    empty = 0

    for pollen_key in typ_keys:
        entry = data.get(pollen_key)
        if not isinstance(entry, dict):
            continue

        prefixes = genus_prefixes_for_typ(pollen_key)
        candidates = collect_candidates(prefixes, pollen_key)
        selected = select_balanced(candidates, max_images=MAX_IMAGES)
        rng.shuffle(selected)
        new_items = build_image_items(selected)

        old_count = 0
        old_imgs = entry.get("images")
        if isinstance(old_imgs, list):
            old_count = len(old_imgs)

        if old_count != len(new_items) or any(
            not isinstance(old_imgs, list)
            or i >= len(old_imgs)
            or not isinstance(old_imgs[i], dict)
            or old_imgs[i].get("path") != new_items[i]["path"]
            for i in range(len(new_items))
        ):
            entry["images"] = new_items
            changed += 1
            print(
                f"{pollen_key}: {old_count} -> {len(new_items)} images "
                f"({len(candidates)} source folders)"
            )

        if new_items:
            filled += 1
        else:
            empty += 1

    print(
        f"Typ taxa: {len(typ_keys)} total, {filled} with images, "
        f"{empty} still empty, {changed} entries updated "
        f"(dry_run={args.dry_run})"
    )

    if changed and not args.dry_run:
        with POLLEN_YAML.open("w", encoding="utf-8", newline="\n") as f:
            yload.dump(data, f)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
