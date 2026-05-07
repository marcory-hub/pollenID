---
name: update-vanderham
description: >-
  Keeps van der Ham pollentabel JSON valid, aligns by-taxon image folders with
  pollen_key slugs, syncs images into data/pollen.yaml, and regenerates
  docs data. Use when editing docs/keys/vanderham/vanderham-pollentabel.json or
  when adding PNGs under docs/assets/images/by-taxon/ for taxa in that key.
---

# Update van der Ham pollentabel

When you edit **`docs/keys/vanderham/vanderham-pollentabel.json`** or drop new bitmaps under **`docs/assets/images/by-taxon/<pollen_key>/`** for taxa used in that key:

## JSON

The file must parse as strict JSON. Watch for missing commas between object properties (e.g. after `"pollen_key"` before `"pollen_keys"`) and corrupted merge artefacts (duplicate `"pollen_key"` / `"name"` on one line). Quick check:

```bash
./.venv/bin/python -c "import json; json.load(open('docs/keys/vanderham/vanderham-pollentabel.json'))"
```

## Markdown in strings

Endpoint `id.name` may use `[label](https://…)` links; **`docs/javascripts/vdh-pollentabel.js`** only turns `http:`/`https:` into links. Keep paired `*…*` for genus emphasis per project rules.

## Images → `data/pollen.yaml`

Runtime lookups use **`docs/data/pollen.json`**, built from **`data/pollen.yaml`**. Do not edit **`docs/data/pollen.json`** by hand.

- The directory name **`docs/assets/images/by-taxon/<slug>/`** must match the **`pollen_key` / `pollen_keys[]`** slug in the JSON (fix typos, e.g. `carex_pendulae` → `carex_pendula`, before adding images).
- After new PNGs appear on disk:

```bash
./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
```

That script only appends images for taxa that **already exist** in **`data/pollen.yaml`**. For a **new** slug, add a minimal YAML entry (at least `latin` + `images[]`) or extend an existing taxon, then re-run sync if needed.

Prefer stable names: **`assets/images/by-taxon/<slug>/<slug>_1.png`**, … (see **`update-pollen-yaml`**). If macOS screenshots use spaces or soft hyphens in the filename, rename them to that pattern so YAML stays one line per `path:` and validators stay green.

## Regenerate and validate

```bash
./.venv/bin/python scripts/build_docs_data.py
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
```

## MkDocs

After substantive doc/data changes, run **`mkdocs build`** (or rely on local serve) to catch broken links.

## References

- **`docs/javascripts/vdh-pollentabel.js`** — `pollen_key` / `pollen_keys` → **`pollen.json`** images
- **`.cursor/skills/update-pollen-yaml/SKILL.md`**
- **`.cursor/skills/interactive-pollen-key/SKILL.md`**
