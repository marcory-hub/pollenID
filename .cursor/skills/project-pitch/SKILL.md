---
name: project-pitch
description: Draft elevator pitches and stakeholder summaries from verified project sources. Use when project pitch, explain the whole project, elevator pitch, or @project-pitch.
---

# Project pitch

Facts only from `.cursor/skills/read-notes/SKILL.md`, `README.md`, and `.cursor/rules/project-context.mdc`. Mark gaps `[to be verified]`. No em dash, no emojis.

README procedures: `.cursor/skills/update-readme/SKILL.md`.

## Read first

Run `read-notes` for layout and recent roadmap (`_project_layout_pid.md`, `_timeline_pid.md` recent entries only). Add `README.md` for public-facing stack summary. Confirm live site URL from README if stated.

## Deliver

| Request | Output |
| :--- | :--- |
| Elevator pitch | 3 to 5 sentences: problem (melissopalynology / pollen ID), MkDocs Material reference site, Dutch keys and taxon pages, GitHub Pages |
| Stakeholder summary | Short prose or bullets; gloss jargon once |
| External talk draft | Offer `@grill-me` before finalizing |

**Must state:** published content lives under `docs/`; taxon SoT is `data/pollen.yaml`; interactive keys use JSON + `pollentabel.js`; site deploys via GitHub Actions to Pages.

## Do not

- Invent pipeline steps, taxon counts, or paths
- Publish note content to git unless user asks
- Edit presentation files unless user explicitly requests
