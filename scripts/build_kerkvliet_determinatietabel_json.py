#!/usr/bin/env python3
"""
Build docs/keys/kerkvliet/kerkvliet-determinatietabel.json from the Kerkvliet
Markdown transcription.

Goal: feed a small JS viewer (section dropdown + size class filter).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Keep the raw transcription separate from the interactive page.
INP = REPO / "docs" / "keys" / "kerkvliet" / "kerkvliet-determinatietabel.transcript.md"
OUT = REPO / "docs" / "keys" / "kerkvliet" / "kerkvliet-determinatietabel.json"


HEADER_RE = re.compile(r"^\s*##\s+(?P<title>.+?)\s*$")


def is_header_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    # Pipe table header/separator
    if s.startswith("Naam |") or s.startswith("--- |"):
        return True
    # Column headers (a few variants)
    if s.startswith("Plant") or s.startswith("(Latijn)"):
        return True
    if s.startswith("Reticulaat") or s.startswith("Netwerk"):
        return True
    if s.startswith("Striaat") or s.startswith("rugulaat") or s.startswith("Rugulaat"):
        return True
    return False


def split_columns(line: str) -> list[str]:
    s = line.rstrip("\n")
    if "|" in s and "\t" not in s:
        # Strict pipe table row: keep cells tight; drop leading/trailing empty.
        raw = [c.strip() for c in s.split("|")]
        if raw and raw[0] == "":
            raw = raw[1:]
        if raw and raw[-1] == "":
            raw = raw[:-1]
        # Keep empty cells to preserve column positions.
        return raw
    if "\t" in s:
        parts = [p.strip() for p in re.split(r"\t+", s.strip())]
    else:
        # Fallback: Kerkvliet uses many multi-space separators in places.
        parts = [p.strip() for p in re.split(r"\s{2,}", s.strip())]
    return [p for p in parts if p != ""]


@dataclass
class Row:
    section: str
    latin: str
    dutch: str
    vorm: str
    grootte: str
    oppervlak: str
    opmerkingen: str


def parse_rows(text: str) -> tuple[list[str], list[Row]]:
    section = ""
    rows: list[Row] = []
    sections: list[str] = []

    pending: str | None = None

    for raw in text.splitlines():
        m = HEADER_RE.match(raw)
        if m:
            section = m.group("title").strip()
            if section and section not in sections:
                sections.append(section)
            pending = None
            continue

        if is_header_line(raw):
            pending = None
            continue

        if not section:
            continue

        line = raw.rstrip()
        stripped = line.lstrip()
        is_continuation = (
            line != stripped  # indented continuation
            or (stripped[:1].islower())  # starts with lowercase word
            or stripped.startswith(("(", "[", "—", "-", "·", "•", ":", ";"))
            or stripped[:1].isdigit()
            or bool(re.match(r"^(A\d{3,}\b|[A-Z]\.)", stripped))
        )

        # Continuation lines should extend the previous row's opmerkingen.
        if is_continuation and rows:
            extra = stripped.strip()
            if extra:
                prev = rows[-1]
                prev.opmerkingen = (prev.opmerkingen + " " + extra).strip() if prev.opmerkingen else extra
            pending = None
            continue

        # Join wrapped lines (common in this transcription).
        if pending is not None:
            line = pending + " " + line.strip()
            pending = None

        parts = split_columns(line)

        # Heuristic: if we don't have enough columns, carry forward.
        if len(parts) < 4:
            pending = line
            continue

        # Pipe-table normalization: accept exactly 6 logical columns, even if empty.
        # If a row has only 5 columns, assume missing 'Nederlandse naam' and insert an empty cell.
        if "|" in line and "\t" not in line:
            # Skip header rows that might slip through.
            if parts and parts[0].lower() in {"naam", "---"}:
                continue
            if parts and re.match(r"^:?-+:?$", parts[0].replace(" ", "")):
                continue
            if len(parts) == 5:
                parts = [parts[0], "", parts[1], parts[2], parts[3], parts[4]]
            elif len(parts) > 6:
                # Merge any extras into the last cell (opmerkingen).
                parts = parts[:5] + [" ".join(p for p in parts[5:] if p).strip()]

        # Normal form: latin, dutch, vorm, grootte, oppervlak, opmerkingen
        latin = parts[0] if len(parts) > 0 else ""
        dutch = parts[1] if len(parts) > 1 else ""
        vorm = parts[2] if len(parts) > 2 else ""
        grootte = parts[3] if len(parts) > 3 else ""
        oppervlak = parts[4] if len(parts) > 4 else ""
        opmerkingen = " ".join(parts[5:]).strip() if len(parts) > 5 else ""

        # If we still look short (e.g. missing surface/notes), accept but keep stable.
        rows.append(
            Row(
                section=section,
                latin=latin,
                dutch=dutch,
                vorm=vorm,
                grootte=grootte,
                oppervlak=oppervlak,
                opmerkingen=opmerkingen,
            )
        )

    return sections, rows


def _load_old_pollen_keys_by_section() -> dict[str, list[str]]:
    """Preserve non-empty pollen_key values from existing JSON, ordered within section."""
    if not OUT.exists():
        return {}
    try:
        old = json.loads(OUT.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    by_sec: dict[str, list[str]] = {}
    for r in old.get("rows") or []:
        if not isinstance(r, dict):
            continue
        sec = r.get("section")
        pk = r.get("pollen_key")
        if not isinstance(sec, str) or not sec.strip():
            continue
        if not isinstance(pk, str) or not pk.strip():
            continue
        by_sec.setdefault(sec, []).append(pk.strip())
    return by_sec


def _slugify_latin(latin: str) -> str:
    """Rough latin -> slug (underscores); for matching old pollen_keys only."""
    s = latin.strip().lower()
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace("-", "_")
    s = re.sub(r"[^a-z0-9_\s]", " ", s)
    parts = [p for p in s.split() if p]
    if not parts:
        return ""
    return "_".join(parts)


def _pick_pollen_key(latin: str, pool: list[str]) -> str | None:
    """Pick and remove best matching key from section pool."""
    if not pool:
        return None
    slug = _slugify_latin(latin)
    if not slug:
        return None

    # Exact match
    if slug in pool:
        pool.remove(slug)
        return slug

    # Old truncated keys: pollen_key is a prefix of slug (robinia_pseudoac ⊂ robinia_pseudoacacia)
    # or slug is a prefix of pollen_key.
    candidates: list[str] = []
    for pk in pool:
        if slug.startswith(pk) or pk.startswith(slug):
            candidates.append(pk)
        else:
            # shared genus+start of epithet
            a, b = slug.split("_", 1) if "_" in slug else (slug, "")
            pa, pb = pk.split("_", 1) if "_" in pk else (pk, "")
            if a == pa and b and pb and (b.startswith(pb) or pb.startswith(b)):
                candidates.append(pk)

    if len(candidates) == 1:
        pk = candidates[0]
        pool.remove(pk)
        return pk
    if len(candidates) > 1:
        # Prefer longest shared prefix with slug
        candidates.sort(key=lambda k: (-sum(1 for x, y in zip(k, slug) if x == y), -len(k)))
        pk = candidates[0]
        pool.remove(pk)
        return pk

    return None


def _attach_pollen_keys(
    rows: list[Row], old_by_sec: dict[str, list[str]]
) -> tuple[list[dict], list[str]]:
    pools = {sec: list(keys) for sec, keys in old_by_sec.items()}
    out: list[dict] = []
    report: list[str] = []
    unmatched_latin: list[str] = []

    for r in rows:
        pool = pools.get(r.section, [])
        pk = _pick_pollen_key(r.latin, pool)
        row: dict = {
            "section": r.section,
            "latin": r.latin,
            "dutch": r.dutch,
            "vorm": r.vorm,
            "grootte": r.grootte,
            "oppervlak": r.oppervlak,
            "opmerkingen": r.opmerkingen,
        }
        if pk:
            row["pollen_key"] = pk
        else:
            unmatched_latin.append(f"{r.section[:40]}… | {r.latin}" if len(r.section) > 40 else f"{r.section} | {r.latin}")
        out.append(row)

    leftovers = {sec: keys for sec, keys in pools.items() if keys}
    if leftovers:
        for sec, keys in leftovers.items():
            report.append(f"leftover old pollen_keys in {sec!r}: {keys}")
    if unmatched_latin:
        report.append(f"rows without pollen_key after match: {len(unmatched_latin)}")
        for line in unmatched_latin[:25]:
            report.append(f"  no-key: {line}")
        if len(unmatched_latin) > 25:
            report.append(f"  … +{len(unmatched_latin) - 25} more")

    return out, report


def main() -> None:
    text = INP.read_text(encoding="utf-8")
    sections, rows = parse_rows(text)
    old_by_sec = _load_old_pollen_keys_by_section()
    row_dicts, report = _attach_pollen_keys(rows, old_by_sec)

    doc = {
        "meta": {
            "key": "kerkvliet_determinatietabel",
            "title": "Determinatietabel (Kerkvliet) — interactieve tabel",
            "locale": "nl",
            "source": "Afgeleid uit docs/keys/kerkvliet/kerkvliet-determinatietabel.transcript.md (transcript).",
            "rowCount": len(row_dicts),
            "sectionCount": len(sections),
        },
        "sections": sections,
        "rows": row_dicts,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with_pk = sum(1 for r in row_dicts if r.get("pollen_key"))
    print(f"Wrote {OUT} ({len(row_dicts)} rows, {len(sections)} sections, pollen_key={with_pk})")
    for line in report:
        print(f"NOTE: {line}")


if __name__ == "__main__":
    main()

