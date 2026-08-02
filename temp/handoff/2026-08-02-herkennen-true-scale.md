# Handoff: Herkennen levels + true-scale images

## Goal
Keep building the Herkennen study path (morphology + lookalike diffs + true-scale comparison) aligned with PalynoQuest niveaus, then expand lookalike coverage and optionally Niveau 2 write-ups.

## Current state
- Nav tab `Herkennen` is live in (`mkdocs.yml`) between Gallerie and Willekeurig.
- Pages exist: (`docs/herkennen/_index.md`), Niveau 1/2/3 under (`docs/herkennen/`).
- Niveau 1: 13 taxa with morphology via `pollen()` macros, lookalike diffs for 9, `[to be verified]` lookalikes for Taraxacum / Centaurea cyanus / Tilia / Ranunculus; 13 `### Beelden` true-scale rows via `pollen_img` (`µm × 2.5`).
- Niveau 2: index table only (22 quiz-eligible prioriteit taxa). Niveau 3: scope page linking to Gallerie (no full 272-row list).
- `mkdocs build --strict` was green after Beelden work; changes appear uncommitted on `main` (check `git status` before commit).
- Aggregate types often have empty YAML morphology; pages pull from representatives (e.g. `brassica_napus`, `vicia_sepium` text / `vicia_faba` image).

## Next steps
1. Decide lookalike partners for the four `[to be verified]` Niveau 1 taxa (user-sourced); then add Beelden partners + diff bullets (do not invent).
2. Optionally fill empty aggregate fields in (`data/pollen.yaml`) so Niveau 1 can drop representative fallbacks.
3. When asked: commit Herkennen nav + docs (and any related uncommitted work); do not push unless asked.
4. Later: Niveau 2 morphology/lookalike/Beelden pass (same pattern as Niveau 1).

## Artifacts
- `docs/herkennen/` — study pages (Niveau 1 full; 2/3 index)
- `mkdocs.yml` — Herkennen nav block
- `notes/pollenID/palynoquest-levels.md` — niveau taxon lists (read-only SoT draft)
- `docs/lookalikes/` — source clusters for Niveau 1 diffs
- `scripts/mkdocs_macros.py` — `pollen` / `pollen_img` / `gallery`
- `~/.cursor/plans/herkennen_nav_section_724e9438.plan.md` — nav/structure plan
- `~/.cursor/plans/herkennen_true-scale_images_d51a4b58.plan.md` — Beelden plan

## Suggested skills
- `@scale-images` — if rechecking true-scale rows or monofloral-style anchors
- `@update-pollen-yaml` — fill empty `_typ` morphology / sizes
- `@add-images-information` — if `vicia_sepium` (or other) needs by-taxon images
- `@edit-doc` — Niveau 2 write-ups when scoped
- `@less-tokens` — if next session is mostly small wiring
