---
name: handoff
description: >-
  Compact the current conversation into a handoff document for another agent.
  Use when the user asks for a handoff, session handoff, or to compact context
  for a fresh agent.
argument-hint: What will the next session focus on?
disable-model-invocation: true
---

# Handoff

Write one handoff markdown file so a fresh agent can continue without replaying the chat.

## Output location

1. Ensure `temp/handoff/` exists under the workspace root (create it if missing). `temp/` is gitignored.
2. Write to:
   `temp/handoff/YYYY-MM-DD-<slug>.md`
   - Date: ISO 8601 calendar date (`yyyy-mm-dd`).
   - Slug: kebab-case from the user argument if present; otherwise from the next-session focus; fallback `session`.
   - If the path already exists, append `-2`, `-3`, … before `.md`.
3. After writing, tell the user the **absolute** path to the file. Do not paste the full document unless asked.

## Arguments

If the user passed an argument, treat it as the next session's focus. Bias Goal, Next steps, and Suggested skills toward that focus. Omit chat digressions that do not serve it.

## Document rules

- Do not duplicate content already in specs, plans, ADRs, issues, commits, or diffs. Reference by path or URL.
- Redact secrets: API keys, passwords, tokens, credentials, and unnecessary PII.
- Prefer bullets over prose. Keep the whole file short enough to read in one pass.
- Cite provenance as `(path)` when pointing at repo files.

## Template

Use this structure exactly (keep the headings):

```markdown
# Handoff: <short title>

## Goal
<One or two sentences: what success looks like for this workstream.>

## Current state
- <Factual status bullets only. What exists, what works, what is blocked.>

## Next steps
1. <Ordered, actionable. First item is what the next agent should do first.>

## Artifacts
- `<path-or-URL>` — <why it matters>
(or `None yet.` plus a short **Propose** list if empty; see below.)

## Suggested skills
- `@skill-name` — <when/why the next agent should invoke it>
```

### Artifacts empty

If there are no durable artifacts yet, write `None yet.` then a **Propose** sublist of 1–3 concrete files or docs the next session should create (path + purpose). Prefer existing project conventions over new invention. Do not create those files in the handoff turn unless the user asks.

### Suggested skills

Scan project skills under `.cursor/skills/` (names only; do not invent skills). Recommend only skills that clearly help the next steps. If none apply, write `None.`

## Example

User argument: `finish update-pollen batch for Salvia and sync YAML`

```markdown
# Handoff: Finish Salvia update-pollen batch

## Goal
Complete by-taxon images, YAML fields, and species pages for the remaining Salvia taxa, then validate the site.

## Current state
- `data/pollen.yaml` has partial Salvia entries; images staged under `by-taxon/_todo/`.
- Species pages for some keys still missing Determinatiesleutels sections.

## Next steps
1. Run `scripts/add_taxon.py` (or `@update-pollen`) for the queued slugs.
2. Confirm Dutch names and sizes against source notes; mark gaps `[to be verified]`.
3. Run `validate_pollen_site.py --rebuild-data --images --links`.

## Artifacts
- `data/pollen.yaml` — taxon SoT
- `docs/pollen/species/` — published pages

## Suggested skills
- `@update-pollen` — full taxon pipeline + validate
```
