#!/usr/bin/env python3
"""
Genereert docs/naslag/raw-documenten-overzicht.md:
alle .md-bestanden onder de pollen-determineren-deelbomen, met onderscheid
tussen wél en niet in mkdocs.yml navigatie.

Gebruik (vanaf repository root):
  python3 scripts/generate-raw-docs-overview.py
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"
OUT = DOCS / "naslag" / "raw-documenten-overzicht.md"

SCAN_DIRS: list[tuple[str, Path]] = [
    (
        "kernset-herkenning",
        DOCS / "pollen-determineren" / "kernset-herkenning",
    ),
    (
        "verdiepingset-herkenning",
        DOCS / "pollen-determineren" / "verdiepingset-herkenning",
    ),
    (
        "pollen-vergelijkingen",
        DOCS / "pollen-determineren" / "pollen-vergelijkingen",
    ),
]


def iter_nav_md_paths(nav: object) -> list[str]:
    """Verzamel alle paden in nav die op .md eindigen (relatief t.o.v. docs/)."""
    out: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for v in node.values():
                if isinstance(v, str) and v.endswith(".md"):
                    out.append(v.replace("\\", "/"))
                else:
                    walk(v)

    walk(nav)
    return out


def rel_docs(path: Path) -> str:
    return path.relative_to(DOCS).as_posix()


def letter_group(stem: str) -> str:
    c = stem[0].upper() if stem else "#"
    return c if c.isalpha() else "#"


def main() -> None:
    with MKDOCS.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    nav_paths = set(iter_nav_md_paths(cfg.get("nav")))

    sections: list[str] = []
    summary_rows: list[tuple[str, int, int, int]] = []

    for label, folder in SCAN_DIRS:
        if not folder.is_dir():
            summary_rows.append((label, 0, 0, 0))
            continue
        paths = sorted(folder.rglob("*.md"), key=lambda p: p.as_posix().lower())
        rels = [rel_docs(p) for p in paths]
        in_nav = [r for r in rels if r in nav_paths]
        not_in_nav = [r for r in rels if r not in nav_paths]
        summary_rows.append((label, len(rels), len(not_in_nav), len(in_nav)))

        sections.append(f"\n## Map: `{label}`\n")
        sections.append(
            f"- Totaal: **{len(rels)}** -- niet in `nav`: **{len(not_in_nav)}** -- "
            f"wel in `nav`: **{len(in_nav)}**\n"
        )

        if in_nav:
            sections.append("\n### Wel in navigatie (`mkdocs.yml`)\n\n")
            for r in sorted(in_nav):
                sections.append(f"- [`{r}`](../{r})\n")

        sections.append("\n### Backlog (niet in navigatie)\n\n")
        if not not_in_nav:
            sections.append("_Geen; alles staat in de navigatie._\n")
            continue

        by_letter: dict[str, list[str]] = defaultdict(list)
        for r in not_in_nav:
            stem = Path(r).stem
            by_letter[letter_group(stem)].append(r)

        for letter in sorted(by_letter.keys(), key=lambda x: (x == "#", x)):
            items = sorted(by_letter[letter])
            sections.append(f"\n#### {letter}\n\n")
            for r in items:
                sections.append(f"- [`{r}`](../{r})\n")

    # ASCII labels in de tabel voorkomt encoding-problemen bij regeneratie op diverse omgevingen.
    table = "| Deelmap | Totaal | Niet in `nav` | Wel in `nav` |\n"
    table += "|---|---:|---:|---:|\n"
    for label, total, raw, navc in summary_rows:
        table += f"| `{label}` | {total} | {raw} | {navc} |\n"

    total_all = sum(r[1] for r in summary_rows)
    raw_all = sum(r[2] for r in summary_rows)

    header = f"""# RAW-documentenoverzicht

Deze pagina staat onder de **RAW**-tab in de hoofdnavigatie (naast Home, microscopie, enz.).

Dit overzicht is **automatisch gegenereerd**. Het toont alle Markdown-pagina's onder de drie
`pollen-determineren`-mappen, en welke daarvan **niet** in `mkdocs.yml` onder **nav** staan.
Dat zijn kandidaten voor verwerking (inhoud, didactiek, koppeling vanaf kernset/vergelijkingen/verdieping).

**Totaal backlog (niet in navigatie): {raw_all}** van **{total_all}** bestanden in deze mappen.

In `mkdocs.yml` staat `validation.nav.omitted_files: ignore`, zodat `mkdocs build` / `serve` dezelfde lijst niet opnieuw in de terminal dumpen. Dit bestand is de leidraad voor wat je nog wilt verwerken of koppelen.

## Tellingen

{table}

## Hoe vernieuwen?

```bash
python3 scripts/generate-raw-docs-overview.py
```

Laatste regeneratie: **{date.today().isoformat()}** (ISO-datum, lokaal).

---
"""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + "".join(sections), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
