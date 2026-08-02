#!/usr/bin/env python3
"""Orchestrate common add-taxon pipeline steps after YAML/page edits.

Chains: rename screenshots → sync YAML images → optional Kerkvliet inject/slim →
optional render species page → validate with --rebuild-data (includes build_docs_data).

Manual YAML field edits and agent-note application stay with the agent/skills.
Do not invent taxa or morphology here.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PY = REPO_ROOT / ".venv" / "bin" / "python"
if not PY.is_file():
    PY = Path(sys.executable)

SCRIPTS = REPO_ROOT / "scripts"


def run(cmd: list[str], *, dry_run: bool) -> int:
    print("+", " ".join(cmd))
    if dry_run:
        return 0
    return subprocess.run(cmd, cwd=str(REPO_ROOT), check=False).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--slug",
        action="append",
        default=[],
        help="Limit rename to by-taxon/<slug>/ (repeatable). Sync still scans all by-taxon folders.",
    )
    ap.add_argument(
        "--skip-rename",
        action="store_true",
        help="Skip Schermafbeelding → <slug>_N.png rename",
    )
    ap.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip sync_yaml_confident_images.py --only-by-taxon",
    )
    ap.add_argument(
        "--kerkvliet",
        action="store_true",
        help="Run inject_pollen_keys_into_key_json.py and slim_pollen_key_endpoints.py",
    )
    ap.add_argument(
        "--render-pages",
        action="store_true",
        help="Render species pages for --slug via render_taxon_pages_from_sot helpers",
    )
    ap.add_argument(
        "--bootstrap",
        action="store_true",
        help="Run bootstrap_by_taxon_task.py --apply after validate",
    )
    ap.add_argument(
        "--mkdocs-build",
        action="store_true",
        help="Pass --mkdocs-build to validate_pollen_site.py",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing",
    )
    args = ap.parse_args()

    if not args.skip_rename:
        if args.slug:
            for slug in args.slug:
                rc = run(
                    [
                        str(PY),
                        str(SCRIPTS / "rename_kerkvliet_screenshot_imports.py"),
                        "--only-folder",
                        slug,
                    ],
                    dry_run=args.dry_run,
                )
                if rc != 0:
                    return rc
        else:
            rc = run(
                [str(PY), str(SCRIPTS / "rename_kerkvliet_screenshot_imports.py")],
                dry_run=args.dry_run,
            )
            if rc != 0:
                return rc

    if not args.skip_sync:
        rc = run(
            [
                str(PY),
                str(SCRIPTS / "sync_yaml_confident_images.py"),
                "--only-by-taxon",
            ],
            dry_run=args.dry_run,
        )
        if rc != 0:
            return rc

    if args.kerkvliet:
        rc = run(
            [str(PY), str(SCRIPTS / "inject_pollen_keys_into_key_json.py")],
            dry_run=args.dry_run,
        )
        if rc != 0:
            return rc
        kerk = (
            REPO_ROOT
            / "docs"
            / "keys"
            / "kerkvliet"
            / "kerkvliet-determinatietabel.json"
        )
        rc = run(
            [
                str(PY),
                str(SCRIPTS / "slim_pollen_key_endpoints.py"),
                str(kerk),
            ],
            dry_run=args.dry_run,
        )
        if rc != 0:
            return rc

    if args.render_pages:
        if not args.slug:
            print("--render-pages requires at least one --slug", file=sys.stderr)
            return 2
        if args.dry_run:
            print("+ render species pages for:", ", ".join(args.slug))
        else:
            sys.path.insert(0, str(SCRIPTS))
            import yaml
            from render_taxon_pages_from_sot import render_taxon_page

            pollen = yaml.safe_load(
                (REPO_ROOT / "data" / "pollen.yaml").read_text(encoding="utf-8")
            )
            out = REPO_ROOT / "docs" / "pollen" / "species"
            for slug in args.slug:
                entry = pollen.get(slug)
                if not isinstance(entry, dict):
                    print(f"missing YAML entry for --slug {slug}", file=sys.stderr)
                    return 1
                path = out / f"{slug}.md"
                path.write_text(render_taxon_page(slug, entry), encoding="utf-8")
                print(f"wrote {path.relative_to(REPO_ROOT)}")

    validate_cmd = [
        str(PY),
        str(SCRIPTS / "validate_pollen_site.py"),
        "--rebuild-data",
        "--images",
        "--links",
    ]
    if args.mkdocs_build:
        validate_cmd.append("--mkdocs-build")
    rc = run(validate_cmd, dry_run=args.dry_run)
    if rc != 0:
        return rc

    if args.bootstrap:
        rc = run(
            [str(PY), str(SCRIPTS / "bootstrap_by_taxon_task.py"), "--apply"],
            dry_run=args.dry_run,
        )
        if rc != 0:
            return rc

    print("add_taxon: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
