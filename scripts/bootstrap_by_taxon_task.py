#!/usr/bin/env python3
"""Create docs/assets/images/by-taxon-task/<source>/<slug>/ for taxa that need images.

A taxon is queued when it appears in selected keys or honey Markdown but has no
usable pollen bitmap under docs/assets/images/by-taxon/<slug>/ (non-placeholder file).

Writes a .gitkeep in each new folder so empty directories are tracked.

Usage: python scripts/bootstrap_by_taxon_task.py [--apply]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

from pollen_asset_lib import DOCS_DIR, IMAGES_DIR, IMAGE_EXTS, POLLEN_YAML

REPO = Path(__file__).resolve().parents[1]
KEYS_DIR = DOCS_DIR / "keys"
TASK_ROOT = IMAGES_DIR / "by-taxon-task"

SKIP_NAME_PARTS = ("placeholder", "no_image_found")


def label_for_json(path: Path) -> str:
    rel = path.as_posix()
    if "/beug/" in rel:
        return "beug"
    if "kerkvliet-determinatietabel" in rel:
        return "kerkvliet"
    if "vanderham" in rel:
        return "vanderham"
    if "/reitsma/" in rel:
        return "reitsma"
    if "/eide/" in rel:
        return "eide"
    if "feagri-iversen" in rel:
        return "feagri-iversen"
    try:
        return path.relative_to(KEYS_DIR).parts[0]
    except ValueError:
        return "keys"


def collect_pollen_keys_from_obj(obj: Any, out: Set[str]) -> None:
    if isinstance(obj, dict):
        pk = obj.get("pollen_key")
        if isinstance(pk, str):
            s = pk.strip()
            if s and s != "-" and re.match(r"^[a-z][a-z0-9_]*\Z", s):
                out.add(s)
        for v in obj.values():
            collect_pollen_keys_from_obj(v, out)
    elif isinstance(obj, list):
        for it in obj:
            collect_pollen_keys_from_obj(it, out)


def collect_keys_from_json_files() -> List[Tuple[str, str]]:
    """List of (source_label, slug)."""
    pairs: List[Tuple[str, str]] = []
    if not KEYS_DIR.is_dir():
        return pairs
    for jp in sorted(KEYS_DIR.rglob("*.json")):
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        found: Set[str] = set()
        collect_pollen_keys_from_obj(data, found)
        src = label_for_json(jp)
        for slug in sorted(found):
            pairs.append((src, slug))
    return pairs


def collect_slugs_from_md(root: Path, source: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if not root.is_dir():
        return out
    for md in sorted(root.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(r'pollen_gallery\(\s*"([a-z][a-z0-9_]*)"', text):
            out.append((source, m.group(1)))
        for m in re.finditer(r'pollen\(\s*"([a-z][a-z0-9_]*)"', text):
            out.append((source, m.group(1)))
        for m in re.finditer(r"assets/images/by-taxon/([a-z][a-z0-9_]*)/", text):
            out.append((source, m.group(1)))
    return out


def disk_has_usable_bitmap(slug: str) -> bool:
    d = IMAGES_DIR / "by-taxon" / slug
    if not d.is_dir():
        return False
    for p in d.iterdir():
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        low = p.name.lower()
        if any(sp in low for sp in SKIP_NAME_PARTS):
            continue
        return True
    return False


def yaml_has_images(slug: str, data: Dict[str, Any]) -> bool:
    e = data.get(slug)
    if not isinstance(e, dict):
        return False
    imgs = e.get("images")
    if not isinstance(imgs, list) or not imgs:
        return False
    for im in imgs:
        if isinstance(im, dict) and isinstance(im.get("path"), str) and im["path"].strip():
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    raw = yaml.safe_load(POLLEN_YAML.read_text(encoding="utf-8")) or {}
    data = raw if isinstance(raw, dict) else {}

    wanted: Set[Tuple[str, str]] = set()
    for t in collect_keys_from_json_files():
        wanted.add(t)
    for t in collect_slugs_from_md(DOCS_DIR / "monoflorale-honing-pollen", "monoflorale-honing"):
        wanted.add(t)
    for t in collect_slugs_from_md(DOCS_DIR / "pollen" / "species", "pollen-species"):
        wanted.add(t)

    to_create: List[Tuple[str, str]] = []
    for src, slug in sorted(wanted):
        if yaml_has_images(slug, data) and disk_has_usable_bitmap(slug):
            continue
        if disk_has_usable_bitmap(slug):
            continue
        to_create.append((src, slug))

    print(f"Task folders to create: {len(to_create)}")
    for src, slug in to_create[:30]:
        print(f"  {src}/{slug}/")
    if len(to_create) > 30:
        print(f"  ... and {len(to_create) - 30} more")

    if not args.apply:
        return 0

    TASK_ROOT.mkdir(parents=True, exist_ok=True)
    for src, slug in to_create:
        d = TASK_ROOT / src / slug
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not gitkeep.is_file():
            gitkeep.write_text("", encoding="utf-8")
    print(f"Created/updated {len(to_create)} task folders under {TASK_ROOT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
