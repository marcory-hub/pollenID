---
name: cursor-unignore
description: Sync .cursorignore negation patterns with .gitignore by discovering gitignored paths the codebase actually references. Use when updating .gitignore, fixing Cursor access, unignore, cursorignore, or @cursor-unignore.
---

# Cursor unignore

Cursor honors `.gitignore` and built-in ignores. Re-include agent-needed paths with `!` in `.cursorignore` so Agent Read / indexing can see them. [Docs](https://cursor.com/docs/reference/ignore-file).

**Every run:** derive candidates from this repo — never copy patterns from memory or other projects.

**Write target:** `.cursorignore` only. Never edit `.gitignore` or nested gitignores.

## Workflow

1. **Read** root `.gitignore`, `.cursorignore`, and any nested `.gitignore` files.
2. **Discover demand** — search the codebase for paths/rules/skills/README/scripts that reference locations under gitignore:
   - Grep for directory names from `.gitignore` and phrases like `gitignored`, `cursorignore`, `Read tool`.
   - List on-disk children of ignored parents (`notes/`, `data/raw/`, etc.).
   - Prefer the **smallest written path** that satisfies references (e.g. `temp/handoff/`, not all of `temp/`). Un-ignore a parent tree only if the user explicitly approves.
   - In-repo references only for automatic sync. Paths named only in chat need an explicit user ask (or a new skill/rule that documents demand) before writing a `!` pattern.
3. **Filter** candidates:

| Policy | Examples |
| :--- | :--- |
| Hard veto (never `!`) | Secrets: `.env`, `.env.*`, `*credentials*`, `*secret*`, `*.pem`, `*.key`. Dependencies: `.venv/`, `node_modules/`, `vendor/`. Caches / tooling: `__pycache__/`, `.*_cache/`, `.pytest_cache/`, `.mypy_cache/`. OS / IDE / build: `.DS_Store`, `.vscode/`, `dist/`, `build/`, `*.o` |
| Ask first | Large binaries / media (`*.pdf`, archives, images) — even with clear in-repo demand or Cursor built-in ignore on that extension |

4. **Diff** filtered candidates against existing `.cursorignore` negations; **add only** missing entries. Do not remove stale `!` patterns unless the user explicitly asks to prune.
5. **Write patterns** — parent before child; directory patterns end with `/`:

```cursorignore
parent/*
!parent/needed/
!parent/needed/**
```

For media/extensions blocked by Cursor **default** ignores, do **not** auto-add `!path/**/*.ext`. Ask the user first; only then add explicit per-extension negations.

6. **Verify** — `git check-ignore -v <sample-file>` (still ignored by git) then Agent Read on one sample per new block.
7. **Format** — one short comment line per pattern block only; no file header, syntax notes, or policy tables.

```cursorignore
# notes/pollenID
notes/*
!notes/pollenID/
!notes/pollenID/**
```

## Limits

- Scope is Agent Read / indexing only. `.cursorignore` does not block terminal/MCP reads.
- Negation fails if a parent dir is excluded with `*` — un-ignore each level explicitly.
- When demand is unclear, ask the user before un-ignoring broad trees or binaries.
