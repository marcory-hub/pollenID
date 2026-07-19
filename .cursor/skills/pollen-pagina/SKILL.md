---
name: pollen-pagina
description: >-
  Create/update a Dutch taxon page under docs/pollen/species/ following calluna_vulgaris.md.
---

# Pollen taxon page

## When to use

- Create or revise a taxon page in `docs/pollen/species/` (or another pollen page the user points to) using the current macro-first standard:
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

Create/update `docs/pollen/species/<slug>.md` with these sections and order:

1. **H1**
   - `# *Genus species* (Nederlandse naam)`

2. **Image gallery (required)**
   - Use the same HTML scaffold as `calluna_vulgaris.md`:
     - `<div class="pid-scale-gallery">` + one `<div class="pid-scale-row pid-scale-row--snug">`
     - repeated `<figure class="pid-scale-item"><img ...></figure>`
   - Populate each figure with a macro call (no `<figcaption>`):
     - `{{ pollen_img("<taxon_id>", "<relative_src_under_docs>", alt="<Latin name>") }}`
   - Image source rule:
     - include **all available pollen images** for the taxon at the top of the page, in **`data/pollen.yaml`** order under `images:` (SoT).
     - on-disk canonical paths: `assets/images/by-taxon/<pollen_key>/<pollen_key>_N.png` (numeric suffix). Do **not** add new pollen bitmaps under legacy corpus folders (`pollenwiki`, `paldat`, etc.).
     - where a full **`{{ gallery("pollen_key") }}`** macro covers the taxon, prefer that over hand-built HTML for new pages.
   - Path rule (important):
     - pass page-relative paths (usually `../../assets/images/by-taxon/<slug>/...`) to `pollen_img(...)`, matching how images already work in this repo.
   - `alt`: short and correct (no placeholders).

3. **`## Kenmerken` (required)**
   - Add a compact table that pulls all relevant YAML fields using `pollen(...)`:

```markdown
## Kenmerken

| Kenmerk | Waarde |
| --- | --- |
| **Latijn** | {{ pollen("<taxon_id>", "name.latin_name") }} |
| **Nederlands** | {{ pollen("<taxon_id>", "name.dutch_name") }} |
| **Familie** | {{ pollen("<taxon_id>", "classification.family_latin") }} |
| **Familie (NL)** | {{ pollen("<taxon_id>", "classification.family_dutch") }} |
| **Grootte (klein-groot)** | {{ pollen("<taxon_id>", "size.size_smallest") }} - {{ pollen("<taxon_id>", "size.size_largest") }} |
| **Vorm** | {{ pollen("<taxon_id>", "pollen_features.shape") }} |
| **Polariteit** | {{ pollen("<taxon_id>", "pollen_features.polarity") }} |
| **P/E-ratio** | {{ pollen("<taxon_id>", "pollen_features.pe_ratio") }} |
| **Apertuur** | {{ pollen("<taxon_id>", "pollen_features.aperture") }} |
| **Ornamentatie** | {{ pollen("<taxon_id>", "pollen_features.ornamentation") }} |
| **Bloeitijd (maand)** | {{ pollen("<taxon_id>", "flowering_time.start") }} - {{ pollen("<taxon_id>", "flowering_time.end") }} |
| **Nectarwaarde** | {{ pollen("<taxon_id>", "value.nectar_value") }} |
| **Pollenwaarde** | {{ pollen("<taxon_id>", "value.pollen_value") }} |
| **Frequentie in NL-honing** | {{ pollen("<taxon_id>", "frequency_in_dutch_honey") }} |
| **Frequentie in EU-honing** | {{ pollen("<taxon_id>", "frequency_in_eu_honey") }} |
| **Frequentie in niet-EU-honing** | {{ pollen("<taxon_id>", "frequency_in_non_eu_honey") }} |
| **Bijdrage (primair/secundair)** | {{ pollen("<taxon_id>", "is_secondary_contributor") }} |
```

4. **`## Determinatiesleutels` (required)**
   - Follow **`.cursor/skills/trace-key-paths/SKILL.md`**: run `python scripts/extract_key_paths.py <pollen_key> --page-section` and merge into the page.
   - Add manual bullets only when JSON has no match (see that skill for fallbacks).
   - Legacy free-text `## Sleutels` → replace with structured `## Determinatiesleutels`.

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

- If the page is new and the user asked for nav updates: prefer linking from the matching family page under `docs/pollen/families/`; do not hand-list every species in nav.
- Do not change nav unless the user explicitly asks (broken-links/SEO risk when renaming/moving pages).

## Verification

- If you changed `mkdocs.yml` or did broad link edits: run `mkdocs build`.

## Canonical example

`docs/pollen/species/calluna_vulgaris.md`
