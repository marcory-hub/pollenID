#!/usr/bin/env python3
"""Migrate browse folders to docs/pollen/{families,species} and update pollen.yaml.

One-shot migration for the families+species restructure:
  - split classification.family into family_latin / family_dutch
  - seed frequency_* and is_secondary_contributor from folder membership
  - move/merge markdown pages into docs/pollen/
  - drop beug-klassen, old browse folders, and niet-eu placeholder

Usage:
  .venv/bin/python scripts/migrate_pollen_docs_layout.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml
from ruamel.yaml import YAML

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "data" / "pollen.yaml"
NL_DIR = REPO / "docs" / "nederlandse-honing-pollen"
SEC_DIR = REPO / "docs" / "secundaire-inbreng"
EU_DIR = REPO / "docs" / "sporadische-eu-pollen"
NIET_EU_DIR = REPO / "docs" / "niet-eu-pollen"
SPECIES_DIR = REPO / "docs" / "pollen" / "species"
FAMILIES_DIR = REPO / "docs" / "pollen" / "families"

FREQ_ENUM = frozenset({"absent", "rare", "occasional", "frequent"})
FREQ_RANK = {"absent": 0, "rare": 1, "occasional": 2, "frequent": 3}

# Family-like stems that are family landing pages, not species/types.
FAMILY_STEM_EXTRAS = frozenset(
    {
        "crucifereae",
        "eleagnaceae",
        "elaeaanaceae",
        "coniferae",
        "papilionaceae",
        "solanaceae",
        "rosaceae",
        "poaceae",
        "lamiaceae",
        "dipsacaceae",
        "buddlejaceae",
        "hydrangeaceae",
        "violaceae",
        "brassicaceae",
        "amaranthaceae",
        "fagaceae",
        "papaveraceae",
        "pinaceae",
    }
)

SKIP_NAMES = frozenset(
    {
        "_index.md",
        "bestimmungshulp-pollenklassen.md",
        "bepalingshulp-pollenklassen.md",
    }
)

# Open follow-up defaults: >10% frequent, >2% occasional, else rare.
PCT_FREQUENT = 10.0
PCT_OCCASIONAL = 2.0


def _ruamel() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.default_flow_style = False
    y.width = 4096
    y.indent(mapping=2, sequence=4, offset=2)
    return y


def _filled(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str) and v.strip() in ("", "-", "null", "None"):
        return False
    return True


def _parse_family(raw: Any) -> Tuple[Optional[str], Optional[str]]:
    """Split mixed family string into (family_latin, family_dutch)."""
    if not _filled(raw) or not isinstance(raw, str):
        return None, None
    s = raw.strip()
    # Special messy cases
    if s.lower() == "duizendknoopfamilie":
        return "Polygonaceae", "duizendknoopfamilie"
    if "Liliaceae (pw)" in s or "Amaryllidaceae (wiki)" in s:
        m = re.search(r"\(([^()]*)\)\s*$", s)
        dutch = m.group(1).strip() if m else None
        return "Amaryllidaceae", dutch

    m = re.match(r"^([A-Za-z][A-Za-z-]*)\s*\(([^()]*)\)\s*$", s)
    if m:
        latin = m.group(1).strip()
        dutch = m.group(2).strip()
        # Title-case Latin family names consistently
        if latin and latin[0].islower():
            latin = latin[0].upper() + latin[1:]
        return latin, dutch

    # Latin only
    if re.match(r"^[A-Za-z][A-Za-z-]*aceae$", s, re.I):
        latin = s[0].upper() + s[1:]
        return latin, None

    # Dutch-only remnant
    if "familie" in s.lower() and "(" not in s:
        return None, s

    # Fallback: keep whole string as latin if it looks botanical
    if re.match(r"^[A-Za-z]", s):
        return s.split()[0], None
    return None, s


def _family_slug(latin: Optional[str]) -> Optional[str]:
    if not latin:
        return None
    slug = re.sub(r"[^a-z0-9]+", "_", latin.lower()).strip("_")
    return slug or None


def _is_family_stem(stem: str) -> bool:
    s = stem.lower().replace("_", "-")
    if s in FAMILY_STEM_EXTRAS or s.replace("-", "") in {
        x.replace("-", "") for x in FAMILY_STEM_EXTRAS
    }:
        return True
    # *aceae / *ideae family endings
    bare = s.replace("-", "_")
    return bool(re.search(r"(aceae|ideae)$", bare, re.I))


def _stem_candidates(stem: str) -> List[str]:
    """Generate possible pollen_key matches for a filename stem."""
    out: List[str] = []
    for cand in (
        stem,
        stem.replace("-", "_"),
        stem.replace("_", "-"),
        re.sub(r"[-_]+", "_", stem),
        re.sub(r"[-_]+", "-", stem),
    ):
        if cand and cand not in out:
            out.append(cand)
    return out


def _resolve_key(stem: str, yaml_keys: Set[str]) -> str:
    for cand in _stem_candidates(stem):
        if cand in yaml_keys:
            return cand
    # Prefer underscore form for new pages
    return re.sub(r"[-_]+", "_", stem).strip("_") or stem


def _max_freq(a: Optional[str], b: Optional[str]) -> Optional[str]:
    if not _filled(a):
        return b if _filled(b) else None
    if not _filled(b):
        return a
    return a if FREQ_RANK.get(str(a), -1) >= FREQ_RANK.get(str(b), -1) else b


def _freq_from_pct(pct: float) -> str:
    if pct > PCT_FREQUENT:
        return "frequent"
    if pct > PCT_OCCASIONAL:
        return "occasional"
    return "rare"


def _parse_index_honey_pcts(index_path: Path) -> Dict[str, float]:
    """Best-effort map of pollen_key-ish slug -> percent from NL _index.md."""
    if not index_path.is_file():
        return {}
    text = index_path.read_text(encoding="utf-8")
    out: Dict[str, float] = {}
    # Lines like: #### [Lotus corniculatus](...) ... or with "In honing: 16.3%"
    # Capture nearby pollen_gallery("key") or markdown links to local .md
    gallery_re = re.compile(r'pollen_gallery\("([a-z0-9_]+)"\)')
    local_link_re = re.compile(r"\]\(([a-z0-9_-]+)\.md\)", re.I)
    pct_re = re.compile(r"In honing:\s*([\d]+(?:\.\d+)?)\s*%", re.I)

    blocks = re.split(r"(?=^####\s)", text, flags=re.M)
    for block in blocks:
        pcts = [float(m.group(1)) for m in pct_re.finditer(block)]
        if not pcts:
            continue
        pct = max(pcts)
        keys = gallery_re.findall(block) + [
            re.sub(r"[-_]+", "_", m.group(1)) for m in local_link_re.finditer(block)
        ]
        for key in keys:
            k = re.sub(r"[-_]+", "_", key)
            out[k] = max(out.get(k, 0.0), pct)
    return out


def _secundaire_mentions(index_path: Path, yaml_keys: Set[str]) -> Set[str]:
    if not index_path.is_file():
        return set()
    text = index_path.read_text(encoding="utf-8")
    found: Set[str] = set()
    # "secundaire inbreng" near latin names or bold names
    for m in re.finditer(
        r"secundaire inbreng[^\n]{0,120}", text, flags=re.I
    ):
        chunk = m.group(0)
        for key in yaml_keys:
            latinish = key.replace("_", " ")
            if latinish.lower() in chunk.lower() or key in chunk:
                found.add(key)
        # Common explicit forms
        for name, key in (
            ("Corylus avellana", "corylus_avelana"),  # typo key in yaml
            ("Chenopodium album", "chenopodium_album"),
            ("Poaceae", "poaceae"),
        ):
            if name.lower() in chunk.lower() and key in yaml_keys:
                found.add(key)
    # Also scan whole file for "secundaire inbreng" on same line as gallery/key
    for line in text.splitlines():
        if "secundaire inbreng" not in line.lower():
            continue
        for m in re.finditer(r'pollen_gallery\("([a-z0-9_]+)"\)', line):
            found.add(m.group(1))
        for m in re.finditer(r"\*([A-Z][a-z]+ [a-z\-]+)\*", line):
            slug = re.sub(r"[^a-z0-9]+", "_", m.group(1).lower()).strip("_")
            if slug in yaml_keys:
                found.add(slug)
            # corylus typo key
            if slug == "corylus_avellana" and "corylus_avelana" in yaml_keys:
                found.add("corylus_avelana")
    return found


def _md_files(directory: Path) -> List[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.glob("*.md")
        if p.name not in SKIP_NAMES and p.is_file()
    )


def _file_richness(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def split_families(data: Dict[str, Any]) -> Dict[str, int]:
    stats = {"split": 0, "empty": 0, "dutch_only": 0}
    for _key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        clas = entry.get("classification")
        if not isinstance(clas, dict):
            clas = {}
            entry["classification"] = clas
        raw = clas.pop("family", None) if "family" in clas else None
        # Already split?
        if "family_latin" in clas or "family_dutch" in clas:
            if "family" in clas:
                del clas["family"]
            continue
        latin, dutch = _parse_family(raw)
        clas["family_latin"] = latin
        clas["family_dutch"] = dutch
        # Keep order/tribe/genus; reorder keys lightly by rewriting clas
        ordered = {
            "order": clas.get("order"),
            "family_latin": clas.get("family_latin"),
            "family_dutch": clas.get("family_dutch"),
            "tribe": clas.get("tribe"),
            "genus": clas.get("genus"),
        }
        # Preserve any extra keys
        for k, v in clas.items():
            if k not in ordered:
                ordered[k] = v
        entry["classification"] = ordered
        if latin or dutch:
            stats["split"] += 1
            if latin is None and dutch:
                stats["dutch_only"] += 1
        else:
            stats["empty"] += 1
    return stats


def seed_frequency_and_secondary(
    data: Dict[str, Any],
    nl_keys: Set[str],
    eu_keys: Set[str],
    sec_keys: Set[str],
    pct_map: Dict[str, float],
    sec_mentions: Set[str],
) -> Dict[str, int]:
    stats = {
        "dutch_set": 0,
        "eu_set": 0,
        "non_eu_set": 0,
        "secondary_set": 0,
        "nl_eu_bumped": 0,
    }
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue

        # Frequency from folder membership
        dutch = entry.get("frequency_in_dutch_honey")
        eu = entry.get("frequency_in_eu_honey")
        non_eu = entry.get("frequency_in_non_eu_honey")

        if key in nl_keys and not _filled(dutch):
            dutch = _freq_from_pct(pct_map[key]) if key in pct_map else "rare"
            entry["frequency_in_dutch_honey"] = dutch
            stats["dutch_set"] += 1
        elif key in pct_map and not _filled(dutch):
            # Percent mentioned even if not a file in NL root
            dutch = _freq_from_pct(pct_map[key])
            entry["frequency_in_dutch_honey"] = dutch
            stats["dutch_set"] += 1

        if key in eu_keys and not _filled(eu):
            entry["frequency_in_eu_honey"] = "rare"
            eu = "rare"
            stats["eu_set"] += 1

        # NL ⊂ EU
        dutch = entry.get("frequency_in_dutch_honey")
        eu = entry.get("frequency_in_eu_honey")
        if _filled(dutch) and str(dutch) in FREQ_ENUM and str(dutch) != "absent":
            if not _filled(eu) or str(eu) == "absent":
                entry["frequency_in_eu_honey"] = dutch
                stats["nl_eu_bumped"] += 1
            elif FREQ_RANK.get(str(eu), -1) < FREQ_RANK.get(str(dutch), -1):
                entry["frequency_in_eu_honey"] = dutch
                stats["nl_eu_bumped"] += 1

        # Secondary contributor: leave unset for unknown; seed secondary only
        if "is_secondary_contributor" not in entry:
            entry["is_secondary_contributor"] = None
        if key in sec_keys or key in sec_mentions:
            if not _filled(entry.get("is_secondary_contributor")):
                entry["is_secondary_contributor"] = "secondary"
                stats["secondary_set"] += 1

    return stats


def ensure_dirs() -> None:
    SPECIES_DIR.mkdir(parents=True, exist_ok=True)
    FAMILIES_DIR.mkdir(parents=True, exist_ok=True)


def write_index(path: Path, title: str, body: str) -> None:
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def migrate_pages(
    data: Dict[str, Any],
    dry_run: bool,
) -> Dict[str, Any]:
    yaml_keys = set(data.keys())
    report: Dict[str, Any] = {
        "species_moved": 0,
        "species_merged": 0,
        "families_from_pages": 0,
        "skipped_beug": 0,
        "collisions": [],
        "family_pages": [],
        "species_pages": [],
    }

    # Collect intended destinations: dest_key -> list of (src, kind)
    planned: Dict[str, List[Tuple[Path, str]]] = defaultdict(list)
    family_planned: Dict[str, List[Path]] = defaultdict(list)

    # NL root pages
    for src in _md_files(NL_DIR):
        stem = src.stem
        if _is_family_stem(stem):
            slug = _family_slug(stem.replace("-", "_").replace("_", " ").title().replace(" ", ""))
            # Prefer stem as family slug directly
            fslug = re.sub(r"[-_]+", "", stem.lower())
            # normalize to underscore latin style
            fslug = re.sub(r"[-_]+", "_", stem.lower())
            family_planned[fslug].append(src)
            continue
        key = _resolve_key(stem, yaml_keys)
        planned[key].append((src, "nl"))

    # Secundaire
    for src in _md_files(SEC_DIR):
        stem = src.stem
        if _is_family_stem(stem):
            fslug = re.sub(r"[-_]+", "_", stem.lower())
            family_planned[fslug].append(src)
            continue
        key = _resolve_key(stem, yaml_keys)
        planned[key].append((src, "sec"))

    # Sporadische EU
    for src in _md_files(EU_DIR):
        stem = src.stem
        if _is_family_stem(stem):
            fslug = re.sub(r"[-_]+", "_", stem.lower())
            family_planned[fslug].append(src)
            continue
        key = _resolve_key(stem, yaml_keys)
        planned[key].append((src, "eu"))

    ensure_dirs()

    # Move/merge species
    for key, sources in sorted(planned.items()):
        # Prefer richest source; if NL present prefer NL over stubs
        ranked = sorted(
            sources,
            key=lambda t: (
                0 if t[1] == "nl" else 1 if t[1] == "sec" else 2,
                0 if t[0].stem == key else 1,  # prefer exact pollen_key filename
                -_file_richness(t[0]),
            ),
        )
        winner_path, winner_kind = ranked[0]
        dest = SPECIES_DIR / f"{key}.md"
        if len(ranked) > 1:
            report["collisions"].append(
                {
                    "key": key,
                    "winner": str(winner_path.relative_to(REPO)),
                    "others": [str(p.relative_to(REPO)) for p, _ in ranked[1:]],
                }
            )
            report["species_merged"] += 1
        else:
            report["species_moved"] += 1

        text = winner_path.read_text(encoding="utf-8")
        # Fix asset-relative paths: from sibling folder ../../assets stays same depth
        # From docs/X/foo.md and docs/pollen/species/foo.md both need ../../assets
        # Depth is identical (2 levels under docs/), so leave as-is.
        if not dry_run:
            dest.write_text(text, encoding="utf-8")
        report["species_pages"].append(key)

    # Family pages from old family markdown
    for fslug, sources in sorted(family_planned.items()):
        ranked = sorted(sources, key=lambda p: -_file_richness(p))
        winner = ranked[0]
        dest = FAMILIES_DIR / f"{fslug}.md"
        text = winner.read_text(encoding="utf-8")
        if not dry_run:
            dest.write_text(text, encoding="utf-8")
        report["families_from_pages"] += 1
        report["family_pages"].append(fslug)

    # Count beug-klassen for report (deleted later)
    beug = NL_DIR / "beug-klassen"
    if beug.is_dir():
        report["skipped_beug"] = len(list(beug.rglob("*.md")))

    return report


def build_family_pages_from_yaml(
    data: Dict[str, Any],
    species_on_disk: Set[str],
    dry_run: bool,
) -> List[str]:
    """Ensure a family page exists for each family_latin; list common species."""
    by_family: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
    dutch_names: Dict[str, Optional[str]] = {}
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        clas = entry.get("classification") or {}
        latin = clas.get("family_latin") if isinstance(clas, dict) else None
        if not _filled(latin):
            continue
        slug = _family_slug(str(latin))
        if not slug:
            continue
        by_family[slug].append((key, entry))
        dutch_names.setdefault(slug, clas.get("family_dutch") if isinstance(clas, dict) else None)

    created: List[str] = []
    for slug, members in sorted(by_family.items()):
        dest = FAMILIES_DIR / f"{slug}.md"
        latin_title = str(members[0][1].get("classification", {}).get("family_latin") or slug)
        dutch = dutch_names.get(slug)
        title = f"*{latin_title}*"
        if _filled(dutch):
            title += f" ({dutch})"

        # Prefer species that have pages and non-empty dutch freq
        def sort_key(item: Tuple[str, Dict[str, Any]]) -> Tuple[int, int, str]:
            key, entry = item
            freq = entry.get("frequency_in_dutch_honey")
            rank = FREQ_RANK.get(str(freq), -1) if _filled(freq) else -1
            has_page = 1 if key in species_on_disk else 0
            return (-rank, -has_page, key)

        ranked = sorted(members, key=sort_key)
        common = [k for k, _ in ranked if k in species_on_disk][:12]
        if not common:
            common = [k for k, _ in ranked[:12]]

        lines = [
            f"# {title}",
            "",
            f"Familiepagina voor *{latin_title}*.",
            "",
            "## Meest voorkomend",
            "",
        ]
        for key in common:
            entry = data[key]
            latin_name = None
            dutch_name = None
            if isinstance(entry, dict):
                name = entry.get("name") or {}
                if isinstance(name, dict):
                    latin_name = name.get("latin_name")
                    dutch_name = name.get("dutch_name")
            label = f"*{latin_name}*" if _filled(latin_name) else key
            if _filled(dutch_name):
                label += f" ({dutch_name})"
            if key in species_on_disk:
                lines.append(f"- [{label}](../species/{key}.md)")
            else:
                lines.append(f"- {label}")

        body = "\n".join(lines) + "\n"
        if dest.exists() and not dry_run:
            # Keep existing unique prose; append species list if missing
            existing = dest.read_text(encoding="utf-8")
            if "## Meest voorkomend" not in existing:
                dest.write_text(existing.rstrip() + "\n\n" + "\n".join(lines[lines.index("## Meest voorkomend"):]) + "\n", encoding="utf-8")
        elif not dry_run:
            dest.write_text(body, encoding="utf-8")
            created.append(slug)
        else:
            created.append(slug)
    return created


def write_indexes(family_slugs: List[str], species_keys: List[str], dry_run: bool) -> None:
    fam_lines = ["# Pollenfamilies", "", "Overzicht van pollenfamilies.", ""]
    for slug in sorted(set(family_slugs)):
        fam_lines.append(f"- [{slug}]({slug}.md)")
    sp_lines = [
        "# Pollensoorten",
        "",
        "Canonieke soort- en typepagina's. Gebruik de familiegroepen of sitezoeken om te bladeren.",
        "",
        f"Aantal pagina's: {len(species_keys)}.",
        "",
    ]
    # Do not list all 700+ in the index body; keep short.
    if not dry_run:
        write_index(FAMILIES_DIR / "_index.md", "Pollenfamilies", "\n".join(fam_lines[2:]))
        # rewrite properly
        (FAMILIES_DIR / "_index.md").write_text("\n".join(fam_lines) + "\n", encoding="utf-8")
        (SPECIES_DIR / "_index.md").write_text("\n".join(sp_lines) + "\n", encoding="utf-8")


def cleanup_old_dirs(dry_run: bool) -> None:
    for path in (NL_DIR, SEC_DIR, EU_DIR, NIET_EU_DIR):
        if path.exists():
            if dry_run:
                print(f"dry-run: would remove {path.relative_to(REPO)}")
            else:
                shutil.rmtree(path)
                print(f"removed {path.relative_to(REPO)}")


def collect_folder_keys(yaml_keys: Set[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    nl: Set[str] = set()
    eu: Set[str] = set()
    sec: Set[str] = set()
    for src in _md_files(NL_DIR):
        if _is_family_stem(src.stem):
            continue
        nl.add(_resolve_key(src.stem, yaml_keys))
    for src in _md_files(EU_DIR):
        if _is_family_stem(src.stem):
            continue
        eu.add(_resolve_key(src.stem, yaml_keys))
    for src in _md_files(SEC_DIR):
        if _is_family_stem(src.stem):
            continue
        sec.add(_resolve_key(src.stem, yaml_keys))
    return nl, eu, sec


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-cleanup", action="store_true", help="Keep old folders")
    args = parser.parse_args()

    y = _ruamel()
    with YAML_PATH.open(encoding="utf-8") as fh:
        data = y.load(fh)
    if not isinstance(data, dict):
        raise SystemExit("pollen.yaml top-level must be a mapping")

    yaml_keys = set(str(k) for k in data.keys())
    nl_keys, eu_keys, sec_keys = collect_folder_keys(yaml_keys)
    pct_map = _parse_index_honey_pcts(NL_DIR / "_index.md")
    # Only keep pct keys that exist in yaml
    pct_map = {k: v for k, v in pct_map.items() if k in yaml_keys}
    sec_mentions = _secundaire_mentions(NL_DIR / "_index.md", yaml_keys)

    print("=== YAML family split ===")
    fam_stats = split_families(data)
    print(fam_stats)

    print("=== Seed frequency + secondary ===")
    seed_stats = seed_frequency_and_secondary(
        data, nl_keys, eu_keys, sec_keys, pct_map, sec_mentions
    )
    print(seed_stats)
    print(f"nl_keys={len(nl_keys)} eu_keys={len(eu_keys)} sec_keys={len(sec_keys)}")
    print(f"pct_map={len(pct_map)} sec_mentions={sorted(sec_mentions)}")

    print("=== Migrate pages ===")
    page_report = migrate_pages(data, dry_run=args.dry_run)
    print(
        f"species_moved={page_report['species_moved']} "
        f"species_merged={page_report['species_merged']} "
        f"families_from_pages={page_report['families_from_pages']} "
        f"beug_md={page_report['skipped_beug']} "
        f"collisions={len(page_report['collisions'])}"
    )
    if page_report["collisions"][:15]:
        for c in page_report["collisions"][:15]:
            print(f"  collision {c['key']}: {c['winner']} over {c['others']}")

    species_on_disk = set(page_report["species_pages"])
    print("=== Build family pages from YAML ===")
    created_fams = build_family_pages_from_yaml(data, species_on_disk, dry_run=args.dry_run)
    all_family_slugs = sorted(
        set(page_report["family_pages"]) | set(created_fams) | {
            p.stem for p in FAMILIES_DIR.glob("*.md") if p.name != "_index.md"
        }
        if FAMILIES_DIR.is_dir()
        else set(page_report["family_pages"]) | set(created_fams)
    )
    write_indexes(all_family_slugs, page_report["species_pages"], dry_run=args.dry_run)
    print(f"family_pages_total≈{len(all_family_slugs)} yaml_generated={len(created_fams)}")

    if not args.dry_run:
        print("=== Write pollen.yaml ===")
        with YAML_PATH.open("w", encoding="utf-8") as fh:
            y.dump(data, fh)
        print(f"wrote {YAML_PATH.relative_to(REPO)}")

    if not args.skip_cleanup and not args.dry_run:
        print("=== Cleanup old folders ===")
        cleanup_old_dirs(dry_run=False)
    elif args.dry_run:
        cleanup_old_dirs(dry_run=True)

    # Summary counts for verification
    print("=== SUMMARY ===")
    print(f"families: {len(all_family_slugs)}")
    print(f"species pages: {len(page_report['species_pages'])}")
    print(f"frequency dutch filled this run: {seed_stats['dutch_set']}")
    print(f"frequency eu filled this run: {seed_stats['eu_set']}")
    print(f"secondary set: {seed_stats['secondary_set']}")
    print(f"nl⊂eu bumps: {seed_stats['nl_eu_bumped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
