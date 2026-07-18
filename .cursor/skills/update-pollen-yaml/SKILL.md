---
name: update-pollen-yaml
description: Update and extend data/pollen.yaml as the single source of truth (sizes, fields, images list). Use when the user asks to add/update taxa fields, add images, deduplicate entries, or align keys/pages to pollen.yaml.
---

# Update `data/pollen.yaml`

## Goal
- Keep `data/pollen.yaml` as the SoT, with minimal diffs and no invented taxa/paths.

## Canonical entry shape
```yaml
slug:
  name:
    latin_name:
    dutch_name:
  classification:
    order:
    family:
    tribe:
    genus:
  size:
    size_smallest:
    size_largest:
    height_px:
  pollen_class_beug:
  pollen_features:
    shape:
    sculpture:
    sculpture_visibility:   # optional: lm_clear | lm_poor | em_only
    aperture:
    aperture_visibility:
    ornamentation:
    ornamentation_visibility:
    polarity:
    pe_ratio:
    pollen-note:
  flowering_time:
    start:
    end:
  value:
    nectar_value:
    pollen_value:
  note:
    note_plant:
    note_honey:
    note_pollen:
  frequency_in_dutch_honey:
  frequency_in_eu_honey:
  frequency_in_non_eu_honey:
  links: { pollenX, tstebler, paldat, waarneming }
  images: [...]
```
Normalize structure with `./.venv/bin/python scripts/normalize_pollen_yaml_schema.py`.
MkDocs macros still accept legacy paths (`latin`, `size.smallest_size`, …) via aliases in `scripts/pollen_display.py`.

## Workflow (token-efficient)
- Read only what you need: use targeted search, then small `Read` windows around the relevant key.
- When adding images, use files under `docs/assets/images/` and write docs-relative paths like `assets/images/...`.
- Canonical layout for taxon-linked pollen bitmaps: `assets/images/by-taxon/<pollen_key>/...` (use `kind` / `source` fields to record provenance, not only the folder name).
- Prefer mechanical changes:
  - Insert `images:` immediately before `image:` in an entry.
  - Sort `images` paths and de-duplicate.
  - Do not modify other fields unless explicitly requested.

## Keep entries alphabetical
- Treat each top-level key (column 0, ending with `:`) as a taxon block.
- When requested, reorder the file by sorting these blocks alphabetically by key, while keeping each block's internal content unchanged.

## Mapping images to keys
- Map an image to a pollen key using the filename stem:
  - Normalize: `-` to `_`, lowercase, collapse `_`.
  - Strip view suffixes: `_ed/_eo/_pd/_po/_em/_om/_o/_d/_e/_p` with optional trailing digits.
  - Strip trailing numeric variants and `_sizeNNum`.
- If a mapped key does not exist in `data/pollen.yaml`, do not create a new entry unless the user explicitly asks.

## `images` schema
Use:

```yaml
  images:
  - path: assets/images/by-taxon/foo_bar/foo_bar_1.png
    kind: pollenwiki
    source: pollenwiki
```

Use **numeric** filenames (`foo_bar_1.png`, …). `kind` and `source` record the image corpus (e.g. `pollenwiki`, `paldat`, `beug`, `kerkvliet`).

Optional YAML `links:` block overrides auto-generated atlas URLs in `pollen.json` (`pollenx`, `tstebler`, `paldat`, `waarneming`); use explicit `null` when a default URL would be wrong.

## Regenerate the runtime index and manifests

`docs/javascripts/pollentabel.js` reads `docs/data/pollen.json` for endpoints that use `id.pollen_key`. After any change to `data/pollen.yaml`, regenerate site data (not tracked in git):

```bash
./.venv/bin/python scripts/build_docs_data.py
```

Rules:
- Do not edit `docs/data/pollen.json` or `docs/assets/manifests/*.json` by hand; they are generated.
- The exporter emits `latin`, `dutch`, `family`, `shape`, `ornamentation`, `aperture`, `size`, `display_width_px`, `links`, and `images` (with per-image `width_px` when derivable; see `scripts/export_pollen_json.py`).

Optional LM/EM visibility (parallel to morphology strings; omit or leave null when unknown):

```yaml
  sculpture: striaat
  sculpture_visibility: lm_clear   # lm_clear | lm_poor | em_only
  aperture: tricolpaat
  aperture_visibility:
  ornamentation:
  ornamentation_visibility:
```

Codes: `lm_clear` (goed zichtbaar met LM), `lm_poor` (matig zichtbaar met LM), `em_only` (alleen zichtbaar met EM). Exported to `pollen.json` only when set.

## Validation

```bash
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
```

## Auditing and migration helpers
- Read-only inventory: `python scripts/audit_pollen_assets.py`
- Append confidently mapped files missing from YAML: `python scripts/sync_yaml_confident_images.py`
- **By-taxon bitmap files** exist under `assets/images/by-taxon/<pollen_key>/` but stay **invisible** in the Kerkvliet table (and anywhere else that reads `pollen.json` `images[]`) until each path appears under **`images:`** in `data/pollen.yaml`. Append those without scanning pollenwiki:  
  `python scripts/sync_yaml_confident_images.py --only-by-taxon`  
  (optional: combine with the usual scan using `--include-by-taxon`.)
- Move resolved bitmaps into `by-taxon` (rewrites references): `python scripts/migrate_pollen_images_by_taxon.py --apply`

## By-taxon folder to YAML key coverage
- When requested, inventory `docs/assets/images/by-taxon/*` subfolders and ensure each folder slug exists as a top-level key in `data/pollen.yaml`.
- For missing slugs, add a minimal stub entry plus an `images:` list containing every `*.png` in that folder (paths under `assets/images/by-taxon/<slug>/...`), using `kind: by_taxon` and `source: by_taxon`.
