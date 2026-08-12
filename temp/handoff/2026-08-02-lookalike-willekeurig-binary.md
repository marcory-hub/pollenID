# Handoff: Lookalike binary quiz in Willekeurig

## Goal
Ship confirmed lookalike pairs (with E/M/D) as a Willekeurig Niveau option: one image, two name choices; keep YAML/manifest pipeline durable and reviewable.

## Current state
- Confirmed lookalike pairs live in (`data/pollen.yaml`) `lookalikes.pairs` (+ optional `groups`); review queue in (`data/lookalike_review.yaml`).
- Manifest (`docs/assets/manifests/lookalike-groups.json`) includes `difficulty` on pairs (27/30 rated; unrated still confirmed: #9 fraxinus↔salix, #22 padus↔serotina, #24 serotina↔rubus).
- Promote/export/manifest scripts carry `difficulty`: (`scripts/promote_lookalikes.py`), (`scripts/export_pollen_json.py`), (`scripts/build_manifests.py`).
- Willekeurig UI: Lookalike is a **Niveau select option** (not a checkbox). Options: Alle / Makkelijk / Matig / Moeilijk in (`docs/naslag/palynoquest.md`); binary MCQ in (`docs/javascripts/palynoquest.js`); cache-bust `?v=2026-08-02-lookalike-binary` in (`mkdocs.yml`).
- Lookalike mode: hides open vraag + sleutel; shows one image from a random side of a pair; exactly two buttons; SRS keyed by `a|b` pair id.
- Brassica type scale fix: (`brassica_typ`) leads with `brassica_napus` image + size (~28.2 µm → 70 px). Laurocerasus face for review: `_3.png`.
- Review Markdown: (`temp/lookalike-all-review.md`) + index (`temp/lookalike-all-index.json`).
- Domain term SoT: Lookalike in (`CONTEXT.md`). Gallery footnote already points at product vs table sense in (`docs/gallerie/gallery-nl-pollen-types.md`).
- No commit requested this stream; manifests under `docs/assets/manifests/` are gitignored and rebuilt in CI.

## Next steps
1. Hard-refresh Willekeurig; spot-check Lookalike Alle/Makkelijk/Matig/Moeilijk (one image, two options, wrong-preview + progress).
2. Close unrated pairs #9 / #22 / #24 (E/M/D or `false`) then re-promote + rebuild manifests if changed.
3. Optional: trim remaining pending shortlist in (`data/lookalike_review.yaml`); align Herkennen / `docs/lookalikes/` pages with final confirmed set.
4. Commit when asked (YAML lookalikes + difficulty, scripts, PalynoQuest UI/JS, mkdocs cache-bust, Herkennen/gallery edits).

## Artifacts
- `data/pollen.yaml` — lookalikes SoT (`pairs` + `difficulty` + `groups`)
- `data/lookalike_review.yaml` — confirmation queue
- `scripts/lookalike_candidates.py` / `scripts/promote_lookalikes.py` / `scripts/build_manifests.py` — pipeline
- `docs/naslag/palynoquest.md` + `docs/javascripts/palynoquest.js` — Willekeurig Lookalike option
- `docs/assets/manifests/lookalike-groups.json` — generated quiz feed (local/CI)
- `temp/lookalike-all-review.md` — true-scale pair review

## Suggested skills
- `@update-pollen-yaml` — edit/confirm lookalike pairs or difficulties in YAML
- `@less-tokens` — small quiz/UI follow-ups
- `@handoff` — refresh this file after the next batch of pair decisions
