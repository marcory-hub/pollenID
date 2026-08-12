# Handoff: Herkennen name-MCQ + mode contract

## Goal
Ship name-MCQ on niveau 1/2/3 (image + 4 names), keep kenmerken/lookalike intact, and leave a durable mode contract so agents do not coerce numeric locks back into kenmerken.

## Current state
- Name-MCQ implemented: locks `1`/`2`/`3` on niveau pages; pools 13 / 26 / 441 from `learning_priority_rank` + images (`docs/data/pollen.json`).
- Distractors from `docs/assets/manifests/morph-neighbours.json` (build via `scripts/morph_lookalike_cluster.py`, ~7 s; wired in `scripts/build_docs_data.py`; gitignored like other manifests).
- Confusion export kept (lookalike only).
- Willekeurig removed from `nav`; page remains at `docs/naslag/palynoquest.md`.
- Contract SoT in docs: `docs/naslag/palynoquest-modes.md` + ADR `docs/adr/0004-palynoquest-mode-locks.md`. Rules/skills only point and require a read (`project-context.mdc`; `@update-pollen` / `@domain-modeling`; no `@palynoquest` skill).
- Local verify done: `build_docs_data.py`, `validate_pollen_site.py` exit 0, `mkdocs build --strict`, `node --check` on `palynoquest.js`.
- Not done: commit, push, live Pages check.

## Next steps
1. Commit the name-MCQ + contract docs changes (user must ask for commit).
2. Push → wait for GitHub Actions → verify live: niveau 1/2/3 = beeld + 4 namen; Pollenkenmerken = kenmerkenstappen; Lookalikes unchanged; Willekeurig absent from nav but URL works.
3. On any further PalynoQuest edit: read `docs/naslag/palynoquest-modes.md` first; never map `1`/`2`/`3` to `kenmerkenMode`.

## Artifacts
- `docs/naslag/palynoquest-modes.md` — mode/lock/pool contract (SoT for agents)
- `docs/adr/0004-palynoquest-mode-locks.md` — accepted decision
- `docs/javascripts/palynoquest.js` — name pool, morph distractors, parseLevelValue
- `scripts/morph_lookalike_cluster.py` — morph-neighbours JSON export
- `docs/herkennen/niveau-{1,2,3}-*/_index.md` — locks `1`/`2`/`3`
- `mkdocs.yml` — nav + `?v=2026-08-12-name-mcq`

## Suggested skills
- None. (Mode contract is docs-only; `@update-pollen` only if taxon YAML/images change; `@domain-modeling` only if revising ADR 0004 after approve.)
