#!/usr/bin/env python3
"""Rename bitmap files under docs/assets/images/by-taxon/<slug>/ to <slug>_1.ext …

Only renames when at least one file does not already match ``<slug>_<n>.<ext>``.
Updates references in data/pollen.yaml and docs/**/*.md, docs/**/*.json.

Usage:
  python scripts/normalize_by_taxon_numeric_images.py --dry-run
  python scripts/normalize_by_taxon_numeric_images.py --apply
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

from pollen_asset_lib import DOCS_DIR, IMAGES_DIR, POLLEN_YAML, IMAGE_EXTS

BY_TAXON = IMAGES_DIR / "by-taxon"


def _image_sort_key(path: Path) -> Tuple[str, int, str]:
    """Stable natural order: trailing ``_123`` sorts numerically; else lexicographic stem."""
    stem = path.stem.lower()
    suf = path.suffix.lower()
    m = re.search(r"_(\d+)$", stem)
    if m:
        return (stem[: m.start()], int(m.group(1)), suf)
    return (stem, 0, suf)


def is_numeric_slug_file(slug: str, path: Path) -> bool:
    if path.suffix.lower() not in IMAGE_EXTS:
        return False
    stem = path.stem
    return bool(re.match(rf"^{re.escape(slug)}_\d+$", stem, re.IGNORECASE))


def plan_folder(slug: str, subdir: Path) -> Tuple[bool, List[Tuple[Path, Path]], List[Tuple[str, str]]]:
    """Return (needs_work, [(src_abs, dest_abs), ...], [(old_docs_rel, new_docs_rel), ...])."""
    files = sorted(
        [p for p in subdir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=_image_sort_key,
    )
    if not files:
        return False, [], []

    if all(is_numeric_slug_file(slug, p) for p in files):
        nums: List[int] = []
        ok = True
        for p in files:
            m = re.search(r"_(\d+)$", p.stem, re.IGNORECASE)
            if not m:
                ok = False
                break
            nums.append(int(m.group(1)))
        if ok and sorted(nums) == list(range(1, len(files) + 1)):
            return False, [], []

    moves: List[Tuple[Path, Path]] = []
    pairs: List[Tuple[str, str]] = []
    for i, src in enumerate(files, start=1):
        dest = subdir / f"{slug}_{i}{src.suffix.lower()}"
        if src.resolve() == dest.resolve():
            continue
        moves.append((src.resolve(), dest.resolve()))
        old_rel = f"assets/images/by-taxon/{slug}/{src.name}"
        new_rel = f"assets/images/by-taxon/{slug}/{dest.name}"
        pairs.append((old_rel.replace("\\", "/"), new_rel.replace("\\", "/")))
    return bool(moves), moves, pairs


def replacement_pairs_for_paths(old_rel: str, new_rel: str) -> List[Tuple[str, str]]:
    old_rel = old_rel.replace("\\", "/")
    new_rel = new_rel.replace("\\", "/")
    if old_rel == new_rel:
        return []
    o = old_rel
    n = new_rel
    return [
        (o, n),
        ("../" + o, "../" + n),
        ("../../" + o, "../../" + n),
    ]


def apply_filesystem_moves(moves: List[Tuple[Path, Path]]) -> None:
    """Two-phase rename within each parent directory."""
    by_parent: Dict[Path, List[Tuple[Path, Path]]] = {}
    for src, dest in moves:
        by_parent.setdefault(src.parent, []).append((src, dest))

    for parent, lst in by_parent.items():
        tmp_paths: List[Path] = []
        for i, (src, _dest) in enumerate(lst):
            tmp = parent / f".__pid_num_{i:05d}{src.suffix.lower()}"
            if tmp.exists():
                raise SystemExit(f"temp exists: {tmp}")
            src.rename(tmp)
            tmp_paths.append(tmp)
        for tmp, (_src, dest) in zip(tmp_paths, lst):
            if dest.exists() and tmp != dest:
                dest.unlink()
            tmp.rename(dest)


def rewrite_text_targets(all_subs: List[Tuple[str, str]]) -> int:
    changed_files = 0
    targets = [POLLEN_YAML]
    for pat in ("**/*.md", "**/*.json"):
        targets.extend(sorted(DOCS_DIR.glob(pat)))

    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        new_text = text
        for old, new in all_subs:
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            changed_files += 1
    return changed_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Rename files and rewrite references")
    ap.add_argument("--dry-run", action="store_true", help="Print planned changes only")
    args = ap.parse_args()
    dry = args.dry_run or not args.apply

    all_moves: List[Tuple[Path, Path]] = []
    all_pair_subs: List[Tuple[str, str]] = []

    if not BY_TAXON.is_dir():
        print("No by-taxon directory")
        return 0

    for subdir in sorted(BY_TAXON.iterdir(), key=lambda p: p.name.lower()):
        if not subdir.is_dir():
            continue
        slug = subdir.name
        needs, moves, pairs = plan_folder(slug, subdir)
        if not needs:
            continue
        print(f"{slug}: {len(moves)} renames")
        all_moves.extend(moves)
        for o, n in pairs:
            all_pair_subs.extend(replacement_pairs_for_paths(o, n))

    if not all_moves:
        print("Nothing to normalize.")
        return 0

    if dry:
        for o, n in all_pair_subs[:40]:
            print(f"  {o} -> {n}")
        if len(all_pair_subs) > 40:
            print(f"  ... and {len(all_pair_subs) - 40} more ref pairs")
        print(f"Dry-run: {len(all_moves)} files, {len(set(all_pair_subs))} unique substitutions")
        return 0

    apply_filesystem_moves(all_moves)
    uniq = list(dict.fromkeys(all_pair_subs))
    n = rewrite_text_targets(uniq)
    print(f"Applied {len(all_moves)} renames; updated {n} text files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
