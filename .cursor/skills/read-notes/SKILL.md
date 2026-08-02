---
name: read-notes
description: Load facts from gitignored notes/ with mandatory Read verification before answering. Use when timeline, layout, CLI sync, roadmap, read notes, or @read-notes.
---

# Read notes first

`notes/` is gitignored. **Read** on an exact path is the only trusted source; Glob/Grep alone are not enough.

## Workflow

1. Pick path from the table below (broad topic: start `notes/pollenID/__pollenID.md`).
2. **Read** full path string with Read tool.
3. If Read fails or file empty: stop; point to `notes/pollenID/_cli_pid.md`. Do not invent paths.
4. Cite `(notes/pollenID/_file.md:line)`. Do not paste large blocks into git-tracked files unless asked.

## Topic to path (single router)

| Topic | Read first |
| :--- | :--- |
| Index | `notes/pollenID/__pollenID.md` |
| CLI / Obsidian sync | `notes/pollenID/_cli_pid.md` |
| Roadmap / milestones | `notes/pollenID/_timeline_pid.md` |
| Layout | `notes/pollenID/_project_layout_pid.md` |
| GitHub / Pages | `notes/pollenID/_github_pid.md` |
| Terminology | `notes/pollenID/pollen terminology.md` |
| Synonym audit | `notes/pollenID/pid synonym audit.md` |
| Priorities | `notes/pollenID/prio pollen.md` |

Matrix pointer: `.cursor/rules/project-context.mdc`.

## Roadmap edits

When user logs a win: suggest 1 to 3 past-tense bullets under `yyyy-mm-dd` for `_timeline_pid.md`. User writes in Obsidian unless apply to file.

## Do not

- Answer from memory or prior chat without successful Read
- Invent note paths
