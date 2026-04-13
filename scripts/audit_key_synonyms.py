#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYS_DIR = DOCS_DIR / "keys"


BINOMIAL_RE = re.compile(r"\b([A-Z][a-z]+)\s+([a-z][a-z-]+)\b")
WS_RE = re.compile(r"\s+")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def strip_emphasis_ast(s: str) -> str:
    # Backward compatible with older labels containing *...*
    return re.sub(r"\*([^*]*)\*", r"\1", s)


def norm_spaces(s: str) -> str:
    return WS_RE.sub(" ", s).strip()


def extract_binomial(name: str) -> Optional[str]:
    """
    Extract first Latin binomial (Genus species) from a string.
    Returns canonical "Genus species" or None.
    """
    if not isinstance(name, str):
        return None
    s = norm_spaces(strip_emphasis_ast(name))
    m = BINOMIAL_RE.search(s)
    if not m:
        return None
    return f"{m.group(1)} {m.group(2)}"


@dataclass(frozen=True)
class EndpointRef:
    key_path: str  # docs-relative keys/...json
    step_id: str
    choice_idx: int
    choice_label: str


def iter_endpoints(key_json_path: Path) -> Iterable[Tuple[str, str, EndpointRef]]:
    """
    Yield (canonical_binomial, raw_name, ref) for each endpoint with id.name.
    """
    data = read_json(key_json_path)
    if not isinstance(data, dict):
        return
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return

    key_rel = key_json_path.relative_to(DOCS_DIR).as_posix()

    for step_id, step in steps.items():
        if not isinstance(step, dict):
            continue
        choices = step.get("choices")
        if not isinstance(choices, list):
            continue
        for idx, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            ident = ch.get("id")
            if not isinstance(ident, dict):
                continue
            raw_name = ident.get("name")
            if not isinstance(raw_name, str) or not raw_name.strip():
                continue
            canon = extract_binomial(raw_name)
            if not canon:
                continue
            ref = EndpointRef(
                key_path=key_rel,
                step_id=str(step_id),
                choice_idx=int(idx),
                choice_label=str(ch.get("label") or ""),
            )
            yield canon, norm_spaces(strip_emphasis_ast(raw_name)), ref


def main() -> int:
    key_paths = sorted(KEYS_DIR.rglob("*.json"))

    # canon -> variant -> [refs]
    refs: Dict[str, Dict[str, List[EndpointRef]]] = defaultdict(lambda: defaultdict(list))

    for kp in key_paths:
        try:
            for canon, raw_name, ref in iter_endpoints(kp):
                refs[canon][raw_name].append(ref)
        except Exception as e:
            raise RuntimeError(f"Failed reading {kp}: {e}") from e

    conflicts: List[Tuple[int, int, str]] = []
    for canon, variants in refs.items():
        if len(variants) <= 1:
            continue
        endpoint_count = sum(len(v) for v in variants.values())
        conflicts.append((len(variants), endpoint_count, canon))

    conflicts.sort(key=lambda t: (-t[0], -t[1], t[2]))

    print("Key synonym audit (endpoint id.name)")
    print(f"keys_scanned={len(key_paths)}")
    print(f"conflict_groups={len(conflicts)}")
    print("")
    top = conflicts[:50]
    for i, (variant_count, endpoint_count, canon) in enumerate(top, 1):
        variants = refs[canon]
        vcounts = {v: len(rs) for v, rs in variants.items()}
        has_syn = any(re.search(r"\bsyn\b\.?", v, flags=re.IGNORECASE) for v in variants.keys())
        print(f"{i:>2}. {canon} | variants={variant_count} endpoints={endpoint_count}" + (" | HAS_SYN" if has_syn else ""))

        # Sort variants: syn-containing first, then by count desc, then alpha
        def vkey(v: str) -> Tuple[int, int, str]:
            syn = 0 if re.search(r"\bsyn\b\.?", v, flags=re.IGNORECASE) else 1
            return (syn, -vcounts[v], v)

        for v in sorted(variants.keys(), key=vkey):
            rs = variants[v]
            c = len(rs)
            syn_flag = " [syn]" if re.search(r"\bsyn\b\.?", v, flags=re.IGNORECASE) else ""
            sample = rs[0]
            print(
                f"    - {c:>3}x{syn_flag} {v}  (e.g. {sample.key_path} step {sample.step_id} choice {sample.choice_idx})"
            )
        print("")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

