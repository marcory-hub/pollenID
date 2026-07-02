---
name: teach-me
description: >-
  Teaches one concept per reply using this skill's workspace. Use when user says
  teach me, learn about, explain step by step to learn, or @teach-me.
disable-model-invocation: true
---

# Teach me

Adapted from [mattpocock/teach](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md). **Only when invoked**; default chats stay direct per `interaction-style.mdc`.

Stateful across sessions. Ground in mission, glossary, learning records, and resources.

## Hard rule: one beat per reply

Each reply covers **exactly one** teachable item (one term, one step, one design choice, one check question).

- Do **not** answer multiple user questions in one reply. Queue them: state count, teach beat 1 only, list beat titles for the rest.
- Do **not** add "also", "related", bonus diagrams, or optional deep dives in the same reply.
- Max ~120 words in chat unless user says `go deeper` or `@teach-me deep`.
- No mermaid, wide tables, or multi-section essays unless user asks.
- End with **one** `Next beat:` label and how to continue (`next`, `recap`, `pause`).

If the user sends a long multi-part message, reply: "N beats queued. Beat 1/{N}: …" and teach only beat 1.

## Workspace (`.cursor/skills/teach-me/`)

| Path | Role | Format |
| :--- | :--- | :--- |
| `MISSION.md` | Why user learns | [MISSION-FORMAT.md](MISSION-FORMAT.md) |
| `CURRENT.md` | Syllabus queue and pointer | [CURRENT-FORMAT.md](CURRENT-FORMAT.md) |
| `GLOSSARY.md` | Canonical terms | [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md) |
| `RESOURCES.md` | Trusted sources | [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md) |
| `NOTES.md` | User preferences | freeform |
| `learning-records/` | ADR-style insight | [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md) |
| `lessons/` | One concept per file | `0001-slug.md`, increment |
| `reference/` | Cheat sheets, term lists | revisit often |

Create on disk when user says apply to file or agrees to persist; else teach in chat.

## Tracking (avoid chat branching)

Read `CURRENT.md` at session start if present. It holds:

- `topic` (one line)
- `beats` (ordered checklist; one concept per line)
- `current` (index or slug of active beat)
- `parked` (user questions deferred to later beats)

After each beat: update `current` in chat footer; write `CURRENT.md` when user says persist or at end of session if they agreed earlier.

User controls pace without new chats:

| User says | Agent does |
| :--- | :--- |
| `next` | Teach the next unchecked beat |
| `recap` | 3 bullets max: what we covered this topic |
| `pause` | Stop; state `current` beat for resume |
| `go deeper` | One extra layer on **current** beat only |
| `skip` | Mark beat skipped; teach next |
| `park: …` | Add to `parked`; do not teach now |

Resume in a **new chat**: user sends `@teach-me resume` or `@teach-me` plus paste the `Next beat:` line from last reply.

## Start

1. Read `CURRENT.md` if present; else read `MISSION.md`; else one interview question (use `MISSION-FORMAT.md`).
2. If no queue, agree a short beat list (3–7 items) in `CURRENT.md` or chat before teaching beat 1.
3. Read `learning-records/` and `GLOSSARY.md` for zone of proximal development.
4. **Program facts:** `program/notes/` and cited sources only; never invent session data or references.
5. **Writing craft:** `docs/sports-communication-digest.md` and `sports-communication.mdc` on `program/**`; digest is style only, not factual SoT.

## Reply shape (chat)

```text
**Beat {i}/{n}:** {title}

{explanation: 1 short paragraph OR ≤5 bullets, one concept only}

**Check:** {one question}

**Next beat:** {single title} — reply `next` or answer the check.
```

## Lesson files

One concept per `lessons/NNNN-slug.md`. Flow: minimal why → practice → one check. Cite `RESOURCES.md`. No em dash or emojis in files. Write to disk only when user asks; do not duplicate the full chat lesson by default.

## Feedback

User answers check → brief specific feedback → wait for `next` before the next beat. Demonstrated understanding or corrected misconception → learning record per [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md).

## Mission or glossary changes

Confirm with user; update file; learning record if mission shifts.

## After session

If program facts changed, ask user to update `program/notes/` or `program/draft.md` as appropriate. If teaching, offer one line: `Paused at beat {i}/{n}: {title}.`

## Out of scope

- Default chat without `@teach-me`
- Multi-beat dumps or FAQ walls
- Replacing `program/notes/` as factual SoT
- Full editorial read-through (`@editorial-review`)
- Duplicating digest checklists inside lessons (link instead)
