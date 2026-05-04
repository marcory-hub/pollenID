/**
 * Pollentabel (van der Ham): wizard + platte tabel uit vanderham-pollentabel.json.
 * Werkt met MkDocs Material instant navigation wanneer document$ beschikbaar is.
 * data-json-url: relatief pad; wordt opgelost met document.baseURI (directory URLs + instant nav).
 * Eindpunttekst: *cursief* + Markdown-links [label](https://…) alleen voor http(s); regelwit in JSON (\n) → <br />.
 */
(function () {
  "use strict";

  const ROOT_KEY = "vdh-pollentabel-root";
  const ROOT_TABLE = "vdh-pollentabel-table-root";

  /** @type {Map<string, Promise<unknown>>} */
  const jsonCache = new Map();

  function esc(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function escAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  /** Relatieve data-json-url → absolute URL voor fetch (zelfde regels als browser voor <a href>). */
  function resolveDataJsonUrl(url) {
    if (typeof url !== "string" || !url) return url;
    try {
      return new URL(url, document.baseURI).href;
    } catch (e) {
      return url;
    }
  }

  /**
   * JSON-labels en eindpunten gebruiken *cursief* zoals in het boek; geen volledige Markdown.
   * Paren asterisken worden <em>; overige tekst ge-escaped.
   */
  function formatEmphasisAst(s) {
    if (typeof s !== "string" || !s) return "";
    const chunks = [];
    let i = 0;
    while (i < s.length) {
      const open = s.indexOf("*", i);
      if (open === -1) {
        chunks.push(esc(s.slice(i)));
        break;
      }
      chunks.push(esc(s.slice(i, open)));
      const close = s.indexOf("*", open + 1);
      if (close === -1) {
        chunks.push(esc(s.slice(open)));
        break;
      }
      chunks.push("<em>" + esc(s.slice(open + 1, close)) + "</em>");
      i = close + 1;
    }
    return chunks.join("");
  }

  /** Markdown-achtige links [label](url): alleen http(s), extern tabblad. */
  const OUTCOME_LINK_RE = /\[([^\]]*)\]\(([^)]+)\)/g;

  /** Verwijdert dubbele weergave als bron `Taxon[Taxon](url)` heeft (zelfde label vóór de link). */
  function stripRedundantLabelBeforeMarkdownLink(s) {
    const m = /^([^[\]]*?)\[([^\]]*)\]\(/.exec(s);
    if (!m) return s;
    const before = m[1];
    const label = m[2];
    if (before.trimEnd() === label) {
      return s.slice(before.length);
    }
    return s;
  }

  function formatOutcomeRichText(s) {
    if (typeof s !== "string" || !s) return "";
    s = stripRedundantLabelBeforeMarkdownLink(s);
    let out = "";
    let last = 0;
    let m;
    OUTCOME_LINK_RE.lastIndex = 0;
    while ((m = OUTCOME_LINK_RE.exec(s)) !== null) {
      out += formatEmphasisAst(s.slice(last, m.index));
      const href = m[2].trim();
      if (/^https?:\/\//i.test(href)) {
        out +=
          '<a href="' +
          escAttr(href) +
          '" class="vdh-pollentabel-outcome-link" rel="noopener noreferrer" target="_blank">' +
          formatEmphasisAst(m[1]) +
          "</a>";
      } else {
        out += esc(m[0]);
      }
      last = OUTCOME_LINK_RE.lastIndex;
    }
    out += formatEmphasisAst(s.slice(last));
    return out.replace(/\n/g, "<br />");
  }

  function isMissingValue(v) {
    return v == null || String(v).trim() === "" || String(v).trim() === "-";
  }

  function fetchJsonCached(url) {
    var abs = resolveDataJsonUrl(url);
    if (!jsonCache.has(abs)) {
      jsonCache.set(
        abs,
        fetch(abs, { credentials: "same-origin" }).then(function (r) {
          if (!r.ok) throw new Error(r.status + " " + r.statusText);
          return r.json();
        })
      );
    }
    return jsonCache.get(abs);
  }

  /**
   * Pollen SoT index, produced by scripts/export_pollen_json.py from data/pollen.yaml.
   * Loaded at runtime so endpoints that carry a `pollen_key` can render latin/dutch/
   * size/images without duplicating those strings in key JSON files.
   */
  let pollenIndexPromise = null;
  let docsRootUrl = null;

  function computePollenIndexUrl(keyAbsUrl) {
    try {
      const u = new URL(keyAbsUrl, document.baseURI);
      if (/\/keys\//.test(u.pathname)) {
        u.pathname = u.pathname.replace(/\/keys\/.*$/, "/data/pollen.json");
      } else {
        u.pathname = u.pathname.replace(/\/[^/]*$/, "/data/pollen.json");
      }
      u.search = "";
      u.hash = "";
      return u.href;
    } catch (e) {
      return null;
    }
  }

  function fetchPollenIndex(fromAbsUrl) {
    if (pollenIndexPromise) return pollenIndexPromise;
    const url = computePollenIndexUrl(fromAbsUrl);
    if (!url) {
      pollenIndexPromise = Promise.resolve({});
      return pollenIndexPromise;
    }
    try {
      // pollen.json lives at `<site-prefix>/data/pollen.json`; one "../" yields the MkDocs site root
      // (e.g. /pollenID/). "../../" wrongly strips subdirectory deploys like GitHub Pages.
      docsRootUrl = new URL("../", url).href;
    } catch (e) {
      docsRootUrl = null;
    }
    pollenIndexPromise = fetch(url, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status + " " + r.statusText);
        return r.json();
      })
      .catch(function () {
        return {};
      });
    return pollenIndexPromise;
  }

  function formatSizeFromIndex(size) {
    if (!size || typeof size !== "object") return null;
    const s = size.smallest_size != null ? String(size.smallest_size).trim() : "";
    const l = size.largest_size != null ? String(size.largest_size).trim() : "";
    if (!s && !l) return null;
    const strip = function (v) { return v.replace(/\s*µm$/i, "").trim(); };
    if (s && l) {
      const su = strip(s);
      const lu = strip(l);
      if (su === lu) return su + " µm";
      return su + "-" + lu + " µm";
    }
    return s || l;
  }

  /** Parse a free-form size string (µm) and return the largest numeric token (matches Kerkvliet parseMaxUm). */
  function parseMaxUm(sizeRaw) {
    if (typeof sizeRaw !== "string") return null;
    const s = String(sizeRaw)
      .replace(/,/g, ".")
      .replace(/[^\d.x\-\(\)\/ ]+/g, " ")
      .trim();
    if (!s) return null;
    const nums = s.match(/\d+(?:\.\d+)?/g);
    if (!nums || nums.length === 0) return null;
    let max = null;
    nums.forEach(function (n) {
      const v = parseFloat(n);
      if (!Number.isFinite(v)) return;
      if (max === null || v > max) max = v;
    });
    return max;
  }

  /** Display width in px: round(max_um * 2.5); default 50 µm => 125 px. */
  function widthPxFromSizeMax(size) {
    if (!size || typeof size !== "object") return null;
    const raw = (String(size.smallest_size || "").trim() + " " + String(size.largest_size || "").trim()).trim();
    if (!raw) return null;
    const maxUm = parseMaxUm(raw);
    if (maxUm == null || maxUm <= 0) return null;
    return Math.round(2.5 * maxUm);
  }

  const FALLBACK_DISPLAY_WIDTH_PX = 125;

  /** Eén visuele rij thumbnails in interactieve sleutels; voorkomt mix van 128 px + 250 px op dezelfde keuze. */
  const POLLEN_THUMB_ROW_MAX_PX = 112;

  function parseCssHeightPx(styleHeight) {
    if (typeof styleHeight !== "string" || !styleHeight) return NaN;
    var m = /^(\d+(?:\.\d+)?)px\s*$/i.exec(styleHeight.trim());
    return m ? parseFloat(m[1]) : NaN;
  }

  /**
   * Schaal alle <img>-hoogtes in de rij met dezelfde factor zodat de grootste niet boven maxPx uitkomt.
   * Alle afbeeldingen op één tak (pollenwiki + placeholders) worden daarmee visueel vergelijkbaar.
   */
  function normalizePollenThumbnailRow(rowEl, maxPx) {
    if (!rowEl || !(maxPx > 0)) return;
    var imgs = rowEl.querySelectorAll("img");
    if (!imgs.length) return;
    var heights = [];
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      var h =
        typeof img.style.height === "string" && img.style.height
          ? parseCssHeightPx(img.style.height)
          : NaN;
      if (!(Number.isFinite(h) && h > 0)) {
        var oh = img.offsetHeight;
        h = oh > 0 ? oh : 24;
      }
      heights.push(h);
    }
    var mh = Math.max.apply(null, heights);
    if (!(mh > 0)) return;
    var factor = mh > maxPx ? maxPx / mh : 1;
    var minPx = 14;
    for (var j = 0; j < imgs.length; j++) {
      var nh = Math.max(minPx, Math.round(heights[j] * factor));
      imgs[j].style.height = String(nh) + "px";
      imgs[j].style.width = "auto";
    }
  }

  function tileWidthPxFromPollenJsonImage(im, entryFallbackPx) {
    if (typeof im.imageWidthPx === "number" && im.imageWidthPx > 0) return im.imageWidthPx;
    if (typeof im.width_px === "number" && im.width_px > 0) return im.width_px;
    if (typeof im.imageHeightPx === "number" && im.imageHeightPx > 0) return im.imageHeightPx;
    if (typeof im.height_px === "number" && im.height_px > 0) return im.height_px;
    if (typeof im.heightPx === "number" && im.heightPx > 0) return im.heightPx;
    return entryFallbackPx;
  }

  function displayWidthFromPollenEntry(entry) {
    if (entry && typeof entry.display_width_px === "number" && entry.display_width_px > 0) {
      return entry.display_width_px;
    }
    return widthPxFromSizeMax(entry && entry.size) || FALLBACK_DISPLAY_WIDTH_PX;
  }

  function imagesFromIndexEntry(entry) {
    if (!entry || !Array.isArray(entry.images)) return [];
    const wFb = displayWidthFromPollenEntry(entry);
    const out = [];
    entry.images.forEach(function (im) {
      if (im && typeof im.path === "string" && im.path) {
        // Pollen-index paths are anchored at the docs root (e.g. "assets/images/...").
        // Resolve them against docsRootUrl so they render correctly from any page.
        let src = im.path;
        if (docsRootUrl) {
          try { src = new URL(im.path, docsRootUrl).href; } catch (e) { /* keep raw */ }
        }
        const tileW = tileWidthPxFromPollenJsonImage(im, wFb);
        out.push({ image: src, imageWidthPx: tileW });
      }
    });
    return out;
  }

  /** Geldige `pollen_key` voor lookups; "-", leegstrings en null tellen niet. */
  function normalizePollenSlug(raw) {
    if (typeof raw !== "string") return "";
    const s = raw.trim();
    if (!s || s === "-") return "";
    return s;
  }

  function resolveEndpointFromIndex(endpoint, pollenIndex) {
    if (!endpoint || !pollenIndex) return null;
    const key = normalizePollenSlug(endpoint.pollen_key);
    if (!key) return null;
    const entry = pollenIndex[key];
    if (!entry) return null;
    var fromIndex = imagesFromIndexEntry(entry);
    /** Sleutels met alleen pollen_key gebruiken pollen.json; lokale overrides alleen bij gebrek aan afbeeldingen in index. */
    var images =
      fromIndex.length > 0
        ? fromIndex
        : Array.isArray(endpoint.images) && endpoint.images.length > 0
          ? endpoint.images
          : [];
    return {
      latin: entry.latin || null,
      dutch: entry.dutch || null,
      size: formatSizeFromIndex(entry.size),
      images: images,
      note: typeof endpoint.note === "string" && endpoint.note.trim() ? endpoint.note : null,
      links: entry.links && typeof entry.links === "object" ? entry.links : null,
    };
  }

  function renderEndpointTable(resolved) {
    const table = document.createElement("table");
    table.className = "vdh-pollentabel-outcome-table";
    const tbody = document.createElement("tbody");
    const rows = [];
    if (!isMissingValue(resolved.latin)) {
      rows.push(["Latijn", "<em>" + esc(String(resolved.latin)) + "</em>"]);
    }
    if (!isMissingValue(resolved.dutch)) {
      rows.push(["Nederlands", esc(String(resolved.dutch))]);
    }
    if (!isMissingValue(resolved.size)) {
      rows.push(["Grootte", esc(String(resolved.size))]);
    }
    rows.push(["Bron", "<code>pollen.yaml</code>"]);
    if (resolved.links && typeof resolved.links === "object") {
      const parts = [];
      if (resolved.links.pollenx) {
        parts.push(
          '<a rel="noopener" target="_blank" href="' +
            esc(String(resolved.links.pollenx)) +
            '">PollenX</a>'
        );
      }
      if (resolved.links.tstebler) {
        parts.push(
          '<a rel="noopener" target="_blank" href="' +
            esc(String(resolved.links.tstebler)) +
            '">Tstebler</a>'
        );
      }
      if (resolved.links.paldat) {
        parts.push(
          '<a rel="noopener" target="_blank" href="' +
            esc(String(resolved.links.paldat)) +
            '">PalDat</a>'
        );
      }
      if (parts.length) {
        rows.push(["Atlas", parts.join(" · ")]);
      }
    }
    if (!isMissingValue(resolved.note)) {
      rows.push(["Opmerking", formatOutcomeRichText(String(resolved.note))]);
    }
    rows.forEach(function (r) {
      const tr = document.createElement("tr");
      const th = document.createElement("th");
      th.scope = "row";
      th.textContent = r[0];
      const td = document.createElement("td");
      td.innerHTML = r[1];
      tr.appendChild(th);
      tr.appendChild(td);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function resolveAssetUrl(maybeRelative, baseUrl) {
    if (typeof maybeRelative !== "string" || !maybeRelative) return maybeRelative;
    if (/^[a-z]+:/i.test(maybeRelative) || maybeRelative.startsWith("/")) {
      return maybeRelative;
    }
    try {
      return new URL(maybeRelative, baseUrl).href;
    } catch (e) {
      return maybeRelative;
    }
  }

  function isPlaceholderImagePath(p) {
    if (typeof p !== "string") return false;
    if (/\/non-pollen\/placeholder\.png$/i.test(p)) return true;
    if (/\/non-pollen\/placeholder_/i.test(p)) return true;
    return /\/PLACEHOLDER_[A-Za-z]+\.png$/i.test(p);
  }

  function resolveNoImageFoundUrl(baseUrl) {
    // Always prefer the real docs root if we managed to compute it from pollen.json.
    if (docsRootUrl) {
      try {
        return new URL("assets/images/non-pollen/no_image_found.jpg", docsRootUrl).href;
      } catch (e) {
        // fall through
      }
    }
    // Otherwise resolve from the current key/page location.
    return resolveAssetUrl("../../assets/images/non-pollen/no_image_found.jpg", baseUrl || document.baseURI);
  }

  /**
   * Afbeeldingen voor interactieve keuzes (zelfde samenstelling als op de knoppen).
   * @param {object} ch
   * @param {Record<string, unknown>} pollenIndex
   * @returns {Array<{image?:string,imageHeightPx?:number,imageWidthPx?:number}>}
   */
  function gatherInteractiveChoiceImages(ch, pollenIndex) {
    pollenIndex = pollenIndex || {};
    var imgsFromChoice = [];
    if (Array.isArray(ch.images) && ch.images.length > 0) {
      imgsFromChoice = ch.images.slice();
      if (
        typeof ch.image === "string" &&
        ch.image.trim() &&
        !imgsFromChoice.some(function (x) {
          return x && x.image === ch.image;
        })
      ) {
        imgsFromChoice.unshift({
          image: ch.image,
          imageHeightPx: ch.imageHeightPx,
          imageWidthPx: ch.imageWidthPx,
        });
      }
    } else if (typeof ch.image === "string" && ch.image.trim()) {
      imgsFromChoice = [
        {
          image: ch.image,
          imageHeightPx: ch.imageHeightPx,
          imageWidthPx: ch.imageWidthPx,
        },
      ];
    }
    const endpoint = ch && ch.id ? ch.id : ch && ch.outcome ? ch.outcome : null;
    var imgsFromEndpoint = [];
    var pollenSlug = endpoint ? normalizePollenSlug(endpoint.pollen_key) : "";
    if (pollenSlug && pollenIndex[pollenSlug]) {
      imgsFromEndpoint = imagesFromIndexEntry(pollenIndex[pollenSlug]);
    }
    if (
      (!imgsFromEndpoint || imgsFromEndpoint.length === 0) &&
      endpoint &&
      Array.isArray(endpoint.images) &&
      endpoint.images.length > 0
    ) {
      imgsFromEndpoint = endpoint.images;
    }
    const imgs = imgsFromChoice.concat(imgsFromEndpoint);
    if (imgs.length > 0) return imgs;
    if (isPlaceholderImagePath(ch.image)) {
      return [{ image: ch.image, imageHeightPx: ch.imageHeightPx, imageWidthPx: ch.imageWidthPx }];
    }
    if (endpoint && isPlaceholderImagePath(endpoint.image)) {
      return [
        {
          image: endpoint.image,
          imageHeightPx: endpoint.imageHeightPx,
          imageWidthPx: endpoint.imageWidthPx,
        },
      ];
    }
    return [];
  }

  /** Voor placeholdertegels: doelstap bij `next`, anders leeg (eindpunt). */
  function choicePlaceholderHint(ch) {
    if (ch && ch.next) return String(ch.next);
    return "";
  }

  function applyImageSizing(img, heightPx, widthPx, isPlaceholder) {
    img.style.display = "block";
    img.style.height = "auto";
    img.style.margin = "0";

    if (typeof heightPx === "number" && Number.isFinite(heightPx) && heightPx > 0) {
      if (isPlaceholder && heightPx <= 1) {
        img.style.height = "20px";
        img.style.width = "auto";
        img.classList.add("pid-placeholder-image");
      } else {
        img.style.height = String(heightPx) + "px";
        img.style.width = "auto";
      }
      return;
    }

    if (typeof widthPx === "number" && Number.isFinite(widthPx) && widthPx > 0) {
      if (isPlaceholder && widthPx <= 1) {
        img.style.width = "20px";
        img.classList.add("pid-placeholder-image");
      } else {
        img.style.width = String(widthPx) + "px";
      }
      return;
    }

    img.style.maxWidth = isPlaceholder ? "20px" : "320px";
    if (isPlaceholder) img.classList.add("pid-placeholder-image");
  }

  /**
   * @param {HTMLElement} flexRow moet flex + nowrap gebruiken
   * @param {{ placeholderBranchHint?: string }} [renderOpts]
   */
  function appendImageTilesToFlexRow(flexRow, images, baseUrl, altPrefix, renderOpts) {
    renderOpts = renderOpts || {};
    var branchHint = renderOpts.placeholderBranchHint || "";
    if (!Array.isArray(images)) return;
    images.forEach(function (im, imIdx) {
      if (!im || !im.image) return;
      const img = document.createElement("img");
      img.alt = "";
      img.title = (altPrefix || "Afbeelding") + " (" + (imIdx + 1) + ")";
      const ph = isPlaceholderImagePath(im.image);
      if (ph && branchHint) img.title += " —→ stap " + branchHint;
      img.src = ph
        ? resolveNoImageFoundUrl(baseUrl || document.baseURI)
        : resolveAssetUrl(im.image, baseUrl || document.baseURI);
      applyImageSizing(img, im.imageHeightPx, im.imageWidthPx, ph);

      if (ph && branchHint) {
        const cell = document.createElement("span");
        cell.className = "vdh-pollentabel-img-with-hint";
        cell.appendChild(img);
        const hintEl = document.createElement("span");
        hintEl.className = "vdh-pollentabel-ph-hint";
        hintEl.textContent = branchHint;
        cell.appendChild(hintEl);
        flexRow.appendChild(cell);
      } else {
        flexRow.appendChild(img);
      }
    });
  }

  /**
   * @param {{ placeholderBranchHint?: string, compactRow?: boolean, skipThumbnailNormalize?: boolean, thumbnailRowMaxPx?: number }} [renderOpts]
   */
  function renderImagesRow(container, images, baseUrl, altPrefix, renderOpts) {
    renderOpts = renderOpts || {};
    if (!Array.isArray(images) || images.length === 0) return;
    const row = document.createElement("div");
    row.className = "vdh-pollentabel-images-row";
    row.style.display = "flex";
    row.style.flexWrap = "nowrap";
    row.style.gap = "6px";
    row.style.alignItems = "flex-start";
    if (!renderOpts.compactRow) {
      row.style.marginTop = "8px";
    }
    row.style.overflowX = "auto";
    appendImageTilesToFlexRow(row, images, baseUrl, altPrefix, renderOpts);
    if (!renderOpts.skipThumbnailNormalize) {
      var cap =
        typeof renderOpts.thumbnailRowMaxPx === "number" && renderOpts.thumbnailRowMaxPx > 0
          ? renderOpts.thumbnailRowMaxPx
          : POLLEN_THUMB_ROW_MAX_PX;
      normalizePollenThumbnailRow(row, cap);
    }
    container.appendChild(row);
  }

  /** Voor elke stap met een `next`-inkomend: id van de vorige stap (eerste binding wint). */
  function computeIncomingParentStepIds(steps) {
    /** @type {Record<string, string>} */
    var incoming = {};
    var ids = Object.keys(steps).sort(function (a, b) {
      return parseInt(a, 10) - parseInt(b, 10);
    });
    ids.forEach(function (sid) {
      var step = steps[sid];
      (step.choices || []).forEach(function (ch) {
        if (ch.next) {
          var t = String(ch.next);
          if (!incoming[t]) incoming[t] = String(sid);
        }
      });
    });
    return incoming;
  }

  /** Platte tabel: alle afbeeldingen van opties op het vorige keuzespunt in één rij + horizontale scroll. */
  function renderTablePreviousForkStrip(hostEl, forkStepId, steps, pollenIndex, baseUrl) {
    if (!forkStepId || !steps[forkStepId]) return;
    var forkStep = steps[forkStepId];
    if (!forkStep.choices || forkStep.choices.length === 0) return;

    var wrap = document.createElement("div");
    wrap.className = "vdh-pollentabel-table-fork";
    var cap = document.createElement("div");
    cap.className = "vdh-pollentabel-table-fork-caption";
    cap.textContent = "Splitsing bij stap " + String(forkStepId);
    wrap.appendChild(cap);

    var sc = document.createElement("div");
    sc.className = "vdh-pollentabel-table-fork-scroll";
    var strip = document.createElement("div");
    strip.className = "vdh-pollentabel-table-fork-strip";

    forkStep.choices.forEach(function (ch, idx) {
      if (idx > 0) {
        var sep = document.createElement("span");
        sep.className = "vdh-pollentabel-table-fork-sep";
        sep.setAttribute("aria-hidden", "true");
        strip.appendChild(sep);
      }
      var imgs = gatherInteractiveChoiceImages(ch, pollenIndex);
      var hint = choicePlaceholderHint(ch);
      var altP =
        (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") +
        " (stap " +
        String(forkStepId) +
        ", afbeelding)";
      if (imgs.length === 0) {
        var emp = document.createElement("span");
        emp.className = "vdh-pollentabel-table-fork-empty";
        emp.textContent = "(geen afbeelding)";
        strip.appendChild(emp);
      } else {
        var chunk = document.createElement("div");
        chunk.className = "vdh-pollentabel-table-fork-choice-chunk";
        renderImagesRow(chunk, imgs, baseUrl || document.baseURI, altP, {
          placeholderBranchHint: hint,
          compactRow: true,
        });
        strip.appendChild(chunk);
      }
    });

    sc.appendChild(strip);
    wrap.appendChild(sc);
    hostEl.appendChild(wrap);
  }

  /** Toont alle keuze-afbeeldingen van het vorige keuzespunt (boven huidige stap / eindpunt). */
  function appendPreviousForkReminder(hostEl, forkStepId, steps, pollenIndex, baseUrl) {
    var forkStep = steps[forkStepId];
    if (!forkStep || !Array.isArray(forkStep.choices) || forkStep.choices.length === 0) return;

    var box = document.createElement("div");
    box.className = "vdh-pollentabel-prev-fork";
    var h = document.createElement("h5");
    h.textContent = "Voorgaande splitsing (stap " + String(forkStepId) + ")";
    box.appendChild(h);

    var groups = document.createElement("div");
    groups.className = "vdh-pollentabel-prev-fork-groups";

    forkStep.choices.forEach(function (ch, idx) {
      var grp = document.createElement("div");
      grp.className = "vdh-pollentabel-prev-fork-group";
      var cap = document.createElement("div");
      cap.className = "vdh-pollentabel-prev-fork-label";
      cap.innerHTML = formatEmphasisAst(String(ch.label || "Optie " + (idx + 1)));
      grp.appendChild(cap);

      var imgs = gatherInteractiveChoiceImages(ch, pollenIndex);
      var hint = choicePlaceholderHint(ch);
      if (imgs.length === 0) {
        var empty = document.createElement("p");
        empty.className = "vdh-pollentabel-prev-fork-empty";
        empty.textContent = "(Geen afbeelding)";
        grp.appendChild(empty);
      } else {
        renderImagesRow(
          grp,
          imgs,
          baseUrl,
          (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") + " (afbeelding)",
          { placeholderBranchHint: hint }
        );
      }
      groups.appendChild(grp);
    });

    box.appendChild(groups);
    hostEl.appendChild(box);
  }

  function runKey(root, data, dataAbsUrl, pollenIndex) {
    const start = data.start || (data.meta && data.meta.start) || "1";
    const steps = data.steps || {};
    pollenIndex = pollenIndex || {};
    const stack = [];
    let currentStepId = String(start);

    const wrap = document.createElement("div");
    wrap.className = "vdh-pollentabel md-typeset";

    const stepEl = document.createElement("div");
    stepEl.className = "vdh-pollentabel-step";
    const actionsEl = document.createElement("div");
    actionsEl.className = "vdh-pollentabel-actions";
    const outcomeEl = document.createElement("div");
    outcomeEl.className = "vdh-pollentabel-outcome";
    outcomeEl.hidden = true;

    wrap.appendChild(stepEl);
    wrap.appendChild(actionsEl);
    wrap.appendChild(outcomeEl);
    root.appendChild(wrap);

    function emit(type, detail) {
      try {
        root.dispatchEvent(
          new CustomEvent(type, {
            detail: detail || {},
            bubbles: true,
          })
        );
      } catch (e) {
        // ignore
      }
    }

    function showStep(id) {
      currentStepId = String(id);
      outcomeEl.hidden = true;
      outcomeEl.replaceChildren();
      actionsEl.replaceChildren();

      const step = steps[id];
      if (!step) {
        stepEl.innerHTML =
          "<p><strong>Onbekende stap:</strong> " + esc(String(id)) + "</p>";
        return;
      }

      stepEl.innerHTML = "<h4>Stap " + esc(String(id)) + "</h4>";
      emit("pid:vdh-step", { stepId: String(id) });

      if (stack.length > 0) {
        var forkFrom = stack[stack.length - 1];
        appendPreviousForkReminder(stepEl, forkFrom, steps, pollenIndex, dataAbsUrl || document.baseURI);
      }

      const choices = step.choices || [];
      if (choices.length === 0) {
        const emptyP = document.createElement("p");
        emptyP.textContent = "Geen keuzes gedefinieerd.";
        stepEl.appendChild(emptyP);
        return;
      }

      choices.forEach(function (ch, idx) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "vdh-pollentabel-btn vdh-pollentabel-btn--choice";
        const labelSpan = document.createElement("span");
        const labelText = ch.label || "Optie " + (idx + 1);
        labelSpan.innerHTML = formatEmphasisAst(labelText);
        btn.appendChild(labelSpan);
        const imgs = gatherInteractiveChoiceImages(ch, pollenIndex);
        const phHint = choicePlaceholderHint(ch);
        if (imgs.length > 0) {
          renderImagesRow(
            btn,
            imgs,
            dataAbsUrl || document.baseURI,
            (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") + " (afbeelding)",
            { placeholderBranchHint: phHint }
          );
        }
        btn.addEventListener("click", function () {
          emit("pid:vdh-choice", {
            stepId: String(id),
            choiceIdx: idx,
            choiceLabel: ch && ch.label ? String(ch.label) : "",
            hasOutcome: !!(
              (ch && ch.outcome && ch.outcome.text) ||
              (ch && ch.id && (ch.id.name || ch.id.text || ch.id.pollen_key))
            ),
            next: ch && ch.next ? String(ch.next) : null,
          });
          var endpoint = ch && ch.id ? ch.id : ch && ch.outcome ? ch.outcome : null;
          if (endpoint && (endpoint.text || endpoint.name || endpoint.pollen_key)) {
            stack.push(id);
            outcomeEl.hidden = false;
            outcomeEl.replaceChildren();
            const h = document.createElement("h4");
            h.textContent = "Eindpunt";
            outcomeEl.appendChild(h);

            if (stack.length > 0) {
              var forkAt = stack[stack.length - 1];
              appendPreviousForkReminder(
                outcomeEl,
                forkAt,
                steps,
                pollenIndex,
                dataAbsUrl || document.baseURI
              );
            }

            const resolved = resolveEndpointFromIndex(endpoint, pollenIndex);
            let altLabel = "Eindpunt";
            let imgs = [];
            if (endpoint.text) {
              const p = document.createElement("p");
              p.innerHTML = formatOutcomeRichText(String(endpoint.text));
              outcomeEl.appendChild(p);
              altLabel = String(endpoint.text);
              imgs = Array.isArray(endpoint.images) ? endpoint.images : [];
            } else if (resolved) {
              outcomeEl.appendChild(renderEndpointTable(resolved));
              altLabel = resolved.latin || resolved.dutch || "Eindpunt";
              imgs = resolved.images || [];
            } else {
              const p = document.createElement("p");
              var lines = [];
              if (!isMissingValue(endpoint.name)) lines.push(formatEmphasisAst(String(endpoint.name)));
              if (!isMissingValue(endpoint.size)) lines.push(esc(String(endpoint.size)));
              if (!isMissingValue(endpoint.source)) lines.push(esc(String(endpoint.source)));
              p.innerHTML = lines.join("<br />");
              outcomeEl.appendChild(p);
              altLabel = String(endpoint.name || "Eindpunt");
              imgs = Array.isArray(endpoint.images) ? endpoint.images : [];
            }

            if (imgs.length > 0) {
              renderImagesRow(
                outcomeEl,
                imgs,
                dataAbsUrl || document.baseURI,
                altLabel
                  .replace(/\*([^*]*)\*/g, "$1")
                  .replace(/\n/g, " ")
                  .trim() + " (afbeelding)"
              );
            }
            actionsEl.replaceChildren();
            addOutcomeNavRow();
            emit("pid:vdh-outcome", {
              stepId: String(id),
              choiceIdx: idx,
              choiceLabel: ch && ch.label ? String(ch.label) : "",
              outcomeText: String(
                endpoint && endpoint.text
                  ? endpoint.text
                  : resolved && resolved.latin
                  ? resolved.latin
                  : endpoint && endpoint.name
                  ? endpoint.name
                  : ""
              ),
            });
            return;
          }
          if (ch.next) {
            stack.push(id);
            showStep(String(ch.next));
            return;
          }
          outcomeEl.hidden = false;
          outcomeEl.innerHTML =
            "<p><strong>Geen vervolg of eindpunt</strong> voor deze keuze.</p>";
          addResetRow();
        });
        actionsEl.appendChild(btn);
      });

      addNavRow();
    }

    function addNavRow() {
      const row = document.createElement("div");
      row.className = "vdh-pollentabel-nav";

      if (stack.length > 0) {
        const back = document.createElement("button");
        back.type = "button";
        back.className = "vdh-pollentabel-btn vdh-pollentabel-btn--nav";
        back.textContent = "Eén stap terug";
        back.addEventListener("click", function () {
          const prev = stack.pop();
          if (prev !== undefined) showStep(prev);
        });
        row.appendChild(back);
      }

      const reset = document.createElement("button");
      reset.type = "button";
      reset.className = "vdh-pollentabel-btn vdh-pollentabel-btn--nav";
      reset.textContent = "Opnieuw beginnen";
      reset.addEventListener("click", function () {
        stack.length = 0;
        showStep(start);
      });
      row.appendChild(reset);

      actionsEl.appendChild(row);
    }

    function addResetRow() {
      const row = document.createElement("div");
      row.className = "vdh-pollentabel-nav";
      const reset = document.createElement("button");
      reset.type = "button";
      reset.className = "vdh-pollentabel-btn vdh-pollentabel-btn--nav";
      reset.textContent = "Opnieuw beginnen";
      reset.addEventListener("click", function () {
        stack.length = 0;
        showStep(start);
      });
      row.appendChild(reset);
      actionsEl.appendChild(row);
    }

    /** Eén rij: terug + opnieuw na eindpunt */
    function addOutcomeNavRow() {
      const row = document.createElement("div");
      row.className = "vdh-pollentabel-nav";
      if (stack.length > 0) {
        const back = document.createElement("button");
        back.type = "button";
        back.className = "vdh-pollentabel-btn vdh-pollentabel-btn--nav";
        back.textContent = "Eén stap terug";
        back.addEventListener("click", function () {
          outcomeEl.hidden = true;
          outcomeEl.replaceChildren();
          const prev = stack.pop();
          if (prev !== undefined) showStep(prev);
        });
        row.appendChild(back);
      }
      const reset = document.createElement("button");
      reset.type = "button";
      reset.className = "vdh-pollentabel-btn vdh-pollentabel-btn--nav";
      reset.textContent = "Opnieuw beginnen";
      reset.addEventListener("click", function () {
        stack.length = 0;
        showStep(start);
      });
      row.appendChild(reset);
      actionsEl.appendChild(row);
    }

    showStep(String(start));

    return {
      start: String(start),
      getCurrentStepId: function () {
        return currentStepId;
      },
      reset: function () {
        stack.length = 0;
        showStep(String(start));
      },
      showStep: function (sid) {
        showStep(String(sid));
      },
      chooseByIndex: function (choiceIdx) {
        const idx = Number(choiceIdx);
        if (!Number.isFinite(idx)) return false;
        const buttons = actionsEl.querySelectorAll(".vdh-pollentabel-btn--choice");
        const btn = buttons && buttons[idx];
        if (btn && typeof btn.click === "function") {
          btn.click();
          return true;
        }
        return false;
      },
    };
  }

  function flattenSteps(data, pollenIndex) {
    const steps = data.steps || {};
    pollenIndex = pollenIndex || {};
    const ids = Object.keys(steps).sort(function (a, b) {
      return parseInt(a, 10) - parseInt(b, 10);
    });
    /** @type {Array<{sid:string,label:string,result:string,kind:string,images:Array<{image?:string,imageHeightPx?:number,imageWidthPx?:number}>}>} */
    const rows = [];
    ids.forEach(function (sid) {
      const step = steps[sid];
      (step.choices || []).forEach(function (ch) {
        let result = "";
        let kind = "";
        if (ch.next) {
          result = "→ stap " + String(ch.next);
          kind = "stap";
        } else if (ch.outcome && ch.outcome.text) {
          result = ch.outcome.text;
          kind = ch.outcome.incomplete ? "eindpunt (onvolledig)" : "eindpunt";
        } else if (ch.id && (ch.id.text || ch.id.name || ch.id.pollen_key)) {
          const resolvedRow = resolveEndpointFromIndex(ch.id, pollenIndex);
          if (ch.id.text) {
            result = ch.id.text;
          } else if (resolvedRow) {
            let txt = "";
            if (resolvedRow.latin) txt += "*" + resolvedRow.latin + "*";
            if (resolvedRow.dutch) txt += (txt ? " " : "") + "(" + resolvedRow.dutch + ")";
            if (resolvedRow.size) txt += (txt ? "\n" : "") + resolvedRow.size;
            if (resolvedRow.note) txt += (txt ? "\n" : "") + resolvedRow.note;
            result = txt || ch.id.pollen_key || "";
          } else {
            result = ch.id.name || "";
          }
          kind = ch.id.incomplete ? "eindpunt (onvolledig)" : "eindpunt";
        } else {
          result = "-";
          kind = "leeg";
        }
        let images = gatherInteractiveChoiceImages(ch, pollenIndex);
        var placeholderHint =
          typeof ch.next === "string" && String(ch.next).trim() !== "" ? String(ch.next) : "";
        rows.push({
          sid: sid,
          label: ch.label || "",
          result: result,
          kind: kind,
          images: images,
          placeholderHint: placeholderHint,
        });
      });
    });
    return rows;
  }

  function runTable(root, data, dataAbsUrl, pollenIndex) {
    const rows = flattenSteps(data, pollenIndex || {});
    const steps = data.steps || {};
    const incomingParent = computeIncomingParentStepIds(steps);
    const wrap = document.createElement("div");
    wrap.className = "vdh-pollentabel-table md-typeset";

    const toolbar = document.createElement("div");
    toolbar.className = "vdh-pollentabel-table-toolbar";

    const label = document.createElement("label");
    label.className = "vdh-pollentabel-table-filter-label";
    label.setAttribute("for", "vdh-pollentabel-filter");
    label.textContent = "Filter (stap, keuze, eindpunt)";

    const input = document.createElement("input");
    input.id = "vdh-pollentabel-filter";
    input.type = "search";
    input.className = "vdh-pollentabel-table-filter";
    input.setAttribute("autocomplete", "off");
    input.setAttribute("placeholder", "Typ om rijen te verbergen…");

    const count = document.createElement("p");
    count.className = "vdh-pollentabel-table-count";
    count.setAttribute("aria-live", "polite");

    toolbar.appendChild(label);
    toolbar.appendChild(input);
    toolbar.appendChild(count);

    const scroll = document.createElement("div");
    scroll.className = "vdh-pollentabel-table-scroll";

    const table = document.createElement("table");
    table.className = "vdh-pollentabel-table-grid";

    const thead = document.createElement("thead");
    const hr = document.createElement("tr");
    ["Stap", "Keuze", "Vervolg of eindpunt"].forEach(function (h) {
      const th = document.createElement("th");
      th.textContent = h;
      hr.appendChild(th);
    });
    thead.appendChild(hr);

    const tbody = document.createElement("tbody");

    rows.forEach(function (row) {
      const tr = document.createElement("tr");
      var forkParent = incomingParent[String(row.sid)] || "";
      var hayBits =
        row.sid + " " + row.label + " " + row.result + " " + row.kind + " " + forkParent;
      if (forkParent)
        hayBits += " splitsing bij stap " + forkParent + " splitsing stap " + forkParent;
      const hay = hayBits.toLowerCase().trim();
      tr.setAttribute("data-vdh-filter", hay);

      const tdS = document.createElement("td");
      tdS.textContent = row.sid;
      tdS.className = "vdh-pollentabel-td-step";

      const tdL = document.createElement("td");
      if (row.label.indexOf("*") !== -1) {
        tdL.innerHTML = formatEmphasisAst(row.label);
      } else {
        tdL.textContent = row.label;
      }

      const tdR = document.createElement("td");
      if (forkParent) {
        renderTablePreviousForkStrip(
          tdR,
          forkParent,
          steps,
          pollenIndex || {},
          dataAbsUrl || document.baseURI
        );
      }
      if (row.kind.indexOf("eindpunt") === 0) {
        const outP = document.createElement("div");
        outP.className = "vdh-pollentabel-table-td-result";
        outP.innerHTML = formatOutcomeRichText(row.result);
        tdR.appendChild(outP);
      } else {
        const outP = document.createElement("div");
        outP.className = "vdh-pollentabel-table-td-result";
        outP.textContent = row.result;
        tdR.appendChild(outP);
      }
      if (row.images && row.images.length > 0) {
        var rowPh =
          row.placeholderHint && row.placeholderHint.length
            ? { placeholderBranchHint: row.placeholderHint }
            : {};
        renderImagesRow(
          tdR,
          row.images,
          dataAbsUrl || document.baseURI,
          (row.kind.indexOf("eindpunt") === 0 ? row.result : row.label || row.result)
            .replace(/\*([^*]*)\*/g, "$1")
            .replace(/\n/g, " ")
            .trim() + " (afbeelding)",
          rowPh
        );
      }

      tr.appendChild(tdS);
      tr.appendChild(tdL);
      tr.appendChild(tdR);
      tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    scroll.appendChild(table);
    wrap.appendChild(toolbar);
    wrap.appendChild(scroll);
    root.appendChild(wrap);

    function applyFilter() {
      const q = input.value.trim().toLowerCase();
      let visible = 0;
      tbody.querySelectorAll("tr").forEach(function (tr) {
        const hay = tr.getAttribute("data-vdh-filter") || "";
        const show = !q || hay.indexOf(q) !== -1;
        tr.hidden = !show;
        if (show) visible += 1;
      });
      count.textContent =
        visible === rows.length
          ? rows.length + " rijen"
          : visible + " van " + rows.length + " rijen";
    }

    input.addEventListener("input", applyFilter);
    applyFilter();
  }

  function bootKey() {
    const root = document.getElementById(ROOT_KEY);
    if (!root) return;
    const jsonUrl = root.getAttribute("data-json-url");
    if (!jsonUrl) return;
    const dataAbsUrl = resolveDataJsonUrl(jsonUrl);

    root.replaceChildren();
    root.innerHTML =
      '<p class="vdh-pollentabel-status">' + esc("Laden…") + "</p>";

    Promise.all([fetchJsonCached(jsonUrl), fetchPollenIndex(dataAbsUrl)])
      .then(function (res) {
        const data = res[0];
        const pollenIndex = res[1] || {};
        root.replaceChildren();
        root.__vdhPollentabelController = runKey(root, data, dataAbsUrl, pollenIndex);
      })
      .catch(function (e) {
        root.innerHTML =
          '<p class="admonition error"><strong>Fout bij laden van de sleutel.</strong> ' +
          esc(String(e.message || e)) +
          "</p>";
      });
  }

  function bootTable() {
    const root = document.getElementById(ROOT_TABLE);
    if (!root) return;
    const jsonUrl = root.getAttribute("data-json-url");
    if (!jsonUrl) return;
    const dataAbsUrl = resolveDataJsonUrl(jsonUrl);

    root.replaceChildren();
    root.innerHTML =
      '<p class="vdh-pollentabel-status">' + esc("Tabel laden…") + "</p>";

    Promise.all([fetchJsonCached(jsonUrl), fetchPollenIndex(dataAbsUrl)])
      .then(function (res) {
        const data = res[0];
        const pollenIndex = res[1] || {};
        root.replaceChildren();
        runTable(root, data, dataAbsUrl, pollenIndex);
      })
      .catch(function (e) {
        root.innerHTML =
          '<p class="admonition error"><strong>Fout bij laden van de tabel.</strong> ' +
          esc(String(e.message || e)) +
          "</p>";
      });
  }

  function boot() {
    bootKey();
    bootTable();
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }

  if (typeof window !== "undefined") {
    window.PID_VDH_POLLENTABEL = window.PID_VDH_POLLENTABEL || {};
    window.PID_VDH_POLLENTABEL.boot = boot;
  }
})();
