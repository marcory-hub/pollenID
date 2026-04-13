#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import unicodedata
from typing import Any, Dict, List, Optional
import struct
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_IMAGES = DOCS_DIR / "assets" / "images"
IMAGES_MANIFEST = DOCS_DIR / "assets" / "manifests" / "images.json"
KERK_JSON = DOCS_DIR / "keys" / "kerkvliet" / "kerkvliet-determinatietabel.json"

BINOMIAL_RE = re.compile(r"\b([A-Z][a-z]+)\s+([a-z][a-z-]+)\b")
POLLENWIKI_TITLE_RE = re.compile(r"https?://pollen\.tstebler\.ch/MediaWiki/index\.php\?title=([^)\s]+)", re.IGNORECASE)
PALDAT_PUB_RE = re.compile(r"https?://www\.paldat\.org/pub/([^)\s]+)", re.IGNORECASE)
POLLENWIKI_MD_LINK_RE = re.compile(r"\[pollenwiki\]\([^)]+\)", re.IGNORECASE)
GENUS_ONLY_RE = re.compile(r"^([A-Z][a-z]+)(?:\s+sp\.?)?$")

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: Any) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_md_links(s: str) -> str:
    # Replace [label](url) with label
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)


def extract_binomial(s: str) -> Optional[str]:
    if not isinstance(s, str):
        return None
    s = strip_md_links(s)
    m = BINOMIAL_RE.search(s)
    if not m:
        return None
    return f"{m.group(1)}_{m.group(2)}"


def extract_pollenwiki_title(s: str) -> Optional[str]:
    if not isinstance(s, str):
        return None
    m = POLLENWIKI_TITLE_RE.search(s)
    if not m:
        return None
    title = m.group(1).strip()
    return title or None


def extract_paldat_pub_slug(s: str) -> Optional[str]:
    """
    Extract the paldat.org pub slug, e.g. "Myosotis_scorpioides" from:
    "[Myosotis](https://www.paldat.org/pub/Myosotis_scorpioides)"
    """
    if not isinstance(s, str):
        return None
    m = PALDAT_PUB_RE.search(s)
    if not m:
        return None
    slug = m.group(1).strip().strip("/")
    return slug or None


def candidate_images(prefix: str) -> List[str]:
    # Search all supported raster formats.
    out: List[str] = []
    if not prefix:
        return out
    for ext in ("png", "jpg", "jpeg", "webp"):
        out.extend([p.as_posix() for p in ASSETS_IMAGES.rglob(f"{prefix}_*.{ext}")])
    # Filter placeholders
    out = [p for p in out if "PLACEHOLDER" not in p.upper()]
    out.sort()
    # Convert to docs-relative paths.
    rel = []
    for p in out:
        try:
            rel.append(Path(p).resolve().relative_to(DOCS_DIR).as_posix())
        except Exception:
            continue
    return rel


def strip_known_nonlatin_tokens(s: str) -> str:
    """
    Remove known inline link tokens that may remain after strip_md_links,
    e.g. "[pollenwiki](...)".
    """
    if not isinstance(s, str):
        return ""
    return POLLENWIKI_MD_LINK_RE.sub("", s).strip()


def normalize_id(s: str) -> str:
    """
    Normalize identifiers for fuzzy matching:
    - NFKD decompose and drop diacritics (Hippophaë -> Hippophae)
    - lower-case
    - keep only [a-z0-9_]
    - collapse runs of '_' and strip edges
    """
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("-", "_")
    s = s.lower()
    s = re.sub(r"[^a-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def build_existing_image_index() -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Build:
    - prefix_to_images: exact prefix -> docs-relative image paths (sorted)
    - norm_prefix_to_prefixes: normalized prefix -> list of exact prefixes

    Prefix heuristics:
    - For 'Myosotis_scorpioides_Eo.png' => prefix 'Myosotis_scorpioides'
    - Also include the full stem as a prefix for single-token names like 'Pinus_silvestris.png'
    """
    prefix_to_images: Dict[str, List[str]] = {}
    norm_prefix_to_prefixes: Dict[str, List[str]] = {}

    if not ASSETS_IMAGES.exists():
        return prefix_to_images, norm_prefix_to_prefixes

    for img in ASSETS_IMAGES.rglob("*"):
        if not img.is_file():
            continue
        if img.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        if "PLACEHOLDER" in img.name.upper():
            continue

        try:
            rel = img.resolve().relative_to(DOCS_DIR).as_posix()
        except Exception:
            continue

        stem = img.stem
        prefixes = {stem}
        if "_" in stem:
            prefixes.add(stem.rsplit("_", 1)[0])

        for pfx in prefixes:
            prefix_to_images.setdefault(pfx, []).append(rel)

    # Sort and de-dupe lists
    for pfx, paths in list(prefix_to_images.items()):
        dedup = sorted(set(paths))
        prefix_to_images[pfx] = dedup
        np = normalize_id(pfx)
        if not np:
            continue
        norm_prefix_to_prefixes.setdefault(np, []).append(pfx)

    # Sort prefixes deterministically
    for np, pfxs in list(norm_prefix_to_prefixes.items()):
        norm_prefix_to_prefixes[np] = sorted(set(pfxs))

    return prefix_to_images, norm_prefix_to_prefixes


def pick_best_prefix(
    raw_prefix: str,
    prefix_to_images: Dict[str, List[str]],
    norm_prefix_to_prefixes: Dict[str, List[str]],
) -> Optional[str]:
    if not raw_prefix:
        return None

    # 1) Exact prefix
    if raw_prefix in prefix_to_images:
        return raw_prefix

    # 2) Normalized exact prefix
    np = normalize_id(raw_prefix)
    if np and np in norm_prefix_to_prefixes:
        # If multiple exact prefixes normalize to the same key, only accept if unambiguous.
        pfxs = norm_prefix_to_prefixes[np]
        if len(pfxs) == 1:
            return pfxs[0]

    # 3) Truncation cleanup: strip trailing '.' and retry (e.g. Acer_pseudoplat.)
    cleaned = raw_prefix.strip().strip(".")
    if cleaned and cleaned != raw_prefix:
        best = pick_best_prefix(cleaned, prefix_to_images, norm_prefix_to_prefixes)
        if best:
            return best

    # 4) Safe genus fallback: only if exactly one unique species-prefix exists for that genus.
    # Example: raw 'Campanula' may map to 'Campanula_rotundifolia' if that is the only Campanula_* prefix.
    genus = cleaned.split("_", 1)[0] if cleaned else ""
    ng = normalize_id(genus)
    if ng:
        candidates: set[str] = set()
        for npfx, pfxs in norm_prefix_to_prefixes.items():
            if npfx == ng or npfx.startswith(ng + "_"):
                candidates.update(pfxs)
        # Prefer "Genus_species" style prefixes over the bare genus stem.
        candidates2 = {c for c in candidates if "_" in c}
        if len(candidates2) == 1:
            return sorted(candidates2)[0]
        if len(candidates2) == 0 and len(candidates) == 1:
            return sorted(candidates)[0]

    return None


def candidate_images_from_index(best_prefix: str, prefix_to_images: Dict[str, List[str]]) -> List[str]:
    if not best_prefix:
        return []
    return list(prefix_to_images.get(best_prefix, []))


def genus_images(genus: str) -> List[str]:
    """
    For Kerkvliet rows that only say "Genus" / "Genus sp":
    attach all available Genus_* images.
    """
    out: List[str] = []
    genus = (genus or "").strip()
    if not genus:
        return out
    if not ASSETS_IMAGES.exists():
        return out
    for ext in ("png", "jpg", "jpeg", "webp"):
        out.extend([p.as_posix() for p in ASSETS_IMAGES.rglob(f"{genus}_*.{ext}")])
    out = [p for p in out if "PLACEHOLDER" not in p.upper()]
    rel: List[str] = []
    for p in out:
        try:
            rel.append(Path(p).resolve().relative_to(DOCS_DIR).as_posix())
        except Exception:
            continue
    return sorted(set(rel))


def extract_genus_if_genus_only(latin_raw: str) -> Optional[str]:
    if not isinstance(latin_raw, str):
        return None
    s = strip_md_links(latin_raw)
    s = strip_known_nonlatin_tokens(s)
    s = re.sub(r"\s+", " ", s).strip()
    m = GENUS_ONLY_RE.match(s)
    if not m:
        return None
    return m.group(1)


PLACEHOLDER_IMAGES: List[Dict[str, Any]] = [
    {"image": "assets/images/pollenwiki/PLACEHOLDER_Eo.png", "imageWidthPx": 72},
    {"image": "assets/images/pollenwiki/PLACEHOLDER_Pd.png", "imageWidthPx": 72},
    {"image": "assets/images/pollenwiki/PLACEHOLDER_Po.png", "imageWidthPx": 72},
    # Only three distinct placeholders exist; duplicate Eo to satisfy "4 images".
    {"image": "assets/images/pollenwiki/PLACEHOLDER_Eo.png", "imageWidthPx": 72},
]


def set_placeholder_images(row: Dict[str, Any]) -> None:
    row["images"] = list(PLACEHOLDER_IMAGES)


def png_dimensions_px(p: Path) -> Optional[tuple[int, int]]:
    try:
        with p.open("rb") as f:
            sig = f.read(8)
            if sig != PNG_SIG:
                return None
            # First chunk should be IHDR: length(4) + type(4) + data(13) + crc(4)
            _len = f.read(4)
            ctype = f.read(4)
            if ctype != b"IHDR":
                return None
            ihdr = f.read(13)
            if len(ihdr) != 13:
                return None
            w, h = struct.unpack(">II", ihdr[:8])
            if w <= 0 or h <= 0:
                return None
            return int(w), int(h)
    except Exception:
        return None


def derive_width_px_from_image(img_docs_rel: str, target_height_px: int) -> Optional[int]:
    """
    Compute a width that yields ~target_height_px when rendered with width set and height:auto.
    Only implemented for PNG to avoid external dependencies.
    """
    if not isinstance(img_docs_rel, str) or not img_docs_rel:
        return None
    p = (DOCS_DIR / img_docs_rel).resolve()
    if not p.exists():
        return None
    if p.suffix.lower() != ".png":
        return None
    dims = png_dimensions_px(p)
    if not dims:
        return None
    w_px, h_px = dims
    if h_px <= 0:
        return None
    w = int(round(w_px * (float(target_height_px) / float(h_px))))
    return w if w > 0 else None


def build_image_width_index() -> Dict[str, int]:
    """
    Best-effort mapping: docs-relative image path -> max imageWidthPx seen in manifests.
    """
    if not IMAGES_MANIFEST.exists():
        return {}
    data = read_json(IMAGES_MANIFEST)
    it = data.get("imageToUses")
    if not isinstance(it, dict):
        return {}
    out: Dict[str, int] = {}
    for img, uses in it.items():
        if not isinstance(img, str) or not isinstance(uses, list):
            continue
        maxw = None
        for u in uses:
            if not isinstance(u, dict):
                continue
            w = u.get("imageWidthPx")
            if isinstance(w, (int, float)) and w > 0:
                if maxw is None or w > maxw:
                    maxw = w
        if maxw is not None:
            out[img] = int(round(maxw))
    return out


def main() -> int:
    width_idx = build_image_width_index()
    prefix_to_images, norm_prefix_to_prefixes = build_existing_image_index()
    data = read_json(KERK_JSON)
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise SystemExit("rows missing or not a list")

    changed = 0
    with_images = 0

    for r in rows:
        if not isinstance(r, dict):
            continue
        if "images" in r and isinstance(r["images"], list) and len(r["images"]) > 0:
            with_images += 1
            continue

        latin = r.get("latin") or ""
        dutch = r.get("dutch") or ""

        # Explicit rule requested by user: for genus-only rows ("Genus" / "Genus sp."),
        # attach all Genus_* images.
        imgs: List[str] = []
        genus = extract_genus_if_genus_only(str(latin))
        if genus:
            imgs = genus_images(genus)

        prefix = extract_binomial(str(latin))
        if not prefix:
            # Prefer identifiers already present in links.
            prefix = (
                extract_paldat_pub_slug(str(latin))
                or extract_pollenwiki_title(str(dutch))
                or extract_pollenwiki_title(str(latin))
            )
        if not imgs:
            best_prefix = pick_best_prefix(prefix or "", prefix_to_images, norm_prefix_to_prefixes) if prefix else None
            imgs = candidate_images_from_index(best_prefix, prefix_to_images) if best_prefix else []
        if not imgs:
            # Explicit rule requested by user: every row should have 4 images;
            # use placeholders when nothing matches.
            set_placeholder_images(r)
            changed += 1
            with_images += 1
            continue

        # Use up to 4 images; use width from manifest when available, else derive from pixel
        # dimensions (targeting same height as the first published galleries).
        ims = []
        target_height_px = 20
        for p in imgs:
            w = width_idx.get(p)
            if not (isinstance(w, int) and w > 0):
                w = derive_width_px_from_image(p, target_height_px)
            ims.append({"image": p, "imageWidthPx": w if isinstance(w, int) and w > 0 else 72})
        r["images"] = ims
        changed += 1
        with_images += 1

    if changed:
        write_json(KERK_JSON, data)

    print(f"rows_with_images={with_images} rows_newly_enriched={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

