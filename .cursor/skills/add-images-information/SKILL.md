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

Mode of **add-pollen** for a **single** taxon when the user supplies screenshots
(or they already sit under `by-taxon/<pollen_key>/`) **and** a metadata block.
Do not invent taxa, morphology, or paths.

Batch / agent-note / multi-slug work → **add-pollen**. Text only → **add-tstebler**.

## User input (minimum)

| Item | Rule |
| :--- | :--- |
| `pollen_key` | ASCII `genus_species`; folder under `by-taxon/` |
| Dutch name | `name.dutch_name`; volksmond in `note.note_plant` if given |
| Family | `classification.family_latin` + `family_dutch` |
| Pollen size | Range → `size.size_smallest` / `size_largest` (µm) |
| Pollen class | `pollen_class_beug` (closed labels in `docs/naslag/scripts.md`) |
| Morphology | Dutch → `pollen_features.*` |
| Value / flowering | Only when user supplies `(np)N` or month numbers |

German atlas text: translate morphology to Dutch; keep PoFormI / PolFeldI in `pollen-note`.
Beug sizes in `size.*`; Kerkvliet-only sizes in `pollen-note` (`Kerkvliet: … µm`).

## Steps

1. Ensure PNGs in `docs/assets/images/by-taxon/<pollen_key>/`.
2. Patch YAML per **update-pollen-yaml** (all user-supplied fields).
3. Write species page (**pollen-pagina**) or use `--render-pages` below.
4. Orchestrator (no separate `build_docs_data.py`):

```bash
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --render-pages
# If taxon is in Kerkvliet and user asked for keys:
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --kerkvliet --render-pages
```

5. Queue hygiene: remove finished `## <pollen_key>` from atlas link files; empty `_todo/<pollen_key>/` only.

## Stop conditions

- Folder slug ≠ `pollen_key`: fix or ask before sync.
- Uncertain Dutch vernacular: leave empty or `[to be verified]`.

## Related

- `.cursor/skills/add-pollen/SKILL.md` (full path)
- `.cursor/skills/add-tstebler/SKILL.md`
- `.cursor/skills/add-images-information/EXAMPLES.md`
- `scripts/add_taxon.py`
