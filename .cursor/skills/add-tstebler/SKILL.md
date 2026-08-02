---
name: add-tstebler
description: >-
  Fill data/pollen.yaml and the species page from a tstebler/pollenwiki atlas
  text block when by-taxon images already exist. Use when add tstebler,
  @add-tstebler, pollenwiki text only, atlas metadata without new screenshots,
  or "add only information/text".
---

# Add tstebler (text only)

Lean mode of **add-pollen**: **images already** under `by-taxon/<pollen_key>/`.
No invent. Chat: English; page: Dutch.

## Map

| Atlas field | YAML |
| :--- | :--- |
| Latin binomial → `genus_species` | top-level key; `name.latin_name` |
| Dutch (if sure) | `name.dutch_name` |
| Familie Latin (+ Dutch if sure) | `family_latin` / `family_dutch`; `genus` from epithet |
| Deutscher Name | `note.note_plant` |
| Pollengrösse `a (b-c)` µm | `size_*` = b–c; `MiW a µm` in `pollen-note` |
| Pollengrösse single `a` µm | both `size_*` = a; `MiW a µm` in note |
| Pollenklasse | `pollen_class_beug` (closed list in `docs/naslag/scripts.md`) |
| Pollen morphology | Dutch → `shape`, `polarity`, `aperture`, `sculpture`, `ornamentation`, `pe_ratio` |
| PoFormI / PolFeldI / exine | `pollen-note` |
| `(np)N` or month numbers | `value.*` / `flowering_time.*` only if present |

Keep existing **Kerkvliet** sizes in `pollen-note`. `N S, M D` = screenshot counts, not nectar/pollen values.

## Steps

1. Grep `^<pollen_key>:` in `data/pollen.yaml`; Read ~60 lines. Stub if missing.
2. Patch only atlas-mapped fields (preserve flowering/value/frequency unless supplied).
3. Close with orchestrator (skip rename; regenerate page + validate):

```bash
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --skip-rename --render-pages
```

## Skip

- Image rename/sync with new screenshots → **add-images-information**
- Batch / Kerkvliet inject / queue → **add-pollen**
- Edit `docs/keys/` unless user asks

## Related

- `.cursor/skills/add-pollen/SKILL.md`
- `.cursor/skills/add-images-information/SKILL.md`
- `scripts/add_taxon.py`
