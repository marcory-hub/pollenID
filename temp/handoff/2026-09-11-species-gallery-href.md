# Handoff: Species gallery image hrefs

## Goal
Species pages on GitHub Pages show pollen images instead of broken-icon alt text.

## Current state
- Live page `https://marcory-hub.github.io/pollenID/pollen/species/brassica_napus/` 404'd images: PNGs exist at `/pollenID/assets/images/by-taxon/brassica_napus/…` (HTTP 200). Hardcoded `../../assets/` from a directory URL resolved to `/pollenID/pollen/assets/` (HTTP 404).
- Renderer now emits `{{ gallery("slug") }}` so MkDocs `normalize_url` yields `../../../assets/…` (same depth as extra JS). Change: (`scripts/render_taxon_pages_from_sot.py`).
- Species markdown is generated and gitignored (`docs/pollen/species/*.md` in `.gitignore`). CI regenerates via (`scripts/build_docs_data.py`) then MkDocs.
- Commit `4dd3d47` `fix gallery images` is on `main` tracking `origin/main`. Working tree clean. Local `mkdocs build --strict` produced correct `src="../../../assets/…"` in `site/pollen/species/brassica_napus/index.html`.
- Live Pages may still be stale until GitHub Actions finishes. `gh` is not authenticated in this environment.

## Next steps
1. Confirm GitHub Actions for `4dd3d47` succeeded, then hard-reload `https://marcory-hub.github.io/pollenID/pollen/species/brassica_napus/` and check img `src` is `../../../assets/…` with images visible.
2. Spot-check another species page with images (e.g. `taraxacum_officinale`) and a gallery page that already used the macro (`docs/gallerie/gallery-nl-common.md`) for no regression.
3. If still broken: inspect built HTML in the Pages artifact / Actions log; do not re-hardcode `../../` in (`scripts/render_taxon_pages_from_sot.py`).

## Artifacts
- `scripts/render_taxon_pages_from_sot.py` — `_gallery_macro`; removed `_static_gallery_html`
- `scripts/mkdocs_macros.py` — `gallery()` / `_resolve_assets_href` (unchanged this session)
- `https://marcory-hub.github.io/pollenID/pollen/species/brassica_napus/` — page that was broken

## Suggested skills
- `@update-pollen` — only if a follow-up is taxon YAML/images rather than this href bug
