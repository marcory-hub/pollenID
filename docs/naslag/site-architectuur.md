# Site-architectuur (GitHub)

Technisch overzicht van de gepubliceerde PollenID-site: wat staat in de repo, hoe het wordt gebouwd, en hoe de onderdelen samenhangen. Klik hier voor overzicht van de [scripts](scripts.md).

Live: https://marcory-hub.github.io/pollenID/

## Pipeline

```
data/pollen.yaml          docs/**/*.md          docs/keys/**/*.json
        │                        │                         │
        └──────── build_docs_data.py ──────────────────────┘
                         │
           docs/data/pollen.json
           docs/assets/manifests/*.json
                         │
                  mkdocs build  (+ scripts/mkdocs_macros.py)
                         │
              GitHub Actions → GitHub Pages (site/)
```

CI: `.github/workflows/ci.yml` — op push naar `main`: `pip install`, `python scripts/build_docs_data.py`, `mkdocs build`, deploy artifact.

## Repository

| Pad | Rol |
| :--- | :--- |
| `mkdocs.yml` | Site-naam, URL, `nav`, theme, plugins, globale CSS/JS |
| `scripts/mkdocs_macros.py` | MkDocs-macros plugin: `pollen`, `gallery`, … (`module_name` in `mkdocs.yml`) |
| `requirements.txt` | MkDocs Material, macros-plugin, PyYAML |
| `data/pollen.yaml` | **SoT** taxonmetadata (één blok per `pollen_key`) |
| `docs/` | Alle site-inhoud en statische assets |
| `.github/workflows/ci.yml` | Build + deploy |


## MkDocs-configuratie (`mkdocs.yml`)

| Onderdeel | Waarde |
| :--- | :--- |
| Theme | Material (`navigation.instant`, tabs, sections) |
| Plugins | `search` (nl), `tags`, `macros` (`module_name: scripts/mkdocs_macros`) |
| Globale CSS | `docs/stylesheets/extra.css` |
| Globale JS | `pollentabel.js`, `kerkvliet-determinatietabel.js`, `palynoquest.js` |
| Nav | Expliciete boom; veel pagina's staan **niet** in nav maar worden wel gebouwd |

Pagina's buiten `nav` (linkbaar, geen menupunten): o.a. `docs/pollen/species/`, `docs/pollen/families/`, `docs/lookalikes/`, individuele Beug-deelsleutels.

## Brondata: `data/pollen.yaml`

Topniveau = `pollen_key` (ASCII slug, meestal `genus_species` of `genus_typ`).

| Blok | Velden (kern) |
| :--- | :--- |
| `name` | `latin_name`, `dutch_name` |
| `classification` | `family_latin`, `family_dutch`, … |
| `size` | `size_smallest`, `size_largest`; optioneel `height_px` |
| `pollen_features` | `shape`, `sculpture`, `aperture`, `ornamentation`, `*_visibility` (`lm_clear` \| `lm_poor` \| `em_only`) |
| `frequency_in_*_honey` | geografie in YAML, niet als aparte mappen |
| `images[]` | `path` (docs-relatief `assets/…`), `kind`, `source`; optioneel `width_px` / `height_px` |
| `links` | Externe atlas-URL's (overschrijft defaults) |

Weergavebreedte site-breed: `display_width_px ≈ round(grootste maat µm × 2,5)`, default **125 px** zonder maat.

## Gegenereerde site-data (niet handmatig bewerken)

| Bestand | Bron | Gebruik |
| :--- | :--- | :--- |
| `docs/data/pollen.json` | `export_pollen_json.py` | Runtime-index voor alle JS-widgets; taxonvelden, beelden, `has_taxon_page`, `monofloral_honey_page` |
| `docs/assets/manifests/keys.json` | `build_manifests.py` | PalynoQuest: lijst interactieve sleutels |
| `docs/assets/manifests/palynoquest-items.json` | idem | Quiz-items (beeld + verwacht label + sleutel-URL) |
| `docs/assets/manifests/images.json` | idem | Beeldinventaris + gebruik in sleutels |

Regenereren: `./.venv/bin/python scripts/build_docs_data.py` (lokaal vóór `mkdocs serve`; CI doet dit automatisch).

## `docs/` — inhoudslagen

```
docs/
├── index.md                          Home
├── Identificatiesleutels/            MkDocs-pagina's voor sleutels
├── keys/                             JSON-bronnen (beug/, vanderham/, kerkvliet/, …)
├── gallerie/                         Curated overzichten + gallery-macro
├── lookalikes/                       Verwisselbare typen
├── monoflorale-honing-pollen/        Honingsoorten (nav)
├── pollen/
│   ├── species/<pollen_key>.md       Taxonpagina's (niet in nav)
│   └── families/<family_slug>.md     Familie-overzichten
├── naslag/                           Referentie
├── assets/
│   ├── images/by-taxon/<slug>/       Pollen-bitmaps: slug_1.png, slug_2.png, …
│   ├── images/non-pollen/            Placeholders, protocolfoto's
│   └── manifests/                    Gegenereerd
├── javascripts/                      Client-widgets
├── stylesheets/extra.css             Site-CSS
└── data/pollen.json                  Gegenereerd
```

Interne links: **relatieve** Markdown-paden tussen bestanden onder `docs/`.

## Paginatypen

### 1. Statische Markdown

Gallerie-tabellen, lookalikes, naslag, monofloraal-proza. Geen JS-mount.

### 2. Macro-pagina's (`scripts/mkdocs_macros.py`)

Macros lezen `data/pollen.yaml` at build time (Jinja in Markdown):

| Macro | Functie |
| :--- | :--- |
| `pollen("slug", "field")` | Enkel YAML-veld |
| `pollen_vis_suffix("slug", "sculpture")` | LM/EM-zichtbaarheidssuffix |
| `pollen_img("slug", "assets/…")` | Afbeelding met schaalbreedte |
| `gallery("slug")` | Alle YAML-`images` in `.pid-scale-gallery` |

Voorbeeld taxonpagina: `docs/pollen/species/calluna_vulgaris.md` — titel, gallery-macro, kenmerkentabel, YAML-dump, determinatiesleutel-blokken.

### 3. Interactieve sleutels (client-side)

MkDocs-pagina = titel + `div` met `data-json-url`. Geen page-specifiek script; globale JS in `mkdocs.yml`.

#### Dichotomische sleutel (`pollentabel.js`)

Beug, van der Ham, Rosaceae (Reitsma/Eide), …

```html
<div id="pollentabel-root" data-json-url="../../keys/beug/beug13-tricolpatae-ps-aconitum-groep.json"></div>

### Tabel-overzicht

<div id="pollentabel-table-root" data-json-url="../../keys/beug/beug13-tricolpatae-ps-aconitum-groep.json"></div>
```

JSON-contract (`docs/keys/`):

| Top-level | Inhoud |
| :--- | :--- |
| `meta` | `key`, `title`, `locale`, `source`, `start`, `stepCount` |
| `start` | id eerste stap |
| `steps` | object: elke stap `choices[]` met `label` + **`next`** (stap-id) of **`outcome.text`** |

Optioneel: `images[]` op choices/outcomes; terminal `id.pollen_key` koppelt aan YAML (slim format: alleen `{ pollen_key, note? }`).

Markup in strings: `*cursief*`; `[label](https://…)` alleen voor http(s).

#### Kerkvliet-tabel (`kerkvliet-determinatietabel.js`)

Pagina: [Determinatietabel Kerkvliet](../Identificatiesleutels/kerkvliet-determinatietabel.md)

```html
<div id="kerkvliet-determinatietabel-root"
     data-json-url="../../keys/kerkvliet/kerkvliet-determinatietabel.json"></div>
```

JSON: `sections[]` + `rows[]` met `{ section, pollen_key }`. UI: sectie-dropdown, grootteklasse-filter, zoeken, HTML-tabel + thumbnails. Kolomdata uit `pollen.json`.

Grootteklassen (max parsed µm): VerySmall &lt;15, Small 15–25, Medium 26–50, Large 51–100, VeryLarge &gt;100.

#### PalynoQuest (`palynoquest.js`)

Pagina: [PalynoQuest](palynoquest.md) (nav: Willekeurig). HTML met `data-pq-*` attributen; laadt `keys.json` + `palynoquest-items.json` + embedded `pollentabel.js`-wizard voor sleutelpad.

## JavaScript — gedeeld gedrag

Alle drie scripts:

- Boot via `document$.subscribe` (Material instant nav) of `DOMContentLoaded`
- Resolven van relatieve `data-json-url` / asset-paden t.o.v. `document.baseURI`
- LM/EM-labels uit `*_visibility` in `pollen.json`
- Latijn-link → `monofloral_honey_page` of `pollen/species/<pollen_key>.md` (skip bij `has_taxon_page === false`)

## CSS (`docs/stylesheets/extra.css`)

| Prefix | Doel |
| :--- | :--- |
| `.pid-scale-*` | Macro-galerijen, true-scale rijen |
| `.pollentabel-*` | Wizard, keuze-knoppen, platte tabel-overzicht |
| `.kerkvliet-*` | Kerkvliet-toolbar en tabel |
| `.pid-pollen-latin-link` | Taxonlinks uit JS |

## Afbeeldingen

| Locatie | Gebruik |
| :--- | :--- |
| `docs/assets/images/by-taxon/<pollen_key>/` | Canonieke pollen-bitmaps (`<key>_N.png`) |
| `docs/assets/images/non-pollen/` | Placeholders, niet-pollen |
| Pad in YAML/JSON | Altijd docs-relatief: `assets/images/by-taxon/…` |

Sleutel-JSON verwijst niet meer naar inline duplicaten wanneer `pollen_key` in YAML staat; beelden komen uit `pollen.json`.

## Sleutel-JSON ↔ YAML koppeling

Eindpunten/rijen dragen `pollen_key` (= YAML top-level slug). Runtime vult aan uit `pollen.json`. Legacy inline velden (`latin`, `grootte`, `images`, …) worden nog ondersteund maar zijn uitgefaseerd ten gunste van slimme rijen.

Taxonpagina's kunnen Kerkvliet/Beug/vdH-paden tonen via determinatiesleutel-secties ( gegenereerd met `extract_key_paths.py` — zie [Scripts](scripts.md)).

