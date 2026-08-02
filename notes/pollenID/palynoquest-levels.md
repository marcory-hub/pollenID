**One-line purpose:** PalynoQuest quiz pools by niveau
**Short summary:** Taxa in each PalynoQuest level from current manifests + pollen.json
**Agent:** list for human review of learning curve tiers
**SoT:** no
**Main Index:** [[__pollenID]]

---

# PalynoQuest niveaus

Generated from `docs/assets/manifests/palynoquest-items.json` + `docs/data/pollen.json`.

Filter rules (`docs/javascripts/palynoquest.js`):

- **Niveau 1:** `learning_priority_rank` ≤ 20
- **Niveau 2:** any `learning_priority_rank` (includes niveau 1)
- **Niveau 3:** full PalynoQuest quiz pool

`monofloral_honey_page` is **not** used for these tiers.

Counts (quiz-eligible taxa only): L1 **13**, L2 **35**, L3 **272**.

## Niveau 1 — Vaak in NL-honing

13 taxa (`learning_priority_rank` ≤ 20).

| Rank | pollen_key | Latijn | Nederlands |
| ---: | :--- | :--- | :--- |
| 1 | `brassica_typ` | Brassica typ | kool type |
| 2 | `prunus_pirus_typ` | Prunus pirus | Pruim/Peer type |
| 3 | `rubus_typ` | Rubus typ | braam/framboos type |
| 4 | `taraxacum_typ` | Taraxacum typ | paardenbloem type |
| 5 | `centaurea_cyanus` | Centaurea cyanus | korenbloem |
| 6 | `trifolium_repens` | Trifolium repens | witte klaver |
| 10 | `vicia_typ` | Vicia typ | Wikke type |
| 11 | `acer_platanoides` | Acer platanoides | Noorse esdoorn |
| 12 | `anthriscus_typ` | Anthriscus typ | Berenklauw type |
| 13 | `salix_typ` | Salix typ | wilg type |
| 15 | `tilia_typ` | Tilia typ | linde type |
| 16 | `ranunculus_typ` | Ranunculus typ | Ranonkel type |
| 18 | `raphanus_typ` | Raphanus typ | Radijs type |

## Niveau 2 — Alle prioriteit

35 taxa (any `learning_priority_rank`). Includes niveau 1.

### Alleen nieuw t.o.v. niveau 1 (rank ≥ 21): 22 taxa

| Rank | pollen_key | Latijn | Nederlands |
| ---: | :--- | :--- | :--- |
| 21 | `lamium_typ` | Lamium typ | dovenetel type |
| 22 | `myosotis_typ` | Myosotis typ | vergeet-me-nietje type |
| 23 | `phacelia_typ` | Phacelia typ | phacelia type |
| 26 | `ailanthus_altissima` | Ailanthus altissima | hemelboom |
| 28 | `sinapis_typ` | Sinapis typ | Mosterd type |
| 31 | `spiraea_typ` | Spiraea typ | spirea type |
| 32 | `allium_typ` | Allium typ | Look type |
| 34 | `cornus_sanguinea` | Cornus sanguinea | rode kornoelje |
| 35 | `populus_typ` | Populus typ | populier type |
| 37 | `achillea_typ` | Achillea typ | Duizendblad type |
| 39 | `castanea_sativa` | Castanea sativa | tamme kastanje |
| 44 | `crataegus_typ` | Crataegus typ | meidoorn type |
| 45 | `trifolium_pratense` | Trifolium pratense | rode klaver |
| 49 | `silene_flos_cuculi` | Silene flos-cuculi | echte koekoeksbloem |
| 50 | `asparagus_typ` | Asparagus typ | Asperge type |
| 64 | `calluna_vulgaris` | Calluna vulgaris | struikheide |
| 65 | `heracleum_typ` | Heracleum typ | Reuzenkruiskruid type |
| 66 | `cynoglossum_typ` | Cynoglossum typ | hondstong type |
| 69 | `centaurea_typ` | Centaurea typ | Centaurea type |
| 71 | `cornus_mas` | Cornus mas | gele kornoelje |
| 75 | `centaurea_jacea` | Centaurea jacea | knoopkruid |
| 77 | `helianthus_typ` | Helianthus typ | zonnebloem type |

### Volledige niveau-2 lijst

| Rank | pollen_key | Latijn | Nederlands |
| ---: | :--- | :--- | :--- |
| 1 | `brassica_typ` | Brassica typ | kool type |
| 2 | `prunus_pirus_typ` | Prunus pirus | Pruim/Peer type |
| 3 | `rubus_typ` | Rubus typ | braam/framboos type |
| 4 | `taraxacum_typ` | Taraxacum typ | paardenbloem type |
| 5 | `centaurea_cyanus` | Centaurea cyanus | korenbloem |
| 6 | `trifolium_repens` | Trifolium repens | witte klaver |
| 10 | `vicia_typ` | Vicia typ | Wikke type |
| 11 | `acer_platanoides` | Acer platanoides | Noorse esdoorn |
| 12 | `anthriscus_typ` | Anthriscus typ | Berenklauw type |
| 13 | `salix_typ` | Salix typ | wilg type |
| 15 | `tilia_typ` | Tilia typ | linde type |
| 16 | `ranunculus_typ` | Ranunculus typ | Ranonkel type |
| 18 | `raphanus_typ` | Raphanus typ | Radijs type |
| 21 | `lamium_typ` | Lamium typ | dovenetel type |
| 22 | `myosotis_typ` | Myosotis typ | vergeet-me-nietje type |
| 23 | `phacelia_typ` | Phacelia typ | phacelia type |
| 26 | `ailanthus_altissima` | Ailanthus altissima | hemelboom |
| 28 | `sinapis_typ` | Sinapis typ | Mosterd type |
| 31 | `spiraea_typ` | Spiraea typ | spirea type |
| 32 | `allium_typ` | Allium typ | Look type |
| 34 | `cornus_sanguinea` | Cornus sanguinea | rode kornoelje |
| 35 | `populus_typ` | Populus typ | populier type |
| 37 | `achillea_typ` | Achillea typ | Duizendblad type |
| 39 | `castanea_sativa` | Castanea sativa | tamme kastanje |
| 44 | `crataegus_typ` | Crataegus typ | meidoorn type |
| 45 | `trifolium_pratense` | Trifolium pratense | rode klaver |
| 49 | `silene_flos_cuculi` | Silene flos-cuculi | echte koekoeksbloem |
| 50 | `asparagus_typ` | Asparagus typ | Asperge type |
| 64 | `calluna_vulgaris` | Calluna vulgaris | struikheide |
| 65 | `heracleum_typ` | Heracleum typ | Reuzenkruiskruid type |
| 66 | `cynoglossum_typ` | Cynoglossum typ | hondstong type |
| 69 | `centaurea_typ` | Centaurea typ | Centaurea type |
| 71 | `cornus_mas` | Cornus mas | gele kornoelje |
| 75 | `centaurea_jacea` | Centaurea jacea | knoopkruid |
| 77 | `helianthus_typ` | Helianthus typ | zonnebloem type |

## Niveau 3 — Alles

272 quiz-eligible taxa (full PalynoQuest pool).

### Met `learning_priority_rank`

| Rank | pollen_key | Latijn | Nederlands |
| ---: | :--- | :--- | :--- |
| 1 | `brassica_typ` | Brassica typ | kool type |
| 2 | `prunus_pirus_typ` | Prunus pirus | Pruim/Peer type |
| 3 | `rubus_typ` | Rubus typ | braam/framboos type |
| 4 | `taraxacum_typ` | Taraxacum typ | paardenbloem type |
| 5 | `centaurea_cyanus` | Centaurea cyanus | korenbloem |
| 6 | `trifolium_repens` | Trifolium repens | witte klaver |
| 10 | `vicia_typ` | Vicia typ | Wikke type |
| 11 | `acer_platanoides` | Acer platanoides | Noorse esdoorn |
| 12 | `anthriscus_typ` | Anthriscus typ | Berenklauw type |
| 13 | `salix_typ` | Salix typ | wilg type |
| 15 | `tilia_typ` | Tilia typ | linde type |
| 16 | `ranunculus_typ` | Ranunculus typ | Ranonkel type |
| 18 | `raphanus_typ` | Raphanus typ | Radijs type |
| 21 | `lamium_typ` | Lamium typ | dovenetel type |
| 22 | `myosotis_typ` | Myosotis typ | vergeet-me-nietje type |
| 23 | `phacelia_typ` | Phacelia typ | phacelia type |
| 26 | `ailanthus_altissima` | Ailanthus altissima | hemelboom |
| 28 | `sinapis_typ` | Sinapis typ | Mosterd type |
| 31 | `spiraea_typ` | Spiraea typ | spirea type |
| 32 | `allium_typ` | Allium typ | Look type |
| 34 | `cornus_sanguinea` | Cornus sanguinea | rode kornoelje |
| 35 | `populus_typ` | Populus typ | populier type |
| 37 | `achillea_typ` | Achillea typ | Duizendblad type |
| 39 | `castanea_sativa` | Castanea sativa | tamme kastanje |
| 44 | `crataegus_typ` | Crataegus typ | meidoorn type |
| 45 | `trifolium_pratense` | Trifolium pratense | rode klaver |
| 49 | `silene_flos_cuculi` | Silene flos-cuculi | echte koekoeksbloem |
| 50 | `asparagus_typ` | Asparagus typ | Asperge type |
| 64 | `calluna_vulgaris` | Calluna vulgaris | struikheide |
| 65 | `heracleum_typ` | Heracleum typ | Reuzenkruiskruid type |
| 66 | `cynoglossum_typ` | Cynoglossum typ | hondstong type |
| 69 | `centaurea_typ` | Centaurea typ | Centaurea type |
| 71 | `cornus_mas` | Cornus mas | gele kornoelje |
| 75 | `centaurea_jacea` | Centaurea jacea | knoopkruid |
| 77 | `helianthus_typ` | Helianthus typ | zonnebloem type |

### Zonder `learning_priority_rank` (alleen in niveau 3)

237 taxa.

| Rank | pollen_key | Latijn | Nederlands |
| ---: | :--- | :--- | :--- |
|  | `acer_campestre` | Acer campestre | Spaanse aak |
|  | `acer_japonicum` | Acer japonicum | Japanse esdoorn |
|  | `acer_negundo` | Acer negundo | verderesdoorn |
|  | `acer_palmatum` | Acer palmatum | Japanse esdoorn |
|  | `acer_pseudoplatanus` | Acer pseudoplatanus | Esdoorn |
|  | `aconitum_typ` | Aconitum typ | ridderspoor type |
|  | `aesculus_carnea` | Aesculus carnea | rode paardekastanje |
|  | `aesculus_hippocastanum` | Aesculus hippocastanum | paardenkastanje |
|  | `agrimonia_eupatoria` | Agrimonia eupatoria | gewone agrimonie |
|  | `agrimonia_odorata` | Agrimonia odorata | welriekende agrimonie |
|  | `ajuga_reptans` | Ajuga reptans | zenegroen |
|  | `allium_cepa` | Allium cepa | ui of tuinui |
|  | `allium_schoenoprasum` | Allium schoenoprasum | bieslook |
|  | `allium_ursinum` | Allium ursinum | daslook |
|  | `alnus_glutinosa` | Alnus glutinosa | zwarte els (zwart - donkere schors, glutinosa - jonge knoppen zijn kleverig) |
|  | `alyssum_typ` | Alyssum typ | schildzaad type |
|  | `ambrosia_artemisiifolia` | Ambrosia artemisiifolia | Ambrosia |
|  | `anchusa_arvensis` | Anchusa arvensis | kromhals |
|  | `anchusa_officinalis` | Anchusa officinalis | gewone ossentong |
|  | `anemone_typ` | Anemone typ | anemoon type |
|  | `anethum_graveolens` | Anethum graveolens | dille |
|  | `anthemis_nobilis` | Anthemis nobilis | roomse kamille |
|  | `antirrhinum_majus` | Antirrhinum majus | grote leeuwebek |
|  | `arctium_lappa` | Arctium lappa | grote klis |
|  | `arctium_minus` | Arctium minus | klit |
|  | `armeria_maritima` | Armeria maritima | strandkruid |
|  | `artemisia_typ` | Artemisia typ | bijvoet/alsem type |
|  | `artemisia_vulgaris` | Artemisia vulgaris | bijvoet |
|  | `aruncus_dioicus` | Aruncus dioicus | geitenbaard |
|  | `asphodelus_aestivus` | Asphodelus aestivus | gewone affodil |
|  | `aster_typ` | Aster typ | aster type |
|  | `astrantia_major` | Astrantia major | Zeeuws knoopje |
|  | `berberis_typ` | Berberis typ | zuurbes type |
|  | `berberis_vulgaris` | Berberis vulgaris | zuurbes |
|  | `betula_pendula` | Betula pendula | ruwe berk |
|  | `bidens_typ` | Bidens typ | tandzaad type |
|  | `borago_officinalis` | Borago officinalis | borage |
|  | `borreria_verticilata` | Borreria verticilata | Borreria |
|  | `brassica_napus` | Brassica napus | koolzaad |
|  | `bryonia_dioica` | Bryonia dioica | heggerank |
|  | `buddleja_davidii` | Buddleja davidii | vlinderstruik |
|  | `cakile_maritima` | Cakile maritima | zeeraket |
|  | `calendula_officinalis` | Calendula officinalis | goudsbloem |
|  | `calystegia_sepium` | Calystegia sepium | haagwinde |
|  | `campanula_latifolia` | Campanula latifolia | Breedbladig klokje |
|  | `campanula_portenschlagiana` | Campanula portenschlagiana | Dalmatiëklokje |
|  | `cannabis_sativa` | Cannabis sativa | cannabis |
|  | `cardamine_pratensis` | Cardamine pratensis | pinksterbloem |
|  | `carduus_nutans` | Carduus nutans | knikkende distel |
|  | `carex_typ` | Carex typ | zegge type |
|  | `carlina_aucalis` | Carlina aucalis | zilverdistel |
|  | `carpinus_betulus` | Carpinus betulus | haagbeuk |
|  | `carthamus_lanatus` | Carthamus lanatus | wollige saffloer |
|  | `carthamus_tinctorius` | Carthamus tinctorius | saffloer |
|  | `carum_carvi` | Carum carvi | karwijzaad |
|  | `centaurea_montana` | Centaurea montana | bergcentaurie |
|  | `centranthus_ruber` | Centranthus ruber | rode spoorbloem |
|  | `ceratonia_silqua` | Ceratonia silqua | Johannesbroodboom |
|  | `cercis_siliquastrum` | Cercis siliquastrum | Judasboom |
|  | `chelidonium_majus` | Chelidonium majus | Chelidonium majus |
|  | `cichorium_intybus` | Cichorium intybus | cichorei |
|  | `cirsium_arvense` | Cirsium arvense | akkerdistel |
|  | `cirsium_vulgare` | Cirsium vulgare | speerdistel |
|  | `cistus_salviifolius` | Cistus salviifolius | Saliebladige zistroos |
|  | `citrullus_lanatus` | Citrullus lanatus | watermeloen |
|  | `clematis_vitalba` | Clematis vitalba | bosrank |
|  | `clethra_alnifolia` | Clethra alnifolia | Clethra |
|  | `coffea_typ` | Coffea typ | koffie type |
|  | `colchicum_autumnale` | Colchicum autumnale | herfsttijloos |
|  | `convolvulus_arvensis` | Convolvulus arvensis | akkerwinde |
|  | `corylopsis_pauciflora` | Corylopsis pauciflora | schijnhazelaar |
|  | `corylus_avellana` | Corylus avellana | hazelaar |
|  | `cosmos_typ` | Cosmos typ | cosmea type |
|  | `cotoneaster_intergerrimus` | Cotoneaster intergerrimus | wilde dwergmispel |
|  | `crataegus_monogyna` | Crataegus monogyna | eenstijlige meidoorn |
|  | `crocus_typ` | Crocus typ | crocus type |
|  | `cucumis_sativus` | Cucumis sativus | komkommer/aug |
|  | `cytisus_typ` | Cytisus typ | brem type |
|  | `daphne_mezereum` | Daphne mezereum | rood peperboompje |
|  | `datura_stramonium` | Datura stramonium | doornappel |
|  | `daucus_carota` | Daucus carota | wilde wortel |
|  | `davidia_involucrata` | Davidia involucrata | vaantjesboom |
|  | `deutzia_typ` | Deutzia typ | Deutzia type |
|  | `digitalis_purpurea` | Digitalis purpurea | vingerhoedskruid |
|  | `diplotaxis_tenuifolia` | Diplotaxis tenuifolia | rucola |
|  | `dipsacus_typ` | Dipsacus typ | kaardebol type |
|  | `dryas_octopetala` | Dryas octopetala | zilverkruid |
|  | `echinops_sphaerocephalus` | Echinops sphaerocephalus | Echinops sphaerocephalus |
|  | `echium_vulgare` | Echium vulgare | slangenkruid |
|  | `elaeagnus_angustifolia` | Elaeagnus angustifolia | smalbladige olijfwilg |
|  | `epilobium_angustifolium` | Epilobium angustifolium | wilgenroosje |
|  | `erica_tetralix` | Erica tetralix | dopheide |
|  | `eruca_sativa` | Eruca sativa | Eruca |
|  | `eschscholzia_californica` | Eschscholzia californica | slaapmutsje |
|  | `eucalyptus_camaldulensis` | Eucalyptus camaldulensis | eucalyptus |
|  | `euonymus_europaeus` | Euonymus europaeus | wilde kardinaalsmuts |
|  | `eupatorium_cannabinum` | Eupatorium cannabinum | leverkruid |
|  | `euphorbia_typ` | Euphorbia typ | euphorbia type |
|  | `fagopyrum_esculentum` | Fagopyrum esculentum | boekweit |
|  | `fallopia_baldschuanica` | Fallopia baldschuanica | bruidsluier |
|  | `filipendula_ulmaria` | Filipendula ulmaria | moerasspirea |
|  | `filipendula_vulgaris` | Filipendula vulgaris | knolspirea |
|  | `fragaria_vesca` | Fragaria vesca | bosaardbei |
|  | `fragaria_viridis` | Fragaria viridis | heuvelaardbei |
|  | `frangula_alnus` | Frangula alnus | vuilboom |
|  | `fraxinus_ornus` | Fraxinus ornus | es |
|  | `fumaria_officinalis` | Fumaria officinalis | duivekervel |
|  | `galinsoga_typ` | Galinsoga typ | knopkruid type |
|  | `galium_odoratum` | Galium odoratum (syn Asperula odorata) | lievevrouwebedstro |
|  | `geranium_typ` | Geranium typ | ooievaarsbek type |
|  | `geum_rivale` | Geum rivale | 23.2-30.6 |
|  | `geum_urbanum` | Geum urbanum | geel nagelkruid |
|  | `gilia_capitata` | Gilia Capitata |  |
|  | `hieracium_typ` | Hieracium typ | havikskruid type |
|  | `hippophae_rhamnoides` | Hippophae rhamnoides | duindoorn |
|  | `humulus_typ` | Humulus typ | hop type |
|  | `hyacinthus_orientalis` | Hyacinthus orientalis | hyacint |
|  | `hydrangea_typ` | Hydrangea typ | hortensia type |
|  | `hypericum_perforatum` | Hypericum perforatum | St. Janskruid |
|  | `ilex_aquifolium` | Ilex aquifolium | hulst |
|  | `impatiens_balsamina` | Impatiens balsamina | tuinbalsemien |
|  | `juglans_regia` | Juglans regia | walnootboom |
|  | `juncus_jacquinii` | Juncus jacquinii |  |
|  | `juniperus_communis` | Juniperus communis | gewone jeneverbes |
|  | `knautia_typ` | Knautia typ | beemdkroon type |
|  | `kolkwitzia_amabilis` | Kolkwitzia amabilis | koninginnenstruik |
|  | `lavandula_angustifolia` | Lavandula angustifolia | lavendel |
|  | `ligustrum_vulgare` | Ligustrum vulgare | liguster |
|  | `lilium_typ` | Lilium typ | lelie type |
|  | `limnanthes_douglasii` | Limnanthes douglasii | moerasbloem |
|  | `limonium_vulgare` | Limonium vulgare | lamsoor |
|  | `linaria_cymbalaria` | Linaria cymbalaria | muurleeuwenbek |
|  | `linaria_vulgaris` | Linaria vulgaris | vlasleeuwenbek |
|  | `linum_usitatissimum` | Linum usitatissimum | vlas |
|  | `liriodendron_tulipifera` | Liriodendron tulipifera | tulpenboom |
|  | `lonicera_typ` | Lonicera typ | kamperfoelie type |
|  | `lotus_corniculatus` | Lotus corniculatus | rolklaver |
|  | `lysimachia_vulgaris` | Lysimachia vulgaris | grote wederik |
|  | `lythrum_salicaria` | Lythrum salicaria | kattenstaart |
|  | `magnolia_kobus` | Magnolia kobus | Magnolia kobus |
|  | `mahonia_aquifolium` | Mahonia aquifolium | mahonie |
|  | `malus_typ` | Malus typ | appel type |
|  | `malva_typ` | Malva typ | kaasjeskruid type |
|  | `mangifera_indica` | Mangifera indica | mango |
|  | `matricaria_chamomilla` | Matricaria chamomilla | echte kamille |
|  | `medicago_sativa` | Medicago sativa | luzerne |
|  | `melampyrum_typ` | Melampyrum typ | hengel type |
|  | `melilotus_officinalis` | Melilotus officinalis | citroengele honingklaver |
|  | `mercurialis_typ` | Mercurialis typ | bingelkruid type |
|  | `morus_alba` | Morus alba | witte moerbei |
|  | `narcissus_typ` | Narcissus typ | narcis type |
|  | `nicotiana_glauca` | Nicotiana glauca | siertabak |
|  | `nicotiana_tabacum` | Nicotiana tabacum | tabak |
|  | `nigella_sativa` | Nigella sativa | zwarte komijn |
|  | `nuphar_lutea` | Nuphar lutea | gele plomp |
|  | `nymphaea_alba` | Nymphaea alba | waterlelie |
|  | `olea_europaea` | Olea europaea | olijf |
|  | `onosis_spinoza` | Ononis spinosa | kattendoorn |
|  | `osmanthus_typ` | Osmanthus typ | Osmanthus type |
|  | `parnassia_palustris` | Parnassia palustris | Parnassia |
|  | `phaseolus_coccineus` | Phaseolus coccineus | pronkboon |
|  | `philadelphus_coronarius` | Philadelphus coronarius | boerenjasmijn |
|  | `phlox_typ` | Phlox typ | phlox type |
|  | `photinia_typ` | Photinia typ | glansmispel type |
|  | `picea_omorika` | Picea omorika | Servische spar |
|  | `pisum_typ` | Pisum typ | erwt type |
|  | `plantago_lanceolata` | Plantago Lanceolata | smalle weegbree |
|  | `platanus_hispanica` | Platanus hispanica | gewone plataan |
|  | `polemonium_caeruleum` | Polemonium caeruleum | Jacobs ladder |
|  | `potentilla_anserina` | Potentilla anserina | zilverschoon |
|  | `primula_vulgaris` | Primula vulgaris | sleutelbloem |
|  | `prunus_avium` | Prunus avium | zoete kers |
|  | `prunus_laurocerasus` | Prunus laurocerasus | laurierkers |
|  | `prunus_padus` | Prunus padus | vogelkers |
|  | `prunus_spinosa` | Prunus spinosa | sleedoorn |
|  | `prunus_spinoza` | Prunus spinosa | sleedoorn |
|  | `punica_granatum` | Punica granatum | granaatappel |
|  | `quercus_robur` | Quercus robur | zomereik |
|  | `ranunculus_ficaria` | Ranunculus ficaria | gewoon speenkruid |
|  | `reseda_lutea` | Reseda lutea | wilde reseda |
|  | `rhododendron_typ` | Rhododendron typ | rhododendron type |
|  | `ribes_sanguineum` | Ribes sanguineum | rode ribes |
|  | `robinia_pseudoacacia` | Robinia pseudoacacia | valse acacia |
|  | `rosa_canina` | Rosa canina | hondsroos |
|  | `rosa_pimpinellifolia` | Rosa pimpinellifolia | duinroos |
|  | `rosa_rubiginosa` | Rosa rubiginosa | egelantier |
|  | `rosmarinus_officinalis` | Rosmarinus officinalis | rozemarijn |
|  | `rubus_fructicosus` | Rubus fructicosus | braam |
|  | `rubus_idaeus` | Rubus idaeus | framboos |
|  | `rubus_saxatilis` | Rubus saxatilis | steenbraam |
|  | `rumex_obtusifolius` | Rumex obtusifolius | zuring |
|  | `ruta_graveolens` | Ruta graveolens | wijnruit |
|  | `salix_caprea` | Salix caprea | boswilg |
|  | `sambucus_ebulus` | Sambucus ebulus | bergvlier |
|  | `sambucus_nigra` | Sambucus nigra | vlier |
|  | `sanguisorba_minor` | Sanguisorba minor | kleine pimpernel |
|  | `sanguisorba_officinalis` | Sanguisorba officinalis | grote pimpernel |
|  | `saxifraga_rotundifolia` | Saxifraga rotundifolia | rondbladige steenbreek |
|  | `scabiosa_columbar` | Scabiosa columbar | duifkruid |
|  | `scilla_nonscripta` | Scilla nonscripta | wilde hyacint |
|  | `sedum_typ` | Sedum typ | vetblad type |
|  | `senecio_typ` | Senecio typ | kruiskruid type |
|  | `sibbaldia_procumbens` | Sibbaldia procumbens |  |
|  | `silene_cucubalis` | Silene cucubalis | blaassilene |
|  | `skimmia_typ` | Skimmia typ | Skimmia type |
|  | `solanum_dulcamara` | Solanum dulcamara | bitterzoet |
|  | `solanum_lycopersicum` | Solanum lycopersicum | tomaat |
|  | `solidago_virgaurea` | Solidago virgaurea | echte guldenroede |
|  | `sonchus_arvensis` | Sonchus arvensis | akkermelkdistel |
|  | `sophora_japonica` | Sophora japonica | honingboom |
|  | `sorbus_aucuparia` | Sorbus aucuparia | wilde lijsterbes |
|  | `staphylea_pinnata` | Staphylea pinnata | pimpernoot |
|  | `succisa_pratensis` | Succisa pratensis | blauwe knoop |
|  | `symphoricarpos_typ` | Symphoricarpos typ | sneeuwbes type |
|  | `symphytum_officinale` | Symphytum officinale | smeerwortel |
|  | `tamarix_typ` | Tamarix typ | Tamarix type |
|  | `taxus_baccata` | Taxus baccata | taxus, venijnboom |
|  | `teucrium_chamaedrys` | Teucrium chamaedrys | echte gamander |
|  | `thalictrum_typ` | Thalictrum typ | ruit type |
|  | `theobroma_cacao` | Theobroma cacao | cacao |
|  | `thuja_typ` | Thuja typ | Thuja type |
|  | `tragopogon_typ` | Tragopogon typ | morgenster type |
|  | `tripolium_pannonicum` | Tripolium pannonicum | zeeaster |
|  | `tulipa_typ` | Tulipa typ | tulp type |
|  | `ulex_typ` | Ulex typ | gaspeldoorn type |
|  | `urtica_typ` | Urtica typ | brandnetel type |
|  | `vaccinium_vitis_idaea` | Vaccinium vitis-idaea | rode bosbes |
|  | `valeriana_officinalis` | Valeriana officinalis | echte valeriaan |
|  | `verbascum_nigrum` | Verbascum nigrum | koningskaars |
|  | `verbena_officinalis` | Verbena officinalis | ijzerhard |
|  | `veronica_typ` | Veronica typ | ereprijs type |
|  | `viburnum_opulus` | Viburnum opulus | Gelderse roos |
|  | `viola_typ` | Viola typ | viool type |
|  | `vitis_vinifera` | Vitis vinifera | druif |
|  | `weigelia_diervilla_typ` | Weigelia/Diervilla typ | Weigelia type |
|  | `xanthium_strumarium` | Xanthium strumarium | late stekelnoot |
|  | `zea_mays` | Zea mays | maïs |

