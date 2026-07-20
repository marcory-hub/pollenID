# Scripts

## Pollen YAML

| Script | Doel |
| :--- | :--- |
| `scripts/fill_pollen_yaml_from_beug.py` | Vult lege velden in `data/pollen.yaml` vanuit Beug-key JSON en `notes/pollenID/Beug.txt`. `pollen_class_beug` = Aperturtyp-label (bijv. `Tricolpat-psilat`), geen hoofdstuknummer. |
| `scripts/normalize_pollen_yaml_schema.py` | Normaliseert schema-layout |
| `scripts/prefill_pollen_atlas_links.py` | Vult lege atlas-links |
| `scripts/sync_yaml_confident_images.py` | Voegt ontbrekende image-paden toe |
| `scripts/build_docs_data.py` | Genereert `docs/data/pollen.json` e.d. |
| `scripts/migrate_typ_type_convention.py` | Eenmalige migratie: genus-only / `sp.`-labels naar `*_typ` (`Genus typ` / `{nl} type`); zie projectregels |

```bash
./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --dry-run
./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py
./.venv/bin/python scripts/fill_pollen_yaml_from_beug.py --report-missing-from-keys
./.venv/bin/python scripts/build_docs_data.py
```

`pollen_class_beug` labels: Polyad, Tetrad, Dyad, Vesiculat, Inaperturat, Monoporat, Monocolpat, Syncolpat, Dicolpat, Dicolporat, Tricolpat-psilat, Tricolporat-psilat, Tricol-clavat, Tricol-echinat, Tricolpat-striat, Tricolporat-striat, Tricolpat-reticulat, Tricolporat-reticulat, Stephanocolpat, Stephanocolporat, Pericolpat, Pericolporat, Heterocolpat, Fenestrat, Diporat, Triporat, Stephanoporat, Periporat.