#!/usr/bin/env python3
"""Obsolete: former NL Beug-class index link sync.

The browse index at docs/nederlandse-honing-pollen/_index.md was removed in the
families+species restructure. Species pages live under docs/pollen/species/.

This script exits with a clear message so old invocations fail loudly.
"""
from __future__ import annotations

import sys


def main() -> int:
    print(
        "sync_nl_index_links.py is obsolete: docs/nederlandse-honing-pollen/_index.md "
        "was removed. Use docs/pollen/families/ and docs/pollen/species/ instead.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
