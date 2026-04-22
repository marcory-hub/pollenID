#!/usr/bin/env python3
"""
Normalize Beug key JSON files under docs/keys/beug/*.json.

Goal: make the JSONs uniform (stable schema) and ensure exactly 4 image slots
everywhere images are used, padding with placeholders when missing.

This script intentionally stays within the vdh-pollentabel renderer contract:
choices may use `next`, `outcome`, or `id` endpoints. We normalize shape and
fill placeholders, but do not introduce novel top-level concepts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
BEUG_DIR = REPO_ROOT / "docs" / "keys" / "beug"

# The renderer treats /PLACEHOLDER_*.png as placeholders and swaps them with
# NO_IMAGE_FOUND.jpg at runtime.
PLACEHOLDER_IMAGE = "../../assets/images/pollenwiki/PLACEHOLDER_Pd.png"
PLACEHOLDER_WIDTH_PX = 1
IMAGES_SLOTS = 4


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def as_str(v: Any) -> Optional[str]:
    return v if isinstance(v, str) else None


def norm_string(v: Any, *, default: str = "-") -> str:
    s = as_str(v)
    if s is None:
        return default
    if s.strip() == "":
        return default
    return s


def norm_bool(v: Any, *, default: bool = False) -> bool:
    return v if isinstance(v, bool) else default


def placeholder_image_obj() -> Dict[str, Any]:
    return {"image": PLACEHOLDER_IMAGE, "imageWidthPx": PLACEHOLDER_WIDTH_PX}


def normalize_images_list(images: Any) -> List[Dict[str, Any]]:
    """
    Normalize an images payload to a list[{image,imageWidthPx}] padded/truncated to 4.
    Accepts legacy single {image,imageWidthPx} fields elsewhere (handled by callers).
    """
    out: List[Dict[str, Any]] = []
    if isinstance(images, list):
        for im in images:
            if not isinstance(im, dict):
                continue
            img = as_str(im.get("image"))
            if not img:
                continue
            im_out: Dict[str, Any] = {"image": img}
            w = im.get("imageWidthPx")
            if isinstance(w, (int, float)) and w > 0:
                im_out["imageWidthPx"] = w
            else:
                im_out["imageWidthPx"] = PLACEHOLDER_WIDTH_PX
            out.append(im_out)
    # pad/truncate
    if len(out) < IMAGES_SLOTS:
        out.extend([placeholder_image_obj() for _ in range(IMAGES_SLOTS - len(out))])
    elif len(out) > IMAGES_SLOTS:
        out = out[:IMAGES_SLOTS]
    return out


def normalize_images_from_legacy(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize `obj.images`, or legacy `obj.image`/`obj.imageWidthPx`.
    Always returns a list of exactly 4 images.
    """
    if isinstance(obj.get("images"), list):
        return normalize_images_list(obj.get("images"))
    img = as_str(obj.get("image"))
    if img:
        w = obj.get("imageWidthPx")
        im: Dict[str, Any] = {"image": img}
        if isinstance(w, (int, float)) and w > 0:
            im["imageWidthPx"] = w
        else:
            im["imageWidthPx"] = PLACEHOLDER_WIDTH_PX
        return normalize_images_list([im])
    return normalize_images_list([])


def normalize_endpoint_obj(endpoint: Any) -> Optional[Dict[str, Any]]:
    """
    Normalize an endpoint object (choice.id or choice.outcome) into a uniform shape.
    Returns None when endpoint is missing or not an object.
    """
    if not isinstance(endpoint, dict):
        return None

    images = normalize_images_from_legacy(endpoint)
    out: Dict[str, Any] = {
        "name": norm_string(endpoint.get("name")),
        "pollen_key": norm_string(endpoint.get("pollen_key")),
        "size": norm_string(endpoint.get("size")),
        "source": norm_string(endpoint.get("source")),
        "note": norm_string(endpoint.get("note")),
        "text": norm_string(endpoint.get("text")),
        "incomplete": norm_bool(endpoint.get("incomplete")),
        "images": images,
    }
    return out


def normalize_choice_obj(choice: Any) -> Dict[str, Any]:
    if not isinstance(choice, dict):
        choice = {}

    # Normalize endpoint objects first so we can also pad their images.
    endpoint_id = normalize_endpoint_obj(choice.get("id"))
    endpoint_outcome = normalize_endpoint_obj(choice.get("outcome"))

    images = normalize_images_from_legacy(choice)

    nxt = choice.get("next")
    next_val: Optional[str] = None
    if isinstance(nxt, str) and nxt.strip():
        next_val = nxt.strip()

    out: Dict[str, Any] = {
        "label": norm_string(choice.get("label")),
        "next": next_val,
        "id": endpoint_id,
        "outcome": endpoint_outcome,
        "images": images,
    }
    return out


def normalize_step_obj(step_id: str, step: Any) -> Dict[str, Any]:
    if not isinstance(step, dict):
        step = {}
    raw_choices = step.get("choices")
    choices_in = raw_choices if isinstance(raw_choices, list) else []
    choices_out = [normalize_choice_obj(ch) for ch in choices_in]

    out: Dict[str, Any] = {
        "id": str(step.get("id") or step_id),
        "type": norm_string(step.get("type"), default="step"),
        "note": norm_string(step.get("note")),
        "choices": choices_out,
    }
    return out


def normalize_meta(meta: Any, *, json_basename: str, start: str, steps_count: int) -> Dict[str, Any]:
    meta = meta if isinstance(meta, dict) else {}
    out: Dict[str, Any] = {
        "key": norm_string(meta.get("key"), default=json_basename),
        "title": norm_string(meta.get("title")),
        "locale": norm_string(meta.get("locale"), default="nl"),
        "source": norm_string(meta.get("source"), default="Beug"),
        "note": norm_string(meta.get("note")),
        "stepCount": steps_count,
        "start": norm_string(meta.get("start"), default=start),
    }
    # Ensure meta.key is the file name (uniform convention).
    out["key"] = json_basename
    # Ensure meta.start matches root start.
    out["start"] = start
    return out


def normalize_beug_key(path: Path) -> Tuple[bool, Dict[str, Any]]:
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected JSON object at root")

    steps_raw = raw.get("steps")
    if not isinstance(steps_raw, dict):
        steps_raw = {}

    # Determine root start.
    start = raw.get("start") or (raw.get("meta") or {}).get("start") or "1"
    start = norm_string(start)

    # Normalize steps in stable numeric-ish order when possible.
    def sort_key(s: str) -> Tuple[int, str]:
        try:
            return (int(s), s)
        except Exception:
            return (10**9, s)

    steps_out: Dict[str, Any] = {}
    for sid in sorted((str(k) for k in steps_raw.keys()), key=sort_key):
        steps_out[sid] = normalize_step_obj(sid, steps_raw.get(sid))

    meta_out = normalize_meta(
        raw.get("meta"),
        json_basename=path.name,
        start=start,
        steps_count=len(steps_out),
    )

    out: Dict[str, Any] = {
        "meta": meta_out,
        "start": start,
        "steps": steps_out,
    }

    changed = out != raw
    return changed, out


def main() -> int:
    if not BEUG_DIR.is_dir():
        raise SystemExit(f"Missing directory: {BEUG_DIR}")

    changed_files = 0
    total_files = 0
    for path in sorted(BEUG_DIR.glob("*.json")):
        total_files += 1
        changed, data = normalize_beug_key(path)
        if changed:
            write_json(path, data)
            changed_files += 1

    print(f"beug_total_files={total_files} beug_changed_files={changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

