**One-line purpose:** 
**Short summary:** 
**Agent:** this is where code lives and dies, keep monorepo
**SoT:** yes
**Main Index:** [[__pollenID]]

---

**pollenID**: single monoreporoot contains all active work

**goal**: make a practical guide for melisopalynology in Dutch

**problem**: information is alfabetical or in databases. This in not the easiest for the human brain to learn melisopalynology

**language**: agent replies in english, text for the document markdownfiles is in Dutch.

**build**: mksdocs

---

**primary learner**
Imker-first as default; palynologist is “verdieping”

**unit of mastery**
type/family + monofloral reasoning is where melissopalynology

---
## Hoofdstructuur
```

docs/

├── index.md # Startpagina (handmatige inhoudslinks)

├── palynologie-paginas/ # Conceptuele en overzichtspagina’s

├── pollen-determineren/ # Determinatiebladen en praktijkpagina’s

├── naslag/ # Referenties, vergelijkingen, deze structuur

├── assets/ # Afbeeldingen (o.a. pollenwiki, paldat, beug)

└── stylesheets/ # Site-CSS (extra.css)

```
## palynologie-paginas

Thema-overzichten en didactische bruggen: microscopie (overzichts- en detailvergroting), kristallen in honing, monoflorale honing als thema, pollen in Nederlandse honing, secundaire inbreng, vergelijkingen, verdiepingsset-landing, PalynoQuest, botanische herkomst, enzovoort. Veel van deze bestanden staan ook in de zichtbare navigatie in `mkdocs.yml`.
## pollen-determineren/`

  

Concrete determinatie- en voorbeeldmateriaal, opgedeeld naar type (aantallen `.md`-bestanden in de map zelf zijn indicatief en veranderen mee met de repo):

  

| Map | Ongeveer aantal pagina’s (1 diepte) | Rol (kort) |

| :--- | ---: | :--- |

| `monoflorale-honing-pollen/` | ~20 | Monoflorale honingsoorten: honingpagina’s met pollenbeeld en context. |

| `nederlandse-honing-pollen/` | ~60 | Taxa die veel in Nederlandse honing voorkomen. |

| `verdiepingsset/` | ~1200+ | Uitgebreide set species- en hulppagina’s (grote bestandscollectie). |

| `secundaire-inbreng/` | ~20 | Secundaire inbreng (o.a. windstuifmeel, grassen). |

| `pollen-vergelijkingen/` | ~20 | Side-by-side vergelijkingen en look-a-like pagina’s. |

  

**Let op:** De zichtbare `nav` in `mkdocs.yml` vermeldt niet elke pagina in deze mappen; ontbrekende bestanden worden door de build genegeerd (`validation.nav.omitted_files: ignore`). Lezers bereiken veel bladen via interne links, de startpagina en zoekfunctie.

  

## naslag/

Langere referentielijsten, hulpmaterialen (bijv. determinatiesleutels) en onderhoudsteksten zoals deze structuurpagina.
## assets/ en stylesheets/
- **assets/images/**: bronnen per map (namen van mappen volgen herkomst of projectconventie). Afbeeldingen horen bij de pagina’s die ernaar linken; schaal en alt-tekst volgen de projectrichtlijnen.
- **stylesheets/extra.css**: aanvullende opmaak voor Material for MkDocs.
## Gerelateerde configuratie
- **Navigatie en plug-ins:** rootbestand `mkdocs.yml`.
- **Privé-notities en bron-tabellen:** map `notes/` (niet onderdeel van de gepubliceerde site; alleen lezen voor auteurs).