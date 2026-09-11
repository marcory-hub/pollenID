---
name: add-pollen
description: >-
  Interactive new-taxon intake: create by-taxon folder, wait for images, draft
  data/pollen.yaml from Pollen-Wiki, PalDat, and local docs/keys/notes/paste,
  confirm with the user, then run add_taxon and validate. Use when adding a new
  species, @add-pollen, add pollen, new taxon, or nieuwe soort.
---

# Add pollen (new taxon intake)

Interactive intake for a **new** `pollen_key`. Do not invent taxa, morphology, or paths. Schema and field map: [`../update-pollen/REFERENCE.md`](../update-pollen/REFERENCE.md). Example: [EXAMPLES.md](EXAMPLES.md).

Existing slug in `data/pollen.yaml` → stop; use **`@update-pollen`**.

## Preconditions

- Latin name from the user (ask if missing).
- `pollen_key`: ASCII lowercase underscores (`crataegus_monogyna`) or `genus_typ` (`Genus typ` / `{vernacular} type`).
- Confirm slug is absent from `data/pollen.yaml` before creating anything.

## Steps (two hard stops)

1. **Folder.** Create `docs/assets/images/by-taxon/<pollen_key>/`. Give the user that path plus default atlas URLs (same construction as `scripts/pollen_display.py` `default_external_links`):
   - Pollen-Wiki: `https://pollen.tstebler.ch/MediaWiki/index.php?title=<Genus_species>`
   - PalDat: `https://www.paldat.org/pub/<Genus_species>`
   - PollenX / Waarneming.nl as needed.
   **STOP.** Do not draft YAML until the user says images are in, or that this taxon is text-only (`images: []`).

2. **Images.** List files under the folder. Rename `Schermafbeelding*` with:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --only-folder <pollen_key>
   ```
   New image rows: `kind` / `source` = `by_taxon`. Ask only if unclear: keep/drop extras, polar vs equatorial vs SEM vs optical section, mixed sources, gallery order. Do not invent view labels.

3. **Sources (no invented morphology).**
   - Fetch Pollen-Wiki (`tstebler`) and PalDat. On 404: set that `links` value to the site’s usual “not in the database” wording; skip morphology from that source.
   - Local: `docs/pollen/families/` if present; `./.venv/bin/python scripts/extract_key_paths.py <pollen_key> --status`; matching `notes/` (read only); sibling YAML in the same genus for **field shape only**, never copy morphology.
   - Anything the user pasted or attached.

4. **Draft YAML in chat, then STOP for confirm.** Map tstebler via the atlas field map in REFERENCE. Beug sizes → `size.*`. PalDat / Kerkvliet measurements → `pollen-note` (`PalDat: …` / `Kerkvliet: …`); do not overwrite Beug `size.*`. Dutch vernacular when sure. `pollen_class_beug` only from the closed list in `docs/naslag/scripts.md`. Show provenance per field (path or URL). User may edit the draft; if they already patched YAML on disk, on-disk wins.

5. **On confirm.** Insert the canonical block into `data/pollen.yaml` (minimal diff). Append `pollen_key` to `data/species_page_slugs.txt`. Then:
   ```bash
   ./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --render-pages
   ./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
   ```
   If the taxon is already in a key: `extract_key_paths.py <pollen_key> --page-section` and merge Determinatiesleutels. Do **not** edit `docs/keys/` or rewrite family pages unless the user asks.

## Stop / out of scope

- Validator failures or slug mismatches: fix or ask before treating the add as done.
- Vague OCR or conflicting sources: ask; never guess.
- Author/reshape dichotomous keys → **`@interactive-pollen-key`**.
- Existing taxon updates → **`@update-pollen`**.
