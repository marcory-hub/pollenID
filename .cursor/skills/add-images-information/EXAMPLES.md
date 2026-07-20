# Examples: add images + information

## Callicarpa bodinieri

### User input

```
Schoonvrucht (Callicarpa bodinieri), in de volksmond vaak 'paarsebesjesplant'
callicarpa_bodinieri
  Familie: Verbenaceae (Eisenkrautgewächse)
  Deutscher Name: Chinesische Schönfrucht
  Pollengrösse: 33 (30.9-36.6) μm (Medium)
  Pollenklasse: 13 Tricolpatae mit psilaten, scabraten, verrucaten oder microverrucaten Skulpturen
  Pollen: Dreieckig konvex bis rundlich, sphäroid (PoFormI ca. 0.87-0.90), isopolar, tricolpat,
  scabrat bis verrucat/rugulat, dichtes PK. Die Aperturmembranen sind stark körnig ornamentiert.
  Mittelgrosses Polarfeld (PolFeldI ca. 0.31).
```

Images on disk: `docs/assets/images/by-taxon/callicarpa_bodinieri/*.png` (four atlas screenshots).

### YAML mapping

```yaml
callicarpa_bodinieri:
  name:
    latin_name: Callicarpa bodinieri
    dutch_name: schoonvrucht
  classification:
    family_latin: Verbenaceae
    family_dutch: ijzerhardfamilie
    genus: Callicarpa
  size:
    size_smallest: 30.9 µm
    size_largest: 36.6 µm
  pollen_class_beug: Tricolpat-psilat
  pollen_features:
    shape: driehoekig convex tot rond, sfereoid
    polarity: isopolaar
    aperture: tricolpaat
    sculpture: scabraat tot verrucaat/rugulaat
    ornamentation: aperturemembranen sterk korrelig geornamenteerd
    pe_ratio: PoFormI ca. 0,87-0,90
    pollen-note: 'PolFeldI ca. 0,31; MiW 33 µm (30,9-36,6 µm); Beug-klasse 13 Tricolpatae (psilaat-scabraat-verrucaat)'
  note:
    note_plant: "volksnaam: paarsebesjesplant; Duitse naam: Chinesische Schönfrucht"
```

Adjust `pollen_class_beug` only to allowed labels in `docs/naslag/scripts.md`; keep German class detail in `pollen-note` when needed.

### Checklist

1. Rename screenshots → `callicarpa_bodinieri_1.png` … `_4.png`.
2. Ensure `images:` rows sit on `callicarpa_bodinieri`, not `callicarpa_typ`.
3. Sync + validate (see SKILL.md).
4. Replace stub `docs/pollen/species/callicarpa_bodinieri.md` with gallery + Kenmerken + sleutels.
5. Remove `## callicarpa_bodinieri` from `_pollen-atlas-links.md`.
