---
name: add-pollen
description: >-
  End-to-end workflow to add or update a pollen taxon across the codebase:
  by-taxon images, data/pollen.yaml fields, species pages, optional key JSON
  wiring, synonyms naslag, and site validation. Use when the user says add
  pollen, @add-pollen, add by-taxon images, wire atlas screenshots, apply
  agent notes, @add-by-taxon-images, add kerkvliet images, or
  @add-kerkvliet-images.
---

# Add pollen (images + data + pages)

Run after atlas PNGs land in `docs/assets/images/by-taxon/<slug>/` (or a filled
`_todo/<slug>/` is moved there). Do not invent taxa, morphology, or paths.

Modes (same pipeline; thinner intake):

| Mode | Skill | When |
| :--- | :--- | :--- |
| Full / batch | **this skill** | Agent notes, renames, Kerkvliet, many slugs |
| Single + metadata | **add-images-information** | User morphology block + screenshots |
| Text only | **add-tstebler** | Images already on disk; atlas text only |

## Preconditions

- Screenshots under **`by-taxon/<slug>/`**, not only `_todo/`.
- Folder name = canonical **`pollen_key`** (ASCII `genus_species`, or `genus_typ`).
- Type aggregates: latin `Genus typ`, dutch `{vernacular} type` (see `project-context.mdc`).
- New YAML image rows: `kind` / `source` = `by_taxon` only.
- Agent notes in **both** `_todo/_links/_kerkvliet.md` and
  `_todo/_links/_pollen-atlas-links.md` when doing batch queue work.
- Beug sizes in `size.*`; Kerkvliet sizes in `pollen_features.pollen-note`
  (`Kerkvliet: … µm`).

## Steps (in order)

### 1. Images on disk

Move `_todo/<slug>/` with `*.png` into `by-taxon/<slug>/` (merge if present).

### 2. YAML (`data/pollen.yaml`)

Apply every `agent:` / `Agent:` note and user-supplied fields (and any confirmed
global rename). Follow **update-pollen-yaml**. Typical tasks: rename/replace key,
fill morphology/family/Dutch/size, merge stubs, remap per note. Do **not** put
plant height into pollen `size`.

### 3. Species page + synonyms + keys (manual)

- Species page: **pollen-pagina** (or `add_taxon.py --render-pages --slug <key>`).
- Synonyms: update `docs/naslag/synoniemen-en-basioniemen.md` on rename/merge.
- Keys: only if user asked or slug is in Kerkvliet; pass `--kerkvliet` to orchestrator.
  Do **not** edit `docs/keys/` otherwise.

### 4. Orchestrator (rename + sync + validate)

One command replaces separate rename / sync / `build_docs_data` / validate shells.
`--rebuild-data` already runs `build_docs_data.py`; do **not** call it separately.

```bash
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key>
# Kerkvliet wire + slim:
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --kerkvliet
# Also regenerate species page from SoT:
./.venv/bin/python scripts/add_taxon.py --slug <pollen_key> --render-pages
# Optional queue bootstrap after batch:
./.venv/bin/python scripts/add_taxon.py --bootstrap --skip-rename --skip-sync
```

### 5. Queue hygiene

Delete finished `## <slug>` from `_kerkvliet.md` / `_pollen-atlas-links.md`; remove
empty `_todo/<slug>/` only.

## Codebase touchpoints (rename / new taxon)

| Area | Path / action |
| :--- | :--- |
| SoT | `data/pollen.yaml` |
| Images | `docs/assets/images/by-taxon/<pollen_key>/` |
| Species page | `docs/pollen/species/<pollen_key>.md` |
| Generated | via `add_taxon.py` → `validate_pollen_site.py --rebuild-data` |
| Kerkvliet | `docs/keys/kerkvliet/kerkvliet-determinatietabel.json` (if listed) |
| Synonyms | `docs/naslag/synoniemen-en-basioniemen.md` |
| Queue | `_todo/_links/_kerkvliet.md`, `_pollen-atlas-links.md` |

## Stop conditions

- Missing image paths from validator: fix or restore before commit.
- Folder slug ≠ YAML / Kerkvliet key: apply rename note or ask first.
- Skip vague agent notes or ask; ask before guessing typos.

## Related

- `scripts/add_taxon.py`
- `.cursor/skills/add-images-information/SKILL.md`
- `.cursor/skills/add-tstebler/SKILL.md`
- `.cursor/skills/update-pollen-yaml/SKILL.md`
- `.cursor/skills/pollen-pagina/SKILL.md`
- `.cursor/skills/trace-key-paths/SKILL.md`
