/* PalynoQuest: see docs/naslag/palynoquest-modes.md (mode locks; do not coerce 1/2/3 into kenmerken). */
(function () {
  "use strict";

  const P = window.PidCore || {};

  function esc(s) {
    if (typeof P.esc === "function") return P.esc(s);
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function visibilityLabelNl(code) {
    if (typeof P.visibilityLabelNl === "function") return P.visibilityLabelNl(code);
    return "";
  }

  function morphWithVisibility(text, visibilityCode) {
    if (typeof P.morphWithVisibility === "function") {
      return P.morphWithVisibility(text, visibilityCode);
    }
    var t = text != null ? String(text).trim() : "";
    return t;
  }

  function isMissingValue(v) {
    if (typeof P.isMissingValue === "function") return P.isMissingValue(v);
    return v == null || String(v).trim() === "" || String(v).trim() === "-";
  }

  function qs(root, sel) {
    return root.querySelector(sel);
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

  /** Site root (…/pollenID/) from the loaded palynoquest.js URL; stable under site_url and instant nav. */
  function siteRootUrl() {
    try {
      var scripts = document.querySelectorAll('script[src*="palynoquest.js"]');
      var el = scripts.length ? scripts[scripts.length - 1] : null;
      var abs = el && el.src ? el.src : "";
      if (abs) {
        var u = new URL(abs);
        var marker = "/javascripts/palynoquest.js";
        var idx = u.pathname.toLowerCase().indexOf(marker);
        if (idx !== -1) {
          u.pathname = u.pathname.slice(0, idx + 1);
          u.search = "";
          u.hash = "";
          return u.href;
        }
      }
    } catch (e) {}
    try {
      var logo = document.querySelector(
        "header.md-header a.md-logo, header.md-header a.md-header__button.md-logo"
      );
      if (logo && logo.href) {
        var lu = new URL(logo.href, document.baseURI);
        var p = lu.pathname.replace(/\/+$/, "");
        if (/\.(html?|php)$/i.test(p)) p = p.replace(/\/[^/]+$/, "");
        lu.pathname = (p || "/") + "/";
        lu.hash = "";
        lu.search = "";
        return lu.href;
      }
    } catch (e2) {}
    try {
      // GitHub project pages: /<repo>/…
      var path = String(location.pathname || "");
      var m = path.match(/^(\/[^/]+\/)/);
      if (m && /\.github\.io$/i.test(location.hostname || "")) {
        return location.origin + m[1];
      }
    } catch (e3) {}
    try {
      return new URL("./", document.baseURI).href;
    } catch (e4) {
      return document.baseURI;
    }
  }

  /** Resolve a site-root-relative path (assets/…, data/…). Strips accidental leading ../. */
  function resolveUrl(rel) {
    var path = String(rel == null ? "" : rel).replace(/^\//, "");
    while (path.indexOf("../") === 0) {
      path = path.slice(3);
    }
    try {
      return new URL(path, siteRootUrl()).href;
    } catch (e) {
      return path;
    }
  }

  function fetchJson(url) {
    return fetch(resolveUrl(url), { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(r.status + " " + r.statusText + " (" + url + ")");
      return r.json();
    });
  }

  function loadAll() {
    // Kenmerken / lookalike / name-MCQ need pollen (+ optional manifests).
    // keys/items are optional so a missing quiz manifest does not blank the whole UI.
    return Promise.all([
      fetchJson("assets/manifests/keys.json").catch(function () {
        return { keys: [] };
      }),
      fetchJson("assets/manifests/palynoquest-items.json").catch(function () {
        return { items: [] };
      }),
      fetchJson("data/pollen.json"),
      fetchJson("assets/manifests/lookalike-groups.json").catch(function () {
        return { pairs: [], groups: {} };
      }),
      fetchJson("assets/manifests/morph-neighbours.json").catch(function () {
        return { version: 1, neighbours: {} };
      }),
    ]).then(function (xs) {
      return {
        keys: xs[0],
        items: xs[1],
        pollen: xs[2],
        lookalikes: xs[3],
        morphNeighbours: xs[4],
      };
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

  var LS_LEVEL = "pid_pq_level";
  var LS_PROGRESS = "pid_pq_progress";
  var LS_CONFUSIONS = "pid_pq_confusions";
  var BOX_MAX = 4;
  var LOOKALIKE_DIFFS = { easy: true, moderate: true, difficult: true };
  var LEVEL1_MAX_RANK = 20;
  // Mirrors data/feature_vocab.yaml (coarse LM codes for Kenmerken-drill).
  var FEATURE_VOCAB = {
    sculptuur: {
      reticulaat: "reticulaat",
      fenestraat: "fenestraat (echinaat T)",
      striaat: "striaat",
      psilaat: "psilaat / glad",
      verrucaat: "verrucaat",
      scabraat: "scabraat",
      foveolaat: "foveolaat",
    },
    apertuur: {
      tricolpaat: "tricolpaat",
      tricolporaat: "tricolporaat",
      monocolpaat: "monocolpaat",
      periporaat: "periporaat",
      stephanocolpaat: "stephanocolpaat",
      syncolpaat: "syncolpaat",
    },
    vorm: {
      rond: "rond / sferoïd",
      driehoekig: "driehoekig (polair aanzicht)",
      prolaat: "prolaat / ovaal",
      oblaat: "oblaat",
    },
    grootteklasse: {
      under_15: "onder 15 µm",
      band_15_25: "15–25 µm",
      band_25_40: "25–40 µm",
      band_40_60: "40–60 µm",
      over_60: "boven 60 µm",
    },
  };
  var FEATURE_FIELDS = ["vorm", "apertuur", "sculptuur", "grootteklasse"];

  function parseLevelValue(raw) {
    var s = String(raw == null ? "1" : raw).trim().toLowerCase();
    var kenMatch = s.match(/^kenmerken(?:-(\d+))?$/);
    if (kenMatch || s === "feature" || s === "features") {
      var kenLv = kenMatch && kenMatch[1] ? Number(kenMatch[1]) : 1;
      if (!isFinite(kenLv) || kenLv < 1) kenLv = 1;
      if (kenLv > 3) kenLv = 3;
      kenLv = Math.floor(kenLv);
      return {
        kenmerkenMode: true,
        lookalikeMode: false,
        lookalikeDiff: "all",
        level: kenLv,
        value: kenLv === 1 ? "kenmerken" : "kenmerken-" + kenLv,
      };
    }
    if (s === "lookalike" || s === "lookalike-all") {
      return {
        kenmerkenMode: false,
        lookalikeMode: true,
        lookalikeDiff: "all",
        level: 1,
        value: "lookalike",
      };
    }
    if (s.indexOf("lookalike-") === 0) {
      var diff = s.slice("lookalike-".length);
      if (!LOOKALIKE_DIFFS[diff]) diff = "all";
      return {
        kenmerkenMode: false,
        lookalikeMode: true,
        lookalikeDiff: diff,
        level: 1,
        value: "lookalike-" + diff,
      };
    }
    var lv = Number(s);
    if (!isFinite(lv) || lv < 1) lv = 1;
    if (lv > 3) lv = 3;
    lv = Math.floor(lv);
    // Numeric tiers: name-MCQ (image + 4 names). Kenmerken drill uses kenmerken / kenmerken-N.
    return {
      kenmerkenMode: false,
      lookalikeMode: false,
      lookalikeDiff: "all",
      level: lv,
      value: String(lv),
    };
  }

  function readLocalJson(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      if (!raw) return fallback;
      var parsed = JSON.parse(raw);
      return parsed == null ? fallback : parsed;
    } catch (e) {
      return fallback;
    }
  }

  function writeLocalJson(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      /* ignore quota / private mode */
    }
  }

  function clampLevel(n) {
    return parseLevelValue(n).level;
  }

  /** Willekeurig dropdown has no numeric options; migrate stale localStorage 1/2/3 → kenmerken*. */
  function normalizeUnlockedLevel(raw, levelEl) {
    var parsed = parseLevelValue(raw);
    if (!levelEl) return parsed.value;
    var want = parsed.value;
    var i;
    for (i = 0; i < levelEl.options.length; i += 1) {
      if (levelEl.options[i].value === want) return want;
    }
    if (parsed.lookalikeMode) return "lookalike";
    if (parsed.level === 2) return "kenmerken-2";
    if (parsed.level === 3) return "kenmerken-3";
    return "kenmerken";
  }

  function groupKeyFromImagePath(p) {
    if (typeof p !== "string" || !p) return "";
    var base = p.split("/").pop() || "";
    base = base.replace(/\.[^.]+$/, "");
    var parts = base.split("_");
    if (parts.length < 2) return "";
    return parts[0] + "_" + parts[1];
  }

  function slugQuizScore(rec) {
    if (!rec || typeof rec !== "object") return 0;
    var score = 0;
    var rank = rec.learning_priority_rank;
    if (typeof rank === "number" && isFinite(rank) && rank > 0) score += 1000 - Math.min(rank, 999);
    var c = rec.controlled;
    if (c && typeof c === "object" && c.vorm && c.sculptuur && c.apertuur && c.grootteklasse) {
      score += 100;
    }
    return score;
  }

  function buildImageToSlugFromPollen(pollen) {
    var map = {};
    var scores = {};
    if (!pollen || typeof pollen !== "object") return map;
    Object.keys(pollen).forEach(function (slug) {
      var rec = pollen[slug];
      if (!rec || typeof rec !== "object") return;
      var imgs = rec.images;
      if (!Array.isArray(imgs)) return;
      var score = slugQuizScore(rec);
      imgs.forEach(function (im) {
        if (!im || typeof im.path !== "string" || !im.path) return;
        var path = im.path.replace(/^\//, "").replace(/^\.\//, "");
        // Prefer learning-priority / controlled taxa when several slugs share an image
        // (e.g. brassica_typ reuses brassica_napus assets).
        if (!map[path] || score > (scores[path] || 0)) {
          map[path] = slug;
          scores[path] = score;
        }
      });
    });
    return map;
  }

  function bootOne(root) {
    var lockLevel = (root.getAttribute("data-pq-lock-level") || "").trim();
    var state = {
      keys: [],
      items: [],
      pool: [],
      namePool: [],
      featurePool: [],
      level: 1,
      kenmerkenMode: false,
      lookalikeMode: false,
      lookalikeDiff: "all",
      lookalikePairs: [],
      lookalikePool: [],
      morphNeighbours: {},
      currentLookalike: null,
      currentFeature: null,
      currentName: null,
      featureStep: 0,
      featureCorrect: 0,
      progress: {},
      confusions: [],
      current: null,
      selectedKeyJsonUrl: null,
      expectedPath: null,
      expectedStepIdx: 0,
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
    var backtrackEl = qs(root, "[data-pq-backtrack]");
    var pathEl = qs(root, "[data-pq-path]");
    var wrongPreviewEl = qs(root, "[data-pq-wrongpreview]");
    var galleryEl = qs(root, "[data-pq-gallery]");
    var infoEl = qs(root, "[data-pq-info]");
    var levelEl = qs(root, "[data-pq-level]");
    var progressEl = qs(root, "[data-pq-progress]");
    var normalPanels = root.querySelectorAll("[data-pq-normal-panel]");
    var lookalikePanelEl = qs(root, "[data-pq-lookalike-panel]");
    var kenmerkenPanelEl = qs(root, "[data-pq-kenmerken-panel]");
    var featurePromptEl = qs(root, "[data-pq-feature-prompt]");
    var lookalikePromptEl = qs(root, "[data-pq-lookalike-prompt]");
    var exportConfusionsEl = qs(root, "[data-pq-export-confusions]");

    if (lockLevel && levelEl) {
      var levelRow = levelEl.closest("p");
      if (levelRow) levelRow.hidden = true;
      else levelEl.hidden = true;
    }

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
      var imgs = [];
      if (opt && opt.chosenSlug) {
        imgs = imagesForSlug(opt.chosenSlug);
      }
      if ((!imgs || !imgs.length) && opt && opt.image) {
        var gk = groupKeyFromImagePath(opt.image);
        imgs = gk ? state.groupToImages[gk] || [] : [];
        if (!Array.isArray(imgs) || imgs.length === 0) {
          imgs = [{ image: opt.image, imageWidthPx: opt.imageWidthPx }];
        }
      }
      if (!imgs || !imgs.length) {
        wrongPreviewEl.hidden = true;
        return;
      }
      wrongPreviewEl.hidden = false;

      var wrap = document.createElement("div");
      wrap.className = "admonition warning";
      wrap.style.margin = "0";

      var title = document.createElement("p");
      var name =
        (opt && opt.text) ||
        (opt && opt.chosenSlug ? labelForSlug(opt.chosenSlug) : "") ||
        "onjuiste keuze";
      title.innerHTML =
        "<strong>Ter vergelijking:</strong> " + esc(name) + " (jouw keuze)";
      wrap.appendChild(title);

      var row = document.createElement("div");
      row.style.display = "flex";
      row.style.flexWrap = "wrap";
      row.style.gap = "6px";
      row.style.overflowX = "auto";
      row.style.alignItems = "flex-start";
      row.style.maxWidth = "100%";

      var maxW = 0;
      imgs.forEach(function (im) {
        if (!im) return;
        var w = im.imageWidthPx;
        if (typeof w === "number" && isFinite(w) && w > maxW) maxW = w;
      });
      var targetMaxPx = 220;
      var scale = maxW > 0 ? Math.min(1, targetMaxPx / maxW) : 1;

      imgs.forEach(function (im) {
        if (!im || !im.image) return;
        var img = document.createElement("img");
        img.src = resolveUrl(String(im.image).replace(/^\//, ""));
        img.alt = name;
        img.style.display = "block";
        img.style.height = "auto";
        img.style.borderRadius = "4px";
        var w = im.imageWidthPx;
        if (typeof w === "number" && isFinite(w) && w > 0) {
          img.style.width = String(Math.max(56, Math.round(w * scale))) + "px";
        } else {
          img.style.width = "96px";
        }
        img.style.maxWidth = "100%";
        row.appendChild(img);
      });
      wrap.appendChild(row);

      wrongPreviewEl.appendChild(wrap);
    }

    function setImage(rel) {
      if (!imgEl) return;
      imgEl.src = resolveUrl(rel.replace(/^\//, ""));
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
        th.src = resolveUrl(String(im.image).replace(/^\//, ""));
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

    function labelForSlug(slug) {
      if (!slug) return "";
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") return slug;
      var latin = !isMissingValue(rec.latin) ? String(rec.latin).trim() : "";
      var dutch = !isMissingValue(rec.dutch) ? String(rec.dutch).trim() : "";
      if (latin && dutch) return latin + " (" + dutch + ")";
      return latin || dutch || slug;
    }

    function exampleForSlug(slug) {
      return pickImageForSlug(slug, false);
    }

    function imagesForSlug(slug) {
      if (!slug) return [];
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") return [];
      var imgs = rec.images;
      if (!Array.isArray(imgs) || imgs.length === 0) return [];
      var out = [];
      imgs.forEach(function (im) {
        if (!im || typeof im.path !== "string" || !im.path) return;
        var path = String(im.path).replace(/^\//, "").replace(/^\.\//, "");
        var w = im.width_px;
        if (!(typeof w === "number" && isFinite(w) && w > 0)) {
          w = rec.display_width_px;
        }
        out.push({
          image: path,
          imageWidthPx: typeof w === "number" && isFinite(w) && w > 0 ? w : null,
        });
      });
      return out;
    }

    function seenImagesForSlug(slug) {
      if (!slug) return [];
      var row = state.progress[slug];
      if (!row || typeof row !== "object" || !Array.isArray(row.seenImages)) return [];
      return row.seenImages;
    }

    function markImageSeen(slug, path) {
      if (!slug || !path) return;
      var row = state.progress[slug];
      if (!row || typeof row !== "object") {
        row = { box: 0, seen: 0, seenImages: [] };
      }
      var seenImages = Array.isArray(row.seenImages) ? row.seenImages.slice() : [];
      if (seenImages.indexOf(path) === -1) seenImages.push(path);
      row.seenImages = seenImages;
      if (typeof row.box !== "number") row.box = boxForSlug(slug);
      if (typeof row.seen !== "number") row.seen = 0;
      state.progress[slug] = row;
      writeLocalJson(LS_PROGRESS, state.progress);
    }

    function pickImageForSlug(slug, preferUnseen) {
      var imgs = imagesForSlug(slug);
      if (!imgs.length) return null;
      if (preferUnseen) {
        var seen = seenImagesForSlug(slug);
        var unseen = imgs.filter(function (im) {
          return seen.indexOf(im.image) === -1;
        });
        if (unseen.length) return pickRandom(unseen);
      }
      return pickRandom(imgs);
    }

    function featureProgressKey(slug) {
      return "feat|" + slug;
    }

    function controlledForSlug(slug) {
      if (!slug) return null;
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") return null;
      var c = rec.controlled;
      if (!c || typeof c !== "object") return null;
      if (!c.vorm || !c.sculptuur || !c.apertuur || !c.grootteklasse) return null;
      return c;
    }

    function featureLabel(field, code) {
      var map = FEATURE_VOCAB[field] || {};
      return map[code] || code;
    }

    function pairKey(a, b) {
      return a <= b ? a + "|" + b : b + "|" + a;
    }

    function usableLookalikeNote(note) {
      if (typeof note !== "string") return "";
      var t = note.trim();
      if (!t) return "";
      if (t.toLowerCase() === "user: lookalike") return "";
      if (t.toLowerCase().indexOf("lookalike (") === 0) return "";
      return t;
    }

    function recordConfusion(shownSlug, chosenSlug, imagePath) {
      if (!shownSlug || !chosenSlug || shownSlug === chosenSlug) return;
      if (!Array.isArray(state.confusions)) state.confusions = [];
      state.confusions.push({
        at: new Date().toISOString().slice(0, 10),
        shown: shownSlug,
        chosen: chosenSlug,
        image: imagePath || null,
      });
      if (state.confusions.length > 200) {
        state.confusions = state.confusions.slice(-200);
      }
      writeLocalJson(LS_CONFUSIONS, state.confusions);
    }

    function buildLookalikePool() {
      var want = state.lookalikeDiff || "all";
      state.lookalikePool = (state.lookalikePairs || []).filter(function (p) {
        if (!p || !p.a || !p.b) return false;
        if (want === "all") return true;
        return p.difficulty === want;
      });
      return state.lookalikePool;
    }

    function buildFeaturePool() {
      var slugs = [];
      var lv = clampLevel(state.level || 1);
      function consider(slug, rec, requireAboveL1) {
        if (!rec || typeof rec !== "object") return;
        var rank = rec.learning_priority_rank;
        var hasRank = typeof rank === "number" && isFinite(rank) && rank > 0;
        if (lv <= 1) {
          if (!(hasRank && rank <= LEVEL1_MAX_RANK)) return;
        } else if (lv === 2) {
          if (!hasRank) return;
          if (requireAboveL1 && !(rank > LEVEL1_MAX_RANK)) return;
        }
        if (!controlledForSlug(slug)) return;
        if (!imagesForSlug(slug).length) return;
        slugs.push(slug);
      }
      Object.keys(state.pollen || {}).forEach(function (slug) {
        consider(slug, state.pollen[slug], lv === 2);
      });
      // Niveau 2/3: if no controlled+images yet for that tier, fall back so MCQ options still appear.
      if (!slugs.length && lv >= 2) {
        Object.keys(state.pollen || {}).forEach(function (slug) {
          consider(slug, state.pollen[slug], false);
        });
      }
      state.featurePool = slugs;
      return state.featurePool;
    }

    function taxonInNameLevel(slug, rec, level) {
      if (!rec || typeof rec !== "object") return false;
      if (!imagesForSlug(slug).length) return false;
      var rank = rec.learning_priority_rank;
      var hasRank = typeof rank === "number" && isFinite(rank) && rank > 0;
      if (level <= 1) return hasRank && rank <= LEVEL1_MAX_RANK;
      if (level === 2) return hasRank && rank > LEVEL1_MAX_RANK;
      return true;
    }

    function buildNamePool() {
      var lv = clampLevel(state.level || 1);
      var slugs = [];
      Object.keys(state.pollen || {}).forEach(function (slug) {
        if (taxonInNameLevel(slug, state.pollen[slug], lv)) slugs.push(slug);
      });
      state.namePool = slugs;
      return state.namePool;
    }

    function apertureFamily(slug) {
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") return "";
      var raw = "";
      var c = rec.controlled;
      if (c && typeof c === "object" && c.apertuur) raw = String(c.apertuur);
      else if (!isMissingValue(rec.aperture)) raw = String(rec.aperture);
      raw = raw.toLowerCase();
      if (!raw) return "";
      if (raw.indexOf("fenestra") >= 0) return "fenestraat";
      if (raw.indexOf("inapertur") >= 0) return "inaperturaat";
      if (raw.indexOf("tetrade") >= 0 || raw.indexOf("tetrad") >= 0) return "tetrade";
      if (raw.indexOf("polyade") >= 0 || raw.indexOf("polyad") >= 0) return "polyade";
      if (raw.indexOf("colpor") >= 0) return "colpor";
      if (raw.indexOf("colp") >= 0) return "colp";
      if (raw.indexOf("por") >= 0) return "por";
      var m = raw.match(/[a-z]+/);
      return m ? m[0] : "";
    }

    function pickNameDistractors(correctSlug, count) {
      var need = typeof count === "number" && count > 0 ? count : 3;
      var used = {};
      used[correctSlug] = true;
      var out = [];
      function tryAdd(slug) {
        if (!slug || used[slug]) return false;
        if (!imagesForSlug(slug).length) return false;
        used[slug] = true;
        out.push(slug);
        return true;
      }
      var neigh =
        (state.morphNeighbours && state.morphNeighbours[correctSlug]) || [];
      var i;
      for (i = 0; i < neigh.length && out.length < need; i += 1) {
        tryAdd(neigh[i]);
      }
      if (out.length < need) {
        var fam = apertureFamily(correctSlug);
        if (fam) {
          var sameAp = [];
          Object.keys(state.pollen || {}).forEach(function (slug) {
            if (used[slug]) return;
            if (!imagesForSlug(slug).length) return;
            if (apertureFamily(slug) === fam) sameAp.push(slug);
          });
          sameAp = shuffle(sameAp);
          while (out.length < need && sameAp.length) tryAdd(sameAp.pop());
        }
      }
      if (out.length < need) {
        var levelPool = shuffle((state.namePool || []).slice());
        while (out.length < need && levelPool.length) tryAdd(levelPool.pop());
      }
      if (out.length < need) {
        var any = shuffle(Object.keys(state.pollen || {}));
        while (out.length < need && any.length) tryAdd(any.pop());
      }
      return out;
    }

    function itemInLevel(item, level) {
      if (level >= 3) return true;
      var slug = slugForCurrentItem(item);
      if (!slug) return false;
      var rec = state.pollen[slug];
      if (!rec || typeof rec !== "object") return false;
      var rank = rec.learning_priority_rank;
      var hasRank = typeof rank === "number" && isFinite(rank) && rank > 0;
      if (!hasRank) return false;
      // Do not use monofloral_honey_page for quiz tiers (that flag marks honey pages, many taxa).
      if (level <= 1) return rank <= LEVEL1_MAX_RANK;
      return true;
    }

    function buildPool(level) {
      var lv = clampLevel(level);
      state.level = lv;
      state.pool = (state.items || []).filter(function (it) {
        return itemInLevel(it, lv);
      });
      return state.pool;
    }

    function boxForSlug(slug) {
      if (!slug) return 0;
      var row = state.progress[slug];
      if (!row || typeof row !== "object") return 0;
      var b = Number(row.box);
      if (!isFinite(b) || b < 0) return 0;
      if (b > BOX_MAX) return BOX_MAX;
      return Math.floor(b);
    }

    function recordAnswer(slug, correct, imagePath) {
      if (!slug) return;
      var row = state.progress[slug];
      if (!row || typeof row !== "object") {
        row = { box: 0, seen: 0, seenImages: [] };
      }
      var box = boxForSlug(slug);
      var seen = Number(row.seen);
      if (!isFinite(seen) || seen < 0) seen = 0;
      seen += 1;
      if (correct) {
        box = Math.min(BOX_MAX, box + 1);
      } else {
        box = 0;
      }
      var seenImages = Array.isArray(row.seenImages) ? row.seenImages.slice() : [];
      if (imagePath && seenImages.indexOf(imagePath) === -1) {
        seenImages.push(imagePath);
      }
      state.progress[slug] = { box: box, seen: seen, seenImages: seenImages };
      writeLocalJson(LS_PROGRESS, state.progress);
      renderProgress();
    }

    function pickWeighted(pool) {
      if (!Array.isArray(pool) || pool.length === 0) return null;
      var weights = [];
      var total = 0;
      for (var i = 0; i < pool.length; i += 1) {
        var slug = slugForCurrentItem(pool[i]);
        var w = BOX_MAX + 1 - boxForSlug(slug);
        if (w < 1) w = 1;
        weights.push(w);
        total += w;
      }
      var r = Math.random() * total;
      var acc = 0;
      for (var j = 0; j < pool.length; j += 1) {
        acc += weights[j];
        if (r < acc) return pool[j];
      }
      return pool[pool.length - 1];
    }

    function pickWeightedSlug(pool, keyFn) {
      if (!Array.isArray(pool) || pool.length === 0) return null;
      var weights = [];
      var total = 0;
      for (var i = 0; i < pool.length; i += 1) {
        var key = keyFn(pool[i]);
        var w = BOX_MAX + 1 - boxForSlug(key);
        if (w < 1) w = 1;
        weights.push(w);
        total += w;
      }
      var r = Math.random() * total;
      var acc = 0;
      for (var j = 0; j < pool.length; j += 1) {
        acc += weights[j];
        if (r < acc) return pool[j];
      }
      return pool[pool.length - 1];
    }

    function pickWeightedLookalike(pool) {
      return pickWeightedSlug(pool, function (p) {
        return pairKey(p.a, p.b);
      });
    }

    function syncModePanels() {
      var i;
      var hideNormal = !!state.lookalikeMode || !!state.kenmerkenMode;
      for (i = 0; i < normalPanels.length; i += 1) {
        normalPanels[i].hidden = hideNormal;
      }
      if (lookalikePanelEl) lookalikePanelEl.hidden = !state.lookalikeMode;
      if (kenmerkenPanelEl) kenmerkenPanelEl.hidden = !state.kenmerkenMode;
    }

    function renderProgress() {
      if (!progressEl) return;
      if (state.kenmerkenMode) {
        var fPool = state.featurePool || [];
        var masteredF = 0;
        fPool.forEach(function (slug) {
          if (boxForSlug(featureProgressKey(slug)) >= BOX_MAX) masteredF += 1;
        });
        var kenLabel =
          state.level === 2
            ? "overige pollen"
            : state.level === 3
              ? "minder frequent"
              : "vaak in NL-honing";
        progressEl.innerHTML =
          '<span class="md-typeset">' +
          "<strong>Kenmerken (" +
          esc(kenLabel) +
          ")</strong>: " +
          esc(String(masteredF)) +
          "/" +
          esc(String(fPool.length)) +
          " taxa in hoogste box</span>";
        return;
      }
      if (state.lookalikeMode) {
        var laPool = state.lookalikePool || [];
        var masteredLa = 0;
        laPool.forEach(function (p) {
          if (boxForSlug(pairKey(p.a, p.b)) >= BOX_MAX) masteredLa += 1;
        });
        var diffLabel =
          state.lookalikeDiff === "easy"
            ? "makkelijk"
            : state.lookalikeDiff === "moderate"
              ? "matig"
              : state.lookalikeDiff === "difficult"
                ? "moeilijk"
                : "alle klassen";
        progressEl.innerHTML =
          '<span class="md-typeset">' +
          "<strong>Lookalike (" +
          esc(diffLabel) +
          ")</strong>: " +
          esc(String(masteredLa)) +
          "/" +
          esc(String(laPool.length)) +
          " paren in hoogste box</span>";
        return;
      }
      var pool = state.namePool || [];
      var total = pool.length;
      var mastered = 0;
      pool.forEach(function (s) {
        if (boxForSlug(s) >= BOX_MAX) mastered += 1;
      });
      var levelLabel =
        state.level === 1
          ? "Vaak in NL-honing"
          : state.level === 2
            ? "Overige prioriteit"
            : "Alles";
      progressEl.innerHTML =
        '<span class="md-typeset">' +
        "<strong>Naam (" +
        esc(levelLabel) +
        ")</strong>: " +
        esc(String(mastered)) +
        "/" +
        esc(String(total)) +
        " taxa in hoogste box</span>";
    }

    function applyLevel(raw, restart) {
      var force = (lockLevel || "").trim().toLowerCase();
      var parsed = parseLevelValue(lockLevel || raw);
      if (force.indexOf("kenmerken") === 0) {
        parsed.kenmerkenMode = true;
        parsed.lookalikeMode = false;
      } else if (force.indexOf("lookalike") === 0) {
        parsed.kenmerkenMode = false;
        parsed.lookalikeMode = true;
      }
      state.kenmerkenMode = !!parsed.kenmerkenMode;
      state.lookalikeMode = !!parsed.lookalikeMode;
      state.lookalikeDiff = parsed.lookalikeDiff;
      state.level = parsed.level;
      if (!lockLevel) {
        writeLocalJson(LS_LEVEL, parsed.value);
      }
      if (levelEl && !lockLevel) levelEl.value = parsed.value;
      syncModePanels();
      if (state.lookalikeMode) {
        buildLookalikePool();
      } else if (state.kenmerkenMode) {
        buildFeaturePool();
      } else {
        buildNamePool();
      }
      renderProgress();
      if (restart) newQuestion();
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
      if (k === "waarneming") return "Waarneming.nl";
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
      var sculptureShown = morphWithVisibility(rec.sculpture, rec.sculpture_visibility);
      if (sculptureShown) {
        addRow(dl, "Sculptuur", esc(sculptureShown));
      }
      var ornamentShown = morphWithVisibility(
        rec.ornamentation,
        rec.ornamentation_visibility
      );
      if (ornamentShown) {
        addRow(dl, "Ornamentatie", esc(ornamentShown));
      }
      var apertureShown = morphWithVisibility(rec.aperture, rec.aperture_visibility);
      if (apertureShown) {
        addRow(dl, "Apertuur", esc(apertureShown));
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

      if (state.lookalikeMode && state.currentLookalike) {
        var la = state.currentLookalike;
        if (la.phase === "rule" && la.ruleText) {
          opts.push({ text: la.ruleText, correct: true, kind: "rule" });
          var distractors = shuffle(
            [
              "Grootte alleen is genoeg",
              "Familie-naam volstaat",
              "Sculptuur is identiek; negeer apertuur",
              "Vorm in poolaanzicht is irrelevant",
            ].filter(function (t) {
              return t !== la.ruleText;
            })
          ).slice(0, 3);
          distractors.forEach(function (t) {
            opts.push({ text: t, correct: false, kind: "rule" });
          });
          opts = shuffle(opts);
        } else {
          var correctLabel = labelForSlug(la.shownSlug) || la.shownSlug;
          var wrongLabel = labelForSlug(la.partnerSlug) || la.partnerSlug;
          var wrongEx = pickImageForSlug(la.partnerSlug, false);
          opts.push({
            text: correctLabel,
            correct: true,
            kind: "name",
            image: la.image,
            imageWidthPx: la.imageWidthPx,
            chosenSlug: la.shownSlug,
          });
          opts.push({
            text: wrongLabel,
            correct: false,
            kind: "name",
            image: wrongEx ? wrongEx.image : null,
            imageWidthPx: wrongEx ? wrongEx.imageWidthPx : null,
            chosenSlug: la.partnerSlug,
          });
          opts = shuffle(opts).slice(0, 2);
        }
      } else if (state.currentName && state.currentName.slug) {
        var cn = state.currentName;
        var rightText = labelForSlug(cn.slug) || cn.slug;
        opts.push({
          text: rightText,
          correct: true,
          kind: "name",
          image: cn.image,
          imageWidthPx: cn.imageWidthPx,
          chosenSlug: cn.slug,
        });
        pickNameDistractors(cn.slug, 3).forEach(function (dSlug) {
          var dex = pickImageForSlug(dSlug, false);
          opts.push({
            text: labelForSlug(dSlug) || dSlug,
            correct: false,
            kind: "name",
            image: dex ? dex.image : null,
            imageWidthPx: dex ? dex.imageWidthPx : null,
            chosenSlug: dSlug,
          });
        });
        opts = shuffle(opts).slice(0, 4);
      } else {
        var anchorSlug = slugForCurrentItem(item);
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
          var pool = (state.pool && state.pool.length ? state.pool : state.items || [])
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
              var ex2 = state.endpointToExample[t] || null;
              opts.push({ text: t, correct: false });
              opts[opts.length - 1].image = ex2 ? ex2.image : null;
              opts[opts.length - 1].imageWidthPx = ex2 ? ex2.imageWidthPx : null;
            }
          }
        }
        opts = shuffle(opts).slice(0, 4);
      }

      opts.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "md-button";
        b.innerHTML = esc(o.text);
        b.style.textAlign = "left";
        b.style.display = "flex";
        b.style.justifyContent = "flex-start";
        b.style.whiteSpace = "normal";
        b.addEventListener("click", function () {
          if (state.lookalikeMode && state.currentLookalike && o.kind === "rule") {
            setMcqStatus(
              o.correct
                ? "<strong>Juist.</strong> Nu de naam."
                : "<strong>Onjuist.</strong> Lees de beslissingsregel opnieuw."
            );
            if (o.correct) {
              state.currentLookalike.phase = "name";
              if (lookalikePromptEl) {
                lookalikePromptEl.textContent = "Welke naam hoort bij dit beeld?";
              }
              buildMcq(null);
            }
            return;
          }
          var correctNameLabel = "";
          if (state.currentName && state.currentName.slug) {
            correctNameLabel = labelForSlug(state.currentName.slug) || state.currentName.slug;
          } else if (state.lookalikeMode && state.currentLookalike) {
            correctNameLabel =
              labelForSlug(state.currentLookalike.shownSlug) ||
              state.currentLookalike.shownSlug;
          }
          if (state.currentName && state.currentName.slug) {
            setMcqStatus(
              o.correct
                ? "<strong>Juist.</strong> " + esc(correctNameLabel)
                : "<strong>Onjuist.</strong> Juiste naam: " +
                    esc(correctNameLabel) +
                    ". Vergelijk met het beeld hieronder."
            );
          } else {
            setMcqStatus(
              o.correct
                ? "<strong>Juist.</strong>"
                : "<strong>Onjuist.</strong> Vergelijk met het beeld hieronder."
            );
          }
          var progressSlug =
            state.lookalikeMode && state.currentLookalike
              ? state.currentLookalike.pairKey
              : state.currentName && state.currentName.slug
                ? state.currentName.slug
                : slugForCurrentItem(state.current);
          var imagePath =
            state.lookalikeMode && state.currentLookalike
              ? state.currentLookalike.image
              : state.currentName && state.currentName.image
                ? state.currentName.image
                : state.current
                  ? state.current.image
                  : null;
          recordAnswer(progressSlug, !!o.correct, imagePath);
          if (
            state.lookalikeMode &&
            state.currentLookalike &&
            !o.correct &&
            o.chosenSlug
          ) {
            recordConfusion(
              state.currentLookalike.shownSlug,
              o.chosenSlug,
              state.currentLookalike.image
            );
          }
          if (o.correct) {
            clearWrongPreview();
            renderInfo(
              state.lookalikeMode && state.currentLookalike
                ? state.currentLookalike.shownSlug
                : state.currentName && state.currentName.slug
                  ? state.currentName.slug
                  : slugForCurrentItem(state.current)
            );
          } else {
            clearInfo();
            showWrongPreview(o);
          }
        });
        mcqEl.appendChild(b);
      });
      if (mcqEl) mcqEl.hidden = false;
    }

    function revealFeatureName() {
      var cf = state.currentFeature;
      if (!cf) return;
      var need = FEATURE_FIELDS.length + 1;
      var allOk = state.featureCorrect >= need;
      recordAnswer(featureProgressKey(cf.slug), allOk, cf.image);
      markImageSeen(cf.slug, cf.image);
      var ctrl = controlledForSlug(cf.slug) || {};
      var bits = FEATURE_FIELDS.map(function (f) {
        return featureLabel(f, ctrl[f]);
      });
      setStatus(
        '<p class="admonition ' +
          (allOk ? "success" : "warning") +
          '"><strong>' +
          esc(labelForSlug(cf.slug) || cf.slug) +
          "</strong><br/>" +
          esc(bits.join(" · ")) +
          (allOk ? "" : "<br/>Niet alles juist.") +
          "</p>"
      );
      renderInfo(cf.slug);
      if (mcqEl) {
        mcqEl.hidden = true;
        mcqEl.replaceChildren();
      }
      setMcqStatus("");
      if (featurePromptEl) featurePromptEl.textContent = "Kies Volgende.";
    }

    function buildFeatureNameMcq() {
      if (!mcqEl || !state.currentFeature) return;
      mcqEl.replaceChildren();
      var cf = state.currentFeature;
      var correctSlug = cf.slug;
      var correctLabel = labelForSlug(correctSlug) || correctSlug;
      var opts = [{ slug: correctSlug, text: correctLabel, correct: true }];
      var pool = shuffle(
        (state.featurePool || []).filter(function (s) {
          return s && s !== correctSlug;
        })
      );
      while (opts.length < 4 && pool.length) {
        var s = pool.pop();
        var lab = labelForSlug(s) || s;
        if (
          !opts.some(function (o) {
            return o.text === lab || o.slug === s;
          })
        ) {
          opts.push({ slug: s, text: lab, correct: false });
        }
      }
      opts = shuffle(opts);
      if (featurePromptEl) {
        featurePromptEl.textContent = "Welke naam hoort bij dit beeld?";
      }
      opts.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "md-button";
        b.innerHTML = esc(o.text);
        b.style.textAlign = "left";
        b.style.whiteSpace = "normal";
        b.addEventListener("click", function () {
          if (o.correct) {
            state.featureCorrect += 1;
            setMcqStatus("<strong>Juist.</strong>");
          } else {
            setMcqStatus(
              "<strong>Onjuist.</strong> Juist was: " + esc(correctLabel)
            );
          }
          revealFeatureName();
        });
        mcqEl.appendChild(b);
      });
      mcqEl.hidden = false;
    }

    function buildFeatureMcq() {
      if (!mcqEl || !state.currentFeature) return;
      mcqEl.replaceChildren();
      var cf = state.currentFeature;
      var field = FEATURE_FIELDS[state.featureStep];
      if (!field) {
        buildFeatureNameMcq();
        return;
      }
      var ctrl = controlledForSlug(cf.slug);
      var correctCode = ctrl[field];
      var vocab = FEATURE_VOCAB[field] || {};
      var codes = Object.keys(vocab);
      if (correctCode && codes.indexOf(correctCode) === -1) {
        codes = codes.concat([correctCode]);
      }
      var opts = shuffle(
        codes.map(function (c) {
          return { code: c, correct: c === correctCode };
        })
      );
      if (featurePromptEl) {
        var titles = {
          vorm: "Welke vorm zie je?",
          apertuur: "Welke apertuur zie je?",
          sculptuur: "Welke sculptuur zie je?",
          grootteklasse: "Welke grootteklasse schat je? (true-scale beeld)",
        };
        featurePromptEl.textContent =
          titles[field] || "Welk kenmerk zie je?";
      }
      opts.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "md-button";
        b.innerHTML = esc(featureLabel(field, o.code));
        b.style.textAlign = "left";
        b.style.whiteSpace = "normal";
        b.addEventListener("click", function () {
          if (o.correct) {
            state.featureCorrect += 1;
            setMcqStatus("<strong>Juist.</strong>");
          } else {
            setMcqStatus(
              "<strong>Onjuist.</strong> Juist was: " +
                esc(featureLabel(field, correctCode))
            );
          }
          state.featureStep += 1;
          if (state.featureStep >= FEATURE_FIELDS.length) {
            buildFeatureNameMcq();
          } else {
            buildFeatureMcq();
          }
        });
        mcqEl.appendChild(b);
      });
      mcqEl.hidden = false;
    }

    function newFeatureQuestion() {
      state.current = null;
      state.currentLookalike = null;
      state.currentFeature = null;
      state.diverged = false;
      state.expectedPath = null;
      state.expectedStepIdx = 0;
      state.pendingJump = false;
      state.selectedKeyJsonUrl = null;
      if (keyWrapEl) keyWrapEl.replaceChildren();
      var pool = state.featurePool || [];
      var slug = pickWeightedSlug(pool, featureProgressKey);
      if (!slug) {
        setStatus(
          '<p class="admonition warning"><strong>Geen kenmerken-taxa beschikbaar.</strong> Vul controlled-features + beelden voor dit niveau.</p>'
        );
        if (mcqEl) {
          mcqEl.hidden = true;
          mcqEl.replaceChildren();
        }
        setMcqStatus("");
        clearWrongPreview();
        clearInfo();
        clearGallery();
        renderProgress();
        return;
      }
      var ex = pickImageForSlug(slug, true);
      if (!ex || !ex.image) {
        setStatus(
          '<p class="admonition warning"><strong>Geen beeld voor dit taxon.</strong> Probeer Volgende.</p>'
        );
        renderProgress();
        return;
      }
      state.currentFeature = {
        slug: slug,
        image: ex.image,
        imageWidthPx: ex.imageWidthPx,
      };
      state.featureStep = 0;
      state.featureCorrect = 0;
      if (inputEl) inputEl.value = "";
      setStatus("");
      setImage(ex.image);
      applyImageWidth({ imageWidthPx: ex.imageWidthPx });
      clearGallery();
      clearWrongPreview();
      clearInfo();
      setMcqStatus("");
      if (pathEl) {
        pathEl.hidden = true;
        pathEl.replaceChildren();
      }
      if (jumpEl) jumpEl.hidden = true;
      if (backtrackEl) backtrackEl.hidden = true;
      buildFeatureMcq();
      renderProgress();
    }

    function newLookalikeQuestion() {
      var pool = state.lookalikePool || [];
      var pair = pickWeightedLookalike(pool);
      state.current = null;
      state.currentFeature = null;
      state.currentLookalike = null;
      state.diverged = false;
      state.expectedPath = null;
      state.expectedStepIdx = 0;
      state.pendingJump = false;
      state.selectedKeyJsonUrl = null;
      if (keyWrapEl) keyWrapEl.replaceChildren();
      if (!pair) {
        setStatus(
          '<p class="admonition warning"><strong>Geen lookalike-paren voor deze klasse.</strong> Kies Alle of een andere lookalike-optie.</p>'
        );
        if (mcqEl) {
          mcqEl.hidden = true;
          mcqEl.replaceChildren();
        }
        setMcqStatus("");
        clearWrongPreview();
        clearInfo();
        clearGallery();
        renderProgress();
        return;
      }
      var showA = Math.random() < 0.5;
      var shownSlug = showA ? pair.a : pair.b;
      var partnerSlug = showA ? pair.b : pair.a;
      var pk = pairKey(pair.a, pair.b);
      var preferUnseen = boxForSlug(pk) >= 3;
      var ex = pickImageForSlug(shownSlug, preferUnseen);
      if (!ex || !ex.image) {
        ex = pickImageForSlug(partnerSlug, preferUnseen);
        if (ex && ex.image) {
          var swap = shownSlug;
          shownSlug = partnerSlug;
          partnerSlug = swap;
        }
      }
      if (!ex || !ex.image) {
        setStatus(
          '<p class="admonition warning"><strong>Geen lookalike-beeld beschikbaar voor dit paar.</strong> Probeer Volgende.</p>'
        );
        renderProgress();
        return;
      }
      var ruleText = usableLookalikeNote(pair.note);
      var phase = ruleText ? "rule" : "name";
      state.currentLookalike = {
        a: pair.a,
        b: pair.b,
        shownSlug: shownSlug,
        partnerSlug: partnerSlug,
        pairKey: pk,
        difficulty: pair.difficulty || null,
        note: pair.note || null,
        ruleText: ruleText,
        phase: phase,
        image: ex.image,
        imageWidthPx: ex.imageWidthPx,
      };
      markImageSeen(shownSlug, ex.image);
      if (inputEl) inputEl.value = "";
      setStatus("");
      setImage(ex.image);
      applyImageWidth({ imageWidthPx: ex.imageWidthPx });
      clearGallery();
      clearWrongPreview();
      clearInfo();
      setMcqStatus("");
      if (lookalikePromptEl) {
        lookalikePromptEl.textContent = ruleText
          ? "Welke beslissingsregel past bij dit lookalike-paar?"
          : "Welke naam hoort bij dit beeld?";
      }
      if (pathEl) {
        pathEl.hidden = true;
        pathEl.replaceChildren();
      }
      if (jumpEl) jumpEl.hidden = true;
      if (backtrackEl) backtrackEl.hidden = true;
      buildMcq(null);
      if (mcqEl) mcqEl.hidden = false;
      renderProgress();
    }

    function newNameQuestion() {
      state.currentLookalike = null;
      state.currentFeature = null;
      var pool = state.namePool || [];
      if (!pool.length) {
        state.currentName = null;
        state.current = null;
        setStatus(
          '<p class="admonition warning"><strong>Geen taxa met beelden in dit niveau.</strong></p>'
        );
        if (mcqEl) {
          mcqEl.hidden = true;
          mcqEl.replaceChildren();
        }
        renderProgress();
        return;
      }
      var slug = pickWeightedSlug(pool, function (s) {
        return s;
      });
      if (!slug) {
        setStatus(
          '<p class="admonition warning"><strong>Geen quiz-taxon beschikbaar.</strong></p>'
        );
        renderProgress();
        return;
      }
      var preferUnseen = boxForSlug(slug) >= 3;
      var ex = pickImageForSlug(slug, preferUnseen);
      if (!ex || !ex.image) {
        setStatus(
          '<p class="admonition warning"><strong>Geen beeld voor dit taxon.</strong> Probeer Volgende.</p>'
        );
        renderProgress();
        return;
      }
      state.currentName = {
        slug: slug,
        image: ex.image,
        imageWidthPx: ex.imageWidthPx,
      };
      state.current = {
        image: ex.image,
        imageWidthPx: ex.imageWidthPx,
      };
      markImageSeen(slug, ex.image);
      if (inputEl) inputEl.value = "";
      setStatus(
        '<p class="admonition info"><strong>Welke naam hoort bij dit beeld?</strong></p>'
      );
      setImage(ex.image);
      applyImageWidth({ imageWidthPx: ex.imageWidthPx });
      clearGallery();
      clearWrongPreview();
      clearInfo();
      setMcqStatus("");
      if (pathEl) {
        pathEl.hidden = true;
        pathEl.replaceChildren();
      }
      if (jumpEl) jumpEl.hidden = true;
      if (backtrackEl) backtrackEl.hidden = true;
      buildMcq(null);
      if (mcqEl) mcqEl.hidden = false;
      renderProgress();
    }

    function newQuestion() {
      if (state.kenmerkenMode) {
        newFeatureQuestion();
        return;
      }
      if (state.lookalikeMode) {
        newLookalikeQuestion();
        return;
      }
      newNameQuestion();
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
      var slug = slugForCurrentItem(state.current);
      if (!guess) {
        setStatus('<p class="admonition warning"><strong>Geen antwoord ingevuld.</strong></p>');
        return;
      }
      if (strict && guess === strict) {
        setStatus('<p class="admonition success"><strong>Correct (strict).</strong></p>');
        recordAnswer(slug, true);
        return;
      }
      for (var i = 0; i < accepted.length; i += 1) {
        if (accepted[i].t && guess === accepted[i].t) {
          var g = accepted[i].g === "partial" ? "Gedeeltelijk correct." : "Correct (acceptabel).";
          setStatus('<p class="admonition info"><strong>' + esc(g) + "</strong></p>");
          recordAnswer(slug, accepted[i].g !== "partial");
          return;
        }
      }
      setStatus('<p class="admonition error"><strong>Onjuist.</strong></p>');
      recordAnswer(slug, false);
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
      state.expectedStepIdx = 0;
      state.diverged = false;
      if (backtrackEl) backtrackEl.hidden = true;
      if (jumpEl) jumpEl.hidden = true;
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
      rootEl.id = "pollentabel-root";
      rootEl.setAttribute("data-json-url", resolveUrl(normUrl));
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
      var idx = state.expectedStepIdx || 0;
      var exp = state.expectedPath[idx];
      if (!exp) return;
      if (String(ev.detail && ev.detail.stepId) !== String(exp.stepId)) return;
      var ok =
        String(ev.detail && ev.detail.choiceLabel) === String(exp.choiceLabel) ||
        Number(ev.detail && ev.detail.choiceIdx) === Number(exp.choiceIdx);
      if (ok) {
        state.expectedStepIdx = idx + 1;
        state.diverged = false;
        if (backtrackEl) backtrackEl.hidden = true;
        if (jumpEl) jumpEl.hidden = true;
        return;
      }
      state.diverged = true;
      if (jumpEl) jumpEl.hidden = false;
      if (backtrackEl) backtrackEl.hidden = false;
      var charHint = exp.choiceLabel ? String(exp.choiceLabel) : "";
      setStatus(
        '<p class="admonition warning"><strong>Afwijking bij stap ' +
          esc(exp.stepId) +
          ".</strong> Dit kenmerk werd gevraagd: <em>" +
          esc(charHint || "(geen label)") +
          "</em>. Gebruik <strong>Eén stap terug</strong> en kies opnieuw, of spring naar het verwachte pad.</p>"
      );
    }

    function backtrackOneStep() {
      var keyRoot = keyWrapEl ? keyWrapEl.querySelector("#pollentabel-root") : null;
      if (!keyRoot) return;
      var ctl = keyRoot.__pollentabelController;
      if (!ctl || typeof ctl.stepBack !== "function") {
        setStatus(
          '<p class="admonition warning"><strong>Terugstap niet beschikbaar.</strong> Gebruik de knop in de sleutel of spring naar het pad.</p>'
        );
        return;
      }
      if (ctl.stepBack()) {
        if (state.expectedStepIdx > 0) state.expectedStepIdx -= 1;
        state.diverged = false;
        if (backtrackEl) backtrackEl.hidden = true;
        if (jumpEl) jumpEl.hidden = true;
        var exp = state.expectedPath && state.expectedPath[state.expectedStepIdx];
        var hint = exp && exp.choiceLabel ? String(exp.choiceLabel) : "";
        setStatus(
          '<p class="admonition info"><strong>Eén stap terug.</strong> Probeer opnieuw' +
            (hint ? ": <em>" + esc(hint) + "</em>" : ".") +
            "</p>"
        );
      }
    }

    function tryJumpNow() {
      var keyRoot = keyWrapEl ? keyWrapEl.querySelector("#pollentabel-root") : null;
      if (!keyRoot) return false;
      var ctl = keyRoot.__pollentabelController;
      if (!ctl || !state.expectedPath || state.expectedPath.length === 0) return false;

      ctl.reset();
      for (var i = 0; i < state.expectedPath.length; i += 1) {
        var exp = state.expectedPath[i];
        if (!exp) continue;
        // Follow the key normally so its back-stack is populated.
        ctl.chooseByIndex(exp.choiceIdx);
      }
      state.expectedStepIdx = state.expectedPath.length;
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
    if (backtrackEl) {
      backtrackEl.addEventListener("click", backtrackOneStep);
    }
    if (exportConfusionsEl) {
      exportConfusionsEl.addEventListener("click", function () {
        var payload = {
          exported_at: new Date().toISOString(),
          confusions: state.confusions || [],
        };
        var text = JSON.stringify(payload, null, 2);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(
            function () {
              setStatus(
                '<p class="admonition success"><strong>Verwarringen gekopieerd.</strong> ' +
                  esc(String((state.confusions || []).length)) +
                  " items in klembord (plak in je logboek / review).</p>"
              );
            },
            function () {
              setStatus(
                '<p class="admonition warning"><strong>Klembord mislukt.</strong> Open de console voor JSON.</p>'
              );
              console.log(text);
            }
          );
        } else {
          console.log(text);
          setStatus(
            '<p class="admonition info"><strong>JSON in console.</strong> Klembord niet beschikbaar.</p>'
          );
        }
      });
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
    if (levelEl && !lockLevel) {
      levelEl.addEventListener("change", function () {
        applyLevel(levelEl.value, true);
      });
    }

    loadAll()
      .then(function (all) {
        state.keys = buildKeyOptions(all.keys || {});
        state.items = (all.items && all.items.items) || [];
        var pollenRoot = all.pollen;
        state.pollen =
          pollenRoot && typeof pollenRoot === "object" && !Array.isArray(pollenRoot) ? pollenRoot : {};
        state.imageToSlug = buildImageToSlugFromPollen(state.pollen);
        state.morphNeighbours = {};
        var mn = all.morphNeighbours || {};
        if (mn && typeof mn === "object" && mn.neighbours && typeof mn.neighbours === "object") {
          state.morphNeighbours = mn.neighbours;
        }
        state.lookalikePairs = [];
        var la = all.lookalikes || {};
        (la.pairs || []).forEach(function (p) {
          if (!p || typeof p.a !== "string" || typeof p.b !== "string") return;
          var diff =
            typeof p.difficulty === "string" && LOOKALIKE_DIFFS[p.difficulty]
              ? p.difficulty
              : null;
          state.lookalikePairs.push({
            a: p.a,
            b: p.b,
            difficulty: diff,
            note: typeof p.note === "string" ? p.note : null,
          });
        });
        state.endpointToExample = {};
        state.groupToImages = {};
        state.progress = readLocalJson(LS_PROGRESS, {}) || {};
        if (typeof state.progress !== "object" || Array.isArray(state.progress)) {
          state.progress = {};
        }
        state.confusions = readLocalJson(LS_CONFUSIONS, []) || [];
        if (!Array.isArray(state.confusions)) state.confusions = [];
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
        var initial = lockLevel
          ? lockLevel
          : normalizeUnlockedLevel(readLocalJson(LS_LEVEL, "kenmerken"), levelEl);
        applyLevel(initial, true);
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

