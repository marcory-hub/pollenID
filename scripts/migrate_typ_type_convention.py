#!/usr/bin/env python3
"""One-shot: typ (Latin) / type (Dutch) convention + kerkvliet genus-only renames.

Preserves pollen.yaml block formatting via split_blocks.
"""

from __future__ import annotations

import json
import re
import shutil
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data/pollen.yaml"
KERKVLIET = ROOT / "docs/keys/kerkvliet/kerkvliet-determinatietabel.json"
SPECIES = ROOT / "docs/pollen/species"
BY_TAXON = ROOT / "docs/assets/images/by-taxon"
TODO_LINKS = ROOT / "docs/assets/images/by-taxon/_todo/_links"

# genus/aggregate key -> new key (species merges and deletes handled separately)
GENUS_TO_TYP: dict[str, str] = {
    "cynoglossum": "cynoglossum_typ",
    "spiraea": "spiraea_typ",
    "myosotis": "myosotis_typ",
    "urtica": "urtica_typ",
    "phacelia": "phacelia_typ",
    "viola": "viola_typ",
    "filipendula": "filipendula_typ",
    "tamarix": "tamarix_typ",
    "humulus": "humulus_typ",
    "melampyrum": "melampyrum_typ",
    "lysimachia": "lysimachia_typ",
    "anemone": "anemone_typ",
    "pisum": "pisum_typ",
    "skimmia": "skimmia_typ",
    "weigelia_diervilla": "weigelia_diervilla_typ",
    "dipsacus": "dipsacus_typ",
    "rhododendron": "rhododendron_typ",
    "citrus_spp_rutaceae": "citrus_typ",
}

# empty or special dutch overrides for typ keys
DUTCH_OVERRIDE: dict[str, str] = {
    "hydrangea_typ": "hortensia type",
    "cynoglossum_typ": "hondstong type",
    "spiraea_typ": "spirea type",
    "brassica_typ": "kool type",
    "knautia_typ": "beemdkroon type",
    "taraxacum_typ": "paardenbloem type",
    "helianthus_typ": "zonnebloem type",
    "phacelia_typ": "phacelia type",
    "citrus_typ": "citrus type",
    "geranium_typ": "ooievaarsbek type",
    "xanthium_italicum": "stekelnoot",  # species; strip erroneous sp.
}

DELETE_KEYS = {
    "castanea",  # stub; castanea_sativa is canonical
    "spirea",  # misspelled stub
    "tilia_type_linde_species",  # merge into tilia_typ
    "dipsacus_pollenwiki",  # empty Dipsacus sp. stub
    "philadelphus",  # merge into philadelphus_coronarius
}

# old_key -> new_key for reference rewrites (includes deletes that redirect)
KEY_REWRITES: dict[str, str] = {
    **GENUS_TO_TYP,
    "tilia_type_linde_species": "tilia_typ",
    "dipsacus_pollenwiki": "dipsacus_typ",
    "philadelphus": "philadelphus_coronarius",
    "castanea": "castanea_sativa",
    "spirea": "spiraea_typ",
    "citrus_spp_rutaceae": "citrus_typ",
}


def split_blocks(text: str) -> OrderedDict[str, str]:
    ms = list(re.finditer(r"^([A-Za-z0-9_-]+):\s*\n", text, re.MULTILINE))
    out: OrderedDict[str, str] = OrderedDict()
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out[m.group(1)] = text[m.start() : end]
    return out


def join_blocks(blocks: OrderedDict[str, str]) -> str:
    return "".join(blocks.values())


def set_name_fields(blob: str, *, latin: str | None = None, dutch: str | None = None) -> str:
    if latin is not None:
        if re.search(r"^    latin_name:", blob, re.M):
            blob = re.sub(r"^(    latin_name:).*", rf"\1 {latin}", blob, count=1, flags=re.M)
        else:
            blob = re.sub(r"^(  name:\n)", rf"\1    latin_name: {latin}\n", blob, count=1, flags=re.M)
    if dutch is not None:
        if re.search(r"^    dutch_name:", blob, re.M):
            blob = re.sub(r"^(    dutch_name:).*", rf"\1 {dutch}", blob, count=1, flags=re.M)
        else:
            blob = re.sub(
                r"^(    latin_name:.*\n)",
                rf"\1    dutch_name: {dutch}\n",
                blob,
                count=1,
                flags=re.M,
            )
    return blob


def get_field(blob: str, field: str) -> str | None:
    m = re.search(rf"^    {re.escape(field)}:\s*(.*)$", blob, re.M)
    if not m:
        return None
    val = m.group(1).strip()
    if val in ("", "~", "null", "None"):
        return ""
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    return val


def ensure_dutch_type_suffix(dutch: str) -> str:
    d = dutch.strip()
    if not d:
        return d
    # normalize soorten / sp. forms first
    d = re.sub(r"-soorten$", "", d, flags=re.I)
    d = re.sub(r"\s+soorten$", "", d, flags=re.I)
    d = re.sub(r"\s+spp?\.?$", "", d, flags=re.I)
    d = d.strip()
    if d.lower().endswith(" type"):
        return d
    return f"{d} type"


def rename_blob_key(blob: str, old: str, new: str) -> str:
    if not blob.startswith(f"{old}:"):
        raise ValueError(f"blob does not start with {old}:")
    return f"{new}:" + blob[len(old) + 1 :]


def _quote_yaml_str(s: str) -> str:
    if "'" in s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return "'" + s + "'"


def append_pollen_note(blob: str, fragment: str) -> str:
    m = re.search(r"^(    pollen-note:\s*)(.*)$", blob, re.M)
    if not m:
        if "  pollen_features:" in blob and "pollen-note:" not in blob:
            quoted = _quote_yaml_str(fragment)
            return re.sub(
                r"(  pollen_features:\n(?:    .*\n)*)",
                rf"\1    pollen-note: {quoted}\n",
                blob,
                count=1,
            )
        return blob
    prefix, rest = m.group(1), m.group(2).strip()
    if fragment in rest:
        return blob
    if (rest.startswith("'") and rest.endswith("'")) or (rest.startswith('"') and rest.endswith('"')):
        inner = rest[1:-1]
    else:
        inner = rest
    if fragment in inner:
        return blob
    new_inner = f"{inner}; {fragment}" if inner else fragment
    return blob[: m.start()] + prefix + _quote_yaml_str(new_inner) + blob[m.end() :]


def ensure_sorted_insert(blocks: OrderedDict[str, str], key: str, blob: str) -> None:
    """Insert blob under key, keeping approximate alpha order by key."""
    if key in blocks:
        blocks[key] = blob
        return
    keys = list(blocks.keys())
    insert_at = len(keys)
    for i, k in enumerate(keys):
        if k > key:
            insert_at = i
            break
    # rebuild
    new = OrderedDict()
    for i, k in enumerate(keys):
        if i == insert_at:
            new[key] = blob
        new[k] = blocks[k]
    if insert_at == len(keys):
        new[key] = blob
    blocks.clear()
    blocks.update(new)


def rewrite_text_keys(text: str, rewrites: dict[str, str]) -> str:
    # longest keys first
    for old, new in sorted(rewrites.items(), key=lambda kv: -len(kv[0])):
        if old == new:
            continue
        text = text.replace(f'gallery("{old}")', f'gallery("{new}")')
        text = text.replace(f"gallery('{old}')", f"gallery('{new}')")
        text = text.replace(f"pollen_key\": \"{old}\"", f"pollen_key\": \"{new}\"")
        text = text.replace(f"pollen_key: {old}", f"pollen_key: {new}")
        text = text.replace(f"/by-taxon/{old}/", f"/by-taxon/{new}/")
        text = text.replace(f"species/{old}.md", f"species/{new}.md")
        text = text.replace(f"species/{old})", f"species/{new})")
        text = text.replace(f"`{old}`", f"`{new}`")
        # yaml top-level / heading keys in embedded dumps
        text = re.sub(rf"(?m)^{re.escape(old)}:", f"{new}:", text)
        text = re.sub(rf"(?m)^## {re.escape(old)}$", f"## {new}", text)
        text = re.sub(rf"(?m)^### {re.escape(old)}$", f"### {new}", text)
    return text


def main() -> None:
    yaml_text = YAML_PATH.read_text(encoding="utf-8")
    blocks = split_blocks(yaml_text)

    # --- philadelphus merge into coronarius ---
    if "philadelphus" in blocks and "philadelphus_coronarius" in blocks:
        blocks["philadelphus_coronarius"] = append_pollen_note(
            blocks["philadelphus_coronarius"],
            "Kerkvliet: 14-16 µm; zeer fijn reticulaat",
        )

    # --- genus -> typ renames ---
    for old, new in GENUS_TO_TYP.items():
        if old not in blocks:
            print(f"WARN missing yaml key {old}")
            continue
        blob = rename_blob_key(blocks.pop(old), old, new)
        old_latin = (get_field(blob, "latin_name") or "").strip()
        if old == "citrus_spp_rutaceae":
            latin = "Citrus typ"
        elif old == "weigelia_diervilla":
            latin = "Weigelia/Diervilla typ"
        elif old_latin.endswith(" typ"):
            latin = old_latin
        elif old_latin.endswith(" type"):
            latin = old_latin[: -len(" type")] + " typ"
        elif re.search(r"\bspp?\b", old_latin, re.I):
            latin = f"{old_latin.split()[0]} typ"
        elif old_latin:
            # genus-only or dual-genus token
            latin = f"{old_latin} typ"
        else:
            latin = f"{new[:-4].replace('_', ' ').title()} typ"
        if new in DUTCH_OVERRIDE:
            dutch = DUTCH_OVERRIDE[new]
        else:
            dutch_src = get_field(blob, "dutch_name") or ""
            dutch = ensure_dutch_type_suffix(dutch_src) if dutch_src else ""
        blob = set_name_fields(blob, latin=latin, dutch=dutch if dutch else None)
        ensure_sorted_insert(blocks, new, blob)
        print(f"renamed {old} -> {new} latin={latin!r} dutch={dutch!r}")

    # --- delete stubs ---
    for k in DELETE_KEYS:
        if k in blocks:
            del blocks[k]
            print(f"deleted {k}")

    # --- append type to all *_typ dutch; fix latin type->typ; special overrides ---
    for key, blob in list(blocks.items()):
        latin = get_field(blob, "latin_name") or ""
        dutch = get_field(blob, "dutch_name") or ""
        is_typ = key.endswith("_typ") or latin.endswith(" typ") or latin.endswith(" type")
        if key == "xanthium_italicum":
            blocks[key] = set_name_fields(blob, dutch=DUTCH_OVERRIDE["xanthium_italicum"])
            continue
        if not is_typ:
            continue
        new_latin = latin
        if latin.endswith(" type"):
            new_latin = latin[: -len(" type")] + " typ"
        new_dutch = DUTCH_OVERRIDE.get(key)
        if new_dutch is None:
            if dutch:
                new_dutch = ensure_dutch_type_suffix(dutch)
            else:
                new_dutch = None  # leave empty unless override
        kwargs = {}
        if new_latin != latin:
            kwargs["latin"] = new_latin
        if new_dutch is not None and new_dutch != dutch:
            kwargs["dutch"] = new_dutch
        if kwargs:
            blocks[key] = set_name_fields(blob, **kwargs)
            print(f"typ fields {key}: {kwargs}")

    YAML_PATH.write_text(join_blocks(blocks), encoding="utf-8")
    print("wrote", YAML_PATH)

    # --- kerkvliet JSON ---
    kj = json.loads(KERKVLIET.read_text(encoding="utf-8"))

    def walk(o):
        if isinstance(o, list):
            for i in o:
                walk(i)
        elif isinstance(o, dict):
            if "pollen_key" in o:
                pk = o["pollen_key"]
                if pk in KEY_REWRITES:
                    o["pollen_key"] = KEY_REWRITES[pk]
                    pk = o["pollen_key"]
                # sync latin/dutch from yaml block if present
                if pk in blocks:
                    lat = get_field(blocks[pk], "latin_name")
                    dut = get_field(blocks[pk], "dutch_name")
                    if lat:
                        o["latin"] = lat
                    if dut:
                        o["dutch"] = dut
                    elif o.get("dutch") in ("-", ""):
                        pass
                # genus-only latin still in row?
                lat = (o.get("latin") or "").strip()
                if lat and not lat.endswith(" typ") and " " not in lat and not lat.endswith("aceae"):
                    # family skip already; single token
                    if pk.endswith("_typ"):
                        o["latin"] = f"{lat} typ"
                dut = (o.get("dutch") or "").strip()
                if pk.endswith("_typ") and dut and dut not in ("-",) and not dut.lower().endswith(" type"):
                    if re.search(r"\bspp?\.?\b|soorten", dut, re.I):
                        o["dutch"] = ensure_dutch_type_suffix(dut)
                    else:
                        o["dutch"] = ensure_dutch_type_suffix(dut)
                if dut and re.search(r"\bspp?\.?\b", dut):
                    o["dutch"] = ensure_dutch_type_suffix(dut) if pk.endswith("_typ") else re.sub(
                        r"\s+spp?\.?$", "", dut
                    ).strip()
            for v in o.values():
                walk(v)

    walk(kj)
    KERKVLIET.write_text(json.dumps(kj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", KERKVLIET)

    # --- species pages rename ---
    for old, new in KEY_REWRITES.items():
        src = SPECIES / f"{old}.md"
        dst = SPECIES / f"{new}.md"
        if not src.exists():
            continue
        if old in DELETE_KEYS and new != old:
            # merge: if dst exists, delete src (content regenerable); else rename
            if dst.exists():
                text = src.read_text(encoding="utf-8")
                # keep manual identificatienotities from genus page? prefer dst for SoT pages
                src.unlink()
                print(f"removed species page {old}.md (target {new}.md exists)")
            else:
                text = rewrite_text_keys(src.read_text(encoding="utf-8"), {old: new})
                dst.write_text(text, encoding="utf-8")
                src.unlink()
                print(f"renamed species {old}.md -> {new}.md")
        else:
            text = rewrite_text_keys(src.read_text(encoding="utf-8"), {old: new})
            if dst.exists() and dst != src:
                src.unlink()
                print(f"removed duplicate species {old}.md")
            else:
                dst.write_text(text, encoding="utf-8")
                if src != dst and src.exists():
                    src.unlink()
                print(f"renamed species {old}.md -> {new}.md")

    # rewrite remaining species pages that mention old keys
    for path in SPECIES.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        new_text = rewrite_text_keys(text, KEY_REWRITES)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated refs in {path.name}")

    # --- by-taxon folders ---
    for old, new in KEY_REWRITES.items():
        src = BY_TAXON / old
        dst = BY_TAXON / new
        if src.is_dir() and not dst.exists():
            src.rename(dst)
            print(f"renamed folder {old} -> {new}")
        elif src.is_dir() and dst.exists() and src != dst:
            for f in src.iterdir():
                target = dst / f.name
                if not target.exists():
                    shutil.move(str(f), str(target))
            shutil.rmtree(src)
            print(f"merged folder {old} into {new}")

    # --- todo link files ---
    for path in [TODO_LINKS / "_kerkvliet.md", TODO_LINKS / "_pollen-atlas-links.md"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text = rewrite_text_keys(text, KEY_REWRITES)
        # also rename ## headings for genus keys
        for old, new in KEY_REWRITES.items():
            new_text = re.sub(rf"(?m)^## {re.escape(old)}$", f"## {new}", new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path}")

    # --- broader docs/scripts reference sweep (text files) ---
    sweep_roots = [
        ROOT / "docs",
        ROOT / "scripts",
        ROOT / ".cursor",
    ]
    skip_parts = {"docs/data", "node_modules", ".venv", "by-taxon-task"}
    for root in sweep_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".mdc", ".py", ".json", ".yml", ".yaml", ".js", ".txt"}:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if any(s in rel for s in skip_parts):
                continue
            if path.resolve() in {YAML_PATH.resolve(), KERKVLIET.resolve()}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            new_text = rewrite_text_keys(text, KEY_REWRITES)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                print(f"swept {rel}")


if __name__ == "__main__":
    main()
