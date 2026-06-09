import os

ROOT = "/storage/emulated/0/MVQUEEN_OS"
DL = "/storage/emulated/0/Download"

def load(fname):
    with open(os.path.join(DL, fname), "r", encoding="utf-8") as f:
        return f.read()

def extract(content, keyword):
    lines = content.split("\n")
    start = None
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower() and line.startswith("#"):
            start = i
            break
    if start is None:
        return None
    hlevel = len(lines[start]) - len(lines[start].lstrip("#"))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            lvl = len(lines[i]) - len(lines[i].lstrip("#"))
            if lvl <= hlevel:
                end = i
                break
    return "\n".join(lines[start:end]).strip()

def write(rel, content):
    dest = os.path.join(ROOT, rel)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)

SPLITS = [
    ("brand_identity.md", "Color System", "02_Brand_Identity/color_system.md"),
    ("brand_identity.md", "Typography System", "02_Brand_Identity/typography_system.md"),
    ("brand_identity.md", "Brand Rules", "02_Brand_Identity/brand_rules.md"),
]

cache = {}
for fname, keyword, dest_rel in SPLITS:
    if fname not in cache:
        cache[fname] = load(fname)
    section = extract(cache[fname], keyword)
    if section:
        write(dest_rel, section)
        print(f"✅ {dest_rel}")
    else:
        print(f"⚠️ Not found: {keyword}")
