# Praktische handleiding en naslagwerk voor melissopalynologie.

Notities voor het herkennen en determineren van pollen in honing, met de nadruk op de praktische uitvoering van microscopische analyse. De documentatie is gebouwd met MkDocs Material.

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

4. **Server starten**
Draai de lokale server vanuit de hoofdmap:
```bash 
mkdocs serve
```

5. **Bekijken**
Open http://127.0.0.1:8000 in je browser.