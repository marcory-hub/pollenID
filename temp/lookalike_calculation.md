# Morph lookalike clustering (one-shot)

Generated read-only from `data/pollen.yaml`, `docs/keys/**`,
`temp/reports/key-path-conflicts.md`, and `data/lookalike_review.yaml`.
Also writes `docs/assets/manifests/morph-neighbours.json` for PalynoQuest name-MCQ distractors.

## 1. Method summary

- **Goal:** taxa hard to tell apart under LM by morph similarity (not key topology).
- **Matching:** exact `pollen_key` only; no synonym merge; no `*_typ` representative fill.
- **Features:** YAML morph + dichotomous key endpoint/path attributes.
- **Size priority:** species-matched Beug/Eide/Reitsma/van der Ham outcome for mid; PK path-gates kept separately and hard-separate when non-overlapping.
- **Conflict mask:** YAML/Kerkvliet-analytic size masked when cross-key size conflicts exist; dichotomous key sizes still used.
- **Clustering:** pure-Python complete-linkage cut; Complete-linkage cut on pairwise morph distance; species-matched key outcome sizes for mid; path-gates hard-separate when non-overlapping.
- **Non-goals:** no promotion; write only this report + morph-neighbours JSON.

## 2. Feature inventory

| Metric | Count |
| :--- | ---: |
| Taxa in `pollen.yaml` | 1698 |
| Taxa with ≥1 usable morph feature | 961 |
| Clusterable | 901 |
| Sparse / appendix | 60 |
| With images (YAML) | 441 |
| Neighbours JSON keys | 381 |
| Conflict-masked (YAML size and/or sculpt) | 34 |
| Key-enriched taxa | 519 |
| With dichotomous key size | 139 |
| With PK path-gate | 47 |
| Learning-priority in clusterable | 39 |
| Already-decided pairs | 95 |

### Aperture families (clusterable)

- `tricol*`: 628
- `peripor*`: 59
- `stephanocol*`: 59
- `monocol*`: 44
- `fenestr*`: 27
- `tripor*`: 23
- `syncol*`: 13
- `stephanopor*`: 12
- `inapert*`: 7
- `stephanocolpor*`: 6
- `heterocol*`: 5
- `monopor*`: 5
- `tetrade*`: 5
- `pericol*`: 4
- `dipor*`: 2
- `vesicul*`: 2

### Conflict-masked taxa

- `aesculus_hippocastanum`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `agrimonia_eupatoria`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `agrimonia_odorata`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `allium_ursinum`: masked [size] (YAML/analytic only; key sizes kept when present)
- `arctium_minus`: masked [size] (YAML/analytic only; key sizes kept when present)
- `carpinus_betulus`: masked [size] (YAML/analytic only; key sizes kept when present)
- `centaurea_cyanus`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `centaurea_montana`: masked [size] (YAML/analytic only; key sizes kept when present)
- `colchicum_autumnale`: masked [size] (YAML/analytic only; key sizes kept when present)
- `convolvulus_arvensis`: masked [size] (YAML/analytic only; key sizes kept when present)
- `coriandrum_sativum`: masked [size] (YAML/analytic only; key sizes kept when present)
- `cornus_sanguinea`: masked [size] (YAML/analytic only; key sizes kept when present)
- `cotoneaster_intergerrimus`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `dryas_octopetala`: masked [size] (YAML/analytic only; key sizes kept when present)
- `hedera_helix`: masked [size] (YAML/analytic only; key sizes kept when present)
- `limonium_vulgare`: masked [size] (YAML/analytic only; key sizes kept when present)
- `linum_usitatissimum`: masked [size] (YAML/analytic only; key sizes kept when present)
- `liriodendron_tulipifera`: masked [size] (YAML/analytic only; key sizes kept when present)
- `medicago_sativa`: masked [size] (YAML/analytic only; key sizes kept when present)
- `olea_europaea`: masked [size] (YAML/analytic only; key sizes kept when present)
- `prunus_avium`: masked [size] (YAML/analytic only; key sizes kept when present)
- `prunus_padus`: masked [sculpt, size] (YAML/analytic only; key sizes kept when present)
- `reseda_lutea`: masked [size] (YAML/analytic only; key sizes kept when present)
- `robinia_pseudoacacia`: masked [size] (YAML/analytic only; key sizes kept when present)
- `rosa_canina`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `rosa_rubiginosa`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `rubus_chamaemorus`: masked [size] (YAML/analytic only; key sizes kept when present)
- `rubus_idaeus`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `sanguisorba_minor`: masked [sculpt, size] (YAML/analytic only; key sizes kept when present)
- `sanguisorba_officinalis`: masked [sculpt] (YAML/analytic only; key sizes kept when present)
- `tordylium_apulum`: masked [size] (YAML/analytic only; key sizes kept when present)
- `trifolium_pratense`: masked [size] (YAML/analytic only; key sizes kept when present)
- `trifolium_repens`: masked [size] (YAML/analytic only; key sizes kept when present)
- `viburnum_opulus`: masked [size] (YAML/analytic only; key sizes kept when present)

## 3. Clustering parameters

| Parameter | Value |
| :--- | :--- |
| Linkage | Complete-linkage cut on pairwise morph distance; species-matched key outcome sizes for mid; path-gates hard-separate when non-overlapping |
| W_APERTURE | 3.0 |
| W_SIZE_NONOVERLAP (preferred or path-gate) | 2.5 |
| W_SIZE_CLASS / ADJ | 2.0 / 0.8 |
| W_SIZE_MID (per 5 µm) | 1.2 |
| W_SCULPT / W_COARSE_SCULPT | 1.5 / 0.55 |
| W_BEUG / W_SHAPE / W_ORN | 0.7 / 0.8 / 0.5 |
| Missing aperture / size | 1.6 / 1.2 |
| **Tight cut** | ≤ **1.000** |
| **Loose cut** | ≤ **1.750** |

### Calibration notes

- Calibration pairs with distance: confirmed n=24, different n=53
- Confirmed distance: min=1.178 median=2.875 max=7.175
- Different distance: min=0.995 median=3.375 max=4.925
- Confirmed vs different may overlap; using guidance defaults tight=1.000, loose=1.750.
- Sanity `trifolium_pratense`–`trifolium_repens` distance=3.625 (species 40.0–50.3 (MiW 45.3) vs 26.3–34.3 (MiW 30.9); path_gate 42–50 vs 0–35)
- Fraction confirmed ≤ tight: 0.00; ≤ loose: 0.12
- Fraction different ≤ tight: 0.02; ≤ loose: 0.09

### Sample decided-pair distances

| Pair | Status | Distance |
| :--- | :--- | ---: |
| `acer_platanoides`–`centaurea_cyanus` | review:different | 2.516 |
| `acer_platanoides`–`malus_typ` | review:different | 3.875 |
| `acer_platanoides`–`prunus_pirus_typ` | review:different | 1.619 |
| `acer_platanoides`–`ranunculus_typ` | review:different | 2.561 |
| `acer_platanoides`–`robinia_pseudoacacia` | review:different | 2.799 |
| `acer_platanoides`–`taraxacum_typ` | review:different | 2.369 |
| `acer_platanoides`–`tilia_typ` | review:different | 4.725 |
| `aesculus_hippocastanum`–`melilotus_officinalis` | review:confirmed | 1.178 |
| `aesculus_hippocastanum`–`trifolium_repens` | review:confirmed | 1.448 |
| `ailanthus_altissima`–`taraxacum_typ` | review:different | 2.665 |
| `ailanthus_altissima`–`tilia_typ` | review:different | 4.425 |
| `amorpha_fruticosa`–`taraxacum_typ` | review:different | 4.725 |
| `anthriscus_typ`–`taraxacum_typ` | review:different | 4.925 |
| `anthriscus_typ`–`vicia_typ` | review:confirmed | 4.125 |
| `brassica_typ`–`fraxinus_ornus` | review:confirmed | 4.927 |
| `brassica_typ`–`ligustrum_vulgare` | review:confirmed | 3.975 |
| `brassica_typ`–`raphanus_typ` | review:confirmed | 2.625 |
| `brassica_typ`–`salix_typ` | review:confirmed | 2.625 |
| `brassica_typ`–`taraxacum_typ` | review:different | 4.125 |
| `brassica_typ`–`tilia_typ` | review:different | 2.625 |
| `calluna_vulgaris`–`centaurea_cyanus` | review:different | 2.476 |
| `calluna_vulgaris`–`ranunculus_typ` | review:different | 3.351 |
| `calluna_vulgaris`–`taraxacum_typ` | review:different | 4.625 |
| `calluna_vulgaris`–`tilia_typ` | review:different | 3.481 |
| `centaurea_cyanus`–`crataegus_typ` | review:different | 1.920 |

## 4. Tight clusters (near-identical)

Clusters with ≥2 members at tight≤1.000 cut. Learning-priority first.

- With ≥1 learning_priority_rank: **21**
- Unranked-only: **137**
- Total: **158**

### C1 (n=5, mean_d=0.406, max_d=0.797) — ranks [1]

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.2, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_typ` | *Brassica typ* | rank=1 | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=medium | mid=23.2µm | size_src=beug | sc={reticulaat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `pyracantha_coccin`–`pyracantha_coccinea` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `brassica_typ`: data/pollen.yaml:size; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm · `fallopia_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mercurialis_annua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pyracantha_coccin`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C2 (n=5, mean_d=0.649, max_d=0.879) — ranks [2]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.3, 33.4)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_pirus_typ` | *Prunus pirus* | rank=2 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={striaat}
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | size_src=yaml | sc={striaat}
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={striaat}
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | size_src=yaml | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | size_src=yaml | sc={striaat}
- Closest pair evidence `potentilla_norvegica`–`rosa_glauca` (d=0.435): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.435}`
- Provenance (sample): `potentilla_norvegica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_mahaleb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_pirus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `rosa_glauca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C3 (n=3, mean_d=0.549, max_d=0.778) — ranks [4]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.0)
- Shared sculpture tokens: echinaat
- Members:
  - `taraxacum_typ` | *Taraxacum typ* | rank=4 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={echinaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | size_src=yaml | sc={echinaat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `senecio_aquaticus`–`taraxacum_typ` (d=0.411): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.411}`
- Provenance (sample): `senecio_aquaticus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphyotrichum_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taraxacum_typ`: data/pollen.yaml:sculpture; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm

### C4 (n=3, mean_d=0.638, max_d=0.770) — ranks [5]

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.0, 37.5)
- Shared sculpture tokens: —
- Members:
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=37.0µm | size_src=beug | path_gate=25–40 | sculpt_MASKED
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={fijn,reticulaat}
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `callicarpa_typ`–`galeopsis_tetrahit` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `callicarpa_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_cyanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `galeopsis_tetrahit`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C5 (n=2, mean_d=0.591, max_d=0.591) — ranks [6]

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.9)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | class=medium | mid=30.9µm | size_src=beug | path_gate=0–35 | yaml_size_MASKED | sc={fijn,reticulaat}
  - `rhinanthus_typ` | *Rhinanthus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `rhinanthus_typ`–`trifolium_repens` (d=0.591): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-trifolium.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.9, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.591}`
- Provenance (sample): `rhinanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C6 (n=2, mean_d=0.675, max_d=0.675) — ranks [8]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.0)
- Shared sculpture tokens: —
- Members:
  - `aesculus` | *Aesculus* | rank=8 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={psilaat}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml
- Closest pair evidence `aesculus`–`solanum_lycopers` (d=0.675): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `aesculus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `solanum_lycopers`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C7 (n=2, mean_d=0.937, max_d=0.937) — ranks [10]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 32.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `vicia_typ` | *Vicia typ* | rank=10 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `euphorbia_cyparissias`–`vicia_typ` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `euphorbia_cyparissias`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse

### C8 (n=2, mean_d=0.745, max_d=0.745) — ranks [11]

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.1, 34.8)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | size_src=yaml | sc={rugulaat,striaat}
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | size_src=yaml | sc={rugulaat,striaat}
- Closest pair evidence `acer_campestre`–`acer_platanoides` (d=0.745): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.25, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.745}`
- Provenance (sample): `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_platanoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C9 (n=4, mean_d=0.728, max_d=0.985) — ranks [13]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.5, 19.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
  - `hypericum_androsaemum` | *Hypericum androsaemum* | unranked | ap=tricol* | class=small | mid=18.8µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `fallopia_baldschur`–`salix_typ` (d=0.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `alyssum_saxatile`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fallopia_baldschur`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_androsaemum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C10 (n=2, mean_d=0.425, max_d=0.425) — ranks [15]

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 36.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `stachys_palustris`–`tilia_typ` (d=0.425): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.425}`
- Provenance (sample): `stachys_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tilia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C11 (n=2, mean_d=0.233, max_d=0.233) — ranks [17]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `parthenocissus` | *Parthenocissus* | rank=17 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `parthenocissus`–`ulex_europaeus` (d=0.233): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.233}`
- Provenance (sample): `parthenocissus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `ulex_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C12 (n=4, mean_d=0.543, max_d=0.961) — ranks [18, 19]

- Shared aperture: tricol*
- Size classes: small; mid range: (19.9, 20.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `raphanus_typ` | *Raphanus typ* | rank=18 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `verbascum` | *Verbascum* | rank=19 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `diplotaxis_tenuifolia`–`raphanus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `diplotaxis_tenuifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `salix_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `verbascum`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse

### C13 (n=3, mean_d=0.775, max_d=0.975) — ranks [21]

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.5, 31.0)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={psilaat,scabraat}
  - `nicandra_physalodes` | *Nicandra physalodes* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=beug | sc={psilaat,scabraat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `lamium_typ`–`photinia_typ` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `lamium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nicandra_physalodes`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug14-tricolporatae-ps.json · `photinia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C14 (n=2, mean_d=0.899, max_d=0.899) — ranks [26]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.4, 31.5)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=31.5µm | size_src=beug | sc={reticulaat,rugulaat,striaat}
  - `medicago_lupulina` | *Medicago lupulina* | unranked | ap=tricol* | class=medium | mid=31.4µm | size_src=beug | sc={reticulaat,rugulaat}
- Closest pair evidence `ailanthus_altissima`–`medicago_lupulina` (d=0.899): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug19-tricolporatae-str-rhus.json vs beug:docs/keys/beug/beug23-tricolporoidatae-ret-medicago-lupulina.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.899}`
- Provenance (sample): `ailanthus_altissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `medicago_lupulina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C15 (n=3, mean_d=0.661, max_d=0.929) — ranks [29]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.4, 21.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | size_src=yaml | sc={reticulaat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | size_src=yaml | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ononis`–`ononis_natrix` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `melilotus_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis_natrix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C16 (n=4, mean_d=0.407, max_d=0.435) — ranks [33]

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 35.2)
- Shared sculpture tokens: echinaat
- Members:
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `helianthus_annuus`–`inula_salicina` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `helianthus_annuus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_salicina`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `senecio_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `xeranthemum_annuum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C17 (n=2, mean_d=0.749, max_d=0.749) — ranks [34]

- Shared aperture: tricol*
- Size classes: large; mid range: (60.2, 62.8)
- Shared sculpture tokens: psilaat, reticulaat, scabraat, verrucaat
- Members:
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | class=large | mid=62.8µm | size_src=beug | yaml_size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | class=large | mid=60.2µm | size_src=beug | yaml_size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `centaurea_montana`–`cornus_sanguinea` (d=0.749): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolporatae-ps.json vs beug:docs/keys/beug/beug15-tricolporoidatae-ps-cornus.json', 'size_class': 'same large', 'size_mid_gap_um': 2.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.749}`
- Provenance (sample): `centaurea_montana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_sanguinea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C18 (n=3, mean_d=0.583, max_d=0.687) — ranks [44]

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.1, 40.4)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | size_src=yaml | sc={striaat}
  - `acer_monspessulanum` | *Acer monspessulanum* | unranked | ap=tricol* | class=medium | mid=39.1µm | size_src=yaml | sc={striaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_opalus`–`crataegus_typ` (d=0.471): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.471}`
- Provenance (sample): `acer_monspessulanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `acer_opalus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crataegus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C19 (n=2, mean_d=0.961, max_d=0.961) — ranks [52]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.5, 35.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `impatiens_glandulifera` | *Impatiens glandulifera* | rank=52 | ap=stephanocol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `impatiens_glandulifera`–`thymus_serpyllum` (d=0.961): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.961}`
- Provenance (sample): `impatiens_glandulifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_serpyllum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C20 (n=3, mean_d=0.868, max_d=0.995) — ranks [53]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 18.5)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat,scabraat,striaat}
- Closest pair evidence `daucus_carota`–`filipendula_typ` (d=0.615): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.615}`
- Provenance (sample): `daucus_carota`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `limnanthes_douglasii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C21 (n=2, mean_d=0.861, max_d=0.861) — ranks [71]

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.6, 26.0)
- Shared sculpture tokens: psilaat, reticulaat, scabraat
- Members:
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=medium | mid=24.6µm | size_src=beug | sc={psilaat,reticulaat,scabraat}
  - `carum_carvi` | *Carum carvi* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `carum_carvi`–`cornus_mas` (d=0.861): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug15-tricolporoidatae-ps-cornus.json', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.5, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.861}`
- Provenance (sample): `carum_carvi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_mas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C22 (n=10, mean_d=0.600, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.3, 32.2)
- Shared sculpture tokens: echinaat
- Members:
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | size_src=yaml | sc={echinaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={echinaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | size_src=yaml | sc={echinaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | size_src=yaml | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | size_src=yaml | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={echinaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `achillea_millefolium`–`anthemis_tinctoria` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `achillea_millefolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `anthemis_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `aster_alpinus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `bidens_ferulifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C23 (n=9, mean_d=0.500, max_d=0.807)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 26.5)
- Shared sculpture tokens: echinaat
- Members:
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | size_src=yaml | sc={echinaat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={echinaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `aster_typ`–`matricaria_chamo` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aster_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erigeron_acer`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hieracium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lampsana_commu`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C24 (n=8, mean_d=0.461, max_d=0.725)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.5, 34.5)
- Shared sculpture tokens: echinaat
- Members:
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={echinaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={echinaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | size_src=yaml | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | size_src=yaml | sc={echinaat}
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `calendula_officinalis`–`senecio_erucifolius` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `calendula_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chrysanthemum_segetum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `doronicum_pardalianches`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helminthotheca_echioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C25 (n=7, mean_d=0.628, max_d=0.950)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.7, 29.4)
- Shared sculpture tokens: —
- Members:
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=medium | mid=28.2µm | size_src=beug | sculpt_MASKED
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | size_src=yaml | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={striaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | size_src=yaml | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | size_src=yaml | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | size_src=yaml | sc={striaat}
- Closest pair evidence `rosa_majalis`–`rosa_villosa` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `aesculus_hippocastanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycium_barbarum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C26 (n=5, mean_d=0.591, max_d=0.771)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.9, 25.6)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=25.6µm | size_src=beug | sc={striaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | size_src=yaml | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | size_src=yaml | sc={striaat}
- Closest pair evidence `potentilla_aurea`–`sempervivum_tectorum` (d=0.399): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.399}`
- Provenance (sample): `fragaria_moschata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug20-tricolporoidatae-str-potentilla.json · `potentilla_aurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_grandiflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rubus_caesius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C27 (n=4, mean_d=0.460, max_d=0.795)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 23.0)
- Shared sculpture tokens: —
- Members:
  - `ambrosia_artemisiifolia` | *Ambrosia artemisiifolia* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={echinaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={echinaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml
- Closest pair evidence `ambrosia_artemisiifolia`–`bidens_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `ambrosia_artemisiifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bidens_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `helenium_autumn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_polyph`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C28 (n=4, mean_d=0.457, max_d=0.531)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.6, 36.2)
- Shared sculpture tokens: echinaat
- Members:
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | size_src=yaml | sc={echinaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | size_src=yaml | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `cosmos_typ`–`senecio_paludosus` (d=0.399): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.399}`
- Provenance (sample): `aster_sedifolius`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cosmos_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_paludosus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `silphium_perfoliatum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C29 (n=4, mean_d=0.650, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.1, 25.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** crambe_maritima ↔ crambe_typ
- Members:
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | size_src=yaml | sc={reticulaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | size_src=yaml | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `crambe_maritima`–`crambe_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `brassica_napus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bunias_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crambe_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `crambe_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C30 (n=4, mean_d=0.957, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 25.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={reticulaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | size_src=yaml | sc={reticulaat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `brassica_oleracea`–`hesperis_matronalis` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `brassica_oleracea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hesperis_matronalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_cinerea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_pentandra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C31 (n=4, mean_d=0.502, max_d=0.993)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.5, 28.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cakile_maritima` | *Cakile maritima* | unranked | ap=tricol* | class=medium | mid=27.5µm | size_src=yaml | sc={reticulaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | size_src=yaml | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=beug | yaml_size_MASKED | sc={reticulaat}
- Closest pair evidence `corylopsis_parcifl`–`scrophularia_nodosa` (d=0.197): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.197}`
- Provenance (sample): `cakile_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_parcifl`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scrophularia_nodosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `viburnum_opulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C32 (n=4, mean_d=0.419, max_d=0.507)

- Shared aperture: tricol*
- Size classes: medium; mid range: (43.5, 44.0)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** carduus_defloratus ↔ carduus_typ
- Members:
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | size_src=yaml | sc={echinaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | size_src=yaml | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | size_src=yaml | sc={echinaat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `carduus_defloratus`–`carduus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_defloratus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carduus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_helenium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `tragopogon_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C33 (n=4, mean_d=0.205, max_d=0.245)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 28.5)
- Shared sculpture tokens: echinaat
- Members:
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={echinaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `carpobrotis_edulis`–`carpobrotus_edulis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carpobrotis_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotus_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_jacobaea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_jacobea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C34 (n=4, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: echinaat
- Members:
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `chrysanthemum_leuc`–`eupatorium_cann` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `chrysanthemum_leuc`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cann`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cannabinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `petasitis_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C35 (n=4, mean_d=0.560, max_d=0.995)

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 24.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `clethra_alnifolia` | *Clethra alnifolia* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | size_src=yaml | sc={reticulaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `polygonum_convol`–`rumex_obtusifolius` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clethra_alnifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polygonum_convol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhus_chinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rumex_obtusifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C36 (n=3, mean_d=0.825, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.0)
- Shared sculpture tokens: —
- Members:
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,rugulaat,striaat}
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,striaat}
- Closest pair evidence `acer_negundo`–`sarothamnus_sco` (d=0.675): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `acer_negundo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sarothamnus_sco`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C37 (n=3, mean_d=0.607, max_d=0.710)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.2, 33.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | size_src=yaml | sculpt_MASKED
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | size_src=yaml | sculpt_MASKED
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `agrimonia_eupatoria`–`rosa_canina` (d=0.424): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'masked_conflict', 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.424}`
- Provenance (sample): `agrimonia_eupatoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rosa_canina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_fragiferum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C38 (n=3, mean_d=0.501, max_d=0.689)

- Shared aperture: monocol*
- Size classes: medium; mid range: (32.2, 33.3)
- Shared sculpture tokens: psilaat, reticulaat, rugulaat, scabraat
- Members:
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | class=medium | mid=32.8µm | size_src=beug | path_gate=25–200 | yaml_size_MASKED | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.3µm | size_src=beug | path_gate=0–50 | sc={psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=32.2µm | size_src=beug | path_gate=25–200 | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `allium_ursinum`–`leucojum_aestivum` (d=0.269): `{'aperture': 'same monocol*', 'size_source': 'beug:docs/keys/beug/beug09-monocolpatae.json vs beug:docs/keys/beug/beug09-monocolpatae.json', 'path_gate': 'overlap 25.0–200.0 / 25.0–200.0', 'size_class': 'same medium', 'size_mid_gap_um': 0.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.269}`
- Provenance (sample): `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `butomus_umbellatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths · `leucojum_aestivum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C39 (n=3, mean_d=0.658, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (18.0, 18.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `alyssum_typ` | *Alyssum typ* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `linaria_vulg`–`linaria_vulgaris` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `alyssum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `linaria_vulg`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `linaria_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C40 (n=3, mean_d=0.965, max_d=0.985)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.8, 24.0)
- Shared sculpture tokens: —
- Members:
  - `amaranthus_caudatus` | *Amaranthus caudatus* | unranked | ap=peripor* | class=medium | mid=24.0µm | size_src=yaml | sc={scabraat}
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm | size_src=yaml
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm | size_src=yaml
- Closest pair evidence `amaranthus_caudatus`–`ribes_alpinum` (d=0.949): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `amaranthus_caudatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C41 (n=3, mean_d=0.973, max_d=0.997)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 28.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={reticulaat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | size_src=yaml | sc={reticulaat}
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `anacardium_occidentale`–`cardamine_flexuosa` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.961}`
- Provenance (sample): `anacardium_occidentale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cardamine_flexuosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_dasyclados`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C42 (n=3, mean_d=0.598, max_d=0.685)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 29.5)
- Shared sculpture tokens: echinaat
- Members:
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | size_src=yaml | sc={echinaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `aster_amellus`–`rudbeckia_hirta` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `anthemis_nobilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aster_amellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rudbeckia_hirta`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C43 (n=3, mean_d=0.221, max_d=0.269)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `aralia_elata`–`ricinus_communis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aralia_elata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ricinus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `viburnum_tinus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C44 (n=3, mean_d=0.692, max_d=0.975)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.5, 45.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
  - `sonchus_arvensis` | *Sonchus arvensis* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
  - `weigelia_diervilla_typ` | *Weigelia/Diervilla typ* | unranked | ap=tricol* | class=medium | mid=45.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arcticum_minus`–`sonchus_arvensis` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `arcticum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sonchus_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `weigelia_diervilla_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C45 (n=3, mean_d=0.495, max_d=0.555)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 23.6)
- Shared sculpture tokens: echinaat
- Members:
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | size_src=yaml | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | size_src=yaml | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `bellis_perennis`–`galinsoga_parviflora` (d=0.411): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `bellis_perennis`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galinsoga_parviflora`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `solidago_gigantea`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C46 (n=3, mean_d=0.372, max_d=0.495)

- Shared aperture: tricol*
- Size classes: large; mid range: (47.2, 47.8)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** serratula_tinctoria ↔ serratula_typ
- Members:
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | size_src=yaml | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | size_src=yaml | sc={echinaat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `serratula_tinctoria`–`serratula_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_crispus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `serratula_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serratula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C47 (n=3, mean_d=0.658, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 47.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carduus_nutans` | *Carduus nutans* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `onopordon_acant`–`onopordum_acanthium` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carduus_nutans`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordon_acant`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordum_acanthium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C48 (n=3, mean_d=0.625, max_d=0.875)

- Shared aperture: tricol*
- Size classes: large; mid range: (60.0, 60.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat}
  - `lonicera_typ` | *Lonicera typ* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat,reticulaat}
- Closest pair evidence `carlina_acaulis`–`carlina_aucalis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carlina_acaulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carlina_aucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C49 (n=3, mean_d=0.292, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (49.0, 49.0)
- Shared sculpture tokens: echinaat
- Members:
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `cirsium_arvense`–`serrulata_tinctoria` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `cirsium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cnicus_benedict`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serrulata_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C50 (n=3, mean_d=0.782, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 33.0)
- Shared sculpture tokens: —
- Members:
  - `cotoneaster_intergerrimus` | *Cotoneaster intergerrimus* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sculpt_MASKED
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={rugulaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | size_src=yaml | sc={rugulaat}
- Closest pair evidence `cotoneaster_intergerrimus`–`davidia_involucrata` (d=0.650): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.65}`
- Provenance (sample): `cotoneaster_intergerrimus`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `davidia_involucrata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_fruticosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C51 (n=3, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 29.0)
- Shared sculpture tokens: echinaat
- Members:
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `crepis_typ`–`hieracium_aurantiacum` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `crepis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hieracium_aurantiacum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `leontodon_autum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C52 (n=3, mean_d=0.695, max_d=0.855)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: fijn, striaat
- Members:
  - `dryas_octopetala` | *Dryas octopetala* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=beug | yaml_size_MASKED | sc={fijn,striaat}
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={fijn,striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | size_src=yaml | sc={fijn,striaat}
- Closest pair evidence `rubus_saxatilis`–`sorbus_aucuparia` (d=0.579): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.579}`
- Provenance (sample): `dryas_octopetala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rubus_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sorbus_aucuparia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C53 (n=3, mean_d=0.471, max_d=0.519)

- Shared aperture: tricol*
- Size classes: large; mid range: (70.0, 70.6)
- Shared sculpture tokens: echinaat
- Members:
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | size_src=yaml | sc={echinaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | size_src=yaml | sc={echinaat}
  - `scabiosa_columbar` | *Scabiosa columbar* | unranked | ap=tricol* | class=large | mid=70.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `echinops_sphaer`–`scabiosa_columbar` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `echinops_sphaer`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_alpigena`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scabiosa_columbar`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C54 (n=3, mean_d=0.647, max_d=0.783)

- Shared aperture: tricol*
- Size classes: large; mid range: (77.0, 78.7)
- Shared sculpture tokens: echinaat
- Members:
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | size_src=yaml | sc={echinaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=78.7µm | size_src=beug | sc={echinaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `echinops_sphaerocephalus`–`scabiosa_ochroleuca` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `echinops_sphaerocephalus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `scabiosa_columbaria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-dipsacaceae.json · `scabiosa_ochroleuca`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C55 (n=3, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `euonymus_europaeus`–`mangifera_indica` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `euonymus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mangifera_indica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melilotus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C56 (n=3, mean_d=0.742, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `foeniculum_vulga` | *Foeniculum vulga* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={scabraat}
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={scabraat}
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sculpt_MASKED
- Closest pair evidence `foeniculum_vulga`–`rubus_idaeus` (d=0.650): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.65}`
- Provenance (sample): `foeniculum_vulga`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hippopha_rhamn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_idaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C57 (n=3, mean_d=0.782, max_d=0.985)

- Shared aperture: monocol*
- Size classes: large; mid range: (56.8, 57.0)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm | size_src=yaml
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=monocol* | class=large | mid=57.0µm | size_src=yaml | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=monocol* | class=large | mid=57.0µm | size_src=yaml | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C58 (n=3, mean_d=0.941, max_d=0.949)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.0, 35.0)
- Shared sculpture tokens: —
- Members:
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `impatiens_balsamina`–`mentha_aquatica` (d=0.937): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `mentha_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C59 (n=3, mean_d=0.949, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.5, 28.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=beug | sc={reticulaat}
- Closest pair evidence `laburnum_anagyroides`–`viburnum_lantana` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-viburnum.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `laburnum_anagyroides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scrophularia_umbrosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viburnum_lantana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C60 (n=3, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (23.0, 23.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lysimachia_typ`–`raphanus_raph` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `lysimachia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_raph`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_raphanistrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C61 (n=3, mean_d=0.735, max_d=0.915)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.7, 28.7)
- Shared sculpture tokens: —
- Members:
  - `olea_europaea` | *Olea europaea* | unranked | ap=tricol* | class=medium | mid=27.7µm | size_src=beug | yaml_size_MASKED | sc={echinaat,microreticulaat,reticulaat,scabraat}
  - `papaver_rhoeas` | *Papaver rhoeas* | unranked | ap=tricol* | class=medium | mid=28.7µm | size_src=beug | sc={echinaat,microechinaat,microreticulaat,reticulaat,scabraat}
  - `rosa_rubiginosa` | *Rosa rubiginosa* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sculpt_MASKED
- Closest pair evidence `olea_europaea`–`rosa_rubiginosa` (d=0.472): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-olea.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.472}`
- Provenance (sample): `olea_europaea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `papaver_rhoeas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rosa_rubiginosa`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; reitsma:docs/keys/reitsma/rosaceae-reitsma.json

### C62 (n=3, mean_d=0.628, max_d=0.879)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.4, 42.5)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | size_src=yaml | sc={striaat}
  - `prunus_laurocerasus` | *Prunus laurocerasus* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={striaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | size_src=yaml | sc={striaat}
- Closest pair evidence `prunus_laurocerasus`–`prunus_spinoza` (d=0.485): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.485}`
- Provenance (sample): `prunus_cerasus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_laurocerasus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinoza`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C63 (n=3, mean_d=0.790, max_d=0.997)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.7, 34.0)
- Shared sculpture tokens: —
- Members:
  - `quercus_robur` | *Quercus robur* | unranked | ap=tricol* | class=medium | mid=33.7µm | size_src=yaml | sc={echinaat,psilaat,reticulaat}
  - `sanguisorba_minor` | *Sanguisorba minor* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=beug | yaml_size_MASKED | sculpt_MASKED
  - `vaccinium_vitis` | *Vaccinium vitis* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml
- Closest pair evidence `quercus_robur`–`sanguisorba_minor` (d=0.674): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug13-tricolpatae-ps.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'masked_conflict', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.674}`
- Provenance (sample): `quercus_robur`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sanguisorba_minor`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_vitis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C64 (n=3, mean_d=0.957, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.4, 23.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | size_src=yaml | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | size_src=yaml | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `salix_alba_var_tristis`–`salix_fragilis` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `salix_alba_var_tristis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_fragilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C65 (n=3, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 47.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `trifolium_incarnat`–`trifolium_incarnatum` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `trifolium_incarnat`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_incarnatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vicia_faba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C66 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | size_src=yaml | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C67 (n=2, mean_d=0.615, max_d=0.615)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 30.0)
- Shared sculpture tokens: striaat
- Members:
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={striaat}
  - `acer_tataricum_subsp_ginnala` | *Acer tataricum* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_japonicum`–`acer_tataricum_subsp_ginnala` (d=0.615): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.615}`
- Provenance (sample): `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_tataricum_subsp_ginnala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C68 (n=2, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.0)
- Shared sculpture tokens: striaat
- Members:
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_palmatum`–`aesculus_hippoca` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_palmatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aesculus_hippoca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C69 (n=2, mean_d=0.822, max_d=0.822)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.9, 42.2)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat
- Members:
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=42.2µm | size_src=beug | sc={grof,microreticulaat,psilaat,reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=41.9µm | size_src=beug | path_gate=36–41 | sc={microreticulaat,psilaat,reticulaat}
- Closest pair evidence `adonis_aestivalis`–`helleborus_niger` (d=0.822): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug13-tricolpatae-ps.json vs beug:docs/keys/beug/beug13-tricolpatae-ps.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.822}`
- Provenance (sample): `adonis_aestivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_niger`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C70 (n=2, mean_d=0.920, max_d=0.920)

- Shared aperture: tricol*
- Size classes: large; mid range: (75.0, 75.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | size_src=yaml | sculpt_MASKED
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | size_src=yaml | sc={grof,reticulaat}
- Closest pair evidence `agrimonia_odorata`–`geranium_typ` (d=0.920): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.92}`
- Provenance (sample): `agrimonia_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `geranium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C71 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: peripor*
- Size classes: medium; mid range: (25.4, 25.4)
- Shared sculpture tokens: —
- Members:
  - `alisma_lanceolatum` | *Alisma lanceolatum* | unranked | ap=peripor* | class=medium | mid=25.4µm | size_src=yaml
  - `plantago_lanceolata` | *Plantago Lanceolata* | unranked | ap=peripor* | class=medium | mid=25.4µm | size_src=beug | sc={verrucaat}
- Closest pair evidence `alisma_lanceolatum`–`plantago_lanceolata` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs beug:docs/keys/beug/beug33-periporatae-plantago-lanceolata.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `alisma_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `plantago_lanceolata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-plantaginaceae.json

### C72 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: monocol*
- Size classes: medium; mid range: (43.9, 44.0)
- Shared sculpture tokens: —
- Members:
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm | size_src=yaml
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | size_src=yaml | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.949): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tradescantia_andersoniana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C73 (n=2, mean_d=0.245, max_d=0.245)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `amorpha_fructico`–`verbascum_nigrum` (d=0.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `amorpha_fructico`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `verbascum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C74 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 32.4)
- Shared sculpture tokens: reticulaat, verrucaat
- Members:
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | size_src=yaml | sc={reticulaat,verrucaat}
- Closest pair evidence `angelica_sylvestris`–`foeniculum_vulgare` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `angelica_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C75 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.5, 35.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `anthriscus_cerefolium` | *Anthriscus cerefolium* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=beug | sc={psilaat}
  - `arctostaphylos_uva_ursi` | *Arctostaphylos uva-ursi* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `anthriscus_cerefolium`–`arctostaphylos_uva_ursi` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `anthriscus_cerefolium`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json · `arctostaphylos_uva_ursi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C76 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 17.0)
- Shared sculpture tokens: —
- Members:
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={microreticulaat,reticulaat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml
- Closest pair evidence `antirrhinum_majus`–`astragalus_sinicus` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `antirrhinum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `astragalus_sinicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C77 (n=2, mean_d=0.653, max_d=0.653)

- Shared aperture: tricol*
- Size classes: large; mid range: (51.0, 53.2)
- Shared sculpture tokens: echinaat
- Members:
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | class=large | mid=53.2µm | size_src=beug | yaml_size_MASKED | sc={echinaat}
  - `cirsium_vulgare` | *Cirsium vulgare* | unranked | ap=tricol* | class=large | mid=51.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arctium_minus`–`cirsium_vulgare` (d=0.653): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug17-ttt-ech-asteraceae.json vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 2.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.653}`
- Provenance (sample): `arctium_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cirsium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C78 (n=2, mean_d=0.387, max_d=0.387)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.9, 39.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | size_src=yaml | sc={echinaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arnica_montana`–`senecio_ovatus` (d=0.387): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `arnica_montana`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `senecio_ovatus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C79 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.9)
- Shared sculpture tokens: gemmaat, reticulaat, scabraat, verrucaat
- Members:
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `astrantia_major`–`ranunculus_repens` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['gemmaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `astrantia_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C80 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 29.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ballota_nigra_ssp_foetida`–`lupinus_typ` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `ballota_nigra_ssp_foetida`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lupinus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C81 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.0, 41.2)
- Shared sculpture tokens: —
- Members:
  - `berberis_typ` | *Berberis typ* | unranked | ap=stephanocol* | class=medium | mid=41.0µm | size_src=yaml | sc={psilaat}
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm | size_src=yaml
- Closest pair evidence `berberis_typ`–`clinopodium_vulgare` (d=0.985): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `berberis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C82 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: peripor*
- Size classes: medium; mid range: (30.0, 30.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** borreria_verticilata ↔ borreria_typ
- Members:
  - `borreria_typ` | *Borreria typ* | unranked | ap=peripor* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=peripor* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `borreria_typ`–`borreria_verticilata` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `borreria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C83 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.6, 28.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `brassica_rapa`–`marrubium_vulgare` (d=0.949): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `brassica_rapa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `marrubium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C84 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.5, 39.5)
- Shared sculpture tokens: —
- Members:
  - `bryonia_dioica` | *Bryonia dioica* | unranked | ap=tricol* | class=medium | mid=39.5µm | size_src=yaml | sc={reticulaat}
  - `vaccinium_corymb` | *Vaccinium corymb* | unranked | ap=tricol* | class=medium | mid=39.5µm | size_src=yaml
- Closest pair evidence `bryonia_dioica`–`vaccinium_corymb` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `bryonia_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_corymb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C85 (n=2, mean_d=0.997, max_d=0.997)

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.7, 34.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `buxus_sempervirens` | *Buxus sempervirens* | unranked | ap=peripor* | class=medium | mid=33.7µm | size_src=beug | sc={reticulaat}
  - `silene_dioica` | *Silene dioica* | unranked | ap=peripor* | class=medium | mid=34.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `buxus_sempervirens`–`silene_dioica` (d=0.997): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-buxus.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.997}`
- Provenance (sample): `buxus_sempervirens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-buxus.json · `silene_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C86 (n=2, mean_d=0.921, max_d=0.921)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 29.5)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | size_src=yaml | sc={psilaat,reticulaat}
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | size_src=yaml | sc={psilaat,reticulaat}
- Closest pair evidence `caltha_palustris`–`capsicum_annuum` (d=0.921): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'mismatch tricol/tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.921}`
- Provenance (sample): `caltha_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `capsicum_annuum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C87 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 29.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | size_src=yaml | sc={psilaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `caltha_palustris_ssp_araneosa`–`papaver_dubium` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `caltha_palustris_ssp_araneosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `papaver_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C88 (n=2, mean_d=0.728, max_d=0.728)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.6, 29.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `cardamine_pratensis`–`corylopsis_pauciflora` (d=0.728): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.333, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.7277}`
- Provenance (sample): `cardamine_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_pauciflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C89 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | size_src=yaml | sc={psilaat,rugulaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | size_src=yaml | sc={psilaat,rugulaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.125): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'rugulaat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C90 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: —
- Members:
  - `cichorium_intybus` | *Cichorium intybus* | unranked | ap=tricol* | class=medium | mid=38.0µm | size_src=yaml | sc={echinaat}
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm | size_src=yaml
- Closest pair evidence `cichorium_intybus`–`empetrum_nigrum` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `cichorium_intybus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `empetrum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation

### C91 (n=2, mean_d=0.573, max_d=0.573)

- Shared aperture: tricol*
- Size classes: large; mid range: (55.8, 56.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | size_src=yaml | sc={reticulaat}
  - `pisum_sativum` | *Pisum sativum* | unranked | ap=tricol* | class=large | mid=55.8µm | size_src=beug | path_gate=53–59 | sc={reticulaat}
- Closest pair evidence `citrullus_lanatus`–`pisum_sativum` (d=0.573): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-vicia.json', 'size_class': 'same large', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.573}`
- Provenance (sample): `citrullus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pisum_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C92 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.0)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `clematis_vitalba`–`melampyrum_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clematis_vitalba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C93 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.8, 23.9)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | size_src=yaml | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `cochlearia_officinalis_ssp_off`–`salix_daphnoides` (d=0.949): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `cochlearia_officinalis_ssp_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_daphnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C94 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.0, 34.1)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | size_src=yaml | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `colutea_arborescens`–`lupinus_angustifolius` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.961}`
- Provenance (sample): `colutea_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lupinus_angustifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C95 (n=2, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.9, 35.9)
- Shared sculpture tokens: striaat
- Members:
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={striaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={striaat}
- Closest pair evidence `cotoneaster_integerrimus`–`prunus_cerasifera` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `cotoneaster_integerrimus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_cerasifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C96 (n=2, mean_d=0.819, max_d=0.819)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.9, 42.7)
- Shared sculpture tokens: fijn, rugulaat, striaat
- Members:
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | size_src=yaml | sc={fijn,rugulaat,striaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | size_src=yaml | sc={fijn,rugulaat,striaat}
- Closest pair evidence `crataegus_monogyna`–`prunus_spinosa` (d=0.819): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'rugulaat', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.819}`
- Provenance (sample): `crataegus_monogyna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C97 (n=2, mean_d=0.507, max_d=0.507)

- Shared aperture: tricol*
- Size classes: large; mid range: (54.7, 55.2)
- Shared sculpture tokens: echinaat
- Members:
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | size_src=yaml | sc={echinaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=54.7µm | size_src=beug | path_gate=28–45 | sc={echinaat}
- Closest pair evidence `cynara_cardunculus`–`lonicera_xylosteum` (d=0.507): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug17-ttt-ech-lonicera.json', 'size_class': 'same large', 'size_mid_gap_um': 0.55, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.507}`
- Provenance (sample): `cynara_cardunculus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_xylosteum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C98 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.8, 30.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cytisus_scoparius` | *Cytisus scoparius* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={psilaat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `cytisus_scoparius`–`solanum_nigrum_ssp_nigrum` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `cytisus_scoparius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_nigrum_ssp_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C99 (n=2, mean_d=0.995, max_d=0.995)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 31.5)
- Shared sculpture tokens: fijn, scabraat
- Members:
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={fijn,reticulaat,scabraat}
  - `teucrium_chamae` | *Teucrium chamae* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={fijn,scabraat}
- Closest pair evidence `cytisus_typ`–`teucrium_chamae` (d=0.995): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['fijn', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.995}`
- Provenance (sample): `cytisus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `teucrium_chamae`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C100 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 17.0)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `deutzia_typ`–`linaria_cymbalaria` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `deutzia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `linaria_cymbalaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C101 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: large; mid range: (73.4, 74.8)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | size_src=yaml | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `dipsacus_pilosus`–`lonicera_caprifolium` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.711}`
- Provenance (sample): `dipsacus_pilosus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_caprifolium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C102 (n=2, mean_d=0.908, max_d=0.908)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 18.7)
- Shared sculpture tokens: fijn, psilaat, reticulaat
- Members:
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,psilaat,reticulaat}
  - `hypericum_perforatum` | *Hypericum perforatum* | unranked | ap=tricol* | class=small | mid=18.7µm | size_src=beug | sc={fijn,microreticulaat,psilaat,reticulaat}
- Closest pair evidence `echium_vulgare`–`hypericum_perforatum` (d=0.908): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug23-tricolporoidatae-ret-hypericum-perforatum.json', 'size_class': 'same small', 'size_mid_gap_um': 1.7, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['fijn', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.908}`
- Provenance (sample): `echium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_perforatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C103 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.9, 35.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | size_src=yaml | sc={reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `erophila_verna`–`galeopsis_segetum` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `erophila_verna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galeopsis_segetum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C104 (n=2, mean_d=0.735, max_d=0.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 32.5)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `eryngium_typ`–`pimpinella_anisum` (d=0.735): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.735}`
- Provenance (sample): `eryngium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_anisum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C105 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.5, 38.6)
- Shared sculpture tokens: —
- Members:
  - `eschscholtzia_calif` | *Eschscholtzia calif* | unranked | ap=stephanocol* | class=medium | mid=38.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm | size_src=yaml
- Closest pair evidence `eschscholtzia_calif`–`melissa_officinalis` (d=0.949): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.949}`
- Provenance (sample): `eschscholtzia_calif`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melissa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C106 (n=2, mean_d=0.975, max_d=0.975)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.5, 43.0)
- Shared sculpture tokens: verrucaat
- Members:
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | size_src=yaml | sc={verrucaat}
  - `rhododendron_ponticum` | *Rhododendron ponticum* | unranked | ap=tricol* | class=medium | mid=43.0µm | size_src=yaml | sc={verrucaat}
- Closest pair evidence `euphorbia_typ`–`rhododendron_ponticum` (d=0.975): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `euphorbia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhododendron_ponticum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C107 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: tricol*
- Size classes: small; mid range: (14.0, 16.0)
- Shared sculpture tokens: clavaat, echinaat, fijn, microechinaat, psilaat, scabraat
- Members:
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | size_src=yaml | sc={clavaat,echinaat,fijn,microechinaat,psilaat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | size_src=yaml | sc={clavaat,echinaat,fijn,microechinaat,psilaat}
- Closest pair evidence `filipendula_ulmaria`–`filipendula_vulgaris` (d=0.605): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat', 'echinaat', 'fijn', 'microechinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `filipendula_ulmaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C108 (n=2, mean_d=0.855, max_d=0.855)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 23.0)
- Shared sculpture tokens: grof, striaat
- Members:
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={grof,striaat}
  - `sibbaldia_procumbens` | *Sibbaldia procumbens* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={grof,striaat}
- Closest pair evidence `fragaria_vesca`–`sibbaldia_procumbens` (d=0.855): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['grof', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.855}`
- Provenance (sample): `fragaria_vesca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sibbaldia_procumbens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C109 (n=2, mean_d=0.887, max_d=0.887)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.1, 23.2)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `frangula_alnus` | *Frangula alnus* | unranked | ap=tricol* | class=medium | mid=23.2µm | size_src=beug | sc={psilaat,scabraat,verrucaat}
  - `melampyrum_pratense` | *Melampyrum pratense* | unranked | ap=tricol* | class=medium | mid=23.1µm | size_src=yaml | sc={scabraat,verrucaat}
- Closest pair evidence `frangula_alnus`–`melampyrum_pratense` (d=0.887): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolporatae-ps.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.887}`
- Provenance (sample): `frangula_alnus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C110 (n=2, mean_d=0.375, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 27.0)
- Shared sculpture tokens: echinaat
- Members:
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `galinsoga_typ`–`senecio_typ` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `galinsoga_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C111 (n=2, mean_d=0.927, max_d=0.927)

- Shared aperture: tricol*
- Size classes: large; mid range: (58.2, 60.5)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | size_src=yaml | sc={clavaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | size_src=yaml | sc={clavaat}
- Closest pair evidence `geranium_molle`–`linum_flavum` (d=0.927): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 2.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.927}`
- Provenance (sample): `geranium_molle`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `linum_flavum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C112 (n=2, mean_d=0.675, max_d=0.675)

- Shared aperture: tricol*
- Size classes: large; mid range: (78.3, 79.6)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | size_src=yaml | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | size_src=yaml | sc={clavaat}
- Closest pair evidence `geranium_nodosum`–`geranium_phaeum` (d=0.675): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.675}`
- Provenance (sample): `geranium_nodosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_phaeum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C113 (n=2, mean_d=0.567, max_d=0.567)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 23.6)
- Shared sculpture tokens: grof, striaat
- Members:
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | size_src=yaml | sc={grof,striaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=yaml | sc={grof,striaat}
- Closest pair evidence `geum_rivale`–`geum_urbanum` (d=0.567): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.8, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['grof', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.567}`
- Provenance (sample): `geum_rivale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geum_urbanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C114 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 33.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | size_src=yaml | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `glaucium_flavum`–`sinapis_arvensis` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `glaucium_flavum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sinapis_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C115 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.6, 41.9)
- Shared sculpture tokens: —
- Members:
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm | size_src=yaml
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm | size_src=yaml
- Closest pair evidence `glechoma_hederacea`–`impatiens_noli_tangere` (d=0.985): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.985}`
- Provenance (sample): `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C116 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.5, 31.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={reticulaat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `gleditsia_triacanthos`–`trifolium_arvense` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `gleditsia_triacanthos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C117 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 24.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `hedysarum_corona`–`sulla_coronaria` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `hedysarum_corona`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sulla_coronaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C118 (n=2, mean_d=0.629, max_d=0.629)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.9, 29.0)
- Shared sculpture tokens: microreticulaat, reticulaat
- Members:
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=26.9µm | size_src=beug | sc={microreticulaat,reticulaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=beug | sc={microreticulaat,reticulaat}
- Closest pair evidence `helleborus_foetidus`–`vitex_agnus_castus` (d=0.629): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-helleborus-foetidus.json vs beug:docs/keys/beug/beug21-tricolpatae-ret-vitex.json', 'size_class': 'same medium', 'size_mid_gap_um': 2.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.629}`
- Provenance (sample): `helleborus_foetidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vitex_agnus_castus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C119 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.5, 35.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `helleborus_viridis_ssp_occidentalis`–`lamium_amplexicaule` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `helleborus_viridis_ssp_occidentalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lamium_amplexicaule`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C120 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (35.3, 35.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm | size_src=yaml
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm | size_src=yaml
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.973): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `sonchus_oleraceus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C121 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (39.5, 39.6)
- Shared sculpture tokens: —
- Members:
  - `hieracium_umbellatum` | *Hieracium umbellatum* | unranked | ap=fenestr* | class=medium | mid=39.6µm | size_src=yaml
  - `vaccinium_corymbosum` | *Vaccinium corymbosum* | unranked | ap=fenestr* | class=medium | mid=39.5µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `hieracium_umbellatum`–`vaccinium_corymbosum` (d=0.961): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.961}`
- Provenance (sample): `hieracium_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `vaccinium_corymbosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C122 (n=2, mean_d=0.447, max_d=0.447)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 26.3)
- Shared sculpture tokens: striaat
- Members:
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | size_src=yaml | sc={striaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
- Closest pair evidence `hippocrepis_comosa`–`potentilla_erecta` (d=0.447): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.447}`
- Provenance (sample): `hippocrepis_comosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_erecta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C123 (n=2, mean_d=0.951, max_d=0.951)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 29.4)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={reticulaat,scabraat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `hippophae_rhamnoides`–`odontites_vernus` (d=0.951): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.951}`
- Provenance (sample): `hippophae_rhamnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `odontites_vernus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C124 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 17.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={reticulaat}
  - `theobroma_cacao` | *Theobroma cacao* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `hypericum_tetrapterum`–`theobroma_cacao` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `hypericum_tetrapterum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `theobroma_cacao`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C125 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.9, 32.1)
- Shared sculpture tokens: —
- Members:
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm | size_src=yaml
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm | size_src=yaml
- Closest pair evidence `hyssopus_officinalis`–`thymus_pulegioides` (d=0.985): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.985}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thymus_pulegioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C126 (n=2, mean_d=0.740, max_d=0.740)

- Shared aperture: inapert*
- Size classes: medium; mid range: (26.0, 27.0)
- Shared sculpture tokens: reticulaat, scabraat, verrucaat
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | size_src=yaml | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.740): `{'aperture': 'same inapert*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same inapert', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.74}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C127 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 23.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `koelreuteria_paniculata` | *Koelreuteria paniculata* | unranked | ap=tricol* | class=medium | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=beug | path_gate=0–35 | sc={reticulaat}
- Closest pair evidence `koelreuteria_paniculata`–`parnassia_palustris` (d=0.973): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-parnassia.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.973}`
- Provenance (sample): `koelreuteria_paniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `parnassia_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C128 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.5, 41.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | size_src=yaml | sc={reticulaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lathyrus_pratensis`–`lathyrus_tuberosus` (d=0.949): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `lathyrus_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_tuberosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C129 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={reticulaat}
  - `pulmonaria_officinalis` | *Pulmonaria officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lavandula_angisti`–`pulmonaria_officinalis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C130 (n=2, mean_d=0.531, max_d=0.531)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (42.5, 43.1)
- Shared sculpture tokens: echinaat
- Members:
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | size_src=yaml | sc={echinaat}
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.531): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.531}`
- Provenance (sample): `leontodon_autumnalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `picris_hieracioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C131 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (21.5, 21.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | size_src=yaml | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `leonurus_cardiaca`–`salix_caprea` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `leonurus_cardiaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_caprea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C132 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 17.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lepidium_sativum`–`tamarix_gallica` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `lepidium_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `tamarix_gallica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C133 (n=2, mean_d=0.997, max_d=0.997)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.2, 34.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=34.2µm | size_src=beug | sc={reticulaat}
  - `onobrychis_viciifolia` | *Onobrychis viciifolia* | unranked | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ligustrum_vulgare`–`onobrychis_viciifolia` (d=0.997): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-ligustrum.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.997}`
- Provenance (sample): `ligustrum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onobrychis_viciifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C134 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.6, 27.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=beug | path_gate=0–35 | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lysimachia_vulgaris`–`ononis_spinosa` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug22-tricolporatae-ret-lysimachia.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `lysimachia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ononis_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C135 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: monocol*
- Size classes: large; mid range: (54.2, 54.2)
- Shared sculpture tokens: —
- Members:
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm | size_src=yaml
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm | size_src=yaml
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.925): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C136 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.0, 31.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat}
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `nepeta_cataria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `satureja_hortensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C137 (n=2, mean_d=0.795, max_d=0.795)

- Shared aperture: tricol*
- Size classes: large; mid range: (46.6, 48.4)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | size_src=yaml | sc={psilaat,reticulaat}
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | size_src=yaml | sc={psilaat,reticulaat}
- Closest pair evidence `nigella_damascena`–`saxifraga_granulata` (d=0.795): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.795}`
- Provenance (sample): `nigella_damascena`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `saxifraga_granulata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C138 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 29.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | size_src=yaml | sc={reticulaat}
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ononis_repens_ssp_repens`–`scrophularia_auriculata` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `ononis_repens_ssp_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scrophularia_auriculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C139 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (33.0, 33.2)
- Shared sculpture tokens: —
- Members:
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm | size_src=yaml
- Closest pair evidence `origanum_vulgare`–`salvia_nemorosa` (d=0.973): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `origanum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `salvia_nemorosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C140 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ornithopus_perpus`–`ornithopus_perpusillus` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `ornithopus_perpus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ornithopus_perpusillus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C141 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.0, 19.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `osmanthus_typ`–`thlaspi_arvense` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `osmanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thlaspi_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C142 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.8, 37.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={reticulaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `parthenocissus_typ`–`tilia_tomentosa` (d=0.973): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `parthenocissus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tilia_tomentosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C143 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (35.1, 35.1)
- Shared sculpture tokens: —
- Members:
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm | size_src=yaml
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm | size_src=yaml
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.925): `{'aperture': 'same stephanopor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `phyteuma_spicatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `phyteuma_spicatum_ssp_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C144 (n=2, mean_d=0.973, max_d=0.973)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 22.7)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={reticulaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `platanus_hybr`–`raphanus_sativus` (d=0.973): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `platanus_hybr`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_sativus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C145 (n=2, mean_d=0.627, max_d=0.627)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.3, 20.4)
- Shared sculpture tokens: striaat
- Members:
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | size_src=yaml | sc={striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | size_src=yaml | sc={striaat}
- Closest pair evidence `potentilla_fruticosa`–`sedum_album` (d=0.627): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 1.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.627}`
- Provenance (sample): `potentilla_fruticosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sedum_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C146 (n=2, mean_d=0.543, max_d=0.543)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (24.1, 24.8)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat, rugulaat, scabraat
- Members:
  - `primula_veris` | *Primula veris* | unranked | ap=stephanocol* | class=medium | mid=24.1µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `salvia_verticillata` | *Salvia verticillata* | unranked | ap=stephanocol* | class=medium | mid=24.8µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `primula_veris`–`salvia_verticillata` (d=0.543): `{'aperture': 'same stephanocol*', 'size_source': 'beug:docs/keys/beug/beug24-stephanocolpatae-primula-veris.json vs beug:docs/keys/beug/beug24-stephanocolpatae-salvia-verticillata.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.543}`
- Provenance (sample): `primula_veris`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-primula-veris.json; beug:docs/keys/beug/beug24-stephanocolpatae.json · `salvia_verticillata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-salvia-verticillata.json

### C147 (n=2, mean_d=0.670, max_d=0.670)

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.5, 37.5)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `pulsatilla_vulgaris` | *Pulsatilla vulgaris* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={scabraat,verrucaat}
  - `teucrium_chamaedrys` | *Teucrium chamaedrys* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=beug | path_gate=0–45 | sc={scabraat,verrucaat}
- Closest pair evidence `pulsatilla_vulgaris`–`teucrium_chamaedrys` (d=0.670): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug13-tricolpatae-ps-teucrium.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat', 'verrucaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.667, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.6703}`
- Provenance (sample): `pulsatilla_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `teucrium_chamaedrys`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C148 (n=2, mean_d=0.557, max_d=0.557)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 28.8)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | class=medium | mid=28.8µm | size_src=beug | yaml_size_MASKED | sc={fijn,reticulaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `reseda_lutea`–`ulex_typ` (d=0.557): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-reseda.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.8, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.557}`
- Provenance (sample): `reseda_lutea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ulex_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C149 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: tricol*
- Size classes: small; mid range: (20.9, 21.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `reseda_luteola`–`salix_triandra` (d=0.949): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `reseda_luteola`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_triandra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C150 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 33.0)
- Shared sculpture tokens: —
- Members:
  - `ribes_sanguineum` | *Ribes sanguineum* | unranked | ap=peripor* | class=medium | mid=33.0µm | size_src=yaml | sc={psilaat,scabraat}
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm | size_src=yaml
- Closest pair evidence `ribes_sanguineum`–`ribes_uva_crispa` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `ribes_sanguineum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_uva_crispa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C151 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: —
- Members:
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml
- Closest pair evidence `rosmarinus_officinalis`–`thymus_vulgaris` (d=0.925): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `rosmarinus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C152 (n=2, mean_d=0.961, max_d=0.961)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.2, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | size_src=yaml | sc={reticulaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `stachys_sylvatica`–`syringa_vulgaris` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `stachys_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `syringa_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C153 (n=2, mean_d=0.875, max_d=0.875)

- Shared aperture: tricol*
- Size classes: large; mid range: (80.0, 80.0)
- Shared sculpture tokens: echinaat
- Members:
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | size_src=yaml | sc={echinaat}
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | size_src=yaml | sc={echinaat,striaat}
- Closest pair evidence `succisa_praten`–`succisa_pratensis` (d=0.875): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.875}`
- Provenance (sample): `succisa_praten`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `succisa_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C154 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.4, 38.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_platyphyllos` | *Tilia Platyphyllos* | unranked | ap=tricol* | class=medium | mid=38.4µm | size_src=beug | sc={reticulaat}
  - `vicia_villosa` | *Vicia villosa* | unranked | ap=tricol* | class=medium | mid=38.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `tilia_platyphyllos`–`vicia_villosa` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug22-tricolporatae-ret-tilia.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `tilia_platyphyllos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_villosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C155 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.8, 33.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=yaml | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `trifolium_dubium`–`vicia_sepium` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `trifolium_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_sepium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C156 (n=2, mean_d=0.645, max_d=0.645)

- Shared aperture: tripor*
- Size classes: small; mid range: (15.5, 16.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** urtica_dioica ↔ urtica_typ
- Members:
  - `urtica_dioica` | *Urtica dioica* | unranked | ap=tripor* | class=small | mid=15.5µm | size_src=yaml | sc={psilaat}
  - `urtica_typ` | *Urtica typ* | unranked | ap=tripor* | class=small | mid=16.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `urtica_dioica`–`urtica_typ` (d=0.645): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.645}`
- Provenance (sample): `urtica_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `urtica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C157 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.2, 25.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `verbascum_blattaria`–`verbascum_densiflorum` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `verbascum_blattaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `verbascum_densiflorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C158 (n=2, mean_d=0.937, max_d=0.937)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.2, 33.3)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | size_src=yaml | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `veronica_officinalis`–`viola_hirta` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `veronica_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viola_hirta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

## 5. Looser clusters (close)

Clusters with ≥2 members at loose≤1.750 cut. Learning-priority first.

- With ≥1 learning_priority_rank: **28**
- Unranked-only: **158**
- Total: **186**

### C1 (n=10, mean_d=1.019, max_d=1.731) — ranks [1]

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.8, 26.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `brassica_typ` | *Brassica typ* | rank=1 | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `fallopia_japonica` | *Fallopia japonica* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `koelreuteria_paniculata` | *Koelreuteria paniculata* | unranked | ap=tricol* | class=medium | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `mercurialis_annua` | *Mercurialis annua* | unranked | ap=tricol* | class=medium | mid=23.2µm | size_src=beug | sc={reticulaat}
  - `parnassia_palustris` | *Parnassia palustris* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=beug | path_gate=0–35 | sc={reticulaat}
  - `pyracantha_coccin` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
  - `pyracantha_coccinea` | *Pyracantha coccinea* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
  - `sambucus_ebulus` | *Sambucus ebulus* | unranked | ap=tricol* | class=medium | mid=24.7µm | size_src=beug | sc={psilaat,reticulaat}
  - `verbascum_blattaria` | *Verbascum blattaria* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `verbascum_densiflorum` | *Verbascum densiflorum* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `pyracantha_coccin`–`pyracantha_coccinea` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `brassica_typ`: data/pollen.yaml:size; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm · `fallopia_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `koelreuteria_paniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `mercurialis_annua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C2 (n=9, mean_d=0.949, max_d=1.479) — ranks [2]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.3, 35.9)
- Shared sculpture tokens: —
- Members:
  - `prunus_pirus_typ` | *Prunus pirus* | rank=2 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={striaat}
  - `agrimonia_eupatoria` | *Agrimonia eupatoria* | unranked | ap=tricol* | class=medium | mid=33.5µm | size_src=yaml | sculpt_MASKED
  - `cotoneaster_integerrimus` | *Cotoneaster integerrimus* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={striaat}
  - `potentilla_norvegica` | *Potentilla norvegica* | unranked | ap=tricol* | class=medium | mid=31.6µm | size_src=yaml | sc={striaat}
  - `prunus_cerasifera` | *Prunus cerasifera* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={striaat}
  - `prunus_mahaleb` | *Prunus mahaleb* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={striaat}
  - `rosa_canina` | *Rosa canina* | unranked | ap=tricol* | class=medium | mid=33.4µm | size_src=yaml | sculpt_MASKED
  - `rosa_glauca` | *Rosa glauca* | unranked | ap=tricol* | class=medium | mid=31.3µm | size_src=yaml | sc={striaat}
  - `rosa_spinosissima` | *Rosa spinosissima* | unranked | ap=tricol* | class=medium | mid=33.4µm | size_src=yaml | sc={striaat}
- Closest pair evidence `cotoneaster_integerrimus`–`prunus_cerasifera` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `agrimonia_eupatoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cotoneaster_integerrimus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_norvegica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `prunus_cerasifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C3 (n=2, mean_d=1.125, max_d=1.125) — ranks [3]

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={psilaat,striaat}
  - `solanum_tuberosum` | *Solanum tuberosum* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `rubus_typ`–`solanum_tuberosum` (d=1.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `rubus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_tuberosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C4 (n=3, mean_d=0.549, max_d=0.778) — ranks [4]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.0)
- Shared sculpture tokens: echinaat
- Members:
  - `taraxacum_typ` | *Taraxacum typ* | rank=4 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={echinaat}
  - `senecio_aquaticus` | *Senecio aquaticus* | unranked | ap=tricol* | class=medium | mid=32.6µm | size_src=yaml | sc={echinaat}
  - `symphyotrichum_lanceolatum` | *Symphyotrichum lanceolatum* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `senecio_aquaticus`–`taraxacum_typ` (d=0.411): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.411}`
- Provenance (sample): `senecio_aquaticus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphyotrichum_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taraxacum_typ`: data/pollen.yaml:sculpture; data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm

### C5 (n=9, mean_d=1.144, max_d=1.692) — ranks [5]

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.1, 38.0)
- Shared sculpture tokens: —
- Members:
  - `centaurea_cyanus` | *Centaurea cyanus* | rank=5 | ap=tricol* | class=medium | mid=37.0µm | size_src=beug | path_gate=25–40 | sculpt_MASKED
  - `callicarpa_typ` | *Callicarpa typ* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={fijn,reticulaat}
  - `empetrum_nigrum` | *Empetrum nigrum* | unranked | ap=tricol* | class=medium | mid=38.0µm | size_src=yaml
  - `euphorbia_amygdaloides` | *Euphorbia amygdaloides* | unranked | ap=tricol* | class=medium | mid=36.1µm | size_src=yaml | sc={reticulaat}
  - `galeopsis_tetrahit` | *Galeopsis tetrahit* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `parthenocissus_typ` | *Parthenocissus typ* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={reticulaat}
  - `tilia_americana` | *Tilia americana* | unranked | ap=tricol* | class=medium | mid=37.9µm | size_src=yaml | sc={reticulaat}
  - `tilia_tomentosa` | *Tilia tomentosa* | unranked | ap=tricol* | class=medium | mid=36.8µm | size_src=yaml | sc={reticulaat}
  - `vicia_cracca` | *Vicia cracca* | unranked | ap=tricol* | class=medium | mid=36.7µm | size_src=yaml | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `callicarpa_typ`–`galeopsis_tetrahit` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `callicarpa_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_cyanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `empetrum_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:shape; data/pollen.yaml:ornamentation · `euphorbia_amygdaloides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C6 (n=3, mean_d=1.202, max_d=1.615) — ranks [6]

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 31.0)
- Shared sculpture tokens: fijn
- Members:
  - `trifolium_repens` | *Trifolium repens* | rank=6 | ap=tricol* | class=medium | mid=30.9µm | size_src=beug | path_gate=0–35 | yaml_size_MASKED | sc={fijn,reticulaat}
  - `rhinanthus_typ` | *Rhinanthus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `teucrium_chamae` | *Teucrium chamae* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={fijn,scabraat}
- Closest pair evidence `rhinanthus_typ`–`trifolium_repens` (d=0.591): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-trifolium.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.9, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.591}`
- Provenance (sample): `rhinanthus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `teucrium_chamae`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C7 (n=6, mean_d=1.288, max_d=1.525) — ranks [7, 14]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 20.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `rhamnus` | *Rhamnus* | rank=7 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `echium` | *Echium* | rank=14 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `arabis_procurrens` | *Arabis procurrens* | unranked | ap=tricol* | class=small | mid=19.5µm | size_src=yaml | sc={reticulaat}
  - `lepidium_sativum` | *Lepidium sativum* | unranked | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat}
  - `salix_purpurea` | *Salix purpurea* | unranked | ap=tricol* | class=small | mid=19.9µm | size_src=yaml | sc={reticulaat}
  - `tamarix_gallica` | *Tamarix gallica* | unranked | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `lepidium_sativum`–`tamarix_gallica` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `arabis_procurrens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `echium`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `lepidium_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rhamnus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse

### C8 (n=6, mean_d=1.008, max_d=1.625) — ranks [8, 18, 19]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.0)
- Shared sculpture tokens: —
- Members:
  - `aesculus` | *Aesculus* | rank=8 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={psilaat}
  - `raphanus_typ` | *Raphanus typ* | rank=18 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `verbascum` | *Verbascum* | rank=19 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `diplotaxis_tenuifolia` | *Diplotaxis tenuifolia* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
  - `erigeron_canaden` | *Erigeron canadensis* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={echinaat}
  - `solanum_lycopers` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml
- Closest pair evidence `diplotaxis_tenuifolia`–`raphanus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aesculus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `diplotaxis_tenuifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erigeron_canaden`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_typ`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse

### C9 (n=5, mean_d=1.195, max_d=1.619) — ranks [9]

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.4, 32.5)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); morph-bin group, not confirmed lookalike.
- Members:
  - `robinia` | *Robinia* | rank=9 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={scabraat}
  - `cytisus_typ` | *Cytisus typ* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={fijn,reticulaat,scabraat}
  - `eryngium_typ` | *Eryngium typ* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `hippophae_rhamnoides` | *Hippophae rhamnoides* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={reticulaat,scabraat}
  - `pimpinella_anisum` | *Pimpinella anisum* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `eryngium_typ`–`pimpinella_anisum` (d=0.735): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.735}`
- Provenance (sample): `cytisus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eryngium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hippophae_rhamnoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_anisum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C10 (n=7, mean_d=1.211, max_d=1.745) — ranks [10, 17]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.2)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `vicia_typ` | *Vicia typ* | rank=10 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
  - `parthenocissus` | *Parthenocissus* | rank=17 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
  - `euphorbia_cyparissias` | *Euphorbia cyparissias* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={reticulaat}
  - `glaucium_flavum` | *Glaucium flavum* | unranked | ap=tricol* | class=medium | mid=32.8µm | size_src=yaml | sc={reticulaat}
  - `sinapis_arvensis` | *Sinapis arvensis* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
  - `trifolium_fragiferum` | *Trifolium fragiferum* | unranked | ap=tricol* | class=medium | mid=33.2µm | size_src=yaml | sc={reticulaat}
  - `ulex_europaeus` | *Ulex europaeus* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `parthenocissus`–`ulex_europaeus` (d=0.233): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.233}`
- Provenance (sample): `euphorbia_cyparissias`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `glaucium_flavum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `parthenocissus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `sinapis_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C11 (n=4, mean_d=0.946, max_d=1.499) — ranks [11]

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.8, 33.1)
- Shared sculpture tokens: —
- Members:
  - `acer_platanoides` | *Acer platanoides* | rank=11 | ap=tricol* | class=medium | mid=33.1µm | size_src=yaml | sc={rugulaat,striaat}
  - `cotoneaster_intergerrimus` | *Cotoneaster intergerrimus* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sculpt_MASKED
  - `davidia_involucrata` | *Davidia involucrata* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={rugulaat}
  - `rubus_fruticosus` | *Rubus fruticosus* | unranked | ap=tricol* | class=medium | mid=32.8µm | size_src=yaml | sc={rugulaat}
- Closest pair evidence `cotoneaster_intergerrimus`–`davidia_involucrata` (d=0.650): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'masked_conflict', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.65}`
- Provenance (sample): `acer_platanoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cotoneaster_intergerrimus`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `davidia_involucrata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_fruticosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C12 (n=7, mean_d=1.009, max_d=1.733) — ranks [13]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.5, 19.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `salix_typ` | *Salix typ* | rank=13 | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat}
  - `alyssum_saxatile` | *Alyssum saxatile* | unranked | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat}
  - `ceanothus_americanus` | *Ceanothus americanus* | unranked | ap=tricol* | class=small | mid=19.4µm | size_src=yaml | sc={reticulaat}
  - `fallopia_baldschur` | *Fallopia baldschur* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
  - `hypericum_androsaemum` | *Hypericum androsaemum* | unranked | ap=tricol* | class=small | mid=18.8µm | size_src=yaml | sc={reticulaat}
  - `osmanthus_typ` | *Osmanthus typ* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
  - `thlaspi_arvense` | *Thlaspi arvense* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `fallopia_baldschur`–`salix_typ` (d=0.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.245}`
- Provenance (sample): `alyssum_saxatile`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ceanothus_americanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `fallopia_baldschur`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_androsaemum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C13 (n=8, mean_d=1.144, max_d=1.725) — ranks [15]

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.9, 37.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_typ` | *Tilia typ* | rank=15 | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `aconitum_typ` | *Aconitum typ* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `erophila_verna` | *Erophila verna* | unranked | ap=tricol* | class=medium | mid=34.9µm | size_src=yaml | sc={reticulaat}
  - `galeopsis_segetum` | *Galeopsis segetum* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `helleborus_viridis_ssp_occidentalis` | *Helleborus viridis* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
  - `lamium_amplexicaule` | *Lamium amplexicaule* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
  - `oxalis_corniculata` | *Oxalis corniculata* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={reticulaat}
  - `stachys_palustris` | *Stachys palustris* | unranked | ap=tricol* | class=medium | mid=36.2µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `stachys_palustris`–`tilia_typ` (d=0.425): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.425}`
- Provenance (sample): `aconitum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erophila_verna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galeopsis_segetum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_viridis_ssp_occidentalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C14 (n=7, mean_d=1.196, max_d=1.747) — ranks [16]

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.8, 34.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `colutea_arborescens` | *Colutea arborescens* | unranked | ap=tricol* | class=medium | mid=34.1µm | size_src=yaml | sc={reticulaat}
  - `ligustrum_vulgare` | *Ligustrum vulgare* | unranked | ap=tricol* | class=medium | mid=34.2µm | size_src=beug | sc={reticulaat}
  - `lupinus_angustifolius` | *Lupinus angustifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={reticulaat}
  - `onobrychis_viciifolia` | *Onobrychis viciifolia* | unranked | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={reticulaat}
  - `trifolium_dubium` | *Trifolium dubium* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=yaml | sc={reticulaat}
  - `vicia_sepium` | *Vicia sepium* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `trifolium_dubium`–`vicia_sepium` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `colutea_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ligustrum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lupinus_angustifolius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onobrychis_viciifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C15 (n=3, mean_d=1.138, max_d=1.245) — ranks [20]

- Shared aperture: tricol*
- Size classes: small; mid range: (20.0, 20.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `lotus` | *Lotus* | rank=20 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={psilaat}
  - `aquilegia_vulgaris` | *Aquilegia vulgaris* | unranked | ap=tricol* | class=small | mid=20.5µm | size_src=yaml | sc={psilaat}
  - `sedum_typ` | *Sedum typ* | unranked | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={psilaat,striaat}
- Closest pair evidence `aquilegia_vulgaris`–`lotus` (d=1.045): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `aquilegia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lotus`: data/pollen.yaml:controlled.sculptuur; data/pollen.yaml:controlled.apertuur; data/pollen.yaml:controlled.vorm; data/pollen.yaml:controlled.grootteklasse · `sedum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C16 (n=4, mean_d=0.994, max_d=1.359) — ranks [21, 40]

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.5, 32.6)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `lamium_typ` | *Lamium typ* | rank=21 | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={psilaat,scabraat}
  - `polygonum_aviculare` | *Polygonum aviculare* | rank=40 | ap=tricol* | class=medium | mid=32.6µm | size_src=beug | sc={psilaat,scabraat}
  - `nicandra_physalodes` | *Nicandra physalodes* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=beug | sc={psilaat,scabraat}
  - `photinia_typ` | *Photinia typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `lamium_typ`–`photinia_typ` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.495}`
- Provenance (sample): `lamium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nicandra_physalodes`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug14-tricolporatae-ps.json · `photinia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polygonum_aviculare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C17 (n=3, mean_d=1.244, max_d=1.603) — ranks [26]

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.4, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ailanthus_altissima` | *Ailanthus altissima* | rank=26 | ap=tricol* | class=medium | mid=31.5µm | size_src=beug | sc={reticulaat,rugulaat,striaat}
  - `medicago_lupulina` | *Medicago lupulina* | unranked | ap=tricol* | class=medium | mid=31.4µm | size_src=beug | sc={reticulaat,rugulaat}
  - `rhus_typhina` | *Rhus typhina* | unranked | ap=tricol* | class=medium | mid=32.4µm | size_src=yaml | sc={reticulaat,striaat}
- Closest pair evidence `ailanthus_altissima`–`medicago_lupulina` (d=0.899): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug19-tricolporatae-str-rhus.json vs beug:docs/keys/beug/beug23-tricolporoidatae-ret-medicago-lupulina.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.899}`
- Provenance (sample): `ailanthus_altissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `medicago_lupulina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rhus_typhina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C18 (n=3, mean_d=0.661, max_d=0.929) — ranks [29]

- Shared aperture: tricol*
- Size classes: small; mid range: (18.4, 21.8)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ononis` | *Ononis natrix* | rank=29 | ap=tricol* | class=small | mid=18.4µm | size_src=yaml | sc={reticulaat}
  - `melilotus_albus` | *Melilotus albus* | unranked | ap=tricol* | class=small | mid=21.8µm | size_src=yaml | sc={reticulaat}
  - `ononis_natrix` | *Ononis natrix* | unranked | ap=tricol* | class=small | mid=18.4µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ononis`–`ononis_natrix` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'prolaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `melilotus_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ononis_natrix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C19 (n=4, mean_d=0.407, max_d=0.435) — ranks [33]

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.0, 35.2)
- Shared sculpture tokens: echinaat
- Members:
  - `helianthus_annuus` | *Helianthus annuus* | rank=33 | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `inula_salicina` | *Inula salicina* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `senecio_vulgaris` | *Senecio vulgaris* | unranked | ap=tricol* | class=medium | mid=35.0µm | size_src=yaml | sc={echinaat}
  - `xeranthemum_annuum` | *Xeranthemum annuum* | unranked | ap=tricol* | class=medium | mid=35.2µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `helianthus_annuus`–`inula_salicina` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `helianthus_annuus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_salicina`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `senecio_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `xeranthemum_annuum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C20 (n=2, mean_d=0.749, max_d=0.749) — ranks [34]

- Shared aperture: tricol*
- Size classes: large; mid range: (60.2, 62.8)
- Shared sculpture tokens: psilaat, reticulaat, scabraat, verrucaat
- Members:
  - `cornus_sanguinea` | *Cornus sanguinea* | rank=34 | ap=tricol* | class=large | mid=62.8µm | size_src=beug | yaml_size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
  - `centaurea_montana` | *Centaurea montana* | unranked | ap=tricol* | class=large | mid=60.2µm | size_src=beug | yaml_size_MASKED | sc={psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `centaurea_montana`–`cornus_sanguinea` (d=0.749): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolporatae-ps.json vs beug:docs/keys/beug/beug15-tricolporoidatae-ps-cornus.json', 'size_class': 'same large', 'size_mid_gap_um': 2.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.749}`
- Provenance (sample): `centaurea_montana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_sanguinea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C21 (n=5, mean_d=0.840, max_d=1.387) — ranks [44]

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.1, 40.4)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_typ` | *Crataegus typ* | rank=44 | ap=tricol* | class=medium | mid=40.0µm | size_src=yaml | sc={striaat}
  - `acer_monspessulanum` | *Acer monspessulanum* | unranked | ap=tricol* | class=medium | mid=39.1µm | size_src=yaml | sc={striaat}
  - `acer_opalus` | *Acer opalus* | unranked | ap=tricol* | class=medium | mid=40.4µm | size_src=yaml | sc={striaat}
  - `prunus_armeniaca` | *Prunus armeniaca* | unranked | ap=tricol* | class=medium | mid=39.1µm | size_src=yaml | sc={striaat}
  - `prunus_cerasus` | *Prunus cerasus* | unranked | ap=tricol* | class=medium | mid=40.4µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_opalus`–`crataegus_typ` (d=0.471): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.471}`
- Provenance (sample): `acer_monspessulanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `acer_opalus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crataegus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_armeniaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C22 (n=2, mean_d=1.523, max_d=1.523) — ranks [45]

- Shared aperture: tricol*
- Size classes: large; mid range: (45.1, 45.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | class=large | mid=45.3µm | size_src=beug | path_gate=42–50 | yaml_size_MASKED | sc={grof,reticulaat}
  - `cistus_albidus` | *Cistus albidus* | unranked | ap=tricol* | class=large | mid=45.1µm | size_src=beug | sc={reticulaat}
- Closest pair evidence `cistus_albidus`–`trifolium_pratense` (d=1.523): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug22-tricolporatae-ret-cistus-albidus.json vs beug:docs/keys/beug/beug22-tricolporatae-ret-trifolium.json', 'size_class': 'same large', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.75, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.523}`
- Provenance (sample): `cistus_albidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `trifolium_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C23 (n=4, mean_d=1.252, max_d=1.663) — ranks [49]

- Shared aperture: peripor*
- Size classes: medium; mid range: (34.8, 36.6)
- Shared sculpture tokens: —
- Members:
  - `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | size_src=yaml | sc={baculaat,reticulaat,verrucaat}
  - `cerastium_fontanum` | *Cerastium fontanum* | unranked | ap=peripor* | class=medium | mid=36.0µm | size_src=yaml | sc={reticulaat}
  - `ribes_nigrum` | *Ribes nigrum* | unranked | ap=peripor* | class=medium | mid=35.2µm | size_src=yaml
  - `stellaria_graminea` | *Stellaria graminea* | unranked | ap=peripor* | class=medium | mid=36.6µm | size_src=yaml
- Closest pair evidence `ribes_nigrum`–`silene_flos_cuculi` (d=1.033): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.033}`
- Provenance (sample): `cerastium_fontanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_nigrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `silene_flos_cuculi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `stellaria_graminea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C24 (n=10, mean_d=1.249, max_d=1.641) — ranks [52]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (33.0, 35.6)
- Shared sculpture tokens: —
- Members:
  - `impatiens_glandulifera` | *Impatiens glandulifera* | rank=52 | ap=stephanocol* | class=medium | mid=35.5µm | size_src=yaml | sc={reticulaat}
  - `borago_officinalis` | *Borago officinalis* | unranked | ap=stephanocol* | class=medium | mid=34.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `impatiens_balsamina` | *Impatiens balsamina* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `lycopus_europaeus` | *Lycopus europaeus* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml
  - `mentha_aquatica` | *Mentha aquatica* | unranked | ap=stephanocol* | class=medium | mid=35.0µm | size_src=yaml | sc={reticulaat}
  - `origanum_vulgare` | *Origanum vulgare* | unranked | ap=stephanocol* | class=medium | mid=33.0µm | size_src=yaml | sc={reticulaat}
  - `salvia_nemorosa` | *Salvia nemorosa* | unranked | ap=stephanocol* | class=medium | mid=33.2µm | size_src=yaml
  - `skimmia_typ` | *Skimmia typ* | unranked | ap=stephanocol* | class=medium | mid=33.5µm | size_src=yaml | sc={reticulaat,striaat}
  - `thymus_praecox` | *Thymus praecox* | unranked | ap=stephanocol* | class=medium | mid=34.4µm | size_src=yaml
  - `thymus_serpyllum` | *Thymus serpyllum* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `impatiens_balsamina`–`mentha_aquatica` (d=0.937): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `borago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_balsamina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `impatiens_glandulifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycopus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C25 (n=6, mean_d=1.045, max_d=1.375) — ranks [53]

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 18.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `filipendula_typ` | *Filipendula typ* | rank=53 | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `alyssum_typ` | *Alyssum typ* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
  - `daucus_carota` | *Daucus carota* | unranked | ap=tricol* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `limnanthes_douglasii` | *Limnanthes douglasii* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat,scabraat,striaat}
  - `linaria_vulg` | *Linaria vulg* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
  - `linaria_vulgaris` | *Linaria vulgaris* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `linaria_vulg`–`linaria_vulgaris` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `alyssum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `daucus_carota`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `limnanthes_douglasii`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C26 (n=2, mean_d=0.861, max_d=0.861) — ranks [71]

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.6, 26.0)
- Shared sculpture tokens: psilaat, reticulaat, scabraat
- Members:
  - `cornus_mas` | *Cornus mas* | rank=71 | ap=tricol* | class=medium | mid=24.6µm | size_src=beug | sc={psilaat,reticulaat,scabraat}
  - `carum_carvi` | *Carum carvi* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `carum_carvi`–`cornus_mas` (d=0.861): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug15-tricolporoidatae-ps-cornus.json', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.5, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.861}`
- Provenance (sample): `carum_carvi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cornus_mas`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C27 (n=5, mean_d=0.854, max_d=1.619) — ranks [75]

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.9, 44.0)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** carduus_defloratus ↔ carduus_typ
- Members:
  - `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=42.9µm | size_src=beug | path_gate=25–40 | sc={echinaat,scabraat}
  - `carduus_defloratus` | *Carduus defloratus* | unranked | ap=tricol* | class=medium | mid=43.5µm | size_src=yaml | sc={echinaat}
  - `carduus_typ` | *Carduus typ* | unranked | ap=tricol* | class=medium | mid=43.5µm | size_src=yaml | sc={echinaat}
  - `inula_helenium` | *Inula helenium* | unranked | ap=tricol* | class=medium | mid=44.0µm | size_src=yaml | sc={echinaat}
  - `tragopogon_typ` | *Tragopogon typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `carduus_defloratus`–`carduus_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_defloratus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carduus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `centaurea_jacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `inula_helenium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C28 (n=3, mean_d=1.368, max_d=1.591) — ranks [76]

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 39.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | size_src=yaml | sc={grof,reticulaat}
  - `oxalis_typ` | *Oxalis typ* | unranked | ap=stephanocol* | class=medium | mid=39.0µm | size_src=yaml | sc={reticulaat}
  - `rosmarinus_officinalis` | *Rosmarinus officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `impatiens_parviflora`–`oxalis_typ` (d=1.149): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.149}`
- Provenance (sample): `impatiens_parviflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `oxalis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rosmarinus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C29 (n=29, mean_d=1.467, max_d=1.575)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.3, 32.2)
- Shared sculpture tokens: echinaat
- Members:
  - `achillea_millefolium` | *Achillea millefolium* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
  - `anthemis_tinctoria` | *Anthemis tinctoria* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
  - `aster_alpinus` | *Aster alpinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | size_src=yaml | sc={echinaat}
  - `bidens_ferulifolia` | *Bidens ferulifolia* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={echinaat}
  - `buphthalmum_salicifolium` | *Buphthalmum salicifolium* | unranked | ap=tricol* | class=medium | mid=31.1µm | size_src=yaml | sc={echinaat}
  - `cirsium_dissectum` | *Cirsium dissectum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_oleraceum` | *Cirsium oleraceum* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_palustre` | *Cirsium palustre* | unranked | ap=tricol* | sc={echinaat}
  - `cirsium_rivulare` | *Cirsium rivulare* | unranked | ap=tricol* | sc={echinaat}
  - `dipsacus_sylvester` | *Dipsacus Sylvester* | unranked | ap=tricol* | sc={echinaat}
  - `erigeron_annuus` | *Erigeron annuus* | unranked | ap=tricol* | sc={echinaat}
  - `galinsoga_ciliata` | *Galinsoga ciliata* | unranked | ap=tricol* | sc={echinaat}
  - `helichrysum_arenarium` | *Helichrysum arenarium* | unranked | ap=tricol* | sc={echinaat}
  - `inula_conyzae` | *Inula conyzae* | unranked | ap=tricol* | sc={echinaat}
  - `leucanthemum_vulgare` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={echinaat}
  - `lonicera_fragrantissima` | *Lonicera Fragrantissima* | unranked | ap=tricol* | sc={echinaat}
  - `lonicera_japonica` | *Lonicera Japonica* | unranked | ap=tricol* | sc={echinaat}
  - `petasites_albus` | *Petasites albus* | unranked | ap=tricol* | sc={echinaat}
  - `pulicaria_dysenterica` | *Pulicaria dysenterica* | unranked | ap=tricol* | sc={echinaat}
  - `senecio_cineraria` | *Senecio Cineraria* | unranked | ap=tricol* | sc={echinaat}
  - `senecio_squalidus` | *Senecio squalidus* | unranked | ap=tricol* | class=medium | mid=32.2µm | size_src=yaml | sc={echinaat}
  - `silybum_marianum` | *Silybum marianum* | unranked | ap=tricol* | sc={echinaat}
  - `tanacetum_corymbosum` | *Tanacetum corymbosum* | unranked | ap=tricol* | sc={echinaat}
  - `tanacetum_vulgare` | *Tanacetum vulgare* | unranked | ap=tricol* | class=medium | mid=30.3µm | size_src=yaml | sc={echinaat}
  - `telekia_speciosa` | *Telekia speciosa* | unranked | ap=tricol* | sc={echinaat}
  - `tephroseris_palustris` | *Tephroseris palustris* | unranked | ap=tricol* | sc={echinaat}
  - `tripleurospermum_maritimum` | *Tripleurospermum maritimum* | unranked | ap=tricol* | sc={echinaat}
  - `tripolium_pannonicum` | *Tripolium pannonicum* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={echinaat}
  - `tussilago_farfara` | *Tussilago farfara* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `achillea_millefolium`–`anthemis_tinctoria` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `achillea_millefolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `anthemis_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `aster_alpinus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `bidens_ferulifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C30 (n=13, mean_d=1.242, max_d=1.728)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.5, 29.0)
- Shared sculpture tokens: —
- Members:
  - `alyssum_montanum` | *Alyssum montanum* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={microreticulaat,reticulaat}
  - `alyssum_repens` | *Alyssum repens* | unranked | ap=tricol* | class=medium | mid=27.5µm | size_src=yaml | sc={reticulaat}
  - `anacardium_occidentale` | *Anacardium occidentale* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={reticulaat}
  - `brassica_rapa` | *Brassica rapa* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
  - `cardamine_flexuosa` | *Cardamine flexuosa* | unranked | ap=tricol* | class=medium | mid=28.1µm | size_src=yaml | sc={reticulaat}
  - `chelidonium_majus` | *Chelidonium majus* | unranked | ap=tricol* | class=medium | mid=27.7µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,scabraat}
  - `helleborus_foetidus` | *Helleborus foetidus* | unranked | ap=tricol* | class=medium | mid=26.9µm | size_src=beug | sc={microreticulaat,reticulaat}
  - `lamium_purpureum` | *Lamium purpureum* | unranked | ap=tricol* | class=medium | mid=27.1µm | size_src=yaml | sc={reticulaat}
  - `marrubium_vulgare` | *Marrubium vulgare* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
  - `olea_europaea` | *Olea europaea* | unranked | ap=tricol* | class=medium | mid=27.7µm | size_src=beug | yaml_size_MASKED | sc={echinaat,microreticulaat,reticulaat,scabraat}
  - `rosa_rubiginosa` | *Rosa rubiginosa* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sculpt_MASKED
  - `salix_dasyclados` | *Salix dasyclados* | unranked | ap=tricol* | class=medium | mid=28.3µm | size_src=yaml | sc={reticulaat}
  - `vitex_agnus_castus` | *Vitex agnus* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=beug | sc={microreticulaat,reticulaat}
- Closest pair evidence `olea_europaea`–`rosa_rubiginosa` (d=0.472): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-olea.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.472}`
- Provenance (sample): `alyssum_montanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `alyssum_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `anacardium_occidentale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `brassica_rapa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C31 (n=11, mean_d=1.137, max_d=1.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 27.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** crambe_maritima ↔ crambe_typ
- Members:
  - `brassica_napus` | *Brassica napus* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={reticulaat}
  - `brassica_oleracea` | *Brassica oleracea* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={reticulaat}
  - `bunias_orientalis` | *Bunias orientalis* | unranked | ap=tricol* | class=medium | mid=25.1µm | size_src=yaml | sc={reticulaat}
  - `crambe_maritima` | *Crambe maritima* | unranked | ap=tricol* | class=medium | mid=25.4µm | size_src=yaml | sc={reticulaat}
  - `crambe_typ` | *Crambe typ* | unranked | ap=tricol* | class=medium | mid=25.4µm | size_src=yaml | sc={reticulaat}
  - `euodia_hupehensis` | *Euodia hupehensis* | unranked | ap=tricol* | class=medium | mid=25.5µm | size_src=yaml | sc={grof,reticulaat}
  - `hesperis_matronalis` | *Hesperis matronalis* | unranked | ap=tricol* | class=medium | mid=24.7µm | size_src=yaml | sc={reticulaat}
  - `iberis_amara` | *Iberis amara* | unranked | ap=tricol* | class=medium | mid=25.7µm | size_src=yaml | sc={reticulaat}
  - `odontites_vernus` | *Odontites vernus* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `salix_cinerea` | *Salix cinerea* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={reticulaat}
  - `salix_pentandra` | *Salix pentandra* | unranked | ap=tricol* | class=medium | mid=25.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `crambe_maritima`–`crambe_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `brassica_napus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `brassica_oleracea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `bunias_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `crambe_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C32 (n=11, mean_d=0.742, max_d=1.567)

- Shared aperture: tricol*
- Size classes: medium; mid range: (33.5, 34.5)
- Shared sculpture tokens: —
- Members:
  - `calendula_officinalis` | *Calendula officinalis* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
  - `chrysanthemum_segetum` | *Chrysanthemum segetum* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={echinaat}
  - `doronicum_pardalianches` | *Doronicum pardalianches* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={echinaat}
  - `helminthotheca_echioides` | *Helminthotheca echioides* | unranked | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={echinaat}
  - `inula_britannica` | *Inula britannica* | unranked | ap=tricol* | class=medium | mid=34.1µm | size_src=yaml | sc={echinaat}
  - `inula_ensifolia` | *Inula ensifolia* | unranked | ap=tricol* | class=medium | mid=33.5µm | size_src=yaml | sc={echinaat}
  - `quercus_robur` | *Quercus robur* | unranked | ap=tricol* | class=medium | mid=33.7µm | size_src=yaml | sc={echinaat,psilaat,reticulaat}
  - `sanguisorba_minor` | *Sanguisorba minor* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=beug | yaml_size_MASKED | sculpt_MASKED
  - `senecio_erucifolius` | *Senecio erucifolius* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
  - `tagetes_erecta` | *Tagetes erecta* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml | sc={echinaat}
  - `vaccinium_vitis` | *Vaccinium vitis* | unranked | ap=tricol* | class=medium | mid=34.0µm | size_src=yaml
- Closest pair evidence `calendula_officinalis`–`senecio_erucifolius` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `calendula_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chrysanthemum_segetum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `doronicum_pardalianches`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helminthotheca_echioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C33 (n=11, mean_d=1.249, max_d=1.749)

- Shared aperture: tricol*
- Size classes: medium; mid range: (21.3, 23.9)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cochlearia_officinalis_ssp_off` | *Cochlearia officinalis* | unranked | ap=tricol* | class=medium | mid=23.8µm | size_src=yaml | sc={reticulaat}
  - `leonurus_cardiaca` | *Leonurus cardiaca* | unranked | ap=tricol* | class=medium | mid=21.6µm | size_src=yaml | sc={reticulaat}
  - `lunaria_annua` | *Lunaria annua* | unranked | ap=tricol* | class=medium | mid=22.1µm | size_src=yaml | sc={reticulaat}
  - `salix_alba_var_tristis` | *Salix alba var. tristis* | unranked | ap=tricol* | class=medium | mid=23.5µm | size_src=yaml | sc={reticulaat}
  - `salix_aurita` | *Salix aurita* | unranked | ap=tricol* | class=medium | mid=22.5µm | size_src=yaml | sc={reticulaat}
  - `salix_caprea` | *Salix caprea* | unranked | ap=tricol* | class=medium | mid=21.5µm | size_src=yaml | sc={reticulaat}
  - `salix_daphnoides` | *Salix daphnoides* | unranked | ap=tricol* | class=medium | mid=23.9µm | size_src=yaml | sc={reticulaat}
  - `salix_fragilis` | *Salix fragilis* | unranked | ap=tricol* | class=medium | mid=23.5µm | size_src=yaml | sc={reticulaat}
  - `salix_repens` | *Salix repens* | unranked | ap=tricol* | class=medium | mid=23.4µm | size_src=yaml | sc={reticulaat}
  - `salix_viminalis` | *Salix viminalis* | unranked | ap=tricol* | class=medium | mid=22.9µm | size_src=yaml | sc={reticulaat}
  - `trollius_europaeus` | *Trollius europaeus* | unranked | ap=tricol* | class=medium | mid=21.3µm | size_src=beug | sc={reticulaat,striaat}
- Closest pair evidence `salix_alba_var_tristis`–`salix_fragilis` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `cochlearia_officinalis_ssp_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `leonurus_cardiaca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lunaria_annua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `salix_alba_var_tristis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C34 (n=11, mean_d=1.535, max_d=1.575)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.3, 22.2)
- Shared sculpture tokens: striaat
- Members:
  - `crataegus_laevigata` | *Crataegus laevigata* | unranked | ap=tricol* | sc={striaat}
  - `cydonia_oblonga` | *Cydonia oblonga* | unranked | ap=tricol* | sc={striaat}
  - `potentilla_fruticosa` | *Potentilla fruticosa* | unranked | ap=tricol* | class=small | mid=19.3µm | size_src=yaml | sc={striaat}
  - `potentilla_palustris` | *Potentilla palustris* | unranked | ap=tricol* | sc={striaat}
  - `prunus_dulcis` | *Prunus dulcis* | unranked | ap=tricol* | sc={striaat}
  - `prunus_persica` | *Prunus persica* | unranked | ap=tricol* | sc={striaat}
  - `securigera_varia_coronilla_varia` | *Securigera varia* | unranked | ap=tricol* | sc={striaat}
  - `sedum_album` | *Sedum album* | unranked | ap=tricol* | class=small | mid=20.4µm | size_src=yaml | sc={striaat}
  - `sedum_telephium` | *Sedum telephium* | unranked | ap=tricol* | class=small | mid=22.2µm | size_src=yaml | sc={striaat}
  - `sorbus_aria` | *Sorbus aria* | unranked | ap=tricol* | sc={striaat}
  - `waldsteinia_ternata` | *Waldsteinia ternata* | unranked | ap=tricol* | sc={striaat}
- Closest pair evidence `potentilla_fruticosa`–`sedum_album` (d=0.627): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 1.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.627}`
- Provenance (sample): `crataegus_laevigata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cydonia_oblonga`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_fruticosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_palustris`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C35 (n=9, mean_d=0.791, max_d=1.721)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.9, 26.3)
- Shared sculpture tokens: striaat
- Members:
  - `acer_palmatum` | *Acer palmatum* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
  - `aesculus_hippoca` | *Aesculus hippoca* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
  - `fragaria_moschata` | *Fragaria moschata* | unranked | ap=tricol* | class=medium | mid=25.6µm | size_src=beug | sc={striaat}
  - `hippocrepis_comosa` | *Hippocrepis comosa* | unranked | ap=tricol* | class=medium | mid=26.3µm | size_src=yaml | sc={striaat}
  - `potentilla_aurea` | *Potentilla aurea* | unranked | ap=tricol* | class=medium | mid=23.9µm | size_src=yaml | sc={striaat}
  - `potentilla_erecta` | *Potentilla erecta* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={striaat}
  - `potentilla_grandiflora` | *Potentilla grandiflora* | unranked | ap=tricol* | class=medium | mid=24.8µm | size_src=yaml | sc={striaat}
  - `rubus_caesius` | *Rubus caesius* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={striaat}
  - `sempervivum_tectorum` | *Sempervivum tectorum* | unranked | ap=tricol* | class=medium | mid=24.1µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_palmatum`–`aesculus_hippoca` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `acer_palmatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `aesculus_hippoca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fragaria_moschata`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug20-tricolporoidatae-str-potentilla.json · `hippocrepis_comosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C36 (n=9, mean_d=1.191, max_d=1.745)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 23.0)
- Shared sculpture tokens: —
- Members:
  - `ambrosia_artemisiifolia` | *Ambrosia artemisiifolia* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={echinaat}
  - `bidens_typ` | *Bidens typ* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={echinaat}
  - `helenium_autumn` | *Helenium autumn* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={echinaat}
  - `hypericum_polyph` | *Hypericum polyph* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml
  - `lysimachia_typ` | *Lysimachia typ* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `prunus_serotina` | *Prunus serotina* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={psilaat}
  - `raphanus_raph` | *Raphanus raph* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `raphanus_raphanistrum` | *Raphanus raphanistrum* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat}
  - `xanthium_italicum` | *Xanthium italicum* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={scabraat}
- Closest pair evidence `ambrosia_artemisiifolia`–`bidens_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `ambrosia_artemisiifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `bidens_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `helenium_autumn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_polyph`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C37 (n=9, mean_d=0.500, max_d=0.807)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.7, 26.5)
- Shared sculpture tokens: echinaat
- Members:
  - `aster_typ` | *Aster typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `erigeron_acer` | *Erigeron acer* | unranked | ap=tricol* | class=medium | mid=24.7µm | size_src=yaml | sc={echinaat}
  - `hieracium_typ` | *Hieracium typ* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `lampsana_commu` | *Lampsana commu* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={echinaat}
  - `lampsana_communis` | *Lampsana communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={echinaat}
  - `matricaria_chamo` | *Matricaria chamo* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `matricaria_chamomilla` | *Matricaria chamomilla* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
  - `matricaria_recutita` | *Matricaria Recutita* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=yaml | sc={echinaat}
  - `senecio_inaequalis` | *Senecio inaequalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `aster_typ`–`matricaria_chamo` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aster_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erigeron_acer`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hieracium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lampsana_commu`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C38 (n=9, mean_d=1.135, max_d=1.497)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.6, 29.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `laburnum_anagyroides` | *Laburnum anagyroides* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={reticulaat}
  - `lysimachia_vulgaris` | *Lysimachia vulgaris* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=beug | path_gate=0–35 | sc={reticulaat}
  - `ononis_repens_ssp_repens` | *Ononis repens* | unranked | ap=tricol* | class=medium | mid=29.2µm | size_src=yaml | sc={reticulaat}
  - `ononis_spinosa` | *Ononis spinosa* | unranked | ap=tricol* | class=medium | mid=27.8µm | size_src=yaml | sc={reticulaat}
  - `ptelea_trifoliata` | *Ptelea trifoliata* | unranked | ap=tricol* | class=medium | mid=29.3µm | size_src=beug | path_gate=25–32 | sc={microreticulaat,reticulaat}
  - `scrophularia_auriculata` | *Scrophularia auriculata* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `scrophularia_umbrosa` | *Scrophularia umbrosa* | unranked | ap=tricol* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat}
  - `verbascum_phlomoides` | *Verbascum phlomoides* | unranked | ap=tricol* | class=medium | mid=28.2µm | size_src=yaml | sc={reticulaat}
  - `viburnum_lantana` | *Viburnum lantana* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=beug | sc={reticulaat}
- Closest pair evidence `laburnum_anagyroides`–`viburnum_lantana` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-viburnum.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `laburnum_anagyroides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lysimachia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ononis_repens_ssp_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ononis_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C39 (n=7, mean_d=0.628, max_d=0.950)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.7, 29.4)
- Shared sculpture tokens: —
- Members:
  - `aesculus_hippocastanum` | *Aesculus hippocastanum* | unranked | ap=tricol* | class=medium | mid=28.2µm | size_src=beug | sculpt_MASKED
  - `lycium_barbarum` | *Lycium barbarum* | unranked | ap=tricol* | class=medium | mid=28.1µm | size_src=yaml | sc={striaat}
  - `potentilla_recta` | *Potentilla recta* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={striaat}
  - `rosa_arvensis` | *Rosa arvensis* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={striaat}
  - `rosa_majalis` | *Rosa majalis* | unranked | ap=tricol* | class=medium | mid=28.9µm | size_src=yaml | sc={striaat}
  - `rosa_tomentosa` | *Rosa tomentosa* | unranked | ap=tricol* | class=medium | mid=27.7µm | size_src=yaml | sc={striaat}
  - `rosa_villosa` | *Rosa villosa* | unranked | ap=tricol* | class=medium | mid=28.9µm | size_src=yaml | sc={striaat}
- Closest pair evidence `rosa_majalis`–`rosa_villosa` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.375}`
- Provenance (sample): `aesculus_hippocastanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lycium_barbarum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C40 (n=7, mean_d=0.588, max_d=1.569)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.5, 30.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `aralia_elata` | *Aralia elata* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `cakile_maritima` | *Cakile maritima* | unranked | ap=tricol* | class=medium | mid=27.5µm | size_src=yaml | sc={reticulaat}
  - `corylopsis_parcifl` | *Corylopsis parcifl* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={reticulaat}
  - `ricinus_communis` | *Ricinus communis* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `scrophularia_nodosa` | *Scrophularia nodosa* | unranked | ap=tricol* | class=medium | mid=28.2µm | size_src=yaml | sc={reticulaat}
  - `viburnum_opulus` | *Viburnum opulus* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=beug | yaml_size_MASKED | sc={reticulaat}
  - `viburnum_tinus` | *Viburnum tinus* | unranked | ap=tricol* | class=medium | mid=30.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `aralia_elata`–`ricinus_communis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `aralia_elata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cakile_maritima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_parcifl`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ricinus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C41 (n=7, mean_d=1.336, max_d=1.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.3, 31.9)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `capsicum_annuum` | *Capsicum annuum* | unranked | ap=tricol* | class=medium | mid=29.5µm | size_src=yaml | sc={psilaat,reticulaat}
  - `cytisus_scoparius` | *Cytisus scoparius* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={psilaat}
  - `levisticum_officinale` | *Levisticum officinale* | unranked | ap=tricol* | class=medium | mid=29.3µm | size_src=beug | sc={psilaat}
  - `malus_typ` | *Malus typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={psilaat,rugulaat}
  - `medicago_falcata` | *Medicago falcata* | unranked | ap=tricol* | class=medium | mid=31.9µm | size_src=yaml | sc={psilaat}
  - `ornithopus_sativus` | *Ornithopus sativus* | unranked | ap=tricol* | class=medium | mid=31.1µm | size_src=yaml | sc={psilaat}
  - `solanum_nigrum_ssp_nigrum` | *Solanum nigrum* | unranked | ap=tricol* | class=medium | mid=29.8µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `capsicum_annuum`–`cytisus_scoparius` (d=0.983): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.983}`
- Provenance (sample): `capsicum_annuum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cytisus_scoparius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `levisticum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `malus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C42 (n=7, mean_d=0.878, max_d=1.125)

- Shared aperture: tricol*
- Size classes: small; mid range: (24.0, 24.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `clethra_alnifolia` | *Clethra alnifolia* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `digitalis_purpurea` | *Digitalis purpurea* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `hedysarum_corona` | *Hedysarum coronarium* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
  - `polygonum_convol` | *Fallopia convolvulus* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
  - `rhus_chinensis` | *Rhus chinensis* | unranked | ap=tricol* | class=small | mid=24.5µm | size_src=yaml | sc={reticulaat}
  - `rumex_obtusifolius` | *Rumex obtusifolius* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
  - `sulla_coronaria` | *Sulla coronaria* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `polygonum_convol`–`rumex_obtusifolius` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `clethra_alnifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `digitalis_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hedysarum_corona`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `polygonum_convol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C43 (n=7, mean_d=1.189, max_d=1.709)

- Shared aperture: tricol*
- Size classes: small; mid range: (20.5, 21.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `erysimum_cheiranthoides` | *Erysimum cheiranthoides* | unranked | ap=tricol* | class=small | mid=20.6µm | size_src=yaml | sc={reticulaat}
  - `hamamelis_japonica` | *Hamamelis japonica* | unranked | ap=tricol* | class=small | mid=21.3µm | size_src=yaml | sc={reticulaat}
  - `ornithopus_perpus` | *Ornithopus perpus* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `ornithopus_perpusillus` | *Ornithopus perpusillus* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `reseda_luteola` | *Reseda luteola* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `rhamnus_cathartica` | *Rhamnus cathartica* | unranked | ap=tricol* | class=small | mid=20.5µm | size_src=yaml | sc={reticulaat,rugulaat}
  - `salix_triandra` | *Salix triandra* | unranked | ap=tricol* | class=small | mid=20.9µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `ornithopus_perpus`–`ornithopus_perpusillus` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `erysimum_cheiranthoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `hamamelis_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `ornithopus_perpus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ornithopus_perpusillus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C44 (n=6, mean_d=1.324, max_d=1.717)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 34.3)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `aconitum_napellus` | *Aconitum napellus* | unranked | ap=tricol* | class=medium | mid=32.8µm | size_src=yaml | sc={microreticulaat,psilaat}
  - `papaver_somniferum` | *Papaver somniferum* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={psilaat}
  - `veronica_officinalis` | *Veronica officinalis* | unranked | ap=tricol* | class=medium | mid=33.2µm | size_src=yaml | sc={psilaat}
  - `veronica_persica` | *Veronica persica* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={psilaat}
  - `viola_hirta` | *Viola hirta* | unranked | ap=tricol* | class=medium | mid=33.3µm | size_src=yaml | sc={psilaat}
  - `viola_riviniana` | *Viola riviniana* | unranked | ap=tricol* | class=medium | mid=34.3µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `veronica_officinalis`–`viola_hirta` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.937}`
- Provenance (sample): `aconitum_napellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `papaver_somniferum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_persica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C45 (n=6, mean_d=1.022, max_d=1.573)

- Shared aperture: monocol*
- Size classes: medium; mid range: (31.1, 33.8)
- Shared sculpture tokens: —
- Members:
  - `allium_porrum` | *Allium porrum* | unranked | ap=monocol* | class=medium | mid=33.3µm | size_src=yaml
  - `allium_scorodoprasum` | *Allium scorodoprasum* | unranked | ap=monocol* | class=medium | mid=33.8µm | size_src=yaml
  - `allium_ursinum` | *Allium ursinum* | unranked | ap=monocol* | class=medium | mid=32.8µm | size_src=beug | path_gate=25–200 | yaml_size_MASKED | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `asparagus_officinalis` | *Asparagus officinalis* | unranked | ap=monocol* | class=medium | mid=31.1µm | size_src=beug | path_gate=0–65 | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `butomus_umbellatus` | *Butomus umbellatus* | unranked | ap=monocol* | class=medium | mid=33.3µm | size_src=beug | path_gate=0–50 | sc={psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_aestivum` | *Leucojum aestivum* | unranked | ap=monocol* | class=medium | mid=32.2µm | size_src=beug | path_gate=25–200 | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `allium_ursinum`–`leucojum_aestivum` (d=0.269): `{'aperture': 'same monocol*', 'size_source': 'beug:docs/keys/beug/beug09-monocolpatae.json vs beug:docs/keys/beug/beug09-monocolpatae.json', 'path_gate': 'overlap 25.0–200.0 / 25.0–200.0', 'size_class': 'same medium', 'size_mid_gap_um': 0.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same monocol', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.269}`
- Provenance (sample): `allium_porrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_scorodoprasum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `allium_ursinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `asparagus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C46 (n=6, mean_d=0.567, max_d=1.478)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.0, 28.5)
- Shared sculpture tokens: echinaat
- Members:
  - `anthemis_nobilis` | *Anthemis nobilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `carpobrotis_edulis` | *Carpobrotis edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `carpobrotus_edulis` | *Carpobrotus edulis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
  - `senecio_jacobaea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={echinaat}
  - `senecio_jacobea` | *Senecio jacobaea* | unranked | ap=tricol* | class=medium | mid=28.5µm | size_src=yaml | sc={echinaat}
  - `taraxacum_officinale` | *Taraxacum officinale* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `carpobrotis_edulis`–`carpobrotus_edulis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `anthemis_nobilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotis_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carpobrotus_edulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_jacobaea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C47 (n=6, mean_d=0.791, max_d=1.179)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.6, 39.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arnica_montana` | *Arnica montana* | unranked | ap=tricol* | class=medium | mid=38.9µm | size_src=yaml | sc={echinaat}
  - `aster_sedifolius` | *Aster sedifolius* | unranked | ap=tricol* | class=medium | mid=36.2µm | size_src=yaml | sc={echinaat}
  - `cosmos_typ` | *Cosmos typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | size_src=yaml | sc={echinaat}
  - `senecio_ovatus` | *Senecio ovatus* | unranked | ap=tricol* | class=medium | mid=39.0µm | size_src=yaml | sc={echinaat}
  - `senecio_paludosus` | *Senecio paludosus* | unranked | ap=tricol* | class=medium | mid=35.9µm | size_src=yaml | sc={echinaat}
  - `silphium_perfoliatum` | *Silphium perfoliatum* | unranked | ap=tricol* | class=medium | mid=35.6µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arnica_montana`–`senecio_ovatus` (d=0.387): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.387}`
- Provenance (sample): `arnica_montana`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `aster_sedifolius`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cosmos_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_ovatus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C48 (n=6, mean_d=0.747, max_d=1.625)

- Shared aperture: tricol*
- Size classes: small; mid range: (25.0, 25.0)
- Shared sculpture tokens: —
- Members:
  - `chrysanthemum_leuc` | *Leucanthemum vulgare* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `eupatorium_cann` | *Eupatorium cann* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `eupatorium_cannabinum` | *Eupatorium cannabinum* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `hippopha_rhamn` | *Hippophaë rhamn* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={scabraat}
  - `petasitis_officinalis` | *Petasitis officinalis* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={echinaat}
  - `rubus_idaeus` | *Rubus idaeus* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sculpt_MASKED
- Closest pair evidence `chrysanthemum_leuc`–`eupatorium_cann` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `chrysanthemum_leuc`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cann`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eupatorium_cannabinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hippopha_rhamn`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C49 (n=6, mean_d=1.162, max_d=1.525)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (42.0, 44.5)
- Shared sculpture tokens: —
- Members:
  - `hieracium_sabaudum` | *Hieracium sabaudum* | unranked | ap=fenestr* | class=medium | mid=42.0µm | size_src=yaml
  - `hypochaeris_radicata` | *Hypochaeris radicata* | unranked | ap=fenestr* | class=medium | mid=44.0µm | size_src=yaml
  - `leontodon_autumnalis` | *Leontodon autumnalis* | unranked | ap=fenestr* | class=medium | mid=43.1µm | size_src=yaml | sc={echinaat}
  - `leontodon_hispidus` | *Leontodon hispidus* | unranked | ap=fenestr* | class=medium | mid=44.5µm | size_src=yaml
  - `picris_hieracioides` | *Picris hieracioides* | unranked | ap=fenestr* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
  - `sonchus_palustris` | *Sonchus palustris* | unranked | ap=fenestr* | class=medium | mid=43.2µm | size_src=yaml
- Closest pair evidence `leontodon_autumnalis`–`picris_hieracioides` (d=0.531): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.531}`
- Provenance (sample): `hieracium_sabaudum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hypochaeris_radicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_autumnalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `leontodon_hispidus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C50 (n=5, mean_d=1.063, max_d=1.745)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 21.5)
- Shared sculpture tokens: —
- Members:
  - `amorpha_fructico` | *Amorpha fruticosa* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat}
  - `clematis_vitalba` | *Clematis vitalba* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `melampyrum_typ` | *Melampyrum typ* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `punica_granatum` | *Punica granatum* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={scabraat}
  - `verbascum_nigrum` | *Verbascum nigrum* | unranked | ap=tricol* | class=small | mid=21.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `clematis_vitalba`–`melampyrum_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'scabraat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `amorpha_fructico`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `clematis_vitalba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `punica_granatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C51 (n=5, mean_d=1.155, max_d=1.429)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.9, 37.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `anthriscus_cerefolium` | *Anthriscus cerefolium* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=beug | sc={psilaat}
  - `arctostaphylos_uva_ursi` | *Arctostaphylos uva-ursi* | unranked | ap=tricol* | class=medium | mid=35.5µm | size_src=yaml | sc={psilaat}
  - `lathyrus_sylvestris` | *Lathyrus sylvestris* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={psilaat}
  - `pimpinella_saxifraga` | *Pimpinella saxifraga* | unranked | ap=tricol* | class=medium | mid=34.9µm | size_src=beug | path_gate=0–43 | sc={psilaat}
  - `styrax_japonicus` | *Styrax japonicus* | unranked | ap=tricol* | class=medium | mid=36.1µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `anthriscus_cerefolium`–`arctostaphylos_uva_ursi` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `anthriscus_cerefolium`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json · `arctostaphylos_uva_ursi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lathyrus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pimpinella_saxifraga`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C52 (n=5, mean_d=1.187, max_d=1.680)

- Shared aperture: tricol*
- Size classes: small; mid range: (16.2, 17.0)
- Shared sculpture tokens: —
- Members:
  - `antirrhinum_majus` | *Antirrhinum majus* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={microreticulaat,reticulaat}
  - `astragalus_sinicus` | *Astragalus sinicus* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml
  - `hypericum_tetrapterum` | *Hypericum tetrapterum* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={reticulaat}
  - `theobroma_cacao` | *Theobroma cacao* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={reticulaat}
  - `veronicastrum_sibiricum` | *Veronicastrum sibiricum* | unranked | ap=tricol* | class=small | mid=16.2µm | size_src=yaml | sc={microreticulaat,psilaat,reticulaat,scabraat}
- Closest pair evidence `antirrhinum_majus`–`astragalus_sinicus` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `antirrhinum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `astragalus_sinicus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_tetrapterum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `theobroma_cacao`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C53 (n=5, mean_d=0.563, max_d=1.195)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 29.5)
- Shared sculpture tokens: echinaat
- Members:
  - `aster_amellus` | *Aster Amellus* | unranked | ap=tricol* | class=medium | mid=29.5µm | size_src=yaml | sc={echinaat}
  - `crepis_typ` | *Crepis typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
  - `hieracium_aurantiacum` | *Hieracium aurantiacum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
  - `leontodon_autum` | *Leontodon autum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
  - `rudbeckia_hirta` | *Rudbeckia hirta* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `crepis_typ`–`hieracium_aurantiacum` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `aster_amellus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `crepis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hieracium_aurantiacum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `leontodon_autum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C54 (n=5, mean_d=1.054, max_d=1.381)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.6, 29.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ballota_nigra_ssp_foetida` | *Ballota nigra* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `cardamine_pratensis` | *Cardamine pratensis* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `corylopsis_pauciflora` | *Corylopsis pauciflora* | unranked | ap=tricol* | class=medium | mid=27.6µm | size_src=yaml | sc={reticulaat}
  - `lupinus_typ` | *Lupinus typ* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={reticulaat}
  - `sinapis_alba` | *Sinapis alba* | unranked | ap=tricol* | class=medium | mid=29.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `cardamine_pratensis`–`corylopsis_pauciflora` (d=0.728): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.333, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.7277}`
- Provenance (sample): `ballota_nigra_ssp_foetida`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cardamine_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylopsis_pauciflora`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lupinus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C55 (n=5, mean_d=1.134, max_d=1.369)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (41.0, 42.8)
- Shared sculpture tokens: —
- Members:
  - `berberis_typ` | *Berberis typ* | unranked | ap=stephanocol* | class=medium | mid=41.0µm | size_src=yaml | sc={psilaat}
  - `clinopodium_vulgare` | *Clinopodium vulgare* | unranked | ap=stephanocol* | class=medium | mid=41.2µm | size_src=yaml
  - `glechoma_hederacea` | *Glechoma hederacea* | unranked | ap=stephanocol* | class=medium | mid=41.6µm | size_src=yaml
  - `impatiens_noli_tangere` | *Impatiens noli* | unranked | ap=stephanocol* | class=medium | mid=41.9µm | size_src=yaml
  - `salvia_argentea` | *Salvia argentea* | unranked | ap=stephanocol* | class=medium | mid=42.8µm | size_src=yaml
- Closest pair evidence `berberis_typ`–`clinopodium_vulgare` (d=0.985): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.985}`
- Provenance (sample): `berberis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `clinopodium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `glechoma_hederacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `impatiens_noli_tangere`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C56 (n=5, mean_d=1.153, max_d=1.453)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (33.9, 36.1)
- Shared sculpture tokens: —
- Members:
  - `campanula_cochleariifolia` | *Campanula cochleariifolia* | unranked | ap=stephanopor* | class=medium | mid=33.9µm | size_src=yaml
  - `campanula_rapunculus` | *Campanula rapunculus* | unranked | ap=stephanopor* | class=medium | mid=34.8µm | size_src=yaml
  - `campanula_trachelium` | *Campanula trachelium* | unranked | ap=stephanopor* | class=medium | mid=36.1µm | size_src=beug | sc={echinaat,microechinaat}
  - `phyteuma_spicatum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm | size_src=yaml
  - `phyteuma_spicatum_ssp_nigrum` | *Phyteuma spicatum* | unranked | ap=stephanopor* | class=medium | mid=35.1µm | size_src=yaml
- Closest pair evidence `phyteuma_spicatum`–`phyteuma_spicatum_ssp_nigrum` (d=0.925): `{'aperture': 'same stephanopor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `campanula_cochleariifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_rapunculus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_trachelium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-trachelium.json · `phyteuma_spicatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C57 (n=5, mean_d=1.374, max_d=1.725)

- Shared aperture: tricol*
- Size classes: medium, small; mid range: (22.8, 26.0)
- Shared sculpture tokens: grof, striaat
- Members:
  - `comarum_palustre` | *Comarum palustre* | unranked | ap=tricol* | sc={grof,striaat}
  - `geum_rivale` | *Geum rivale* | unranked | ap=tricol* | class=medium | mid=23.6µm | size_src=yaml | sc={grof,striaat}
  - `geum_urbanum` | *Geum urbanum* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=yaml | sc={grof,striaat}
  - `potentilla_anserina` | *Potentilla anserina* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={grof,striaat}
  - `potentilla_crantzii` | *Potentilla crantzii* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={grof,striaat}
- Closest pair evidence `geum_rivale`–`geum_urbanum` (d=0.567): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.8, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['grof', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.567}`
- Provenance (sample): `comarum_palustre`: data/pollen.yaml:shape; eide:docs/keys/eide/rosaceae-eide.json; feagri-iversen:docs/keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json; reitsma:docs/keys/reitsma/rosaceae-reitsma.json · `geum_rivale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geum_urbanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `potentilla_anserina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C58 (n=5, mean_d=1.311, max_d=1.575)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: fijn, striaat
- Members:
  - `crataegus_oxycantha` | *Crataegus oxycantha* | unranked | ap=tricol* | sc={fijn,striaat}
  - `dryas_octopetala` | *Dryas octopetala* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=beug | yaml_size_MASKED | sc={fijn,striaat}
  - `rubus_saxatilis` | *Rubus saxatilis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={fijn,striaat}
  - `sorbus_arranensis` | *Sorbus arranensis* | unranked | ap=tricol* | sc={fijn,striaat}
  - `sorbus_aucuparia` | *Sorbus aucuparia* | unranked | ap=tricol* | class=medium | mid=27.1µm | size_src=yaml | sc={fijn,striaat}
- Closest pair evidence `rubus_saxatilis`–`sorbus_aucuparia` (d=0.579): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.579}`
- Provenance (sample): `crataegus_oxycantha`: eide:docs/keys/eide/rosaceae-eide.json · `dryas_octopetala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rubus_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sorbus_arranensis`: eide:docs/keys/eide/rosaceae-eide.json

### C59 (n=5, mean_d=1.266, max_d=1.705)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (32.5, 35.8)
- Shared sculpture tokens: —
- Members:
  - `crepis_tectorum` | *Crepis tectorum* | unranked | ap=fenestr* | class=medium | mid=35.8µm | size_src=yaml
  - `crepis_vesicaria_ssp_taraxacifol` | *Crepis vesicaria* | unranked | ap=fenestr* | class=medium | mid=32.5µm | size_src=yaml
  - `hieracium_pilosella` | *Hieracium pilosella* | unranked | ap=fenestr* | class=medium | mid=35.5µm | size_src=yaml
  - `lapsana_communis` | *Lapsana communis* | unranked | ap=fenestr* | class=medium | mid=34.9µm | size_src=yaml
  - `sonchus_oleraceus` | *Sonchus oleraceus* | unranked | ap=fenestr* | class=medium | mid=35.3µm | size_src=yaml
- Closest pair evidence `hieracium_pilosella`–`sonchus_oleraceus` (d=0.973): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `crepis_tectorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `crepis_vesicaria_ssp_taraxacifol`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `hieracium_pilosella`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lapsana_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C60 (n=5, mean_d=1.007, max_d=1.129)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.6, 26.5)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `euonymus_europaeus` | *Euonymus europaeus* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `genista_pilosa` | *Genista pilosa* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={reticulaat}
  - `mangifera_indica` | *Mangifera indica* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `melilotus_officinalis` | *Melilotus officinalis* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat}
  - `verbascum_thapsus` | *Verbascum thapsus* | unranked | ap=tricol* | class=medium | mid=25.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `euonymus_europaeus`–`mangifera_indica` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `euonymus_europaeus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `genista_pilosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `mangifera_indica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melilotus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C61 (n=5, mean_d=1.209, max_d=1.473)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.5, 43.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `helianthemum_typ` | *Helianthemum typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | size_src=yaml | sc={reticulaat}
  - `lathyrus_palustris` | *Lathyrus palustris* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={reticulaat}
  - `lathyrus_pratensis` | *Lathyrus pratensis* | unranked | ap=tricol* | class=medium | mid=41.5µm | size_src=yaml | sc={reticulaat}
  - `lathyrus_tuberosus` | *Lathyrus tuberosus* | unranked | ap=tricol* | class=medium | mid=41.6µm | size_src=yaml | sc={reticulaat}
  - `persicaria_bistorta` | *Persicaria bistorta* | unranked | ap=tricol* | class=medium | mid=43.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `lathyrus_pratensis`–`lathyrus_tuberosus` (d=0.949): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.949}`
- Provenance (sample): `helianthemum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lathyrus_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lathyrus_tuberosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C62 (n=4, mean_d=1.065, max_d=1.579)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.1, 30.0)
- Shared sculpture tokens: —
- Members:
  - `acer_negundo` | *Acer negundo* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,rugulaat,striaat}
  - `caltha_palustris` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | size_src=yaml | sc={psilaat,reticulaat}
  - `sarothamnus_sco` | *Sarothamnus sco* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml
  - `veronica_typ` | *Veronica typ* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,striaat}
- Closest pair evidence `acer_negundo`–`sarothamnus_sco` (d=0.675): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.675}`
- Provenance (sample): `acer_negundo`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `caltha_palustris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sarothamnus_sco`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `veronica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C63 (n=4, mean_d=1.411, max_d=1.725)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.0, 42.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `aegopodium_podagraria` | *Aegopodium podagraria* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={psilaat}
  - `cornus_alba` | *Cornus alba* | unranked | ap=tricol* | class=medium | mid=42.1µm | size_src=yaml | sc={psilaat}
  - `mespilus_germanica` | *Mespilus germanica* | unranked | ap=tricol* | class=medium | mid=40.0µm | size_src=yaml | sc={psilaat}
  - `symphoricarpos_albus` | *Symphoricarpos albus* | unranked | ap=tricol* | class=medium | mid=40.0µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `aegopodium_podagraria`–`cornus_alba` (d=1.009): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.009}`
- Provenance (sample): `aegopodium_podagraria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `cornus_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `mespilus_germanica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphoricarpos_albus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C64 (n=4, mean_d=1.021, max_d=1.105)

- Shared aperture: peripor*
- Size classes: medium; mid range: (23.2, 24.0)
- Shared sculpture tokens: —
- Members:
  - `amaranthus_caudatus` | *Amaranthus caudatus* | unranked | ap=peripor* | class=medium | mid=24.0µm | size_src=yaml | sc={scabraat}
  - `plantago_major` | *Plantago major* | unranked | ap=peripor* | class=medium | mid=23.2µm | size_src=yaml
  - `ribes_alpinum` | *Ribes alpinum* | unranked | ap=peripor* | class=medium | mid=23.9µm | size_src=yaml
  - `thalictrum_minus` | *Thalictrum minus* | unranked | ap=peripor* | class=medium | mid=23.8µm | size_src=yaml
- Closest pair evidence `amaranthus_caudatus`–`ribes_alpinum` (d=0.949): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `amaranthus_caudatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `plantago_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ribes_alpinum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C65 (n=4, mean_d=1.226, max_d=1.405)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (28.0, 30.0)
- Shared sculpture tokens: —
- Members:
  - `anemone_typ` | *Anemone typ* | unranked | ap=stephanocol* | class=medium | mid=28.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `coffea_typ` | *Coffea typ* | unranked | ap=stephanocol* | class=medium | mid=28.5µm | size_src=yaml | sc={scabraat}
  - `mentha_pulegium` | *Mentha pulegium* | unranked | ap=stephanocol* | class=medium | mid=29.2µm | size_src=yaml
  - `symphytum_off` | *Symphytum off* | unranked | ap=stephanocol* | class=medium | mid=30.0µm | size_src=yaml
- Closest pair evidence `coffea_typ`–`mentha_pulegium` (d=1.093): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.093}`
- Provenance (sample): `anemone_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `coffea_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mentha_pulegium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `symphytum_off`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C66 (n=4, mean_d=1.207, max_d=1.605)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.4, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `angelica_sylvestris` | *Angelica sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `foeniculum_vulgare` | *Foeniculum vulgare* | unranked | ap=tricol* | class=medium | mid=32.4µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `scrophularia_vernalis` | *Scrophularia vernalis* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat}
  - `trifolium_campestre` | *Trifolium campestre* | unranked | ap=tricol* | class=medium | mid=30.4µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `angelica_sylvestris`–`foeniculum_vulgare` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `angelica_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `scrophularia_vernalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `trifolium_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C67 (n=4, mean_d=1.272, max_d=1.687)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.9)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `astrantia_major` | *Astrantia major* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `genista_tinctoria` | *Genista tinctoria* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={scabraat,verrucaat}
  - `pyrus_communis` | *Pyrus communis* | unranked | ap=tricol* | class=medium | mid=32.6µm | size_src=yaml | sc={rugulaat,scabraat,striaat,verrucaat}
  - `ranunculus_repens` | *Ranunculus repens* | unranked | ap=tricol* | class=medium | mid=33.9µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `astrantia_major`–`ranunculus_repens` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['gemmaat', 'reticulaat', 'scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.711}`
- Provenance (sample): `astrantia_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `genista_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pyrus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_repens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C68 (n=4, mean_d=0.925, max_d=1.463)

- Shared aperture: tricol*
- Size classes: medium, small; mid range: (22.8, 24.0)
- Shared sculpture tokens: echinaat
- Members:
  - `bellis_perennis` | *Bellis perennis* | unranked | ap=tricol* | class=medium | mid=23.4µm | size_src=yaml | sc={echinaat}
  - `galinsoga_parviflora` | *Galinsoga parviflora* | unranked | ap=tricol* | class=medium | mid=23.6µm | size_src=yaml | sc={echinaat}
  - `solidago_gigantea` | *Solidago gigantea* | unranked | ap=tricol* | class=medium | mid=22.8µm | size_src=yaml | sc={echinaat}
  - `solidago_virgaurea` | *Solidago virgaurea* | unranked | ap=tricol* | class=small | mid=24.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `bellis_perennis`–`galinsoga_parviflora` (d=0.411): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.411}`
- Provenance (sample): `bellis_perennis`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `galinsoga_parviflora`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `solidago_gigantea`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `solidago_virgaurea`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C69 (n=4, mean_d=1.132, max_d=1.449)

- Shared aperture: peripor*
- Size classes: medium; mid range: (28.6, 30.0)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** borreria_verticilata ↔ borreria_typ
- Members:
  - `borreria_typ` | *Borreria typ* | unranked | ap=peripor* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `borreria_verticilata` | *Borreria verticilata* | unranked | ap=peripor* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat}
  - `chenopodium_bonus_henricus` | *Chenopodium bonus* | unranked | ap=peripor* | class=medium | mid=29.5µm | size_src=yaml
  - `daphne_mezereum` | *Daphne mezereum* | unranked | ap=peripor* | class=medium | mid=28.6µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `borreria_typ`–`borreria_verticilata` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `borreria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `borreria_verticilata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `chenopodium_bonus_henricus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `daphne_mezereum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C70 (n=4, mean_d=1.354, max_d=1.735)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.5, 41.0)
- Shared sculpture tokens: —
- Members:
  - `bryonia_dioica` | *Bryonia dioica* | unranked | ap=tricol* | class=medium | mid=39.5µm | size_src=yaml | sc={reticulaat}
  - `fagus_sylvatica` | *Fagus sylvatica* | unranked | ap=tricol* | class=medium | mid=41.0µm | size_src=yaml | sc={reticulaat,rugulaat,scabraat}
  - `pastinaca_sativa` | *Pastinaca sativa* | unranked | ap=tricol* | class=medium | mid=40.0µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `vaccinium_corymb` | *Vaccinium corymb* | unranked | ap=tricol* | class=medium | mid=39.5µm | size_src=yaml
- Closest pair evidence `bryonia_dioica`–`vaccinium_corymb` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `bryonia_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `fagus_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pastinaca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vaccinium_corymb`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C71 (n=4, mean_d=0.808, max_d=1.197)

- Shared aperture: tricol*
- Size classes: large; mid range: (67.2, 70.6)
- Shared sculpture tokens: echinaat
- Members:
  - `carthamus_lanatus` | *Carthamus lanatus* | unranked | ap=tricol* | class=large | mid=67.2µm | size_src=beug | sc={echinaat}
  - `echinops_sphaer` | *Echinops sphaer* | unranked | ap=tricol* | class=large | mid=70.0µm | size_src=yaml | sc={echinaat}
  - `lonicera_alpigena` | *Lonicera alpigena* | unranked | ap=tricol* | class=large | mid=70.6µm | size_src=yaml | sc={echinaat}
  - `scabiosa_columbar` | *Scabiosa columbar* | unranked | ap=tricol* | class=large | mid=70.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `echinops_sphaer`–`scabiosa_columbar` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `carthamus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `echinops_sphaer`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_alpigena`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `scabiosa_columbar`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C72 (n=4, mean_d=1.219, max_d=1.465)

- Shared aperture: monocol*
- Size classes: large; mid range: (52.0, 54.2)
- Shared sculpture tokens: —
- Members:
  - `colchicinum_autu` | *Colchicinum autu* | unranked | ap=monocol* | class=large | mid=52.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `magnolia_kobus` | *Magnolia kobus* | unranked | ap=monocol* | class=large | mid=53.6µm | size_src=yaml
  - `narcissus_pseudonarcissus` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm | size_src=yaml
  - `narcissus_pseudonarcissus_ssp_major` | *Narcissus pseudonarcissus* | unranked | ap=monocol* | class=large | mid=54.2µm | size_src=yaml
- Closest pair evidence `narcissus_pseudonarcissus`–`narcissus_pseudonarcissus_ssp_major` (d=0.925): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `colchicinum_autu`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `magnolia_kobus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `narcissus_pseudonarcissus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `narcissus_pseudonarcissus_ssp_major`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C73 (n=4, mean_d=1.075, max_d=1.683)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.0, 18.7)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `deutzia_typ` | *Deutzia typ* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,reticulaat}
  - `echium_vulgare` | *Echium vulgare* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,psilaat,reticulaat}
  - `hypericum_perforatum` | *Hypericum perforatum* | unranked | ap=tricol* | class=small | mid=18.7µm | size_src=beug | sc={fijn,microreticulaat,psilaat,reticulaat}
  - `linaria_cymbalaria` | *Linaria cymbalaria* | unranked | ap=tricol* | class=small | mid=17.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `deutzia_typ`–`linaria_cymbalaria` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `deutzia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `echium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hypericum_perforatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `linaria_cymbalaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C74 (n=4, mean_d=1.193, max_d=1.417)

- Shared aperture: peripor*
- Size classes: medium; mid range: (39.1, 41.1)
- Shared sculpture tokens: —
- Members:
  - `dianthus_deltoides` | *Dianthus Deltoides* | unranked | ap=peripor* | class=medium | mid=41.1µm | size_src=yaml
  - `stellaria_holostea` | *Stellaria holostea* | unranked | ap=peripor* | class=medium | mid=39.7µm | size_src=beug | sc={fijn,microechinaat,microreticulaat,scabraat}
  - `stellaria_nemorum` | *Stellaria nemorum* | unranked | ap=peripor* | class=medium | mid=40.2µm | size_src=yaml
  - `thymelaea_passerina` | *Thymelaea passerina* | unranked | ap=peripor* | class=medium | mid=39.1µm | size_src=beug | path_gate=34–47
- Closest pair evidence `stellaria_holostea`–`stellaria_nemorum` (d=1.057): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-stellaria-holostea.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.55, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.057}`
- Provenance (sample): `dianthus_deltoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `stellaria_holostea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-caryophyllaceae.json · `stellaria_nemorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thymelaea_passerina`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths; beug:docs/keys/beug/beug33-periporatae-thymelaea.json

### C75 (n=4, mean_d=0.783, max_d=1.095)

- Shared aperture: tricol*
- Size classes: large; mid range: (77.0, 80.0)
- Shared sculpture tokens: echinaat
- Members:
  - `echinops_sphaerocephalus` | *Echinops sphaerocephalus* | unranked | ap=tricol* | class=large | mid=77.0µm | size_src=yaml | sc={echinaat}
  - `scabiosa_columbaria` | *Scabiosa columbaria* | unranked | ap=tricol* | class=large | mid=78.7µm | size_src=beug | sc={echinaat}
  - `scabiosa_ochroleuca` | *Scabiosa ochroleuca* | unranked | ap=tricol* | class=large | mid=77.5µm | size_src=yaml | sc={echinaat}
  - `succisa_praten` | *Succisa praten* | unranked | ap=tricol* | class=large | mid=80.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `echinops_sphaerocephalus`–`scabiosa_ochroleuca` (d=0.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.495}`
- Provenance (sample): `echinops_sphaerocephalus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `scabiosa_columbaria`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug17-ttt-ech-dipsacaceae.json · `scabiosa_ochroleuca`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `succisa_praten`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C76 (n=3, mean_d=1.219, max_d=1.691)

- Shared aperture: tricol*
- Size classes: large; mid range: (55.1, 56.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `acanthus_mollis` | *Acanthus mollis* | unranked | ap=tricol* | class=large | mid=55.1µm | size_src=beug | sc={reticulaat}
  - `citrullus_lanatus` | *Citrullus lanatus* | unranked | ap=tricol* | class=large | mid=56.0µm | size_src=yaml | sc={reticulaat}
  - `pisum_sativum` | *Pisum sativum* | unranked | ap=tricol* | class=large | mid=55.8µm | size_src=beug | path_gate=53–59 | sc={reticulaat}
- Closest pair evidence `citrullus_lanatus`–`pisum_sativum` (d=0.573): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug22-tricolporatae-ret-vicia.json', 'size_class': 'same large', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.573}`
- Provenance (sample): `acanthus_mollis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `citrullus_lanatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pisum_sativum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C77 (n=3, mean_d=1.085, max_d=1.515)

- Shared aperture: tricol*
- Size classes: medium; mid range: (29.0, 30.0)
- Shared sculpture tokens: striaat
- Members:
  - `acer_japonicum` | *Acer japonicum* | unranked | ap=tricol* | class=medium | mid=29.0µm | size_src=yaml | sc={striaat}
  - `acer_tataricum_subsp_ginnala` | *Acer tataricum* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={striaat}
  - `malus_domestica` | *Malus domestica* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={rugulaat,striaat}
- Closest pair evidence `acer_japonicum`–`acer_tataricum_subsp_ginnala` (d=0.615): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.615}`
- Provenance (sample): `acer_japonicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `acer_tataricum_subsp_ginnala`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `malus_domestica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C78 (n=3, mean_d=1.117, max_d=1.353)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.9, 43.1)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `adonis_aestivalis` | *Adonis aestivalis* | unranked | ap=tricol* | class=medium | mid=42.2µm | size_src=beug | sc={grof,microreticulaat,psilaat,reticulaat}
  - `helleborus_niger` | *Helleborus niger* | unranked | ap=tricol* | class=medium | mid=41.9µm | size_src=beug | path_gate=36–41 | sc={microreticulaat,psilaat,reticulaat}
  - `nigella_sativa` | *Nigella sativa* | unranked | ap=tricol* | class=medium | mid=43.1µm | size_src=yaml | sc={psilaat,reticulaat}
- Closest pair evidence `adonis_aestivalis`–`helleborus_niger` (d=0.822): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug13-tricolpatae-ps.json vs beug:docs/keys/beug/beug13-tricolpatae-ps.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.822}`
- Provenance (sample): `adonis_aestivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helleborus_niger`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `nigella_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C79 (n=3, mean_d=1.528, max_d=1.605)

- Shared aperture: tricol*
- Size classes: medium; mid range: (26.0, 28.0)
- Shared sculpture tokens: rugulaat
- Members:
  - `ajuga_reptans` | *Ajuga reptans* | unranked | ap=tricol* | class=medium | mid=26.0µm | size_src=yaml | sc={reticulaat,rugulaat}
  - `ferula_communis` | *Ferula communis* | unranked | ap=tricol* | class=medium | mid=26.5µm | size_src=yaml | sc={rugulaat,scabraat}
  - `nicotiana_glauca` | *Nicotiana glauca* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=yaml | sc={rugulaat}
- Closest pair evidence `ferula_communis`–`nicotiana_glauca` (d=1.485): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.485}`
- Provenance (sample): `ajuga_reptans`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ferula_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `nicotiana_glauca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C80 (n=3, mean_d=1.109, max_d=1.201)

- Shared aperture: peripor*
- Size classes: medium; mid range: (27.4, 28.6)
- Shared sculpture tokens: —
- Members:
  - `alisma_plantago_aquatica` | *Alisma plantago* | unranked | ap=peripor* | class=medium | mid=27.4µm | size_src=beug
  - `gypsophila_paniculata` | *Gypsophila paniculata* | unranked | ap=peripor* | class=medium | mid=27.8µm | size_src=yaml
  - `ribes_rubrum` | *Ribes rubrum* | unranked | ap=peripor* | class=medium | mid=28.6µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `alisma_plantago_aquatica`–`gypsophila_paniculata` (d=1.009): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-alisma-typ.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.009}`
- Provenance (sample): `alisma_plantago_aquatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-alisma-typ.json · `gypsophila_paniculata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ribes_rubrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C81 (n=3, mean_d=1.405, max_d=1.645)

- Shared aperture: monocol*
- Size classes: medium; mid range: (39.0, 42.0)
- Shared sculpture tokens: —
- Members:
  - `allium_senescens` | *Allium senescens* | unranked | ap=monocol* | class=medium | mid=39.0µm | size_src=yaml
  - `convallaria_majalis` | *Convallaria majalis* | unranked | ap=monocol* | class=medium | mid=42.0µm | size_src=beug | path_gate=0–65 | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `leucojum_vernum` | *Leucojum vernum* | unranked | ap=monocol* | class=medium | mid=39.9µm | size_src=yaml
- Closest pair evidence `allium_senescens`–`leucojum_vernum` (d=1.141): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.9, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.141}`
- Provenance (sample): `allium_senescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `convallaria_majalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths · `leucojum_vernum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C82 (n=3, mean_d=0.692, max_d=0.975)

- Shared aperture: tricol*
- Size classes: medium; mid range: (42.5, 45.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_minus` | *Arcticum minus* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
  - `sonchus_arvensis` | *Sonchus arvensis* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={echinaat}
  - `weigelia_diervilla_typ` | *Weigelia/Diervilla typ* | unranked | ap=tricol* | class=medium | mid=45.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arcticum_minus`–`sonchus_arvensis` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `arcticum_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sonchus_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `weigelia_diervilla_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C83 (n=3, mean_d=1.575, max_d=1.575)

- Shared aperture: fenestr*
- Size classes: very-large; mid range: (95.0, 95.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arctium_lappa` | *Arctium lappa* | unranked | ap=fenestr* | sc={echinaat}
  - `helenium_autumnale` | *Helenium autumnale* | unranked | ap=fenestr* | sc={echinaat}
  - `knautia_typ` | *Knautia typ* | unranked | ap=fenestr* | class=very-large | mid=95.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arctium_lappa`–`helenium_autumnale` (d=1.575): `{'aperture': 'same fenestr*', 'size': 'missing_one_or_both', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.575}`
- Provenance (sample): `arctium_lappa`: data/pollen.yaml:sculpture; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json; vanderham:docs/keys/vanderham/vanderham-pollentabel.json; kerkvliet:analytic (not dichotomous source) · `helenium_autumnale`: kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json; kerkvliet:analytic (not dichotomous source) · `knautia_typ`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C84 (n=3, mean_d=1.170, max_d=1.693)

- Shared aperture: tricol*
- Size classes: large, medium; mid range: (50.0, 53.2)
- Shared sculpture tokens: echinaat
- Members:
  - `arctium_minus` | *Arctium minus* | unranked | ap=tricol* | class=large | mid=53.2µm | size_src=beug | yaml_size_MASKED | sc={echinaat}
  - `cirsium_vulgare` | *Cirsium vulgare* | unranked | ap=tricol* | class=large | mid=51.0µm | size_src=yaml | sc={echinaat}
  - `sylibum_marianum` | *Sylibum marianum* | unranked | ap=tricol* | class=medium | mid=50.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arctium_minus`–`cirsium_vulgare` (d=0.653): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug17-ttt-ech-asteraceae.json vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 2.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.653}`
- Provenance (sample): `arctium_minus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cirsium_vulgare`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sylibum_marianum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C85 (n=3, mean_d=1.298, max_d=1.485)

- Shared aperture: peripor*
- Size classes: medium; mid range: (32.5, 34.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `buxus_sempervirens` | *Buxus sempervirens* | unranked | ap=peripor* | class=medium | mid=33.7µm | size_src=beug | sc={reticulaat}
  - `phlox_typ` | *Phlox typ* | unranked | ap=peripor* | class=medium | mid=32.5µm | size_src=yaml | sc={grof,reticulaat}
  - `silene_dioica` | *Silene dioica* | unranked | ap=peripor* | class=medium | mid=34.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `buxus_sempervirens`–`silene_dioica` (d=0.997): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-buxus.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.997}`
- Provenance (sample): `buxus_sempervirens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-buxus.json · `phlox_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `silene_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C86 (n=3, mean_d=1.174, max_d=1.280)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.5, 33.8)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `callicarpa_bodinieri` | *Callicarpa bodinieri* | unranked | ap=tricol* | class=medium | mid=33.8µm | size_src=yaml | sc={rugulaat,scabraat,verrucaat}
  - `ranunculus_ficaria` | *Ranunculus ficaria* | unranked | ap=tricol* | class=medium | mid=32.9µm | size_src=yaml | sc={clavaat,echinaat,scabraat,verrucaat}
  - `saxifraga_rotundifolia` | *Saxifraga rotundifolia* | unranked | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={psilaat,rugulaat,scabraat,striaat,verrucaat}
- Closest pair evidence `callicarpa_bodinieri`–`saxifraga_rotundifolia` (d=1.013): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.2, 'sculpture': {'jaccard_dist': 0.4, 'shared': ['rugulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.013}`
- Provenance (sample): `callicarpa_bodinieri`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_ficaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `saxifraga_rotundifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C87 (n=3, mean_d=1.037, max_d=1.093)

- Shared aperture: tricol*
- Size classes: medium; mid range: (28.7, 29.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `caltha_palustris_ssp_araneosa` | *Caltha palustris* | unranked | ap=tricol* | class=medium | mid=29.1µm | size_src=yaml | sc={psilaat}
  - `lamium_maculatum_cv_var` | *Lamium maculatum* | unranked | ap=tricol* | class=medium | mid=28.7µm | size_src=yaml | sc={psilaat}
  - `papaver_dubium` | *Papaver dubium* | unranked | ap=tricol* | class=medium | mid=29.4µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `caltha_palustris_ssp_araneosa`–`papaver_dubium` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `caltha_palustris_ssp_araneosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lamium_maculatum_cv_var`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `papaver_dubium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C88 (n=3, mean_d=0.372, max_d=0.495)

- Shared aperture: tricol*
- Size classes: large; mid range: (47.2, 47.8)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** serratula_tinctoria ↔ serratula_typ
- Members:
  - `carduus_crispus` | *Carduus crispus* | unranked | ap=tricol* | class=large | mid=47.8µm | size_src=yaml | sc={echinaat}
  - `serratula_tinctoria` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | size_src=yaml | sc={echinaat}
  - `serratula_typ` | *Serratula tinctoria* | unranked | ap=tricol* | class=large | mid=47.2µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `serratula_tinctoria`–`serratula_typ` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `carduus_crispus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `serratula_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serratula_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C89 (n=3, mean_d=0.658, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 47.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carduus_nutans` | *Carduus nutans* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
  - `onopordon_acant` | *Onopordon acant* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
  - `onopordum_acanthium` | *Onopordum acanthium* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `onopordon_acant`–`onopordum_acanthium` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carduus_nutans`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordon_acant`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `onopordum_acanthium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C90 (n=3, mean_d=0.625, max_d=0.875)

- Shared aperture: tricol*
- Size classes: large; mid range: (60.0, 60.0)
- Shared sculpture tokens: echinaat
- Members:
  - `carlina_acaulis` | *Carlina acaulis* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat}
  - `carlina_aucalis` | *Carlina aucalis* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat}
  - `lonicera_typ` | *Lonicera typ* | unranked | ap=tricol* | class=large | mid=60.0µm | size_src=yaml | sc={echinaat,reticulaat}
- Closest pair evidence `carlina_acaulis`–`carlina_aucalis` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `carlina_acaulis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `carlina_aucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lonicera_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C91 (n=3, mean_d=0.962, max_d=1.213)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (24.1, 26.0)
- Shared sculpture tokens: —
- Members:
  - `ceratonia_silqua` | *Ceratonia silqua* | unranked | ap=stephanocol* | class=medium | mid=26.0µm | size_src=yaml
  - `primula_veris` | *Primula veris* | unranked | ap=stephanocol* | class=medium | mid=24.1µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `salvia_verticillata` | *Salvia verticillata* | unranked | ap=stephanocol* | class=medium | mid=24.8µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `primula_veris`–`salvia_verticillata` (d=0.543): `{'aperture': 'same stephanocol*', 'size_source': 'beug:docs/keys/beug/beug24-stephanocolpatae-primula-veris.json vs beug:docs/keys/beug/beug24-stephanocolpatae-salvia-verticillata.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat', 'rugulaat', 'scabraat']}, 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.543}`
- Provenance (sample): `ceratonia_silqua`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `primula_veris`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-primula-veris.json; beug:docs/keys/beug/beug24-stephanocolpatae.json · `salvia_verticillata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-salvia-verticillata.json

### C92 (n=3, mean_d=1.245, max_d=1.405)

- Shared aperture: fenestr*
- Size classes: large; mid range: (52.8, 54.8)
- Shared sculpture tokens: —
- Members:
  - `cichorium_endivia` | *Cichorium endivia* | unranked | ap=fenestr* | class=large | mid=52.8µm | size_src=yaml
  - `leontodon_saxatilis` | *Leontodon saxatilis* | unranked | ap=fenestr* | class=large | mid=53.4µm | size_src=yaml
  - `prenanthes_purpurea` | *Prenanthes purpurea* | unranked | ap=fenestr* | class=large | mid=54.8µm | size_src=yaml
- Closest pair evidence `cichorium_endivia`–`leontodon_saxatilis` (d=1.081): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same fenestr', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.081}`
- Provenance (sample): `cichorium_endivia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `leontodon_saxatilis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `prenanthes_purpurea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C93 (n=3, mean_d=0.292, max_d=0.375)

- Shared aperture: tricol*
- Size classes: medium; mid range: (49.0, 49.0)
- Shared sculpture tokens: echinaat
- Members:
  - `cirsium_arvense` | *Cirsium arvense* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
  - `cnicus_benedict` | *Cnicus benedictus* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
  - `serrulata_tinctoria` | *Serrulata tinctoria* | unranked | ap=tricol* | class=medium | mid=49.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `cirsium_arvense`–`serrulata_tinctoria` (d=0.125): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `cirsium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `cnicus_benedict`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `serrulata_tinctoria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C94 (n=3, mean_d=1.197, max_d=1.333)

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.5, 38.1)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `consolida_regalis` | *Consolida regalis* | unranked | ap=tricol* | class=medium | mid=38.1µm | size_src=yaml | sc={psilaat}
  - `veronica_chamaedrys` | *Veronica chamaedrys* | unranked | ap=tricol* | class=medium | mid=36.9µm | size_src=yaml | sc={psilaat}
  - `viola_reichenbachiana` | *Viola reichenbachiana* | unranked | ap=tricol* | class=medium | mid=36.5µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `veronica_chamaedrys`–`viola_reichenbachiana` (d=1.033): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.45, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.033}`
- Provenance (sample): `consolida_regalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_chamaedrys`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `viola_reichenbachiana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C95 (n=3, mean_d=1.182, max_d=1.649)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.5, 31.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `corylopsis_spicata` | *Corylopsis spicata* | unranked | ap=tricol* | class=medium | mid=31.6µm | size_src=yaml | sc={reticulaat}
  - `gleditsia_triacanthos` | *Gleditsia triacanthos* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={reticulaat}
  - `trifolium_arvense` | *Trifolium arvense* | unranked | ap=tricol* | class=medium | mid=31.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `gleditsia_triacanthos`–`trifolium_arvense` (d=0.937): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.937}`
- Provenance (sample): `corylopsis_spicata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `gleditsia_triacanthos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_arvense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C96 (n=3, mean_d=1.240, max_d=1.575)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.9, 42.7)
- Shared sculpture tokens: fijn, rugulaat, striaat
- Members:
  - `crataegus_monogyna` | *Crataegus monogyna* | unranked | ap=tricol* | class=medium | mid=42.7µm | size_src=yaml | sc={fijn,rugulaat,striaat}
  - `prunus_avium` | *Prunus avium* | unranked | ap=tricol* | size_src=masked_no_key_size | yaml_size_MASKED | sc={fijn,rugulaat,striaat}
  - `prunus_spinosa` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=40.9µm | size_src=yaml | sc={fijn,rugulaat,striaat}
- Closest pair evidence `crataegus_monogyna`–`prunus_spinosa` (d=0.819): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.85, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'rugulaat', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.819}`
- Provenance (sample): `crataegus_monogyna`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_avium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C97 (n=3, mean_d=1.115, max_d=1.485)

- Shared aperture: tricol*
- Size classes: medium; mid range: (25.5, 27.0)
- Shared sculpture tokens: echinaat
- Members:
  - `crepis_biennis` | *Crepis biennis* | unranked | ap=tricol* | class=medium | mid=25.5µm | size_src=yaml | sc={echinaat,microreticulaat}
  - `galinsoga_typ` | *Galinsoga typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={echinaat}
  - `senecio_typ` | *Senecio typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `galinsoga_typ`–`senecio_typ` (d=0.375): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `crepis_biennis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `galinsoga_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `senecio_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C98 (n=3, mean_d=1.208, max_d=1.449)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (35.6, 37.0)
- Shared sculpture tokens: —
- Members:
  - `diplotaxis_muralis` | *Diplotaxis muralis* | unranked | ap=stephanocol* | class=medium | mid=37.0µm | size_src=yaml | sc={reticulaat}
  - `origanum_majorana` | *Origanum majorana* | unranked | ap=stephanocol* | class=medium | mid=35.6µm | size_src=yaml | sc={reticulaat,rugulaat}
  - `satureja_montana` | *Satureja montana* | unranked | ap=stephanocol* | class=medium | mid=36.5µm | size_src=yaml
- Closest pair evidence `diplotaxis_muralis`–`satureja_montana` (d=1.045): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.045}`
- Provenance (sample): `diplotaxis_muralis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `origanum_majorana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `satureja_montana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C99 (n=3, mean_d=1.267, max_d=1.567)

- Shared aperture: tricol*
- Size classes: small; mid range: (18.9, 19.8)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `escallonia_typ` | *Escallonia typ* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={psilaat}
  - `lotus_corniculatus` | *Lotus corniculatus* | unranked | ap=tricol* | class=small | mid=18.9µm | size_src=yaml | sc={psilaat,scabraat}
  - `solanum_lycopersicum` | *Solanum lycopersicum* | unranked | ap=tricol* | class=small | mid=19.8µm | size_src=yaml | sc={psilaat,rugulaat,scabraat}
- Closest pair evidence `lotus_corniculatus`–`solanum_lycopersicum` (d=1.096): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.85, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.333, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.0957}`
- Provenance (sample): `escallonia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lotus_corniculatus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `solanum_lycopersicum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C100 (n=3, mean_d=1.158, max_d=1.549)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (36.0, 38.6)
- Shared sculpture tokens: —
- Members:
  - `eschscholtzia_calif` | *Eschscholtzia calif* | unranked | ap=stephanocol* | class=medium | mid=38.5µm | size_src=yaml | sc={reticulaat,scabraat}
  - `melissa_officinalis` | *Melissa officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.6µm | size_src=yaml
  - `veronica_filiformis` | *Veronica filiformis* | unranked | ap=stephanocol* | class=medium | mid=36.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `eschscholtzia_calif`–`melissa_officinalis` (d=0.949): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.949}`
- Provenance (sample): `eschscholtzia_calif`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melissa_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `veronica_filiformis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C101 (n=3, mean_d=1.275, max_d=1.725)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.5, 43.0)
- Shared sculpture tokens: verrucaat
- **Human review (species↔*_typ):** rhododendron_ponticum ↔ rhododendron_typ
- Members:
  - `euphorbia_typ` | *Euphorbia typ* | unranked | ap=tricol* | class=medium | mid=40.5µm | size_src=yaml | sc={verrucaat}
  - `rhododendron_ponticum` | *Rhododendron ponticum* | unranked | ap=tricol* | class=medium | mid=43.0µm | size_src=yaml | sc={verrucaat}
  - `rhododendron_typ` | *Rhododendron typ* | unranked | ap=tricol* | class=medium | mid=43.0µm | size_src=yaml | sc={echinaat,verrucaat}
- Closest pair evidence `euphorbia_typ`–`rhododendron_ponticum` (d=0.975): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.975}`
- Provenance (sample): `euphorbia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhododendron_ponticum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `rhododendron_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C102 (n=3, mean_d=1.488, max_d=1.675)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.4, 36.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `ficaria_typ` | *Ficaria typ* | unranked | ap=tricol* | class=medium | mid=36.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `lupinus_polyphyllus` | *Lupinus polyphyllus* | unranked | ap=tricol* | class=medium | mid=35.4µm | size_src=yaml | sc={reticulaat}
  - `parthenocissus_quinquefolia` | *Parthenocissus quinquefolia* | unranked | ap=tricol* | class=medium | mid=35.4µm | size_src=yaml | sc={reticulaat,rugulaat}
- Closest pair evidence `ficaria_typ`–`lupinus_polyphyllus` (d=1.269): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.6, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.269}`
- Provenance (sample): `ficaria_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lupinus_polyphyllus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `parthenocissus_quinquefolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C103 (n=3, mean_d=1.615, max_d=1.735)

- Shared aperture: tricol*
- Size classes: small; mid range: (17.5, 19.0)
- Shared sculpture tokens: striaat
- Members:
  - `fragaria_viridis` | *Fragaria viridis* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={grof,striaat}
  - `rubus_arcticus` | *Rubus arcticus* | unranked | ap=tricol* | class=small | mid=17.5µm | size_src=yaml | sc={fijn,striaat}
  - `sedum_acre` | *Sedum acre* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={rugulaat,striaat}
- Closest pair evidence `fragaria_viridis`–`rubus_arcticus` (d=1.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.495}`
- Provenance (sample): `fragaria_viridis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_arcticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `sedum_acre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C104 (n=3, mean_d=0.782, max_d=0.985)

- Shared aperture: monocol*
- Size classes: large; mid range: (56.8, 57.0)
- Shared sculpture tokens: —
- Members:
  - `fritillaria_meleagris` | *Fritillaria meleagris* | unranked | ap=monocol* | class=large | mid=56.8µm | size_src=yaml
  - `liriodendron_tulip` | *Liriodendron tulip* | unranked | ap=monocol* | class=large | mid=57.0µm | size_src=yaml | sc={verrucaat}
  - `lirodendron_tulipi` | *Lirodendron tulipi* | unranked | ap=monocol* | class=large | mid=57.0µm | size_src=yaml | sc={verrucaat}
- Closest pair evidence `liriodendron_tulip`–`lirodendron_tulipi` (d=0.375): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.375}`
- Provenance (sample): `fritillaria_meleagris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `liriodendron_tulip`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `lirodendron_tulipi`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C105 (n=3, mean_d=1.368, max_d=1.489)

- Shared aperture: monocol*
- Size classes: medium; mid range: (29.1, 31.5)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** muscari_botryoides ↔ muscari_typ
- Members:
  - `galanthus_nivalis` | *Galanthus nivalis* | unranked | ap=monocol* | class=medium | mid=29.1µm | size_src=yaml
  - `muscari_botryoides` | *Muscari botryoides* | unranked | ap=monocol* | class=medium | mid=31.5µm | size_src=yaml | sc={reticulaat}
  - `muscari_typ` | *Muscari typ* | unranked | ap=monocol* | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `galanthus_nivalis`–`muscari_typ` (d=1.129): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.85, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.129}`
- Provenance (sample): `galanthus_nivalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `muscari_botryoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `muscari_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C106 (n=3, mean_d=1.146, max_d=1.197)

- Shared aperture: tricol*
- Size classes: medium; mid range: (43.8, 44.3)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `galeopsis_speciosa` | *Galeopsis speciosa* | unranked | ap=tricol* | class=medium | mid=44.3µm | size_src=yaml | sc={reticulaat}
  - `melittis_melissophyllum` | *Melittis melissophyllum* | unranked | ap=tricol* | class=medium | mid=43.8µm | size_src=yaml | sc={reticulaat}
  - `symphoricarpos_typ` | *Symphoricarpos typ* | unranked | ap=tricol* | class=medium | mid=44.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `galeopsis_speciosa`–`melittis_melissophyllum` (d=1.057): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.55, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.057}`
- Provenance (sample): `galeopsis_speciosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `melittis_melissophyllum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `symphoricarpos_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C107 (n=3, mean_d=1.255, max_d=1.695)

- Shared aperture: tricol*
- Size classes: large; mid range: (55.0, 60.5)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_dissectum` | *Geranium dissectum* | unranked | ap=tricol* | class=large | mid=55.0µm | size_src=yaml | sc={clavaat}
  - `geranium_molle` | *Geranium molle* | unranked | ap=tricol* | class=large | mid=58.2µm | size_src=yaml | sc={clavaat}
  - `linum_flavum` | *Linum flavum* | unranked | ap=tricol* | class=large | mid=60.5µm | size_src=yaml | sc={clavaat}
- Closest pair evidence `geranium_molle`–`linum_flavum` (d=0.927): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 2.3, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.927}`
- Provenance (sample): `geranium_dissectum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_molle`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `linum_flavum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C108 (n=3, mean_d=1.069, max_d=1.141)

- Shared aperture: fenestr*
- Size classes: medium; mid range: (39.5, 40.4)
- Shared sculpture tokens: —
- Members:
  - `hieracium_umbellatum` | *Hieracium umbellatum* | unranked | ap=fenestr* | class=medium | mid=39.6µm | size_src=yaml
  - `lactuca_sativa` | *Lactuca sativa* | unranked | ap=fenestr* | class=medium | mid=40.4µm | size_src=yaml
  - `vaccinium_corymbosum` | *Vaccinium corymbosum* | unranked | ap=fenestr* | class=medium | mid=39.5µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `hieracium_umbellatum`–`vaccinium_corymbosum` (d=0.961): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.961}`
- Provenance (sample): `hieracium_umbellatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lactuca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json · `vaccinium_corymbosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C109 (n=3, mean_d=1.053, max_d=1.117)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.9, 32.7)
- Shared sculpture tokens: —
- Members:
  - `hyssopus_officinalis` | *Hyssopus officinalis* | unranked | ap=stephanocol* | class=medium | mid=31.9µm | size_src=yaml
  - `lavandula_angustifolia` | *Lavandula angustifolia* | unranked | ap=stephanocol* | class=medium | mid=32.7µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
  - `thymus_pulegioides` | *Thymus pulegioides* | unranked | ap=stephanocol* | class=medium | mid=32.1µm | size_src=yaml
- Closest pair evidence `hyssopus_officinalis`–`thymus_pulegioides` (d=0.985): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.985}`
- Provenance (sample): `hyssopus_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `lavandula_angustifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_pulegioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C110 (n=3, mean_d=1.158, max_d=1.625)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (38.0, 38.0)
- Shared sculpture tokens: —
- Members:
  - `lavandula_angisti` | *Lavandula angisti* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={reticulaat}
  - `pulmonaria_officinalis` | *Pulmonaria officinalis* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml | sc={reticulaat}
  - `thymus_vulgaris` | *Thymus vulgaris* | unranked | ap=stephanocol* | class=medium | mid=38.0µm | size_src=yaml
- Closest pair evidence `lavandula_angisti`–`pulmonaria_officinalis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `lavandula_angisti`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `pulmonaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `thymus_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C111 (n=3, mean_d=0.813, max_d=1.267)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.0, 28.8)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `mercurialis_perennis` | *Mercurialis perennis* | unranked | ap=tricol* | class=medium | mid=28.0µm | size_src=beug | sc={fijn,reticulaat}
  - `reseda_lutea` | *Reseda lutea* | unranked | ap=tricol* | class=medium | mid=28.8µm | size_src=beug | yaml_size_MASKED | sc={fijn,reticulaat}
  - `ulex_typ` | *Ulex typ* | unranked | ap=tricol* | class=medium | mid=27.0µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `reseda_lutea`–`ulex_typ` (d=0.557): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug21-tricolpatae-ret-reseda.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.8, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['fijn', 'reticulaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.557}`
- Provenance (sample): `mercurialis_perennis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `reseda_lutea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ulex_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C112 (n=3, mean_d=1.424, max_d=1.596)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.0, 22.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `onosis_spinoza` | *Ononis spinosa* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={psilaat}
  - `verbena_officinalis` | *Verbena officinalis* | unranked | ap=tricol* | class=small | mid=22.1µm | size_src=beug | path_gate=21–28 | sc={psilaat,rugulaat,scabraat,verrucaat}
  - `vitis_vinifera` | *Vitis vinifera* | unranked | ap=tricol* | class=small | mid=22.0µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `onosis_spinoza`–`vitis_vinifera` (d=1.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.245}`
- Provenance (sample): `onosis_spinoza`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `verbena_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vitis_vinifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C113 (n=3, mean_d=1.138, max_d=1.245)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 23.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `platanus_hybr` | *Platanus hybr* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={reticulaat}
  - `raphanus_sativus` | *Raphanus sativus* | unranked | ap=tricol* | class=small | mid=22.7µm | size_src=yaml | sc={reticulaat}
  - `rubus_fructicosus` | *Rubus fructicosus* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={reticulaat,striaat}
- Closest pair evidence `platanus_hybr`–`raphanus_sativus` (d=0.973): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.973}`
- Provenance (sample): `platanus_hybr`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `raphanus_sativus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rubus_fructicosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C114 (n=3, mean_d=1.200, max_d=1.237)

- Shared aperture: peripor*
- Size classes: large; mid range: (46.5, 47.8)
- Shared sculpture tokens: —
- Members:
  - `polemonium_boreale` | *Polemonium boreale* | unranked | ap=peripor* | class=large | mid=47.6µm | size_src=beug | sc={reticulaat,striaat}
  - `polemonium_caeruleum` | *Polemonium caeruleum* | unranked | ap=peripor* | class=large | mid=47.8µm | size_src=beug | sc={striaat}
  - `saponaria_officinalis` | *Saponaria officinalis* | unranked | ap=peripor* | class=large | mid=46.5µm | size_src=yaml
- Closest pair evidence `polemonium_boreale`–`polemonium_caeruleum` (d=1.173): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-polemonium.json vs beug:docs/keys/beug/beug33-periporatae-polemonium.json', 'size_class': 'same large', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['striaat']}, 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.173}`
- Provenance (sample): `polemonium_boreale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-polemonium.json · `polemonium_caeruleum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `saponaria_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C115 (n=3, mean_d=1.098, max_d=1.585)

- Shared aperture: tricol*
- Size classes: medium; mid range: (41.0, 43.8)
- Shared sculpture tokens: striaat
- Members:
  - `prunus_domestica` | *Prunus domestica* | unranked | ap=tricol* | class=medium | mid=43.8µm | size_src=yaml | sc={striaat}
  - `prunus_laurocerasus` | *Prunus laurocerasus* | unranked | ap=tricol* | class=medium | mid=42.5µm | size_src=yaml | sc={striaat}
  - `prunus_spinoza` | *Prunus spinosa* | unranked | ap=tricol* | class=medium | mid=41.0µm | size_src=yaml | sc={striaat}
- Closest pair evidence `prunus_laurocerasus`–`prunus_spinoza` (d=0.485): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['striaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.485}`
- Provenance (sample): `prunus_domestica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_laurocerasus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `prunus_spinoza`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C116 (n=3, mean_d=1.197, max_d=1.620)

- Shared aperture: peripor*
- Size classes: medium; mid range: (33.0, 33.5)
- Shared sculpture tokens: —
- Members:
  - `ribes_sanguineum` | *Ribes sanguineum* | unranked | ap=peripor* | class=medium | mid=33.0µm | size_src=yaml | sc={psilaat,scabraat}
  - `ribes_uva_crispa` | *Ribes uva* | unranked | ap=peripor* | class=medium | mid=33.0µm | size_src=yaml
  - `ulmus_typ` | *Ulmus typ* | unranked | ap=peripor* | class=medium | mid=33.5µm | size_src=yaml | sc={reticulaat,rugulaat,scabraat}
- Closest pair evidence `ribes_sanguineum`–`ribes_uva_crispa` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 0.925}`
- Provenance (sample): `ribes_sanguineum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ribes_uva_crispa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `ulmus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C117 (n=3, mean_d=0.989, max_d=1.021)

- Shared aperture: tricol*
- Size classes: medium; mid range: (32.0, 32.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `stachys_sylvatica` | *Stachys sylvatica* | unranked | ap=tricol* | class=medium | mid=32.4µm | size_src=yaml | sc={reticulaat}
  - `syringa_vulgaris` | *Syringa vulgaris* | unranked | ap=tricol* | class=medium | mid=32.2µm | size_src=yaml | sc={reticulaat}
  - `tropaeolum_majus` | *Tropaeolum majus* | unranked | ap=tricol* | class=medium | mid=32.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `stachys_sylvatica`–`syringa_vulgaris` (d=0.961): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.15, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.961}`
- Provenance (sample): `stachys_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `syringa_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `tropaeolum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C118 (n=3, mean_d=0.925, max_d=0.925)

- Shared aperture: tricol*
- Size classes: medium; mid range: (47.0, 47.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `trifolium_incarnat` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
  - `trifolium_incarnatum` | *Trifolium incarnatum* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
  - `vicia_faba` | *Vicia faba* | unranked | ap=tricol* | class=medium | mid=47.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `trifolium_incarnat`–`trifolium_incarnatum` (d=0.925): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `trifolium_incarnat`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `trifolium_incarnatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vicia_faba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C119 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: peripor*
- Size classes: very-large; mid range: (175.0, 175.0)
- Shared sculpture tokens: echinaat
- Members:
  - `abelmoschus_esculentus` | *Abelmoschus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | size_src=yaml | sc={echinaat}
  - `hibiscus_esculent` | *Hibiscus esculentus* | unranked | ap=peripor* | class=very-large | mid=175.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `abelmoschus_esculentus`–`hibiscus_esculent` (d=0.125): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same very-large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.125}`
- Provenance (sample): `abelmoschus_esculentus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `hibiscus_esculent`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C120 (n=2, mean_d=1.197, max_d=1.197)

- Shared aperture: tricol*
- Size classes: medium; mid range: (34.8, 35.1)
- Shared sculpture tokens: striaat
- Members:
  - `acer_campestre` | *Acer campestre* | unranked | ap=tricol* | class=medium | mid=34.8µm | size_src=yaml | sc={rugulaat,striaat}
  - `saxifraga_umbrosa` | *Saxifraga umbrosa* | unranked | ap=tricol* | class=medium | mid=35.1µm | size_src=yaml | sc={striaat}
- Closest pair evidence `acer_campestre`–`saxifraga_umbrosa` (d=1.197): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['striaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.197}`
- Provenance (sample): `acer_campestre`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `saxifraga_umbrosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C121 (n=2, mean_d=1.395, max_d=1.395)

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.0, 37.5)
- Shared sculpture tokens: rugulaat, striaat
- Members:
  - `acer_pseudoplatanus` | *Acer pseudoplatanus* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={rugulaat,striaat,verrucaat}
  - `rhinanthus_alectorolophus` | *Rhinanthus alectorolophus* | unranked | ap=tricol* | class=medium | mid=37.0µm | size_src=yaml | sc={rugulaat,scabraat,striaat}
- Closest pair evidence `acer_pseudoplatanus`–`rhinanthus_alectorolophus` (d=1.395): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat', 'striaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.5, 'shared': ['driehoekig', 'oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.395}`
- Provenance (sample): `acer_pseudoplatanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `rhinanthus_alectorolophus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C122 (n=2, mean_d=1.427, max_d=1.427)

- Shared aperture: monocol*
- Size classes: large; mid range: (72.7, 75.0)
- Shared sculpture tokens: reticulaat, rugulaat
- Members:
  - `agave_striata` | *Agave striata* | unranked | ap=monocol* | class=large | mid=75.0µm | size_src=yaml | sc={reticulaat,rugulaat}
  - `liriodendron_tulipifera` | *Liriodendron tulipifera* | unranked | ap=monocol* | class=large | mid=72.7µm | size_src=beug | yaml_size_MASKED | sc={reticulaat,rugulaat,verrucaat}
- Closest pair evidence `agave_striata`–`liriodendron_tulipifera` (d=1.427): `{'aperture': 'same monocol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug09-monocolpatae-magnoliaceae.json', 'size_class': 'same large', 'size_mid_gap_um': 2.3, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['reticulaat', 'rugulaat']}, 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.427}`
- Provenance (sample): `agave_striata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `liriodendron_tulipifera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C123 (n=2, mean_d=0.920, max_d=0.920)

- Shared aperture: tricol*
- Size classes: large; mid range: (75.0, 75.5)
- Shared sculpture tokens: —
- Members:
  - `agrimonia_odorata` | *Agrimonia odorata* | unranked | ap=tricol* | class=large | mid=75.5µm | size_src=yaml | sculpt_MASKED
  - `geranium_typ` | *Geranium typ* | unranked | ap=tricol* | class=large | mid=75.0µm | size_src=yaml | sc={grof,reticulaat}
- Closest pair evidence `agrimonia_odorata`–`geranium_typ` (d=0.920): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.92}`
- Provenance (sample): `agrimonia_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `geranium_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C124 (n=2, mean_d=1.725, max_d=1.725)

- Shared aperture: tricol*
- Size classes: small; mid range: (13.0, 13.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `alchemilla_acutiloba` | *Alchemilla acutiloba* | unranked | ap=tricol* | sc={psilaat}
  - `cynoglossum_officinale` | *Cynoglossum officinale* | unranked | ap=tricol* | class=small | mid=13.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `alchemilla_acutiloba`–`cynoglossum_officinale` (d=1.725): `{'aperture': 'same tricol*', 'size': 'missing_one_or_both', 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['driehoekig']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.725}`
- Provenance (sample): `alchemilla_acutiloba`: eide:docs/keys/eide/rosaceae-eide.json · `cynoglossum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C125 (n=2, mean_d=1.069, max_d=1.069)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.9, 24.6)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `alchemilla_alpina` | *Alchemilla alpina* | unranked | ap=tricol* | class=medium | mid=23.9µm | size_src=yaml | sc={psilaat}
  - `veronica_arvensis` | *Veronica arvensis* | unranked | ap=tricol* | class=medium | mid=24.6µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `alchemilla_alpina`–`veronica_arvensis` (d=1.069): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.6, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.069}`
- Provenance (sample): `alchemilla_alpina`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C126 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: peripor*
- Size classes: medium; mid range: (25.4, 25.4)
- Shared sculpture tokens: —
- Members:
  - `alisma_lanceolatum` | *Alisma lanceolatum* | unranked | ap=peripor* | class=medium | mid=25.4µm | size_src=yaml
  - `plantago_lanceolata` | *Plantago Lanceolata* | unranked | ap=peripor* | class=medium | mid=25.4µm | size_src=beug | sc={verrucaat}
- Closest pair evidence `alisma_lanceolatum`–`plantago_lanceolata` (d=0.925): `{'aperture': 'same peripor*', 'size_source': 'yaml vs beug:docs/keys/beug/beug33-periporatae-plantago-lanceolata.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.925}`
- Provenance (sample): `alisma_lanceolatum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `plantago_lanceolata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug33-periporatae-plantaginaceae.json

### C127 (n=2, mean_d=0.949, max_d=0.949)

- Shared aperture: monocol*
- Size classes: medium; mid range: (43.9, 44.0)
- Shared sculpture tokens: —
- Members:
  - `allium_oleraceum` | *Allium oleraceum* | unranked | ap=monocol* | class=medium | mid=43.9µm | size_src=yaml
  - `tradescantia_andersoniana` | *Tradescantia andersoniana* | unranked | ap=monocol* | class=medium | mid=44.0µm | size_src=yaml | sc={rugulaat,verrucaat}
- Closest pair evidence `allium_oleraceum`–`tradescantia_andersoniana` (d=0.949): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.949}`
- Provenance (sample): `allium_oleraceum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `tradescantia_andersoniana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C128 (n=2, mean_d=1.697, max_d=1.697)

- Shared aperture: peripor*
- Size classes: large; mid range: (84.2, 84.5)
- Shared sculpture tokens: —
- Members:
  - `althaea_officinalis` | *Althaea officinalis* | unranked | ap=peripor* | class=large | mid=84.5µm | size_src=yaml
  - `calystegia_sepium` | *Calystegia sepium* | unranked | ap=peripor* | class=large | mid=84.2µm | size_src=beug | sc={gemmaat,psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `althaea_officinalis`–`calystegia_sepium` (d=1.697): `{'aperture': 'same peripor*', 'size_source': 'yaml vs beug:docs/keys/beug/beug33-periporatae-calystegia.json', 'size_class': 'same large', 'size_mid_gap_um': 0.3, 'sculpture': 'missing_one_or_both', 'beug_fam': 'mismatch peripor/dipor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.697}`
- Provenance (sample): `althaea_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `calystegia_sepium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C129 (n=2, mean_d=1.695, max_d=1.695)

- Shared aperture: tricol*
- Size classes: small; mid range: (19.0, 19.5)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); morph-bin group, not confirmed lookalike.
- Members:
  - `anethum_graveolens` | *Anethum graveolens* | unranked | ap=tricol* | class=small | mid=19.0µm | size_src=yaml | sc={gemmaat,microreticulaat,reticulaat,scabraat,verrucaat}
  - `foeniculum_vulgaris` | *Foeniculum vulgaris* | unranked | ap=tricol* | class=small | mid=19.5µm | size_src=yaml | sc={scabraat}
- Closest pair evidence `anethum_graveolens`–`foeniculum_vulgaris` (d=1.695): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.8, 'shared': ['scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.695}`
- Provenance (sample): `anethum_graveolens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C130 (n=2, mean_d=1.221, max_d=1.221)

- Shared aperture: tricol*
- Size classes: medium; mid range: (36.2, 36.6)
- Shared sculpture tokens: rugulaat
- Members:
  - `angelica_archangelica` | *Angelica archangelica* | unranked | ap=tricol* | class=medium | mid=36.2µm | size_src=yaml | sc={rugulaat}
  - `rosa_gallica_officinalis` | *Rosa gallica officinalis* | unranked | ap=tricol* | class=medium | mid=36.6µm | size_src=yaml | sc={rugulaat,scabraat}
- Closest pair evidence `angelica_archangelica`–`rosa_gallica_officinalis` (d=1.221): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['rugulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.221}`
- Provenance (sample): `angelica_archangelica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture · `rosa_gallica_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C131 (n=2, mean_d=1.257, max_d=1.257)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.9, 23.4)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `anthriscus_caucalis` | *Anthriscus caucalis* | unranked | ap=tricol* | class=medium | mid=23.4µm | size_src=yaml | sc={psilaat}
  - `artemisia_dracunculus` | *Artemisia dracunculus* | unranked | ap=tricol* | class=medium | mid=22.9µm | size_src=yaml | sc={echinaat,psilaat}
- Closest pair evidence `anthriscus_caucalis`–`artemisia_dracunculus` (d=1.257): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.55, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.257}`
- Provenance (sample): `anthriscus_caucalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `artemisia_dracunculus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C132 (n=2, mean_d=1.125, max_d=1.125)

- Shared aperture: tripor*
- Size classes: medium; mid range: (50.0, 50.0)
- Shared sculpture tokens: echinaat
- Members:
  - `arcticum_lappa` | *Arctium lappa* | unranked | ap=tripor* | class=medium | mid=50.0µm | size_src=yaml | sc={echinaat,verrucaat}
  - `arcticum_majus` | *Arcticum majus* | unranked | ap=tripor* | class=medium | mid=50.0µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `arcticum_lappa`–`arcticum_majus` (d=1.125): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `arcticum_lappa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `arcticum_majus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C133 (n=2, mean_d=1.245, max_d=1.245)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.5, 22.0)
- Shared sculpture tokens: echinaat
- **Human review (species↔*_typ):** artemisia_vulgaris ↔ artemisia_typ
- Members:
  - `artemisia_typ` | *Artemisia typ* | unranked | ap=tricol* | class=small | mid=22.0µm | size_src=yaml | sc={echinaat}
  - `artemisia_vulgaris` | *Artemisia vulgaris* | unranked | ap=tricol* | class=small | mid=21.5µm | size_src=yaml | sc={echinaat,reticulaat}
- Closest pair evidence `artemisia_typ`–`artemisia_vulgaris` (d=1.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.245}`
- Provenance (sample): `artemisia_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `artemisia_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C134 (n=2, mean_d=1.009, max_d=1.009)

- Shared aperture: tripor*
- Size classes: medium; mid range: (24.1, 24.5)
- Shared sculpture tokens: —
- Members:
  - `betula_nigra` | *Betula nigra* | unranked | ap=tripor* | class=medium | mid=24.5µm | size_src=yaml | sc={psilaat}
  - `humulus_lupulus` | *Humulus lupulus* | unranked | ap=tripor* | class=medium | mid=24.1µm | size_src=yaml
- Closest pair evidence `betula_nigra`–`humulus_lupulus` (d=1.009): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.35, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same tripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.009}`
- Provenance (sample): `betula_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `humulus_lupulus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C135 (n=2, mean_d=1.521, max_d=1.521)

- Shared aperture: tripor*
- Size classes: medium; mid range: (27.0, 28.6)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); morph-bin group, not confirmed lookalike.
- Members:
  - `betula_pendula` | *Betula pendula* | unranked | ap=tripor* | class=medium | mid=28.6µm | size_src=yaml | sc={reticulaat,scabraat}
  - `corylus_avellana` | *Corylus avellana* | unranked | ap=tripor* | class=medium | mid=27.0µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `betula_pendula`–`corylus_avellana` (d=1.521): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.65, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['scabraat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.521}`
- Provenance (sample): `betula_pendula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `corylus_avellana`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C136 (n=2, mean_d=1.528, max_d=1.528)

- Shared aperture: stephanocolpor*
- Size classes: medium; mid range: (30.3, 32.5)
- Shared sculpture tokens: —
- Members:
  - `borrago_officinalis` | *Borrago officinalis* | unranked | ap=stephanocolpor* | class=medium | mid=32.5µm | size_src=yaml | sc={scabraat,verrucaat}
  - `sanguisorba_officinalis` | *Sanguisorba officinalis* | unranked | ap=stephanocolpor* | class=medium | mid=30.3µm | size_src=yaml | sculpt_MASKED
- Closest pair evidence `borrago_officinalis`–`sanguisorba_officinalis` (d=1.528): `{'aperture': 'same stephanocolpor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.2, 'sculpture': 'masked_conflict', 'shape': {'jaccard_dist': 0.75, 'shared': ['oblaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.528}`
- Provenance (sample): `borrago_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sanguisorba_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C137 (n=2, mean_d=1.441, max_d=1.441)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (30.4, 32.5)
- Shared sculpture tokens: —
- Members:
  - `campanula_glomerata` | *Campanula glomerata* | unranked | ap=stephanopor* | class=medium | mid=30.4µm | size_src=yaml
  - `campanula_patula` | *Campanula patula* | unranked | ap=stephanopor* | class=medium | mid=32.5µm | size_src=yaml
- Closest pair evidence `campanula_glomerata`–`campanula_patula` (d=1.441): `{'aperture': 'same stephanopor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.15, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.441}`
- Provenance (sample): `campanula_glomerata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `campanula_patula`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C138 (n=2, mean_d=1.201, max_d=1.201)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (42.4, 43.5)
- Shared sculpture tokens: —
- Members:
  - `campanula_medium` | *Campanula medium* | unranked | ap=stephanopor* | class=medium | mid=42.4µm | size_src=beug | sc={echinaat,microechinaat}
  - `campanula_rapunculoides` | *Campanula rapunculoides* | unranked | ap=stephanopor* | class=medium | mid=43.5µm | size_src=yaml
- Closest pair evidence `campanula_medium`–`campanula_rapunculoides` (d=1.201): `{'aperture': 'same stephanopor*', 'size_source': 'beug:docs/keys/beug/beug32-stephanoporatae-campanula-medium.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.15, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.201}`
- Provenance (sample): `campanula_medium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug32-stephanoporatae-campanula-medium.json · `campanula_rapunculoides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C139 (n=2, mean_d=1.045, max_d=1.045)

- Shared aperture: stephanopor*
- Size classes: medium; mid range: (38.5, 39.0)
- Shared sculpture tokens: —
- Members:
  - `campanula_persicifolia` | *Campanula persicifolia* | unranked | ap=stephanopor* | class=medium | mid=38.5µm | size_src=yaml
  - `juglans_regia` | *Juglans regia* | unranked | ap=stephanopor* | class=medium | mid=39.0µm | size_src=yaml | sc={psilaat,reticulaat,scabraat}
- Closest pair evidence `campanula_persicifolia`–`juglans_regia` (d=1.045): `{'aperture': 'same stephanopor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.045}`
- Provenance (sample): `campanula_persicifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `juglans_regia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C140 (n=2, mean_d=1.525, max_d=1.525)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.5, 25.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); morph-bin group, not confirmed lookalike.
- Members:
  - `caragana_arborescens` | *Caragana arborescens* | unranked | ap=tricol* | class=small | mid=22.5µm | size_src=yaml | sc={scabraat}
  - `foeniculum_vulga` | *Foeniculum vulga* | unranked | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={scabraat}
- Closest pair evidence `caragana_arborescens`–`foeniculum_vulga` (d=1.525): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat']}, 'coarse_sculpt_penalty': 'scabraat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.525}`
- Provenance (sample): `caragana_arborescens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `foeniculum_vulga`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C141 (n=2, mean_d=1.731, max_d=1.731)

- Shared aperture: peripor*
- Size classes: large; mid range: (49.5, 51.4)
- Shared sculpture tokens: reticulaat, verrucaat
- Members:
  - `carex_typ` | *Carex typ* | unranked | ap=peripor* | class=large | mid=49.5µm | size_src=yaml | sc={reticulaat,verrucaat}
  - `persicaria_maculosa` | *Persicaria maculosa* | unranked | ap=peripor* | class=large | mid=51.4µm | size_src=beug | path_gate=0–60 | sc={echinaat,microechinaat,reticulaat,striaat,verrucaat}
- Closest pair evidence `carex_typ`–`persicaria_maculosa` (d=1.731): `{'aperture': 'same peripor*', 'size_source': 'yaml vs beug:docs/keys/beug/beug33-periporatae-persicaria.json', 'size_class': 'same large', 'size_mid_gap_um': 1.9, 'sculpture': {'jaccard_dist': 0.6, 'shared': ['reticulaat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.731}`
- Provenance (sample): `carex_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `persicaria_maculosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C142 (n=2, mean_d=1.625, max_d=1.625)

- Shared aperture: tricol*
- Size classes: large; mid range: (61.0, 61.0)
- Shared sculpture tokens: —
- Members:
  - `carthamus_tinctorius` | *Carthamus tinctorius* | unranked | ap=tricol* | class=large | mid=61.0µm | size_src=yaml | sc={echinaat}
  - `convolvulus_arve` | *Convolvulus arve* | unranked | ap=tricol* | class=large | mid=61.0µm | size_src=yaml | sc={scabraat}
- Closest pair evidence `carthamus_tinctorius`–`convolvulus_arve` (d=1.625): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 1.0, 'shared': []}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.625}`
- Provenance (sample): `carthamus_tinctorius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `convolvulus_arve`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C143 (n=2, mean_d=1.043, max_d=1.043)

- Shared aperture: tricol*
- Size classes: medium; mid range: (24.5, 25.2)
- Shared sculpture tokens: fijn, reticulaat
- Members:
  - `cercis_siliquastrum` | *Cercis siliquastrum* | unranked | ap=tricol* | class=medium | mid=25.2µm | size_src=beug | path_gate=20–28 | sc={fijn,microreticulaat,reticulaat}
  - `mercurialis_typ` | *Mercurialis typ* | unranked | ap=tricol* | class=medium | mid=24.5µm | size_src=yaml | sc={fijn,reticulaat}
- Closest pair evidence `cercis_siliquastrum`–`mercurialis_typ` (d=1.043): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug23-tricolporoidatae-ret-cercis.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.7, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['fijn', 'reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.043}`
- Provenance (sample): `cercis_siliquastrum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `mercurialis_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C144 (n=2, mean_d=0.125, max_d=0.125)

- Shared aperture: tripor*
- Size classes: large; mid range: (82.0, 82.0)
- Shared sculpture tokens: psilaat, rugulaat
- Members:
  - `chamerion_angustifolium` | *Chamerion angustifolium (synoniem: Epilobium angustifolium)* | unranked | ap=tripor* | class=large | mid=82.0µm | size_src=yaml | sc={psilaat,rugulaat}
  - `epilobium_angustifolium` | *Epilobium angustifolium* | unranked | ap=tripor* | class=large | mid=82.0µm | size_src=yaml | sc={psilaat,rugulaat}
- Closest pair evidence `chamerion_angustifolium`–`epilobium_angustifolium` (d=0.125): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'rugulaat']}, 'beug_fam': 'same tripor', 'shape': {'jaccard_dist': 0.0, 'shared': ['driehoekig', 'oblaat', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.125}`
- Provenance (sample): `chamerion_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `epilobium_angustifolium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C145 (n=2, mean_d=1.245, max_d=1.245)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.0, 38.5)
- Shared sculpture tokens: echinaat
- Members:
  - `cichorium_intybus` | *Cichorium intybus* | unranked | ap=tricol* | class=medium | mid=38.0µm | size_src=yaml | sc={echinaat}
  - `erica_tetralix` | *Erica tetralix* | unranked | ap=tricol* | class=medium | mid=38.5µm | size_src=yaml | sc={echinaat,verrucaat}
- Closest pair evidence `cichorium_intybus`–`erica_tetralix` (d=1.245): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['echinaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.245}`
- Provenance (sample): `cichorium_intybus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `erica_tetralix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C146 (n=2, mean_d=1.221, max_d=1.221)

- Shared aperture: tricol*
- Size classes: large; mid range: (49.0, 49.4)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `cistus_incanus` | *Cistus incanus* | unranked | ap=tricol* | class=large | mid=49.4µm | size_src=yaml | sc={reticulaat}
  - `helianthemum_nummularium` | *Helianthemum nummularium* | unranked | ap=tricol* | class=large | mid=49.0µm | size_src=beug | sc={reticulaat,striaat}
- Closest pair evidence `cistus_incanus`–`helianthemum_nummularium` (d=1.221): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug19-tricolporatae-str-helianthemum.json', 'size_class': 'same large', 'size_mid_gap_um': 0.4, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.221}`
- Provenance (sample): `cistus_incanus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `helianthemum_nummularium`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug19-tricolporatae-str-helianthemum.json

### C147 (n=2, mean_d=1.285, max_d=1.285)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (23.5, 25.0)
- Shared sculpture tokens: —
- Members:
  - `citrus_sinensis` | *Citrus sinensis* | unranked | ap=stephanocol* | class=small | mid=25.0µm | size_src=yaml
  - `eruca_sativa` | *Eruca sativa* | unranked | ap=stephanocol* | class=small | mid=23.5µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `citrus_sinensis`–`eruca_sativa` (d=1.285): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 1.5, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.285}`
- Provenance (sample): `citrus_sinensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eruca_sativa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C148 (n=2, mean_d=1.305, max_d=1.305)

- Shared aperture: tricol*
- Size classes: small; mid range: (22.0, 22.8)
- Shared sculpture tokens: verrucaat
- Members:
  - `clematis_recta` | *Clematis recta* | unranked | ap=tricol* | class=small | mid=22.8µm | size_src=yaml | sc={scabraat,verrucaat}
  - `eucalyptus_camaldulensis` | *Eucalyptus camaldulensis* | unranked | ap=tricol* | class=small | mid=22.0µm | size_src=yaml | sc={verrucaat}
- Closest pair evidence `clematis_recta`–`eucalyptus_camaldulensis` (d=1.305): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.75, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.305}`
- Provenance (sample): `clematis_recta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `eucalyptus_camaldulensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C149 (n=2, mean_d=0.507, max_d=0.507)

- Shared aperture: tricol*
- Size classes: large; mid range: (54.7, 55.2)
- Shared sculpture tokens: echinaat
- Members:
  - `cynara_cardunculus` | *Cynara cardunculus* | unranked | ap=tricol* | class=large | mid=55.2µm | size_src=yaml | sc={echinaat}
  - `lonicera_xylosteum` | *Lonicera xylosteum* | unranked | ap=tricol* | class=large | mid=54.7µm | size_src=beug | path_gate=28–45 | sc={echinaat}
- Closest pair evidence `cynara_cardunculus`–`lonicera_xylosteum` (d=0.507): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug17-ttt-ech-lonicera.json', 'size_class': 'same large', 'size_mid_gap_um': 0.55, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.507}`
- Provenance (sample): `cynara_cardunculus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_xylosteum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C150 (n=2, mean_d=1.441, max_d=1.441)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (9.5, 11.7)
- Shared sculpture tokens: —
- Members:
  - `cynoglossum_creticum` | *Cynoglossum creticum* | unranked | ap=heterocol* | class=very-small | mid=9.5µm | size_src=yaml
  - `myosotis_ramosissima` | *Myosotis ramosissima* | unranked | ap=heterocol* | class=very-small | mid=11.7µm | size_src=yaml
- Closest pair evidence `cynoglossum_creticum`–`myosotis_ramosissima` (d=1.441): `{'aperture': 'same heterocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same very-small', 'size_mid_gap_um': 2.15, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same heterocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.441}`
- Provenance (sample): `cynoglossum_creticum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_ramosissima`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C151 (n=2, mean_d=0.711, max_d=0.711)

- Shared aperture: tricol*
- Size classes: large; mid range: (73.4, 74.8)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_pilosus` | *Dipsacus pilosus* | unranked | ap=tricol* | class=large | mid=74.8µm | size_src=yaml | sc={echinaat}
  - `lonicera_caprifolium` | *Lonicera Caprifolium* | unranked | ap=tricol* | class=large | mid=73.4µm | size_src=yaml | sc={echinaat}
- Closest pair evidence `dipsacus_pilosus`–`lonicera_caprifolium` (d=0.711): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['echinaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.711}`
- Provenance (sample): `dipsacus_pilosus`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lonicera_caprifolium`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C152 (n=2, mean_d=1.370, max_d=1.370)

- Shared aperture: fenestr*
- Size classes: large; mid range: (80.0, 80.5)
- Shared sculpture tokens: echinaat
- Members:
  - `dipsacus_typ` | *Dipsacus typ* | unranked | ap=fenestr* | class=large | mid=80.5µm | size_src=yaml | sc={echinaat}
  - `portulacca_oleacera` | *Portulaca oleracea* | unranked | ap=fenestr* | class=large | mid=80.0µm | size_src=yaml | sc={echinaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `dipsacus_typ`–`portulacca_oleacera` (d=1.370): `{'aperture': 'same fenestr*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.75, 'shared': ['echinaat']}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.37}`
- Provenance (sample): `dipsacus_typ`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:shape; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json · `portulacca_oleacera`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C153 (n=2, mean_d=1.403, max_d=1.403)

- Shared aperture: tricol*
- Size classes: medium; mid range: (40.1, 42.3)
- Shared sculpture tokens: echinaat, microechinaat, psilaat, scabraat
- Members:
  - `eranthis_hyemalis` | *Eranthis hyemalis* | unranked | ap=tricol* | class=medium | mid=42.3µm | size_src=beug | sc={echinaat,microechinaat,psilaat,scabraat}
  - `nigella_arvensis` | *Nigella arvensis* | unranked | ap=tricol* | class=medium | mid=40.1µm | size_src=beug | sc={echinaat,fijn,grof,microechinaat,psilaat}
- Closest pair evidence `eranthis_hyemalis`–`nigella_arvensis` (d=1.403): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug13-tricolpatae-ps.json vs beug:docs/keys/beug/beug13-tricolpatae-ps.json', 'size_class': 'same medium', 'size_mid_gap_um': 2.2, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['echinaat', 'microechinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.403}`
- Provenance (sample): `eranthis_hyemalis`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug13-tricolpatae-ps.json · `nigella_arvensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C154 (n=2, mean_d=1.305, max_d=1.305)

- Shared aperture: tricol*
- Size classes: medium; mid range: (30.0, 30.8)
- Shared sculpture tokens: verrucaat
- Members:
  - `erica_arborea` | *Erica arborea* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=yaml | sc={verrucaat}
  - `ranunculus_bulbosus` | *Ranunculus bulbosus* | unranked | ap=tricol* | class=medium | mid=30.8µm | size_src=yaml | sc={baculaat,verrucaat}
- Closest pair evidence `erica_arborea`–`ranunculus_bulbosus` (d=1.305): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.75, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.305}`
- Provenance (sample): `erica_arborea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `ranunculus_bulbosus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C155 (n=2, mean_d=1.177, max_d=1.177)

- Shared aperture: tricol*
- Size classes: large; mid range: (60.8, 61.8)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `eryngium_maritimum` | *Eryngium maritimum* | unranked | ap=tricol* | class=large | mid=60.8µm | size_src=yaml | sc={psilaat}
  - `orlaya_grandiflora` | *Orlaya grandiflora* | unranked | ap=tricol* | class=large | mid=61.8µm | size_src=beug | path_gate=54–67 | sc={psilaat}
- Closest pair evidence `eryngium_maritimum`–`orlaya_grandiflora` (d=1.177): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json', 'size_class': 'same large', 'size_mid_gap_um': 1.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.177}`
- Provenance (sample): `eryngium_maritimum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `orlaya_grandiflora`: data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C156 (n=2, mean_d=1.584, max_d=1.584)

- Shared aperture: tricol*
- Size classes: large; mid range: (47.4, 47.8)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `eryngium_planum` | *Eryngium planum* | unranked | ap=tricol* | class=large | mid=47.8µm | size_src=yaml | sc={psilaat}
  - `heracleum_sphondylium` | *Heracleum sphondylium* | unranked | ap=tricol* | class=large | mid=47.4µm | size_src=beug | sc={psilaat,reticulaat,scabraat,verrucaat}
- Closest pair evidence `eryngium_planum`–`heracleum_sphondylium` (d=1.584): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json', 'size_class': 'same large', 'size_mid_gap_um': 0.35, 'sculpture': {'jaccard_dist': 0.75, 'shared': ['psilaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.584}`
- Provenance (sample): `eryngium_planum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `heracleum_sphondylium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C157 (n=2, mean_d=1.249, max_d=1.249)

- Shared aperture: tricol*
- Size classes: medium; mid range: (39.6, 41.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `euphrasia_stricta` | *Euphrasia stricta* | unranked | ap=tricol* | class=medium | mid=41.0µm | size_src=yaml | sc={psilaat}
  - `veronica_austriaca_ssp_teucrium` | *Veronica austriaca* | unranked | ap=tricol* | class=medium | mid=39.6µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `euphrasia_stricta`–`veronica_austriaca_ssp_teucrium` (d=1.249): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.35, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.249}`
- Provenance (sample): `euphrasia_stricta`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `veronica_austriaca_ssp_teucrium`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C158 (n=2, mean_d=0.605, max_d=0.605)

- Shared aperture: tricol*
- Size classes: small; mid range: (14.0, 16.0)
- Shared sculpture tokens: clavaat, echinaat, fijn, microechinaat, psilaat, scabraat
- Members:
  - `filipendula_ulmaria` | *Filipendula ulmaria* | unranked | ap=tricol* | class=small | mid=14.0µm | size_src=yaml | sc={clavaat,echinaat,fijn,microechinaat,psilaat}
  - `filipendula_vulgaris` | *Filipendula vulgaris* | unranked | ap=tricol* | class=small | mid=16.0µm | size_src=yaml | sc={clavaat,echinaat,fijn,microechinaat,psilaat}
- Closest pair evidence `filipendula_ulmaria`–`filipendula_vulgaris` (d=0.605): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat', 'echinaat', 'fijn', 'microechinaat', 'psilaat', 'scabraat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.0, 'shared': ['prolaat', 'rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.605}`
- Provenance (sample): `filipendula_ulmaria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `filipendula_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C159 (n=2, mean_d=0.855, max_d=0.855)

- Shared aperture: tricol*
- Size classes: small; mid range: (21.0, 23.0)
- Shared sculpture tokens: grof, striaat
- Members:
  - `fragaria_vesca` | *Fragaria vesca* | unranked | ap=tricol* | class=small | mid=21.0µm | size_src=yaml | sc={grof,striaat}
  - `sibbaldia_procumbens` | *Sibbaldia procumbens* | unranked | ap=tricol* | class=small | mid=23.0µm | size_src=yaml | sc={grof,striaat}
- Closest pair evidence `fragaria_vesca`–`sibbaldia_procumbens` (d=0.855): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['grof', 'striaat']}, 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.855}`
- Provenance (sample): `fragaria_vesca`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sibbaldia_procumbens`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C160 (n=2, mean_d=0.887, max_d=0.887)

- Shared aperture: tricol*
- Size classes: medium; mid range: (23.1, 23.2)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `frangula_alnus` | *Frangula alnus* | unranked | ap=tricol* | class=medium | mid=23.2µm | size_src=beug | sc={psilaat,scabraat,verrucaat}
  - `melampyrum_pratense` | *Melampyrum pratense* | unranked | ap=tricol* | class=medium | mid=23.1µm | size_src=yaml | sc={scabraat,verrucaat}
- Closest pair evidence `frangula_alnus`–`melampyrum_pratense` (d=0.887): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug14-tricolporatae-ps.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['scabraat', 'verrucaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 0.887}`
- Provenance (sample): `frangula_alnus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `melampyrum_pratense`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C161 (n=2, mean_d=1.706, max_d=1.706)

- Shared aperture: stephanocol*
- Size classes: small; mid range: (20.0, 20.2)
- Shared sculpture tokens: reticulaat, scabraat
- Members:
  - `galium_odoratum` | *Galium odoratum (syn Asperula odorata)* | unranked | ap=stephanocol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat,scabraat}
  - `phacelia_tanacetifolia` | *Phacelia tanacetifolia* | unranked | ap=stephanocol* | class=small | mid=20.2µm | size_src=beug | sc={fijn,microreticulaat,psilaat,reticulaat,rugulaat}
- Closest pair evidence `galium_odoratum`–`phacelia_tanacetifolia` (d=1.706): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug24-stephanocolpatae-phacelia.json', 'size_class': 'same small', 'size_mid_gap_um': 0.2, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['reticulaat', 'scabraat']}, 'beug_fam': 'same stephanocol', 'shape': {'jaccard_dist': 0.667, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.7063}`
- Provenance (sample): `galium_odoratum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phacelia_tanacetifolia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C162 (n=2, mean_d=0.675, max_d=0.675)

- Shared aperture: tricol*
- Size classes: large; mid range: (78.3, 79.6)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_nodosum` | *Geranium nodosum* | unranked | ap=tricol* | class=large | mid=78.3µm | size_src=yaml | sc={clavaat}
  - `geranium_phaeum` | *Geranium phaeum* | unranked | ap=tricol* | class=large | mid=79.6µm | size_src=yaml | sc={clavaat}
- Closest pair evidence `geranium_nodosum`–`geranium_phaeum` (d=0.675): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.675}`
- Provenance (sample): `geranium_nodosum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_phaeum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C163 (n=2, mean_d=1.735, max_d=1.735)

- Shared aperture: tricol*
- Size classes: large; mid range: (64.8, 66.2)
- Shared sculpture tokens: clavaat
- Members:
  - `geranium_pyrenaicum` | *Geranium pyrenaicum* | unranked | ap=tricol* | class=large | mid=64.8µm | size_src=yaml | sc={clavaat}
  - `geranium_robertianum` | *Geranium robertianum* | unranked | ap=tricol* | class=large | mid=66.2µm | size_src=yaml | sc={clavaat,rugulaat,striaat}
- Closest pair evidence `geranium_pyrenaicum`–`geranium_robertianum` (d=1.735): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.5, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['clavaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.735}`
- Provenance (sample): `geranium_pyrenaicum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `geranium_robertianum`: data/pollen.yaml:size; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C164 (n=2, mean_d=1.478, max_d=1.478)

- Shared aperture: tricol*
- Size classes: medium; mid range: (35.3, 36.7)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat
- Members:
  - `hedera_helix` | *Hedera helix* | unranked | ap=tricol* | class=medium | mid=36.7µm | size_src=beug | path_gate=32–42 | yaml_size_MASKED | sc={microreticulaat,psilaat,reticulaat,striaat}
  - `robinia_pseudoacacia` | *Robinia pseudoacacia* | unranked | ap=tricol* | class=medium | mid=35.3µm | size_src=beug | path_gate=30–40 | yaml_size_MASKED | sc={grof,microreticulaat,psilaat,reticulaat,rugulaat}
- Closest pair evidence `hedera_helix`–`robinia_pseudoacacia` (d=1.478): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug22-tricolporatae-ret-hedera.json vs beug:docs/keys/beug/beug23-tricolporoidatae-ret-robinia.json', 'path_gate': 'overlap 32.0–42.0 / 30.0–40.0', 'size_class': 'same medium', 'size_mid_gap_um': 1.4, 'sculpture': {'jaccard_dist': 0.571, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 0.2, 'shared': ['driehoekig', 'prolaat', 'rond', 'sferoid']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.4781}`
- Provenance (sample): `hedera_helix`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `robinia_pseudoacacia`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C165 (n=2, mean_d=1.125, max_d=1.125)

- Shared aperture: monocol*
- Size classes: medium; mid range: (45.0, 45.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `hyacinthus_orientalis` | *Hyacinthus orientalis* | unranked | ap=monocol* | class=medium | mid=45.0µm | size_src=yaml | sc={reticulaat}
  - `narcissus_typ` | *Narcissus typ* | unranked | ap=monocol* | class=medium | mid=45.0µm | size_src=yaml | sc={reticulaat,scabraat}
- Closest pair evidence `hyacinthus_orientalis`–`narcissus_typ` (d=1.125): `{'aperture': 'same monocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.5, 'shared': ['reticulaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.125}`
- Provenance (sample): `hyacinthus_orientalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `narcissus_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C166 (n=2, mean_d=1.225, max_d=1.225)

- Shared aperture: tricol*
- Size classes: very-small; mid range: (11.2, 12.5)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `hydrangea_typ` | *Hydrangea typ* | unranked | ap=tricol* | class=very-small | mid=11.2µm | size_src=yaml | sc={psilaat}
  - `spiraea_japonica` | *Spiraea japonica* | unranked | ap=tricol* | class=very-small | mid=12.5µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `hydrangea_typ`–`spiraea_japonica` (d=1.225): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same very-small', 'size_mid_gap_um': 1.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'coarse_sculpt_penalty': 'psilaat', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.225}`
- Provenance (sample): `hydrangea_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `spiraea_japonica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C167 (n=2, mean_d=1.045, max_d=1.045)

- Shared aperture: tricol*
- Size classes: medium; mid range: (22.1, 22.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `hypericum_montanum` | *Hypericum montanum* | unranked | ap=tricol* | class=medium | mid=22.6µm | size_src=yaml | sc={reticulaat}
  - `lysimachia_nemorum` | *Lysimachia nemorum* | unranked | ap=tricol* | class=medium | mid=22.1µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `hypericum_montanum`–`lysimachia_nemorum` (d=1.045): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.045}`
- Provenance (sample): `hypericum_montanum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `lysimachia_nemorum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C168 (n=2, mean_d=0.740, max_d=0.740)

- Shared aperture: inapert*
- Size classes: medium; mid range: (26.0, 27.0)
- Shared sculpture tokens: reticulaat, scabraat, verrucaat
- Members:
  - `juniperus_communis` | *Juniperus communis* | unranked | ap=inapert* | class=medium | mid=26.0µm | size_src=yaml | sc={gemmaat,reticulaat,scabraat,verrucaat}
  - `taxus_baccata` | *Taxus baccata* | unranked | ap=inapert* | class=medium | mid=27.0µm | size_src=yaml | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `juniperus_communis`–`taxus_baccata` (d=0.740): `{'aperture': 'same inapert*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.0, 'sculpture': {'jaccard_dist': 0.25, 'shared': ['reticulaat', 'scabraat', 'verrucaat']}, 'beug_fam': 'same inapert', 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.74}`
- Provenance (sample): `juniperus_communis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `taxus_baccata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C169 (n=2, mean_d=1.421, max_d=1.421)

- Shared aperture: tricol*
- Size classes: medium; mid range: (27.1, 30.0)
- Shared sculpture tokens: microreticulaat, psilaat, reticulaat
- Members:
  - `lamium_album` | *Lamium album* | unranked | ap=tricol* | class=medium | mid=27.1µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat}
  - `viola_odorata` | *Viola odorata* | unranked | ap=tricol* | class=medium | mid=30.0µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat}
- Closest pair evidence `lamium_album`–`viola_odorata` (d=1.421): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug13-tricolpatae-ps.json vs beug:docs/keys/beug/beug13-tricolpatae-ps.json', 'size_class': 'same medium', 'size_mid_gap_um': 2.9, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['microreticulaat', 'psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.75, 'shared': ['prolaat']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.421}`
- Provenance (sample): `lamium_album`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `viola_odorata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C170 (n=2, mean_d=1.355, max_d=1.355)

- Shared aperture: tricol*
- Size classes: medium; mid range: (31.0, 33.0)
- Shared sculpture tokens: fijn, striaat
- Members:
  - `malus_sylvestris` | *Malus sylvestris* | unranked | ap=tricol* | class=medium | mid=31.0µm | size_src=yaml | sc={fijn,rugulaat,striaat}
  - `rosa_pimpinellifolia` | *Rosa pimpinellifolia* | unranked | ap=tricol* | class=medium | mid=33.0µm | size_src=yaml | sc={fijn,striaat}
- Closest pair evidence `malus_sylvestris`–`rosa_pimpinellifolia` (d=1.355): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 2.0, 'sculpture': {'jaccard_dist': 0.333, 'shared': ['fijn', 'striaat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.355}`
- Provenance (sample): `malus_sylvestris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `rosa_pimpinellifolia`: data/pollen.yaml:size; eide:docs/keys/eide/rosaceae-eide.json

### C171 (n=2, mean_d=1.495, max_d=1.495)

- Shared aperture: tricol*
- Size classes: medium; mid range: (44.5, 45.0)
- Shared sculpture tokens: scabraat
- **Low specificity:** shared sculpture is a single coarse token (`scabraat`); morph-bin group, not confirmed lookalike.
- Members:
  - `mespilus_germani` | *Mespilus germani* | unranked | ap=tricol* | class=medium | mid=45.0µm | size_src=yaml | sc={scabraat,striaat}
  - `tordylium_apulum` | *Tordylium apulum* | unranked | ap=tricol* | class=medium | mid=44.5µm | size_src=beug | path_gate=39–200 | yaml_size_MASKED | sc={rugulaat,scabraat}
- Closest pair evidence `mespilus_germani`–`tordylium_apulum` (d=1.495): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug14-tricolpatae-ps-apiaceae.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.667, 'shared': ['scabraat']}, 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.495}`
- Provenance (sample): `mespilus_germani`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `tordylium_apulum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C172 (n=2, mean_d=1.489, max_d=1.489)

- Shared aperture: tetrade*
- Size classes: large; mid range: (45.3, 47.6)
- Shared sculpture tokens: —
- Members:
  - `moneses_uniflora` | *Moneses uniflora* | unranked | ap=tetrade* | class=large | mid=45.3µm | size_src=beug | sc={scabraat,verrucaat}
  - `vaccinium_uliginosum` | *Vaccinium uliginosum* | unranked | ap=tetrade* | class=large | mid=47.6µm | size_src=yaml
- Closest pair evidence `moneses_uniflora`–`vaccinium_uliginosum` (d=1.489): `{'aperture': 'same tetrade*', 'size_source': 'beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 2.35, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.489}`
- Provenance (sample): `moneses_uniflora`: data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json; size_preferred:beug:docs/keys/beug/beug04-tetradeae-ericaceae-empetrum.json · `vaccinium_uliginosum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C173 (n=2, mean_d=1.081, max_d=1.081)

- Shared aperture: heterocol*
- Size classes: very-small; mid range: (6.0, 6.6)
- Shared sculpture tokens: —
- Members:
  - `myosotis_scorpioides` | *Myosotis scorpioides* | unranked | ap=heterocol* | class=very-small | mid=6.6µm | size_src=yaml | sc={psilaat}
  - `myosotis_sylvatica` | *Myosotis sylvatica* | unranked | ap=heterocol* | class=very-small | mid=6.0µm | size_src=beug | path_gate=0–18
- Closest pair evidence `myosotis_scorpioides`–`myosotis_sylvatica` (d=1.081): `{'aperture': 'same heterocol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug28-heterocolpatae-myosotis-sylvatica.json', 'size_class': 'same very-small', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same heterocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.081}`
- Provenance (sample): `myosotis_scorpioides`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `myosotis_sylvatica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths

### C174 (n=2, mean_d=0.925, max_d=0.925)

- Shared aperture: stephanocol*
- Size classes: medium; mid range: (31.0, 31.0)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `nepeta_cataria` | *Nepeta cataria* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat}
  - `satureja_hortensis` | *Satureja hortensis* | unranked | ap=stephanocol* | class=medium | mid=31.0µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `nepeta_cataria`–`satureja_hortensis` (d=0.925): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.925}`
- Provenance (sample): `nepeta_cataria`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `satureja_hortensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; kerkvliet-analytic:docs/keys/kerkvliet/kerkvliet-determinatietabel.json

### C175 (n=2, mean_d=0.795, max_d=0.795)

- Shared aperture: tricol*
- Size classes: large; mid range: (46.6, 48.4)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `nigella_damascena` | *Nigella damascena* | unranked | ap=tricol* | class=large | mid=46.6µm | size_src=yaml | sc={psilaat,reticulaat}
  - `saxifraga_granulata` | *Saxifraga granulata* | unranked | ap=tricol* | class=large | mid=48.4µm | size_src=yaml | sc={psilaat,reticulaat}
- Closest pair evidence `nigella_damascena`–`saxifraga_granulata` (d=0.795): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.75, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.795}`
- Provenance (sample): `nigella_damascena`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `saxifraga_granulata`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C176 (n=2, mean_d=1.081, max_d=1.081)

- Shared aperture: monopor*
- Size classes: medium; mid range: (37.0, 37.6)
- Shared sculpture tokens: —
- Members:
  - `nymphaea_alba` | *Nymphaea alba* | unranked | ap=monopor* | class=medium | mid=37.0µm | size_src=yaml | sc={echinaat}
  - `phalaris_arundinacea` | *Phalaris arundinacea* | unranked | ap=monopor* | class=medium | mid=37.6µm | size_src=yaml
- Closest pair evidence `nymphaea_alba`–`phalaris_arundinacea` (d=1.081): `{'aperture': 'same monopor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.65, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same monopor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.081}`
- Provenance (sample): `nymphaea_alba`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `phalaris_arundinacea`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C177 (n=2, mean_d=1.572, max_d=1.572)

- Shared aperture: peripor*
- Size classes: medium; mid range: (37.4, 37.7)
- Shared sculpture tokens: psilaat, scabraat
- Members:
  - `papaver_argemone` | *Papaver argemone* | unranked | ap=peripor* | class=medium | mid=37.7µm | size_src=beug | path_gate=33–44 | sc={clavaat,echinaat,gemmaat,microechinaat,microreticulaat}
  - `scirpus_sylvaticus` | *Scirpus sylvaticus* | unranked | ap=peripor* | class=medium | mid=37.4µm | size_src=yaml | sc={psilaat,scabraat}
- Closest pair evidence `papaver_argemone`–`scirpus_sylvaticus` (d=1.572): `{'aperture': 'same peripor*', 'size_source': 'beug:docs/keys/beug/beug33-periporatae-papaver-argemone.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.3, 'sculpture': {'jaccard_dist': 0.75, 'shared': ['psilaat', 'scabraat']}, 'beug_fam': 'same peripor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.572}`
- Provenance (sample): `papaver_argemone`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; data/pollen.yaml:beug_key_paths · `scirpus_sylvaticus`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; vanderham:docs/keys/vanderham/vanderham-pollentabel.json

### C178 (n=2, mean_d=1.693, max_d=1.693)

- Shared aperture: tricol*
- Size classes: small; mid range: (18.0, 21.2)
- Shared sculpture tokens: psilaat, reticulaat
- Members:
  - `philadelphus_coronarius` | *Philadelphus coronarius* | unranked | ap=tricol* | class=small | mid=18.0µm | size_src=yaml | sc={psilaat,reticulaat}
  - `sambucus_nigra` | *Sambucus nigra* | unranked | ap=tricol* | class=small | mid=21.2µm | size_src=beug | sc={psilaat,reticulaat}
- Closest pair evidence `philadelphus_coronarius`–`sambucus_nigra` (d=1.693): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug23-tricolporoidatae-ret-sambucus-nigra.json', 'size_class': 'same small', 'size_mid_gap_um': 3.2, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat', 'reticulaat']}, 'beug_fam': 'same tricolpor', 'shape': {'jaccard_dist': 1.0, 'shared': []}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 1.693}`
- Provenance (sample): `philadelphus_coronarius`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `sambucus_nigra`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C179 (n=2, mean_d=1.213, max_d=1.213)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (48.3, 49.5)
- Shared sculpture tokens: —
- Members:
  - `prunella_vulgaris` | *Prunella vulgaris* | unranked | ap=stephanocol* | class=large | mid=48.3µm | size_src=yaml
  - `salvia_glutinosa` | *Salvia glutinosa* | unranked | ap=stephanocol* | class=large | mid=49.5µm | size_src=yaml
- Closest pair evidence `prunella_vulgaris`–`salvia_glutinosa` (d=1.213): `{'aperture': 'same stephanocol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 1.2, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.213}`
- Provenance (sample): `prunella_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `salvia_glutinosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug

### C180 (n=2, mean_d=1.333, max_d=1.333)

- Shared aperture: stephanocolpor*
- Size classes: medium; mid range: (33.0, 34.7)
- Shared sculpture tokens: —
- Members:
  - `pulmonaria_montana` | *Pulmonaria montana* | unranked | ap=stephanocolpor* | class=medium | mid=34.7µm | size_src=yaml
  - `symphytum_officinale` | *Symphytum officinale* | unranked | ap=stephanocolpor* | class=medium | mid=33.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `pulmonaria_montana`–`symphytum_officinale` (d=1.333): `{'aperture': 'same stephanocolpor*', 'size_source': 'yaml vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 1.7, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.333}`
- Provenance (sample): `pulmonaria_montana`: data/pollen.yaml:size; data/pollen.yaml:pollen_class_beug · `symphytum_officinale`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C181 (n=2, mean_d=0.670, max_d=0.670)

- Shared aperture: tricol*
- Size classes: medium; mid range: (37.5, 37.5)
- Shared sculpture tokens: scabraat, verrucaat
- Members:
  - `pulsatilla_vulgaris` | *Pulsatilla vulgaris* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=yaml | sc={scabraat,verrucaat}
  - `teucrium_chamaedrys` | *Teucrium chamaedrys* | unranked | ap=tricol* | class=medium | mid=37.5µm | size_src=beug | path_gate=0–45 | sc={scabraat,verrucaat}
- Closest pair evidence `pulsatilla_vulgaris`–`teucrium_chamaedrys` (d=0.670): `{'aperture': 'same tricol*', 'size_source': 'yaml vs beug:docs/keys/beug/beug13-tricolpatae-ps-teucrium.json', 'size_class': 'same medium', 'size_mid_gap_um': 0.05, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['scabraat', 'verrucaat']}, 'beug_fam': 'same tricol', 'shape': {'jaccard_dist': 0.667, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 5, 'distance': 0.6703}`
- Provenance (sample): `pulsatilla_vulgaris`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `teucrium_chamaedrys`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C182 (n=2, mean_d=1.429, max_d=1.429)

- Shared aperture: stephanocol*
- Size classes: large; mid range: (41.3, 43.4)
- Shared sculpture tokens: —
- Members:
  - `salvia_officinalis` | *Salvia officinalis* | unranked | ap=stephanocol* | class=large | mid=43.4µm | size_src=beug
  - `salvia_pratensis` | *Salvia pratensis* | unranked | ap=stephanocol* | class=large | mid=41.3µm | size_src=beug | sc={microreticulaat,psilaat,reticulaat,rugulaat,scabraat}
- Closest pair evidence `salvia_officinalis`–`salvia_pratensis` (d=1.429): `{'aperture': 'same stephanocol*', 'size_source': 'beug:docs/keys/beug/beug24-stephanocolpatae-salvia-pratensis.json vs beug:docs/keys/beug/beug24-stephanocolpatae-salvia-pratensis.json', 'size_class': 'same large', 'size_mid_gap_um': 2.1, 'sculpture': 'missing_one_or_both', 'beug_fam': 'same stephanocol', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 3, 'distance': 1.429}`
- Provenance (sample): `salvia_officinalis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug; beug:docs/keys/beug/beug24-stephanocolpatae-salvia-pratensis.json · `salvia_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C183 (n=2, mean_d=1.625, max_d=1.625)

- Shared aperture: tricol*
- Size classes: large; mid range: (80.0, 80.0)
- Shared sculpture tokens: —
- Members:
  - `succisa_pratensis` | *Succisa pratensis* | unranked | ap=tricol* | class=large | mid=80.0µm | size_src=yaml | sc={echinaat,striaat}
  - `vinca_typ` | *Vinca typ* | unranked | ap=tricol* | class=large | mid=80.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `succisa_pratensis`–`vinca_typ` (d=1.625): `{'aperture': 'same tricol*', 'size_source': 'yaml vs yaml', 'size_class': 'same large', 'size_mid_gap_um': 0.0, 'sculpture': {'jaccard_dist': 1.0, 'shared': []}, 'shape': {'jaccard_dist': 0.0, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 1.625}`
- Provenance (sample): `succisa_pratensis`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `vinca_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C184 (n=2, mean_d=1.597, max_d=1.597)

- Shared aperture: peripor*
- Size classes: small; mid range: (18.5, 21.3)
- Shared sculpture tokens: —
- **Human review (species↔*_typ):** thalictrum_lucidum ↔ thalictrum_typ
- Members:
  - `thalictrum_lucidum` | *Thalictrum lucidum* | unranked | ap=peripor* | class=small | mid=21.3µm | size_src=yaml
  - `thalictrum_typ` | *Thalictrum typ* | unranked | ap=peripor* | class=small | mid=18.5µm | size_src=yaml | sc={reticulaat,scabraat,verrucaat}
- Closest pair evidence `thalictrum_lucidum`–`thalictrum_typ` (d=1.597): `{'aperture': 'same peripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 2.8, 'sculpture': 'missing_one_or_both', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 2, 'distance': 1.597}`
- Provenance (sample): `thalictrum_lucidum`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:pollen_class_beug · `thalictrum_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

### C185 (n=2, mean_d=0.985, max_d=0.985)

- Shared aperture: tricol*
- Size classes: medium; mid range: (38.4, 38.6)
- Shared sculpture tokens: reticulaat
- **Low specificity:** shared sculpture is a single coarse token (`reticulaat`); morph-bin group, not confirmed lookalike.
- Members:
  - `tilia_platyphyllos` | *Tilia Platyphyllos* | unranked | ap=tricol* | class=medium | mid=38.4µm | size_src=beug | sc={reticulaat}
  - `vicia_villosa` | *Vicia villosa* | unranked | ap=tricol* | class=medium | mid=38.6µm | size_src=yaml | sc={reticulaat}
- Closest pair evidence `tilia_platyphyllos`–`vicia_villosa` (d=0.985): `{'aperture': 'same tricol*', 'size_source': 'beug:docs/keys/beug/beug22-tricolporatae-ret-tilia.json vs yaml', 'size_class': 'same medium', 'size_mid_gap_um': 0.25, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['reticulaat']}, 'coarse_sculpt_penalty': 'reticulaat', 'beug_fam': 'same tricolpor', 'shape': 'missing_one_or_both', 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.985}`
- Provenance (sample): `tilia_platyphyllos`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug · `vicia_villosa`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:pollen_class_beug

### C186 (n=2, mean_d=0.645, max_d=0.645)

- Shared aperture: tripor*
- Size classes: small; mid range: (15.5, 16.0)
- Shared sculpture tokens: psilaat
- **Low specificity:** shared sculpture is a single coarse token (`psilaat`); morph-bin group, not confirmed lookalike.
- **Human review (species↔*_typ):** urtica_dioica ↔ urtica_typ
- Members:
  - `urtica_dioica` | *Urtica dioica* | unranked | ap=tripor* | class=small | mid=15.5µm | size_src=yaml | sc={psilaat}
  - `urtica_typ` | *Urtica typ* | unranked | ap=tripor* | class=small | mid=16.0µm | size_src=yaml | sc={psilaat}
- Closest pair evidence `urtica_dioica`–`urtica_typ` (d=0.645): `{'aperture': 'same tripor*', 'size_source': 'yaml vs yaml', 'size_class': 'same small', 'size_mid_gap_um': 0.5, 'sculpture': {'jaccard_dist': 0.0, 'shared': ['psilaat']}, 'shape': {'jaccard_dist': 0.5, 'shared': ['rond']}, 'ornamentation': 'missing_one_or_both', 'dims_used': 4, 'distance': 0.645}`
- Provenance (sample): `urtica_dioica`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape · `urtica_typ`: data/pollen.yaml:size; data/pollen.yaml:aperture; data/pollen.yaml:sculpture; data/pollen.yaml:shape

## 6. already_decided tags (summary)

- Decided pairs co-clustered at tight cut: 0
- Decided pairs co-clustered at loose cut: 0
- Per-cluster tags listed above; sources not modified.

## 7. Human review flags

- Clusters with species↔`*_typ` co-membership (loose cut): **9**
  - `carduus_defloratus`, `carduus_typ`, `centaurea_jacea`, `inula_helenium`, `tragopogon_typ`: carduus_defloratus ↔ carduus_typ
  - `brassica_napus`, `brassica_oleracea`, `bunias_orientalis`, `crambe_maritima`, `crambe_typ`, `euodia_hupehensis`, `hesperis_matronalis`, `iberis_amara`, `odontites_vernus`, `salix_cinerea`, `salix_pentandra`: crambe_maritima ↔ crambe_typ
  - `borreria_typ`, `borreria_verticilata`, `chenopodium_bonus_henricus`, `daphne_mezereum`: borreria_verticilata ↔ borreria_typ
  - `carduus_crispus`, `serratula_tinctoria`, `serratula_typ`: serratula_tinctoria ↔ serratula_typ
  - `euphorbia_typ`, `rhododendron_ponticum`, `rhododendron_typ`: rhododendron_ponticum ↔ rhododendron_typ
  - `galanthus_nivalis`, `muscari_botryoides`, `muscari_typ`: muscari_botryoides ↔ muscari_typ
  - `artemisia_typ`, `artemisia_vulgaris`: artemisia_vulgaris ↔ artemisia_typ
  - `thalictrum_lucidum`, `thalictrum_typ`: thalictrum_lucidum ↔ thalictrum_typ
  - `urtica_dioica`, `urtica_typ`: urtica_dioica ↔ urtica_typ

- Borderline: YAML size-masked taxa rely on dichotomous key sizes when present.
- Sparse taxa (appendix) were not forced into clusters.

## 8. Limits / risks

- Missing fields inflate distance; empty never treated as a match.
- Kerkvliet section morph is analytic; not used as dichotomous size when conflict-masked.
- Dichotomous key sizes (Beug species lines / path gates) drive separation when YAML conflicts.
- No synonym / fuzzy Latin merge; no key-topology similarity signal.
- Tokenization is heuristic; coarse `reticulaat`-only groups remain low-specificity.
- Linkage: Complete-linkage cut on pairwise morph distance; species-matched key outcome sizes for mid; path-gates hard-separate when non-overlapping.
- This report does not confirm or promote lookalikes.

## Appendix A. Sparse / singleton taxa

Taxa with fewer than 2 usable feature dimensions (not forced into clusters).

- `acer_cappadocicum` | *Acer cappadocicum* | unranked | ap=tricol* · features=1
- `anemone_apennina` | *Anemone apennina* | unranked | class=medium | mid=24.9µm | size_src=yaml · features=1
- `anemone_ranunculoides` | *Anemone ranunculoides* | unranked | class=medium | mid=28.2µm | size_src=yaml · features=1
- `anemone_sylvestris` | *Anemone sylvestris* | unranked | class=small | mid=17.9µm | size_src=yaml · features=1
- `anthyllis_barba_jovis` | *Anthyllis barba-jovis* | unranked | class=medium | mid=30.1µm | size_src=yaml · features=1
- `asperula_odorata` | *Asperula odorata* | unranked | class=small | mid=20.0µm | size_src=yaml | sc={scabraat} · features=3
- `catalpa_ovata` | *Catalpa ovata* | unranked | class=large | mid=73.0µm | size_src=yaml | sc={reticulaat} · features=2
- `ceratocapnos_claviculata_corydalis_claviculata` | *Ceratocapnos claviculata* | unranked | ap=pericol* · features=1
- `chaerophyllum_bulbosum` | *Chaerophyllum bulbosum* | unranked | class=medium | mid=25.1µm | size_src=yaml · features=1
- `chenopodium_album` | *Chenopodium album* | unranked | class=medium | mid=28.0µm | size_src=yaml | sc={reticulaat,scabraat} · features=2
- `citrus_typ` | *Citrus typ* | unranked | class=medium | mid=33.2µm | size_src=yaml | sc={reticulaat} · features=3
- `corydalis_solida` | *Corydalis solida* | unranked | ap=pericol* · features=1
- `corylus_avelana` | *Corylus avelana* | unranked | class=medium | mid=26.0µm | size_src=yaml | sc={scabraat} · features=3
- `crepis_capillaris` | *Crepis capillaris* | unranked | ap=fenestr* · features=1
- `crepis_paludosa` | *Crepis paludosa* | unranked | ap=fenestr* · features=1
- `crocus_typ` | *Crocus typ* | unranked | class=very-large | mid=90.0µm | size_src=yaml | sc={reticulaat,scabraat} · features=2
- `cynoglossum_typ` | *Cynoglossum typ* | rank=66 | class=very-small | mid=11.0µm | size_src=yaml | sc={psilaat} · features=2
- `dactylorhiza_maculata` | *Dactylorhiza maculata* | unranked | class=large | mid=55.3µm | size_src=yaml | sc={reticulaat} · features=2
- `ephedra_helvetica` | *Ephedra helvetica* | unranked | class=medium | mid=38.0µm | size_src=yaml | sc={psilaat} · features=2
- `epipactis_palustris` | *Epipactis palustris* | unranked | ap=tetrade* · features=1
- `erica_vagans` | *Erica vagans* | unranked | class=medium | mid=33.1µm | size_src=yaml · features=1
- `fallopia_baldschuanica` | *Fallopia baldschuanica* | unranked | sc={reticulaat} · features=1
- `hieracium_austriacum` | *Hieracium austriacum* | unranked | ap=fenestr* · features=1
- `hypericum_polyphyllum` | *Hypericum polyphyllum* | unranked | sc={psilaat} · features=1
- `juncus_jacquinii` | *Juncus jacquinii* | unranked | ap=inapert* · features=1
- `juniperus_commu` | *Juniperus commu* | unranked | class=medium | mid=26.0µm | size_src=yaml | sc={scabraat} · features=3
- `kalmia_angustifolia` | *Kalmia angustifolia* | unranked | class=medium | mid=29.5µm | size_src=yaml · features=1
- `lactuca_tatarica` | *Lactuca tatarica* | unranked | ap=fenestr* · features=1
- `lappula_deflexa` | *Lappula deflexa* | unranked | ap=heterocol* · features=1
- `lithospermum_officinale` | *Lithospermum officinale* | unranked | class=very-small | mid=11.7µm | size_src=yaml | sc={psilaat} · features=3
- `luzula_sylvatica` | *Luzula sylvatica* | unranked | ap=inapert* · features=1
- `lychnis_coronaria` | *Lychnis coronaria* | unranked | ap=peripor* · features=1
- `lythrum_virgatum` | *Lythrum virgatum* | unranked | ap=heterocol* · features=1
- `mentha_arvensis` | *Mentha arvensis* | unranked | ap=stephanocol* · features=1
- `mentha_longifolia` | *Mentha longifolia* | unranked | ap=stephanocol* · features=1
- `mimulus_guttatus` | *Mimulus guttatus* | unranked | class=medium | mid=40.0µm | size_src=yaml | sc={reticulaat,scabraat} · features=2
- `minuartia_biflora` | *Minuartia biflora* | unranked | ap=peripor* · features=1
- `persicaria_hydropiper` | *Persicaria hydropiper* | unranked | ap=peripor* · features=1
- `persicaria_lapathifolia` | *Persicaria lapathifolia* | unranked | ap=peripor* · features=1
- `picea_omorika` | *Picea omorika* | unranked | sc={reticulaat,rugulaat} · features=2
- `platanus_hispanica` | *Platanus hispanica* | unranked | sc={reticulaat} · features=1
- `polygonatum_multiflorum` | *Polygonatum multiflorum* | unranked | ap=monocol* · features=1
- `polygonum_persicaria` | *Polygonum persicaria* | rank=41 | ap=peripor* · features=1
- `populus_typ` | *Populus typ* | rank=35 | class=medium | mid=27.0µm | size_src=yaml | sc={reticulaat,scabraat} · features=2
- `primula_elatior` | *Primula elatior* | unranked | ap=stephanocol* · features=1
- `prunella_grandiflora` | *Prunella grandiflora* | unranked | ap=stephanocol* · features=1
- `prunus_padus` | *Prunus padus* | unranked | ap=tricol* | size_src=masked_no_key_size | yaml_size_MASKED | sculpt_MASKED · features=2
- `pseudofumaria_alba_corydalis_alba` | *Pseudofumaria alba* | unranked | ap=pericol* · features=1
- `pseudofumaria_lutea_corydalis_lutea` | *Pseudofumaria lutea* | unranked | ap=syncol* · features=1
- `sagina_nodosa` | *Sagina nodosa* | unranked | ap=peripor* · features=1
- `sagina_subulata` | *Sagina subulata* | unranked | ap=peripor* · features=1
- `salvia_typ` | *Salvia typ* | unranked | class=medium | mid=35.0µm | size_src=yaml | sc={grof,reticulaat} · features=2
- `sonchus_asper` | *Sonchus asper* | unranked | ap=fenestr* · features=1
- `sophora_japonica` | *Sophora japonica* | unranked | class=small | mid=16.5µm | size_src=yaml | sc={reticulaat} · features=2
- `spiraea_typ` | *Spiraea typ* | rank=31 | class=small | mid=14.0µm | size_src=yaml | sc={psilaat} · features=2
- `spirea_x_vanhouttei` | *Spirea x vanhouttei* | unranked | class=small | mid=17.0µm | size_src=yaml · features=2
- `stellaria_media` | *Stellaria media* | unranked | ap=peripor* · features=1
- `thuja_typ` | *Thuja typ* | unranked | class=medium | mid=30.0µm | size_src=yaml | sc={reticulaat,scabraat} · features=2
- `vincetoxicum_hirundinaria` | *Vincetoxicum hirundinaria* | unranked | class=very-large | mid=150.0µm | size_src=yaml | sc={psilaat,scabraat} · features=2
- `xanthoceras_sorbifolium` | *Sapindaceae (fam.)* | unranked | class=small | mid=23.0µm | size_src=yaml | sc={psilaat,reticulaat} · features=2

## Appendix B. Clusterable singletons at tight cut

Clusterable taxa not in any tight multi-member cluster: **490**.
Of which learning-priority: **17**
- `rubus_typ` | *Rubus typ* | rank=3 | ap=tricol* | class=small | mid=25.0µm | size_src=yaml | sc={psilaat,striaat}
- `rhamnus` | *Rhamnus* | rank=7 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
- `robinia` | *Robinia* | rank=9 | ap=tricol* | class=medium | mid=32.5µm | size_src=yaml | sc={scabraat}
- `anthriscus_typ` | *Anthriscus typ* | rank=12 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={verrucaat}
- `echium` | *Echium* | rank=14 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={reticulaat}
- `ranunculus_typ` | *Ranunculus typ* | rank=16 | ap=tricol* | class=medium | mid=34.5µm | size_src=yaml | sc={reticulaat,verrucaat}
- `lotus` | *Lotus* | rank=20 | ap=tricol* | class=small | mid=20.0µm | size_src=yaml | sc={psilaat}
- `myosotis_typ` | *Myosotis typ* | rank=22 | ap=stephanocol* | class=very-small | mid=7.0µm | size_src=yaml | sc={psilaat}
- `phacelia_typ` | *Phacelia typ* | rank=23 | ap=stephanocol* | class=small | mid=22.0µm | size_src=yaml | sc={psilaat}
- `castanea_sativa` | *Castanea sativa* | rank=39 | ap=tricol* | class=very-small | mid=13.0µm | size_src=yaml | sc={psilaat,rugulaat,scabraat}
- `polygonum_aviculare` | *Polygonum aviculare* | rank=40 | ap=tricol* | class=medium | mid=32.6µm | size_src=beug | sc={psilaat,scabraat}
- `amorpha_fruticosa` | *Amorpha fruticosa* | rank=42 | ap=tricol* | class=small | mid=20.9µm | size_src=yaml | sc={reticulaat,verrucaat}
- `trifolium_pratense` | *Trifolium pratense* | rank=45 | ap=tricol* | class=large | mid=45.3µm | size_src=beug | path_gate=42–50 | yaml_size_MASKED | sc={grof,reticulaat}
- `silene_flos_cuculi` | *Silene flos-cuculi* | rank=49 | ap=peripor* | class=medium | mid=34.8µm | size_src=yaml | sc={baculaat,reticulaat,verrucaat}
- `calluna_vulgaris` | *Calluna vulgaris* | rank=64 | ap=tricol* | class=medium | mid=39.4µm | size_src=beug | sc={echinaat,grof,psilaat,scabraat,verrucaat}
- `centaurea_jacea` | *Centaurea jacea* | rank=75 | ap=tricol* | class=medium | mid=42.9µm | size_src=beug | path_gate=25–40 | sc={echinaat,scabraat}
- `impatiens_parviflora` | *Impatiens parviflora* | rank=76 | ap=stephanocol* | class=medium | mid=38.9µm | size_src=yaml | sc={grof,reticulaat}

