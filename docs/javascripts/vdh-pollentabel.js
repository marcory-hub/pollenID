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
    return typeof p === "string" && /\/PLACEHOLDER_[A-Za-z]+\.png$/i.test(p);
  }

  function applyImageSizing(img, widthPx, isPlaceholder) {
    img.style.display = "block";
    img.style.height = "auto";
    img.style.margin = "0";

    if (typeof widthPx === "number" && Number.isFinite(widthPx) && widthPx > 0) {
      if (isPlaceholder && widthPx <= 1) {
        img.style.width = "24px";
        img.classList.add("pid-placeholder-image");
      } else {
        img.style.width = String(widthPx) + "px";
      }
      return;
    }

    img.style.maxWidth = isPlaceholder ? "24px" : "320px";
    if (isPlaceholder) img.classList.add("pid-placeholder-image");
  }

  function renderImagesRow(container, images, baseUrl, altPrefix) {
    if (!Array.isArray(images) || images.length === 0) return;
    const row = document.createElement("div");
    row.className = "vdh-pollentabel-images-row";
    row.style.display = "flex";
    row.style.flexWrap = "nowrap";
    row.style.gap = "6px";
    row.style.alignItems = "flex-start";
    row.style.marginTop = "8px";
    row.style.overflowX = "auto";
    container.appendChild(row);

    images.forEach(function (im, imIdx) {
      if (!im || !im.image) return;
      const img = document.createElement("img");
      img.src = resolveAssetUrl(im.image, baseUrl || document.baseURI);
      img.alt = (altPrefix || "Afbeelding") + " (" + (imIdx + 1) + ")";
      const ph = isPlaceholderImagePath(im.image);
      applyImageSizing(img, im.imageWidthPx, ph);
      row.appendChild(img);
    });
  }

  function runKey(root, data, dataAbsUrl) {
    const start = data.start || (data.meta && data.meta.start) || "1";
    const steps = data.steps || {};
    const stack = [];

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

    function showStep(id) {
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

      const choices = step.choices || [];
      if (choices.length === 0) {
        stepEl.innerHTML += "<p>Geen keuzes gedefinieerd.</p>";
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
        // Interactive choices: show placeholders only (not real images),
        // so authors see "slots" without cluttering the UI.
        const phFromChoice = Array.isArray(ch.images)
          ? ch.images.filter(function (im) {
              return im && isPlaceholderImagePath(im.image);
            })
          : [];
        const phFromOutcome =
          ch.outcome && Array.isArray(ch.outcome.images)
            ? ch.outcome.images.filter(function (im) {
                return im && isPlaceholderImagePath(im.image);
              })
            : [];
        const phImgs = phFromChoice.concat(phFromOutcome);
        if (phImgs.length > 0) {
          renderImagesRow(
            btn,
            phImgs,
            dataAbsUrl || document.baseURI,
            (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") + " (placeholder)"
          );
        } else if (isPlaceholderImagePath(ch.image)) {
          renderImagesRow(
            btn,
            [{ image: ch.image, imageWidthPx: ch.imageWidthPx }],
            dataAbsUrl || document.baseURI,
            (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") + " (placeholder)"
          );
        } else if (ch.outcome && isPlaceholderImagePath(ch.outcome.image)) {
          renderImagesRow(
            btn,
            [{ image: ch.outcome.image, imageWidthPx: ch.outcome.imageWidthPx }],
            dataAbsUrl || document.baseURI,
            (ch.label || "Keuze").replace(/\*([^*]*)\*/g, "$1") + " (placeholder)"
          );
        }
        btn.addEventListener("click", function () {
          if (ch.outcome && ch.outcome.text) {
            stack.push(id);
            outcomeEl.hidden = false;
            outcomeEl.replaceChildren();
            const h = document.createElement("h4");
            h.textContent = "Eindpunt";
            const p = document.createElement("p");
            p.innerHTML = formatOutcomeRichText(ch.outcome.text);
            outcomeEl.appendChild(h);
            outcomeEl.appendChild(p);

            const imgs =
              ch.outcome && Array.isArray(ch.outcome.images) ? ch.outcome.images : [];
            if (imgs.length > 0) {
              renderImagesRow(
                outcomeEl,
                imgs,
                dataAbsUrl || document.baseURI,
                (ch.outcome.text || "Eindpunt")
                  .replace(/\*([^*]*)\*/g, "$1")
                  .replace(/\n/g, " ")
                  .trim() + " (afbeelding)"
              );
            }
            actionsEl.replaceChildren();
            addOutcomeNavRow();
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
  }

  function flattenSteps(data) {
    const steps = data.steps || {};
    const ids = Object.keys(steps).sort(function (a, b) {
      return parseInt(a, 10) - parseInt(b, 10);
    });
    /** @type {Array<{sid:string,label:string,result:string,kind:string,images:Array<{image?:string,imageWidthPx?:number}>}>} */
    const rows = [];
    ids.forEach(function (sid) {
      const step = steps[sid];
      (step.choices || []).forEach(function (ch) {
        let result = "";
        let kind = "";
        let images = [];
        if (ch.next) {
          result = "→ stap " + String(ch.next);
          kind = "stap";
          if (Array.isArray(ch.images)) {
            images = ch.images;
          } else if (ch.image) {
            images = [{ image: ch.image, imageWidthPx: ch.imageWidthPx }];
          }
        } else if (ch.outcome && ch.outcome.text) {
          result = ch.outcome.text;
          kind = ch.outcome.incomplete ? "eindpunt (onvolledig)" : "eindpunt";
          if (Array.isArray(ch.outcome.images)) {
            images = ch.outcome.images;
          } else if (ch.outcome.image) {
            images = [{ image: ch.outcome.image, imageWidthPx: ch.outcome.imageWidthPx }];
          }
        } else {
          result = "-";
          kind = "leeg";
          if (Array.isArray(ch.images)) {
            images = ch.images;
          } else if (ch.image) {
            images = [{ image: ch.image, imageWidthPx: ch.imageWidthPx }];
          }
        }
        rows.push({
          sid: sid,
          label: ch.label || "",
          result: result,
          kind: kind,
          images: images,
        });
      });
    });
    return rows;
  }

  function runTable(root, data, dataAbsUrl) {
    const rows = flattenSteps(data);
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
      const hay = (row.sid + " " + row.label + " " + row.result + " " + row.kind)
        .toLowerCase()
        .trim();
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
      if (row.kind.indexOf("eindpunt") === 0) {
        tdR.innerHTML = formatOutcomeRichText(row.result);
      } else {
        tdR.textContent = row.result;
      }
      if (row.images && row.images.length > 0) {
        renderImagesRow(
          tdR,
          row.images,
          dataAbsUrl || document.baseURI,
          (row.kind.indexOf("eindpunt") === 0 ? row.result : row.label || row.result)
            .replace(/\*([^*]*)\*/g, "$1")
            .replace(/\n/g, " ")
            .trim() + " (afbeelding)"
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

    fetchJsonCached(jsonUrl)
      .then(function (data) {
        root.replaceChildren();
        runKey(root, data, dataAbsUrl);
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

    fetchJsonCached(jsonUrl)
      .then(function (data) {
        root.replaceChildren();
        runTable(root, data, dataAbsUrl);
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
})();
