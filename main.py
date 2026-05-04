from __future__ import annotations

import sys
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from mkdocs.utils import normalize_url

_SCRIPTS = Path(__file__).resolve().parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from pollen_display import display_width_px_for_yaml_entry, per_image_width_px  # noqa: E402


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


def _canonical_assets_uri(src: str) -> Optional[str]:
    """Strip Markdown-relative prefixes so nested pages resolve under MkDocs base_url."""
    s = src.strip().replace("\\", "/")
    while s.startswith("../"):
        s = s[3:]
    if s.startswith("assets/"):
        return s
    return None


def _resolve_assets_href(canonical_uri: Optional[str], macros_plugin: Any) -> str:
    """Resolve docs-relative assets/… to correct href for current MkDocs output page."""
    if not isinstance(canonical_uri, str) or not canonical_uri.startswith("assets/"):
        return canonical_uri or ""
    page = getattr(macros_plugin, "_page", None)
    if page is None:
        return canonical_uri
    try:
        return normalize_url(path=canonical_uri, page=page)
    except Exception:
        return canonical_uri


def define_env(env) -> None:
    pollen_data = _load_pollen_data()
    # Do not name this variable 'pollen' to avoid shadowing the pollen() macro in templates.
    env.variables["pollen_data"] = pollen_data

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
    def pollen_img(
        key: str,
        src: str,
        alt: str = "",
        item_height_px: Optional[Any] = None,
    ) -> str:
        entry = pollen_data.get(key, {}) if isinstance(pollen_data, dict) else {}
        height_px: Optional[int] = None
        if isinstance(entry, dict):
            height_px = display_width_px_for_yaml_entry(entry)

        ih = item_height_px
        if isinstance(ih, int) and ih > 0:
            height_px = ih

        canonical = (
            src if isinstance(src, str) and src.strip().startswith("assets/") else _canonical_assets_uri(src)
        )
        resolved_src = _resolve_assets_href(canonical, env) if canonical else src

        safe_src = escape(resolved_src or "", quote=True)
        lat = ""
        if isinstance(entry, dict) and isinstance(entry.get("latin"), str):
            lat = entry["latin"].strip()
        safe_alt = escape(alt or lat or key, quote=True)

        if height_px is None:
            return f'<img src="{safe_src}" alt="{safe_alt}">'

        return f'<img src="{safe_src}" style="width: {height_px}px; height: auto;" alt="{safe_alt}">'

    @env.macro
    def pollen_gallery(key: str) -> str:
        """Render all YAML `images` for taxon `key` in gallery layout."""
        entry = pollen_data.get(key) if isinstance(pollen_data, dict) else None
        if not isinstance(entry, dict):
            return ""

        latin = ""
        if isinstance(entry.get("latin"), str):
            latin = entry["latin"].strip()

        default_w = display_width_px_for_yaml_entry(entry)

        imgs = entry.get("images")
        if not isinstance(imgs, list) or not imgs:
            return ""

        figures: List[str] = []
        for im in imgs:
            if not isinstance(im, dict):
                continue
            raw_path = im.get("path")
            if not isinstance(raw_path, str) or not raw_path.strip():
                continue

            canon = raw_path.strip().replace("\\", "/").lstrip("./")
            if not canon.startswith("assets/"):
                continue

            iw = per_image_width_px(im, default_w)

            href = _resolve_assets_href(canon, env)
            safe_src = escape(href, quote=True)

            fname = Path(canon).name
            caption = latin or key
            safe_alt = escape(f"{caption} ({fname})", quote=True)

            style = ""
            if iw > 0:
                style = f' style="width: {iw}px; height: auto;"'

            figures.append(
                f'<figure class="pid-scale-item"><img src="{safe_src}"{style} alt="{safe_alt}"></figure>'
            )

        if not figures:
            return ""

        inner = "".join(figures)
        return (
            '<div class="pid-scale-gallery">'
            '<div class="pid-scale-row pid-scale-row--snug">'
            f"{inner}"
            "</div></div>"
        )

