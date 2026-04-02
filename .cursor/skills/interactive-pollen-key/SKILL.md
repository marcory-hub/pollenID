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

`meta` (`key`, `title`, `locale`, `source`, `start`, `stepCount`), top-level `start`, `steps`. Each step has `choices`; each choice has `label` and **either** `next` **or** `outcome.text` (optional `outcome.incomplete`). Optional: `image`, `imageWidthPx`, step `note`. No other shape: the renderer requires this.

Italics: paired `*asterisks*` only (e.g. `*Ephedra*`), not full Markdown.

## Markdown page (Dutch mirrors the site)

```markdown
# <Nederlandse titel>

<div id="vdh-pollentabel-root" data-json-url="../../keys/<map>/<bestandsnaam>.json"></div>

### Tabel-overzicht

<div id="vdh-pollentabel-table-root" data-json-url="../../keys/<map>/<bestandsnaam>.json"></div>
```

`data-json-url` relative to the `.md` (often `../../keys/...` from `docs/Identificatiesleutels/`). No extra page JS; `mkdocs.yml` loads the script.

## Dutch in labels (examples)

*Pollenkorrels (PK)* / *PK* for German PK; prefer **colpi/colpus**, **poriën/porie**, **exine**, **tectum**, **aperturen** like existing `docs/`. Use **verdiepingen**, not *vertiepingen*. Gaps: **[te verifiëren]** per project rules.

## Boundaries

No writes to `notes/`. Change `mkdocs.yml` `nav` only if the user asks. After substantive doc changes: `mkdocs build`. Wire keys to `_index.md` only when the user specifies the branch.
