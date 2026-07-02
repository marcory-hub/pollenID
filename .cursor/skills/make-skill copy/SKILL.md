---
name: make-skill
description: >-
  Create or update Cursor Agent Skills with proper structure and repo placement
  for training-program workflows. Use when the user asks to make a skill, add a
  workflow skill, convert repeated prompts into .cursor/skills/, or @make-skill.
disable-model-invocation: true
---

# Make a skill

Project authoring guide. For Cursor-wide mechanics (scripts, personal skills, AskQuestion), see `~/.cursor/skills-cursor/create-skill/SKILL.md`. Walk the review checklist below before calling the skill done.

## Where things go

| Add to | When |
| :--- | :--- |
| `.cursor/skills/` | Judgment, format, read order (composable) |
| `.cursor/rules/` | Always-on invariants and style pointers |

Never create skills in `~/.cursor/skills-cursor/` (Cursor internal).

**This repo:** program prose style → `sports-communication.mdc` + `docs/sports-communication-digest.md`; chat tone → `interaction-style.mdc`; facts → `program/notes/`.

## Process

1. **Gather** (ask if unclear): task/domain, triggers, reference paths (`docs/repo-map.md`, `knowledge/`, digest).
2. **Draft:** `.cursor/skills/<name>/SKILL.md`; add `REFERENCE.md` only if body would exceed 100 lines.
3. **Review:** walk the checklist below with the user.

## Folder layout

```
skill-name/
├── SKILL.md        # required
├── REFERENCE.md    # optional; long tables or rare domain detail
└── EXAMPLES.md     # optional; sample prompts/outputs
```

## Description (discovery)

YAML `description` is what Cursor uses to pick a skill. Max ~1024 chars. Third person.

- Sentence 1: what it does
- Sentence 2: `Use when ...` with concrete keywords

**Good:** `Editor read-through for clarity and flow. Use when @editorial-review, proofread, or final check on a session .md under program/.`

**Good (writing):** Style companion while drafting; see `sports-communication` rule on `program/**`.

**Bad:** `Helps with writing.`

No stale word counts or dates in YAML; point to `docs/repo-map.md` or README.

Default `disable-model-invocation: true` unless the skill should auto-load from ambient context.

## SKILL.md template

```markdown
---
name: skill-name
description: What it does. Use when [triggers].
disable-model-invocation: true
---

# Skill name

## Quick start
[Minimal path: one command or 3-step checklist]

## Workflow
[Numbered steps; link program paths for detail]

## Out of scope
[Point to other skills or rules]
```

## Body rules

- Under 100 lines in `SKILL.md`
- One SoT per topic; no duplicate digest or rule content in skills
- Factual claims: point to `program/notes/` or sources, not the digest
- Verbatim user copy: use exact wording when the user supplies skill text

## Review checklist

- [ ] Description has `Use when` triggers
- [ ] `SKILL.md` under 100 lines
- [ ] No time-sensitive pins in YAML
- [ ] References one level deep (no nested doc chains)
- [ ] Overlap with existing skill resolved or cross-linked
- [ ] Deprecated aliases deleted

## Anti-patterns

- Long essays competing with rules
- Duplicating digest checklists inside skills
- Skill that only repeats a rule verbatim
