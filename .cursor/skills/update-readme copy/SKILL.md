---
name: update-readme
description: >-
  Make or update README files with project voice and GitHub conventions for this
  training-program repo. Use when the user asks to improve README, write readme
  copy, polish README.md, create the first README after setup, or @update-readme.
disable-model-invocation: true
---

# Make README

**Role:** Style and structure only. Never use this skill as a factual source. Facts come from `README.md`, `docs/repo-map.md`, `knowledge/`, `program/`, or the user prompt. Mark gaps `[to be verified]`.

**Note:** Root `README.md` may not exist until project setup is done. Create it only when the user asks; do not pre-write a placeholder README during setup.

## Audience

1. **Author:** knows program scope; needs structure and file map fast.
2. **Collaborator:** coach; needs context, then where to look.

Serve both: terse file map, welcoming intro. No dumbing down scope or burying the draft path.

## Edits

- Operate on the user-specified path only (default: root `README.md`).
- Do not rewrite existing sections unless the user asks to polish or rewrite.
- Insert new content at the requested anchor. User-edit authority: `.cursor/rules/interaction-style.mdc`.
- If path, anchor, or factual claim is missing, ask before writing.

## Intro contract (root README)

Two lines after the title:

1. **What:** concrete noun, no hype (e.g. coach-to-coach training block on pressing triggers in the final third).
2. **Who:** author and/or collaborator (see above).

Never open with background, full outline, or TOC.

## Section modes

Do not mix modes in one section.

| Mode | Use in | Rules |
| :--- | :--- | :--- |
| **Prose** | Intro, background | Inverted pyramid (main point first). No throat-clearing openers. |
| **Procedure** | Workflow, file map | Goal, prerequisites, numbered steps. No hooks or digressions. End with next step or success criteria. |

## Voice

Colleague notes, not blog or chatbot. Follow project-wide ban: no em dash, no emojis (`.cursor/rules/interaction-style.mdc`).

**Banned:** "In this section we will…", "It's worth noting…", "Let's dive in", empty enthusiasm, tricolon stacks ("clear, engaging, and accurate"), filler under every heading, generic sentences that fit any repo.

**Preferred:** direct and specific; concrete nouns ("6-week block", `knowledge/session-rules/strength.json`); explain jargon once or drop it; active voice; bold key paths for scanning only; simplify without distorting facts.

## GitHub conventions

- **No Cursor:** Public README copy must not name Cursor or `.cursor/` paths. See `.cursor/rules/interaction-style.mdc` (Public documentation).
- Title + intro contract at top.
- TOC on long READMEs; anchors match GitHub IDs.
- Fenced code blocks with language tag when showing commands.
- Link to sections instead of repeating (`See [Structure](#structure)`).
- Update TOC when adding sections.

## Pre-publish test

1. Can a collaborator find the active track paths in `docs/repo-map.md` in 30 seconds?
2. Would you send any paragraph to a colleague unchanged?
3. Delete each section's first sentence: if nothing is lost, cut the opener.

## Out of scope

- **Program prose style:** `sports-communication.mdc` and `docs/sports-communication-digest.md`.
- **Loads, drills, periodization facts:** `knowledge/` and cited sources.
- **Chat tone:** `interaction-style.mdc`.
