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
- Canonical layout for taxon-linked rasters: `assets/images/by-taxon/<pollen_key>/...` (use `kind` / `source` fields to record provenance, not only the folder name).
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
  - path: assets/images/by-taxon/foo_bar/Foo_bar_Eo.png
    kind: pollenwiki
    source: pollenwiki
```

`kind` and `source` record the image corpus (e.g. `pollenwiki`, `paldat`, `persano_oddo`, `beug`, `kerkvliet`).

## Regenerate the runtime index and manifests

`docs/javascripts/vdh-pollentabel.js` reads `docs/data/pollen.json` for endpoints that use `id.pollen_key`. After any change to `data/pollen.yaml`, regenerate site data (not tracked in git):

```bash
./.venv/bin/python scripts/build_docs_data.py
```

Rules:
- Do not edit `docs/data/pollen.json` or `docs/assets/manifests/*.json` by hand; they are generated.
- The exporter emits `latin`, `dutch`, `family`, `shape`, `ornamentation`, `aperture`, `size`, and `images` (see `scripts/export_pollen_json.py`).

## Auditing and migration helpers
- Read-only inventory: `python scripts/audit_pollen_assets.py`
- Append confidently mapped files missing from YAML: `python scripts/sync_yaml_confident_images.py`
- Move resolved rasters into `by-taxon` (rewrites references): `python scripts/migrate_pollen_images_by_taxon.py --apply`
