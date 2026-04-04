#!/usr/bin/env python3
"""One-off helper: resolve Pollen-Wiki pkd from search + raw wikitext."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://pollen.tstebler.ch/MediaWiki/"
UA = "pollenID-docs-bot/1.0 (https://github.com/; pkd prefix helper)"

# | pkd ={{PK22}}, 22.6 Taxon …  OR  | pkd={{PK09}}, 9.35 …
PKD_DECIMAL = re.compile(
    r"\|\s*pkd\s*=\{\{PK\d+\}\}\s*,\s*([\d.]+(?:\.[\d]+)*)", re.IGNORECASE
)
# | pkd ={{PK33}} end (no decimal segment)
PKD_PK_ONLY = re.compile(r"\|\s*pkd\s*=\{\{PK(\d+)\}\}\s*\|", re.IGNORECASE)

# line_number -> override search term (1-based lines in _index.md)
SEARCH_OVERRIDES: dict[int, str] = {
    618: "Sinapis",
    624: "Raphanus",
}


def api_search(term: str) -> list[str]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "srlimit": "8",
            "format": "json",
        }
    )
    url = f"{BASE}api.php?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8-sig"))
    hits = data.get("query", {}).get("search", [])
    return [h["title"] for h in hits]


def fetch_raw(title: str) -> str:
    params = urllib.parse.urlencode({"title": title, "action": "raw"})
    url = f"{BASE}index.php?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_pkd(wikitext: str) -> str | None:
    m = PKD_DECIMAL.search(wikitext)
    if m:
        return m.group(1).rstrip(".")
    m = PKD_PK_ONLY.search(wikitext)
    if m:
        return m.group(1)
    return None


def first_token_after_hashes(line: str) -> str:
    rest = line.split("#####", 1)[1].strip()
    return rest.split()[0]


def search_term_from_line(line: str, line_no: int) -> str:
    if line_no in SEARCH_OVERRIDES:
        return SEARCH_OVERRIDES[line_no]
    tok = first_token_after_hashes(line)
    if tok.endswith("-Typ"):
        return tok[: -len("-Typ")]
    return tok


def pick_title(term: str, titles: list[str]) -> str | None:
    if not titles:
        return None
    t0 = term[0].upper() + term[1:] if term else term
    # exact title match
    for t in titles:
        if t == term or t == t0:
            return t
    # title starts with term (genus pages)
    for t in titles:
        if t.startswith(t0) or t.startswith(term):
            return t
    # substring
    for t in titles:
        if term.lower() in t.lower():
            return t
    return titles[0]


def resolve_pkd(line: str, line_no: int) -> tuple[str, str, str | None, str | None]:
    term = search_term_from_line(line, line_no)
    titles = api_search(term)
    title = pick_title(term, titles)
    if not title:
        return term, "", None, "no_search_hits"
    try:
        raw = fetch_raw(title)
    except Exception as e:
        return term, title, None, f"fetch_error:{e}"
    pkd = extract_pkd(raw)
    if pkd is None:
        return term, title, None, "no_pkd_in_wikitext"
    return term, title, pkd, None


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/nederlandse-honing-pollen/_index.md"
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # 1-based line numbers 616-687 inclusive
    results: list[dict] = []
    prefix_re = re.compile(r"^[\d.]+\s+(#####\s)")
    for i in range(615, 687):  # 0-based index: 615 = line 616
        raw = lines[i]
        line = raw
        m = prefix_re.match(raw)
        if m:
            line = m.group(1) + raw.split("#####", 1)[1]
        if not line.startswith("#####"):
            continue
        term, title, pkd, err = resolve_pkd(line, i + 1)
        results.append(
            {
                "line": i + 1,
                "term": term,
                "title": title,
                "pkd": pkd,
                "error": err,
                "original": raw.rstrip("\n"),
            }
        )
        time.sleep(0.35)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
