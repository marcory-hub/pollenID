# Morph lookalike clustering (one-shot)

Generated read-only from `data/pollen.yaml`, `docs/keys/**`,
`temp/reports/key-path-conflicts.md`, and `data/lookalike_review.yaml`.

## 1. Method summary

- **Goal:** taxa whose pollen are hard to tell apart under LM (morph similarity), not key-topology lookalikes.
- **Matching:** exact `pollen_key` only; no synonym merge; no `*_typ` representative fill.
- **Features:** YAML size / aperture / sculpture / shape / ornamentation / `pollen_class_beug` / controlled.*; key endpoint + path morph tokens; Kerkvliet sections marked analytic.
- **Conflict mask:** size and/or sculpture dimensions masked for taxa in the key-path conflict table.
- **Clustering:** pure-Python agglomerative complete-linkage cut; Complete-linkage cut on pairwise morph distance (merge only if every cross-pair ≤ threshold; avoids single-link chaining).
- **Non-goals:** no promotion to lookalikes; no edits outside this report.

## 2. Feature inventory

| Metric | Count |
| :--- | ---: |
| Taxa in `pollen.yaml` | 1698 |
| Taxa with ≥1 usable morph feature | 961 |
| Clusterable (≥2 feature dims) | 907 |
| Sparse / appendix (<2 dims) | 54 |
| Conflict-masked taxa | 34 |
| Key-enriched taxa (any key hit) | 519 |
| Learning-priority ranked in clusterable | 40 |
| Already-decided pairs (confirmed/different) | 95 |

### Aperture families (clusterable)

- `tricol*`: 626
- `stephanocol*`: 59
- `peripor*`: 58
- `monocol*`: 44
- `fenestr*`: 25
- `tripor*`: 23
- `syncol*`: 13
- `stephanopor*`: 12
- `inapert*`: 9
- `porate*`: 7
- `heterocol*`: 5
- `monopor*`: 5
- `stephanocolpor*`: 5
- `tetrade*`: 5
- `pericol*`: 4
- `colpate*`: 3
- `dipor*`: 2
- `vesicul*`: 2

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
| Linkage | Complete-linkage cut on pairwise morph distance (merge only if every cross-pair ≤ threshold; avoids single-link chaining) |
| W_APERTURE (mismatch) | 3.0 |
| W_SIZE_CLASS (mismatch) | 2.0 |
| W_SIZE_CLASS_ADJ (adjacent) | 0.8 |
| W_SIZE_MID (per 5 µm) | 1.2 |
| W_SCULPT (× Jaccard dist) | 1.5 |
| W_COARSE_SCULPT (single coarse token) | 0.55 |
| W_BEUG (class family mismatch) | 0.7 |
| W_SHAPE / W_ORN | 0.8 / 0.5 |
| Missing aperture / size | 1.6 / 1.2 |
| Missing-dim inflate | 0.55 |
| Size classes | Kerkvliet bins from max µm (`kerkvliet-determinatietabel.js`) |
| **Tight cut** | distance ≤ **1.000** |
| **Loose cut** | distance ≤ **1.750** |

### Calibration notes

- Calibration pairs with distance: confirmed n=24, different n=53
- Confirmed distance: min=1.120 median=2.277 max=6.255
- Different distance: min=0.725 median=2.561 max=6.597
- Confirmed vs different distances overlap; using guidance defaults tight=1.000, loose=1.750 (not median split).
- Fraction confirmed pairs ≤ tight: 0.00; ≤ loose: 0.25
- Fraction different pairs ≤ tight: 0.04; ≤ loose: 0.13

### Sample decided-pair distances

| Pair | Status | Distance |
| :--- | :--- | ---: |
| `acer_platanoides`–`centaurea_cyanus` | review:different | 2.780 |
| `acer_platanoides`–`malus_typ` | review:different | 2.119 |
| `acer_platanoides`–`prunus_pirus_typ` | review:different | 1.619 |
| `acer_platanoides`–`ranunculus_typ` | review:different | 2.561 |
| `acer_platanoides`–`robinia_pseudoacacia` | review:different | 2.955 |
| `acer_platanoides`–`taraxacum_typ` | review:different | 2.369 |
| `acer_platanoides`–`tilia_typ` | review:different | 2.681 |
| `aesculus_hippocastanum`–`melilotus_officinalis` | review:confirmed | 1.930 |
| `aesculus_hippocastanum`–`trifolium_repens` | review:confirmed | 1.520 |
| `ailanthus_altissima`–`taraxacum_typ` | review:different | 3.985 |
| `ailanthus_altissima`–`tilia_typ` | review:different | 4.085 |
| `amorpha_fruticosa`–`taraxacum_typ` | review:different | 5.821 |
| `anthriscus_typ`–`taraxacum_typ` | review:different | 6.225 |
| `anthriscus_typ`–`vicia_typ` | review:confirmed | 5.425 |
| `brassica_typ`–`fraxinus_ornus` | review:confirmed | 6.255 |
| `brassica_typ`–`ligustrum_vulgare` | review:confirmed | 2.351 |
| `brassica_typ`–`raphanus_typ` | review:confirmed | 2.185 |
| `brassica_typ`–`salix_typ` | review:confirmed | 2.545 |
| `brassica_typ`–`taraxacum_typ` | review:different | 3.365 |
| `brassica_typ`–`tilia_typ` | review:different | 2.465 |
| `calluna_vulgaris`–`centaurea_cyanus` | review:different | 2.524 |
| `calluna_vulgaris`–`ranunculus_typ` | review:different | 2.365 |
| `calluna_vulgaris`–`taraxacum_typ` | review:different | 2.770 |
| `calluna_vulgaris`–`tilia_typ` | review:different | 2.545 |
| `centaurea_cyanus`–`crataegus_typ` | review:different | 1.656 |

## 4. Tight clusters (near-identical)

Clusters with ≥2 members at tight≤1.000 cut. Learning-priority clusters listed first.

- With ≥1 learning_priority_rank: **23**
- Unranked-only: **131**
- Total: **154**

### C1 (n=6, mean_d=0.366, max_d=0.765) — ranks [1]

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.0, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_typ` | *Brassica typ* | rank=1 | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `euodia_hupehensis` | *Euodia hupehensis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
- Closest pair evidence `pyracantha_coccin`–`pyracantha_coccinea` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `brassica_typ`: data/pollen.yaml:size; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm · `euodia_hupehensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fallopia_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `parnassia_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C2 (n=3, mean_d=0.567, max_d=0.663) — ranks [2]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.3, 32.5)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_pirus_typ` | *Prunus pirus* | rank=2 | ap=tricol* | class=medium | mid=32.5µm | sc={striaat}
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={striaat}
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | sc={striaat}
- Closest pair evidence `potentilla_norvegica`–`rosa_glauca` (d=0.435): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.435}`
- Provenance (sample): `potentilla_norvegica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_pirus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `rosa_glauca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C3 (n=5, mean_d=0.575, max_d=0.898) — ranks [4]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.0, 33.5)
- Shared sculpture tokens: echinaat
- Members:
  - `taraxacum_typ` | *Taraxacum typ* | rank=4 | ap=tricol* | class=medium | mid=32.5µm | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | sc={echinaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={echinaat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
- Closest pair evidence `taraxacum_typ`–`tussilago_farfara` (d=0.245): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `inula_ensifolia`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `senecio_aquaticus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphyotrichum_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taraxacum_typ`: data/pollen.yaml:sculpture; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm

### C4 (n=3, mean_d=0.774, max_d=0.949) — ranks [5]

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.9, 38.1)
- Shared sculpture tokens: —
- Members:
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=38.1µm | sculpt_MASKED
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm
  - `tilia_americana` | *Tilia americana* | unranked | ap=tricol* | class=medium | mid=37.9µm | sc={reticulaat}
- Closest pair evidence `centaurea_cyanus`–`empetrum_nigrum` (d=0.674): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.674}`
- Provenance (sample): `centaurea_cyanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `empetrum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `tilia_americana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C5 (n=2, mean_d=0.845, max_d=0.845) — ranks [6, 45]

- Shared aperture: tricol*
- Size classes: —; mid range: None
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | size_MASKED | sc={reticulaat}
  - `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | size_MASKED | sc={reticulaat}
- Closest pair evidence `trifolium_pratense`–`trifolium_repens` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `trifolium_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C6 (n=2, mean_d=0.675, max_d=0.675) — ranks [8]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.0)
- Shared sculpture tokens: —
- Members:
  - `aesculus` | *Aesculus* | rank=8 | ap=tricol* | class=small | mid=20.0µm | sc={psilaat}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm
- Closest pair evidence `aesculus`–`solanum_lycopers` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `aesculus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `solanum_lycopers`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C7 (n=2, mean_d=0.937, max_d=0.937) — ranks [10]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 32.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `vicia_typ` | *Vicia typ* | rank=10 | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
- Closest pair evidence `euphorbia_cyparissias`–`vicia_typ` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `euphorbia_cyparissias`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband

### C8 (n=2, mean_d=0.745, max_d=0.745) — ranks [11]

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.1, 34.8)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | sc={rugulaat,striaat}
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | sc={rugulaat,striaat}
- Closest pair evidence `acer_campestre`–`acer_platanoides` (d=0.745): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.25, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.745}`
- Provenance (sample): `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_platanoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C9 (n=2, mean_d=0.855, max_d=0.855) — ranks [12]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 22.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `anthriscus_typ` | *Anthriscus typ* | rank=12 | ap=tricol* | class=small | mid=20.0µm | sc={verrucaat}
  - `eucalyptus_camaldulensis` | *Eucalyptus camaldulensis* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={verrucaat}
- Closest pair evidence `anthriscus_typ`–`eucalyptus_camaldulensis` (d=0.855): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.855}`
- Provenance (sample): `anthriscus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `eucalyptus_camaldulensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C10 (n=7, mean_d=0.456, max_d=0.885) — ranks [13]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 19.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
- Closest pair evidence `deutzia_typ`–`linaria_cymbalaria` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `alyssum_saxatile`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `deutzia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fallopia_baldschur`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `linaria_cymbalaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C11 (n=2, mean_d=0.425, max_d=0.425) — ranks [15]

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 36.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={reticulaat}
- Closest pair evidence `stachys_palustris`–`tilia_typ` (d=0.425): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.425}`
- Provenance (sample): `stachys_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tilia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C12 (n=2, mean_d=0.845, max_d=0.845) — ranks [16]

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.5, 34.5)
- Shared sculpture tokens: reticulaat, verrucaat
- Members:
  - `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat,verrucaat}
  - `linum_usitatissimum` | *Linum usitatissimum* | unranked | ap=tricol* | size_MASKED | sc={reticulaat,verrucaat}
- Closest pair evidence `linum_usitatissimum`–`ranunculus_typ` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.845}`
- Provenance (sample): `linum_usitatissimum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C13 (n=5, mean_d=0.528, max_d=0.833) — ranks [17]

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 33.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `parthenocissus` | *Parthenocissus* | rank=17 | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={reticulaat}
- Closest pair evidence `aralia_elata`–`ricinus_communis` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aralia_elata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `parthenocissus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `ricinus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ulex_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C14 (n=4, mean_d=0.543, max_d=0.961) — ranks [18, 19]

- Shared aperture: tricol*
- Size classes: small; mid range: (19.9, 20.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `raphanus_typ` | *Raphanus typ* | rank=18 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `verbascum` | *Verbascum* | rank=19 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | sc={reticulaat}
- Closest pair evidence `diplotaxis_tenuifolia`–`raphanus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `diplotaxis_tenuifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `salix_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `verbascum`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband

### C15 (n=2, mean_d=0.495, max_d=0.495) — ranks [21]

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.5, 29.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | sc={psilaat,scabraat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={psilaat,scabraat}
- Closest pair evidence `lamium_typ`–`photinia_typ` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `lamium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `photinia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C16 (n=3, mean_d=0.661, max_d=0.929) — ranks [29]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.4, 21.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
- Closest pair evidence `ononis`–`ononis_natrix` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `melilotus_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis_natrix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C17 (n=15, mean_d=0.612, max_d=0.965) — ranks [33]

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.9, 36.2)
- Shared sculpture tokens: echinaat
- Members:
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat}
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={echinaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={echinaat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | sc={echinaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | sc={echinaat}
- Closest pair evidence `helianthus_annuus`–`tagetes_erecta` (d=0.365): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.365}`
- Provenance (sample): `aster_sedifolius`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `calendula_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chrysanthemum_segetum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cosmos_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C18 (n=2, mean_d=0.845, max_d=0.845) — ranks [34]

- Shared aperture: tricol*
- Size classes: —; mid range: None
- Shared sculpture tokens: psilaat, reticulaat, scabraat, verrucaat
- Members:
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `centaurea_montana`–`cornus_sanguinea` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `centaurea_montana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_sanguinea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C19 (n=4, mean_d=0.577, max_d=0.831) — ranks [44]

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.1, 41.0)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | sc={striaat}
  - `acer_monspessulanum` | *Acer monspessulanum* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={striaat}
- Closest pair evidence `crataegus_typ`–`prunus_spinoza` (d=0.365): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.365}`
- Provenance (sample): `acer_monspessulanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `acer_opalus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crataegus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinoza`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C20 (n=2, mean_d=0.961, max_d=0.961) — ranks [52]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.5, 35.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `impatiens_glandulifera` | *Impatiens glandulifera* | rank=52 | ap=stephanocol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat}
- Closest pair evidence `impatiens_glandulifera`–`thymus_serpyllum` (d=0.961): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.961}`
- Provenance (sample): `impatiens_glandulifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_serpyllum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C21 (n=3, mean_d=0.868, max_d=0.995) — ranks [53]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 18.5)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat,scabraat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,scabraat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat,scabraat,striaat}
- Closest pair evidence `daucus_carota`–`filipendula_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `daucus_carota`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `limnanthes_douglasii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C22 (n=3, mean_d=0.727, max_d=0.890) — ranks [71]

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=small | mid=25.0µm | sc={psilaat,reticulaat,scabraat}
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=small | mid=24.0µm | sculpt_MASKED
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | sculpt_MASKED
- Closest pair evidence `aesculus_hippocastanum`–`cornus_mas` (d=0.640): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': 'masked_conflict', 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.64}`
- Provenance (sample): `aesculus_hippocastanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_mas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_idaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C23 (n=2, mean_d=0.949, max_d=0.949) — ranks [76]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.9, 39.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | sc={reticulaat}
  - `oxalis_typ` | *Oxalis typ* | unranked | ap=stephanocol* | class=medium | mid=39.0µm | sc={reticulaat}
- Closest pair evidence `impatiens_parviflora`–`oxalis_typ` (d=0.949): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `impatiens_parviflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `oxalis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C24 (n=13, mean_d=0.556, max_d=0.975)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 28.5)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** senecio_jacobaea ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_jacobea ↔ senecio_typ
- Members:
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat}
- Closest pair evidence `aster_typ`–`matricaria_chamo` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aster_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotis_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotus_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `galinsoga_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C25 (n=9, mean_d=0.584, max_d=0.898)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.3, 32.2)
- Shared sculpture tokens: echinaat
- Members:
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={echinaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={echinaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={echinaat}
- Closest pair evidence `achillea_millefolium`–`anthemis_tinctoria` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `achillea_millefolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `anthemis_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `aster_alpinus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `bidens_ferulifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C26 (n=9, mean_d=0.586, max_d=0.927)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.1, 29.4)
- Shared sculpture tokens: striaat
- Members:
  - `comarum_palustre` | *Comarum palustre* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={striaat}
- Closest pair evidence `comarum_palustre`–`potentilla_recta` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `comarum_palustre`: data/pollen.yaml:shape; docs/keys/**:outcome_size; eide:docs/keys/eide/rosaceae-eide.json; feagri-iversen:docs/keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json · `lycium_barbarum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C27 (n=6, mean_d=0.544, max_d=0.855)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `sylibum_marianum` | *Sylibum marianum* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={echinaat}
- Closest pair evidence `cirsium_arvense`–`serrulata_tinctoria` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `cirsium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cnicus_benedict`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordon_acant`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordum_acanthium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C28 (n=6, mean_d=0.547, max_d=0.723)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.6, 24.1)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=23.7µm | sc={striaat}
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={striaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={striaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={striaat}
  - `sedum_sexangulare` | *Sedum sexangulare* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | sc={striaat}
- Closest pair evidence `fragaria_moschata`–`geum_rivale` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `fragaria_moschata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `geum_rivale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geum_urbanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_aurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C29 (n=5, mean_d=0.673, max_d=0.963)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 25.2)
- Shared sculpture tokens: echinaat
- Members:
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={echinaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={echinaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={echinaat}
- Closest pair evidence `bellis_perennis`–`galinsoga_parviflora` (d=0.411): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `bellis_perennis`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `erigeron_acer`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galinsoga_parviflora`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `matricaria_recutita`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C30 (n=5, mean_d=0.473, max_d=0.995)

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 24.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `clethra_alnifolia` | *Clethra alnifolia* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat,verrucaat}
  - `digitalis_purpurea` | *Digitalis purpurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | sc={reticulaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
- Closest pair evidence `digitalis_purpurea`–`polygonum_convol` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clethra_alnifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `digitalis_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polygonum_convol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhus_chinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C31 (n=5, mean_d=0.415, max_d=0.825)

- Shared aperture: tricol*
- Size classes: small; mid range: (23.0, 23.0)
- Shared sculpture tokens: —
- Members:
  - `genista_anglica` | *Genista anglica* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
- Closest pair evidence `genista_anglica`–`lysimachia_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `genista_anglica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_polyph`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lysimachia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_raph`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C32 (n=5, mean_d=0.555, max_d=0.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.8, 26.3)
- Shared sculpture tokens: striaat
- Members:
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | sc={striaat}
  - `potentilla_crantzii` | *Potentilla crantzii* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={striaat}
- Closest pair evidence `potentilla_crantzii`–`potentilla_erecta` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `hippocrepis_comosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_crantzii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_erecta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `potentilla_grandiflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C33 (n=4, mean_d=0.565, max_d=0.845)

- Shared aperture: tricol*
- Size classes: small; mid range: (20.5, 21.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
- Closest pair evidence `amorpha_fructico`–`mercurialis_annua` (d=0.245): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `amorpha_fructico`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mercurialis_annua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `verbascum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `viburnum_opulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C34 (n=4, mean_d=0.685, max_d=0.845)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.5, 45.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat}
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | size_MASKED | sc={echinaat}
  - `viscum_album` | *Viscum album* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={echinaat}
  - `weigelia_diervilla_typ` | *Weigelia/Diervilla typ* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={echinaat}
- Closest pair evidence `arcticum_minus`–`viscum_album` (d=0.245): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `arcticum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arctium_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `viscum_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `weigelia_diervilla_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C35 (n=4, mean_d=0.593, max_d=0.855)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.0, 24.0)
- Shared sculpture tokens: echinaat
- Members:
  - `artemisia_typ` | *Artemisia typ* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={echinaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={echinaat}
  - `solidago_virgaurea` | *Solidago virgaurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={echinaat}
- Closest pair evidence `bidens_typ`–`helenium_autumn` (d=0.245): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `artemisia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bidens_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `helenium_autumn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solidago_virgaurea`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C36 (n=4, mean_d=0.650, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.1, 25.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** crambe_maritima ↔ crambe_typ
- Members:
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | sc={reticulaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
- Closest pair evidence `crambe_maritima`–`crambe_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `brassica_napus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bunias_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crambe_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `crambe_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C37 (n=4, mean_d=0.957, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 25.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={reticulaat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
- Closest pair evidence `brassica_oleracea`–`hesperis_matronalis` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `brassica_oleracea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hesperis_matronalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_cinerea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_pentandra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C38 (n=4, mean_d=0.450, max_d=0.993)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 28.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cakile_maritima` | *Cakile maritima* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat}
- Closest pair evidence `corylopsis_parcifl`–`scrophularia_nodosa` (d=0.197): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.197}`
- Provenance (sample): `cakile_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_parcifl`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scrophularia_nodosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ulex_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C39 (n=4, mean_d=0.419, max_d=0.507)

- Shared aperture: tricol*
- Size classes: medium; mid range: (43.5, 44.0)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** carduus_defloratus ↔ carduus_typ
- Members:
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
- Closest pair evidence `carduus_defloratus`–`carduus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_defloratus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carduus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_helenium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `tragopogon_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C40 (n=4, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: echinaat
- Members:
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
- Closest pair evidence `chrysanthemum_leuc`–`eupatorium_cann` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `chrysanthemum_leuc`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cann`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cannabinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `petasitis_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C41 (n=4, mean_d=0.495, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 29.0)
- Shared sculpture tokens: echinaat
- Members:
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `taraxacum_officinale` | *Taraxacum officinale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
- Closest pair evidence `crepis_typ`–`hieracium_aurantiacum` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `crepis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hieracium_aurantiacum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `leontodon_autum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taraxacum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C42 (n=3, mean_d=0.535, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 30.0)
- Shared sculpture tokens: striaat
- Members:
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `acer_tataricum_subsp_ginnala` | *Acer tataricum* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={striaat}
  - `sorbus_arranensis` | *Sorbus arranensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
- Closest pair evidence `acer_japonicum`–`sorbus_arranensis` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_tataricum_subsp_ginnala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sorbus_arranensis`: docs/keys/**:outcome_size; eide:docs/keys/eide/rosaceae-eide.json

### C43 (n=3, mean_d=0.825, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.0)
- Shared sculpture tokens: —
- Members:
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,rugulaat,striaat}
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,striaat}
- Closest pair evidence `acer_negundo`–`sarothamnus_sco` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `acer_negundo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sarothamnus_sco`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C44 (n=3, mean_d=0.748, max_d=0.935)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.9, 43.1)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={microreticulaat,psilaat,reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=42.9µm | sc={microreticulaat,psilaat,reticulaat}
  - `nigella_sativa` | *Nigella sativa* | unranked | ap=tricol* | class=medium | mid=43.1µm | sc={psilaat,reticulaat}
- Closest pair evidence `adonis_aestivalis`–`helleborus_niger` (d=0.411): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `adonis_aestivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_niger`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `nigella_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C45 (n=3, mean_d=0.607, max_d=0.710)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.2, 33.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | sculpt_MASKED
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | sculpt_MASKED
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={reticulaat}
- Closest pair evidence `agrimonia_eupatoria`–`rosa_canina` (d=0.424): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'masked_conflict', 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.424}`
- Provenance (sample): `agrimonia_eupatoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rosa_canina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_fragiferum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C46 (n=3, mean_d=0.965, max_d=0.985)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.8, 24.0)
- Shared sculpture tokens: —
- Members:
  - `amaranthus_caudatus` | *Amaranthus caudatus* | unranked | ap=peripor* | class=medium | mid=24.0µm | sc={scabraat}
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm
- Closest pair evidence `amaranthus_caudatus`–`ribes_alpinum` (d=0.949): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `amaranthus_caudatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C47 (n=3, mean_d=0.973, max_d=0.997)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 28.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={reticulaat}
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | sc={reticulaat}
- Closest pair evidence `anacardium_occidentale`–`cardamine_flexuosa` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.961}`
- Provenance (sample): `anacardium_occidentale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cardamine_flexuosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_dasyclados`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C48 (n=3, mean_d=0.598, max_d=0.685)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 29.5)
- Shared sculpture tokens: echinaat
- Members:
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={echinaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
- Closest pair evidence `aster_amellus`–`rudbeckia_hirta` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `anthemis_nobilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aster_amellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rudbeckia_hirta`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C49 (n=3, mean_d=0.941, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.9, 29.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
- Closest pair evidence `ballota_nigra_ssp_foetida`–`lupinus_typ` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `ballota_nigra_ssp_foetida`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ligustrum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lupinus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C50 (n=3, mean_d=0.941, max_d=0.949)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (35.1, 35.2)
- Shared sculpture tokens: —
- Members:
  - `campanula_trachelium` | *Campanula trachelium* | unranked | ap=stephanopor* | class=medium | mid=35.2µm | sc={echinaat,microechinaat}
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.925): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `campanula_trachelium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-trachelium.json · `phyteuma_spicatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `phyteuma_spicatum_ssp_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C51 (n=3, mean_d=0.372, max_d=0.495)

- Shared aperture: tricol*
- Size classes: large; mid range: (47.2, 47.8)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** serratula_tinctoria ↔ serratula_typ
- Members:
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
- Closest pair evidence `serratula_tinctoria`–`serratula_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_crispus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `serratula_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serratula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C52 (n=3, mean_d=0.285, max_d=0.365)

- Shared aperture: tricol*
- Size classes: large; mid range: (60.0, 61.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carthamus_tinctorius` | *Carthamus tinctorius* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={echinaat}
- Closest pair evidence `carlina_acaulis`–`carlina_aucalis` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carlina_acaulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carlina_aucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carthamus_tinctorius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C53 (n=3, mean_d=0.949, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.0, 34.1)
- Shared sculpture tokens: —
- Members:
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={reticulaat}
  - `vaccinium_vitis` | *Vaccinium vitis* | unranked | ap=tricol* | class=medium | mid=34.0µm
- Closest pair evidence `lupinus_angustifolius`–`vaccinium_vitis` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `colutea_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lupinus_angustifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_vitis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C54 (n=3, mean_d=0.615, max_d=0.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 32.5)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat,scabraat}
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat,scabraat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `cytisus_typ`–`pimpinella_anisum` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `cytisus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eryngium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_anisum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C55 (n=3, mean_d=0.599, max_d=0.711)

- Shared aperture: tricol*
- Size classes: large; mid range: (73.4, 74.8)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | sc={echinaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=73.8µm | sc={echinaat}
- Closest pair evidence `lonicera_caprifolium`–`scabiosa_columbaria` (d=0.483): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.483}`
- Provenance (sample): `dipsacus_pilosus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_caprifolium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `scabiosa_columbaria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-dipsacaceae.json

### C56 (n=3, mean_d=0.471, max_d=0.519)

- Shared aperture: tricol*
- Size classes: large; mid range: (70.0, 70.6)
- Shared sculpture tokens: echinaat
- Members:
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | sc={echinaat}
  - `scabiosa_columbar` | *Scabiosa columbar* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
- Closest pair evidence `echinops_sphaer`–`scabiosa_columbar` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `echinops_sphaer`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_alpigena`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scabiosa_columbar`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C57 (n=3, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
- Closest pair evidence `euonymus_europaeus`–`mangifera_indica` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `euonymus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mangifera_indica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melilotus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C58 (n=3, mean_d=0.647, max_d=0.783)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.3, 21.0)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={striaat}
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | sc={striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | sc={striaat}
- Closest pair evidence `fragaria_vesca`–`sedum_album` (d=0.531): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.531}`
- Provenance (sample): `fragaria_vesca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `potentilla_fruticosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sedum_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C59 (n=3, mean_d=0.782, max_d=0.985)

- Shared aperture: monocol*
- Size classes: large; mid range: (56.8, 57.0)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=monocol* | class=large | mid=57.0µm | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=monocol* | class=large | mid=57.0µm | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C60 (n=3, mean_d=0.957, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.8, 37.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | sc={reticulaat}
- Closest pair evidence `galeopsis_tetrahit`–`parthenocissus_typ` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `galeopsis_tetrahit`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `parthenocissus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tilia_tomentosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C61 (n=3, mean_d=0.941, max_d=0.949)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.0, 35.0)
- Shared sculpture tokens: —
- Members:
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
- Closest pair evidence `impatiens_balsamina`–`mentha_aquatica` (d=0.937): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `mentha_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C62 (n=3, mean_d=0.738, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.5, 28.0)
- Shared sculpture tokens: —
- Members:
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={reticulaat}
  - `rosa_rubiginosa` | *Rosa rubiginosa* | unranked | ap=tricol* | class=medium | mid=28.0µm | sculpt_MASKED
- Closest pair evidence `lysimachia_vulgaris`–`rosa_rubiginosa` (d=0.520): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.52}`
- Provenance (sample): `lysimachia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ononis_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_rubiginosa`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; reitsma:docs/keys/reitsma/rosaceae-reitsma.json

### C63 (n=3, mean_d=0.965, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 29.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
- Closest pair evidence `ononis_repens_ssp_repens`–`viburnum_lantana` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `ononis_repens_ssp_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scrophularia_auriculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viburnum_lantana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C64 (n=3, mean_d=0.439, max_d=0.471)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.0, 33.4)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `rosa_pimpinellifolia` | *Rosa pimpinellifolia* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | sc={striaat}
- Closest pair evidence `prunus_mahaleb`–`rosa_pimpinellifolia` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.387}`
- Provenance (sample): `prunus_mahaleb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_pimpinellifolia`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json · `rosa_spinosissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C65 (n=3, mean_d=0.957, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.4, 23.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={reticulaat}
- Closest pair evidence `salix_alba_var_tristis`–`salix_fragilis` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `salix_alba_var_tristis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_fragilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C66 (n=3, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 47.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
- Closest pair evidence `trifolium_incarnat`–`trifolium_incarnatum` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `trifolium_incarnat`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_incarnatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vicia_faba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C67 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same peripor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C68 (n=2, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: striaat
- Members:
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
- Closest pair evidence `acer_palmatum`–`aesculus_hippoca` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_palmatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aesculus_hippoca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C69 (n=2, mean_d=0.615, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 36.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `aconitum_typ` | *Aconitum typ* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,scabraat}
  - `ficaria_typ` | *Ficaria typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `aconitum_typ`–`ficaria_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `aconitum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ficaria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C70 (n=2, mean_d=0.920, max_d=0.920)

- Shared aperture: tricol*
- Size classes: large; mid range: (75.0, 75.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | sculpt_MASKED
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | sc={reticulaat}
- Closest pair evidence `agrimonia_odorata`–`geranium_typ` (d=0.920): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.92}`
- Provenance (sample): `agrimonia_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `geranium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C71 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: monocol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `allium_cepa` | *Allium cepa* | unranked | ap=monocol* | class=medium | mid=28.0µm | sc={psilaat,scabraat}
  - `allium_schoenoprasum` | *Allium schoenoprasum* | unranked | ap=monocol* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
- Closest pair evidence `allium_cepa`–`allium_schoenoprasum` (d=0.605): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `allium_cepa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `allium_schoenoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C72 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: monocol*
- Size classes: medium; mid range: (43.9, 44.0)
- Shared sculpture tokens: —
- Members:
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.949): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tradescantia_andersoniana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C73 (n=2, mean_d=0.845, max_d=0.845)

- Shared aperture: monocol*
- Size classes: medium; mid range: (42.2, 42.2)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat, rugulaat, scabraat
- Members:
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | size_MASKED | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `convallaria_majalis` | *Convallaria majalis* | unranked | ap=monocol* | class=medium | mid=42.2µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `allium_ursinum`–`convallaria_majalis` (d=0.845): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `convallaria_majalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json

### C74 (n=2, mean_d=0.845, max_d=0.845)

- Shared aperture: peripor*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `alnus_glutinosa` | *Alnus glutinosa* | unranked | ap=peripor* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `carpinus_betulus` | *Carpinus betulus* | unranked | ap=peripor* | size_MASKED | sc={psilaat,scabraat}
- Closest pair evidence `alnus_glutinosa`–`carpinus_betulus` (d=0.845): `{'aperture': 'same peripor*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same stephanopor', 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `alnus_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpinus_betulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C75 (n=2, mean_d=0.833, max_d=0.833)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.5, 26.5)
- Shared sculpture tokens: microreticulaat, reticulaat
- Members:
  - `alyssum_montanum` | *Alyssum montanum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,reticulaat}
  - `fraxinus_excelsior` | *Fraxinus excelsior* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={microreticulaat,reticulaat}
- Closest pair evidence `alyssum_montanum`–`fraxinus_excelsior` (d=0.833): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.6, 'shared': ['prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.833}`
- Provenance (sample): `alyssum_montanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fraxinus_excelsior`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C76 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 32.4)
- Shared sculpture tokens: reticulaat, verrucaat
- Members:
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,verrucaat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,verrucaat}
- Closest pair evidence `angelica_sylvestris`–`foeniculum_vulgare` (d=0.711): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `angelica_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C77 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 17.0)
- Shared sculpture tokens: —
- Members:
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={microreticulaat,reticulaat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm
- Closest pair evidence `antirrhinum_majus`–`astragalus_sinicus` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `antirrhinum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `astragalus_sinicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C78 (n=2, mean_d=0.392, max_d=0.392)

- Shared aperture: tricol*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** arbutus_unedo ↔ arbutus_typ
- Members:
  - `arbutus_typ` | *Arbutus typ* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
  - `arbutus_unedo` | *Arbutus unedo* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
- Closest pair evidence `arbutus_typ`–`arbutus_unedo` (d=0.392): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.333, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.3917}`
- Provenance (sample): `arbutus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arbutus_unedo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C79 (n=2, mean_d=0.495, max_d=0.495)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (39.5, 40.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arctium_lappa` | *Arctium lappa* | unranked | ap=fenestr* | class=medium | mid=40.0µm | sc={echinaat}
  - `vaccinium_corymbosum` | *Vaccinium corymbosum* | unranked | ap=fenestr* | class=medium | mid=39.5µm | sc={echinaat}
- Closest pair evidence `arctium_lappa`–`vaccinium_corymbosum` (d=0.495): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `arctium_lappa`: data/pollen.yaml:sculpture; docs/keys/**:outcome_size; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `vaccinium_corymbosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C80 (n=2, mean_d=0.650, max_d=0.650)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.0, 33.0)
- Shared sculpture tokens: —
- Members:
  - `arctostaphylos_alpina` | *Arctostaphylos alpina* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={scabraat,verrucaat}
  - `cotoneaster_intergerrimus` | *Cotoneaster intergerrimus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sculpt_MASKED
- Closest pair evidence `arctostaphylos_alpina`–`cotoneaster_intergerrimus` (d=0.650): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.65}`
- Provenance (sample): `arctostaphylos_alpina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cotoneaster_intergerrimus`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C81 (n=2, mean_d=0.387, max_d=0.387)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.9, 39.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | sc={echinaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={echinaat}
- Closest pair evidence `arnica_montana`–`senecio_ovatus` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `arnica_montana`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `senecio_ovatus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C82 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.9)
- Shared sculpture tokens: gemmaat, reticulaat, scabraat, verrucaat
- Members:
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `astrantia_major`–`ranunculus_repens` (d=0.711): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['gemmaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `astrantia_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C83 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.0, 41.2)
- Shared sculpture tokens: —
- Members:
  - `berberis_typ` | *Berberis typ* | unranked | ap=stephanocol* | class=medium | mid=41.0µm | sc={psilaat}
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm
- Closest pair evidence `berberis_typ`–`clinopodium_vulgare` (d=0.985): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `berberis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C84 (n=2, mean_d=0.855, max_d=0.855)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (34.0, 36.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `borago_officinalis` | *Borago officinalis* | unranked | ap=stephanocol* | class=medium | mid=34.0µm | sc={reticulaat,scabraat}
  - `veronica_filiformis` | *Veronica filiformis* | unranked | ap=stephanocol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `borago_officinalis`–`veronica_filiformis` (d=0.855): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.855}`
- Provenance (sample): `borago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_filiformis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C85 (n=2, mean_d=0.449, max_d=0.449)

- Shared aperture: peripor*
- Size classes: medium; mid range: (28.6, 30.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=peripor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `daphne_mezereum` | *Daphne mezereum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={reticulaat}
- Closest pair evidence `borreria_verticilata`–`daphne_mezereum` (d=0.449): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.449}`
- Provenance (sample): `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `daphne_mezereum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C86 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.5, 25.7)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_nigra` | *Brassica nigra* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `iberis_amara` | *Iberis amara* | unranked | ap=tricol* | class=medium | mid=25.7µm | sc={reticulaat}
- Closest pair evidence `brassica_nigra`–`iberis_amara` (d=0.973): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.973}`
- Provenance (sample): `brassica_nigra`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `iberis_amara`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C87 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.6, 28.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
- Closest pair evidence `brassica_rapa`–`marrubium_vulgare` (d=0.949): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `brassica_rapa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `marrubium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C88 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.5, 39.5)
- Shared sculpture tokens: —
- Members:
  - `bryonia_dioica` | *Bryonia dioica* | unranked | ap=tricol* | class=medium | mid=39.5µm | sc={reticulaat}
  - `vaccinium_corymb` | *Vaccinium corymb* | unranked | ap=tricol* | class=medium | mid=39.5µm
- Closest pair evidence `bryonia_dioica`–`vaccinium_corymb` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `bryonia_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_corymb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C89 (n=2, mean_d=0.821, max_d=0.821)

- Shared aperture: monocol*
- Size classes: medium; mid range: (31.5, 33.1)
- Shared sculpture tokens: psilaat, reticulaat, rugulaat, scabraat
- Members:
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.1µm | sc={psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `butomus_umbellatus`–`leucojum_aestivum` (d=0.821): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.65, 'sculpture': {'jaccard_dist': 0.2, 'shared': ['psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.821}`
- Provenance (sample): `butomus_umbellatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json · `leucojum_aestivum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json

### C90 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.5, 37.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `oxalis_corniculata` | *Oxalis corniculata* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
- Closest pair evidence `callicarpa_typ`–`oxalis_corniculata` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `callicarpa_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `oxalis_corniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C91 (n=2, mean_d=0.921, max_d=0.921)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 29.5)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat,reticulaat}
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={psilaat,reticulaat}
- Closest pair evidence `caltha_palustris`–`capsicum_annuum` (d=0.921): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'mismatch tricol/tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.921}`
- Provenance (sample): `caltha_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `capsicum_annuum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C92 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 29.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={psilaat}
- Closest pair evidence `caltha_palustris_ssp_araneosa`–`papaver_dubium` (d=0.985): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `caltha_palustris_ssp_araneosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `papaver_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C93 (n=2, mean_d=0.728, max_d=0.728)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.6, 29.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | sc={reticulaat}
- Closest pair evidence `cardamine_pratensis`–`corylopsis_pauciflora` (d=0.728): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.333, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.7277}`
- Provenance (sample): `cardamine_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_pauciflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C94 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.125): `{'aperture': 'same tripor*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'rugulaat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C95 (n=2, mean_d=0.845, max_d=0.845)

- Shared aperture: tricol*
- Size classes: large; mid range: (56.0, 56.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | sc={reticulaat}
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
- Closest pair evidence `citrullus_lanatus`–`reseda_lutea` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.845}`
- Provenance (sample): `citrullus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `reseda_lutea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C96 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `clematis_vitalba`–`melampyrum_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clematis_vitalba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C97 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.8, 23.9)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={reticulaat}
- Closest pair evidence `cochlearia_officinalis_ssp_off`–`salix_daphnoides` (d=0.949): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `cochlearia_officinalis_ssp_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_daphnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C98 (n=2, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.9, 35.9)
- Shared sculpture tokens: striaat
- Members:
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
- Closest pair evidence `cotoneaster_integerrimus`–`prunus_cerasifera` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `cotoneaster_integerrimus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_cerasifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C99 (n=2, mean_d=0.819, max_d=0.819)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.9, 42.7)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | sc={rugulaat,striaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | sc={rugulaat,striaat}
- Closest pair evidence `crataegus_monogyna`–`prunus_spinosa` (d=0.819): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.819}`
- Provenance (sample): `crataegus_monogyna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C100 (n=2, mean_d=0.411, max_d=0.411)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 35.1)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_oxycantha` | *Crataegus oxycantha* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={striaat}
  - `saxifraga_umbrosa` | *Saxifraga umbrosa* | unranked | ap=tricol* | class=medium | mid=35.1µm | sc={striaat}
- Closest pair evidence `crataegus_oxycantha`–`saxifraga_umbrosa` (d=0.411): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.411}`
- Provenance (sample): `crataegus_oxycantha`: docs/keys/**:outcome_size; eide:docs/keys/eide/rosaceae-eide.json · `saxifraga_umbrosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C101 (n=2, mean_d=0.975, max_d=0.975)

- Shared aperture: tricol*
- Size classes: large; mid range: (52.8, 55.2)
- Shared sculpture tokens: echinaat
- Members:
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | sc={echinaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=52.8µm | sc={echinaat}
- Closest pair evidence `cynara_cardunculus`–`lonicera_xylosteum` (d=0.975): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.975}`
- Provenance (sample): `cynara_cardunculus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_xylosteum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-lonicera.json

### C102 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 33.0)
- Shared sculpture tokens: rugulaat
- Members:
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={rugulaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={rugulaat}
- Closest pair evidence `davidia_involucrata`–`rubus_fruticosus` (d=0.985): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat']}, 'shape': {'jaccard_dist': 1.0, 'shared': []}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `davidia_involucrata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_fruticosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C103 (n=2, mean_d=0.495, max_d=0.495)

- Shared aperture: tricol*
- Size classes: large; mid range: (77.0, 77.5)
- Shared sculpture tokens: echinaat
- Members:
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | sc={echinaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | sc={echinaat}
- Closest pair evidence `echinops_sphaerocephalus`–`scabiosa_ochroleuca` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `echinops_sphaerocephalus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `scabiosa_ochroleuca`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C104 (n=2, mean_d=0.365, max_d=0.365)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 18.0)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat,reticulaat}
  - `sambucus_nigra` | *Sambucus nigra* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={psilaat,reticulaat}
- Closest pair evidence `echium_vulgare`–`sambucus_nigra` (d=0.365): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.365}`
- Provenance (sample): `echium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sambucus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C105 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.9, 35.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | sc={reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
- Closest pair evidence `erophila_verna`–`galeopsis_segetum` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `erophila_verna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galeopsis_segetum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C106 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.5, 38.6)
- Shared sculpture tokens: —
- Members:
  - `eschscholtzia_calif` | *Eschscholtzia calif* | unranked | ap=stephanocol* | class=medium | mid=38.5µm | sc={reticulaat,scabraat}
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm
- Closest pair evidence `eschscholtzia_calif`–`melissa_officinalis` (d=0.949): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.949}`
- Provenance (sample): `eschscholtzia_calif`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melissa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C107 (n=2, mean_d=0.975, max_d=0.975)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.5, 43.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | sc={verrucaat}
  - `rhododendron_ponticum` | *Rhododendron ponticum* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={verrucaat}
- Closest pair evidence `euphorbia_typ`–`rhododendron_ponticum` (d=0.975): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `euphorbia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhododendron_ponticum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C108 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: tricol*
- Size classes: small; mid range: (14.0, 16.0)
- Shared sculpture tokens: clavaat, echinaat, microechinaat, psilaat, scabraat
- Members:
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | sc={clavaat,echinaat,microechinaat,psilaat,scabraat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={clavaat,echinaat,microechinaat,psilaat,scabraat}
- Closest pair evidence `filipendula_ulmaria`–`filipendula_vulgaris` (d=0.605): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat', 'echinaat', 'microechinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `filipendula_ulmaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C109 (n=2, mean_d=0.495, max_d=0.495)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 18.0)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_viridis` | *Fragaria viridis* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={striaat}
  - `rubus_arcticus` | *Rubus arcticus* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={striaat}
- Closest pair evidence `fragaria_viridis`–`rubus_arcticus` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `fragaria_viridis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_arcticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C110 (n=2, mean_d=0.485, max_d=0.485)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (17.0, 18.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `galium_sylvatica` | *Galium sylvatica* | unranked | ap=stephanocol* | class=small | mid=17.0µm | sc={reticulaat}
  - `primula_vulgaris` | *Primula vulgaris* | unranked | ap=stephanocol* | class=small | mid=18.5µm | sc={reticulaat}
- Closest pair evidence `galium_sylvatica`–`primula_vulgaris` (d=0.485): `{'aperture': 'same stephanocol*', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.485}`
- Provenance (sample): `galium_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `primula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C111 (n=2, mean_d=0.927, max_d=0.927)

- Shared aperture: tricol*
- Size classes: large; mid range: (58.2, 60.5)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | sc={clavaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | sc={clavaat}
- Closest pair evidence `geranium_molle`–`linum_flavum` (d=0.927): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 2.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.927}`
- Provenance (sample): `geranium_molle`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `linum_flavum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C112 (n=2, mean_d=0.675, max_d=0.675)

- Shared aperture: tricol*
- Size classes: large; mid range: (78.3, 79.6)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | sc={clavaat}
- Closest pair evidence `geranium_nodosum`–`geranium_phaeum` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.675}`
- Provenance (sample): `geranium_nodosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_phaeum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C113 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 33.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat}
- Closest pair evidence `glaucium_flavum`–`sinapis_arvensis` (d=0.985): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `glaucium_flavum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sinapis_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C114 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.6, 41.9)
- Shared sculpture tokens: —
- Members:
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm
- Closest pair evidence `glechoma_hederacea`–`impatiens_noli_tangere` (d=0.985): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.985}`
- Provenance (sample): `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C115 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.5, 31.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
- Closest pair evidence `gleditsia_triacanthos`–`trifolium_arvense` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `gleditsia_triacanthos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C116 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 24.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
- Closest pair evidence `hedysarum_corona`–`sulla_coronaria` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `hedysarum_corona`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sulla_coronaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C117 (n=2, mean_d=0.437, max_d=0.437)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 30.3)
- Shared sculpture tokens: microreticulaat, reticulaat
- Members:
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={microreticulaat,reticulaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={microreticulaat,reticulaat}
- Closest pair evidence `helleborus_foetidus`–`vitex_agnus_castus` (d=0.437): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.437}`
- Provenance (sample): `helleborus_foetidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vitex_agnus_castus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C118 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.5, 35.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
- Closest pair evidence `helleborus_viridis_ssp_occidentalis`–`lamium_amplexicaule` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `helleborus_viridis_ssp_occidentalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lamium_amplexicaule`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C119 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (35.3, 35.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.973): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `sonchus_oleraceus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C120 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: tricol*
- Size classes: small; mid range: (23.0, 25.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `xanthium_italicum` | *Xanthium italicum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={scabraat}
- Closest pair evidence `hippopha_rhamn`–`xanthium_italicum` (d=0.605): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.605}`
- Provenance (sample): `hippopha_rhamn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `xanthium_italicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C121 (n=2, mean_d=0.951, max_d=0.951)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 29.4)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={reticulaat,scabraat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `hippophae_rhamnoides`–`odontites_vernus` (d=0.951): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.951}`
- Provenance (sample): `hippophae_rhamnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `odontites_vernus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C122 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 17.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `theobroma_cacao` | *Theobroma cacao* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
- Closest pair evidence `hypericum_tetrapterum`–`theobroma_cacao` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `hypericum_tetrapterum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `theobroma_cacao`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C123 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.9, 32.1)
- Shared sculpture tokens: —
- Members:
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm
- Closest pair evidence `hyssopus_officinalis`–`thymus_pulegioides` (d=0.985): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.985}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thymus_pulegioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C124 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: inapert*
- Size classes: very-small; mid range: (1.0, 1.0)
- Shared sculpture tokens: —
- Members:
  - `juncus_jacquinii` | *Juncus jacquinii* | unranked | ap=inapert* | class=very-small | mid=1.0µm
  - `luzula_sylvatica` | *Luzula sylvatica* | unranked | ap=inapert* | class=very-small | mid=1.0µm
- Closest pair evidence `juncus_jacquinii`–`luzula_sylvatica` (d=0.925): `{'aperture': 'same inapert*', 'size_class': 'same very-small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `juncus_jacquinii`: docs/keys/**:outcome_size; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `luzula_sylvatica`: docs/keys/**:outcome_size; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C125 (n=2, mean_d=0.740, max_d=0.740)

- Shared aperture: inapert*
- Size classes: medium; mid range: (26.0, 27.0)
- Shared sculpture tokens: reticulaat, scabraat, verrucaat
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.740): `{'aperture': 'same inapert*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same inapert', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.74}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C126 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.5, 28.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
- Closest pair evidence `laburnum_anagyroides`–`scrophularia_umbrosa` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `laburnum_anagyroides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scrophularia_umbrosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C127 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.5, 41.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | sc={reticulaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | sc={reticulaat}
- Closest pair evidence `lathyrus_pratensis`–`lathyrus_tuberosus` (d=0.949): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `lathyrus_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_tuberosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C128 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `pulmonaria_officinalis` | *Pulmonaria officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
- Closest pair evidence `lavandula_angisti`–`pulmonaria_officinalis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C129 (n=2, mean_d=0.531, max_d=0.531)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (42.5, 43.1)
- Shared sculpture tokens: echinaat
- Members:
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | sc={echinaat}
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | sc={echinaat}
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.531): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.531}`
- Provenance (sample): `leontodon_autumnalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `picris_hieracioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C130 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (21.5, 21.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | sc={reticulaat}
- Closest pair evidence `leonurus_cardiaca`–`salix_caprea` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `leonurus_cardiaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_caprea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C131 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 17.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
- Closest pair evidence `lepidium_sativum`–`tamarix_gallica` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `lepidium_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `tamarix_gallica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C132 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.8, 29.9)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `levisticum_officinale` | *Levisticum officinale* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={psilaat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | sc={psilaat}
- Closest pair evidence `levisticum_officinale`–`solanum_nigrum_ssp_nigrum` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `levisticum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `solanum_nigrum_ssp_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C133 (n=2, mean_d=0.615, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 31.0)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `malus_domestica` | *Malus domestica* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={rugulaat,striaat}
  - `malus_sylvestris` | *Malus sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={rugulaat,striaat}
- Closest pair evidence `malus_domestica`–`malus_sylvestris` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `malus_domestica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `malus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C134 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.5, 24.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** mercurialis_perennis ↔ mercurialis_typ
- Members:
  - `mercurialis_perennis` | *Mercurialis perennis* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mercurialis_typ` | *Mercurialis typ* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
- Closest pair evidence `mercurialis_perennis`–`mercurialis_typ` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `mercurialis_perennis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mercurialis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C135 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tetrade*
- Size classes: large; mid range: (47.4, 47.6)
- Shared sculpture tokens: —
- Members:
  - `moneses_uniflora` | *Moneses uniflora* | unranked | ap=tetrade* | class=large | mid=47.4µm | sc={scabraat,verrucaat}
  - `vaccinium_uliginosum` | *Vaccinium uliginosum* | unranked | ap=tetrade* | class=large | mid=47.6µm
- Closest pair evidence `moneses_uniflora`–`vaccinium_uliginosum` (d=0.985): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `moneses_uniflora`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json · `vaccinium_uliginosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C136 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: monocol*
- Size classes: large; mid range: (54.2, 54.2)
- Shared sculpture tokens: —
- Members:
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.925): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C137 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.0, 31.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `nepeta_cataria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `satureja_hortensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C138 (n=2, mean_d=0.795, max_d=0.795)

- Shared aperture: tricol*
- Size classes: large; mid range: (46.6, 48.4)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | sc={psilaat,reticulaat}
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | sc={psilaat,reticulaat}
- Closest pair evidence `nigella_damascena`–`saxifraga_granulata` (d=0.795): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.795}`
- Provenance (sample): `nigella_damascena`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `saxifraga_granulata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C139 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (33.0, 33.2)
- Shared sculpture tokens: —
- Members:
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm
- Closest pair evidence `origanum_vulgare`–`salvia_nemorosa` (d=0.973): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `origanum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `salvia_nemorosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C140 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
- Closest pair evidence `ornithopus_perpus`–`ornithopus_perpusillus` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `ornithopus_perpus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ornithopus_perpusillus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C141 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.0, 19.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
- Closest pair evidence `osmanthus_typ`–`thlaspi_arvense` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `osmanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thlaspi_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C142 (n=2, mean_d=0.615, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (43.0, 44.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `persicaria_bistorta` | *Persicaria bistorta* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat,scabraat}
  - `symphoricarpos_typ` | *Symphoricarpos typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `persicaria_bistorta`–`symphoricarpos_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `persicaria_bistorta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `symphoricarpos_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C143 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 22.7)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={reticulaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | sc={reticulaat}
- Closest pair evidence `platanus_hybr`–`raphanus_sativus` (d=0.973): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `platanus_hybr`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_sativus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C144 (n=2, mean_d=0.675, max_d=0.675)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.1, 40.4)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_armeniaca` | *Prunus armeniaca* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
- Closest pair evidence `prunus_armeniaca`–`prunus_cerasus` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.675}`
- Provenance (sample): `prunus_armeniaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_cerasus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C145 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: small; mid range: (20.9, 21.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat}
- Closest pair evidence `reseda_luteola`–`salix_triandra` (d=0.949): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `reseda_luteola`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_triandra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C146 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 33.0)
- Shared sculpture tokens: —
- Members:
  - `ribes_sanguineum` | *Ribes sanguineum* | unranked | ap=peripor* | class=medium | mid=33.0µm | sc={psilaat,scabraat}
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm
- Closest pair evidence `ribes_sanguineum`–`ribes_uva_crispa` (d=0.925): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `ribes_sanguineum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_uva_crispa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C147 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: —
- Members:
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm
- Closest pair evidence `rosmarinus_officinalis`–`thymus_vulgaris` (d=0.925): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `rosmarinus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C148 (n=2, mean_d=0.555, max_d=0.555)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.2, 23.0)
- Shared sculpture tokens: striaat
- Members:
  - `sedum_telephium` | *Sedum telephium* | unranked | ap=tricol* | class=small | mid=22.2µm | sc={striaat}
  - `sibbaldia_procumbens` | *Sibbaldia procumbens* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={striaat}
- Closest pair evidence `sedum_telephium`–`sibbaldia_procumbens` (d=0.555): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.555}`
- Provenance (sample): `sedum_telephium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sibbaldia_procumbens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C149 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.2, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat}
- Closest pair evidence `stachys_sylvatica`–`syringa_vulgaris` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `stachys_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `syringa_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C150 (n=2, mean_d=0.875, max_d=0.875)

- Shared aperture: tricol*
- Size classes: large; mid range: (80.0, 80.0)
- Shared sculpture tokens: echinaat
- Members:
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat}
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat,striaat}
- Closest pair evidence `succisa_praten`–`succisa_pratensis` (d=0.875): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.875}`
- Provenance (sample): `succisa_praten`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `succisa_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C151 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.8, 33.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
- Closest pair evidence `trifolium_dubium`–`vicia_sepium` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `trifolium_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_sepium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C152 (n=2, mean_d=0.645, max_d=0.645)

- Shared aperture: tripor*
- Size classes: small; mid range: (15.5, 16.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** urtica_dioica ↔ urtica_typ
- Members:
  - `urtica_dioica` | *Urtica dioica* | unranked | ap=tripor* | class=small | mid=15.5µm | sc={psilaat}
  - `urtica_typ` | *Urtica typ* | unranked | ap=tripor* | class=small | mid=16.0µm | sc={psilaat}
- Closest pair evidence `urtica_dioica`–`urtica_typ` (d=0.645): `{'aperture': 'same tripor*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.645}`
- Provenance (sample): `urtica_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `urtica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C153 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.2, 25.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
- Closest pair evidence `verbascum_blattaria`–`verbascum_densiflorum` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `verbascum_blattaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `verbascum_densiflorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C154 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.2, 33.3)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | sc={psilaat}
- Closest pair evidence `veronica_officinalis`–`viola_hirta` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `veronica_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viola_hirta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

## 5. Looser clusters (close)

Clusters with ≥2 members at loose≤1.750 cut. Learning-priority clusters listed first.

- With ≥1 learning_priority_rank: **30**
- Unranked-only: **148**
- Total: **178**

### C1 (n=12, mean_d=0.746, max_d=1.569) — ranks [1]

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.0, 30.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_typ` | *Brassica typ* | rank=1 | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `cakile_maritima` | *Cakile maritima* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `euodia_hupehensis` | *Euodia hupehensis* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={reticulaat}
- Closest pair evidence `aralia_elata`–`ricinus_communis` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aralia_elata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `brassica_typ`: data/pollen.yaml:size; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm · `cakile_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_parcifl`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C2 (n=9, mean_d=0.872, max_d=1.573) — ranks [2]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.3, 34.0)
- Shared sculpture tokens: —
- Members:
  - `prunus_pirus_typ` | *Prunus pirus* | rank=2 | ap=tricol* | class=medium | mid=32.5µm | sc={striaat}
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | sculpt_MASKED
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={striaat}
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | sculpt_MASKED
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | sc={striaat}
  - `rosa_pimpinellifolia` | *Rosa pimpinellifolia* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | sc={striaat}
  - `vaccinium_vitis` | *Vaccinium vitis* | unranked | ap=tricol* | class=medium | mid=34.0µm
- Closest pair evidence `prunus_mahaleb`–`rosa_pimpinellifolia` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.387}`
- Provenance (sample): `agrimonia_eupatoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `potentilla_norvegica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_mahaleb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_pirus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband

### C3 (n=2, mean_d=1.125, max_d=1.125) — ranks [3]

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | sc={psilaat,striaat}
  - `solanum_tuberosum` | *Solanum tuberosum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={psilaat}
- Closest pair evidence `rubus_typ`–`solanum_tuberosum` (d=1.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `rubus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_tuberosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C4 (n=41, mean_d=1.326, max_d=1.645) — ranks [4, 33]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.0, 36.2)
- Shared sculpture tokens: echinaat
- **already_decided:** `helianthus_annuus`–`taraxacum_typ` (review:different)
- Members:
  - `taraxacum_typ` | *Taraxacum typ* | rank=4 | ap=tricol* | class=medium | mid=32.5µm | sc={echinaat}
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat}
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `cirsium_dissectum` | *Cirsium dissectum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_oleraceum` | *Cirsium oleraceum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_palustre` | *Cirsium palustre* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_rivulare` | *Cirsium rivulare* | unranked | ap=tricol* | sc={echinaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={echinaat}
  - `erigeron_annuus` | *Erigeron annuus* | unranked | ap=tricol* | sc={echinaat}
  - `galinsoga_ciliata` | *Galinsoga ciliata* | unranked | ap=tricol* | sc={echinaat}
  - `helichrysum_arenarium` | *Helichrysum arenarium* | unranked | ap=tricol* | sc={echinaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={echinaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={echinaat}
  - `inula_conyzae` | *Inula conyzae* | unranked | ap=tricol* | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `lonicera_fragrantissima` | *Lonicera Fragrantissima* | unranked | ap=tricol* | sc={echinaat}
  - `lonicera_japonica` | *Lonicera Japonica* | unranked | ap=tricol* | sc={echinaat}
  - `petasites_albus` | *Petasites albus* | unranked | ap=tricol* | sc={echinaat}
  - `pulicaria_dysenterica` | *Pulicaria dysenterica* | unranked | ap=tricol* | sc={echinaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={echinaat}
  - `senecio_cineraria` | *Senecio Cineraria* | unranked | ap=tricol* | sc={echinaat}
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={echinaat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | sc={echinaat}
  - `silybum_marianum` | *Silybum marianum* | unranked | ap=tricol* | sc={echinaat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={echinaat}
  - `tanacetum_corymbosum` | *Tanacetum corymbosum* | unranked | ap=tricol* | sc={echinaat}
  - `telekia_speciosa` | *Telekia speciosa* | unranked | ap=tricol* | sc={echinaat}
  - `tephroseris_palustris` | *Tephroseris palustris* | unranked | ap=tricol* | sc={echinaat}
  - `tripleurospermum_maritimum` | *Tripleurospermum maritimum* | unranked | ap=tricol* | sc={echinaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={echinaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | sc={echinaat}
- Closest pair evidence `taraxacum_typ`–`tussilago_farfara` (d=0.245): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `achillea_millefolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `anthemis_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `aster_sedifolius`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `calendula_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C5 (n=11, mean_d=1.124, max_d=1.687) — ranks [5]

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.1, 38.6)
- Shared sculpture tokens: —
- Members:
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=38.1µm | sculpt_MASKED
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={reticulaat}
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm
  - `euphorbia_amygdaloides` | *Euphorbia amygdaloides* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={reticulaat}
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `paeonia_officinalis` | *Paeonia officinalis* | unranked | ap=tricol* | class=medium | mid=37.2µm | sc={microreticulaat,reticulaat}
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `tilia_americana` | *Tilia americana* | unranked | ap=tricol* | class=medium | mid=37.9µm | sc={reticulaat}
  - `tilia_platyphyllos` | *Tilia Platyphyllos* | unranked | ap=tricol* | class=medium | mid=37.3µm | sc={reticulaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | sc={reticulaat}
  - `vicia_villosa` | *Vicia villosa* | unranked | ap=tricol* | class=medium | mid=38.6µm | sc={reticulaat}
- Closest pair evidence `centaurea_cyanus`–`empetrum_nigrum` (d=0.674): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.674}`
- Provenance (sample): `callicarpa_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_cyanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `empetrum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `euphorbia_amygdaloides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C6 (n=5, mean_d=1.208, max_d=1.645) — ranks [6, 45]

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.5, 40.0)
- Shared sculpture tokens: —
- Members:
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | size_MASKED | sc={reticulaat}
  - `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | size_MASKED | sc={reticulaat}
  - `bryonia_dioica` | *Bryonia dioica* | unranked | ap=tricol* | class=medium | mid=39.5µm | sc={reticulaat}
  - `pisum_sativum` | *Pisum sativum* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={reticulaat}
  - `vaccinium_corymb` | *Vaccinium corymb* | unranked | ap=tricol* | class=medium | mid=39.5µm
- Closest pair evidence `trifolium_pratense`–`trifolium_repens` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `bryonia_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pisum_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `trifolium_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C7 (n=7, mean_d=1.279, max_d=1.525) — ranks [7, 14]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 20.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `rhamnus` | *Rhamnus* | rank=7 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `echium` | *Echium* | rank=14 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `alyssum_typ` | *Alyssum typ* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `arabis_procurrens` | *Arabis procurrens* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={reticulaat}
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | sc={reticulaat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat}
- Closest pair evidence `lepidium_sativum`–`tamarix_gallica` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `alyssum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arabis_procurrens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `echium`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `lepidium_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C8 (n=3, mean_d=0.992, max_d=1.625) — ranks [8]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.0)
- Shared sculpture tokens: —
- Members:
  - `aesculus` | *Aesculus* | rank=8 | ap=tricol* | class=small | mid=20.0µm | sc={psilaat}
  - `erigeron_canaden` | *Erigeron canadensis* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={echinaat}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm
- Closest pair evidence `aesculus`–`solanum_lycopers` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `aesculus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `erigeron_canaden`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_lycopers`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C9 (n=4, mean_d=1.042, max_d=1.407) — ranks [9]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.0)
- Shared sculpture tokens: —
- Members:
  - `robinia` | *Robinia* | rank=9 | ap=tricol* | class=medium | mid=32.5µm | sc={scabraat}
  - `arctostaphylos_alpina` | *Arctostaphylos alpina* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={scabraat,verrucaat}
  - `cotoneaster_intergerrimus` | *Cotoneaster intergerrimus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sculpt_MASKED
  - `genista_tinctoria` | *Genista tinctoria* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={scabraat,verrucaat}
- Closest pair evidence `arctostaphylos_alpina`–`cotoneaster_intergerrimus` (d=0.650): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.65}`
- Provenance (sample): `arctostaphylos_alpina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cotoneaster_intergerrimus`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `genista_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `robinia`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband

### C10 (n=6, mean_d=1.141, max_d=1.697) — ranks [10]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.0, 32.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `vicia_typ` | *Vicia typ* | rank=10 | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={reticulaat}
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat}
  - `tropaeolum_majus` | *Tropaeolum majus* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={reticulaat}
- Closest pair evidence `euphorbia_cyparissias`–`vicia_typ` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `euphorbia_cyparissias`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `glaucium_flavum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `stachys_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `syringa_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C11 (n=2, mean_d=0.745, max_d=0.745) — ranks [11]

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.1, 34.8)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | sc={rugulaat,striaat}
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | sc={rugulaat,striaat}
- Closest pair evidence `acer_campestre`–`acer_platanoides` (d=0.745): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.25, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.745}`
- Provenance (sample): `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_platanoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C12 (n=2, mean_d=0.855, max_d=0.855) — ranks [12]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 22.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `anthriscus_typ` | *Anthriscus typ* | rank=12 | ap=tricol* | class=small | mid=20.0µm | sc={verrucaat}
  - `eucalyptus_camaldulensis` | *Eucalyptus camaldulensis* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={verrucaat}
- Closest pair evidence `anthriscus_typ`–`eucalyptus_camaldulensis` (d=0.855): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.855}`
- Provenance (sample): `anthriscus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `eucalyptus_camaldulensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C13 (n=16, mean_d=0.774, max_d=1.685) — ranks [13, 18, 19]

- Shared aperture: tricol*
- Size classes: small; mid range: (15.0, 21.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `raphanus_typ` | *Raphanus typ* | rank=18 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `verbascum` | *Verbascum* | rank=19 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat}
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat}
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
  - `tamarix_typ` | *Tamarix typ* | unranked | ap=tricol* | class=small | mid=15.0µm | sc={reticulaat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | size_MASKED | sc={reticulaat}
- Closest pair evidence `deutzia_typ`–`linaria_cymbalaria` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `alyssum_saxatile`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `amorpha_fructico`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `deutzia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `diplotaxis_tenuifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C14 (n=5, mean_d=0.883, max_d=1.617) — ranks [15, 17]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 36.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `parthenocissus` | *Parthenocissus* | rank=17 | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={reticulaat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={reticulaat}
- Closest pair evidence `parthenocissus`–`ulex_europaeus` (d=0.233): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.233}`
- Provenance (sample): `parthenocissus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `sinapis_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `stachys_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tilia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C15 (n=2, mean_d=0.845, max_d=0.845) — ranks [16]

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.5, 34.5)
- Shared sculpture tokens: reticulaat, verrucaat
- Members:
  - `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat,verrucaat}
  - `linum_usitatissimum` | *Linum usitatissimum* | unranked | ap=tricol* | size_MASKED | sc={reticulaat,verrucaat}
- Closest pair evidence `linum_usitatissimum`–`ranunculus_typ` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.845}`
- Provenance (sample): `linum_usitatissimum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C16 (n=3, mean_d=1.138, max_d=1.245) — ranks [20]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `lotus` | *Lotus* | rank=20 | ap=tricol* | class=small | mid=20.0µm | sc={psilaat}
  - `aquilegia_vulgaris` | *Aquilegia vulgaris* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={psilaat}
  - `sedum_typ` | *Sedum typ* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={psilaat,striaat}
- Closest pair evidence `aquilegia_vulgaris`–`lotus` (d=1.045): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `aquilegia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lotus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteband · `sedum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C17 (n=3, mean_d=0.855, max_d=1.095) — ranks [21]

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 29.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | sc={psilaat,scabraat}
  - `cannabis_sativa` | *Cannabis sativa* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={psilaat,scabraat}
- Closest pair evidence `lamium_typ`–`photinia_typ` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `cannabis_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lamium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `photinia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C18 (n=2, mean_d=1.715, max_d=1.715) — ranks [26]

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.0, 26.0)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat,rugulaat,striaat}
  - `aesculus_carnea` | *Aesculus carnea* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={psilaat,rugulaat,striaat}
- Closest pair evidence `aesculus_carnea`–`ailanthus_altissima` (d=1.715): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat', 'striaat']}, 'shape': {'jaccard_dist': 0.75, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.715}`
- Provenance (sample): `aesculus_carnea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ailanthus_altissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C19 (n=3, mean_d=0.661, max_d=0.929) — ranks [29]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.4, 21.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | sc={reticulaat}
- Closest pair evidence `ononis`–`ononis_natrix` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `melilotus_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis_natrix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C20 (n=3, mean_d=1.112, max_d=1.245) — ranks [34]

- Shared aperture: tricol*
- Size classes: medium; mid range: (20.1, 20.1)
- Shared sculpture tokens: psilaat, reticulaat, scabraat, verrucaat
- Members:
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `anthriscus_sylvestris` | *Anthriscus sylvestris* | unranked | ap=tricol* | class=medium | mid=20.1µm | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `centaurea_montana`–`cornus_sanguinea` (d=0.845): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `anthriscus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_montana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_sanguinea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C21 (n=2, mean_d=1.220, max_d=1.220) — ranks [39]

- Shared aperture: tricol*
- Size classes: very-small; mid range: (13.0, 13.0)
- Shared sculpture tokens: psilaat, rugulaat, scabraat
- Members:
  - `castanea_sativa` | *Castanea sativa* | rank=39 | ap=tricol* | class=very-small | mid=13.0µm | sc={psilaat,rugulaat,scabraat}
  - `medicago_sativa` | *Medicago sativa* | unranked | ap=tricol* | size_MASKED | sc={psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `castanea_sativa`–`medicago_sativa` (d=1.220): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.25, 'shared': ['psilaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.22}`
- Provenance (sample): `castanea_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `medicago_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C22 (n=2, mean_d=1.481, max_d=1.481) — ranks [42]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.9, 21.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `amorpha_fruticosa` | *Amorpha fruticosa* | rank=42 | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat,verrucaat}
  - `artemisia_vulgaris` | *Artemisia vulgaris* | unranked | ap=tricol* | class=small | mid=21.5µm | sc={echinaat,reticulaat}
- Closest pair evidence `amorpha_fruticosa`–`artemisia_vulgaris` (d=1.481): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.25, 'shared': ['oblaat', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.481}`
- Provenance (sample): `amorpha_fruticosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `artemisia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C23 (n=6, mean_d=0.781, max_d=1.579) — ranks [44]

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.1, 42.5)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | sc={striaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `prunus_armeniaca` | *Prunus armeniaca* | unranked | ap=tricol* | class=medium | mid=39.1µm | sc={striaat}
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={striaat}
  - `prunus_laurocerasus` | *Prunus laurocerasus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={striaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={striaat}
- Closest pair evidence `crataegus_typ`–`prunus_spinoza` (d=0.365): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.365}`
- Provenance (sample): `acer_opalus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crataegus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_armeniaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_cerasus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C24 (n=4, mean_d=1.252, max_d=1.663) — ranks [49]

- Shared aperture: peripor*
- Size classes: medium; mid range: (34.8, 36.6)
- Shared sculpture tokens: —
- Members:
  - `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | sc={baculaat,reticulaat,verrucaat}
  - `cerastium_fontanum` | *Cerastium fontanum* | unranked | ap=peripor* | class=medium | mid=36.0µm | sc={reticulaat}
  - `ribes_nigrum` | *Ribes nigrum* | unranked | ap=peripor* | class=medium | mid=35.2µm
  - `stellaria_graminea` | *Stellaria graminea* | unranked | ap=peripor* | class=medium | mid=36.6µm
- Closest pair evidence `ribes_nigrum`–`silene_flos_cuculi` (d=1.033): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.033}`
- Provenance (sample): `cerastium_fontanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `silene_flos_cuculi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `stellaria_graminea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C25 (n=8, mean_d=1.156, max_d=1.527) — ranks [52]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (34.0, 36.0)
- Shared sculpture tokens: —
- Members:
  - `impatiens_glandulifera` | *Impatiens glandulifera* | rank=52 | ap=stephanocol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `borago_officinalis` | *Borago officinalis* | unranked | ap=stephanocol* | class=medium | mid=34.0µm | sc={reticulaat,scabraat}
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `thymus_praecox` | *Thymus praecox* | unranked | ap=stephanocol* | class=medium | mid=34.4µm
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat}
  - `veronica_filiformis` | *Veronica filiformis* | unranked | ap=stephanocol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `borago_officinalis`–`veronica_filiformis` (d=0.855): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.855}`
- Provenance (sample): `borago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_glandulifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C26 (n=6, mean_d=1.212, max_d=1.735) — ranks [53]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 21.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | sc={reticulaat,scabraat}
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | sc={reticulaat,scabraat}
  - `foeniculum_vulgaris` | *Foeniculum vulgaris* | unranked | ap=tricol* | class=small | mid=19.5µm | sc={scabraat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={reticulaat,scabraat,striaat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `clematis_vitalba`–`melampyrum_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clematis_vitalba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `daucus_carota`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C27 (n=2, mean_d=1.068, max_d=1.068) — ranks [64]

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.5, 36.2)
- Shared sculpture tokens: echinaat, psilaat, scabraat
- Members:
  - `calluna_vulgaris` | *Calluna vulgaris* | rank=64 | ap=tricol* | class=medium | mid=35.5µm | sc={echinaat,psilaat,scabraat,verrucaat}
  - `vaccinium_vitis_idaea` | *Vaccinium vitis-idaea* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={echinaat,psilaat,scabraat}
- Closest pair evidence `calluna_vulgaris`–`vaccinium_vitis_idaea` (d=1.068): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['echinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tetrade', 'shape': {'jaccard_dist': 0.5, 'shared': ['sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.068}`
- Provenance (sample): `calluna_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_vitis_idaea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C28 (n=3, mean_d=0.968, max_d=1.625) — ranks [71]

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=small | mid=25.0µm | sc={psilaat,reticulaat,scabraat}
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=small | mid=24.0µm | sculpt_MASKED
  - `potentilla_anserina` | *Potentilla anserina* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={striaat}
- Closest pair evidence `aesculus_hippocastanum`–`cornus_mas` (d=0.640): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': 'masked_conflict', 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.64}`
- Provenance (sample): `aesculus_hippocastanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_mas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `potentilla_anserina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C29 (n=4, mean_d=1.356, max_d=1.750) — ranks [75]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.8)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat,scabraat}
  - `callicarpa_bodinieri` | *Callicarpa bodinieri* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={rugulaat,scabraat,verrucaat}
  - `ranunculus_ficaria` | *Ranunculus ficaria* | unranked | ap=tricol* | class=medium | mid=32.9µm | sc={clavaat,echinaat,scabraat,verrucaat}
  - `saxifraga_rotundifolia` | *Saxifraga rotundifolia* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={psilaat,rugulaat,scabraat,striaat,verrucaat}
- Closest pair evidence `callicarpa_bodinieri`–`saxifraga_rotundifolia` (d=1.013): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.2, 'sculpture': {'jaccard_dist': 0.4, 'shared': ['rugulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.013}`
- Provenance (sample): `callicarpa_bodinieri`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_jacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_ficaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `saxifraga_rotundifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C30 (n=4, mean_d=1.064, max_d=1.245) — ranks [76]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.5, 39.0)
- Shared sculpture tokens: —
- Members:
  - `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | sc={reticulaat}
  - `eschscholtzia_calif` | *Eschscholtzia calif* | unranked | ap=stephanocol* | class=medium | mid=38.5µm | sc={reticulaat,scabraat}
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm
  - `oxalis_typ` | *Oxalis typ* | unranked | ap=stephanocol* | class=medium | mid=39.0µm | sc={reticulaat}
- Closest pair evidence `eschscholtzia_calif`–`melissa_officinalis` (d=0.949): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.949}`
- Provenance (sample): `eschscholtzia_calif`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_parviflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melissa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `oxalis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C31 (n=20, mean_d=0.751, max_d=1.565)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 29.5)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** hieracium_aurantiacum ↔ hieracium_typ; senecio_jacobaea ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_jacobea ↔ senecio_typ; aster_amellus ↔ aster_typ
- Members:
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={echinaat}
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={echinaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={echinaat}
  - `taraxacum_officinale` | *Taraxacum officinale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={echinaat}
- Closest pair evidence `aster_typ`–`matricaria_chamo` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `anthemis_nobilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aster_amellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aster_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotis_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C32 (n=15, mean_d=1.364, max_d=1.575)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.6, 24.1)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_laevigata` | *Crataegus laevigata* | unranked | ap=tricol* | sc={striaat}
  - `cydonia_oblonga` | *Cydonia oblonga* | unranked | ap=tricol* | sc={striaat}
  - `dryas_octopetala` | *Dryas octopetala* | unranked | ap=tricol* | size_MASKED | sc={striaat}
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=23.7µm | sc={striaat}
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={striaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={striaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={striaat}
  - `potentilla_palustris` | *Potentilla palustris* | unranked | ap=tricol* | sc={striaat}
  - `prunus_dulcis` | *Prunus dulcis* | unranked | ap=tricol* | sc={striaat}
  - `prunus_persica` | *Prunus persica* | unranked | ap=tricol* | sc={striaat}
  - `securigera_varia_coronilla_varia` | *Securigera varia* | unranked | ap=tricol* | sc={striaat}
  - `sedum_sexangulare` | *Sedum sexangulare* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | sc={striaat}
  - `sorbus_aria` | *Sorbus aria* | unranked | ap=tricol* | sc={striaat}
  - `waldsteinia_ternata` | *Waldsteinia ternata* | unranked | ap=tricol* | sc={striaat}
- Closest pair evidence `fragaria_moschata`–`geum_rivale` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `crataegus_laevigata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cydonia_oblonga`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `dryas_octopetala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `fragaria_moschata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size

### C33 (n=14, mean_d=1.161, max_d=1.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.5, 29.2)
- Shared sculpture tokens: —
- Members:
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={reticulaat}
  - `genista_pilosa` | *Genista pilosa* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={reticulaat}
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={reticulaat,scabraat}
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={reticulaat}
  - `ptelea_trifoliata` | *Ptelea trifoliata* | unranked | ap=tricol* | class=medium | mid=28.5µm | sc={microreticulaat,reticulaat}
  - `rosa_rubiginosa` | *Rosa rubiginosa* | unranked | ap=tricol* | class=medium | mid=28.0µm | sculpt_MASKED
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `verbascum_phlomoides` | *Verbascum phlomoides* | unranked | ap=tricol* | class=medium | mid=28.2µm | sc={reticulaat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=29.2µm | sc={reticulaat}
- Closest pair evidence `lysimachia_vulgaris`–`rosa_rubiginosa` (d=0.520): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.52}`
- Provenance (sample): `anacardium_occidentale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `genista_pilosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `laburnum_anagyroides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lupinus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C34 (n=11, mean_d=0.674, max_d=1.519)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.1, 29.4)
- Shared sculpture tokens: striaat
- Members:
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `comarum_palustre` | *Comarum palustre* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={striaat}
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | sc={striaat}
  - `sorbus_arranensis` | *Sorbus arranensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={striaat}
- Closest pair evidence `acer_japonicum`–`sorbus_arranensis` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `comarum_palustre`: data/pollen.yaml:shape; docs/keys/**:outcome_size; eide:docs/keys/eide/rosaceae-eide.json; feagri-iversen:docs/keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json · `lycium_barbarum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C35 (n=11, mean_d=1.050, max_d=1.437)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** crambe_maritima ↔ crambe_typ
- Members:
  - `ajuga_reptans` | *Ajuga reptans* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat,rugulaat}
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `brassica_nigra` | *Brassica nigra* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={reticulaat}
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | sc={reticulaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | sc={reticulaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={reticulaat}
  - `iberis_amara` | *Iberis amara* | unranked | ap=tricol* | class=medium | mid=25.7µm | sc={reticulaat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
- Closest pair evidence `crambe_maritima`–`crambe_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `ajuga_reptans`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `brassica_napus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `brassica_nigra`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `brassica_oleracea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C36 (n=11, mean_d=1.247, max_d=1.737)

- Shared aperture: tricol*
- Size classes: medium; mid range: (21.4, 23.9)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | sc={reticulaat}
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | sc={reticulaat}
  - `lunaria_annua` | *Lunaria annua* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_aurita` | *Salix aurita* | unranked | ap=tricol* | class=medium | mid=22.5µm | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={reticulaat}
  - `salix_viminalis` | *Salix viminalis* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={reticulaat}
  - `trollius_europaeus` | *Trollius europaeus* | unranked | ap=tricol* | class=medium | mid=21.4µm | sc={reticulaat,striaat}
- Closest pair evidence `salix_alba_var_tristis`–`salix_fragilis` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `cochlearia_officinalis_ssp_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `leonurus_cardiaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lunaria_annua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_alba_var_tristis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C37 (n=11, mean_d=0.732, max_d=1.485)

- Shared aperture: tricol*
- Size classes: small; mid range: (23.0, 24.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `digitalis_purpurea` | *Digitalis purpurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `genista_anglica` | *Genista anglica* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | sc={reticulaat}
  - `rubus_fructicosus` | *Rubus fructicosus* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={reticulaat,striaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={reticulaat}
- Closest pair evidence `digitalis_purpurea`–`polygonum_convol` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `digitalis_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `genista_anglica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hedysarum_corona`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lysimachia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C38 (n=10, mean_d=0.770, max_d=1.590)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `artemisia_typ` | *Artemisia typ* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={echinaat}
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={echinaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={echinaat}
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | sculpt_MASKED
  - `solidago_virgaurea` | *Solidago virgaurea* | unranked | ap=tricol* | class=small | mid=24.0µm | sc={echinaat}
- Closest pair evidence `chrysanthemum_leuc`–`eupatorium_cann` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `artemisia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bidens_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chrysanthemum_leuc`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cann`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C39 (n=9, mean_d=1.112, max_d=1.631)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.5, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** mercurialis_perennis ↔ mercurialis_typ
- Members:
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat}
  - `mercurialis_perennis` | *Mercurialis perennis* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `mercurialis_typ` | *Mercurialis typ* | unranked | ap=tricol* | class=medium | mid=24.5µm | sc={reticulaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=25.0µm | sc={reticulaat}
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={reticulaat}
  - `verbascum_thapsus` | *Verbascum thapsus* | unranked | ap=tricol* | class=medium | mid=25.6µm | sc={reticulaat}
- Closest pair evidence `euonymus_europaeus`–`mangifera_indica` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `euonymus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mangifera_indica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melilotus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mercurialis_perennis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C40 (n=8, mean_d=0.799, max_d=1.447)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.5, 45.0)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** carduus_defloratus ↔ carduus_typ
- Members:
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat}
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
  - `sonchus_arvensis` | *Sonchus arvensis* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={echinaat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={echinaat}
  - `viscum_album` | *Viscum album* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={echinaat}
  - `weigelia_diervilla_typ` | *Weigelia/Diervilla typ* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={echinaat}
- Closest pair evidence `carduus_defloratus`–`carduus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `arcticum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carduus_defloratus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carduus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_helenium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C41 (n=8, mean_d=0.834, max_d=1.415)

- Shared aperture: tricol*
- Size classes: large, medium; mid range: (30.3, 31.5)
- Shared sculpture tokens: echinaat
- Members:
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | sc={echinaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={echinaat}
  - `dipsacus_sylvester` | *Dipsacus Sylvester* | unranked | ap=tricol* | class=large | mid=30.5µm | sc={echinaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `picris_echioides` | *Picris echioides* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={echinaat}
- Closest pair evidence `bidens_ferulifolia`–`leucanthemum_vulgare` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `aster_alpinus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `bidens_ferulifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `buphthalmum_salicifolium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `dipsacus_sylvester`: docs/keys/**:outcome_size; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C42 (n=7, mean_d=0.686, max_d=1.363)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.8, 26.3)
- Shared sculpture tokens: striaat
- Members:
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | sc={striaat}
  - `potentilla_crantzii` | *Potentilla crantzii* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={striaat}
- Closest pair evidence `acer_palmatum`–`aesculus_hippoca` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_palmatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aesculus_hippoca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hippocrepis_comosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_crantzii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C43 (n=7, mean_d=0.730, max_d=1.645)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carduus_nutans` | *Carduus nutans* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={echinaat}
  - `sylibum_marianum` | *Sylibum marianum* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={echinaat}
- Closest pair evidence `cirsium_arvense`–`serrulata_tinctoria` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carduus_nutans`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cirsium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cnicus_benedict`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordon_acant`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C44 (n=7, mean_d=1.115, max_d=1.441)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.2, 35.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | sc={reticulaat}
  - `lupinus_polyphyllus` | *Lupinus polyphyllus* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat}
  - `onobrychis_viciifolia` | *Onobrychis viciifolia* | unranked | ap=tricol* | class=medium | mid=34.5µm | sc={reticulaat}
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | sc={reticulaat}
- Closest pair evidence `trifolium_dubium`–`vicia_sepium` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `colutea_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lupinus_angustifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lupinus_polyphyllus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onobrychis_viciifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C45 (n=7, mean_d=1.189, max_d=1.709)

- Shared aperture: tricol*
- Size classes: small; mid range: (20.5, 21.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `erysimum_cheiranthoides` | *Erysimum cheiranthoides* | unranked | ap=tricol* | class=small | mid=20.6µm | sc={reticulaat}
  - `hamamelis_japonica` | *Hamamelis japonica* | unranked | ap=tricol* | class=small | mid=21.3µm | sc={reticulaat}
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={reticulaat}
  - `rhamnus_cathartica` | *Rhamnus cathartica* | unranked | ap=tricol* | class=small | mid=20.5µm | sc={reticulaat,rugulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat}
- Closest pair evidence `ornithopus_perpus`–`ornithopus_perpusillus` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `erysimum_cheiranthoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hamamelis_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ornithopus_perpus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ornithopus_perpusillus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C46 (n=7, mean_d=0.985, max_d=1.695)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 23.0)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={striaat}
  - `fragaria_viridis` | *Fragaria viridis* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={striaat}
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | sc={striaat}
  - `rubus_arcticus` | *Rubus arcticus* | unranked | ap=tricol* | class=small | mid=17.5µm | sc={striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | sc={striaat}
  - `sedum_telephium` | *Sedum telephium* | unranked | ap=tricol* | class=small | mid=22.2µm | sc={striaat}
  - `sibbaldia_procumbens` | *Sibbaldia procumbens* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={striaat}
- Closest pair evidence `fragaria_viridis`–`rubus_arcticus` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `fragaria_vesca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fragaria_viridis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `potentilla_fruticosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rubus_arcticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C47 (n=7, mean_d=1.254, max_d=1.725)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.0, 33.5)
- Shared sculpture tokens: —
- Members:
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `skimmia_typ` | *Skimmia typ* | unranked | ap=stephanocol* | class=medium | mid=33.5µm | sc={reticulaat,striaat}
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `nepeta_cataria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `origanum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `salvia_nemorosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C48 (n=6, mean_d=1.324, max_d=1.717)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 34.3)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `aconitum_napellus` | *Aconitum napellus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={microreticulaat,psilaat}
  - `papaver_somniferum` | *Papaver somniferum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={psilaat}
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | sc={psilaat}
  - `veronica_persica` | *Veronica persica* | unranked | ap=tricol* | class=medium | mid=32.0µm | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | sc={psilaat}
  - `viola_riviniana` | *Viola riviniana* | unranked | ap=tricol* | class=medium | mid=34.3µm | sc={psilaat}
- Closest pair evidence `veronica_officinalis`–`viola_hirta` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `aconitum_napellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `papaver_somniferum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_persica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C49 (n=6, mean_d=1.176, max_d=1.501)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.1, 29.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `alyssum_repens` | *Alyssum repens* | unranked | ap=tricol* | class=medium | mid=27.5µm | sc={reticulaat}
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | sc={reticulaat}
  - `lamium_purpureum` | *Lamium purpureum* | unranked | ap=tricol* | class=medium | mid=27.1µm | sc={reticulaat}
  - `sinapis_alba` | *Sinapis alba* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={reticulaat}
- Closest pair evidence `cardamine_pratensis`–`corylopsis_pauciflora` (d=0.728): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.333, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.7277}`
- Provenance (sample): `alyssum_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ballota_nigra_ssp_foetida`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cardamine_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_pauciflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C50 (n=6, mean_d=1.207, max_d=1.573)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (32.5, 35.2)
- Shared sculpture tokens: —
- Members:
  - `campanula_cochleariifolia` | *Campanula cochleariifolia* | unranked | ap=stephanopor* | class=medium | mid=33.9µm
  - `campanula_patula` | *Campanula patula* | unranked | ap=stephanopor* | class=medium | mid=32.5µm
  - `campanula_rapunculus` | *Campanula rapunculus* | unranked | ap=stephanopor* | class=medium | mid=34.8µm
  - `campanula_trachelium` | *Campanula trachelium* | unranked | ap=stephanopor* | class=medium | mid=35.2µm | sc={echinaat,microechinaat}
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.925): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `campanula_cochleariifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_patula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_rapunculus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_trachelium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-trachelium.json

### C51 (n=6, mean_d=1.264, max_d=1.713)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.5, 44.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `helianthemum_typ` | *Helianthemum typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat}
  - `lathyrus_palustris` | *Lathyrus palustris* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={reticulaat}
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | sc={reticulaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | sc={reticulaat}
  - `persicaria_bistorta` | *Persicaria bistorta* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={reticulaat,scabraat}
  - `symphoricarpos_typ` | *Symphoricarpos typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `persicaria_bistorta`–`symphoricarpos_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `helianthemum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lathyrus_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_tuberosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C52 (n=6, mean_d=1.162, max_d=1.525)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (42.0, 44.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_sabaudum` | *Hieracium sabaudum* | unranked | ap=fenestr* | class=medium | mid=42.0µm
  - `hypochaeris_radicata` | *Hypochaeris radicata* | unranked | ap=fenestr* | class=medium | mid=44.0µm
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | sc={echinaat}
  - `leontodon_hispidus` | *Leontodon hispidus* | unranked | ap=fenestr* | class=medium | mid=44.5µm
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | sc={echinaat}
  - `sonchus_palustris` | *Sonchus palustris* | unranked | ap=fenestr* | class=medium | mid=43.2µm
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.531): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.531}`
- Provenance (sample): `hieracium_sabaudum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hypochaeris_radicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_autumnalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `leontodon_hispidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C53 (n=5, mean_d=1.114, max_d=1.579)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 30.0)
- Shared sculpture tokens: —
- Members:
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,rugulaat,striaat}
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat,reticulaat}
  - `rhinanthus_typ` | *Rhinanthus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat}
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={reticulaat,striaat}
- Closest pair evidence `acer_negundo`–`sarothamnus_sco` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `acer_negundo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `caltha_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhinanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sarothamnus_sco`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C54 (n=5, mean_d=1.248, max_d=1.711)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.9, 44.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={microreticulaat,psilaat,reticulaat}
  - `galeopsis_speciosa` | *Galeopsis speciosa* | unranked | ap=tricol* | class=medium | mid=44.3µm | sc={reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=42.9µm | sc={microreticulaat,psilaat,reticulaat}
  - `melittis_melissophyllum` | *Melittis melissophyllum* | unranked | ap=tricol* | class=medium | mid=43.8µm | sc={reticulaat}
  - `nigella_sativa` | *Nigella sativa* | unranked | ap=tricol* | class=medium | mid=43.1µm | sc={psilaat,reticulaat}
- Closest pair evidence `adonis_aestivalis`–`helleborus_niger` (d=0.411): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `adonis_aestivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galeopsis_speciosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_niger`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `melittis_melissophyllum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C55 (n=5, mean_d=1.033, max_d=1.165)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.2, 24.2)
- Shared sculpture tokens: —
- Members:
  - `amaranthus_caudatus` | *Amaranthus caudatus* | unranked | ap=peripor* | class=medium | mid=24.0µm | sc={scabraat}
  - `plantago_major` | *Plantago major* | unranked | ap=peripor* | class=medium | mid=23.2µm
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm
  - `thymelaea_passerina` | *Thymelaea passerina* | unranked | ap=peripor* | class=medium | mid=24.2µm
- Closest pair evidence `amaranthus_caudatus`–`ribes_alpinum` (d=0.949): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `amaranthus_caudatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `plantago_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ribes_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C56 (n=5, mean_d=1.365, max_d=1.699)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.4, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,verrucaat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,verrucaat}
  - `rhus_typhina` | *Rhus typhina* | unranked | ap=tricol* | class=medium | mid=32.4µm | sc={reticulaat,striaat}
  - `scrophularia_vernalis` | *Scrophularia vernalis* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat}
  - `trifolium_campestre` | *Trifolium campestre* | unranked | ap=tricol* | class=medium | mid=30.4µm | sc={reticulaat}
- Closest pair evidence `angelica_sylvestris`–`foeniculum_vulgare` (d=0.711): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `angelica_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhus_typhina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scrophularia_vernalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C57 (n=5, mean_d=1.187, max_d=1.680)

- Shared aperture: tricol*
- Size classes: small; mid range: (16.2, 17.0)
- Shared sculpture tokens: —
- Members:
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={microreticulaat,reticulaat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `theobroma_cacao` | *Theobroma cacao* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={reticulaat}
  - `veronicastrum_sibiricum` | *Veronicastrum sibiricum* | unranked | ap=tricol* | class=small | mid=16.2µm | sc={microreticulaat,psilaat,reticulaat,scabraat}
- Closest pair evidence `antirrhinum_majus`–`astragalus_sinicus` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `antirrhinum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `astragalus_sinicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_tetrapterum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `theobroma_cacao`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C58 (n=5, mean_d=0.785, max_d=1.595)

- Shared aperture: tricol*
- Size classes: large; mid range: (60.0, 61.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | size_MASKED | sc={echinaat}
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat}
  - `carthamus_tinctorius` | *Carthamus tinctorius* | unranked | ap=tricol* | class=large | mid=61.0µm | sc={echinaat}
  - `lonicera_typ` | *Lonicera typ* | unranked | ap=tricol* | class=large | mid=60.0µm | sc={echinaat,reticulaat}
- Closest pair evidence `carlina_acaulis`–`carlina_aucalis` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `arctium_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carlina_acaulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carlina_aucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carthamus_tinctorius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C59 (n=5, mean_d=0.673, max_d=0.963)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 25.2)
- Shared sculpture tokens: echinaat
- Members:
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={echinaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | sc={echinaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | sc={echinaat}
- Closest pair evidence `bellis_perennis`–`galinsoga_parviflora` (d=0.411): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `bellis_perennis`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `erigeron_acer`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galinsoga_parviflora`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `matricaria_recutita`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C60 (n=5, mean_d=1.134, max_d=1.369)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.0, 42.8)
- Shared sculpture tokens: —
- Members:
  - `berberis_typ` | *Berberis typ* | unranked | ap=stephanocol* | class=medium | mid=41.0µm | sc={psilaat}
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm
  - `salvia_argentea` | *Salvia argentea* | unranked | ap=stephanocol* | class=medium | mid=42.8µm
- Closest pair evidence `berberis_typ`–`clinopodium_vulgare` (d=0.985): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `berberis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C61 (n=5, mean_d=1.095, max_d=1.489)

- Shared aperture: peripor*
- Size classes: medium; mid range: (28.6, 31.0)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** borreria_verticilata ↔ borreria_typ
- Members:
  - `borreria_typ` | *Borreria typ* | unranked | ap=peripor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=peripor* | class=medium | mid=30.0µm | sc={reticulaat}
  - `chenopodium_bonus_henricus` | *Chenopodium bonus* | unranked | ap=peripor* | class=medium | mid=29.5µm
  - `daphne_mezereum` | *Daphne mezereum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={reticulaat}
  - `phlox_subulata` | *Phlox subulata* | unranked | ap=peripor* | class=medium | mid=31.0µm | sc={reticulaat}
- Closest pair evidence `borreria_verticilata`–`daphne_mezereum` (d=0.449): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.449}`
- Provenance (sample): `borreria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chenopodium_bonus_henricus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `daphne_mezereum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C62 (n=5, mean_d=1.014, max_d=1.105)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.1, 28.9)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={reticulaat}
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=28.9µm | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | sc={reticulaat}
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | sc={reticulaat}
- Closest pair evidence `brassica_rapa`–`marrubium_vulgare` (d=0.949): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `brassica_rapa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cardamine_flexuosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ligustrum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `marrubium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C63 (n=5, mean_d=1.341, max_d=1.677)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.5, 31.9)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | sc={psilaat,reticulaat}
  - `cytisus_scoparius` | *Cytisus scoparius* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat}
  - `malus_typ` | *Malus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={psilaat,rugulaat}
  - `medicago_falcata` | *Medicago falcata* | unranked | ap=tricol* | class=medium | mid=31.9µm | sc={psilaat}
  - `ornithopus_sativus` | *Ornithopus sativus* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={psilaat}
- Closest pair evidence `capsicum_annuum`–`cytisus_scoparius` (d=0.983): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.983}`
- Provenance (sample): `capsicum_annuum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cytisus_scoparius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `malus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `medicago_falcata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C64 (n=5, mean_d=1.198, max_d=1.635)

- Shared aperture: tricol*
- Size classes: large; mid range: (66.0, 70.6)
- Shared sculpture tokens: echinaat
- Members:
  - `carthamus_lanatus` | *Carthamus lanatus* | unranked | ap=tricol* | class=large | mid=66.0µm | sc={echinaat}
  - `centranthus_ruber` | *Centranthus ruber* | unranked | ap=tricol* | class=large | mid=68.5µm | sc={echinaat,reticulaat}
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | sc={echinaat}
  - `scabiosa_columbar` | *Scabiosa columbar* | unranked | ap=tricol* | class=large | mid=70.0µm | sc={echinaat}
- Closest pair evidence `echinops_sphaer`–`scabiosa_columbar` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `carthamus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centranthus_ruber`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `echinops_sphaer`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_alpigena`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C65 (n=5, mean_d=1.165, max_d=1.405)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 49.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cistus_salviifolius` | *Cistus salviifolius* | unranked | ap=tricol* | class=medium | mid=49.0µm | sc={reticulaat}
  - `pisum_typ` | *Pisum typ* | unranked | ap=tricol* | class=medium | mid=48.0µm | sc={reticulaat}
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | sc={reticulaat}
- Closest pair evidence `trifolium_incarnat`–`trifolium_incarnatum` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `cistus_salviifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pisum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_incarnat`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_incarnatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C66 (n=5, mean_d=1.266, max_d=1.705)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (32.5, 35.8)
- Shared sculpture tokens: —
- Members:
  - `crepis_tectorum` | *Crepis tectorum* | unranked | ap=fenestr* | class=medium | mid=35.8µm
  - `crepis_vesicaria_ssp_taraxacifol` | *Crepis vesicaria* | unranked | ap=fenestr* | class=medium | mid=32.5µm
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm
  - `lapsana_communis` | *Lapsana communis* | unranked | ap=fenestr* | class=medium | mid=34.9µm
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.973): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `crepis_tectorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `crepis_vesicaria_ssp_taraxacifol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lapsana_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C67 (n=5, mean_d=0.997, max_d=1.509)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.4, 32.5)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat,scabraat}
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={reticulaat,scabraat}
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={reticulaat,scabraat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={reticulaat,scabraat}
  - `teucrium_chamae` | *Teucrium chamae* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={scabraat}
- Closest pair evidence `cytisus_typ`–`pimpinella_anisum` (d=0.495): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `cytisus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eryngium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hippophae_rhamnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_anisum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C68 (n=5, mean_d=1.323, max_d=1.599)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.6, 37.0)
- Shared sculpture tokens: —
- Members:
  - `diplotaxis_muralis` | *Diplotaxis muralis* | unranked | ap=stephanocol* | class=medium | mid=37.0µm | sc={reticulaat}
  - `eschscholzia_californica` | *Eschscholzia californica* | unranked | ap=stephanocol* | class=medium | mid=36.0µm | sc={psilaat,reticulaat}
  - `lavandula_angustifolia` | *Lavandula angustifolia* | unranked | ap=stephanocol* | class=medium | mid=37.0µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `origanum_majorana` | *Origanum majorana* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | sc={reticulaat,rugulaat}
  - `satureja_montana` | *Satureja montana* | unranked | ap=stephanocol* | class=medium | mid=36.5µm
- Closest pair evidence `diplotaxis_muralis`–`satureja_montana` (d=1.045): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.045}`
- Provenance (sample): `diplotaxis_muralis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eschscholzia_californica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lavandula_angustifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `origanum_majorana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C69 (n=5, mean_d=0.920, max_d=1.359)

- Shared aperture: tricol*
- Size classes: large; mid range: (73.4, 77.5)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | sc={echinaat}
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | sc={echinaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=73.8µm | sc={echinaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | sc={echinaat}
- Closest pair evidence `lonicera_caprifolium`–`scabiosa_columbaria` (d=0.483): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.483}`
- Provenance (sample): `dipsacus_pilosus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `echinops_sphaerocephalus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `lonicera_caprifolium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `scabiosa_columbaria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-dipsacaceae.json

### C70 (n=5, mean_d=1.084, max_d=1.269)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.9, 35.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | sc={reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat}
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
  - `ilex_aquifolium` | *Ilex aquifolium* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={clavaat,reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={reticulaat}
- Closest pair evidence `helleborus_viridis_ssp_occidentalis`–`lamium_amplexicaule` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `erophila_verna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galeopsis_segetum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_viridis_ssp_occidentalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ilex_aquifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C71 (n=4, mean_d=1.411, max_d=1.725)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.0, 42.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `aegopodium_podagraria` | *Aegopodium podagraria* | unranked | ap=tricol* | class=medium | mid=42.5µm | sc={psilaat}
  - `cornus_alba` | *Cornus alba* | unranked | ap=tricol* | class=medium | mid=42.1µm | sc={psilaat}
  - `mespilus_germanica` | *Mespilus germanica* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={psilaat}
  - `symphoricarpos_albus` | *Symphoricarpos albus* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={psilaat,scabraat}
- Closest pair evidence `aegopodium_podagraria`–`cornus_alba` (d=1.009): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.009}`
- Provenance (sample): `aegopodium_podagraria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cornus_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `mespilus_germanica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphoricarpos_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C72 (n=4, mean_d=1.124, max_d=1.477)

- Shared aperture: monocol*
- Size classes: medium; mid range: (31.5, 33.8)
- Shared sculpture tokens: —
- Members:
  - `allium_porrum` | *Allium porrum* | unranked | ap=monocol* | class=medium | mid=33.3µm
  - `allium_scorodoprasum` | *Allium scorodoprasum* | unranked | ap=monocol* | class=medium | mid=33.8µm
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.1µm | sc={psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `butomus_umbellatus`–`leucojum_aestivum` (d=0.821): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.65, 'sculpture': {'jaccard_dist': 0.2, 'shared': ['psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.821}`
- Provenance (sample): `allium_porrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_scorodoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `butomus_umbellatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json · `leucojum_aestivum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json

### C73 (n=4, mean_d=1.412, max_d=1.705)

- Shared aperture: monocol*
- Size classes: medium; mid range: (39.0, 42.2)
- Shared sculpture tokens: —
- Members:
  - `allium_senescens` | *Allium senescens* | unranked | ap=monocol* | class=medium | mid=39.0µm
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | size_MASKED | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `convallaria_majalis` | *Convallaria majalis* | unranked | ap=monocol* | class=medium | mid=42.2µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_vernum` | *Leucojum vernum* | unranked | ap=monocol* | class=medium | mid=39.9µm
- Closest pair evidence `allium_ursinum`–`convallaria_majalis` (d=0.845): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `allium_senescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `convallaria_majalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug09-monocolpatae.json · `leucojum_vernum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C74 (n=4, mean_d=0.955, max_d=1.141)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (39.5, 40.4)
- Shared sculpture tokens: —
- Members:
  - `arctium_lappa` | *Arctium lappa* | unranked | ap=fenestr* | class=medium | mid=40.0µm | sc={echinaat}
  - `hieracium_umbellatum` | *Hieracium umbellatum* | unranked | ap=fenestr* | class=medium | mid=39.6µm
  - `lactuca_sativa` | *Lactuca sativa* | unranked | ap=fenestr* | class=medium | mid=40.4µm
  - `vaccinium_corymbosum` | *Vaccinium corymbosum* | unranked | ap=fenestr* | class=medium | mid=39.5µm | sc={echinaat}
- Closest pair evidence `arctium_lappa`–`vaccinium_corymbosum` (d=0.495): `{'aperture': 'same fenestr*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `arctium_lappa`: data/pollen.yaml:sculpture; docs/keys/**:outcome_size; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `hieracium_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lactuca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `vaccinium_corymbosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C75 (n=4, mean_d=1.189, max_d=1.405)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 37.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `arctostaphylos_uva_ursi` | *Arctostaphylos uva-ursi* | unranked | ap=tricol* | class=medium | mid=35.5µm | sc={psilaat}
  - `lathyrus_sylvestris` | *Lathyrus sylvestris* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={psilaat}
  - `pimpinella_saxifraga` | *Pimpinella saxifraga* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={psilaat}
  - `styrax_japonicus` | *Styrax japonicus* | unranked | ap=tricol* | class=medium | mid=36.1µm | sc={psilaat}
- Closest pair evidence `arctostaphylos_uva_ursi`–`pimpinella_saxifraga` (d=1.045): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `arctostaphylos_uva_ursi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lathyrus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_saxifraga`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `styrax_japonicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C76 (n=4, mean_d=1.113, max_d=1.303)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.0, 39.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | sc={echinaat}
  - `cichorium_intybus` | *Cichorium intybus* | unranked | ap=tricol* | class=medium | mid=38.0µm | sc={echinaat}
  - `erica_tetralix` | *Erica tetralix* | unranked | ap=tricol* | class=medium | mid=38.5µm | sc={echinaat,verrucaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | sc={echinaat}
- Closest pair evidence `arnica_montana`–`senecio_ovatus` (d=0.387): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `arnica_montana`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cichorium_intybus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erica_tetralix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_ovatus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C77 (n=4, mean_d=1.242, max_d=1.733)

- Shared aperture: tricol*
- Size classes: small; mid range: (18.8, 19.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `ceanothus_americanus` | *Ceanothus americanus* | unranked | ap=tricol* | class=small | mid=19.4µm | sc={reticulaat}
  - `hypericum_androsaemum` | *Hypericum androsaemum* | unranked | ap=tricol* | class=small | mid=18.8µm | sc={reticulaat}
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={reticulaat}
- Closest pair evidence `osmanthus_typ`–`thlaspi_arvense` (d=0.925): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `ceanothus_americanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hypericum_androsaemum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `osmanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thlaspi_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C78 (n=4, mean_d=1.219, max_d=1.465)

- Shared aperture: monocol*
- Size classes: large; mid range: (52.0, 54.2)
- Shared sculpture tokens: —
- Members:
  - `colchicinum_autu` | *Colchicinum autu* | unranked | ap=monocol* | class=large | mid=52.0µm | sc={reticulaat}
  - `magnolia_kobus` | *Magnolia kobus* | unranked | ap=monocol* | class=large | mid=53.6µm
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.925): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `colchicinum_autu`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `magnolia_kobus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C79 (n=4, mean_d=0.746, max_d=1.255)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 35.9)
- Shared sculpture tokens: striaat
- Members:
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `crataegus_oxycantha` | *Crataegus oxycantha* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={striaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | sc={striaat}
  - `saxifraga_umbrosa` | *Saxifraga umbrosa* | unranked | ap=tricol* | class=medium | mid=35.1µm | sc={striaat}
- Closest pair evidence `cotoneaster_integerrimus`–`prunus_cerasifera` (d=0.375): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `cotoneaster_integerrimus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crataegus_oxycantha`: docs/keys/**:outcome_size; eide:docs/keys/eide/rosaceae-eide.json · `prunus_cerasifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `saxifraga_umbrosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C80 (n=4, mean_d=1.304, max_d=1.613)

- Shared aperture: peripor*
- Size classes: medium; mid range: (38.6, 41.1)
- Shared sculpture tokens: —
- Members:
  - `dianthus_deltoides` | *Dianthus Deltoides* | unranked | ap=peripor* | class=medium | mid=41.1µm
  - `papaver_argemone` | *Papaver argemone* | unranked | ap=peripor* | class=medium | mid=38.6µm | sc={clavaat,echinaat,gemmaat,microechinaat,microreticulaat}
  - `stellaria_holostea` | *Stellaria holostea* | unranked | ap=peripor* | class=medium | mid=39.9µm | sc={microechinaat,microreticulaat,scabraat}
  - `stellaria_nemorum` | *Stellaria nemorum* | unranked | ap=peripor* | class=medium | mid=40.2µm
- Closest pair evidence `stellaria_holostea`–`stellaria_nemorum` (d=1.009): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.009}`
- Provenance (sample): `dianthus_deltoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `papaver_argemone`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-papaver-argemone.json · `stellaria_holostea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-caryophyllaceae.json · `stellaria_nemorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C81 (n=4, mean_d=1.052, max_d=1.365)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 18.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat,reticulaat}
  - `philadelphus_coronarius` | *Philadelphus coronarius* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={psilaat,reticulaat}
  - `sambucus_nigra` | *Sambucus nigra* | unranked | ap=tricol* | class=small | mid=18.0µm | sc={psilaat,reticulaat}
  - `spiraea_cantoniensis_x_trilobata` | *S. cantoniensis x S. trilobata* | unranked | ap=tricol* | class=small | mid=17.0µm | sc={psilaat}
- Closest pair evidence `echium_vulgare`–`sambucus_nigra` (d=0.365): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.365}`
- Provenance (sample): `echium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `philadelphus_coronarius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sambucus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spiraea_cantoniensis_x_trilobata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C82 (n=4, mean_d=1.302, max_d=1.615)

- Shared aperture: tricol*
- Size classes: small; mid range: (18.9, 20.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `escallonia_typ` | *Escallonia typ* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={psilaat}
  - `frangula_alnus` | *Frangula alnus* | unranked | ap=tricol* | class=small | mid=20.0µm | sc={psilaat,scabraat,verrucaat}
  - `lotus_corniculatus` | *Lotus corniculatus* | unranked | ap=tricol* | class=small | mid=18.9µm | sc={psilaat,scabraat}
  - `solanum_lycopersicum` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=19.8µm | sc={psilaat,rugulaat,scabraat}
- Closest pair evidence `frangula_alnus`–`lotus_corniculatus` (d=1.077): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 1.05, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.25, 'shared': ['driehoekig', 'prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.077}`
- Provenance (sample): `escallonia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `frangula_alnus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lotus_corniculatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_lycopersicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C83 (n=4, mean_d=1.158, max_d=1.625)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: —
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `pulmonaria_officinalis` | *Pulmonaria officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | sc={reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm
- Closest pair evidence `lavandula_angisti`–`pulmonaria_officinalis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rosmarinus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C84 (n=3, mean_d=0.980, max_d=1.283)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 36.7)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `aconitum_typ` | *Aconitum typ* | unranked | ap=tricol* | class=medium | mid=35.0µm | sc={reticulaat,scabraat}
  - `ficaria_typ` | *Ficaria typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | sc={reticulaat,scabraat}
  - `vicia_cracca` | *Vicia cracca* | unranked | ap=tricol* | class=medium | mid=36.7µm | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `aconitum_typ`–`ficaria_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `aconitum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ficaria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vicia_cracca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C85 (n=3, mean_d=1.189, max_d=1.321)

- Shared aperture: peripor*
- Size classes: medium; mid range: (26.9, 28.6)
- Shared sculpture tokens: —
- Members:
  - `alisma_plantago_aquatica` | *Alisma plantago* | unranked | ap=peripor* | class=medium | mid=26.9µm
  - `gypsophila_paniculata` | *Gypsophila paniculata* | unranked | ap=peripor* | class=medium | mid=27.8µm
  - `ribes_rubrum` | *Ribes rubrum* | unranked | ap=peripor* | class=medium | mid=28.6µm | sc={psilaat,scabraat}
- Closest pair evidence `gypsophila_paniculata`–`ribes_rubrum` (d=1.117): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.8, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.117}`
- Provenance (sample): `alisma_plantago_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-alisma-typ.json · `gypsophila_paniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ribes_rubrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C86 (n=3, mean_d=1.206, max_d=1.693)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.5, 26.5)
- Shared sculpture tokens: microreticulaat, reticulaat
- Members:
  - `alyssum_montanum` | *Alyssum montanum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,reticulaat}
  - `cercis_siliquastrum` | *Cercis siliquastrum* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={microreticulaat,reticulaat}
  - `fraxinus_excelsior` | *Fraxinus excelsior* | unranked | ap=tricol* | class=medium | mid=25.5µm | sc={microreticulaat,reticulaat}
- Closest pair evidence `alyssum_montanum`–`fraxinus_excelsior` (d=0.833): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.95, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.6, 'shared': ['prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.833}`
- Provenance (sample): `alyssum_montanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cercis_siliquastrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fraxinus_excelsior`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C87 (n=3, mean_d=1.118, max_d=1.215)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 36.2)
- Shared sculpture tokens: rugulaat
- Members:
  - `angelica_archangelica` | *Angelica archangelica* | unranked | ap=tricol* | class=medium | mid=36.2µm | sc={rugulaat}
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | sc={rugulaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | sc={rugulaat}
- Closest pair evidence `davidia_involucrata`–`rubus_fruticosus` (d=0.985): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat']}, 'shape': {'jaccard_dist': 1.0, 'shared': []}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `angelica_archangelica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture · `davidia_involucrata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_fruticosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C88 (n=3, mean_d=1.306, max_d=1.497)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.9, 24.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `anthriscus_caucalis` | *Anthriscus caucalis* | unranked | ap=tricol* | class=medium | mid=23.4µm | sc={psilaat}
  - `artemisia_dracunculus` | *Artemisia dracunculus* | unranked | ap=tricol* | class=medium | mid=22.9µm | sc={echinaat,psilaat}
  - `pimpinella_major` | *Pimpinella major* | unranked | ap=tricol* | class=medium | mid=24.4µm | sc={psilaat}
- Closest pair evidence `anthriscus_caucalis`–`pimpinella_major` (d=1.165): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.165}`
- Provenance (sample): `anthriscus_caucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `artemisia_dracunculus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `pimpinella_major`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size

### C89 (n=3, mean_d=1.266, max_d=1.687)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.9)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `pyrus_communis` | *Pyrus communis* | unranked | ap=tricol* | class=medium | mid=32.6µm | sc={rugulaat,scabraat,striaat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `astrantia_major`–`ranunculus_repens` (d=0.711): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['gemmaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `astrantia_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pyrus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C90 (n=3, mean_d=1.165, max_d=1.285)

- Shared aperture: peripor*
- Size classes: medium; mid range: (32.5, 34.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `buxus_sempervirens` | *Buxus sempervirens* | unranked | ap=peripor* | class=medium | mid=33.5µm | sc={reticulaat}
  - `phlox_typ` | *Phlox typ* | unranked | ap=peripor* | class=medium | mid=32.5µm | sc={reticulaat}
  - `silene_dioica` | *Silene dioica* | unranked | ap=peripor* | class=medium | mid=34.0µm | sc={reticulaat}
- Closest pair evidence `buxus_sempervirens`–`silene_dioica` (d=1.045): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `buxus_sempervirens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-buxus.json · `phlox_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `silene_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C91 (n=3, mean_d=1.037, max_d=1.093)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.7, 29.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | sc={psilaat}
  - `lamium_maculatum_cv_var` | *Lamium maculatum* | unranked | ap=tricol* | class=medium | mid=28.7µm | sc={psilaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | sc={psilaat}
- Closest pair evidence `caltha_palustris_ssp_araneosa`–`papaver_dubium` (d=0.985): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `caltha_palustris_ssp_araneosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lamium_maculatum_cv_var`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `papaver_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C92 (n=3, mean_d=0.372, max_d=0.495)

- Shared aperture: tricol*
- Size classes: large; mid range: (47.2, 47.8)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** serratula_tinctoria ↔ serratula_typ
- Members:
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | sc={echinaat}
- Closest pair evidence `serratula_tinctoria`–`serratula_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_crispus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `serratula_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serratula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C93 (n=3, mean_d=1.555, max_d=1.645)

- Shared aperture: peripor*
- Size classes: large; mid range: (46.5, 49.5)
- Shared sculpture tokens: —
- Members:
  - `carex_typ` | *Carex typ* | unranked | ap=peripor* | class=large | mid=49.5µm | sc={reticulaat,verrucaat}
  - `polemonium_boreale` | *Polemonium boreale* | unranked | ap=peripor* | class=large | mid=48.4µm | sc={reticulaat,striaat}
  - `saponaria_officinalis` | *Saponaria officinalis* | unranked | ap=peripor* | class=large | mid=46.5µm
- Closest pair evidence `polemonium_boreale`–`saponaria_officinalis` (d=1.381): `{'aperture': 'same peripor*', 'size_class': 'same large', 'size_mid_gap_um': 1.9, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.381}`
- Provenance (sample): `carex_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polemonium_boreale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-polemonium.json · `saponaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C94 (n=3, mean_d=1.245, max_d=1.405)

- Shared aperture: fenestr*
- Size classes: large; mid range: (52.8, 54.8)
- Shared sculpture tokens: —
- Members:
  - `cichorium_endivia` | *Cichorium endivia* | unranked | ap=fenestr* | class=large | mid=52.8µm
  - `leontodon_saxatilis` | *Leontodon saxatilis* | unranked | ap=fenestr* | class=large | mid=53.4µm
  - `prenanthes_purpurea` | *Prenanthes purpurea* | unranked | ap=fenestr* | class=large | mid=54.8µm
- Closest pair evidence `cichorium_endivia`–`leontodon_saxatilis` (d=1.081): `{'aperture': 'same fenestr*', 'size_class': 'same large', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.081}`
- Provenance (sample): `cichorium_endivia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `prenanthes_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C95 (n=3, mean_d=1.238, max_d=1.395)

- Shared aperture: tricol*
- Size classes: large; mid range: (51.0, 55.2)
- Shared sculpture tokens: echinaat
- Members:
  - `cirsium_vulgare` | *Cirsium vulgare* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={echinaat}
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | sc={echinaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=52.8µm | sc={echinaat}
- Closest pair evidence `cynara_cardunculus`–`lonicera_xylosteum` (d=0.975): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.975}`
- Provenance (sample): `cirsium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cynara_cardunculus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_xylosteum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-lonicera.json

### C96 (n=3, mean_d=1.472, max_d=1.645)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (22.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `citrus_sinensis` | *Citrus sinensis* | unranked | ap=stephanocol* | class=small | mid=25.0µm
  - `eruca_sativa` | *Eruca sativa* | unranked | ap=stephanocol* | class=small | mid=23.5µm | sc={reticulaat}
  - `fraxinus_ornus` | *Fraxinus ornus* | unranked | ap=stephanocol* | class=small | mid=22.0µm | sc={microreticulaat,reticulaat}
- Closest pair evidence `citrus_sinensis`–`eruca_sativa` (d=1.285): `{'aperture': 'same stephanocol*', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.285}`
- Provenance (sample): `citrus_sinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eruca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fraxinus_ornus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C97 (n=3, mean_d=1.165, max_d=1.285)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (28.5, 30.0)
- Shared sculpture tokens: —
- Members:
  - `coffea_typ` | *Coffea typ* | unranked | ap=stephanocol* | class=medium | mid=28.5µm | sc={scabraat}
  - `mentha_pulegium` | *Mentha pulegium* | unranked | ap=stephanocol* | class=medium | mid=29.2µm
  - `symphytum_off` | *Symphytum off* | unranked | ap=stephanocol* | class=medium | mid=30.0µm
- Closest pair evidence `coffea_typ`–`mentha_pulegium` (d=1.093): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.093}`
- Provenance (sample): `coffea_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mentha_pulegium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `symphytum_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C98 (n=3, mean_d=1.197, max_d=1.333)

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.5, 38.1)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `consolida_regalis` | *Consolida regalis* | unranked | ap=tricol* | class=medium | mid=38.1µm | sc={psilaat}
  - `veronica_chamaedrys` | *Veronica chamaedrys* | unranked | ap=tricol* | class=medium | mid=36.9µm | sc={psilaat}
  - `viola_reichenbachiana` | *Viola reichenbachiana* | unranked | ap=tricol* | class=medium | mid=36.5µm | sc={psilaat}
- Closest pair evidence `veronica_chamaedrys`–`viola_reichenbachiana` (d=1.033): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.033}`
- Provenance (sample): `consolida_regalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_chamaedrys`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viola_reichenbachiana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C99 (n=3, mean_d=1.495, max_d=1.745)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: echinaat, microreticulaat, reticulaat, scabraat
- Members:
  - `convolvulus_arvensis` | *Convolvulus arvensis* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microechinaat,microreticulaat,psilaat,reticulaat}
  - `olea_europaea` | *Olea europaea* | unranked | ap=tricol* | size_MASKED | sc={echinaat,microreticulaat,reticulaat,scabraat}
  - `papaver_rhoeas` | *Papaver rhoeas* | unranked | ap=tricol* | class=medium | mid=26.0µm | sc={echinaat,microechinaat,microreticulaat,reticulaat,scabraat}
- Closest pair evidence `convolvulus_arvensis`–`papaver_rhoeas` (d=1.345): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.167, 'shared': ['echinaat', 'microechinaat', 'microreticulaat', 'reticulaat', 'scabraat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.345}`
- Provenance (sample): `convolvulus_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `olea_europaea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `papaver_rhoeas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C100 (n=3, mean_d=1.182, max_d=1.649)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.5, 31.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `corylopsis_spicata` | *Corylopsis spicata* | unranked | ap=tricol* | class=medium | mid=31.6µm | sc={reticulaat}
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | sc={reticulaat}
- Closest pair evidence `gleditsia_triacanthos`–`trifolium_arvense` (d=0.937): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `corylopsis_spicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `gleditsia_triacanthos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C101 (n=3, mean_d=1.082, max_d=1.161)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.8, 29.9)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cotoneaster_niger` | *Cotoneaster niger* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={psilaat,striaat}
  - `levisticum_officinale` | *Levisticum officinale* | unranked | ap=tricol* | class=medium | mid=29.9µm | sc={psilaat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | sc={psilaat}
- Closest pair evidence `levisticum_officinale`–`solanum_nigrum_ssp_nigrum` (d=0.961): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `cotoneaster_niger`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `levisticum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `solanum_nigrum_ssp_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C102 (n=3, mean_d=0.920, max_d=1.095)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.9, 42.7)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | sc={rugulaat,striaat}
  - `prunus_avium` | *Prunus avium* | unranked | ap=tricol* | size_MASKED | sc={rugulaat,striaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | sc={rugulaat,striaat}
- Closest pair evidence `crataegus_monogyna`–`prunus_spinosa` (d=0.819): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.819}`
- Provenance (sample): `crataegus_monogyna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_avium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C103 (n=3, mean_d=1.275, max_d=1.725)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.5, 43.0)
- Shared sculpture tokens: verrucaat
- **Human review (species↔*_typ):** rhododendron_ponticum ↔ rhododendron_typ
- Members:
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | sc={verrucaat}
  - `rhododendron_ponticum` | *Rhododendron ponticum* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={verrucaat}
  - `rhododendron_typ` | *Rhododendron typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | sc={echinaat,verrucaat}
- Closest pair evidence `euphorbia_typ`–`rhododendron_ponticum` (d=0.975): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `euphorbia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhododendron_ponticum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `rhododendron_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C104 (n=3, mean_d=1.524, max_d=1.680)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.6, 41.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `euphrasia_stricta` | *Euphrasia stricta* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={psilaat}
  - `nigella_arvensis` | *Nigella arvensis* | unranked | ap=tricol* | class=medium | mid=40.4µm | sc={echinaat,microechinaat,psilaat,scabraat}
  - `veronica_austriaca_ssp_teucrium` | *Veronica austriaca* | unranked | ap=tricol* | class=medium | mid=39.6µm | sc={psilaat}
- Closest pair evidence `euphrasia_stricta`–`veronica_austriaca_ssp_teucrium` (d=1.249): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.249}`
- Provenance (sample): `euphrasia_stricta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `nigella_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_austriaca_ssp_teucrium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C105 (n=3, mean_d=0.782, max_d=0.985)

- Shared aperture: monocol*
- Size classes: large; mid range: (56.8, 57.0)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=monocol* | class=large | mid=57.0µm | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=monocol* | class=large | mid=57.0µm | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same monocol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C106 (n=3, mean_d=1.368, max_d=1.489)

- Shared aperture: monocol*
- Size classes: medium; mid range: (29.1, 31.5)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** muscari_botryoides ↔ muscari_typ
- Members:
  - `galanthus_nivalis` | *Galanthus nivalis* | unranked | ap=monocol* | class=medium | mid=29.1µm
  - `muscari_botryoides` | *Muscari botryoides* | unranked | ap=monocol* | class=medium | mid=31.5µm | sc={reticulaat}
  - `muscari_typ` | *Muscari typ* | unranked | ap=monocol* | class=medium | mid=30.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `galanthus_nivalis`–`muscari_typ` (d=1.129): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.85, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.129}`
- Provenance (sample): `galanthus_nivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `muscari_botryoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `muscari_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C107 (n=3, mean_d=1.105, max_d=1.595)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (17.0, 20.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `galium_odoratum` | *Galium odoratum (syn Asperula odorata)* | unranked | ap=stephanocol* | class=small | mid=20.0µm | sc={reticulaat,scabraat}
  - `galium_sylvatica` | *Galium sylvatica* | unranked | ap=stephanocol* | class=small | mid=17.0µm | sc={reticulaat}
  - `primula_vulgaris` | *Primula vulgaris* | unranked | ap=stephanocol* | class=small | mid=18.5µm | sc={reticulaat}
- Closest pair evidence `galium_sylvatica`–`primula_vulgaris` (d=0.485): `{'aperture': 'same stephanocol*', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.485}`
- Provenance (sample): `galium_odoratum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `galium_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `primula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C108 (n=3, mean_d=1.255, max_d=1.695)

- Shared aperture: tricol*
- Size classes: large; mid range: (55.0, 60.5)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_dissectum` | *Geranium dissectum* | unranked | ap=tricol* | class=large | mid=55.0µm | sc={clavaat}
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | sc={clavaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | sc={clavaat}
- Closest pair evidence `geranium_molle`–`linum_flavum` (d=0.927): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 2.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.927}`
- Provenance (sample): `geranium_dissectum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_molle`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `linum_flavum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C109 (n=3, mean_d=0.802, max_d=1.141)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 31.1)
- Shared sculpture tokens: microreticulaat, reticulaat
- Members:
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=29.0µm | sc={microreticulaat,reticulaat}
  - `viola_odorata` | *Viola odorata* | unranked | ap=tricol* | class=medium | mid=31.1µm | sc={microreticulaat,psilaat,reticulaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=30.3µm | sc={microreticulaat,reticulaat}
- Closest pair evidence `helleborus_foetidus`–`vitex_agnus_castus` (d=0.437): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.437}`
- Provenance (sample): `helleborus_foetidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viola_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vitex_agnus_castus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C110 (n=3, mean_d=0.765, max_d=1.085)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 25.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
  - `punica_granatum` | *Punica granatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={scabraat}
  - `xanthium_italicum` | *Xanthium italicum* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={scabraat}
- Closest pair evidence `hippopha_rhamn`–`xanthium_italicum` (d=0.605): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.605}`
- Provenance (sample): `hippopha_rhamn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `punica_granatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `xanthium_italicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C111 (n=3, mean_d=1.077, max_d=1.153)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.1, 23.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hypericum_montanum` | *Hypericum montanum* | unranked | ap=tricol* | class=medium | mid=22.6µm | sc={reticulaat}
  - `koelreuteria_paniculata` | *Koelreuteria paniculata* | unranked | ap=tricol* | class=medium | mid=23.0µm | sc={reticulaat}
  - `lysimachia_nemorum` | *Lysimachia nemorum* | unranked | ap=tricol* | class=medium | mid=22.1µm | sc={reticulaat}
- Closest pair evidence `hypericum_montanum`–`koelreuteria_paniculata` (d=1.033): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.033}`
- Provenance (sample): `hypericum_montanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `koelreuteria_paniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lysimachia_nemorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C112 (n=3, mean_d=0.952, max_d=1.365)

- Shared aperture: tripor*
- Size classes: small; mid range: (15.5, 19.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** urtica_dioica ↔ urtica_typ
- Members:
  - `morus_alba` | *Morus alba* | unranked | ap=tripor* | class=small | mid=19.0µm | sc={psilaat}
  - `urtica_dioica` | *Urtica dioica* | unranked | ap=tripor* | class=small | mid=15.5µm | sc={psilaat}
  - `urtica_typ` | *Urtica typ* | unranked | ap=tripor* | class=small | mid=16.0µm | sc={psilaat}
- Closest pair evidence `urtica_dioica`–`urtica_typ` (d=0.645): `{'aperture': 'same tripor*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.645}`
- Provenance (sample): `morus_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `urtica_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `urtica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C113 (n=3, mean_d=1.135, max_d=1.245)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.0, 23.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `onosis_spinoza` | *Ononis spinosa* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={psilaat}
  - `prunus_serotina` | *Prunus serotina* | unranked | ap=tricol* | class=small | mid=23.0µm | sc={psilaat}
  - `vitis_vinifera` | *Vitis vinifera* | unranked | ap=tricol* | class=small | mid=22.0µm | sc={psilaat,scabraat}
- Closest pair evidence `onosis_spinoza`–`prunus_serotina` (d=1.045): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `onosis_spinoza`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_serotina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vitis_vinifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C114 (n=3, mean_d=1.640, max_d=1.704)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 28.1)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `pterostyrax_hispida` | *Pterostyrax hispida* | unranked | ap=tricol* | class=medium | mid=27.2µm | sc={psilaat}
  - `verbena_officinalis` | *Verbena officinalis* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={psilaat,rugulaat,scabraat,verrucaat}
  - `xanthium_strumarium` | *Xanthium strumarium* | unranked | ap=tricol* | class=medium | mid=28.1µm | sc={microechinaat,psilaat,reticulaat,scabraat}
- Closest pair evidence `pterostyrax_hispida`–`verbena_officinalis` (d=1.560): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.75, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.56}`
- Provenance (sample): `pterostyrax_hispida`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `verbena_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `xanthium_strumarium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C115 (n=3, mean_d=1.197, max_d=1.620)

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 33.5)
- Shared sculpture tokens: —
- Members:
  - `ribes_sanguineum` | *Ribes sanguineum* | unranked | ap=peripor* | class=medium | mid=33.0µm | sc={psilaat,scabraat}
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm
  - `ulmus_typ` | *Ulmus typ* | unranked | ap=peripor* | class=medium | mid=33.5µm | sc={reticulaat,rugulaat,scabraat}
- Closest pair evidence `ribes_sanguineum`–`ribes_uva_crispa` (d=0.925): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `ribes_sanguineum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_uva_crispa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ulmus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C116 (n=3, mean_d=1.375, max_d=1.625)

- Shared aperture: tricol*
- Size classes: large; mid range: (80.0, 80.0)
- Shared sculpture tokens: —
- Members:
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat}
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={echinaat,striaat}
  - `vinca_typ` | *Vinca typ* | unranked | ap=tricol* | class=large | mid=80.0µm | sc={psilaat}
- Closest pair evidence `succisa_praten`–`succisa_pratensis` (d=0.875): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.875}`
- Provenance (sample): `succisa_praten`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `succisa_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vinca_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C117 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same peripor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C118 (n=2, mean_d=1.679, max_d=1.679)

- Shared aperture: tricol*
- Size classes: large; mid range: (55.1, 56.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `acanthus_mollis` | *Acanthus mollis* | unranked | ap=tricol* | class=large | mid=55.1µm | sc={reticulaat}
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | sc={reticulaat}
- Closest pair evidence `acanthus_mollis`–`citrullus_lanatus` (d=1.679): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': {'jaccard_dist': 1.0, 'shared': []}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.679}`
- Provenance (sample): `acanthus_mollis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `citrullus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C119 (n=2, mean_d=1.395, max_d=1.395)

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.0, 37.5)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `acer_pseudoplatanus` | *Acer pseudoplatanus* | unranked | ap=tricol* | class=medium | mid=37.5µm | sc={rugulaat,striaat,verrucaat}
  - `rhinanthus_alectorolophus` | *Rhinanthus alectorolophus* | unranked | ap=tricol* | class=medium | mid=37.0µm | sc={rugulaat,scabraat,striaat}
- Closest pair evidence `acer_pseudoplatanus`–`rhinanthus_alectorolophus` (d=1.395): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.5, 'shared': ['driehoekig', 'oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.395}`
- Provenance (sample): `acer_pseudoplatanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhinanthus_alectorolophus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C120 (n=2, mean_d=1.595, max_d=1.595)

- Shared aperture: monocol*
- Size classes: large; mid range: (75.0, 75.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `agave_striata` | *Agave striata* | unranked | ap=monocol* | class=large | mid=75.0µm | sc={reticulaat,rugulaat}
  - `liriodendron_tulipifera` | *Liriodendron tulipifera* | unranked | ap=monocol* | size_MASKED | sc={reticulaat,rugulaat,verrucaat}
- Closest pair evidence `agave_striata`–`liriodendron_tulipifera` (d=1.595): `{'aperture': 'same monocol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.595}`
- Provenance (sample): `agave_striata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `liriodendron_tulipifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C121 (n=2, mean_d=0.920, max_d=0.920)

- Shared aperture: tricol*
- Size classes: large; mid range: (75.0, 75.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | sculpt_MASKED
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | sc={reticulaat}
- Closest pair evidence `agrimonia_odorata`–`geranium_typ` (d=0.920): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.92}`
- Provenance (sample): `agrimonia_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `geranium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C122 (n=2, mean_d=1.725, max_d=1.725)

- Shared aperture: tricol*
- Size classes: small; mid range: (13.0, 13.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `alchemilla_acutiloba` | *Alchemilla acutiloba* | unranked | ap=tricol* | sc={psilaat}
  - `cynoglossum_officinale` | *Cynoglossum officinale* | unranked | ap=tricol* | class=small | mid=13.0µm | sc={psilaat}
- Closest pair evidence `alchemilla_acutiloba`–`cynoglossum_officinale` (d=1.725): `{'aperture': 'same tricol*', 'size': 'missing_one_or_both', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['driehoekig']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.725}`
- Provenance (sample): `alchemilla_acutiloba`: eide:docs/keys/eide/rosaceae-eide.json · `cynoglossum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C123 (n=2, mean_d=1.069, max_d=1.069)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.9, 24.6)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `alchemilla_alpina` | *Alchemilla alpina* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={psilaat}
  - `veronica_arvensis` | *Veronica arvensis* | unranked | ap=tricol* | class=medium | mid=24.6µm | sc={psilaat}
- Closest pair evidence `alchemilla_alpina`–`veronica_arvensis` (d=1.069): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.069}`
- Provenance (sample): `alchemilla_alpina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C124 (n=2, mean_d=1.009, max_d=1.009)

- Shared aperture: peripor*
- Size classes: medium; mid range: (25.1, 25.4)
- Shared sculpture tokens: —
- Members:
  - `alisma_lanceolatum` | *Alisma lanceolatum* | unranked | ap=peripor* | class=medium | mid=25.4µm
  - `plantago_lanceolata` | *Plantago Lanceolata* | unranked | ap=peripor* | class=medium | mid=25.1µm | sc={verrucaat}
- Closest pair evidence `alisma_lanceolatum`–`plantago_lanceolata` (d=1.009): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.009}`
- Provenance (sample): `alisma_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `plantago_lanceolata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-plantaginaceae.json

### C125 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: monocol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `allium_cepa` | *Allium cepa* | unranked | ap=monocol* | class=medium | mid=28.0µm | sc={psilaat,scabraat}
  - `allium_schoenoprasum` | *Allium schoenoprasum* | unranked | ap=monocol* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
- Closest pair evidence `allium_cepa`–`allium_schoenoprasum` (d=0.605): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `allium_cepa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `allium_schoenoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C126 (n=2, mean_d=1.737, max_d=1.737)

- Shared aperture: monocol*
- Size classes: large, medium; mid range: (36.1, 36.2)
- Shared sculpture tokens: —
- Members:
  - `allium_fistulosum` | *Allium fistulosum* | unranked | ap=monocol* | class=medium | mid=36.2µm
  - `polygonatum_odoratum` | *Polygonatum odoratum* | unranked | ap=monocol* | class=large | mid=36.1µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `allium_fistulosum`–`polygonatum_odoratum` (d=1.737): `{'aperture': 'same monocol*', 'size_class': 'adjacent medium/large', 'size_mid_gap_um': 0.05, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.737}`
- Provenance (sample): `allium_fistulosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `polygonatum_odoratum`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug09-monocolpatae.json

### C127 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: monocol*
- Size classes: medium; mid range: (43.9, 44.0)
- Shared sculpture tokens: —
- Members:
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.949): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tradescantia_andersoniana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C128 (n=2, mean_d=0.845, max_d=0.845)

- Shared aperture: peripor*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `alnus_glutinosa` | *Alnus glutinosa* | unranked | ap=peripor* | class=medium | mid=26.0µm | sc={psilaat,scabraat}
  - `carpinus_betulus` | *Carpinus betulus* | unranked | ap=peripor* | size_MASKED | sc={psilaat,scabraat}
- Closest pair evidence `alnus_glutinosa`–`carpinus_betulus` (d=0.845): `{'aperture': 'same peripor*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same stephanopor', 'shape': {'jaccard_dist': 0.0, 'shared': ['oblaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.845}`
- Provenance (sample): `alnus_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpinus_betulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C129 (n=2, mean_d=1.155, max_d=1.155)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: —
- Members:
  - `anemone_typ` | *Anemone typ* | unranked | ap=stephanocol* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `ceratonia_silqua` | *Ceratonia silqua* | unranked | ap=stephanocol* | class=medium | mid=26.0µm
- Closest pair evidence `anemone_typ`–`ceratonia_silqua` (d=1.155): `{'aperture': 'same stephanocol*', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.155}`
- Provenance (sample): `anemone_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ceratonia_silqua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C130 (n=2, mean_d=1.389, max_d=1.389)

- Shared aperture: tricol*
- Size classes: medium; mid range: (19.1, 20.2)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `anthriscus_cerefolium` | *Anthriscus cerefolium* | unranked | ap=tricol* | class=medium | mid=20.2µm | sc={psilaat}
  - `nicandra_physalodes` | *Nicandra physalodes* | unranked | ap=tricol* | class=medium | mid=19.1µm | sc={psilaat,scabraat}
- Closest pair evidence `anthriscus_cerefolium`–`nicandra_physalodes` (d=1.389): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.1, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.389}`
- Provenance (sample): `anthriscus_cerefolium`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `nicandra_physalodes`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size

### C131 (n=2, mean_d=1.647, max_d=1.647)

- Shared aperture: tricol*
- Size classes: large; mid range: (42.6, 44.1)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `anthyllis_vulneraria` | *Anthyllis vulneraria* | unranked | ap=tricol* | class=large | mid=44.1µm | sc={psilaat,rugulaat,scabraat,verrucaat}
  - `elaeagnus_angustifolia` | *Elaeagnus angustifolia* | unranked | ap=tricol* | class=large | mid=42.6µm | sc={psilaat,scabraat}
- Closest pair evidence `anthyllis_vulneraria`–`elaeagnus_angustifolia` (d=1.647): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.55, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.5, 'shared': ['driehoekig', 'oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.647}`
- Provenance (sample): `anthyllis_vulneraria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `elaeagnus_angustifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C132 (n=2, mean_d=0.392, max_d=0.392)

- Shared aperture: tricol*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** arbutus_unedo ↔ arbutus_typ
- Members:
  - `arbutus_typ` | *Arbutus typ* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
  - `arbutus_unedo` | *Arbutus unedo* | unranked | ap=tricol* | class=medium | mid=50.0µm | sc={psilaat}
- Closest pair evidence `arbutus_typ`–`arbutus_unedo` (d=0.392): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.333, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.3917}`
- Provenance (sample): `arbutus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arbutus_unedo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C133 (n=2, mean_d=1.125, max_d=1.125)

- Shared aperture: tripor*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_lappa` | *Arctium lappa* | unranked | ap=tripor* | class=medium | mid=50.0µm | sc={echinaat,verrucaat}
  - `arcticum_majus` | *Arcticum majus* | unranked | ap=tripor* | class=medium | mid=50.0µm | sc={echinaat}
- Closest pair evidence `arcticum_lappa`–`arcticum_majus` (d=1.125): `{'aperture': 'same tripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `arcticum_lappa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arcticum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C134 (n=2, mean_d=1.645, max_d=1.645)

- Shared aperture: tricol*
- Size classes: small; mid range: (16.0, 19.0)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `aruncus_dioicus` | *Aruncus dioicus* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={rugulaat,striaat}
  - `sedum_acre` | *Sedum acre* | unranked | ap=tricol* | class=small | mid=19.0µm | sc={rugulaat,striaat}
- Closest pair evidence `aruncus_dioicus`–`sedum_acre` (d=1.645): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 1.0, 'shared': []}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.645}`
- Provenance (sample): `aruncus_dioicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sedum_acre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C135 (n=2, mean_d=1.009, max_d=1.009)

- Shared aperture: tripor*
- Size classes: medium; mid range: (24.1, 24.5)
- Shared sculpture tokens: —
- Members:
  - `betula_nigra` | *Betula nigra* | unranked | ap=tripor* | class=medium | mid=24.5µm | sc={psilaat}
  - `humulus_lupulus` | *Humulus lupulus* | unranked | ap=tripor* | class=medium | mid=24.1µm
- Closest pair evidence `betula_nigra`–`humulus_lupulus` (d=1.009): `{'aperture': 'same tripor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same tripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.009}`
- Provenance (sample): `betula_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `humulus_lupulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C136 (n=2, mean_d=1.521, max_d=1.521)

- Shared aperture: tripor*
- Size classes: medium; mid range: (27.0, 28.6)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `betula_pendula` | *Betula pendula* | unranked | ap=tripor* | class=medium | mid=28.6µm | sc={reticulaat,scabraat}
  - `corylus_avellana` | *Corylus avellana* | unranked | ap=tripor* | class=medium | mid=27.0µm | sc={psilaat,scabraat}
- Closest pair evidence `betula_pendula`–`corylus_avellana` (d=1.521): `{'aperture': 'same tripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.65, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['scabraat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.521}`
- Provenance (sample): `betula_pendula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylus_avellana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C137 (n=2, mean_d=1.237, max_d=1.237)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (42.2, 43.5)
- Shared sculpture tokens: —
- Members:
  - `campanula_medium` | *Campanula medium* | unranked | ap=stephanopor* | class=medium | mid=42.2µm | sc={echinaat,microechinaat}
  - `campanula_rapunculoides` | *Campanula rapunculoides* | unranked | ap=stephanopor* | class=medium | mid=43.5µm
- Closest pair evidence `campanula_medium`–`campanula_rapunculoides` (d=1.237): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.3, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.237}`
- Provenance (sample): `campanula_medium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-medium.json · `campanula_rapunculoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C138 (n=2, mean_d=1.045, max_d=1.045)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (38.5, 39.0)
- Shared sculpture tokens: —
- Members:
  - `campanula_persicifolia` | *Campanula persicifolia* | unranked | ap=stephanopor* | class=medium | mid=38.5µm
  - `juglans_regia` | *Juglans regia* | unranked | ap=stephanopor* | class=medium | mid=39.0µm | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `campanula_persicifolia`–`juglans_regia` (d=1.045): `{'aperture': 'same stephanopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `campanula_persicifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `juglans_regia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C139 (n=2, mean_d=1.525, max_d=1.525)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 25.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `caragana_arborescens` | *Caragana arborescens* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={scabraat}
  - `foeniculum_vulga` | *Foeniculum vulga* | unranked | ap=tricol* | class=small | mid=25.0µm | sc={scabraat}
- Closest pair evidence `caragana_arborescens`–`foeniculum_vulga` (d=1.525): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat']}, 'coarse_sculpt_penalty': 'scabraat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.525}`
- Provenance (sample): `caragana_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulga`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C140 (n=2, mean_d=1.117, max_d=1.117)

- Shared aperture: tetrade*
- Size classes: large; mid range: (71.0, 71.8)
- Shared sculpture tokens: —
- Members:
  - `catalpa_bignonioides` | *Catalpa bignonioides* | unranked | ap=tetrade* | class=large | mid=71.0µm
  - `listera_cordata` | *Listera cordata* | unranked | ap=tetrade* | class=large | mid=71.8µm | sc={reticulaat,striaat}
- Closest pair evidence `catalpa_bignonioides`–`listera_cordata` (d=1.117): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.8, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.117}`
- Provenance (sample): `catalpa_bignonioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `listera_cordata`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-epipactis.json

### C141 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | sc={psilaat,rugulaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.125): `{'aperture': 'same tripor*', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'rugulaat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C142 (n=2, mean_d=1.320, max_d=1.320)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 27.8)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat
- Members:
  - `chelidonium_majus` | *Chelidonium majus* | unranked | ap=tricol* | class=medium | mid=27.0µm | sc={microreticulaat,psilaat,reticulaat,scabraat}
  - `lamium_album` | *Lamium album* | unranked | ap=tricol* | class=medium | mid=27.8µm | sc={microreticulaat,psilaat,reticulaat}
- Closest pair evidence `chelidonium_majus`–`lamium_album` (d=1.320): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.75, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.8, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.32}`
- Provenance (sample): `chelidonium_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lamium_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C143 (n=2, mean_d=1.202, max_d=1.202)

- Shared aperture: porate*
- Size classes: medium; mid range: (28.0, 30.3)
- Shared sculpture tokens: —
- Members:
  - `chenopodium_album` | *Chenopodium album* | unranked | ap=porate* | class=medium | mid=28.0µm | sc={reticulaat,scabraat}
  - `sanguisorba_officinalis` | *Sanguisorba officinalis* | unranked | ap=porate* | class=medium | mid=30.3µm | sculpt_MASKED
- Closest pair evidence `chenopodium_album`–`sanguisorba_officinalis` (d=1.202): `{'aperture': 'same porate*', 'size_class': 'same medium', 'size_mid_gap_um': 2.3, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.202}`
- Provenance (sample): `chenopodium_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sanguisorba_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C144 (n=2, mean_d=1.309, max_d=1.309)

- Shared aperture: tricol*
- Size classes: large; mid range: (49.4, 51.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `cistus_incanus` | *Cistus incanus* | unranked | ap=tricol* | class=large | mid=49.4µm | sc={reticulaat}
  - `fagopyrum_esculentum` | *Fagopyrum esculentum* | unranked | ap=tricol* | class=large | mid=51.0µm | sc={reticulaat}
- Closest pair evidence `cistus_incanus`–`fagopyrum_esculentum` (d=1.309): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.309}`
- Provenance (sample): `cistus_incanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `fagopyrum_esculentum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C145 (n=2, mean_d=1.271, max_d=1.271)

- Shared aperture: tricol*
- Size classes: medium, small; mid range: (22.8, 23.1)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `clematis_recta` | *Clematis recta* | unranked | ap=tricol* | class=small | mid=22.8µm | sc={scabraat,verrucaat}
  - `melampyrum_pratense` | *Melampyrum pratense* | unranked | ap=tricol* | class=medium | mid=23.1µm | sc={scabraat,verrucaat}
- Closest pair evidence `clematis_recta`–`melampyrum_pratense` (d=1.271): `{'aperture': 'same tricol*', 'size_class': 'adjacent small/medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.271}`
- Provenance (sample): `clematis_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C146 (n=2, mean_d=1.745, max_d=1.745)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 31.0)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `coriandrum_sativum` | *Coriandrum sativum* | unranked | ap=tricol* | size_MASKED | sc={reticulaat,scabraat,verrucaat}
  - `teucrium_chamaedrys` | *Teucrium chamaedrys* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={scabraat,verrucaat}
- Closest pair evidence `coriandrum_sativum`–`teucrium_chamaedrys` (d=1.745): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.333, 'shared': ['scabraat', 'verrucaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.5, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.745}`
- Provenance (sample): `coriandrum_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `teucrium_chamaedrys`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C147 (n=2, mean_d=1.746, max_d=1.746)

- Shared aperture: pericol*
- Size classes: medium; mid range: (33.8, 35.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `corydalis_cava` | *Corydalis cava* | unranked | ap=pericol* | class=medium | mid=35.0µm | sc={reticulaat,rugulaat,verrucaat}
  - `spergula_arvensis` | *Spergula arvensis* | unranked | ap=pericol* | class=medium | mid=33.8µm | sc={echinaat,microechinaat,psilaat,reticulaat,rugulaat}
- Closest pair evidence `corydalis_cava`–`spergula_arvensis` (d=1.746): `{'aperture': 'same pericol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.714, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same pericol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.7464}`
- Provenance (sample): `corydalis_cava`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spergula_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C148 (n=2, mean_d=1.441, max_d=1.441)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (9.5, 11.7)
- Shared sculpture tokens: —
- Members:
  - `cynoglossum_creticum` | *Cynoglossum creticum* | unranked | ap=heterocol* | class=very-small | mid=9.5µm
  - `myosotis_ramosissima` | *Myosotis ramosissima* | unranked | ap=heterocol* | class=very-small | mid=11.7µm
- Closest pair evidence `cynoglossum_creticum`–`myosotis_ramosissima` (d=1.441): `{'aperture': 'same heterocol*', 'size_class': 'same very-small', 'size_mid_gap_um': 2.15, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same heterocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.441}`
- Provenance (sample): `cynoglossum_creticum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_ramosissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C149 (n=2, mean_d=1.575, max_d=1.575)

- Shared aperture: fenestr*
- Size classes: large; mid range: (80.5, 80.5)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_typ` | *Dipsacus typ* | unranked | ap=fenestr* | class=large | mid=80.5µm | sc={echinaat}
  - `helenium_autumnale` | *Helenium autumnale* | unranked | ap=fenestr* | sc={echinaat}
- Closest pair evidence `dipsacus_typ`–`helenium_autumnale` (d=1.575): `{'aperture': 'same fenestr*', 'size': 'missing_one_or_both', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.575}`
- Provenance (sample): `dipsacus_typ`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `helenium_autumnale`: kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json; kerkvliet:analytic (not dichotomous source)

### C150 (n=2, mean_d=1.625, max_d=1.625)

- Shared aperture: tricol*
- Size classes: medium; mid range: (45.0, 45.0)
- Shared sculpture tokens: —
- Members:
  - `eleagnus_angustif` | *Eleagnus angustif* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={psilaat}
  - `mespilus_germani` | *Mespilus germani* | unranked | ap=tricol* | class=medium | mid=45.0µm | sc={scabraat,striaat}
- Closest pair evidence `eleagnus_angustif`–`mespilus_germani` (d=1.625): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 1.0, 'shared': []}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.625}`
- Provenance (sample): `eleagnus_angustif`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mespilus_germani`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C151 (n=2, mean_d=1.595, max_d=1.595)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.9, 23.9)
- Shared sculpture tokens: echinaat, psilaat, scabraat
- Members:
  - `eranthis_hyemalis` | *Eranthis hyemalis* | unranked | ap=tricol* | class=medium | mid=23.9µm | sc={echinaat,microechinaat,psilaat,scabraat}
  - `rubus_chamaemorus` | *Rubus chamaemorus* | unranked | ap=tricol* | size_MASKED | sc={clavaat,echinaat,psilaat,scabraat,striaat}
- Closest pair evidence `eranthis_hyemalis`–`rubus_chamaemorus` (d=1.595): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.595}`
- Provenance (sample): `eranthis_hyemalis`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size · `rubus_chamaemorus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug16-ttt-clav.json

### C152 (n=2, mean_d=1.305, max_d=1.305)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.8)
- Shared sculpture tokens: verrucaat
- Members:
  - `erica_arborea` | *Erica arborea* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={verrucaat}
  - `ranunculus_bulbosus` | *Ranunculus bulbosus* | unranked | ap=tricol* | class=medium | mid=30.8µm | sc={baculaat,verrucaat}
- Closest pair evidence `erica_arborea`–`ranunculus_bulbosus` (d=1.305): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.75, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.305}`
- Provenance (sample): `erica_arborea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_bulbosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C153 (n=2, mean_d=1.695, max_d=1.695)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.0, 41.0)
- Shared sculpture tokens: reticulaat, rugulaat, scabraat
- Members:
  - `fagus_sylvatica` | *Fagus sylvatica* | unranked | ap=tricol* | class=medium | mid=41.0µm | sc={reticulaat,rugulaat,scabraat}
  - `robinia_pseudoacacia` | *Robinia pseudoacacia* | unranked | ap=tricol* | size_MASKED | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `fagus_sylvatica`–`robinia_pseudoacacia` (d=1.695): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.4, 'shared': ['reticulaat', 'rugulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.695}`
- Provenance (sample): `fagus_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `robinia_pseudoacacia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C154 (n=2, mean_d=1.095, max_d=1.095)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.5, 26.5)
- Shared sculpture tokens: rugulaat, scabraat
- Members:
  - `ferula_communis` | *Ferula communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | sc={rugulaat,scabraat}
  - `tordylium_apulum` | *Tordylium apulum* | unranked | ap=tricol* | size_MASKED | sc={rugulaat,scabraat}
- Closest pair evidence `ferula_communis`–`tordylium_apulum` (d=1.095): `{'aperture': 'same tricol*', 'size': 'masked_conflict', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.095}`
- Provenance (sample): `ferula_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tordylium_apulum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C155 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: tricol*
- Size classes: small; mid range: (14.0, 16.0)
- Shared sculpture tokens: clavaat, echinaat, microechinaat, psilaat, scabraat
- Members:
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | sc={clavaat,echinaat,microechinaat,psilaat,scabraat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | sc={clavaat,echinaat,microechinaat,psilaat,scabraat}
- Closest pair evidence `filipendula_ulmaria`–`filipendula_vulgaris` (d=0.605): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat', 'echinaat', 'microechinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `filipendula_ulmaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C156 (n=2, mean_d=1.509, max_d=1.509)

- Shared aperture: peripor*
- Size classes: medium; mid range: (37.4, 39.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `fumaria_officinalis` | *Fumaria officinalis* | unranked | ap=peripor* | class=medium | mid=39.0µm | sc={psilaat}
  - `scirpus_sylvaticus` | *Scirpus sylvaticus* | unranked | ap=peripor* | class=medium | mid=37.4µm | sc={psilaat,scabraat}
- Closest pair evidence `fumaria_officinalis`–`scirpus_sylvaticus` (d=1.509): `{'aperture': 'same peripor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.6, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.509}`
- Provenance (sample): `fumaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scirpus_sylvaticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C157 (n=2, mean_d=0.675, max_d=0.675)

- Shared aperture: tricol*
- Size classes: large; mid range: (78.3, 79.6)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | sc={clavaat}
- Closest pair evidence `geranium_nodosum`–`geranium_phaeum` (d=0.675): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.675}`
- Provenance (sample): `geranium_nodosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_phaeum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C158 (n=2, mean_d=1.735, max_d=1.735)

- Shared aperture: tricol*
- Size classes: large; mid range: (64.8, 66.2)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_pyrenaicum` | *Geranium pyrenaicum* | unranked | ap=tricol* | class=large | mid=64.8µm | sc={clavaat}
  - `geranium_robertianum` | *Geranium robertianum* | unranked | ap=tricol* | class=large | mid=66.2µm | sc={clavaat,rugulaat,striaat}
- Closest pair evidence `geranium_pyrenaicum`–`geranium_robertianum` (d=1.735): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.735}`
- Provenance (sample): `geranium_pyrenaicum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_robertianum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C159 (n=2, mean_d=1.335, max_d=1.335)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.5, 40.0)
- Shared sculpture tokens: reticulaat, scabraat, verrucaat
- Members:
  - `heracleum_sphondylium` | *Heracleum sphondylium* | unranked | ap=tricol* | class=medium | mid=38.5µm | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `pastinaca_sativa` | *Pastinaca sativa* | unranked | ap=tricol* | class=medium | mid=40.0µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `heracleum_sphondylium`–`pastinaca_sativa` (d=1.335): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.4, 'shared': ['reticulaat', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.335}`
- Provenance (sample): `heracleum_sphondylium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pastinaca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C160 (n=2, mean_d=1.125, max_d=1.125)

- Shared aperture: monocol*
- Size classes: medium; mid range: (45.0, 45.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hyacinthus_orientalis` | *Hyacinthus orientalis* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat}
  - `narcissus_typ` | *Narcissus typ* | unranked | ap=monocol* | class=medium | mid=45.0µm | sc={reticulaat,scabraat}
- Closest pair evidence `hyacinthus_orientalis`–`narcissus_typ` (d=1.125): `{'aperture': 'same monocol*', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `hyacinthus_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `narcissus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C161 (n=2, mean_d=1.225, max_d=1.225)

- Shared aperture: tricol*
- Size classes: very-small; mid range: (11.2, 12.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `hydrangea_typ` | *Hydrangea typ* | unranked | ap=tricol* | class=very-small | mid=11.2µm | sc={psilaat}
  - `spiraea_japonica` | *Spiraea japonica* | unranked | ap=tricol* | class=very-small | mid=12.5µm | sc={psilaat}
- Closest pair evidence `hydrangea_typ`–`spiraea_japonica` (d=1.225): `{'aperture': 'same tricol*', 'size_class': 'same very-small', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.225}`
- Provenance (sample): `hydrangea_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spiraea_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C162 (n=2, mean_d=1.025, max_d=1.025)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.0)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `hypericum_perforatum` | *Hypericum perforatum* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={microreticulaat,psilaat,reticulaat}
  - `sambucus_ebulus` | *Sambucus ebulus* | unranked | ap=tricol* | class=small | mid=21.0µm | sc={psilaat,reticulaat}
- Closest pair evidence `hypericum_perforatum`–`sambucus_ebulus` (d=1.025): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.025}`
- Provenance (sample): `hypericum_perforatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sambucus_ebulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C163 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: inapert*
- Size classes: very-small; mid range: (1.0, 1.0)
- Shared sculpture tokens: —
- Members:
  - `juncus_jacquinii` | *Juncus jacquinii* | unranked | ap=inapert* | class=very-small | mid=1.0µm
  - `luzula_sylvatica` | *Luzula sylvatica* | unranked | ap=inapert* | class=very-small | mid=1.0µm
- Closest pair evidence `juncus_jacquinii`–`luzula_sylvatica` (d=0.925): `{'aperture': 'same inapert*', 'size_class': 'same very-small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `juncus_jacquinii`: docs/keys/**:outcome_size; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `luzula_sylvatica`: docs/keys/**:outcome_size; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C164 (n=2, mean_d=0.740, max_d=0.740)

- Shared aperture: inapert*
- Size classes: medium; mid range: (26.0, 27.0)
- Shared sculpture tokens: reticulaat, scabraat, verrucaat
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.740): `{'aperture': 'same inapert*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same inapert', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.74}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C165 (n=2, mean_d=0.615, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 31.0)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `malus_domestica` | *Malus domestica* | unranked | ap=tricol* | class=medium | mid=30.0µm | sc={rugulaat,striaat}
  - `malus_sylvestris` | *Malus sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | sc={rugulaat,striaat}
- Closest pair evidence `malus_domestica`–`malus_sylvestris` (d=0.615): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `malus_domestica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `malus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C166 (n=2, mean_d=1.141, max_d=1.141)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (122.5, 123.4)
- Shared sculpture tokens: —
- Members:
  - `malva_moschata` | *Malva moschata* | unranked | ap=peripor* | class=very-large | mid=122.5µm
  - `malva_sylvestris` | *Malva sylvestris* | unranked | ap=peripor* | class=very-large | mid=123.4µm
- Closest pair evidence `malva_moschata`–`malva_sylvestris` (d=1.141): `{'aperture': 'same peripor*', 'size_class': 'same very-large', 'size_mid_gap_um': 0.9, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.141}`
- Provenance (sample): `malva_moschata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `malva_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-malva-sylvestris.json

### C167 (n=2, mean_d=1.143, max_d=1.143)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.2, 35.4)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `medicago_lupulina` | *Medicago lupulina* | unranked | ap=tricol* | class=medium | mid=32.2µm | sc={reticulaat,rugulaat}
  - `parthenocissus_quinquefolia` | *Parthenocissus quinquefolia* | unranked | ap=tricol* | class=medium | mid=35.4µm | sc={reticulaat,rugulaat}
- Closest pair evidence `medicago_lupulina`–`parthenocissus_quinquefolia` (d=1.143): `{'aperture': 'same tricol*', 'size_class': 'same medium', 'size_mid_gap_um': 3.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.143}`
- Provenance (sample): `medicago_lupulina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `parthenocissus_quinquefolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C168 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tetrade*
- Size classes: large; mid range: (47.4, 47.6)
- Shared sculpture tokens: —
- Members:
  - `moneses_uniflora` | *Moneses uniflora* | unranked | ap=tetrade* | class=large | mid=47.4µm | sc={scabraat,verrucaat}
  - `vaccinium_uliginosum` | *Vaccinium uliginosum* | unranked | ap=tetrade* | class=large | mid=47.6µm
- Closest pair evidence `moneses_uniflora`–`vaccinium_uliginosum` (d=0.985): `{'aperture': 'same tetrade*', 'size_class': 'same large', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `moneses_uniflora`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; docs/keys/**:outcome_size; beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json · `vaccinium_uliginosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C169 (n=2, mean_d=1.045, max_d=1.045)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (6.2, 6.6)
- Shared sculpture tokens: —
- Members:
  - `myosotis_scorpioides` | *Myosotis scorpioides* | unranked | ap=heterocol* | class=very-small | mid=6.6µm | sc={psilaat}
  - `myosotis_sylvatica` | *Myosotis sylvatica* | unranked | ap=heterocol* | class=very-small | mid=6.2µm
- Closest pair evidence `myosotis_scorpioides`–`myosotis_sylvatica` (d=1.045): `{'aperture': 'same heterocol*', 'size_class': 'same very-small', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same heterocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `myosotis_scorpioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug28-heterocolpatae-myosotis-sylvatica.json

### C170 (n=2, mean_d=1.645, max_d=1.645)

- Shared aperture: syncol*
- Size classes: small; mid range: (17.0, 20.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); treat as morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** nemophila_menziesii ↔ nemophila_typ
- Members:
  - `nemophila_menziesii` | *Nemophila menziesii* | unranked | ap=syncol* | class=small | mid=17.0µm | sc={psilaat}
  - `nemophila_typ` | *Nemophila typ* | unranked | ap=syncol* | class=small | mid=20.0µm | sc={psilaat}
- Closest pair evidence `nemophila_menziesii`–`nemophila_typ` (d=1.645): `{'aperture': 'same syncol*', 'size_class': 'same small', 'size_mid_gap_um': 3.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.645}`
- Provenance (sample): `nemophila_menziesii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nemophila_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C171 (n=2, mean_d=0.795, max_d=0.795)

- Shared aperture: tricol*
- Size classes: large; mid range: (46.6, 48.4)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | sc={psilaat,reticulaat}
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | sc={psilaat,reticulaat}
- Closest pair evidence `nigella_damascena`–`saxifraga_granulata` (d=0.795): `{'aperture': 'same tricol*', 'size_class': 'same large', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.795}`
- Provenance (sample): `nigella_damascena`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `saxifraga_granulata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C172 (n=2, mean_d=1.081, max_d=1.081)

- Shared aperture: monopor*
- Size classes: medium; mid range: (37.0, 37.6)
- Shared sculpture tokens: —
- Members:
  - `nymphaea_alba` | *Nymphaea alba* | unranked | ap=monopor* | class=medium | mid=37.0µm | sc={echinaat}
  - `phalaris_arundinacea` | *Phalaris arundinacea* | unranked | ap=monopor* | class=medium | mid=37.6µm
- Closest pair evidence `nymphaea_alba`–`phalaris_arundinacea` (d=1.081): `{'aperture': 'same monopor*', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.081}`
- Provenance (sample): `nymphaea_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phalaris_arundinacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C173 (n=2, mean_d=1.160, max_d=1.160)

- Shared aperture: vesicul*
- Size classes: large; mid range: (63.5, 65.0)
- Shared sculpture tokens: —
- Members:
  - `pinus_nigra` | *Pinus nigra* | unranked | ap=vesicul* | class=large | mid=63.5µm
  - `pinus_sylvestris` | *Pinus sylvestris* | unranked | ap=vesicul* | class=large | mid=65.0µm
- Closest pair evidence `pinus_nigra`–`pinus_sylvestris` (d=1.160): `{'aperture': 'same vesicul*', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same vesicul', 'shape': 'missing_one_or_both', 'ornamentation': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'dims_used': 4, 'distance': 1.16}`
- Provenance (sample): `pinus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `pinus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation

### C174 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 22.7)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); treat as morph-bin group, not confirmed lookalike.
- Members:
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | sc={reticulaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | sc={reticulaat}
- Closest pair evidence `platanus_hybr`–`raphanus_sativus` (d=0.973): `{'aperture': 'same tricol*', 'size_class': 'same small', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `platanus_hybr`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_sativus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C175 (n=2, mean_d=1.213, max_d=1.213)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (48.3, 49.5)
- Shared sculpture tokens: —
- Members:
  - `prunella_vulgaris` | *Prunella vulgaris* | unranked | ap=stephanocol* | class=large | mid=48.3µm
  - `salvia_glutinosa` | *Salvia glutinosa* | unranked | ap=stephanocol* | class=large | mid=49.5µm
- Closest pair evidence `prunella_vulgaris`–`salvia_glutinosa` (d=1.213): `{'aperture': 'same stephanocol*', 'size_class': 'same large', 'size_mid_gap_um': 1.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.213}`
- Provenance (sample): `prunella_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C176 (n=2, mean_d=1.333, max_d=1.333)

- Shared aperture: stephanocolpor*
- Size classes: medium; mid range: (33.0, 34.7)
- Shared sculpture tokens: —
- Members:
  - `pulmonaria_montana` | *Pulmonaria montana* | unranked | ap=stephanocolpor* | class=medium | mid=34.7µm
  - `symphytum_officinale` | *Symphytum officinale* | unranked | ap=stephanocolpor* | class=medium | mid=33.0µm | sc={psilaat}
- Closest pair evidence `pulmonaria_montana`–`symphytum_officinale` (d=1.333): `{'aperture': 'same stephanocolpor*', 'size_class': 'same medium', 'size_mid_gap_um': 1.7, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.333}`
- Provenance (sample): `pulmonaria_montana`: data/pollen.yaml:size; data/pollen.yaml:pollen_class_beug · `symphytum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C177 (n=2, mean_d=1.357, max_d=1.357)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (42.5, 44.2)
- Shared sculpture tokens: —
- Members:
  - `salvia_officinalis` | *Salvia officinalis* | unranked | ap=stephanocol* | class=large | mid=42.5µm
  - `salvia_pratensis` | *Salvia pratensis* | unranked | ap=stephanocol* | class=large | mid=44.2µm | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `salvia_officinalis`–`salvia_pratensis` (d=1.357): `{'aperture': 'same stephanocol*', 'size_class': 'same large', 'size_mid_gap_um': 1.8, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.357}`
- Provenance (sample): `salvia_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-salvia-pratensis.json · `salvia_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C178 (n=2, mean_d=1.597, max_d=1.597)

- Shared aperture: peripor*
- Size classes: small; mid range: (18.5, 21.3)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** thalictrum_lucidum ↔ thalictrum_typ
- Members:
  - `thalictrum_lucidum` | *Thalictrum lucidum* | unranked | ap=peripor* | class=small | mid=21.3µm
  - `thalictrum_typ` | *Thalictrum typ* | unranked | ap=peripor* | class=small | mid=18.5µm | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `thalictrum_lucidum`–`thalictrum_typ` (d=1.597): `{'aperture': 'same peripor*', 'size_class': 'same small', 'size_mid_gap_um': 2.8, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.597}`
- Provenance (sample): `thalictrum_lucidum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

## 6. already_decided tags (summary)

- Decided pairs co-clustered at tight cut: 0
- Decided pairs co-clustered at loose cut: 1
- Per-cluster tags are listed under each cluster above; sources not modified.

## 7. Human review flags

- Clusters with species↔`*_typ` co-membership (loose cut): **12**
  - `anthemis_nobilis`, `aster_amellus`, `aster_typ`, `carpobrotis_edulis`, `carpobrotus_edulis`, `crepis_typ`, `galinsoga_typ`, `hieracium_aurantiacum`, `hieracium_typ`, `lampsana_commu`, `lampsana_communis`, `leontodon_autum`, `matricaria_chamo`, `matricaria_chamomilla`, `rudbeckia_hirta`, `senecio_inaequalis`, `senecio_jacobaea`, `senecio_jacobea`, `senecio_typ`, `taraxacum_officinale`: hieracium_aurantiacum ↔ hieracium_typ; senecio_jacobaea ↔ senecio_typ; senecio_inaequalis ↔ senecio_typ; senecio_jacobea ↔ senecio_typ; aster_amellus ↔ aster_typ
  - `ajuga_reptans`, `brassica_napus`, `brassica_nigra`, `brassica_oleracea`, `bunias_orientalis`, `crambe_maritima`, `crambe_typ`, `hesperis_matronalis`, `iberis_amara`, `salix_cinerea`, `salix_pentandra`: crambe_maritima ↔ crambe_typ
  - `euonymus_europaeus`, `mangifera_indica`, `melilotus_officinalis`, `mercurialis_perennis`, `mercurialis_typ`, `parnassia_palustris`, `verbascum_blattaria`, `verbascum_densiflorum`, `verbascum_thapsus`: mercurialis_perennis ↔ mercurialis_typ
  - `arcticum_minus`, `carduus_defloratus`, `carduus_typ`, `inula_helenium`, `sonchus_arvensis`, `tragopogon_typ`, `viscum_album`, `weigelia_diervilla_typ`: carduus_defloratus ↔ carduus_typ
  - `borreria_typ`, `borreria_verticilata`, `chenopodium_bonus_henricus`, `daphne_mezereum`, `phlox_subulata`: borreria_verticilata ↔ borreria_typ
  - `carduus_crispus`, `serratula_tinctoria`, `serratula_typ`: serratula_tinctoria ↔ serratula_typ
  - `euphorbia_typ`, `rhododendron_ponticum`, `rhododendron_typ`: rhododendron_ponticum ↔ rhododendron_typ
  - `galanthus_nivalis`, `muscari_botryoides`, `muscari_typ`: muscari_botryoides ↔ muscari_typ
  - `morus_alba`, `urtica_dioica`, `urtica_typ`: urtica_dioica ↔ urtica_typ
  - `arbutus_typ`, `arbutus_unedo`: arbutus_unedo ↔ arbutus_typ
  - `nemophila_menziesii`, `nemophila_typ`: nemophila_menziesii ↔ nemophila_typ
  - `thalictrum_lucidum`, `thalictrum_typ`: thalictrum_lucidum ↔ thalictrum_typ

- Borderline: conflict-masked taxa appear with MASKED tags; treat size/sculpt agreement as unreliable.
- Sparse taxa (appendix) were not forced into clusters.

## 8. Limits / risks

- Missing morph fields lower confidence via distance inflate; empty never treated as a match.
- Kerkvliet morph from section titles / YAML enrichment is **analytic**, not dichotomous source.
- Conflict mask removes unreliable dims but can leave taxa under-specified (easier false merges on remaining dims).
- No synonym / fuzzy Latin merge; duplicate concepts under different slugs stay separate.
- Key **topology** (late forks, co-endpoints) is intentionally unused as a similarity signal.
- Tokenization of free-text sculpture/shape is heuristic; compound phrases may under-match.
- Confirmed vs different lookalike pairs overlap in this morph distance; cuts follow guidance, not a clean ROC split.
- Linkage detail: Complete-linkage cut on pairwise morph distance (merge only if every cross-pair ≤ threshold; avoids single-link chaining).
- This report does not confirm or promote lookalikes.

## Appendix A. Sparse / singleton taxa

Taxa with fewer than 2 usable feature dimensions (not forced into clusters).

- `acer_cappadocicum` | *Acer cappadocicum* | unranked | ap=tricol* · features=1
- `anemone_apennina` | *Anemone apennina* | unranked | class=medium | mid=24.9µm · features=1
- `anemone_ranunculoides` | *Anemone ranunculoides* | unranked | class=medium | mid=28.2µm · features=1
- `anemone_sylvestris` | *Anemone sylvestris* | unranked | class=small | mid=17.9µm · features=1
- `anthyllis_barba_jovis` | *Anthyllis barba-jovis* | unranked | class=medium | mid=30.1µm · features=1
- `asperula_odorata` | *Asperula odorata* | unranked | class=small | mid=20.0µm | sc={scabraat} · features=3
- `catalpa_ovata` | *Catalpa ovata* | unranked | class=large | mid=73.0µm | sc={reticulaat} · features=2
- `ceratocapnos_claviculata_corydalis_claviculata` | *Ceratocapnos claviculata* | unranked | ap=pericol* · features=1
- `chaerophyllum_bulbosum` | *Chaerophyllum bulbosum* | unranked | class=medium | mid=25.1µm · features=1
- `corydalis_solida` | *Corydalis solida* | unranked | ap=pericol* · features=1
- `corylus_avelana` | *Corylus avelana* | unranked | class=medium | mid=26.0µm | sc={scabraat} · features=3
- `crepis_capillaris` | *Crepis capillaris* | unranked | ap=fenestr* · features=1
- `crepis_paludosa` | *Crepis paludosa* | unranked | ap=fenestr* · features=1
- `dactylorhiza_maculata` | *Dactylorhiza maculata* | unranked | class=large | mid=55.3µm | sc={reticulaat} · features=2
- `ephedra_helvetica` | *Ephedra helvetica* | unranked | class=medium | mid=38.0µm | sc={psilaat} · features=2
- `epipactis_palustris` | *Epipactis palustris* | unranked | ap=tetrade* · features=1
- `erica_vagans` | *Erica vagans* | unranked | class=medium | mid=33.1µm · features=1
- `fallopia_baldschuanica` | *Fallopia baldschuanica* | unranked | sc={reticulaat} · features=1
- `hieracium_austriacum` | *Hieracium austriacum* | unranked | ap=fenestr* · features=1
- `hypericum_polyphyllum` | *Hypericum polyphyllum* | unranked | sc={psilaat} · features=1
- `juniperus_commu` | *Juniperus commu* | unranked | class=medium | mid=26.0µm | sc={scabraat} · features=3
- `kalmia_angustifolia` | *Kalmia angustifolia* | unranked | class=medium | mid=29.5µm · features=1
- `lactuca_tatarica` | *Lactuca tatarica* | unranked | ap=fenestr* · features=1
- `lappula_deflexa` | *Lappula deflexa* | unranked | ap=heterocol* · features=1
- `lychnis_coronaria` | *Lychnis coronaria* | unranked | ap=peripor* · features=1
- `lythrum_virgatum` | *Lythrum virgatum* | unranked | ap=heterocol* · features=1
- `mentha_arvensis` | *Mentha arvensis* | unranked | ap=stephanocol* · features=1
- `mentha_longifolia` | *Mentha longifolia* | unranked | ap=stephanocol* · features=1
- `mimulus_guttatus` | *Mimulus guttatus* | unranked | class=medium | mid=40.0µm | sc={reticulaat,scabraat} · features=2
- `minuartia_biflora` | *Minuartia biflora* | unranked | ap=peripor* · features=1
- `persicaria_hydropiper` | *Persicaria hydropiper* | unranked | ap=peripor* · features=1
- `persicaria_lapathifolia` | *Persicaria lapathifolia* | unranked | ap=peripor* · features=1
- `picea_omorika` | *Picea omorika* | unranked | sc={reticulaat,rugulaat} · features=2
- `platanus_hispanica` | *Platanus hispanica* | unranked | sc={reticulaat} · features=1
- `polygonatum_multiflorum` | *Polygonatum multiflorum* | unranked | ap=monocol* · features=1
- `polygonum_persicaria` | *Polygonum persicaria* | rank=41 | ap=peripor* · features=1
- `populus_typ` | *Populus typ* | rank=35 | class=medium | mid=27.0µm | sc={reticulaat,scabraat} · features=2
- `primula_elatior` | *Primula elatior* | unranked | ap=stephanocol* · features=1
- `prunella_grandiflora` | *Prunella grandiflora* | unranked | ap=stephanocol* · features=1
- `prunus_padus` | *Prunus padus* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED · features=2
- `pseudofumaria_alba_corydalis_alba` | *Pseudofumaria alba* | unranked | ap=pericol* · features=1
- `pseudofumaria_lutea_corydalis_lutea` | *Pseudofumaria lutea* | unranked | ap=syncol* · features=1
- `sagina_nodosa` | *Sagina nodosa* | unranked | ap=peripor* · features=1
- `sagina_subulata` | *Sagina subulata* | unranked | ap=peripor* · features=1
- `salvia_typ` | *Salvia typ* | unranked | class=medium | mid=35.0µm | sc={reticulaat} · features=2
- `sanguisorba_minor` | *Sanguisorba minor* | unranked | ap=tricol* | size_MASKED | sculpt_MASKED · features=2
- `sonchus_asper` | *Sonchus asper* | unranked | ap=fenestr* · features=1
- `sophora_japonica` | *Sophora japonica* | unranked | class=small | mid=16.5µm | sc={reticulaat} · features=2
- `spiraea_typ` | *Spiraea typ* | rank=31 | class=small | mid=14.0µm | sc={psilaat} · features=2
- `spirea_x_vanhouttei` | *Spirea x vanhouttei* | unranked | class=small | mid=17.0µm · features=2
- `stellaria_media` | *Stellaria media* | unranked | ap=peripor* · features=1
- `thuja_typ` | *Thuja typ* | unranked | class=medium | mid=30.0µm | sc={reticulaat,scabraat} · features=2
- `vincetoxicum_hirundinaria` | *Vincetoxicum hirundinaria* | unranked | class=very-large | mid=150.0µm | sc={psilaat,scabraat} · features=2
- `xanthoceras_sorbifolium` | *Sapindaceae (fam.)* | unranked | class=small | mid=23.0µm | sc={psilaat,reticulaat} · features=2

## Appendix B. Clusterable singletons at tight cut

Clusterable taxa not in any tight multi-member cluster: **474** (not listed exhaustively).
Of which learning-priority: **15**
- `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | sc={psilaat,striaat}
- `rhamnus` | *Rhamnus* | rank=7 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
- `robinia` | *Robinia* | rank=9 | ap=tricol* | class=medium | mid=32.5µm | sc={scabraat}
- `echium` | *Echium* | rank=14 | ap=tricol* | class=small | mid=20.0µm | sc={reticulaat}
- `lotus` | *Lotus* | rank=20 | ap=tricol* | class=small | mid=20.0µm | sc={psilaat}
- `myosotis_typ` | *Myosotis typ* | rank=22 | ap=stephanocol* | class=very-small | mid=7.0µm | sc={psilaat}
- `phacelia_typ` | *Phacelia typ* | rank=23 | ap=stephanocol* | class=small | mid=22.0µm | sc={psilaat}
- `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=26.0µm | sc={reticulaat,rugulaat,striaat}
- `castanea_sativa` | *Castanea sativa* | rank=39 | ap=tricol* | class=very-small | mid=13.0µm | sc={psilaat,rugulaat,scabraat}
- `polygonum_aviculare` | *Polygonum aviculare* | rank=40 | ap=tricol* | class=medium | mid=32.9µm | sc={psilaat,scabraat}
- `amorpha_fruticosa` | *Amorpha fruticosa* | rank=42 | ap=tricol* | class=small | mid=20.9µm | sc={reticulaat,verrucaat}
- `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | sc={baculaat,reticulaat,verrucaat}
- `calluna_vulgaris` | *Calluna vulgaris* | rank=64 | ap=tricol* | class=medium | mid=35.5µm | sc={echinaat,psilaat,scabraat,verrucaat}
- `cynoglossum_typ` | *Cynoglossum typ* | rank=66 | ap=colpate* | class=very-small | mid=11.0µm | sc={psilaat}
- `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=33.0µm | sc={echinaat,scabraat}

