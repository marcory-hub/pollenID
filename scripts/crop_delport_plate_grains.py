#!/usr/bin/env python3
"""Crop labelled pollen panels from Delport 2025 atlas plates into by-taxon PNGs.

Reads ``docs/keys/flora-regio-kaap/taxa-index.json`` for plate letters and
``pollen_key`` values. Extracts the largest embedded RGB image per plate page
(page_index = plate_num + 2), segments lettered panels (white-gutter split with
uniform-grid fallback), then tight-crops significant pollen blobs inside each
panel.

Does not modify ``data/pollen.yaml``.

Examples::

    ./.venv/bin/python scripts/crop_delport_plate_grains.py --plate 4
    ./.venv/bin/python scripts/crop_delport_plate_grains.py --plate 1 --dry-run
    ./.venv/bin/python scripts/crop_delport_plate_grains.py --all
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import pymupdf
from PIL import Image, ImageChops, ImageFilter, ImageOps

REPO = Path(__file__).resolve().parents[1]
DEFAULT_PDF = (
    REPO
    / "pdf"
    / "pollen-determinatie"
    / "Delport 2025 - Pollen atlas Greater Cape Floristic Region.pdf"
)
DEFAULT_INDEX = REPO / "docs" / "keys" / "flora-regio-kaap" / "taxa-index.json"
DEFAULT_OUT = REPO / "docs" / "assets" / "images" / "by-taxon"

# Plate N is PDF page_index N+2 (Plate 1 -> index 3, Plate 4 -> index 6).
PLATE_PAGE_OFFSET = 2

Box = Tuple[int, int, int, int]  # x0, y0, x1, y1


@dataclass
class TaxonPanel:
    plate_num: int
    plate_letter: str
    latin_name: str
    pollen_key: str


def load_taxa_by_plate(index_path: Path) -> Dict[int, List[TaxonPanel]]:
    data = json.loads(index_path.read_text(encoding="utf-8"))
    by_plate: Dict[int, List[TaxonPanel]] = defaultdict(list)
    for row in data["taxa"]:
        by_plate[int(row["plate_num"])].append(
            TaxonPanel(
                plate_num=int(row["plate_num"]),
                plate_letter=str(row["plate_letter"]).strip().upper(),
                latin_name=str(row["latin_name"]),
                pollen_key=str(row["pollen_key"]),
            )
        )
    for plate_num, items in by_plate.items():
        items.sort(key=lambda t: (len(t.plate_letter), t.plate_letter))
    return dict(by_plate)


def extract_largest_page_image(doc: pymupdf.Document, page_index: int) -> Image.Image:
    page = doc[page_index]
    images = page.get_images(full=True)
    if not images:
        raise RuntimeError(f"page_index {page_index}: no embedded images")
    best_xref = None
    best_pixels = -1
    for img in images:
        xref = img[0]
        meta = doc.extract_image(xref)
        pixels = int(meta["width"]) * int(meta["height"])
        if pixels > best_pixels:
            best_pixels = pixels
            best_xref = xref
    assert best_xref is not None
    meta = doc.extract_image(best_xref)
    return Image.open(io.BytesIO(meta["image"])).convert("RGB")


def render_page_image(doc: pymupdf.Document, page_index: int, dpi: int) -> Image.Image:
    page = doc[page_index]
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def choose_ncols(n_letters: int) -> int:
    if n_letters <= 4:
        return 2
    if n_letters <= 9:
        return 3
    return 4


def uniform_grid_panels(
    width: int,
    height: int,
    n_letters: int,
    *,
    top_frac: float = 0.0,
    bottom_frac: float = 0.0,
) -> List[Box]:
    """Row-major A,B,C... cells over the content area."""
    top = int(height * top_frac)
    bot = int(height * (1.0 - bottom_frac))
    content_h = max(1, bot - top)
    ncols = choose_ncols(n_letters)
    nrows = int(math.ceil(n_letters / ncols))
    panels: List[Box] = []
    for i in range(n_letters):
        r = i // ncols
        c = i % ncols
        x0 = int(c * width / ncols)
        x1 = int((c + 1) * width / ncols)
        y0 = top + int(r * content_h / nrows)
        y1 = top + int((r + 1) * content_h / nrows)
        panels.append((x0, y0, x1, y1))
    return panels


def _find_runs(
    values: Sequence[float], coords: Sequence[int], thr: float, min_run: int
) -> List[Tuple[int, int]]:
    bands: List[Tuple[int, int]] = []
    in_run = False
    start = end = 0
    for c, v in zip(coords, values):
        if v >= thr:
            if not in_run:
                in_run = True
                start = c
            end = c
        else:
            if in_run:
                if end - start + 1 >= min_run:
                    bands.append((start, end))
                in_run = False
    if in_run and end - start + 1 >= min_run:
        bands.append((start, end))
    return bands


def _row_means(gray: Image.Image, y0: int, y1: int, step_x: int = 2) -> Tuple[List[int], List[float]]:
    px = gray.load()
    w, _ = gray.size
    coords: List[int] = []
    means: List[float] = []
    for y in range(y0, y1):
        total = 0
        n = 0
        for x in range(0, w, step_x):
            total += px[x, y]
            n += 1
        coords.append(y)
        means.append(total / max(1, n))
    return coords, means


def _col_span_scores(
    gray: Image.Image, y0: int, y1: int, bright: float, min_span_frac: float
) -> Tuple[List[int], List[float]]:
    px = gray.load()
    w, _ = gray.size
    coords: List[int] = []
    scores: List[float] = []
    for x in range(w):
        bright_n = 0
        total = 0
        s = 0
        for y in range(y0, y1):
            v = px[x, y]
            s += v
            total += 1
            if v >= bright:
                bright_n += 1
        span = bright_n / max(1, total)
        mean = s / max(1, total)
        scores.append(mean if span >= min_span_frac else 0.0)
        coords.append(x)
    return coords, scores


def _merge_thin_intervals(
    cuts: Sequence[int], min_size: int
) -> List[Tuple[int, int]]:
    intervals: List[Tuple[int, int]] = []
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        if b - a < min_size and intervals:
            intervals[-1] = (intervals[-1][0], b)
        else:
            intervals.append((a, b))
    return intervals


def segment_by_gutters(
    img: Image.Image,
    *,
    bright: float,
    min_h_run: int = 5,
    min_v_run: int = 6,
    min_row_h: int = 80,
    min_col_w: int = 60,
    min_span_frac: float = 0.80,
) -> List[Box]:
    """Split plate image into panels using full-width H gutters and full-height V gutters."""
    gray = ImageOps.grayscale(img)
    w, h = gray.size
    coords, means = _row_means(gray, 0, h)
    hg = _find_runs(means, coords, bright, min_h_run)
    hg = [(a, b) for a, b in hg if a > 30 and b < h - 30]
    ys = [0] + [(a + b) // 2 for a, b in hg] + [h]
    rows = _merge_thin_intervals(ys, min_row_h)

    panels: List[Box] = []
    for y0, y1 in rows:
        inner0 = y0 + 5
        inner1 = max(inner0 + 1, y1 - 5)
        ccoords, scores = _col_span_scores(gray, inner0, inner1, bright, min_span_frac)
        vg = _find_runs(scores, ccoords, bright, min_v_run)
        vg = [(a, b) for a, b in vg if a > 40 and b < w - 40]
        xs = [0] + [(a + b) // 2 for a, b in vg] + [w]
        cols = _merge_thin_intervals(xs, min_col_w)
        for x0, x1 in cols:
            panels.append((x0, y0, x1, y1))
    return panels


def segment_panels(img: Image.Image, n_letters: int) -> Tuple[List[Box], str]:
    """Return panels matching n_letters, preferring gutter split over uniform grid."""
    best: Optional[List[Box]] = None
    best_bright: Optional[float] = None
    best_delta = 10**9
    for bright in range(230, 249):
        panels = segment_by_gutters(img, bright=float(bright))
        delta = abs(len(panels) - n_letters)
        if delta < best_delta:
            best_delta = delta
            best = panels
            best_bright = float(bright)
        if delta == 0:
            break
    if best is not None and len(best) == n_letters:
        return best, f"gutters(bright={best_bright:g})"
    # Uniform grid fallback (content area; embedded plate images usually have no caption).
    grid = uniform_grid_panels(img.size[0], img.size[1], n_letters)
    note = "grid"
    if best is not None and best_bright is not None:
        note = f"grid(fallback; gutters@{best_bright:g} gave {len(best)})"
    return grid, note


def connected_components(
    mask: Image.Image, *, min_area: int
) -> List[dict]:
    """mask: mode L, 255 = foreground."""
    w, h = mask.size
    px = mask.load()
    visited = bytearray(w * h)
    comps: List[dict] = []

    def idx(x: int, y: int) -> int:
        return y * w + x

    for y in range(h):
        for x in range(w):
            if visited[idx(x, y)] or px[x, y] == 0:
                continue
            stack = [(x, y)]
            visited[idx(x, y)] = 1
            minx = maxx = x
            miny = maxy = y
            area = 0
            while stack:
                cx, cy = stack.pop()
                area += 1
                if cx < minx:
                    minx = cx
                if cx > maxx:
                    maxx = cx
                if cy < miny:
                    miny = cy
                if cy > maxy:
                    maxy = cy
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if (
                        0 <= nx < w
                        and 0 <= ny < h
                        and not visited[idx(nx, ny)]
                        and px[nx, ny]
                    ):
                        visited[idx(nx, ny)] = 1
                        stack.append((nx, ny))
            bw = maxx - minx + 1
            bh = maxy - miny + 1
            comps.append(
                {
                    "bbox": (minx, miny, maxx + 1, maxy + 1),
                    "area": area,
                    "w": bw,
                    "h": bh,
                    "aspect": bw / max(1, bh),
                    "fill": area / (bw * bh),
                }
            )
    return [c for c in comps if c["area"] >= min_area]


def _foreground_mask(panel: Image.Image, dark_thr: int) -> Image.Image:
    """Dark or saturated pixels (catches purple stains and yellowish grains)."""
    gray = ImageOps.grayscale(panel)
    dark = gray.point(lambda p: 255 if p < dark_thr else 0)
    r, g, b = panel.split()
    # sat ~= max-min; approximate with pairwise abs diffs OR'd together.
    rg = ImageChops.difference(r, g)
    rb = ImageChops.difference(r, b)
    gb = ImageChops.difference(g, b)
    sat = ImageChops.lighter(ImageChops.lighter(rg, rb), gb)
    sat_m = sat.point(lambda p: 255 if p >= 28 else 0)
    mask = ImageChops.lighter(dark, sat_m)
    # Light close only: fill spine gaps without bridging neighbouring grains.
    mask = mask.filter(ImageFilter.MaxFilter(3))
    mask = mask.filter(ImageFilter.MinFilter(3))
    return mask


def _try_split_wide_blob(
    panel: Image.Image, bbox: Box, mask: Image.Image
) -> Optional[List[Box]]:
    """If one wide blob looks like two side-by-side grains, split on a column valley."""
    x0, y0, x1, y1 = bbox
    bw = x1 - x0
    bh = y1 - y0
    if bw < 80 or bh < 40 or (bw / max(1, bh)) < 1.55:
        return None
    mpx = mask.load()
    # ink density per column inside bbox
    dens: List[int] = []
    for x in range(x0, x1):
        s = 0
        for y in range(y0, y1):
            if mpx[x, y]:
                s += 1
        dens.append(s)
    # search valley in central 50%
    lo = int(len(dens) * 0.25)
    hi = int(len(dens) * 0.75)
    if hi <= lo + 2:
        return None
    window = dens[lo:hi]
    min_i = min(range(len(window)), key=lambda i: window[i])
    valley = window[min_i]
    peak = max(dens) if dens else 0
    if peak <= 0 or valley > peak * 0.35:
        return None
    split_x = x0 + lo + min_i
    left = (x0, y0, split_x, y1)
    right = (split_x, y0, x1, y1)
    if (split_x - x0) < bw * 0.25 or (x1 - split_x) < bw * 0.25:
        return None
    return [left, right]


def find_grain_crops(
    panel: Image.Image, *, margin: int, dark_thr: int = 195, max_grains: int = 3
) -> List[Image.Image]:
    """Tight-crop significant grain blobs; empty list means caller should keep panel."""
    mask = _foreground_mask(panel, dark_thr)
    panel_area = panel.size[0] * panel.size[1]
    min_area = max(600, int(panel_area * 0.015))
    comps = connected_components(mask, min_area=min_area)

    good: List[dict] = []
    for c in comps:
        if c["aspect"] > 5.5 or c["aspect"] < (1.0 / 5.5):
            continue
        if c["w"] < 24 or c["h"] < 24:
            continue
        if c["fill"] < 0.28:
            continue
        # Reject only near-total panel fills (failed separation into grains).
        if c["area"] > panel_area * 0.96:
            continue
        circ = (4.0 * math.pi * c["area"]) / max(1.0, (c["w"] + c["h"]) ** 2)
        if circ < 0.12:
            continue
        good.append(c)

    if not good:
        return []

    good.sort(key=lambda c: -c["area"])
    # Optional split of a single wide dual-grain blob.
    if len(good) == 1:
        split = _try_split_wide_blob(panel, good[0]["bbox"], mask)
        if split:
            good = [
                {
                    "bbox": box,
                    "area": (box[2] - box[0]) * (box[3] - box[1]),
                    "w": box[2] - box[0],
                    "h": box[3] - box[1],
                }
                for box in split
            ]

    largest = good[0]["area"]
    good = [c for c in good if c["area"] >= largest * 0.22][:max_grains]

    crops: List[Image.Image] = []
    pw, ph = panel.size
    for c in good:
        x0, y0, x1, y1 = c["bbox"]
        # Re-tighten each split half to the actual mask content.
        mpx = mask.load()
        minx, miny, maxx, maxy = x1, y1, x0, y0
        found = False
        for y in range(max(0, y0), min(ph, y1)):
            for x in range(max(0, x0), min(pw, x1)):
                if mpx[x, y]:
                    found = True
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        if found:
            x0, y0, x1, y1 = minx, miny, maxx + 1, maxy + 1
        x0 = max(0, x0 - margin)
        y0 = max(0, y0 - margin)
        x1 = min(pw, x1 + margin)
        y1 = min(ph, y1 + margin)
        crops.append(panel.crop((x0, y0, x1, y1)))
    return crops


def max_existing_index(folder: Path, slug: str) -> int:
    if not folder.is_dir():
        return 0
    pat = re.compile(rf"^{re.escape(slug)}_(\d+)\.png$", re.IGNORECASE)
    hi = 0
    for p in folder.iterdir():
        if not p.is_file():
            continue
        m = pat.match(p.name)
        if m:
            hi = max(hi, int(m.group(1)))
    return hi


def save_crops(
    crops: Sequence[Image.Image],
    *,
    slug: str,
    out_root: Path,
    counters: Dict[str, int],
    dry_run: bool,
) -> List[Path]:
    folder = out_root / slug
    if slug not in counters:
        counters[slug] = max_existing_index(folder, slug)
    written: List[Path] = []
    for crop in crops:
        counters[slug] += 1
        dest = folder / f"{slug}_{counters[slug]}.png"
        written.append(dest)
        if dry_run:
            continue
        folder.mkdir(parents=True, exist_ok=True)
        crop.save(dest, format="PNG")
    return written


def process_plate(
    doc: pymupdf.Document,
    plate_num: int,
    taxa: Sequence[TaxonPanel],
    *,
    out_root: Path,
    counters: Dict[str, int],
    margin: int,
    dpi: int,
    dry_run: bool,
    prefer_render: bool,
) -> Tuple[int, List[str]]:
    page_index = plate_num + PLATE_PAGE_OFFSET
    if page_index < 0 or page_index >= doc.page_count:
        return 0, [f"plate {plate_num}: page_index {page_index} out of range"]

    letters = [t.plate_letter for t in taxa]
    n = len(taxa)
    errors: List[str] = []

    try:
        if prefer_render:
            plate_img = render_page_image(doc, page_index, dpi)
            source = f"render@{dpi}dpi"
        else:
            try:
                plate_img = extract_largest_page_image(doc, page_index)
                source = "embedded"
            except RuntimeError:
                plate_img = render_page_image(doc, page_index, dpi)
                source = f"render@{dpi}dpi(fallback)"
    except Exception as exc:  # noqa: BLE001 - report and continue other plates
        return 0, [f"plate {plate_num}: failed to load image: {exc}"]

    panels, seg_note = segment_panels(plate_img, n)
    if len(panels) != n:
        errors.append(
            f"plate {plate_num}: panel count {len(panels)} != letters {n}; using first {min(len(panels), n)}"
        )

    print(
        f"Plate {plate_num}: page_index={page_index} source={source} "
        f"size={plate_img.size[0]}x{plate_img.size[1]} panels={len(panels)} via {seg_note}"
    )

    created = 0
    rows_out: List[str] = []
    for i, taxon in enumerate(taxa):
        if i >= len(panels):
            errors.append(f"plate {plate_num}{taxon.plate_letter}: no panel")
            rows_out.append(f"  {taxon.plate_letter} {taxon.pollen_key}: FAIL (no panel)")
            continue
        x0, y0, x1, y1 = panels[i]
        panel = plate_img.crop((x0, y0, x1, y1))
        crops = find_grain_crops(panel, margin=margin)
        used_fallback = False
        if not crops:
            crops = [panel]
            used_fallback = True
        paths = save_crops(
            crops,
            slug=taxon.pollen_key,
            out_root=out_root,
            counters=counters,
            dry_run=dry_run,
        )
        created += len(paths)
        flag = " [panel-fallback]" if used_fallback else ""
        path_s = ", ".join(str(p.relative_to(REPO)) for p in paths)
        rows_out.append(
            f"  {taxon.plate_letter} {taxon.latin_name} -> {taxon.pollen_key}: "
            f"{len(paths)} image(s){flag}\n    {path_s}"
        )
    return created, errors + rows_out


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Crop Delport 2025 plate panels into by-taxon pollen PNGs."
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--plate", type=int, action="append", help="Plate number (repeatable)")
    g.add_argument("--all", action="store_true", help="Process every plate in the taxa index")
    p.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="Path to Delport main PDF")
    p.add_argument("--index", type=Path, default=DEFAULT_INDEX, help="taxa-index.json path")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="by-taxon output root")
    p.add_argument("--margin", type=int, default=16, help="Padding around each grain blob (px)")
    p.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI when rendering a page (fallback if no embedded image, or with --render)",
    )
    p.add_argument(
        "--render",
        action="store_true",
        help="Force full-page render at --dpi instead of extracting the embedded image",
    )
    p.add_argument("--dry-run", action="store_true", help="Segment and plan paths only; write nothing")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if not args.pdf.is_file():
        print(f"ERROR: PDF not found: {args.pdf}", file=sys.stderr)
        return 1
    if not args.index.is_file():
        print(f"ERROR: taxa index not found: {args.index}", file=sys.stderr)
        return 1

    by_plate = load_taxa_by_plate(args.index)
    if args.all:
        plate_nums = sorted(by_plate)
    else:
        plate_nums = list(args.plate or [])

    missing = [n for n in plate_nums if n not in by_plate]
    if missing:
        print(f"ERROR: plates not in index: {missing}", file=sys.stderr)
        return 1

    doc = pymupdf.open(args.pdf)
    counters: Dict[str, int] = {}
    total = 0
    all_lines: List[str] = []

    for plate_num in plate_nums:
        n_created, lines = process_plate(
            doc,
            plate_num,
            by_plate[plate_num],
            out_root=args.out,
            counters=counters,
            margin=args.margin,
            dpi=args.dpi,
            dry_run=args.dry_run,
            prefer_render=args.render,
        )
        total += n_created
        all_lines.extend(lines)
        print("\n".join(lines))
        print()

    mode = "dry-run planned" if args.dry_run else "wrote"
    print(f"Summary: {mode} {total} image(s) across plate(s) {plate_nums}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
