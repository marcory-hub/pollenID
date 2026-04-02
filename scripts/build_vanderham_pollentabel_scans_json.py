#!/usr/bin/env python3
"""
Build docs/keys/vanderham/vanderham-pollentabel.json from the Pollentabel
transcript (Python STEPS). Regenerate after correcting transcript errors against
the book. Site + PalynoQuest load this file (wizard + tabel).
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "keys" / "vanderham" / "vanderham-pollentabel.json"


def ch_next(label: str, nxt: str) -> dict:
    return {"label": label, "next": nxt}


def ch_out(label: str, text: str, *, incomplete: bool = False) -> dict:
    o: dict = {"text": text}
    if incomplete:
        o["incomplete"] = True
    return {"label": label, "outcome": o}


def step(sid: str, choices: list[dict], note: str | None = None) -> dict:
    d: dict = {"id": sid, "type": "step", "choices": choices}
    if note:
        d["note"] = note
    return d


STEPS: dict[str, dict] = {
    "1": step(
        "1",
        [
            ch_next("vier pollenkorrels bij elkaar (tetrade)", "2"),
            ch_next("één losse pollenkorrel (monade)", "3"),
        ],
    ),
    "2": step(
        "2",
        [
            ch_out(
                "individuele korrels los verbonden, triporaat",
                "Onagraceae (*Epilobium*)",
            ),
            ch_out(
                "individuele korrels stevig verbonden, tricolpaat of tricolporaat",
                "Ericaceae (*Calluna, Erica, Rhododendron, Vaccinium*)",
            ),
            ch_out(
                "individuele korrels stevig verbonden, zeer dunwandig (dunner dan 1 µm), inaperturaat",
                "Juncaceae (*Juncus, Luzula*)",
            ),
        ],
    ),
    "3": step(
        "3",
        [
            ch_out(
                "pollenkorrel met twee luchtzakken (vesiculaat)",
                "Pinaceae (*Picea, Pinus*)",
            ),
            ch_next("pollenkorrel zonder luchtzakken", "4"),
        ],
    ),
    "4": step(
        "4",
        [
            ch_out(
                "pollenkorrel met ‘vensters’ (fenestraat)",
                "Asteraceae (*Cichorium, Hieracium, Lactuca, Sonchus, Taraxacum*)",
            ),
            ch_next("pollenkorrel zonder ‘vensters’", "5"),
        ],
    ),
    "5": step(
        "5",
        [
            ch_next("pollenkorrel zonder aperturen (inaperturaat)", "6"),
            ch_next("pollenkorrel met één of meer aperturen", "9"),
        ],
    ),
    "6": step(
        "6",
        [
            ch_out("pollenkorrel peervormig", "Cyperaceae (*Carex, Scirpus*)"),
            ch_next("pollenkorrel ± rond", "7"),
        ],
    ),
    "7": step(
        "7",
        [
            ch_out(
                "ornamentatie perforaat tot fijn reticulaat, pollenkorrel niet gespleten",
                "Thymelaeaceae (*Daphne*)",
            ),
            ch_out(
                "ornamentatie dicht scabraat, pollenkorrel niet gespleten",
                "Salicaceae (*Populus*)",
            ),
            ch_next(
                "ornamentatie meer of minder dicht verrucaat, pollenkorrel vaak gespleten",
                "8",
            ),
        ],
    ),
    "8": step(
        "8",
        [
            ch_out(
                "wratten onregelmatig verspreid (oppervlak met kale plekken)",
                "Cupressaceae (*Juniperus*)",
            ),
            ch_out(
                "wratten regelmatig verspreid (geen kale plekken)",
                "Taxaceae (*Taxus baccata*)",
            ),
        ],
    ),
    "9": step(
        "9",
        [
            ch_next("pollenkorrel met één apertuur", "10"),
            ch_next("pollenkorrel met drie of meer aperturen", "12"),
        ],
    ),
    "10": step(
        "10",
        [
            ch_out(
                "apertuur spiraal- of lusvormig: ‘tennisbal-patroon’ (syncolpaat)",
                "Berberidaceae (*Berberis*)",
            ),
            ch_out(
                "apertuur langwerpig, groot (monocolpaat)",
                "Veel monocotylen (o.m. Iridaceae, Liliaceae), enkele dicotylen (o.m. *Magnolia*)",
            ),
            ch_next(
                "apertuur ± rond, klein (monoporaat)",
                "11",
            ),
        ],
    ),
    "11": step(
        "11",
        [
            ch_out(
                "porus duidelijk, met verdikte rand (annulus), pollenkorrel ± rond",
                "Poaceae (alle geslachten)",
            ),
            ch_out(
                "porus onduidelijk, zonder verdikte rand, aan de stompe zijde van een peervormige korrel",
                "[Bronscan eindigt hier; vervolgstap niet op deze pagina — zie drukwerk van der Ham.]",
                incomplete=True,
            ),
        ],
        note="Tweede optie afgekapt op eerste pagina-scan.",
    ),
    "12": step(
        "12",
        [
            ch_next(
                "pollenkorrel met drie of meer langwerpige aperturen (colpi) zonder pori (colpaat)",
                "16",
            ),
            ch_next(
                "pollenkorrel met drie of meer langwerpige aperturen (colpi) met pori (colporaat)",
                "36",
            ),
            ch_next(
                "pollenkorrel met drie colpi met pori afgewisseld door drie colpi zonder pori, "
                "of colpi op een andere manier verschillend (heterocolpaat)",
                "13",
            ),
            ch_next(
                "pollenkorrel met drie of meer ± ronde aperturen (pori; poraat)",
                "72",
            ),
        ],
    ),
    "13": step(
        "13",
        [
            ch_next("pollenkorrel kleiner dan 15 µm", "14"),
            ch_next("pollenkorrel groter dan 15 µm", "15"),
        ],
    ),
    "14": step(
        "14",
        [
            ch_out(
                "colpi kruisvormig (met equatoriale ‘takken’)",
                "Boraginaceae (*Cynoglossum officinale*)",
            ),
            ch_out("colpi recht (niet ‘vertakt’)", "Boraginaceae (*Myosotis*)"),
        ],
    ),
    "15": step(
        "15",
        [
            ch_out("ornamentatie striaat", "Lythraceae (*Lythrum salicaria*)"),
            ch_out(
                "ornamentatie fijn reticulaat (mazen kleiner dan 1 µm)",
                "Hydrophyllaceae (*Phacelia tanacetifolia*)",
            ),
        ],
    ),
    "16": step(
        "16",
        [
            ch_out(
                "pollenkorrel met zes lange colpi (stephanocolpaat)",
                "Lamiaceae (vele geslachten)",
            ),
            ch_out(
                "pollenkorrel stomp rechthoekig, met vier korte colpi op de hoekpunten (stephanocolpaat)",
                "Balsaminaceae (*Impatiens*)",
            ),
            ch_next(
                "pollenkorrel met drie korte of lange colpi (tricolpaat)",
                "17",
            ),
        ],
    ),
    "17": step(
        "17",
        [
            ch_next(
                "tectum afwezig (intectaat) of aanwezig als een netwerk (eureticulaat)",
                "18",
            ),
            ch_next("tectum aanwezig (tectaat)", "26"),
        ],
    ),
    "18": step(
        "18",
        [
            ch_next("tectum afwezig", "19"),
            ch_next("tectum netvormig", "20"),
        ],
    ),
    "19": step(
        "19",
        [
            ch_out(
                "ornamentatie-elementen variabel van grootte",
                "Aquifoliaceae (*Ilex*)",
            ),
            ch_out(
                "ornamentatie-elementen uniform of in twee duidelijk gescheiden formaten aanwezig",
                "Linaceae (*Linum*)",
            ),
        ],
    ),
    "20": step(
        "20",
        [
            ch_next("colpi in het midden niet versmald", "21"),
            ch_next("colpi in het midden versmald", "25"),
        ],
    ),
    "21": step(
        "21",
        [
            ch_next("pollenkorrel groter dan 50 µm", "22"),
            ch_next("pollenkorrel kleiner dan 50 µm", "23"),
        ],
    ),
    "22": step(
        "22",
        [
            ch_out(
                "netwerk met duidelijke knotsvormige ornamentatie-elementen",
                "Geraniaceae (*Geranium*)",
            ),
            ch_out(
                "netwerk met stekeltjes (kleiner dan 1 µm)",
                "Plumbaginaceae (*Armeria maritima, Limonium vulgare*)",
            ),
        ],
    ),
    "23": step(
        "23",
        [
            ch_out(
                "mazen van het netwerk kleiner dan 1 µm",
                "Saxifragaceae (*Saxifraga*)",
            ),
            ch_next(
                "tenminste een deel van de mazen groter dan 1 µm",
                "24",
            ),
        ],
    ),
    "24": step(
        "24",
        [
            ch_out(
                "mazen duidelijk kleiner naar de colpi toe, colpusranden meestal naar binnen gevouwen",
                "Salicaceae (*Salix*)",
            ),
            ch_out(
                "mazen niet duidelijk kleiner naar de colpi toe, colpusranden reticulaat",
                "Brassicaceae (*Brassica, Raphanus, Sinapis*)",
            ),
        ],
    ),
    "25": step(
        "25",
        [
            ch_out(
                "pollenkorrel kleiner dan 25 µm",
                "Caprifoliaceae (*Sambucus nigra*)",
            ),
            ch_out(
                "pollenkorrel groter dan 25 µm",
                "Oleaceae (*Ligustrum*)",
            ),
        ],
    ),
    "26": step(
        "26",
        [
            ch_out("ornamentatie perforaat", "Saxifragaceae (*Saxifraga*)"),
            ch_next("ornamentatie psilaat of scabraat", "27"),
            ch_next("ornamentatie echinaat", "28"),
            ch_next("ornamentatie striaat of rugulaat", "31"),
            ch_next(
                "ornamentatie suprareticulaat (netwerk op het tectum)",
                "34",
            ),
        ],
    ),
    "27": step(
        "27",
        [
            ch_out(
                "nexine onduidelijk, zeer dun",
                "Saxifragaceae (*Saxifraga*)",
            ),
            ch_out(
                "nexine duidelijk, scabrae verspreid",
                "Ranunculaceae (*Ranunculus*)",
            ),
            ch_out(
                "nexine duidelijk, scabrae dicht opeen",
                "Papaveraceae (*Chelidonium majus*)",
            ),
        ],
    ),
    "28": step(
        "28",
        [
            ch_next("pollenkorrel kleiner dan 40 µm", "29"),
            ch_next("pollenkorrel groter dan 40 µm", "30"),
        ],
    ),
    "29": step(
        "29",
        [
            ch_out(
                "colpi met duidelijke wratten op de membraan (= nexine in/onder colpi)",
                "Ranunculaceae (*Ranunculus*)",
            ),
            ch_out(
                "colpi zonder wratten op de membraan (of membraan gescheurd)",
                "Fagaceae (*Quercus*)",
            ),
        ],
    ),
    "30": step(
        "30",
        [
            ch_out(
                "colpi lang, stekels duidelijk, op een verbrede basis",
                "Valerianaceae (*Valeriana officinalis*)",
            ),
            ch_out(
                "colpi kort, stekels klein, niet op een verbrede basis",
                "Dipsacaceae (*Dipsacus, Scabiosa, Succisa*)",
            ),
        ],
    ),
    "31": step(
        "31",
        [
            ch_out(
                "pollenkorrel groter dan 50 µm",
                "Geraniaceae (*Geranium*)",
            ),
            ch_next("pollenkorrel kleiner dan 50 µm", "32"),
        ],
    ),
    "32": step(
        "32",
        [
            ch_out(
                "colpusranden niet recht",
                "Rosaceae (o.m. *Cotoneaster, Malus, Prunus, Rubus, Spiraea*)",
            ),
            ch_next("colpusranden recht", "33"),
        ],
    ),
    "33": step(
        "33",
        [
            ch_out(
                "ornamentatie-elementen (muri) vooral meridionaal (± loodrecht op equatoriale vlak)",
                "Aceraceae (*Acer*)",
            ),
            ch_out(
                "ornamentatie-elementen (muri) meestal dwars (± parallel aan equatoriale vlak)",
                "Saxifragaceae (*Saxifraga*)",
            ),
        ],
    ),
    "34": step(
        "34",
        [
            ch_out(
                "colpi in het midden versmald of met onderbroken randen",
                "Fabaceae (*Cytisus, Genista, Ulex*)",
            ),
            ch_next(
                "colpi in het midden niet versmald of met onderbroken randen",
                "35",
            ),
        ],
    ),
    "35": step(
        "35",
        [
            ch_out(
                "pollenkorrel prolaat (P duidelijk groter dan E)",
                "Fabaceae (verschillende geslachten)",
            ),
            ch_out(
                "pollenkorrel ± rond tot iets prolaat (P gelijk aan of iets groter dan E)",
                "Lamiaceae (*Ajuga, Scutellaria, Stachys*)",
            ),
        ],
    ),
    "36": step(
        "36",
        [
            ch_next("pollenkorrel met meer dan drie colpi", "37"),
            ch_next(
                "pollenkorrel met drie colpi (tricolporaat)",
                "39",
            ),
        ],
    ),
    "37": step(
        "37",
        [
            ch_out(
                "colpi niet alle meridionaal (pericolporaat)",
                "Polygonaceae (*Rumex*)",
            ),
            ch_next("colpi alle meridionaal (stephanocolporaat)", "38"),
        ],
    ),
    "38": step(
        "38",
        [
            ch_out(
                "pollenkorrel groter dan 40 µm, met vier colpi",
                "Violaceae (*Viola*)",
            ),
            ch_out(
                "pollenkorrel kleiner dan 40 µm, met zes colpi",
                "Boraginaceae (*Cynoglossum officinale*)",
            ),
        ],
    ),
    "39": step(
        "39",
        [
            ch_out("ornamentatie perforaat", "Polygonaceae (*Rumex*)"),
            ch_next("ornamentatie psilaat of scabraat", "40"),
            ch_next("ornamentatie echinaat", "55"),
            ch_next("ornamentatie striaat of rugulaat", "61"),
            ch_next(
                "ornamentatie foveolaat (tectum met putjes) of suprareticulaat (netwerk op tectum)",
                "63",
            ),
            ch_next(
                "ornamentatie eureticulaat (netwerk is tectum)",
                "68",
            ),
        ],
    ),
    "40": step(
        "40",
        [
            ch_out(
                "pollenkorrel vanbinnen met twee equatoriale ringvormige verdikkingen",
                "Asteraceae (*Centaurea cyanus*)",
            ),
            ch_next(
                "pollenkorrel zonder equatoriale verdikkingen",
                "41",
            ),
        ],
    ),
    "41": step(
        "41",
        [
            ch_out(
                "pollenkorrel in zijaanzicht oblaat (P kleiner dan E), in bovenaanzicht sterk driehoekig",
                "Elaeagnaceae (*Elaeagnus*)",
            ),
            ch_next(
                "pollenkorrel in zijaanzicht prolaat (P duidelijk groter dan E), met rechte of holle zijden",
                "42",
            ),
            ch_next(
                "pollenkorrel in zijaanzicht ± rond tot iets prolaat (P gelijk aan of iets groter dan E)",
                "44",
            ),
        ],
    ),
    "42": step(
        "42",
        [
            ch_out(
                "pollenkorrel groter dan 35 µm",
                "Apiaceae (*Heracleum*)",
            ),
            ch_next("pollenkorrel kleiner dan 35 µm", "43"),
        ],
    ),
    "43": step(
        "43",
        [
            ch_out(
                "colpusranden vormen iets uitstekende kapjes over de pori",
                "Apiaceae (*Carum carvi*)",
            ),
            ch_out(
                "colpusranden vormen geen uitstekende kapjes over de pori",
                "Apiaceae (*Anthriscus sylvestris*)",
            ),
        ],
    ),
    "44": step(
        "44",
        [
            ch_next(
                "pollenkorrel in zijaanzicht ± rond (P = E)",
                "45",
            ),
            ch_next(
                "pollenkorrel in zijaanzicht prolaat (P duidelijk groter dan E)",
                "51",
            ),
        ],
    ),
    "45": step(
        "45",
        [
            ch_next(
                "wandgedeelten tussen de colpi recht tot hol (in bovenaanzicht van de pollenkorrel)",
                "46",
            ),
            ch_next(
                "wandgedeelten tussen de colpi bol (in bovenaanzicht van de pollenkorrel)",
                "49",
            ),
        ],
    ),
    "46": step(
        "46",
        [
            ch_next("pori duidelijk", "47"),
            ch_next("pori onduidelijk (soms ‘H’-vormig)", "48"),
        ],
    ),
    "47": step(
        "47",
        [
            ch_out(
                "pori smal (dwars), met spitse uiteinden",
                "Solanaceae (*Capsicum, Solanum* incl. tomaat)",
            ),
            ch_out(
                "pori rond tot elliptisch (dwars)",
                "Rhamnaceae (*Rhamnus frangula*)",
            ),
        ],
    ),
    "48": step(
        "48",
        [
            ch_out(
                "colpi naar binnen gevouwen of smal, pori soms ‘H’-vormig",
                "Cornaceae (*Cornus mas*)",
            ),
            ch_out(
                "colpi niet naar binnen gevouwen, colpusmembranen (= nexine in/onder colpi) met wratjes",
                "Fabaceae (*Robinia pseudoacacia*)",
            ),
        ],
    ),
    "49": step(
        "49",
        [
            ch_out(
                "pori onduidelijk (soms ‘H’-vormig), colpi lang",
                "Cornaceae (*Cornus mas*)",
            ),
            ch_out(
                "pori groot, elliptisch (dwars), colpi kort",
                "Caprifoliaceae (*Symphoricarpos*)",
            ),
            ch_next("pori smal (dwars), colpi lang", "50"),
        ],
    ),
    "50": step(
        "50",
        [
            ch_out(
                "ornamentatie fijn echinaat (stekeltjes kleiner dan 1 µm)",
                "Rosaceae (*Filipendula*)",
            ),
            ch_out(
                "ornamentatie ± psilaat",
                "Solanaceae (*Capsicum, Solanum* incl. tomaat)",
            ),
        ],
    ),
    "51": step(
        "51",
        [
            ch_out(
                "pollenkorrel in zijaanzicht elliptisch tot stomp rechthoekig",
                "Fabaceae (*Lotus corniculatus*)",
            ),
            ch_next(
                "pollenkorrel in zijaanzicht elliptisch tot stomp ruitvormig",
                "52",
            ),
        ],
    ),
    "52": step(
        "52",
        [
            ch_out(
                "pori onduidelijk (soms ‘H’-vormig)",
                "Cornaceae (*Cornus mas*)",
            ),
            ch_next(
                "pori duidelijk, rond tot langwerpig (dwars)",
                "53",
            ),
        ],
    ),
    "53": step(
        "53",
        [
            ch_out(
                "ornamentatie fijn echinaat (stekeltjes kleiner dan 1 µm)",
                "Rosaceae (*Filipendula*)",
            ),
            ch_next(
                "ornamentatie ± psilaat of onduidelijk rugulaat",
                "54",
            ),
        ],
    ),
    "54": step(
        "54",
        [
            ch_out(
                "pollenkorrel in zijaanzicht stomp ruitvormig, pori in bovenaanzicht op de hoekpunten",
                "Solanaceae (*Capsicum, Solanum* incl. tomaat)",
            ),
            ch_out(
                "pollenkorrel in zijaanzicht smal elliptisch, pori in bovenaanzicht tussen de hoekpunten",
                "Fagaceae (*Castanea sativa*)",
            ),
        ],
    ),
    "55": step(
        "55",
        [
            ch_out(
                "stekels met cylindrische basis, zuiltjes in infratectum recht, niet vertakt",
                "Caprifoliaceae (*Lonicera*)",
            ),
            ch_next(
                "stekels kegelvormig (soms erg klein), zuiltjes in infratectum vertakt of onduidelijk",
                "56",
            ),
        ],
    ),
    "56": step(
        "56",
        [
            ch_next(
                "stekels kleiner dan 1½ µm of onduidelijk",
                "57",
            ),
            ch_next("stekels groter dan 1½ µm", "58"),
        ],
    ),
    "57": step(
        "57",
        [
            ch_out(
                "pollenkorrel klein (20–30 µm)",
                "Asteraceae (*Artemisia*)",
            ),
            ch_out(
                "pollenkorrel groot (± 100 µm)",
                "Asteraceae (*Echinops sphaerocephalus*)",
            ),
        ],
    ),
    "58": step(
        "58",
        [
            ch_out(
                "zuiltjes in infratectum onduidelijk",
                "Asteraceae (*Aster, Helianthus, Senecio, Solidago*)",
            ),
            ch_next("zuiltjes in infratectum duidelijk", "59"),
        ],
    ),
    "59": step(
        "59",
        [
            ch_out(
                "zuiltjes onder de stekels langer en ten dele scheef (stervorm in bovenaanzicht)",
                "Asteraceae (*Carduus, Cirsium*)",
            ),
            ch_next(
                "zuiltjes loodrecht onder de stekels (geen stervorm in bovenaanzicht)",
                "60",
            ),
        ],
    ),
    "60": step(
        "60",
        [
            ch_out(
                "pollenkorrel meestal groter dan 40 µm",
                "Asteraceae (*Arctium*)",
            ),
            ch_out(
                "pollenkorrel meestal kleiner dan 40 µm",
                "Asteraceae (*Matricaria*)",
            ),
        ],
    ),
    "61": step(
        "61",
        [
            ch_out(
                "colpusmembranen (= nexine in/onder colpi) met duidelijke stekels",
                "Hippocastanaceae (*Aesculus hippocastanum*)",
            ),
            ch_next("colpusmembranen zonder stekels", "62"),
        ],
    ),
    "62": step(
        "62",
        [
            ch_out(
                "colpi in het midden niet versmald, ornamentatie striaat-reticulaat",
                "Simarubaceae (*Ailanthus altissima*)",
            ),
            ch_out(
                "colpi in het midden versmald, ornamentatie striaat-rugulaat",
                "Rosaceae (o.m. *Cotoneaster, Malus, Prunus, Rubus, Spiraea*)",
            ),
        ],
    ),
    "63": step(
        "63",
        [
            ch_out("pollenkorrel peervormig", "Boraginaceae (*Echium vulgare*)"),
            ch_next(
                "pollenkorrel ± rond tot ellipsvormig",
                "64",
            ),
        ],
    ),
    "64": step(
        "64",
        [
            ch_out(
                "pollenkorrel oblaat (P duidelijk kleiner dan E), colpi zeer kort, pori met sterk verdikte rand",
                "Tiliaceae (*Tilia*)",
            ),
            ch_next(
                "pollenkorrel ± rond tot prolaat (P groter of gelijk aan E), colpi vrij lang, pori zonder sterk verdikte rand",
                "65",
            ),
        ],
    ),
    "65": step(
        "65",
        [
            ch_out(
                "wand dikker dan 2 µm, zuiltjes in infratectum zeer duidelijk, vertakt",
                "Polygonaceae (*Fagopyrum esculentum*)",
            ),
            ch_next(
                "wand dunner dan 2 µm, zuiltjes in infratectum klein of onduidelijk",
                "66",
            ),
        ],
    ),
    "66": step(
        "66",
        [
            ch_out(
                "netwerk onduidelijk",
                "Fabaceae (*Medicago, Melilotus, Vicia cracca, Vicia sepium*)",
            ),
            ch_next("netwerk duidelijk", "67"),
        ],
    ),
    "67": step(
        "67",
        [
            ch_out(
                "pollenkorrel kleiner dan 40 µm",
                "Fabaceae (*Trifolium, Vicia*)",
            ),
            ch_out(
                "pollenkorrel groter dan 40 µm",
                "Fabaceae (*Pisum sativum, Trifolium incarnatum, Vicia faba*)",
            ),
        ],
    ),
    "68": step(
        "68",
        [
            ch_out(
                "netwerk onduidelijk, naar de polen toe grover en vaak incompleet",
                "Vitaceae (*Vitis vinifera*)",
            ),
            ch_next("netwerk duidelijk", "69"),
        ],
    ),
    "69": step(
        "69",
        [
            ch_out(
                "mazen kleiner dan 1 µm",
                "Clusiaceae (*Hypericum*)",
            ),
            ch_next("mazen groter dan 1 µm", "70"),
        ],
    ),
    "70": step(
        "70",
        [
            ch_out(
                "pollenkorrel groter dan 40 µm",
                "Cucurbitaceae (*Bryonia dioica*)",
            ),
            ch_next("pollenkorrel kleiner dan 40 µm", "71"),
        ],
    ),
    "71": step(
        "71",
        [
            ch_out(
                "wand meestal dikker dan 2 µm, pori hoger dan breed",
                "Celastraceae (*Euonymus*)",
            ),
            ch_out(
                "wand meestal dunner dan 2 µm, pori breder dan hoog of onduidelijk",
                "Caprifoliaceae (*Sambucus nigra*)",
            ),
        ],
    ),
    "72": step(
        "72",
        [
            ch_next(
                "pollenkorrel met drie equatoriale pori (triporaat)",
                "73",
            ),
            ch_next(
                "pollenkorrel met meer dan drie equatoriale pori (stephanoporaat)",
                "75",
            ),
            ch_next(
                "pollenkorrel met meer dan drie verspreide (niet-equatoriale) pori (periporaat)",
                "76",
            ),
        ],
    ),
    "73": step(
        "73",
        [
            ch_out(
                "pori groot, duidelijk uitstekend (pollenkorrels soms met elkaar verbonden)",
                "Onagraceae (*Chamerion angustifolium, Epilobium, Oenothera*)",
            ),
            ch_out(
                "pori iets uitstekend, ornamentatie echinaat (stekels groter dan 1 µm)",
                "Caprifoliaceae (*Weigelia*)",
            ),
            ch_next(
                "pori niet uitstekend, indien ornamentatie echinaat dan stekels kleiner dan 1 µm",
                "74",
            ),
        ],
    ),
    "74": step(
        "74",
        [
            ch_out(
                "pollenkorrel kleiner dan 50 µm, ornamentatie echinaat",
                "Campanulaceae (*Campanula*)",
            ),
            ch_out(
                "pollenkorrel ± 50 µm, ornamentatie reticulaat",
                "Cucurbitaceae (*Cucumis sativus*)",
            ),
            ch_out(
                "pollenkorrel groter dan 60 µm, ornamentatie echinaat",
                "Dipsacaceae (*Dipsacus, Knautia*)",
            ),
        ],
    ),
    "75": step(
        "75",
        [
            ch_out(
                "pollenkorrel met vier pori, ornamentatie fijn echinaat (stekeltjes kleiner dan 1 µm)",
                "Campanulaceae (*Campanula*)",
            ),
            ch_out(
                "pollenkorrel met vier tot elf pori, ornamentatie striaat of perforaat",
                "Polemoniaceae (*Gilia*)",
            ),
        ],
    ),
    "76": step(
        "76",
        [
            ch_out(
                "ornamentatie verrucaat of onregelmatig golvend",
                "Plantaginaceae (*Plantago*)",
            ),
            ch_out(
                "ornamentatie fijn echinaat (stekeltjes kleiner dan 1 µm)",
                "Caryophyllaceae (diverse geslachten)",
            ),
            ch_next("ornamentatie reticulaat", "77"),
            ch_next(
                "ornamentatie psilaat, perforaat of scabraat",
                "78",
            ),
        ],
    ),
    "77": step(
        "77",
        [
            ch_out(
                "pori ± even groot als de mazen van het netwerk (mazen groter dan 3 µm)",
                "Polemoniaceae (*Phlox*)",
            ),
            ch_out(
                "pori ± even groot als de mazen van het netwerk (mazen kleiner dan 3 µm)",
                "Thymelaeaceae (*Daphne*)",
            ),
            ch_out(
                "pori duidelijk groter dan de mazen van het netwerk",
                "Caryophyllaceae (*Silene*)",
            ),
        ],
    ),
    "78": step(
        "78",
        [
            ch_out("pollenkorrel peervormig", "Cyperaceae (*Carex, Scirpus*)"),
            ch_next(
                "pollenkorrel ± rond tot ellipsvormig",
                "79",
            ),
        ],
    ),
    "79": step(
        "79",
        [
            ch_out(
                "pori vooral op één helft van de pollenkorrel",
                "Juglandaceae (*Juglans regia*)",
            ),
            ch_next("pori over de hele pollenkorrel verspreid", "80"),
        ],
    ),
    "80": step(
        "80",
        [
            ch_out(
                "pori omgeven (en soms verbonden) door tectum-loze (scabrate) zones",
                "Grossulariaceae (*Ribes*)",
            ),
            ch_next(
                "pori niet omgeven of verbonden door tectum-loze (scabrate) zones",
                "81",
            ),
        ],
    ),
    "81": step(
        "81",
        [
            ch_out(
                "vier tot twaalf pori, pori zonder massieve rand",
                "Ranunculaceae (*Thalictrum*)",
            ),
            ch_next(
                "meestal meer dan tien pori, pori met massieve rand (annulus)",
                "82",
            ),
        ],
    ),
    "82": step(
        "82",
        [
            ch_out(
                "meestal meer dan 50 pori, tectum zonder perforaties",
                "Amaranthaceae (diverse geslachten), Chenopodiaceae (diverse geslachten)",
            ),
            ch_out(
                "minder dan 50 pori, tectum met perforaties",
                "Caryophyllaceae (diverse geslachten)",
            ),
        ],
    ),
}


def validate(steps: dict[str, dict]) -> list[str]:
    errs: list[str] = []
    for sid, node in steps.items():
        for i, c in enumerate(node["choices"]):
            if "next" in c and "outcome" in c:
                errs.append(f"{sid} choice {i}: both next and outcome")
            if "next" not in c and "outcome" not in c:
                errs.append(f"{sid} choice {i}: missing next and outcome")
            if c.get("next") and c["next"] not in steps:
                errs.append(f"{sid} -> missing step {c['next']}")
    return errs


def main() -> None:
    errs = validate(STEPS)
    if errs:
        raise SystemExit("Validation failed:\n" + "\n".join(errs))

    doc = {
        "meta": {
            "key": "vanderham_pollentabel_scans",
            "title": "Pollentabel (van der Ham) — interactieve structuur uit scans",
            "locale": "nl",
            "source": "Handgetypte transcriptie van door de gebruiker aangeleverde paginascans (april 2026). "
            "Geen koppeling met docs/keys/vanderham/*.md.",
            "note": "Druk-cijfers tussen haakjes in het boek zijn weggelaten. "
            "Stap 11: tweede optie is op de eerste scan afgekapt.",
            "stepCount": len(STEPS),
            "start": "1",
        },
        "start": "1",
        "steps": STEPS,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(STEPS)} steps)")


if __name__ == "__main__":
    main()
