**One-line purpose:** what is done and what move to todays task list
**Short summary:** tasks to do and what is done
**Agent:** 
**SoT:** yes
**Main Index:** [[__pollenID]]

---

### implemented for quest

- Manifest generation (CI): `scripts/build_manifests.py` scans `docs/keys/**/*.json`, normalizes relative image refs, and generates:
    - `docs/assets/manifests/keys.json` (all JSON keys)
    - `docs/assets/manifests/images.json` (all images + where they occur in keys)
    - `docs/assets/manifests/palynoquest-items.json` (v1 seed: 10 items with endpoint text + expected first step)
- GitHub Action step: `.github/workflows/ci.yml` now runs the manifest builder before `mkdocs build`.
- Key instrumentation: `docs/javascripts/vdh-pollentabel.js` now:
    - exposes a `boot()` on `window.PID_VDH_POLLENTABEL`
    - emits events on step/choice/outcome (`pid:vdh-step`, `pid:vdh-choice`, `pid:vdh-outcome`)
    - stores a controller on the root element (`__vdhPollentabelController`) so PalynoQuest can “jump to expected path”
- Quiz UI: `docs/naslag/palynoquest.md` now contains the quiz block and loads `docs/javascripts/palynoquest.js` via an inline `<script src=...>` (no `mkdocs.yml` change needed).
- Quiz logic: `docs/javascripts/palynoquest.js` supports:
    - random item selection
    - open question grading (normalized, case-insensitive, punctuation/markup stripped)
    - MCQ grading (currently only strict answer + placeholders for distractors)
    - key selection list (from `keys.json`)
    - “wrong key for this image” is implicitly supported by loading any key; divergence warnings trigger when expected-path metadata exists for the item.

### Notes / known limitations (v1)

- Distractors are empty in the seeded 10 items right now (the structure is there; the generator does not fabricate distractors yet).
- Expected path is currently only the first keyed decision (single step); you can extend items later to full paths.
- Local terminal used `python3` (CI is Python 3.12, already set up).