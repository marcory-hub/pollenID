#!/usr/bin/env python3
"""Read-only inventory: image files, YAML coverage, and pollen_key resolution from stems.

Writes JSON to --out (default: _build/pollen_asset_audit.json).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set

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
    yaml_image_paths,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "_build" / "pollen_asset_audit.json"


def collect_md_asset_refs() -> Dict[str, List[str]]:
    refs: Dict[str, Set[str]] = defaultdict(set)
    for md in sorted(DOCS_DIR.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        if "assets/images/" not in text:
            continue
        rel_md = md.relative_to(REPO_ROOT).as_posix()
        i = 0
        while True:
            j = text.find("assets/images/", i)
            if j == -1:
                break
            fragment_start = j
            end = fragment_start + 400
            chunk = text[fragment_start:end]
            token_chars = []
            for ch in chunk:
                if ch in ('"', "'", " ", "\n", "\r", ")", "]"):
                    break
                token_chars.append(ch)
            raw = ("".join(token_chars)).replace("\\", "/")
            if raw.startswith("assets/images/"):
                refs[raw].add(rel_md)
            i = fragment_start + 10
    return {k: sorted(v) for k, v in refs.items()}


def scan_key_json_for_image_strings() -> Dict[str, List[str]]:
    out: Dict[str, Set[str]] = defaultdict(set)
    keys_dir = DOCS_DIR / "keys"
    if not keys_dir.is_dir():
        return {}
    for jp in sorted(keys_dir.rglob("*.json")):
        try:
            t = jp.read_text(encoding="utf-8")
        except OSError:
            continue
        rel_j = jp.relative_to(DOCS_DIR).as_posix()
        pos = 0
        while True:
            m = t.find("assets/images/", pos)
            if m == -1:
                break
            semi = t.find('"', m)
            raw = ""
            if semi != -1:
                candidate = t[m:semi].replace("\\", "/")
                if candidate.startswith("assets/images/"):
                    raw = candidate
            if raw:
                out[raw].add(rel_j)
            pos = m + len("assets/images/")
    return {k: sorted(v) for k, v in out.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"JSON output path (default: {DEFAULT_OUT})",
    )
    args = ap.parse_args()

    yaml_data = load_pollen_yaml_dict()
    slug_to_key, stem_to_keys = build_pollen_indexes(yaml_data)

    yaml_paths: Set[str] = set()
    for _k, entry in yaml_data.items():
        if isinstance(entry, dict):
            for p in yaml_image_paths(entry):
                yaml_paths.add(p.replace("\\", "/"))

    by_status: Dict[str, List[Dict[str, Any]]] = {
        "confident": [],
        "ambiguous": [],
        "none": [],
    }
    rel_files: List[str] = []
    for p in iter_image_files(IMAGES_DIR):
        rel = image_file_to_docs_path(p)
        rel_files.append(rel)

    for p in iter_image_files(IMAGES_DIR):
        rel = image_file_to_docs_path(p)
        stem = normalize_image_stem(p.stem)
        status, keys = resolve_pollen_key_for_stem(
            stem, stem_to_keys=stem_to_keys, slug_to_key=slug_to_key
        )
        rec = {
            "path": rel,
            "stem": p.stem,
            "stem_normalized": stem,
            "in_yaml": rel.replace("\\", "/") in yaml_paths,
            "under_by_taxon": is_under_by_taxon(rel.replace("\\", "/")),
            "keys": keys,
        }
        bucket = "none" if status == "none" else status
        by_status[bucket].append(rec)

    md_refs = collect_md_asset_refs()
    key_refs = scan_key_json_for_image_strings()

    report = {
        "pollen_yaml": str(POLLEN_YAML.relative_to(REPO_ROOT)),
        "images_dir": str(IMAGES_DIR.relative_to(REPO_ROOT)),
        "taxa_count": sum(1 for k, v in yaml_data.items() if isinstance(v, dict)),
        "files_on_disk": len(rel_files),
        "yaml_distinct_image_paths": len(yaml_paths),
        "resolution": {k: len(v) for k, v in by_status.items()},
        "not_in_yaml_but_confident": [
            r
            for r in by_status["confident"]
            if not r["in_yaml"] and not r["under_by_taxon"]
        ],
        "ambiguous": by_status["ambiguous"],
        "unresolved": by_status["none"],
        "markdown_refs_count": len(md_refs),
        "key_json_refs_count": len(key_refs),
        "generated_artifacts": [
            "docs/data/pollen.json",
            "docs/assets/manifests/images.json",
            "docs/assets/manifests/keys.json",
            "docs/assets/manifests/palynoquest-items.json",
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {args.out.relative_to(REPO_ROOT)}")
    print(
        f"files={len(rel_files)} confident_unlisted={len(report['not_in_yaml_but_confident'])} "
        f"ambiguous={len(by_status['ambiguous'])} unresolved={len(by_status['none'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
