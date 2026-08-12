# Handoff: Morph lookalike clustering

## Goal
One-shot hierarchical clustering of taxa with near-identical LM morph (YAML + all keys as attribute sources), write `temp/lookalike_calculation.md`, then stop for human review. No site/YAML/key mutations.

## Current state
- Grill complete (`@grill-with-docs`); decisions locked; copy-paste plan-mode prompt delivered in chat (not saved to disk).
- Distinct from key-path **conflicts** (same taxon, disagreeing claims) and from key-**topology** lookalike signals.
- Existing pair pipeline still valid: `(scripts/lookalike_candidates.py)` → `(data/lookalike_review.yaml)` → promote; this pass does **not** feed it automatically.
- Conflict mask ready: `(temp/reports/key-path-conflicts.md)`; path helper `(scripts/extract_key_paths.py)`.
- Target artifact **not written yet**: `temp/lookalike_calculation.md`.
- `requirements.txt` has no numpy/scipy/sklearn; prefer pure-Python one-shot.

## Next steps
1. Paste the plan-mode prompt from the grill session (or reconstruct from decisions below); **plan, then execute** after approval.
2. Build morph feature bags (exact `pollen_key`); mask conflicted dimensions; agglomerative cluster; two cuts (tight / looser).
3. Write only `temp/lookalike_calculation.md`; summarize cluster counts; do not promote lookalikes or add a durable script unless asked.
4. Optional: if result is useful, later promote to `scripts/` and/or merge candidates into `lookalike_review.yaml`.

### Locked decisions (brief)
- Sources: `data/pollen.yaml` + all `docs/keys/**`; conflict report as unreliability mask.
- Tight cut: same aperture/Beug-class family; prefer Kerkvliet size class + midpoint ≤~5 µm; sculpture/shape when both filled.
- Emphasize clusters with ≥1 ranked taxon; exact slug match; species↔`*_typ` → Human review; tag `already_decided` from review/YAML.
- Non-goals: no edits to keys, YAML, `docs/lookalikes/`, review YAML, notes; no auto-confirm; no topology similarity.

## Artifacts
- None yet. (`temp/lookalike_calculation.md` pending)
- **Propose:** `temp/lookalike_calculation.md` — clustering method, cuts, evidence, limits
- Related: `(temp/reports/key-path-conflicts.md)`, `(temp/handoff/2026-08-12-key-path-conflicts.md)`, `(data/lookalike_review.yaml)`, `(CONTEXT.md)` Lookalike term

## Suggested skills
- None for the one-shot analysis itself.
- `@domain-modeling` — only if pinning “morph cluster” vs Lookalike in `CONTEXT.md` after user **approve**
- `@update-pollen` / `@interactive-pollen-key` — only if a later triage asks for YAML or key edits
