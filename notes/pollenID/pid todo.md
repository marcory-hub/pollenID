## Status vs prio list

|Status|Count|Meaning|
|---|---|---|
|Mature|42|Species page with gallery + YAML-backed content|
|Stub|30|`-typ`, family page, or `[to be verified]` aggregate|
|Partial|2|Good text, no gallery/SoT yet|
|Thin / missing|3|`spiraea.md`, `rhus.md` minimal; no NL page for boekweit|

Already mature (no action unless you want polish): 1, 3-10, 12-16, 20, 22-23, 25-28, 30, 33-35, 38-39, 45, 49, 53, 57, 59, 61-62, 64-66, 68-69, 71-72, 77.

Note: #7 Rhamnus is correctly covered by `frangula_alnus.md` (not `rhamnus.md`). #29 Ononis is mature as `onosis_spinoza.md`, but `mkdocs.yml` still links `ononis.md`.

---

## What to add (recommended order)

Work in batches of 3-5 taxa: species page → `build_docs_data.py` → fix `mkdocs.yml` nav → optionally turn the old `-typ` page into a short redirect/hub.

### Batch 1 - Top of prio, data already there (start here)

|Prio|Target|YAML slug|Images|Action|
|---|---|---|---|---|
|54|Fagopyrum (Boekweit)|`fagopyrum_esculentum`|10|New page `fagopyrum_esculentum.md`; add to `mkdocs.yml` nav|
|2|Prunus/Pirus|`prunus_avium` (+ `malus_domestica`, `prunus_spinosa`)|4-5 each|Replace `prunus-pirus-typ.md` with exemplar page(s) or hub linking to species|
|11|Acer platanoides|`acer_platanoides`|4|New `acer_platanoides.md`; retire mislabeled `acer-platanoides.md` (now describes _A. pseudoplatanus_)|
|55|Fragaria|`fragaria_vesca`|4|New `fragaria_vesca.md`; replace `fragaria.md` stub|
|31|Spiraea|`spiraea_japonica`|4|New `spiraea_japonica.md`; replace thin `spiraea.md`|

### Batch 2 - Partial pages (text exists, add structure)

|Prio|File|Action|
|---|---|---|
|52|`impatiens-glandulifera.md`|Add `impatiens_glandulifera` to YAML if missing, gallery + kenmerkentabel + SoT|
|42|`amorpha-fruticosa.md`|Same pattern; YAML entry `amorpha_fruticosa` exists|
|76|`impatiens-parviflora.md`|Full species page once YAML slug exists|

### Batch 3 - Stubs with YAML + images (upgrade template)

|Prio|Stub now|Species slug to build|
|---|---|---|
|19|`verbascum.md`|`verbascum_nigrum` (4 images)|
|29|`ononis.md`|Point nav to existing `onosis_spinoza.md`|
|18|`raphanus-typ.md`|`eruca_sativa` (already mature) - convert stub to hub|
|32|`allium-typ.md`|`allium_cepa` (mature) - hub only|
|28|`sinapis-typ.md`|`sinapis_arvensis` (mature) - hub only|

### Batch 4 - Stubs needing YAML and/or images first

|Prio|Issue|Next step|
|---|---|---|
|44 Crataegus|`crataegus_monogyna` in YAML, 0 images|Add microphotos or queue `by-taxon-task/`|
|46 Hedera|No `hedera_helix` in YAML|Add YAML + images, then page|
|47 Rhus|`rhus_chinensis` in YAML, 0 images|Images first|
|17 Parthenocissus|No YAML slug found|Add `parthenocissus_tricuspidata` (or correct sp.) to YAML|
|40-41 Polygonum|Stub only|Link to `rumex_obtusifolius` / add `persicaria` slug if in keys|

### Batch 5 - Family / type aggregates (lower urgency per species, high for teaching)

Keep as comparison hubs (links + short determination notes), not full species pages:

`rosaceae.md` (51), `brassicaceae.md` (68), `hydrangeaceae.md` (36), `buddlejaceae.md` (60), `violaceae.md` (30 - species `viola_tricolor` already mature), `eleagnaceae.md` (57 - `elaeagnus_angustifolia` mature).

For `-typ` pages without a mature species yet: 21 Lamium → `lamium_album`, 24 Genista → `genista_anglica`, 37 Achillea → `achillea_millefolium`, 50 Asparagus → check YAML (`asparagus_setaceus` exists; verify correct NL honey taxon).

---

## Per-page checklist (pollen-pagina skill)

For each new/upgrade page:

1. Confirm `pollen_key` in `data/pollen.yaml` (latin, dutch, size, aperture, `images:`).
2. Images under `docs/assets/images/by-taxon/<pollen_key>/` as `slug_1.png`, …
3. Create `docs/nederlandse-honing-pollen/<pollen_key>.md`:
    - `{{ pollen_gallery("pollen_key") }}`
    - `## Kenmerken` table with `pollen(...)` macros
    - `### SoT` YAML block
    - Kerkvliet / Beug / vanderham callouts where you have paths (see `calluna_vulgaris.md`)
4. `python scripts/build_docs_data.py`
5. Update `mkdocs.yml` nav entry (slug change = broken link risk)
6. Old stub: replace with 3-line hub linking to the species page(s)

---

## Suggested first session (2-3 hours)

1. `fagopyrum_esculentum.md` - highest gap (prio 54, 10 images, no NL page).
2. `acer_platanoides.md` - fix prio 11 naming mismatch.
3. Nav fix: `ononis` → `onosis_spinoza`; add fagopyrum + acer entries.
4. `fragaria_vesca.md` + `spiraea_japonica.md`.

That clears 5 prio items with minimal new microscopy work.