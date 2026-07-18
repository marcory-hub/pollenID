#!/usr/bin/env python3
"""Obsolete: former NL index orphan-link fixer.

docs/nederlandse-honing-pollen/_index.md was removed in the families+species
restructure. Use docs/pollen/species/ and render_taxon_pages_from_sot.py instead.
"""
from __future__ import annotations

import sys


def main() -> int:
    print(
        "fix_nl_index_orphan_links.py is obsolete: the NL Beug-class index was removed. "
        "Use docs/pollen/species/ and scripts/render_taxon_pages_from_sot.py.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
