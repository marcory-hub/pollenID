---
name: add-images-information
description: >-
  Add atlas by-taxon images and user-supplied pollen metadata to the codebase:
  rename PNGs, fill data/pollen.yaml, update the species page, sync images, and
  validate. Use when the user says add images information, @add-images-information,
  supplies a taxon info block with morphology/family/size plus screenshots, or
  wires a new by-taxon folder with pollen.yaml fields.
---

# Add images + information

End-to-end when the user supplies **both** atlas screenshots (or they already sit
under `by-taxon/<pollen_key>/`) **and** a metadata block (family, size, pollen
class, morphology, Dutch name). Do not invent taxa, morphology, or paths.

For batch queue work (agent notes, Kerkvliet inject, renames across many slugs),
use **add-pollen** instead.

## User input (minimum)

| Item | Rule |
| :--- | :--- |
| `pollen_key` | ASCII `genus_species`; folder name under `by-taxon/` |
| Dutch name | `name.dutch_name`; volksmond in `note.note_plant` if given |
| Family | `classification.family_latin` + `classification.family_dutch` |
| Pollen size | Range → `size.size_smallest` / `size_largest` (µm); mean in `pollen-note` if useful |
| Pollen class | `pollen_class_beug` (closed label from scripts.md); German chapter text in `pollen-note` when no exact label |
| Morphology | Dutch → `pollen_features.*` (`shape`, `polarity`, `aperture`, `sculpture`, `ornamentation`, `pe_ratio`) |
| Value / flowering | Only when user supplies `(np)N` or month numbers |

German atlas text: translate morphology to Dutch; keep PoFormI / PolFeldI ratios in `pollen-note`.

## Steps (in order)

### 1. Images on disk

1. PNGs in `docs/assets/images/by-taxon/<pollen_key>/` (move from `_todo/<pollen_key>/` if needed).
2. Rename macOS screenshots:
   ```bash
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
   ./.venv/bin/python scripts/rename_kerkvliet_screenshot_imports.py
   ```
   Result: `<pollen_key>_N.png`.
3. If images were listed under the wrong YAML key, move rows to the correct key and clear the wrong entry.

### 2. YAML (`data/pollen.yaml`)

Follow **update-pollen-yaml**. Fill every user-supplied field on the `pollen_key` block:

- `classification.genus` from the Latin epithet when empty.
- Beug sizes in `size.*`; Kerkvliet-only sizes in `pollen_features.pollen-note` (`Kerkvliet: … µm`).
- Do not put plant height into pollen `size`.
- Stub if missing (`latin_name` + empty `images:`).

Sync disk → YAML and drop stale screenshot paths:

```bash
./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
```

Remove `Schermafbeelding*` / soft-hyphen paths for this slug after sync.

### 3. Species page (`docs/pollen/species/<pollen_key>.md`)

Follow **pollen-pagina** (canonical: `aconitum_napellus.md` / `calluna_vulgaris.md`):

- H1: `# *Genus species* (Nederlandse naam)`
- `{{ gallery("<pollen_key>") }}` when all images are in YAML
- `## Kenmerken` table with `pollen(...)` macros
- `## Determinatiesleutels`: `extract_key_paths.py --page-section`
- `## Online databases`: links from YAML `links:`

Replace auto-generated Imkerpedia stubs when YAML and images are complete.

### 4. Keys (only when applicable)

If the taxon is in `docs/keys/kerkvliet/kerkvliet-determinatietabel.json` or the user asked for keys:

```bash
./.venv/bin/python scripts/inject_pollen_keys_into_key_json.py
./.venv/bin/python scripts/slim_pollen_key_endpoints.py \
  docs/keys/kerkvliet/kerkvliet-determinatietabel.json
```

Do not edit `docs/keys/` otherwise.

### 5. Regenerate + validate

```bash
./.venv/bin/python scripts/build_docs_data.py
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
```

### 6. Queue hygiene

Remove finished `## <pollen_key>` from `_todo/_links/_pollen-atlas-links.md` (and `_kerkvliet.md` when present). Remove empty `_todo/<pollen_key>/` only.

## Codebase touchpoints

| Area | Path |
| :--- | :--- |
| SoT | `data/pollen.yaml` |
| Images | `docs/assets/images/by-taxon/<pollen_key>/` |
| Species page | `docs/pollen/species/<pollen_key>.md` |
| Generated | `docs/data/pollen.json` via `build_docs_data.py` |
| Queue | `_todo/_links/_pollen-atlas-links.md` |

## Stop conditions

- Folder slug ≠ `pollen_key`: fix or ask before sync.
- Missing image paths from validator: fix rename/sync before commit.
- Uncertain Dutch vernacular: leave empty or `[to be verified]`; do not guess obscure names.

## Related

- `.cursor/skills/add-tstebler/SKILL.md` (text only; images already on disk)
- `.cursor/skills/add-pollen/SKILL.md` (batch / Kerkvliet / renames)
- `.cursor/skills/add-images-information/EXAMPLES.md` (worked example)
- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/pollen-pagina/SKILL.md`
