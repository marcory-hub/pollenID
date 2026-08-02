# Handoff: CI deploy fix + --strict rules

## Goal
Keep GitHub Pages deploy green under `mkdocs build --strict`, and stop repeating link/asset path mistakes via always-on rules.

## Current state
- Deploy fix committed as `737683d` (`fix deploy`) and synced with `origin/main` (CI hardening + staining image fixes + mkdocs link validation `info`).
- Uncommitted only: (`.cursor/rules/project-context.mdc`) section **4b** expanded with `--strict` / Linux case-sensitivity / image Markdown / `NO_MKDOCS_2_WARNING` guardrails.
- PalynoQuest levels + SRS and NL lookalike clusters shipped earlier (`5a78515`); confusable-pairs trainer still deferred (needs `pollen_key` lists per lookalike group).
- `gh` is installed locally but not authenticated; use signed-in browser or `gh auth login` to read Actions logs if CI fails again.

## Next steps
1. Confirm Actions run after `737683d` is green (Deploy MkDocs site to GitHub Pages).
2. Commit the `project-context.mdc` rule update when the user asks (do not leave the lesson only in chat).
3. If still pursuing learning curve option 3: collect lookalike `pollen_key` lists, then add `docs/assets/manifests/lookalike-groups.json` + Verwarring mode in `palynoquest.js`.

## Artifacts
- `.github/workflows/ci.yml` — `NO_MKDOCS_2_WARNING`, UTF-8 env, tee/grep on `--strict` build
- `mkdocs.yml` — `validation.links.*: info`; monofloraal groepsindeling in nav
- `docs/naslag/pollen-staining-protocols.md` + `docs/assets/images/non-pollen/safranin1-ali2021.png` — image Markdown / filename fixes
- `.cursor/rules/project-context.mdc` — uncommitted `--strict`/CI path rules (4b)
- `temp/handoff/2026-08-02-palynoquest-levels-lookalikes.md` — prior learning-curve handoff

## Suggested skills
- None.
