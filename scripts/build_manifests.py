#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYS_DIR = DOCS_DIR / "keys"
IMAGES_DIR = DOCS_DIR / "assets" / "images"
OUT_DIR = DOCS_DIR / "assets" / "manifests"
KEYS_INDEX_MD = DOCS_DIR / "Identificatiesleutels" / "_index.md"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm_rel_posix(p: Path) -> str:
    return p.as_posix()


def list_images() -> List[str]:
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
    out: List[str] = []
    if not IMAGES_DIR.exists():
        return out
    for p in IMAGES_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            out.append(norm_rel_posix(p.relative_to(DOCS_DIR)))
    out.sort()
    return out


def is_placeholder_path(p: str) -> bool:
    return isinstance(p, str) and "PLACEHOLDER" in p.upper()


def normalize_image_ref(image_ref: str, base_dir: Path) -> Optional[str]:
    if not isinstance(image_ref, str) or not image_ref:
        return None
    if "://" in image_ref:
        return None
    try:
        p = (base_dir / image_ref).resolve()
        if DOCS_DIR in p.parents:
            return norm_rel_posix(p.relative_to(DOCS_DIR))
    except Exception:
        return None
    return None


def extract_images_from_node(node: Any, base_dir: Path) -> Iterable[Tuple[str, Optional[float]]]:
    if not isinstance(node, dict):
        return []
    found: List[Tuple[str, Optional[float]]] = []
    if isinstance(node.get("image"), str) and node.get("image"):
        img = normalize_image_ref(node["image"], base_dir)
        if img:
            w = node.get("imageWidthPx")
            found.append((img, w if isinstance(w, (int, float)) else None))
    imgs = node.get("images")
    if isinstance(imgs, list):
        for im in imgs:
            if isinstance(im, dict) and isinstance(im.get("image"), str) and im.get("image"):
                img = normalize_image_ref(im["image"], base_dir)
                if img:
                    w = im.get("imageWidthPx")
                    found.append((img, w if isinstance(w, (int, float)) else None))
    return found


@dataclass(frozen=True)
class ImageUse:
    key: str
    key_title: str
    key_json_url: str
    step_id: str
    choice_idx: int
    choice_label: str
    kind: str  # "choice" | "outcome"
    outcome_text: Optional[str] = None
    image_width_px: Optional[float] = None


def rel_json_url(key_json_path: Path) -> str:
    return norm_rel_posix(key_json_path.relative_to(DOCS_DIR))


def extract_from_key_json(key_json_path: Path) -> Tuple[Dict[str, Any], Dict[str, List[ImageUse]]]:
    data = read_json(key_json_path)
    base_dir = key_json_path.parent
    meta = data.get("meta") if isinstance(data, dict) else None
    key_id = ""
    key_title = ""
    if isinstance(meta, dict):
        key_id = str(meta.get("key") or "")
        key_title = str(meta.get("title") or "")
    if not key_id:
        key_id = key_json_path.stem
    if not key_title:
        key_title = key_id

    key_info = {
        "id": key_id,
        "title": key_title,
        "jsonUrl": rel_json_url(key_json_path),
        "sourcePath": str(key_json_path.relative_to(REPO_ROOT)),
    }

    image_map: Dict[str, List[ImageUse]] = {}
    steps = data.get("steps") if isinstance(data, dict) else None
    if not isinstance(steps, dict):
        return key_info, image_map

    key_json_url = key_info["jsonUrl"]

    for step_id, step in steps.items():
        if not isinstance(step_id, str):
            step_id = str(step_id)
        if not isinstance(step, dict):
            continue
        choices = step.get("choices")
        if not isinstance(choices, list):
            continue
        for idx, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            label = str(ch.get("label") or "")

            for image, _w in extract_images_from_node(ch, base_dir):
                w = _w
                use = ImageUse(
                    key=key_id,
                    key_title=key_title,
                    key_json_url=key_json_url,
                    step_id=step_id,
                    choice_idx=idx,
                    choice_label=label,
                    kind="choice",
                    image_width_px=w,
                )
                image_map.setdefault(image, []).append(use)

            out = ch.get("id") if isinstance(ch.get("id"), dict) else ch.get("outcome")
            if isinstance(out, dict):
                outcome_text = out.get("text") if "text" in out else out.get("name")
                if not isinstance(outcome_text, str) or not outcome_text.strip():
                    outcome_text = None
                for image, _w in extract_images_from_node(out, base_dir):
                    w = _w
                    use = ImageUse(
                        key=key_id,
                        key_title=key_title,
                        key_json_url=key_json_url,
                        step_id=step_id,
                        choice_idx=idx,
                        choice_label=label,
                        kind="outcome",
                        outcome_text=outcome_text,
                        image_width_px=w,
                    )
                    image_map.setdefault(image, []).append(use)

    return key_info, image_map


def compute_paths_for_key(key_json_path: Path) -> Dict[Tuple[str, int], List[Dict[str, Any]]]:
    """
    Compute a click-path from key start to each (stepId, choiceIdx) reachable.
    The path is a list of {stepId, choiceIdx, choiceLabel}.
    """
    data = read_json(key_json_path)
    if not isinstance(data, dict):
        return {}
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return {}
    start = str(data.get("start") or (data.get("meta") or {}).get("start") or "1")

    from collections import deque

    q = deque()
    q.append((start, []))
    seen_steps = set([start])
    paths: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}

    while q:
        sid, path = q.popleft()
        step = steps.get(sid)
        if not isinstance(step, dict):
            continue
        choices = step.get("choices")
        if not isinstance(choices, list):
            continue
        for idx, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            label = str(ch.get("label") or "")
            here = path + [{"stepId": str(sid), "choiceIdx": idx, "choiceLabel": label}]
            paths[(str(sid), idx)] = here
            nxt = ch.get("next")
            if isinstance(nxt, str) or isinstance(nxt, int):
                nsid = str(nxt)
                if nsid not in seen_steps:
                    seen_steps.add(nsid)
                    q.append((nsid, here))

    return paths


def parse_key_order_from_index() -> List[str]:
    """
    Returns docs-relative JSON URLs (keys/...) in the same order as
    docs/Identificatiesleutels/_index.md, by following linked md pages and reading their data-json-url.
    """
    if not KEYS_INDEX_MD.exists():
        return []
    txt = KEYS_INDEX_MD.read_text(encoding="utf-8")
    md_links: List[str] = []
    for line in txt.splitlines():
        # Markdown link: [label](file.md)
        if "](" in line and ")" in line:
            start = line.find("](")
            if start == -1:
                continue
            start += 2
            end = line.find(")", start)
            if end == -1:
                continue
            href = line[start:end].strip()
            if href.endswith(".md") and not href.startswith("http"):
                md_links.append(href)

    out: List[str] = []
    seen = set()
    for href in md_links:
        md_path = (KEYS_INDEX_MD.parent / href).resolve()
        if not md_path.exists():
            continue
        md_txt = md_path.read_text(encoding="utf-8")
        # Look for: data-json-url="...json" or data-json-url=...json
        marker = "data-json-url="
        pos = md_txt.find(marker)
        if pos == -1:
            continue
        s = md_txt[pos + len(marker) :].lstrip()
        if not s:
            continue
        if s[0] in ("'", '"'):
            q = s[0]
            s = s[1:]
            endq = s.find(q)
            if endq == -1:
                continue
            json_ref = s[:endq].strip()
        else:
            # unquoted: read until whitespace or >
            cut = len(s)
            for ch in (" ", "\t", "\n", ">", "/"):
                i = s.find(ch)
                if i != -1:
                    cut = min(cut, i)
            json_ref = s[:cut].strip()
        if not json_ref.endswith(".json"):
            continue
        # Resolve relative to the md file location and normalize to docs-relative.
        try:
            resolved = (md_path.parent / json_ref).resolve()
            if DOCS_DIR not in resolved.parents:
                continue
            rel = norm_rel_posix(resolved.relative_to(DOCS_DIR))
        except Exception:
            continue
        if rel in seen:
            continue
        seen.add(rel)
        out.append(rel)
    return out


def main() -> int:
    key_paths = sorted(KEYS_DIR.rglob("*.json"))
    keys: List[Dict[str, Any]] = []
    image_to_uses: Dict[str, List[Dict[str, Any]]] = {}
    key_paths_map: Dict[str, Path] = {}

    for kp in key_paths:
        try:
            key_info, image_map = extract_from_key_json(kp)
        except Exception as e:
            raise RuntimeError(f"Failed parsing {kp}: {e}") from e

        keys.append(key_info)
        key_paths_map[key_info["jsonUrl"]] = kp
        for img, uses in image_map.items():
            for u in uses:
                image_to_uses.setdefault(img, []).append(
                    {
                        "key": u.key,
                        "keyTitle": u.key_title,
                        "keyJsonUrl": u.key_json_url,
                        "stepId": u.step_id,
                        "choiceIdx": u.choice_idx,
                        "choiceLabel": u.choice_label,
                        "kind": u.kind,
                        "outcomeText": u.outcome_text,
                        "imageWidthPx": u.image_width_px,
                    }
                )

    # Order keys to match docs/Identificatiesleutels/_index.md when possible.
    desired_order = parse_key_order_from_index()
    by_url = {k.get("jsonUrl"): k for k in keys if isinstance(k.get("jsonUrl"), str)}
    ordered: List[Dict[str, Any]] = []
    used = set()
    for u in desired_order:
        k = by_url.get(u)
        if not k:
            continue
        ordered.append(k)
        used.add(u)
    for k in keys:
        u = k.get("jsonUrl")
        if isinstance(u, str) and u in used:
            continue
        ordered.append(k)

    all_images = list_images()
    write_json(OUT_DIR / "keys.json", {"keys": ordered})
    write_json(
        OUT_DIR / "images.json",
        {
            "images": all_images,
            "imageToUses": image_to_uses,
        },
    )

    # Seed v1 quiz items: pick images that are used in an outcome with outcomeText.
    items: List[Dict[str, Any]] = []
    for img in all_images:
        if is_placeholder_path(img):
            continue
        uses = image_to_uses.get(img, [])
        outcome_uses = [u for u in uses if u.get("kind") == "outcome" and u.get("outcomeText")]
        if not outcome_uses:
            continue
        u0 = outcome_uses[0]
        w0 = u0.get("imageWidthPx")
        if not isinstance(w0, (int, float)) or not (w0 and w0 > 0):
            w0 = None

        expected_path = None
        kp = key_paths_map.get(u0.get("keyJsonUrl"))
        if kp and kp.exists():
            try:
                paths = compute_paths_for_key(kp)
                expected_path = paths.get((str(u0.get("stepId")), int(u0.get("choiceIdx"))))
            except Exception:
                expected_path = None
        if not expected_path:
            expected_path = [
                {
                    "stepId": u0["stepId"],
                    "choiceIdx": u0["choiceIdx"],
                    "choiceLabel": u0["choiceLabel"],
                }
            ]
        items.append(
            {
                "image": img,
                "imageWidthPx": w0,
                "strict": {
                    "endpointText": u0["outcomeText"],
                    "keyJsonUrl": u0["keyJsonUrl"],
                },
                "accepted": [
                    {"endpointText": u["outcomeText"], "grade": "acceptable"}
                    for u in outcome_uses[:5]
                    if u.get("outcomeText")
                ],
                "expectedPath": expected_path,
                "distractors": [],
            }
        )

    write_json(OUT_DIR / "palynoquest-items.json", {"items": items})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

