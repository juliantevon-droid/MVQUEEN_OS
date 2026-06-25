import json
import os
import subprocess
import datetime
from collections import defaultdict

# Configuration
DRIVE_SEARCH_QUERY = "name contains 'MvQueen' or name contains 'mvqueen' or name contains 'MVQUEEN' or name contains 'Miss.Princess'"
GITHUB_REPO_PATH = "/home/ubuntu/MVQUEEN_OS"
LOG_DIR = os.path.join(GITHUB_REPO_PATH, "14_Data_And_Analytics")
SYNC_LOG = os.path.join(LOG_DIR, "sync_history.json")
AUDIT_DIR = os.path.join(LOG_DIR, "audit_reports")

def get_drive_files():
    try:
        result = subprocess.run(
            ["gws", "drive", "files", "list", "--params", json.dumps({
                "pageSize": 1000,
                "q": DRIVE_SEARCH_QUERY,
                "fields": "files(id, name, mimeType, md5Checksum, modifiedTime)"
            }), "--format", "json"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout).get("files", [])
    except Exception as e:
        print(f"Error fetching Drive files: {e}")
        return []

def run_maintenance():
    print(f"--- Starting Maintenance Hub: {datetime.datetime.now()} ---")
    drive_files = get_drive_files()
    
    # 1. SYNC LOGIC
    github_files = {}
    for root, dirs, files in os.walk(GITHUB_REPO_PATH):
        if ".git" in root: continue
        for f in files: github_files[f] = os.path.join(root, f)

    new_files_count = 0
    for f in drive_files:
        name, f_id, mime = f["name"], f["id"], f["mimeType"]
        if mime == "application/vnd.google-apps.folder" or ".trashed" in name: continue
        if name not in github_files:
            target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets")
            if name.endswith(".py") or "Code" in name or "Script" in name: target_dir = os.path.join(GITHUB_REPO_PATH, "15_Scripts_And_Code")
            elif "Prompt" in name: target_dir = os.path.join(GITHUB_REPO_PATH, "10_AI_Systems")
            elif name.endswith(".pdf"): target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets/PDFs")
            elif name.endswith(".docx"): target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets/Documents")
            
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, name)
            try:
                if "google-apps" in mime:
                    export_mime = "text/markdown" if "document" in mime else "text/csv"
                    subprocess.run(["gws", "drive", "files", "export", "--params", json.dumps({"fileId": f_id, "mimeType": export_mime}), "--output", target_path], check=True)
                else:
                    subprocess.run(["gws", "drive", "files", "get", "--params", json.dumps({"fileId": f_id, "alt": "media"}), "--output", target_path], check=True)
                new_files_count += 1
            except: pass

    # 2. AUDIT LOGIC
    by_hash = defaultdict(list)
    for f in drive_files:
        f_hash = f.get("md5Checksum")
        if f_hash: by_hash[f_hash].append(f)
    duplicates = {h: files for h, files in by_hash.items() if len(files) > 1}
    
    # Cleanup duplicates
    if duplicates:
        for h, files in duplicates.items():
            for f in files[1:]:
                subprocess.run(["gws", "drive", "files", "delete", "--params", json.dumps({"fileId": f["id"]})])

    # 3. LOGGING & COMMITTING
    if new_files_count > 0 or duplicates:
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "add", "."], check=True)
        msg = f"🔧 Maintenance: Synced {new_files_count} files and cleaned up duplicates"
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "commit", "-m", msg], check=True)
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "push", "origin", "main"], check=True)

    print("Maintenance complete.")

if __name__ == "__main__":
    run_maintenance()
