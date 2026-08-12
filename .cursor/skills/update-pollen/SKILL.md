---
name: update-pollen
description: >-
  Full taxon pipeline: by-taxon images, data/pollen.yaml, species page
  (Kenmerken + Determinatiesleutels), optional Kerkvliet/beug_key_paths wiring,
  synonyms on rename, then validate so nothing is left broken. Use when images
  or taxon information are added or changed; update pollen, @update-pollen,
  add pollen, @add-pollen, add images information, @add-tstebler, pollenwiki
  text, update pollen.yaml, @trace-key-paths, @pollen-pagina, van der Ham
  by-taxon sync, @add-by-taxon-images, or @add-kerkvliet-images.
---

# Update pollen (whole codebase)

Run when atlas PNGs or taxon metadata arrive. Do not invent taxa, morphology, or paths. End every run with validation.

## Modes (same skill)

| Mode | When |
| :--- | :--- |
| Full / batch | Agent notes, renames, Kerkvliet, many slugs |
| Single + metadata | User morphology block + screenshots |
| Text only | Images already on disk; atlas text only |

YAML schema, atlas field map, page/sleutel details, helpers: [REFERENCE.md](REFERENCE.md). Example intake: [EXAMPLES.md](EXAMPLES.md).

## Preconditions

- PNGs under `docs/assets/images/by-taxon/<pollen_key>/` (move from `_todo/<slug>/` if needed).
- Folder = `pollen_key` (`genus_species` or `genus_typ`). Type aggregates: latin `Genus typ`, dutch `{vernacular} type`.
- New image rows: `kind` / `source` = `by_taxon` unless user names another corpus.
- Beug sizes in `size.*`; Kerkvliet sizes in `pollen-note` (`Kerkvliet: … µm`). No plant height in pollen `size`.

## Steps

1. **Images:** ensure numeric `slug_N.png` under `by-taxon/<pollen_key>/`.
2. **YAML:** patch user/atlas/agent fields only (minimal diff). Dutch vernacular when sure. Normalize if needed: `scripts/normalize_pollen_yaml_schema.py`.
3. **Page:** add `pollen_key` to `data/species_page_slugs.txt` if new; run orchestrator below (regenerates `docs/pollen/species/<pollen_key>.md`). Merge Determinatiesleutels section from `extract_key_paths` when needed.
4. **Determinatiesleutels:** `python scripts/extract_key_paths.py <pollen_key> --page-section`; replace that section. Manual bullets only from verified sources.
5. **Synonyms:** on rename/merge, update `docs/naslag/synoniemen-en-basioniemen.md`.
6. **Keys wiring (not authoring):** `--kerkvliet` if listed/asked; `sync_beug_key_paths`; if empty run `inject_pollen_keys_into_key_json.py` then re-sync. Do **not** edit `docs/keys/` unless user explicitly asks.
7. **Orchestrator + validate:**

```bash
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --render-pages
# optional: --kerkvliet   |   text-only: --skip-rename
./.venv/bin/python scripts/validate_pollen_site.py --rebuild-data --images --links
```

Do not also run `build_docs_data.py` in the same turn. For van der Ham taxa after new PNGs: `sync_yaml_confident_images.py --only-by-taxon` then validate.

8. **Queue hygiene:** remove finished `## <slug>` from `_todo/_links/` files; delete empty `_todo/<slug>/` only.

## Stop

- Validator missing images or slug mismatches: fix or ask before commit.
- Vague agent notes: skip or ask; ask before guessing typos.

## Out of scope

Author/reshape dichotomous key trees → **`@interactive-pollen-key`**.
