# Handoff: Agent rules vs skills cleanup

## Goal
Keep a lean agent guidance stack: standing invariants in rules, multi-step work in skills; no thin trigger rules or duplicate always-on maps.

## Current state
- Grill decisions applied; ADR written at `docs/adr/0001-rules-vs-skills.md`.
- Always-on rules: `interaction-style.mdc`, `project-context.mdc` (merged map + guardrails), `anti-hallucination-verification.mdc`, `rules-notes-boundary.mdc`.
- File-scoped: `python-environment.mdc`, `wetenschapscommunicatie.mdc`.
- Deleted: `project-reference.mdc`, `add-pollen.mdc`, `add-images-information.mdc`.
- trainingPRG leftovers stripped earlier in session from anti-hallucination / interaction-style / wetenschapscommunicatie.
- Changes are local only; not committed.

## Next steps
1. Review the six remaining rule files and ADR for any leftover cross-project wording.
2. Commit when the user asks (rules + ADR only unless they expand scope).
3. Do not reintroduce thin “run the skill” `.mdc` triggers; invoke `@add-pollen` / `@add-images-information` by name.

## Artifacts
- `docs/adr/0001-rules-vs-skills.md` — decision record
- `.cursor/rules/project-context.mdc` — single map + hygiene guardrails
- `.cursor/rules/rules-notes-boundary.mdc` — stack order + notes/ boundary

## Suggested skills
- `@domain-modeling` — if further process decisions need ADR/glossary updates
- `@grill-with-docs` — if the next session reopens the rules/skills boundary
