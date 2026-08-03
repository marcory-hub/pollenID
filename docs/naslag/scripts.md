# Scripts

Voer scripts uit vanuit de repository-root met geactiveerde venv:

```bash
source .venv/bin/activate
python scripts/<script>.py …
```

## MkDocs

| Script | Doel |
| :--- | :--- |
| `scripts/mkdocs_macros.py` | MkDocs-macros: `pollen`, `pollen_vis_suffix`, `pollen_img`, `gallery` (via `module_name` in `mkdocs.yml`) |
| `scripts/pollen_display.py` | Gedeelde helpers: display-breedte (px), atlas-URL's, zichtbaarheidslabels (gebruikt door export en macros) |

## Validatie en data-build

| Script | Doel |
| :--- | :--- |
| `scripts/validate_pollen_site.py` | Controleert YAML-beeldpaden; optioneel rebuild, asset-layout, atlas-links, `mkdocs build` |
| `scripts/build_docs_data.py` | Genereert `docs/data/pollen.json` en manifesten |
| `scripts/export_pollen_json.py` | Exporteert alleen `docs/data/pollen.json` (subset van `build_docs_data.py`); inclusief `controlled` kenmerkcodes |
| `scripts/build_manifests.py` | Bouwt asset-manifesten onder `docs/assets/manifests/` (lookalike-paren inclusief `note`) |
| `scripts/audit_pollen_assets.py` | Read-only inventaris: beelden, YAML-dekking, pollen_key-resolutie |

```bash
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
./.venv/bin/python scripts/build_docs_data.py
```

| Vlag (`validate_pollen_site.py`) | Betekenis |
| :--- | :--- |
| `--rebuild-data` | Eerst `build_docs_data.py` |
| `--images` | Alias voor `--enforce-asset-layout` (canonieke `by-taxon/`-paden) |
| `--links` | Atlas-URL's in `pollen.json` voor binomiale taxa |
| `--mkdocs-build` | `mkdocs build` na geslaagde checks |

## Pollen YAML

| Script | Doel |
| :--- | :--- |
| `scripts/fill_pollen_yaml_from_beug.py` | Vult lege velden in `data/pollen.yaml` vanuit Beug-key JSON en `notes/pollenID/Beug.txt`. `pollen_class_beug` = Aperturtyp-label (bijv. `Tricolpat-psilat`), geen hoofdstuknummer. |
| `scripts/normalize_pollen_yaml_schema.py` | Normaliseert schema-layout |
| `scripts/prefill_pollen_atlas_links.py` | Vult lege atlas-links |
| `scripts/sync_yaml_confident_images.py` | Voegt ontbrekende image-paden toe |
| `scripts/fill_typ_images.py` | Vult `images` voor `*_typ`-taxa vanuit genus-matchende by-taxon-mappen (max 8, seed 42) |
| `scripts/sync_pollen_placeholders.py` | Synchroniseert placeholder-taxa |
| `scripts/sync_placeholder_taxa_from_keys.py` | Placeholder-taxa vanuit sleutel-JSON |
| `scripts/lookalike_candidates.py` | Kandidaten-shortlist (grootte ±10 µm, apertuur-bucket, Beug multi-class) → `data/lookalike_review.yaml` |
| `scripts/promote_lookalikes.py` | Promoveert `status: confirmed` uit review naar `lookalikes` in `data/pollen.yaml` |

```bash
./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --dry-run
./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py
./.venv/bin/python scripts/fill_typ_images.py --dry-run
./.venv/bin/python scripts/sync_yaml_confident_images.py
./.venv/bin/python scripts/lookalike_candidates.py --confirm-published
./.venv/bin/python scripts/promote_lookalikes.py --dry-run
./.venv/bin/python scripts/promote_lookalikes.py
```

`pollen_class_beug` labels: Polyad, Tetrad, Dyad, Vesiculat, Inaperturat, Monoporat, Monocolpat, Syncolpat, Dicolpat, Dicolporat, Tricolpat-psilat, Tricolporat-psilat, Tricol-clavat, Tricol-echinat, Tricolpat-striat, Tricolporat-striat, Tricolpat-reticulat, Tricolporat-reticulat, Stephanocolpat, Stephanocolporat, Pericolpat, Pericolporat, Heterocolpat, Fenestrat, Diporat, Triporat, Stephanoporat, Periporat.

## Taxon toevoegen / pagina's

| Script | Doel |
| :--- | :--- |
| `scripts/add_taxon.py` | Orchestrator: rename → sync YAML-beelden → optioneel inject/slim → validate `--rebuild-data` |
| `scripts/rename_kerkvliet_screenshot_imports.py` | Hernoemt Schermafbeelding*.png naar `<slug>_N.png` |
| `scripts/render_taxon_pages_from_sot.py` | Genereert species-pagina's vanuit `data/pollen.yaml` |
| `scripts/bootstrap_by_taxon_task.py` | Maakt `by-taxon-task/`-mappen voor taxa zonder bruikbare bitmaps |
| `scripts/update_monofloral_pages.py` | Vernieuwt kenmerkentabellen op monoflorale honingpagina's vanuit YAML |

## Keys / Kerkvliet

| Script | Doel |
| :--- | :--- |
| `scripts/inject_pollen_keys_into_key_json.py` | Zet `pollen_key` op Kerkvliet-rijen (match op Latijn ↔ YAML-slug) |
| `scripts/slim_pollen_key_endpoints.py` | Strip inline taxonvelden uit key-JSON wanneer slug in YAML staat |
| `scripts/extract_key_paths.py` | Determinatiesleutels-sectie per taxon voor species-pagina's |
| `scripts/merge_pollen.py` | Legacy: merge Kerkvliet-inlinevelden naar pollen-YAML |
| `scripts/audit_key_synonyms.py` | Audit synoniemen in sleutel-JSON |
| `scripts/build_vanderham_pollentabel_scans_json.py` | Bouwt van der Ham pollentabel-JSON uit transcript |

```bash
./.venv/bin/python scripts/extract_key_paths.py <pollen_key> --page-section
```

Zie [Site-architectuur](site-architectuur.md).
