/**
 * PollenID shared client utilities: fetch cache, pollen.json index, visibility labels.
 * Load before pollentabel.js, kerkvliet-determinatietabel.js, and palynoquest.js.
 */
(function () {
  "use strict";

  /** @type {Map<string, Promise<unknown>>} */
  const jsonCache = new Map();

  /** @type {Promise<Record<string, unknown>>|null} */
  let pollenIndexPromise = null;

  let docsRootUrl = null;

  const VISIBILITY_LABELS_NL = {
    lm_clear: "goed zichtbaar met LM",
    lm_poor: "matig zichtbaar met LM",
    em_only: "alleen zichtbaar met EM",
  };

  function esc(s) {
    const d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function escAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  function visibilityLabelNl(code) {
    if (code == null) return "";
    const s = String(code).trim();
    if (!s || s === "-" || s === "null" || s === "None") return "";
    return VISIBILITY_LABELS_NL[s] || "";
  }

  function morphWithVisibility(text, visibilityCode) {
    const t = text != null ? String(text).trim() : "";
    const label = visibilityLabelNl(visibilityCode);
    if (t && label) return t + " (" + label + ")";
    if (t) return t;
    if (label) return "(" + label + ")";
    return "";
  }

  function isMissingValue(v) {
    return v == null || String(v).trim() === "" || String(v).trim() === "-";
  }

  function resolveDataJsonUrl(url) {
    if (typeof url !== "string" || !url) return url;
    try {
      return new URL(url, document.baseURI).href;
    } catch (e) {
      return url;
    }
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

  function computePollenIndexUrl(keyAbsUrl) {
    try {
      const u = new URL(keyAbsUrl, document.baseURI);
      const keyQ = u.search;
      if (/\/keys\//.test(u.pathname)) {
        u.pathname = u.pathname.replace(/\/keys\/.*$/, "/data/pollen.json");
      } else {
        u.pathname = u.pathname.replace(/\/[^/]*$/, "/data/pollen.json");
      }
      u.search = keyQ || "";
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

  function getDocsRootUrl() {
    return docsRootUrl;
  }

  function resetPollenIndexCache() {
    pollenIndexPromise = null;
    docsRootUrl = null;
  }

  window.PidCore = {
    esc: esc,
    escAttr: escAttr,
    visibilityLabelNl: visibilityLabelNl,
    morphWithVisibility: morphWithVisibility,
    VISIBILITY_LABELS_NL: VISIBILITY_LABELS_NL,
    isMissingValue: isMissingValue,
    resolveDataJsonUrl: resolveDataJsonUrl,
    fetchJsonCached: fetchJsonCached,
    computePollenIndexUrl: computePollenIndexUrl,
    fetchPollenIndex: fetchPollenIndex,
    getDocsRootUrl: getDocsRootUrl,
    resetPollenIndexCache: resetPollenIndexCache,
  };
})();
