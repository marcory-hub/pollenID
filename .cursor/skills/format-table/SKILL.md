---
name: format-table
description: Ensure tables use strict, compact formatting with unpadded cells and exact separator lines.
---

When asked to format-table:
- **First decide scope**: confirm whether the user wants *one table* or *one table per section* (e.g. per `##` heading) before reformatting.
- **Single source of truth**: use the dataset the user points at; do not mix multiple versions of “the same” table unless the user explicitly asks for a merge rule.
- **Remove duplication**: if identical/near-identical table blocks appear multiple times, keep only one according to the user’s policy (default: keep-first).
- **Emit tight pipe tables** (GFM/CommonMark):
  - Use exactly one header row and one separator row.
  - Separator row uses exactly `---` per column: `|---|---|---|` (no alignment colons, no extended dashes).
  - No padded cells for visual alignment (no extra spaces to “line up” columns).
  - Use leading/trailing pipes consistently on every row.
- **Do not invent data**: only reflow/normalize; keep cell content unchanged unless the user requests a normalization (units, spelling, etc.).
- **Output discipline**: output only the table(s) requested, nothing else.

Example (target style):

| A | B |
|---|---|
| 1 | 2 |