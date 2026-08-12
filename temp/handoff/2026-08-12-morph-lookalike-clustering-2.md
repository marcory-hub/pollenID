# Handoff: Morph lookalike clustering

## Goal
Triage LM morph lookalike candidates from the clustering report; decide which pairs/clusters deserve review, without auto-promoting lookalikes.

## Current state
- Durable runner: `(scripts/morph_lookalike_cluster.py)` → `(temp/lookalike_calculation.md)`.
- Report (v3): ~901 clusterable taxa; tight **158** / loose **187**; conflict-masked YAML size notes 34 taxa; **47** with PK path-gate.
- Method v3: species-matched Beug/Eide/Reitsma outcome lines supply mid/interval; dichotomous **PK path-gates** kept separately; `W_SIZE_NONOVERLAP` applies if preferred intervals **or** path-gates are non-overlapping (once). Open path-gates (e.g. 0–35) never become taxon mid.
- Worked correction: `trifolium_pratense` vs `trifolium_repens` distance **3.625**; species **40.0–50.3 (MiW 45.3)** vs **26.3–34.3 (MiW 30.9)**; path_gate **42–50** vs **0–35**; not co-clustered.
- Local review sheets under `temp/` are Markdown (not HTML): `lookalike-review.md`, `lookalike-all-review.md`, `lookalike-gaps-all.md`, `lookalike-fenestraat-taraxacum.md`, `lookalike-prunus-pirus*.md`.
- Matching: exact `pollen_key` only. Keys / YAML / lookalikes docs / notes unchanged by the clusterer.

## Next steps
1. Triage `(temp/lookalike_calculation.md)` §4 ranked tight clusters: drop **low specificity** coarse-sculpt bins; keep high-evidence pairs.
2. Cross-check remaining groups against Beug outcome sizes and path-gates before lookalike review edits.
3. Do not promote clusters into `data/lookalike_review.yaml` / `data/pollen.yaml` unless explicitly asked.

## Artifacts
- `scripts/morph_lookalike_cluster.py` — durable morph clustering
- `temp/lookalike_calculation.md` — clustering report
- `temp/lookalike-*.md` — local true-scale review sheets (converted from HTML)
- `temp/reports/key-path-conflicts.md` — conflict mask source
- `docs/keys/beug/beug22-tricolporatae-ret-trifolium.json` — Beug Trifolium size separation
- `docs/naslag/scripts.md` — script index row for morph clusterer

## Suggested skills
- `@update-pollen` — only if triage leads to YAML morph/size corrections
- `@interactive-pollen-key` — only if user explicitly asks to change key JSON
