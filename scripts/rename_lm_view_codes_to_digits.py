#!/usr/bin/env python3
"""Rename palynological LM view suffixes on by-taxon rasters (ed,eo,pd,po,eo2,...) to _1,_2,... and fix path strings across the repo.

Only touches PNGs under docs/assets/images/by-taxon/.

Convention (longest suffix wins; optional size token _NN before extension is preserved):

  Ed/ed -> _1      Eo/eo -> _2      Pd/pd -> _3      Po/po -> _4
  Eo2/eo2 -> _5    Ed2/ed2 -> _6    Eo3/eo3 -> _7    Eo4/eo4 -> _8
  Pd2/pd2 -> _9    Po2/po2 -> _10   Po3/po3 -> _11   Em/em -> _12

Example: genus_species_ed_26.png -> genus_species_1_26.png

Skips manifests/ (regenerate build_manifests.py). Skips docs/data/pollen.json (export_pollen_json.py).

Usage:
  python3 scripts/rename_lm_view_codes_to_digits.py --dry-run
  python3 scripts/rename_lm_view_codes_to_digits.py --apply
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"
BY_TAXON = DOCS / "assets" / "images" / "by-taxon"

# Longest-first in alternation
_CODE_RE = re.compile(
    r"^(?P<base>.+)_(?P<code>eo4|eo3|eo2|ed2|eo|ed|pd2|pd|po3|po2|po|em)"
    r"(?P<size>_\d+)?\.png$",
    flags=re.IGNORECASE,
)

CODE_TO_DIGIT = {
    "ed": "1",
    "eo": "2",
    "pd": "3",
    "po": "4",
    "eo2": "5",
    "ed2": "6",
    "eo3": "7",
    "eo4": "8",
    "pd2": "9",
    "po2": "10",
    "po3": "11",
    "em": "12",
}

SKIP_TOP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "site",
    "_build",
    "notes",
}


def docs_rel_posix(p: Path) -> str:
    return p.resolve().relative_to(DOCS.resolve()).as_posix()


def proposed_name(lower_stem_png: str) -> str | None:
    """Input: filename only, lowercased, ending in .png. Output: full new basename or None."""
    m = _CODE_RE.match(lower_stem_png)
    if not m:
        return None
    code = m.group("code").lower()
    digit = CODE_TO_DIGIT.get(code)
    if not digit:
        return None
    size = m.group("size") or ""
    base = m.group("base").lower()
    return f"{base}_{digit}{size}.png"


def iter_by_taxon_pngs() -> List[Path]:
    if not BY_TAXON.is_dir():
        return []
    out = sorted(BY_TAXON.rglob("*.png"), key=lambda p: p.as_posix().lower())
    return out


def build_rename_pairs() -> List[Tuple[Path, Path]]:
    pairs: List[Tuple[Path, Path]] = []
    for src in iter_by_taxon_pngs():
        new_base = proposed_name(src.name.lower())
        if not new_base or new_base == src.name.lower():
            continue
        dst = src.with_name(new_base)
        pairs.append((src, dst))

    # Within each directory, ensure targets are unique.
    dir_to_pairs: Dict[Path, List[Tuple[Path, Path]]] = {}
    for s, d in pairs:
        dir_to_pairs.setdefault(s.parent.resolve(), []).append((s, d))

    validated: List[Tuple[Path, Path]] = []
    for parent, plist in sorted(dir_to_pairs.items(), key=lambda x: str(x[0]).lower()):
        tgt_count: Dict[str, int] = {}
        existing = {p.name.lower(): p for p in parent.glob("*.png")}
        for s, d in plist:
            key = d.name.lower()
            tgt_count[key] = tgt_count.get(key, 0) + 1
        dup = [k for k, v in tgt_count.items() if v > 1]
        if dup:
            raise SystemExit(f"Duplicate targets in {parent}: {dup!r}")

        for s, d in plist:
            dl = d.name.lower()
            if dl in existing and existing[dl].resolve() != s.resolve():
                raise SystemExit(
                    f"Target exists and blocks rename:\n"
                    f"  {s}\n"
                    f"  -> {d}\n"
                    f"  existing: {existing[dl]}"
                )
        validated.extend(plist)

    validated.sort(key=lambda x: x[0].as_posix().lower())
    return validated


def two_phase_bulk_rename(pairs: Sequence[Tuple[Path, Path]]) -> None:
    """Avoid intermediate collisions when A->B and B is occupied by another source."""
    by_dir: Dict[Path, List[Tuple[Path, Path]]] = {}
    for s, d in pairs:
        by_dir.setdefault(s.parent.resolve(), []).append((s, d))

    for parent, plist in sorted(by_dir.items(), key=lambda x: str(x[0]).lower()):
        tmps: List[Tuple[Path, Path]] = []
        for i, (s, d) in enumerate(plist):
            tmp = parent / f".lmv_step1_{i}_{s.name}"
            s.rename(tmp)
            tmps.append((tmp, d))
        for tmp, d in tmps:
            if tmp.resolve() == d.resolve():
                continue
            tmp.rename(d)


def replacement_pairs(pairs: List[Tuple[Path, Path]]) -> List[Tuple[str, str]]:
    rep: List[Tuple[str, str]] = []
    for src, dst in pairs:
        rep.append((docs_rel_posix(src), docs_rel_posix(dst)))
    rep.sort(key=lambda x: len(x[0]), reverse=True)
    return rep


def iter_text_files_for_replace() -> Iterable[Path]:
    self_script = (REPO / "scripts" / "rename_lm_view_codes_to_digits.py").resolve()
    manifests = (DOCS / "assets" / "manifests").resolve()
    pollen_json = (DOCS / "data" / "pollen.json").resolve()
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
            if rfp in {self_script, pollen_json} or rfp == manifests or manifests in rfp.parents:
                continue
            yield fp


def patch_file_contents(path: Path, reps: List[Tuple[str, str]]) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    orig = text

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

    pairs = build_rename_pairs()
    reps = replacement_pairs(pairs)
    print(f"by-taxon PNG renames (view code -> digit): {len(pairs)}")
    print(f"Path replacement rules: {len(reps)}")

    if args.dry_run:
        for src, dst in pairs[:50]:
            print(f"  {src.relative_to(REPO)} -> {dst.name}")
        if len(pairs) > 50:
            print(f"  ... and {len(pairs) - 50} more")
        return 0

    if pairs:
        two_phase_bulk_rename(pairs)

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
