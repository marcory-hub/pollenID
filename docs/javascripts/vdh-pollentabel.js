/**
 * Pollentabel (van der Ham): wizard + platte tabel uit vanderham-pollentabel.json.
 * Werkt met MkDocs Material instant navigation wanneer document$ beschikbaar is.
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

  /**
   * JSON-eindpunten gebruiken *cursief* zoals in het boek; geen volledige Markdown.
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

  function runKey(root, data) {
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
        // Render label + optional image as a small "proof-of-concept".
        const labelSpan = document.createElement("span");
        labelSpan.textContent = ch.label || "Optie " + (idx + 1);
        btn.appendChild(labelSpan);
        if (ch.image) {
          const img = document.createElement("img");
          img.src = ch.image;
          img.alt = (ch.label || "Keuze") + " (afbeelding)";
          img.style.display = "block";
          if (ch.imageWidthPx) {
            img.style.width = String(ch.imageWidthPx) + "px";
          } else {
            img.style.maxWidth = "160px";
          }
          img.style.height = "auto";
          img.style.margin = "6px auto 0";
          btn.appendChild(img);
        }
        btn.addEventListener("click", function () {
          if (ch.outcome && ch.outcome.text) {
            stack.push(id);
            outcomeEl.hidden = false;
            outcomeEl.innerHTML =
              "<h4>Eindpunt</h4><p>" + formatEmphasisAst(ch.outcome.text) + "</p>";
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
    /** @type {Array<{sid:string,label:string,result:string,kind:string}>} */
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
        } else {
          result = "—";
          kind = "leeg";
        }
        rows.push({
          sid: sid,
          label: ch.label || "",
          result: result,
          kind: kind,
        });
      });
    });
    return rows;
  }

  function runTable(root, data) {
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
    ["Stap", "Keuze", "Vervolg of eindpunt", "Type"].forEach(function (h) {
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
      tdL.textContent = row.label;

      const tdR = document.createElement("td");
      if (row.kind.indexOf("eindpunt") === 0 && row.result.indexOf("*") !== -1) {
        tdR.innerHTML = formatEmphasisAst(row.result);
      } else {
        tdR.textContent = row.result;
      }

      const tdK = document.createElement("td");
      tdK.textContent = row.kind;

      tr.appendChild(tdS);
      tr.appendChild(tdL);
      tr.appendChild(tdR);
      tr.appendChild(tdK);
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

    root.replaceChildren();
    root.innerHTML =
      '<p class="vdh-pollentabel-status">' + esc("Laden…") + "</p>";

    fetchJsonCached(jsonUrl)
      .then(function (data) {
        root.replaceChildren();
        runKey(root, data);
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

    root.replaceChildren();
    root.innerHTML =
      '<p class="vdh-pollentabel-status">' + esc("Tabel laden…") + "</p>";

    fetchJsonCached(jsonUrl)
      .then(function (data) {
        root.replaceChildren();
        runTable(root, data);
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
