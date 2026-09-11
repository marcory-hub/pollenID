# Handoff: Buiten EU gallery size sort

## Goal
Make `docs/gallerie/gallery-non-eu.md` (live: https://marcory-hub.github.io/pollenID/gallerie/gallery-non-eu/) show pollen grains in one true-scale strip, sorted small to large.

## Current state
- Live page already renders `{{ gallery() }}` per taxon, but the Markdown is alphabetical: ~335-row table, then 335 `###` sections. TOC is unusable; size comparison is not possible.
- Cape coverage (counted this session from `data/pollen.yaml` + `docs/keys/flora-regio-kaap/taxa-index.json`): 335 unique keys, all have images; 5 numeric `size.*`; 248 Delport size class in `pollen-note`; 85 no size. Class labels include Dutch and English (`klein`/`small`, `middelgroot`/`medium`).
- Do not write Delport bins into `size.size_*` (`scripts/fill_pollen_yaml_from_delport.py` keeps bins in `pollen-note` only). Use class midpoints for gallery sort/display only; caption must show the class, not a fake µm.
- Helpers landed in (`scripts/pollen_display.py`): `canonicalize_delport_size_class`, `parse_delport_size_class`, `json_entry_max_um`, `json_entry_size_class`, `json_entry_size_sort_key`, `json_entry_gallery_width_px`, `json_entry_size_caption`. Midpoints: zeer klein 8, klein 18, middelgroot 38, groot 75, zeer groot 120. Unknown last.
- Not done: `gallery_non_eu()` / `gallery_sorted` in (`scripts/mkdocs_macros.py`), CSS `--compare`, rewrite of (`docs/gallerie/gallery-non-eu.md`), ingest `update_gallery()` in (`scripts/ingest_flora_regio_kaap_taxa.py`), macro rows in (`docs/naslag/site-architectuur.md`) and (`docs/naslag/scripts.md`).
- `gallery()` itself is unchanged (no captions). Existing species-page display widths stay on measured size or 50 µm default.

## Next steps
1. Add `gallery_sorted(*keys)` plus `gallery_non_eu()` in (`scripts/mkdocs_macros.py`): Coffea + unique keys from (`docs/keys/flora-regio-kaap/taxa-index.json`); one first image per taxon; sort via `json_entry_size_sort_key`; width via `json_entry_gallery_width_px`; figcaption latin + `json_entry_size_caption`; link to `pollen/species/<key>.md` via `normalize_url`.
2. Add `.pid-scale-row--compare` in (`docs/stylesheets/extra.css`): `min-width: 0` on captioned items so small grains stay small (`:has(figcaption)` currently forces 10.5rem).
3. Replace (`docs/gallerie/gallery-non-eu.md`) with a short slide sheet: 2-row index table (Coffea + taxa-index), one sentence on sort/scale rule, `{{ gallery_non_eu() }}`. Drop the 335 headings and per-taxon galleries.
4. Change `update_gallery()` in (`scripts/ingest_flora_regio_kaap_taxa.py`) so a later `--apply` does not restore the alphabetical dump.
5. Add one macro row each in (`docs/naslag/site-architectuur.md`) and (`docs/naslag/scripts.md`). Rebuild JSON if needed, then `mkdocs build --strict`. Do not commit/push unless asked.

## Artifacts
- `scripts/pollen_display.py` — size-class parse/sort/width/caption (done)
- `docs/gallerie/gallery-non-eu.md` — still the alphabetical dump (must rewrite)
- `docs/keys/flora-regio-kaap/taxa-index.json` — Cape key list for `gallery_non_eu()`
- `scripts/mkdocs_macros.py` — existing `gallery()` to extend
- `scripts/ingest_flora_regio_kaap_taxa.py` — `update_gallery()` still writes the dump

## Suggested skills
- None.
