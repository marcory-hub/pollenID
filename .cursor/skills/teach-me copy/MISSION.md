# Mission: trainingPRG ingestion and knowledge compilation (PoC)

## Why

trainingPRG exists so coaches stop hand-building every group session in Obsidian or Excel. The project goal is coach-owned knowledge (movements, periodization rules, cycle structures) that compiles into cited JSON and feeds prompt-driven session generation, not a proprietary exercise catalog or generic individual-tracking AI. This mission track teaches the ingestion pipeline so you own each step: raw source to draft object to reviewed canonical knowledge to traceable program output.

## Success looks like

- Can explain the ingestion loop (ingest, review, generate, explain) and what each folder or script is for.
- Has one approved movement JSON (conventional deadlift) with every field traceable to a source locator.
- Has one approved method JSON from Overcoming Gravity periodization material.
- Can run or walk through draft parsing, validate against `schemas/`, and approve into `knowledge/approved/` without inventing cues or protocols.
- Can scope the next source (sumo deadlift, second method) using the same pattern, including when a source is the wrong movement.

## Constraints

- PoC first: conventional deadlift, sumo deadlift, one OG method, CF as movement cues.
- Human review on all draft objects; no auto-promote to canonical knowledge.
- `local/` stays private and gitignored; provenance via a source manifest, not committed raw PDFs.
- KISS: flat JSON, small scripts, no vector DB, multi-agent stack, or UI until the first vertical slice works.
- Program facts and citations live in knowledge objects and `program/notes/`; lessons teach process and structure, not invented session data.

## Out of scope

- Full movement library, templates, or progression tracking (Phase 2).
- Orchestrator and generated training plans until at least one movement and one method are approved.
- Athlete logging, CRM, payments, or delivery UI.
- Replacing Obsidian `notes/` as design SoT; teach-me tracks learning, not project planning drafts.
- Editorial read-through of finished coaching prose (`@editorial-review`).
