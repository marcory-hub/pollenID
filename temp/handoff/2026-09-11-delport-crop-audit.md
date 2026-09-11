# Handoff: Delport GCFR plate crop audit

## Goal
Keep Delport 2025 Greater Cape Floristic Region atlas taxa correctly placed in YAML, aperture keys / type-members, and by-taxon crops, then leave the site validator green on image paths.

## Current state
- Plate 26 D/E swap fixed: `albuca_clanwilliamae_gloria_1.png` is panel D (teardrop); `albuca_juncifolia_1.png` is panel E (round). Spurious `_2` for clanwilliamae removed from disk and `data/pollen.yaml`.
- Five former orphans are in `docs/keys/flora-regio-kaap/type-members.json`: `heliophila_linearis` → `harveya_typ`; `mesembryanthemum_guerichianum` → `adenogramma_typ`; `tetragonia_fruticosa` → `tetragonia_typ`; `olea_exasperata` → `olea_typ`; `indigofera_procumbens` → `monopsis_typ`.
- Plate-by-plate visual audit (montages under `/tmp/audit/plate_XX.png`) plus geometry flags: primaries clean on plates 1–2, 4–8, 10, 15–25, 27.
- Cleanup done: 37 secondary crops deleted (including `disperis_capensis_2`/`_3` Satyrium misassignment) and matching YAML image rows removed. Primaries left in place, including 18 geometry-flagged `*_1.png` files that are still full grains.
- `scripts/validate_pollen_site.py --images` is OK. `--rebuild-data --images --links` still fails on a pre-existing pollen.json link check (many `*_typ` and other binomials without pollenX/tstebler/PalDat). Rebuild already regenerated `docs/data/pollen.json`, species pages, and morph-neighbours.

## Next steps
1. Do not re-delete primaries from the geometry list unless a visual check against the atlas plate shows a wrong panel.
2. Optional: re-crop remaining thin/awkward primaries (e.g. `lebeckia_plukenetiana_1`, `berzelia_lanuginosa_1`, `lessertia_herbacea_1`, `limeum_africanum_1`) from `(pdf/pollen-determinatie/Delport 2025 - Pollen atlas Greater Cape Floristic Region.pdf)`.
3. If committing this workstream, include YAML, type-members, by-taxon deletions, and generated data only if those files were meant to ship; do not mention Cursor in public docs.
4. Treat `--links` failures as a separate pre-existing issue; do not "fix" vernaculars or links by invention.

## Artifacts
- `data/pollen.yaml` — taxon SoT; image lists after junk-crop removal
- `docs/keys/flora-regio-kaap/taxa-index.json` — plate letter / pollen_key index
- `docs/keys/flora-regio-kaap/type-members.json` — type membership including the five added taxa
- `docs/assets/images/by-taxon/` — Delport crops; primaries kept
- `pdf/pollen-determinatie/Delport 2025 - Pollen atlas Greater Cape Floristic Region.pdf` — plate source
- `/tmp/audit/plate_XX.png` — local montages (not in repo)
- `/tmp/crop_stats.py` — local geometry flagger (not in repo)

## Suggested skills
- `@update-pollen` — replace remaining bad primaries and re-validate
- `@interactive-pollen-key` — only if aperture keys or type JSON need further authoring
