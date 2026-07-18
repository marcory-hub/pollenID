"""Shared helpers for pollen image paths, filename stems, and YAML slug resolution."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
IMAGES_DIR = DOCS_DIR / "assets" / "images"
POLLEN_YAML = REPO_ROOT / "data" / "pollen.yaml"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}

# Matches _ed, _eo2, _d, _o, _p, _e, _26, etc. after normalization.
_RE_STRIP_TOKEN = re.compile(
    r"_(?:"
    r"ed|eo\d*|em\d*|pd|po\d*|om|d\d*|o\d*|e\d*|p\d*"
    r")$",
    re.IGNORECASE,
)

_RE_SIZE_SUFFIX = re.compile(
    r"_(?:size[_\d]*(?:um|µm|u_m)?|\d+um)$",
    re.IGNORECASE,
)

_RE_TRAILING_NUM = re.compile(r"_\d+$", re.IGNORECASE)


def norm_rel_posix(p: Path, base: Path = DOCS_DIR) -> str:
    return p.resolve().relative_to(base.resolve()).as_posix()


def load_pollen_yaml_dict(path: Path = POLLEN_YAML) -> Dict[str, Any]:
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def latin_to_pollen_slug(latin: str) -> str:
    """Approximate slug from latin binomial (same idea as scripts/merge_pollen.latin_to_id)."""
    s = latin.strip()
    s = s.replace("*", "").replace("_", " ")
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = s.replace("×", "x")
    s = re.sub(r"[()]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    s = re.sub(r"_+", "_", s)
    return s


def stems_from_pollen_key(key: str) -> Set[str]:
    k = key.strip().lower().replace("-", "_")
    k = re.sub(r"_+", "_", k).strip("_")
    out = {k}
    return out


def normalize_image_stem(raw_stem: str) -> str:
    """Reduce a filename stem toward a pollen_key-like token."""
    s = raw_stem.strip().lower().replace("-", "_")
    s = s.replace("+", "_")
    s = re.sub(r"_+", "_", s).strip("_")
    # Underscore-only artifacts
    s = re.sub(r"^_+$", "", s) or s
    changed = True
    while changed:
        changed = False
        before = s
        s = _RE_SIZE_SUFFIX.sub("", s)
        m = _RE_STRIP_TOKEN.search(s)
        if m:
            s = s[: m.start()].rstrip("_")
        s = _RE_TRAILING_NUM.sub("", s)
        s = re.sub(r"_+", "_", s).strip("_")
        if s != before:
            changed = True
    # trim trailing orphan underscores from names like Eucalyptus_
    s = s.rstrip("_")
    return s


def yaml_image_paths(entry: Any) -> List[str]:
    if not isinstance(entry, dict):
        return []
    imgs = entry.get("images")
    if not isinstance(imgs, list):
        return []
    out: List[str] = []
    for im in imgs:
        if isinstance(im, dict):
            p = im.get("path")
            if isinstance(p, str) and p.strip():
                out.append(p.strip().lstrip("./").replace("\\", "/"))
    return out


def iter_image_files(root: Path = IMAGES_DIR) -> List[Path]:
    if not root.exists():
        return []
    out: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            out.append(p)
    out.sort(key=lambda x: x.as_posix().lower())
    return out


def build_pollen_indexes(
    data: Dict[str, Any],
) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """Return (slug_to_key, stem_to_keys) for disambiguation."""
    slug_to_key: Dict[str, str] = {}
    stem_to_keys: Dict[str, List[str]] = {}

    for key, entry in data.items():
        if not isinstance(key, str) or not isinstance(entry, dict):
            continue
        sk = key.strip()
        for st in stems_from_pollen_key(sk):
            stem_to_keys.setdefault(st, []).append(sk)

        from pollen_display import entry_latin

        lat = entry_latin(entry)
        if isinstance(lat, str) and lat.strip():
            slug = latin_to_pollen_slug(lat)
            if slug:
                slug_to_key.setdefault(slug, sk)
                stem_to_keys.setdefault(slug, []).append(sk)
            parts = slug.split("_") if slug else []
            if len(parts) >= 2:
                binomial = "_".join(parts[:2])
                slug_to_key.setdefault(binomial, sk)
                stem_to_keys.setdefault(binomial, []).append(sk)

    for k, keys in list(stem_to_keys.items()):
        stem_to_keys[k] = sorted(set(keys))
    return slug_to_key, stem_to_keys


def resolve_pollen_key_for_stem(
    stem_norm: str,
    *,
    stem_to_keys: Dict[str, List[str]],
    slug_to_key: Dict[str, str],
) -> Tuple[str, List[str]]:
    """Return ('confident'|'ambiguous'|'none', [keys])."""
    if not stem_norm:
        return "none", []

    if stem_norm in stem_to_keys and len(stem_to_keys[stem_norm]) == 1:
        return "confident", stem_to_keys[stem_norm]

    if stem_norm in slug_to_key:
        k = slug_to_key[stem_norm]
        return "confident", [k]

    # Longest stem prefix match to exactly one yaml key (handles typos in extra tokens).
    matches: List[str] = []
    if stem_norm in stem_to_keys:
        matches = stem_to_keys[stem_norm]
    else:
        best_len = 0
        for cand_stem, keys in stem_to_keys.items():
            if stem_norm == cand_stem or stem_norm.startswith(cand_stem + "_"):
                if len(cand_stem) > best_len:
                    best_len = len(cand_stem)
                    matches = keys
        matches = sorted(set(matches))

    if len(matches) == 1:
        return "confident", matches
    if len(matches) > 1:
        return "ambiguous", matches
    return "none", []


def image_file_to_docs_path(path: Path) -> str:
    return norm_rel_posix(path, DOCS_DIR)


def is_under_by_taxon(rel: str) -> bool:
    return rel.replace("\\", "/").startswith("assets/images/by-taxon/")
