#!/usr/bin/env python3
"""Export data/pollen.yaml to docs/data/pollen.json for runtime use.

Writes a deterministic JSON index so `docs/javascripts/vdh-pollentabel.js`
can resolve endpoint info (latin, dutch, family, size, images) from the SoT.

Each exported taxon includes:
  - pollen_key — same string as the top-level JSON entry key (useful inside nested payloads)
  - images[].height_px — per-image display height matching vdh logic when possible:

    * explicit `height_px` on YAML image item wins
    * else YAML `entry.image.height_px` if set
    * else computed from µm averages (average of smallest_size & largest_size) × 2.5 px/µm
    * else FALLBACK_IMG_PX when image paths exist without size clues

Usage: python3 scripts/export_pollen_json.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
JSON_PATH = REPO / "docs" / "data" / "pollen.json"

FIELDS_SIZE = ("smallest_size", "largest_size")

# Mirrors docs/javascripts/vdh-pollentabel.js FALLBACK_IMAGE_HEIGHT_PX when no size.
FALLBACK_IMG_PX = 50


def _clean_scalar(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s in ("", "-", "null", "None"):
            return None
        return s
    return v


RE_SIZE_NUM = re.compile(r"(?P<num>\d+(?:[.,]\d+)?)\s*(?:[µμu]m)?", re.IGNORECASE)


def _segment_before_um_marker(text: str) -> str:
    """Truncate after the µm marker so trailing citations do not add spurious numbers."""
    if not text:
        return ""
    s = text.strip().replace("μm", "µm")
    low = s.lower()
    cut = len(s)
    i = low.find("µm")
    if i != -1:
        cut = min(cut, i + 2)
    j = low.find("um")  # plain 'um' without micro sign
    if j != -1:
        prev = "" if j == 0 else low[j - 1]
        if prev.isalpha():  # e.g. 'forum' contains 'um'
            pass
        else:
            cut = min(cut, j + 2)
    return s[:cut]


def _parse_um_numbers(text: str) -> List[float]:
    nums: List[float] = []
    seg = _segment_before_um_marker(text)
    for m in RE_SIZE_NUM.finditer(seg):
        raw = m.group("num").replace(",", ".")
        try:
            nums.append(float(raw))
        except ValueError:
            continue
    return nums


def _first_um_aggregate(s: Optional[str]) -> Optional[float]:
    if not isinstance(s, str) or not s.strip():
        return None
    nums = _parse_um_numbers(s)
    if not nums:
        return None
    return float(sum(nums) / len(nums))


def _avg_um_float_from_um_strings(smallest_str: Optional[str], largest_str: Optional[str]) -> Optional[float]:
    """Average µm numeric value from YAML size strings; mirrors JS heightPxFromSize averaging."""
    a = _first_um_aggregate(smallest_str)
    b = _first_um_aggregate(largest_str)
    if a is None and b is None:
        return None
    if a is not None and b is not None:
        return (a + b) / 2
    return a if a is not None else b


def _height_px_from_avg_um(avg_um: Optional[float]) -> Optional[int]:
    if avg_um is None or avg_um <= 0:
        return None
    return int(round(2.5 * avg_um))


def _coerce_int_px(v: Any) -> Optional[int]:
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v if v > 0 else None
    if isinstance(v, float) and v.is_integer():
        ii = int(v)
        return ii if ii > 0 else None
    if isinstance(v, str) and v.strip():
        try:
            ii = int(float(v.replace(",", ".").strip()))
            return ii if ii > 0 else None
        except ValueError:
            return None
    return None


def _size_dict_for_height(src_size: Any) -> Tuple[Optional[str], Optional[str]]:
    if not isinstance(src_size, dict):
        return (None, None)
    smallest = _clean_scalar(src_size.get("smallest_size"))
    largest = _clean_scalar(src_size.get("largest_size"))
    s_s = smallest if isinstance(smallest, str) else None
    s_l = largest if isinstance(largest, str) else None
    return (s_s, s_l)


def _default_tile_height_px(
    *,
    avg_um_height: Optional[int],
    legacy_image_px: Optional[int],
) -> int:
    for candidate in (legacy_image_px, avg_um_height):
        if isinstance(candidate, int) and candidate > 0:
            return candidate
    return FALLBACK_IMG_PX


def _build_entry(pollen_key_slug: str, src: Dict[str, Any]) -> Dict[str, Any]:
    """Build one JSON object keyed by pollen_key_slug elsewhere."""
    out: Dict[str, Any] = {}

    latin = _clean_scalar(src.get("latin"))
    dutch = _clean_scalar(src.get("dutch"))
    family = _clean_scalar(src.get("family"))

    out["pollen_key"] = pollen_key_slug

    if latin is not None:
        out["latin"] = latin
    if dutch is not None:
        out["dutch"] = dutch
    if family is not None:
        out["family"] = family

    for morph in ("shape", "ornamentation", "aperture"):
        mv = _clean_scalar(src.get(morph))
        if mv is not None:
            out[morph] = mv

    size_src = src.get("size") or {}
    ss, ls = _size_dict_for_height(size_src)

    avg_um = None
    if isinstance(size_src, dict):
        size_out: Dict[str, Any] = {}
        for key in FIELDS_SIZE:
            val = _clean_scalar(size_src.get(key))
            if val is not None:
                size_out[key] = val
        if size_out:
            out["size"] = size_out
        avg_um = _avg_um_float_from_um_strings(ss, ls)

    avg_um_px = _height_px_from_avg_um(avg_um)

    legacy_block = src.get("image") if isinstance(src.get("image"), dict) else {}
    legacy_px = _coerce_int_px(legacy_block.get("height_px") if legacy_block else None)

    without_per_image_px = _default_tile_height_px(avg_um_height=avg_um_px, legacy_image_px=legacy_px)

    images_src = src.get("images")
    if isinstance(images_src, list) and images_src:
        images_out = []
        for im in images_src:
            if not isinstance(im, dict):
                continue
            path = _clean_scalar(im.get("path"))
            if not path:
                continue
            item: Dict[str, Any] = {"path": str(path)}
            kind = _clean_scalar(im.get("kind"))
            source = _clean_scalar(im.get("source"))
            if kind is not None:
                item["kind"] = kind
            if source is not None:
                item["source"] = source
            ih = _coerce_int_px(im.get("height_px"))
            item["height_px"] = ih if ih is not None else without_per_image_px
            images_out.append(item)
        if images_out:
            out["images"] = images_out

    return out


def main() -> int:
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Unexpected top-level YAML type: {type(data).__name__}")

    exported: Dict[str, Dict[str, Any]] = {}
    for key in sorted(data.keys()):
        entry = data.get(key)
        if not isinstance(entry, dict):
            continue
        exported[key] = _build_entry(str(key), entry)

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(exported, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH.relative_to(REPO)} ({len(exported)} entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
