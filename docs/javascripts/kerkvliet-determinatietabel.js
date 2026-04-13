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

    fetchJsonCached(jsonUrl)
      .then(function (data) {
        root.replaceChildren();
        run(root, data);
      })
      .catch(function (e) {
        root.innerHTML =
          '<p class="admonition error"><strong>Fout bij laden van de tabel.</strong> ' +
          esc(String(e.message || e)) +
          "</p>";
      });
  }

  function run(root, data) {
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

    function resolveAssetUrl(maybeRelative) {
      if (typeof maybeRelative !== "string" || !maybeRelative) return maybeRelative;
      if (/^[a-z]+:/i.test(maybeRelative) || maybeRelative.startsWith("/")) return maybeRelative;
      // Rows use docs-relative paths like "assets/images/...".
      // This page lives under "Identificatiesleutels/", so prefix with "../../" to reach docs root.
      if (maybeRelative.startsWith("assets/")) {
        maybeRelative = "../../" + maybeRelative;
      }
      try {
        return new URL(maybeRelative, document.baseURI).href;
      } catch (e) {
        return maybeRelative;
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
      let maxW = null;
      images.slice(0, 4).forEach(function (im) {
        const w = im && im.imageWidthPx;
        if (typeof w === "number" && Number.isFinite(w) && w > 0) {
          if (maxW === null || w > maxW) maxW = w;
        }
      });
      const targetMaxPx = 96;
      const scale = maxW ? Math.min(1, targetMaxPx / maxW) : 1;
      images.slice(0, 4).forEach(function (im) {
        if (!im || !im.image) return;
        const img = document.createElement("img");
        img.src = resolveAssetUrl(im.image);
        img.alt = "Afbeelding";
        img.style.display = "block";
        img.style.height = "auto";
        img.style.borderRadius = "4px";
        const w = im.imageWidthPx;
        if (typeof w === "number" && Number.isFinite(w) && w > 0) {
          img.style.width = String(Math.max(28, Math.round(w * scale))) + "px";
        } else {
          img.style.width = "72px";
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

        const maxUm = parseMaxUm(r.grootte || "");
        const cls = sizeClassFromMaxUm(maxUm);
        if (selectedSize !== "alle" && cls !== selectedSize) return;

        const hay = (
          (r.latin || "") +
          " " +
          (r.dutch || "") +
          " " +
          (r.vorm || "") +
          " " +
          (r.grootte || "") +
          " " +
          (r.oppervlak || "") +
          " " +
          (r.opmerkingen || "")
        )
          .toLowerCase()
          .trim();
        if (query && hay.indexOf(query) === -1) return;

        // Optional full-width image row above the data row.
        if (Array.isArray(r.images) && r.images.length > 0) {
          const trImg = document.createElement("tr");
          const tdImg = document.createElement("td");
          tdImg.colSpan = 6;
          renderImagesTd(tdImg, r.images);
          trImg.appendChild(tdImg);
          tbody.appendChild(trImg);
        }

        const tr = document.createElement("tr");
        const cells = [
          r.latin || "",
          r.dutch || "",
          r.vorm || "",
          r.grootte || "",
          r.oppervlak || "",
          r.opmerkingen || "",
        ];
        cells.forEach(function (cell, idx) {
          const td = document.createElement("td");
          // Render Markdown-style links in Latin (pd) and Dutch (pw) columns.
          if (idx === 0 || idx === 1) {
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

