# Handoff: Skill entry-point consolidation

## Goal
Keep a short public skill set with clear when→skill routing; next work can use `@update-pollen` / `@interactive-pollen-key` without rediscovering old skill names.

## Current state
- Public skills: `update-pollen`, `interactive-pollen-key`, `grill-me`, `grill-with-docs`, `domain-modeling`, `teach-me`, `handoff`, `cursor-unignore`. Library: `grilling` only.
- Dropped/merged this stream: taxon cluster → `@update-pollen`; `beug-key` OCR rules → `@interactive-pollen-key`; also dropped `read-notes`, `make-skill`, `fix-json`, `project-pitch`, `edit-doc`, `format-table`, `update-readme`, `less-tokens`, and absorbed add/yaml/page/sleutel/vanderham skills.
- Discovery map in (`project-context.mdc`); inventory ADR (`docs/adr/0002-skill-entry-points.md`); note topic table in (`rules-notes-boundary.mdc`); `.cursorignore` has `!notes/`.
- First real `@update-pollen` end-to-end run not yet smoke-tested against `scripts/add_taxon.py`.

## Next steps
1. Spot-check `@update-pollen` on one queued taxon (images or text) through validate.
2. Spot-check `@interactive-pollen-key` OCR/attachment subsection if next key work is from a scan.
3. Optionally sync `notes/` mentions of old skill names in Obsidian (`pid todo.md`, `pid scripts.md`).

## Artifacts
- `.cursor/skills/update-pollen/` — full taxon pipeline skill
- `.cursor/skills/interactive-pollen-key/SKILL.md` — keys + OCR/attachment
- `.cursor/rules/project-context.mdc` — when→skill map + skill hygiene
- `docs/adr/0002-skill-entry-points.md` — entry-point inventory
- `.cursorignore` — `!notes/` allow

## Suggested skills
- `@update-pollen` — next taxon image/metadata work
- `@interactive-pollen-key` — key JSON/page or OCR→Beug
- `@cursor-unignore` — if more paths need Cursor Read access
