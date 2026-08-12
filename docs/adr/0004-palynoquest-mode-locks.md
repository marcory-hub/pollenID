# PalynoQuest mode locks (name vs kenmerken vs lookalike)

Numeric `data-pq-lock-level` values (`1` / `2` / `3`) drive **name-MCQ** (image + four names). Feature drill uses only `kenmerken` / `kenmerken-N`. Lookalike uses `lookalike*`. Do not coerce numeric tiers into kenmerken mode in `parseLevelValue` or `applyLevel`; that emptied the name path and made niveau pages share the small `controlled` pool.

Status: accepted

Contract page: `docs/naslag/palynoquest-modes.md`.
