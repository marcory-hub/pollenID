from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

from render_taxon_pages_from_sot import render_taxon_page


REPO_ROOT = Path(__file__).resolve().parents[1]
NL_DIR = REPO_ROOT / "docs" / "nederlandse-honing-pollen"
INDEX_MD = NL_DIR / "_index.md"
POLLEN_YAML = REPO_ROOT / "data" / "pollen.yaml"


HEADING_RE = re.compile(r"^####\s+\[(?P<label>[^\]]+)\]\((?P<href>[^)]+)\)(?P<tail>.*)$")
GALLERY_RE = re.compile(r'\{\{\s*pollen_gallery\(\s*"([^"]+)"\s*\)\s*\}\}')


def _slugify(label: str) -> str:
    s = label.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "taxon"


def main() -> int:
    pollen: Dict[str, Any] = yaml.safe_load(POLLEN_YAML.read_text(encoding="utf-8")) or {}
    lines = INDEX_MD.read_text(encoding="utf-8").splitlines()

    out = []
    i = 0
    changed = 0
    created = 0

    while i < len(lines):
        line = lines[i]
        m = HEADING_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        label = m.group("label")
        href = m.group("href").strip()
        tail = m.group("tail")

        if not href.endswith(".md"):
            out.append(line)
            i += 1
            continue

        # Determine if this heading actually owns a gallery before the next heading/section.
        j = i + 1
        has_gallery = False
        while j < len(lines) and not lines[j].startswith("#### ") and not lines[j].startswith("### "):
            if GALLERY_RE.search(lines[j]):
                has_gallery = True
                break
            j += 1

        if has_gallery:
            out.append(line)
            i += 1
            continue

        # Orphan local link: point to its own derived slug page.
        key = _slugify(label)
        out.append(f"#### [{label}]({key}.md){tail}")
        changed += 1

        # Create stub page if missing.
        md_path = NL_DIR / f"{key}.md"
        if not md_path.exists():
            entry = pollen.get(key)
            if isinstance(entry, dict):
                md_path.write_text(render_taxon_page(key, entry), encoding="utf-8")
            else:
                md_path.write_text(f'# *{label}*\\n\\n[to be verified]\\n', encoding="utf-8")
            created += 1

        i += 1

    INDEX_MD.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"fixed_orphan_links={changed} created_pages={created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
