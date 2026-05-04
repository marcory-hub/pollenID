#!/usr/bin/env python3
"""Move confidently resolved bitmap images into assets/images/by-taxon/<pollen_key>/.

Rewrites paths in data/pollen.yaml, docs/**/*.md, and docs/**/*.json.
Use --dry-run first; then --apply.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

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
)

SKIP_NAME_SUBSTRINGS = ("placeholder", "no_image_found")


def should_skip_path(rel: str) -> bool:
    low = rel.lower()
    return any(s in low for s in SKIP_NAME_SUBSTRINGS)


def tail_after_assets_images(rel: str) -> str:
    rel = rel.replace("\\", "/").lstrip("./")
    prefix = "assets/images/"
    if not rel.startswith(prefix):
        return ""
    return rel[len(prefix) :]


def plan_moves() -> List[Tuple[Path, Path, str, str]]:
    """(src_abs, dest_abs, old_docs_rel, new_docs_rel)."""
    data = load_pollen_yaml_dict()
    slug_to_key, stem_to_keys = build_pollen_indexes(data)

    planned: List[Tuple[Path, Path, str, str]] = []
    dest_abs_seen: Dict[Tuple[str, str], Path] = {}

    for p in iter_image_files(IMAGES_DIR):
        old_rel = image_file_to_docs_path(p).replace("\\", "/")
        if should_skip_path(old_rel):
            continue
        if is_under_by_taxon(old_rel):
            continue

        stem = normalize_image_stem(p.stem)
        status, keys = resolve_pollen_key_for_stem(
            stem, stem_to_keys=stem_to_keys, slug_to_key=slug_to_key
        )
        if status != "confident" or len(keys) != 1:
            continue

        pollen_key = keys[0]
        basename = p.name
        dest_dir = IMAGES_DIR / "by-taxon" / pollen_key
        dest_abs = dest_dir / basename

        dup_key = (pollen_key, basename)
        other = dest_abs_seen.get(dup_key)
        if other is not None and other != p.resolve():
            basename = f"{p.parent.name}__{p.name}"
            dest_abs = dest_dir / basename
            dup_key = (pollen_key, basename)

        if dest_abs.exists() and dest_abs.resolve() != p.resolve():
            basename = f"{p.parent.name}__{p.name}"
            dest_abs = dest_dir / basename
            dup_key = (pollen_key, basename)

        dest_abs_seen[dup_key] = p.resolve()

        new_rel = f"assets/images/by-taxon/{pollen_key}/{basename}"
        planned.append((p.resolve(), dest_abs.resolve(), old_rel, new_rel))

    return planned


def replacement_pairs_for_old(old_rel: str, new_rel: str) -> List[Tuple[str, str]]:
    old_tail = tail_after_assets_images(old_rel)
    new_tail = tail_after_assets_images(new_rel)
    if not old_tail or not new_tail:
        return []
    pairs = [
        (f"assets/images/{old_tail}", f"assets/images/{new_tail}"),
        (f"../assets/images/{old_tail}", f"../assets/images/{new_tail}"),
        (f"../../assets/images/{old_tail}", f"../../assets/images/{new_tail}"),
    ]
    return pairs


def rewrite_text_paths(text: str, subs: List[Tuple[str, str]]) -> str:
    for old, new in subs:
        if old in text:
            text = text.replace(old, new)
    return text


def gather_text_targets() -> List[Path]:
    out: List[Path] = [POLLEN_YAML]
    for pat in ("**/*.md", "**/*.json"):
        out.extend(sorted(DOCS_DIR.glob(pat)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("Use only one of --apply or --dry-run")

    moves = plan_moves()
    if not moves:
        print("No moves planned.")
        return 0

    all_subs: List[Tuple[str, str]] = []
    for _src, _dst, old_rel, new_rel in moves:
        all_subs.extend(replacement_pairs_for_old(old_rel, new_rel))
    all_subs.sort(key=lambda t: len(t[0]), reverse=True)

    print(f"planned_moves={len(moves)} unique_subs={len(set(all_subs))}")
    if args.dry_run:
        for src, dst, old_r, new_r in moves[:15]:
            print(f"  {old_r} -> {new_r}")
        if len(moves) > 15:
            print(f"  ... and {len(moves) - 15} more")
        return 0

    if not args.apply:
        raise SystemExit("Specify --dry-run or --apply")

    for src, dst, old_r, new_r in moves:
        if src == dst:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        print(f"moved {old_r} -> {new_r}")

    changed = 0
    for path in gather_text_targets():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        new_text = rewrite_text_paths(text, all_subs)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            changed += 1
    print(f"rewrote_paths_in_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
