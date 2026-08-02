#!/usr/bin/env python3
"""Generate lookalike candidate shortlist into data/lookalike_review.yaml.

Scope (v1):
  - Anchors: learning_priority_rank <= LEVEL1_MAX_RANK (default 20)
  - Partners: any taxon with learning_priority_rank, plus optional hand-seeded pairs
  - Size: midpoints within ± SIZE_WINDOW_UM (default 10)
  - Aperture: exact bucket, or shared tricol* near-group
  - Sculpture: compare when both filled; empty → borderline flag (not hard exclude)
  - Beug multi-class: soft signal from docs/keys/beug/*.json pollen_key hits

Does not promote confirmed lookalikes. AI / vision suggestions are advisory only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pollen_display import entry_feature, entry_latin, entry_size_strings

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
REVIEW_PATH = REPO / "data" / "lookalike_review.yaml"
BEUG_DIR = REPO / "docs" / "keys" / "beug"

LEVEL1_MAX_RANK = 20
SIZE_WINDOW_UM = 10.0

# Morphology fallbacks when aggregate *_typ fields are empty (Herkennen representatives).
TYP_REPRESENTATIVES: Dict[str, str] = {
    "brassica_typ": "brassica_napus",
    "raphanus_typ": "raphanus_raphanistrum",
    "sinapis_typ": "sinapis_arvensis",
    "prunus_pirus_typ": "prunus_padus",
    "rubus_typ": "rubus_fruticosus",
    "taraxacum_typ": "taraxacum_officinale",
    "vicia_typ": "vicia_sepium",
    "anthriscus_typ": "anthriscus_sylvestris",
    "salix_typ": "salix_caprea",
    "tilia_typ": "tilia_platyphyllos",
    "ranunculus_typ": "ranunculus_acris",
    "lamium_typ": "lamium_album",
    "myosotis_typ": "myosotis_scorpioides",
    "phacelia_typ": "phacelia_tanacetifolia",
    "allium_typ": "allium_ursinum",
    "asparagus_typ": "asparagus_officinalis",
    "achillea_typ": "achillea_millefolium",
    "heracleum_typ": "heracleum_sphondylium",
    "cynoglossum_typ": "cynoglossum_officinale",
    "centaurea_typ": "centaurea_jacea",
    "helianthus_typ": "helianthus_annuus",
    "crataegus_typ": "crataegus_monogyna",
    "spiraea_typ": "spiraea_japonica",
    "populus_typ": "populus_nigra",
}

# Existing Honingcluster / Herkennen-implied pairs (hand seed; may include unranked partners).
HAND_SEED_PAIRS: List[Tuple[str, str, str]] = [
    # acer-prunus-pyrus
    ("acer_platanoides", "prunus_pirus_typ", "acer-prunus-pyrus"),
    ("acer_platanoides", "malus_typ", "acer-prunus-pyrus"),
    ("acer_platanoides", "robinia_pseudoacacia", "acer-prunus-pyrus"),
    ("prunus_pirus_typ", "malus_typ", "acer-prunus-pyrus"),
    ("prunus_pirus_typ", "robinia_pseudoacacia", "acer-prunus-pyrus"),
    ("malus_typ", "robinia_pseudoacacia", "acer-prunus-pyrus"),
    # rubus-prunus-vogelkers
    ("rubus_typ", "prunus_padus", "rubus-prunus-vogelkers"),
    ("rubus_typ", "prunus_serotina", "rubus-prunus-vogelkers"),
    ("prunus_padus", "prunus_serotina", "rubus-prunus-vogelkers"),
    # melilotus-trifolium-repens
    ("trifolium_repens", "melilotus_officinalis", "melilotus-trifolium-repens"),
    ("trifolium_repens", "aesculus_hippocastanum", "melilotus-trifolium-repens"),
    ("melilotus_officinalis", "aesculus_hippocastanum", "melilotus-trifolium-repens"),
    # raphanus-brassica-sinapis-ligustrum
    ("raphanus_typ", "brassica_typ", "raphanus-brassica-sinapis-ligustrum"),
    ("raphanus_typ", "sinapis_typ", "raphanus-brassica-sinapis-ligustrum"),
    ("raphanus_typ", "ligustrum_vulgare", "raphanus-brassica-sinapis-ligustrum"),
    ("brassica_typ", "sinapis_typ", "raphanus-brassica-sinapis-ligustrum"),
    ("brassica_typ", "ligustrum_vulgare", "raphanus-brassica-sinapis-ligustrum"),
    ("sinapis_typ", "ligustrum_vulgare", "raphanus-brassica-sinapis-ligustrum"),
    # fraxinus-salix-cruciferae
    ("salix_typ", "fraxinus_ornus", "fraxinus-salix-cruciferae"),
    ("salix_typ", "brassica_typ", "fraxinus-salix-cruciferae"),
    ("fraxinus_ornus", "brassica_typ", "fraxinus-salix-cruciferae"),
    # umbelliferae-vicia
    ("anthriscus_typ", "vicia_typ", "umbelliferae-vicia"),
    # fenestraat / letter T (composieten ABCHJST)
    ("taraxacum_typ", "cichorium_intybus", "fenestraat-taraxacum"),
    ("taraxacum_typ", "hieracium_typ", "fenestraat-taraxacum"),
    ("taraxacum_typ", "hieracium_aurantiacum", "fenestraat-taraxacum"),
    ("taraxacum_typ", "crepis_biennis", "fenestraat-taraxacum"),
    ("taraxacum_typ", "tragopogon_typ", "fenestraat-taraxacum"),
    ("taraxacum_typ", "sonchus_arvensis", "fenestraat-taraxacum"),
]

BEUG_AP_TOKENS = (
    "polyadeae",
    "tetradeae",
    "dyadeae",
    "vesiculatae",
    "inaperturatae",
    "monoporatae",
    "monocolpatae",
    "syncolpatae",
    "dicolpatae",
    "dicolporatae",
    "tricolpatae",
    "tricolporatae",
    "tricolporoidatae",
    "stephanocolpatae",
    "stephanocolporatae",
    "pericolpatae",
    "pericolporatae",
    "heterocolpatae",
    "fenestratae",
    "diporatae",
    "triporatae",
    "stephanoporatae",
    "periporatae",
)

RE_NUM = re.compile(r"\d+(?:\.\d+)?")
POLLEN_KEY_RE = re.compile(r'"pollen_key"\s*:\s*"([^"]+)"')


def _rank(entry: Dict[str, Any]) -> Optional[int]:
    r = entry.get("learning_priority_rank")
    if isinstance(r, int) and r > 0:
        return r
    if isinstance(r, str) and r.strip().isdigit():
        v = int(r.strip())
        return v if v > 0 else None
    return None


def _parse_um_midpoint(smallest: Optional[str], largest: Optional[str]) -> Optional[float]:
    vals: List[float] = []
    for raw in (smallest, largest):
        if not raw:
            continue
        s = (
            str(raw)
            .replace(",", ".")
            .replace("µ", "u")
            .replace("μm", " ")
            .replace("um", " ")
        )
        for n in RE_NUM.findall(s):
            try:
                vals.append(float(n))
            except ValueError:
                continue
    if not vals:
        return None
    return (min(vals) + max(vals)) / 2.0


def _aperture_bucket(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    s = str(raw).strip().lower()
    if not s or s in ("-", "null", "none"):
        return None
    # Normalize spelling variants before class detection.
    s = (
        s.replace("ï", "i")
        .replace("ó", "o")
        .replace("ö", "o")
        .replace(" ", "")
        .replace("_", "")
    )
    s = s.replace("3-4-", "3").replace("3-", "3").replace("4-", "4")
    # tricol* near-group (tricolpaat / tricolporaat / tricolporoidaat + 3-col* variants)
    if re.search(r"(?:^|[^a-z])(?:3)?tr?icol(?:por(?:oid)?)?(?:aat|at)?", s) or re.search(
        r"3col(?:por(?:oid)?)?(?:aat|at)?", s
    ):
        # Prefer tricol* when mixed with "tot tricolporaat" etc.
        if "tricol" in s or "3col" in s:
            return "tricol*"
    if "monocol" in s or "sulcaat" in s:
        return "monocol*"
    if "stephanocolpor" in s:
        return "stephanocolpor*"
    if "stephanocol" in s:
        return "stephanocol*"
    if "heterocol" in s:
        return "heterocol*"
    if "peripor" in s or "periporaat" in s:
        return "peripor*"
    if "tripor" in s:
        return "tripor*"
    if "inapert" in s:
        return "inapert*"
    # Fallback: first alphanumeric token cluster
    m = re.match(r"[a-z0-9*]+", s)
    return m.group(0) if m else None


def _clean_text(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "null", "None"):
        return None
    return s


def _resolve_entry(
    data: Dict[str, Any], slug: str
) -> Tuple[Dict[str, Any], Optional[str]]:
    """Return entry (with optional representative merge for empty morph) and rep slug used."""
    entry = data.get(slug)
    if not isinstance(entry, dict):
        return {}, None
    rep_slug = TYP_REPRESENTATIVES.get(slug)
    if not rep_slug:
        return entry, None
    rep = data.get(rep_slug)
    if not isinstance(rep, dict):
        return entry, None
    # Shallow morph/size fallback only when primary empty.
    merged = dict(entry)
    pf = dict(entry.get("pollen_features") or {}) if isinstance(entry.get("pollen_features"), dict) else {}
    rpf = rep.get("pollen_features") if isinstance(rep.get("pollen_features"), dict) else {}
    for k in ("aperture", "sculpture", "ornamentation", "shape"):
        if not _clean_text(pf.get(k)) and _clean_text(rpf.get(k)):
            pf[k] = rpf.get(k)
    merged["pollen_features"] = pf
    size = dict(entry.get("size") or {}) if isinstance(entry.get("size"), dict) else {}
    rsize = rep.get("size") if isinstance(rep.get("size"), dict) else {}
    for k in ("size_smallest", "size_largest"):
        if not _clean_text(size.get(k)) and _clean_text(rsize.get(k)):
            size[k] = rsize.get(k)
    if size:
        merged["size"] = size
    return merged, rep_slug


def _taxon_metrics(data: Dict[str, Any], slug: str) -> Dict[str, Any]:
    entry, rep = _resolve_entry(data, slug)
    ss, ls = entry_size_strings(entry)
    mid = _parse_um_midpoint(ss, ls)
    ap = _clean_text(entry_feature(entry, "aperture"))
    sc = _clean_text(entry_feature(entry, "sculpture"))
    orn = _clean_text(entry_feature(entry, "ornamentation"))
    return {
        "slug": slug,
        "latin": entry_latin(entry),
        "rank": _rank(data.get(slug) or {}),
        "mid_um": mid,
        "size_smallest": ss,
        "size_largest": ls,
        "aperture": ap,
        "aperture_bucket": _aperture_bucket(ap),
        "sculpture": sc,
        "ornamentation": orn,
        "rep_slug": rep,
    }


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def load_beug_multi_class() -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = {}
    if not BEUG_DIR.is_dir():
        return out
    for path in BEUG_DIR.glob("*.json"):
        name = path.name.lower()
        classes = [t for t in BEUG_AP_TOKENS if t in name]
        if not classes:
            continue
        text = path.read_text(encoding="utf-8")
        for m in POLLEN_KEY_RE.finditer(text):
            slug = m.group(1).strip()
            if not slug:
                continue
            out.setdefault(slug, set()).update(classes)
    return out


def size_overlap(
    a_mid: Optional[float], b_mid: Optional[float], window: float
) -> Optional[List[float]]:
    if a_mid is None or b_mid is None:
        return None
    if abs(a_mid - b_mid) <= window:
        lo = round(min(a_mid, b_mid), 1)
        hi = round(max(a_mid, b_mid), 1)
        return [lo, hi]
    return None


def aperture_compatible(a_bucket: Optional[str], b_bucket: Optional[str]) -> bool:
    if not a_bucket or not b_bucket:
        # Empty aperture: do not hard-exclude; treat as compatible for shortlist.
        return True
    return a_bucket == b_bucket


def is_borderline(signals: Dict[str, Any]) -> bool:
    if signals.get("size_overlap_um") is None and signals.get("size_known") is False:
        return True
    if signals.get("aperture_empty"):
        return True
    if signals.get("sculpture_empty"):
        return True
    if signals.get("beug_multi_class"):
        return True
    overlap = signals.get("size_overlap_um")
    if isinstance(overlap, list) and len(overlap) == 2:
        span = abs(float(overlap[1]) - float(overlap[0]))
        if span >= SIZE_WINDOW_UM * 0.8:
            return True
    return False


def build_signals(
    a: Dict[str, Any],
    b: Dict[str, Any],
    beug_multi: Dict[str, Set[str]],
    *,
    hand: bool = False,
) -> Dict[str, Any]:
    overlap = size_overlap(a["mid_um"], b["mid_um"], SIZE_WINDOW_UM)
    a_bucket = a["aperture_bucket"]
    b_bucket = b["aperture_bucket"]
    sc_a = a["sculpture"]
    sc_b = b["sculpture"]
    sculpture_note = None
    if sc_a or sc_b:
        sculpture_note = f"{sc_a or '[empty]'} vs {sc_b or '[empty]'}"
    a_classes = beug_multi.get(a["slug"], set())
    b_classes = beug_multi.get(b["slug"], set())
    beug_flag = len(a_classes) > 1 or len(b_classes) > 1
    return {
        "size_overlap_um": overlap,
        "size_known": a["mid_um"] is not None and b["mid_um"] is not None,
        "aperture_bucket": a_bucket if a_bucket == b_bucket else f"{a_bucket}|{b_bucket}",
        "aperture_empty": not a_bucket or not b_bucket,
        "sculpture_note": sculpture_note,
        "sculpture_empty": not sc_a or not sc_b,
        "beug_multi_class": beug_flag,
        "hand_seeded": hand,
        "group": None,
    }


def auto_candidates(
    data: Dict[str, Any],
    beug_multi: Dict[str, Set[str]],
    *,
    level1_max: int,
) -> List[Dict[str, Any]]:
    ranked = [k for k, e in data.items() if isinstance(e, dict) and _rank(e)]
    anchors = [k for k in ranked if (_rank(data[k]) or 999) <= level1_max]
    partners = ranked[:]
    metrics = {k: _taxon_metrics(data, k) for k in set(anchors) | set(partners)}
    rows: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()
    for a_slug in anchors:
        for b_slug in partners:
            if a_slug == b_slug:
                continue
            pk = _pair_key(a_slug, b_slug)
            if pk in seen:
                continue
            a = metrics[a_slug]
            b = metrics[b_slug]
            # Auto-shortlist requires known aperture buckets on both sides.
            if not a["aperture_bucket"] or not b["aperture_bucket"]:
                continue
            if not aperture_compatible(a["aperture_bucket"], b["aperture_bucket"]):
                continue
            # Auto-shortlist requires known sizes and ±window overlap.
            if a["mid_um"] is None or b["mid_um"] is None:
                continue
            overlap = size_overlap(a["mid_um"], b["mid_um"], SIZE_WINDOW_UM)
            if overlap is None:
                continue
            signals = build_signals(a, b, beug_multi, hand=False)
            seen.add(pk)
            rows.append(
                {
                    "anchor": a_slug,
                    "partner": b_slug,
                    "status": "pending",
                    "signals": signals,
                    "borderline": is_borderline(signals),
                    "ai_suggestion": None,
                    "decided_by": None,
                }
            )
    return rows


def hand_seed_rows(
    data: Dict[str, Any],
    beug_multi: Dict[str, Set[str]],
    existing: Set[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for a_slug, b_slug, group in HAND_SEED_PAIRS:
        if a_slug not in data or b_slug not in data:
            continue
        pk = _pair_key(a_slug, b_slug)
        if pk in existing:
            # Enrich existing auto row with group / hand flag later in merge.
            continue
        a = _taxon_metrics(data, a_slug)
        b = _taxon_metrics(data, b_slug)
        signals = build_signals(a, b, beug_multi, hand=True)
        signals["group"] = group
        signals["size_overlap_um"] = size_overlap(a["mid_um"], b["mid_um"], SIZE_WINDOW_UM)
        rows.append(
            {
                "anchor": a_slug,
                "partner": b_slug,
                "status": "pending",
                "signals": signals,
                "borderline": is_borderline(signals),
                "ai_suggestion": None,
                "decided_by": None,
                "source": "hand_seed",
            }
        )
        existing.add(pk)
    return rows


def merge_preserve_decisions(
    new_rows: List[Dict[str, Any]], old_rows: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    old_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for r in old_rows:
        if not isinstance(r, dict):
            continue
        a, b = r.get("anchor"), r.get("partner")
        if not isinstance(a, str) or not isinstance(b, str):
            continue
        old_map[_pair_key(a, b)] = r
    out: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()
    for r in new_rows:
        pk = _pair_key(r["anchor"], r["partner"])
        seen.add(pk)
        prev = old_map.get(pk)
        if prev and prev.get("status") and prev.get("status") != "pending":
            merged = dict(r)
            merged["status"] = prev["status"]
            merged["decided_by"] = prev.get("decided_by")
            if prev.get("ai_suggestion") is not None:
                merged["ai_suggestion"] = prev.get("ai_suggestion")
            # Keep prior note if any
            if prev.get("note"):
                merged["note"] = prev.get("note")
            out.append(merged)
        else:
            out.append(r)
    # Keep old hand-only decisions not regenerated
    for pk, prev in old_map.items():
        if pk in seen:
            continue
        out.append(prev)
    out.sort(key=lambda r: (r.get("anchor") or "", r.get("partner") or ""))
    return out


def annotate_hand_groups(rows: List[Dict[str, Any]]) -> None:
    group_map = {_pair_key(a, b): g for a, b, g in HAND_SEED_PAIRS}
    for r in rows:
        a, b = r.get("anchor"), r.get("partner")
        if not isinstance(a, str) or not isinstance(b, str):
            continue
        g = group_map.get(_pair_key(a, b))
        if not g:
            continue
        signals = r.get("signals") if isinstance(r.get("signals"), dict) else {}
        signals = dict(signals)
        signals["group"] = g
        signals["hand_seeded"] = True
        r["signals"] = signals
        r.setdefault("source", "hand_seed")


def confirm_published_herkennen(rows: List[Dict[str, Any]]) -> int:
    """Mark Honingcluster / Herkennen-asserted pairs as confirmed.

    Provenance: published docs/herkennen/niveau-1 and docs/lookalikes Honingcluster pages.
    Does not invent partners for Taraxacum / Centaurea cyanus / Tilia / Ranunculus gaps.
    """
    seed_keys = {_pair_key(a, b) for a, b, _ in HAND_SEED_PAIRS}
    n = 0
    for r in rows:
        a, b = r.get("anchor"), r.get("partner")
        if not isinstance(a, str) or not isinstance(b, str):
            continue
        if _pair_key(a, b) not in seed_keys:
            continue
        if r.get("status") in ("confirmed", "different", "unsure"):
            continue
        r["status"] = "confirmed"
        r["decided_by"] = "herkennen-published"
        n += 1
    return n


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=REVIEW_PATH,
        help="Output review YAML path",
    )
    parser.add_argument(
        "--level1-max-rank",
        type=int,
        default=LEVEL1_MAX_RANK,
        help="Level 1 rank cutoff for anchors",
    )
    parser.add_argument(
        "--confirm-published",
        action="store_true",
        help="Mark Honingcluster/Herkennen seed pairs as confirmed",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Overwrite review file without preserving prior decisions",
    )
    args = parser.parse_args()

    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit("data/pollen.yaml must be a mapping")

    beug_multi = load_beug_multi_class()
    auto = auto_candidates(data, beug_multi, level1_max=args.level1_max_rank)
    seen = {_pair_key(r["anchor"], r["partner"]) for r in auto}
    hand = hand_seed_rows(data, beug_multi, seen)
    rows = auto + hand
    annotate_hand_groups(rows)

    if not args.no_merge and args.out.exists():
        old = yaml.safe_load(args.out.read_text(encoding="utf-8")) or []
        if isinstance(old, list):
            rows = merge_preserve_decisions(rows, old)

    confirmed = 0
    if args.confirm_published:
        confirmed = confirm_published_herkennen(rows)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        yaml.safe_dump(
            rows,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        ),
        encoding="utf-8",
    )

    pending = sum(1 for r in rows if r.get("status") == "pending")
    borderline = sum(1 for r in rows if r.get("borderline"))
    print(
        f"Wrote {args.out.relative_to(REPO)}: {len(rows)} pairs "
        f"({pending} pending, {confirmed} newly confirmed from published Herkennen, "
        f"{borderline} borderline)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
