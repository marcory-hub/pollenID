/* PalynoQuest: image-first quiz that can embed a JSON key (vdh-pollentabel.js). */
(function () {
  "use strict";

  function qs(root, sel) {
    return root.querySelector(sel);
  }

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function normText(s) {
    if (typeof s !== "string") return "";
    return s
      .replace(/\*([^*]*)\*/g, "$1")
      .replace(/[^\p{L}\p{N}]+/gu, " ")
      .toLowerCase()
      .trim()
      .replace(/\s+/g, " ");
  }

  function displayNameFromEndpointText(s) {
    if (typeof s !== "string") return "";
    s = s.replace(/\*([^*]*)\*/g, "$1").trim();
    // If a size is present, drop a trailing fragment like ", 34 (30.2-37.0) μm" or ", 51-100 µm"
    if (/[µμ]m\b/u.test(s)) {
      s = s.replace(/\s*,\s*[^,]*[0-9][^,]*[µμ]m\b.*$/u, "");
    }
    return s.trim();
  }

  function isMissingValue(v) {
    return v == null || String(v).trim() === "" || String(v).trim() === "-";
  }

  function resolveUrl(rel) {
    try {
      return new URL(rel, document.baseURI).href;
    } catch (e) {
      return rel;
    }
  }

  function fetchJson(url) {
    return fetch(resolveUrl(url), { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(r.status + " " + r.statusText);
      return r.json();
    });
  }

  function loadAll() {
    return Promise.all([
      fetchJson("../../assets/manifests/keys.json"),
      fetchJson("../../assets/manifests/palynoquest-items.json"),
      fetchJson("../../data/pollen.json"),
    ]).then(function (xs) {
      return { keys: xs[0], items: xs[1], pollen: xs[2] };
    });
  }

  function buildKeyOptions(keys) {
    return (keys.keys || []).map(function (k) {
      return {
        id: k.id,
        title: k.title,
        jsonUrl: k.jsonUrl,
      };
    });
  }

  function pickRandom(arr) {
    if (!Array.isArray(arr) || arr.length === 0) return null;
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  function groupKeyFromImagePath(p) {
    if (typeof p !== "string" || !p) return "";
    var base = p.split("/").pop() || "";
    base = base.replace(/\.[^.]+$/, "");
    var parts = base.split("_");
    if (parts.length < 2) return "";
    return parts[0] + "_" + parts[1];
  }

  function buildImageToSlugFromPollen(pollen) {
    var map = {};
    if (!pollen || typeof pollen !== "object") return map;
    Object.keys(pollen).forEach(function (slug) {
      var rec = pollen[slug];
      if (!rec || typeof rec !== "object") return;
      var imgs = rec.images;
      if (!Array.isArray(imgs)) return;
      imgs.forEach(function (im) {
        if (!im || typeof im.path !== "string" || !im.path) return;
        var p = im.path.replace(/^\//, "").replace(/^\.\//, "");
        map[p] = slug;
      });
    });
    return map;
  }

  function bootOne(root) {
    var state = {
      keys: [],
      items: [],
      current: null,
      selectedKeyJsonUrl: null,
      expectedPath: null,
      diverged: false,
      pendingJump: false,
      endpointToExample: {},
      groupToImages: {},
      pollen: {},
      imageToSlug: {},
    };

    var imgEl = qs(root, "[data-pq-image]");
    var statusEl = qs(root, "[data-pq-status]");
    var inputEl = qs(root, "[data-pq-input]");
    var submitEl = qs(root, "[data-pq-submit]");
    var mcqEl = qs(root, "[data-pq-mcq]");
    var showMcqEl = qs(root, "[data-pq-showmcq]");
    var mcqStatusEl = qs(root, "[data-pq-mcqstatus]");
    var nextEl = qs(root, "[data-pq-next]");
    var keySelEl = qs(root, "[data-pq-keyselect]");
    var loadKeyEl = qs(root, "[data-pq-loadkey]");
    var keyWrapEl = qs(root, "[data-pq-keywrap]");
    var jumpEl = qs(root, "[data-pq-jump]");
    var pathEl = qs(root, "[data-pq-path]");
    var wrongPreviewEl = qs(root, "[data-pq-wrongpreview]");
    var galleryEl = qs(root, "[data-pq-gallery]");
    var infoEl = qs(root, "[data-pq-info]");

    function setStatus(html) {
      if (!statusEl) return;
      statusEl.innerHTML = html;
    }

    function setMcqStatus(html) {
      if (!mcqStatusEl) return;
      mcqStatusEl.innerHTML = html;
    }

    function clearWrongPreview() {
      if (!wrongPreviewEl) return;
      wrongPreviewEl.hidden = true;
      wrongPreviewEl.replaceChildren();
    }

    function clearGallery() {
      if (!galleryEl) return;
      galleryEl.hidden = true;
      galleryEl.replaceChildren();
    }

    function showWrongPreview(opt) {
      if (!wrongPreviewEl) return;
      wrongPreviewEl.replaceChildren();
      if (!opt || !opt.image) {
        wrongPreviewEl.hidden = true;
        return;
      }
      wrongPreviewEl.hidden = false;

      var wrap = document.createElement("div");
      wrap.className = "admonition warning";
      wrap.style.margin = "0";

      var p = document.createElement("p");
      p.innerHTML = "<strong>Gekozen (onjuist)</strong>";
      wrap.appendChild(p);

      var gk = groupKeyFromImagePath(opt.image);
      var imgs = gk ? state.groupToImages[gk] || [] : [];
      if (!Array.isArray(imgs) || imgs.length === 0) {
        imgs = [{ image: opt.image, imageWidthPx: opt.imageWidthPx }];
      }

      var row = document.createElement("div");
      row.style.display = "flex";
      row.style.flexWrap = "wrap";
      row.style.gap = "6px";
      row.style.overflowX = "auto";
      row.style.alignItems = "flex-start";
      row.style.maxWidth = "50vw";

      var maxW = 0;
      imgs.forEach(function (im) {
        if (!im) return;
        var w = im.imageWidthPx;
        if (typeof w === "number" && isFinite(w) && w > maxW) maxW = w;
      });
      // Scale so the largest pollen preview stays compact, while preserving relative size ratios.
      var targetMaxPx = 180;
      var scale = maxW > 0 ? Math.min(1, targetMaxPx / maxW) : 1;

      imgs.forEach(function (im) {
        if (!im || !im.image) return;
        var img = document.createElement("img");
        img.src = resolveUrl("../../" + String(im.image).replace(/^\//, ""));
        img.alt = "Onjuist gekozen pollen";
        img.style.display = "block";
        img.style.height = "auto";
        img.style.borderRadius = "4px";
        var w = im.imageWidthPx;
        if (typeof w === "number" && isFinite(w) && w > 0) {
          img.style.width = String(Math.max(44, Math.round(w * scale))) + "px";
        } else {
          img.style.width = "72px";
        }
        img.style.maxWidth = "100%";
        row.appendChild(img);
      });
      wrap.appendChild(row);

      wrongPreviewEl.appendChild(wrap);
    }

    function setImage(rel) {
      if (!imgEl) return;
      imgEl.src = resolveUrl("../../" + rel.replace(/^\//, ""));
      imgEl.alt = "Quiz afbeelding";
    }

    function setMainImage(item, imagePath) {
      if (!item) return;
      var imgs = state.groupToImages[groupKeyFromImagePath(item.image)] || [];
      var chosen = null;
      for (var i = 0; i < imgs.length; i += 1) {
        if (imgs[i].image === imagePath) {
          chosen = imgs[i];
          break;
        }
      }
      if (!chosen) {
        chosen = { image: imagePath, imageWidthPx: item.imageWidthPx };
      }
      setImage(chosen.image);
      applyImageWidth(chosen);
    }

    function applyImageWidth(item) {
      if (!imgEl) return;
      var w = item && item.imageWidthPx;
      if (typeof w === "number" && isFinite(w) && w > 0) {
        imgEl.style.width = String(Math.round(w)) + "px";
        imgEl.style.maxWidth = "100%";
      } else {
        imgEl.style.width = "";
        imgEl.style.maxWidth = "420px";
      }
    }

    function renderGallery(item) {
      if (!galleryEl) return;
      galleryEl.replaceChildren();
      galleryEl.hidden = true;
      if (!item || !item.image) return;
      var gk = groupKeyFromImagePath(item.image);
      if (!gk) return;
      var imgs = state.groupToImages[gk] || [];
      if (!Array.isArray(imgs) || imgs.length <= 1) return;

      galleryEl.hidden = false;
      var row = document.createElement("div");
      row.style.display = "flex";
      row.style.flexWrap = "nowrap";
      row.style.gap = "6px";
      row.style.overflowX = "auto";
      row.style.alignItems = "flex-start";

      imgs.forEach(function (im) {
        if (!im || !im.image) return;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "md-button";
        btn.style.padding = "0";
        btn.style.minWidth = "unset";
        btn.style.lineHeight = "0";

        var th = document.createElement("img");
        th.src = resolveUrl("../../" + String(im.image).replace(/^\//, ""));
        th.alt = "Variant";
        th.style.display = "block";
        th.style.height = "auto";
        th.style.width = "72px";
        th.style.maxWidth = "72px";
        th.style.borderRadius = "4px";

        btn.addEventListener("click", function () {
          setMainImage(item, im.image);
        });
        btn.appendChild(th);
        row.appendChild(btn);
      });

      galleryEl.appendChild(row);
    }

    function slugForCurrentItem(item) {
      if (!item || typeof item.image !== "string" || !item.image) return "";
      var rel = item.image.replace(/^\//, "").replace(/^\.\//, "");
      if (state.imageToSlug[rel]) return state.imageToSlug[rel];
      return groupKeyFromImagePath(item.image) || "";
    }

    function clearInfo() {
      if (!infoEl) return;
      infoEl.hidden = true;
      infoEl.replaceChildren();
    }

    function linkLabelForPollenLinkKey(key) {
      var k = String(key || "").toLowerCase();
      if (k === "pollenx") return "PollenX";
      if (k === "tstebler") return "Tstebler";
      if (k === "paldat") return "PalDat";
      return esc(key);
    }

    function renderInfo(slug) {
      if (!infoEl) return;
      infoEl.replaceChildren();
      if (!slug || !state.pollen || typeof state.pollen !== "object") {
        infoEl.hidden = true;
        return;
      }
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") {
        infoEl.hidden = true;
        return;
      }

      function addRow(dl, labelHtml, valueHtml) {
        var dt = document.createElement("dt");
        dt.style.fontWeight = "600";
        dt.style.marginTop = "6px";
        dt.innerHTML = labelHtml;
        var dd = document.createElement("dd");
        dd.style.margin = "0 0 0 0.75rem";
        dd.innerHTML = valueHtml;
        dl.appendChild(dt);
        dl.appendChild(dd);
      }

      var dl = document.createElement("dl");
      dl.style.margin = "0";
      dl.style.fontSize = "0.85rem";

      if (!isMissingValue(rec.latin)) {
        addRow(dl, "Latijnse naam", "<em>" + esc(rec.latin) + "</em>");
      }
      if (!isMissingValue(rec.dutch)) {
        addRow(dl, "Nederlandse naam", esc(rec.dutch));
      }
      if (!isMissingValue(rec.family)) {
        addRow(dl, "Familie", esc(rec.family));
      }
      if (!isMissingValue(rec.shape)) {
        addRow(dl, "Vorm", esc(rec.shape));
      }
      if (!isMissingValue(rec.ornamentation)) {
        addRow(dl, "Ornamentatie", esc(rec.ornamentation));
      }
      if (!isMissingValue(rec.aperture)) {
        addRow(dl, "Apertuur", esc(rec.aperture));
      }
      var sz = rec.size;
      if (sz && typeof sz === "object") {
        var a = !isMissingValue(sz.smallest_size) ? String(sz.smallest_size).trim() : "";
        var b = !isMissingValue(sz.largest_size) ? String(sz.largest_size).trim() : "";
        var sizeStr = "";
        if (a && b) {
          sizeStr = a === b ? a : a + " – " + b;
        } else {
          sizeStr = a || b || "";
        }
        if (sizeStr) {
          addRow(dl, "Grootte", esc(sizeStr));
        }
      }
      var links = rec.links;
      if (links && typeof links === "object") {
        var parts = [];
        Object.keys(links).forEach(function (lk) {
          var url = links[lk];
          if (isMissingValue(url)) return;
          parts.push(
            '<a href="' +
              esc(String(url)) +
              '" target="_blank" rel="noopener">' +
              linkLabelForPollenLinkKey(lk) +
              "</a>"
          );
        });
        if (parts.length) {
          addRow(dl, "Externe links", parts.join(" · "));
        }
      }

      if (!dl.childNodes.length) {
        infoEl.hidden = true;
        return;
      }

      var wrap = document.createElement("div");
      wrap.className = "admonition info";
      wrap.style.margin = "0";
      var title = document.createElement("p");
      title.innerHTML = "<strong>Pollengegevens</strong>";
      title.style.margin = "0 0 8px 0";
      wrap.appendChild(title);
      wrap.appendChild(dl);
      infoEl.appendChild(wrap);
      infoEl.hidden = false;
    }

    function buildMcq(item) {
      if (!mcqEl) return;
      mcqEl.replaceChildren();
      var opts = [];
      if (item && item.strict && item.strict.endpointText) {
        var strictText = item.strict.endpointText;
        opts.push({
          text: displayNameFromEndpointText(strictText) || strictText,
          correct: true,
          image: item.image,
          imageWidthPx: item.imageWidthPx,
        });
      }
      (item.distractors || []).forEach(function (d) {
        if (d && d.endpointText) {
          var dt = d.endpointText;
          var dn = displayNameFromEndpointText(dt) || dt;
          var ex = state.endpointToExample[dn] || null;
          opts.push({
            text: dn,
            correct: false,
            image: ex ? ex.image : null,
            imageWidthPx: ex ? ex.imageWidthPx : null,
          });
        }
      });
      if (opts.length < 4) {
        var pool = (state.items || [])
          .map(function (it) {
            var t = it && it.strict ? it.strict.endpointText : "";
            return displayNameFromEndpointText(t) || t;
          })
          .filter(function (t) {
            var strictFull = item && item.strict ? item.strict.endpointText : "";
            var strictName = displayNameFromEndpointText(strictFull) || strictFull;
            return typeof t === "string" && t && t !== strictName;
          });
        pool = shuffle(pool);
        while (opts.length < 4 && pool.length > 0) {
          var t = pool.pop();
          if (
            t &&
            !opts.some(function (o) {
              return o.text === t;
            })
          ) {
            var ex = state.endpointToExample[t] || null;
            opts.push({ text: t, correct: false });
            opts[opts.length - 1].image = ex ? ex.image : null;
            opts[opts.length - 1].imageWidthPx = ex ? ex.imageWidthPx : null;
          }
        }
      }
      opts = shuffle(opts).slice(0, 4);
      var correctText = "";
      for (var ci = 0; ci < opts.length; ci += 1) {
        if (opts[ci].correct) {
          correctText = opts[ci].text;
          break;
        }
      }
      opts.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "md-button";
        b.innerHTML = esc(o.text);
        // Align option labels left (more readable with varying lengths)
        b.style.textAlign = "left";
        b.style.display = "flex";
        b.style.justifyContent = "flex-start";
        b.style.whiteSpace = "normal";
        b.addEventListener("click", function () {
          setMcqStatus(
            o.correct ? "<strong>Juist.</strong>" : "<strong>Onjuist.</strong>"
          );
          if (o.correct) {
            clearWrongPreview();
            renderInfo(slugForCurrentItem(state.current));
          } else {
            clearInfo();
            showWrongPreview(o);
          }
        });
        mcqEl.appendChild(b);
      });
    }

    function newQuestion() {
      state.current = pickRandom(state.items);
      state.diverged = false;
      state.expectedPath = state.current && state.current.expectedPath ? state.current.expectedPath : null;
      state.pendingJump = false;
      state.selectedKeyJsonUrl = null;
      if (keyWrapEl) {
        keyWrapEl.replaceChildren();
      }
      if (!state.current) {
        setStatus('<p class="admonition warning"><strong>Geen quiz-items gevonden.</strong></p>');
        return;
      }
      if (inputEl) inputEl.value = "";
      setStatus("");
      setImage(state.current.image);
      applyImageWidth(state.current);
      renderGallery(state.current);
      // Keep MCQ hidden until user explicitly reveals it.
      if (mcqEl) {
        mcqEl.hidden = true;
        mcqEl.replaceChildren();
      }
      setMcqStatus("");
      clearWrongPreview();
      clearInfo();
      // Gallery stays visible for this question.
      if (pathEl) {
        pathEl.hidden = true;
        pathEl.replaceChildren();
      }
      if (jumpEl) jumpEl.hidden = true;

      // Preselect recommended key for this item (but don't auto-load).
      var rec = state.current && state.current.strict ? state.current.strict.keyJsonUrl : "";
      if (keySelEl && rec) {
        for (var i = 0; i < keySelEl.options.length; i += 1) {
          if (keySelEl.options[i].value === rec) {
            keySelEl.selectedIndex = i;
            break;
          }
        }
      }
    }

    function renderExpectedPath() {
      if (!pathEl) return;
      if (!state.expectedPath || state.expectedPath.length === 0) return;
      pathEl.replaceChildren();
      pathEl.hidden = false;

      var wrap = document.createElement("div");
      wrap.className = "admonition info";
      var title = document.createElement("p");
      title.innerHTML = "<strong>Verwacht pad</strong>";
      wrap.appendChild(title);

      var ol = document.createElement("ol");
      ol.style.margin = "0";
      ol.style.paddingLeft = "1.25rem";
      state.expectedPath.forEach(function (p) {
        if (!p) return;
        var li = document.createElement("li");
        var sid = p.stepId != null ? String(p.stepId) : "";
        var lbl = p.choiceLabel != null ? String(p.choiceLabel) : "";
        li.textContent = (sid ? "Stap " + sid + ": " : "") + lbl;
        ol.appendChild(li);
      });
      wrap.appendChild(ol);
      pathEl.appendChild(wrap);
    }

    function gradeOpenAnswer() {
      if (!state.current) return;
      var guess = normText(inputEl ? inputEl.value : "");
      var strictFull = state.current.strict && state.current.strict.endpointText;
      var strict = normText(displayNameFromEndpointText(strictFull) || strictFull);
      var accepted = (state.current.accepted || []).map(function (a) {
        var full = a.endpointText || "";
        var disp = displayNameFromEndpointText(full) || full;
        return { t: normText(disp), g: a.grade || "acceptable" };
      });
      if (!guess) {
        setStatus('<p class="admonition warning"><strong>Geen antwoord ingevuld.</strong></p>');
        return;
      }
      if (strict && guess === strict) {
        setStatus('<p class="admonition success"><strong>Correct (strict).</strong></p>');
        return;
      }
      for (var i = 0; i < accepted.length; i += 1) {
        if (accepted[i].t && guess === accepted[i].t) {
          var g = accepted[i].g === "partial" ? "Gedeeltelijk correct." : "Correct (acceptabel).";
          setStatus('<p class="admonition info"><strong>' + esc(g) + "</strong></p>");
          return;
        }
      }
      setStatus('<p class="admonition error"><strong>Onjuist.</strong></p>');
    }

    function populateKeys() {
      if (!keySelEl) return;
      keySelEl.replaceChildren();
      var ph = document.createElement("option");
      ph.value = "";
      ph.textContent = "Kies een sleutel…";
      keySelEl.appendChild(ph);
      state.keys.forEach(function (k) {
        var o = document.createElement("option");
        // Keep docs-relative (keys/...) in value; resolve on load.
        o.value = String(k.jsonUrl || "").replace(/^\.\//, "").replace(/^\//, "");
        o.textContent = k.title;
        keySelEl.appendChild(o);
      });
    }

    function loadKey(jsonUrl) {
      if (!keyWrapEl) return;
      state.selectedKeyJsonUrl = jsonUrl || null;
      keyWrapEl.replaceChildren();
      if (!jsonUrl) return;
      var normUrl = String(jsonUrl).replace(/^\.\//, "").replace(/^\//, "");
      if (normUrl.indexOf("kerkvliet-determinatietabel.json") !== -1) {
        state.selectedKeyJsonUrl = null;
        setStatus(
          '<p class="admonition info">' +
            "<strong>Determinatietabel (Kerkvliet)</strong> heeft een eigen opzoektabel-gezicht (geen stappenwizard hier). " +
            "Ga naar <em>Identificatiesleutels → Determinatietabel voor pollen in Nederlandse honing</em>.</p>"
        );
        return;
      }
      var rootEl = document.createElement("div");
      rootEl.id = "vdh-pollentabel-root";
      rootEl.setAttribute("data-json-url", "../../" + normUrl);
      keyWrapEl.appendChild(rootEl);
      if (window.PID_VDH_POLLENTABEL && typeof window.PID_VDH_POLLENTABEL.boot === "function") {
        window.PID_VDH_POLLENTABEL.boot();
      }
      setStatus(
        '<p class="admonition info"><strong>Sleutel geladen.</strong> Volg de stappen, of geef direct een antwoord.</p>'
      );
    }

    function onVdhChoice(ev) {
      if (!state.current || !state.expectedPath || state.expectedPath.length === 0) return;
      // If the wrong key is loaded, don't attempt divergence logic.
      var recKey = state.current && state.current.strict ? state.current.strict.keyJsonUrl : "";
      if (recKey && state.selectedKeyJsonUrl && state.selectedKeyJsonUrl !== recKey) return;
      var exp = state.expectedPath[0];
      if (!exp) return;
      if (String(ev.detail && ev.detail.stepId) !== String(exp.stepId)) return;
      var ok =
        String(ev.detail && ev.detail.choiceLabel) === String(exp.choiceLabel) ||
        Number(ev.detail && ev.detail.choiceIdx) === Number(exp.choiceIdx);
      if (!ok) {
        state.diverged = true;
        if (jumpEl) jumpEl.hidden = false;
        setStatus(
          '<p class="admonition warning"><strong>Afwijking bij stap ' +
            esc(exp.stepId) +
            ".</strong> Je keuze wijkt af van het verwachte pad.</p>"
        );
      }
    }

    function tryJumpNow() {
      var keyRoot = keyWrapEl ? keyWrapEl.querySelector("#vdh-pollentabel-root") : null;
      if (!keyRoot) return false;
      var ctl = keyRoot.__vdhPollentabelController;
      if (!ctl || !state.expectedPath || state.expectedPath.length === 0) return false;

      ctl.reset();
      for (var i = 0; i < state.expectedPath.length; i += 1) {
        var exp = state.expectedPath[i];
        if (!exp) continue;
        // Follow the key normally so its back-stack is populated.
        ctl.chooseByIndex(exp.choiceIdx);
      }
      return true;
    }

    function jumpToExpected() {
      if (!state.current || !state.expectedPath || state.expectedPath.length === 0) return;
      var recKey = state.current && state.current.strict ? state.current.strict.keyJsonUrl : "";
      if (recKey && state.selectedKeyJsonUrl !== recKey) {
        // Auto-load the correct key, then jump once it is ready.
        state.pendingJump = true;
        if (keySelEl) keySelEl.value = recKey;
        loadKey(recKey);
        setStatus(
          '<p class="admonition info"><strong>Andere sleutel geladen.</strong> Springen naar het verwachte pad zodra de sleutel klaar is.</p>'
        );
      }

      // Controller is async: retry briefly until it exists.
      var tries = 0;
      function retry() {
        tries += 1;
        if (tryJumpNow()) {
          state.pendingJump = false;
          renderExpectedPath();
          return;
        }
        if (tries < 20) setTimeout(retry, 150);
      }
      retry();
    }

    root.addEventListener("pid:vdh-choice", onVdhChoice);
    if (jumpEl) {
      jumpEl.addEventListener("click", jumpToExpected);
    }
    if (showMcqEl) {
      showMcqEl.addEventListener("click", function () {
        if (!state.current) return;
        buildMcq(state.current);
        if (mcqEl) mcqEl.hidden = false;
      });
    }
    if (submitEl) submitEl.addEventListener("click", gradeOpenAnswer);
    if (nextEl) nextEl.addEventListener("click", newQuestion);
    if (loadKeyEl)
      loadKeyEl.addEventListener("click", function () {
        loadKey(keySelEl ? keySelEl.value : "");
      });

    loadAll()
      .then(function (all) {
        state.keys = buildKeyOptions(all.keys || {});
        state.items = (all.items && all.items.items) || [];
        var pollenRoot = all.pollen;
        state.pollen =
          pollenRoot && typeof pollenRoot === "object" && !Array.isArray(pollenRoot) ? pollenRoot : {};
        state.imageToSlug = buildImageToSlugFromPollen(state.pollen);
        state.endpointToExample = {};
        state.groupToImages = {};
        (state.items || []).forEach(function (it) {
          if (!it || !it.strict || !it.strict.endpointText) return;
          var name = displayNameFromEndpointText(it.strict.endpointText) || it.strict.endpointText;
          if (!name) return;
          if (!state.endpointToExample[name]) {
            state.endpointToExample[name] = {
              image: it.image,
              imageWidthPx: it.imageWidthPx,
            };
          }

          var gk = groupKeyFromImagePath(it.image);
          if (gk) {
            if (!state.groupToImages[gk]) state.groupToImages[gk] = [];
            if (!state.groupToImages[gk].some(function (x) { return x && x.image === it.image; })) {
              state.groupToImages[gk].push({ image: it.image, imageWidthPx: it.imageWidthPx });
            }
          }
        });
        populateKeys();
        newQuestion();
      })
      .catch(function (e) {
        setStatus(
          '<p class="admonition error"><strong>Fout bij laden van PalynoQuest data.</strong> ' +
            esc(String(e && e.message ? e.message : e)) +
            "</p>"
        );
      });
  }

  function boot() {
    document.querySelectorAll("[data-palynoquest]").forEach(function (root) {
      bootOne(root);
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();

