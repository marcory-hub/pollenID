# Notities melissopalynologie.

## Online
https://marcory-hub.github.io/pollenID/

## Lokaal

1. **Project ophalen**
Clone de repository naar je lokale machine:
```bash
git clone https://github.com/marcory-hub/pollenID
cd pollenID 
```

2. **Virtuele omgeving opzetten**
- installeer Python
- maak een nieuwe omgeving aan:

**Omgeving aanmaken**
```bash
python -m venv .venv
```
Activeren (Windows)
```bash
.\.venv\Scripts\activate
```
Activeren (Mac/Linux)
```bash
source .venv/bin/activate
```

3. **Installatie**
Installeer de benodigde software (MkDocs en plugins):
 
```bash
pip install -r requirements.txt
```

4. **_pollen.json_ en manifesten genereren**
Vanuit de hoofdmap:
```bash 
python scripts/build_docs_data.py
```

5. **Server starten**
Draai de lokale server vanuit de hoofdmap:
```bash 
mkdocs serve
```

6. **Bekijken**
Open http://127.0.0.1:8000 in je browser.

## Pollengegevens en afbeeldingen toevoegen

- **Bron**: alles bewerk je in `data/pollen.yaml` (één record per `pollen_key`, de sleutelregel bovenaan het blok).
- **Nieuwe soort**: voeg een nieuw topniveau-item toe met minimaal `latin` (en waar nodig `dutch`, `family`, `size`, `shape`, `aperture`, `ornamentation`, enz.).
- **Bitmapafbeeldingen van pollen (canoniek)**: zet bestanden onder `docs/assets/images/by-taxon/<pollen_key>/` met **numerieke** bestandsnamen `pollen_key_1.png`, `pollen_key_2.png`, … (provenance zit in `kind` / `source`).
- **Niet-pollen / placeholders**: alleen onder `docs/assets/images/non-pollen/` (bijv. `placeholder.png`, `no_image_found.jpg`).
- **Ontbrekende afbeeldingen (taken)**: lege mappen `docs/assets/images/by-taxon-task/<bron>/<pollen_key>/` (met `.gitkeep`) markeren werkitems; voer `python scripts/bootstrap_by_taxon_task.py` opnieuw uit na grote wijzigingen aan sleutels/pagina’s.
- **Koppeling in YAML**: onder het taxon een lijst `images:` met per bestand:
  - `path`: docs-relatief pad, bijv. `assets/images/by-taxon/mijn_sleutel/mijn_sleutel_1.png`
  - `kind` en `source`: corpus of herkomst (bijv. `pollenwiki`, `paldat`, `beug`, `kerkvliet`)
  - optioneel `width_px` / `height_px` per afbeelding (voor beeldverhouding); **weergavebreedte** voor index/sleutels komt uit export: `display_width_px ≈ round(grootste maat in µm × 2,5)`, default **125 px** als er geen maat is.
- **Externe atlas-URL’s**: standaard gegenereerd naar `pollen.json` vanuit `latin` (`pollenx`, `tstebler`, `paldat`); overschrijf of zet op `null` via optioneel blok `links:` in YAML waar een URL fout is.
- **Standaardhoogte voor macro’s**: blok `image:` met `height_px` als er geen per-afbeelding `width_px`/`height_px` staat (zie `scripts/mkdocs_macros.py`).
- **Pagina met alle YAML-foto’s**: in Markdown `{{ gallery("pollen_key") }}` (macro’s staan in `scripts/mkdocs_macros.py`).
- **Na elke YAML-wijziging**: `python scripts/build_docs_data.py` en daarna `mkdocs serve` (of `mkdocs build`).
- **Niet bewerken**: `docs/data/pollen.json` en `docs/assets/manifests/*.json` worden automatisch gegenereerd.
- **Validatie (aanbevolen)**:
  ```bash
  ./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
  ```
- **Migratie / normalisatie (bulk)**:
  - `python scripts/normalize_by_taxon_numeric_images.py` — hernoemt naar `slug_N.png` en herschrijft verwijzingen.
  - `python scripts/migrate_pollen_images_by_taxon.py` — verplaatst bitmapbestanden naar `by-taxon` waar van toepassing.
  - `python scripts/audit_pollen_assets.py` — inventarisatie (JSON-rapport).

## Publishen (GitHub Pages)

Pushes naar `main` bouwen de site via GitHub Actions (`.github/workflows/ci.yml`): `pip install -r requirements.txt`, daarna `python scripts/build_docs_data.py` en `mkdocs build`, gevolgd door deploy naar Pages.

## Meer hulpscripts

Overige Python-tools in `scripts/` (sleutel-JSON genereren, screenshot-import hernoemen, pollenwiki-paden herschrijven, enz.) hebben bovenaan een korte uitleg in de **docstring**; ze horen bij onderhoud en staan niet allemaal in de workflow hierboven.