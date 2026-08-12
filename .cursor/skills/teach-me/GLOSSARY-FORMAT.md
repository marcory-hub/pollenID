# GLOSSARY.md format

Canonical language for this teaching workspace. Lessons and learning records use these terms.

## Structure

```md
# {Topic} Glossary

{One or two sentences: what domain this glossary covers.}

## Terms

**pollen_key**:
ASCII slug for a taxon or type aggregate in `data/pollen.yaml` (e.g. `calluna_vulgaris`, `cynoglossum_typ`).
_Avoid_: species id, folder name (when used as a separate concept)

**colpaat**:
Apertuurtype met spleetvormige colpi (Beug/Dutch site wording).
_Avoid_: colpate (in Dutch learner text unless quoting English source)
```

## Rules

- **Add a term only when the user understands it.** Record compressed knowledge, not a dictionary to learn from cold.
- **Be opinionated.** Pick one term; list loose synonyms under `_Avoid_`.
- **Definitions tight.** One or two sentences; what it IS, not full procedure.
- **Use glossary terms inside other definitions** once promoted.
- **Subheadings** when clusters emerge (e.g. `## Morphology`, `## Keys`).
- **Flag ambiguities.** "In this workspace, *type* means Beug pollentype unless noted as honey type."
- **Revise in place** when understanding deepens.

Do not duplicate `notes/` or YAML SoT tables; glossary is teaching vocabulary.
