# Handoff: Cape taxon Dutch names

## Goal
Cape (flora-regio-kaap) taxa in `data/pollen.yaml` have verified Dutch vernaculars only. Empty is correct when Wikipedia/Wikidata has no Dutch name. Do not invent.

## Current state
- 335 unique Cape `pollen_key`s in `docs/keys/flora-regio-kaap/taxa-index.json`. All have YAML rows.
- **16** have `dutch_name`: 3 already present (`papaver_rhoeas` grote klaproos, `punica_granatum` granaatappel, `raphanus_raphanistrum` wilde radijs) plus 13 added this session.
- **319** still have empty `dutch_name`. nl.wikipedia exact-title + Wikidata labels/P1843/nlwiki sitelinks found no species vernacular. Mass SPARQL/search hit HTTP 429; do not retry aggressively.
- **109** empty `family_dutch` filled from Dutch Wikipedia family articles (e.g. wijnruitfamilie, lissenfamilie, ijskruidfamilie). **23** still empty: Wikipedia family page title is Latin only (Bruniaceae, Cunoniaceae, Curtisiaceae, Ebenaceae, Francoaceae, Limeaceae, Molluginaceae, Neuradaceae, Penaeaceae, Peraceae, Stillbaceae, Tecophilaeaceae, Vahliaceae, Xyridaceae, Zygophyllaceae).
- Rejected lookalikes (Wikipedia is a different species): hottentotvijg = *Carpobrotus edulis* not `carpobrotus_acinaciformis`; stekelpapaver = *Argemone mexicana*; reigersbek = *Erodium cicutarium*; boksdoorn = *Lycium barbarum*; smalle wikke = *Vicia sativa* var. *nigra* (used voederwikke for `vicia_sativa`).
- `scripts/add_taxon.py --render-pages` for the 13 slugs also ran `sync_beug_key_paths.py`, which **rewrote all of** `data/pollen.yaml` via ruamel (removed empty `beug_key_paths` on those 13; wrapped some image paths). Species pages are gitignored (`docs/pollen/species/*.md`).
- Validate `--rebuild-data --images --links` failed on 77 older non-Cape `*_typ` link checks (same set as `temp/handoff/2026-09-11-flora-regio-kaap-pre-push.md`). Not caused by this name fill.
- Broader Cape intake still uncommitted. See that pre-push handoff for keys, gallery, `mkdocs build --strict`.

## Next steps
1. Do not fill remaining Cape `dutch_name` unless a new source is named (nl.wikipedia / Wikidata / user). Leave empty.
2. Optional: add the new family vernaculars to `FAMILY_DUTCH` in `scripts/ingest_flora_regio_kaap_taxa.py` so later ingest matches YAML.
3. Continue Cape pre-push from `temp/handoff/2026-09-11-flora-regio-kaap-pre-push.md` (`mkdocs build --strict`, no commit unless asked).

## Artifacts
- `data/pollen.yaml` — 13 species `dutch_name` + 109 `family_dutch`
- `docs/keys/flora-regio-kaap/taxa-index.json` — Cape slug list
- `docs/data/pollen.json` — regenerated, gitignored; widgets read `dutch` from here
- `temp/handoff/2026-09-11-flora-regio-kaap-pre-push.md` — intake/push checklist

## Suggested skills
- `@update-pollen` — if a later source gives a verified vernacular for a named slug
- `@interactive-pollen-key` — only with an explicit Cape keys ask (type tiles still placeholders)
