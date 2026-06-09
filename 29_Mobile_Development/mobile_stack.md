# Mobile Stack
## MVQUEEN_OS / 29_Mobile_Development

---

## Purpose

Documents the mobile development environment and tools powering MVQUEEN_OS on Android. The entire MVQUEEN operating system is managed from a mobile device — this is the technical foundation.

---

## Current Stack

| Tool | Purpose | Status |
|---|---|---|
| Termux | Linux terminal on Android | Active |
| Andronix | Ubuntu environment | Active |
| Obsidian | Markdown vault / note system | Active |
| DriveSync | Google Drive sync | Active |
| Python 3.x | Script execution | Active |
| Bash | Shell scripting | Active |
| Claude AI | AI operations and builds | Active |

---

## Key Paths

| Location | Path |
|---|---|
| MVQUEEN_OS Root | `/storage/emulated/0/MVQUEEN_OS` |
| Termux Home | `~` |
| Python Scripts | `/storage/emulated/0/MVQUEEN_OS/scripts` |

---

## Common Commands

```bash
# Count all files in OS
find /storage/emulated/0/MVQUEEN_OS -type f | wc -l

# List folder file counts
find /storage/emulated/0/MVQUEEN_OS -maxdepth 1 -type d | while read dir; do
  count=$(find "$dir" -type f | wc -l)
  echo "$count $dir"
done | sort -rn

# Run a Python script
python3 /storage/emulated/0/MVQUEEN_OS/scripts/script_name.py

# Install Python package
pip install package_name --break-system-packages
```

---

## Status
Active
