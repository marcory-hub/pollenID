---
name: fix-json
description: >-
  Repairs JSON syntax and structure only (parse errors, brackets, commas,
  quotes, escaping). Does not alter the meaning or wording inside string values.
  Uses the smallest possible read/edit surface and minimal diffs. Use when the
  user asks to fix JSON, validate JSON, or make JSON parse; or when they say to
  leave text/content unchanged, syntax-only, or structure-only.
---

# fix-json

## Hard rule

**Do not change the characters inside JSON string values** except when required to make the file valid JSON (see “Allowed string edits” below).

Treat every `"…"` value as the user’s authoritative copy: plant names, Dutch prose, Markdown inside strings, URLs, file paths, and `[to be verified]` markers stay exactly as written unless the user explicitly asks for copy or taxonomy edits.

## Allowed edits (syntax and structure)

- Add/remove/move: `{` `}` `[` `]` `,` between properties or array elements
- Inside a string value, change characters **only** when the file is not valid JSON without it (e.g. escape an embedded `"` or `\`). A two-character sequence like `/n` is valid JSON; turning it into `\n` changes displayed text → **out of scope** unless the user allows content fixes.
- Normalize indentation and trailing newlines if the project expects it (optional; ask if unsure)
- Remove duplicate keys if the parser rejects them (keep the first or ask; document which)

## Forbidden unless the user explicitly requests it

- Spelling, grammar, or botanical corrections inside strings
- “Improving” Markdown links, species names, or family names
- Renaming keys (`label` → `Label`, etc.) unless the schema requires it
- Changing numbers, booleans, or `null`
- Pretty-printing that reorders keys if order matters to the user or tooling

## Workflow

1. Run `python3 -m json.tool <file>` (or project equivalent) and capture the error line/column.
2. Fix the **minimum** structural change that resolves the error.
3. Re-run validation until exit code 0.
4. If a string contains raw newlines or unescaped quotes that break JSON, escape or split only as much as needed for validity; do not rewrite the prose.

## Token economy (agent behavior)

- Read only the region around the parser error (plus small context) unless the file is tiny or errors are scattered.
- Apply **surgical patches** (one comma, one brace, one escape). Do not rewrite or reformat the whole file unless the user asks.
- Skip optional pretty-print, key reordering, and “while we’re here” cleanups.
- Keep the chat reply short: what broke, what changed (line or property), validation result.

## When the user wants copy edits too

They must say so explicitly, e.g. “fix JSON **and** correct spelling in labels” or “typo pass on Dutch text allowed.”

## Suggested user phrasing (paste next time)

- “Fix JSON syntax only; **do not change any string contents**.”
- “Make this file valid JSON; **leave all text inside quotes exactly as-is**.”
- “Structure/errors only; **no edits to botanical or Dutch wording**.”
- “Run `json.tool` and fix delimiters/commas; **verbatim strings**.”

If they use **@fix-json** or mention this skill, apply the same constraints.
