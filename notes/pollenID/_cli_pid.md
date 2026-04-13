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
rsync -av --delete "/Users/md/Library/Mobile Documents/iCloud~md~obsidian/Documents/notes/500 pollenonderzoek/pollenID" "/Users/md/Developer/pollenID/notes"
```

---
