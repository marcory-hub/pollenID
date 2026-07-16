/**
 * Determinatietabel (Kerkvliet): section dropdown + size-class filter + search.
 * Data source: docs/keys/kerkvliet/kerkvliet-determinatietabel.json
 *
 * Works with MkDocs Material instant navigation when document$ is available.
 */
(function () {
  "use strict";

  const ROOT_ID = "kerkvliet-determinatietabel-root";

  /** @type {Map<string, Promise<unknown>>} */
  const jsonCache = new Map();

  function esc(s) {
    const d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function fetchJsonCached(url) {
    if (!jsonCache.has(url)) {
      jsonCache.set(
        url,
        fetch(url, { credentials: "same-origin" }).then(function (r) {
          if (!r.ok) throw new Error(r.status + " " + r.statusText);
          return r.json();
        })
      );
    }
    return jsonCache.get(url);
  }

  function resolveDataJsonUrl(url) {
    if (typeof url !== "string" || !url) return url;
    try {
      return new URL(url, document.baseURI).href;
    } catch (e) {
      return url;
    }
  }

  /** @type {Promise<Record<string, unknown>>|null} */
  let kerkvlietPollenIndexPromise = null;

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

  function fetchPollenIndexForKerk(fromAbsUrl) {
    if (kerkvlietPollenIndexPromise) return kerkvlietPollenIndexPromise;
    const url = computePollenIndexUrl(fromAbsUrl);
    if (!url) {
      kerkvlietPollenIndexPromise = Promise.resolve({});
      return kerkvlietPollenIndexPromise;
    }
    kerkvlietPollenIndexPromise = fetch(url, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status + " " + r.statusText);
        return r.json();
      })
      .catch(function () {
        return {};
      });
    return kerkvlietPollenIndexPromise;
  }

  /**
   * Parse a free-form size string (µm) and return an estimated max dimension.
   * Examples handled: "7x5", "10-12,5", "20(-25)", "31 (34)", "ca. 30?", "92(80-104)", "35/28-32"
   */
  function parseMaxUm(sizeRaw) {
    if (typeof sizeRaw !== "string") return null;
    const s = sizeRaw
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

  function sizeClassFromMaxUm(maxUm) {
    if (maxUm == null) return "onbekend";
    // Bins as specified by the user (µm), based on max parsed dimension.
    // VerySmall < 15; Small 15–25; Medium 26–50; Large 51–100; VeryLarge > 100
    if (maxUm < 15) return "very-small";
    if (maxUm <= 25) return "small";
    if (maxUm <= 50) return "medium";
    if (maxUm <= 100) return "large";
    return "very-large";
  }

  function sizeClassLabel(id) {
    switch (id) {
      case "very-small":
        return "VerySmall (<15 µm)";
      case "small":
        return "Small (15–25 µm)";
      case "medium":
        return "Medium (26–50 µm)";
      case "large":
        return "Large (51–100 µm)";
      case "very-large":
        return "VeryLarge (>100 µm)";
      case "onbekend":
        return "Onbekend (niet parseerbaar)";
      default:
        return id;
    }
  }

  function normalizeSectionTitle(s) {
    if (typeof s !== "string") return "";
    let t = s
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim()
      .replace(/[:\s]+$/g, "");

    // Robust against subtitle variants like
    // "Enkele (sub)tropische pollen Alleen op grootte gesorteerd:".
    if (t.indexOf("enkele") === 0) {
      const m = t.match(/\bpollen\b/);
      if (m && typeof m.index === "number") t = t.slice(0, m.index + "pollen".length);
    }
    return t;
  }

  function boot() {
    const root = document.getElementById(ROOT_ID);
    if (!root) return;
    const jsonUrl = root.getAttribute("data-json-url");
    if (!jsonUrl) return;

    root.replaceChildren();
    root.innerHTML = '<p class="kerkvliet-status">' + esc("Tabel laden…") + "</p>";

    const dataAbsUrl = resolveDataJsonUrl(jsonUrl);
    Promise.all([fetchJsonCached(jsonUrl), fetchPollenIndexForKerk(dataAbsUrl)])
      .then(function (parts) {
        root.replaceChildren();
        run(root, parts[0], parts[1] || {});
      })
      .catch(function (e) {
        root.innerHTML =
          '<p class="admonition error"><strong>Fout bij laden van de tabel.</strong> ' +
          esc(String(e.message || e)) +
          "</p>";
      });
  }

  function normalizePollenKey(raw) {
    if (typeof raw !== "string") return "";
    const s = raw.trim();
    if (!s || s === "-") return "";
    return s;
  }

  function formatSizeFromPollen(size) {
    if (!size || typeof size !== "object") return "";
    const s = size.smallest_size != null ? String(size.smallest_size).trim() : "";
    const l = size.largest_size != null ? String(size.largest_size).trim() : "";
    if (!s && !l) return "";
    const strip = function (v) {
      return v.replace(/\s*µm$/i, "").trim();
    };
    if (s && l) {
      const su = strip(s);
      const lu = strip(l);
      if (su === lu) return su + " µm";
      return su + "-" + lu + " µm";
    }
    return s || l;
  }

  function displayWidthFromPollenEntry(entry) {
    if (entry && typeof entry.display_width_px === "number" && entry.display_width_px > 0) {
      return entry.display_width_px;
    }
    const sz = entry && entry.size;
    if (!sz || typeof sz !== "object") return 125;
    const raw = (String(sz.smallest_size || "").trim() + " " + String(sz.largest_size || "").trim()).trim();
    const m = parseMaxUm(raw);
    if (m == null || m <= 0) return 125;
    return Math.round(2.5 * m);
  }

  function pollenRowImagesFromIndex(entry) {
    if (!entry || !Array.isArray(entry.images)) return [];
    const out = [];
    const wFb = displayWidthFromPollenEntry(entry);
    entry.images.forEach(function (im) {
      if (!im || typeof im.path !== "string" || !im.path) return;
      var p = String(im.path).trim().replace(/^\.\.\/\.\.\/+/, "");
      if (p.indexOf("assets/") !== 0) return;
      var w =
        typeof im.width_px === "number" && im.width_px > 0
          ? im.width_px
          : typeof im.imageWidthPx === "number" && im.imageWidthPx > 0
            ? im.imageWidthPx
            : typeof im.height_px === "number" && im.height_px > 0
              ? im.height_px
              : typeof im.heightPx === "number" && im.heightPx > 0
                ? im.heightPx
                : wFb;
      out.push({ image: p, imageWidthPx: w });
    });
    return out;
  }

  /** @param {Record<string, unknown>} pollenIndex */
  function mergedPollenRowView(r, pollenIndex) {
    if (!r || !pollenIndex) return null;
    const pk = normalizePollenKey(r.pollen_key);
    if (!pk || !pollenIndex[pk]) return null;
    const e = /** @type {Record<string, unknown>} */ (pollenIndex[pk]);
    const oppervlak = e.ornamentation != null ? String(e.ornamentation).trim() : "";
    return {
      latin: e.latin != null ? String(e.latin) : "",
      dutch: e.dutch != null ? String(e.dutch) : "",
      vorm: e.shape != null ? String(e.shape) : "",
      grootte: formatSizeFromPollen(
        typeof e.size === "object" && e.size !== null ? /** @type {object} */ (e.size) : null
      ),
      oppervlak: oppervlak,
      opmerkingen: e.aperture != null ? String(e.aperture) : "",
      images: pollenRowImagesFromIndex(e),
      pollen_key: pk,
    };
  }

  /** @param {Record<string, unknown>} pollenIndex */
  function run(root, data, pollenIndex) {
    pollenIndex = pollenIndex || {};
    const sections = Array.isArray(data.sections) ? data.sections : [];
    const rows = Array.isArray(data.rows) ? data.rows : [];

    const wrap = document.createElement("div");
    wrap.className = "kerkvliet md-typeset";

    const toolbar = document.createElement("div");
    toolbar.className = "kerkvliet-toolbar";

    const toolbarRow1 = document.createElement("div");
    toolbarRow1.className = "kerkvliet-toolbar-row kerkvliet-toolbar-row--primary";

    const toolbarRow2 = document.createElement("div");
    toolbarRow2.className = "kerkvliet-toolbar-row kerkvliet-toolbar-row--secondary";

    // Section selector
    const sectionLabel = document.createElement("label");
    sectionLabel.className = "kerkvliet-label";
    sectionLabel.setAttribute("for", "kerkvliet-section");
    sectionLabel.textContent = "Tabel";

    const sectionSel = document.createElement("select");
    sectionSel.id = "kerkvliet-section";
    sectionSel.className = "kerkvliet-select";
    sections.forEach(function (t) {
      const opt = document.createElement("option");
      opt.value = t;
      opt.textContent = t;
      sectionSel.appendChild(opt);
    });

    // Size-class selector
    const sizeLabel = document.createElement("label");
    sizeLabel.className = "kerkvliet-label";
    sizeLabel.setAttribute("for", "kerkvliet-size");
    sizeLabel.textContent = "Grootteklasse";

    const sizeSel = document.createElement("select");
    sizeSel.id = "kerkvliet-size";
    sizeSel.className = "kerkvliet-select";
    [
      { id: "alle", label: "Alle" },
      { id: "very-small", label: sizeClassLabel("very-small") },
      { id: "small", label: sizeClassLabel("small") },
      { id: "medium", label: sizeClassLabel("medium") },
      { id: "large", label: sizeClassLabel("large") },
      { id: "very-large", label: sizeClassLabel("very-large") },
      { id: "onbekend", label: sizeClassLabel("onbekend") },
    ].forEach(function (x) {
      const opt = document.createElement("option");
      opt.value = x.id;
      opt.textContent = x.label;
      sizeSel.appendChild(opt);
    });

    // Search
    const qLabel = document.createElement("label");
    qLabel.className = "kerkvliet-label";
    qLabel.setAttribute("for", "kerkvliet-q");
    qLabel.textContent = "Zoeken";

    const q = document.createElement("input");
    q.id = "kerkvliet-q";
    q.type = "search";
    q.className = "kerkvliet-search";
    q.setAttribute("autocomplete", "off");
    q.setAttribute("placeholder", "Latijn, Nederlands, opmerkingen…");

    const count = document.createElement("p");
    count.className = "kerkvliet-count";
    count.setAttribute("aria-live", "polite");

    toolbarRow1.appendChild(sectionLabel);
    toolbarRow1.appendChild(sectionSel);

    toolbarRow2.appendChild(sizeLabel);
    toolbarRow2.appendChild(sizeSel);
    toolbarRow2.appendChild(qLabel);
    toolbarRow2.appendChild(q);
    toolbarRow2.appendChild(count);

    toolbar.appendChild(toolbarRow1);
    toolbar.appendChild(toolbarRow2);

    const scroll = document.createElement("div");
    scroll.className = "kerkvliet-scroll";

    const table = document.createElement("table");
    table.className = "kerkvliet-table";

    function escAttr(s) {
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;");
    }

    function resolveMdHref(relativeMd) {
      if (typeof relativeMd !== "string" || !relativeMd) return relativeMd;
      if (/^https?:\/\//i.test(relativeMd)) return relativeMd;
      return resolveSiteRelativeMarkdownHref(relativeMd);
    }

    /** Tab-separated tail aligned with Kerkvliet kolommen vorm / grootte / oppervlak / opmerkingen. */
    function morphTailTabsFromPollenEntry(ent) {
      if (!ent || typeof ent !== "object") return "\t\t\t\t";
      const vorm = ent.shape != null ? String(ent.shape).trim() : "";
      const grootte = formatSizeFromPollen(
        typeof ent.size === "object" && ent.size !== null ? /** @type {object} */ (ent.size) : null
      );
      const ornament = ent.ornamentation != null ? String(ent.ornamentation).trim() : "";
      const oppervlak = ornament;
      const opm = ent.aperture != null ? String(ent.aperture).trim() : "";
      return "\t" + vorm + "\t" + grootte + "\t" + oppervlak + "\t" + opm;
    }

    function primaryTaxonDocHrefFromPollenEntry(ent, pollenKey) {
      if (!pollenKey) return "";
      const mono =
        ent && typeof ent.monofloral_honey_page === "string"
          ? String(ent.monofloral_honey_page).trim()
          : "";
      const rel = mono
        ? mono.replace(/^\/*/, "")
        : "nederlandse-honing-pollen/" + pollenKey + ".md";
      return resolveSiteRelativeMarkdownHref(rel);
    }

    function latinHeadHtmlFromPollenEntry(ent, latinPlain, pollenKey) {
      if (!latinPlain) return "";
      const hrefRaw = primaryTaxonDocHrefFromPollenEntry(ent, pollenKey);
      const href = resolveMdHref(hrefRaw);
      const tail = morphTailTabsFromPollenEntry(ent || {});
      const link =
        '<a class="pid-pollen-latin-link" href="' +
        escAttr(href) +
        '"><strong>' +
        esc(String(latinPlain)) +
        "</strong></a>";
      return link + '<span class="pid-pollen-morph-tail">' + esc(tail) + "</span>";
    }

    /** MkDocs site root (…/pollenID/) for resolving docs-relative assets/… under GitHub Pages + instant nav. */
    function resolveDocsSiteRoot() {
      try {
        const sel =
          "header.md-header a.md-logo, header.md-header a.md-header__button.md-logo, nav.md-header__inner a.md-header__button.md-logo";
        const el = document.querySelector(sel);
        if (el && el.href) {
          const u = new URL(el.href, document.baseURI);
          let p = u.pathname.replace(/\/+$/, "");
          if (/\.(html?|php)$/i.test(p)) {
            p = p.replace(/\/[^/]+$/, "");
          }
          u.pathname = (p || "/") + "/";
          u.hash = "";
          u.search = "";
          return u.href;
        }
      } catch (e) {}
      try {
        return new URL("../../", document.baseURI).href;
      } catch (e2) {
        return document.baseURI;
      }
    }

    function resolveSiteRelativeMarkdownHref(hrefRaw) {
      if (typeof hrefRaw !== "string" || !hrefRaw) return hrefRaw;
      const h = hrefRaw.trim();
      if (/^https?:\/\//i.test(h)) return h;
      if (h.startsWith("/")) {
        try {
          return new URL(h, location.origin).href;
        } catch (e) {
          return h;
        }
      }
      let rel = h.replace(/^\.\/+/, "");
      while (rel.startsWith("../")) {
        rel = rel.slice(3);
      }
      if (/\.md$/i.test(rel)) {
        rel = rel.slice(0, -3);
      }
      if (rel && !rel.endsWith("/")) {
        rel += "/";
      }
      try {
        return new URL(rel, resolveDocsSiteRoot()).href;
      } catch (e) {
        try {
          return new URL(hrefRaw, document.baseURI).href;
        } catch (e2) {
          return hrefRaw;
        }
      }
    }

    function resolveAssetUrl(maybeRelative) {
      if (typeof maybeRelative !== "string" || !maybeRelative) return maybeRelative;
      const s = maybeRelative.trim();
      if (/^[a-z]+:/i.test(s) || s.startsWith("//")) return s;
      if (s.startsWith("/")) {
        try {
          return new URL(s, location.origin).href;
        } catch (e) {
          return s;
        }
      }
      const rel = s.replace(/^\.\.\/\.\.\/+/, "");
      if (rel.startsWith("assets/")) {
        try {
          return new URL(rel, resolveDocsSiteRoot()).href;
        } catch (e) {
          return new URL("../../" + rel, document.baseURI).href;
        }
      }
      try {
        return new URL(rel, document.baseURI).href;
      } catch (e) {
        return rel;
      }
    }

    /** Markdown-achtige links [label](url): alleen http(s), extern tabblad. */
    const MD_LINK_RE = /\[([^\]]*)\]\(([^)]+)\)/g;
    function formatMarkdownLinks(s) {
      if (typeof s !== "string" || !s) return "";
      let out = "";
      let last = 0;
      let m;
      MD_LINK_RE.lastIndex = 0;
      while ((m = MD_LINK_RE.exec(s)) !== null) {
        out += esc(s.slice(last, m.index));
        const href = (m[2] || "").trim();
        if (/^https?:\/\//i.test(href)) {
          out +=
            '<a href="' +
            escAttr(href) +
            '" rel="noopener noreferrer" target="_blank">' +
            esc(m[1] || "") +
            "</a>";
        } else if (/\.md$/i.test(href) || /^\.\.\//.test(href) || /^\.\//.test(href)) {
          try {
            const abs = resolveSiteRelativeMarkdownHref(href);
            out +=
              '<a href="' +
              escAttr(abs) +
              '" class="pid-pollen-latin-link">' +
              esc(m[1] || "") +
              "</a>";
          } catch (e2) {
            out += esc(m[0]);
          }
        } else {
          out += esc(m[0]);
        }
        last = MD_LINK_RE.lastIndex;
      }
      out += esc(s.slice(last));
      return out;
    }

    function renderImagesTd(td, images) {
      if (!Array.isArray(images) || images.length === 0) return;
      const row = document.createElement("div");
      row.style.display = "flex";
      row.style.flexWrap = "wrap";
      row.style.gap = "6px";
      row.style.alignItems = "flex-start";
      row.style.width = "100%";

      // Preserve relative size ratios while keeping the row compact.
      // Preferred: imageHeightPx (JSON uses heights). Backward-compatible: imageWidthPx.
      let maxH = null;
      let maxW = null;
      images.slice(0, 4).forEach(function (im) {
        const h = im && im.imageHeightPx;
        if (typeof h === "number" && Number.isFinite(h) && h > 0) {
          if (maxH === null || h > maxH) maxH = h;
        }
        const w = im && im.imageWidthPx;
        if (typeof w === "number" && Number.isFinite(w) && w > 0) {
          if (maxW === null || w > maxW) maxW = w;
        }
      });
      const targetMaxPx = 96;
      const scale = maxH
        ? Math.min(1, targetMaxPx / maxH)
        : maxW
          ? Math.min(1, targetMaxPx / maxW)
          : 1;
      images.slice(0, 4).forEach(function (im) {
        if (!im || !im.image) return;
        const img = document.createElement("img");
        img.src = resolveAssetUrl(im.image);
        img.alt = "";
        img.loading = "lazy";
        img.decoding = "async";
        img.addEventListener("error", function () {
          img.remove();
          if (row.childElementCount === 0) {
            const tr = td.closest("tr");
            if (tr) tr.remove();
          }
        });
        img.style.display = "block";
        img.style.height = "auto";
        img.style.borderRadius = "4px";
        const h = im.imageHeightPx;
        if (typeof h === "number" && Number.isFinite(h) && h > 0) {
          img.style.height = String(Math.max(18, Math.round(h * scale))) + "px";
          img.style.width = "auto";
        } else {
          const w = im.imageWidthPx;
          if (typeof w === "number" && Number.isFinite(w) && w > 0) {
            img.style.width = String(Math.max(28, Math.round(w * scale))) + "px";
          } else {
            img.style.width = "72px";
          }
        }
        row.appendChild(img);
      });
      td.appendChild(row);
    }

    const thead = document.createElement("thead");
    const hr = document.createElement("tr");
    ["Plant (Latijn) (pd)", "Plant (Nederlands) (pw)", "Vorm", "Grootte (µm)", "Oppervlak", "Opmerkingen"].forEach(
      function (h) {
        const th = document.createElement("th");
        th.textContent = h;
        hr.appendChild(th);
      }
    );
    thead.appendChild(hr);

    const tbody = document.createElement("tbody");
    table.appendChild(thead);
    table.appendChild(tbody);
    scroll.appendChild(table);

    wrap.appendChild(toolbar);
    wrap.appendChild(scroll);
    root.appendChild(wrap);

    function render() {
      const selectedSection = sectionSel.value;
      const selectedSize = sizeSel.value;
      const query = q.value.trim().toLowerCase();
      const selectedSectionKey = normalizeSectionTitle(selectedSection);

      tbody.replaceChildren();

      let totalInSection = 0;
      let shown = 0;

      rows.forEach(function (r) {
        if (!r) return;
        if (normalizeSectionTitle(r.section) !== selectedSectionKey) return;
        totalInSection += 1;

        const pv = mergedPollenRowView(r, pollenIndex);
        const grootteDisp = pv ? pv.grootte : String(r.grootte || "");

        const maxUm = parseMaxUm(grootteDisp || "");
        const cls = sizeClassFromMaxUm(maxUm);
        if (selectedSize !== "alle" && cls !== selectedSize) return;

        const latinHay = pv ? pv.latin : String(r.latin || "");
        const dutchHay = pv ? pv.dutch : String(r.dutch || "");
        const vormHay = pv ? pv.vorm : String(r.vorm || "");
        const grootteHay = pv ? pv.grootte : String(r.grootte || "");
        const oppHay = pv ? pv.oppervlak : String(r.oppervlak || "");
        const opmHay = pv ? pv.opmerkingen : String(r.opmerkingen || "");
        const pkResolved =
          pv && pv.pollen_key ? pv.pollen_key : normalizePollenKey(r.pollen_key);
        const entryFull =
          pkResolved && pollenIndex[pkResolved]
            ? /** @type {Record<string, unknown>} */ (pollenIndex[pkResolved])
            : null;
        const hay = (
          latinHay +
          " " +
          dutchHay +
          " " +
          vormHay +
          " " +
          grootteHay +
          " " +
          oppHay +
          " " +
          opmHay +
          " " +
          (pv && pv.pollen_key ? String(pv.pollen_key) : normalizePollenKey(r.pollen_key))
        )
          .toLowerCase()
          .trim();
        if (query && hay.indexOf(query) === -1) return;

        const rowImages =
          pv && Array.isArray(pv.images) && pv.images.length > 0
            ? pv.images
            : Array.isArray(r.images)
              ? r.images
              : [];
        // Optional full-width image row above the data row (thumbnails only; name stays in the data row).
        if (Array.isArray(rowImages) && rowImages.length > 0) {
          const trImg = document.createElement("tr");
          const tdImg = document.createElement("td");
          tdImg.colSpan = 6;
          renderImagesTd(tdImg, rowImages);
          trImg.appendChild(tdImg);
          tbody.appendChild(trImg);
        }

        const tr = document.createElement("tr");
        const cells = pv
          ? [pv.latin, pv.dutch, pv.vorm, pv.grootte, pv.oppervlak, pv.opmerkingen]
          : [
              r.latin || "",
              r.dutch || "",
              r.vorm || "",
              r.grootte || "",
              r.oppervlak || "",
              r.opmerkingen || "",
            ];
        cells.forEach(function (cell, idx) {
          const td = document.createElement("td");
          if (idx === 0 && latinHay && pkResolved) {
            td.innerHTML = latinHeadHtmlFromPollenEntry(entryFull, latinHay, pkResolved);
          } else if (idx === 0 || idx === 1) {
            td.innerHTML = formatMarkdownLinks(String(cell || "")).replace(/\s{2,}/g, " ").trim();
          } else {
            td.textContent = cell;
          }
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
        shown += 1;
      });

      count.textContent =
        shown === totalInSection
          ? shown + " rijen"
          : shown + " van " + totalInSection + " rijen";
    }

    // Default section: first in file.
    if (sections.length > 0) sectionSel.value = sections[0];
    render();

    sectionSel.addEventListener("change", render);
    sizeSel.addEventListener("change", render);
    q.addEventListener("input", render);
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();

