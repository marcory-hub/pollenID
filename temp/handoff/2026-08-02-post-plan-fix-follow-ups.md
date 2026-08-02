# Handoff: Post plan-fix follow-ups

## Goal
Close remaining gaps after the fix-broken / token-efficiency / workflow-speed plan: fill monofloraal content, review uncommitted diffs, then commit when the user asks.

## Current state
- Plan implemented on `main` (ahead of `origin/main` by 2). Changes are **uncommitted**.
- `mkdocs build --strict` and `validate_pollen_site.py --rebuild-data --images` were green at end of session.
- OCR/duplicate YAML keys merged (e.g. `lychnis_*` → `silene_flos_cuculi`; typo stubs into correct keys). Images moved to `by-taxon/silene_flos_cuculi/`.
- Always-on `.cursor/rules` decontaminated and trimmed; wrong-project skills rewritten for pollenID.
- New orchestrator: `scripts/add_taxon.py`; `add-pollen` / `add-images-information` / `add-tstebler` consolidated (no double `build_docs_data`).
- Obsolete scripts removed; `docs/naslag/scripts.md` updated.
- `docs/naslag/monofloraal-groepsindeling.md` is **title-only stub** (needed for `--strict`). User said they will provide Representatiegroep content; not filled yet.
- CI: `.github/workflows/ci.yml` now uses `mkdocs build --strict`.

## Next steps
1. Ask user for monofloraal Representatiegroep copy; replace the stub in `docs/naslag/monofloraal-groepsindeling.md` (optionally add to `mkdocs.yml` naslag nav).
2. Spot-check uncommitted taxon merges (latin names, species pages, gallery family for *Silene* still shows Grossulariaceae in `docs/gallerie/gallery-nl-pollen-types.md` — pre-existing error, fix only if user wants).
3. When user asks: commit the working tree (do not push unless asked).
4. For next taxon adds: prefer `scripts/add_taxon.py --slug <key>` / `@add-pollen` instead of separate rename/sync/build/validate shells.

## Artifacts
- Plan (reference only): `~/.cursor/plans/fix_broken_items,_token_efficiency,_workflow_speed_9dfce0de.plan.md`
- `scripts/add_taxon.py` — add-taxon orchestrator
- `docs/naslag/monofloraal-groepsindeling.md` — stub awaiting user content
- `docs/pollen/species/silene_flos_cuculi.md` — canonical page after lychnis merge
- `data/pollen.yaml` — merged typo/duplicate keys
- `.cursor/rules/anti-hallucination-verification.mdc` — pollenID SoT (was trainingPRG)
- `.cursor/docs/site-layout.md` — docs tree moved out of always-on rules

## Suggested skills
- `@add-pollen` — continue taxon batch work with the new orchestrator
- `@update-readme` — only if public README should mention `add_taxon.py`
- `@less-tokens` — if further always-on rule cuts are needed
