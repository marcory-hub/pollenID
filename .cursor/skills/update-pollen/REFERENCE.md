# `update-pollen` reference

Load when editing YAML shape, atlas field mapping, page/sleutel details, or audit helpers.

## Canonical YAML entry

```yaml
slug:
  name:
    latin_name:
    dutch_name:
  classification:
    order:
    family_latin:
    family_dutch:
    tribe:
    genus:
  size:
    size_smallest:
    size_largest:
    height_px:
  pollen_class_beug:
  beug_key_paths:
  pollen_features:
    shape:
    sculpture:
    sculpture_visibility:   # lm_clear | lm_poor | em_only
    aperture:
    aperture_visibility:
    ornamentation:
    ornamentation_visibility:
    polarity:
    pe_ratio:
    pollen-note:
  flowering_time: { start, end }
  value: { nectar_value, pollen_value }
  note: { note_plant, note_honey, note_pollen }
  frequency_in_dutch_honey:
  frequency_in_eu_honey:
  frequency_in_non_eu_honey:
  learning_priority_rank:
  lookalikes:
  links: { pollenX, tstebler, paldat, waarneming }
  images: [...]
```

```yaml
  images:
  - path: assets/images/by-taxon/foo_bar/foo_bar_1.png
    kind: by_taxon
    source: by_taxon
```

Visibility: `lm_clear` / `lm_poor` / `em_only`. Lookalikes: `lookalike_candidates.py` → `lookalike_review.yaml` → `promote_lookalikes.py` → `build_manifests.py`.

## Atlas / tstebler field map

| Atlas field | YAML |
| :--- | :--- |
| Latin → `genus_species` | top-level key; `name.latin_name` |
| Dutch (if sure) | `name.dutch_name` |
| Familie | `family_latin` / `family_dutch`; `genus` from epithet |
| Deutscher Name | `note.note_plant` |
| Pollengrösse `a (b-c)` µm | `size_*` = b–c; `MiW a µm` in `pollen-note` |
| Pollengrösse single `a` | both `size_*` = a; `MiW` in note |
| Pollenklasse | `pollen_class_beug` (closed list: `docs/naslag/scripts.md`) |
| Morphology | Dutch → `shape`, `polarity`, `aperture`, `sculpture`, `ornamentation`, `pe_ratio` |
| PoFormI / PolFeldI / exine | `pollen-note` |
| `(np)N` / months | `value.*` / `flowering_time.*` only if present |

Keep existing Kerkvliet sizes in `pollen-note`. `N S, M D` = screenshot counts, not nectar/pollen values.

## Filename → key

Normalize stem: `-`→`_`, lowercase, collapse `_`. Strip `_ed/_eo/_pd/_po/_em/_om/_o/_d/_e/_p` (+ digits), trailing numerics, `_sizeNNum`. Do not create a missing YAML key unless asked.

## Species page

Match `docs/pollen/species/calluna_vulgaris.md`. Dutch in `docs/`. No invented URLs; no em dash; escape `<` as `&lt;`. Prefer `{{ gallery("pollen_key") }}` when available. Callouts: Material HTML `admonition`, not `!!!`. Do not change `mkdocs.yml` unless asked.

## Determinatiesleutels

```bash
python scripts/extract_key_paths.py <pollen_key> --status
python scripts/extract_key_paths.py <pollen_key> --page-section
```

Replace from `## Determinatiesleutels` through the line before `## Online databases`. Keep `### Beug` / `### Vanderham` / `### Kerkvliet`. Fallbacks (verified only): monofloral/notes for Beug; inject then re-extract for van der Ham; state no Kerkvliet row if absent.

## Helpers

- `scripts/audit_pollen_assets.py`
- `scripts/sync_yaml_confident_images.py` (`--only-by-taxon`, `--include-by-taxon`)
- `scripts/migrate_pollen_images_by_taxon.py --apply`
- By-taxon folder coverage: stub missing YAML keys with `images:` for every `*.png`
