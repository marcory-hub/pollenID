# Handoff: Key-path conflict analysis

## Goal
Human review and triage of factual size/morphology conflicts across identification keys; no site or key mutations unless explicitly asked.

## Current state
- Conflict report complete at `(temp/reports/key-path-conflicts.md)`: 344 key JSON files, 884 endpoints, 160 multi-system taxa, **53 conflict rows / 34 taxa**.
- Matching: exact `pollen_key` only; no structured YAML synonyms; Kerkvliet as **analytic** paths only (section + YAML/index size class + morph).
- Size conflicts mostly Beug MiW vs Kerkvliet-enriched YAML; Rosaceae specialty keys contribute morphology gates (striaat/psilaat, opercul).
- Worked example `rubus_chamaemorus`: Beug `33,0–41,0 µm, MiW` vs Eide `langste as 28.5 µm` (clear contradiction); annex paths present.
- `fragaria_vesca` in Human review (Eide synonym note); `tilia_platyphyllos` multi-key but no conflict (no competing numeric size).
- Analysis was one-shot REPL (no new `scripts/`); plan at Cursor plans `key-path_conflicts_82de0f58.plan.md` (do not edit unless asked).
- Keys / YAML / notes / species pages **unchanged**.

## Next steps
1. Triage `(temp/reports/key-path-conflicts.md)` §3: separate clear size contradictions from `needs review` morphology (many Rosaceae gate false-positives possible).
2. Resolve Human review items (§5): synonym notes, empty YAML morph for Kerkvliet enrichment.
3. Decide follow-up policy: YAML size/morph corrections vs key-label notes vs leave as documented source disagreement (ask before editing `docs/keys/**` or `data/pollen.yaml`).
4. If re-run needed: reuse method in plan + `scripts/extract_key_paths.py`; do not add a permanent script unless asked.

## Artifacts
- `temp/reports/key-path-conflicts.md` — full conflict table, path annex, human review, limits
- `scripts/extract_key_paths.py` — Beug / van der Ham / Kerkvliet section path reconstruction
- `docs/keys/{beug,vanderham,kerkvliet,eide,reitsma,feagri-iversen}/` — corpus (read-only for this task)
- `data/pollen.yaml` / `docs/data/pollen.json` — Kerkvliet enrichment SoT

## Suggested skills
- `@update-pollen` — only if triage leads to YAML size/morph or taxon-page fixes
- `@interactive-pollen-key` — only if user explicitly asks to change key JSON / Identificatiesleutels
- None for re-reading the report alone
