---
name: add-by-taxon-images
description: >-
  After new atlas screenshots land under by-taxon, rename them, apply agent:
  notes from both _todo link files into pollen.yaml / key JSON, sync images,
  inject pollen_key when needed, regenerate site data, update the synonyms
  naslag table, and remove completed taxa from the _todo queue. Use when the
  user says add by-taxon images, wire atlas screenshots, apply agent notes,
  @add-by-taxon-images, add kerkvliet images, wire kerkvliet screenshots, or
  @add-kerkvliet-images.
---

# Add by-taxon images

Run after atlas PNGs land in `docs/assets/images/by-taxon/<slug>/` (or a filled
`_todo/<slug>/` is moved there). Do not invent taxa.

## Preconditions

- Screenshots under **`by-taxon/<slug>/`**, not only `_todo/`.
- Folder name = canonical **`pollen_key`** (ASCII `genus_species`).
- New YAML image rows: `kind` / `source` = `by_taxon` only (sync does this).
  Do not invent atlas-specific `source`; do not strip historical ones.
- Agent notes in **both** `_todo/_links/_kerkvliet.md` and
  `_todo/_links/_pollen-atlas-links.md` (`agent:` / `Agent:` lines).

## Steps (in order)

1. **Move** `_todo/<slug>/` with `*.png` into `by-taxon/<slug>/` (merge if
   present; remove empty `_todo` stub).
2. **Apply every `agent:` / `Agent:` note** for the batch from **both** link
   files (and any confirmed global rename). Typical tasks:
   - **Rename / replace key**: OCR/truncated slug → `genus_species`. Rename
     `by-taxon/<old>/` if present; update Kerkvliet JSON `pollen_key` (and
     latin/dutch) when the taxon is in that key; rename/merge YAML key; drop
     duplicate stubs. Prefer Pollen Wiki spelling when the note says so; other
     spellings in `note` / `latin` (see
     `docs/naslag/synoniemen-en-basioniemen.md`).
   - **YAML fields** when supplied: `dutch`, `bloeitijd.start` / `.end` (1–12),
     `nectar_value` / `pollen_value`, `note`. Map `(np)N` to both values = N
     unless told otherwise.
   - **Merge** stubs; **remove** genus/`sp.` rows when species keys exist.
   - **Remap** (e.g. Aster → Symphyotrichum / Tripolium / Galatella) per note.
   - Do **not** put plant height into pollen `size`.
   - Skip vague notes or ask; ask before guessing typos.
3. **Synonyms table**: when this batch applies a rename, merge, remap, or
   synonym/basioniem `note`, update
   `docs/naslag/synoniemen-en-basioniemen.md` **Verzamelde voorbeelden**:
   - Add or refresh the row for the accepted `pollen_key`.
   - Drop “(beoogd)” / “YAML heeft nog …” once the accepted key is in
     `data/pollen.yaml` and the old key is gone or only kept as `note`/`latin`.
   - Do not invent rows without a verified YAML or agent-note source.
4. **Rename** macOS screenshots:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py
   ```
   Result: `<slug>_N.png` (appends after existing numbered files).
5. **YAML stub** if missing (`latin` + `images:`) per **update-pollen-yaml**.
6. **Sync disk → YAML**:
   ```bash
   ./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
   ```
7. **Remove stale paths** (`Schermafbeelding*`, soft-hyphen names) for those slugs.
8. **Wire Kerkvliet** only if any batch slug is in
   `docs/keys/kerkvliet/kerkvliet-determinatietabel.json`, or the user said the
   batch is for Kerkvliet. Atlas-only taxa skip.
   ```bash
   ./.venv/bin/python scripts/inject_pollen_keys_into_key_json.py
   ./.venv/bin/python scripts/slim_pollen_key_endpoints.py \
     docs/keys/kerkvliet/kerkvliet-determinatietabel.json
   ```
   (`slim` is optional after inject.)
9. **Regenerate + validate**:
   ```bash
   ./.venv/bin/python scripts/build_docs_data.py
   ./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
   ```
10. **Queue hygiene**: delete finished `## <slug>` (incl. `agent:` lines) from
    **whichever** of `_kerkvliet.md` / `_pollen-atlas-links.md` still has it;
    remove `_todo/<slug>/` (not `by-taxon/<slug>/` with images); optional:
    ```bash
    ./.venv/bin/python scripts/bootstrap_by_taxon_task.py --apply
    ```

## Stop conditions

- Missing image paths from validator: fix or restore before commit.
- Folder slug ≠ `pollen.yaml` / Kerkvliet key: apply rename note or ask first.
- Do **not** rebuild Kerkvliet JSON from transcript without re-running inject.

## Related

- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/update-vanderham/SKILL.md`
- `docs/naslag/synoniemen-en-basioniemen.md`
- `scripts/rename_kerkvliet_screenshot_imports.py`
