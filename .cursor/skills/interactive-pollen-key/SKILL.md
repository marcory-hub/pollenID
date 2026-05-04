---
name: interactive-pollen-key
description: >-
  Dichotomous pollen keys as JSON + MkDocs page using vdh-pollentabel.js. German source, Dutch in docs/ and JSON strings. Use for Beug/van der Ham style keys and branches from docs/Identificatiesleutels/_index.md.
---

# Interactive pollen / honey key (JSON + MkDocs)

## Policy

**Do not edit this skill** except when the user explicitly asks. **Do not list or mirror repo paths here**; new keys live only under `docs/` and `docs/keys/`.

## When to use

- Dichotomous keys like van der Ham / Beug; German in, **Dutch** in `docs/` and JSON `label` / `outcome.text`.
- Follow the branch the user names; **docs/Identificatiesleutels/_index.md** is the outline.

## Before you start

Read **one** existing JSON under `docs/keys/vanderham/` or `docs/keys/beug/` and its paired `.md` under `docs/Identificatiesleutels/`. Implementation details: `docs/javascripts/vdh-pollentabel.js`, italics via `docs/stylesheets/extra.css` (`.vdh-pollentabel-btn--choice em`).

## JSON contract

`meta` (`key`, `title`, `locale`, `source`, `start`, `stepCount`), top-level `start`, `steps`. Each step has `choices`; each choice has `label` and **either** `next` **or** `outcome.text` (optional `outcome.incomplete`). Optional: step `note`.

Images (overview + endpoint + placeholders):
- Prefer multi-image arrays:
  - `choice.images`: `[{ image, imageWidthPx }]` shown in the overzicht. In the interactive choice list, only placeholder images are shown.
  - `outcome.images`: `[{ image, imageWidthPx }]` shown at the endpoint and in the overzicht.
- Backward compatible single-image fields:
  - `choice.image` + `choice.imageWidthPx`
  - `outcome.image` + `outcome.imageWidthPx`

Placeholder policy (site authoring):
- Use `../../assets/images/non-pollen/placeholder.png` (repeated if needed) with `imageWidthPx: 1` when the user asks to add placeholder slots broadly.

Italics: paired `*asterisks*` only (e.g. `*Ephedra*`), not full Markdown.

## Markdown page (Dutch mirrors the site)

```markdown
# <Nederlandse titel>

<div id="vdh-pollentabel-root" data-json-url="../../keys/<map>/<bestandsnaam>.json"></div>

### Tabel-overzicht

<div id="vdh-pollentabel-table-root" data-json-url="../../keys/<map>/<bestandsnaam>.json"></div>
```

`data-json-url` relative to the `.md` (often `../../keys/...` from `docs/Identificatiesleutels/`). No extra page JS; `mkdocs.yml` loads the script.

**No boilerplate above the widgets** unless the user explicitly requests it: do not add lines such as "Onderdeel van…", "Uitkomst … volgt…", "Deelsleutel bij §…", "Zie […]", or "PK = …" between the `H1` and the first `div`. Stick to the snippet above. Pages without a key JSON may keep a single relative Markdown link directly under the `H1` (no extra prose).

## Dutch in labels (examples)

*Pollenkorrels (PK)* / *PK* for German PK; prefer **colpi/colpus**, **poriën/porie**, **exine**, **tectum**, **aperturen** like existing `docs/`. Use **verdiepingen**, not *vertiepingen*. Gaps: **[te verifiëren]** per project rules.

## Boundaries

No writes to `notes/`. Change `mkdocs.yml` `nav` only if the user asks. After substantive doc changes: `mkdocs build`. Wire keys to `_index.md` only when the user specifies the branch.
