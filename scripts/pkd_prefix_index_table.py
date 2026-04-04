#!/usr/bin/env python3
"""Prefix Latin column in tier-4 pipe table with Pollen-Wiki pkd (decimal or PKnn)."""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pollenwiki_fetch_pkd import api_search, extract_pkd, fetch_raw, pick_title  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "docs/nederlandse-honing-pollen/_index.md"

# Tier-4 incident table rows (five columns, last two: 4 | —)
TIER4_ROW = re.compile(r"^\| ([^|]*) \| ([^|]*) \| ([^|]*) \| 4 \| — \|$")

# Full Latin cell (no pkd prefix) -> Pollen-Wiki search term
LATIN_OVERRIDES: dict[str, str] = {
    "Ambrosia artemis": "Ambrosia",
    "Carlina aucalis": "Carlina",
    "Cnicus benedict": "Centaurea benedicta",
    "Cosmos sp.": "Cosmos",
    "Crepis sp.": "Crepis",
    "Lampsana commu": "Lapsana",
    "Leontodon  autum": "Leontodon",
    "Onopordon acant": "Onopordum",
    "Picris echinoïdes": "Picris",
    "Picris hiëracioïdes": "Picris",
    "Portulacca oleacera": "Portulaca",
    "Weigelia/Diervilla": "Weigelia",
    "Buddleiea": "Buddleja",
    "Escallonia sp": "Escallonia",
    "Eschscholtzia calif": "Eschscholzia",
    "Larix decidua": "Larix",
    "Morus alba": "Morus",
    "Nemophila menzi": "Nemophila",
    "Nemophila sp.": "Nemophila",
    "Sarothamnus sco of": "Cytisus scoparius",
    "Spirea (van Houti?)": "Spiraea",
    "Alyssum sp.": "Alyssum",
    "Anethum graveole": "Anethum",
    "Cakile maritima": "Cakile",
    "Euodia hupehensis": "Euodia",
    "Hippophaë rhamn": "Hippophae",
    "Lychnis-flos-cuculi": "Silene flos-cuculi",
    "Odontites vernus gelig": "Odontites",
    "Ornithopus perpus": "Ornithopus",
    "Pastinaca sativa": "Pastinaca",
    "Platanus hybr": "Platanus",
    "Pyracantha coccin": "Pyracantha",
    "Satureia hortensis": "Satureja",
    "Sophora japonica onregelmatig": "Styphnolobium japonicum",
    "Symphoricarpus sp": "Symphoricarpos",
    "Xanthium italicum": "Xanthium",
    "Mespilus germani": "Mespilus",
    "Prunus-laurocera": "Prunus laurocerasus",
    "Anacardium occid": "Anacardium",
    "Borreria sp. (Rubia)": "Borreria",
    "Carpobrotis edulis": "Carpobrotus",
    "Carragena arbores": "Caragana",
    "Hedysarum corona": "Hedysarum",
    "Loranthus europaeus": "Loranthus",
    "Tordylium apulum": "Tordylium",
    "Pachysandra ter(?)": "Pachysandra",
    "Santolina": "Santolina",
}

FIRST_TOKEN_MAP: dict[str, str] = {
    "arcticum": "Arctium",
    "serrulata": "Serratula",
    "sylibum": "Silybum",
    "onosis": "Ononis",
    "scropuhlaria": "Scrophularia",
    "lirodendron": "Liriodendron",
    "mercurialus": "Mercurialis",
    "escholzia": "Eschscholzia",
    "colchicinum": "Colchicum",
    "petasitis": "Petasites",
    "cnicus": "Cnicus",
    "lampsana": "Lapsana",
    "anthirrhinum": "Antirrhinum",
    "coriandrum": "Coriandrum",
    "galeopsis": "Galeopsis",
    "euonymus": "Euonymus",
    "symphoricarpus": "Symphoricarpus",
    "salix)+striaat": "Salix",
}

SKIP_SUBSTRINGS = (
    "Cyto:",
    "Granulair",
    "Afrika",
    "Oost Azië",
    "Sapindaceae (fam.)",
)

HAS_PKD_PREFIX = re.compile(r"^((?:\d+\.)+\d+|PK\d+)\s+\S")


def strip_existing_pkd(latin_col: str) -> tuple[bool, str]:
    """If cell already starts with pkd prefix, return (True, full cell unchanged)."""
    s = latin_col.strip()
    if HAS_PKD_PREFIX.match(s):
        return True, s
    return False, s


def latin_to_search_term(latin_col: str) -> str | None:
    s = latin_col.strip()
    if not s:
        return None
    if s in LATIN_OVERRIDES:
        return LATIN_OVERRIDES[s]
    if any(x in s for x in SKIP_SUBSTRINGS):
        return None
    if "/" in s and "Mercurialus" not in s:
        s = s.split("/")[0].strip()
    parts = s.replace("?", "").split()
    if not parts:
        return None
    raw_tok = parts[0].lower().rstrip(".,;:")
    if raw_tok in FIRST_TOKEN_MAP:
        return FIRST_TOKEN_MAP[raw_tok]
    w = parts[0]
    if w.endswith("-Typ"):
        w = w[: -len("-Typ")]
    if not w or not w[0].isalpha():
        return None
    return w


def resolve_term(term: str) -> str | None:
    titles = api_search(term)
    title = pick_title(term, titles)
    if not title:
        return None
    try:
        raw = fetch_raw(title)
    except Exception:
        return None
    pkd = extract_pkd(raw)
    if pkd is None:
        return None
    if re.fullmatch(r"\d{1,2}", pkd):
        return f"PK{int(pkd):02d}"
    return pkd


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    cache: dict[str, str | None] = {}
    for line in lines:
        stripped = line.rstrip("\n")
        m = TIER4_ROW.match(stripped)
        if not m:
            out.append(line)
            continue
        sec, latin, norm = (g.strip() for g in m.groups())
        already, base_latin = strip_existing_pkd(latin)
        if already:
            out.append(line)
            continue
        term = latin_to_search_term(base_latin)
        pkd: str | None = None
        if term:
            if term not in cache:
                cache[term] = resolve_term(term)
                time.sleep(0.35)
            pkd = cache[term]
        new_latin = f"{pkd} {base_latin}" if pkd else base_latin
        out.append(f"| {sec} | {new_latin} | {norm} | 4 | — |\n")

    INDEX.write_text("".join(out), encoding="utf-8")
    n = sum(1 for v in cache.values() if v)
    print(f"Updated {INDEX}: {len(cache)} unique terms, {n} resolved pkd")


if __name__ == "__main__":
    main()
