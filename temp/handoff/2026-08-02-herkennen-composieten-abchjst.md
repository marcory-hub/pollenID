# Handoff: Herkennen Composieten ABCHJST

## Goal
Keep the Herkennen Asteraceae type page accurate (A/C/H/J/S/T), fill missing by-taxon images from the backlog, and leave letter/family tags consistent with Kerkvliet without inventing taxa.

## Current state
- Live page: (`docs/herkennen/composieten-abchjst/_index.md`); nav in (`mkdocs.yml`); linked from (`docs/herkennen/_index.md`).
- Type definitions from Kerkvliet "Pollentypen in de Asteraceae"; letters from stekelsectie in (`notes/pollenID/Determinatietabel voor pollen in Nederlandse honing mrt2014.txt`).
- **C-type** = verrucaat/reticulaat, geen stekels: *Centaurea cyanus*, *C. montana* (not *Echinops*; "echinaat C" on *Echinops* is a separate letter tag).
- YAML letter/family fills applied for many Asteraceae keys in (`data/pollen.yaml`); ambiguous tags carry `[to be verified]` (*Aster*/*Symphyotrichum* H, *Carduus* S genus-level, *Artemisia* mixed).
- "oefenen" forbidden in (`/.cursor/rules/interaction-style.mdc`); Willekeurig/Beug footer lines removed from Herkennen pages.
- Validate: `--rebuild-data --images` OK; `mkdocs build --strict` OK; `--links` still fails on many pre-existing `_typ` entries without atlas links.
- Changes appear uncommitted (check `git status`).

## Next steps
1. Optionally commit Herkennen ABCHJST + YAML + rule (ask first; do not push unless asked).
2. When PNGs land in `_todo/<slug>/`, run `@add-pollen` / `scripts/add_taxon.py --slug <key> --kerkvliet --render-pages` for backlog genera (*Tagetes*, *Erigeron*, *Petasites*, *Picris*, *Leontodon*, *Serratula*, …).
3. Resolve `[to be verified]` letter notes and the `santolina_jasione` queue entry with user input.
4. Optionally align (`docs/pollen/families/asteraceae.md`) "7 hoofdtypen" vs Kerkvliet’s six types (user ask only).

## Artifacts
- `docs/herkennen/composieten-abchjst/_index.md` — learning page + backlog
- `data/pollen.yaml` — letter/family tags
- `mkdocs.yml` — Herkennen nav
- `.cursor/rules/interaction-style.mdc` — "oefenen" ban
- `notes/pollenID/Determinatietabel voor pollen in Nederlandse honing mrt2014.txt` — source (read-only)

## Suggested skills
- `@add-pollen` — wire backlog taxa when images exist
- `@update-pollen-yaml` — further letter/family fills
- `@scale-images` — if adding true-scale Beelden rows
- `@less-tokens` — small follow-up edits
