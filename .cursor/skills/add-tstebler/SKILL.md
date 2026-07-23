---
name: add-tstebler
description: >-
  Fill data/pollen.yaml and the species page from a tstebler/pollenwiki atlas
  text block when by-taxon images already exist. Use when add tstebler,
  @add-tstebler, pollenwiki text only, atlas metadata without new screenshots,
  or "add only information/text".
---

# Add tstebler (text only)

Lean path: **images already** under `by-taxon/<pollen_key>/`. No invent. Chat: English; page: Dutch.

## Map

| Atlas field | YAML |
| :--- | :--- |
| Latin binomial → `genus_species` | top-level key; `name.latin_name` |
| Dutch (if sure) | `name.dutch_name` |
| Familie Latin (+ Dutch if sure) | `family_latin` / `family_dutch`; `genus` from epithet |
| Deutscher Name | `note.note_plant` |
| Pollengrösse `a (b-c)` µm | `size_*` = b–c; `MiW a µm` in `pollen-note` |
| Pollengrösse single `a` µm | both `size_*` = a; `MiW a µm` in note |
| Pollenklasse | `pollen_class_beug` (closed list in `docs/naslag/scripts.md`); chapter/type id in `pollen-note` |
| Pollen morphology | Dutch → `shape`, `polarity`, `aperture`, `sculpture`, `ornamentation`, `pe_ratio` |
| PoFormI / PolFeldI / exine | `pollen-note` |
| `(np)N` or month numbers | `value.*` / `flowering_time.*` only if present |

- Keep existing **Kerkvliet** sizes in `pollen-note` (`Kerkvliet: … µm`); do not put them in `size.*`.
- `N S, M D` = screenshot counts, not nectar/pollen values.
- If atlas family ≠ modern family already in YAML: keep YAML family; record atlas family in `note_plant`.

## Steps

1. Grep `^<pollen_key>:` in `data/pollen.yaml`; Read ~60 lines. Stub if missing (`latin_name` + `images:`).
2. Patch only atlas-mapped fields (preserve flowering/value/frequency unless user supplies).
3. Write/replace `docs/pollen/species/<pollen_key>.md`:
   - `# *Genus species* (dutch)`
   - `{{ gallery("<pollen_key>") }}`
   - Kenmerken table via `pollen(...)` (see `corylopsis_pauciflora.md`)
   - `./.venv/bin/python scripts/extract_key_paths.py <pollen_key> --page-section`
   - Online databases from YAML `links:`
4. `./.venv/bin/python scripts/build_docs_data.py`
5. `./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links`

## Skip

- Image rename/sync → `add-images-information`
- Batch / Kerkvliet inject / queue → `add-pollen`
- Edit `docs/keys/` unless user asks

## Related

- `.cursor/skills/add-images-information/SKILL.md` (images + text)
- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/pollen-pagina/SKILL.md`
