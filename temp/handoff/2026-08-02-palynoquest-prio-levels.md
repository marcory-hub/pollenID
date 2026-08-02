# Handoff: PalynoQuest level naming (prio, not monofloral)

## Goal
Keep PalynoQuest tiers labeled and filtered as common-in-NL-honey priority pollen, not monofloral honey pages; commit when asked and optionally tighten Level 1 rank cutoff.

## Current state
- Uncommitted: PalynoQuest levels no longer use `monofloral_honey_page` for pools.
- Level 1: `learning_priority_rank <= 20` (“Vaak in NL-honing”); Level 2: any rank (“Alle prioriteit”); Level 3: full quiz pool.
- Approx. quiz pools last checked: L1 ~13 taxa / 65 images; L2 ~35 / 196; L3 ~272 / 1274.
- `monofloral_honey_page` still exists in (`docs/data/pollen.json`) for key Latin→honey-page links only (~18 taxa from `docs/monoflorale-honing-pollen/`).
- Also uncommitted: (`.cursor/rules/project-context.mdc`) `--strict`/CI path guardrails in section 4b.
- Deploy fix `737683d` already on `origin/main`; these level/label edits are not pushed.

## Next steps
1. Confirm with user whether `LEVEL1_MAX_RANK = 20` in (`docs/javascripts/palynoquest.js`) should be tighter (e.g. 10).
2. Commit when asked: `palynoquest.md`, `palynoquest.js`, `mkdocs.yml` cache-bust (`?v=2026-08-02-levels-prio`), and optionally `project-context.mdc`.
3. After push, hard-refresh Willekeurig / PalynoQuest (script cache-bust) and spot-check niveau counts.
4. Deferred: confusable-pairs trainer still needs lookalike `pollen_key` lists.

## Artifacts
- `docs/javascripts/palynoquest.js` — `itemInLevel` / `LEVEL1_MAX_RANK` / progress labels
- `docs/naslag/palynoquest.md` — niveau `<select>` labels
- `mkdocs.yml` — `palynoquest.js?v=2026-08-02-levels-prio`
- `.cursor/rules/project-context.mdc` — uncommitted CI/`--strict` notes
- `notes/pollenID/prio pollen.md` — SoT for `learning_priority_rank` (read-only)
- `temp/handoff/2026-08-02-ci-strict-rules.md` — prior deploy/rules handoff

## Suggested skills
- None.
