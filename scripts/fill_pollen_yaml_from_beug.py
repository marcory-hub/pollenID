#!/usr/bin/env python3
"""Fill data/pollen.yaml from Beug key JSON (primary) and Beug.txt (sizes fallback).

pollen_class_beug stores Beug Aperturtyp labels (not chapter numbers), e.g. Tricolpat-psilat.

Usage:
  ./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --dry-run
  ./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py
  ./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --relabel-classes
  ./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --report-missing-from-keys
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data" / "pollen.yaml"
BEUG_KEYS = ROOT / "docs" / "keys" / "beug"
BEUG_TXT = ROOT / "notes" / "pollenID" / "Beug.txt"

CLASS_RE = re.compile(r"^beug(\d\d)", re.I)
SPECIES_SIZE_RE = re.compile(
    r"(?<![A-Za-z])\*?([A-Z][a-z]+)\s+([a-z][a-z\-]+)\*?"
    r"(?:\s+(?:subsp\.|var\.)\s+[a-z][a-z\-]+)?"
    r"(?:\s+[A-Z][A-Za-zÀ-ÿ\.\-\s&]+)?"
    r"\s*\((\d+)\)\s*"
    r"(\d+[.,]\d+)\s*[–\-]\s*(\d+[.,]\d+)\s*(?:µm|μm|um)\b",
    re.M,
)
# Species/type title lines without requiring a size block
SPECIES_TITLE_RE = re.compile(
    r"(?m)^\d+(?:\.\d+)+\s+\*?([A-Z][a-z]+)(?:\s+([a-z][a-z\-]+))?\*?"
)
# Any italic binomial in outcome (incl. Non vidi) gets chapter class
BINOMIAL_RE = re.compile(
    r"\*([A-Z][a-z]+)\s+([a-z][a-z\-]+)\*"
)

OVERVIEW_CLASSES = {"01", "02"}
CORRUPT_MARKERS = (
    "Herkünfte wurden untersucht",
    "Kleinster Meßwert",
    "Kleinster Messwert",
    "Zweckmäßig ist",
    "Zweckmaessig ist",
)

# Chapter number → Aperturtyp (SoT for pollen_class_beug)
CLASS_LABEL: Dict[str, str] = {
    "3": "Polyad",
    "4": "Tetrad",
    "5": "Dyad",
    "6": "Vesiculat",
    "7": "Inaperturat",
    "8": "Monoporat",
    "9": "Monocolpat",
    "10": "Syncolpat",
    "11": "Dicolpat",
    "12": "Dicolporat",
    "13": "Tricolpat-psilat",
    "14": "Tricolporat-psilat",
    "15": "Tricolporat-psilat",
    "16": "Tricol-clavat",
    "17": "Tricol-echinat",
    "18": "Tricolpat-striat",
    "19": "Tricolporat-striat",
    "20": "Tricolporat-striat",
    "21": "Tricolpat-reticulat",
    "22": "Tricolporat-reticulat",
    "23": "Tricolporat-reticulat",
    "24": "Stephanocolpat",
    "25": "Stephanocolporat",
    "26": "Pericolpat",
    "27": "Pericolporat",
    "28": "Heterocolpat",
    "29": "Fenestrat",
    "30": "Diporat",
    "31": "Triporat",
    "32": "Stephanoporat",
    "33": "Periporat",
}

# Known wrong YAML slugs → Beug / accepted slug
SLUG_ALIASES: Dict[str, str] = {
    "liguster_vulgare": "ligustrum_vulgare",
    "asparagus_officinalis_ssp_officinalis": "asparagus_officinalis",
    "asparagus_officinalis_ssp_prostratus": "asparagus_officinalis",
    "brassica_napus_ssp_oleofera": "brassica_napus",
    "caltha_palustris_ssp_palustris": "caltha_palustris",
    "centaurea_jacea_typ": "centaurea_jacea",
    "lotus_corniculatus_var_corniculatus": "lotus_corniculatus",
    "lotus_corniculatus_var_sativus": "lotus_corniculatus",
    "narcissus_pseudonarcissus_ssp_pseudonarcissus": "narcissus_pseudonarcissus",
    "ononis_repens_ssp_spinosa": "ononis_spinosa",
    "phyteuma_spicatum_ssp_spicatum": "phyteuma_spicatum",
    "tragopogon_pratensis_s_orientalis": "tragopogon_pratensis",
    "tragopogon_pratensis_s_pratensis": "tragopogon_pratensis",
}


def class_label_from_num(num: str | int) -> Optional[str]:
    return CLASS_LABEL.get(str(int(num)))


def normalize_class_value(raw: Any) -> Optional[str]:
    """Map legacy number / long German string / freestyle → Aperturtyp label."""
    if raw is None:
        return None
    s = str(raw).strip().strip("'\"")
    if not s:
        return None
    if s in CLASS_LABEL.values():
        return s
    m = re.match(r"^(\d+)\b", s)
    if m:
        return class_label_from_num(m.group(1))
    low = s.lower().replace("ï", "i")
    # freestyle morphology leftovers
    if "echina" in low and "tricol" in low:
        return "Tricol-echinat"
    if "retic" in low and "tricolpor" in low:
        return "Tricolporat-reticulat"
    if "retic" in low and "tricol" in low:
        return "Tricolpat-reticulat"
    if "striat" in low and "tricolpor" in low:
        return "Tricolporat-striat"
    if "striat" in low and "tricol" in low:
        return "Tricolpat-striat"
    if "psila" in low and "tricolpor" in low:
        return "Tricolporat-psilat"
    if "psila" in low and "tricol" in low:
        return "Tricolpat-psilat"
    return None


@dataclass
class TaxonBeug:
    lo: Optional[float] = None
    hi: Optional[float] = None
    classes: Set[str] = field(default_factory=set)  # Aperturtyp labels
    apertures: Set[str] = field(default_factory=set)
    sculptures: Set[str] = field(default_factory=set)
    pe_ratios: Set[str] = field(default_factory=set)
    notes: List[str] = field(default_factory=list)
    sources: Set[str] = field(default_factory=set)


def _empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
        return True
    return False


def _fmt_um(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x))} µm"
    s = f"{x:.1f}".rstrip("0").rstrip(".")
    if "." not in s:
        s = f"{x:.1f}"
    return f"{s} µm"


def _height_px(hi: float) -> int:
    return int(round(hi * 2.5))


def _hints_from_meta_key(meta_key: str) -> Tuple[Optional[str], Optional[str]]:
    k = meta_key.lower()
    aperture = None
    sculpture = None
    if "tricolporoid" in k:
        aperture = "tricolporoïd"
    elif "tricolporat" in k:
        aperture = "tricolporaat"
    elif "tricolpat" in k:
        aperture = "tricolpaat"
    elif "stephanocolpat" in k:
        aperture = "stephanocolpaat"
    elif "stephanoporat" in k:
        aperture = "stephanoporaat"
    elif "pericolporat" in k:
        aperture = "pericolporaat"
    elif "pericolpat" in k:
        aperture = "pericolpaat"
    elif "periporat" in k:
        aperture = "periporaat"
    elif "triporat" in k:
        aperture = "triporaat"
    elif "diporat" in k:
        aperture = "diporaat"
    elif "monoporat" in k:
        aperture = "monoporaat"
    elif "monocolpat" in k:
        aperture = "monocolpaat"
    elif "inapert" in k:
        aperture = "inaperturaat"
    elif "heterocolpat" in k:
        aperture = "heterocolpaat"
    elif "syncolpat" in k:
        aperture = "syncolpaat"
    elif "dicolpat" in k:
        aperture = "dicolpaat"
    elif "vesiculat" in k:
        aperture = "vesiculaat"
    elif "fenestrat" in k:
        aperture = "fenestraat"
    elif "polyade" in k or "polyad" in k:
        aperture = "polyade"
    elif "tetrade" in k or "tetrad" in k:
        aperture = "tetrade"
    elif "dyade" in k or "dyad" in k:
        aperture = "dyade"

    if re.search(r"(^|-)ret($|-)|retic", k):
        sculpture = "reticulaat"
    elif re.search(r"(^|-)str($|-)|striat", k):
        sculpture = "striaat"
    elif re.search(r"(^|-)ps($|-)|psilat|psilaat", k):
        sculpture = "psilaat"
    elif re.search(r"echinat|(^|-)ech($|-)", k):
        sculpture = "echinaat"
    elif "clav" in k:
        sculpture = "clavaat"
    elif "bacul" in k:
        sculpture = "baculaat"
    elif "verruc" in k:
        sculpture = "verrucaat"
    elif "gemmat" in k:
        sculpture = "gemmataat"
    return aperture, sculpture


def _pe_from_text(text: str) -> Set[str]:
    t = text.lower()
    out: Set[str] = set()
    for term in (
        "perprolaat",
        "prolaat",
        "oblaat",
        "sferoïdisch",
        "sphaeroïdisch",
        "sferoidisch",
    ):
        if term in t:
            if term.startswith("sphaero") or term.startswith("sferoid"):
                out.add("sferoïdisch")
            else:
                out.add(term)
    return out


def _pk_note_from_outcome(text: str) -> Optional[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if ln.startswith("PK ") or ln.startswith("Exine "):
            note = ln
            if len(note) > 280:
                note = note[:277].rstrip() + "..."
            return note
    return None


def _merge_size(tb: TaxonBeug, lo: float, hi: float) -> None:
    if lo > hi:
        lo, hi = hi, lo
    tb.lo = lo if tb.lo is None else min(tb.lo, lo)
    tb.hi = hi if tb.hi is None else max(tb.hi, hi)


def _slug(genus: str, species: Optional[str] = None) -> str:
    if not species:
        return genus.lower().replace("-", "_")
    return f"{genus}_{species}".lower().replace("-", "_")


def _outcome_unusable(text: str, n_sizes: int) -> bool:
    if len(text) > 20000:
        return True
    if n_sizes > 200:
        return True
    return any(m in text for m in CORRUPT_MARKERS)


def _outcome_endpoints(ch: dict) -> Tuple[Set[str], Optional[str]]:
    keyed: Set[str] = set()
    text: Optional[str] = None
    pk = ch.get("pollen_key")
    if isinstance(pk, str) and pk.strip():
        keyed.add(pk.strip())
    for pk in ch.get("pollen_keys") or []:
        if isinstance(pk, str) and pk.strip():
            keyed.add(pk.strip())
    oc = ch.get("outcome")
    if isinstance(oc, dict):
        if isinstance(oc.get("text"), str):
            text = oc["text"]
        pk = oc.get("pollen_key")
        if isinstance(pk, str) and pk.strip():
            keyed.add(pk.strip())
        for pk in oc.get("pollen_keys") or []:
            if isinstance(pk, str) and pk.strip():
                keyed.add(pk.strip())
    return keyed, text


def _add_class(tb: TaxonBeug, class_num: Optional[str]) -> None:
    if not class_num:
        return
    label = class_label_from_num(class_num)
    if label:
        tb.classes.add(label)


def collect_from_beug_json() -> Dict[str, TaxonBeug]:
    out: Dict[str, TaxonBeug] = defaultdict(TaxonBeug)
    if not BEUG_KEYS.is_dir():
        return out
    skipped_corrupt = 0

    for path in sorted(BEUG_KEYS.glob("beug*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        meta = data.get("meta") or {}
        meta_key = str(meta.get("key") or path.stem)
        m = CLASS_RE.match(meta_key)
        class_num = m.group(1) if m else None
        if class_num in OVERVIEW_CLASSES:
            class_num = None
        ap, sc = _hints_from_meta_key(meta_key)

        for step in (data.get("steps") or {}).values():
            if not isinstance(step, dict):
                continue
            for ch in step.get("choices") or []:
                if not isinstance(ch, dict):
                    continue
                keyed, text = _outcome_endpoints(ch)
                n_sizes = len(SPECIES_SIZE_RE.findall(text)) if text else 0
                corrupt = bool(text and _outcome_unusable(text, n_sizes))
                if corrupt:
                    skipped_corrupt += 1

                for pk in keyed:
                    canon = SLUG_ALIASES.get(pk, pk)
                    tb = out[canon]
                    tb.sources.add(path.name)
                    if not corrupt:
                        _add_class(tb, class_num)
                        if ap:
                            tb.apertures.add(ap)
                        if sc:
                            tb.sculptures.add(sc)

                if not text or corrupt:
                    continue

                note = _pk_note_from_outcome(text)
                pe = _pe_from_text(text)
                attach_note = note is not None and n_sizes <= 6

                for sm in SPECIES_SIZE_RE.finditer(text):
                    genus, species, _n, lo_s, hi_s = sm.groups()
                    slug = SLUG_ALIASES.get(_slug(genus, species), _slug(genus, species))
                    tb = out[slug]
                    tb.sources.add(path.name)
                    _merge_size(
                        tb,
                        float(lo_s.replace(",", ".")),
                        float(hi_s.replace(",", ".")),
                    )
                    _add_class(tb, class_num)
                    if ap:
                        tb.apertures.add(ap)
                    if sc:
                        tb.sculptures.add(sc)
                    tb.pe_ratios.update(pe)
                    if attach_note and note not in tb.notes and len(tb.notes) < 2:
                        tb.notes.append(note)

                # Title lines: assign class even without size (species in key)
                for tm in SPECIES_TITLE_RE.finditer(text):
                    genus, species = tm.group(1), tm.group(2)
                    if not species:
                        continue
                    slug = SLUG_ALIASES.get(_slug(genus, species), _slug(genus, species))
                    tb = out[slug]
                    tb.sources.add(path.name)
                    _add_class(tb, class_num)
                    if ap:
                        tb.apertures.add(ap)
                    if sc:
                        tb.sculptures.add(sc)

                # Italic binomials (incl. Non vidi / without size): class only
                for bm in BINOMIAL_RE.finditer(text):
                    genus, species = bm.group(1), bm.group(2)
                    slug = SLUG_ALIASES.get(_slug(genus, species), _slug(genus, species))
                    tb = out[slug]
                    tb.sources.add(path.name)
                    _add_class(tb, class_num)
                    if ap:
                        tb.apertures.add(ap)
                    if sc:
                        tb.sculptures.add(sc)

                if pe:
                    for pk in keyed:
                        out[SLUG_ALIASES.get(pk, pk)].pe_ratios.update(pe)

    if skipped_corrupt:
        print(f"skipped corrupt outcomes: {skipped_corrupt}")
    return out


def collect_from_beug_txt() -> Dict[str, TaxonBeug]:
    """Sizes (+ chapter class when a numbered heading precedes the measurement)."""
    out: Dict[str, TaxonBeug] = defaultdict(TaxonBeug)
    if not BEUG_TXT.is_file():
        return out
    text = BEUG_TXT.read_text(encoding="utf-8", errors="replace")
    # Track last seen chapter number from lines like "13. Tricolpatae" or "4.7.4 Calluna"
    chapter_re = re.compile(
        r"(?m)^(?:\s*)(\d{1,2})(?:\.\d+)*\.?\s+[A-ZÄÖÜa-z]"
    )
    # Walk with a simple line scan for chapter context near size lines
    lines = text.splitlines()
    current_chapter: Optional[str] = None
    buf = text
    # Prefer structured: find each size match and look back in text for chapter
    for sm in SPECIES_SIZE_RE.finditer(text):
        genus, species, _n, lo_s, hi_s = sm.groups()
        slug = SLUG_ALIASES.get(_slug(genus, species), _slug(genus, species))
        tb = out[slug]
        tb.sources.add("Beug.txt")
        _merge_size(
            tb,
            float(lo_s.replace(",", ".")),
            float(hi_s.replace(",", ".")),
        )
        # look back up to 800 chars for a chapter start "NN. Name" at line start
        start = max(0, sm.start() - 800)
        window = text[start : sm.start()]
        chs = re.findall(r"(?m)^(\d{1,2})\.(?:\d+\.)*\s", window)
        if chs:
            num = chs[-1]
            if num not in OVERVIEW_CLASSES and int(num) >= 3:
                _add_class(tb, num)
    return out


def merge_beug(
    from_json: Dict[str, TaxonBeug], from_txt: Dict[str, TaxonBeug]
) -> Dict[str, TaxonBeug]:
    """JSON primary; txt adds sizes/classes only when JSON lacks them."""
    out: Dict[str, TaxonBeug] = defaultdict(TaxonBeug)
    for slug, tb in from_json.items():
        dest = out[slug]
        if tb.lo is not None:
            _merge_size(dest, tb.lo, tb.hi if tb.hi is not None else tb.lo)
        dest.classes.update(tb.classes)
        dest.apertures.update(tb.apertures)
        dest.sculptures.update(tb.sculptures)
        dest.pe_ratios.update(tb.pe_ratios)
        dest.sources.update(tb.sources)
        for n in tb.notes:
            if n not in dest.notes and len(dest.notes) < 2:
                dest.notes.append(n)
    for slug, tb in from_txt.items():
        dest = out[slug]
        if dest.lo is None and tb.lo is not None:
            _merge_size(dest, tb.lo, tb.hi if tb.hi is not None else tb.lo)
            dest.sources.add("Beug.txt")
        if not dest.classes and tb.classes:
            dest.classes.update(tb.classes)
            dest.sources.add("Beug.txt")
    return out


def _latin_to_slug(latin: str) -> Optional[str]:
    parts = re.findall(r"[A-Za-z]+", latin.strip())
    if len(parts) < 2:
        return None
    return _slug(parts[0], parts[1])


def _unique(values: Set[str]) -> Optional[str]:
    if len(values) == 1:
        return next(iter(values))
    return None


def _class_value(classes: Set[str]) -> Optional[str]:
    if not classes:
        return None
    if len(classes) == 1:
        return next(iter(classes))
    # Prefer deterministic join only when distinct labels remain
    return ", ".join(sorted(classes))


def resolve_yaml_slug(beug_slug: str, data: Dict[str, Any], latin_index: Dict[str, str]) -> Optional[str]:
    beug_slug = SLUG_ALIASES.get(beug_slug, beug_slug)
    if beug_slug in data:
        return beug_slug
    return latin_index.get(beug_slug)


def planned_fills(
    data: Dict[str, Any],
    beug: Dict[str, TaxonBeug],
    *,
    overwrite_class: bool = False,
) -> Dict[str, Dict[str, Any]]:
    latin_index: Dict[str, str] = {}
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        name = entry.get("name") or {}
        latin = name.get("latin_name") if isinstance(name, dict) else None
        if isinstance(latin, str) and latin.strip():
            ls = _latin_to_slug(latin)
            if ls:
                latin_index.setdefault(ls, slug)
                latin_index.setdefault(SLUG_ALIASES.get(ls, ls), slug)

    fills: Dict[str, Dict[str, Any]] = {}
    for beug_slug, tb in beug.items():
        yaml_slug = resolve_yaml_slug(beug_slug, data, latin_index)
        if yaml_slug is None:
            continue
        entry = data[yaml_slug]
        if not isinstance(entry, dict):
            continue
        planned: Dict[str, Any] = {}

        size = entry.get("size") if isinstance(entry.get("size"), dict) else {}
        feats = (
            entry.get("pollen_features")
            if isinstance(entry.get("pollen_features"), dict)
            else {}
        )

        if tb.lo is not None and tb.hi is not None:
            filled_size = False
            if _empty(size.get("size_smallest")):
                planned["size.size_smallest"] = _fmt_um(tb.lo)
                filled_size = True
            if _empty(size.get("size_largest")):
                planned["size.size_largest"] = _fmt_um(tb.hi)
                filled_size = True
            expected_h = _height_px(tb.hi)
            cur_h = size.get("height_px")
            if filled_size or _empty(cur_h):
                planned["size.height_px"] = expected_h
            else:
                try:
                    hi_yaml = float(
                        str(size.get("size_largest"))
                        .replace("µm", "")
                        .replace("μm", "")
                        .replace("um", "")
                        .strip()
                        .replace(",", ".")
                    )
                except (TypeError, ValueError):
                    hi_yaml = None
                if hi_yaml is not None and abs(hi_yaml - tb.hi) < 0.05:
                    if cur_h != expected_h:
                        planned["size.height_px"] = expected_h

        cv = _class_value(tb.classes)
        if cv:
            cur = entry.get("pollen_class_beug")
            if overwrite_class or _empty(cur):
                if normalize_class_value(cur) != cv or _empty(cur) or overwrite_class:
                    if _empty(cur) or overwrite_class or normalize_class_value(cur) != cv:
                        if str(cur).strip() != cv:
                            planned["pollen_class_beug"] = cv
            elif normalize_class_value(cur) and normalize_class_value(cur) != str(cur).strip():
                # legacy number → label even without --relabel when empty path missed
                pass

        ap = _unique(tb.apertures)
        if ap and _empty(feats.get("aperture")):
            planned["pollen_features.aperture"] = ap

        sc = _unique(tb.sculptures)
        if sc and _empty(feats.get("sculpture")):
            planned["pollen_features.sculpture"] = sc

        if tb.pe_ratios and _empty(feats.get("pe_ratio")):
            order = ("oblaat", "sferoïdisch", "prolaat", "perprolaat")
            pe_list = [x for x in order if x in tb.pe_ratios]
            pe_list.extend(sorted(tb.pe_ratios - set(pe_list)))
            planned["pollen_features.pe_ratio"] = (
                pe_list[0] if len(pe_list) == 1 else " tot ".join(pe_list)
            )

        if tb.notes and _empty(feats.get("pollen-note")):
            planned["pollen_features.pollen-note"] = tb.notes[0]

        if planned:
            fills[yaml_slug] = planned
    return fills


def planned_relabel_only(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Convert existing pollen_class_beug numbers / legacy strings → Aperturtyp."""
    fills: Dict[str, Dict[str, Any]] = {}
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        cur = entry.get("pollen_class_beug")
        if _empty(cur):
            continue
        label = normalize_class_value(cur)
        if label and str(cur).strip() != label:
            fills[slug] = {"pollen_class_beug": label}
    return fills


def apply_fills_surgical(
    text: str, fills: Dict[str, Dict[str, Any]], *, allow_replace_class: bool = False
) -> Tuple[str, int]:
    parts = re.split(r"(?m)^(?=[a-z][a-z0-9_]*:)", text)
    if not parts:
        return text, 0

    out_parts: List[str] = []
    n_repl = 0

    class_empty = re.compile(r"(?m)^(  pollen_class_beug:)[ \t]*$")
    class_any = re.compile(r"(?m)^(  pollen_class_beug:)[ \t]*.*$")

    field_line = {
        "size.size_smallest": re.compile(r"(?m)^(    size_smallest:)[ \t]*$"),
        "size.size_largest": re.compile(r"(?m)^(    size_largest:)[ \t]*$"),
        "size.height_px": re.compile(r"(?m)^(    height_px:)[ \t]*.*$"),
        "pollen_features.aperture": re.compile(r"(?m)^(    aperture:)[ \t]*$"),
        "pollen_features.sculpture": re.compile(r"(?m)^(    sculpture:)[ \t]*$"),
        "pollen_features.pe_ratio": re.compile(r"(?m)^(    pe_ratio:)[ \t]*$"),
        "pollen_features.pollen-note": re.compile(r"(?m)^(    pollen-note:)[ \t]*$"),
    }

    for part in parts:
        m = re.match(r"^([a-z][a-z0-9_]*):", part)
        if not m:
            out_parts.append(part)
            continue
        slug = m.group(1)
        planned = fills.get(slug)
        if not planned:
            out_parts.append(part)
            continue
        block = part
        for key, value in planned.items():
            if isinstance(value, int):
                rendered = str(value)
            else:
                s = str(value)
                if any(c in s for c in (":", "#", "{", "}", "[", "]", ",", "\n")) or s.startswith(
                    ("@", "*", "&", "!", "|", ">", "'", '"', "%")
                ):
                    rendered = json.dumps(s, ensure_ascii=False)
                else:
                    rendered = s

            if key == "pollen_class_beug":
                rx = class_any if allow_replace_class else class_empty
                new_block, count = rx.subn(rf"\1 {rendered}", block, count=1)
            else:
                rx = field_line.get(key)
                if not rx:
                    continue
                new_block, count = rx.subn(rf"\1 {rendered}", block, count=1)
            if count:
                block = new_block
                n_repl += count
        out_parts.append(block)

    return "".join(out_parts), n_repl


def report_missing_from_keys() -> int:
    """Species with sizes in Beug.txt that never appear in key JSON outcomes."""
    from_json = collect_from_beug_json()
    from_txt = collect_from_beug_txt()
    json_slugs = set(from_json.keys())
    txt_sized = {s for s, t in from_txt.items() if t.lo is not None}
    missing = sorted(txt_sized - json_slugs)
    print(f"Beug.txt sized taxa: {len(txt_sized)}")
    print(f"Beug keys taxa (any hit): {len(json_slugs)}")
    print(f"In Beug.txt with size, not in keys: {len(missing)}")
    for s in missing[:80]:
        t = from_txt[s]
        print(f"  {s}  {t.lo}–{t.hi} µm  class={sorted(t.classes) or '-'}")
    if len(missing) > 80:
        print(f"  ... +{len(missing) - 80} more")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--path", type=Path, default=YAML_PATH)
    parser.add_argument("--report", type=int, default=20)
    parser.add_argument(
        "--relabel-classes",
        action="store_true",
        help="Rewrite existing pollen_class_beug numbers/legacy → Aperturtyp labels",
    )
    parser.add_argument(
        "--report-missing-from-keys",
        action="store_true",
        help="List Beug.txt species with sizes absent from key JSON",
    )
    args = parser.parse_args()

    if args.report_missing_from_keys:
        return report_missing_from_keys()

    import yaml

    raw = args.path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        print(f"{args.path}: invalid root", file=sys.stderr)
        return 1

    fills: Dict[str, Dict[str, Any]] = {}
    allow_replace_class = False

    if args.relabel_classes:
        fills = planned_relabel_only(data)
        allow_replace_class = True
        print(f"relabel candidates: {len(fills)}")
    else:
        from_json = collect_from_beug_json()
        from_txt = collect_from_beug_txt()
        beug = merge_beug(from_json, from_txt)
        fills = planned_fills(data, beug, overwrite_class=False)
        # Also convert legacy numbers on taxa we touch / all empty→label already
        # Convert any remaining numeric classes when Beug supplies label
        for slug, planned in list(fills.items()):
            if "pollen_class_beug" in planned:
                allow_replace_class = True
        # Second pass: relabel all numeric even if not in fills
        for slug, entry in data.items():
            if not isinstance(entry, dict):
                continue
            cur = entry.get("pollen_class_beug")
            if _empty(cur):
                continue
            label = normalize_class_value(cur)
            if label and str(cur).strip() != label:
                fills.setdefault(slug, {})["pollen_class_beug"] = label
                allow_replace_class = True

        print(f"beug taxa parsed: {len(beug)}")
        print(f"  from json sizes: {sum(1 for t in from_json.values() if t.lo is not None)}")
        print(f"  from txt sizes: {sum(1 for t in from_txt.values() if t.lo is not None)}")
        print(f"yaml taxa with ≥1 fill: {len(fills)}")

    slot_counts: Dict[str, int] = defaultdict(int)
    for planned in fills.values():
        for k in planned:
            slot_counts[k] += 1
    print("slots:")
    for k in sorted(slot_counts):
        print(f"  {k}: {slot_counts[k]}")

    if args.report:
        print("sample:")
        for i, (slug, planned) in enumerate(sorted(fills.items())):
            if i >= args.report:
                break
            print(f"  {slug}: {planned}")

    if args.dry_run:
        print("dry-run: no file written")
        return 0

    new_text, n_repl = apply_fills_surgical(
        raw, fills, allow_replace_class=allow_replace_class
    )
    args.path.write_text(new_text, encoding="utf-8")
    print(f"wrote {args.path} ({n_repl} line replacements)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
