#!/usr/bin/env python3
"""Lowercase basenames of bitmap/SVG files under docs/assets/images/ and fix path strings in repo files.

Skips docs/assets/manifests/ (regenerate with build_docs_data.py after YAML changes).
Skips docs/data/pollen.json (regenerate with export_pollen_json.py).

Usage:
  python3 scripts/lowercase_asset_image_files.py --dry-run
  python3 scripts/lowercase_asset_image_files.py --apply
"""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"
IMAGES_ROOT = DOCS / "assets" / "images"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
SKIP_UNDER_IMAGES_PARTS = frozenset({"manifests"})

SKIP_TOP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "site",
    "_build",
    "notes",
}


def iter_image_files() -> List[Path]:
    if not IMAGES_ROOT.is_dir():
        return []
    out: List[Path] = []
    for p in IMAGES_ROOT.rglob("*"):
        if not p.is_file():
            continue
        parts = set(p.parts)
        if "manifests" in parts:
            continue
        try:
            rel_to_img = p.relative_to(IMAGES_ROOT)
        except ValueError:
            continue
        if rel_to_img.parts and rel_to_img.parts[0] in SKIP_UNDER_IMAGES_PARTS:
            continue
        if p.suffix.lower() not in IMAGE_EXTS:
            continue
        out.append(p)
    out.sort(key=lambda x: x.as_posix().lower())
    return out


def docs_rel_posix(p: Path) -> str:
    return p.resolve().relative_to(DOCS.resolve()).as_posix()


def build_renames() -> List[Tuple[Path, Path]]:
    """Return list of (src, dst) where basename must become lowercase."""
    files = iter_image_files()
    # Detect basename collisions after lowercasing (same parent folder).
    by_key: Dict[Tuple[str, str], Path] = {}
    for p in files:
        parent = p.parent.resolve()
        low = p.name.lower()
        key = (str(parent), low)
        if key in by_key and by_key[key] != p:
            raise SystemExit(
                f"Collision: two files in {p.parent} lower to same name {low!r}:\n"
                f"  {by_key[key]}\n  {p}"
            )
        by_key[key] = p

    pairs: List[Tuple[Path, Path]] = []
    for p in files:
        new_name = p.name.lower()
        if p.name == new_name:
            continue
        dst = p.parent / new_name
        pairs.append((p, dst))
    return pairs


def physical_rename(src: Path, dst: Path) -> None:
    if src.resolve() == dst.resolve():
        return
    if not dst.exists():
        src.rename(dst)
        return
    if src.resolve() == dst.resolve():
        return
    # Same folder, case-only change on case-insensitive volume: two-step via temp.
    fd, tmp_name = tempfile.mkstemp(prefix=".lcimg_", suffix=src.suffix, dir=str(src.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        src.rename(tmp)
        tmp.rename(dst)
    except Exception:
        if tmp.exists():
            tmp.rename(src)
        raise


def replacement_pairs(pairs: List[Tuple[Path, Path]]) -> List[Tuple[str, str]]:
    """(old docs-relative path, new docs-relative path) longest first."""
    rep: List[Tuple[str, str]] = []
    for src, dst in pairs:
        rep.append((docs_rel_posix(src), docs_rel_posix(dst)))
    rep.sort(key=lambda x: len(x[0]), reverse=True)
    return rep


def iter_text_files_for_replace() -> Iterable[Path]:
    self_script = (REPO / "scripts" / "lowercase_asset_image_files.py").resolve()
    manifests = (DOCS / "assets" / "manifests").resolve()
    for dirpath, dirnames, filenames in os.walk(REPO, topdown=True):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_TOP_DIRS and (not d.startswith(".") or d == ".cursor")
        ]
        root = Path(dirpath)
        try:
            rel_root = root.relative_to(REPO)
        except ValueError:
            continue
        if rel_root.parts and rel_root.parts[0] in SKIP_TOP_DIRS:
            continue
        for name in filenames:
            suf = Path(name).suffix.lower()
            if suf not in {
                ".md",
                ".yaml",
                ".yml",
                ".json",
                ".js",
                ".css",
                ".html",
                ".htm",
                ".tsx",
                ".ts",
                ".txt",
                ".py",
                ".toml",
            }:
                continue
            fp = root / name
            try:
                rfp = fp.resolve()
            except OSError:
                continue
            if rfp == self_script:
                continue
            if rfp == manifests or manifests in rfp.parents:
                continue
            yield fp


def patch_file_contents(path: Path, reps: List[Tuple[str, str]]) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    orig = text

    # Also replace backslash-separated copies (unlikely but cheap).
    for old, new in reps:
        old_b = old.replace("/", "\\")
        new_b = new.replace("/", "\\")
        if old in text:
            text = text.replace(old, new)
        if old_b in text:
            text = text.replace(old_b, new_b)

    if text == orig:
        return False

    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true", dest="apply", help="rename files + patch refs")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply", file=__import__("sys").stderr)
        return 2

    pairs = build_renames()
    reps = replacement_pairs(pairs)
    print(f"Image files to rename (basename -> lowercase): {len(pairs)}")

    if args.dry_run:
        for src, dst in pairs[:40]:
            print(f"  {src.relative_to(REPO)} -> {dst.name}")
        if len(pairs) > 40:
            print(f"  ... and {len(pairs) - 40} more")
        print(f"Path replacement rules: {len(reps)}")
        return 0

    for src, dst in pairs:
        physical_rename(src, dst)

    changed = 0
    for fp in sorted(iter_text_files_for_replace(), key=lambda p: p.as_posix().lower()):
        if patch_file_contents(fp, reps):
            changed += 1
            print(f"patched {fp.relative_to(REPO)}")

    print(f"Renamed {len(pairs)} images; patched {changed} files.")
    print("Run: python3 scripts/export_pollen_json.py && python3 scripts/build_manifests.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
