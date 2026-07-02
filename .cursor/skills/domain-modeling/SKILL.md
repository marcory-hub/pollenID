---
name: domain-modeling
description: >-
  Build and sharpen the project domain model: CONTEXT.md glossary and ADRs.
  Draft in chat; save after user approve. Use when grill-with-docs is active,
  when pinning terminology, recording an architectural decision, or @domain-modeling.
---

# Domain modeling

Actively sharpen ubiquitous language and record hard decisions as they crystallise during design. Read existing `CONTEXT.md` before adding terms. This is not `notes/` (read-only SoT) and not a dump of `knowledge/` tables.

## File layout (single context)

```
/
├── CONTEXT.md
└── docs/
    └── adr/
        └── 0001-slug.md
```

Create `CONTEXT.md` and `docs/adr/` lazily on first **approve**. If `CONTEXT-MAP.md` exists at repo root, read [context-format.md](context-format.md) for multi-context layout.

## Approve gate

**No write** to `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` before the user says **approve** for that item.

1. When a term or ADR is settled, show the draft in chat (glossary block or ADR body).
2. User edits or approves.
3. On **approve**, write or patch the file on disk. Create parent directories if needed.

During a grill, one item per approve is fine; do not batch silent writes at the end.

## During the session

**Challenge glossary conflicts.** If the user contradicts `CONTEXT.md`, call it out.

**Sharpen fuzzy terms.** Propose one canonical term; list loose synonyms under `_Avoid_`.

**Stress-test with scenarios.** Invent edge cases that force precise boundaries between concepts.

**Cross-check the codebase.** Surface contradictions between stated rules and code.

**Draft glossary updates.** When a term is settled, show the `CONTEXT.md` addition or edit in chat using [context-format.md](context-format.md). Glossary only: no implementation detail, specs, or scratch notes. Write on **approve** only.

**Offer ADRs sparingly.** Only when all three hold: hard to reverse, surprising without context, real trade-off. Show draft in chat using [ADR-format.md](ADR-format.md); write on **approve** only.
