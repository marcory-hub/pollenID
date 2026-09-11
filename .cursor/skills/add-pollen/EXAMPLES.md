# Examples: add-pollen intake

## New taxon (images pending)

### User

```
@add-pollen Callicarpa bodinieri
```

### Agent (before STOP)

1. Confirm `callicarpa_bodinieri` is absent from `data/pollen.yaml`.
2. Create `docs/assets/images/by-taxon/callicarpa_bodinieri/`.
3. Give the user:
   - Folder path
   - Pollen-Wiki: `https://pollen.tstebler.ch/MediaWiki/index.php?title=Callicarpa_bodinieri`
   - PalDat: `https://www.paldat.org/pub/Callicarpa_bodinieri`
4. **STOP** until images are dropped (or user says text-only).

### After images

1. Rename screenshots → `callicarpa_bodinieri_1.png` … (rename is not a Kerkvliet claim).
2. Default `kind` / `source`: `pollenwiki`. Use `paldat` only if from PalDat. Never `kerkvliet` or `pollenx`.
3. Ask only if PalDat vs wiki, or views, are unclear.
4. Fetch atlas pages + local docs/keys/notes/paste; draft YAML in chat with provenance.
5. **STOP** for confirm; then write YAML, append `species_page_slugs.txt`, run `add_taxon.py --render-pages` and validate.

Atlas field mapping for tstebler blocks: [`../update-pollen/EXAMPLES.md`](../update-pollen/EXAMPLES.md) and [`../update-pollen/REFERENCE.md`](../update-pollen/REFERENCE.md).

## Existing slug

If `callicarpa_bodinieri` already exists in YAML → do not create a second folder; redirect to `@update-pollen`.
