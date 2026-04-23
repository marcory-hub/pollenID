#!/usr/bin/env python3
"""
Fix broken GitHub Pages asset paths in docs pages.

Problem: pages under e.g. docs/nederlandse-honing-pollen/ used
  src="../../assets/..."
which resolves outside the /pollenID/ repo subpath on GitHub Pages, yielding
  GET /assets/... 404

For Markdown files inside these directories, the correct relative path to the
docs root assets is:
  src="../assets/..."
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"

TARGET_DIRS = [
    DOCS / "nederlandse-honing-pollen",
    DOCS / "monoflorale-honing-pollen",
]

FROM = 'src="../../assets/'
TO = 'src="../assets/'


def main() -> int:
    changed_files = 0
    changed_refs = 0
    for d in TARGET_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            if FROM not in text:
                continue
            new_text = text.replace(FROM, TO)
            if new_text != text:
                p.write_text(new_text, encoding="utf-8", newline="\n")
                changed_files += 1
                changed_refs += text.count(FROM)
    print(f"changed_files={changed_files} changed_refs={changed_refs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

