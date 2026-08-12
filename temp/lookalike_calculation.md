# Morph lookalike clustering (one-shot)

Generated read-only from `data/pollen.yaml`, `docs/keys/**`,
`temp/reports/key-path-conflicts.md`, and `data/lookalike_review.yaml`.

## 1. Method summary

- **Goal:** taxa whose pollen are hard to tell apart under LM (morph similarity), not key-topology lookalikes.
- **Matching:** exact `pollen_key` only; no synonym merge; no `*_typ` representative fill.
- **Features:** YAML size / aperture / sculpture / shape / ornamentation / `pollen_class_beug` / controlled.*; key endpoint + path morph tokens; Kerkvliet sections marked analytic.
- **Conflict mask:** size and/or sculpture dimensions masked for taxa in the key-path conflict table.
- **Clustering:** pure-Python agglomerative; UPGMA within aperture-family blocks; Kruskal single-link within blocks n>200.
- **Non-goals:** no promotion to lookalikes; no edits outside this report.

## 2. Feature inventory

| Metric | Count |
| :--- | ---: |
| Taxa in `pollen.yaml` | 1698 |
| Taxa with ≥1 usable morph feature | 961 |
| Clusterable (≥2 feature dims) | 917 |
| Sparse / appendix (<2 dims) | 44 |
| Conflict-masked taxa | 34 |
| Key-enriched taxa (any key hit) | 519 |
| Learning-priority ranked in clusterable | 42 |
| Already-decided pairs (confirmed/different) | 95 |

### Conflict-masked taxa

- `aesculus_hippocastanum`: masked [sculpt]
- `agrimonia_eupatoria`: masked [sculpt]
- `agrimonia_odorata`: masked [sculpt]
- `allium_ursinum`: masked [size]
- `arctium_minus`: masked [size]
- `carpinus_betulus`: masked [size]
- `centaurea_cyanus`: masked [sculpt]
- `centaurea_montana`: masked [size]
- `colchicum_autumnale`: masked [size]
- `convolvulus_arvensis`: masked [size]
- `coriandrum_sativum`: masked [size]
- `cornus_sanguinea`: masked [size]
- `cotoneaster_intergerrimus`: masked [sculpt]
- `dryas_octopetala`: masked [size]
- `hedera_helix`: masked [size]
- `limonium_vulgare`: masked [size]
- `linum_usitatissimum`: masked [size]
- `liriodendron_tulipifera`: masked [size]
- `medicago_sativa`: masked [size]
- `olea_europaea`: masked [size]
- `prunus_avium`: masked [size]
- `prunus_padus`: masked [sculpt, size]
- `reseda_lutea`: masked [size]
- `robinia_pseudoacacia`: masked [size]
- `rosa_canina`: masked [sculpt]
- `rosa_rubiginosa`: masked [sculpt]
- `rubus_chamaemorus`: masked [size]
- `rubus_idaeus`: masked [sculpt]
- `sanguisorba_minor`: masked [sculpt, size]
- `sanguisorba_officinalis`: masked [sculpt]
- `tordylium_apulum`: masked [size]
- `trifolium_pratense`: masked [size]
- `trifolium_repens`: masked [size]
- `viburnum_opulus`: masked [size]

## 3. Clustering parameters

| Parameter | Value |
| :--- | :--- |
| Linkage | UPGMA within aperture-family blocks; Kruskal single-link within blocks n>200 |
| W_APERTURE (mismatch) | 3.0 |
| W_SIZE_CLASS (mismatch) | 2.0 |
| W_SIZE_CLASS_ADJ (adjacent) | 0.8 |
| W_SIZE_MID (per 5 µm) | 1.0 |
| W_SCULPT (× Jaccard dist) | 1.5 |
| W_SHAPE / W_ORN | 0.8 / 0.5 |
| Missing-dim inflate | 0.35 |
| Size classes | Kerkvliet bins from max µm (`kerkvliet-determinatietabel.js`) |
| **Tight cut** | distance ≤ **1.872** |
| **Loose cut** | distance ≤ **2.272** |

### Calibration notes

- Calibration pairs with distance: confirmed n=24, different n=53
- Confirmed distance: min=0.475 median=1.975 max=5.275
- Different distance: min=1.200 median=2.430 max=4.775
- Calibrated cuts from medians → tight=1.872, loose=2.272

### Sample decided-pair distances

| Pair | Status | Distance |
| :--- | :--- | ---: |
| `acer_platanoides`–`centaurea_cyanus` | review:different | 1.900 |
| `acer_platanoides`–`malus_typ` | review:different | 2.195 |
| `acer_platanoides`–`prunus_pirus_typ` | review:different | 2.646 |
| `acer_platanoides`–`ranunculus_typ` | review:different | 1.976 |
| `acer_platanoides`–`robinia_pseudoacacia` | review:different | 1.900 |
| `acer_platanoides`–`taraxacum_typ` | review:different | 2.396 |
| `acer_platanoides`–`tilia_typ` | review:different | 2.441 |
| `aesculus_hippocastanum`–`melilotus_officinalis` | review:confirmed | 1.750 |
| `aesculus_hippocastanum`–`trifolium_repens` | review:confirmed | 1.275 |
| `ailanthus_altissima`–`taraxacum_typ` | review:different | 3.125 |
| `ailanthus_altissima`–`tilia_typ` | review:different | 3.725 |
| `amorpha_fruticosa`–`taraxacum_typ` | review:different | 2.992 |
| `anthriscus_typ`–`taraxacum_typ` | review:different | 3.125 |
| `anthriscus_typ`–`vicia_typ` | review:confirmed | 1.975 |
| `brassica_typ`–`fraxinus_ornus` | review:confirmed | 3.375 |
| `brassica_typ`–`ligustrum_vulgare` | review:confirmed | 2.505 |
| `brassica_typ`–`raphanus_typ` | review:confirmed | 1.975 |
| `brassica_typ`–`salix_typ` | review:confirmed | 2.625 |
| `brassica_typ`–`taraxacum_typ` | review:different | 2.125 |
| `brassica_typ`–`tilia_typ` | review:different | 3.775 |
| `calluna_vulgaris`–`centaurea_cyanus` | review:different | 1.620 |
| `calluna_vulgaris`–`ranunculus_typ` | review:different | 2.325 |
| `calluna_vulgaris`–`taraxacum_typ` | review:different | 2.625 |
| `calluna_vulgaris`–`tilia_typ` | review:different | 2.375 |
| `centaurea_cyanus`–`crataegus_typ` | review:different | 1.480 |

## 4. Tight clusters (near-identical)

Clusters with ≥2 members at tight≤1.872 cut. Learning-priority clusters listed first.

- With ≥1 learning_priority_rank: **3**
- Unranked-only: **44**
- Total: **47**

### C1 (n=596, mean_d=4.136) — ranks [3, 5, 6, 11, 13, 15, 16, 21, 26, 29, 33, 34, 39, 40, 42, 44, 45, 53, 64, 71, 75]

- Shared aperture: tricol*
- Size classes: large, medium, small, very-large, very-small; mid range: (11.2, 107.9)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** pisum_sativum ↔ pisum_typ; lysimachia_vulgaris ↔ lysimachia_typ; lysimachia_nemorum ↔ lysimachia_typ; oxalis_corniculata ↔ oxalis_typ; lonicera_alpigena ↔ lonicera_typ; lonicera_caprifolium ↔ lonicera_typ; lonicera_xylosteum ↔ lonicera_typ; artemisia_dracunculus ↔ artemisia_typ; artemisia_vulgaris ↔ artemisia_typ; aconitum_napellus ↔ aconitum_typ; eryngium_maritimum ↔ eryngium_typ; eryngium_campestre ↔ eryngium_typ; eryngium_planum ↔ eryngium_typ; lupinus_angustifolius ↔ lupinus_typ; lupinus_polyphyllus ↔ lupinus_typ; lamium_purpureum ↔ lamium_typ; lamium_amplexicaule ↔ lamium_typ; lamium_album ↔ lamium_typ; lamium_maculatum_cv_var ↔ lamium_typ; sedum_acre ↔ sedum_typ; sedum_album ↔ sedum_typ; sedum_telephium ↔ sedum_typ; sedum_sexangulare ↔ sedum_typ; salix_aurita ↔ salix_typ; salix_repens ↔ salix_typ; salix_caprea ↔ salix_typ; salix_dasyclados ↔ salix_typ; salix_triandra ↔ salix_typ; salix_daphnoides ↔ salix_typ; salix_viminalis ↔ salix_typ; salix_cinerea ↔ salix_typ; salix_alba_var_tristis ↔ salix_typ; salix_fragilis ↔ salix_typ; salix_purpurea ↔ salix_typ; salix_pentandra ↔ salix_typ; aster_alpinus ↔ aster_typ; aster_amellus ↔ aster_typ; aster_sedifolius ↔ aster_typ; filipendula_vulgaris ↔ filipendula_typ; filipendula_ulmaria ↔ filipendula_typ; rubus_chamaemorus ↔ rubus_typ; rubus_fructicosus ↔ rubus_typ; rubus_fruticosus ↔ rubus_typ; rubus_saxatilis ↔ rubus_typ; rubus_caesius ↔ rubus_typ; rubus_idaeus ↔ rubus_typ; bidens_ferulifolia ↔ bidens_typ; senecio_squalidus ↔ senecio_typ; senecio_ovatus ↔ senecio_typ; senecio_aquaticus ↔ senecio_typ; senecio_jacobaea ↔ senecio_typ; senecio_paludosus ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_vulgaris ↔ senecio_typ; senecio_erucifolius ↔ senecio_typ; senecio_jacobea ↔ senecio_typ; arbutus_unedo ↔ arbutus_typ; ranunculus_ficaria ↔ ranunculus_typ; ranunculus_repens ↔ ranunculus_typ; ranunculus_acris ↔ ranunculus_typ; ranunculus_bulbosus ↔ ranunculus_typ; hydrangea_macrophylla ↔ hydrangea_typ; helianthemum_nummularium ↔ helianthemum_typ; crepis_biennis ↔ crepis_typ; galinsoga_parviflora ↔ galinsoga_typ; galinsoga_ciliata ↔ galinsoga_typ; melampyrum_pratense ↔ melampyrum_typ; mercurialis_annua ↔ mercurialis_typ; mercurialis_perennis ↔ mercurialis_typ; alyssum_repens ↔ alyssum_typ; alyssum_saxatile ↔ alyssum_typ; alyssum_montanum ↔ alyssum_typ; cytisus_scoparius ↔ cytisus_typ; malus_domestica ↔ malus_typ; malus_sylvestris ↔ malus_typ; euphorbia_cyparissias ↔ euphorbia_typ; euphorbia_amygdaloides ↔ euphorbia_typ; crambe_maritima ↔ crambe_typ; geranium_nodosum ↔ geranium_typ; geranium_dissectum ↔ geranium_typ; geranium_robertianum ↔ geranium_typ; geranium_phaeum ↔ geranium_typ; geranium_macrorrhizum ↔ geranium_typ; geranium_molle ↔ geranium_typ; geranium_sanguineum ↔ geranium_typ; geranium_pratense ↔ geranium_typ; geranium_pyrenaicum ↔ geranium_typ; rhinanthus_alectorolophus ↔ rhinanthus_typ; carduus_crispus ↔ carduus_typ; carduus_defloratus ↔ carduus_typ; carduus_nutans ↔ carduus_typ; hieracium_aurantiacum ↔ hieracium_typ; ulex_europaeus ↔ ulex_typ; serratula_tinctoria ↔ serratula_typ; veronica_arvensis ↔ veronica_typ; veronica_austriaca_ssp_teucrium ↔ veronica_typ; veronica_chamaedrys ↔ veronica_typ; veronica_officinalis ↔ veronica_typ; veronica_persica ↔ veronica_typ; parthenocissus_tricuspidata ↔ parthenocissus_typ; parthenocissus_quinquefolia ↔ parthenocissus_typ; symphoricarpos_albus ↔ symphoricarpos_typ; crataegus_monogyna ↔ crataegus_typ; crataegus_laevigata ↔ crataegus_typ; tamarix_gallica ↔ tamarix_typ; callicarpa_bodinieri ↔ callicarpa_typ; tilia_platyphyllos ↔ tilia_typ; tilia_americana ↔ tilia_typ; tilia_tomentosa ↔ tilia_typ
- **already_decided:** `acer_platanoides`–`centaurea_cyanus` (review:different); `acer_platanoides`–`malus_typ` (review:different); `acer_platanoides`–`ranunculus_typ` (review:different); `acer_platanoides`–`robinia_pseudoacacia` (review:different); `acer_platanoides`–`tilia_typ` (review:different); `aesculus_hippocastanum`–`melilotus_officinalis` (review:confirmed); `aesculus_hippocastanum`–`trifolium_repens` (review:confirmed); `ailanthus_altissima`–`tilia_typ` (review:different); `calluna_vulgaris`–`centaurea_cyanus` (review:different); `calluna_vulgaris`–`ranunculus_typ` (review:different); `calluna_vulgaris`–`tilia_typ` (review:different); `centaurea_cyanus`–`crataegus_typ` (review:different); `centaurea_cyanus`–`helianthus_annuus` (review:different); `centaurea_cyanus`–`ranunculus_typ` (review:different); `centaurea_cyanus`–`tilia_typ` (review:different); `centaurea_cyanus`–`trifolium_pratense` (review:confirmed); `centaurea_jacea`–`ranunculus_typ` (review:different); `centaurea_jacea`–`tilia_typ` (review:different); `cornus_mas`–`tilia_typ` (review:different); `crataegus_typ`–`tilia_typ` (review:different); `helianthus_annuus`–`ranunculus_typ` (review:different); `helianthus_annuus`–`tilia_typ` (review:different); `lamium_typ`–`tilia_typ` (review:different); `malus_typ`–`robinia_pseudoacacia` (review:different); `melilotus_officinalis`–`trifolium_repens` (review:confirmed); `polygonum_aviculare`–`tilia_typ` (review:different); `prunus_padus`–`prunus_serotina` (review:confirmed); `prunus_padus`–`rubus_typ` (review:confirmed); `prunus_serotina`–`rubus_typ` (review:confirmed); `ranunculus_typ`–`tilia_typ` (review:different); `rubus_typ`–`tilia_typ` (review:different); `tilia_typ`–`trifolium_pratense` (review:different)
- Members:
  - `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | sc={driehoekig,psilaat,striaat,tricolporaat}
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=38.1µm | sculpt_MASKED
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | size_MASKED | sc={driehoekig,prolaat,reticulaat,rond,tricolporaat}
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | sc={rond,rugulaat,striaat,tricolpaat}
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,rond,tricolpaat}
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,rond,tricolporaat}
  - `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat,rond,tricolpaat,verrucaat}
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | sc={psilaat,scabraat}
  - `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,reticulaat,rugulaat,striaat,tricolporaat}
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | size_MASKED | sc={driehoekig,oblaat,prolaat,psilaat,reticulaat}
  - `castanea_sativa` | *Castanea sativa* | rank=39 | ap=tricol* | class=very-small | mid=13.0µm | sc={prolaat,psilaat,rond,rugulaat,scabraat}
  - `polygonum_aviculare` | *Polygonum aviculare* | rank=40 | ap=tricol* | class=medium | mid=32.9µm | sc={driehoekig,oblaat,prolaat,psilaat,scabraat}
  - `amorpha_fruticosa` | *Amorpha fruticosa* | rank=42 | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat,verrucaat}
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | sc={striaat}
  - `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | size_MASKED | sc={prolaat,reticulaat,rond,tricolporaat}
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat,scabraat}
  - `calluna_vulgaris` | *Calluna vulgaris* | rank=64 | ap=tricol* | class=medium | mid=35.5µm | sc={echinaat,fenestraat,psilaat,scabraat,tetrade}
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=small | mid=25.0µm | sc={prolaat,psilaat,reticulaat,rond,scabraat}
  - `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=33.0µm | sc={driehoekig,echinaat,fenestraat,oblaat,scabraat}
  - `acanthus_mollis` | *Acanthus mollis* | unranked | ap=tricol* | class=large | mid=55.1µm | sc={prolaat,reticulaat}
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | sc={rugulaat,striaat,tricolpaat}
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `acer_monspessulanum` | *Acer monspessulanum* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,rugulaat,striaat,tricolpaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `acer_pseudoplatanus` | *Acer pseudoplatanus* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={rugulaat,striaat,tricolpaat,verrucaat}
  - `acer_tataricum_subsp_ginnala` | *Acer tataricum* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={striaat}
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat,fenestraat}
  - `aconitum_napellus` | *Aconitum napellus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={microreticulaat,psilaat}
  - `aconitum_typ` | *Aconitum typ* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,scabraat}
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={microreticulaat,psilaat,reticulaat}
  - `aegopodium_podagraria` | *Aegopodium podagraria* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={psilaat}
  - `aesculus_carnea` | *Aesculus carnea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={psilaat,rugulaat,striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=small | mid=24.0µm | sculpt_MASKED
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | sculpt_MASKED
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | sculpt_MASKED
  - `ajuga_reptans` | *Ajuga reptans* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,reticulaat,rond,rugulaat,tricolpaat}
  - `alchemilla_alpina` | *Alchemilla alpina* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={driehoekig,psilaat,tricolporaat}
  - `alliaria_petiolata` | *Alliaria petiolata* | unranked | ap=tricol* | sc={reticulaat}
  - `alyssum_montanum` | *Alyssum montanum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,reticulaat}
  - `alyssum_repens` | *Alyssum repens* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `alyssum_typ` | *Alyssum typ* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat}
  - `anchusa_arvensis` | *Anchusa arvensis* | unranked | ap=tricol* | class=medium | mid=48.0µm | sc={psilaat,scabraat}
  - `anemone_typ` | *Anemone typ* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `anethum_graveolens` | *Anethum graveolens* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={gemmaat,microreticulaat,reticulaat,scabraat,verrucaat}
  - `angelica_archangelica` | *Angelica archangelica* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={rugulaat}
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,verrucaat}
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat,fenestraat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `anthriscus_caucalis` | *Anthriscus caucalis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={psilaat}
  - `anthriscus_cerefolium` | *Anthriscus cerefolium* | unranked | ap=tricol* | class=medium | mid=20.2µm | sc={psilaat}
  - `anthriscus_sylvestris` | *Anthriscus sylvestris* | unranked | ap=tricol* | class=medium | mid=20.1µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `anthyllis_vulneraria` | *Anthyllis vulneraria* | unranked | ap=tricol* | class=large | mid=44.1µm | sc={driehoekig,oblaat,prolaat,psilaat,rugulaat}
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={microreticulaat,reticulaat}
  - `aquilegia_vulgaris` | *Aquilegia vulgaris* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={psilaat}
  - `arabis_hirsuta_ssp_hirsuta` | *Arabis hirsuta* | unranked | ap=tricol* | sc={reticulaat}
  - `arabis_procurrens` | *Arabis procurrens* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={reticulaat}
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `arbutus_typ` | *Arbutus typ* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
  - `arbutus_unedo` | *Arbutus unedo* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={driehoekig,psilaat,rond}
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat}
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | size_MASKED | sc={echinaat,fenestraat,tricolporaat}
  - `arctostaphylos_alpina` | *Arctostaphylos alpina* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={driehoekig,rond,scabraat,verrucaat}
  - `arctostaphylos_uva_ursi` | *Arctostaphylos uva-ursi* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={psilaat}
  - `armeria_maritima` | *Armeria maritima* | unranked | ap=tricol* | class=large | mid=68.0µm | sc={reticulaat,tricolpaat}
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | sc={echinaat}
  - `artemisia_dracunculus` | *Artemisia dracunculus* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={echinaat,psilaat,tricolporaat}
  - `artemisia_typ` | *Artemisia typ* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={echinaat,fenestraat}
  - `artemisia_vulgaris` | *Artemisia vulgaris* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={echinaat,reticulaat,tricolporaat}
  - `aruncus_dioicus` | *Aruncus dioicus* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={rugulaat,striaat}
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={echinaat,tricolporaat}
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={echinaat,tricolporaat}
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat}
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `atropa_bella_donna` | *Atropa bella* | unranked | ap=tricol* | class=medium | mid=46.0µm | sc={microreticulaat,prolaat,rugulaat,striaat}
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={echinaat}
  - `berteroa_incana` | *Berteroa incana* | unranked | ap=tricol* | sc={reticulaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={echinaat,fenestraat}
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat,tricolpaat}
  - `brassica_nigra` | *Brassica nigra* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat,tricolpaat}
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | sc={reticulaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={echinaat}
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat,fenestraat}
  - `callicarpa_bodinieri` | *Callicarpa bodinieri* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={rugulaat,scabraat,verrucaat}
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat,reticulaat}
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat}
  - `camelina_sativa` | *Camelina sativa* | unranked | ap=tricol* | sc={reticulaat}
  - `capsella_bursa_pastoris` | *Capsella bursa* | unranked | ap=tricol* | sc={reticulaat}
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={psilaat,reticulaat}
  - `caragana_arborescens` | *Caragana arborescens* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={scabraat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={reticulaat}
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={echinaat}
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carduus_nutans` | *Carduus nutans* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat,fenestraat}
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carragena_arbores` | *Carragena arbores* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={scabraat}
  - `carthamus_lanatus` | *Carthamus lanatus* | unranked | ap=tricol* | class=large | mid=66.0µm | sc={echinaat,fenestraat,prolaat}
  - `carthamus_tinctorius` | *Carthamus tinctorius* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={echinaat,fenestraat}
  - `carum_carvi` | *Carum carvi* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `ceanothus_americanus` | *Ceanothus americanus* | unranked | ap=tricol* | class=small | mid=19.4µm | sc={reticulaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | size_MASKED | sc={driehoekig,oblaat,prolaat,psilaat,reticulaat}
  - `centaurea_scabiosa` | *Centaurea scabiosa* | unranked | ap=tricol* | class=large | mid=54.0µm | sc={driehoekig,echinaat,oblaat,psilaat,scabraat}
  - `cercis_siliquastrum` | *Cercis siliquastrum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `chelidonium_majus` | *Chelidonium majus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,scabraat}
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `cichorium_intybus` | *Cichorium intybus* | unranked | ap=tricol* | class=medium | mid=38.0µm | sc={echinaat,fenestraat}
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cirsium_dissectum` | *Cirsium dissectum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_oleraceum` | *Cirsium oleraceum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_palustre` | *Cirsium palustre* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_rivulare` | *Cirsium rivulare* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_vulgare` | *Cirsium vulgare* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cistus_albidus` | *Cistus albidus* | unranked | ap=tricol* | class=large | mid=45.1µm | sc={prolaat,reticulaat}
  - `cistus_incanus` | *Cistus incanus* | unranked | ap=tricol* | class=large | mid=49.4µm | sc={reticulaat}
  - `cistus_salviifolius` | *Cistus salviifolius* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={reticulaat}
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | sc={reticulaat}
  - `clematis_recta` | *Clematis recta* | unranked | ap=tricol* | class=small | mid=22.8µm | sc={scabraat,verrucaat}
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `clethra_alnifolia` | *Clethra alnifolia* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat,verrucaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat,fenestraat}
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | sc={reticulaat}
  - `coffea_typ` | *Coffea typ* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={scabraat}
  - `coincya_monensis_ssp_recurvata` | *Coincya monensis* | unranked | ap=tricol* | sc={reticulaat}
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={reticulaat}
  - `consolida_ajacis` | *Consolida ajacis* | unranked | ap=tricol* | sc={psilaat}
  - `consolida_regalis` | *Consolida regalis* | unranked | ap=tricol* | class=medium | mid=38.1µm | sc={psilaat}
  - `convolvulus_arve` | *Convolvulus arve* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={scabraat}
  - `convolvulus_arvensis` | *Convolvulus arvensis* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microechinaat,microreticulaat,prolaat,psilaat}
  - `coriandrum_sativum` | *Coriandrum sativum* | unranked | ap=tricol* | size_MASKED | sc={prolaat,reticulaat,scabraat,verrucaat}
  - `cornus_alba` | *Cornus alba* | unranked | ap=tricol* | class=medium | mid=42.1µm | sc={psilaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | sc={reticulaat}
  - `corylopsis_spicata` | *Corylopsis spicata* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={reticulaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={echinaat,fenestraat}
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `cotoneaster_niger` | *Cotoneaster niger* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={psilaat,striaat,tricolporaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crataegus_laevigata` | *Crataegus laevigata* | unranked | ap=tricol* | sc={striaat}
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | sc={rugulaat,striaat,tricolporaat}
  - `crepis_biennis` | *Crepis biennis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={echinaat,microreticulaat}
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat,fenestraat}
  - `cydonia_oblonga` | *Cydonia oblonga* | unranked | ap=tricol* | sc={striaat}
  - `cymbalaria_muralis` | *Cymbalaria muralis* | unranked | ap=tricol* | sc={reticulaat}
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | sc={echinaat}
  - `cynoglossum_officinale` | *Cynoglossum officinale* | unranked | ap=tricol* | class=small | mid=13.0µm | sc={heterocolpaat,psilaat,stephanocolporaat}
  - `cytisus_scoparius` | *Cytisus scoparius* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat,tricolpaat}
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat,scabraat}
  - `datura_stramonium` | *Datura stramonium* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={oblaat,rugulaat,striaat,verrucaat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,scabraat}
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={rugulaat}
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `digitalis_purpurea` | *Digitalis purpurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `dipsacus_fullonum` | *Dipsacus fullonum* | unranked | ap=tricol* | class=large | mid=89.0µm | sc={echinaat}
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `dryas_octopetala` | *Dryas octopetala* | unranked | ap=tricol* | size_MASKED | sc={striaat,tricolporaat}
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat,reticulaat,tricolporaat}
  - `elaeagnus_angustifolia` | *Elaeagnus angustifolia* | unranked | ap=tricol* | class=large | mid=42.6µm | sc={driehoekig,oblaat,psilaat,scabraat,tricolporaat}
  - `eleagnus_angustif` | *Eleagnus angustif* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={psilaat}
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm
  - `eranthis_hyemalis` | *Eranthis hyemalis* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={echinaat,microechinaat,prolaat,psilaat,scabraat}
  - `erica_arborea` | *Erica arborea* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={verrucaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={echinaat}
  - `erigeron_annuus` | *Erigeron annuus* | unranked | ap=tricol* | sc={echinaat}
  - `erigeron_canaden` | *Erigeron canadensis* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={echinaat,fenestraat}
  - `erodium_cicutarium` | *Erodium cicutarium* | unranked | ap=tricol* | class=large | mid=54.0µm | sc={striaat}
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | sc={reticulaat}
  - `eryngium_campestre` | *Eryngium campestre* | unranked | ap=tricol* | class=large | mid=49.5µm | sc={gemmaat,verrucaat}
  - `eryngium_maritimum` | *Eryngium maritimum* | unranked | ap=tricol* | class=large | mid=60.8µm | sc={psilaat}
  - `eryngium_planum` | *Eryngium planum* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={psilaat}
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat,scabraat}
  - `erysimum_cheiranthoides` | *Erysimum cheiranthoides* | unranked | ap=tricol* | class=small | mid=20.6µm | sc={reticulaat}
  - `erysimum_cheiri` | *Erysimum cheiri* | unranked | ap=tricol* | sc={reticulaat}
  - `escallonia_typ` | *Escallonia typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={psilaat}
  - `eucalyptus_camaldulensis` | *Eucalyptus camaldulensis* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={verrucaat}
  - `euodia_hupehensis` | *Euodia hupehensis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat,tricolporaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `euphorbia_amygdaloides` | *Euphorbia amygdaloides* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | sc={verrucaat}
  - `euphrasia_stricta` | *Euphrasia stricta* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={psilaat}
  - `fagopyrum_esculentum` | *Fagopyrum esculentum* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `fagus_sylvatica` | *Fagus sylvatica* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={reticulaat,rugulaat,scabraat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `fallopia_convolvulus` | *Fallopia convolvulus* | unranked | ap=tricol* | sc={psilaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `ferula_communis` | *Ferula communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={rugulaat,scabraat}
  - `ficaria_typ` | *Ficaria typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | sc={clavaat,echinaat,microechinaat,prolaat,psilaat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={clavaat,echinaat,microechinaat,prolaat,psilaat}
  - `foeniculum_vulga` | *Foeniculum vulga* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,verrucaat}
  - `foeniculum_vulgaris` | *Foeniculum vulgaris* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={scabraat}
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=23.7µm | sc={operculaat,prolaat,striaat}
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={operculaat,prolaat,striaat,tricolporaat}
  - `fragaria_viridis` | *Fragaria viridis* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={striaat,tricolporaat}
  - `frangula_alnus` | *Frangula alnus* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={driehoekig,oblaat,prolaat,psilaat,rond}
  - `fraxinus_excelsior` | *Fraxinus excelsior* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `galeopsis_speciosa` | *Galeopsis speciosa* | unranked | ap=tricol* | class=medium | mid=44.3µm | sc={reticulaat}
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `galinsoga_ciliata` | *Galinsoga ciliata* | unranked | ap=tricol* | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={echinaat}
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat,fenestraat}
  - `genista_anglica` | *Genista anglica* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `genista_pilosa` | *Genista pilosa* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={reticulaat}
  - `genista_tinctoria` | *Genista tinctoria* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={scabraat,verrucaat}
  - `geranium_dissectum` | *Geranium dissectum* | unranked | ap=tricol* | class=large | mid=55.0µm | sc={clavaat}
  - `geranium_macrorrhizum` | *Geranium macrorrhizum* | unranked | ap=tricol* | class=very-large | mid=89.0µm | sc={clavaat}
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | sc={clavaat}
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | sc={clavaat}
  - `geranium_pratense` | *Geranium pratense* | unranked | ap=tricol* | class=very-large | mid=107.9µm | sc={clavaat}
  - `geranium_pyrenaicum` | *Geranium pyrenaicum* | unranked | ap=tricol* | class=large | mid=64.8µm | sc={clavaat}
  - `geranium_robertianum` | *Geranium robertianum* | unranked | ap=tricol* | class=large | mid=66.2µm | sc={clavaat,rugulaat,striaat,tricolpaat}
  - `geranium_sanguineum` | *Geranium sanguineum* | unranked | ap=tricol* | class=very-large | mid=102.0µm | sc={clavaat}
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | sc={reticulaat}
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={operculaat,striaat,tricolporaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={operculaat,striaat,tricolporaat}
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={reticulaat}
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `hamamelis_japonica` | *Hamamelis japonica* | unranked | ap=tricol* | class=small | mid=21.3µm | sc={reticulaat}
  - `hedera_helix` | *Hedera helix* | unranked | ap=tricol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rond}
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={echinaat}
  - `helianthemum_nummularium` | *Helianthemum nummularium* | unranked | ap=tricol* | class=large | mid=30.9µm | sc={prolaat,reticulaat,striaat}
  - `helianthemum_typ` | *Helianthemum typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat}
  - `helichrysum_arenarium` | *Helichrysum arenarium* | unranked | ap=tricol* | sc={echinaat}
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={microreticulaat,prolaat,reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=42.9µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={echinaat,fenestraat}
  - `heracleum_sphondylium` | *Heracleum sphondylium* | unranked | ap=tricol* | class=medium | mid=38.5µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={reticulaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat,fenestraat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | sc={striaat}
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={reticulaat,scabraat}
  - `hydrangea_macrophylla` | *Hydrangea macrophylla* | unranked | ap=tricol* | class=very-small | mid=13.0µm | sc={reticulaat}
  - `hydrangea_typ` | *Hydrangea typ* | unranked | ap=tricol* | class=very-small | mid=11.2µm | sc={psilaat}
  - `hypericum_androsaemum` | *Hypericum androsaemum* | unranked | ap=tricol* | class=small | mid=18.8µm | sc={reticulaat}
  - `hypericum_montanum` | *Hypericum montanum* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={reticulaat}
  - `hypericum_perforatum` | *Hypericum perforatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,tricolporaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `iberis_amara` | *Iberis amara* | unranked | ap=tricol* | class=medium | mid=25.7µm | sc={reticulaat}
  - `ilex_aquifolium` | *Ilex aquifolium* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={clavaat,prolaat,reticulaat,tricolpaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={echinaat}
  - `inula_conyzae` | *Inula conyzae* | unranked | ap=tricol* | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `koelreuteria_paniculata` | *Koelreuteria paniculata* | unranked | ap=tricol* | class=medium | mid=23.0µm | sc={reticulaat}
  - `kolkwitzia_amabilis` | *Kolkwitzia amabilis* | unranked | ap=tricol* | class=large | mid=52.0µm | sc={echinaat,scabraat,striaat}
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `lamium_album` | *Lamium album* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `lamium_maculatum_cv_var` | *Lamium maculatum* | unranked | ap=tricol* | class=medium | mid=28.7µm | sc={psilaat}
  - `lamium_purpureum` | *Lamium purpureum* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={reticulaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat,fenestraat}
  - `lathyrus_palustris` | *Lathyrus palustris* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={reticulaat}
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | sc={reticulaat}
  - `lathyrus_sylvestris` | *Lathyrus sylvestris* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={psilaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | sc={reticulaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | sc={reticulaat}
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `levisticum_officinale` | *Levisticum officinale* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={prolaat,psilaat}
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={reticulaat,tricolpaat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat,scabraat,striaat}
  - `limonium_vulgare` | *Limonium vulgare* | unranked | ap=tricol* | size_MASKED | sc={echinaat,reticulaat,scabraat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `linaria_repens` | *Linaria repens* | unranked | ap=tricol* | sc={reticulaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | sc={clavaat}
  - `linum_usitatissimum` | *Linum usitatissimum* | unranked | ap=tricol* | size_MASKED | sc={reticulaat,tricolpaat,verrucaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | sc={echinaat,tricolporaat}
  - `lonicera_typ` | *Lonicera typ* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat,fenestraat,reticulaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=52.8µm | sc={echinaat,prolaat}
  - `lotus_corniculatus` | *Lotus corniculatus* | unranked | ap=tricol* | class=small | mid=18.9µm | sc={prolaat,psilaat,rond,scabraat,tricolporaat}
  - `lotus_pedunculatus` | *Lotus pedunculatus (syn Lotus uliginosus)* | unranked | ap=tricol* | class=small | mid=14.9µm | sc={psilaat}
  - `lunaria_annua` | *Lunaria annua* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={reticulaat}
  - `lupinus_polyphyllus` | *Lupinus polyphyllus* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={striaat}
  - `lysimachia_nemorum` | *Lysimachia nemorum* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={prolaat,reticulaat}
  - `malus_domestica` | *Malus domestica* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `malus_sylvestris` | *Malus sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `malus_typ` | *Malus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat,rugulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={echinaat,tricolporaat}
  - `medicago_falcata` | *Medicago falcata* | unranked | ap=tricol* | class=medium | mid=31.9µm | sc={psilaat}
  - `medicago_lupulina` | *Medicago lupulina* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat,rugulaat}
  - `medicago_sativa` | *Medicago sativa* | unranked | ap=tricol* | size_MASKED | sc={prolaat,psilaat,reticulaat,rugulaat,scabraat}
  - `melampyrum_pratense` | *Melampyrum pratense* | unranked | ap=tricol* | class=medium | mid=23.1µm | sc={scabraat,verrucaat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `melittis_melissophyllum` | *Melittis melissophyllum* | unranked | ap=tricol* | class=medium | mid=43.8µm | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat}
  - `mercurialis_perennis` | *Mercurialis perennis* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mercurialis_typ` | *Mercurialis typ* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mespilus_germani` | *Mespilus germani* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={scabraat,striaat}
  - `mespilus_germanica` | *Mespilus germanica* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={psilaat,tricolporaat}
  - `misopates_orontium` | *Misopates orontium* | unranked | ap=tricol* | sc={reticulaat}
  - `nicandra_physalodes` | *Nicandra physalodes* | unranked | ap=tricol* | class=medium | mid=19.1µm | sc={driehoekig,psilaat,scabraat}
  - `nicotiana_glauca` | *Nicotiana glauca* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={rugulaat}
  - `nigella_arvensis` | *Nigella arvensis* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={echinaat,microechinaat,psilaat,scabraat,tricolpaat}
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | sc={psilaat,reticulaat}
  - `nigella_sativa` | *Nigella sativa* | unranked | ap=tricol* | class=medium | mid=43.1µm | sc={psilaat,reticulaat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat,scabraat}
  - `odontites_vernus_ssp_serotines` | *Odontites vernus* | unranked | ap=tricol* | sc={reticulaat}
  - `olea_europaea` | *Olea europaea* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microreticulaat,prolaat,reticulaat,scabraat}
  - `onobrychis_viciifolia` | *Onobrychis viciifolia* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={reticulaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat,fenestraat}
  - `onosis_spinoza` | *Ononis spinosa* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={psilaat}
  - `orlaya_grandiflora` | *Orlaya grandiflora* | unranked | ap=tricol* | class=large | mid=34.0µm | sc={psilaat}
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_sativus` | *Ornithopus sativus* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={psilaat}
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `oxalis_corniculata` | *Oxalis corniculata* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `oxalis_typ` | *Oxalis typ* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={reticulaat}
  - `paeonia_officinalis` | *Paeonia officinalis* | unranked | ap=tricol* | class=medium | mid=37.2µm | sc={microreticulaat,prolaat,reticulaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={psilaat}
  - `papaver_rhoeas` | *Papaver rhoeas* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,microechinaat,microreticulaat,reticulaat,scabraat}
  - `papaver_somniferum` | *Papaver somniferum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={psilaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={prolaat,reticulaat,rond}
  - `parthenocissus_quinquefolia` | *Parthenocissus quinquefolia* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat,rugulaat}
  - `parthenocissus_tricuspidata` | *Parthenocissus tricuspidata* | unranked | ap=tricol* | sc={reticulaat}
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `pastinaca_sativa` | *Pastinaca sativa* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `persicaria_bistorta` | *Persicaria bistorta* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat,scabraat}
  - `petasites_albus` | *Petasites albus* | unranked | ap=tricol* | sc={echinaat}
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `philadelphus_coronarius` | *Philadelphus coronarius* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={psilaat,reticulaat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={psilaat,scabraat}
  - `picris_echioides` | *Picris echioides* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,scabraat}
  - `pimpinella_major` | *Pimpinella major* | unranked | ap=tricol* | class=medium | mid=24.4µm | sc={prolaat,psilaat}
  - `pimpinella_saxifraga` | *Pimpinella saxifraga* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={psilaat}
  - `pisum_sativum` | *Pisum sativum* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `pisum_typ` | *Pisum typ* | unranked | ap=tricol* | class=medium | mid=48.0µm | sc={reticulaat}
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={reticulaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `potentilla_anserina` | *Potentilla anserina* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={operculaat,prolaat,striaat,tricolporaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={striaat}
  - `potentilla_crantzii` | *Potentilla crantzii* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat,tricolporaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={striaat}
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={striaat}
  - `potentilla_palustris` | *Potentilla palustris* | unranked | ap=tricol* | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `prunus_armeniaca` | *Prunus armeniaca* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `prunus_avium` | *Prunus avium* | unranked | ap=tricol* | size_MASKED | sc={oblaat,rugulaat,striaat,tricolpaat,tricolporaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `prunus_domestica` | *Prunus domestica* | unranked | ap=tricol* | class=medium | mid=43.8µm | sc={striaat}
  - `prunus_dulcis` | *Prunus dulcis* | unranked | ap=tricol* | sc={striaat}
  - `prunus_laurocerasus` | *Prunus laurocerasus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={striaat}
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `prunus_padus` | *Prunus padus* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED
  - `prunus_persica` | *Prunus persica* | unranked | ap=tricol* | sc={striaat}
  - `prunus_serotina` | *Prunus serotina* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={psilaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={striaat}
  - `ptelea_trifoliata` | *Ptelea trifoliata* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `pterostyrax_hispida` | *Pterostyrax hispida* | unranked | ap=tricol* | class=medium | mid=27.2µm | sc={psilaat}
  - `pulicaria_dysenterica` | *Pulicaria dysenterica* | unranked | ap=tricol* | sc={echinaat}
  - `pulsatilla_vulgaris` | *Pulsatilla vulgaris* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={scabraat,verrucaat}
  - `punica_granatum` | *Punica granatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={rond,scabraat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyrus_communis` | *Pyrus communis* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={rugulaat,scabraat,striaat,verrucaat}
  - `quercus_petraea` | *Quercus petraea* | unranked | ap=tricol* | sc={psilaat}
  - `quercus_robur` | *Quercus robur* | unranked | ap=tricol* | class=medium | mid=33.7µm | sc={echinaat,psilaat,reticulaat,tricolpaat}
  - `ranunculus_acris` | *Ranunculus acris* | unranked | ap=tricol* | class=medium | mid=30.9µm | sc={echinaat,microechinaat,psilaat,scabraat,tricolpaat}
  - `ranunculus_bulbosus` | *Ranunculus bulbosus* | unranked | ap=tricol* | class=medium | mid=30.8µm | sc={baculaat,verrucaat}
  - `ranunculus_ficaria` | *Ranunculus ficaria* | unranked | ap=tricol* | class=medium | mid=32.9µm | sc={clavaat,echinaat,scabraat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat,tricolpaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | sc={reticulaat}
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `rhamnus_cathartica` | *Rhamnus cathartica* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat,rugulaat}
  - `rhinanthus_alectorolophus` | *Rhinanthus alectorolophus* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={rugulaat,scabraat,striaat}
  - `rhinanthus_typ` | *Rhinanthus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | sc={reticulaat}
  - `rhus_typhina` | *Rhus typhina* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,striaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `robinia_pseudoacacia` | *Robinia pseudoacacia* | unranked | ap=tricol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rond}
  - `rorippa_amphibia` | *Rorippa amphibia* | unranked | ap=tricol* | sc={reticulaat}
  - `rorippa_austriaca` | *Rorippa austriaca* | unranked | ap=tricol* | sc={reticulaat}
  - `rorippa_sylvestris` | *Rorippa sylvestris* | unranked | ap=tricol* | sc={reticulaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={striaat}
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | sculpt_MASKED
  - `rosa_gallica_officinalis` | *Rosa gallica officinalis* | unranked | ap=tricol* | class=medium | mid=36.6µm | sc={operculaat,rugulaat,scabraat}
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={striaat}
  - `rubus_chamaemorus` | *Rubus chamaemorus* | unranked | ap=tricol* | size_MASKED | sc={clavaat,echinaat,prolaat,psilaat,scabraat}
  - `rubus_fructicosus` | *Rubus fructicosus* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat,striaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={rugulaat}
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | sculpt_MASKED
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={striaat,tricolporaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat,tricolporaat}
  - `ruta_graveolens` | *Ruta graveolens* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={microreticulaat,prolaat,rugulaat}
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat,tricolpaat}
  - `salix_aurita` | *Salix aurita* | unranked | ap=tricol* | class=medium | mid=22.5µm | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | sc={reticulaat,tricolpaat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={reticulaat}
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={reticulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat}
  - `salix_viminalis` | *Salix viminalis* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={reticulaat}
  - `sambucus_ebulus` | *Sambucus ebulus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={psilaat,reticulaat}
  - `sambucus_nigra` | *Sambucus nigra* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={prolaat,psilaat,reticulaat,tricolpaat,tricolporaat}
  - `sanguisorba_minor` | *Sanguisorba minor* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | sc={psilaat,reticulaat}
  - `saxifraga_rotundifolia` | *Saxifraga rotundifolia* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={psilaat,rugulaat,scabraat,striaat,tricolpaat}
  - `saxifraga_umbrosa` | *Saxifraga umbrosa* | unranked | ap=tricol* | class=medium | mid=35.1µm | sc={striaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=73.8µm | sc={echinaat,tricolpaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | sc={echinaat}
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `scrophularia_vernalis` | *Scrophularia vernalis* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `securigera_varia_coronilla_varia` | *Securigera varia* | unranked | ap=tricol* | sc={striaat}
  - `sedum_acre` | *Sedum acre* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={rugulaat,striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | sc={striaat}
  - `sedum_sexangulare` | *Sedum sexangulare* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={striaat}
  - `sedum_telephium` | *Sedum telephium* | unranked | ap=tricol* | class=small | mid=22.2µm | sc={striaat}
  - `sedum_typ` | *Sedum typ* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={psilaat,striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | sc={striaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={echinaat}
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat,fenestraat,tricolporaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat,fenestraat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat,fenestraat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | sc={echinaat}
  - `silybum_marianum` | *Silybum marianum* | unranked | ap=tricol* | sc={echinaat,fenestraat}
  - `sinapis_alba` | *Sinapis alba* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat,tricolpaat}
  - `sisymbrium_officinale` | *Sisymbrium officinale* | unranked | ap=tricol* | sc={reticulaat}
  - `solanum_dulcamara` | *Solanum dulcamara* | unranked | ap=tricol* | class=small | mid=13.7µm | sc={driehoekig,oblaat,prolaat,psilaat,rond}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm
  - `solanum_lycopersicum` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=19.8µm | sc={prolaat,psilaat,rond,rugulaat,scabraat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | sc={psilaat}
  - `solanum_tuberosum` | *Solanum tuberosum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={psilaat}
  - `solidago_canadensis` | *Solidago canadensis* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={echinaat}
  - `solidago_virgaurea` | *Solidago virgaurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={echinaat,fenestraat}
  - `sonchus_arvensis` | *Sonchus arvensis* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat,fenestraat}
  - `sorbus_aria` | *Sorbus aria* | unranked | ap=tricol* | sc={striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={striaat,tricolporaat}
  - `spiraea_cantoniensis_x_trilobata` | *S. cantoniensis x S. trilobata* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat}
  - `spiraea_japonica` | *Spiraea japonica* | unranked | ap=tricol* | class=very-small | mid=12.5µm | sc={psilaat}
  - `stachys_arvensis` | *Stachys arvensis* | unranked | ap=tricol* | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={reticulaat}
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat}
  - `styrax_japonicus` | *Styrax japonicus* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={psilaat}
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat}
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat,fenestraat,striaat,tricolpaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `sylibum_marianum` | *Sylibum marianum* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={echinaat}
  - `symphoricarpos_albus` | *Symphoricarpos albus* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={prolaat,psilaat,rond,scabraat,tricolporaat}
  - `symphoricarpos_typ` | *Symphoricarpos typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={reticulaat,scabraat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat,fenestraat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `tamarix_typ` | *Tamarix typ* | unranked | ap=tricol* | class=small | mid=15.0µm | sc={reticulaat}
  - `tanacetum_corymbosum` | *Tanacetum corymbosum* | unranked | ap=tricol* | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={echinaat}
  - `taraxacum_officinale` | *Taraxacum officinale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat,fenestraat}
  - `telekia_speciosa` | *Telekia speciosa* | unranked | ap=tricol* | sc={echinaat}
  - `tephroseris_palustris` | *Tephroseris palustris* | unranked | ap=tricol* | sc={echinaat}
  - `teucrium_chamae` | *Teucrium chamae* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={scabraat}
  - `teucrium_chamaedrys` | *Teucrium chamaedrys* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={prolaat,rond,scabraat,verrucaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `tilia_americana` | *Tilia americana* | unranked | ap=tricol* | class=medium | mid=37.9µm | sc={reticulaat}
  - `tilia_platyphyllos` | *Tilia Platyphyllos* | unranked | ap=tricol* | class=medium | mid=37.3µm | sc={oblaat,reticulaat,rond,tricolporaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | sc={reticulaat}
  - `tordylium_apulum` | *Tordylium apulum* | unranked | ap=tricol* | size_MASKED | sc={rugulaat,scabraat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat,fenestraat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `trifolium_campestre` | *Trifolium campestre* | unranked | ap=tricol* | class=medium | mid=30.4µm | sc={reticulaat}
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={reticulaat}
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `tripleurospermum_maritimum` | *Tripleurospermum maritimum* | unranked | ap=tricol* | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={echinaat,fenestraat}
  - `trollius_europaeus` | *Trollius europaeus* | unranked | ap=tricol* | class=medium | mid=21.4µm | sc={prolaat,reticulaat,striaat,tricolpaat}
  - `tropaeolum_majus` | *Tropaeolum majus* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={reticulaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat,fenestraat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat,tricolpaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat}
  - `vaccinium_myrtillus` | *Vaccinium myrtillus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat,fenestraat,psilaat}
  - `vaccinium_oxycoccos` | *Vaccinium oxycoccos* | unranked | ap=tricol* | class=large | mid=48.0µm | sc={scabraat}
  - `vaccinium_vitis_idaea` | *Vaccinium vitis-idaea* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat,fenestraat,psilaat,scabraat,tetrade}
  - `valeriana_officinalis` | *Valeriana officinalis* | unranked | ap=tricol* | class=large | mid=45.5µm | sc={echinaat,prolaat,rugulaat,scabraat,tricolpaat}
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={reticulaat}
  - `verbascum_phlomoides` | *Verbascum phlomoides* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `verbascum_thapsus` | *Verbascum thapsus* | unranked | ap=tricol* | class=medium | mid=25.6µm | sc={reticulaat}
  - `verbena_officinalis` | *Verbena officinalis* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={driehoekig,oblaat,psilaat,rugulaat,scabraat}
  - `veronica_arvensis` | *Veronica arvensis* | unranked | ap=tricol* | class=medium | mid=24.6µm | sc={psilaat}
  - `veronica_austriaca_ssp_teucrium` | *Veronica austriaca* | unranked | ap=tricol* | class=medium | mid=39.6µm | sc={psilaat}
  - `veronica_chamaedrys` | *Veronica chamaedrys* | unranked | ap=tricol* | class=medium | mid=36.9µm | sc={psilaat}
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={psilaat}
  - `veronica_persica` | *Veronica persica* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={psilaat}
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,striaat}
  - `veronicastrum_sibiricum` | *Veronicastrum sibiricum* | unranked | ap=tricol* | class=small | mid=16.2µm | sc={microreticulaat,psilaat,reticulaat,scabraat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={reticulaat}
  - `vicia_cracca` | *Vicia cracca* | unranked | ap=tricol* | class=medium | mid=36.7µm | sc={prolaat,psilaat,reticulaat,rond,scabraat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `vicia_hirsuta` | *Vicia hirsuta* | unranked | ap=tricol* | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `vicia_tetrasperma` | *Vicia tetrasperma* | unranked | ap=tricol* | sc={reticulaat}
  - `vicia_villosa` | *Vicia villosa* | unranked | ap=tricol* | class=medium | mid=38.6µm | sc={reticulaat}
  - `vinca_typ` | *Vinca typ* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | sc={psilaat}
  - `viola_odorata` | *Viola odorata* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `viola_reichenbachiana` | *Viola reichenbachiana* | unranked | ap=tricol* | class=medium | mid=36.5µm | sc={psilaat}
  - `viola_riviniana` | *Viola riviniana* | unranked | ap=tricol* | class=medium | mid=34.3µm | sc={psilaat}
  - `viscum_album` | *Viscum album* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={echinaat,tricolpaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={microreticulaat,prolaat,reticulaat}
  - `vitis_vinifera` | *Vitis vinifera* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={psilaat,scabraat,tricolporaat}
  - `waldsteinia_ternata` | *Waldsteinia ternata* | unranked | ap=tricol* | sc={striaat}
  - `xanthium_italicum` | *Xanthium italicum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={scabraat}
  - `xanthium_strumarium` | *Xanthium strumarium* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={driehoekig,microechinaat,oblaat,psilaat,reticulaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | sc={echinaat}
- Closest pair evidence `anthemis_nobilis`–`taraxacum_officinale` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat', 'fenestraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `acanthus_mollis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_monspessulanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C2 (n=4, mean_d=1.102) — ranks [49]

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 35.2)
- Shared sculpture tokens: —
- Members:
  - `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | sc={baculaat,reticulaat,verrucaat}
  - `buxus_sempervirens` | *Buxus sempervirens* | unranked | ap=peripor* | class=medium | mid=33.5µm | sc={reticulaat}
  - `ribes_nigrum` | *Ribes nigrum* | unranked | ap=peripor* | class=medium | mid=35.2µm
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm
- Closest pair evidence `ribes_nigrum`–`silene_flos_cuculi` (d=0.815): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.815}`
- Provenance (sample): `buxus_sempervirens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-buxus.json · `ribes_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ribes_uva_crispa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `silene_flos_cuculi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C3 (n=18, mean_d=1.386) — ranks [76]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (29.2, 38.9)
- Shared sculpture tokens: —
- Members:
  - `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | sc={reticulaat}
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat,stephanocolpaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `mentha_pulegium` | *Mentha pulegium* | unranked | ap=stephanocol* | class=medium | mid=29.2µm
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `origanum_majorana` | *Origanum majorana* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat,rugulaat}
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `satureja_montana` | *Satureja montana* | unranked | ap=stephanocol* | class=medium | mid=36.5µm
  - `thymus_praecox` | *Thymus praecox* | unranked | ap=stephanocol* | class=medium | mid=34.4µm
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.375): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_parviflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C4 (n=11, mean_d=1.303)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.2, 29.5)
- Shared sculpture tokens: —
- Members:
  - `alisma_lanceolatum` | *Alisma lanceolatum* | unranked | ap=peripor* | class=medium | mid=25.4µm
  - `alisma_plantago_aquatica` | *Alisma plantago* | unranked | ap=peripor* | class=medium | mid=26.9µm
  - `chenopodium_bonus_henricus` | *Chenopodium bonus* | unranked | ap=peripor* | class=medium | mid=29.5µm
  - `daphne_mezereum` | *Daphne mezereum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={inaperturaat,periporaat,reticulaat,rond}
  - `gypsophila_paniculata` | *Gypsophila paniculata* | unranked | ap=peripor* | class=medium | mid=27.8µm
  - `plantago_lanceolata` | *Plantago Lanceolata* | unranked | ap=peripor* | class=medium | mid=25.1µm | sc={periporaat,verrucaat}
  - `plantago_major` | *Plantago major* | unranked | ap=peripor* | class=medium | mid=23.2µm
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm
  - `ribes_rubrum` | *Ribes rubrum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={periporaat,psilaat,rond,scabraat}
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm
  - `thymelaea_passerina` | *Thymelaea passerina* | unranked | ap=peripor* | class=medium | mid=24.2µm
- Closest pair evidence `ribes_alpinum`–`thalictrum_minus` (d=0.755): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.755}`
- Provenance (sample): `alisma_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `alisma_plantago_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-alisma-typ.json · `chenopodium_bonus_henricus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `daphne_mezereum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C5 (n=9, mean_d=1.304)

- Shared aperture: fenestr*
- Size classes: large, medium; mid range: (39.6, 44.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_laevigatum` | *Hieracium laevigatum* | unranked | ap=fenestr* | class=large | mid=44.0µm
  - `hieracium_sabaudum` | *Hieracium sabaudum* | unranked | ap=fenestr* | class=medium | mid=42.0µm
  - `hieracium_umbellatum` | *Hieracium umbellatum* | unranked | ap=fenestr* | class=medium | mid=39.6µm
  - `hypochaeris_radicata` | *Hypochaeris radicata* | unranked | ap=fenestr* | class=medium | mid=44.0µm
  - `lactuca_sativa` | *Lactuca sativa* | unranked | ap=fenestr* | class=medium | mid=40.4µm | sc={fenestraat}
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | sc={echinaat,fenestraat}
  - `leontodon_hispidus` | *Leontodon hispidus* | unranked | ap=fenestr* | class=medium | mid=44.5µm
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | sc={echinaat,fenestraat}
  - `sonchus_palustris` | *Sonchus palustris* | unranked | ap=fenestr* | class=medium | mid=43.2µm
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.505): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat', 'fenestraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.505}`
- Provenance (sample): `hieracium_laevigatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_sabaudum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hypochaeris_radicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C6 (n=7, mean_d=1.125)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (30.4, 35.2)
- Shared sculpture tokens: —
- Members:
  - `campanula_cochleariifolia` | *Campanula cochleariifolia* | unranked | ap=stephanopor* | class=medium | mid=33.9µm
  - `campanula_glomerata` | *Campanula glomerata* | unranked | ap=stephanopor* | class=medium | mid=30.4µm
  - `campanula_patula` | *Campanula patula* | unranked | ap=stephanopor* | class=medium | mid=32.5µm
  - `campanula_rapunculus` | *Campanula rapunculus* | unranked | ap=stephanopor* | class=medium | mid=34.8µm
  - `campanula_trachelium` | *Campanula trachelium* | unranked | ap=stephanopor* | class=medium | mid=35.2µm | sc={echinaat,microechinaat}
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.725): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.725}`
- Provenance (sample): `campanula_cochleariifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_glomerata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_patula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_rapunculus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C7 (n=6, mean_d=0.860)

- Shared aperture: multipor*
- Size classes: medium; mid range: (30.0, 36.0)
- Shared sculpture tokens: reticulaat
- **Human review (species↔*_typ):** borreria_verticilata ↔ borreria_typ
- Members:
  - `borreria_typ` | *Borreria typ* | unranked | ap=multipor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=multipor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `cerastium_fontanum` | *Cerastium fontanum* | unranked | ap=multipor* | class=medium | mid=36.0µm | sc={reticulaat}
  - `colchicum_autumnale` | *Colchicum autumnale* | unranked | ap=multipor* | size_MASKED | sc={reticulaat}
  - `phlox_subulata` | *Phlox subulata* | unranked | ap=multipor* | class=medium | mid=31.0µm | sc={reticulaat}
  - `silene_dioica` | *Silene dioica* | unranked | ap=multipor* | class=medium | mid=34.0µm | sc={reticulaat}
- Closest pair evidence `borreria_typ`–`borreria_verticilata` (d=0.375): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `borreria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cerastium_fontanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `colchicum_autumnale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C8 (n=6, mean_d=1.407)

- Shared aperture: stephanocol*
- Size classes: large, medium; mid range: (41.2, 44.2)
- Shared sculpture tokens: —
- Members:
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm
  - `salvia_argentea` | *Salvia argentea* | unranked | ap=stephanocol* | class=medium | mid=42.8µm
  - `salvia_officinalis` | *Salvia officinalis* | unranked | ap=stephanocol* | class=large | mid=42.5µm
  - `salvia_pratensis` | *Salvia pratensis* | unranked | ap=stephanocol* | class=large | mid=44.2µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `glechoma_hederacea`–`impatiens_noli_tangere` (d=0.775): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.775}`
- Provenance (sample): `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_argentea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C9 (n=6, mean_d=1.312)

- Shared aperture: peripor*
- Size classes: medium; mid range: (36.6, 41.1)
- Shared sculpture tokens: —
- Members:
  - `dianthus_deltoides` | *Dianthus Deltoides* | unranked | ap=peripor* | class=medium | mid=41.1µm
  - `papaver_argemone` | *Papaver argemone* | unranked | ap=peripor* | class=medium | mid=38.6µm | sc={clavaat,echinaat,gemmaat,microechinaat,microreticulaat}
  - `scirpus_sylvaticus` | *Scirpus sylvaticus* | unranked | ap=peripor* | class=medium | mid=37.4µm | sc={inaperturaat,periporaat,psilaat,scabraat}
  - `stellaria_graminea` | *Stellaria graminea* | unranked | ap=peripor* | class=medium | mid=36.6µm
  - `stellaria_holostea` | *Stellaria holostea* | unranked | ap=peripor* | class=medium | mid=39.9µm | sc={microechinaat,microreticulaat,scabraat}
  - `stellaria_nemorum` | *Stellaria nemorum* | unranked | ap=peripor* | class=medium | mid=40.2µm
- Closest pair evidence `stellaria_holostea`–`stellaria_nemorum` (d=0.795): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.795}`
- Provenance (sample): `dianthus_deltoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `papaver_argemone`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-papaver-argemone.json · `scirpus_sylvaticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `stellaria_graminea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C10 (n=5, mean_d=1.248)

- Shared aperture: monocol*
- Size classes: medium; mid range: (36.2, 42.2)
- Shared sculpture tokens: —
- Members:
  - `allium_fistulosum` | *Allium fistulosum* | unranked | ap=monocol* | class=medium | mid=36.2µm
  - `allium_senescens` | *Allium senescens* | unranked | ap=monocol* | class=medium | mid=39.0µm
  - `convallaria_majalis` | *Convallaria majalis* | unranked | ap=monocol* | class=medium | mid=42.2µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `leucojum_vernum` | *Leucojum vernum* | unranked | ap=monocol* | class=medium | mid=39.9µm
  - `liriodendron_tulipifera` | *Liriodendron tulipifera* | unranked | ap=monocol* | size_MASKED | sc={reticulaat,rugulaat,verrucaat}
- Closest pair evidence `allium_fistulosum`–`liriodendron_tulipifera` (d=0.900): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 1, 'distance': 0.9}`
- Provenance (sample): `allium_fistulosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_senescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `convallaria_majalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json · `leucojum_vernum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C11 (n=5, mean_d=1.458)

- Shared aperture: monocol*
- Size classes: large, medium; mid range: (43.9, 45.0)
- Shared sculpture tokens: —
- Members:
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm
  - `asphodeline_lutea` | *Asphodeline lutea* | unranked | ap=monocol* | class=large | mid=44.5µm
  - `hyacinthus_orientalis` | *Hyacinthus orientalis* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat}
  - `narcissus_typ` | *Narcissus typ* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat,scabraat}
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.745): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.745}`
- Provenance (sample): `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `asphodeline_lutea`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug09-monocolpatae-asphodelus.json · `hyacinthus_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `narcissus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C12 (n=5, mean_d=1.146)

- Shared aperture: monocol*
- Size classes: medium; mid range: (31.5, 33.8)
- Shared sculpture tokens: —
- Members:
  - `allium_porrum` | *Allium porrum* | unranked | ap=monocol* | class=medium | mid=33.3µm
  - `allium_scorodoprasum` | *Allium scorodoprasum* | unranked | ap=monocol* | class=medium | mid=33.8µm
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.1µm | sc={prolaat,psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `muscari_botryoides` | *Muscari botryoides* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={reticulaat}
- Closest pair evidence `allium_porrum`–`butomus_umbellatus` (d=0.755): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.755}`
- Provenance (sample): `allium_porrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_scorodoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `butomus_umbellatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json · `leucojum_aestivum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json

### C13 (n=5, mean_d=1.009)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (32.5, 35.8)
- Shared sculpture tokens: —
- Members:
  - `crepis_tectorum` | *Crepis tectorum* | unranked | ap=fenestr* | class=medium | mid=35.8µm
  - `crepis_vesicaria_ssp_taraxacifol` | *Crepis vesicaria* | unranked | ap=fenestr* | class=medium | mid=32.5µm
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm
  - `lapsana_communis` | *Lapsana communis* | unranked | ap=fenestr* | class=medium | mid=34.9µm
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.765): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.765}`
- Provenance (sample): `crepis_tectorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `crepis_vesicaria_ssp_taraxacifol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lapsana_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C14 (n=5, mean_d=1.268)

- Shared aperture: monocol*
- Size classes: large; mid range: (53.6, 57.8)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm
  - `magnolia_kobus` | *Magnolia kobus* | unranked | ap=monocol* | class=large | mid=53.6µm | sc={monocolpaat}
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `tulipa_sylvestris` | *Tulipa sylvestris* | unranked | ap=monocol* | class=large | mid=57.8µm | sc={rugulaat,striaat}
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.725): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.725}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `magnolia_kobus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C15 (n=4, mean_d=1.296)

- Shared aperture: multipor*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: scabraat
- Members:
  - `alnus_glutinosa` | *Alnus glutinosa* | unranked | ap=multipor* | class=medium | mid=26.0µm | sc={oblaat,psilaat,scabraat}
  - `carpinus_betulus` | *Carpinus betulus* | unranked | ap=multipor* | size_MASKED | sc={oblaat,psilaat,rond,scabraat}
  - `chenopodium_album` | *Chenopodium album* | unranked | ap=multipor* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `corylus_avellana` | *Corylus avellana* | unranked | ap=multipor* | class=medium | mid=27.0µm | sc={psilaat,scabraat}
- Closest pair evidence `alnus_glutinosa`–`carpinus_betulus` (d=0.675): `{'aperture': 'same multipor*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.25, 'shared': ['oblaat', 'psilaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `alnus_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpinus_betulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chenopodium_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylus_avellana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C16 (n=4, mean_d=1.122)

- Shared aperture: fenestr*
- Size classes: large; mid range: (51.0, 54.8)
- Shared sculpture tokens: —
- Members:
  - `cichorium_endivia` | *Cichorium endivia* | unranked | ap=fenestr* | class=large | mid=52.8µm
  - `leontodon_saxatilis` | *Leontodon saxatilis* | unranked | ap=fenestr* | class=large | mid=53.4µm
  - `prenanthes_purpurea` | *Prenanthes purpurea* | unranked | ap=fenestr* | class=large | mid=54.8µm
  - `tragopogon_pratensis` | *Tragopogon pratensis* | unranked | ap=fenestr* | class=large | mid=51.0µm
- Closest pair evidence `cichorium_endivia`–`leontodon_saxatilis` (d=0.855): `{'aperture': 'same fenestr*', 'size_class': 'same large', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.855}`
- Provenance (sample): `cichorium_endivia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `prenanthes_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tragopogon_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C17 (n=4, mean_d=1.370)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (6.2, 11.7)
- Shared sculpture tokens: —
- Members:
  - `cynoglossum_creticum` | *Cynoglossum creticum* | unranked | ap=heterocol* | class=very-small | mid=9.5µm
  - `myosotis_ramosissima` | *Myosotis ramosissima* | unranked | ap=heterocol* | class=very-small | mid=11.7µm
  - `myosotis_scorpioides` | *Myosotis scorpioides* | unranked | ap=heterocol* | class=very-small | mid=6.6µm | sc={heterocolpaat,psilaat}
  - `myosotis_sylvatica` | *Myosotis sylvatica* | unranked | ap=heterocol* | class=very-small | mid=6.2µm
- Closest pair evidence `myosotis_scorpioides`–`myosotis_sylvatica` (d=0.825): `{'aperture': 'same heterocol*', 'size_class': 'same very-small', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.825}`
- Provenance (sample): `cynoglossum_creticum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_ramosissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `myosotis_scorpioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug28-heterocolpatae-myosotis-sylvatica.json

### C18 (n=3, mean_d=0.945)

- Shared aperture: monocol*
- Size classes: medium; mid range: (26.0, 29.1)
- Shared sculpture tokens: —
- Members:
  - `allium_cepa` | *Allium cepa* | unranked | ap=monocol* | class=medium | mid=28.0µm | sc={psilaat,scabraat}
  - `allium_schoenoprasum` | *Allium schoenoprasum* | unranked | ap=monocol* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `galanthus_nivalis` | *Galanthus nivalis* | unranked | ap=monocol* | class=medium | mid=29.1µm
- Closest pair evidence `allium_cepa`–`allium_schoenoprasum` (d=0.525): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.525}`
- Provenance (sample): `allium_cepa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `allium_schoenoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `galanthus_nivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C19 (n=3, mean_d=1.308)

- Shared aperture: monocol*
- Size classes: small; mid range: (22.0, 23.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `asparagus_officinalis` | *Asparagus officinalis* | unranked | ap=monocol* | class=small | mid=23.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `asparagus_setaceus` | *Asparagus setaceus* | unranked | ap=monocol* | class=small | mid=22.0µm | sc={reticulaat}
- Closest pair evidence `allium_ursinum`–`asparagus_officinalis` (d=0.550): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'prolaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.55}`
- Provenance (sample): `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `asparagus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `asparagus_setaceus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C20 (n=3, mean_d=1.508)

- Shared aperture: 4colporaat
- Size classes: medium; mid range: (26.0, 31.5)
- Shared sculpture tokens: —
- Members:
  - `anchusa_officinalis` | *Anchusa officinalis* | unranked | ap=4colporaat | class=medium | mid=31.5µm | sc={psilaat,rugulaat}
  - `ceratonia_silqua` | *Ceratonia silqua* | unranked | ap=4colporaat | class=medium | mid=26.0µm
  - `nicotiana_tabacum` | *Nicotiana tabacum* | unranked | ap=4colporaat | class=medium | mid=31.0µm | sc={rugulaat}
- Closest pair evidence `anchusa_officinalis`–`nicotiana_tabacum` (d=1.225): `{'aperture': 'same 4colporaat', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.225}`
- Provenance (sample): `anchusa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ceratonia_silqua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nicotiana_tabacum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C21 (n=3, mean_d=1.592)

- Shared aperture: tripor*
- Size classes: medium; mid range: (24.1, 28.6)
- Shared sculpture tokens: —
- Members:
  - `betula_pendula` | *Betula pendula* | unranked | ap=tripor* | class=medium | mid=28.6µm | sc={reticulaat,scabraat}
  - `cannabis_sativa` | *Cannabis sativa* | unranked | ap=tripor* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `humulus_lupulus` | *Humulus lupulus* | unranked | ap=tripor* | class=medium | mid=24.1µm
- Closest pair evidence `cannabis_sativa`–`humulus_lupulus` (d=1.095): `{'aperture': 'same tripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.095}`
- Provenance (sample): `betula_pendula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cannabis_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `humulus_lupulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C22 (n=3, mean_d=1.518)

- Shared aperture: stephanocolpor*
- Size classes: medium; mid range: (32.5, 34.7)
- Shared sculpture tokens: —
- Members:
  - `borrago_officinalis` | *Borrago officinalis* | unranked | ap=stephanocolpor* | class=medium | mid=32.5µm | sc={scabraat,verrucaat}
  - `pulmonaria_montana` | *Pulmonaria montana* | unranked | ap=stephanocolpor* | class=medium | mid=34.7µm
  - `symphytum_officinale` | *Symphytum officinale* | unranked | ap=stephanocolpor* | class=medium | mid=33.0µm | sc={psilaat}
- Closest pair evidence `pulmonaria_montana`–`symphytum_officinale` (d=1.065): `{'aperture': 'same stephanocolpor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.7, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.065}`
- Provenance (sample): `borrago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_montana`: data/pollen.yaml:size; data/pollen.yaml:pollen_class_beug · `symphytum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C23 (n=3, mean_d=1.398)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (38.5, 43.5)
- Shared sculpture tokens: —
- Members:
  - `campanula_medium` | *Campanula medium* | unranked | ap=stephanopor* | class=medium | mid=42.2µm | sc={echinaat,microechinaat}
  - `campanula_persicifolia` | *Campanula persicifolia* | unranked | ap=stephanopor* | class=medium | mid=38.5µm
  - `campanula_rapunculoides` | *Campanula rapunculoides* | unranked | ap=stephanopor* | class=medium | mid=43.5µm
- Closest pair evidence `campanula_medium`–`campanula_rapunculoides` (d=0.985): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.3, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `campanula_medium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-medium.json · `campanula_persicifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_rapunculoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C24 (n=3, mean_d=1.425)

- Shared aperture: multipor*
- Size classes: medium; mid range: (39.0, 40.0)
- Shared sculpture tokens: —
- Members:
  - `fumaria_officinalis` | *Fumaria officinalis* | unranked | ap=multipor* | class=medium | mid=39.0µm | sc={psilaat}
  - `gramineae` | *Gramineae* | unranked | ap=multipor* | class=medium | mid=40.0µm | sc={psilaat,scabraat}
  - `phaseolus_coccin` | *Phaseolus coccin* | unranked | ap=multipor* | class=medium | mid=40.0µm | sc={scabraat}
- Closest pair evidence `gramineae`–`phaseolus_coccin` (d=0.875): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.875}`
- Provenance (sample): `fumaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `gramineae`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phaseolus_coccin`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C25 (n=3, mean_d=1.305)

- Shared aperture: inapert*
- Size classes: medium; mid range: (22.4, 27.0)
- Shared sculpture tokens: —
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | sc={gemmaat,inaperturaat,reticulaat,rond,scabraat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | sc={inaperturaat,reticulaat,rond,scabraat,verrucaat}
  - `thesium_alpinum` | *Thesium alpinum* | unranked | ap=inapert* | class=medium | mid=22.4µm
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.825): `{'aperture': 'same inapert*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.167, 'shared': ['inaperturaat', 'reticulaat', 'rond', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.825}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thesium_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C26 (n=3, mean_d=1.192)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (122.5, 126.0)
- Shared sculpture tokens: —
- Members:
  - `malva_alcea` | *Malva alcea* | unranked | ap=peripor* | class=very-large | mid=126.0µm
  - `malva_moschata` | *Malva moschata* | unranked | ap=peripor* | class=very-large | mid=122.5µm
  - `malva_sylvestris` | *Malva sylvestris* | unranked | ap=peripor* | class=very-large | mid=123.4µm
- Closest pair evidence `malva_moschata`–`malva_sylvestris` (d=0.905): `{'aperture': 'same peripor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.9, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.905}`
- Provenance (sample): `malva_alcea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `malva_moschata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `malva_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-malva-sylvestris.json

### C27 (n=3, mean_d=1.608)

- Shared aperture: peripor*
- Size classes: large; mid range: (46.5, 51.0)
- Shared sculpture tokens: —
- Members:
  - `polemonium_boreale` | *Polemonium boreale* | unranked | ap=peripor* | class=large | mid=48.4µm | sc={reticulaat,striaat}
  - `saponaria_officinalis` | *Saponaria officinalis* | unranked | ap=peripor* | class=large | mid=46.5µm
  - `silene_cucubalis` | *Silene cucubalis* | unranked | ap=peripor* | class=large | mid=51.0µm | sc={baculaat,clavaat,periporaat,reticulaat}
- Closest pair evidence `polemonium_boreale`–`saponaria_officinalis` (d=1.105): `{'aperture': 'same peripor*', 'size_class': 'same large', 'size_mid_gap_um': 1.9, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.105}`
- Provenance (sample): `polemonium_boreale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-polemonium.json · `saponaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `silene_cucubalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C28 (n=2, mean_d=0.125)

- Shared aperture: multipor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=multipor* | class=very-large | mid=175.0µm | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=multipor* | class=very-large | mid=175.0µm | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same multipor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C29 (n=2, mean_d=1.125)

- Shared aperture: multipor*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_lappa` | *Arctium lappa* | unranked | ap=multipor* | class=medium | mid=50.0µm | sc={echinaat,verrucaat}
  - `arcticum_majus` | *Arcticum majus* | unranked | ap=multipor* | class=medium | mid=50.0µm | sc={echinaat}
- Closest pair evidence `arcticum_lappa`–`arcticum_majus` (d=1.125): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `arcticum_lappa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arcticum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C30 (n=2, mean_d=1.500)

- Shared aperture: multipor*
- Size classes: medium; mid range: (33.5, 38.5)
- Shared sculpture tokens: echinaat, stephanoporaat, triporaat
- Members:
  - `campanula_latifolia` | *Campanula latifolia* | unranked | ap=multipor* | class=medium | mid=38.5µm | sc={echinaat,stephanoporaat,triporaat}
  - `campanula_rotundifolia` | *Campanula Rotundifolia* | unranked | ap=multipor* | class=medium | mid=33.5µm | sc={echinaat,stephanoporaat,triporaat,verrucaat}
- Closest pair evidence `campanula_latifolia`–`campanula_rotundifolia` (d=1.500): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 5.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['echinaat', 'stephanoporaat', 'triporaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.5}`
- Provenance (sample): `campanula_latifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `campanula_rotundifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C31 (n=2, mean_d=0.885)

- Shared aperture: tetrade*
- Size classes: large; mid range: (71.0, 71.8)
- Shared sculpture tokens: —
- Members:
  - `catalpa_bignonioides` | *Catalpa bignonioides* | unranked | ap=tetrade* | class=large | mid=71.0µm
  - `listera_cordata` | *Listera cordata* | unranked | ap=tetrade* | class=large | mid=71.8µm | sc={reticulaat,striaat}
- Closest pair evidence `catalpa_bignonioides`–`listera_cordata` (d=0.885): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.8, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.885}`
- Provenance (sample): `catalpa_bignonioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `listera_cordata`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-epipactis.json

### C32 (n=2, mean_d=0.500)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat, triporaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat,triporaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat,tetrade,triporaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.500): `{'aperture': 'same tripor*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['psilaat', 'rugulaat', 'triporaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.5}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C33 (n=2, mean_d=1.325)

- Shared aperture: 4colporaat
- Size classes: small; mid range: (22.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `citrus_sinensis` | *Citrus sinensis* | unranked | ap=4colporaat | class=small | mid=25.0µm
  - `fraxinus_ornus` | *Fraxinus ornus* | unranked | ap=4colporaat | class=small | mid=22.0µm | sc={microreticulaat,prolaat,reticulaat}
- Closest pair evidence `citrus_sinensis`–`fraxinus_ornus` (d=1.325): `{'aperture': 'same 4colporaat', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.325}`
- Provenance (sample): `citrus_sinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fraxinus_ornus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C34 (n=2, mean_d=1.792)

- Shared aperture: pericol*
- Size classes: medium; mid range: (33.8, 35.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `corydalis_cava` | *Corydalis cava* | unranked | ap=pericol* | class=medium | mid=35.0µm | sc={reticulaat,rugulaat,verrucaat}
  - `spergula_arvensis` | *Spergula arvensis* | unranked | ap=pericol* | class=medium | mid=33.8µm | sc={echinaat,microechinaat,pericolpaat,psilaat,reticulaat}
- Closest pair evidence `corydalis_cava`–`spergula_arvensis` (d=1.792): `{'aperture': 'same pericol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.778, 'shared': ['reticulaat', 'rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.7917}`
- Provenance (sample): `corydalis_cava`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spergula_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C35 (n=2, mean_d=1.595)

- Shared aperture: peripor*
- Size classes: large; mid range: (53.9, 58.2)
- Shared sculpture tokens: —
- Members:
  - `dianthus_plumarius` | *Dianthus plumarius* | unranked | ap=peripor* | class=large | mid=58.2µm
  - `persicaria_maculosa` | *Persicaria maculosa* | unranked | ap=peripor* | class=large | mid=53.9µm | sc={echinaat,microechinaat,reticulaat,striaat,verrucaat}
- Closest pair evidence `dianthus_plumarius`–`persicaria_maculosa` (d=1.595): `{'aperture': 'same peripor*', 'size_class': 'same large', 'size_mid_gap_um': 4.35, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.595}`
- Provenance (sample): `dianthus_plumarius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `persicaria_maculosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-persicaria.json

### C36 (n=2, mean_d=1.325)

- Shared aperture: 3
- Size classes: medium; mid range: (36.0, 37.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `diplotaxis_muralis` | *Diplotaxis muralis* | unranked | ap=3 | class=medium | mid=37.0µm | sc={reticulaat}
  - `veronica_filiformis` | *Veronica filiformis* | unranked | ap=3 | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `diplotaxis_muralis`–`veronica_filiformis` (d=1.325): `{'aperture': 'same 3', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.325}`
- Provenance (sample): `diplotaxis_muralis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_filiformis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C37 (n=2, mean_d=1.848)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (20.0, 21.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `galium_odoratum` | *Galium odoratum (syn Asperula odorata)* | unranked | ap=stephanocol* | class=small | mid=20.0µm | sc={reticulaat,scabraat}
  - `phacelia_tanacetifolia` | *Phacelia tanacetifolia* | unranked | ap=stephanocol* | class=small | mid=21.0µm | sc={heterocolpaat,microreticulaat,psilaat,reticulaat,rugulaat}
- Closest pair evidence `galium_odoratum`–`phacelia_tanacetifolia` (d=1.848): `{'aperture': 'same stephanocol*', 'size_class': 'same small', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.667, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.8483}`
- Provenance (sample): `galium_odoratum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phacelia_tanacetifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C38 (n=2, mean_d=1.175)

- Shared aperture: multipor*
- Size classes: small; mid range: (18.5, 20.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `humulus_typ` | *Humulus typ* | unranked | ap=multipor* | class=small | mid=20.0µm | sc={reticulaat,scabraat}
  - `thalictrum_typ` | *Thalictrum typ* | unranked | ap=multipor* | class=small | mid=18.5µm | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `humulus_typ`–`thalictrum_typ` (d=1.175): `{'aperture': 'same multipor*', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.175}`
- Provenance (sample): `humulus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thalictrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C39 (n=2, mean_d=1.525)

- Shared aperture: 6
- Size classes: medium; mid range: (38.0, 40.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=6 | class=medium | mid=38.0µm | sc={reticulaat}
  - `mimulus_guttatus` | *Mimulus guttatus* | unranked | ap=6 | class=medium | mid=40.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `lavandula_angisti`–`mimulus_guttatus` (d=1.525): `{'aperture': 'same 6', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.525}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mimulus_guttatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C40 (n=2, mean_d=0.375)

- Shared aperture: 1
- Size classes: large; mid range: (57.0, 57.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=1 | class=large | mid=57.0µm | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=1 | class=large | mid=57.0µm | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same 1', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C41 (n=2, mean_d=0.775)

- Shared aperture: tetrade*
- Size classes: large; mid range: (47.4, 47.6)
- Shared sculpture tokens: —
- Members:
  - `moneses_uniflora` | *Moneses uniflora* | unranked | ap=tetrade* | class=large | mid=47.4µm | sc={scabraat,tetrade,verrucaat}
  - `vaccinium_uliginosum` | *Vaccinium uliginosum* | unranked | ap=tetrade* | class=large | mid=47.6µm
- Closest pair evidence `moneses_uniflora`–`vaccinium_uliginosum` (d=0.775): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.775}`
- Provenance (sample): `moneses_uniflora`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json · `vaccinium_uliginosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C42 (n=2, mean_d=0.975)

- Shared aperture: syncol*
- Size classes: small; mid range: (17.0, 20.0)
- Shared sculpture tokens: psilaat
- **Human review (species↔*_typ):** nemophila_menziesii ↔ nemophila_typ
- Members:
  - `nemophila_menziesii` | *Nemophila menziesii* | unranked | ap=syncol* | class=small | mid=17.0µm | sc={psilaat}
  - `nemophila_typ` | *Nemophila typ* | unranked | ap=syncol* | class=small | mid=20.0µm | sc={psilaat}
- Closest pair evidence `nemophila_menziesii`–`nemophila_typ` (d=0.975): `{'aperture': 'same syncol*', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `nemophila_menziesii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nemophila_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C43 (n=2, mean_d=0.855)

- Shared aperture: monopor*
- Size classes: medium; mid range: (37.0, 37.6)
- Shared sculpture tokens: —
- Members:
  - `nymphaea_alba` | *Nymphaea alba* | unranked | ap=monopor* | class=medium | mid=37.0µm | sc={echinaat,fenestraat}
  - `phalaris_arundinacea` | *Phalaris arundinacea* | unranked | ap=monopor* | class=medium | mid=37.6µm
- Closest pair evidence `nymphaea_alba`–`phalaris_arundinacea` (d=0.855): `{'aperture': 'same monopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.855}`
- Provenance (sample): `nymphaea_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phalaris_arundinacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C44 (n=2, mean_d=1.575)

- Shared aperture: multipor*
- Size classes: medium; mid range: (33.5, 37.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `phaseolus_vulgaris` | *Phaseolus vulgaris* | unranked | ap=multipor* | class=medium | mid=37.0µm | sc={reticulaat,scabraat}
  - `ulmus_typ` | *Ulmus typ* | unranked | ap=multipor* | class=medium | mid=33.5µm | sc={reticulaat,rugulaat,scabraat}
- Closest pair evidence `phaseolus_vulgaris`–`ulmus_typ` (d=1.575): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 3.5, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.575}`
- Provenance (sample): `phaseolus_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ulmus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C45 (n=2, mean_d=0.900)

- Shared aperture: vesiculaat
- Size classes: large; mid range: (63.5, 65.0)
- Shared sculpture tokens: —
- Members:
  - `pinus_nigra` | *Pinus nigra* | unranked | ap=vesiculaat | class=large | mid=63.5µm
  - `pinus_sylvestris` | *Pinus sylvestris* | unranked | ap=vesiculaat | class=large | mid=65.0µm
- Closest pair evidence `pinus_nigra`–`pinus_sylvestris` (d=0.900): `{'aperture': 'same vesiculaat', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'dims_used': 3, 'distance': 0.9}`
- Provenance (sample): `pinus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `pinus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation

### C46 (n=2, mean_d=0.965)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (48.3, 49.5)
- Shared sculpture tokens: —
- Members:
  - `prunella_vulgaris` | *Prunella vulgaris* | unranked | ap=stephanocol* | class=large | mid=48.3µm
  - `salvia_glutinosa` | *Salvia glutinosa* | unranked | ap=stephanocol* | class=large | mid=49.5µm
- Closest pair evidence `prunella_vulgaris`–`salvia_glutinosa` (d=0.965): `{'aperture': 'same stephanocol*', 'size_class': 'same large', 'size_mid_gap_um': 1.2, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.965}`
- Provenance (sample): `prunella_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C47 (n=2, mean_d=1.365)

- Shared aperture: monocol*
- Size classes: large, medium; mid range: (49.0, 50.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `scilla_bifolia` | *Scilla bifolia* | unranked | ap=monocol* | class=large | mid=49.0µm | sc={reticulaat}
  - `scilla_nonscripta` | *Scilla nonscripta* | unranked | ap=monocol* | class=medium | mid=50.0µm | sc={reticulaat}
- Closest pair evidence `scilla_bifolia`–`scilla_nonscripta` (d=1.365): `{'aperture': 'same monocol*', 'size_class': 'adjacent large/medium', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.365}`
- Provenance (sample): `scilla_bifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scilla_nonscripta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

## 5. Looser clusters (close)

Clusters with ≥2 members at loose≤2.272 cut. Learning-priority clusters listed first.

- With ≥1 learning_priority_rank: **3**
- Unranked-only: **44**
- Total: **47**

### C1 (n=596, mean_d=4.136) — ranks [3, 5, 6, 11, 13, 15, 16, 21, 26, 29, 33, 34, 39, 40, 42, 44, 45, 53, 64, 71, 75]

- Shared aperture: tricol*
- Size classes: large, medium, small, very-large, very-small; mid range: (11.2, 107.9)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** pisum_sativum ↔ pisum_typ; lysimachia_vulgaris ↔ lysimachia_typ; lysimachia_nemorum ↔ lysimachia_typ; oxalis_corniculata ↔ oxalis_typ; lonicera_alpigena ↔ lonicera_typ; lonicera_caprifolium ↔ lonicera_typ; lonicera_xylosteum ↔ lonicera_typ; artemisia_dracunculus ↔ artemisia_typ; artemisia_vulgaris ↔ artemisia_typ; aconitum_napellus ↔ aconitum_typ; eryngium_maritimum ↔ eryngium_typ; eryngium_campestre ↔ eryngium_typ; eryngium_planum ↔ eryngium_typ; lupinus_angustifolius ↔ lupinus_typ; lupinus_polyphyllus ↔ lupinus_typ; lamium_purpureum ↔ lamium_typ; lamium_amplexicaule ↔ lamium_typ; lamium_album ↔ lamium_typ; lamium_maculatum_cv_var ↔ lamium_typ; sedum_acre ↔ sedum_typ; sedum_album ↔ sedum_typ; sedum_telephium ↔ sedum_typ; sedum_sexangulare ↔ sedum_typ; salix_aurita ↔ salix_typ; salix_repens ↔ salix_typ; salix_caprea ↔ salix_typ; salix_dasyclados ↔ salix_typ; salix_triandra ↔ salix_typ; salix_daphnoides ↔ salix_typ; salix_viminalis ↔ salix_typ; salix_cinerea ↔ salix_typ; salix_alba_var_tristis ↔ salix_typ; salix_fragilis ↔ salix_typ; salix_purpurea ↔ salix_typ; salix_pentandra ↔ salix_typ; aster_alpinus ↔ aster_typ; aster_amellus ↔ aster_typ; aster_sedifolius ↔ aster_typ; filipendula_vulgaris ↔ filipendula_typ; filipendula_ulmaria ↔ filipendula_typ; rubus_chamaemorus ↔ rubus_typ; rubus_fructicosus ↔ rubus_typ; rubus_fruticosus ↔ rubus_typ; rubus_saxatilis ↔ rubus_typ; rubus_caesius ↔ rubus_typ; rubus_idaeus ↔ rubus_typ; bidens_ferulifolia ↔ bidens_typ; senecio_squalidus ↔ senecio_typ; senecio_ovatus ↔ senecio_typ; senecio_aquaticus ↔ senecio_typ; senecio_jacobaea ↔ senecio_typ; senecio_paludosus ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_vulgaris ↔ senecio_typ; senecio_erucifolius ↔ senecio_typ; senecio_jacobea ↔ senecio_typ; arbutus_unedo ↔ arbutus_typ; ranunculus_ficaria ↔ ranunculus_typ; ranunculus_repens ↔ ranunculus_typ; ranunculus_acris ↔ ranunculus_typ; ranunculus_bulbosus ↔ ranunculus_typ; hydrangea_macrophylla ↔ hydrangea_typ; helianthemum_nummularium ↔ helianthemum_typ; crepis_biennis ↔ crepis_typ; galinsoga_parviflora ↔ galinsoga_typ; galinsoga_ciliata ↔ galinsoga_typ; melampyrum_pratense ↔ melampyrum_typ; mercurialis_annua ↔ mercurialis_typ; mercurialis_perennis ↔ mercurialis_typ; alyssum_repens ↔ alyssum_typ; alyssum_saxatile ↔ alyssum_typ; alyssum_montanum ↔ alyssum_typ; cytisus_scoparius ↔ cytisus_typ; malus_domestica ↔ malus_typ; malus_sylvestris ↔ malus_typ; euphorbia_cyparissias ↔ euphorbia_typ; euphorbia_amygdaloides ↔ euphorbia_typ; crambe_maritima ↔ crambe_typ; geranium_nodosum ↔ geranium_typ; geranium_dissectum ↔ geranium_typ; geranium_robertianum ↔ geranium_typ; geranium_phaeum ↔ geranium_typ; geranium_macrorrhizum ↔ geranium_typ; geranium_molle ↔ geranium_typ; geranium_sanguineum ↔ geranium_typ; geranium_pratense ↔ geranium_typ; geranium_pyrenaicum ↔ geranium_typ; rhinanthus_alectorolophus ↔ rhinanthus_typ; carduus_crispus ↔ carduus_typ; carduus_defloratus ↔ carduus_typ; carduus_nutans ↔ carduus_typ; hieracium_aurantiacum ↔ hieracium_typ; ulex_europaeus ↔ ulex_typ; serratula_tinctoria ↔ serratula_typ; veronica_arvensis ↔ veronica_typ; veronica_austriaca_ssp_teucrium ↔ veronica_typ; veronica_chamaedrys ↔ veronica_typ; veronica_officinalis ↔ veronica_typ; veronica_persica ↔ veronica_typ; parthenocissus_tricuspidata ↔ parthenocissus_typ; parthenocissus_quinquefolia ↔ parthenocissus_typ; symphoricarpos_albus ↔ symphoricarpos_typ; crataegus_monogyna ↔ crataegus_typ; crataegus_laevigata ↔ crataegus_typ; tamarix_gallica ↔ tamarix_typ; callicarpa_bodinieri ↔ callicarpa_typ; tilia_platyphyllos ↔ tilia_typ; tilia_americana ↔ tilia_typ; tilia_tomentosa ↔ tilia_typ
- **already_decided:** `acer_platanoides`–`centaurea_cyanus` (review:different); `acer_platanoides`–`malus_typ` (review:different); `acer_platanoides`–`ranunculus_typ` (review:different); `acer_platanoides`–`robinia_pseudoacacia` (review:different); `acer_platanoides`–`tilia_typ` (review:different); `aesculus_hippocastanum`–`melilotus_officinalis` (review:confirmed); `aesculus_hippocastanum`–`trifolium_repens` (review:confirmed); `ailanthus_altissima`–`tilia_typ` (review:different); `calluna_vulgaris`–`centaurea_cyanus` (review:different); `calluna_vulgaris`–`ranunculus_typ` (review:different); `calluna_vulgaris`–`tilia_typ` (review:different); `centaurea_cyanus`–`crataegus_typ` (review:different); `centaurea_cyanus`–`helianthus_annuus` (review:different); `centaurea_cyanus`–`ranunculus_typ` (review:different); `centaurea_cyanus`–`tilia_typ` (review:different); `centaurea_cyanus`–`trifolium_pratense` (review:confirmed); `centaurea_jacea`–`ranunculus_typ` (review:different); `centaurea_jacea`–`tilia_typ` (review:different); `cornus_mas`–`tilia_typ` (review:different); `crataegus_typ`–`tilia_typ` (review:different); `helianthus_annuus`–`ranunculus_typ` (review:different); `helianthus_annuus`–`tilia_typ` (review:different); `lamium_typ`–`tilia_typ` (review:different); `malus_typ`–`robinia_pseudoacacia` (review:different); `melilotus_officinalis`–`trifolium_repens` (review:confirmed); `polygonum_aviculare`–`tilia_typ` (review:different); `prunus_padus`–`prunus_serotina` (review:confirmed); `prunus_padus`–`rubus_typ` (review:confirmed); `prunus_serotina`–`rubus_typ` (review:confirmed); `ranunculus_typ`–`tilia_typ` (review:different); `rubus_typ`–`tilia_typ` (review:different); `tilia_typ`–`trifolium_pratense` (review:different)
- Members:
  - `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | sc={driehoekig,psilaat,striaat,tricolporaat}
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=38.1µm | sculpt_MASKED
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | size_MASKED | sc={driehoekig,prolaat,reticulaat,rond,tricolporaat}
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | sc={rond,rugulaat,striaat,tricolpaat}
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,rond,tricolpaat}
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,rond,tricolporaat}
  - `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat,rond,tricolpaat,verrucaat}
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | sc={psilaat,scabraat}
  - `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,reticulaat,rugulaat,striaat,tricolporaat}
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | size_MASKED | sc={driehoekig,oblaat,prolaat,psilaat,reticulaat}
  - `castanea_sativa` | *Castanea sativa* | rank=39 | ap=tricol* | class=very-small | mid=13.0µm | sc={prolaat,psilaat,rond,rugulaat,scabraat}
  - `polygonum_aviculare` | *Polygonum aviculare* | rank=40 | ap=tricol* | class=medium | mid=32.9µm | sc={driehoekig,oblaat,prolaat,psilaat,scabraat}
  - `amorpha_fruticosa` | *Amorpha fruticosa* | rank=42 | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat,verrucaat}
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | sc={striaat}
  - `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | size_MASKED | sc={prolaat,reticulaat,rond,tricolporaat}
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat,scabraat}
  - `calluna_vulgaris` | *Calluna vulgaris* | rank=64 | ap=tricol* | class=medium | mid=35.5µm | sc={echinaat,fenestraat,psilaat,scabraat,tetrade}
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=small | mid=25.0µm | sc={prolaat,psilaat,reticulaat,rond,scabraat}
  - `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=33.0µm | sc={driehoekig,echinaat,fenestraat,oblaat,scabraat}
  - `acanthus_mollis` | *Acanthus mollis* | unranked | ap=tricol* | class=large | mid=55.1µm | sc={prolaat,reticulaat}
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | sc={rugulaat,striaat,tricolpaat}
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `acer_monspessulanum` | *Acer monspessulanum* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,rugulaat,striaat,tricolpaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `acer_pseudoplatanus` | *Acer pseudoplatanus* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={rugulaat,striaat,tricolpaat,verrucaat}
  - `acer_tataricum_subsp_ginnala` | *Acer tataricum* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={striaat}
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat,fenestraat}
  - `aconitum_napellus` | *Aconitum napellus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={microreticulaat,psilaat}
  - `aconitum_typ` | *Aconitum typ* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,scabraat}
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={microreticulaat,psilaat,reticulaat}
  - `aegopodium_podagraria` | *Aegopodium podagraria* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={psilaat}
  - `aesculus_carnea` | *Aesculus carnea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={psilaat,rugulaat,striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=small | mid=24.0µm | sculpt_MASKED
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | sculpt_MASKED
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | sculpt_MASKED
  - `ajuga_reptans` | *Ajuga reptans* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,reticulaat,rond,rugulaat,tricolpaat}
  - `alchemilla_alpina` | *Alchemilla alpina* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={driehoekig,psilaat,tricolporaat}
  - `alliaria_petiolata` | *Alliaria petiolata* | unranked | ap=tricol* | sc={reticulaat}
  - `alyssum_montanum` | *Alyssum montanum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,reticulaat}
  - `alyssum_repens` | *Alyssum repens* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `alyssum_typ` | *Alyssum typ* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat}
  - `anchusa_arvensis` | *Anchusa arvensis* | unranked | ap=tricol* | class=medium | mid=48.0µm | sc={psilaat,scabraat}
  - `anemone_typ` | *Anemone typ* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `anethum_graveolens` | *Anethum graveolens* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={gemmaat,microreticulaat,reticulaat,scabraat,verrucaat}
  - `angelica_archangelica` | *Angelica archangelica* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={rugulaat}
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,verrucaat}
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat,fenestraat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `anthriscus_caucalis` | *Anthriscus caucalis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={psilaat}
  - `anthriscus_cerefolium` | *Anthriscus cerefolium* | unranked | ap=tricol* | class=medium | mid=20.2µm | sc={psilaat}
  - `anthriscus_sylvestris` | *Anthriscus sylvestris* | unranked | ap=tricol* | class=medium | mid=20.1µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `anthyllis_vulneraria` | *Anthyllis vulneraria* | unranked | ap=tricol* | class=large | mid=44.1µm | sc={driehoekig,oblaat,prolaat,psilaat,rugulaat}
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={microreticulaat,reticulaat}
  - `aquilegia_vulgaris` | *Aquilegia vulgaris* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={psilaat}
  - `arabis_hirsuta_ssp_hirsuta` | *Arabis hirsuta* | unranked | ap=tricol* | sc={reticulaat}
  - `arabis_procurrens` | *Arabis procurrens* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={reticulaat}
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `arbutus_typ` | *Arbutus typ* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
  - `arbutus_unedo` | *Arbutus unedo* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={driehoekig,psilaat,rond}
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat}
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | size_MASKED | sc={echinaat,fenestraat,tricolporaat}
  - `arctostaphylos_alpina` | *Arctostaphylos alpina* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={driehoekig,rond,scabraat,verrucaat}
  - `arctostaphylos_uva_ursi` | *Arctostaphylos uva-ursi* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={psilaat}
  - `armeria_maritima` | *Armeria maritima* | unranked | ap=tricol* | class=large | mid=68.0µm | sc={reticulaat,tricolpaat}
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | sc={echinaat}
  - `artemisia_dracunculus` | *Artemisia dracunculus* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={echinaat,psilaat,tricolporaat}
  - `artemisia_typ` | *Artemisia typ* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={echinaat,fenestraat}
  - `artemisia_vulgaris` | *Artemisia vulgaris* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={echinaat,reticulaat,tricolporaat}
  - `aruncus_dioicus` | *Aruncus dioicus* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={rugulaat,striaat}
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={echinaat,tricolporaat}
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={echinaat,tricolporaat}
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat}
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `atropa_bella_donna` | *Atropa bella* | unranked | ap=tricol* | class=medium | mid=46.0µm | sc={microreticulaat,prolaat,rugulaat,striaat}
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={echinaat}
  - `berteroa_incana` | *Berteroa incana* | unranked | ap=tricol* | sc={reticulaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={echinaat,fenestraat}
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat,tricolpaat}
  - `brassica_nigra` | *Brassica nigra* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat,tricolpaat}
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | sc={reticulaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={echinaat}
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat,fenestraat}
  - `callicarpa_bodinieri` | *Callicarpa bodinieri* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={rugulaat,scabraat,verrucaat}
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat,reticulaat}
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat}
  - `camelina_sativa` | *Camelina sativa* | unranked | ap=tricol* | sc={reticulaat}
  - `capsella_bursa_pastoris` | *Capsella bursa* | unranked | ap=tricol* | sc={reticulaat}
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={psilaat,reticulaat}
  - `caragana_arborescens` | *Caragana arborescens* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={scabraat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={reticulaat}
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={echinaat}
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carduus_nutans` | *Carduus nutans* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat,fenestraat}
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carragena_arbores` | *Carragena arbores* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={scabraat}
  - `carthamus_lanatus` | *Carthamus lanatus* | unranked | ap=tricol* | class=large | mid=66.0µm | sc={echinaat,fenestraat,prolaat}
  - `carthamus_tinctorius` | *Carthamus tinctorius* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={echinaat,fenestraat}
  - `carum_carvi` | *Carum carvi* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `ceanothus_americanus` | *Ceanothus americanus* | unranked | ap=tricol* | class=small | mid=19.4µm | sc={reticulaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | size_MASKED | sc={driehoekig,oblaat,prolaat,psilaat,reticulaat}
  - `centaurea_scabiosa` | *Centaurea scabiosa* | unranked | ap=tricol* | class=large | mid=54.0µm | sc={driehoekig,echinaat,oblaat,psilaat,scabraat}
  - `cercis_siliquastrum` | *Cercis siliquastrum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `chelidonium_majus` | *Chelidonium majus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,scabraat}
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `cichorium_intybus` | *Cichorium intybus* | unranked | ap=tricol* | class=medium | mid=38.0µm | sc={echinaat,fenestraat}
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cirsium_dissectum` | *Cirsium dissectum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_oleraceum` | *Cirsium oleraceum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_palustre` | *Cirsium palustre* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_rivulare` | *Cirsium rivulare* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_vulgare` | *Cirsium vulgare* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `cistus_albidus` | *Cistus albidus* | unranked | ap=tricol* | class=large | mid=45.1µm | sc={prolaat,reticulaat}
  - `cistus_incanus` | *Cistus incanus* | unranked | ap=tricol* | class=large | mid=49.4µm | sc={reticulaat}
  - `cistus_salviifolius` | *Cistus salviifolius* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={reticulaat}
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | sc={reticulaat}
  - `clematis_recta` | *Clematis recta* | unranked | ap=tricol* | class=small | mid=22.8µm | sc={scabraat,verrucaat}
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `clethra_alnifolia` | *Clethra alnifolia* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat,verrucaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat,fenestraat}
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | sc={reticulaat}
  - `coffea_typ` | *Coffea typ* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={scabraat}
  - `coincya_monensis_ssp_recurvata` | *Coincya monensis* | unranked | ap=tricol* | sc={reticulaat}
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={reticulaat}
  - `consolida_ajacis` | *Consolida ajacis* | unranked | ap=tricol* | sc={psilaat}
  - `consolida_regalis` | *Consolida regalis* | unranked | ap=tricol* | class=medium | mid=38.1µm | sc={psilaat}
  - `convolvulus_arve` | *Convolvulus arve* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={scabraat}
  - `convolvulus_arvensis` | *Convolvulus arvensis* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microechinaat,microreticulaat,prolaat,psilaat}
  - `coriandrum_sativum` | *Coriandrum sativum* | unranked | ap=tricol* | size_MASKED | sc={prolaat,reticulaat,scabraat,verrucaat}
  - `cornus_alba` | *Cornus alba* | unranked | ap=tricol* | class=medium | mid=42.1µm | sc={psilaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | sc={reticulaat}
  - `corylopsis_spicata` | *Corylopsis spicata* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={reticulaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={echinaat,fenestraat}
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `cotoneaster_niger` | *Cotoneaster niger* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={psilaat,striaat,tricolporaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crataegus_laevigata` | *Crataegus laevigata* | unranked | ap=tricol* | sc={striaat}
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | sc={rugulaat,striaat,tricolporaat}
  - `crepis_biennis` | *Crepis biennis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={echinaat,microreticulaat}
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat,fenestraat}
  - `cydonia_oblonga` | *Cydonia oblonga* | unranked | ap=tricol* | sc={striaat}
  - `cymbalaria_muralis` | *Cymbalaria muralis* | unranked | ap=tricol* | sc={reticulaat}
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | sc={echinaat}
  - `cynoglossum_officinale` | *Cynoglossum officinale* | unranked | ap=tricol* | class=small | mid=13.0µm | sc={heterocolpaat,psilaat,stephanocolporaat}
  - `cytisus_scoparius` | *Cytisus scoparius* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat,tricolpaat}
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat,scabraat}
  - `datura_stramonium` | *Datura stramonium* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={oblaat,rugulaat,striaat,verrucaat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,scabraat}
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={rugulaat}
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `digitalis_purpurea` | *Digitalis purpurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `dipsacus_fullonum` | *Dipsacus fullonum* | unranked | ap=tricol* | class=large | mid=89.0µm | sc={echinaat}
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `dryas_octopetala` | *Dryas octopetala* | unranked | ap=tricol* | size_MASKED | sc={striaat,tricolporaat}
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat,reticulaat,tricolporaat}
  - `elaeagnus_angustifolia` | *Elaeagnus angustifolia* | unranked | ap=tricol* | class=large | mid=42.6µm | sc={driehoekig,oblaat,psilaat,scabraat,tricolporaat}
  - `eleagnus_angustif` | *Eleagnus angustif* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={psilaat}
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm
  - `eranthis_hyemalis` | *Eranthis hyemalis* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={echinaat,microechinaat,prolaat,psilaat,scabraat}
  - `erica_arborea` | *Erica arborea* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={verrucaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={echinaat}
  - `erigeron_annuus` | *Erigeron annuus* | unranked | ap=tricol* | sc={echinaat}
  - `erigeron_canaden` | *Erigeron canadensis* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={echinaat,fenestraat}
  - `erodium_cicutarium` | *Erodium cicutarium* | unranked | ap=tricol* | class=large | mid=54.0µm | sc={striaat}
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | sc={reticulaat}
  - `eryngium_campestre` | *Eryngium campestre* | unranked | ap=tricol* | class=large | mid=49.5µm | sc={gemmaat,verrucaat}
  - `eryngium_maritimum` | *Eryngium maritimum* | unranked | ap=tricol* | class=large | mid=60.8µm | sc={psilaat}
  - `eryngium_planum` | *Eryngium planum* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={psilaat}
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat,scabraat}
  - `erysimum_cheiranthoides` | *Erysimum cheiranthoides* | unranked | ap=tricol* | class=small | mid=20.6µm | sc={reticulaat}
  - `erysimum_cheiri` | *Erysimum cheiri* | unranked | ap=tricol* | sc={reticulaat}
  - `escallonia_typ` | *Escallonia typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={psilaat}
  - `eucalyptus_camaldulensis` | *Eucalyptus camaldulensis* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={verrucaat}
  - `euodia_hupehensis` | *Euodia hupehensis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat,tricolporaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `euphorbia_amygdaloides` | *Euphorbia amygdaloides* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | sc={verrucaat}
  - `euphrasia_stricta` | *Euphrasia stricta* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={psilaat}
  - `fagopyrum_esculentum` | *Fagopyrum esculentum* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `fagus_sylvatica` | *Fagus sylvatica* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={reticulaat,rugulaat,scabraat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `fallopia_convolvulus` | *Fallopia convolvulus* | unranked | ap=tricol* | sc={psilaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `ferula_communis` | *Ferula communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={rugulaat,scabraat}
  - `ficaria_typ` | *Ficaria typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | sc={clavaat,echinaat,microechinaat,prolaat,psilaat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={clavaat,echinaat,microechinaat,prolaat,psilaat}
  - `foeniculum_vulga` | *Foeniculum vulga* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,verrucaat}
  - `foeniculum_vulgaris` | *Foeniculum vulgaris* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={scabraat}
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=23.7µm | sc={operculaat,prolaat,striaat}
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={operculaat,prolaat,striaat,tricolporaat}
  - `fragaria_viridis` | *Fragaria viridis* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={striaat,tricolporaat}
  - `frangula_alnus` | *Frangula alnus* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={driehoekig,oblaat,prolaat,psilaat,rond}
  - `fraxinus_excelsior` | *Fraxinus excelsior* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `galeopsis_speciosa` | *Galeopsis speciosa* | unranked | ap=tricol* | class=medium | mid=44.3µm | sc={reticulaat}
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `galinsoga_ciliata` | *Galinsoga ciliata* | unranked | ap=tricol* | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={echinaat}
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat,fenestraat}
  - `genista_anglica` | *Genista anglica* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `genista_pilosa` | *Genista pilosa* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={reticulaat}
  - `genista_tinctoria` | *Genista tinctoria* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={scabraat,verrucaat}
  - `geranium_dissectum` | *Geranium dissectum* | unranked | ap=tricol* | class=large | mid=55.0µm | sc={clavaat}
  - `geranium_macrorrhizum` | *Geranium macrorrhizum* | unranked | ap=tricol* | class=very-large | mid=89.0µm | sc={clavaat}
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | sc={clavaat}
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | sc={clavaat}
  - `geranium_pratense` | *Geranium pratense* | unranked | ap=tricol* | class=very-large | mid=107.9µm | sc={clavaat}
  - `geranium_pyrenaicum` | *Geranium pyrenaicum* | unranked | ap=tricol* | class=large | mid=64.8µm | sc={clavaat}
  - `geranium_robertianum` | *Geranium robertianum* | unranked | ap=tricol* | class=large | mid=66.2µm | sc={clavaat,rugulaat,striaat,tricolpaat}
  - `geranium_sanguineum` | *Geranium sanguineum* | unranked | ap=tricol* | class=very-large | mid=102.0µm | sc={clavaat}
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | sc={reticulaat}
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={operculaat,striaat,tricolporaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={operculaat,striaat,tricolporaat}
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={reticulaat}
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `hamamelis_japonica` | *Hamamelis japonica* | unranked | ap=tricol* | class=small | mid=21.3µm | sc={reticulaat}
  - `hedera_helix` | *Hedera helix* | unranked | ap=tricol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rond}
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={echinaat}
  - `helianthemum_nummularium` | *Helianthemum nummularium* | unranked | ap=tricol* | class=large | mid=30.9µm | sc={prolaat,reticulaat,striaat}
  - `helianthemum_typ` | *Helianthemum typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat}
  - `helichrysum_arenarium` | *Helichrysum arenarium* | unranked | ap=tricol* | sc={echinaat}
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={microreticulaat,prolaat,reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=42.9µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={echinaat,fenestraat}
  - `heracleum_sphondylium` | *Heracleum sphondylium* | unranked | ap=tricol* | class=medium | mid=38.5µm | sc={prolaat,psilaat,reticulaat,scabraat,tricolporaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={reticulaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat,fenestraat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | sc={striaat}
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={reticulaat,scabraat}
  - `hydrangea_macrophylla` | *Hydrangea macrophylla* | unranked | ap=tricol* | class=very-small | mid=13.0µm | sc={reticulaat}
  - `hydrangea_typ` | *Hydrangea typ* | unranked | ap=tricol* | class=very-small | mid=11.2µm | sc={psilaat}
  - `hypericum_androsaemum` | *Hypericum androsaemum* | unranked | ap=tricol* | class=small | mid=18.8µm | sc={reticulaat}
  - `hypericum_montanum` | *Hypericum montanum* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={reticulaat}
  - `hypericum_perforatum` | *Hypericum perforatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,tricolporaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `iberis_amara` | *Iberis amara* | unranked | ap=tricol* | class=medium | mid=25.7µm | sc={reticulaat}
  - `ilex_aquifolium` | *Ilex aquifolium* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={clavaat,prolaat,reticulaat,tricolpaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={echinaat}
  - `inula_conyzae` | *Inula conyzae* | unranked | ap=tricol* | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `koelreuteria_paniculata` | *Koelreuteria paniculata* | unranked | ap=tricol* | class=medium | mid=23.0µm | sc={reticulaat}
  - `kolkwitzia_amabilis` | *Kolkwitzia amabilis* | unranked | ap=tricol* | class=large | mid=52.0µm | sc={echinaat,scabraat,striaat}
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `lamium_album` | *Lamium album* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `lamium_maculatum_cv_var` | *Lamium maculatum* | unranked | ap=tricol* | class=medium | mid=28.7µm | sc={psilaat}
  - `lamium_purpureum` | *Lamium purpureum* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={reticulaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat,fenestraat}
  - `lathyrus_palustris` | *Lathyrus palustris* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={reticulaat}
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | sc={reticulaat}
  - `lathyrus_sylvestris` | *Lathyrus sylvestris* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={psilaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | sc={reticulaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | sc={reticulaat}
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `levisticum_officinale` | *Levisticum officinale* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={prolaat,psilaat}
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={reticulaat,tricolpaat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat,scabraat,striaat}
  - `limonium_vulgare` | *Limonium vulgare* | unranked | ap=tricol* | size_MASKED | sc={echinaat,reticulaat,scabraat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `linaria_repens` | *Linaria repens* | unranked | ap=tricol* | sc={reticulaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | sc={clavaat}
  - `linum_usitatissimum` | *Linum usitatissimum* | unranked | ap=tricol* | size_MASKED | sc={reticulaat,tricolpaat,verrucaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | sc={echinaat,tricolporaat}
  - `lonicera_typ` | *Lonicera typ* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat,fenestraat,reticulaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=52.8µm | sc={echinaat,prolaat}
  - `lotus_corniculatus` | *Lotus corniculatus* | unranked | ap=tricol* | class=small | mid=18.9µm | sc={prolaat,psilaat,rond,scabraat,tricolporaat}
  - `lotus_pedunculatus` | *Lotus pedunculatus (syn Lotus uliginosus)* | unranked | ap=tricol* | class=small | mid=14.9µm | sc={psilaat}
  - `lunaria_annua` | *Lunaria annua* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={reticulaat}
  - `lupinus_polyphyllus` | *Lupinus polyphyllus* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={striaat}
  - `lysimachia_nemorum` | *Lysimachia nemorum* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={prolaat,reticulaat}
  - `malus_domestica` | *Malus domestica* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `malus_sylvestris` | *Malus sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `malus_typ` | *Malus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat,rugulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat,tricolporaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={echinaat,tricolporaat}
  - `medicago_falcata` | *Medicago falcata* | unranked | ap=tricol* | class=medium | mid=31.9µm | sc={psilaat}
  - `medicago_lupulina` | *Medicago lupulina* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat,rugulaat}
  - `medicago_sativa` | *Medicago sativa* | unranked | ap=tricol* | size_MASKED | sc={prolaat,psilaat,reticulaat,rugulaat,scabraat}
  - `melampyrum_pratense` | *Melampyrum pratense* | unranked | ap=tricol* | class=medium | mid=23.1µm | sc={scabraat,verrucaat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `melittis_melissophyllum` | *Melittis melissophyllum* | unranked | ap=tricol* | class=medium | mid=43.8µm | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat}
  - `mercurialis_perennis` | *Mercurialis perennis* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mercurialis_typ` | *Mercurialis typ* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mespilus_germani` | *Mespilus germani* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={scabraat,striaat}
  - `mespilus_germanica` | *Mespilus germanica* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={psilaat,tricolporaat}
  - `misopates_orontium` | *Misopates orontium* | unranked | ap=tricol* | sc={reticulaat}
  - `nicandra_physalodes` | *Nicandra physalodes* | unranked | ap=tricol* | class=medium | mid=19.1µm | sc={driehoekig,psilaat,scabraat}
  - `nicotiana_glauca` | *Nicotiana glauca* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={rugulaat}
  - `nigella_arvensis` | *Nigella arvensis* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={echinaat,microechinaat,psilaat,scabraat,tricolpaat}
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | sc={psilaat,reticulaat}
  - `nigella_sativa` | *Nigella sativa* | unranked | ap=tricol* | class=medium | mid=43.1µm | sc={psilaat,reticulaat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat,scabraat}
  - `odontites_vernus_ssp_serotines` | *Odontites vernus* | unranked | ap=tricol* | sc={reticulaat}
  - `olea_europaea` | *Olea europaea* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microreticulaat,prolaat,reticulaat,scabraat}
  - `onobrychis_viciifolia` | *Onobrychis viciifolia* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={reticulaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat,fenestraat}
  - `onosis_spinoza` | *Ononis spinosa* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={psilaat}
  - `orlaya_grandiflora` | *Orlaya grandiflora* | unranked | ap=tricol* | class=large | mid=34.0µm | sc={psilaat}
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_sativus` | *Ornithopus sativus* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={psilaat}
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `oxalis_corniculata` | *Oxalis corniculata* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `oxalis_typ` | *Oxalis typ* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={reticulaat}
  - `paeonia_officinalis` | *Paeonia officinalis* | unranked | ap=tricol* | class=medium | mid=37.2µm | sc={microreticulaat,prolaat,reticulaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={psilaat}
  - `papaver_rhoeas` | *Papaver rhoeas* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,microechinaat,microreticulaat,reticulaat,scabraat}
  - `papaver_somniferum` | *Papaver somniferum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={psilaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={prolaat,reticulaat,rond}
  - `parthenocissus_quinquefolia` | *Parthenocissus quinquefolia* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat,rugulaat}
  - `parthenocissus_tricuspidata` | *Parthenocissus tricuspidata* | unranked | ap=tricol* | sc={reticulaat}
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `pastinaca_sativa` | *Pastinaca sativa* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `persicaria_bistorta` | *Persicaria bistorta* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat,scabraat}
  - `petasites_albus` | *Petasites albus* | unranked | ap=tricol* | sc={echinaat}
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat,fenestraat}
  - `philadelphus_coronarius` | *Philadelphus coronarius* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={psilaat,reticulaat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={psilaat,scabraat}
  - `picris_echioides` | *Picris echioides* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,scabraat}
  - `pimpinella_major` | *Pimpinella major* | unranked | ap=tricol* | class=medium | mid=24.4µm | sc={prolaat,psilaat}
  - `pimpinella_saxifraga` | *Pimpinella saxifraga* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={psilaat}
  - `pisum_sativum` | *Pisum sativum* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `pisum_typ` | *Pisum typ* | unranked | ap=tricol* | class=medium | mid=48.0µm | sc={reticulaat}
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={reticulaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `potentilla_anserina` | *Potentilla anserina* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={operculaat,prolaat,striaat,tricolporaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={striaat}
  - `potentilla_crantzii` | *Potentilla crantzii* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat,tricolporaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={striaat}
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={striaat}
  - `potentilla_palustris` | *Potentilla palustris* | unranked | ap=tricol* | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `prunus_armeniaca` | *Prunus armeniaca* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `prunus_avium` | *Prunus avium* | unranked | ap=tricol* | size_MASKED | sc={oblaat,rugulaat,striaat,tricolpaat,tricolporaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `prunus_domestica` | *Prunus domestica* | unranked | ap=tricol* | class=medium | mid=43.8µm | sc={striaat}
  - `prunus_dulcis` | *Prunus dulcis* | unranked | ap=tricol* | sc={striaat}
  - `prunus_laurocerasus` | *Prunus laurocerasus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={striaat}
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `prunus_padus` | *Prunus padus* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED
  - `prunus_persica` | *Prunus persica* | unranked | ap=tricol* | sc={striaat}
  - `prunus_serotina` | *Prunus serotina* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={psilaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | sc={rugulaat,striaat,tricolpaat,tricolporaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={striaat}
  - `ptelea_trifoliata` | *Ptelea trifoliata* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={microreticulaat,prolaat,reticulaat}
  - `pterostyrax_hispida` | *Pterostyrax hispida* | unranked | ap=tricol* | class=medium | mid=27.2µm | sc={psilaat}
  - `pulicaria_dysenterica` | *Pulicaria dysenterica* | unranked | ap=tricol* | sc={echinaat}
  - `pulsatilla_vulgaris` | *Pulsatilla vulgaris* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={scabraat,verrucaat}
  - `punica_granatum` | *Punica granatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={rond,scabraat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyrus_communis` | *Pyrus communis* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={rugulaat,scabraat,striaat,verrucaat}
  - `quercus_petraea` | *Quercus petraea* | unranked | ap=tricol* | sc={psilaat}
  - `quercus_robur` | *Quercus robur* | unranked | ap=tricol* | class=medium | mid=33.7µm | sc={echinaat,psilaat,reticulaat,tricolpaat}
  - `ranunculus_acris` | *Ranunculus acris* | unranked | ap=tricol* | class=medium | mid=30.9µm | sc={echinaat,microechinaat,psilaat,scabraat,tricolpaat}
  - `ranunculus_bulbosus` | *Ranunculus bulbosus* | unranked | ap=tricol* | class=medium | mid=30.8µm | sc={baculaat,verrucaat}
  - `ranunculus_ficaria` | *Ranunculus ficaria* | unranked | ap=tricol* | class=medium | mid=32.9µm | sc={clavaat,echinaat,scabraat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat,tricolpaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | sc={reticulaat}
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `rhamnus_cathartica` | *Rhamnus cathartica* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat,rugulaat}
  - `rhinanthus_alectorolophus` | *Rhinanthus alectorolophus* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={rugulaat,scabraat,striaat}
  - `rhinanthus_typ` | *Rhinanthus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | sc={reticulaat}
  - `rhus_typhina` | *Rhus typhina* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,striaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `robinia_pseudoacacia` | *Robinia pseudoacacia* | unranked | ap=tricol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rond}
  - `rorippa_amphibia` | *Rorippa amphibia* | unranked | ap=tricol* | sc={reticulaat}
  - `rorippa_austriaca` | *Rorippa austriaca* | unranked | ap=tricol* | sc={reticulaat}
  - `rorippa_sylvestris` | *Rorippa sylvestris* | unranked | ap=tricol* | sc={reticulaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={striaat}
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | sculpt_MASKED
  - `rosa_gallica_officinalis` | *Rosa gallica officinalis* | unranked | ap=tricol* | class=medium | mid=36.6µm | sc={operculaat,rugulaat,scabraat}
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={striaat}
  - `rubus_chamaemorus` | *Rubus chamaemorus* | unranked | ap=tricol* | size_MASKED | sc={clavaat,echinaat,prolaat,psilaat,scabraat}
  - `rubus_fructicosus` | *Rubus fructicosus* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat,striaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={rugulaat}
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | sculpt_MASKED
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={striaat,tricolporaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat,tricolporaat}
  - `ruta_graveolens` | *Ruta graveolens* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={microreticulaat,prolaat,rugulaat}
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat,tricolpaat}
  - `salix_aurita` | *Salix aurita* | unranked | ap=tricol* | class=medium | mid=22.5µm | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | sc={reticulaat,tricolpaat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={reticulaat}
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={reticulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat}
  - `salix_viminalis` | *Salix viminalis* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={reticulaat}
  - `sambucus_ebulus` | *Sambucus ebulus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={psilaat,reticulaat}
  - `sambucus_nigra` | *Sambucus nigra* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={prolaat,psilaat,reticulaat,tricolpaat,tricolporaat}
  - `sanguisorba_minor` | *Sanguisorba minor* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | sc={psilaat,reticulaat}
  - `saxifraga_rotundifolia` | *Saxifraga rotundifolia* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={psilaat,rugulaat,scabraat,striaat,tricolpaat}
  - `saxifraga_umbrosa` | *Saxifraga umbrosa* | unranked | ap=tricol* | class=medium | mid=35.1µm | sc={striaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=73.8µm | sc={echinaat,tricolpaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | sc={echinaat}
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `scrophularia_vernalis` | *Scrophularia vernalis* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `securigera_varia_coronilla_varia` | *Securigera varia* | unranked | ap=tricol* | sc={striaat}
  - `sedum_acre` | *Sedum acre* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={rugulaat,striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | sc={striaat}
  - `sedum_sexangulare` | *Sedum sexangulare* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={striaat}
  - `sedum_telephium` | *Sedum telephium* | unranked | ap=tricol* | class=small | mid=22.2µm | sc={striaat}
  - `sedum_typ` | *Sedum typ* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={psilaat,striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | sc={striaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={echinaat}
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,fenestraat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat,fenestraat,tricolporaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat,fenestraat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat,fenestraat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | sc={echinaat}
  - `silybum_marianum` | *Silybum marianum* | unranked | ap=tricol* | sc={echinaat,fenestraat}
  - `sinapis_alba` | *Sinapis alba* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat,tricolpaat}
  - `sisymbrium_officinale` | *Sisymbrium officinale* | unranked | ap=tricol* | sc={reticulaat}
  - `solanum_dulcamara` | *Solanum dulcamara* | unranked | ap=tricol* | class=small | mid=13.7µm | sc={driehoekig,oblaat,prolaat,psilaat,rond}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm
  - `solanum_lycopersicum` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=19.8µm | sc={prolaat,psilaat,rond,rugulaat,scabraat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | sc={psilaat}
  - `solanum_tuberosum` | *Solanum tuberosum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={psilaat}
  - `solidago_canadensis` | *Solidago canadensis* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={echinaat}
  - `solidago_virgaurea` | *Solidago virgaurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={echinaat,fenestraat}
  - `sonchus_arvensis` | *Sonchus arvensis* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat,fenestraat}
  - `sorbus_aria` | *Sorbus aria* | unranked | ap=tricol* | sc={striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={striaat,tricolporaat}
  - `spiraea_cantoniensis_x_trilobata` | *S. cantoniensis x S. trilobata* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat}
  - `spiraea_japonica` | *Spiraea japonica* | unranked | ap=tricol* | class=very-small | mid=12.5µm | sc={psilaat}
  - `stachys_arvensis` | *Stachys arvensis* | unranked | ap=tricol* | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={reticulaat}
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat}
  - `styrax_japonicus` | *Styrax japonicus* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={psilaat}
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat}
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat,fenestraat,striaat,tricolpaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `sylibum_marianum` | *Sylibum marianum* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={echinaat}
  - `symphoricarpos_albus` | *Symphoricarpos albus* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={prolaat,psilaat,rond,scabraat,tricolporaat}
  - `symphoricarpos_typ` | *Symphoricarpos typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={reticulaat,scabraat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat,fenestraat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `tamarix_typ` | *Tamarix typ* | unranked | ap=tricol* | class=small | mid=15.0µm | sc={reticulaat}
  - `tanacetum_corymbosum` | *Tanacetum corymbosum* | unranked | ap=tricol* | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={echinaat}
  - `taraxacum_officinale` | *Taraxacum officinale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat,fenestraat}
  - `telekia_speciosa` | *Telekia speciosa* | unranked | ap=tricol* | sc={echinaat}
  - `tephroseris_palustris` | *Tephroseris palustris* | unranked | ap=tricol* | sc={echinaat}
  - `teucrium_chamae` | *Teucrium chamae* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={scabraat}
  - `teucrium_chamaedrys` | *Teucrium chamaedrys* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={prolaat,rond,scabraat,verrucaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `tilia_americana` | *Tilia americana* | unranked | ap=tricol* | class=medium | mid=37.9µm | sc={reticulaat}
  - `tilia_platyphyllos` | *Tilia Platyphyllos* | unranked | ap=tricol* | class=medium | mid=37.3µm | sc={oblaat,reticulaat,rond,tricolporaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | sc={reticulaat}
  - `tordylium_apulum` | *Tordylium apulum* | unranked | ap=tricol* | size_MASKED | sc={rugulaat,scabraat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat,fenestraat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `trifolium_campestre` | *Trifolium campestre* | unranked | ap=tricol* | class=medium | mid=30.4µm | sc={reticulaat}
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={reticulaat}
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `tripleurospermum_maritimum` | *Tripleurospermum maritimum* | unranked | ap=tricol* | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={echinaat,fenestraat}
  - `trollius_europaeus` | *Trollius europaeus* | unranked | ap=tricol* | class=medium | mid=21.4µm | sc={prolaat,reticulaat,striaat,tricolpaat}
  - `tropaeolum_majus` | *Tropaeolum majus* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={reticulaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat,fenestraat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat,tricolpaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat}
  - `vaccinium_myrtillus` | *Vaccinium myrtillus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat,fenestraat,psilaat}
  - `vaccinium_oxycoccos` | *Vaccinium oxycoccos* | unranked | ap=tricol* | class=large | mid=48.0µm | sc={scabraat}
  - `vaccinium_vitis_idaea` | *Vaccinium vitis-idaea* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat,fenestraat,psilaat,scabraat,tetrade}
  - `valeriana_officinalis` | *Valeriana officinalis* | unranked | ap=tricol* | class=large | mid=45.5µm | sc={echinaat,prolaat,rugulaat,scabraat,tricolpaat}
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={reticulaat}
  - `verbascum_phlomoides` | *Verbascum phlomoides* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `verbascum_thapsus` | *Verbascum thapsus* | unranked | ap=tricol* | class=medium | mid=25.6µm | sc={reticulaat}
  - `verbena_officinalis` | *Verbena officinalis* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={driehoekig,oblaat,psilaat,rugulaat,scabraat}
  - `veronica_arvensis` | *Veronica arvensis* | unranked | ap=tricol* | class=medium | mid=24.6µm | sc={psilaat}
  - `veronica_austriaca_ssp_teucrium` | *Veronica austriaca* | unranked | ap=tricol* | class=medium | mid=39.6µm | sc={psilaat}
  - `veronica_chamaedrys` | *Veronica chamaedrys* | unranked | ap=tricol* | class=medium | mid=36.9µm | sc={psilaat}
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={psilaat}
  - `veronica_persica` | *Veronica persica* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={psilaat}
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,striaat}
  - `veronicastrum_sibiricum` | *Veronicastrum sibiricum* | unranked | ap=tricol* | class=small | mid=16.2µm | sc={microreticulaat,psilaat,reticulaat,scabraat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={reticulaat}
  - `vicia_cracca` | *Vicia cracca* | unranked | ap=tricol* | class=medium | mid=36.7µm | sc={prolaat,psilaat,reticulaat,rond,scabraat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={prolaat,reticulaat,rond,tricolporaat}
  - `vicia_hirsuta` | *Vicia hirsuta* | unranked | ap=tricol* | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `vicia_tetrasperma` | *Vicia tetrasperma* | unranked | ap=tricol* | sc={reticulaat}
  - `vicia_villosa` | *Vicia villosa* | unranked | ap=tricol* | class=medium | mid=38.6µm | sc={reticulaat}
  - `vinca_typ` | *Vinca typ* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | sc={psilaat}
  - `viola_odorata` | *Viola odorata* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={microreticulaat,prolaat,psilaat,reticulaat}
  - `viola_reichenbachiana` | *Viola reichenbachiana* | unranked | ap=tricol* | class=medium | mid=36.5µm | sc={psilaat}
  - `viola_riviniana` | *Viola riviniana* | unranked | ap=tricol* | class=medium | mid=34.3µm | sc={psilaat}
  - `viscum_album` | *Viscum album* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={echinaat,tricolpaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={microreticulaat,prolaat,reticulaat}
  - `vitis_vinifera` | *Vitis vinifera* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={psilaat,scabraat,tricolporaat}
  - `waldsteinia_ternata` | *Waldsteinia ternata* | unranked | ap=tricol* | sc={striaat}
  - `xanthium_italicum` | *Xanthium italicum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={scabraat}
  - `xanthium_strumarium` | *Xanthium strumarium* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={driehoekig,microechinaat,oblaat,psilaat,reticulaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | sc={echinaat}
- Closest pair evidence `anthemis_nobilis`–`taraxacum_officinale` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat', 'fenestraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `acanthus_mollis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_monspessulanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C2 (n=10, mean_d=1.639) — ranks [49]

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 41.1)
- Shared sculpture tokens: —
- Members:
  - `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | sc={baculaat,reticulaat,verrucaat}
  - `buxus_sempervirens` | *Buxus sempervirens* | unranked | ap=peripor* | class=medium | mid=33.5µm | sc={reticulaat}
  - `dianthus_deltoides` | *Dianthus Deltoides* | unranked | ap=peripor* | class=medium | mid=41.1µm
  - `papaver_argemone` | *Papaver argemone* | unranked | ap=peripor* | class=medium | mid=38.6µm | sc={clavaat,echinaat,gemmaat,microechinaat,microreticulaat}
  - `ribes_nigrum` | *Ribes nigrum* | unranked | ap=peripor* | class=medium | mid=35.2µm
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm
  - `scirpus_sylvaticus` | *Scirpus sylvaticus* | unranked | ap=peripor* | class=medium | mid=37.4µm | sc={inaperturaat,periporaat,psilaat,scabraat}
  - `stellaria_graminea` | *Stellaria graminea* | unranked | ap=peripor* | class=medium | mid=36.6µm
  - `stellaria_holostea` | *Stellaria holostea* | unranked | ap=peripor* | class=medium | mid=39.9µm | sc={microechinaat,microreticulaat,scabraat}
  - `stellaria_nemorum` | *Stellaria nemorum* | unranked | ap=peripor* | class=medium | mid=40.2µm
- Closest pair evidence `stellaria_holostea`–`stellaria_nemorum` (d=0.795): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.795}`
- Provenance (sample): `buxus_sempervirens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-buxus.json · `dianthus_deltoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `papaver_argemone`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-papaver-argemone.json · `ribes_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C3 (n=18, mean_d=1.386) — ranks [76]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (29.2, 38.9)
- Shared sculpture tokens: —
- Members:
  - `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | sc={reticulaat}
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat,stephanocolpaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `mentha_pulegium` | *Mentha pulegium* | unranked | ap=stephanocol* | class=medium | mid=29.2µm
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `origanum_majorana` | *Origanum majorana* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat,rugulaat}
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `satureja_montana` | *Satureja montana* | unranked | ap=stephanocol* | class=medium | mid=36.5µm
  - `thymus_praecox` | *Thymus praecox* | unranked | ap=stephanocol* | class=medium | mid=34.4µm
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.375): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_parviflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C4 (n=12, mean_d=1.408)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.2, 30.8)
- Shared sculpture tokens: —
- Members:
  - `alisma_lanceolatum` | *Alisma lanceolatum* | unranked | ap=peripor* | class=medium | mid=25.4µm
  - `alisma_plantago_aquatica` | *Alisma plantago* | unranked | ap=peripor* | class=medium | mid=26.9µm
  - `anemone_coronaria` | *Anemone coronaria* | unranked | ap=peripor* | class=medium | mid=30.8µm | sc={clavaat,echinaat,gemmaat,microechinaat,microreticulaat}
  - `chenopodium_bonus_henricus` | *Chenopodium bonus* | unranked | ap=peripor* | class=medium | mid=29.5µm
  - `daphne_mezereum` | *Daphne mezereum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={inaperturaat,periporaat,reticulaat,rond}
  - `gypsophila_paniculata` | *Gypsophila paniculata* | unranked | ap=peripor* | class=medium | mid=27.8µm
  - `plantago_lanceolata` | *Plantago Lanceolata* | unranked | ap=peripor* | class=medium | mid=25.1µm | sc={periporaat,verrucaat}
  - `plantago_major` | *Plantago major* | unranked | ap=peripor* | class=medium | mid=23.2µm
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm
  - `ribes_rubrum` | *Ribes rubrum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={periporaat,psilaat,rond,scabraat}
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm
  - `thymelaea_passerina` | *Thymelaea passerina* | unranked | ap=peripor* | class=medium | mid=24.2µm
- Closest pair evidence `ribes_alpinum`–`thalictrum_minus` (d=0.755): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.755}`
- Provenance (sample): `alisma_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `alisma_plantago_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-alisma-typ.json · `anemone_coronaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-anemone.json · `chenopodium_bonus_henricus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C5 (n=10, mean_d=1.642)

- Shared aperture: monocol*
- Size classes: large, medium; mid range: (36.2, 45.0)
- Shared sculpture tokens: —
- Members:
  - `allium_fistulosum` | *Allium fistulosum* | unranked | ap=monocol* | class=medium | mid=36.2µm
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm
  - `allium_senescens` | *Allium senescens* | unranked | ap=monocol* | class=medium | mid=39.0µm
  - `asphodeline_lutea` | *Asphodeline lutea* | unranked | ap=monocol* | class=large | mid=44.5µm
  - `convallaria_majalis` | *Convallaria majalis* | unranked | ap=monocol* | class=medium | mid=42.2µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `hyacinthus_orientalis` | *Hyacinthus orientalis* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat}
  - `leucojum_vernum` | *Leucojum vernum* | unranked | ap=monocol* | class=medium | mid=39.9µm
  - `liriodendron_tulipifera` | *Liriodendron tulipifera* | unranked | ap=monocol* | size_MASKED | sc={reticulaat,rugulaat,verrucaat}
  - `narcissus_typ` | *Narcissus typ* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat,scabraat}
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.745): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.745}`
- Provenance (sample): `allium_fistulosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_senescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `asphodeline_lutea`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug09-monocolpatae-asphodelus.json

### C6 (n=10, mean_d=1.653)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (30.4, 43.5)
- Shared sculpture tokens: —
- Members:
  - `campanula_cochleariifolia` | *Campanula cochleariifolia* | unranked | ap=stephanopor* | class=medium | mid=33.9µm
  - `campanula_glomerata` | *Campanula glomerata* | unranked | ap=stephanopor* | class=medium | mid=30.4µm
  - `campanula_medium` | *Campanula medium* | unranked | ap=stephanopor* | class=medium | mid=42.2µm | sc={echinaat,microechinaat}
  - `campanula_patula` | *Campanula patula* | unranked | ap=stephanopor* | class=medium | mid=32.5µm
  - `campanula_persicifolia` | *Campanula persicifolia* | unranked | ap=stephanopor* | class=medium | mid=38.5µm
  - `campanula_rapunculoides` | *Campanula rapunculoides* | unranked | ap=stephanopor* | class=medium | mid=43.5µm
  - `campanula_rapunculus` | *Campanula rapunculus* | unranked | ap=stephanopor* | class=medium | mid=34.8µm
  - `campanula_trachelium` | *Campanula trachelium* | unranked | ap=stephanopor* | class=medium | mid=35.2µm | sc={echinaat,microechinaat}
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.725): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.725}`
- Provenance (sample): `campanula_cochleariifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_glomerata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_medium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-medium.json · `campanula_patula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C7 (n=9, mean_d=1.522)

- Shared aperture: multipor*
- Size classes: medium; mid range: (30.0, 37.0)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** borreria_verticilata ↔ borreria_typ
- Members:
  - `borreria_typ` | *Borreria typ* | unranked | ap=multipor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=multipor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `cerastium_fontanum` | *Cerastium fontanum* | unranked | ap=multipor* | class=medium | mid=36.0µm | sc={reticulaat}
  - `colchicum_autumnale` | *Colchicum autumnale* | unranked | ap=multipor* | size_MASKED | sc={reticulaat}
  - `phaseolus_vulgaris` | *Phaseolus vulgaris* | unranked | ap=multipor* | class=medium | mid=37.0µm | sc={reticulaat,scabraat}
  - `phlox_subulata` | *Phlox subulata* | unranked | ap=multipor* | class=medium | mid=31.0µm | sc={reticulaat}
  - `ribes_sanguineum` | *Ribes sanguineum* | unranked | ap=multipor* | class=medium | mid=33.0µm | sc={periporaat,psilaat,rond,scabraat}
  - `silene_dioica` | *Silene dioica* | unranked | ap=multipor* | class=medium | mid=34.0µm | sc={reticulaat}
  - `ulmus_typ` | *Ulmus typ* | unranked | ap=multipor* | class=medium | mid=33.5µm | sc={reticulaat,rugulaat,scabraat}
- Closest pair evidence `borreria_typ`–`borreria_verticilata` (d=0.375): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `borreria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cerastium_fontanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `colchicum_autumnale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C8 (n=9, mean_d=1.304)

- Shared aperture: fenestr*
- Size classes: large, medium; mid range: (39.6, 44.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_laevigatum` | *Hieracium laevigatum* | unranked | ap=fenestr* | class=large | mid=44.0µm
  - `hieracium_sabaudum` | *Hieracium sabaudum* | unranked | ap=fenestr* | class=medium | mid=42.0µm
  - `hieracium_umbellatum` | *Hieracium umbellatum* | unranked | ap=fenestr* | class=medium | mid=39.6µm
  - `hypochaeris_radicata` | *Hypochaeris radicata* | unranked | ap=fenestr* | class=medium | mid=44.0µm
  - `lactuca_sativa` | *Lactuca sativa* | unranked | ap=fenestr* | class=medium | mid=40.4µm | sc={fenestraat}
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | sc={echinaat,fenestraat}
  - `leontodon_hispidus` | *Leontodon hispidus* | unranked | ap=fenestr* | class=medium | mid=44.5µm
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | sc={echinaat,fenestraat}
  - `sonchus_palustris` | *Sonchus palustris* | unranked | ap=fenestr* | class=medium | mid=43.2µm
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.505): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat', 'fenestraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.505}`
- Provenance (sample): `hieracium_laevigatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_sabaudum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hypochaeris_radicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C9 (n=8, mean_d=1.577)

- Shared aperture: monocol*
- Size classes: medium; mid range: (26.0, 33.8)
- Shared sculpture tokens: —
- Members:
  - `allium_cepa` | *Allium cepa* | unranked | ap=monocol* | class=medium | mid=28.0µm | sc={psilaat,scabraat}
  - `allium_porrum` | *Allium porrum* | unranked | ap=monocol* | class=medium | mid=33.3µm
  - `allium_schoenoprasum` | *Allium schoenoprasum* | unranked | ap=monocol* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `allium_scorodoprasum` | *Allium scorodoprasum* | unranked | ap=monocol* | class=medium | mid=33.8µm
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.1µm | sc={prolaat,psilaat,reticulaat,rugulaat,scabraat}
  - `galanthus_nivalis` | *Galanthus nivalis* | unranked | ap=monocol* | class=medium | mid=29.1µm
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `muscari_botryoides` | *Muscari botryoides* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={reticulaat}
- Closest pair evidence `allium_cepa`–`allium_schoenoprasum` (d=0.525): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.525}`
- Provenance (sample): `allium_cepa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `allium_porrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_schoenoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `allium_scorodoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C10 (n=6, mean_d=1.714)

- Shared aperture: multipor*
- Size classes: medium; mid range: (24.0, 28.0)
- Shared sculpture tokens: —
- Members:
  - `alnus_glutinosa` | *Alnus glutinosa* | unranked | ap=multipor* | class=medium | mid=26.0µm | sc={oblaat,psilaat,scabraat}
  - `amaranthus_caudatus` | *Amaranthus caudatus* | unranked | ap=multipor* | class=medium | mid=24.0µm | sc={scabraat}
  - `betula_nigra` | *Betula nigra* | unranked | ap=multipor* | class=medium | mid=24.5µm | sc={psilaat}
  - `carpinus_betulus` | *Carpinus betulus* | unranked | ap=multipor* | size_MASKED | sc={oblaat,psilaat,rond,scabraat}
  - `chenopodium_album` | *Chenopodium album* | unranked | ap=multipor* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `corylus_avellana` | *Corylus avellana* | unranked | ap=multipor* | class=medium | mid=27.0µm | sc={psilaat,scabraat}
- Closest pair evidence `alnus_glutinosa`–`carpinus_betulus` (d=0.675): `{'aperture': 'same multipor*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.25, 'shared': ['oblaat', 'psilaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `alnus_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `amaranthus_caudatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `betula_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpinus_betulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C11 (n=6, mean_d=1.407)

- Shared aperture: stephanocol*
- Size classes: large, medium; mid range: (41.2, 44.2)
- Shared sculpture tokens: —
- Members:
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm
  - `salvia_argentea` | *Salvia argentea* | unranked | ap=stephanocol* | class=medium | mid=42.8µm
  - `salvia_officinalis` | *Salvia officinalis* | unranked | ap=stephanocol* | class=large | mid=42.5µm
  - `salvia_pratensis` | *Salvia pratensis* | unranked | ap=stephanocol* | class=large | mid=44.2µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `glechoma_hederacea`–`impatiens_noli_tangere` (d=0.775): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.775}`
- Provenance (sample): `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_argentea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C12 (n=5, mean_d=1.009)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (32.5, 35.8)
- Shared sculpture tokens: —
- Members:
  - `crepis_tectorum` | *Crepis tectorum* | unranked | ap=fenestr* | class=medium | mid=35.8µm
  - `crepis_vesicaria_ssp_taraxacifol` | *Crepis vesicaria* | unranked | ap=fenestr* | class=medium | mid=32.5µm
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm
  - `lapsana_communis` | *Lapsana communis* | unranked | ap=fenestr* | class=medium | mid=34.9µm
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.765): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.765}`
- Provenance (sample): `crepis_tectorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `crepis_vesicaria_ssp_taraxacifol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lapsana_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C13 (n=5, mean_d=1.268)

- Shared aperture: monocol*
- Size classes: large; mid range: (53.6, 57.8)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm
  - `magnolia_kobus` | *Magnolia kobus* | unranked | ap=monocol* | class=large | mid=53.6µm | sc={monocolpaat}
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `tulipa_sylvestris` | *Tulipa sylvestris* | unranked | ap=monocol* | class=large | mid=57.8µm | sc={rugulaat,striaat}
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.725): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.725}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `magnolia_kobus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C14 (n=4, mean_d=1.122)

- Shared aperture: fenestr*
- Size classes: large; mid range: (51.0, 54.8)
- Shared sculpture tokens: —
- Members:
  - `cichorium_endivia` | *Cichorium endivia* | unranked | ap=fenestr* | class=large | mid=52.8µm
  - `leontodon_saxatilis` | *Leontodon saxatilis* | unranked | ap=fenestr* | class=large | mid=53.4µm
  - `prenanthes_purpurea` | *Prenanthes purpurea* | unranked | ap=fenestr* | class=large | mid=54.8µm
  - `tragopogon_pratensis` | *Tragopogon pratensis* | unranked | ap=fenestr* | class=large | mid=51.0µm
- Closest pair evidence `cichorium_endivia`–`leontodon_saxatilis` (d=0.855): `{'aperture': 'same fenestr*', 'size_class': 'same large', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.855}`
- Provenance (sample): `cichorium_endivia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `prenanthes_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tragopogon_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C15 (n=4, mean_d=1.370)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (6.2, 11.7)
- Shared sculpture tokens: —
- Members:
  - `cynoglossum_creticum` | *Cynoglossum creticum* | unranked | ap=heterocol* | class=very-small | mid=9.5µm
  - `myosotis_ramosissima` | *Myosotis ramosissima* | unranked | ap=heterocol* | class=very-small | mid=11.7µm
  - `myosotis_scorpioides` | *Myosotis scorpioides* | unranked | ap=heterocol* | class=very-small | mid=6.6µm | sc={heterocolpaat,psilaat}
  - `myosotis_sylvatica` | *Myosotis sylvatica* | unranked | ap=heterocol* | class=very-small | mid=6.2µm
- Closest pair evidence `myosotis_scorpioides`–`myosotis_sylvatica` (d=0.825): `{'aperture': 'same heterocol*', 'size_class': 'same very-small', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.825}`
- Provenance (sample): `cynoglossum_creticum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_ramosissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `myosotis_scorpioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug28-heterocolpatae-myosotis-sylvatica.json

### C16 (n=4, mean_d=1.740)

- Shared aperture: inapert*
- Size classes: medium; mid range: (22.4, 31.3)
- Shared sculpture tokens: —
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | sc={gemmaat,inaperturaat,reticulaat,rond,scabraat}
  - `populus_nigra` | *Populus nigra* | unranked | ap=inapert* | class=medium | mid=31.3µm | sc={inaperturaat,rond,scabraat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | sc={inaperturaat,reticulaat,rond,scabraat,verrucaat}
  - `thesium_alpinum` | *Thesium alpinum* | unranked | ap=inapert* | class=medium | mid=22.4µm
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.825): `{'aperture': 'same inapert*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.167, 'shared': ['inaperturaat', 'reticulaat', 'rond', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.825}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `populus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thesium_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C17 (n=3, mean_d=1.308)

- Shared aperture: monocol*
- Size classes: small; mid range: (22.0, 23.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | size_MASKED | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `asparagus_officinalis` | *Asparagus officinalis* | unranked | ap=monocol* | class=small | mid=23.0µm | sc={microreticulaat,prolaat,psilaat,reticulaat,rugulaat}
  - `asparagus_setaceus` | *Asparagus setaceus* | unranked | ap=monocol* | class=small | mid=22.0µm | sc={reticulaat}
- Closest pair evidence `allium_ursinum`–`asparagus_officinalis` (d=0.550): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'prolaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.55}`
- Provenance (sample): `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `asparagus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `asparagus_setaceus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C18 (n=3, mean_d=1.508)

- Shared aperture: 4colporaat
- Size classes: medium; mid range: (26.0, 31.5)
- Shared sculpture tokens: —
- Members:
  - `anchusa_officinalis` | *Anchusa officinalis* | unranked | ap=4colporaat | class=medium | mid=31.5µm | sc={psilaat,rugulaat}
  - `ceratonia_silqua` | *Ceratonia silqua* | unranked | ap=4colporaat | class=medium | mid=26.0µm
  - `nicotiana_tabacum` | *Nicotiana tabacum* | unranked | ap=4colporaat | class=medium | mid=31.0µm | sc={rugulaat}
- Closest pair evidence `anchusa_officinalis`–`nicotiana_tabacum` (d=1.225): `{'aperture': 'same 4colporaat', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.225}`
- Provenance (sample): `anchusa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ceratonia_silqua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nicotiana_tabacum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C19 (n=3, mean_d=1.592)

- Shared aperture: tripor*
- Size classes: medium; mid range: (24.1, 28.6)
- Shared sculpture tokens: —
- Members:
  - `betula_pendula` | *Betula pendula* | unranked | ap=tripor* | class=medium | mid=28.6µm | sc={reticulaat,scabraat}
  - `cannabis_sativa` | *Cannabis sativa* | unranked | ap=tripor* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `humulus_lupulus` | *Humulus lupulus* | unranked | ap=tripor* | class=medium | mid=24.1µm
- Closest pair evidence `cannabis_sativa`–`humulus_lupulus` (d=1.095): `{'aperture': 'same tripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.095}`
- Provenance (sample): `betula_pendula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cannabis_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `humulus_lupulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C20 (n=3, mean_d=1.518)

- Shared aperture: stephanocolpor*
- Size classes: medium; mid range: (32.5, 34.7)
- Shared sculpture tokens: —
- Members:
  - `borrago_officinalis` | *Borrago officinalis* | unranked | ap=stephanocolpor* | class=medium | mid=32.5µm | sc={scabraat,verrucaat}
  - `pulmonaria_montana` | *Pulmonaria montana* | unranked | ap=stephanocolpor* | class=medium | mid=34.7µm
  - `symphytum_officinale` | *Symphytum officinale* | unranked | ap=stephanocolpor* | class=medium | mid=33.0µm | sc={psilaat}
- Closest pair evidence `pulmonaria_montana`–`symphytum_officinale` (d=1.065): `{'aperture': 'same stephanocolpor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.7, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.065}`
- Provenance (sample): `borrago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_montana`: data/pollen.yaml:size; data/pollen.yaml:pollen_class_beug · `symphytum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C21 (n=3, mean_d=1.425)

- Shared aperture: multipor*
- Size classes: medium; mid range: (39.0, 40.0)
- Shared sculpture tokens: —
- Members:
  - `fumaria_officinalis` | *Fumaria officinalis* | unranked | ap=multipor* | class=medium | mid=39.0µm | sc={psilaat}
  - `gramineae` | *Gramineae* | unranked | ap=multipor* | class=medium | mid=40.0µm | sc={psilaat,scabraat}
  - `phaseolus_coccin` | *Phaseolus coccin* | unranked | ap=multipor* | class=medium | mid=40.0µm | sc={scabraat}
- Closest pair evidence `gramineae`–`phaseolus_coccin` (d=0.875): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.875}`
- Provenance (sample): `fumaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `gramineae`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phaseolus_coccin`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C22 (n=3, mean_d=1.192)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (122.5, 126.0)
- Shared sculpture tokens: —
- Members:
  - `malva_alcea` | *Malva alcea* | unranked | ap=peripor* | class=very-large | mid=126.0µm
  - `malva_moschata` | *Malva moschata* | unranked | ap=peripor* | class=very-large | mid=122.5µm
  - `malva_sylvestris` | *Malva sylvestris* | unranked | ap=peripor* | class=very-large | mid=123.4µm
- Closest pair evidence `malva_moschata`–`malva_sylvestris` (d=0.905): `{'aperture': 'same peripor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.9, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.905}`
- Provenance (sample): `malva_alcea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `malva_moschata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `malva_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-malva-sylvestris.json

### C23 (n=3, mean_d=1.675)

- Shared aperture: syncol*
- Size classes: small; mid range: (17.0, 23.0)
- Shared sculpture tokens: psilaat
- **Human review (species↔*_typ):** nemophila_menziesii ↔ nemophila_typ
- Members:
  - `nemophila_menziesii` | *Nemophila menziesii* | unranked | ap=syncol* | class=small | mid=17.0µm | sc={psilaat}
  - `nemophila_typ` | *Nemophila typ* | unranked | ap=syncol* | class=small | mid=20.0µm | sc={psilaat}
  - `sapindaceae` | *Sapindaceae* | unranked | ap=syncol* | class=small | mid=23.0µm | sc={psilaat,reticulaat}
- Closest pair evidence `nemophila_menziesii`–`nemophila_typ` (d=0.975): `{'aperture': 'same syncol*', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `nemophila_menziesii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nemophila_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sapindaceae`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C24 (n=3, mean_d=1.608)

- Shared aperture: peripor*
- Size classes: large; mid range: (46.5, 51.0)
- Shared sculpture tokens: —
- Members:
  - `polemonium_boreale` | *Polemonium boreale* | unranked | ap=peripor* | class=large | mid=48.4µm | sc={reticulaat,striaat}
  - `saponaria_officinalis` | *Saponaria officinalis* | unranked | ap=peripor* | class=large | mid=46.5µm
  - `silene_cucubalis` | *Silene cucubalis* | unranked | ap=peripor* | class=large | mid=51.0µm | sc={baculaat,clavaat,periporaat,reticulaat}
- Closest pair evidence `polemonium_boreale`–`saponaria_officinalis` (d=1.105): `{'aperture': 'same peripor*', 'size_class': 'same large', 'size_mid_gap_um': 1.9, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.105}`
- Provenance (sample): `polemonium_boreale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-polemonium.json · `saponaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `silene_cucubalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C25 (n=2, mean_d=0.125)

- Shared aperture: multipor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=multipor* | class=very-large | mid=175.0µm | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=multipor* | class=very-large | mid=175.0µm | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same multipor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C26 (n=2, mean_d=1.895)

- Shared aperture: monocol*
- Size classes: large; mid range: (71.9, 75.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `agave_striata` | *Agave striata* | unranked | ap=monocol* | class=large | mid=75.0µm | sc={reticulaat,rugulaat}
  - `ornithogalum_umbellatum` | *Ornithogalum umbellatum* | unranked | ap=monocol* | class=large | mid=71.9µm | sc={prolaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `agave_striata`–`ornithogalum_umbellatum` (d=1.895): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 3.1, 'sculpture': {'jaccard_dist': 0.6, 'shared': ['reticulaat', 'rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.895}`
- Provenance (sample): `agave_striata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ornithogalum_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json

### C27 (n=2, mean_d=1.125)

- Shared aperture: multipor*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_lappa` | *Arctium lappa* | unranked | ap=multipor* | class=medium | mid=50.0µm | sc={echinaat,verrucaat}
  - `arcticum_majus` | *Arcticum majus* | unranked | ap=multipor* | class=medium | mid=50.0µm | sc={echinaat}
- Closest pair evidence `arcticum_lappa`–`arcticum_majus` (d=1.125): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `arcticum_lappa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arcticum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C28 (n=2, mean_d=2.075)

- Shared aperture: multipor*
- Size classes: large; mid range: (80.0, 81.5)
- Shared sculpture tokens: psilaat
- Members:
  - `calystegia_sepium` | *Calystegia sepium* | unranked | ap=multipor* | class=large | mid=81.5µm | sc={gemmaat,psilaat,reticulaat,scabraat,verrucaat}
  - `zea_mays` | *Zea mays* | unranked | ap=multipor* | class=large | mid=80.0µm | sc={psilaat,rond}
- Closest pair evidence `calystegia_sepium`–`zea_mays` (d=2.075): `{'aperture': 'same multipor*', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.833, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 2.075}`
- Provenance (sample): `calystegia_sepium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `zea_mays`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C29 (n=2, mean_d=1.500)

- Shared aperture: multipor*
- Size classes: medium; mid range: (33.5, 38.5)
- Shared sculpture tokens: echinaat, stephanoporaat, triporaat
- Members:
  - `campanula_latifolia` | *Campanula latifolia* | unranked | ap=multipor* | class=medium | mid=38.5µm | sc={echinaat,stephanoporaat,triporaat}
  - `campanula_rotundifolia` | *Campanula Rotundifolia* | unranked | ap=multipor* | class=medium | mid=33.5µm | sc={echinaat,stephanoporaat,triporaat,verrucaat}
- Closest pair evidence `campanula_latifolia`–`campanula_rotundifolia` (d=1.500): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 5.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['echinaat', 'stephanoporaat', 'triporaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.5}`
- Provenance (sample): `campanula_latifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `campanula_rotundifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C30 (n=2, mean_d=0.885)

- Shared aperture: tetrade*
- Size classes: large; mid range: (71.0, 71.8)
- Shared sculpture tokens: —
- Members:
  - `catalpa_bignonioides` | *Catalpa bignonioides* | unranked | ap=tetrade* | class=large | mid=71.0µm
  - `listera_cordata` | *Listera cordata* | unranked | ap=tetrade* | class=large | mid=71.8µm | sc={reticulaat,striaat}
- Closest pair evidence `catalpa_bignonioides`–`listera_cordata` (d=0.885): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.8, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.885}`
- Provenance (sample): `catalpa_bignonioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `listera_cordata`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-epipactis.json

### C31 (n=2, mean_d=0.500)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat, triporaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat,triporaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat,tetrade,triporaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.500): `{'aperture': 'same tripor*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['psilaat', 'rugulaat', 'triporaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.5}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C32 (n=2, mean_d=1.325)

- Shared aperture: 4colporaat
- Size classes: small; mid range: (22.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `citrus_sinensis` | *Citrus sinensis* | unranked | ap=4colporaat | class=small | mid=25.0µm
  - `fraxinus_ornus` | *Fraxinus ornus* | unranked | ap=4colporaat | class=small | mid=22.0µm | sc={microreticulaat,prolaat,reticulaat}
- Closest pair evidence `citrus_sinensis`–`fraxinus_ornus` (d=1.325): `{'aperture': 'same 4colporaat', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.325}`
- Provenance (sample): `citrus_sinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fraxinus_ornus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C33 (n=2, mean_d=1.875)

- Shared aperture: 1
- Size classes: large; mid range: (52.0, 52.0)
- Shared sculpture tokens: —
- Members:
  - `colchicinum_autu` | *Colchicinum autu* | unranked | ap=1 | class=large | mid=52.0µm | sc={reticulaat}
  - `tulipa_typ` | *Tulipa typ* | unranked | ap=1 | class=large | mid=52.0µm | sc={rugulaat,striaat}
- Closest pair evidence `colchicinum_autu`–`tulipa_typ` (d=1.875): `{'aperture': 'same 1', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 1.0, 'shared': []}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.875}`
- Provenance (sample): `colchicinum_autu`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tulipa_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C34 (n=2, mean_d=1.792)

- Shared aperture: pericol*
- Size classes: medium; mid range: (33.8, 35.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `corydalis_cava` | *Corydalis cava* | unranked | ap=pericol* | class=medium | mid=35.0µm | sc={reticulaat,rugulaat,verrucaat}
  - `spergula_arvensis` | *Spergula arvensis* | unranked | ap=pericol* | class=medium | mid=33.8µm | sc={echinaat,microechinaat,pericolpaat,psilaat,reticulaat}
- Closest pair evidence `corydalis_cava`–`spergula_arvensis` (d=1.792): `{'aperture': 'same pericol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.778, 'shared': ['reticulaat', 'rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.7917}`
- Provenance (sample): `corydalis_cava`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spergula_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C35 (n=2, mean_d=1.595)

- Shared aperture: peripor*
- Size classes: large; mid range: (53.9, 58.2)
- Shared sculpture tokens: —
- Members:
  - `dianthus_plumarius` | *Dianthus plumarius* | unranked | ap=peripor* | class=large | mid=58.2µm
  - `persicaria_maculosa` | *Persicaria maculosa* | unranked | ap=peripor* | class=large | mid=53.9µm | sc={echinaat,microechinaat,reticulaat,striaat,verrucaat}
- Closest pair evidence `dianthus_plumarius`–`persicaria_maculosa` (d=1.595): `{'aperture': 'same peripor*', 'size_class': 'same large', 'size_mid_gap_um': 4.35, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.595}`
- Provenance (sample): `dianthus_plumarius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `persicaria_maculosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-persicaria.json

### C36 (n=2, mean_d=1.325)

- Shared aperture: 3
- Size classes: medium; mid range: (36.0, 37.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `diplotaxis_muralis` | *Diplotaxis muralis* | unranked | ap=3 | class=medium | mid=37.0µm | sc={reticulaat}
  - `veronica_filiformis` | *Veronica filiformis* | unranked | ap=3 | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `diplotaxis_muralis`–`veronica_filiformis` (d=1.325): `{'aperture': 'same 3', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.325}`
- Provenance (sample): `diplotaxis_muralis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_filiformis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C37 (n=2, mean_d=1.875)

- Shared aperture: 5
- Size classes: medium; mid range: (33.5, 36.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `eschscholzia_californica` | *Eschscholzia californica* | unranked | ap=5 | class=medium | mid=36.0µm | sc={psilaat,reticulaat}
  - `skimmia_typ` | *Skimmia typ* | unranked | ap=5 | class=medium | mid=33.5µm | sc={reticulaat,striaat}
- Closest pair evidence `eschscholzia_californica`–`skimmia_typ` (d=1.875): `{'aperture': 'same 5', 'size_class': 'same medium', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.875}`
- Provenance (sample): `eschscholzia_californica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `skimmia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C38 (n=2, mean_d=1.848)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (20.0, 21.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `galium_odoratum` | *Galium odoratum (syn Asperula odorata)* | unranked | ap=stephanocol* | class=small | mid=20.0µm | sc={reticulaat,scabraat}
  - `phacelia_tanacetifolia` | *Phacelia tanacetifolia* | unranked | ap=stephanocol* | class=small | mid=21.0µm | sc={heterocolpaat,microreticulaat,psilaat,reticulaat,rugulaat}
- Closest pair evidence `galium_odoratum`–`phacelia_tanacetifolia` (d=1.848): `{'aperture': 'same stephanocol*', 'size_class': 'same small', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.667, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.8483}`
- Provenance (sample): `galium_odoratum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phacelia_tanacetifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C39 (n=2, mean_d=1.175)

- Shared aperture: multipor*
- Size classes: small; mid range: (18.5, 20.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `humulus_typ` | *Humulus typ* | unranked | ap=multipor* | class=small | mid=20.0µm | sc={reticulaat,scabraat}
  - `thalictrum_typ` | *Thalictrum typ* | unranked | ap=multipor* | class=small | mid=18.5µm | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `humulus_typ`–`thalictrum_typ` (d=1.175): `{'aperture': 'same multipor*', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.175}`
- Provenance (sample): `humulus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thalictrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C40 (n=2, mean_d=1.525)

- Shared aperture: 6
- Size classes: medium; mid range: (38.0, 40.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=6 | class=medium | mid=38.0µm | sc={reticulaat}
  - `mimulus_guttatus` | *Mimulus guttatus* | unranked | ap=6 | class=medium | mid=40.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `lavandula_angisti`–`mimulus_guttatus` (d=1.525): `{'aperture': 'same 6', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.525}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mimulus_guttatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C41 (n=2, mean_d=0.375)

- Shared aperture: 1
- Size classes: large; mid range: (57.0, 57.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=1 | class=large | mid=57.0µm | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=1 | class=large | mid=57.0µm | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same 1', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C42 (n=2, mean_d=0.775)

- Shared aperture: tetrade*
- Size classes: large; mid range: (47.4, 47.6)
- Shared sculpture tokens: —
- Members:
  - `moneses_uniflora` | *Moneses uniflora* | unranked | ap=tetrade* | class=large | mid=47.4µm | sc={scabraat,tetrade,verrucaat}
  - `vaccinium_uliginosum` | *Vaccinium uliginosum* | unranked | ap=tetrade* | class=large | mid=47.6µm
- Closest pair evidence `moneses_uniflora`–`vaccinium_uliginosum` (d=0.775): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.775}`
- Provenance (sample): `moneses_uniflora`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json · `vaccinium_uliginosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C43 (n=2, mean_d=0.855)

- Shared aperture: monopor*
- Size classes: medium; mid range: (37.0, 37.6)
- Shared sculpture tokens: —
- Members:
  - `nymphaea_alba` | *Nymphaea alba* | unranked | ap=monopor* | class=medium | mid=37.0µm | sc={echinaat,fenestraat}
  - `phalaris_arundinacea` | *Phalaris arundinacea* | unranked | ap=monopor* | class=medium | mid=37.6µm
- Closest pair evidence `nymphaea_alba`–`phalaris_arundinacea` (d=0.855): `{'aperture': 'same monopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.855}`
- Provenance (sample): `nymphaea_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phalaris_arundinacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C44 (n=2, mean_d=2.075)

- Shared aperture: multipor*
- Size classes: medium; mid range: (45.0, 46.0)
- Shared sculpture tokens: —
- Members:
  - `pachysandra_terminalis` | *Pachysandra terminalis* | unranked | ap=multipor* | class=medium | mid=46.0µm | sc={clavaat,reticulaat}
  - `polemonium_caeruleum` | *Polemonium caeruleum* | unranked | ap=multipor* | class=medium | mid=45.0µm | sc={striaat}
- Closest pair evidence `pachysandra_terminalis`–`polemonium_caeruleum` (d=2.075): `{'aperture': 'same multipor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 1.0, 'shared': []}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 2.075}`
- Provenance (sample): `pachysandra_terminalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polemonium_caeruleum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C45 (n=2, mean_d=0.900)

- Shared aperture: vesiculaat
- Size classes: large; mid range: (63.5, 65.0)
- Shared sculpture tokens: —
- Members:
  - `pinus_nigra` | *Pinus nigra* | unranked | ap=vesiculaat | class=large | mid=63.5µm
  - `pinus_sylvestris` | *Pinus sylvestris* | unranked | ap=vesiculaat | class=large | mid=65.0µm
- Closest pair evidence `pinus_nigra`–`pinus_sylvestris` (d=0.900): `{'aperture': 'same vesiculaat', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'dims_used': 3, 'distance': 0.9}`
- Provenance (sample): `pinus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `pinus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation

### C46 (n=2, mean_d=0.965)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (48.3, 49.5)
- Shared sculpture tokens: —
- Members:
  - `prunella_vulgaris` | *Prunella vulgaris* | unranked | ap=stephanocol* | class=large | mid=48.3µm
  - `salvia_glutinosa` | *Salvia glutinosa* | unranked | ap=stephanocol* | class=large | mid=49.5µm
- Closest pair evidence `prunella_vulgaris`–`salvia_glutinosa` (d=0.965): `{'aperture': 'same stephanocol*', 'size_class': 'same large', 'size_mid_gap_um': 1.2, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.965}`
- Provenance (sample): `prunella_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C47 (n=2, mean_d=1.365)

- Shared aperture: monocol*
- Size classes: large, medium; mid range: (49.0, 50.0)
- Shared sculpture tokens: reticulaat
- Members:
  - `scilla_bifolia` | *Scilla bifolia* | unranked | ap=monocol* | class=large | mid=49.0µm | sc={reticulaat}
  - `scilla_nonscripta` | *Scilla nonscripta* | unranked | ap=monocol* | class=medium | mid=50.0µm | sc={reticulaat}
- Closest pair evidence `scilla_bifolia`–`scilla_nonscripta` (d=1.365): `{'aperture': 'same monocol*', 'size_class': 'adjacent large/medium', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.365}`
- Provenance (sample): `scilla_bifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scilla_nonscripta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

## 6. already_decided tags (summary)

- Decided pairs co-clustered at tight cut: 32
- Decided pairs co-clustered at loose cut: 32
- Per-cluster tags are listed under each cluster above; sources not modified.

## 7. Human review flags

- Clusters with species↔`*_typ` co-membership (loose cut): **3**
  - `acanthus_mollis`, `acer_campestre`, `acer_japonicum`, `acer_monspessulanum`, `acer_negundo`, `acer_opalus`, `acer_palmatum`, `acer_platanoides`, `acer_pseudoplatanus`, `acer_tataricum_subsp_ginnala`, `achillea_millefolium`, `aconitum_napellus`, `aconitum_typ`, `adonis_aestivalis`, `aegopodium_podagraria`, `aesculus_carnea`, `aesculus_hippoca`, `aesculus_hippocastanum`, `agrimonia_eupatoria`, `agrimonia_odorata`, `ailanthus_altissima`, `ajuga_reptans`, `alchemilla_alpina`, `alliaria_petiolata`, `alyssum_montanum`, `alyssum_repens`, `alyssum_saxatile`, `alyssum_typ`, `amorpha_fructico`, `amorpha_fruticosa`, `anacardium_occidentale`, `anchusa_arvensis`, `anemone_typ`, `anethum_graveolens`, `angelica_archangelica`, `angelica_sylvestris`, `anthemis_nobilis`, `anthemis_tinctoria`, `anthriscus_caucalis`, `anthriscus_cerefolium`, `anthriscus_sylvestris`, `anthyllis_vulneraria`, `antirrhinum_majus`, `aquilegia_vulgaris`, `arabis_hirsuta_ssp_hirsuta`, `arabis_procurrens`, `aralia_elata`, `arbutus_typ`, `arbutus_unedo`, `arcticum_minus`, `arctium_minus`, `arctostaphylos_alpina`, `arctostaphylos_uva_ursi`, `armeria_maritima`, `arnica_montana`, `artemisia_dracunculus`, `artemisia_typ`, `artemisia_vulgaris`, `aruncus_dioicus`, `aster_alpinus`, `aster_amellus`, `aster_sedifolius`, `aster_typ`, `astragalus_sinicus`, `astrantia_major`, `atropa_bella_donna`, `ballota_nigra_ssp_foetida`, `bellis_perennis`, `berteroa_incana`, `bidens_ferulifolia`, `bidens_typ`, `brassica_napus`, `brassica_nigra`, `brassica_oleracea`, `brassica_rapa`, `bunias_orientalis`, `buphthalmum_salicifolium`, `calendula_officinalis`, `callicarpa_bodinieri`, `callicarpa_typ`, `calluna_vulgaris`, `caltha_palustris`, `caltha_palustris_ssp_araneosa`, `camelina_sativa`, `capsella_bursa_pastoris`, `capsicum_annuum`, `caragana_arborescens`, `cardamine_flexuosa`, `cardamine_pratensis`, `carduus_crispus`, `carduus_defloratus`, `carduus_nutans`, `carduus_typ`, `carlina_acaulis`, `carlina_aucalis`, `carpobrotis_edulis`, `carpobrotus_edulis`, `carragena_arbores`, `carthamus_lanatus`, `carthamus_tinctorius`, `carum_carvi`, `castanea_sativa`, `ceanothus_americanus`, `centaurea_cyanus`, `centaurea_jacea`, `centaurea_montana`, `centaurea_scabiosa`, `cercis_siliquastrum`, `chelidonium_majus`, `chrysanthemum_leuc`, `chrysanthemum_segetum`, `cichorium_intybus`, `cirsium_arvense`, `cirsium_dissectum`, `cirsium_oleraceum`, `cirsium_palustre`, `cirsium_rivulare`, `cirsium_vulgare`, `cistus_albidus`, `cistus_incanus`, `cistus_salviifolius`, `citrullus_lanatus`, `clematis_recta`, `clematis_vitalba`, `clethra_alnifolia`, `cnicus_benedict`, `cochlearia_officinalis_ssp_off`, `coffea_typ`, `coincya_monensis_ssp_recurvata`, `colutea_arborescens`, `consolida_ajacis`, `consolida_regalis`, `convolvulus_arve`, `convolvulus_arvensis`, `coriandrum_sativum`, `cornus_alba`, `cornus_mas`, `cornus_sanguinea`, `corylopsis_parcifl`, `corylopsis_pauciflora`, `corylopsis_spicata`, `cosmos_typ`, `cotoneaster_integerrimus`, `cotoneaster_niger`, `crambe_maritima`, `crambe_typ`, `crataegus_laevigata`, `crataegus_monogyna`, `crataegus_typ`, `crepis_biennis`, `crepis_typ`, `cydonia_oblonga`, `cymbalaria_muralis`, `cynara_cardunculus`, `cynoglossum_officinale`, `cytisus_scoparius`, `cytisus_typ`, `datura_stramonium`, `daucus_carota`, `davidia_involucrata`, `deutzia_typ`, `digitalis_purpurea`, `diplotaxis_tenuifolia`, `dipsacus_fullonum`, `dipsacus_pilosus`, `doronicum_pardalianches`, `dryas_octopetala`, `echinops_sphaer`, `echinops_sphaerocephalus`, `echium_vulgare`, `elaeagnus_angustifolia`, `eleagnus_angustif`, `empetrum_nigrum`, `eranthis_hyemalis`, `erica_arborea`, `erigeron_acer`, `erigeron_annuus`, `erigeron_canaden`, `erodium_cicutarium`, `erophila_verna`, `eryngium_campestre`, `eryngium_maritimum`, `eryngium_planum`, `eryngium_typ`, `erysimum_cheiranthoides`, `erysimum_cheiri`, `escallonia_typ`, `eucalyptus_camaldulensis`, `euodia_hupehensis`, `euonymus_europaeus`, `eupatorium_cann`, `eupatorium_cannabinum`, `euphorbia_amygdaloides`, `euphorbia_cyparissias`, `euphorbia_typ`, `euphrasia_stricta`, `fagopyrum_esculentum`, `fagus_sylvatica`, `fallopia_baldschur`, `fallopia_convolvulus`, `fallopia_japonica`, `ferula_communis`, `ficaria_typ`, `filipendula_typ`, `filipendula_ulmaria`, `filipendula_vulgaris`, `foeniculum_vulga`, `foeniculum_vulgare`, `foeniculum_vulgaris`, `fragaria_moschata`, `fragaria_vesca`, `fragaria_viridis`, `frangula_alnus`, `fraxinus_excelsior`, `galeopsis_segetum`, `galeopsis_speciosa`, `galeopsis_tetrahit`, `galinsoga_ciliata`, `galinsoga_parviflora`, `galinsoga_typ`, `genista_anglica`, `genista_pilosa`, `genista_tinctoria`, `geranium_dissectum`, `geranium_macrorrhizum`, `geranium_molle`, `geranium_nodosum`, `geranium_phaeum`, `geranium_pratense`, `geranium_pyrenaicum`, `geranium_robertianum`, `geranium_sanguineum`, `geranium_typ`, `geum_rivale`, `geum_urbanum`, `glaucium_flavum`, `gleditsia_triacanthos`, `hamamelis_japonica`, `hedera_helix`, `hedysarum_corona`, `helenium_autumn`, `helianthemum_nummularium`, `helianthemum_typ`, `helianthus_annuus`, `helichrysum_arenarium`, `helleborus_foetidus`, `helleborus_niger`, `helleborus_viridis_ssp_occidentalis`, `helminthotheca_echioides`, `heracleum_sphondylium`, `hesperis_matronalis`, `hieracium_aurantiacum`, `hieracium_typ`, `hippocrepis_comosa`, `hippopha_rhamn`, `hippophae_rhamnoides`, `hydrangea_macrophylla`, `hydrangea_typ`, `hypericum_androsaemum`, `hypericum_montanum`, `hypericum_perforatum`, `hypericum_polyph`, `hypericum_tetrapterum`, `iberis_amara`, `ilex_aquifolium`, `inula_britannica`, `inula_conyzae`, `inula_ensifolia`, `inula_helenium`, `inula_salicina`, `koelreuteria_paniculata`, `kolkwitzia_amabilis`, `laburnum_anagyroides`, `lamium_album`, `lamium_amplexicaule`, `lamium_maculatum_cv_var`, `lamium_purpureum`, `lamium_typ`, `lampsana_commu`, `lampsana_communis`, `lathyrus_palustris`, `lathyrus_pratensis`, `lathyrus_sylvestris`, `lathyrus_tuberosus`, `leontodon_autum`, `leonurus_cardiaca`, `lepidium_sativum`, `leucanthemum_vulgare`, `levisticum_officinale`, `ligustrum_vulgare`, `limnanthes_douglasii`, `limonium_vulgare`, `linaria_cymbalaria`, `linaria_repens`, `linaria_vulg`, `linaria_vulgaris`, `linum_flavum`, `linum_usitatissimum`, `lonicera_alpigena`, `lonicera_caprifolium`, `lonicera_typ`, `lonicera_xylosteum`, `lotus_corniculatus`, `lotus_pedunculatus`, `lunaria_annua`, `lupinus_angustifolius`, `lupinus_polyphyllus`, `lupinus_typ`, `lycium_barbarum`, `lysimachia_nemorum`, `lysimachia_typ`, `lysimachia_vulgaris`, `malus_domestica`, `malus_sylvestris`, `malus_typ`, `mangifera_indica`, `marrubium_vulgare`, `matricaria_chamo`, `matricaria_chamomilla`, `matricaria_recutita`, `medicago_falcata`, `medicago_lupulina`, `medicago_sativa`, `melampyrum_pratense`, `melampyrum_typ`, `melilotus_albus`, `melilotus_officinalis`, `melittis_melissophyllum`, `mercurialis_annua`, `mercurialis_perennis`, `mercurialis_typ`, `mespilus_germani`, `mespilus_germanica`, `misopates_orontium`, `nicandra_physalodes`, `nicotiana_glauca`, `nigella_arvensis`, `nigella_damascena`, `nigella_sativa`, `odontites_vernus`, `odontites_vernus_ssp_serotines`, `olea_europaea`, `onobrychis_viciifolia`, `ononis`, `ononis_natrix`, `ononis_repens_ssp_repens`, `ononis_spinosa`, `onopordon_acant`, `onopordum_acanthium`, `onosis_spinoza`, `orlaya_grandiflora`, `ornithopus_perpus`, `ornithopus_perpusillus`, `ornithopus_sativus`, `osmanthus_typ`, `oxalis_corniculata`, `oxalis_typ`, `paeonia_officinalis`, `papaver_dubium`, `papaver_rhoeas`, `papaver_somniferum`, `parnassia_palustris`, `parthenocissus_quinquefolia`, `parthenocissus_tricuspidata`, `parthenocissus_typ`, `pastinaca_sativa`, `persicaria_bistorta`, `petasites_albus`, `petasitis_officinalis`, `philadelphus_coronarius`, `photinia_typ`, `picris_echioides`, `pimpinella_anisum`, `pimpinella_major`, `pimpinella_saxifraga`, `pisum_sativum`, `pisum_typ`, `platanus_hybr`, `polygonum_aviculare`, `polygonum_convol`, `potentilla_anserina`, `potentilla_aurea`, `potentilla_crantzii`, `potentilla_erecta`, `potentilla_fruticosa`, `potentilla_grandiflora`, `potentilla_norvegica`, `potentilla_palustris`, `potentilla_recta`, `prunus_armeniaca`, `prunus_avium`, `prunus_cerasifera`, `prunus_cerasus`, `prunus_domestica`, `prunus_dulcis`, `prunus_laurocerasus`, `prunus_mahaleb`, `prunus_padus`, `prunus_persica`, `prunus_serotina`, `prunus_spinosa`, `prunus_spinoza`, `ptelea_trifoliata`, `pterostyrax_hispida`, `pulicaria_dysenterica`, `pulsatilla_vulgaris`, `punica_granatum`, `pyracantha_coccin`, `pyracantha_coccinea`, `pyrus_communis`, `quercus_petraea`, `quercus_robur`, `ranunculus_acris`, `ranunculus_bulbosus`, `ranunculus_ficaria`, `ranunculus_repens`, `ranunculus_typ`, `raphanus_raph`, `raphanus_raphanistrum`, `raphanus_sativus`, `reseda_lutea`, `reseda_luteola`, `rhamnus_cathartica`, `rhinanthus_alectorolophus`, `rhinanthus_typ`, `rhus_chinensis`, `rhus_typhina`, `ricinus_communis`, `robinia_pseudoacacia`, `rorippa_amphibia`, `rorippa_austriaca`, `rorippa_sylvestris`, `rosa_arvensis`, `rosa_canina`, `rosa_gallica_officinalis`, `rosa_glauca`, `rosa_majalis`, `rosa_spinosissima`, `rosa_tomentosa`, `rosa_villosa`, `rubus_caesius`, `rubus_chamaemorus`, `rubus_fructicosus`, `rubus_fruticosus`, `rubus_idaeus`, `rubus_saxatilis`, `rubus_typ`, `rudbeckia_hirta`, `rumex_obtusifolius`, `ruta_graveolens`, `salix_alba_var_tristis`, `salix_aurita`, `salix_caprea`, `salix_cinerea`, `salix_daphnoides`, `salix_dasyclados`, `salix_fragilis`, `salix_pentandra`, `salix_purpurea`, `salix_repens`, `salix_triandra`, `salix_typ`, `salix_viminalis`, `sambucus_ebulus`, `sambucus_nigra`, `sanguisorba_minor`, `sarothamnus_sco`, `saxifraga_granulata`, `saxifraga_rotundifolia`, `saxifraga_umbrosa`, `scabiosa_columbaria`, `scabiosa_ochroleuca`, `scrophularia_auriculata`, `scrophularia_nodosa`, `scrophularia_umbrosa`, `scrophularia_vernalis`, `securigera_varia_coronilla_varia`, `sedum_acre`, `sedum_album`, `sedum_sexangulare`, `sedum_telephium`, `sedum_typ`, `sempervivum_tectorum`, `senecio_aquaticus`, `senecio_erucifolius`, `senecio_inaequalis`, `senecio_jacobaea`, `senecio_jacobea`, `senecio_ovatus`, `senecio_paludosus`, `senecio_squalidus`, `senecio_typ`, `senecio_vulgaris`, `serratula_tinctoria`, `serratula_typ`, `serrulata_tinctoria`, `silphium_perfoliatum`, `silybum_marianum`, `sinapis_alba`, `sinapis_arvensis`, `sisymbrium_officinale`, `solanum_dulcamara`, `solanum_lycopers`, `solanum_lycopersicum`, `solanum_nigrum_ssp_nigrum`, `solanum_tuberosum`, `solidago_canadensis`, `solidago_gigantea`, `solidago_virgaurea`, `sonchus_arvensis`, `sorbus_aria`, `sorbus_aucuparia`, `spiraea_cantoniensis_x_trilobata`, `spiraea_japonica`, `stachys_arvensis`, `stachys_palustris`, `stachys_sylvatica`, `styrax_japonicus`, `succisa_praten`, `succisa_pratensis`, `sulla_coronaria`, `sylibum_marianum`, `symphoricarpos_albus`, `symphoricarpos_typ`, `symphyotrichum_lanceolatum`, `syringa_vulgaris`, `tagetes_erecta`, `tamarix_gallica`, `tamarix_typ`, `tanacetum_corymbosum`, `tanacetum_vulgare`, `taraxacum_officinale`, `telekia_speciosa`, `tephroseris_palustris`, `teucrium_chamae`, `teucrium_chamaedrys`, `thlaspi_arvense`, `tilia_americana`, `tilia_platyphyllos`, `tilia_tomentosa`, `tilia_typ`, `tordylium_apulum`, `tragopogon_typ`, `trifolium_arvense`, `trifolium_campestre`, `trifolium_dubium`, `trifolium_fragiferum`, `trifolium_incarnat`, `trifolium_incarnatum`, `trifolium_pratense`, `trifolium_repens`, `tripleurospermum_maritimum`, `tripolium_pannonicum`, `trollius_europaeus`, `tropaeolum_majus`, `tussilago_farfara`, `ulex_europaeus`, `ulex_typ`, `vaccinium_myrtillus`, `vaccinium_oxycoccos`, `vaccinium_vitis_idaea`, `valeriana_officinalis`, `verbascum_blattaria`, `verbascum_densiflorum`, `verbascum_nigrum`, `verbascum_phlomoides`, `verbascum_thapsus`, `verbena_officinalis`, `veronica_arvensis`, `veronica_austriaca_ssp_teucrium`, `veronica_chamaedrys`, `veronica_officinalis`, `veronica_persica`, `veronica_typ`, `veronicastrum_sibiricum`, `viburnum_lantana`, `viburnum_opulus`, `viburnum_tinus`, `vicia_cracca`, `vicia_faba`, `vicia_hirsuta`, `vicia_sepium`, `vicia_tetrasperma`, `vicia_villosa`, `vinca_typ`, `viola_hirta`, `viola_odorata`, `viola_reichenbachiana`, `viola_riviniana`, `viscum_album`, `vitex_agnus_castus`, `vitis_vinifera`, `waldsteinia_ternata`, `xanthium_italicum`, `xanthium_strumarium`, `xeranthemum_annuum`: pisum_sativum ↔ pisum_typ; lysimachia_vulgaris ↔ lysimachia_typ; lysimachia_nemorum ↔ lysimachia_typ; oxalis_corniculata ↔ oxalis_typ; lonicera_alpigena ↔ lonicera_typ; lonicera_caprifolium ↔ lonicera_typ; lonicera_xylosteum ↔ lonicera_typ; artemisia_dracunculus ↔ artemisia_typ; artemisia_vulgaris ↔ artemisia_typ; aconitum_napellus ↔ aconitum_typ; eryngium_maritimum ↔ eryngium_typ; eryngium_campestre ↔ eryngium_typ; eryngium_planum ↔ eryngium_typ; lupinus_angustifolius ↔ lupinus_typ; lupinus_polyphyllus ↔ lupinus_typ; lamium_purpureum ↔ lamium_typ; lamium_amplexicaule ↔ lamium_typ; lamium_album ↔ lamium_typ; lamium_maculatum_cv_var ↔ lamium_typ; sedum_acre ↔ sedum_typ; sedum_album ↔ sedum_typ; sedum_telephium ↔ sedum_typ; sedum_sexangulare ↔ sedum_typ; salix_aurita ↔ salix_typ; salix_repens ↔ salix_typ; salix_caprea ↔ salix_typ; salix_dasyclados ↔ salix_typ; salix_triandra ↔ salix_typ; salix_daphnoides ↔ salix_typ; salix_viminalis ↔ salix_typ; salix_cinerea ↔ salix_typ; salix_alba_var_tristis ↔ salix_typ; salix_fragilis ↔ salix_typ; salix_purpurea ↔ salix_typ; salix_pentandra ↔ salix_typ; aster_alpinus ↔ aster_typ; aster_amellus ↔ aster_typ; aster_sedifolius ↔ aster_typ; filipendula_vulgaris ↔ filipendula_typ; filipendula_ulmaria ↔ filipendula_typ; rubus_chamaemorus ↔ rubus_typ; rubus_fructicosus ↔ rubus_typ; rubus_fruticosus ↔ rubus_typ; rubus_saxatilis ↔ rubus_typ; rubus_caesius ↔ rubus_typ; rubus_idaeus ↔ rubus_typ; bidens_ferulifolia ↔ bidens_typ; senecio_squalidus ↔ senecio_typ; senecio_ovatus ↔ senecio_typ; senecio_aquaticus ↔ senecio_typ; senecio_jacobaea ↔ senecio_typ; senecio_paludosus ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_vulgaris ↔ senecio_typ; senecio_erucifolius ↔ senecio_typ; senecio_jacobea ↔ senecio_typ; arbutus_unedo ↔ arbutus_typ; ranunculus_ficaria ↔ ranunculus_typ; ranunculus_repens ↔ ranunculus_typ; ranunculus_acris ↔ ranunculus_typ; ranunculus_bulbosus ↔ ranunculus_typ; hydrangea_macrophylla ↔ hydrangea_typ; helianthemum_nummularium ↔ helianthemum_typ; crepis_biennis ↔ crepis_typ; galinsoga_parviflora ↔ galinsoga_typ; galinsoga_ciliata ↔ galinsoga_typ; melampyrum_pratense ↔ melampyrum_typ; mercurialis_annua ↔ mercurialis_typ; mercurialis_perennis ↔ mercurialis_typ; alyssum_repens ↔ alyssum_typ; alyssum_saxatile ↔ alyssum_typ; alyssum_montanum ↔ alyssum_typ; cytisus_scoparius ↔ cytisus_typ; malus_domestica ↔ malus_typ; malus_sylvestris ↔ malus_typ; euphorbia_cyparissias ↔ euphorbia_typ; euphorbia_amygdaloides ↔ euphorbia_typ; crambe_maritima ↔ crambe_typ; geranium_nodosum ↔ geranium_typ; geranium_dissectum ↔ geranium_typ; geranium_robertianum ↔ geranium_typ; geranium_phaeum ↔ geranium_typ; geranium_macrorrhizum ↔ geranium_typ; geranium_molle ↔ geranium_typ; geranium_sanguineum ↔ geranium_typ; geranium_pratense ↔ geranium_typ; geranium_pyrenaicum ↔ geranium_typ; rhinanthus_alectorolophus ↔ rhinanthus_typ; carduus_crispus ↔ carduus_typ; carduus_defloratus ↔ carduus_typ; carduus_nutans ↔ carduus_typ; hieracium_aurantiacum ↔ hieracium_typ; ulex_europaeus ↔ ulex_typ; serratula_tinctoria ↔ serratula_typ; veronica_arvensis ↔ veronica_typ; veronica_austriaca_ssp_teucrium ↔ veronica_typ; veronica_chamaedrys ↔ veronica_typ; veronica_officinalis ↔ veronica_typ; veronica_persica ↔ veronica_typ; parthenocissus_tricuspidata ↔ parthenocissus_typ; parthenocissus_quinquefolia ↔ parthenocissus_typ; symphoricarpos_albus ↔ symphoricarpos_typ; crataegus_monogyna ↔ crataegus_typ; crataegus_laevigata ↔ crataegus_typ; tamarix_gallica ↔ tamarix_typ; callicarpa_bodinieri ↔ callicarpa_typ; tilia_platyphyllos ↔ tilia_typ; tilia_americana ↔ tilia_typ; tilia_tomentosa ↔ tilia_typ
  - `borreria_typ`, `borreria_verticilata`, `cerastium_fontanum`, `colchicum_autumnale`, `phaseolus_vulgaris`, `phlox_subulata`, `ribes_sanguineum`, `silene_dioica`, `ulmus_typ`: borreria_verticilata ↔ borreria_typ
  - `nemophila_menziesii`, `nemophila_typ`, `sapindaceae`: nemophila_menziesii ↔ nemophila_typ

- Borderline: conflict-masked taxa appear with MASKED tags; treat size/sculpt agreement as unreliable.
- Sparse taxa (appendix) were not forced into clusters.

## 8. Limits / risks

- Missing morph fields lower confidence via distance inflate; empty never treated as a match.
- Kerkvliet morph from section titles / YAML enrichment is **analytic**, not dichotomous source.
- Conflict mask removes unreliable dims but can leave taxa under-specified (easier false merges on remaining dims).
- No synonym / fuzzy Latin merge; duplicate concepts under different slugs stay separate.
- Key **topology** (late forks, co-endpoints) is intentionally unused as a similarity signal.
- Tokenization of free-text sculpture/shape is heuristic; compound phrases may under-match.
- Linkage detail: UPGMA within aperture-family blocks; Kruskal single-link within blocks n>200.
- This report does not confirm or promote lookalikes.

## Appendix A. Sparse / singleton taxa

Taxa with &lt;2 usable feature dimensions (not forced into clusters).

- `acer_cappadocicum` | *Acer cappadocicum* | unranked | ap=aperturmembranensindnichtornamentiert · features=1
- `alchemilla_acutiloba` | *Alchemilla acutiloba* | unranked | sc={driehoekig,psilaat,tricolporaat} · features=1
- `anemone_apennina` | *Anemone apennina* | unranked | class=medium | mid=24.9µm · features=1
- `anemone_ranunculoides` | *Anemone ranunculoides* | unranked | class=medium | mid=28.2µm · features=1
- `anemone_sylvestris` | *Anemone sylvestris* | unranked | class=small | mid=17.9µm · features=1
- `anthyllis_barba_jovis` | *Anthyllis barba-jovis* | unranked | class=medium | mid=30.1µm · features=1
- `ceratocapnos_claviculata_corydalis_claviculata` | *Ceratocapnos claviculata* | unranked | ap=pericol* · features=1
- `chaerophyllum_bulbosum` | *Chaerophyllum bulbosum* | unranked | class=medium | mid=25.1µm · features=1
- `corydalis_solida` | *Corydalis solida* | unranked | ap=pericol* · features=1
- `cotoneaster_intergerrimus` | *Cotoneaster intergerrimus* | unranked | class=medium | mid=33.0µm | sculpt_MASKED · features=1
- `crepis_capillaris` | *Crepis capillaris* | unranked | ap=fenestr* · features=1
- `crepis_paludosa` | *Crepis paludosa* | unranked | ap=fenestr* · features=1
- `epipactis_palustris` | *Epipactis palustris* | unranked | ap=tetrade* · features=1
- `erica_vagans` | *Erica vagans* | unranked | class=medium | mid=33.1µm · features=1
- `fallopia_baldschuanica` | *Fallopia baldschuanica* | unranked | sc={reticulaat} · features=1
- `gilia_capitata` | *Gilia Capitata* | unranked | sc={stephanoporaat,striaat} · features=1
- `helenium_autumnale` | *Helenium autumnale* | unranked | sc={echinaat,fenestraat} · features=1
- `hieracium_austriacum` | *Hieracium austriacum* | unranked | sc={fenestraat} · features=1
- `hypericum_polyphyllum` | *Hypericum polyphyllum* | unranked | sc={psilaat} · features=1
- `kalmia_angustifolia` | *Kalmia angustifolia* | unranked | class=medium | mid=29.5µm · features=1
- `lactuca_tatarica` | *Lactuca tatarica* | unranked | ap=fenestr* · features=1
- `lappula_deflexa` | *Lappula deflexa* | unranked | ap=heterocol* · features=1
- `lonicera_fragrantissima` | *Lonicera Fragrantissima* | unranked | sc={echinaat,tricolporaat} · features=1
- `lonicera_japonica` | *Lonicera Japonica* | unranked | sc={echinaat,tricolporaat} · features=1
- `lychnis_coronaria` | *Lychnis coronaria* | unranked | ap=peripor* · features=1
- `lythrum_virgatum` | *Lythrum virgatum* | unranked | ap=heterocol* · features=1
- `mentha_arvensis` | *Mentha arvensis* | unranked | ap=stephanocol* · features=1
- `mentha_longifolia` | *Mentha longifolia* | unranked | ap=stephanocol* · features=1
- `minuartia_biflora` | *Minuartia biflora* | unranked | ap=peripor* · features=1
- `persicaria_hydropiper` | *Persicaria hydropiper* | unranked | ap=peripor* · features=1
- `persicaria_lapathifolia` | *Persicaria lapathifolia* | unranked | ap=peripor* · features=1
- `platanus_hispanica` | *Platanus hispanica* | unranked | sc={reticulaat} · features=1
- `polygonatum_multiflorum` | *Polygonatum multiflorum* | unranked | ap=monocol* · features=1
- `polygonum_persicaria` | *Polygonum persicaria* | rank=41 | ap=peripor* · features=1
- `primula_elatior` | *Primula elatior* | unranked | ap=stephanocol* · features=1
- `prunella_grandiflora` | *Prunella grandiflora* | unranked | ap=stephanocol* · features=1
- `pseudofumaria_alba_corydalis_alba` | *Pseudofumaria alba* | unranked | ap=pericol* · features=1
- `pseudofumaria_lutea_corydalis_lutea` | *Pseudofumaria lutea* | unranked | ap=syncol* · features=1
- `rosa_rubiginosa` | *Rosa rubiginosa* | unranked | class=medium | mid=28.0µm | sculpt_MASKED · features=1
- `sagina_nodosa` | *Sagina nodosa* | unranked | ap=peripor* · features=1
- `sagina_subulata` | *Sagina subulata* | unranked | ap=peripor* · features=1
- `senecio_cineraria` | *Senecio Cineraria* | unranked | sc={echinaat,tricolporaat} · features=1
- `sonchus_asper` | *Sonchus asper* | unranked | ap=fenestr* · features=1
- `stellaria_media` | *Stellaria media* | unranked | ap=peripor* · features=1

## Appendix B. Clusterable singletons at tight cut

Clusterable taxa not in any tight multi-member cluster: **147** (not listed exhaustively).
Of which learning-priority: **19**
- `brassica_typ` | *Brassica typ* | rank=1 | class=medium | mid=25.2µm | sc={reticulaat,rond,tricolpaat}
- `prunus_pirus_typ` | *Prunus pirus* | rank=2 | sc={driehoekig,striaat,tricolporaat}
- `taraxacum_typ` | *Taraxacum typ* | rank=4 | sc={echinaat,fenestraat,rond,tricolpaat}
- `rhamnus` | *Rhamnus* | rank=7 | sc={driehoekig,reticulaat,tricolporaat}
- `aesculus` | *Aesculus* | rank=8 | sc={psilaat,rond,tricolporaat}
- `robinia` | *Robinia* | rank=9 | sc={driehoekig,scabraat,tricolpaat}
- `vicia_typ` | *Vicia typ* | rank=10 | sc={prolaat,reticulaat,tricolporaat}
- `anthriscus_typ` | *Anthriscus typ* | rank=12 | sc={prolaat,tricolporaat,verrucaat}
- `echium` | *Echium* | rank=14 | sc={prolaat,reticulaat,tricolporaat}
- `parthenocissus` | *Parthenocissus* | rank=17 | sc={reticulaat,rond,tricolporaat}
- `raphanus_typ` | *Raphanus typ* | rank=18 | sc={reticulaat,rond,tricolporaat}
- `verbascum` | *Verbascum* | rank=19 | sc={reticulaat,rond,tricolporaat}
- `lotus` | *Lotus* | rank=20 | sc={prolaat,psilaat,tricolporaat}
- `myosotis_typ` | *Myosotis typ* | rank=22 | ap=6 | class=very-small | mid=7.0µm | sc={psilaat}
- `phacelia_typ` | *Phacelia typ* | rank=23 | ap=6 | class=small | mid=22.0µm | sc={psilaat}
- `spiraea_typ` | *Spiraea typ* | rank=31 | class=small | mid=14.0µm | sc={psilaat}
- `populus_typ` | *Populus typ* | rank=35 | class=medium | mid=27.0µm | sc={reticulaat,scabraat}
- `impatiens_glandulifera` | *Impatiens glandulifera* | rank=52 | ap=4colpaat | class=medium | mid=35.5µm | sc={reticulaat}
- `cynoglossum_typ` | *Cynoglossum typ* | rank=66 | ap=n | class=very-small | mid=11.0µm | sc={psilaat}

