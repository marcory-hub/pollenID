# Handoff: Morph lookalike clustering failed

## Goal
Treat the YAML+keys morph clustering experiment as a **failed** approach for finding LM lookalikes; do not promote its clusters. Prefer the existing review/promote pipeline if lookalike work continues.

## Current state
- Experiment verdict (user): **failure**. Cluster members often do not look alike under LM.
- False-positive examples from `(temp/lookalike_calculation.md)`:
  - Sample decided-pair `acer_platanoides`–`centaurea_cyanus` does **not** look the same; decided-pair distance table is **not** a useful “nearest lookalikes” list.
  - Tight cluster with `taraxacum_typ` / `senecio_aquaticus` / `symphyotrichum_lanceolatum` (shared `tricol*` + `echinaat` + similar mid µm) is **completely different** morphologically in practice.
- Root cause (observed): coarse token bags (aperture family, sculpture tokens like `echinaat`/`reticulaat`, size class/mid) over-merge unrelated taxa; size/path-gate fixes (v3) do not fix sculpture/aperture coarseness.
- Durable runner exists: `(scripts/morph_lookalike_cluster.py)` → `(temp/lookalike_calculation.md)`. Do **not** treat output as lookalike SoT.
- Existing pair pipeline still valid: `(scripts/lookalike_candidates.py)` → `(data/lookalike_review.yaml)` → `(scripts/promote_lookalikes.py)` → YAML `lookalikes`.
- Local review sheets are Markdown under `temp/lookalike-*.md` (converted from HTML). Keys / published lookalike pages unchanged by this experiment.

## Next steps
1. Do **not** promote or triage morph clusters into `data/lookalike_review.yaml` / `data/pollen.yaml` from this report.
2. If lookalike work resumes: use human/true-scale review + `lookalike_candidates` / published confirmed pairs, not agglomerative morph clustering.
3. Optional later: leave `scripts/morph_lookalike_cluster.py` as archival, or delete/stop indexing it if the user wants the experiment removed from the script table.
4. Any new similarity approach needs finer LM traits (and likely images), not only coarse YAML tokens + key path sizes.

## Artifacts
- `temp/lookalike_calculation.md` — failed clustering report (evidence of over-merge; not for promotion)
- `scripts/morph_lookalike_cluster.py` — durable runner that produced the report
- `scripts/lookalike_candidates.py` / `scripts/promote_lookalikes.py` — working lookalike pipeline
- `data/lookalike_review.yaml` / `data/pollen.yaml` lookalikes — SoT for confirmed pairs
- `temp/handoff/2026-08-12-morph-lookalike-clustering-2.md` — prior “still triage” handoff; superseded by this failure verdict

## Suggested skills
- `@update-pollen` — only if continuing confirmed lookalike YAML/page work outside this experiment
- None for further morph-cluster iteration unless the user designs a new method
