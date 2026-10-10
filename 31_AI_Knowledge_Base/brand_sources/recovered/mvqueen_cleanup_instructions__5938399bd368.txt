# MVQUEEN OS — Drive Stabilization
## Master Instructions (Pick One Method)

All three options do the exact same thing:
- Move MVQUEEN_CONTEXT.md + _ecosystem_index.json → 99_Command_Center
- Move pull_phase1.sh → 15_Scripts_And_Code
- Archive Phase2 HTML docs + all diagnostic .txt files → 98_Archive
- Archive all duplicate .md files at root → 98_Archive
- Move 5 ghost folders (Brand_Identity, Command_Center, Templates, merge_review, 20_Scripts_And_Code) → 98_Archive

Nothing is deleted — everything goes to 98_Archive first.

---

## OPTION 1 — Google Apps Script (Recommended, 2 min)

1. Open https://script.google.com
2. Click "New Project"
3. Delete any existing code in the editor
4. Open `mvqueen_cleanup.gs` → copy all content → paste into the editor
5. Click the floppy disk icon to Save (name it anything)
6. Click "Run" (▶️ button) → function: `runMVQUEENCleanup`
7. A popup will say "Authorization required" → click "Review Permissions"
8. Choose your Google account → click "Allow"
9. Click Run again — watch the Execution Log at the bottom
10. Done. A "MVQUEEN_Cleanup_Log" spreadsheet will appear in 99_Command_Center.

**No install required. Runs entirely in your browser.**

---

## OPTION 2 — Python Script (Terminal)

### Prerequisites (one-time setup)

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Google Cloud Setup (one-time, ~5 min)

1. Go to https://console.cloud.google.com
2. Create a new project (name it anything, e.g. "mvqueen-tools")
3. In the left menu → "APIs & Services" → "Library"
4. Search "Google Drive API" → click it → click "Enable"
5. Go to "APIs & Services" → "Credentials"
6. Click "Create Credentials" → "OAuth client ID"
7. Application type: "Desktop app" → name it anything → click Create
8. Click the download icon (⬇) → save as `credentials.json`
9. Place `credentials.json` in the same folder as `mvqueen_cleanup.py`

### Run

```bash
python mvqueen_cleanup.py
```

First run opens a browser tab → sign in → allow access.
A `token.json` is saved so you never need to authorize again.
A `mvqueen_cleanup_log_YYYYMMDD.json` is saved with full results.

---

## OPTION 3 — n8n Workflow

### Prerequisites

- n8n running (cloud at https://app.n8n.io or self-hosted)
- Google Drive credential connected in n8n

### Setup

1. In n8n → click "+" to create a new workflow
2. Click the "..." menu → "Import from JSON"
3. Paste the contents of `mvqueen_cleanup_n8n.json`
4. Click the "Move Files & Folders" node
5. In the Credentials field → select your Google Drive account
   (If not connected: click "Create new" → follow Google OAuth flow)
6. Click "Save"

### Run

1. Click "Execute Workflow" (▶️ button)
2. Watch nodes turn green as operations complete
3. Check the "Log Results" node output for success/failure count

### Note on n8n Google Drive node

The workflow uses `operation: move` on the Google Drive node.
If your n8n version uses a different operation name, you may need to
manually set: Resource = File, Operation = Move, and map fileId + folderId.

---

## What each method is best for

| Method | Best if... |
|---|---|
| Google Apps Script | You just want it done now, no setup |
| Python | You want a local log file + reusable script |
| n8n | You already use n8n and want it in your automation stack |

---

## After running any option

Your MVQUEEN root will contain only:
- All numbered module folders (00–39, 99)
- 98_Archive (containing archived duplicates)
- _BACKUPS
- MVQUEEN_CONTEXT.md and _ecosystem_index.json will be in 99_Command_Center
- Root will be clean

**Next step:** audit empty modules and begin completing them.
Priority order: 08_Social_Media → 07_Marketing → 03_Customer_Psychology → 05_SEO_And_Content
