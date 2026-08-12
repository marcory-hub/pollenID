# Handoff: Herkennen naam-MCQ (niveau 1/2/3)

## Goal
On Herkennen niveau pages: one pollen image with four name choices. Kenmerken-drill stays only on Pollenkenmerken. Drop Willekeurig from nav (keep the file). Verify only via push → Actions → Pages.

## Current state
- Grill decisions locked (see Artifacts prompt summary below); no implementation of the naam-MCQ switch yet.
- `Exporteer verwarringen` button removed from `(docs/naslag/palynoquest.md)` (uncommitted unless already saved).
- Live niveau-1 works as kenmerken-drill (`0/13` taxa); niveau-2 falls back to the same 13 and quizzes the wrong pool (`Kenmerken (overige pollen): 0/13`).
- Only 20 taxa have `controlled` codes (all rank 1–20); 13 of those have images. Numeric levels map to kenmerken-drill since commit `10e4bb0`; name-MCQ path still exists in JS but is unreachable.
- Image→slug preference + kenmerken force + cache-bust `?v=2026-08-12-willekeurig-pool` already in `(docs/javascripts/palynoquest.js)` / `(mkdocs.yml)` from the earlier pool fix.
- Site check rule: no local `mkdocs serve` as SoT (`project-context.mdc` §4b).

## Next steps
1. Implement the locked design: restore numeric levels as name-MCQ; pools from `pollen.json` (tier 1 = rank ≤20, tier 2 = rank >20, tier 3 = all with images); distractors from morph-neighbours JSON.
2. Extend `(scripts/morph_lookalike_cluster.py)` with JSON neighbour output; wire into `(scripts/build_docs_data.py)`; measure CI runtime first.
3. Retarget `(docs/herkennen/niveau-{1,2,3}-*/_index.md)` locks to `1`/`2`/`3`; drop Willekeurig from `(mkdocs.yml)` nav; bump `palynoquest.js` cache-bust; fix niveau-2 raw-slug link text.
4. Push → Actions → Pages; spot-check live niveau 1/2/3, Pollenkenmerken, Lookalikes.

## Artifacts
- `(docs/javascripts/palynoquest.js)` — quiz logic; reusable: `buildMcq`, wrongpreview, Leitner weights
- `(docs/herkennen/niveau-*-*/_index.md)` — locked embeds to retarget
- `(scripts/morph_lookalike_cluster.py)` — morph distance; report-only today (`temp/lookalike_calculation.md`)
- `(docs/naslag/palynoquest.md)` — keep on disk; remove nav row only
- Grill prompt (chat, not yet a separate file): Herkennen naam-MCQ steps/verification as drafted in the prior turn

## Suggested skills
- None for the JS/manifest work itself.
- `@grill-with-docs` — only if tier rules or distractor source need reopening.
- `@handoff` — after the Pages spot-check, if work continues.
