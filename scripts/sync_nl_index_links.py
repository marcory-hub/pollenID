from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_MD = REPO_ROOT / "docs" / "nederlandse-honing-pollen" / "_index.md"


GALLERY_RE = re.compile(r'\{\{\s*pollen_gallery\(\s*"([^"]+)"\s*\)\s*\}\}')
HEADING_RE = re.compile(r"^####\s+\[(?P<label>[^\]]+)\]\((?P<href>[^)]+)\)(?P<tail>.*)$")


def _standard_summary(key: str) -> List[str]:
    # Only the requested fields; all values come from SoT via macros.
    return [
        f'- Latijn: {{{{ pollen("{key}", "latin") }}}}',
        f'- Nederlands: {{{{ pollen("{key}", "dutch") }}}}',
        f'- Grootte: {{{{ pollen("{key}", "size.smallest_size") }}}}-{{{{ pollen("{key}", "size.largest_size") }}}}',
        f'- Vorm: {{{{ pollen("{key}", "shape") }}}}',
        f'- Sculptuur: {{{{ pollen("{key}", "sculpture") }}}}',
        f'- Apertuur: {{{{ pollen("{key}", "aperture") }}}}',
        f'- Ornamentatie: {{{{ pollen("{key}", "ornamentation") }}}}',
    ]


def main() -> int:
    lines = INDEX_MD.read_text(encoding="utf-8").splitlines()

    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = HEADING_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        # Identify gallery key in the next few lines
        key: Optional[str] = None
        for j in range(i + 1, min(i + 8, len(lines))):
            gm = GALLERY_RE.search(lines[j])
            if gm:
                key = gm.group(1).strip()
                break

        if not key:
            out.append(line)
            i += 1
            continue

        # Rewrite the heading link to local page using underscore naming.
        label = m.group("label")
        tail = m.group("tail")
        out.append(f"#### [{label}]({key}.md){tail}")

        # Copy lines until (and including) the pollen_gallery line, then replace the free bullets.
        i += 1
        # Keep any immediate gallery line(s) as-is
        while i < len(lines):
            out.append(lines[i])
            if GALLERY_RE.search(lines[i]):
                i += 1
                break
            i += 1

        # Skip existing bullet block immediately following the gallery, replace with canonical summary.
        while i < len(lines) and lines[i].startswith("- "):
            i += 1

        out.extend(_standard_summary(key))
        out.append("")  # blank line separator

        # Skip any extra blank lines that belonged to the old block
        while i < len(lines) and lines[i].strip() == "":
            i += 1

    INDEX_MD.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

