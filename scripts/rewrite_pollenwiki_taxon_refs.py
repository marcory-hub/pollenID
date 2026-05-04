#!/usr/bin/env python3
"""Replace assets/images/pollenwiki/<taxon>.png references with first YAML by-taxon image.

Skips paths whose filename starts with ``placeholder_``. Does not move files.

Usage: python scripts/rewrite_pollenwiki_taxon_refs.py [--apply]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from pollen_asset_lib import (
    DOCS_DIR,
    POLLEN_YAML,
    build_pollen_indexes,
    normalize_image_stem,
    resolve_pollen_key_for_stem,
    yaml_image_paths,
)

REPO = Path(__file__).resolve().parents[1]

RE_REF = re.compile(r"((?:\.\./)*)(assets/images/pollenwiki/([^\"\'\s\)]+))")

# PollenWiki stems that do not match a by-taxon folder name.
KNOWN_FOLDER_ALIASES = {
    "erica_carnea": "erica_tetralix",
}


def disk_folder_key_for_pollenwiki(fname: str) -> Optional[str]:
    """Resolve ``by-taxon/<folder>/`` from a legacy pollenwiki filename."""
    s = Path(fname).stem.lower().replace("avallana", "avellana")
    for _ in range(8):
        ns = re.sub(r"_(?:ed|eo|pd|po|[dop])\d*$", "", s, flags=re.IGNORECASE)
        if ns == s:
            break
        s = ns
    unders = s.replace("-", "_")
    unders = KNOWN_FOLDER_ALIASES.get(unders, unders)
    for c in (s, unders):
        if c and (DOCS_DIR / "assets" / "images" / "by-taxon" / c).is_dir():
            return c
    return None


def first_by_taxon_image(entry: Dict[str, Any]) -> Optional[str]:
    for p in yaml_image_paths(entry):
        if "assets/images/by-taxon/" in p.replace("\\", "/"):
            return p.replace("\\", "/")
    return None


def find_by_taxon_basename(fname: str) -> Optional[str]:
    """Locate ``by-taxon/**/<basename>`` when folder slug does not match the stem."""
    bn = Path(fname).name
    root = DOCS_DIR / "assets" / "images" / "by-taxon"
    if not root.is_dir():
        return None
    for p in root.rglob(bn):
        if p.is_file():
            rel = p.relative_to(DOCS_DIR).as_posix().replace("\\", "/")
            if not rel.startswith("assets/"):
                rel = "assets/" + rel
            return rel
    return None


def first_file_on_disk(pollen_key: str) -> Optional[str]:
    d = DOCS_DIR / "assets" / "images" / "by-taxon" / pollen_key
    if not d.is_dir():
        return None
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    files = sorted([p for p in d.iterdir() if p.is_file() and p.suffix.lower() in exts], key=lambda x: x.name.lower())
    if not files:
        return None
    rel = files[0].relative_to(DOCS_DIR).as_posix()
    if not rel.startswith("assets/"):
        return "assets/" + rel
    return rel


def _folder_slug_candidates(fname: str) -> List[str]:
    """Map a pollenwiki filename stem to possible by-taxon folder names."""
    raw_stem = Path(fname).stem
    s0 = raw_stem.strip().lower().replace("-", "_")
    out: List[str] = []
    n1 = normalize_image_stem(raw_stem)
    if n1:
        out.append(n1)
    # e.g. moneses_uniflora2.png → folder moneses_uniflora
    s2 = re.sub(r"\d+$", "", s0).rstrip("_")
    if s2 and s2 not in out:
        out.append(s2)
    if s0 not in out:
        out.append(s0)
    return out


def _prefix_folder_candidates(fname: str) -> List[str]:
    """Longest-prefix match: ``populus_nigra_scabraat_…`` → ``populus_nigra``."""
    stem_lc = Path(fname).stem.lower().replace("-", "_").replace("avallana", "avellana")
    stem_lc = re.sub(r"_(?:ed|eo|pd|po|[dop])\d*$", "", stem_lc, flags=re.IGNORECASE)
    parts = [p for p in stem_lc.split("_") if p]
    out: List[str] = []
    for n in range(min(len(parts), 8), 1, -1):
        fold = "_".join(parts[:n])
        out.append(fold)
    return out


def resolve_new_path(fname: str, data: Dict[str, Any], slug_to_key: Dict[str, str], stem_to_keys: Dict[str, List[str]]) -> Optional[str]:
    low = fname.lower()
    if low == "tilia_platyphyllos_kristals.png":
        return "assets/images/non-pollen/tilia_kristals.png"

    pk = disk_folder_key_for_pollenwiki(fname)
    if not pk:
        seen: set[str] = set()
        candidates: List[str] = []
        for c in _prefix_folder_candidates(fname) + _folder_slug_candidates(fname):
            if c and c not in seen:
                seen.add(c)
                candidates.append(c)

        for stem in candidates:
            status, keys = resolve_pollen_key_for_stem(stem, stem_to_keys=stem_to_keys, slug_to_key=slug_to_key)
            if status == "confident" and keys:
                pk = keys[0]
                break
            if (DOCS_DIR / "assets" / "images" / "by-taxon" / stem).is_dir():
                pk = stem
                break
    if not pk:
        return None
    entry = data.get(pk)
    if isinstance(entry, dict):
        img = first_by_taxon_image(entry)
        if img:
            return img
    disk = first_file_on_disk(pk)
    if disk:
        return disk
    return find_by_taxon_basename(fname)


def rewrite_text(text: str, data: Dict[str, Any], slug_to_key: Dict[str, str], stem_to_keys: Dict[str, List[str]]) -> Tuple[str, int]:
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        prefix = m.group(1) or ""
        full = m.group(2)
        fname = m.group(3)
        fl = fname.lower()
        if fl == "placeholder.png" or fl.startswith("placeholder_"):
            return m.group(0)
        new_tail = resolve_new_path(fname, data, slug_to_key, stem_to_keys)
        if not new_tail:
            return m.group(0)
        n += 1
        return prefix + new_tail

    new_text = RE_REF.sub(repl, text)
    return new_text, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    data = yaml.safe_load(POLLEN_YAML.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        print("Invalid YAML")
        return 1
    slug_to_key, stem_to_keys = build_pollen_indexes(data)

    total = 0
    touched = 0
    targets: List[Path] = []
    for pat in ("**/*.md", "**/*.json"):
        targets.extend(sorted(DOCS_DIR.glob(pat)))

    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if "pollenwiki/" not in text:
            continue
        new_text, c = rewrite_text(text, data, slug_to_key, stem_to_keys)
        if c == 0:
            continue
        total += c
        if args.apply:
            path.write_text(new_text, encoding="utf-8", newline="\n")
        touched += 1
        print(f"{path.relative_to(REPO)}\t{c}")

    print(f"Total replacements: {total} in {touched} files (apply={args.apply})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
