---
name: trace-key-paths
description: >-
  Traces a pollen_key through Beug, van der Ham, and Kerkvliet key JSON and
  renders Determinatiesleutels blocks for Dutch taxon pages. Use when filling
  sleutel sections, tracing key paths, extract_key_paths, or @trace-key-paths.
---

# Trace key paths (Beug / van der Ham / Kerkvliet)

## When to use

- Fill or refresh `## Determinatiesleutels` on `docs/pollen/species/<pollen_key>.md`
- User asks to trace a species through identification keys
- After adding `pollen_key` to key JSON endpoints (`inject_pollen_keys_into_key_json.py`)

Pair with **`.cursor/skills/pollen-pagina/SKILL.md`** for full page layout; this skill covers only the three key subsections.

## Engine (do not reimplement)

```bash
source .venv/bin/activate
python scripts/extract_key_paths.py <pollen_key> --status
python scripts/extract_key_paths.py <pollen_key> --page-section
```

- **`--status`**: counts paths per system on stderr (`beug`, `vanderham`, `kerkvliet`)
- **`--page-section`**: wraps output in `## Determinatiesleutels`

Script: `scripts/extract_key_paths.py` (read-only on `docs/keys/`).

## Workflow

1. **Resolve `pollen_key`** from `data/pollen.yaml` (ASCII slug, e.g. `fagopyrum_esculentum`).
2. **Run** `--status` then `--page-section`; inspect stderr.
3. **Merge into the taxon page**:
   - Replace the block from `## Determinatiesleutels` through the line before `## Online databases`.
   - Keep subsections the script emits: `### Beug`, `### Vanderham`, `### Kerkvliet`.
   - Output uses `<details><summary>…</summary>` and `pid-key-choice--on/off` spans (same as `calluna_vulgaris.md`).
4. **Gaps** (see below): add manual bullets only when JSON has no match; cite source in chat, not invented paths.
5. **Do not edit** `docs/keys/*.json` unless the user explicitly requests a keys change.

## What each system returns

| System | JSON source | Match rule |
| :--- | :--- | :--- |
| **Beug** | `docs/keys/beug/beug*.json` | DFS to choice/outcome with matching `pollen_key`; chains base key → subkey when applicable |
| **Vanderham** | `docs/keys/vanderham/*.json` | Same step graph; summary fixed to `Pollentabel (van der Ham)` |
| **Kerkvliet** | `docs/keys/kerkvliet/kerkvliet-determinatietabel.json` | Flat `rows[]` where `pollen_key` matches; renders `- Sectie: …` |

## When JSON returns nothing

| System | Fallback (verified sources only) |
| :--- | :--- |
| **Beug** | `docs/monoflorale-honing-pollen/<honing>.md` `## Sleutels` / `### Beug`; or Beug book OCR in notes (read-only). Many taxa are not yet in `beug*.json`. |
| **Vanderham** | Run `inject_pollen_keys_into_key_json.py` if endpoint exists but lacks `pollen_key`; re-run extract. |
| **Kerkvliet** | No row: state that explicitly; add nearest `section` from a related taxon only if morphologically justified; optional `(k)` frequency from `data/pollen.yaml` `frequency_in_dutch_honey`. |

Mark manual Beug paths with endpoint reference (e.g. `22.28 Fagopyrum (tabel 76:7-10)`).

## Output shape (per subsection)

```markdown
### Vanderham
<details><summary>Pollentabel (van der Ham)</summary>

- Stap 1:
  - <span class="pid-key-choice pid-key-choice--on">…</span>
  - <span class="pid-key-choice pid-key-choice--off">…</span>
- Eindpunt: …

</details>
```

- Multiple Beug `<details>` blocks are normal (base key + subkey).
- Escape `<` in labels as `&lt;` (script does this).
- Never use `—`; use `-`.

## Verification

```bash
python scripts/extract_key_paths.py <pollen_key> --status
```

If the page was edited: `mkdocs build` only when `mkdocs.yml` or broad links changed.

## Out of scope

- Creating or fixing key JSON → **`interactive-pollen-key`**, **`beug-key`**, **`update-vanderham`**
- Full taxon page → **`pollen-pagina`**
- YAML / images → **`update-pollen-yaml`**

## Canonical examples

- Generated: `python scripts/extract_key_paths.py calluna_vulgaris`
- Page: `docs/pollen/species/calluna_vulgaris.md`
- Manual Beug fallback: `docs/monoflorale-honing-pollen/boekweithoning.md`
