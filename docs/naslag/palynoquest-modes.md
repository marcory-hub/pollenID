# PalynoQuest: modi en niveau-locks

Contract voor de quiz-widget (`docs/javascripts/palynoquest.js`). Doel: modi niet door elkaar halen.

## Drie modi (niet uitwisselbaar)

| Modus | `data-pq-lock-level` / select-waarde | Vraagvorm | Pool |
| :--- | :--- | :--- | :--- |
| **Naam-MCQ** | `1`, `2`, `3` | één beeld + vier namen | `learning_priority_rank` + beelden in `pollen.json` |
| **Kenmerken** | `kenmerken`, `kenmerken-2`, `kenmerken-3` | vorm → apertuur → sculptuur → grootteklasse → naam | alleen taxa met volledige `controlled` + beelden |
| **Lookalike** | `lookalike`, `lookalike-easy`, … | regel (optioneel) + twee namen | `lookalike-groups.json` |

Regel: numerieke locks zijn **nooit** kenmerken-drill. Kenmerken-drill alleen via `kenmerken*`.

## Pagina’s (vaste locks)

| Pagina | Lock | Modus |
| :--- | :--- | :--- |
| `docs/herkennen/niveau-1-vaak-in-nl-honing/_index.md` | `1` | Naam-MCQ |
| `docs/herkennen/niveau-2-alle-prioriteit/_index.md` | `2` | Naam-MCQ |
| `docs/herkennen/niveau-3-alles/_index.md` | `3` | Naam-MCQ |
| `docs/herkennen/pollenkenmerken/_index.md` | `kenmerken` | Kenmerken |
| `docs/herkennen/lookalikes-oefenen/_index.md` | `lookalike` | Lookalike |
| `docs/naslag/palynoquest.md` | (geen lock; dropdown) | keuze; **niet** in `nav` |

## Naam-MCQ: poolregels (disjunct)

Bron: `docs/data/pollen.json` (niet `palynoquest-items.json`).

| Niveau | Filter | Verwachte grootte (2026-08-12) |
| ---: | :--- | ---: |
| 1 | rank 1–20 én ≥1 beeld | 13 |
| 2 | rank > 20 én ≥1 beeld (geen niveau-1) | 26 |
| 3 | elk taxon met ≥1 beeld | 441 |

Constante in JS: `LEVEL1_MAX_RANK = 20`.

## Naam-MCQ: afleiders

Bron: `docs/assets/manifests/morph-neighbours.json` (build via `scripts/morph_lookalike_cluster.py`).

Volgorde bij tekort:

1. dichtste morfologische buren (max 8 per slug; alleen taxa met beelden)
2. zelfde apertuurfamilie (`controlled.apertuur` of `aperture`)
3. willekeurig uit het niveau-pool
4. willekeurig uit alle taxa met beelden

Fout antwoord: `[data-pq-wrongpreview]` toont beeld(en) van het **gekozen** taxon (`chosenSlug`).

## Kenmerken-drill (niet wijzigen voor naam-niveaus)

- Vereist `controlled`: `vorm`, `apertuur`, `sculptuur`, `grootteklasse`
- Progress-key: `feat|<slug>`
- Alleen op Pollenkenmerken (en optioneel Willekeurig-dropdown)

## Lookalike (niet wijzigen voor naam-niveaus)

- Paren uit `lookalike-groups.json`
- Confusion-log: `pid_pq_confusions` + `[data-pq-export-confusions]` (alleen lookalike)

## Parse-contract (`parseLevelValue`)

| Invoer | `kenmerkenMode` | `lookalikeMode` | `level` |
| :--- | :---: | :---: | ---: |
| `kenmerken` / `kenmerken-N` | true | false | N |
| `lookalike` / `lookalike-*` | false | true | 1 |
| `1` / `2` / `3` | **false** | **false** | 1–3 |

`applyLevel` mag numerieke waarden **niet** forceren naar kenmerken. Alleen een lock die met `kenmerken` of `lookalike` begint overschrijft de modus.

## Build / CI

```
build_docs_data.py
  → export_pollen_json.py
  → render_taxon_pages_from_sot.py
  → build_manifests.py          (keys, items, lookalike-groups, …)
  → morph_lookalike_cluster.py  (morph-neighbours.json + temp-rapport)
```

- Manifesten onder `docs/assets/manifests/` zijn gegenereerd (gitignored).
- Conflictmask `temp/reports/key-path-conflicts.md` mag ontbreken in CI (lege mask).
- Clustering-runtime ca. 7 s; hoort in CI via `build_docs_data.py`.

## Verboden regressies

- Niveau-pagina’s terugzetten op `data-pq-lock-level="kenmerken"` / `kenmerken-2` / `kenmerken-3`
- In `parseLevelValue`: numerieke niveaus mappen naar `kenmerkenMode: true`
- In `applyLevel`: `if (!lookalikeMode) kenmerkenMode = true`
- Naam-pools filteren op `controlled` (dat is alleen kenmerken)
- Afleiders zonder beelden (wrong-preview breekt)
- `docs/keys/` of veldwaarden in `data/pollen.yaml` “even” herschrijven voor de quiz
- Willekeurig weer in `nav` zetten zonder expliciete vraag (pagina blijft bereikbaar via URL / naslag)

## Cache-bust

Na wijziging van `palynoquest.js`: query-string in `mkdocs.yml` `extra_javascript` ophogen (bijv. `?v=YYYY-MM-DD-…`).

## Verificatie

1. `.venv/bin/python scripts/build_docs_data.py`
2. `.venv/bin/python scripts/validate_pollen_site.py` (exit 0)
3. `.venv/bin/mkdocs build --strict`
4. Live (na push): niveau 1/2/3 = beeld + 4 namen; Pollenkenmerken = kenmerkenstappen; Lookalikes ongewijzigd

Zie ook: [Site-architectuur](site-architectuur.md), ADR [0004](../adr/0004-palynoquest-mode-locks.md).
