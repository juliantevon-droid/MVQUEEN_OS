#!/usr/bin/env python3
"""
MVQUEEN_OS — Cleanup Script
Run this FIRST before any batch scripts.
Fixes: duplicate folders, missing numbers, loose files, empty files.
"""

import os
import shutil

BASE = "/storage/emulated/0/MVQUEEN_OS"

print("🔍 MVQUEEN_OS Cleanup Starting...\n")

# ── 1. DELETE empty file ────────────────────────────────────────────────────
empty_file = os.path.join(BASE, "Run folder agent.md")
if os.path.exists(empty_file):
    size = os.path.getsize(empty_file)
    if size == 0:
        os.remove(empty_file)
        print("🗑️  Deleted empty file: Run folder agent.md")
    else:
        print(f"⚠️  Skipped Run folder agent.md — not empty ({size} bytes)")
else:
    print("✅ Run folder agent.md already gone")

# ── 2. RENAME 13_Scripts_And_Code → 20_Scripts_And_Code ───────────────────
src_13 = os.path.join(BASE, "13_Scripts_And_Code")
dst_20 = os.path.join(BASE, "20_Scripts_And_Code")
if os.path.exists(src_13):
    if not os.path.exists(dst_20):
        shutil.move(src_13, dst_20)
        print("✅ Renamed: 13_Scripts_And_Code → 20_Scripts_And_Code (fixes duplicate 13)")
    else:
        print("⚠️  20_Scripts_And_Code already exists — merging contents")
        for f in os.listdir(src_13):
            shutil.move(os.path.join(src_13, f), os.path.join(dst_20, f))
        os.rmdir(src_13)
        print("✅ Merged 13_Scripts_And_Code into 20_Scripts_And_Code")
else:
    print("✅ 13_Scripts_And_Code already resolved")

# ── 3. MERGE 27_Templates into 17_Templates, then remove 27 ───────────────
src_27 = os.path.join(BASE, "27_Templates")
dst_17 = os.path.join(BASE, "17_Templates")
if os.path.exists(src_27):
    os.makedirs(dst_17, exist_ok=True)
    moved = 0
    for f in os.listdir(src_27):
        src_file = os.path.join(src_27, f)
        dst_file = os.path.join(dst_17, f)
        if not os.path.exists(dst_file):
            shutil.move(src_file, dst_file)
            moved += 1
        else:
            # Rename to avoid collision
            name, ext = os.path.splitext(f)
            dst_file = os.path.join(dst_17, f"{name}_from27{ext}")
            shutil.move(src_file, dst_file)
            moved += 1
    if not os.listdir(src_27):
        os.rmdir(src_27)
        print(f"✅ Merged 27_Templates → 17_Templates ({moved} files), removed 27_Templates")
    else:
        print(f"⚠️  27_Templates not empty after merge — check manually")
else:
    print("✅ 27_Templates already resolved")

# ── 4. CREATE missing 24_Email_And_SMS ────────────────────────────────────
folder_24 = os.path.join(BASE, "24_Email_And_SMS")
os.makedirs(folder_24, exist_ok=True)
readme_24 = os.path.join(folder_24, "README.md")
if not os.path.exists(readme_24):
    with open(readme_24, "w") as f:
        f.write("""# 24_Email_And_SMS
## MVQUEEN_OS

Email and SMS system — flows, sequences, templates, and performance tracking.
Sits between 23_Team_And_Delegation and 25_Retention_And_Community.

Key files to build:
- email_system.md — full flow architecture
- sms_system.md — SMS strategy and sequences
- klaviyo_setup.md — platform configuration
- email_templates.md — reusable email templates
""")
    print("✅ Created: 24_Email_And_SMS with README")
else:
    print("✅ 24_Email_And_SMS already exists")

# ── 5. MOVE loose scripts to 15_Scripts_And_Code ──────────────────────────
scripts_dst = os.path.join(BASE, "15_Scripts_And_Code")
os.makedirs(scripts_dst, exist_ok=True)

loose_scripts = [
    "install_critical.py",
    "split_phase2.py",
    "split_rebuilds.py",
    "run_all.py",
    "extract_bible_v2.py",
    "extract_bible.py",
    "generate_readmes.py",
    "crawler_v2.sh",
    "crawler.sh",
    "pull_phase1.sh",
]

moved_scripts = 0
for script in loose_scripts:
    src = os.path.join(BASE, script)
    dst = os.path.join(scripts_dst, script)
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.move(src, dst)
            moved_scripts += 1
        else:
            print(f"  ⚠️  {script} already in 15_Scripts_And_Code — skipped")
    else:
        pass  # already moved or never existed

print(f"✅ Moved {moved_scripts} scripts → 15_Scripts_And_Code")

# ── 6. MOVE Tiktok_seo.html to 05_SEO_And_Content ─────────────────────────
tiktok_src = os.path.join(BASE, "Tiktok_seo.html")
tiktok_dst = os.path.join(BASE, "05_SEO_And_Content", "Tiktok_seo.html")
if os.path.exists(tiktok_src):
    if not os.path.exists(tiktok_dst):
        shutil.move(tiktok_src, tiktok_dst)
        print("✅ Moved: Tiktok_seo.html → 05_SEO_And_Content/")
    else:
        print("⚠️  Tiktok_seo.html already in 05_SEO_And_Content")
else:
    print("✅ Tiktok_seo.html already moved")

# ── 7. MOVE folder_agent.md to 36_Agent_Systems ───────────────────────────
agent_src = os.path.join(BASE, "folder_agent.md")
agent_dst = os.path.join(BASE, "36_Agent_Systems", "folder_agent.md")
if os.path.exists(agent_src):
    os.makedirs(os.path.dirname(agent_dst), exist_ok=True)
    if not os.path.exists(agent_dst):
        shutil.move(agent_src, agent_dst)
        print("✅ Moved: folder_agent.md → 36_Agent_Systems/")
    else:
        print("⚠️  folder_agent.md already in 36_Agent_Systems")
else:
    print("✅ folder_agent.md already moved")

# ── 8. MOVE Weekly_Focus.md to 99_Command_Center ──────────────────────────
weekly_src = os.path.join(BASE, "Weekly_Focus.md")
weekly_dst = os.path.join(BASE, "99_Command_Center", "Weekly_Focus.md")
if os.path.exists(weekly_src):
    os.makedirs(os.path.dirname(weekly_dst), exist_ok=True)
    if not os.path.exists(weekly_dst):
        shutil.move(weekly_src, weekly_dst)
        print("✅ Moved: Weekly_Focus.md → 99_Command_Center/")
    else:
        print("⚠️  Weekly_Focus.md already in 99_Command_Center")
else:
    print("✅ Weekly_Focus.md already moved")

# ── 9. MOVE zips to _BACKUPS ──────────────────────────────────────────────
zips = ["MVQUEEN_ToneVoice_updated.zip", "MVQUEEN_new_modules.zip"]
backups_dst = os.path.join(BASE, "_BACKUPS")
os.makedirs(backups_dst, exist_ok=True)
for z in zips:
    src = os.path.join(BASE, z)
    dst = os.path.join(backups_dst, z)
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.move(src, dst)
            print(f"✅ Moved: {z} → _BACKUPS/")
        else:
            print(f"⚠️  {z} already in _BACKUPS")
    else:
        print(f"✅ {z} already moved")

# ── SUMMARY ────────────────────────────────────────────────────────────────
print("\n" + "="*50)
print("✅ MVQUEEN_OS Cleanup Complete")
print("="*50)
print("""
Changes made:
  • Deleted empty 'Run folder agent.md'
  • Renamed 13_Scripts_And_Code → 20_Scripts_And_Code
  • Merged 27_Templates → 17_Templates
  • Created 24_Email_And_SMS
  • Moved all loose scripts → 15_Scripts_And_Code
  • Moved Tiktok_seo.html → 05_SEO_And_Content
  • Moved folder_agent.md → 36_Agent_Systems
  • Moved Weekly_Focus.md → 99_Command_Center
  • Moved .zip files → _BACKUPS

Next: Run batch scripts 1 → 2 → 3 → 4
""")
