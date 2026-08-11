**One-line purpose:** single SoT for pollen data
**Short summary:** tasks to do and what is done
**Agent:** 
**SoT:** yes
**Main Index:** [[__pollenID]]

---

You are an expert MkDocs + mkdocs-material developer. Follow these rules strictly at all times:

1. Strict Factuality: Only include verified, standard MkDocs/mkdocs-material/mkdocs-macros-plugin steps. Mark anything non-standard or unverified as '[to be verified]'.
2. Safety First: Never suggest delete, rm -rf, force overwrite, or destructive commands without a clear, bold **DATA LOSS WARNING**.
3. No Jargon: Use plain English only. Explain each concept in one short sentence.
4. Concise Structure: Use a high-level table or bullet lists for the plan. No preambles, no filler, no closing summary.
5. Context-Driven: Use ONLY the information provided in this message. Do not invent new tools or behaviors.

Objective: Create one clean central data/pollen.yaml file (all keys and content in English) that stores pollen/palynology information, load it with mkdocs-macros-plugin, and provide simple macros so we can easily display plant names, bloom periods, sizes, and scaled images on any Markdown page.

Available information from user:
- Central file should be data/pollen.yaml
- Example structure:
  taraxacum_officinale:
    latin: Taraxacum officinale
    dutch: Paardenbloem
    family: Asteraceae
    size:
      smallest_size: "30 µm" [put smallest size you find in the data here]
      largest_size: "38 µm" [put largest size you find i
- shape:
- polarity:
- P/E-ratio:
- Aperture
- Ornamentation
  image:
    height_px: 220 [take largest size * 2.5]
  bloeitijd:
    start: 3
    end: 6
  nectar_value: [can be null]
  pollen_value: [can be null]
  frequency_in_honey: [can be null]
- 

- ID is latin name, example: taraxacum_officinale
- put IDs in alfabetical order
- collect data from: 
docs/keys/eide/rosaceae-eide.json
docs/keys/kerkvliet/kerkvliet-determinatietabel.json
docs/keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json
docs/keys/vanderham/vanderham-pollentabel.json
docs/monoflorale-honing-pollen/*.md
docs/nederlandse-honing-pollen/*.md

- We want to use image.height_px to control the height of each pollen image.
- Use mkdocs-macros-plugin (standard way: add to plugins in mkdocs.yml and create main.py with define_env). (plugin is not installed yet)
- There is a example merge script (scripts/merge_pollen.py) that reads raw JSON files from raw_json/ folder, normalizes them, creates the key from latin name (lowercase, spaces → underscore), and writes to data/pollen.yaml. Use this as example to make a script that works with the current data in this project. 
- Handle duplicates by logging.
- Bloom periods should be stored as start/end numbers (month 1-12).
- Missing values should be null.
- Image macro should output MkDocs/Material-specific image syntax so we can use it to replace our current messy code. You find the locations of the images here:
docs/assets/images/beug
docs/assets/images/kerkvliet
docs/assets/images/paldat
docs/assets/images/persano_oddo
docs/assets/images/pollenwiki

Plan the exact steps to:
1. Set up or improve the data merging process.
2. Configure mkdocs-macros-plugin correctly.
3. Create two macros: one for text fields (pollen(key, field)) and one for images (pollen_img(key, src, alt="")) that automatically applies the height_px from the YAML.
4. Show how to use them safely in Markdown pages.

Output Format (use exactly this):

**Objective:** [One sentence goal]

**The Plan:**

| Step | Action | Details |
|------|--------|---------|

**Safety/Verification Check:** [Bullet list of any [to be verified] items and all warnings]


Before you start with the creation of the plan ask clarifying questions if needed. Then create the full plan.


---
**Role:** You are a Prompt Architect specializing in mkdocs-material

**Task:** Write a detailed prompt for cursor.ai agent in plan mode, ask clarifying questions if needed


**Instructions for cursor.ai in plan mode (The Rules):**

1. **Strict Factuality:** Only include verified steps. If a process is not standard or verifiable, mark it as '[to be verified]'.
    
2. **Safety First:** Do not suggest destructive commands (e.g., "delete all," "force overwrite," or "remove folder") without a clear, bold warning about potential data loss.
    
3. **No Jargon:** Use plain English. Avoid "API," "Backend," "Latency," or other technical terms. Explain concepts in one short scentence.
    
4. **Concise Structure:** Use a high-level table or bulleted list for the plan. Skip preambles/introductory filler and omit closing summaries.
    
5. **Context-Driven:** Only use the information provided in this session or from cited sources. Do not invent hypothetical tools or behaviors.
   

**Output Format for Agent 2:**

- **Objective:** [One sentence goal]
    
- **The Plan:** [High-level steps in a table]
    
- **Safety/Verification Check:** [A list of any [to be verified] items or warnings]

# The messy plan
One central file data/pollen.yaml (translate everything to english)
```
taraxacum_officinale:
  latin: Taraxacum officinale
  dutch: Paardenbloem
  family: Asteraceae

  size:
    kerkvliet: "30–35 µm"
    pollenwiki: "28–38 µm"

  image:
    height_px: 220

  bloeitijd:
    start: 3
    end: 6

  nectar_value:
  pollen_value:

  frequency_in_honey:
```
can we use   imageheightpx to scale the images height

Then use a plugin like:

- `mkdocs-macros-plugin`

In `mkdocs.yml`:

plugins:  
  - macros

In `main.py` (macros file):

import yaml  
  
def define_env(env):  
    with open("data/pollen.yaml") as f:  
        pollen_data = yaml.safe_load(f)  
  
    @env.macro  
    def pollen(key, field):  
        return pollen_data[key].get(field, "")

---

Step 0: extract data from existing files
- check every file that we have so far
- extract the messy data
- the ID is the latin name with underscore
- (taraxacum_officinale)
```
scripts/merge_pollen.py
import os
import json
import yaml

INPUT_DIR = "raw_json"
OUTPUT_FILE = "data/pollen.yaml"

def normalize(entry):
    """Map messy JSON to your clean schema"""
    return {
        "latin": entry.get("latin") or entry.get("name_latin"),
        "dutch": entry.get("dutch") or entry.get("nl"),
        "family": entry.get("family"),

        "size": {
            "kerkvliet": entry.get("size_kerkvliet") or entry.get("size", {}).get("kerk"),
            "pollenwiki": entry.get("size_pollenwiki")
        },

        "image": {
            "height_px": entry.get("imageheightpx", 200)
        },

        "bloeitijd": parse_bloeitijd(entry.get("bloeitijd")),

        "nectar_value": entry.get("nectar_value"),
        "pollen_value": entry.get("pollen_value"),
        "frequency_in_honey": entry.get("frequency_in_honey")
    }

def parse_bloeitijd(value):
    if not value:
        return None
    if isinstance(value, str) and "-" in value:
        start, end = value.split("-")
        return {"start": int(start), "end": int(end)}
    return None

def make_key(latin_name):
    return latin_name.lower().replace(" ", "_")

def main():
    result = {}

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(INPUT_DIR, filename)

        with open(path) as f:
            data = json.load(f)

        entry = normalize(data)

        if not entry["latin"]:
            continue

        key = make_key(entry["latin"])
        result[key] = entry

    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(result, f, sort_keys=True, allow_unicode=True)

if __name__ == "__main__":
    main()
```
▶️ Run it
```
python scripts/merge_pollen.py
```
check for duplicates
### 1. Duplicate species

Different JSON files might contain the same pollen.

👉 Solution:  
Add logging:

if key in result:  
    print(f"Duplicate: {key}")
## 2. Inconsistent bloom periods 
- put start and end of bloom in numbers so we can do some selections

handel missing info with nectar_value: null

### Usage in Markdown pages:

**Latijnse naam:** {{ pollen("salix", "latin") }}    
**Nederlandse naam:** {{ pollen("salix", "dutch") }}    
**Grootte (Kerkvliet):** {{ pollen("salix", "size_kerkvliet") }}    
**Bloeitijd:** {{ pollen("salix", "bloeitijd") }}

### Step 1: Macro for image rendering

In your `main.py`:

def define_env(env):  
    import yaml  
  
    with open("data/pollen.yaml") as f:  
        pollen_data = yaml.safe_load(f)  
  
    @env.macro  
    def pollen_img(key, src, alt=""):  
        data = pollen_data.get(key, {})  
        height = data.get("image", {}).get("height_px", 200)  
  
        return f'<img src="{src}" alt="{alt}" height="{height}px">'

---

### Step 2: Use it in Markdown

{{ pollen_img("taraxacum_officinale", "../assets/images/taraxacum.jpg", "Paardenbloem pollen") }}