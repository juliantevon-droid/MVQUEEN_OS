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
    ("brand_strategy_rebuilds.md", "Brand Values",              "01_Brand_Strategy/Brand_Values.md"),
    ("brand_strategy_rebuilds.md", "Brand Essence",             "01_Brand_Strategy/Brand_Essence.md"),
    ("brand_strategy_rebuilds.md", "Brand Messaging Framework", "06_Tone_And_Voice/Brand_Messaging.md"),
    ("brand_strategy_rebuilds.md", "Brand Story",               "01_Brand_Strategy/Brand_Story.md"),
    ("brand_strategy_rebuilds.md", "Brand Positioning",         "01_Brand_Strategy/Brand_Positioning.md"),
    ("ai_systems_rebuilds.md",     "AI Prompt Library",         "10_AI_Systems/AI_Prompt_Library.md"),
    ("ai_systems_rebuilds.md",     "Ad Copy Prompts",           "10_AI_Systems/Ad_Copy_Prompts.md"),
]

cache = {}
written = 0
for fname, keyword, dest_rel in SPLITS:
    if fname not in cache:
        cache[fname] = load(fname)
    section = extract(cache[fname], keyword)
    if section:
        write(dest_rel, section)
        print(f"✅ {dest_rel}")
        written += 1
    else:
        print(f"⚠️  Not found: {keyword}")

print(f"\n🏁 {written} files written")
