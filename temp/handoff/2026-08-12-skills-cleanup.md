# Handoff: Skills cleanup follow-through

## Goal
Finish optional skills consolidation after the leftover/token pass, or move on knowing `.cursor/skills/` is pollenID-scoped and under 100 lines per `SKILL.md`.

## Current state
- Foreign-project leftovers removed from teach-me formats, make-skill, less-tokens, domain-modeling, handoff (`GV2`, Colab, flash, `knowledge/`, donor-repo, phantom commands).
- Overlaps clarified: add-pollen modes kept; grill-me now loads grilling; update-pollen-yaml schema in `REFERENCE.md`; pollen-pagina points at `calluna_vulgaris.md`.
- All `.cursor/skills/*/SKILL.md` ≤100 lines; edit-doc name fixed; YAML stub uses `family_latin`.
- Optional items not done: drop handoff, further slim update-readme, merge add-images-information into add-pollen.

## Next steps
1. Decide optional merges (handoff keep/drop; add-images into add-pollen) with the user before editing again.
2. If merging: update `project-context.mdc` skill pointer table and description triggers in one pass.
3. Spot-check one workflow skill (@add-pollen or @trace-key-paths) in a real task to confirm instructions still match `scripts/add_taxon.py` / `extract_key_paths.py`.

## Artifacts
- `.cursor/skills/` — updated skill set
- `.cursor/skills/update-pollen-yaml/REFERENCE.md` — schema/helpers split out of SKILL.md
- `docs/adr/0001-rules-vs-skills.md` — rules vs skills decision (unchanged this session)

## Suggested skills
- `@make-skill` — further skill edits or merges
- `@less-tokens` — if the next session is a long audit pass
