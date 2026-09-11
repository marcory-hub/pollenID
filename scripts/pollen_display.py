"""Shared helpers for pollen display width (px) and external atlas URLs.

Used by export_pollen_json.py and MkDocs macros (scripts/mkdocs_macros.py) via sys.path.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional
from urllib.parse import quote_plus

RE_NUM = re.compile(r"\d+(?:\.\d+)?")

# LM/EM visibility for sculpture / aperture / ornamentation (data/pollen.yaml).
VISIBILITY_LABELS_NL: Dict[str, str] = {
    "lm_clear": "goed zichtbaar met LM",
    "lm_poor": "matig zichtbaar met LM",
    "em_only": "alleen zichtbaar met EM",
}
VISIBILITY_CODES = frozenset(VISIBILITY_LABELS_NL)
VISIBILITY_FIELDS = (
    "sculpture_visibility",
    "aperture_visibility",
    "ornamentation_visibility",
)

# Legacy macro/script field paths → nested SoT paths in data/pollen.yaml.
FIELD_ALIASES: Dict[str, str] = {
    "latin": "name.latin_name",
    "dutch": "name.dutch_name",
    "family": "classification.family_latin",
    "family_latin": "classification.family_latin",
    "family_dutch": "classification.family_dutch",
    "shape": "pollen_features.shape",
    "sculpture": "pollen_features.sculpture",
    "sculpture_visibility": "pollen_features.sculpture_visibility",
    "aperture": "pollen_features.aperture",
    "aperture_visibility": "pollen_features.aperture_visibility",
    "ornamentation": "pollen_features.ornamentation",
    "ornamentation_visibility": "pollen_features.ornamentation_visibility",
    "polarity": "pollen_features.polarity",
    "pe_ratio": "pollen_features.pe_ratio",
    "pollen-note": "pollen_features.pollen-note",
    "pollen_class": "pollen_class_beug",
    "nectar_value": "value.nectar_value",
    "pollen_value": "value.pollen_value",
    "note": "note.note_plant",
    "size.smallest_size": "size.size_smallest",
    "size.largest_size": "size.size_largest",
}


def get_dotted(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def resolve_pollen_field(entry: Dict[str, Any], field: str) -> Any:
    """Resolve a field path, accepting legacy flat aliases."""
    if not isinstance(entry, dict) or not field:
        return None
    direct = get_dotted(entry, field)
    if direct is not None:
        return direct
    alias = FIELD_ALIASES.get(field)
    if alias:
        return get_dotted(entry, alias)
    return None


def entry_latin(entry: Dict[str, Any]) -> Optional[str]:
    v = resolve_pollen_field(entry, "latin")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def entry_dutch(entry: Dict[str, Any]) -> Optional[str]:
    v = resolve_pollen_field(entry, "dutch")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def entry_family(entry: Dict[str, Any]) -> Optional[str]:
    """Display family: Latin, optionally with Dutch in parentheses."""
    latin = resolve_pollen_field(entry, "family_latin")
    dutch = resolve_pollen_field(entry, "family_dutch")
    # Legacy unsplit field (pre-migration)
    legacy = resolve_pollen_field(entry, "classification.family")
    if isinstance(legacy, str) and legacy.strip() and not (
        isinstance(latin, str) and latin.strip()
    ):
        return legacy.strip()
    if isinstance(latin, str) and latin.strip():
        if isinstance(dutch, str) and dutch.strip():
            return f"{latin.strip()} ({dutch.strip()})"
        return latin.strip()
    if isinstance(dutch, str) and dutch.strip():
        return dutch.strip()
    return None


def entry_feature(entry: Dict[str, Any], name: str) -> Any:
    return resolve_pollen_field(entry, name)


def entry_visibility(entry: Dict[str, Any], morph_field: str) -> Any:
    return resolve_pollen_field(entry, f"{morph_field}_visibility")


def entry_size_strings(entry: Dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
    size_src = entry.get("size") if isinstance(entry.get("size"), dict) else {}
    ss = size_src.get("size_smallest", size_src.get("smallest_size"))
    ls = size_src.get("size_largest", size_src.get("largest_size"))
    if isinstance(ss, str):
        ss = ss.strip() or None
    else:
        ss = None
    if isinstance(ls, str):
        ls = ls.strip() or None
    else:
        ls = None
    return ss, ls


def visibility_label_nl(code: Any) -> Optional[str]:
    """Dutch label for a visibility code, or None if unset/invalid."""
    if code is None:
        return None
    if isinstance(code, str):
        s = code.strip()
        if s in ("", "-", "null", "None"):
            return None
        return VISIBILITY_LABELS_NL.get(s)
    return None


def format_morph_with_visibility(morph_text: Any, visibility_code: Any) -> str:
    """Morph string, optionally with ' (Dutch visibility label)' appended."""
    text = ""
    if morph_text is not None:
        text = str(morph_text).strip()
        if text in ("", "-", "null", "None"):
            text = ""
    label = visibility_label_nl(visibility_code)
    if text and label:
        return f"{text} ({label})"
    if text:
        return text
    if label:
        return f"({label})"
    return ""


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


# Delport GCFR atlas size bins (Dutch and English labels in pollen-note).
# Midpoints are for gallery sort/display only; they are not measured sizes.
_DELPORT_SIZE_CLASS_RE = re.compile(r"Delport size class:\s*([^;]+)", re.I)
_DELPORT_SIZE_CLASS_UM: Dict[str, float] = {
    "zeer klein": 8.0,
    "klein": 18.0,
    "middelgroot": 38.0,
    "groot": 75.0,
    "zeer groot": 120.0,
}
_DELPORT_SIZE_CLASS_LABEL_NL: Dict[str, str] = {
    "zeer klein": "zeer klein (<10 µm)",
    "klein": "klein (10–25 µm)",
    "middelgroot": "middelgroot (26–50 µm)",
    "groot": "groot (51–100 µm)",
    "zeer groot": "zeer groot (>100 µm)",
}


def canonicalize_delport_size_class(raw: Any) -> Optional[str]:
    """Map a Delport size-class phrase to a canonical Dutch key, or None."""
    if not isinstance(raw, str):
        return None
    s = raw.strip().lower().replace("–", "-").replace("—", "-")
    if not s:
        return None
    if "zeer klein" in s or "<10" in s or "< 10" in s:
        return "zeer klein"
    if "zeer groot" in s or ">100" in s or "> 100" in s:
        return "zeer groot"
    if s.startswith("klein") or s.startswith("small") or "10-25" in s:
        return "klein"
    if "middelgroot" in s or s.startswith("medium") or "26-50" in s:
        return "middelgroot"
    if s.startswith("groot") or "51-100" in s:
        return "groot"
    return None


def parse_delport_size_class(note: Any) -> Optional[str]:
    """Canonical size-class key from a pollen-note string, or None."""
    if not isinstance(note, str) or not note.strip():
        return None
    m = _DELPORT_SIZE_CLASS_RE.search(note)
    if not m:
        return None
    return canonicalize_delport_size_class(m.group(1))


def json_entry_max_um(entry: Dict[str, Any]) -> Optional[float]:
    """Largest measured µm from a pollen.json size object, or None."""
    size_src = entry.get("size") if isinstance(entry.get("size"), dict) else {}
    ss = size_src.get("smallest_size", size_src.get("size_smallest"))
    ls = size_src.get("largest_size", size_src.get("size_largest"))
    ss_s = ss.strip() if isinstance(ss, str) else None
    ls_s = ls.strip() if isinstance(ls, str) else None
    return parse_max_um_from_size_strings(ss_s, ls_s)


def json_entry_size_class(entry: Dict[str, Any]) -> Optional[str]:
    note = entry.get("pollen-note", entry.get("pollen_note"))
    return parse_delport_size_class(note)


def json_entry_size_sort_key(entry: Dict[str, Any], latin: str = "") -> tuple:
    """Sort key: measured or class-midpoint µm ascending; unknown last; then latin."""
    lat = latin.strip().lower() if latin else str(entry.get("latin") or "").strip().lower()
    um = json_entry_max_um(entry)
    if um is not None and um > 0:
        return (0, um, lat)
    cls = json_entry_size_class(entry)
    if cls is not None:
        return (0, _DELPORT_SIZE_CLASS_UM[cls], lat)
    return (1, 0.0, lat)


def json_entry_gallery_width_px(entry: Dict[str, Any]) -> int:
    """True-scale width: measured size, else Delport class midpoint, else default."""
    um = json_entry_max_um(entry)
    if um is not None and um > 0:
        return display_width_px_from_max_um(um)
    cls = json_entry_size_class(entry)
    if cls is not None:
        return display_width_px_from_max_um(_DELPORT_SIZE_CLASS_UM[cls])
    return display_width_px_for_json_entry(entry)


def json_entry_size_caption(entry: Dict[str, Any]) -> str:
    """Caption: measured µm, else Delport class label, else unknown."""
    um = json_entry_max_um(entry)
    if um is not None and um > 0:
        size_src = entry.get("size") if isinstance(entry.get("size"), dict) else {}
        ss = size_src.get("smallest_size", size_src.get("size_smallest"))
        ls = size_src.get("largest_size", size_src.get("size_largest"))
        ss_s = ss.strip() if isinstance(ss, str) and ss.strip() else ""
        ls_s = ls.strip() if isinstance(ls, str) and ls.strip() else ""
        if ss_s and ls_s and ss_s != ls_s:
            return f"{ss_s}–{ls_s}".replace(" µm–", "–")
        return ls_s or ss_s or f"{um:g} µm"
    cls = json_entry_size_class(entry)
    if cls is not None:
        return _DELPORT_SIZE_CLASS_LABEL_NL[cls]
    return "grootte onbekend"


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
    q = quote_plus(slug.replace("_", " ").lower())
    return {
        "pollenx": f"https://pollenx.eu/species.php?species={slug}",
        "tstebler": f"https://pollen.tstebler.ch/MediaWiki/index.php?title={slug}",
        "paldat": f"https://www.paldat.org/pub/{slug}",
        "waarneming": f"https://waarneming.nl/search/?q={q}",
    }


def merge_links_yaml_defaults(latin: str, links_yaml: Any) -> Dict[str, Optional[str]]:
    """Return link keys pollenx, tstebler, paldat, waarneming — None means omit from JSON."""
    base = default_external_links(latin)
    out: Dict[str, Optional[str]] = {
        "pollenx": base.get("pollenx"),
        "tstebler": base.get("tstebler"),
        "paldat": base.get("paldat"),
        "waarneming": base.get("waarneming"),
    }
    if not isinstance(links_yaml, dict):
        return out
    yaml_by_canonical = {
        "pollenx": links_yaml.get("pollenx", links_yaml.get("pollenX")),
        "tstebler": links_yaml.get("tstebler"),
        "paldat": links_yaml.get("paldat"),
        "waarneming": links_yaml.get("waarneming"),
    }
    for k in ("pollenx", "tstebler", "paldat", "waarneming"):
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
        ss, ls = entry_size_strings(entry)

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


# Macro field paths used in curated MD → exported pollen.json keys.
JSON_FIELD_ALIASES: Dict[str, str] = {
    "latin": "latin",
    "dutch": "dutch",
    "family": "family",
    "shape": "shape",
    "sculpture": "sculpture",
    "ornamentation": "ornamentation",
    "aperture": "aperture",
    "sculpture_visibility": "sculpture_visibility",
    "aperture_visibility": "aperture_visibility",
    "ornamentation_visibility": "ornamentation_visibility",
    "size.size_smallest": "size.smallest_size",
    "size.smallest_size": "size.smallest_size",
    "size.size_largest": "size.largest_size",
    "size.largest_size": "size.largest_size",
    "pollen-note": "pollen-note",
    "pollen_note": "pollen-note",
    "pe_ratio": "pe_ratio",
    "polarity": "polarity",
}


def resolve_json_field(entry: Dict[str, Any], field: str) -> Any:
    """Resolve a macro field from an exported pollen.json index entry."""
    if not isinstance(entry, dict) or not field:
        return None
    mapped = JSON_FIELD_ALIASES.get(field, field)
    if "." in mapped:
        return get_dotted(entry, mapped)
    if mapped in entry:
        return entry.get(mapped)
    # Legacy YAML-style aliases via FIELD_ALIASES top-level morph names
    alias = FIELD_ALIASES.get(field)
    if alias and "." not in alias:
        return entry.get(alias.split(".")[-1])
    return None


def display_width_px_for_json_entry(entry: Dict[str, Any]) -> int:
    """Display width from exported index entry."""
    w = entry.get("display_width_px")
    if isinstance(w, int) and w > 0:
        return w
    if isinstance(w, float) and w > 0:
        return int(round(w))
    size = entry.get("size")
    ss = ls = None
    if isinstance(size, dict):
        ss = size.get("smallest_size")
        ls = size.get("largest_size")
    max_um = parse_max_um_from_size_strings(
        str(ss).strip() if ss is not None else None,
        str(ls).strip() if ls is not None else None,
    )
    return display_width_px_from_max_um(max_um)
