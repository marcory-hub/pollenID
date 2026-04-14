---
name: pollen-pagina
description: >-
  Create/update a Dutch taxon page under docs/nederlandse-honing-pollen/ following calluna_vulgaris.md.
---

# Pollen taxon page (Nederlandse honing)

## When to use

- Create or revise a taxon page in `docs/nederlandse-honing-pollen/` in the exact structure of `calluna_vulgaris.md`.

## Hard constraints

- **Language**: Dutch in `docs/` (headings, prose, link labels). Chat stays English.
- **notes/**: read-only.
- **docs/keys/**: read-only unless the user explicitly asks for keys changes.
- **URLs**: do not invent; reuse verified URLs already in repo or provided by the user.
- **Typography**: never use `—`; use `-`. In HTML, escape `<` as `&lt;`.

## Callouts (required)

Do not use Markdown `!!!` admonitions. Use HTML callouts (Material style) so `<ol>` / `<ul>` render correctly:

```html
<div class="admonition info">
<p class="admonition-title">Verwacht pad</p>
<ol>
<li><strong>Stap 1:</strong> ...</li>
</ol>
</div>
```

Patterns used in `calluna_vulgaris.md`:
- **Path**: title `Verwacht pad` + `<ol>` with steps and an `Eindpunt`.
- **Kerkvliet row summary**: title `Diversen <em>…</em>` + `<ul>` with fixed fields.
- **Beug path**: title `Beug` (or `Beug: <groep>`) + `<ol>`.

## Output template (match calluna_vulgaris.md)

Create/update `docs/nederlandse-honing-pollen/<slug>.md` with these sections and order:

1. **H1**
   - `# *Genus species* (Nederlandse naam)`

2. **Image gallery (required)**
   - Use the same HTML scaffold as `calluna_vulgaris.md`:
     - `<div class="pid-scale-gallery">` + one `<div class="pid-scale-row pid-scale-row--snug">`
     - repeated `<figure class="pid-scale-item"><img ...></figure>`
   - Keep image `style="height: ...px; width: auto;"` values consistent with existing assets for that taxon (copy, do not recalculate).
   - `alt`: short, correct (no placeholders).

3. **`## Determinatiesleutels`**
   - Add subsections as applicable, each using HTML callouts:
     - `### Kerkvliet-determinatietabel voor pollen in Nederlandse honing`
       - One callout summarising the table row (fields exactly as in `calluna_vulgaris.md`):
         `Nederlands`, `Vorm`, `Grootte (µm)`, `Oppervlak`, `Opmerkingen`
     - `### Pollentabel van der Ham`
       - One callout `Verwacht pad` with `<ol>` and an `Eindpunt` (family-level is fine; state it).
     - `### Beug: <hoofdstuk/groep>`
       - One callout tracing the main path.
       - If a sub-key/group is needed for species: add a second callout titled `Beug: <subgroep>` with its path and endpoint.
   - Source rule: trace paths by reading JSON; do not edit JSON.

4. **`## Online databases`**
   - Optional internal pointer(s) first (as in calluna):
     - `- Zie ook [<Monofloraal>](../monoflorale-honing-pollen/<page>.md).`
   - Then external bullets (only verified):
     - `- [PollenX - *Genus species*](...)`
     - `- [pollenwiki - *Genus species*](...)`
     - `- [Paldat - *Genus species*](...)`

5. **`## Naslag`** (optional)
   - Bullet list of references if you have verified URLs (e.g. existing PDF links already used elsewhere in repo).

## Navigation (`mkdocs.yml`)

- If the page is new and the user asked for nav updates: add under `Nederlands` in alphabetical order.
- Do not change nav unless the user explicitly asks (broken-links/SEO risk when renaming/moving pages).

## Verification

- If you changed `mkdocs.yml` or did broad link edits: run `mkdocs build`.

## Canonical example

`docs/nederlandse-honing-pollen/calluna_vulgaris.md`
