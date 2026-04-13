---
name: pollen-pagina
description: >-
  Builds a Dutch taxon page under docs/nederlandse-honing-pollen/ like calluna_vulgaris.md:
  image gallery, internal and external links, sleutelpaden from Beug / van der Ham / Kerkvliet JSON,
  nav entry, and _index link. Use when the user asks for a pollen species page, taxon landing page,
  or the same layout as Calluna / sleutels en paden.
---

# Pollen taxon page (Nederlandse honing)

## When to use

- New or expanded species (or type) page in **`docs/nederlandse-honing-pollen/`**, same structure as **`calluna_vulgaris.md`**.
- User wants gallery + PollenX / pollenwiki / Paldat + **Sleutels en paden** with **Verwacht pad** callouts.

## Policy (repo)

- **Language:** Dutch for all reader-facing prose in **`docs/`**; Latin taxon in italics in headings where appropriate. Agent chat stays English.
- **No writes to `notes/`.** Do not edit **`docs/keys/`** JSON unless the user explicitly requests a keys change; for these pages, **read** JSON to extract paths and table rows only.
- **`mkdocs.yml`:** Add a **`nav`** entry under **Nederlands** when the page is new (alphabetical slug key, path to the `.md` file). User must approve if they prefer to batch nav edits.
- **URLs:** Take PollenX / pollenwiki / Paldat targets from existing repo sources (e.g. **`kerkvliet-determinatietabel.json`** `latin` / neighbour rows, or **`nederlandse-honing-pollen/_index.md`** before it was replaced by an internal link). Do not invent URLs.
- **Typography:** Do not use the em dash `—`; use `-`. In HTML callouts, escape `<` as `&lt;`.

## Admonitions

This project’s **`mkdocs.yml`** does not enable Markdown `!!!` admonitions. Use **HTML** Material callouts so lists render correctly:

```html
<div class="admonition info">
<p class="admonition-title">Verwacht pad</p>
<ol>
<li><strong>Stap 1:</strong> …</li>
</ol>
</div>
```

Kerkvliet summary: same wrapper with **`<ul>`** and title e.g. `Tabelrij <em>…</em>`.

## Workflow (ordered)

1. **Source of truth for images and bullets**  
   Open **`docs/nederlandse-honing-pollen/_index.md`** for the taxon block: copy **`pid-scale-gallery`** paths and image **heights** (Nederlandse honing scale **2.5 px/µm** per project context). Add any extra images listed for that taxon in **`kerkvliet-determinatietabel.json`** (e.g. `persano_oddo/`), with heights consistent with those assets’ use elsewhere.

2. **Create the Markdown file**  
   Path: **`docs/nederlandse-honing-pollen/<slug>.md`**. Slug: match repo habit (**`calluna_vulgaris.md`** uses underscore; **`mkdocs.yml`** nav key may use hyphens).

3. **Page top**  
   - `# *Genus species* (Nederlandse naam)`  
   - One **`pid-scale-gallery`** / **`pid-scale-row pid-scale-row--snug`** / **`figure.pid-scale-item`** row (all figures for that taxon in one row unless the user asks to split).  
   - **`alt`:** short sensible text (no placeholder artefact alts).

4. **Links block**  
   - `Zie het overzicht [_index.md](_index.md)` and, if relevant, a monoflorale page under **`../monoflorale-honing-pollen/`**.  
   - Bullet list: **PollenX** (`https://pollenx.eu/species.php?species=Genus_species`), **pollenwiki**, **Paldat** from verified URLs only.

5. **`## Sleutels en paden`**  
   For each relevant key (user- or taxon-specific):
   - **`###`** short title + one line **`[Interactieve sleutel](../Identificatiesleutels/….md)`** (or Kerkvliet tabel page).  
   - Short intro (JSON filename, eindpunt name, familieniveau vs species).  
   - **Beug:** Trace **`docs/keys/beug/*.json`** from **`start`** following **`next`** and choice **`label`** until the taxon **`id.name`** endpoint or subgroup named in the key. If species lives in a **sub-key** (e.g. Ericaceae-Empetrum), document **two** blocks: main **`beug04-tetradeae.json`** path to subgroup + **`beug04-tetradeae-ericaceae-empetrum.json`** path to species. Step numbers in titles must match **`steps`** **ids** in JSON (non-sequential is normal).  
   - **Van der Ham:** Trace **`vanderham-pollentabel.json`**; if the endpoint is only **family**, state that explicitly.  
   - **Kerkvliet:** No dichotomous path; copy **dutch**, **vorm**, **grootte**, **oppervlak**, **opmerkingen** from the matching row into the **`<ul>`** callout.  
   - Closing line optional: Latin/links are authored in JSON and rendered by the site table.

6. **Overzicht entry**  
   If the taxon is listed on **`_index.md`** with an external-only heading, switch to **`[Genus species](<slug>.md) (naam)`** when the user wants the landing page (sibling-relative path).

7. **Navigation**  
   Insert under **`mkdocs.yml` → Nederlands** in **alphabetical** order:  
   `- <nav-key>: nederlandse-honing-pollen/<slug>.md`

8. **Verify**  
   Run **`mkdocs build`**. Confirm **`mkdocs.yml`** is consistent with the new page.

## Paired references

- **`scale-images`** skill: true-scale galleries on other page types.  
- **`interactive-pollen-key`**: JSON sleutel contract (not for editing keys unless requested).  
- **`project-context.mdc`** Keys + image scale defaults.

## Canonical example

**`docs/nederlandse-honing-pollen/calluna_vulgaris.md`** (gallery, externe links, vier sleutel-secties, HTML callouts).
