#!/usr/bin/env python3
"""Align docs/keys/beug/*.json names with Identificatiesleutels/beug*.md stems.

Phase 1: move sources to unique temp names. Phase 2: move temps to final names.
Deletes any .json in docs/keys/beug/ not in the final kept set (after renames).
On --apply, rewrites data-json-url in wired beug*.md files after renames.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENT = ROOT / "docs" / "Identificatiesleutels"
BEUG = ROOT / "docs" / "keys" / "beug"

URL_RE = re.compile(r'data-json-url="\.\./\.\./keys/beug/([^"]+)"')


def target_json_basename(md_stem: str) -> str:
    if md_stem == "beug01-pollenklasse":
        return "beug-pollenklasse.json"
    if md_stem == "beug02-sculptuurtype":
        return "beug-sculptuurtype.json"
    return f"{md_stem}.json"


def collect_old_to_new() -> dict[str, str]:
    """Map current JSON basename -> target basename (one entry per wired MD page)."""
    old_to_new: dict[str, str] = {}
    for md in sorted(IDENT.glob("beug*.md")):
        text = md.read_text(encoding="utf-8")
        m = URL_RE.search(text)
        if not m:
            continue
        old = m.group(1)
        new = target_json_basename(md.stem)
        if old in old_to_new and old_to_new[old] != new:
            raise SystemExit(
                f"Conflict: {old!r} mapped to both {old_to_new[old]!r} and {new!r}"
            )
        old_to_new[old] = new
    return old_to_new


def apply_renames_and_delete(old_to_new: dict[str, str], *, dry_run: bool) -> None:
    final_basenames = set(old_to_new.values())
    renames = [(o, n) for o, n in old_to_new.items() if o != n]

    for old, new in renames:
        src = BEUG / old
        if not src.is_file():
            raise SystemExit(f"Missing source file: {src}")

    tmp_paths: list[tuple[Path, Path]] = []
    for i, (old, _) in enumerate(renames):
        src = BEUG / old
        tmp = BEUG / f".__beug_align_tmp_{i:03d}.json"
        tmp_paths.append((src, tmp))

    if dry_run:
        print("Would rename (phase 1 -> phase 2):")
        for old, new in renames:
            print(f"  {old} -> {new}")
        return

    for src, tmp in tmp_paths:
        src.rename(tmp)

    for i, (old, new) in enumerate(renames):
        tmp = BEUG / f".__beug_align_tmp_{i:03d}.json"
        dst = BEUG / new
        if dst.exists():
            raise SystemExit(f"Refusing to overwrite existing: {dst}")
        tmp.rename(dst)

    for p in sorted(BEUG.glob("*.json")):
        if p.name in final_basenames:
            continue
        p.unlink()

    leftover = list(BEUG.glob(".__beug_align_tmp_*.json"))
    if leftover:
        raise SystemExit(f"Leftover temp files: {leftover}")


def update_markdown_urls(old_to_new: dict[str, str], *, dry_run: bool) -> None:
    for md in sorted(IDENT.glob("beug*.md")):
        text = md.read_text(encoding="utf-8")
        new_text = text
        for old, new in old_to_new.items():
            old_url = f'../../keys/beug/{old}'
            new_url = f'../../keys/beug/{new}'
            new_text = new_text.replace(old_url, new_url)
        if new_text != text:
            if dry_run:
                print(f"Would update {md.name}")
            else:
                md.write_text(new_text, encoding="utf-8", newline="\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Perform renames and deletes (default is print plan only)",
    )
    args = ap.parse_args()
    dry_run = not args.apply

    old_to_new = collect_old_to_new()
    print(f"Wired pages: {len(old_to_new)}")
    renames = [(o, n) for o, n in old_to_new.items() if o != n]
    print(f"Renames needed: {len(renames)}")

    all_json = {p.name for p in BEUG.glob("*.json")}
    kept = set(old_to_new.keys())
    to_delete = sorted(all_json - kept)
    print(f"JSON files to delete after rename: {len(to_delete)}")

    if dry_run:
        apply_renames_and_delete(old_to_new, dry_run=True)
        update_markdown_urls(old_to_new, dry_run=True)
        return

    apply_renames_and_delete(old_to_new, dry_run=False)
    update_markdown_urls(old_to_new, dry_run=False)


if __name__ == "__main__":
    main()
