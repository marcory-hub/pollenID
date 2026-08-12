# ADR Format

ADRs live in `docs/adr/` as `0001-slug.md`, `0002-slug.md`, …

Create `docs/adr/` lazily on first approved ADR.

## Template

```md
# {Short title of the decision}

{1-3 sentences: context, decision, why.}
```

Optional (only when useful): Status frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`); Considered Options; Consequences.

## Numbering

Scan `docs/adr/` for highest `NNNN`; increment.

## When to offer an ADR

All three must hold: hard to reverse; surprising without context; real trade-off.

### Qualifies (pollenID examples)

- Agent guidance shape (rules vs skills; see `0001-rules-vs-skills.md`)
- SoT boundaries (`data/pollen.yaml` vs generated `docs/data/`)
- Key JSON contract choices that lock page + `pollentabel.js` behaviour
- Deliberate deviations a later editor would "fix"

Skip easy reversals, unsurprising defaults, and "we did the only obvious thing."
