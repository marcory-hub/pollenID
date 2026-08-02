# Handoff: Rosaceae Beug-typen herkennen page

## Goal
Keep the Rosaceae learning page accurate for determination training, then optionally fill missing species pages for taxa that already have by-taxon PNGs.

## Current state
- Live page: (`docs/herkennen/rosaceae-beugtypen/_index.md`); nav in (`mkdocs.yml`); linked from (`docs/herkennen/_index.md`).
- Backbone: Beug ch. 20 types (Agrimonia, Potentilla, Rosa, Aruncus, Geum, Sorbus-groep) plus Sanguisorba (13.7 / 25.15) and Filipendula (14.24); Reitsma/Eide linked as cross-keys.
- Galleries use `pollen_img` (true-scale); only taxa with PNGs in tables/galleries; backlog at bottom.
- Validated this session: `validate_pollen_site.py --rebuild-data --images` OK; `mkdocs build --strict` OK.
- Changes appear uncommitted (check `git status`).
- Out of scope still open: family page (`docs/pollen/families/rosaceae.md`) still thin / Fabaceae bleed; missing species pages for PNG-ready slugs.

## Next steps
1. Commit when asked: Rosaceae herkennen page + `mkdocs.yml` + `docs/herkennen/_index.md` (and any rebuilt `docs/data/pollen.json` if dirty).
2. Optional `@add-pollen` / `@pollen-pagina` for PNG-ready keys without pages: `agrimonia_eupatoria`, `agrimonia_odorata`, `potentilla_erecta`, `fragaria_viridis`, `rosa_gallica_officinalis`, `sibbaldia_procumbens`, `cotoneaster_intergerrimus`, `rubus_saxatilis`, `dryas_octopetala`.
3. After pages exist, turn plain italic names on the herkennen page into species links.
4. Separate ask only: clean (`docs/pollen/families/rosaceae.md`); backlog genera without PNGs (*Pyrus*, *Mespilus*, *Alchemilla*, …).

## Artifacts
- `docs/herkennen/rosaceae-beugtypen/_index.md` — learning page
- `mkdocs.yml` — Herkennen nav entry
- `docs/herkennen/_index.md` — overview table link
- `docs/Identificatiesleutels/rosaceae-reitsma.md` / `rosaceae-eide.md` — special keys
- `docs/keys/beug/beug20-tricolporoidatae-str-*.json` — Beug type SoT for section text
- `/Users/md/.cursor/plans/rosaceae_herkennen_page_07e9ebad.plan.md` — implemented plan

## Suggested skills
- `@add-pollen` — wire missing species pages for PNG-ready Rosaceae slugs
- `@pollen-pagina` — Dutch taxon page template
- `@trace-key-paths` — Determinatiesleutels blocks on new species pages
- `@scale-images` — if gallery rows need retuning after size YAML fixes
