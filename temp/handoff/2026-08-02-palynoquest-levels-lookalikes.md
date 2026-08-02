# Handoff: PalynoQuest levels + lookalike clusters

## Goal
Keep building a stepwise honey-pollen recognition trainer: levels and SRS are live; next is a confusable-pairs mode fed by lookalike groups, plus filling gaps (images, unmatched prio ranks).

## Current state
- PalynoQuest levels + Leitner SRS shipped in (`docs/naslag/palynoquest.md`, `docs/javascripts/palynoquest.js`); level/progress in `localStorage` (`pid_pq_level`, `pid_pq_progress`).
- Level 1 = taxa with `monofloral_honey_page` in `docs/data/pollen.json`; Level 2 = + `learning_priority_rank` from YAML; Level 3 = full quiz pool.
- `learning_priority_rank` set on 74 taxa in (`data/pollen.yaml`) from (`notes/pollenID/prio pollen.md`); skipped #43 Serratula, #48 Anchusa (no genus key), #57 Eleagnaceae (no family key).
- Pool sizes at last check: L1 ~73 images / 10 taxa; L2 ~238 / 41; L3 ~1274 / 272 (quiz items still key-wired only via `scripts/build_manifests.py`).
- Lookalike “Honingcluster (NL)” added under (`docs/lookalikes/_index.md`): Acer/Prunus/Malus/Robinia, Rubus/vogelkers, Trifolium/Melilotus/Aesculus, Raphanus/Brassica/Sinapis/Ligustrum.
- Confusable-pairs trainer (plan option 3) still deferred: needs explicit `pollen_key` lists per lookalike group.
- `validate_pollen_site.py --rebuild-data` was OK after the levels work; lookalike pages not re-validated in that run.
- No commit made this session unless user did so separately.

## Next steps
1. Ask user for `pollen_key` lists per lookalike group (start with the four Honingcluster pages), then add `docs/assets/manifests/lookalike-groups.json` + a “Verwarring” mode in `palynoquest.js`.
2. Optionally expand Level 1 coverage: more monofloral taxa need quiz-eligible images (key/Kerkvliet wiring), not only `monofloral_honey_page`.
3. Resolve unmatched prio ranks (Anchusa, Eleagnaceae) if user picks a slug; add *Prunus serotina* by-taxon images when available.
4. Commit when asked: YAML ranks, export JSON, PalynoQuest UI/JS, lookalike pages, schema/export script tweaks.

## Artifacts
- `docs/javascripts/palynoquest.js` — levels, pool filter, weighted SRS, MCQ in-pool distractors
- `docs/naslag/palynoquest.md` — niveau selector + progress line
- `data/pollen.yaml` — `learning_priority_rank` SoT
- `scripts/export_pollen_json.py` / `scripts/normalize_pollen_yaml_schema.py` — field export + preserve
- `docs/lookalikes/` — new/updated NL lookalike clusters
- `/Users/md/.cursor/plans/palynoquest_stepwise_learning_tiers_ca2c6284.plan.md` — original plan (option 3 deferred section)

## Suggested skills
- `@update-pollen-yaml` — fill ranks / Anchusa–Eleagnaceae slug decisions
- `@add-images-information` or `@add-pollen` — *Prunus serotina* images + YAML when screenshots land
- `@scale-images` — true-scale lookalike galleries if user wants Lindehoning-aligned rows
- `@less-tokens` — if next session is mostly wiring lookalike JSON + small JS
