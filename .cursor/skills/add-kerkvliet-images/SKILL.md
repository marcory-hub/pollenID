---
name: add-kerkvliet-images
description: >-
  After new Kerkvliet atlas screenshots land under by-taxon, rename them,
  sync data/pollen.yaml, inject pollen_key into the Kerkvliet JSON, and
  regenerate site data so images appear in the table and taxon pages.
  Use when the user says add kerkvliet images, wire kerkvliet screenshots,
  or @add-kerkvliet-images.
---

# Add Kerkvliet images

Run after the user drops atlas PNGs into `docs/assets/images/by-taxon/<slug>/`
(or moves a filled `_todo/<slug>/` into `by-taxon/`). Do not invent taxa.

## Preconditions

- Screenshots live under **`docs/assets/images/by-taxon/<slug>/`**, not only `_todo/`.
- Folder name is the canonical **`pollen_key`** (ASCII `genus_species`). Apply clear
  `agent:` rename notes from `_todo/_links/_kerkvliet.md` before wiring.
- Prefer `kind` / `source: kerkvliet` on new YAML image rows when adding by hand.

## Steps (in order)

1. **Move** any `_todo/<slug>/` that already has `*.png` into `by-taxon/<slug>/`
   (merge into existing folder if present; remove empty `_todo` stub).
2. **Rename** macOS screenshots:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py
   ```
   Result: `<slug>_N.png` (appends after existing numbered files).
3. **YAML entry**: if `data/pollen.yaml` lacks the slug, add a minimal stub
   (`latin` + `images:`) per **update-pollen-yaml**. Do not invent fields.
4. **Sync disk → YAML**:
   ```bash
   ./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
   ```
5. **Remove stale paths** in YAML that still point at deleted `Schermafbeelding*`
   or soft-hyphen names for those slugs.
6. **Wire Kerkvliet rows**:
   ```bash
   ./.venv/bin/python scripts/inject_pollen_keys_into_key_json.py
   ```
   Optional after inject: slim rows that now have a valid key:
   ```bash
   ./.venv/bin/python scripts/slim_pollen_key_endpoints.py \
     docs/keys/kerkvliet/kerkvliet-determinatietabel.json
   ```
7. **Regenerate + validate**:
   ```bash
   ./.venv/bin/python scripts/build_docs_data.py
   ./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
   ```
8. **Queue hygiene** (optional): refresh task folders; drop done entries from
   `_todo/_links/_kerkvliet.md` only when the user asks.
   ```bash
   ./.venv/bin/python scripts/bootstrap_by_taxon_task.py --apply
   ```

## Stop conditions

- Validator reports missing image paths: fix paths or restore files before commit.
- Slug in folder ≠ Kerkvliet/`pollen.yaml` key: stop and apply the agent rename note
  (or ask) before syncing.
- Do **not** rebuild Kerkvliet JSON from the transcript without re-running inject.

## Related

- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/update-vanderham/SKILL.md` (same YAML → `pollen.json` tail)
- `scripts/rename_kerkvliet_screenshot_imports.py`
