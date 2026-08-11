**One-line purpose:** cli commands
**Short summary:** sync notes from obsidian
**Agent:** 
**SoT:** NO
**Index:** [[__pollenID]]

---
**Sync from Obsidian to Cursor 
(open .venv and 1:1 mirror into `notes/`)**

```bash
source .venv/bin/activate
rsync -av --delete "/Users/md/Library/Mobile Documents/iCloud~md~obsidian/Documents/notes/500 pollenonderzoek/pollenID" "/Volumes/nvme/Developer/projects/pollenID/notes"
```

---


rename images files in by-taxon-kerkvliet
```
python3 scripts/rename_kerkvliet_screenshot_imports.py
```

---
after adding images run
```
python scripts/sync_yaml_confident_images.py --only-by-taxon
```

```
`python scripts/export_pollen_json.py
```

```
python scripts/build_manifests.py
```

---

update van der ham after adding images
```sh
./.venv/bin/python scripts/sync_yaml_confident_images.py --only-by-taxon
./.venv/bin/python scripts/build_docs_data.py
```