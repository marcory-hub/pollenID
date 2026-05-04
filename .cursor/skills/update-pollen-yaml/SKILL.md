---
name: update-pollen-yaml
description: Update and extend data/pollen.yaml as the single source of truth (sizes, fields, images list). Use when the user asks to add/update taxa fields, add images, deduplicate entries, or align keys/pages to pollen.yaml.
---

# Update `data/pollen.yaml`

## Goal
- Keep `data/pollen.yaml` as the SoT, with minimal diffs and no invented taxa/paths.

## Workflow (token-efficient)
- Read only what you need: use targeted search, then small `Read` windows around the relevant key.
- When adding images, use files under `docs/assets/images/` and write docs-relative paths like `assets/images/...`.
- Canonical layout for taxon-linked pollen bitmaps: `assets/images/by-taxon/<pollen_key>/...` (use `kind` / `source` fields to record provenance, not only the folder name).
- Prefer mechanical changes:
  - Insert `images:` immediately before `image:` in an entry.
  - Sort `images` paths and de-duplicate.
  - Do not modify other fields unless explicitly requested.

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

Optional YAML `links:` block overrides auto-generated atlas URLs in `pollen.json` (`pollenx`, `tstebler`, `paldat`); use explicit `null` when a default URL would be wrong.

## Regenerate the runtime index and manifests

`docs/javascripts/vdh-pollentabel.js` reads `docs/data/pollen.json` for endpoints that use `id.pollen_key`. After any change to `data/pollen.yaml`, regenerate site data (not tracked in git):

```bash
./.venv/bin/python scripts/build_docs_data.py
```

Rules:
- Do not edit `docs/data/pollen.json` or `docs/assets/manifests/*.json` by hand; they are generated.
- The exporter emits `latin`, `dutch`, `family`, `shape`, `ornamentation`, `aperture`, `size`, `display_width_px`, `links`, and `images` (with per-image `width_px` when derivable; see `scripts/export_pollen_json.py`).

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
