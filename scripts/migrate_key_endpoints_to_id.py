#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYS_DIR = DOCS_DIR / "keys"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def strip_emphasis_ast(s: str) -> str:
    return re.sub(r"\*([^*]*)\*", r"\1", s)


def split_text_name_size_source(raw_text: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Best-effort split of legacy outcome.text into:
    - name: taxon/type/family label (no size)
    - size: size fragment when it contains µm/μm
    - source: remaining provenance/citation fragment
    """
    if not isinstance(raw_text, str):
        return "", None, None

    s = strip_emphasis_ast(raw_text).strip()
    s = re.sub(r"\s+", " ", s)

    # Common pattern: "<name>, <size> µm, <source...>"
    # Also handle: "<name>, <size> μm" (Greek mu)
    mu_pat = r"(?:µm|μm)"
    m = re.search(rf"^(?P<name>.*?)(?:,\s*(?P<size>[^,]*\b{mu_pat}\b[^,]*))(?:,\s*(?P<src>.*))?$", s)
    if m:
        name = (m.group("name") or "").strip()
        size = (m.group("size") or "").strip() or None
        src = (m.group("src") or "").strip() or None
        return name, size, src

    # Pattern: "<name> <size> µm <source...>" (no comma before size)
    m2 = re.search(rf"^(?P<name>.*?)(?P<size>\b[0-9][^,]*\b{mu_pat}\b[^,]*)(?:,\s*(?P<src>.*))?$", s)
    if m2:
        name = (m2.group("name") or "").strip(" ,")
        size = (m2.group("size") or "").strip() or None
        src = (m2.group("src") or "").strip() or None
        return name, size, src

    return s, None, None


def normalize_images(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Move legacy image/imageWidthPx into images[] when needed.
    Keep existing images[] unchanged.
    """
    if "images" not in obj:
        images = []
        if isinstance(obj.get("image"), str) and obj.get("image"):
            im = {"image": obj.get("image")}
            if isinstance(obj.get("imageWidthPx"), (int, float)):
                im["imageWidthPx"] = obj.get("imageWidthPx")
            images.append(im)
        if images:
            obj["images"] = images
    return obj


def migrate_key(path: Path) -> Tuple[bool, int]:
    data = read_json(path)
    if not isinstance(data, dict):
        return False, 0
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return False, 0

    changed = False
    migrated = 0

    for _sid, step in steps.items():
        if not isinstance(step, dict):
            continue
        choices = step.get("choices")
        if not isinstance(choices, list):
            continue
        for ch in choices:
            if not isinstance(ch, dict):
                continue

            # Already migrated
            if isinstance(ch.get("id"), dict) and "name" in ch["id"]:
                continue

            out = ch.get("outcome")
            if not isinstance(out, dict):
                continue
            text = out.get("text")
            if not isinstance(text, str) or not text.strip():
                continue

            name, size, source = split_text_name_size_source(text)

            ident: Dict[str, Any] = {"name": name}
            if size:
                ident["size"] = size
            if source:
                ident["source"] = source

            # Preserve outcome metadata that affects rendering/overview
            if isinstance(out.get("incomplete"), bool):
                ident["incomplete"] = out["incomplete"]

            # Carry images (prefer outcome images)
            if "images" in out or "image" in out:
                tmp = dict(out)
                tmp = normalize_images(tmp)
                if isinstance(tmp.get("images"), list) and tmp["images"]:
                    ident["images"] = tmp["images"]

            # Replace outcome with id
            ch["id"] = ident
            ch.pop("outcome", None)

            changed = True
            migrated += 1

    if changed:
        write_json(path, data)
    return changed, migrated


def main() -> int:
    key_paths = sorted(KEYS_DIR.rglob("*.json"))
    total_migrated = 0
    changed_files = 0
    for kp in key_paths:
        changed, migrated = migrate_key(kp)
        if changed:
            changed_files += 1
            total_migrated += migrated
    print(f"migrated_endpoints={total_migrated} changed_files={changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

