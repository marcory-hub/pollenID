---
name: update-pollen-yaml
description: Update and extend data/pollen.yaml as the single source of truth (sizes, fields, images list). Use when the user asks to add/update taxa fields, add images, deduplicate entries, or align keys/pages to pollen.yaml.
---

# Update `data/pollen.yaml`

## Goal
- Keep `data/pollen.yaml` as the SoT, with minimal diffs and no invented taxa/paths.

## Workflow (token-efficient)
- Read only what you need: use targeted search, then small `Read` windows around the relevant key.
- When adding images, derive them from existing files under `docs/assets/images/` and write docs-relative paths like `assets/images/...`.
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
  - path: assets/images/pollenwiki/Foo_bar_Eo.png
    kind: pollenwiki
    source: pollenwiki
```

`kind` and `source` should usually match the folder under `assets/images/` (e.g. `pollenwiki`, `paldat`, `persano_oddo`, `beug`, `kerkvliet`).

## Regenerate the runtime index

`docs/javascripts/vdh-pollentabel.js` reads `docs/assets/data/pollen.json` for endpoints that use `id.pollen_key`. After any change to `data/pollen.yaml`, regenerate that file:

```bash
./.venv/bin/python scripts/export_pollen_json.py
```

Rules:
- Always run the exporter in the same turn as the YAML edit; commit both files together.
- Do not edit `docs/assets/data/pollen.json` by hand; it is generated.
- The exporter only emits `latin`, `dutch`, `family`, `size.smallest_size/largest_size`, and `images`; extending those fields requires editing `scripts/export_pollen_json.py`.

