---
name: beug-key
description: >-
  Emits Beug-style vdh-pollentabel JSON from user-supplied OCR, scan text, or image/transcript in chat. Use when the user attaches or @-mentions a source file and wants key JSON without copying species or measurements from other repo keys.
---

# Beug JSON from user attachment

## Source (hard rule)

- **All key content** (taxa, sizes, MiW, couplets, morphology, table/figure refs): **only** from what the user **attached, @-referenced, or pasted in the same request** you are answering. Do **not** take values from `docs/keys/`, `notes/`, or the open editor unless that path is explicitly the user’s supplied source for this task.
- Illegible or missing OCR: **[te verifiëren]** or leave out; **do not guess**.

## Shape

- Valid object for `vdh-pollentabel.js`: see **interactive-pollen-key** (this repo) — top-level `start`, `steps` with `choices`, each choice: `label` + **`next`** *or* **`outcome.text`** only. Italics: `*Genus species*`, not HTML.

## Standard `meta` (Beug keys)

| Field | Value |
| --- | --- |
| `key` | Paired Markdown slug: **filename of the `.md` page without extension** (e.g. `beug04-tetradeae-drosera`). |
| `title` | **Heading taken from the scan** (Dutch where you translate; use `*taxon*` for genus/species). |
| `locale` | `nl` |
| `source` | Exactly `"Beug"` — no extra prose. |
| `note` | `"-"` |
| `start`, `stepCount` | As required by the key structure. |

## Dutch & numbers

- `label` / `outcome.text`: **Nederlands**. Measurements: **decimal comma** (`61,0–81,3 µm`). Keep Beug abbreviations (e.g. MiW, T, PK) consistent with the attachment.

## Mapping (minimal)

1. Order of the source → ordered steps `"1"`, `"2"`, …
2. **label** = diagnostic arm (the “question” side), compact.
3. Terminal arm → **outcome.text** = subsection label if present + species lines with data **as on the attachment**.

## Token discipline

- **Do not** read other `docs/keys/**/*.json` for **content**. If the contract is unclear, open **interactive-pollen-key** `SKILL.md` once for the schema line only.
- **Do not** paste long JSON examples into chat unless the user asks.

## Repo hygiene

- No writes to `notes/`. `mkdocs.yml` / nav only if the user asks. After adding or changing keys/pages, run **`mkdocs build`** when the workflow already involves site checks.
