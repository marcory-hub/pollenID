# Synoniemen en basioniemen

## Naamgeving in `pollen.yaml`

**Leidend:** de soortnaam zoals op [Pollen Wiki](https://pollen.tstebler.ch/MediaWiki/). Die naam wordt de `pollen_key` / mapnaam onder `by-taxon`.

**Uitzonderingen** (dan een andere naam kiezen en Tstebler / oudere namen als synoniem of basioniem noteren):

1. **Type-namen** in de wiki (bijv. *Centaurea jacea-Typ*, *Aster solidago*): geen soort als de entry alleen een pollentype is; of juist de soortnaam als de type-entry eigenlijk een soort betreft.
2. **Nieuwe nomenclatuurconventies** wanneer de T Stebler-naam verouderd is (geslachtsverhuizing, geaccepteerde spelling, basioniem → nieuwe combinatie).

Synoniemen en basioniemen horen in `latin` of `note` in `data/pollen.yaml`.

## Begrippen

### Basioniem (basionym)

De oorspronkelijke geldig gepubliceerde naam waarvan later een nieuwe combinatie is gemaakt. Het epitheton blijft behouden; het geslacht (of de rang) verandert.

Voorbeeld: basioniem *Epilobium angustifolium* L. → *Chamerion angustifolium* (L.) Holub.

### Synoniem

Een andere naam voor hetzelfde taxon. Niet elk synoniem is een basioniem.

| Soort | Engels | Kenmerk |
|---|---|---|
| Homotypisch | homotypic | Zelfde type; vaak basioniem ↔ nieuwe combinatie |
| Heterotypisch | heterotypic | Andere types; taxonomen behandelen ze als één taxon |

## Verzamelde voorbeelden

Bronnen: `data/pollen.yaml`, `docs/assets/images/by-taxon/_todo/_links/_kerkvliet.md`, `docs/assets/images/by-taxon/_todo/_links/_pollen-atlas-links.md`, `docs/keys/eide/rosaceae-eide.json`. Status: sommige hernoemingen staan al in YAML, andere nog alleen als agent-noot.

| pollen_key (site / beoogd) | T Stebler (indien anders) | Synoniem / basioniem / oude naam | Relatie | Bron |
|---|---|---|---|---|
| `galium_odoratum` | *Asperula odorata* | *Asperula odorata* | basioniem; merge beoogd | kerkvliet; YAML `latin`: Galium odoratum (syn Asperula odorata) |
| `mahonia_aquifolium` | *Berberis aquifolium* | *Berberis aquifolium* | synoniem; nieuwe conventie *Mahonia* | kerkvliet; YAML `note` |
| `mahonia_bealei` | *Berberis bealei* | *Berberis bealei* | synoniem; nieuwe conventie *Mahonia* | kerkvliet; YAML `note` |
| `mahonia_japonica` | *Berberis japonica* | *Berberis japonica* | synoniem; nieuwe conventie *Mahonia* | kerkvliet; YAML `note` |
| `campanula_medium` | *Campanula media* | *Campanula media* (*C. media*) | synoniem / spelling | kerkvliet; YAML `note` |
| `chamerion_angustifolium` | *Epilobium angustifolium* (ook *Chamerion* in links) | *Epilobium angustifolium* (basioniem); *Chamaenerion angustifolium* (synoniem) | nieuwe conventie / spelling | kerkvliet; YAML `latin` |
| `centaurea_benedicta` (beoogd) | *Cnicus benedict* | *Cnicus benedictus* | synoniem; YAML heeft nog `cnicus_benedictus` | kerkvliet |
| `colchicum_autumnale` | *Colchicinum autu* (typo in wiki-slug) | *Colchicum multiflorum* | synoniem | kerkvliet |
| `leucanthemum_vulgare` | *Chrysanthemum leuc* | *Chrysanthemum leucanthemum* / *Chrysanthemum leuc* | oude naam; YAML heeft nog `chrysanthemum_leuc` | kerkvliet |
| `robinia_pseudoacacia` | *Acacia robinia* | *Acacia robinia* (verdere synoniemenlijst nog open) | oude / foutieve atlasnaam | pollen-atlas-links; YAML heeft beide keys |
| `frangula_alnus` | *Frangula alnus* | *Rhamnus frangula* | synoniem; projectregel: niet *Rhamnus* | projectcontext; YAML heeft ook `rhamnus_frangula` |
| `rosa_pimpinellifolia` | | *Rosa spinosissima* | synoniem | eide rosaceae-sleutel |
| `fragaria_vesca` | | *Potentilla palustris* | genoteerd als synoniem in sleutel [to be verified] | eide rosaceae-sleutel |
| `symphyotrichum_laeve` (beoogd) | *Aster laevis* e.d. | *Aster laevis* | nieuwe conventie (*Symphyotrichum*) | kerkvliet (`aster_sp`) |
| `symphyotrichum_novae_angliae` | *Aster novae-angliae* | *Aster novae-angliae* | nieuwe conventie | kerkvliet |
| `symphyotrichum_novi_belgii` | *Aster novi-belgii* | *Aster novi-belgii* | nieuwe conventie | kerkvliet |
| `symphyotrichum_lanceolatum` (beoogd) | *Aster lanceolatus* | *Aster lanceolatus*; *Aster tradescantii* = synoniem van smalle aster | nieuwe conventie + synoniem | kerkvliet |
| `tripolium_pannonicum` (beoogd) | *Aster tripolium* | *Aster tripolium* | nieuwe conventie; YAML heeft nog `aster_tripolium` | kerkvliet |
| `galatella_linosyris` (beoogd) | *Aster linosyris* | *Aster linosyris* | nieuwe conventie | kerkvliet |
| `centaurea_jacea` (beoogd i.p.v. type) | *Centaurea jacea-Typ* | type-naam → soortnaam | uitzondering: type | kerkvliet |

## Leeswijzer in bronnen

> *Chamerion angustifolium* (L.) Holub, synoniem: *Chamaenerion angustifolium* (L.) Scop., basioniem: *Epilobium angustifolium* L.

| Label | Betekenis |
|---|---|
| synoniem | andere naam voor hetzelfde taxon |
| basioniem | oorspronkelijke naam van de huidige combinatie |

## Praktijk

1. Start bij de T Stebler-naam.
2. Afwijken alleen bij type-entry of duidelijke nieuwe conventie.
3. Zet afwijkende / oude namen in `note` of `latin`.
4. Houd atlaslinks (PollenX, Paldat, T Stebler) bruikbaar via die notitie, ook als de `pollen_key` anders is.

## Terminologie (NL / EN)

| Nederlands | Engels |
|---|---|
| synoniem | synonym |
| basioniem | basionym |
| geaccepteerde naam | accepted name |
| nieuwe combinatie | new combination (comb. nov.) |
| homotypisch synoniem | homotypic synonym |
| heterotypisch synoniem | heterotypic synonym |
| pollentype | pollen type |
