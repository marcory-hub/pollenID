---
name: pollen-pagina
description: >-
  Create/update a Dutch taxon page under docs/nederlandse-honing-pollen/ following calluna_vulgaris.md.
---

# Pollen taxon page (Nederlandse honing)

## When to use

- Create or revise a taxon page in `docs/nederlandse-honing-pollen/` (or another pollen page the user points to) using the current macro-first standard:
  - `pollen(key, field)` for facts
  - `pollen_img(key, src, alt="")` for images with YAML-driven height
  - one top-of-page gallery with all available images
  - no figcaptions
  - no grayscale reference strip

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
   - Populate each figure with a macro call (no `<figcaption>`):
     - `{{ pollen_img("<taxon_id>", "<relative_src_under_docs>", alt="<Latin name>") }}`
   - Image source rule:
     - include **all available images** for the taxon at the top of the page.
     - search under `docs/assets/images/` for filenames containing the Latin binomial (underscore or hyphen variants) and include each match once.
     - prefer a stable order by folder then filename (for example: `pollenwiki/`, `paldat/`, `persano_oddo/`, `beug/`, `kerkvliet/`).
   - Path rule (important):
     - pass page-relative paths (usually `../../assets/images/...`) to `pollen_img(...)`, matching how images already work in this repo.
   - `alt`: short and correct (no placeholders).

3. **`## Kenmerken` (required)**
   - Add a compact table that pulls all relevant YAML fields using `pollen(...)`:

```markdown
## Kenmerken

| Kenmerk | Waarde |
| --- | --- |
| **Latijn** | {{ pollen("<taxon_id>", "latin") }} |
| **Nederlands** | {{ pollen("<taxon_id>", "dutch") }} |
| **Familie** | {{ pollen("<taxon_id>", "family") }} |
| **Grootte (klein-groot)** | {{ pollen("<taxon_id>", "size.smallest_size") }} - {{ pollen("<taxon_id>", "size.largest_size") }} |
| **Vorm** | {{ pollen("<taxon_id>", "shape") }} |
| **Polariteit** | {{ pollen("<taxon_id>", "polarity") }} |
| **P/E-ratio** | {{ pollen("<taxon_id>", "pe_ratio") }} |
| **Apertuur** | {{ pollen("<taxon_id>", "aperture") }} |
| **Ornamentatie** | {{ pollen("<taxon_id>", "ornamentation") }} |
| **Bloeitijd (maand)** | {{ pollen("<taxon_id>", "bloeitijd.start") }} - {{ pollen("<taxon_id>", "bloeitijd.end") }} |
| **Nectarwaarde** | {{ pollen("<taxon_id>", "nectar_value") }} |
| **Pollenwaarde** | {{ pollen("<taxon_id>", "pollen_value") }} |
| **Frequentie in honing** | {{ pollen("<taxon_id>", "frequency_in_honey") }} |
```

4. **`## Determinatiesleutels` (required)**
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
   - Replacement rule: if the page already contains a free-text `## Sleutels` section, replace it with this structured `## Determinatiesleutels` section.

5. **`## Online databases`**
   - Optional internal pointer(s) first (as in calluna):
     - `- Zie ook [<Monofloraal>](../monoflorale-honing-pollen/<page>.md).`
   - Then external bullets (only verified):
     - `- [PollenX - *Genus species*](...)`
     - `- [pollenwiki - *Genus species*](...)`
     - `- [Paldat - *Genus species*](...)`

6. **`## Naslag`** (optional)
   - Bullet list of references if you have verified URLs (e.g. existing PDF links already used elsewhere in repo).

## Navigation (`mkdocs.yml`)

- If the page is new and the user asked for nav updates: add under `Nederlands` in alphabetical order.
- Do not change nav unless the user explicitly asks (broken-links/SEO risk when renaming/moving pages).

## Verification

- If you changed `mkdocs.yml` or did broad link edits: run `mkdocs build`.

## Canonical example

`docs/nederlandse-honing-pollen/calluna_vulgaris.md`
