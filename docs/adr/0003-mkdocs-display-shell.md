# MkDocs as display shell; JSON pipeline for taxon UI

PollenID keeps MkDocs Material on GitHub Pages as the lasting site shell for page-per-key determination and curated curriculum Markdown. Taxon display does not read `data/pollen.yaml` at runtime or via leaf macros: YAML remains authoring SoT; build exports split JSON (slim shared index at `docs/data/pollen.json` plus per-slug detail under `docs/data/taxa/`); thin taxon leaves are generated in `build_docs_data` / CI and are not committed. Interactive JS uses a shared core plus page entrypoints. Hand-authored Identificatiesleutels MD stays; macros remain only for curated non-leaf pages (gallerie, herkennen).

Status: accepted
