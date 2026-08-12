#!/usr/bin/env python3
"""Morph lookalike clustering (v3): preferred key size + path-gate.

Writes:
  - temp/lookalike_calculation.md (report; no YAML/key promotion)
  - docs/assets/manifests/morph-neighbours.json (closest imaged neighbours)

v2: conflict mask must not erase Beug/Eide/Reitsma outcome sizes.
v3: keep species-matched outcome size for mid; keep PK path-gates separately and
hard-separate when either preferred intervals or path-gates are non-overlapping.

Usage:
  ./.venv/bin/python scripts/morph_lookalike_cluster.py
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from pollen_display import entry_feature, entry_latin, entry_size_strings  # noqa: E402

YAML_PATH = REPO / "data" / "pollen.yaml"
REVIEW_PATH = REPO / "data" / "lookalike_review.yaml"
CONFLICT_PATH = REPO / "temp" / "reports" / "key-path-conflicts.md"
KEYS_DIR = REPO / "docs" / "keys"
OUT_PATH = REPO / "temp" / "lookalike_calculation.md"
NEIGHBOURS_PATH = REPO / "docs" / "assets" / "manifests" / "morph-neighbours.json"
NEIGHBOURS_MAX = 8

RE_NUM = re.compile(r"\d+(?:\.\d+)?")
MORPH_TOKEN_RE = re.compile(
    r"\b("
    r"psilaat|psilate|scabraat|scabrate|striaat|striate|rugulaat|rugulate|"
    r"reticulaat|reticulate|microreticulaat|microreticulate|grof|fijn|"
    r"echinaat|echinate|microechinaat|verrucaat|verrucate|"
    r"clavate|clavaat|baculaat|baculate|gemmate|gemmaat|"
    r"fenestraat|fenestrate|operculaat|operculate|inaperturaat|inaperturate|"
    r"prolaat|prolate|oblaat|oblate|sfero[iï]d|spheroidal|rond|driehoekig|"
    r"tricolporoidaat|tricolporaat|tricolpaat|triporaat|diporaat|monocolpaat|"
    r"stephanocolporaat|stephanocolpaat|stephanoporaat|periporaat|pericolpaat|"
    r"heterocolpaat|syncolpaat|dicolpaat|dicolporaat|polyade|tetrade|dyade"
    r")\b",
    re.I,
)
# Beug species line: *Name* ... \n 40,0–50,3 µm, MiW 45,3 µm
RE_BEUG_LINE = re.compile(
    r"\*([^*\n]+)\*[^\n]*\n\s*"
    r"(\d+(?:[.,]\d+)?)\s*[–\-]\s*(\d+(?:[.,]\d+)?)\s*µm"
    r"(?:[^;\n]*MiW\s*(\d+(?:[.,]\d+)?)\s*µm)?",
    re.I,
)
RE_SIZE_RANGE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*[–\-]\s*(\d+(?:[.,]\d+)?)\s*µm",
    re.I,
)
RE_MIW = re.compile(r"MiW\s*(\d+(?:[.,]\d+)?)\s*µm", re.I)
RE_LANGSTE = re.compile(r"langste\s+as\s+(\d+(?:[.,]\d+)?)\s*µm", re.I)
RE_PK_GATE = re.compile(
    r"PK\s+(groter|kleiner|kleiner dan|groter dan)?\s*"
    r"(?:dan\s+)?"
    r"(\d+(?:[.,]\d+)?)\s*(?:[–\-]\s*(\d+(?:[.,]\d+)?))?\s*µm",
    re.I,
)

BEUG_AP_TOKENS = (
    "polyadeae", "tetradeae", "dyadeae", "vesiculatae", "inaperturatae",
    "monoporatae", "monocolpatae", "syncolpatae", "dicolpatae", "dicolporatae",
    "tricolpatae", "tricolporatae", "tricolporoidatae", "stephanocolpatae",
    "stephanocolporatae", "pericolpatae", "pericolporatae", "heterocolpatae",
    "fenestratae", "diporatae", "triporatae", "stephanoporatae", "periporatae",
)
SIZE_CLASS_ORDER = ["very-small", "small", "medium", "large", "very-large"]
APERTURE_TOKEN_SET = {
    "tricolporoidaat", "tricolporaat", "tricolpaat", "triporaat", "diporaat",
    "monocolpaat", "stephanocolporaat", "stephanocolpaat", "stephanoporaat",
    "periporaat", "pericolpaat", "heterocolpaat", "syncolpaat", "dicolpaat",
    "dicolporaat", "polyade", "tetrade", "dyade", "inaperturaat", "fenestraat",
    "operculaat",
}
SHAPE_TOKEN_SET = {"prolaat", "oblaat", "sferoid", "rond", "driehoekig"}
COARSE_SCULPT = {"reticulaat", "psilaat", "scabraat"}

W_APERTURE = 3.0
W_SIZE_CLASS = 2.0
W_SIZE_CLASS_ADJ = 0.8
W_SIZE_MID = 1.2
W_SIZE_NONOVERLAP = 2.5  # non-overlapping dichotomous key intervals
W_SCULPT = 1.5
W_SHAPE = 0.8
W_ORN = 0.5
W_MISSING = 0.55
W_MISSING_APERTURE = 1.6
W_MISSING_SIZE = 1.2
W_COARSE_SCULPT = 0.55
W_BEUG = 0.7
MISSING_INFLATE = 0.25


def clean_text(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "null", "None"):
        return None
    return s


def parse_nums(raw: Optional[str]) -> List[float]:
    if not raw:
        return []
    s = str(raw).replace(",", ".").replace("µ", "u").replace("μm", " ").replace("um", " ")
    out: List[float] = []
    for n in RE_NUM.findall(s):
        try:
            out.append(float(n))
        except ValueError:
            continue
    return out


def parse_um_midpoint(smallest: Optional[str], largest: Optional[str]) -> Optional[float]:
    vals = parse_nums(smallest) + parse_nums(largest)
    if not vals:
        return None
    return (min(vals) + max(vals)) / 2.0


def parse_um_max(smallest: Optional[str], largest: Optional[str]) -> Optional[float]:
    vals = parse_nums(smallest) + parse_nums(largest)
    return max(vals) if vals else None


def size_class_from_max(max_um: Optional[float]) -> Optional[str]:
    if max_um is None:
        return None
    if max_um < 15:
        return "very-small"
    if max_um <= 25:
        return "small"
    if max_um <= 50:
        return "medium"
    if max_um <= 100:
        return "large"
    return "very-large"


def aperture_bucket(raw: Any) -> Optional[str]:
    if raw is None:
        return None
    s0 = str(raw).strip().lower()
    if not s0 or s0 in ("-", "null", "none"):
        return None
    s = (
        s0.replace("ï", "i").replace("ó", "o").replace("ö", "o")
        .replace(" ", "").replace("_", "").replace("(", "").replace(")", "").replace(">", "")
    )
    checks = [
        ("vesicul", "vesicul*"), ("fenestr", "fenestr*"), ("inapert", "inapert*"),
        ("polyade", "polyade*"), ("polyad", "polyade*"), ("tetrade", "tetrade*"),
        ("tetrad", "tetrade*"), ("dyade", "dyade*"), ("dyad", "dyade*"),
        ("stephanocolpor", "stephanocolpor*"), ("stephanocol", "stephanocol*"),
        ("stephanopor", "stephanopor*"), ("heterocol", "heterocol*"),
        ("pericolpor", "pericolpor*"), ("pericol", "pericol*"), ("peripor", "peripor*"),
        ("syncol", "syncol*"), ("dicolpor", "dicolpor*"), ("dicol", "dicol*"),
    ]
    for needle, bucket in checks:
        if needle in s:
            return bucket
    if "tricol" in s or re.search(r"(?:^|[^a-z])3-?col", s) or re.search(r"^\(?3-?\)?col", s):
        return "tricol*"
    if "monocol" in s or "sulcaat" in s or re.search(r"(?:^|[^a-z])1-?col", s):
        return "monocol*"
    if "tripor" in s or re.search(r"(?:^|[^a-z])3-?por", s):
        return "tripor*"
    if "dipor" in s or re.search(r"(?:^|[^a-z])2-?por", s):
        return "dipor*"
    if "monopor" in s or re.search(r"(?:^|[^a-z])1-?por", s):
        return "monopor*"
    if re.search(r"(?:[4-9]|1[0-9])-?colpor", s) or re.search(r"(?:[4-9]|1[0-9])-?colp", s):
        return "stephanocol*"
    if re.search(r"(?:n|[4-9]|1[0-9]|20)-?por", s):
        return "peripor*"
    return None


def beug_class_to_aperture(beug: Optional[str]) -> Optional[str]:
    if not beug:
        return None
    s = beug.lower()
    for needle, bucket in [
        ("polyade", "polyade*"), ("tetrade", "tetrade*"), ("dyade", "dyade*"),
        ("fenestr", "fenestr*"), ("inapert", "inapert*"), ("monopor", "monopor*"),
        ("monocol", "monocol*"), ("syncol", "syncol*"), ("dicolpor", "dicolpor*"),
        ("dicol", "dicol*"), ("tricolporoid", "tricol*"), ("tricolpor", "tricol*"),
        ("tricol", "tricol*"), ("stephanocolpor", "stephanocolpor*"),
        ("stephanocol", "stephanocol*"), ("stephanopor", "stephanopor*"),
        ("pericolpor", "pericolpor*"), ("pericol", "pericol*"),
        ("heterocol", "heterocol*"), ("peripor", "peripor*"),
        ("tripor", "tripor*"), ("dipor", "dipor*"), ("vesicul", "vesicul*"),
    ]:
        if needle in s:
            return bucket
    return None


def beug_family(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    s = raw.lower()
    for fam in (
        "polyade", "tetrade", "dyade", "fenestr", "inapert", "monopor", "monocol",
        "syncol", "dicolpor", "dicol", "tricolporoid", "tricolpor", "tricol",
        "stephanocolpor", "stephanocol", "stephanopor", "pericolpor", "pericol",
        "heterocol", "peripor", "tripor", "dipor", "vesicul", "striat", "retic",
        "psilat", "echinat", "clav",
    ):
        if fam in s:
            return fam
    return None


def tokenize_morph(text: Optional[str]) -> Set[str]:
    if not text:
        return set()
    s = text.lower().replace("ï", "i")
    toks: Set[str] = set()
    for m in MORPH_TOKEN_RE.finditer(s):
        t = m.group(1).lower()
        for eng, nl in (
            ("psilate", "psilaat"), ("scabrate", "scabraat"), ("striate", "striaat"),
            ("rugulate", "rugulaat"), ("reticulate", "reticulaat"),
            ("microreticulate", "microreticulaat"), ("echinate", "echinaat"),
            ("verrucate", "verrucaat"), ("clavate", "clavaat"), ("baculate", "baculaat"),
            ("gemmate", "gemmaat"), ("fenestrate", "fenestraat"),
            ("operculate", "operculaat"), ("inaperturate", "inaperturaat"),
            ("prolate", "prolaat"), ("oblate", "oblaat"), ("spheroidal", "sferoid"),
        ):
            if t == eng:
                t = nl
                break
        if t.startswith("sfero"):
            t = "sferoid"
        toks.add(t)
    return toks


def split_morph_tokens(toks: Set[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    sc, sh, ap = set(), set(), set()
    for t in toks:
        if t in APERTURE_TOKEN_SET:
            ap.add(t)
        elif t in SHAPE_TOKEN_SET:
            sh.add(t)
        else:
            sc.add(t)
    return sc, sh, ap


def jaccard_dist(a: Set[str], b: Set[str]) -> Optional[float]:
    if not a or not b:
        return None
    union = len(a | b)
    return 1.0 - (len(a & b) / union) if union else None


def rank_of(entry: Dict[str, Any]) -> Optional[int]:
    r = entry.get("learning_priority_rank")
    if isinstance(r, int) and r > 0:
        return r
    if isinstance(r, str) and r.strip().isdigit():
        v = int(r.strip())
        return v if v > 0 else None
    return None


def fnum(s: str) -> float:
    return float(s.replace(",", "."))


@dataclass
class SizeInterval:
    lo: float
    hi: float
    mid: float
    source: str  # beug|eide|reitsma|vanderham|yaml|kerkvliet-analytic|path-gate

    @property
    def max_um(self) -> float:
        return self.hi


@dataclass
class TaxonFeat:
    slug: str
    latin: str = ""
    rank: Optional[int] = None
    # Preferred size for clustering (dichotomous key > YAML when conflict-masked)
    mid_um: Optional[float] = None
    max_um: Optional[float] = None
    size_class: Optional[str] = None
    size_interval: Optional[SizeInterval] = None
    size_source: str = ""
    path_gate: Optional[SizeInterval] = None  # dichotomous PK gate; not used as mid
    yaml_mid: Optional[float] = None
    key_sizes: List[SizeInterval] = field(default_factory=list)
    aperture: Optional[str] = None
    aperture_bucket: Optional[str] = None
    beug_class: Optional[str] = None
    beug_fam: Optional[str] = None
    sculpture: Set[str] = field(default_factory=set)
    shape: Set[str] = field(default_factory=set)
    ornamentation: Set[str] = field(default_factory=set)
    mask_yaml_size: bool = False  # YAML/Kerkvliet analytic unreliable
    mask_sculpt: bool = False
    provenance: List[str] = field(default_factory=list)
    key_hits: Set[str] = field(default_factory=set)
    feature_count: int = 0
    sparse: bool = False


def intervals_overlap(a: SizeInterval, b: SizeInterval) -> bool:
    return not (a.hi < b.lo or b.hi < a.lo)


def parse_conflict_mask(path: Path) -> Dict[str, Set[str]]:
    masks: Dict[str, Set[str]] = defaultdict(set)
    if not path.is_file():
        return {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        m = re.match(r"`([a-z0-9_]+)`", parts[0])
        if not m:
            continue
        slug = m.group(1)
        claim = parts[2].lower()
        if "grain size" in claim or ("non-overlapping" in claim and "µm" in claim) or (
            "size" in claim and "µm" in claim
        ):
            masks[slug].add("size")
        if "morphology" in claim or "contradictory path morphology" in claim:
            masks[slug].add("sculpt")
    return dict(masks)


def taxa_with_images(data: Dict[str, Any]) -> Set[str]:
    """Slugs that have at least one image path in YAML."""
    out: Set[str] = set()
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        imgs = entry.get("images")
        if not isinstance(imgs, list):
            continue
        for im in imgs:
            if isinstance(im, dict) and isinstance(im.get("path"), str) and im["path"].strip():
                out.add(str(slug))
                break
    return out


def build_neighbours_json(
    clusterable: List[str],
    dist_map: Dict[Tuple[str, str], float],
    imaged: Set[str],
    max_n: int = NEIGHBOURS_MAX,
) -> Dict[str, Any]:
    """Closest morph neighbours per imaged slug (closest first, max_n)."""
    neighbours: Dict[str, List[str]] = {}
    imaged_clusterable = [s for s in clusterable if s in imaged]
    for a in imaged_clusterable:
        pairs: List[Tuple[float, str]] = []
        for b in imaged_clusterable:
            if a == b:
                continue
            key = (a, b) if a < b else (b, a)
            d = dist_map.get(key)
            if d is None:
                continue
            pairs.append((d, b))
        pairs.sort(key=lambda x: (x[0], x[1]))
        neighbours[a] = [b for _, b in pairs[:max_n]]
    return {"version": 1, "neighbours": neighbours}


def collect_pollen_keys_from_choice(ch: Dict[str, Any]) -> List[str]:
    keys: List[str] = []
    for node in (ch.get("id"), ch.get("outcome")):
        if not isinstance(node, dict):
            continue
        pk = node.get("pollen_key")
        if isinstance(pk, str) and pk.strip():
            keys.append(pk.strip())
        pks = node.get("pollen_keys")
        if isinstance(pks, list):
            for x in pks:
                if isinstance(x, str) and x.strip():
                    keys.append(x.strip())
    return keys


def choice_label_text(ch: Dict[str, Any]) -> str:
    bits: List[str] = []
    if isinstance(ch.get("label"), str):
        bits.append(ch["label"])
    for node in (ch.get("id"), ch.get("outcome")):
        if not isinstance(node, dict):
            continue
        for k in ("text", "name", "note", "note_plant"):
            if isinstance(node.get(k), str):
                bits.append(node[k])
    return " ".join(bits)


def slug_to_latin_guess(slug: str) -> str:
    return slug.replace("_", " ")


def extract_key_size_from_outcome(
    text: str, pollen_key: str, system: str, source_path: str
) -> Optional[SizeInterval]:
    """Prefer species-line size matching pollen_key; else first MiW/range in outcome."""
    latin = slug_to_latin_guess(pollen_key)
    # Try exact species line
    for m in RE_BEUG_LINE.finditer(text):
        name = m.group(1).strip().lower()
        # strip authorship noise: take first two words
        name_core = " ".join(name.split()[:2])
        latin_core = " ".join(latin.split()[:2])
        if name_core == latin_core or latin_core in name or name_core in latin:
            lo, hi = fnum(m.group(2)), fnum(m.group(3))
            mid = fnum(m.group(4)) if m.group(4) else (lo + hi) / 2.0
            return SizeInterval(lo, hi, mid, f"{system}:{source_path}")
    # langste as (Eide)
    m = RE_LANGSTE.search(text)
    if m:
        v = fnum(m.group(1))
        return SizeInterval(v, v, v, f"{system}:{source_path}")
    # MiW
    m = RE_MIW.search(text)
    if m:
        v = fnum(m.group(1))
        # try nearby range
        rm = RE_SIZE_RANGE.search(text)
        if rm:
            lo, hi = fnum(rm.group(1)), fnum(rm.group(2))
            return SizeInterval(lo, hi, v, f"{system}:{source_path}")
        return SizeInterval(v, v, v, f"{system}:{source_path}")
    rm = RE_SIZE_RANGE.search(text)
    if rm:
        lo, hi = fnum(rm.group(1)), fnum(rm.group(2))
        return SizeInterval(lo, hi, (lo + hi) / 2.0, f"{system}:{source_path}")
    return None


def extract_path_gate_size(labels: List[str], system: str, source_path: str) -> Optional[SizeInterval]:
    """Infer a size band from dichotomous PK size gates on the path."""
    # Collect the most specific gate (last matching)
    lo = hi = None
    for lab in labels:
        m = RE_PK_GATE.search(lab)
        if not m:
            # also "PK 42–50 µm"
            m2 = re.search(
                r"PK\s+(\d+(?:[.,]\d+)?)\s*[–\-]\s*(\d+(?:[.,]\d+)?)\s*µm", lab, re.I
            )
            if m2:
                lo, hi = fnum(m2.group(1)), fnum(m2.group(2))
            continue
        cmp_word = (m.group(1) or "").lower()
        a = fnum(m.group(2))
        b = fnum(m.group(3)) if m.group(3) else None
        if b is not None:
            lo, hi = a, b
        elif "kleiner" in cmp_word:
            lo, hi = 0.0, a
        elif "groter" in cmp_word:
            lo, hi = a, 200.0
    if lo is None or hi is None:
        return None
    return SizeInterval(lo, hi, (lo + hi) / 2.0, f"path-gate:{system}:{source_path}")


def walk_step_graph(key_json: Dict[str, Any], system: str, source_path: str) -> Dict[str, Dict[str, Any]]:
    start = key_json.get("start")
    steps = key_json.get("steps")
    if not isinstance(start, str) or not isinstance(steps, dict):
        return {}
    acc: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "tokens": set(),
            "sizes": [],
            "sources": set(),
            "labels": [],
            "analytic": False,
        }
    )

    def dfs(step_id: str, path_labels: List[str], seen: Set[str]) -> None:
        if step_id in seen:
            return
        seen2 = set(seen)
        seen2.add(step_id)
        step = steps.get(step_id)
        if not isinstance(step, dict):
            return
        choices = step.get("choices")
        if not isinstance(choices, list):
            return
        for ch in choices:
            if not isinstance(ch, dict):
                continue
            lab = ch.get("label") if isinstance(ch.get("label"), str) else ""
            new_path = path_labels + ([lab] if lab else [])
            pks = collect_pollen_keys_from_choice(ch)
            if pks:
                blob = " ".join(new_path + [choice_label_text(ch)])
                toks = tokenize_morph(blob)
                gate = extract_path_gate_size(new_path, system, source_path)
                for pk in pks:
                    acc[pk]["tokens"] |= toks
                    acc[pk]["sources"].add(f"{system}:{source_path}")
                    if lab:
                        acc[pk]["labels"].append(lab[:160])
                    # outcome size
                    out_text = ""
                    for node in (ch.get("outcome"), ch.get("id")):
                        if isinstance(node, dict) and isinstance(node.get("text"), str):
                            out_text = node["text"]
                            break
                    if out_text:
                        sz = extract_key_size_from_outcome(out_text, pk, system, source_path)
                        if sz:
                            acc[pk]["sizes"].append(sz)
                    if gate:
                        acc[pk]["sizes"].append(gate)
            nxt = ch.get("next")
            if isinstance(nxt, str) and nxt.strip():
                dfs(nxt.strip(), new_path, seen2)

    dfs(start.strip(), [], set())
    return acc


def walk_kerkvliet(key_json: Dict[str, Any], source_path: str) -> Dict[str, Dict[str, Any]]:
    acc: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"tokens": set(), "sizes": [], "sources": set(), "labels": [], "analytic": True}
    )
    rows = key_json.get("rows")
    if not isinstance(rows, list):
        return {}
    for r in rows:
        if not isinstance(r, dict):
            continue
        pk = r.get("pollen_key")
        if not isinstance(pk, str) or not pk.strip():
            continue
        pk = pk.strip()
        sec = r.get("section") if isinstance(r.get("section"), str) else ""
        acc[pk]["tokens"] |= tokenize_morph(sec)
        if sec:
            acc[pk]["labels"].append(sec[:160])
        acc[pk]["sources"].add(f"kerkvliet-analytic:{source_path}")
        acc[pk]["analytic"] = True
    return acc


def scan_all_keys() -> Dict[str, Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "tokens": set(),
            "sizes": [],
            "sources": set(),
            "labels": [],
            "beug_classes": set(),
            "analytic": False,
        }
    )
    for path in sorted(KEYS_DIR.rglob("*.json")):
        rel = str(path.relative_to(REPO))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        name = path.name.lower()
        system = path.parent.name
        if "kerkvliet" in name or system == "kerkvliet":
            part = walk_kerkvliet(data, rel)
        elif "steps" in data and "start" in data:
            part = walk_step_graph(data, system, rel)
        else:
            part = {}
        beug_classes = [t for t in BEUG_AP_TOKENS if t in name]
        for pk, info in part.items():
            merged[pk]["tokens"] |= info.get("tokens", set())
            merged[pk]["sizes"].extend(info.get("sizes", []))
            merged[pk]["sources"] |= info.get("sources", set())
            merged[pk]["labels"].extend(info.get("labels", [])[:5])
            if info.get("analytic"):
                merged[pk]["analytic"] = True
            for bc in beug_classes:
                merged[pk]["beug_classes"].add(bc)
    return merged


def _system_of_size(source: str) -> str:
    if source.startswith("path-gate:"):
        return "path-gate"
    if "analytic" in source:
        return "analytic"
    return source.split(":")[0]


def prefer_key_size(sizes: List[SizeInterval]) -> Optional[SizeInterval]:
    """Prefer dichotomous outcome sizes for mid: beug > eide/reitsma/vanderham > path-gate fallback."""
    if not sizes:
        return None

    order = ("beug", "eide", "reitsma", "feagri-iversen", "vanderham", "path-gate")
    for pref in order:
        cands = [s for s in sizes if _system_of_size(s.source) == pref]
        if not cands:
            continue
        if pref == "path-gate":
            pool = list(cands)
            pool.sort(key=lambda s: (
                0 if (s.lo > 0.5 and s.hi < 150) else 1,
                s.hi - s.lo,
                abs(s.mid),
            ))
            return pool[0]
        finite = [s for s in cands if s.lo > 0.5 and s.hi < 150]
        pool = finite or cands
        pool.sort(key=lambda s: (s.hi - s.lo, abs(s.mid)))
        return pool[0]
    return None


def prefer_path_gate(sizes: List[SizeInterval]) -> Optional[SizeInterval]:
    """Most specific dichotomous PK path-gate (never used as taxon mid when open-ended)."""
    gates = [s for s in sizes if _system_of_size(s.source) == "path-gate"]
    if not gates:
        return None
    gates.sort(key=lambda s: (
        (0 if s.lo > 0.5 else 1) + (0 if s.hi < 150 else 1),
        s.hi - s.lo,
        abs(s.mid),
    ))
    return gates[0]


def build_features(
    data: Dict[str, Any],
    key_attrs: Dict[str, Dict[str, Any]],
    masks: Dict[str, Set[str]],
) -> Dict[str, TaxonFeat]:
    feats: Dict[str, TaxonFeat] = {}
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        tf = TaxonFeat(slug=slug)
        tf.latin = entry_latin(entry) or slug
        tf.rank = rank_of(entry)
        ss, ls = entry_size_strings(entry)
        tf.yaml_mid = parse_um_midpoint(ss, ls)
        yaml_max = parse_um_max(ss, ls)
        if ss or ls:
            tf.provenance.append("data/pollen.yaml:size")

        ap = clean_text(entry_feature(entry, "aperture"))
        sc = clean_text(entry_feature(entry, "sculpture"))
        sh = clean_text(entry_feature(entry, "shape"))
        orn = clean_text(entry_feature(entry, "ornamentation"))
        beug = clean_text(entry.get("pollen_class_beug"))
        tf.aperture = ap
        tf.beug_class = beug
        tf.beug_fam = beug_family(beug)
        tf.aperture_bucket = aperture_bucket(ap) or beug_class_to_aperture(beug)
        sc_toks, sh_from_sc, ap_from_sc = split_morph_tokens(tokenize_morph(sc))
        tf.sculpture = sc_toks
        tf.shape = split_morph_tokens(tokenize_morph(sh))[1] | sh_from_sc
        tf.ornamentation = split_morph_tokens(tokenize_morph(orn))[0]
        if ap_from_sc and not tf.aperture_bucket:
            for t in ap_from_sc:
                b = aperture_bucket(t)
                if b:
                    tf.aperture_bucket = b
                    break
        if ap:
            tf.provenance.append("data/pollen.yaml:aperture")
        if sc:
            tf.provenance.append("data/pollen.yaml:sculpture")
        if sh:
            tf.provenance.append("data/pollen.yaml:shape")
        if orn:
            tf.provenance.append("data/pollen.yaml:ornamentation")
        if beug:
            tf.provenance.append("data/pollen.yaml:pollen_class_beug")

        # YAML beug_key_paths size gates (already published path)
        bkp = entry.get("beug_key_paths")
        if isinstance(bkp, list):
            for item in bkp:
                if not isinstance(item, dict):
                    continue
                chosen = item.get("chosen")
                if isinstance(chosen, list):
                    labs = [str(x) for x in chosen if x]
                    gate = extract_path_gate_size(labs, "beug", "yaml:beug_key_paths")
                    if gate:
                        tf.key_sizes.append(gate)
                        tf.provenance.append("data/pollen.yaml:beug_key_paths")

        pf = entry.get("pollen_features", {})
        if isinstance(pf, dict):
            ctrl = pf.get("controlled")
            if isinstance(ctrl, dict):
                sc_c = clean_text(ctrl.get("sculptuur") or ctrl.get("sculpture"))
                ap_c = clean_text(ctrl.get("apertuur") or ctrl.get("aperture"))
                sh_c = clean_text(ctrl.get("vorm") or ctrl.get("shape"))
                gb_c = clean_text(ctrl.get("grootteklasse") or ctrl.get("size_band"))
                if sc_c:
                    tf.sculpture |= split_morph_tokens(tokenize_morph(sc_c))[0]
                    tf.provenance.append("data/pollen.yaml:controlled.sculptuur")
                if ap_c:
                    if not tf.aperture_bucket:
                        tf.aperture_bucket = aperture_bucket(ap_c)
                    if not tf.aperture:
                        tf.aperture = ap_c
                    tf.provenance.append("data/pollen.yaml:controlled.apertuur")
                if sh_c:
                    tf.shape |= split_morph_tokens(tokenize_morph(sh_c))[1]
                    tf.provenance.append("data/pollen.yaml:controlled.vorm")
                if gb_c:
                    nums = parse_nums(gb_c)
                    if len(nums) >= 2 and tf.yaml_mid is None:
                        tf.yaml_mid = (min(nums) + max(nums)) / 2.0
                        yaml_max = max(nums)
                        tf.provenance.append("data/pollen.yaml:controlled.grootteklasse")

        mset = masks.get(slug, set())
        tf.mask_yaml_size = "size" in mset
        tf.mask_sculpt = "sculpt" in mset

        ka = key_attrs.get(slug)
        if ka:
            tf.key_hits = {s.split(":")[0] for s in ka.get("sources", set())}
            k_sc, k_sh, k_ap = split_morph_tokens(set(ka.get("tokens", set())))
            if not tf.mask_sculpt:
                tf.sculpture |= k_sc
            tf.shape |= k_sh
            if not tf.aperture_bucket:
                for t in k_ap:
                    b = aperture_bucket(t)
                    if b:
                        tf.aperture_bucket = b
                        break
            for sz in ka.get("sizes", []):
                if isinstance(sz, SizeInterval):
                    # Skip kerkvliet-analytic sizes when conflict-masked
                    if tf.mask_yaml_size and "analytic" in sz.source:
                        continue
                    tf.key_sizes.append(sz)
            if not tf.aperture_bucket:
                for bc in ka.get("beug_classes", set()):
                    b = beug_class_to_aperture(bc)
                    if b:
                        tf.aperture_bucket = b
                        tf.provenance.append(f"docs/keys/beug:filename_class:{bc}")
                        break
            if not tf.beug_fam:
                for bc in ka.get("beug_classes", set()):
                    fam = beug_family(bc)
                    if fam:
                        tf.beug_fam = fam
                        break
            for src in sorted(ka.get("sources", set()))[:8]:
                tf.provenance.append(src)
            if ka.get("analytic"):
                tf.provenance.append("kerkvliet:analytic (not dichotomous source)")

        # Resolve preferred size (outcome/species line) + separate path-gate
        key_pref = prefer_key_size(tf.key_sizes)
        tf.path_gate = prefer_path_gate(tf.key_sizes)
        if tf.path_gate:
            tf.provenance.append(f"path_gate:{tf.path_gate.source}")
        if key_pref and _system_of_size(key_pref.source) != "path-gate":
            tf.size_interval = key_pref
            tf.mid_um = key_pref.mid
            tf.max_um = key_pref.max_um
            tf.size_class = size_class_from_max(key_pref.max_um)
            tf.size_source = key_pref.source
            tf.provenance.append(f"size_preferred:{key_pref.source}")
        elif key_pref and _system_of_size(key_pref.source) == "path-gate":
            # No outcome size: keep path-gate for hard-sep only; do not use open mid
            if key_pref.lo > 0.5 and key_pref.hi < 150:
                tf.size_interval = key_pref
                tf.mid_um = key_pref.mid
                tf.max_um = key_pref.max_um
                tf.size_class = size_class_from_max(key_pref.max_um)
                tf.size_source = key_pref.source
                tf.provenance.append(f"size_preferred:{key_pref.source}")
            else:
                tf.size_source = "path_gate_open_no_mid"
                tf.provenance.append("size:path_gate_only_open_bounds")
        elif not tf.mask_yaml_size and tf.yaml_mid is not None:
            tf.mid_um = tf.yaml_mid
            tf.max_um = yaml_max
            tf.size_class = size_class_from_max(yaml_max)
            tf.size_source = "yaml"
            tf.size_interval = SizeInterval(
                parse_nums(ss)[0] if parse_nums(ss) else tf.yaml_mid,
                parse_nums(ls)[-1] if parse_nums(ls) else tf.yaml_mid,
                tf.yaml_mid,
                "yaml",
            )
        elif not tf.mask_yaml_size and tf.yaml_mid is None:
            pass
        else:
            # YAML masked and no key size: size unknown for clustering
            tf.mid_um = None
            tf.max_um = None
            tf.size_class = None
            tf.size_source = "masked_no_key_size"
            tf.provenance.append("size:masked_yaml_no_dichotomous_key_size")

        n = 0
        if tf.aperture_bucket:
            n += 1
        if tf.size_class or tf.mid_um is not None:
            n += 1
        if tf.sculpture and not tf.mask_sculpt:
            n += 1
        if tf.shape:
            n += 1
        if tf.ornamentation:
            n += 1
        tf.feature_count = n
        has_size = tf.size_class is not None or tf.mid_um is not None
        has_sculpt = bool(tf.sculpture) and not tf.mask_sculpt
        tf.sparse = (not tf.aperture_bucket) or (n < 2) or not (has_size or has_sculpt)
        if n >= 1:
            feats[slug] = tf
    return feats


def pair_distance(a: TaxonFeat, b: TaxonFeat) -> Tuple[float, Dict[str, Any]]:
    d = 0.0
    dims_used = 0
    evidence: Dict[str, Any] = {}

    if a.aperture_bucket and b.aperture_bucket:
        dims_used += 1
        if a.aperture_bucket != b.aperture_bucket:
            d += W_APERTURE
            evidence["aperture"] = f"mismatch {a.aperture_bucket} vs {b.aperture_bucket}"
        else:
            evidence["aperture"] = f"same {a.aperture_bucket}"
    else:
        d += W_MISSING_APERTURE
        evidence["aperture"] = "missing_one_or_both"

    # Size: preferred intervals + path-gates; hard-sep if either non-overlaps
    a_ok = a.mid_um is not None or a.size_interval is not None or a.path_gate is not None
    b_ok = b.mid_um is not None or b.size_interval is not None or b.path_gate is not None
    if a_ok and b_ok:
        dims_used += 1
        evidence["size_source"] = f"{a.size_source or 'none'} vs {b.size_source or 'none'}"
        hard_bits: List[str] = []
        if a.size_interval and b.size_interval and not intervals_overlap(a.size_interval, b.size_interval):
            hard_bits.append(
                "non_overlapping_key_intervals "
                f"{a.size_interval.lo:.1f}–{a.size_interval.hi:.1f} vs "
                f"{b.size_interval.lo:.1f}–{b.size_interval.hi:.1f}"
            )
        if a.path_gate and b.path_gate and not intervals_overlap(a.path_gate, b.path_gate):
            hard_bits.append(
                "non_overlapping_path_gates "
                f"{a.path_gate.lo:.1f}–{a.path_gate.hi:.1f} vs "
                f"{b.path_gate.lo:.1f}–{b.path_gate.hi:.1f}"
            )
            evidence["path_gate"] = (
                f"{a.path_gate.lo:.1f}–{a.path_gate.hi:.1f} vs "
                f"{b.path_gate.lo:.1f}–{b.path_gate.hi:.1f}"
            )
        elif a.path_gate and b.path_gate:
            evidence["path_gate"] = (
                f"overlap {a.path_gate.lo:.1f}–{a.path_gate.hi:.1f} / "
                f"{b.path_gate.lo:.1f}–{b.path_gate.hi:.1f}"
            )
        if hard_bits:
            d += W_SIZE_NONOVERLAP
            evidence["size"] = "; ".join(hard_bits)
        else:
            if a.size_class and b.size_class:
                if a.size_class == b.size_class:
                    evidence["size_class"] = f"same {a.size_class}"
                else:
                    ia = SIZE_CLASS_ORDER.index(a.size_class) if a.size_class in SIZE_CLASS_ORDER else -1
                    ib = SIZE_CLASS_ORDER.index(b.size_class) if b.size_class in SIZE_CLASS_ORDER else -1
                    if ia >= 0 and ib >= 0 and abs(ia - ib) == 1:
                        d += W_SIZE_CLASS_ADJ
                        evidence["size_class"] = f"adjacent {a.size_class}/{b.size_class}"
                    else:
                        d += W_SIZE_CLASS
                        evidence["size_class"] = f"mismatch {a.size_class}/{b.size_class}"
            if a.mid_um is not None and b.mid_um is not None:
                gap = abs(a.mid_um - b.mid_um)
                d += W_SIZE_MID * (gap / 5.0)
                evidence["size_mid_gap_um"] = round(gap, 2)
    else:
        d += W_MISSING_SIZE
        evidence["size"] = "missing_one_or_both"

    if a.mask_sculpt or b.mask_sculpt:
        evidence["sculpture"] = "masked_conflict"
        d += W_MISSING * 0.5
    else:
        jd = jaccard_dist(a.sculpture, b.sculpture)
        if jd is None:
            d += W_MISSING
            evidence["sculpture"] = "missing_one_or_both"
        else:
            dims_used += 1
            d += W_SCULPT * jd
            shared = sorted(a.sculpture & b.sculpture)
            evidence["sculpture"] = {"jaccard_dist": round(jd, 3), "shared": shared[:8]}
            if (
                jd == 0.0
                and len(a.sculpture) == 1
                and len(b.sculpture) == 1
                and shared
                and shared[0] in COARSE_SCULPT
            ):
                sh_jd = jaccard_dist(a.shape, b.shape)
                if sh_jd is None or sh_jd > 0.5:
                    d += W_COARSE_SCULPT
                    evidence["coarse_sculpt_penalty"] = shared[0]

    if a.beug_fam and b.beug_fam:
        dims_used += 1
        sculpt_beug = {"striat", "retic", "psilat", "echinat", "clav"}
        if a.beug_fam != b.beug_fam:
            if a.beug_fam in sculpt_beug or b.beug_fam in sculpt_beug:
                d += W_BEUG * 0.5
                evidence["beug_fam"] = f"qualifier_mismatch {a.beug_fam}/{b.beug_fam}"
            else:
                d += W_BEUG
                evidence["beug_fam"] = f"mismatch {a.beug_fam}/{b.beug_fam}"
        else:
            evidence["beug_fam"] = f"same {a.beug_fam}"

    jd = jaccard_dist(a.shape, b.shape)
    if jd is None:
        d += MISSING_INFLATE
        evidence["shape"] = "missing_one_or_both"
    else:
        dims_used += 1
        d += W_SHAPE * jd
        evidence["shape"] = {"jaccard_dist": round(jd, 3), "shared": sorted(a.shape & b.shape)[:6]}

    jd = jaccard_dist(a.ornamentation, b.ornamentation)
    if jd is None:
        d += MISSING_INFLATE * 0.5
        evidence["ornamentation"] = "missing_one_or_both"
    else:
        dims_used += 1
        d += W_ORN * jd
        evidence["ornamentation"] = {
            "jaccard_dist": round(jd, 3),
            "shared": sorted(a.ornamentation & b.ornamentation)[:6],
        }

    evidence["dims_used"] = dims_used
    evidence["distance"] = round(d, 4)
    return d, evidence


def complete_linkage_clusters(
    labels: List[str], dist_map: Dict[Tuple[str, str], float], threshold: float
) -> List[Set[str]]:
    parent = {lab: lab for lab in labels}
    ranku = {lab: 0 for lab in labels}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if ranku[ra] < ranku[rb]:
            parent[ra] = rb
        elif ranku[ra] > ranku[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            ranku[ra] += 1

    def members_of(root: str) -> List[str]:
        return [x for x in labels if find(x) == root]

    edges = []
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            key = (a, b) if a < b else (b, a)
            edges.append((dist_map[key], a, b))
    edges.sort()
    for d, a, b in edges:
        if d > threshold:
            break
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        ca, cb = members_of(ra), members_of(rb)
        ok = True
        for x in ca:
            for y in cb:
                key = (x, y) if x < y else (y, x)
                if dist_map[key] > threshold:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            union(ra, rb)
    groups: Dict[str, Set[str]] = defaultdict(set)
    for lab in labels:
        groups[find(lab)].add(lab)
    return list(groups.values())


def load_already_decided(data: Dict[str, Any], review_path: Path) -> Dict[Tuple[str, str], str]:
    out: Dict[Tuple[str, str], str] = {}
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        lk = entry.get("lookalikes")
        if not isinstance(lk, dict):
            continue
        pairs = lk.get("pairs")
        if not isinstance(pairs, list):
            continue
        for p in pairs:
            if not isinstance(p, dict):
                continue
            partner, status = p.get("partner"), p.get("status")
            if isinstance(partner, str) and status in ("confirmed", "different"):
                key = (slug, partner) if slug <= partner else (partner, slug)
                out[key] = f"yaml:{status}"
    if review_path.is_file():
        rev = yaml.safe_load(review_path.read_text(encoding="utf-8"))
        if isinstance(rev, list):
            for row in rev:
                if not isinstance(row, dict):
                    continue
                a, b, st = row.get("anchor"), row.get("partner"), row.get("status")
                if isinstance(a, str) and isinstance(b, str) and st in ("confirmed", "different"):
                    key = (a, b) if a <= b else (b, a)
                    out[key] = f"review:{st}"
    return out


def typ_genus(slug: str) -> Optional[str]:
    return slug[: -len("_typ")] if slug.endswith("_typ") else None


def species_typ_flag(members: Set[str]) -> List[str]:
    flags: List[str] = []
    typs = [m for m in members if m.endswith("_typ")]
    specs = [m for m in members if not m.endswith("_typ")]
    for t in typs:
        g = typ_genus(t)
        if not g:
            continue
        for s in specs:
            if s == g or s.startswith(g + "_"):
                flags.append(f"{s} ↔ {t}")
    return flags


def cluster_summary_bits(members: Set[str], feats: Dict[str, TaxonFeat]) -> Dict[str, Any]:
    fs = [feats[m] for m in members if m in feats]
    aps = {f.aperture_bucket for f in fs if f.aperture_bucket}
    scs = {f.size_class for f in fs if f.size_class}
    mids = [f.mid_um for f in fs if f.mid_um is not None]
    shared_sculpt = (
        set.intersection(*(f.sculpture for f in fs))
        if fs and all(f.sculpture and not f.mask_sculpt for f in fs)
        else set()
    )
    ranks = sorted({f.rank for f in fs if f.rank is not None})
    return {
        "aperture_buckets": sorted(aps),
        "size_classes": sorted(scs),
        "mid_range": (round(min(mids), 1), round(max(mids), 1)) if mids else None,
        "shared_sculpture": sorted(shared_sculpt)[:10],
        "ranks": ranks,
        "has_rank": bool(ranks),
    }


def fmt_member(f: TaxonFeat) -> str:
    r = f"rank={f.rank}" if f.rank else "unranked"
    bits = [f"`{f.slug}`", f"*{f.latin}*", r]
    if f.aperture_bucket:
        bits.append(f"ap={f.aperture_bucket}")
    if f.size_class:
        bits.append(f"class={f.size_class}")
    if f.mid_um is not None:
        bits.append(f"mid={f.mid_um:.1f}µm")
    if f.size_source:
        bits.append(f"size_src={f.size_source.split(':')[0]}")
    if f.path_gate is not None:
        bits.append(f"path_gate={f.path_gate.lo:.0f}–{f.path_gate.hi:.0f}")
    if f.mask_yaml_size:
        bits.append("yaml_size_MASKED")
    if f.mask_sculpt:
        bits.append("sculpt_MASKED")
    if f.sculpture and not f.mask_sculpt:
        bits.append("sc={" + ",".join(sorted(f.sculpture)[:5]) + "}")
    return " | ".join(bits)


def calibrate_thresholds(
    feats: Dict[str, TaxonFeat], decided: Dict[Tuple[str, str], str], dist_map: Dict[Tuple[str, str], float]
) -> Tuple[float, float, List[str]]:
    notes: List[str] = []
    conf_d: List[float] = []
    diff_d: List[float] = []
    for (a, b), st in decided.items():
        if a not in feats or b not in feats:
            continue
        key = (a, b) if a < b else (b, a)
        if key not in dist_map:
            continue
        d = dist_map[key]
        if "confirmed" in st:
            conf_d.append(d)
        elif "different" in st:
            diff_d.append(d)
    notes.append(f"Calibration pairs with distance: confirmed n={len(conf_d)}, different n={len(diff_d)}")
    if conf_d:
        notes.append(
            f"Confirmed distance: min={min(conf_d):.3f} median={sorted(conf_d)[len(conf_d)//2]:.3f} max={max(conf_d):.3f}"
        )
    if diff_d:
        notes.append(
            f"Different distance: min={min(diff_d):.3f} median={sorted(diff_d)[len(diff_d)//2]:.3f} max={max(diff_d):.3f}"
        )
    tight, loose = 1.00, 1.75
    notes.append(
        "Confirmed vs different may overlap; using guidance defaults "
        f"tight={tight:.3f}, loose={loose:.3f}."
    )
    # Explicit sanity: trifolium pair — species lines + path-gates
    for pair in (("trifolium_pratense", "trifolium_repens"),):
        a, b = pair
        key = (a, b) if a < b else (b, a)
        if key in dist_map and a in feats and b in feats:
            fa, fb = feats[a], feats[b]

            def _iv(f: TaxonFeat) -> str:
                if f.size_interval:
                    return f"{f.size_interval.lo:.1f}–{f.size_interval.hi:.1f} (MiW {f.mid_um})"
                return "n/a"

            def _pg(f: TaxonFeat) -> str:
                if f.path_gate:
                    return f"{f.path_gate.lo:.0f}–{f.path_gate.hi:.0f}"
                return "n/a"

            notes.append(
                f"Sanity `{a}`–`{b}` distance={dist_map[key]:.3f} "
                f"(species {_iv(fa)} vs {_iv(fb)}; path_gate {_pg(fa)} vs {_pg(fb)})"
            )
    if conf_d:
        notes.append(
            f"Fraction confirmed ≤ tight: {sum(1 for d in conf_d if d <= tight)/len(conf_d):.2f}; "
            f"≤ loose: {sum(1 for d in conf_d if d <= loose)/len(conf_d):.2f}"
        )
    if diff_d:
        notes.append(
            f"Fraction different ≤ tight: {sum(1 for d in diff_d if d <= tight)/len(diff_d):.2f}; "
            f"≤ loose: {sum(1 for d in diff_d if d <= loose)/len(diff_d):.2f}"
        )
    return tight, loose, notes


def main() -> None:
    t0 = time.perf_counter()
    print("Loading YAML…")
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    imaged = taxa_with_images(data)
    print(f"  taxa with images: {len(imaged)}")
    print("Parsing conflict mask…")
    if not CONFLICT_PATH.is_file():
        print(f"  note: {CONFLICT_PATH.relative_to(REPO)} missing; using empty mask")
    masks = parse_conflict_mask(CONFLICT_PATH)
    print(f"  masked taxa: {len(masks)}")
    print("Scanning keys…")
    key_attrs = scan_all_keys()
    print(f"  key attribute taxa: {len(key_attrs)}")
    print("Building features…")
    feats = build_features(data, key_attrs, masks)
    # Debug trifolium
    for s in ("trifolium_pratense", "trifolium_repens"):
        f = feats.get(s)
        if f:
            print(
                f"  DEBUG {s}: mid={f.mid_um} class={f.size_class} src={f.size_source} "
                f"interval={f.size_interval} path_gate={f.path_gate} "
                f"yaml_masked={f.mask_yaml_size} sc={f.sculpture}"
            )
            if s in feats and "trifolium_repens" in feats and s == "trifolium_pratense":
                d, ev = pair_distance(feats["trifolium_pratense"], feats["trifolium_repens"])
                print(f"  DEBUG pair distance={d:.3f} ev={ev}")

    sparse = {k for k, v in feats.items() if v.sparse}
    clusterable = sorted(k for k, v in feats.items() if not v.sparse)
    print(f"  features={len(feats)} clusterable={len(clusterable)} sparse={len(sparse)}")
    decided = load_already_decided(data, REVIEW_PATH)

    print("Pairwise distances…")
    dist_map: Dict[Tuple[str, str], float] = {}
    evid_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    n = len(clusterable)
    for i, a in enumerate(clusterable):
        if i % 50 == 0:
            print(f"  {i}/{n}")
        fa = feats[a]
        for b in clusterable[i + 1 :]:
            d, ev = pair_distance(fa, feats[b])
            dist_map[(a, b)] = d
            evid_map[(a, b)] = ev
    for (a, b) in decided:
        if a in feats and b in feats:
            key = (a, b) if a < b else (b, a)
            if key not in dist_map:
                d, ev = pair_distance(feats[a], feats[b])
                dist_map[key] = d
                evid_map[key] = ev

    neighbours_payload = build_neighbours_json(clusterable, dist_map, imaged)
    NEIGHBOURS_PATH.parent.mkdir(parents=True, exist_ok=True)
    NEIGHBOURS_PATH.write_text(
        json.dumps(neighbours_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {NEIGHBOURS_PATH.relative_to(REPO)} "
        f"({len(neighbours_payload['neighbours'])} imaged taxa with neighbour lists)"
    )

    tight_t, loose_t, cal_notes = calibrate_thresholds(feats, decided, dist_map)
    print("Calibration:", cal_notes)
    linkage_note = (
        "Complete-linkage cut on pairwise morph distance; "
        "species-matched key outcome sizes for mid; path-gates hard-separate when non-overlapping"
    )
    print("Clustering…")
    tight_sets = [c for c in complete_linkage_clusters(clusterable, dist_map, tight_t) if len(c) >= 2]
    loose_sets = [c for c in complete_linkage_clusters(clusterable, dist_map, loose_t) if len(c) >= 2]

    def sort_key(c: Set[str]) -> Tuple:
        summ = cluster_summary_bits(c, feats)
        min_rank = min(summ["ranks"]) if summ["ranks"] else 9999
        return (0 if summ["has_rank"] else 1, min_rank, -len(c), sorted(c)[0])

    tight_sets.sort(key=sort_key)
    loose_sets.sort(key=sort_key)
    print(f"Tight={len(tight_sets)} Loose={len(loose_sets)}")
    # Verify trifolium not co-clustered
    for label, sets in (("tight", tight_sets), ("loose", loose_sets)):
        together = any("trifolium_pratense" in c and "trifolium_repens" in c for c in sets)
        print(f"  trifolium pair co-clustered ({label}): {together}")

    lines: List[str] = []
    lines.append("# Morph lookalike clustering (one-shot)")
    lines.append("")
    lines.append(f"Generated read-only from `{YAML_PATH.relative_to(REPO)}`, `docs/keys/**`,")
    conflict_note = (
        f"`{CONFLICT_PATH.relative_to(REPO)}`"
        if CONFLICT_PATH.is_file()
        else f"`{CONFLICT_PATH.relative_to(REPO)}` (missing; empty mask)"
    )
    lines.append(f"{conflict_note}, and `{REVIEW_PATH.relative_to(REPO)}`.")
    lines.append(f"Also writes `{NEIGHBOURS_PATH.relative_to(REPO)}` for PalynoQuest name-MCQ distractors.")
    lines.append("")
    lines.append("## 1. Method summary")
    lines.append("")
    lines.append("- **Goal:** taxa hard to tell apart under LM by morph similarity (not key topology).")
    lines.append("- **Matching:** exact `pollen_key` only; no synonym merge; no `*_typ` representative fill.")
    lines.append("- **Features:** YAML morph + dichotomous key endpoint/path attributes.")
    lines.append("- **Size priority:** species-matched Beug/Eide/Reitsma/van der Ham outcome for mid; PK path-gates kept separately and hard-separate when non-overlapping.")
    lines.append("- **Conflict mask:** YAML/Kerkvliet-analytic size masked when cross-key size conflicts exist; dichotomous key sizes still used.")
    lines.append("- **Clustering:** pure-Python complete-linkage cut; " + linkage_note + ".")
    lines.append("- **Non-goals:** no promotion; write only this report + morph-neighbours JSON.")
    lines.append("")
    lines.append("## 2. Feature inventory")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("| :--- | ---: |")
    lines.append(f"| Taxa in `pollen.yaml` | {len(data)} |")
    lines.append(f"| Taxa with ≥1 usable morph feature | {len(feats)} |")
    lines.append(f"| Clusterable | {len(clusterable)} |")
    lines.append(f"| Sparse / appendix | {len(sparse)} |")
    lines.append(f"| With images (YAML) | {len(imaged)} |")
    lines.append(f"| Neighbours JSON keys | {len(neighbours_payload['neighbours'])} |")
    lines.append(f"| Conflict-masked (YAML size and/or sculpt) | {len(masks)} |")
    lines.append(f"| Key-enriched taxa | {sum(1 for f in feats.values() if f.key_hits)} |")
    lines.append(f"| With dichotomous key size | {sum(1 for f in feats.values() if f.size_source.startswith(('beug','eide','reitsma','vanderham','path-gate','feagri')))} |")
    lines.append(f"| With PK path-gate | {sum(1 for f in feats.values() if f.path_gate is not None)} |")
    lines.append(f"| Learning-priority in clusterable | {sum(1 for s in clusterable if feats[s].rank)} |")
    lines.append(f"| Already-decided pairs | {len(decided)} |")
    lines.append("")
    ap_counts: Dict[str, int] = defaultdict(int)
    for s in clusterable:
        ap_counts[feats[s].aperture_bucket or "(none)"] += 1
    lines.append("### Aperture families (clusterable)")
    lines.append("")
    for ap, cnt in sorted(ap_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- `{ap}`: {cnt}")
    lines.append("")
    lines.append("### Conflict-masked taxa")
    lines.append("")
    for slug in sorted(masks):
        lines.append(f"- `{slug}`: masked [{', '.join(sorted(masks[slug]))}] (YAML/analytic only; key sizes kept when present)")
    lines.append("")
    lines.append("## 3. Clustering parameters")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("| :--- | :--- |")
    lines.append(f"| Linkage | {linkage_note} |")
    lines.append(f"| W_APERTURE | {W_APERTURE} |")
    lines.append(f"| W_SIZE_NONOVERLAP (preferred or path-gate) | {W_SIZE_NONOVERLAP} |")
    lines.append(f"| W_SIZE_CLASS / ADJ | {W_SIZE_CLASS} / {W_SIZE_CLASS_ADJ} |")
    lines.append(f"| W_SIZE_MID (per 5 µm) | {W_SIZE_MID} |")
    lines.append(f"| W_SCULPT / W_COARSE_SCULPT | {W_SCULPT} / {W_COARSE_SCULPT} |")
    lines.append(f"| W_BEUG / W_SHAPE / W_ORN | {W_BEUG} / {W_SHAPE} / {W_ORN} |")
    lines.append(f"| Missing aperture / size | {W_MISSING_APERTURE} / {W_MISSING_SIZE} |")
    lines.append(f"| **Tight cut** | ≤ **{tight_t:.3f}** |")
    lines.append(f"| **Loose cut** | ≤ **{loose_t:.3f}** |")
    lines.append("")
    lines.append("### Calibration notes")
    lines.append("")
    for nline in cal_notes:
        lines.append(f"- {nline}")
    lines.append("")
    lines.append("### Sample decided-pair distances")
    lines.append("")
    lines.append("| Pair | Status | Distance |")
    lines.append("| :--- | :--- | ---: |")
    shown = 0
    for (a, b), st in sorted(decided.items(), key=lambda x: x[0]):
        key = (a, b) if a < b else (b, a)
        if key not in dist_map:
            continue
        if shown >= 25:
            break
        lines.append(f"| `{a}`–`{b}` | {st} | {dist_map[key]:.3f} |")
        shown += 1
    lines.append("")

    def emit_clusters(title: str, clusters: List[Set[str]], cut_name: str) -> None:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"Clusters with ≥2 members at {cut_name} cut. Learning-priority first.")
        lines.append("")
        ranked_c = [c for c in clusters if cluster_summary_bits(c, feats)["has_rank"]]
        other_c = [c for c in clusters if not cluster_summary_bits(c, feats)["has_rank"]]
        lines.append(f"- With ≥1 learning_priority_rank: **{len(ranked_c)}**")
        lines.append(f"- Unranked-only: **{len(other_c)}**")
        lines.append(f"- Total: **{len(clusters)}**")
        lines.append("")
        for i, c in enumerate(clusters, 1):
            summ = cluster_summary_bits(c, feats)
            flags = species_typ_flag(c)
            ad_tags: List[str] = []
            ml = sorted(c)
            for ii, a in enumerate(ml):
                for b in ml[ii + 1 :]:
                    key = (a, b) if a < b else (b, a)
                    if key in decided:
                        ad_tags.append(f"`{a}`–`{b}` ({decided[key]})")
            pdists = []
            for ii, a in enumerate(ml):
                for b in ml[ii + 1 :]:
                    key = (a, b) if a < b else (b, a)
                    if key in dist_map:
                        pdists.append(dist_map[key])
            mean_d = sum(pdists) / len(pdists) if pdists else float("nan")
            max_d = max(pdists) if pdists else float("nan")
            header = f"### C{i} (n={len(c)}, mean_d={mean_d:.3f}, max_d={max_d:.3f})"
            if summ["has_rank"]:
                header += f" — ranks {summ['ranks']}"
            lines.append(header)
            lines.append("")
            lines.append(f"- Shared aperture: {', '.join(summ['aperture_buckets']) or '—'}")
            lines.append(
                f"- Size classes: {', '.join(summ['size_classes']) or '—'}; mid range: {summ['mid_range']}"
            )
            lines.append(f"- Shared sculpture tokens: {', '.join(summ['shared_sculpture']) or '—'}")
            if len(summ["shared_sculpture"]) == 1 and summ["shared_sculpture"][0] in COARSE_SCULPT:
                lines.append(
                    "- **Low specificity:** shared sculpture is a single coarse token "
                    f"(`{summ['shared_sculpture'][0]}`); morph-bin group, not confirmed lookalike."
                )
            if flags:
                lines.append(f"- **Human review (species↔*_typ):** {'; '.join(flags)}")
            if ad_tags:
                lines.append(f"- **already_decided:** {'; '.join(ad_tags)}")
            lines.append("- Members:")
            for slug in sorted(c, key=lambda s: (feats[s].rank is None, feats[s].rank or 9999, s)):
                lines.append(f"  - {fmt_member(feats[slug])}")
            if pdists:
                best = None
                best_d = float("inf")
                for ii, a in enumerate(ml):
                    for b in ml[ii + 1 :]:
                        key = (a, b) if a < b else (b, a)
                        if key in dist_map and dist_map[key] < best_d:
                            best_d = dist_map[key]
                            best = key
                if best:
                    lines.append(
                        f"- Closest pair evidence `{best[0]}`–`{best[1]}` (d={best_d:.3f}): `{evid_map.get(best, {})}`"
                    )
            provs = [f"`{slug}`: " + "; ".join(feats[slug].provenance[:4]) for slug in ml[:4]]
            lines.append("- Provenance (sample): " + " · ".join(provs))
            lines.append("")

    emit_clusters("4. Tight clusters (near-identical)", tight_sets, f"tight≤{tight_t:.3f}")
    emit_clusters("5. Looser clusters (close)", loose_sets, f"loose≤{loose_t:.3f}")

    lines.append("## 6. already_decided tags (summary)")
    lines.append("")
    n_in_tight = sum(1 for (a, b) in decided if any(a in c and b in c for c in tight_sets))
    n_in_loose = sum(1 for (a, b) in decided if any(a in c and b in c for c in loose_sets))
    lines.append(f"- Decided pairs co-clustered at tight cut: {n_in_tight}")
    lines.append(f"- Decided pairs co-clustered at loose cut: {n_in_loose}")
    lines.append("- Per-cluster tags listed above; sources not modified.")
    lines.append("")
    lines.append("## 7. Human review flags")
    lines.append("")
    hr = []
    for c in loose_sets:
        fl = species_typ_flag(c)
        if fl:
            hr.append((sorted(c), fl))
    lines.append(f"- Clusters with species↔`*_typ` co-membership (loose cut): **{len(hr)}**")
    for members, fl in hr[:40]:
        lines.append(f"  - {', '.join('`'+m+'`' for m in members)}: {'; '.join(fl)}")
    if len(hr) > 40:
        lines.append(f"  - … and {len(hr) - 40} more")
    lines.append("")
    lines.append("- Borderline: YAML size-masked taxa rely on dichotomous key sizes when present.")
    lines.append("- Sparse taxa (appendix) were not forced into clusters.")
    lines.append("")
    lines.append("## 8. Limits / risks")
    lines.append("")
    lines.append("- Missing fields inflate distance; empty never treated as a match.")
    lines.append("- Kerkvliet section morph is analytic; not used as dichotomous size when conflict-masked.")
    lines.append("- Dichotomous key sizes (Beug species lines / path gates) drive separation when YAML conflicts.")
    lines.append("- No synonym / fuzzy Latin merge; no key-topology similarity signal.")
    lines.append("- Tokenization is heuristic; coarse `reticulaat`-only groups remain low-specificity.")
    lines.append(f"- Linkage: {linkage_note}.")
    lines.append("- This report does not confirm or promote lookalikes.")
    lines.append("")
    lines.append("## Appendix A. Sparse / singleton taxa")
    lines.append("")
    lines.append("Taxa with fewer than 2 usable feature dimensions (not forced into clusters).")
    lines.append("")
    for slug in sorted(sparse):
        lines.append(f"- {fmt_member(feats[slug])} · features={feats[slug].feature_count}")
    lines.append("")
    lines.append("## Appendix B. Clusterable singletons at tight cut")
    lines.append("")
    in_tight = set().union(*tight_sets) if tight_sets else set()
    singles = [s for s in clusterable if s not in in_tight]
    ranked_singles = [s for s in singles if feats[s].rank]
    lines.append(f"Clusterable taxa not in any tight multi-member cluster: **{len(singles)}**.")
    lines.append(f"Of which learning-priority: **{len(ranked_singles)}**")
    for s in sorted(ranked_singles, key=lambda x: feats[x].rank or 9999)[:60]:
        lines.append(f"- {fmt_member(feats[s])}")
    lines.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elapsed = time.perf_counter() - t0
    print(f"Wrote {OUT_PATH}")
    print(f"SUMMARY tight={len(tight_sets)} loose={len(loose_sets)}")
    print(f"RUNTIME {elapsed:.1f}s")
    print("TOP TIGHT (ranked):")
    for i, c in enumerate(tight_sets[:12], 1):
        summ = cluster_summary_bits(c, feats)
        print(f"  {i}. n={len(c)} ranks={summ['ranks']} members={sorted(c)[:8]}")


if __name__ == "__main__":
    main()
