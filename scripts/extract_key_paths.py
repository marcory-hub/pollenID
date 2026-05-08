from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
KEYS_DIR = REPO_ROOT / "docs" / "keys"


@dataclass(frozen=True)
class StepRender:
    step_id: str
    choices: List[str]
    chosen_idx: int


@dataclass(frozen=True)
class PathRender:
    key_id: str
    key_title: str
    steps: List[StepRender]
    outcome_label: str


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def _norm_title(s: str) -> str:
    t = (s or "").strip().lower()
    t = t.replace("–", "-").replace("—", "-")
    # remove parenthetical qualifiers, which differ between base and subkeys
    t = re.sub(r"\([^)]*\)", "", t)
    # keep only alnum and separators for stable matching
    t = re.sub(r"[^a-z0-9]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\bbeug\b", "", t).strip()
    t = re.sub(r"\s+", " ", t).strip()
    return t

def _beug_num_from_meta_key(meta_key: str) -> str:
    # Examples: beug04-tetradeae.json, beug04-tetradeae-ericaceae-empetrum.json
    m = re.match(r"^(beug\d\d)", (meta_key or "").strip(), flags=re.I)
    return m.group(1).lower() if m else ""


def _as_str(x: Any) -> str:
    return "" if x is None else str(x)


def _iter_key_files() -> Iterable[Tuple[str, Path]]:
    yield ("beug", KEYS_DIR / "beug")
    yield ("vanderham", KEYS_DIR / "vanderham")
    yield ("kerkvliet", KEYS_DIR / "kerkvliet")


def _key_title(meta: Any, fallback: str) -> str:
    if isinstance(meta, dict) and isinstance(meta.get("title"), str) and meta["title"].strip():
        return meta["title"].strip()
    return fallback


def _is_terminal_for_taxon(choice: Dict[str, Any], taxon_key: str) -> bool:
    cid = choice.get("id")
    if isinstance(cid, dict):
        pk = cid.get("pollen_key")
        if isinstance(pk, str) and pk.strip() == taxon_key:
            return True
        pks = cid.get("pollen_keys")
        if isinstance(pks, list) and any(isinstance(x, str) and x.strip() == taxon_key for x in pks):
            return True
    out = choice.get("outcome")
    if isinstance(out, dict):
        pk = out.get("pollen_key")
        if isinstance(pk, str) and pk.strip() == taxon_key:
            return True
        pks = out.get("pollen_keys")
        if isinstance(pks, list) and any(isinstance(x, str) and x.strip() == taxon_key for x in pks):
            return True
    return False


def _choice_outcome_label(choice: Dict[str, Any], taxon_key: str) -> str:
    cid = choice.get("id")
    if isinstance(cid, dict):
        if isinstance(cid.get("name"), str) and cid["name"].strip():
            return cid["name"].strip()
        if isinstance(cid.get("text"), str) and cid["text"].strip():
            return cid["text"].strip()
        if isinstance(cid.get("note"), str) and cid["note"].strip():
            return cid["note"].strip()
        pk = cid.get("pollen_key")
        if isinstance(pk, str) and pk.strip():
            return pk.strip()
        pks = cid.get("pollen_keys")
        if isinstance(pks, list) and pks:
            return ", ".join([_as_str(x) for x in pks if _as_str(x)])
    out = choice.get("outcome")
    if isinstance(out, dict) and isinstance(out.get("text"), str) and out["text"].strip():
        return out["text"].strip()
    return taxon_key


def _extract_paths_from_steps(key_json: Dict[str, Any], taxon_key: str) -> List[PathRender]:
    meta = key_json.get("meta")
    key_id = ""
    if isinstance(meta, dict) and isinstance(meta.get("key"), str):
        key_id = meta["key"].strip()
    if not key_id:
        key_id = "key"

    key_title = _key_title(meta, key_id)

    start = key_json.get("start")
    steps = key_json.get("steps")
    if not isinstance(start, str) or not isinstance(steps, dict):
        return []

    results: List[PathRender] = []

    def dfs(step_id: str, acc: List[StepRender], seen: set[str]) -> None:
        if step_id in seen:
            return
        seen2 = set(seen)
        seen2.add(step_id)

        step = steps.get(step_id)
        if not isinstance(step, dict):
            return
        choices = step.get("choices")
        if not isinstance(choices, list) or not choices:
            return

        labels: List[str] = []
        for ch in choices:
            if isinstance(ch, dict) and isinstance(ch.get("label"), str):
                labels.append(ch["label"].strip())
            else:
                labels.append("")

        for idx, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            next_id = ch.get("next")
            chosen = StepRender(step_id=step_id, choices=labels, chosen_idx=idx)

            if _is_terminal_for_taxon(ch, taxon_key):
                results.append(
                    PathRender(
                        key_id=key_id,
                        key_title=key_title,
                        steps=acc + [chosen],
                        outcome_label=_choice_outcome_label(ch, taxon_key),
                    )
                )
                continue

            if isinstance(next_id, str) and next_id.strip():
                dfs(next_id.strip(), acc + [chosen], seen2)

    dfs(start.strip(), [], set())
    return results


def _extract_all_named_endpoints_paths(key_json: Dict[str, Any]) -> Dict[str, List[StepRender]]:
    """
    For Beug base keys: map endpoint id.name (normalized) to the step path reaching it.
    This lets us prepend base-key steps when a subkey title is reached as an endpoint.
    """
    start = key_json.get("start")
    steps = key_json.get("steps")
    if not isinstance(start, str) or not isinstance(steps, dict):
        return {}

    out: Dict[str, List[StepRender]] = {}

    def dfs(step_id: str, acc: List[StepRender], seen: set[str]) -> None:
        if step_id in seen:
            return
        seen2 = set(seen)
        seen2.add(step_id)

        step = steps.get(step_id)
        if not isinstance(step, dict):
            return
        choices = step.get("choices")
        if not isinstance(choices, list) or not choices:
            return

        labels: List[str] = []
        for ch in choices:
            if isinstance(ch, dict) and isinstance(ch.get("label"), str):
                labels.append(ch["label"].strip())
            else:
                labels.append("")

        for idx, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            next_id = ch.get("next")
            chosen = StepRender(step_id=step_id, choices=labels, chosen_idx=idx)

            cid = ch.get("id")
            if cid is None and isinstance(ch.get("outcome"), dict):
                cid = ch.get("outcome")
            if isinstance(cid, dict) and isinstance(cid.get("name"), str) and cid["name"].strip():
                nm = _norm_title(cid["name"])
                out.setdefault(nm, acc + [chosen])

            if isinstance(next_id, str) and next_id.strip():
                dfs(next_id.strip(), acc + [chosen], seen2)

    dfs(start.strip(), [], set())
    return out


def _extract_kerkvliet_sections(key_json: Dict[str, Any], taxon_key: str) -> List[PathRender]:
    meta = key_json.get("meta")
    key_id = ""
    if isinstance(meta, dict) and isinstance(meta.get("key"), str):
        key_id = meta["key"].strip()
    if not key_id:
        key_id = "kerkvliet"
    key_title = _key_title(meta, "Kerkvliet determinatietabel")

    rows = key_json.get("rows")
    if not isinstance(rows, list):
        return []
    sections: List[str] = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        if r.get("pollen_key") == taxon_key and isinstance(r.get("section"), str):
            sections.append(r["section"].strip())

    # Kerkvliet is a flat section list, not a dichotomous path; render as a single-step “location”.
    results: List[PathRender] = []
    for sec in sorted({s for s in sections if s}):
        results.append(
            PathRender(
                key_id=key_id,
                key_title=key_title,
                steps=[StepRender(step_id="section", choices=[sec], chosen_idx=0)],
                outcome_label=taxon_key,
            )
        )
    return results


def extract_paths_for_taxon(taxon_key: str) -> Dict[str, List[PathRender]]:
    out: Dict[str, List[PathRender]] = {"beug": [], "vanderham": [], "kerkvliet": []}

    # Beug: step graphs with base->subkey chaining per beug number
    beug_root = KEYS_DIR / "beug"
    if beug_root.exists():
        beug_files = sorted(beug_root.glob("beug*.json"))
        beug_json: Dict[str, Dict[str, Any]] = {}
        beug_meta: Dict[str, Tuple[str, str]] = {}  # meta.key -> (title, beug_num)
        for p in beug_files:
            data = _read_json(p)
            if not isinstance(data, dict):
                continue
            meta = data.get("meta")
            meta_key = ""
            title = p.name
            if isinstance(meta, dict):
                if isinstance(meta.get("key"), str):
                    meta_key = meta["key"].strip()
                title = _key_title(meta, p.name)
            if not meta_key:
                meta_key = p.name
            beug_json[meta_key] = data
            beug_meta[meta_key] = (title, _beug_num_from_meta_key(meta_key))

        # Build base endpoint maps for each base Beug file (beugNN-<group>.json)
        base_endpoint_paths: Dict[str, Dict[str, List[StepRender]]] = {}
        base_titles: Dict[str, str] = {}
        for meta_key, (title, _) in beug_meta.items():
            if re.match(r"^beug\d\d-[^-]+\.json$", meta_key, flags=re.I):
                base_endpoint_paths[meta_key] = _extract_all_named_endpoints_paths(beug_json[meta_key])
                base_titles[meta_key] = title

        # Extract taxon paths and prepend base path when subkey title is reachable as endpoint
        for meta_key, data in beug_json.items():
            title, _ = beug_meta.get(meta_key, (meta_key, ""))
            prs = _extract_paths_from_steps(data, taxon_key)
            if not prs:
                continue

            # Attempt chaining: for beugNN-<group>-<subkey>.json, base is beugNN-<group>.json
            base_key = re.sub(r"^(beug\d\d-[^-]+)-.+\.json$", r"\1.json", meta_key, flags=re.I)
            if base_key != meta_key and base_key in base_endpoint_paths:
                nm = _norm_title(title)
                base_map = base_endpoint_paths[base_key]
                if nm in base_map:
                    base_steps = base_map[nm]
                    chained: List[PathRender] = []
                    for pr in prs:
                        # Base key path ends at the subkey endpoint (id.name), not at a species.
                        chained.append(
                            PathRender(
                                key_id=base_key,
                                key_title=base_titles.get(base_key, base_key),
                                steps=base_steps,
                                outcome_label=title,
                            )
                        )
                        # Then render the subkey path separately (this is where the species resolves).
                        chained.append(
                            PathRender(
                                key_id=meta_key,
                                key_title=title,
                                steps=pr.steps,
                                outcome_label=pr.outcome_label,
                            )
                        )
                    out["beug"].extend(chained)
                    continue

            out["beug"].extend(prs)

    # Vanderham: step graphs
    vdh_root = KEYS_DIR / "vanderham"
    if vdh_root.exists():
        for path in sorted(vdh_root.glob("*.json")):
            data = _read_json(path)
            if not isinstance(data, dict):
                continue
            out["vanderham"].extend(_extract_paths_from_steps(data, taxon_key))

    # Kerkvliet: flat table
    k_path = KEYS_DIR / "kerkvliet" / "kerkvliet-determinatietabel.json"
    if k_path.exists():
        k_data = _read_json(k_path)
        if isinstance(k_data, dict):
            out["kerkvliet"].extend(_extract_kerkvliet_sections(k_data, taxon_key))

    return out


def render_paths_markdown(taxon_key: str) -> str:
    paths = extract_paths_for_taxon(taxon_key)
    blocks: List[str] = []

    def render_one(pr: PathRender) -> str:
        step_lines: List[str] = []
        for st in pr.steps:
            # Kerkvliet pseudo-step
            if st.step_id == "section":
                step_lines.append(f'- Sectie: {st.choices[0]}')
                continue
            step_lines.append(f'- Stap {st.step_id}:')
            for i, lbl in enumerate(st.choices):
                cls = (
                    "pid-key-choice pid-key-choice--on"
                    if i == st.chosen_idx
                    else "pid-key-choice pid-key-choice--off"
                )
                safe = lbl.replace("<", "&lt;").replace(">", "&gt;")
                step_lines.append(f'  - <span class="{cls}">{safe}</span>')
        return "\n".join(step_lines)

    for system in ["beug", "vanderham", "kerkvliet"]:
        sys_paths = paths.get(system, [])
        if not sys_paths:
            continue
        # group by key_id
        grouped: Dict[str, List[PathRender]] = {}
        for pr in sys_paths:
            grouped.setdefault(pr.key_id, []).append(pr)

        blocks.append(f"### {system.capitalize()}")
        def sort_key(item: tuple[str, List[PathRender]]) -> tuple[int, str]:
            key_id, _prs = item
            if system == "beug":
                # base Beug keys first: beugNN-<group>.json
                if re.match(r"^beug\d\d-[^-]+\.json$", key_id, flags=re.I):
                    return (0, key_id)
                return (1, key_id)
            return (0, key_id)

        for _, prs in sorted(grouped.items(), key=sort_key):
            title = prs[0].key_title
            blocks.append(f"<details><summary>{title}</summary>\n")
            for idx, pr in enumerate(prs, start=1):
                if len(prs) > 1:
                    blocks.append(f"<details><summary>Pad {idx}</summary>\n")
                blocks.append(render_one(pr))
                if len(prs) > 1:
                    blocks.append("\n</details>")
                blocks.append("")
            blocks.append("</details>\n")

    return "\n".join(blocks).strip() + "\n"


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("taxon_key")
    args = ap.parse_args()
    print(render_paths_markdown(args.taxon_key))
