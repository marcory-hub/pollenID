# Notities melissopalynologie.

## Online
https://marcory-hub.github.io/pollenID/

## Aan de slag (Lokaal draaien)
Volg deze stappen om de documentatie op je eigen computer te bekijken:

1. **Project ophalen**
Kloon de repository naar je lokale machine:
```bash
git clone https://github.com/marcory-hub/pollenID
cd pollenID 
```

2. **Virtuele omgeving opzetten**
Zorg dat je Python hebt geïnstalleerd en maak een nieuwe omgeving aan:

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
- **Afbeeldingsbestand**: zet bestanden onder `docs/assets/images/by-taxon/<pollen_key>/` (mapnaam = dezelfde string als de sleutel).
- **Koppeling in YAML**: onder het taxon een lijst `images:` met per bestand:
  - `path`: docs-relatief pad, bijv. `assets/images/by-taxon/mijn_sleutel/Bestand.png`
  - `kind` en `source`: corpus of herkomst (bijv. `pollenwiki`, `paldat`, `persano_oddo`, `beug`)
  - optioneel `height_px` per afbeelding
- **Standaardhoogte voor macro’s**: blok `image:` met `height_px` als er geen per-afbeelding `height_px` staat.
- **Pagina met alle YAML-foto’s**: in Markdown `{{ pollen_gallery("pollen_key") }}` (macro’s staan in `main.py`).
- **Na elke YAML-wijziging**: `python scripts/build_docs_data.py` en daarna `mkdocs serve` (of `mkdocs build`).
- **Niet bewerken**: `docs/data/pollen.json` en `docs/assets/manifests/*.json` worden automatisch gegenereerd.