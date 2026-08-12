# CONTEXT.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**pollen_key**:
ASCII slug for a taxon or type aggregate in `data/pollen.yaml`.
_Avoid_: species id (as a separate concept)

**Pollentype**:
Morphology bucket for reporting and grouping (see root `CONTEXT.md`).
_Avoid_: pollen type (as a separate product concept)
```

## Rules

- **Be opinionated.** Pick one term; list loose synonyms under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. Define what it IS, not what it does.
- **Only domain terms.** No general programming concepts. Ask: unique to this context?
- **Group under subheadings** when clusters emerge; otherwise a flat list is fine.

## Single vs multi-context

**Single (this repo):** One root `CONTEXT.md`.

**Multiple:** Root `CONTEXT-MAP.md` lists contexts and relationships. Infer which context applies; ask if unclear. Create root `CONTEXT.md` lazily on first approved term if neither file exists.
