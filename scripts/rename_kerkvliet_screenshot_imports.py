#!/usr/bin/env python3
"""Rename Schermafbeelding*.png files under docs/assets/images/by-taxon-kerkvliet/<slug>/.

Each matching file becomes <slug>_1.png, <slug>_2.png, … using the folder basename as slug
(e.g. calendula_officin/armeria_maritima_* under that folder).

macOS screenshots are often spelled with a Unicode soft hyphen (U+00AD) inside the word
(Scherm + U+00AD + afbeelding). That invisible character breaks a naive "schermafbeelding*"
prefix check; we strip U+00AD and common zero-width characters before matching.

Use --dry-run to preview without changing files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO / "docs" / "assets" / "images" / "by-taxon-kerkvliet"

# Dutch macOS default; allow optional overrides.
DEFAULT_PREFIX = "schermafbeelding"

# Finder often emits U+00AD between "Scherm" and "afbeelding". Strip that and ZW chars for matching only.
_REMOVE_FOR_SCREENSHOT_MATCH = dict.fromkeys(
    ord(c)
    for c in (
        "\u00ad",  # soft hyphen
        "\u200b",
        "\u200c",
        "\u200d",
        "\ufeff",  # BOM (if ever pasted into basename)
    )
)


def screenshot_compare_key(name: str) -> str:
    """Normalize basename for prefix matching (not for on-disk rename)."""
    base = Path(name).name
    return base.translate(_REMOVE_FOR_SCREENSHOT_MATCH).lower()


def is_screenshot_candidate(name: str, prefix_lc: str) -> bool:
    if Path(name).suffix.lower() != ".png":
        return False
    return screenshot_compare_key(name).startswith(prefix_lc)


def sorted_sources(files: List[Path], *, by_mtime: bool) -> List[Path]:
    if by_mtime:
        return sorted(files, key=lambda p: (p.stat().st_mtime_ns, p.name.lower()))
    return sorted(files, key=lambda p: p.name.lower())


def planned_destinations(slug: str, count: int) -> List[str]:
    return [f"{slug}_{i}.png" for i in range(1, count + 1)]


def process_folder(folder: Path, slug: str, *, prefix_lc: str, by_mtime: bool, dry_run: bool) -> int:
    if not folder.is_dir():
        return 0

    sources = sorted_sources(
        [p for p in folder.iterdir() if p.is_file() and is_screenshot_candidate(p.name, prefix_lc)],
        by_mtime=by_mtime,
    )
    if not sources:
        return 0

    n = len(sources)
    dest_names = planned_destinations(slug, n)
    dest_paths = [folder / dn for dn in dest_names]

    for dst in dest_paths:
        if dst.exists() and dst not in sources:
            print(
                f"skip {folder.relative_to(REPO)}: destination exists "
                f"and is not a screenshot being renamed — {dst.name}",
                file=sys.stderr,
            )
            return 0

    seq = ", ".join(f"{s.name}->{d.name}" for s, d in zip(sources, dest_paths))
    if dry_run:
        print(f"{folder.relative_to(REPO)} ({n}): {seq}")
        return n

    for i in range(n - 1, -1, -1):
        sources[i].rename(dest_paths[i])
    print(f"{folder.relative_to(REPO)}: renamed {n} file(s)")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Rename Schermafbeelding*.png imports to <slug>_N.png under by-taxon-kerkvliet."
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"staging root (default: {DEFAULT_ROOT.relative_to(REPO)})",
    )
    ap.add_argument(
        "--prefix",
        default=DEFAULT_PREFIX,
        help=f"filename prefix match, case-insensitive (default: {DEFAULT_PREFIX})",
    )
    ap.add_argument(
        "--sort",
        choices=("name", "mtime"),
        default="name",
        help="order screenshots before numbering (default: name)",
    )
    ap.add_argument("--dry-run", action="store_true", help="print planned renames only")
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print per-folder skip reasons when no screenshots matched but other .png files exist",
    )
    ap.add_argument(
        "--only-folder",
        type=str,
        default="",
        help="basename of a single subfolder to process (otherwise all children)",
    )
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    prefix_lc = str(args.prefix).strip().lower()
    if not prefix_lc:
        print("prefix must be non-empty", file=sys.stderr)
        return 2

    if not root.is_dir():
        print(f"root is not a directory: {root}", file=sys.stderr)
        return 2

    by_mtime = args.sort == "mtime"
    total = 0

    dirs = sorted([p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")])
    if args.only_folder.strip():
        one = root / args.only_folder.strip()
        if not one.is_dir():
            print(f"--only-folder does not exist: {one}", file=sys.stderr)
            return 2
        dirs = [one]

    for folder in dirs:
        slug = folder.name
        if slug.startswith("."):
            continue
        n = process_folder(folder, slug, prefix_lc=prefix_lc, by_mtime=by_mtime, dry_run=args.dry_run)
        total += n
        if (
            args.verbose
            and n == 0
            and folder.is_dir()
            and any(p.suffix.lower() == ".png" for p in folder.iterdir() if p.is_file())
        ):
            print(
                f"no match under {folder.relative_to(REPO)} (prefix '{prefix_lc}'); "
                f"first png name repr: {repr(next(p.name for p in sorted(folder.iterdir()) if p.is_file() and p.suffix.lower()=='.png'))}",
                file=sys.stderr,
            )

    if total == 0:
        print(
            "No matching screenshots. Expect Dutch macOS PNGs whose name spells Scherm(+optional U+00AD)afbeelding…png; "
            "default prefix matches after stripping invisible characters.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
