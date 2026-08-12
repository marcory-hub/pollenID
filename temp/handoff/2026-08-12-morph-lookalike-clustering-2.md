# Handoff: Morph lookalike clustering

## Goal
Triage LM morph lookalike candidates from the one-shot clustering report; decide which pairs/clusters deserve review or a durable script, without auto-promoting lookalikes.

## Current state
- One-shot morph clustering report (v3) at `(temp/lookalike_calculation.md)`: ~901 clusterable taxa; tight **158** / loose **187** multi-member clusters; conflict-masked YAML size notes 34 taxa; **with PK path-gate** counted in inventory.
- Method v3: species-matched Beug/Eide/Reitsma outcome lines supply mid/interval; dichotomous **PK path-gates** kept separately; `W_SIZE_NONOVERLAP` applies if preferred intervals **or** path-gates are non-overlapping (once). Open path-gates (e.g. 0–35) never become taxon mid.
- Worked correction: `trifolium_pratense` vs `trifolium_repens` distance **3.625**; species **40.0–50.3 (MiW 45.3)** vs **26.3–34.3 (MiW 30.9)**; path_gate **42–50** vs **0–35**; not co-clustered at tight or loose. Evidence includes both non-overlapping key intervals and non-overlapping path-gates.
- Matching: exact `pollen_key` only; no synonym / `*_typ` fill. Keys used as morph attribute sources only (not topology).
- No durable `scripts/` tool added; throwaway runner was `/tmp/morph_lookalike_cluster.py`. Keys / YAML / lookalikes docs / notes unchanged.

## Next steps
1. Triage `(temp/lookalike_calculation.md)` §4 ranked tight clusters: drop **low specificity** coarse-sculpt bins; keep high-evidence pairs (e.g. Acer campestre/platanoides).
2. Cross-check remaining ranked tight/loose groups against Beug (or specialty) outcome sizes **and** path-gates before any lookalike review edits.
3. Decide whether to keep the report as triage-only or ask for a durable re-runnable script under `scripts/` (only if re-runs are needed).
4. Do not promote clusters into `data/lookalike_review.yaml` / `data/pollen.yaml` lookalikes unless explicitly asked.

## Artifacts
- `temp/lookalike_calculation.md` — morph clustering report (v3 method, cuts, clusters, flags)
- `temp/reports/key-path-conflicts.md` — conflict mask source (YAML/analytic size conflicts)
- `docs/keys/beug/beug22-tricolporatae-ret-trifolium.json` — Beug size separation for Trifolium types
- `data/lookalike_review.yaml` / `data/pollen.yaml` lookalikes — already_decided tags only (read-only this pass)
- Cursor plan `lookalike_size_recalculation_6755b2db.plan.md` — v3 dual size-model re-run

## Suggested skills
- `@update-pollen` — only if triage leads to YAML morph/size corrections
- `@interactive-pollen-key` — only if user explicitly asks to change key JSON
- None for re-reading the report alone
