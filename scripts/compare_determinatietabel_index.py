#!/usr/bin/env python3
"""
Loose-compare Latin names in pollenanalyse determinatietabel (notes .txt)
against docs/nederlandse-honing-pollen/_index.md.

Does not modify source files. Example:

  python3 scripts/compare_determinatietabel_index.py \\
    --out notes/pollenID/determinatietabel-vs-index.md

(Obsidian: create that path yourself if the agent cannot write notes.)
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# --- notes parsing -----------------------------------------------------------

SECTION_PATTERNS = [
    (re.compile(r"^Pollen met een \(min of meer\) glad", re.I), "glad"),
    (re.compile(r"^Pollen met een netwerk", re.I), "reticulaat"),
    (re.compile(r"^Pollen met groeven", re.I), "striaat"),
    (re.compile(r"^Pollen met stekels", re.I), "echinaat"),
    (re.compile(r"^Diversen\s*:", re.I), "diversen"),
    (re.compile(r"^Enkele \(sub\)tropische", re.I), "subtropical"),
]

STOP_MARKERS = re.compile(
    r"^(Bronvermelding|Oppervlakstructuren|Pollen typen in de Asteraceae|Versie\s+\d|Drs\.\s|Tel\s)",
    re.I,
)


def split_columns(line: str) -> list[str]:
    s = line.rstrip("\n")
    if "\t" in s:
        parts = [p.strip() for p in re.split(r"\t+", s.strip())]
    else:
        parts = [p.strip() for p in re.split(r"\s{2,}", s.strip())]
    return [p for p in parts if p != ""]


def is_notes_header_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("Determinatietabel:"):
        return True
    if s.startswith("Plant") and "vorm" in s and "grootte" in s:
        return True
    if s.startswith("(Latijn)") or s.startswith("(Nederlands)"):
        return True
    if re.match(r"^Reticulaat\s", s) and "verrucaat" in s:
        return True
    if s.startswith("Netwerk") and "wratten" in s:
        return True
    if re.match(r"^\s*●", line):
        return True
    if re.match(r"^(Striaat|Rugulaat|rugulaat)\s", s):
        return True
    if STOP_MARKERS.match(s):
        return True
    if s.startswith("Kenmerken ") or s.startswith("Gebruikte termen"):
        return True
    if s.startswith("Afkortingen:") or s.startswith("  l=lang"):
        return True
    if s.startswith("Pollen die op elkaar lijken"):
        return True
    return False


def section_for_line(line: str, current: str) -> str:
    for pat, slug in SECTION_PATTERNS:
        if pat.match(line.strip()):
            return slug
    return current


LATIN_START = re.compile(r"^[A-Z][a-z]+")


def looks_like_latin_cell(s: str) -> bool:
    s = s.strip()
    if not s:
        return False
    if LATIN_START.match(s):
        return True
    return False


def merge_hyphen_break(prev: str, nxt: str) -> tuple[str, str]:
    """Join prev (line that ended with hyphen break) to first alphabetic token on next line."""
    if not prev:
        return prev, nxt
    t = prev.rstrip()
    stem = t[:-1].rstrip() if t.endswith("-") else t.rstrip()
    nxt_st = nxt.strip()
    if not nxt_st:
        return prev, nxt
    first = re.match(r"^([A-Za-z]+)", nxt_st)
    if not first:
        return prev, nxt
    frag = first.group(1)
    rest = nxt_st[len(frag) :].lstrip()
    return stem + frag, rest


# Whole-word replacements on normalized lowercase string
TYPO_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bcoryllus\b"), "corylus"),
    (re.compile(r"\bavelana\b"), "avellana"),
    (re.compile(r"\bonosis\b"), "ononis"),
    (re.compile(r"\bulginosis\b"), "uliginosus"),
    (re.compile(r"\bbuddleiea\b"), "buddleja"),
    (re.compile(r"\banthirrhinum\b"), "antirrhinum"),
    (re.compile(r"\bgramineae\b"), "poaceae"),
]

# Trailing / token abbreviations (substring replace on tokens)
TOKEN_ABBREV: dict[str, str] = {
    "tuber.": "tuberosum",
    "tuberc.": "tuberosum",
    "lycopers": "lycopersicum",
    "hippocas": "hippocastanum",
    "hippocast.": "hippocastanum",
    "pseudoac": "pseudoacacia",
    "pseudo-": "pseudoacacia",  # merged oddly; cleaned below
    "off.": "officinalis",
    "off": "officinalis",
    "sativ": "sativa",
    "praten": "pratensis",
    "macr.": "macrophylla",
    "vulg": "vulgaris",
    "ornus": "ornus",
    "raph": "raphanistrum",
    "sylv": "sylvestris",
    "convol": "convolvulus",
    "ebulus": "ebulus",
    "sco": "scoparius",
    "graveole": "graveolens",
    "vulga": "vulgare",
    "sphon.": "sphondylium",
    "angust": "angustifolia",
    "californ": "californica",
    "polyph": "perforatum",  # Hypericum polyph -> likely perforatum cluster; weak
    "perfo-": "perforatum",
    "menzi": "menziesii",
    "platanoïdes": "platanoides",
    "pseudoplat.": "pseudoplatanus",
    "hybr": "hybrida",
    "italicum": "italicum",
    "perpus": "perpusillus",
    "coccin": "coccinea",
    "sylvatica": "sylvaticum",  # Galium
    "tenuïfolia": "tenuifolia",
    "dougl": "douglasii",
    "baldschur": "baldschuanica",
    "lancelota": "lanceolata",
    "angu": "angustifolium",
    "tetrag": "tetragona",
    "oleacera": "oleracea",
    "nigrum": "nigrum",
    "tinctor": "tinctoria",
    "maritima": "maritima",
    "sanguineum": "sanguineum",
    "chamo": "chamomilla",
    "jacobea": "jacobaea",
    "inaequalis": "inaequalis",
    "virga au": "virgaurea",
    "cann": "cannabinum",
    "autu": "autumnale",
    "autum": "autumnale",
    "satives": "sativus",
    "involcrata": "involucrata",
    "angisti": "angustifolia",
    "sinicus": "sinicus",
    "arbores": "arborescens",
    "marianum": "marianum",
    "sylibum": "silybum",  # typo Silybum
    "sphaer": "sphaerocephalus",
}

# Genera where trailing "off" means officinalis (not a false positive)
_OFFICINALIS_GENERA = frozenset(
    {
        "symphytum",
        "verbascum",
        "melilotus",
        "plantago",
        "mentha",
        "origanum",
        "satureja",
        "teucrium",
        "verbena",
        "mercurialis",
        "pulmonaria",
        "petasites",
        "galium",
        "asperula",
        "scrophularia",
        "sanguisorba",
        "scabiosa",
        "echium",
        "digitalis",
        "fumaria",
        "anchusa",
        "reseda",
        "lysimachia",
        "saxifraga",
    }
)


def normalize_latin(raw: str) -> str:
    s = raw.strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\([^)]*\)", "", s)  # Spirea (van Houti?)
    s = s.replace("?", "").strip()
    # Split tokens and expand abbreviations
    tokens = s.split()
    out: list[str] = []
    for i, tok in enumerate(tokens):
        base = tok
        blo = base.lower().rstrip(".,;-")
        if blo in TOKEN_ABBREV:
            base = TOKEN_ABBREV[blo]
        elif blo == "off" and out and out[0].lower() in _OFFICINALIS_GENERA:
            base = "officinalis"
        elif blo.endswith(".") and blo[:-1] in TOKEN_ABBREV:
            base = TOKEN_ABBREV[blo[:-1]]
        out.append(base)
    s2 = " ".join(out)
    low = s2.lower()
    low = (
        low.replace("vitis ideae", "vitis-idaea")
        .replace("vitisidaea", "vitis-idaea")
        .replace("vitis idea", "vitis-idaea")
    )
    for pat, repl in TYPO_FIXES:
        low = pat.sub(repl, low)
    return low.strip() if low else s2.lower().strip()


def normalized_lower_for_match(s: str) -> str:
    return normalize_latin(s)


_NOT_EPITHET = frozenset(
    {"sp", "sp.", "cv", "x", "semperflorens", "cultivar", "agg.", "aff."}
)


def genus_epithet(norm_lower: str) -> tuple[str, str | None]:
    parts = norm_lower.split()
    if not parts:
        return "", None
    g = parts[0]
    if len(parts) >= 2 and parts[1] not in _NOT_EPITHET:
        if parts[1].endswith("."):
            return g, parts[1].rstrip(".")
        return g, parts[1]
    return g, None


# synonym cluster: each key expands to extra strings to try (all lowercase)
SYNONYM_EXPANSIONS: dict[str, list[str]] = {
    "chamerion angustifolium": ["epilobium angustifolium"],
    "chamerion": ["epilobium"],
    "rhamnus frangula": ["frangula alnus", "frangula"],
    "frangula alnus": ["rhamnus frangula", "rhamnus"],
    "polygonum persicaria": ["persicaria maculosa", "persicaria"],
    "polygonum convolvulus": ["polygonum aviculare", "fallopia"],
    "gramineae": ["poaceae"],
    "robina pseudoacacia": ["robinia pseudoacacia"],
    "euodia hupehensis": ["tetradium", "evodia"],
    "colchicinum autumnale": ["colchicum autumnale"],
    "scrophularia nodo": ["scrophularia nodosa"],
    "serrulata tinctoria": ["serratula tinctoria"],
    "arcticum minus": ["arctium minus"],
    "arcticum majus": ["arctium"],
    "sylibum marianum": ["silybum marianum"],
    "cynoglossum": ["cynoglossum officinale"],
    "myosotis": ["myosotis scorpioides"],
    "plantago": ["plantago lanceolata"],
    "rumex": ["rumex obtusifolius"],
    "salix": ["salix sp"],
    "anthriscus sylv": ["anthriscus sylvestris"],
    "heracleum sphon": ["heracleum sphondylium"],
}


def expansions_for(norm_lower: str) -> list[str]:
    out: list[str] = [norm_lower]
    g, e = genus_epithet(norm_lower)
    if e:
        key = f"{g} {e}"
        out.extend(SYNONYM_EXPANSIONS.get(key, []))
    out.extend(SYNONYM_EXPANSIONS.get(g, []))
    seen: set[str] = set()
    uniq: list[str] = []
    for x in out:
        if x and x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


@dataclass
class TableRow:
    section: str
    latin_raw: str
    latin_norm: str
    genus: str
    epithet: str | None


def parse_notes_table(text: str) -> list[TableRow]:
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == "Determinatietabel:")
    except StopIteration:
        start = 0

    section = "preamble"
    rows: list[TableRow] = []
    pending_hyphen: str | None = None

    i = start + 1
    while i < len(lines):
        raw = lines[i]
        if STOP_MARKERS.match(raw.strip()):
            break

        ns = section_for_line(raw, section)
        if ns != section:
            section = ns
            pending_hyphen = None
            i += 1
            continue

        if is_notes_header_line(raw):
            pending_hyphen = None
            i += 1
            continue

        line = raw.rstrip("\n")
        if pending_hyphen:
            merged, remainder = merge_hyphen_break(pending_hyphen, line)
            sep = "\t" if "\t" in line else "  "
            line = f"{merged}{sep}{remainder}" if remainder.strip() else merged
            pending_hyphen = None

        stripped = line.lstrip()
        # Continuation: indented, first token lowercase Latin fragment -> append to previous row
        if line != stripped and rows and re.match(r"^[a-z][a-z]+\b", stripped):
            first = re.match(r"^([a-z][a-z]+)", stripped)
            if first:
                frag = first.group(1)
                if len(frag) <= 22 and frag not in {"onder", "einde", "soms", "ca", "zie"}:
                    rows[-1].latin_raw = (rows[-1].latin_raw + " " + frag).strip()
                    nn = normalized_lower_for_match(rows[-1].latin_raw)
                    g, e = genus_epithet(nn)
                    rows[-1].latin_norm = nn
                    rows[-1].genus = g
                    rows[-1].epithet = e
            i += 1
            continue

        # Hyphen continuation for next iteration (keep trailing hyphen on stored line)
        if re.search(r"[a-zA-Z]-\s*$", line.rstrip()) and not line.rstrip().endswith("--"):
            pending_hyphen = line.rstrip()
            i += 1
            continue

        parts = split_columns(line)
        if not parts:
            i += 1
            continue

        latin = parts[0]
        if not looks_like_latin_cell(latin):
            i += 1
            continue

        norm = normalized_lower_for_match(latin)
        g, e = genus_epithet(norm)
        rows.append(TableRow(section=section, latin_raw=latin, latin_norm=norm, genus=g, epithet=e))
        i += 1

    return rows


# --- index extraction --------------------------------------------------------

PKD_PREFIX = re.compile(r"^[\d.]+\s+(?=#####\s+)")
HEAD_LINE = re.compile(
    r"^#{2,5}\s*(?:[\d.]+\s+)?(.+)$",
)


def extract_index_tokens(md: str) -> tuple[set[str], set[str]]:
    """Return (single_words, bigrams) lowercase."""
    words: set[str] = set()
    bigrams: set[str] = set()

    def feed_fragment(frag: str) -> None:
        frag = frag.strip()
        frag = re.split(r"\s*[—–]\s*Kerkvliet:", frag, maxsplit=1)[0]
        frag = re.split(r"\s+—\s+", frag, maxsplit=1)[0]
        frag = re.sub(r"\([^)]*\)", " ", frag)
        frag = PKD_PREFIX.sub("", frag)
        frag = frag.replace("#####", " ").replace("####", " ")
        toks = re.findall(r"[A-Za-z][a-z]+(?:\.[a-z]+)?", frag)
        for t in toks:
            words.add(t.lower())
        for a, b in zip(toks, toks[1:]):
            bigrams.add(f"{a.lower()} {b.lower()}")

    for line in md.splitlines():
        m = HEAD_LINE.match(line)
        if m:
            feed_fragment(m.group(1))
        else:
            # Inline headings like "#### Vaccinium" without hash at line start in broken md
            m2 = re.match(r"^#{2,5}\s+", line)
            if m2:
                feed_fragment(line[m2.end() :])

    # Whole-file boundary scan for binomials in prose (lightweight)
    blob = re.sub(r"```.*?```", " ", md, flags=re.S)
    for m in re.finditer(r"\b([A-Z][a-z]+)\s+([a-z][a-z.-]+)\b", blob):
        words.add(m.group(1).lower())
        words.add(m.group(2).lower())
        bigrams.add(f"{m.group(1).lower()} {m.group(2).lower()}")

    return words, bigrams


def word_in_index(w: str, words: set[str]) -> bool:
    return w.lower() in words


def bigram_in_index(g: str, e: str | None, bigrams: set[str]) -> bool:
    if not e:
        return False
    return f"{g} {e}" in bigrams


def match_tier(
    row: TableRow, words: set[str], bigrams: set[str]
) -> tuple[int, str]:
    """
    Return (tier, detail) where tier 1=binomial, 2=synonym hit, 3=genus only, 4=missing.
    """
    g, e = row.genus, row.epithet
    expansions = expansions_for(row.latin_norm)

    # Tier 1: binomial present in extracted heading bigrams
    for ex in expansions:
        gg, ee = genus_epithet(ex)
        if ee and bigram_in_index(gg, ee, bigrams):
            return 1, f"binomial `{gg} {ee}`"

    if e and bigram_in_index(g, e, bigrams):
        return 1, f"binomial `{g} {e}`"

    # Tier 2: synonym expansion genus or phrase
    for ex in expansions[1:]:
        gg, ee = genus_epithet(ex)
        if ee and (bigram_in_index(gg, ee, bigrams) or (word_in_index(gg, words) and word_in_index(ee, words))):
            return 2, f"synonym→`{ex}`"
        if word_in_index(gg, words):
            return 2, f"synonym genus `{gg}`"

    # Tier 3: genus only
    for ex in expansions:
        gg, _ = genus_epithet(ex)
        if word_in_index(gg, words):
            return 3, f"genus `{gg}` (only)"

    if word_in_index(g, words):
        return 3, f"genus `{g}` (only)"

    return 4, "—"


def markdown_report(
    rows: list[TableRow],
    notes_path: Path,
    index_path: Path,
    words: set[str],
    bigrams: set[str],
) -> str:
    lines: list[str] = []
    lines.append("# Determinatietabel vs `_index.md` (loose compare)")
    lines.append("")
    lines.append(f"- Notes: `{notes_path}`")
    lines.append(f"- Index: `{index_path}`")
    lines.append(f"- Parsed rows: **{len(rows)}**")
    lines.append("")

    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    details: list[tuple[int, TableRow, str]] = []
    for r in rows:
        tier, det = match_tier(r, words, bigrams)
        counts[tier] += 1
        details.append((tier, r, det))

    lines.append("## Summary")
    lines.append("")
    lines.append("| Tier | Meaning | Count |")
    lines.append("|---|---|---:|")
    lines.append(f"| 1 | Binomial (or both tokens) | {counts[1]} |")
    lines.append(f"| 2 | Synonym / alias hit | {counts[2]} |")
    lines.append(f"| 3 | Genus only | {counts[3]} |")
    lines.append(f"| 4 | Missing | {counts[4]} |")
    lines.append("")

    lines.append("## All rows")
    lines.append("")
    lines.append("| Section | Latin (raw) | Normalized | Tier | Detail |")
    lines.append("|---|---|---:|---|---|")
    for tier, r, det in sorted(details, key=lambda x: (x[0], x[1].section, x[1].latin_raw)):
        nm = r.latin_norm.replace("|", "\\|")
        raw = r.latin_raw.replace("|", "\\|")
        lines.append(f"| {r.section} | {raw} | {nm} | {tier} | {det} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--notes",
        type=Path,
        default=REPO / "notes/pollenID/pollenanalyse determinatietabel mrt2014.txt",
    )
    ap.add_argument(
        "--index",
        type=Path,
        default=REPO / "docs/nederlandse-honing-pollen/_index.md",
    )
    ap.add_argument("--out", type=Path, default=None, help="Write Markdown here (default: stdout)")
    args = ap.parse_args()

    text = args.notes.read_text(encoding="utf-8", errors="replace")
    md = args.index.read_text(encoding="utf-8", errors="replace")

    rows = parse_notes_table(text)
    words, bigrams = extract_index_tokens(md)
    report = markdown_report(rows, args.notes.resolve(), args.index.resolve(), words, bigrams)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"Wrote {args.out} ({len(rows)} rows)")
    else:
        print(report)


if __name__ == "__main__":
    main()
