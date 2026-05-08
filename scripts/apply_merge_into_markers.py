#!/usr/bin/env python3
"""Apply merge_into / merge_note markers in data/pollen.yaml; update docs references."""

from __future__ import annotations

import re
import subprocess
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data/pollen.yaml"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets/images/by-taxon"


def split_blocks(text: str) -> OrderedDict[str, str]:
    ms = list(re.finditer(r"^([A-Za-z0-9_-]+):\s*\n", text, re.MULTILINE))
    out: OrderedDict[str, str] = OrderedDict()
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out[m.group(1)] = text[m.start() : end]
    return out


def blob_body(blob: str) -> str:
    i = blob.find(":\n")
    return blob[i + 2 :] if i >= 0 else blob


def norm_merge_target(raw: str) -> str:
    s = raw.strip()
    if not s:
        return s
    if re.fullmatch(r"[A-Za-z0-9_]+", s):
        return s.lower()
    parts = [p.lower() for p in re.split(r"\s+", s.replace("-", " ").strip()) if p]
    return "_".join(parts)


def find_merge_into(blob: str) -> str | None:
    for ln in blob.splitlines():
        m = re.match(r"^\s*merge_into:\s*(.+)$", ln)
        if m:
            return norm_merge_target(m.group(1))
        m = re.match(r"^\s*merge_into\s*\([^)]*\):\s*(.+)$", ln)
        if m:
            return norm_merge_target(m.group(1))
        m = re.match(r"^\s*rename_into:\s*(.+)$", ln)
        if m:
            return norm_merge_target(m.group(1))
        m = re.match(r"^\s*rename to:\s*(.+)$", ln)
        if m:
            return norm_merge_target(m.group(1))
    return None


def strip_mark(body: str) -> str:
    lines = []
    for ln in body.splitlines():
        ls = ln.lstrip()
        if ls.startswith(
            (
                "merge_into:",
                "merge_note:",
                "rename to:",
                "rename_into:",
                "merge_into (",
            )
        ):
            continue
        if re.match(r"^\s*merge_into\s*\([^)]*\):", ln):
            continue
        lines.append(ln)
    return "\n".join(lines).rstrip() + "\n"


def latin_slug(slug: str) -> str:
    pts = slug.split("_")
    while pts and pts[-1].lower() == "pollenwiki":
        pts.pop()
    return " ".join([pts[0].capitalize(), *pts[1:]]) if pts else slug


def scl(body: str, field: str) -> str | None:
    mm = re.search(rf"(?m)^  {re.escape(field)}:\s*(.*)$", body)
    if not mm:
        return None
    v = mm.group(1).strip()
    return v if v else None


def nes(body: str, section: str, field: str) -> str | None:
    m = re.search(rf"(?ms)^  {re.escape(section)}:\n(.*?)(?=^  [a-z_]|\Z)", body)
    if not m:
        return None
    im = re.search(rf"(?m)^    {re.escape(field)}:\s*(.*)$", m.group(1))
    if not im:
        return None
    v = im.group(1).strip()
    return v if v else None


def set_blank(body: str, field: str, val: str | None) -> str:
    if val is None:
        return body
    return re.sub(
        rf"(?m)^  {re.escape(field)}:\s*(.*)$",
        lambda z: f"  {field}: {val}" if not z.group(1).strip() else z.group(0),
        body,
        count=1,
    )


def fill_nes(body: str, section: str, field: str, val: str | None) -> str:
    if val is None:
        return body
    m = re.search(rf"(?ms)^  {re.escape(section)}:\n(.*?)(?=^  [a-z_]|\Z)", body)
    if not m:
        return body
    inner = m.group(1)
    inner2 = re.sub(
        rf"(?m)^    {re.escape(field)}:\s*(.*)$",
        lambda z: f"    {field}: {val}" if not z.group(1).strip() else z.group(0),
        inner,
        count=1,
    )
    return body[: m.start()] + f"  {section}:\n" + inner2 + body[m.end() :]


SRC_B = re.compile(r"(?ms)^    - source:.*?(?=^    - source:|^  [a-z_]|\Z)")


def sources_list(body: str) -> list[str]:
    m = re.search(r"(?ms)^  sources:\n(.*?)(?=^  [a-z_]|\Z)", body)
    if not m:
        return []
    inner = m.group(1).rstrip("\n") + "\n"
    if not inner.strip() or inner.strip().startswith("[]"):
        return []
    return [x.group(0).rstrip("\n") + "\n" for x in SRC_B.finditer(inner)]


def merge_sources(a: str, b: str) -> str:
    seen: set[str] = set()
    bits: list[str] = []
    for item in sources_list(a) + sources_list(b):
        k = " ".join(item.split())
        if k and k not in seen:
            seen.add(k)
            bits.append(item)
    if not bits:
        return a
    sec = "  sources:\n" + "".join(bits).rstrip("\n") + "\n"
    pat = rf"(?ms)^  sources:\n(.*?)(?=^  [a-z_]|\Z)"
    if re.search(pat, a):
        return re.sub(pat, sec, a, count=1)

    ix = a.find("\n  images:")
    return a[:ix] + "\n" + sec + a[ix:] if ix != -1 else a.rstrip() + "\n" + sec


def parse_images(body: str) -> list[tuple[str, str, str]]:
    m = re.search(r"(?ms)^  images:\n(.*?)(?=^  [a-z_]|\Z)", body)
    if not m:
        return []
    lines = m.group(1).splitlines()
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(lines):
        if re.match(r"^    - path:", lines[i]):
            p = lines[i].split(":", 1)[1].strip()
            kd, sr = "by_taxon", "by_taxon"
            i += 1
            if not p and i < len(lines) and "/" in lines[i]:
                p = lines[i].strip()
                i += 1
            while i < len(lines) and not re.match(r"^    - path:", lines[i]):
                if lines[i].startswith("      kind:"):
                    kd = lines[i].split(":", 1)[1].strip() or kd
                if lines[i].startswith("      source:"):
                    sr = lines[i].split(":", 1)[1].strip() or sr
                i += 1
            if p:
                out.append((p, kd, sr))
        else:
            i += 1
    return out


def seg(p: str) -> str | None:
    mm = re.search(r"/by-taxon/([^/]+)/", p)
    return mm.group(1) if mm else None


def ok_img(p: str, old: str, new: str) -> bool:
    s = seg(p) or ""
    return s == old or s.startswith(old + "_") or s == new


def rw(p: str, old: str, new: str) -> str:
    # Only substitute by-taxon folder segment; substring replace broke e.g.
    # lonicera -> lonicera_caprifolium on paths already mentioning lonicera_caprifolium.
    if f"/by-taxon/{old}/" not in p:
        return p
    out = p.replace(f"/by-taxon/{old}/", f"/by-taxon/{new}/")
    base = out.rsplit("/", 1)[-1]
    if base.startswith(old + "_"):
        nb = new + "_" + base.removeprefix(old + "_")
        return out.rsplit("/", 1)[0] + "/" + nb
    return out


def merge_imgs(tb: str, db: str, old: str, new: str) -> str:
    acc: OrderedDict[str, tuple[str, str]] = OrderedDict()
    for p, kd, sr in parse_images(tb):
        acc[p] = (kd, sr)
    for p, kd, sr in parse_images(db):
        if ok_img(p, old, new):
            p2 = rw(p, old, new)
            acc.setdefault(p2, (kd, sr))
    fld = ASSETS / new
    if fld.is_dir():
        for png in sorted(fld.glob("*.png")):
            acc.setdefault(
                f"assets/images/by-taxon/{new}/{png.name}",
                ("by_taxon", "by_taxon"),
            )
    if not acc:
        return tb
    txt = "".join(
        f"    - path: {p}\n      kind: {kd}\n      source: {sr}\n"
        for p, (kd, sr) in acc.items()
    )
    rep = "  images:\n" + txt.rstrip("\n") + "\n"
    pat = rf"(?ms)^  images:\n(.*?)(?=^  [a-z_]|\Z)"
    return re.sub(pat, rep, tb, count=1) if re.search(pat, tb) else tb.rstrip() + "\n" + rep


_FIELDS = (
    "latin",
    "dutch",
    "family",
    "shape",
    "sculpture",
    "aperture",
    "ornamentation",
    "polarity",
    "pe_ratio",
    "nectar_value",
    "pollen_value",
    "frequency_in_honey",
)


def absorb(tgt: str, base_body: str, donors: OrderedDict[str, str]) -> str:
    b = strip_mark(base_body)
    for old, chunk in donors.items():
        d = strip_mark(blob_body(chunk))
        has_sz = bool(nes(b, "size", "smallest_size") or nes(b, "size", "largest_size"))
        if not has_sz:
            for f in ("smallest_size", "largest_size", "height_px"):
                v = nes(d, "size", f)
                if v:
                    b = fill_nes(b, "size", f, v)
        for f in _FIELDS:
            dv = scl(d, f)
            if dv and not scl(b, f):
                b = set_blank(b, f, dv)
        for f in ("start", "end"):
            v = nes(d, "bloeitijd", f)
            if v:
                b = fill_nes(b, "bloeitijd", f, v)
        b = merge_sources(b, d)
        b = merge_imgs(b, d, old, tgt)
    b = strip_mark(b)
    if not scl(b, "latin"):
        b = set_blank(b, "latin", latin_slug(tgt))
    return f"{tgt}:\n" + b.rstrip() + "\n"


def rewrite_docs(omap: OrderedDict[str, str]) -> int:
    exts = {".md", ".json", ".yaml", ".yml", ".py", ".js", ".css"}
    n = 0
    gen = DOCS / "data/pollen.json"
    for p in DOCS.rglob("*"):
        if not p.is_file() or p.suffix not in exts:
            continue
        if p.resolve() == gen.resolve():
            continue
        try:
            s = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        ns = s
        for old, nw in omap.items():
            ns = re.sub(
                rf'"pollen_key"\s*:\s*"{re.escape(old)}"',
                f'"pollen_key": "{nw}"',
                ns,
            )
            ns = ns.replace(f'pollen_gallery("{old}")', f'pollen_gallery("{nw}")')
            ns = ns.replace(f'pollen("{old}",', f'pollen("{nw}",')
            ns = ns.replace(f'pollen_img("{old}"', f'pollen_img("{nw}"')
            ns = ns.replace(f"by-taxon/{old}/", f"by-taxon/{nw}/")
        if ns != s:
            p.write_text(ns, encoding="utf-8")
            n += 1
    return n


def main() -> int:
    raw = YAML_PATH.read_text(encoding="utf-8")
    blocks = split_blocks(raw)
    orig = list(blocks.keys())
    stale: OrderedDict[str, str] = OrderedDict()
    for k, blob in blocks.items():
        t = find_merge_into(blob)
        if t:
            stale[k] = t
    if not stale:
        print("No merge_into entries.")
        return 0

    by_tgt: defaultdict[str, list[str]] = defaultdict(list)
    for o, t in stale.items():
        by_tgt[t].append(o)

    stale_set = set(stale)
    merged: dict[str, str] = {}

    for tgt, olds in by_tgt.items():
        od = OrderedDict((o, blocks[o]) for o in olds)
        if tgt in blocks and tgt not in stale_set:
            inner = strip_mark(blob_body(blocks[tgt]))
            merged[tgt] = absorb(tgt, inner, od)
        else:
            _, fb = next(iter(od.items()))
            inner = strip_mark(blob_body(fb))
            merged[tgt] = absorb(tgt, inner, od)

    out_parts: list[str] = []
    emitted = set()
    first_stale: dict[str, int] = {}
    kept = set(orig) - stale_set
    for i, k in enumerate(orig):
        if k in stale_set:
            t = stale[k]
            first_stale.setdefault(t, i)

    for i, k in enumerate(orig):
        if k in stale_set:
            t = stale[k]
            if t not in kept and i == first_stale[t] and t not in emitted:
                out_parts.append(merged[t])
                emitted.add(t)
            continue
        if k in merged:
            out_parts.append(merged[k])
            continue
        out_parts.append(blocks[k])

    YAML_PATH.write_text("".join(p.rstrip() + "\n" for p in out_parts), encoding="utf-8")
    nf = rewrite_docs(OrderedDict((o, stale[o]) for o in stale))
    print(f"Merged {len(stale)} stale keys into {len(by_tgt)} targets; updated {nf} docs files.")

    py = ROOT / ".venv/bin/python"
    val = ROOT / "scripts/validate_pollen_site.py"
    rc = subprocess.run(
        [str(py), str(val), "--rebuild-data", "--images", "--links"],
        cwd=str(ROOT),
        check=False,
    ).returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
