# Scripts (`scripts/`)

Overzicht van alle Python-scripts. Voer ze uit vanuit de **repository-root** met geactiveerde venv:

```bash
source .venv/bin/activate
python scripts/<script>.py …
```

Laatste controle: 2026-06-28.

---

## Dagelijks / na YAML-wijziging

**build_docs_data.py**: Regenereert `docs/data/pollen.json` en alle manifesten. Startpunt na elke `data/pollen.yaml`-wijziging.

```bash
python scripts/build_docs_data.py
```

**export_pollen_json.py**: Alleen `pollen.json` exporteren (subset van `build_docs_data.py`).

```bash
python scripts/export_pollen_json.py
```

**validate_pollen_site.py**: Controleert YAML-paden, optioneel layout, atlas-links en `mkdocs build`.

```bash
python scripts/validate_pollen_site.py --rebuild-data --images --links
python scripts/validate_pollen_site.py --mkdocs-build
```

| Vlag | Betekenis |
| --- | --- |
| `--rebuild-data` | Eerst `build_docs_data.py` |
| `--images` | Alias voor `--enforce-asset-layout` (canonieke `by-taxon/`-paden) |
| `--links` | Atlas-URL's in `pollen.json` voor binomiale taxa |
| `--mkdocs-build` | `mkdocs build` na geslaagde checks |

---

## Taxonpagina's en sleutelpaden

**extract_key_paths.py**: Traceert `pollen_key` door Beug-, van der Ham- en Kerkvliet-JSON; rendert `Determinatiesleutels`-Markdown. Zie `.cursor/skills/trace-key-paths/SKILL.md`.

```bash
python scripts/extract_key_paths.py <pollen_key> --status
python scripts/extract_key_paths.py <pollen_key> --page-section
```

| Vlag | Betekenis |
| --- | --- |
| `--status` | Aantallen paden per sleutel (stderr) |
| `--page-section` | Wrap in `## Determinatiesleutels` |

**render_taxon_pages_from_sot.py**: Genereert NL-taxpagina's voor alle `pollen_gallery`-keys in `nederlandse-honing-pollen/_index.md`.

```bash
python scripts/render_taxon_pages_from_sot.py
```

**update_monofloral_pages.py**: Vernieuwt kenmerkentabellen op monoflorale honingpagina's vanuit YAML.

```bash
python scripts/update_monofloral_pages.py
```

**sync_nl_index_links.py**: Voegt standaard macro-samenvattingen toe onder `####`-koppen in `nederlandse-honing-pollen/_index.md`.

```bash
python scripts/sync_nl_index_links.py
```

**fix_nl_index_orphan_links.py**: Vervangt externe `pollenx`-links in de NL-index door lokale `.md`-pagina's (maakt ontbrekende pagina's aan).

```bash
python scripts/fix_nl_index_orphan_links.py
```

---

## Sleutel-JSON (alleen bij expliciete sleuteltaak)

**build_vanderham_pollentabel_scans_json.py**: Bouwt `docs/keys/vanderham/vanderham-pollentabel.json` uit het transcript.

```bash
python scripts/build_vanderham_pollentabel_scans_json.py
```

**build_kerkvliet_determinatietabel_json.py**: Bouwt `docs/keys/kerkvliet/kerkvliet-determinatietabel.json` uit het transcript.

```bash
python scripts/build_kerkvliet_determinatietabel_json.py
```

**inject_pollen_keys_into_key_json.py**: Zet `pollen_key` op endpoints/rijen waar de slug uit YAML past.

```bash
python scripts/inject_pollen_keys_into_key_json.py --dry-run
python scripts/inject_pollen_keys_into_key_json.py
```

**slim_pollen_key_endpoints.py**: Verwijdert gedupliceerde taxonpayloads uit sleutels wanneer YAML de slug al dekt.

```bash
python scripts/slim_pollen_key_endpoints.py \
  docs/keys/vanderham/vanderham-pollentabel.json \
  docs/keys/kerkvliet/kerkvliet-determinatietabel.json
```

**audit_key_synonyms.py**: Rapporteert tegenstrijdige endpoint-`id.name`-varianten in sleutel-JSON.

```bash
python scripts/audit_key_synonyms.py
```

---

## YAML: samenvoegen, placeholders, schema

**merge_pollen.py**: Voegt bronnen (Kerkvliet, monofloraal/NL-md, sleutels) samen in `data/pollen.yaml`.

```bash
python scripts/merge_pollen.py --report _build/merge_pollen_report.txt
```

**sync_placeholder_taxa_from_keys.py**: Voegt placeholder-taxa toe voor slugs uit sleutels die nog niet in YAML staan.

```bash
python scripts/sync_placeholder_taxa_from_keys.py --dry-run
python scripts/sync_placeholder_taxa_from_keys.py
```

**apply_merge_into_markers.py**: Past `merge_into` / `merge_note` in YAML toe en werkt docs-verwijzingen bij.

```bash
python scripts/apply_merge_into_markers.py
```

**normalize_pollen_yaml_schema.py**: Normaliseert veldvolgorde en top-level keys in `pollen.yaml` (geen nieuwe feiten).

```bash
python scripts/normalize_pollen_yaml_schema.py --dry-run
python scripts/normalize_pollen_yaml_schema.py
```

---

## Afbeeldingen en assets

**audit_pollen_assets.py**: Read-only inventaris: disk vs YAML vs slug-resolutie.

```bash
python scripts/audit_pollen_assets.py
python scripts/audit_pollen_assets.py --out _build/pollen_asset_audit.json
```

**bootstrap_by_taxon_task.py**: Maakt `by-taxon-task/`-mappen voor taxa zonder foto.

```bash
python scripts/bootstrap_by_taxon_task.py --dry-run   # geen vlag = dry-run
python scripts/bootstrap_by_taxon_task.py --apply
```

**sync_yaml_confident_images.py**: Voegt zeker gemapte bestanden toe aan YAML `images:`.

```bash
python scripts/sync_yaml_confident_images.py --dry-run
python scripts/sync_yaml_confident_images.py --include-by-taxon
```

**normalize_by_taxon_numeric_images.py**: Hernoemt naar `slug_N.png` onder `by-taxon/`.

```bash
python scripts/normalize_by_taxon_numeric_images.py --dry-run
python scripts/normalize_by_taxon_numeric_images.py --apply
```

**migrate_pollen_images_by_taxon.py**: Verplaatst opgeloste bitmaps naar `by-taxon/<pollen_key>/`.

```bash
python scripts/migrate_pollen_images_by_taxon.py --dry-run
python scripts/migrate_pollen_images_by_taxon.py --apply
```

**rename_kerkvliet_screenshot_imports.py**: Hernoemt `Schermafbeelding*.png` naar `slug_N.png`.

```bash
python scripts/rename_kerkvliet_screenshot_imports.py --dry-run
python scripts/rename_kerkvliet_screenshot_imports.py --only-folder borago_officinalis
```

**rename_lm_view_codes_to_digits.py**: Zet LM-view-suffixen (`_ed`, `_eo`, …) om naar `_1`, `_2`, …

```bash
python scripts/rename_lm_view_codes_to_digits.py --dry-run
python scripts/rename_lm_view_codes_to_digits.py --apply
```

**lowercase_asset_image_files.py**: Lowercase voor asset-basenames en padverwijzingen in de repo.

```bash
python scripts/lowercase_asset_image_files.py --dry-run
python scripts/lowercase_asset_image_files.py --apply
```

**rewrite_pollenwiki_taxon_refs.py**: Vervangt legacy `pollenwiki/`-paden door eerste YAML by-taxon-image.

```bash
python scripts/rewrite_pollenwiki_taxon_refs.py --dry-run   # geen vlag = dry-run
python scripts/rewrite_pollenwiki_taxon_refs.py --apply
```

---

## Bibliotheken (niet direct aanroepen)

**pollen_asset_lib.py**: Gedeelde helpers voor image-paden en slug-resolutie; geïmporteerd door andere scripts.

**pollen_display.py**: Weergavebreedte (px) en atlas-URL-logica; gebruikt door `export_pollen_json.py` en `main.py`.

**build_manifests.py**: Wordt alleen via `build_docs_data.py` aangeroepen; bouwt `docs/assets/manifests/*.json`.

---

## Snelle keuze

| Doel | Commando |
| --- | --- |
| Site-data vernieuwen | `python scripts/build_docs_data.py` |
| Alles valideren | `python scripts/validate_pollen_site.py --rebuild-data --images --links` |
| Sleutelpaden op taxonpagina | `python scripts/extract_key_paths.py <slug> --page-section` |
| Image-gat inventariseren | `python scripts/audit_pollen_assets.py` |
| Ontbrekende foto-mappen | `python scripts/bootstrap_by_taxon_task.py --apply` |
| Sleutel-endpoints koppelen | `python scripts/inject_pollen_keys_into_key_json.py` |
