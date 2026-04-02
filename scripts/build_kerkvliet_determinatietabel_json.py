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


def main() -> None:
    text = INP.read_text(encoding="utf-8")
    sections, rows = parse_rows(text)

    doc = {
        "meta": {
            "key": "kerkvliet_determinatietabel",
            "title": "Determinatietabel (Kerkvliet) — interactieve tabel",
            "locale": "nl",
            "source": "Afgeleid uit docs/keys/kerkvliet/kerkvliet-determinatietabel.transcript.md (transcript).",
            "rowCount": len(rows),
            "sectionCount": len(sections),
        },
        "sections": sections,
        "rows": [
            {
                "section": r.section,
                "latin": r.latin,
                "dutch": r.dutch,
                "vorm": r.vorm,
                "grootte": r.grootte,
                "oppervlak": r.oppervlak,
                "opmerkingen": r.opmerkingen,
            }
            for r in rows
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(rows)} rows, {len(sections)} sections)")


if __name__ == "__main__":
    main()

