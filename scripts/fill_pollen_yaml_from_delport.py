#!/usr/bin/env python3
"""Fill empty Cape pollen_features from flora-regio-kaap key paths and type members.

Does not invent morphology. Size bins go into pollen-note only (never size.size_*).
Does not set pollen_class_beug. Empty fields only; existing Beug/YAML values kept.

Examples::

    ./.venv/bin/python scripts/fill_pollen_yaml_from_delport.py --dry-run
    ./.venv/bin/python scripts/fill_pollen_yaml_from_delport.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from ruamel.yaml import YAML

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
KEYS_DIR = REPO / "docs" / "keys" / "flora-regio-kaap"
TYPE_MEMBERS = KEYS_DIR / "type-members.json"
INDEX_PATH = KEYS_DIR / "taxa-index.json"

APERTURE_FROM_FILE = {
    "flora-regio-kaap-tricolporate.json": "tricolporaat",
    "flora-regio-kaap-tricolpate.json": "tricolpaat",
    "flora-regio-kaap-monosulcate.json": "monosulcaat",
    "flora-regio-kaap-pantoporate.json": "pantoporaat",
    "flora-regio-kaap-massula.json": "massula",
    "flora-regio-kaap-polyad.json": "polyade",
    "flora-regio-kaap-pseudomonad.json": "pseudomonade",
    "flora-regio-kaap-tetrad.json": "tetrade",
    "flora-regio-kaap-inaperturate.json": "inaperturaat",
    "flora-regio-kaap-diporate.json": "diporaat",
    "flora-regio-kaap-triporate.json": "triporaat",
    "flora-regio-kaap-monoporate.json": "monoporaat",
    "flora-regio-kaap-stephanocolpate.json": "stephanocolpaat",
    "flora-regio-kaap-stephanocolporate.json": "stephanocolporaat",
    "flora-regio-kaap-tetracolpate.json": "tetracolpaat",
    "flora-regio-kaap-tetracolporate.json": "tetracolporaat",
    "flora-regio-kaap-heteroaperturate.json": "heteroaperturaat",
    "flora-regio-kaap-trisulcate.json": "trisulcaat",
    "flora-regio-kaap-trisindemicolporate.json": "trisindemicolporaat",
}

SKIP_FILES = {"flora-regio-kaap-index.json", "taxa-index.json", "type-members.json"}


@dataclass
class DelportBundle:
    aperture: Optional[str] = None
    polarity: Optional[str] = None
    sculpture: Optional[str] = None
    shape: Optional[str] = None
    ornamentation: Optional[str] = None
    size_class: Optional[str] = None
    path_note: Optional[str] = None
    type_name: Optional[str] = None
    sources: Set[str] = field(default_factory=set)


def _empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
        return True
    return False


def _parse_path_labels(aperture: str, labels: List[str]) -> DelportBundle:
    b = DelportBundle(aperture=aperture)
    orn_bits: List[str] = []
    for lab in labels:
        low = lab.lower().strip()
        if low.startswith("isopolair"):
            b.polarity = "isopolair"
        elif low.startswith("heteropolair"):
            b.polarity = "heteropolair"
        m = re.match(r"primaire sculptuur\s+(.+)", lab, re.I)
        if m:
            b.sculpture = m.group(1).strip().lower()
        if re.search(r"\bprolaat\b", low):
            b.shape = "prolaat"
        elif re.search(r"\bafgeplat\b", low) or re.search(r"\boblaat\b", low):
            b.shape = "afgeplat"
        elif re.search(r"\bisodiametrisch\b", low):
            if _empty(b.shape):
                b.shape = "isodiametrisch"
        m2 = re.match(r"omtrek(?: in polair aanzicht)?[:\s]+(.+)", lab, re.I)
        if m2:
            outline = m2.group(1).strip().lower()
            b.shape = f"{b.shape}; {outline}" if b.shape else outline
        if re.search(r"klein\s*\(10", low):
            b.size_class = "klein (10–25 µm)"
        elif re.search(r"middelgroot\s*\(26", low):
            b.size_class = "middelgroot (26–50 µm)"
        elif re.search(r"groot\s*\(51", low):
            b.size_class = "groot (51–100 µm)"
        elif re.search(r"zeer groot", low):
            b.size_class = "zeer groot (>100 µm)"
        elif re.search(r"zeer klein|<\s*10", low):
            b.size_class = "zeer klein (<10 µm)"
        if re.search(r"stekels|lumina|secundaire|apocolp", low) and not low.startswith(
            "primaire"
        ):
            if not re.search(
                r"primaire sculptuur|isopolair|heteropolair|klein \(|middelgroot|"
                r"groot \(|vorm |omtrek|prolaat|afgeplat|isodiametrisch",
                low,
            ):
                orn_bits.append(lab.strip())
    if orn_bits:
        b.ornamentation = "; ".join(orn_bits[:3])
    if labels:
        # Compact path summary for pollen-note
        short = " → ".join(labels[:6])
        if len(labels) > 6:
            short += " → …"
        b.path_note = short
    return b


def _find_paths(
    key_json: Dict[str, Any], target: str
) -> List[Tuple[List[str], Optional[str]]]:
    """Return list of (labels, outcome_text) for terminals matching target."""
    steps = key_json.get("steps") or {}
    start = key_json.get("start")
    out: List[Tuple[List[str], Optional[str]]] = []

    def walk(sid: str, path: List[str]) -> None:
        step = steps.get(str(sid))
        if not isinstance(step, dict):
            return
        for ch in step.get("choices") or []:
            if not isinstance(ch, dict):
                continue
            label = (ch.get("label") or "").strip()
            new_path = path + [label] if label else path
            pk = ch.get("pollen_key")
            pks = ch.get("pollen_keys") or []
            if isinstance(pks, list) and not all(isinstance(x, str) for x in pks):
                pks = [x for x in pks if isinstance(x, str)]
            hit = pk == target or (isinstance(pks, list) and target in pks)
            if hit:
                ot = None
                outcome = ch.get("outcome")
                if isinstance(outcome, dict) and isinstance(outcome.get("text"), str):
                    ot = outcome["text"].strip()
                out.append((new_path, ot))
            nxt = ch.get("next")
            if nxt is not None:
                walk(str(nxt), new_path)

    if start is not None:
        walk(str(start), [])
    return out


def _merge_bundle(dst: DelportBundle, src: DelportBundle) -> None:
    for attr in (
        "aperture",
        "polarity",
        "sculpture",
        "shape",
        "ornamentation",
        "size_class",
        "path_note",
        "type_name",
    ):
        cur = getattr(dst, attr)
        new = getattr(src, attr)
        if _empty(cur) and not _empty(new):
            setattr(dst, attr, new)
    dst.sources |= src.sources


def collect_bundles() -> Dict[str, DelportBundle]:
    bundles: Dict[str, DelportBundle] = {}

    for jf in sorted(KEYS_DIR.glob("*.json")):
        if jf.name in SKIP_FILES or not jf.name.startswith("flora-regio-kaap-"):
            continue
        aperture = APERTURE_FROM_FILE.get(jf.name)
        if not aperture:
            continue
        key_json = json.loads(jf.read_text(encoding="utf-8"))
        # Collect all terminal pollen_keys in this file
        terminals: Set[str] = set()

        def collect_terminals(obj: Any) -> None:
            if isinstance(obj, dict):
                pk = obj.get("pollen_key")
                if isinstance(pk, str) and pk.strip():
                    terminals.add(pk.strip())
                pks = obj.get("pollen_keys")
                if isinstance(pks, list):
                    for x in pks:
                        if isinstance(x, str) and x.strip():
                            terminals.add(x.strip())
                for v in obj.values():
                    collect_terminals(v)
            elif isinstance(obj, list):
                for it in obj:
                    collect_terminals(it)

        collect_terminals(key_json)
        for pk in sorted(terminals):
            paths = _find_paths(key_json, pk)
            if not paths:
                continue
            # Prefer first path; if multiple, keep first and note conflict in path_note
            labels, _ot = paths[0]
            b = _parse_path_labels(aperture, labels)
            b.sources.add(jf.name)
            if len(paths) > 1:
                b.path_note = (b.path_note or "") + f" (+{len(paths) - 1} alternative pad(s))"
            if pk not in bundles:
                bundles[pk] = b
            else:
                _merge_bundle(bundles[pk], b)

    # Type members: inherit type path features
    if TYPE_MEMBERS.is_file():
        tm = json.loads(TYPE_MEMBERS.read_text(encoding="utf-8"))
        for t in tm.get("types") or []:
            if not isinstance(t, dict):
                continue
            type_pk = t.get("pollen_key")
            name = t.get("name")
            feats = t.get("features") or {}
            size_class = t.get("size_class")
            members = t.get("members") or []
            type_bundle = bundles.get(type_pk) if isinstance(type_pk, str) else None
            base = DelportBundle()
            if type_bundle:
                _merge_bundle(base, type_bundle)
            # features from type-members.json override empty only
            if isinstance(feats, dict):
                for field_name in ("aperture", "polarity", "sculpture", "shape", "ornamentation"):
                    val = feats.get(field_name)
                    if not _empty(val) and _empty(getattr(base, field_name)):
                        setattr(base, field_name, val)
            if size_class and _empty(base.size_class):
                base.size_class = size_class
            if isinstance(name, str):
                base.type_name = name
            base.sources.add("type-members.json")
            for mem in members:
                if not isinstance(mem, str) or not mem.strip():
                    continue
                mem = mem.strip()
                if mem not in bundles:
                    bundles[mem] = DelportBundle()
                _merge_bundle(bundles[mem], base)
                if isinstance(name, str) and _empty(bundles[mem].type_name):
                    bundles[mem].type_name = name

    return bundles


def _append_note(existing: Any, *tags: str) -> str:
    parts: List[str] = []
    if isinstance(existing, str) and existing.strip():
        parts.append(existing.strip())
    joined = "; ".join(parts) if parts else ""
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        if tag in joined:
            continue
        joined = f"{joined}; {tag}" if joined else tag
    return joined


def apply_bundles(
    data: Dict[str, Any],
    bundles: Dict[str, DelportBundle],
    cape_keys: Set[str],
    *,
    dry: bool,
) -> Dict[str, int]:
    stats = {
        "filled": 0,
        "skipped_already_set": 0,
        "unmatched_cape": 0,
        "fields_set": 0,
    }
    matched = set()
    for pk, bundle in bundles.items():
        if pk not in data or not isinstance(data[pk], dict):
            continue
        if pk not in cape_keys:
            continue
        matched.add(pk)
        entry = data[pk]
        pf = entry.get("pollen_features")
        if not isinstance(pf, dict):
            continue
        changed = False
        already = True
        for field_name, val in (
            ("aperture", bundle.aperture),
            ("polarity", bundle.polarity),
            ("sculpture", bundle.sculpture),
            ("shape", bundle.shape),
            ("ornamentation", bundle.ornamentation),
        ):
            if _empty(val):
                continue
            if _empty(pf.get(field_name)):
                if not dry:
                    pf[field_name] = val
                changed = True
                already = False
                stats["fields_set"] += 1
        note_tags: List[str] = []
        if bundle.type_name:
            note_tags.append(f"Delport type: {bundle.type_name}")
        if bundle.size_class:
            note_tags.append(f"Delport size class: {bundle.size_class}")
        if bundle.path_note and not bundle.type_name:
            # Path summary for unique terminals; type members already have type tag
            note_tags.append(f"Delport pad: {bundle.path_note}")
        if note_tags:
            new_note = _append_note(pf.get("pollen-note"), *note_tags)
            if new_note != (pf.get("pollen-note") or ""):
                if not dry:
                    pf["pollen-note"] = new_note
                changed = True
                already = False
        if changed:
            stats["filled"] += 1
        elif already and any(
            not _empty(getattr(bundle, a))
            for a in ("aperture", "polarity", "sculpture", "shape", "ornamentation")
        ):
            stats["skipped_already_set"] += 1

    for pk in cape_keys:
        if pk not in matched and pk in data:
            pf = data[pk].get("pollen_features") if isinstance(data[pk], dict) else None
            if isinstance(pf, dict) and all(
                _empty(pf.get(f))
                for f in ("aperture", "sculpture", "shape", "polarity", "ornamentation")
            ):
                stats["unmatched_cape"] += 1
    return stats


def cape_pollen_keys() -> Set[str]:
    keys: Set[str] = set()
    if INDEX_PATH.is_file():
        idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        for r in idx.get("taxa") or []:
            if isinstance(r, dict) and isinstance(r.get("pollen_key"), str):
                keys.add(r["pollen_key"])
    if TYPE_MEMBERS.is_file():
        tm = json.loads(TYPE_MEMBERS.read_text(encoding="utf-8"))
        for t in tm.get("types") or []:
            if isinstance(t, dict):
                if isinstance(t.get("pollen_key"), str):
                    keys.add(t["pollen_key"])
                for m in t.get("members") or []:
                    if isinstance(m, str):
                        keys.add(m)
    return keys


NOT_IN_DB = "not in the database"


def _http_ok(url: str, timeout: float = 8.0) -> bool:
    """True when URL looks present (2xx/3xx). Soft-fail on network errors."""
    import urllib.error
    import urllib.request

    headers = {"User-Agent": "pollenID-delport-link-check/1.0"}
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= getattr(resp, "status", 200) < 400
    except Exception:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = getattr(resp, "status", 200)
                return 200 <= code < 400
        except urllib.error.HTTPError as e:
            return 200 <= e.code < 400
        except Exception:
            return False


def probe_atlas_links(
    data: Dict[str, Any],
    cape_keys: Set[str],
    *,
    dry: bool,
    workers: int = 16,
) -> Dict[str, int]:
    """Mark missing tstebler/paldat URLs as 'not in the database' for Cape taxa."""
    import concurrent.futures

    stats = {"checked": 0, "ok": 0, "missing": 0, "patched": 0}
    jobs: List[Tuple[str, str, str]] = []  # pk, atlas_key, url

    for pk in sorted(cape_keys):
        entry = data.get(pk)
        if not isinstance(entry, dict):
            continue
        links = entry.get("links")
        if not isinstance(links, dict):
            continue
        for atlas_key in ("tstebler", "paldat"):
            url = links.get(atlas_key)
            if not isinstance(url, str) or not url.strip():
                continue
            if url.strip() == NOT_IN_DB:
                continue
            if not url.strip().startswith(("http://", "https://")):
                continue
            jobs.append((pk, atlas_key, url.strip()))

    def check_one(job: Tuple[str, str, str]) -> Tuple[str, str, str, bool]:
        pk, atlas_key, url = job
        return pk, atlas_key, url, _http_ok(url)

    results: List[Tuple[str, str, str, bool]] = []
    if jobs:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            for fut in concurrent.futures.as_completed(
                [ex.submit(check_one, j) for j in jobs]
            ):
                results.append(fut.result())

    for pk, atlas_key, url, ok in results:
        stats["checked"] += 1
        if ok:
            stats["ok"] += 1
            continue
        stats["missing"] += 1
        entry = data.get(pk)
        if not isinstance(entry, dict):
            continue
        links = entry.get("links")
        if not isinstance(links, dict):
            continue
        if links.get(atlas_key) == NOT_IN_DB:
            continue
        if not dry:
            links[atlas_key] = NOT_IN_DB
        stats["patched"] += 1
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Write data/pollen.yaml")
    ap.add_argument("--dry-run", action="store_true", help="Report only (default if no --apply)")
    ap.add_argument(
        "--probe-links",
        action="store_true",
        help="Also probe tstebler/paldat URLs for Cape taxa (404 → not in the database)",
    )
    ap.add_argument(
        "--skip-features",
        action="store_true",
        help="Skip pollen_features fill (probe-links only)",
    )
    args = ap.parse_args()
    dry = not args.apply

    if not KEYS_DIR.is_dir():
        print(f"missing {KEYS_DIR}", file=sys.stderr)
        return 1

    cape_keys = cape_pollen_keys()

    ry = YAML()
    ry.preserve_quotes = True
    ry.default_flow_style = False
    ry.width = 100
    ry.indent(mapping=2, sequence=4, offset=2)
    data = ry.load(YAML_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("invalid pollen.yaml", file=sys.stderr)
        return 1

    if not args.skip_features:
        bundles = collect_bundles()
        stats = apply_bundles(data, bundles, cape_keys, dry=dry)
        print(
            f"bundles={len(bundles)} cape_keys={len(cape_keys)} "
            f"filled={stats['filled']} skipped_already_set={stats['skipped_already_set']} "
            f"unmatched_cape={stats['unmatched_cape']} fields_set={stats['fields_set']}"
        )

    if args.probe_links:
        link_stats = probe_atlas_links(data, cape_keys, dry=dry)
        print(
            f"links checked={link_stats['checked']} ok={link_stats['ok']} "
            f"missing={link_stats['missing']} patched={link_stats['patched']}"
        )

    if dry:
        print("dry-run: no writes")
        return 0

    stream = StringIO()
    ry.dump(data, stream)
    YAML_PATH.write_text(stream.getvalue(), encoding="utf-8")
    print(f"wrote {YAML_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
