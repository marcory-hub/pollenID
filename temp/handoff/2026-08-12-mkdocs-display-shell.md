# Handoff: MkDocs display shell refactor

## Goal
Keep MkDocs Material + GitHub Pages as the site shell; taxon display reads split JSON (not dual YAML/macros paths), with build-generated uncommitted thin leaves and a shared JS core.

## Current state
- ADR accepted: `docs/adr/0003-mkdocs-display-shell.md`.
- `build_docs_data.py`: export slim `docs/data/pollen.json`, per-slug `docs/data/taxa/<slug>.json` (links), regenerate species leaves, then manifests.
- `data/species_page_slugs.txt`: committed slug manifest (1524 slugs) for leaf generation after untrack.
- Species MD gitignored (`docs/pollen/species/*.md`; `_index.md` committed). CI regenerates leaves before `mkdocs build`.
- Macros (`scripts/mkdocs_macros.py`) read display JSON for curated gallerie/herkennen only.
- `docs/javascripts/pid-core.js` shared by pollentabel, Kerkvliet, PalynoQuest.
- `mkdocs build --strict` green locally after full rebuild.

## Next steps
1. When adding a new species leaf: append slug to `data/species_page_slugs.txt`, then `@update-pollen` / `build_docs_data.py`.
2. Optional: dynamic JS bootloader (load entrypoints only when mount present); not required for ADR closure.
3. `--links` validator still flags typ/stub taxa without atlas URLs (pre-existing; not introduced by split).

## Artifacts
- `docs/adr/0003-mkdocs-display-shell.md` — accepted stack decision
- `data/species_page_slugs.txt` — leaf slug manifest
- `docs/javascripts/pid-core.js` — shared client core
- `scripts/export_pollen_json.py`, `scripts/render_taxon_pages_from_sot.py`, `scripts/mkdocs_macros.py` — display pipeline

## Suggested skills
- `@update-pollen` — taxon YAML/images + slug manifest + validate
- `@interactive-pollen-key` — key JSON / pollentabel contract changes only
