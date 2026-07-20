---
name: add-pollen
description: >-
  End-to-end workflow to add or update a pollen taxon across the codebase:
  by-taxon images, data/pollen.yaml fields, species pages, optional key JSON
  wiring, synonyms naslag, and site validation. Use when the user says add
  pollen, @add-pollen, add by-taxon images, wire atlas screenshots, apply
  agent notes, @add-by-taxon-images, add kerkvliet images, or
  @add-kerkvliet-images.
---

# Add pollen (images + data + pages)

Run after atlas PNGs land in `docs/assets/images/by-taxon/<slug>/` (or a filled
`_todo/<slug>/` is moved there). Do not invent taxa, morphology, or paths.

## Preconditions

- Screenshots under **`by-taxon/<slug>/`**, not only `_todo/`.
- Folder name = canonical **`pollen_key`** (ASCII `genus_species`, or `genus_typ` for type aggregates).
- Type aggregates: latin `Genus typ`, dutch `{vernacular} type` (never `sp.` / `spp.` / `soorten`). See `project-context.mdc`.
- New YAML image rows: `kind` / `source` = `by_taxon` only (sync does this).
  Do not invent atlas-specific `source`; do not strip historical ones.
- Agent notes in **both** `_todo/_links/_kerkvliet.md` and
  `_todo/_links/_pollen-atlas-links.md` (`agent:` / `Agent:` lines).
- User-supplied morphology, family, Dutch name, sizes: write to `data/pollen.yaml`
  (SoT). Beug sizes in `size.*`; Kerkvliet sizes in `pollen_features.pollen-note`
  (`Kerkvliet: … µm`).

## Steps (in order)

### 1. Images on disk

1. **Move** `_todo/<slug>/` with `*.png` into `by-taxon/<slug>/` (merge if
   present; remove empty `_todo` stub).
2. **Rename** macOS screenshots:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py
   ```
   Result: `<slug>_N.png` (appends after existing numbered files).

### 2. YAML (`data/pollen.yaml`)

Apply every `agent:` / `Agent:` note and user-supplied fields from **both** link
files (and any confirmed global rename). Typical tasks:

- **Rename / replace key**: OCR/truncated slug → `genus_species` (or `genus_typ`
  when no species epithet). Rename `by-taxon/<old>/` if present; update Kerkvliet
  JSON `pollen_key` (and latin/dutch) when the taxon is in that key; rename/merge
  YAML key; drop duplicate stubs. Update all references in one pass.
- **Fields** when supplied: `name.dutch_name`, `classification.family_latin` /
  `family_dutch`, `classification.genus`, morphology under `pollen_features.*`,
  `flowering_time.start` / `.end` (1–12), `value.nectar_value` / `pollen_value`,
  `note.*`, `frequency_in_*_honey`. Map `(np)N` to both values = N unless told
  otherwise.
- **Merge** stubs; **remove** genus/`sp.` rows when species keys exist.
- **Remap** (e.g. Aster → Symphyotrichum / Tripolium / Galatella) per note.
- Do **not** put plant height into pollen `size`.
- **YAML stub** if missing (`latin` + `images:`) per **update-pollen-yaml**.
- **Sync disk → YAML**:
  ```bash
  ./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
  ```
- **Remove stale paths** (`Schermafbeelding*`, soft-hyphen names) for those slugs.

### 3. Species page (`docs/pollen/species/<pollen_key>.md`)

Follow **pollen-pagina** (canonical: `calluna_vulgaris.md`):

- H1: `# *Genus species* (Nederlandse naam)`
- Top gallery: `{{ gallery("<pollen_key>") }}` when all images are in YAML
- `## Kenmerken` table with `{{ pollen("<pollen_key>", "field") }}` macros
- `## Determinatiesleutels`: run `extract_key_paths.py`; add manual Beug bullets
  only when JSON lacks `pollen_key` on the endpoint (cite source)
- `## Online databases`: verified links from YAML `links:` or atlas queue

### 4. Synonyms table

When this batch applies a rename, merge, remap, or synonym/basioniem `note`, update
`docs/naslag/synoniemen-en-basioniemen.md` **Verzamelde voorbeelden**:

- Add or refresh the row for the accepted `pollen_key`.
- Drop “(beoogd)” / “YAML heeft nog …” once the accepted key is in
  `data/pollen.yaml` and the old key is gone or only kept as `note`/`latin`.
- Do not invent rows without a verified YAML or agent-note source.

### 5. Keys (only when applicable)

**Wire Kerkvliet** only if any batch slug is in
`docs/keys/kerkvliet/kerkvliet-determinatietabel.json`, or the user said the
batch is for Kerkvliet. Atlas-only taxa skip.

```bash
./.venv/bin/python scripts/inject_pollen_keys_into_key_json.py
./.venv/bin/python scripts/slim_pollen_key_endpoints.py \
  docs/keys/kerkvliet/kerkvliet-determinatietabel.json
```

Do **not** edit `docs/keys/` unless the user explicitly requests keys changes.

### 6. Regenerate + validate

```bash
./.venv/bin/python scripts/build_docs_data.py
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
```

### 7. Queue hygiene

Delete finished `## <slug>` (incl. `agent:` lines) from **whichever** of
`_kerkvliet.md` / `_pollen-atlas-links.md` still has it; remove `_todo/<slug>/`
(not `by-taxon/<slug>/` with images); optional:

```bash
./.venv/bin/python scripts/bootstrap_by_taxon_task.py --apply
```

## Codebase touchpoints (rename / new taxon)

Update together when `pollen_key` changes:

| Area | Path / action |
| :--- | :--- |
| SoT | `data/pollen.yaml` |
| Images | `docs/assets/images/by-taxon/<pollen_key>/` |
| Species page | `docs/pollen/species/<pollen_key>.md` |
| Generated | `docs/data/pollen.json` via `build_docs_data.py` |
| Kerkvliet | `docs/keys/kerkvliet/kerkvliet-determinatietabel.json` (if listed) |
| Synonyms | `docs/naslag/synoniemen-en-basioniemen.md` |
| Queue | `_todo/_links/_kerkvliet.md`, `_pollen-atlas-links.md` |
| Nav | `mkdocs.yml` only when user asks (family page link preferred) |

## Stop conditions

- Missing image paths from validator: fix or restore before commit.
- Folder slug ≠ `pollen.yaml` / Kerkvliet key: apply rename note or ask first.
- Do **not** rebuild Kerkvliet JSON from transcript without re-running inject.
- Skip vague agent notes or ask; ask before guessing typos.

## Related

- `.cursor/skills/add-images-information/SKILL.md` (single taxon with user metadata block)
- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/pollen-pagina/SKILL.md`
- `.cursor/skills/trace-key-paths/SKILL.md`
- `.cursor/skills/update-vanderham/SKILL.md`
- `docs/naslag/synoniemen-en-basioniemen.md`
- `scripts/rename_kerkvliet_screenshot_imports.py`
