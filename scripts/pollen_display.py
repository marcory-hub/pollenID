"""Shared helpers for pollen display width (px) and external atlas URLs.

Used by export_pollen_json.py and MkDocs macros (main.py) via sys.path.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

RE_NUM = re.compile(r"\d+(?:\.\d+)?")


def parse_max_um_from_size_strings(smallest: Optional[str], largest: Optional[str]) -> Optional[float]:
    """Largest numeric dimension (µm) found in YAML size strings (mirrors kerkvliet parseMaxUm spirit)."""
    raw = f"{(smallest or '').strip()} {(largest or '').strip()}".strip()
    if not raw:
        return None
    s = (
        raw.replace(",", ".")
        .replace("µ", "u")
        .replace("μm", " ")
        .replace("um", " ")
    )
    s = re.sub(r"[^\d.x\-()/\s]+", " ", s)
    nums = RE_NUM.findall(s)
    if not nums:
        return None
    max_v: Optional[float] = None
    for n in nums:
        try:
            v = float(n)
        except ValueError:
            continue
        if max_v is None or v > max_v:
            max_v = v
    return max_v


def display_width_px_from_max_um(max_um: Optional[float], *, default_um: float = 50.0) -> int:
    """Display width in px: round(largest_um * 2.5), default 50 µm => 125 px."""
    u = max_um if max_um is not None and max_um > 0 else default_um
    return int(round(2.5 * u))


def latin_binomial_underscore(latin: str) -> Optional[str]:
    """Genus_epitheton for external URLs (e.g. Abeliophyllum_distichum)."""
    if not isinstance(latin, str) or not latin.strip():
        return None
    s = latin.strip()
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = s.replace("×", "x")
    s = re.sub(r"[()*]", " ", s)
    parts = [p for p in re.split(r"\s+", s) if p and re.match(r"^[A-Za-z]", p)]
    if len(parts) < 2:
        return None
    genus = parts[0].strip()
    epit = parts[1].strip().lower().rstrip(".")
    if not genus or not epit:
        return None
    g0 = genus[0].upper() + genus[1:].lower() if len(genus) > 1 else genus.upper()
    return f"{g0}_{epit}"


def default_external_links(latin: str) -> Dict[str, str]:
    slug = latin_binomial_underscore(latin)
    if not slug:
        return {}
    return {
        "pollenx": f"https://pollenx.eu/species.php?species={slug}",
        "tstebler": f"https://pollen.tstebler.ch/MediaWiki/index.php?title={slug}",
        "paldat": f"https://www.paldat.org/pub/{slug}",
    }


def merge_links_yaml_defaults(latin: str, links_yaml: Any) -> Dict[str, Optional[str]]:
    """Return link keys pollenx, tstebler, paldat — None means omit from JSON."""
    base = default_external_links(latin)
    out: Dict[str, Optional[str]] = {
        "pollenx": base.get("pollenx"),
        "tstebler": base.get("tstebler"),
        "paldat": base.get("paldat"),
    }
    if not isinstance(links_yaml, dict):
        return out
    yaml_by_canonical = {
        "pollenx": links_yaml.get("pollenx", links_yaml.get("pollenX")),
        "tstebler": links_yaml.get("tstebler"),
        "paldat": links_yaml.get("paldat"),
    }
    for k in ("pollenx", "tstebler", "paldat"):
        if k not in yaml_by_canonical:
            continue
        v = yaml_by_canonical.get(k)
        if v is False or v is None or v == "":
            out[k] = None
        elif isinstance(v, str) and v.strip():
            out[k] = v.strip()
    return out


def display_width_px_for_yaml_entry(entry: Dict[str, Any]) -> int:
    """Single display width for a taxon from size + legacy height_px fallback."""
    legacy_px = None

    size_src = entry.get("size") or {}
    ss = ls = None
    if isinstance(size_src, dict):
        h = size_src.get("height_px")
        if isinstance(h, int) and h > 0:
            legacy_px = h
        elif isinstance(h, float) and h > 0:
            legacy_px = int(round(h))
        ss = size_src.get("smallest_size")
        ls = size_src.get("largest_size")
        if isinstance(ss, str):
            ss = ss.strip() or None
        else:
            ss = None
        if isinstance(ls, str):
            ls = ls.strip() or None
        else:
            ls = None

    max_um = parse_max_um_from_size_strings(ss, ls)
    if max_um is not None and max_um > 0:
        return display_width_px_from_max_um(max_um)
    if legacy_px is not None:
        return legacy_px
    return display_width_px_from_max_um(None)


def per_image_width_px(im: Dict[str, Any], entry_default: int) -> int:
    w = im.get("width_px")
    if isinstance(w, int) and w > 0:
        return w
    if isinstance(w, float) and w > 0:
        return int(round(w))
    h = im.get("height_px")
    if isinstance(h, int) and h > 0:
        return h
    if isinstance(h, float) and h > 0:
        return int(round(h))
    return entry_default
