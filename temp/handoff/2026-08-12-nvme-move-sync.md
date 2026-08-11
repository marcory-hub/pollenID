# Handoff: Project moved to NVMe and notes synced

## Goal
Keep working from `/Volumes/nvme/Developer/projects/pollenID` with a correct Obsidian notes sync path and a local `.venv` bound to that location.

## Current state
- Workspace root is `/Volumes/nvme/Developer/projects/pollenID` (old `/Users/md/Developer/pollenID` gone).
- Git: `main`, clean, all tracked files present (5434 checked).
- Obsidian sync target updated in `_cli_pid.md` to the NVMe `notes/` path; rsync `--delete` run; repo `notes/pollenID` matches Obsidian.
- Four files that existed only in the old repo notes copy were deleted by sync: `Beug.txt`, `Determinatietabel voor pollen in Nederlandse honing mrt2014.txt`, `kerkvliet-vanderham-pollen-lijst.md`, `palynoquest-levels.md` (not in Obsidian).
- `.venv` recreated at the new path; `requirements.txt` installed; imports OK.
- No other stale `/Users/md/Developer/pollenID` references found outside that sync doc.

## Next steps
1. Open the workspace from `/Volumes/nvme/Developer/projects/pollenID` (not the old Developer path).
2. For notes sync, use the command in `(notes/pollenID/_cli_pid.md)` (Obsidian remains SoT; agents do not edit `notes/` unless explicitly asked).
3. Continue normal taxon/site work from here; no further move cleanup expected unless those deleted note files are needed again in Obsidian.

## Artifacts
- `/Volumes/nvme/Developer/projects/pollenID` — live project root
- `notes/pollenID/_cli_pid.md` — rsync source/dest for Obsidian sync
- `.venv/` — local env at new path (`pyvenv.cfg` command points at NVMe)

## Suggested skills
- `@read-notes` — when loading facts from gitignored / Obsidian-synced `notes/`
- `@add-pollen` — if next work is taxon ingest after the move
- `@update-pollen-yaml` — if next work is YAML field updates only
