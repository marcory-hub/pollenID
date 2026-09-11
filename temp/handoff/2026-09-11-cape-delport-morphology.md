# Handoff: Cape Delport morphology fill

## Goal
Cape Flora-regio-kaap taxa have Kenmerken from Delport key paths / §3.3 types (not Wiki/PalDat), Determinatiesleutels show Flora regio Kaap pads, and atlas links are hygiene-only.

## Current state
- Plan implemented: Delport-only morphology fill; Wiki/PalDat = link probe only. Plan file: user Cursor plans (`cape_delport_morphology`); do not edit unless asked.
- `docs/keys/flora-regio-kaap/`: interactive keys + `taxa-index.json` (335 unique keys) + new `type-members.json` (15 types, ~102 members).
- `scripts/fill_pollen_yaml_from_delport.py`: fills empty `pollen_features` from key paths + type members; size bins → `pollen-note` only; `--probe-links` marks 404s as `not in the database`.
- `scripts/ingest_flora_regio_kaap_taxa.py`: after `--apply` runs the fill unless `--skip-fill`; `wiki_title()` keeps infraspecific `_ssp._` form.
- `scripts/extract_key_paths.py`: walks `flora-regio-kaap`; heading **Flora regio Kaap**; type members resolve via `type-members.json`.
- Coverage: **327/335** Cape taxa have aperture/sculpture/shape/polarity; **8 still empty**: `aspalathus_cymbiformis`, `heliophila_linearis`, `indigofera_procumbens`, `mesembryanthemum_guerichianum`, `olea_exasperata`, `sparrmannia_africana`, `tetragonia_fruticosa`, `xiphotheca_reflexa` (plate-only / multi-taxon leaves / no unique path).
- Link probe: 670 checked → 229 patched to `not in the database`.
- Validate: `--images` OK; `--rebuild-data` regenerates species pages. `--links` still fails on **77 pre-existing non-Cape** entries (mostly `*_typ`); **0 Cape** link errors.
- Parent intake (keys, crops, gallery) was earlier session [flora-regio-kaap intake](58404ae9-1b7c-44fb-af22-896ab56c9985); this session thickened Kenmerken.

## Next steps
1. For the 8 empty slugs: check if they appear in multi-taxon key outcomes or only plates; fill only from verified Delport path/§3.5 text (no invention); else leave empty + plate note.
2. Optionally normalize legacy `3-colporaat` / `3-colpaat` on Felicia-type members to Dutch `tricolporaat` / `tricolpaat` (empty-fields-only left prior values).
3. Fix or defer the 77 non-Cape `--links` validator failures if a green full validate is needed before push.
4. Do not invent `pollen_class_beug` or numeric `size_*` from Delport size classes.

## Artifacts
- `docs/keys/flora-regio-kaap/type-members.json` — §3.3 membership + type features
- `scripts/fill_pollen_yaml_from_delport.py` — Cape morphology + optional link probe
- `scripts/extract_key_paths.py` — Determinatiesleutels include Flora regio Kaap
- `scripts/ingest_flora_regio_kaap_taxa.py` — skeleton + optional fill hook
- `data/pollen.yaml` — filled Cape `pollen_features`
- `docs/naslag/scripts.md` — script index rows
- `.cursor/skills/update-pollen/REFERENCE.md` — Cape bulk = Delport fill note

## Suggested skills
- `@update-pollen` — if filling the 8 empties from user-pasted §3.5 / plate text per taxon
- `@interactive-pollen-key` — only if key JSON terminals need fixing so those 8 get unique paths (explicit keys ask required)
