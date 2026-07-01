#!/usr/bin/env python3
"""Normalize top-level field order and keys in data/pollen.yaml.

- One canonical key set per taxon (no duplicate nectar_value / pollen_class blocks).
- pollen-class merged into pollen_class.
- Fixed field order; missing keys get empty/null defaults.
- Does not invent taxon facts; only structure.
"""

from __future__ import annotations

import argparse
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from ruamel.yaml import YAML
from yaml.loader import SafeLoader

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"

CANONICAL_FIELDS: Tuple[str, ...] = (
    "latin",
    "dutch",
    "family",
    "size",
    "pollen_class",
    "shape",
    "sculpture",
    "aperture",
    "ornamentation",
    "polarity",
    "pe_ratio",
    "pollen-note",
    "bloeitijd",
    "nectar_value",
    "pollen_value",
    "frequency_in_honey",
    "links",
    "sources",
    "images",
)

SIZE_KEYS = ("smallest_size", "largest_size", "height_px")
BLOEITIJD_KEYS = ("start", "end")
LINK_KEYS = ("pollenX", "tstebler", "paldat")


def _empty_scalar() -> None:
    return None


def _merge_scalar(a: Any, b: Any) -> Any:
    def filled(v: Any) -> bool:
        if v is None:
            return False
        if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
            return False
        return True

    if filled(a) and filled(b) and a != b:
        return a
    if filled(a):
        return a
    if filled(b):
        return b
    return a if a is not None else b


def _merge_dict(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(a) if isinstance(a, dict) else {}
    if isinstance(b, dict):
        for k, v in b.items():
            if k not in out:
                out[k] = deepcopy(v)
            elif isinstance(out[k], dict) and isinstance(v, dict):
                out[k] = _merge_dict(out[k], v)
            else:
                out[k] = _merge_scalar(out[k], v)
    return out


def _merge_list(a: Any, b: Any) -> List[Any]:
    items: List[Any] = []
    for src in (a, b):
        if not isinstance(src, list):
            continue
        for item in src:
            if item not in items:
                items.append(deepcopy(item))
    return items


def _normalize_entry(raw: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}

    if isinstance(raw.get("pollen-class"), str) or raw.get("pollen-class") is None:
        pc_alt = raw.get("pollen-class")
        pc = raw.get("pollen_class")
        merged["pollen_class"] = _merge_scalar(pc, pc_alt)
    elif "pollen_class" in raw:
        merged["pollen_class"] = raw.get("pollen_class")

    for key, val in raw.items():
        if key in ("pollen-class",):
            continue
        if key not in merged:
            merged[key] = deepcopy(val)
        elif key in ("sources", "images"):
            merged[key] = _merge_list(merged.get(key), val)
        elif key in ("links", "size", "bloeitijd") and isinstance(val, dict):
            merged[key] = _merge_dict(
                merged.get(key) if isinstance(merged.get(key), dict) else {},
                val,
            )
        else:
            merged[key] = _merge_scalar(merged.get(key), val)

    out: Dict[str, Any] = {}
    for field in CANONICAL_FIELDS:
        if field == "size":
            src = merged.get("size") if isinstance(merged.get("size"), dict) else {}
            out["size"] = {k: src.get(k, _empty_scalar()) for k in SIZE_KEYS}
        elif field == "bloeitijd":
            src = merged.get("bloeitijd") if isinstance(merged.get("bloeitijd"), dict) else {}
            out["bloeitijd"] = {k: src.get(k, _empty_scalar()) for k in BLOEITIJD_KEYS}
        elif field == "links":
            src = merged.get("links") if isinstance(merged.get("links"), dict) else {}
            out["links"] = {k: src.get(k, _empty_scalar()) for k in LINK_KEYS}
        elif field == "sources":
            src = merged.get("sources")
            out["sources"] = deepcopy(src) if isinstance(src, list) else []
        elif field == "images":
            src = merged.get("images")
            out["images"] = deepcopy(src) if isinstance(src, list) else []
        else:
            out[field] = merged.get(field, _empty_scalar())

    return out


def _load_yaml(path: Path) -> Dict[str, Any]:
    class MergeLoader(SafeLoader):
        pass

    def _construct_mapping(loader: MergeLoader, node: yaml.nodes.MappingNode) -> Dict[str, Any]:
        mapping: Dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            val = loader.construct_object(value_node)
            if key in mapping:
                if key in ("sources", "images"):
                    mapping[key] = _merge_list(mapping[key], val)
                elif isinstance(mapping[key], dict) and isinstance(val, dict):
                    mapping[key] = _merge_dict(mapping[key], val)
                else:
                    mapping[key] = _merge_scalar(mapping[key], val)
            else:
                mapping[key] = val
        return mapping

    MergeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_mapping,
    )

    with path.open(encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=MergeLoader)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: top-level must be a mapping")
    return data


def _scan_duplicate_keys_in_text(text: str) -> List[Tuple[str, List[str]]]:
    import re

    issues: List[Tuple[str, List[str]]] = []
    parts = re.split(r"(?m)^(?=[a-z][a-z0-9_]*:$)", text)
    for part in parts:
        m = re.match(r"^([a-z][a-z0-9_]*):", part)
        if not m:
            continue
        key = m.group(1)
        fields = re.findall(r"^  ([a-zA-Z0-9_-]+):", part, re.M)
        from collections import Counter

        dups = [f for f, c in Counter(fields).items() if c > 1]
        if dups:
            issues.append((key, dups))
    return issues


def _write_yaml(path: Path, data: Dict[str, Any]) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.width = 4096
    yaml.indent(mapping=2, sequence=4, offset=2)
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(data, fh)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write")
    parser.add_argument("--path", type=Path, default=YAML_PATH)
    args = parser.parse_args()

    raw_text = args.path.read_text(encoding="utf-8")
    dup_before = _scan_duplicate_keys_in_text(raw_text)
    if dup_before:
        print(f"duplicate field keys before normalize: {len(dup_before)}")
        for key, dups in dup_before:
            print(f"  {key}: {dups}")

    data = _load_yaml(args.path)
    normalized: Dict[str, Any] = {}
    for slug in data.keys():
        entry = data[slug]
        if not isinstance(entry, dict):
            normalized[slug] = entry
            continue
        normalized[slug] = _normalize_entry(entry)

    # spot-check merged duplicates
    fago = normalized.get("fagopyrum_esculentum", {})
    if isinstance(fago, dict):
        print(
            "fagopyrum_esculentum nectar/pollen:",
            fago.get("nectar_value"),
            fago.get("pollen_value"),
        )

    missing_images = sum(1 for e in normalized.values() if isinstance(e, dict) and e.get("images") == [])
    print(f"taxa: {len(normalized)}")
    print(f"entries with empty images: []: {missing_images}")

    if args.dry_run:
        print("dry-run: no file written")
        return 0

    _write_yaml(args.path, normalized)
    dup_after = _scan_duplicate_keys_in_text(args.path.read_text(encoding="utf-8"))
    print(f"duplicate field keys after normalize: {len(dup_after)}")
    print(f"wrote {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
