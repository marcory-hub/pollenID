#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYS_DIR = DOCS_DIR / "keys"
IMAGES_DIR = DOCS_DIR / "assets" / "images"
OUT_DIR = DOCS_DIR / "assets" / "manifests"
KEYS_INDEX_MD = DOCS_DIR / "Identificatiesleutels" / "_index.md"
POLLEN_YAML = REPO_ROOT / "data" / "pollen.yaml"
POLLEN_JSON = DOCS_DIR / "data" / "pollen.json"


def pollen_slug_normalized(raw: Any) -> Optional[str]:
    if not isinstance(raw, str):
        return None
    s = raw.strip()
    if not s or s == "-":
        return None
    return s


def load_pollen_json_assets(json_path: Path = POLLEN_JSON) -> Dict[str, List[Tuple[str, Optional[float]]]]:
    """Slug → normalized docs asset paths for images (+ optional height_px as sizing proxy)."""
    if not json_path.exists():
        return {}
    try:
        data = read_json(json_path)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    out: Dict[str, List[Tuple[str, Optional[float]]]] = {}
    for slug, rec in data.items():
        if not isinstance(rec, dict):
            continue
        sk = pollen_slug_normalized(str(slug))
        if not sk:
            continue
        imgs = rec.get("images")
        if not isinstance(imgs, list):
            continue
        tuples: List[Tuple[str, Optional[float]]] = []
        for im in imgs:
            if not isinstance(im, dict):
                continue
            rel = normalize_docs_asset_path(im.get("path"))
            if not rel:
                continue
            hp = im.get("height_px")
            w_proxy: Optional[float] = float(hp) if isinstance(hp, (int, float)) and hp > 0 else None
            tuples.append((rel, w_proxy))
        if tuples:
            out[sk] = tuples
    return out


# PalynoQuest quiz items only use images from identification keys excluding Beug (Beug deferred).
PALYNOQUEST_BEUG_JSON_PREFIX = "keys/beug/"
# Same image may appear under several JSON keys; canonical sleutel order (Kerkvliet → Van der Ham → Reitsma → Eide → rest).
PALYNOQUEST_KEY_PRIORITY_ORDER: List[str] = [
    "keys/kerkvliet/kerkvliet-determinatietabel.json",
    "keys/vanderham/vanderham-pollentabel.json",
    "keys/reitsma/rosaceae-reitsma.json",
    "keys/eide/rosaceae-eide.json",
]


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


def is_sem_em_png_path(rel: str) -> bool:
    """True when the filename indicates a PalDat-style SEM raster (quiz uses LM views)."""
    if not isinstance(rel, str):
        return False
    seg = Path(rel).name
    return seg.endswith("EM.png")


def palynoquest_key_allowed(key_json_url: Optional[str]) -> bool:
    if not isinstance(key_json_url, str) or not key_json_url.strip():
        return False
    url = key_json_url.strip().lstrip("./").replace("\\", "/")
    return not url.startswith(PALYNOQUEST_BEUG_JSON_PREFIX)


def palynoquest_key_priority_rank(key_json_url: Optional[str]) -> int:
    if not isinstance(key_json_url, str):
        return len(PALYNOQUEST_KEY_PRIORITY_ORDER)
    url = key_json_url.strip().lstrip("./").replace("\\", "/")
    try:
        return PALYNOQUEST_KEY_PRIORITY_ORDER.index(url)
    except ValueError:
        return len(PALYNOQUEST_KEY_PRIORITY_ORDER)


def sort_palynoquest_outcomes(outcomes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        outcomes,
        key=lambda u: (
            palynoquest_key_priority_rank(str(u.get("keyJsonUrl")) if u.get("keyJsonUrl") is not None else None),
            str(u.get("stepId") or ""),
            int(u.get("choiceIdx") or 0),
        ),
    )


def is_bad_outcome_placeholder(text: Optional[str]) -> bool:
    if text is None:
        return True
    t = str(text).strip()
    return t == "" or t == "-"


def md_link_plain(s: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s).strip()


def strip_leading_key_number(s: str) -> str:
    """Strip leading '4.10.1 '-style prefixes from key outcome headings."""
    s = s.strip()
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"^(\d+\.)+\d*\s+", "", s).strip()
    return s


def load_pollen_key_labels(path: Path) -> Dict[str, str]:
    """Map pollen.yaml record key (e.g. agrimonia_eupatoria) to Latin (Dutch) label strings."""
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    out: Dict[str, str] = {}
    for slug, rec in raw.items():
        if not isinstance(rec, dict):
            continue
        sk = str(slug)
        latin = rec.get("latin")
        if not isinstance(latin, str) or not latin.strip():
            continue
        dutch = rec.get("dutch")
        d = dutch.strip() if isinstance(dutch, str) else ""
        if d and d not in ("-", "–", "—", "…"):
            out[sk] = f"{latin.strip()} ({d})"
        else:
            out[sk] = latin.strip()
    return out


def resolve_outcome_display(out: dict, pollen_labels: Dict[str, str]) -> Optional[str]:
    """
    Build a single human-readable endpoint string for PalynoQuest from a choice `id` / `outcome` dict.
    Order: explicit text (if meaningful) → pollen_key via pollen.yaml → cleaned `name` (markdown heading).
    """
    raw_text = out.get("text")
    if isinstance(raw_text, str):
        t = raw_text.strip()
        if t and t != "-":
            return t

    pk = out.get("pollen_key")
    if isinstance(pk, str):
        p = pk.strip()
        if p and p != "-":
            lbl = pollen_labels.get(p)
            if lbl:
                return lbl

    nm = out.get("name")
    if isinstance(nm, str):
        s = md_link_plain(nm)
        s = strip_leading_key_number(s)
        if s and s != "-":
            return s
    return None


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


def extract_from_key_json(
    key_json_path: Path,
    pollen_labels: Dict[str, str],
    pollen_assets: Dict[str, List[Tuple[str, Optional[float]]]],
) -> Tuple[Dict[str, Any], Dict[str, List[ImageUse]]]:
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
                outcome_text = resolve_outcome_display(out, pollen_labels)
                imgs_from_choice = list(extract_images_from_node(out, base_dir))
                if not imgs_from_choice:
                    slug = pollen_slug_normalized(out.get("pollen_key"))
                    if slug and slug in pollen_assets:
                        imgs_from_choice = pollen_assets.get(slug) or []
                for image, _w in imgs_from_choice:
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


def normalize_docs_asset_path(rel: Any) -> Optional[str]:
    if not isinstance(rel, str):
        return None
    r = rel.strip().lstrip("./").replace("\\", "/")
    if not r or is_placeholder_path(r):
        return None
    try:
        p = Path(r)
        if (DOCS_DIR / p).is_file():
            return norm_rel_posix(p)
    except (OSError, ValueError):
        return None
    return None


def kerkvliet_row_endpoint_label(row: Dict[str, Any]) -> Optional[str]:
    lat = md_link_plain(str(row.get("latin") or "")).strip()
    nl = md_link_plain(str(row.get("dutch") or "")).strip()
    if not lat and not nl:
        return None
    if lat and nl:
        return f"{lat} ({nl})"
    return lat or nl


def items_from_kerkvliet_determinatietabel(
    json_path: Path,
    key_json_url: str,
    *,
    pollen_labels: Dict[str, str],
    pollen_assets: Dict[str, List[Tuple[str, Optional[float]]]],
) -> List[Dict[str, Any]]:
    """
    Determinatietabel (Kerkvliet): flat rows met images[]. Geen dichotomisch steps-bestand —
    daarom apart van extract_from_key_json.
    """
    if not json_path.exists():
        return []
    try:
        data = read_json(json_path)
    except Exception:
        return []
    rows = data.get("rows")
    if not isinstance(rows, list):
        return []

    seen_image: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        if not isinstance(row, dict):
            continue
        slug = pollen_slug_normalized(row.get("pollen_key"))
        label = kerkvliet_row_endpoint_label(row)
        if not label and slug:
            lbl = pollen_labels.get(slug)
            if lbl:
                label = lbl
        if not label:
            continue

        imgs = row.get("images")
        imgs_list = imgs if isinstance(imgs, list) else []

        if not imgs_list and slug and slug in pollen_assets:
            for docs_rel, hp in pollen_assets.get(slug) or []:
                iw = int(hp) if isinstance(hp, (int, float)) and hp > 0 else None
                seen_image[docs_rel] = {
                    "image": docs_rel,
                    "imageWidthPx": iw,
                    "strict": {"endpointText": label, "keyJsonUrl": key_json_url},
                    "accepted": [{"endpointText": label, "grade": "acceptable"}],
                    "expectedPath": [],
                    "distractors": [],
                }
            continue

        if not imgs_list:
            continue

        for im in imgs_list:
            if not isinstance(im, dict):
                continue
            rel_raw = im.get("image")
            docs_rel = normalize_docs_asset_path(rel_raw)
            if not docs_rel or is_sem_em_png_path(docs_rel):
                continue
            wp = im.get("imageWidthPx")
            hp = im.get("imageHeightPx")
            w0: Optional[float] = None
            if isinstance(wp, (int, float)) and wp > 0:
                w0 = float(wp)
            elif isinstance(hp, (int, float)) and hp > 0:
                w0 = float(hp)
            iw = int(w0) if w0 is not None else None

            seen_image[docs_rel] = {
                "image": docs_rel,
                "imageWidthPx": iw,
                "strict": {"endpointText": label, "keyJsonUrl": key_json_url},
                "accepted": [{"endpointText": label, "grade": "acceptable"}],
                "expectedPath": [],
                "distractors": [],
            }

    return sorted(seen_image.values(), key=lambda x: str(x["image"]))


def _unique_accepted(outcome_uses: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, str]]:
    seen: set[str] = set()
    out: List[Dict[str, str]] = []
    for u in outcome_uses:
        t = u.get("outcomeText")
        if not isinstance(t, str) or is_bad_outcome_placeholder(t):
            continue
        if t in seen:
            continue
        seen.add(t)
        out.append({"endpointText": t, "grade": "acceptable"})
        if len(out) >= limit:
            break
    return out


def main() -> int:
    pollen_labels = load_pollen_key_labels(POLLEN_YAML)
    pollen_assets = load_pollen_json_assets()
    key_paths = sorted(KEYS_DIR.rglob("*.json"))
    keys: List[Dict[str, Any]] = []
    image_to_uses: Dict[str, List[Dict[str, Any]]] = {}
    key_paths_map: Dict[str, Path] = {}

    for kp in key_paths:
        try:
            key_info, image_map = extract_from_key_json(kp, pollen_labels, pollen_assets)
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

    # Quiz items: images that appear on an endpoint with a resolved label (not "-" / empty).
    items: List[Dict[str, Any]] = []
    for img in all_images:
        if is_placeholder_path(img):
            continue
        if is_sem_em_png_path(img):
            continue
        uses = image_to_uses.get(img, [])
        outcome_uses_raw = [
            u
            for u in uses
            if u.get("kind") == "outcome"
            and u.get("outcomeText")
            and not is_bad_outcome_placeholder(u.get("outcomeText"))
        ]
        outcome_uses = [
            u for u in outcome_uses_raw if palynoquest_key_allowed(u.get("keyJsonUrl"))
        ]
        outcome_uses = sort_palynoquest_outcomes(outcome_uses)
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
                "accepted": _unique_accepted(outcome_uses, limit=5),
                "expectedPath": expected_path,
                "distractors": [],
            }
        )

    # Kerkvliet-determinatietabel is geen vdh-steps JSON; plaatjes + labels apart verzameld.
    # Bij dezelfde afbeelding wint deze bron (prioriteit hoger dan Reitsma/Eide enz.).
    kerkv_json = KEYS_DIR / "kerkvliet" / "kerkvliet-determinatietabel.json"
    kerk_url = norm_rel_posix(kerkv_json.relative_to(DOCS_DIR))
    kerk_items = items_from_kerkvliet_determinatietabel(
        kerkv_json,
        key_json_url=kerk_url,
        pollen_labels=pollen_labels,
        pollen_assets=pollen_assets,
    )

    merged: Dict[str, Dict[str, Any]] = {}
    for it in items:
        merged[str(it["image"])] = it
    for it in kerk_items:
        merged[str(it["image"])] = it

    items = sorted(merged.values(), key=lambda x: str(x.get("image") or ""))

    write_json(OUT_DIR / "palynoquest-items.json", {"items": items})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

