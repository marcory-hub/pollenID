---
name: add-kerkvliet-images
description: >-
  After new Kerkvliet atlas screenshots land under by-taxon, rename them,
  apply agent: notes into pollen.yaml / key JSON, sync images, inject
  pollen_key, and regenerate site data so images appear in the table and
  taxon pages. Use when the user says add kerkvliet images, wire kerkvliet
  screenshots, or @add-kerkvliet-images.
---

# Add Kerkvliet images

Run after the user drops atlas PNGs into `docs/assets/images/by-taxon/<slug>/`
(or moves a filled `_todo/<slug>/` into `by-taxon/`). Do not invent taxa.

## Preconditions

- Screenshots live under **`docs/assets/images/by-taxon/<slug>/`**, not only `_todo/`.
- Folder name is the canonical **`pollen_key`** (ASCII `genus_species`).
- Prefer `kind` / `source: kerkvliet` on new YAML image rows when adding by hand.

## Steps (in order)

1. **Move** any `_todo/<slug>/` that already has `*.png` into `by-taxon/<slug>/`
   (merge into existing folder if present; remove empty `_todo` stub).
2. **Apply `agent:` notes** from `docs/assets/images/by-taxon/_todo/_links/_kerkvliet.md`
   for every taxon in this batch (and any clear global rename the user confirmed):
   - **Folder / key renames**: rename `by-taxon/<old>/` to `<new>/` when needed; update
     `pollen_key` (and latin/dutch when stated) in
     `docs/keys/kerkvliet/kerkvliet-determinatietabel.json`; rename or merge the
     matching top-level key in `data/pollen.yaml`.
   - **YAML fields** when the note supplies them: `dutch`, `bloeitijd.start` /
     `bloeitijd.end` (month numbers 1–12), `nectar_value` / `pollen_value`, `note`
     (synonyms, literature). Map `(np)N` to **both** `nectar_value` and
     `pollen_value` = N unless the user says otherwise.
   - Do **not** put plant height into pollen `size`.
   - Skip vague notes (`replace by` with empty target, “no images online”) or ask.
   - Ask before guessing typos (`hippocastaneum` vs `hippocastanum`, etc.).
3. **Rename** macOS screenshots:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py
   ```
   Result: `<slug>_N.png` (appends after existing numbered files).
4. **YAML entry**: if `data/pollen.yaml` lacks the slug, add a minimal stub
   (`latin` + `images:`) per **update-pollen-yaml**. Do not invent fields.
5. **Sync disk → YAML**:
   ```bash
   ./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
   ```
6. **Remove stale paths** in YAML that still point at deleted `Schermafbeelding*`
   or soft-hyphen names for those slugs.
7. **Wire Kerkvliet rows**:
   ```bash
   ./.venv/bin/python scripts/inject_pollen_keys_into_key_json.py
   ```
   Optional after inject: slim rows that now have a valid key:
   ```bash
   ./.venv/bin/python scripts/slim_pollen_key_endpoints.py \
     docs/keys/kerkvliet/kerkvliet-determinatietabel.json
   ```
8. **Regenerate + validate**:
   ```bash
   ./.venv/bin/python scripts/build_docs_data.py
   ./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
   ```
9. **Queue hygiene** (optional): refresh task folders; drop done entries from
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
