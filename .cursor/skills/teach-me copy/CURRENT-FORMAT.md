# CURRENT.md format

Single place to resume teaching without branching chats.

## Template

```md
# Teaching queue

**Topic:** {one line}

**Current:** {beat index} — {beat title}

## Beats

- [x] 1. {done}
- [ ] 2. {active or next}
- [ ] 3. {upcoming}

## Parked

- {user question deferred to a future beat}
```

## Rules

- One concept per beat line (verb + noun, e.g. "manifest routes extraction").
- Check off beats only after user says `next` or passes the check.
- `Parked` holds multi-part questions split across sessions; promote to beats when scheduled.
- Keep ≤10 beats per topic; start a new topic block when the list grows.

## Resume

New chat: `@teach-me resume` reads this file and continues at `Current`.
