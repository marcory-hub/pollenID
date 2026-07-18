#!/usr/bin/env python3
"""Normalize data/pollen.yaml to the nested SoT schema.

Canonical layout per taxon:
  name / classification / size / pollen_class_beug / pollen_features /
  flowering_time / value / note / frequency_* / links / images

Migrates legacy flat keys (latin, dutch, family, shape, …) without inventing facts.
"""

from __future__ import annotations

import argparse
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from ruamel.yaml import YAML
from yaml.loader import SafeLoader

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"

NAME_KEYS = ("latin_name", "dutch_name")
CLASSIFICATION_KEYS = ("order", "family_latin", "family_dutch", "tribe", "genus")
SIZE_KEYS = ("size_smallest", "size_largest", "height_px")
FEATURE_KEYS = (
    "shape",
    "sculpture",
    "sculpture_visibility",
    "aperture",
    "aperture_visibility",
    "ornamentation",
    "ornamentation_visibility",
    "polarity",
    "pe_ratio",
    "pollen-note",
)
FLOWERING_TIME_KEYS = ("start", "end")
VALUE_KEYS = ("nectar_value", "pollen_value")
NOTE_KEYS = ("note_plant", "note_honey", "note_pollen")
LINK_KEYS = ("pollenX", "tstebler", "paldat", "waarneming")

CANONICAL_TOP: Tuple[str, ...] = (
    "name",
    "classification",
    "size",
    "pollen_class_beug",
    "pollen_features",
    "flowering_time",
    "value",
    "note",
    "frequency_in_dutch_honey",
    "frequency_in_eu_honey",
    "frequency_in_non_eu_honey",
    "is_secondary_contributor",
    "links",
    "images",
)


def _empty_scalar() -> None:
    return None


def _filled(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
        return False
    return True


def _merge_scalar(a: Any, b: Any) -> Any:
    if _filled(a) and _filled(b) and a != b:
        return a
    if _filled(a):
        return a
    if _filled(b):
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


def _as_dict(v: Any) -> Dict[str, Any]:
    return deepcopy(v) if isinstance(v, dict) else {}


def _subdict(keys: Tuple[str, ...], src: Dict[str, Any], *fallbacks: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k in keys:
        val = src.get(k, _empty_scalar())
        if not _filled(val):
            for fb in fallbacks:
                if k in fb and _filled(fb.get(k)):
                    val = fb.get(k)
                    break
        out[k] = val if val is not None else _empty_scalar()
    return out


def _normalize_entry(raw: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}

    # Drop legacy sources block.
    for key, val in raw.items():
        if key == "sources":
            continue
        if key not in merged:
            merged[key] = deepcopy(val)
        elif key == "images":
            merged[key] = _merge_list(merged.get(key), val)
        elif key in (
            "links",
            "size",
            "flowering_time",
            "name",
            "classification",
            "pollen_features",
            "value",
            "note",
        ) and isinstance(val, dict):
            merged[key] = _merge_dict(
                merged.get(key) if isinstance(merged.get(key), dict) else {},
                val,
            )
        else:
            merged[key] = _merge_scalar(merged.get(key), val)

    # pollen-class → pollen_class_beug
    pc = _merge_scalar(merged.pop("pollen_class", None), merged.pop("pollen-class", None))
    pc = _merge_scalar(merged.get("pollen_class_beug"), pc)
    merged["pollen_class_beug"] = pc

    # frequency_in_honey → frequency_in_dutch_honey
    legacy_freq = merged.pop("frequency_in_honey", None)
    if legacy_freq is not None:
        merged["frequency_in_dutch_honey"] = _merge_scalar(
            merged.get("frequency_in_dutch_honey"), legacy_freq
        )

    # bloeitijd → flowering_time
    if "bloeitijd" in merged:
        bloom = merged.pop("bloeitijd")
        if isinstance(bloom, dict):
            merged["flowering_time"] = _merge_dict(
                _as_dict(merged.get("flowering_time")), bloom
            )

    name_src = _as_dict(merged.get("name"))
    class_src = _as_dict(merged.get("classification"))
    size_src = _as_dict(merged.get("size"))
    feat_src = _as_dict(merged.get("pollen_features"))
    value_src = _as_dict(merged.get("value"))
    note_src = _as_dict(merged.get("note")) if isinstance(merged.get("note"), dict) else {}

    # Legacy flat name fields
    name_src["latin_name"] = _merge_scalar(name_src.get("latin_name"), merged.get("latin"))
    name_src["dutch_name"] = _merge_scalar(name_src.get("dutch_name"), merged.get("dutch"))

    # Legacy flat / unsplit classification.family → family_latin + family_dutch
    legacy_family = _merge_scalar(class_src.get("family"), merged.get("family"))
    if _filled(legacy_family) and isinstance(legacy_family, str):
        m = re.match(r"^([A-Za-z][A-Za-z-]*)\s*\(([^()]*)\)\s*$", legacy_family.strip())
        if m:
            latin = m.group(1).strip()
            dutch = m.group(2).strip()
            class_src["family_latin"] = _merge_scalar(class_src.get("family_latin"), latin)
            class_src["family_dutch"] = _merge_scalar(class_src.get("family_dutch"), dutch)
        else:
            class_src["family_latin"] = _merge_scalar(
                class_src.get("family_latin"), legacy_family.strip()
            )
    class_src.pop("family", None)
    class_src["family_latin"] = class_src.get("family_latin")
    class_src["family_dutch"] = class_src.get("family_dutch")

    # Legacy size key names
    size_src["size_smallest"] = _merge_scalar(
        size_src.get("size_smallest"),
        _merge_scalar(size_src.get("smallest_size"), merged.get("smallest_size")),
    )
    size_src["size_largest"] = _merge_scalar(
        size_src.get("size_largest"),
        _merge_scalar(size_src.get("largest_size"), merged.get("largest_size")),
    )
    size_src.pop("smallest_size", None)
    size_src.pop("largest_size", None)

    # Legacy flat morphology → pollen_features
    for fk in FEATURE_KEYS:
        flat = merged.get(fk)
        feat_src[fk] = _merge_scalar(feat_src.get(fk), flat)

    # Legacy flat value fields
    value_src["nectar_value"] = _merge_scalar(
        value_src.get("nectar_value"), merged.get("nectar_value")
    )
    value_src["pollen_value"] = _merge_scalar(
        value_src.get("pollen_value"), merged.get("pollen_value")
    )

    # Legacy scalar note → note_plant; keep nested note.* if already present
    legacy_note = merged.get("note")
    if not isinstance(legacy_note, dict) and _filled(legacy_note):
        note_src["note_plant"] = _merge_scalar(note_src.get("note_plant"), legacy_note)

    out: Dict[str, Any] = {
        "name": _subdict(NAME_KEYS, name_src),
        "classification": _subdict(CLASSIFICATION_KEYS, class_src),
        "size": _subdict(SIZE_KEYS, size_src),
        "pollen_class_beug": merged.get("pollen_class_beug", _empty_scalar()),
        "pollen_features": _subdict(FEATURE_KEYS, feat_src),
        "flowering_time": _subdict(
            FLOWERING_TIME_KEYS, _as_dict(merged.get("flowering_time"))
        ),
        "value": _subdict(VALUE_KEYS, value_src),
        "note": _subdict(NOTE_KEYS, note_src),
        "frequency_in_dutch_honey": merged.get("frequency_in_dutch_honey", _empty_scalar()),
        "frequency_in_eu_honey": merged.get("frequency_in_eu_honey", _empty_scalar()),
        "frequency_in_non_eu_honey": merged.get(
            "frequency_in_non_eu_honey", _empty_scalar()
        ),
        "links": _subdict(LINK_KEYS, _as_dict(merged.get("links"))),
        "images": deepcopy(merged["images"])
        if isinstance(merged.get("images"), list)
        else [],
    }

    # Preserve only canonical top-level order (already built).
    assert tuple(out.keys()) == CANONICAL_TOP
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
                if key in ("images",):
                    mapping[key] = _merge_list(mapping[key], val)
                elif key == "sources":
                    continue
                elif isinstance(mapping[key], dict) and isinstance(val, dict):
                    mapping[key] = _merge_dict(mapping[key], val)
                else:
                    mapping[key] = _merge_scalar(mapping[key], val)
            else:
                if key == "sources":
                    continue
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
    from collections import Counter

    issues: List[Tuple[str, List[str]]] = []
    parts = re.split(r"(?m)^(?=[a-z][a-z0-9_]*:$)", text)
    for part in parts:
        m = re.match(r"^([a-z][a-z0-9_]*):", part)
        if not m:
            continue
        key = m.group(1)
        fields = re.findall(r"^  ([a-zA-Z0-9_-]+):", part, re.M)
        dups = [f for f, c in Counter(fields).items() if c > 1]
        if dups:
            issues.append((key, dups))
    return issues


def _write_yaml(path: Path, data: Dict[str, Any]) -> None:
    yaml_w = YAML()
    yaml_w.preserve_quotes = True
    yaml_w.default_flow_style = False
    yaml_w.width = 4096
    yaml_w.indent(mapping=2, sequence=4, offset=2)
    with path.open("w", encoding="utf-8") as fh:
        yaml_w.dump(data, fh)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write")
    parser.add_argument("--path", type=Path, default=YAML_PATH)
    args = parser.parse_args()

    raw_text = args.path.read_text(encoding="utf-8")
    dup_before = _scan_duplicate_keys_in_text(raw_text)
    if dup_before:
        print(f"duplicate field keys before normalize: {len(dup_before)}")
        for key, dups in dup_before[:20]:
            print(f"  {key}: {dups}")

    data = _load_yaml(args.path)
    normalized: Dict[str, Any] = {}
    for slug in data.keys():
        entry = data[slug]
        if not isinstance(entry, dict):
            normalized[slug] = entry
            continue
        normalized[slug] = _normalize_entry(entry)

    sample = normalized.get("acacia_dealbata", {})
    if isinstance(sample, dict):
        print(
            "acacia_dealbata:",
            sample.get("name"),
            sample.get("size"),
            sample.get("value"),
        )

    missing_images = sum(
        1 for e in normalized.values() if isinstance(e, dict) and e.get("images") == []
    )
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
