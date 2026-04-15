from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _load_pollen_data() -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parent
    path = repo_root / "data" / "pollen.yaml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _get_dotted(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def define_env(env) -> None:
    pollen_data = _load_pollen_data()
    # Do not name this variable 'pollen' to avoid shadowing the pollen() macro in templates.
    env.variables["pollen_data"] = pollen_data

    get_context = None
    try:
        get_context = env.macros.get("context")
    except Exception:
        get_context = None

    @env.macro
    def pollen(key: str, field: str) -> str:
        entry = pollen_data.get(key)
        if not isinstance(entry, dict):
            return ""
        value = _get_dotted(entry, field)
        if value is None:
            return ""
        if isinstance(value, (dict, list)):
            return ""
        return str(value)

    @env.macro
    def pollen_img(key: str, src: str, alt: str = "") -> str:
        entry = pollen_data.get(key, {}) if isinstance(pollen_data, dict) else {}
        height_px: Optional[int] = None
        if isinstance(entry, dict):
            img = entry.get("image")
            if isinstance(img, dict):
                h = img.get("height_px")
                if isinstance(h, int):
                    height_px = h

        resolved_src = src
        if isinstance(src, str) and src.startswith("assets/") and callable(get_context):
            # Make docs-root relative assets work on nested pages using the page base_url.
            # [to be verified] context keys, validated via mkdocs build + rendered HTML.
            ctx = get_context() or {}
            if isinstance(ctx, list):
                picked = None
                for item in ctx:
                    if isinstance(item, dict) and ("base_url" in item or "base" in item):
                        picked = item
                        break
                ctx = picked or {}
            elif not isinstance(ctx, dict):
                ctx = {}
            base_url = ctx.get("base_url") or ctx.get("base") or ""
            if base_url:
                resolved_src = f"{base_url}/{src}"

        safe_src = escape(resolved_src, quote=True)
        safe_alt = escape(alt or key, quote=True)

        if height_px is None:
            return f'<img src="{safe_src}" alt="{safe_alt}">'

        return f'<img src="{safe_src}" style="height: {height_px}px; width: auto;" alt="{safe_alt}">'

