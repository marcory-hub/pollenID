# Handoff: Flora-regio-kaap pre-push checks

## Goal
Finish local checks so the user can commit and push the Cape atlas intake. Gallery Buiten EU and Flora regio Kaap keys should then appear on GitHub Pages.

## Current state
- Intake is in the working tree (uncommitted). Live Pages still shows only *Coffea* on Buiten EU (`https://marcory-hub.github.io/pollenID/gallerie/gallery-non-eu/`).
- Gallery source is complete: 335 unique Cape slugs + *Coffea* in `docs/gallerie/gallery-non-eu.md` (table + `{{ gallery() }}`); YAML, by-taxon images, and species pages exist.
- Keys: 19 aperture JSON files under `docs/keys/flora-regio-kaap/` plus index; paired pages under `docs/Identificatiesleutels/`; branch on `docs/Identificatiesleutels/_index.md`. Plan: user file `flora_regio_kaap_4f8229e0.plan.md`.
- Slug mismatches fixed in this session: `xiphotheca_reflexa`, `sparrmannia_africana`, `aspalathus_cymbiformis` (JSON + outcome Latin) in `flora-regio-kaap-tricolpate.json` / `flora-regio-kaap-tricolporate.json`.
- 15 atlas-type terminals (`aloe_typ`, `gnidia_typ`, `medium_felicia_typ`, …) still have no YAML/`pollen.json` row, so key tiles are placeholders. Members are listed in `docs/keys/flora-regio-kaap/type-members.json`. `pollentabel.js` does not load that file.
- `./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images` succeeded (`validate_pollen_site: OK`). Regenerated 1837 species pages and morph-neighbours. Skip `--links` (77 older non-Cape `*_typ` failures; 0 Cape).
- `mkdocs build --strict` was requested but **not run** (validate was backgrounded, then this handoff).
- Optional leftover from morphology fill (`temp/handoff/2026-09-11-cape-delport-morphology.md`): 8 Cape slugs still empty Kenmerken.

## Next steps
1. Run `./.venv/bin/mkdocs build --strict` from the repo root. Fix any Cape/new-page failures; do not “fix” the known `--links` set unless the user asks.
2. Report build result. Do not commit or push unless the user asks.
3. If they want type tiles with grains: either add 15 `genus_typ` YAML entries with a representative image, or put member `pollen_keys` on those key outcomes (`@interactive-pollen-key` only with an explicit keys ask).
4. After push: confirm live Buiten EU and Identificatiesleutels Flora regio Kaap (project SoT is GitHub Pages, not local `site/`).

## Artifacts
- `docs/gallerie/gallery-non-eu.md` — Cape gallery
- `docs/keys/flora-regio-kaap/` — key JSON, `taxa-index.json`, `type-members.json`
- `docs/Identificatiesleutels/flora-regio-kaap*.md` — key pages
- `data/pollen.yaml` — Cape taxa SoT
- `scripts/validate_pollen_site.py` — `--rebuild-data --images` already green this session

## Suggested skills
- `@interactive-pollen-key` — only if the user asks to wire type endpoints so images show
- `@update-pollen` — only if adding `genus_typ` YAML + images for those 15 types
