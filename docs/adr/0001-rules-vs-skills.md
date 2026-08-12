# Rules vs skills

Agent guidance is split by cost and trigger. `.cursor/rules/` holds standing invariants (always-on or file-scoped constraints you should not have to restate). `.cursor/skills/` holds multi-step workflows invoked by name (`@update-pollen`, and so on). Thin “run the skill” rules and a second always-on map file (`project-reference.mdc`) were rejected to cut token load and avoid drift; map and “do not suggest” guardrails live in one `project-context.mdc`. Entry-point inventory: `docs/adr/0002-skill-entry-points.md`.
