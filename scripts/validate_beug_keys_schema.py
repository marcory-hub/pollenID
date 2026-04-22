#!/usr/bin/env python3
"""
Validate that docs/keys/beug/*.json follow the normalized schema:
- root has meta/start/steps
- steps map contains step objects with id/type/note/choices
- choices contain label/next/id/outcome/images
- any images arrays present are exactly length 4 and contain {image,imageWidthPx}
- endpoints (choice.id / choice.outcome) are either null or objects with the
  normalized keys and images length 4.

Intended as a lightweight guard to prevent schema drift.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
BEUG_DIR = REPO_ROOT / "docs" / "keys" / "beug"

IMAGES_SLOTS = 4


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fail(path: Path, msg: str) -> None:
    raise ValueError(f"{path}: {msg}")


def expect_keys(path: Path, obj: Dict[str, Any], keys: Iterable[str], where: str) -> None:
    for k in keys:
        if k not in obj:
            fail(path, f"missing key {k!r} at {where}")


def validate_images(path: Path, images: Any, where: str) -> None:
    if not isinstance(images, list):
        fail(path, f"{where}.images must be a list")
    if len(images) != IMAGES_SLOTS:
        fail(path, f"{where}.images must have length {IMAGES_SLOTS}, got {len(images)}")
    for i, im in enumerate(images):
        if not isinstance(im, dict):
            fail(path, f"{where}.images[{i}] must be an object")
        if not isinstance(im.get("image"), str) or not im.get("image"):
            fail(path, f"{where}.images[{i}].image must be a non-empty string")
        w = im.get("imageWidthPx")
        if not isinstance(w, (int, float)) or w <= 0:
            fail(path, f"{where}.images[{i}].imageWidthPx must be a positive number")


ENDPOINT_KEYS = ["name", "pollen_key", "size", "source", "note", "text", "incomplete", "images"]


def validate_endpoint(path: Path, endpoint: Any, where: str) -> None:
    if endpoint is None:
        return
    if not isinstance(endpoint, dict):
        fail(path, f"{where} must be null or an object")
    expect_keys(path, endpoint, ENDPOINT_KEYS, where)
    if not isinstance(endpoint.get("incomplete"), bool):
        fail(path, f"{where}.incomplete must be boolean")
    validate_images(path, endpoint.get("images"), where)


def validate_choice(path: Path, ch: Any, where: str) -> None:
    if not isinstance(ch, dict):
        fail(path, f"{where} choice must be an object")
    expect_keys(path, ch, ["label", "next", "id", "outcome", "images"], where)
    if not isinstance(ch.get("label"), str):
        fail(path, f"{where}.label must be a string")
    nxt = ch.get("next")
    if nxt is not None and not isinstance(nxt, str):
        fail(path, f"{where}.next must be string or null")
    validate_endpoint(path, ch.get("id"), f"{where}.id")
    validate_endpoint(path, ch.get("outcome"), f"{where}.outcome")
    validate_images(path, ch.get("images"), where)


def validate_step(path: Path, sid: str, step: Any) -> None:
    if not isinstance(step, dict):
        fail(path, f"steps[{sid!r}] must be an object")
    expect_keys(path, step, ["id", "type", "note", "choices"], f"steps[{sid}]")
    if not isinstance(step.get("id"), str):
        fail(path, f"steps[{sid}].id must be a string")
    if not isinstance(step.get("type"), str):
        fail(path, f"steps[{sid}].type must be a string")
    if not isinstance(step.get("note"), str):
        fail(path, f"steps[{sid}].note must be a string")
    choices = step.get("choices")
    if not isinstance(choices, list):
        fail(path, f"steps[{sid}].choices must be a list")
    for i, ch in enumerate(choices):
        validate_choice(path, ch, f"steps[{sid}].choices[{i}]")


def validate_file(path: Path) -> None:
    data = read_json(path)
    if not isinstance(data, dict):
        fail(path, "root must be an object")
    expect_keys(path, data, ["meta", "start", "steps"], "root")
    if not isinstance(data.get("start"), str) or not data.get("start"):
        fail(path, "root.start must be a non-empty string")
    meta = data.get("meta")
    if not isinstance(meta, dict):
        fail(path, "meta must be an object")
    expect_keys(path, meta, ["key", "title", "locale", "source", "note", "stepCount", "start"], "meta")
    if not isinstance(meta.get("key"), str) or meta.get("key") != path.name:
        fail(path, f"meta.key must equal file basename ({path.name})")
    if not isinstance(meta.get("stepCount"), int):
        fail(path, "meta.stepCount must be an integer")
    if meta.get("start") != data.get("start"):
        fail(path, "meta.start must equal root.start")
    steps = data.get("steps")
    if not isinstance(steps, dict):
        fail(path, "steps must be an object")
    if meta.get("stepCount") != len(steps):
        fail(path, f"meta.stepCount must equal number of steps ({len(steps)})")
    for sid, step in steps.items():
        validate_step(path, str(sid), step)


def main() -> int:
    if not BEUG_DIR.is_dir():
        raise SystemExit(f"Missing directory: {BEUG_DIR}")
    files = sorted(BEUG_DIR.glob("*.json"))
    for p in files:
        validate_file(p)
    print(f"ok beug_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

