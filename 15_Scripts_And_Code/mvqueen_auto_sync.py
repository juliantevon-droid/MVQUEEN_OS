import json
import os
import subprocess
import datetime

# Configuration
DRIVE_SEARCH_QUERY = "name contains 'MvQueen' or name contains 'mvqueen' or name contains 'MVQUEEN' or name contains 'Miss.Princess'"
GITHUB_REPO_PATH = "/home/ubuntu/MVQUEEN_OS"
SYNC_LOG_PATH = os.path.join(GITHUB_REPO_PATH, "14_Data_And_Analytics/sync_history.json")

def get_drive_files():
    """Fetch all relevant files from Google Drive."""
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

def sync():
    print(f"--- Starting Sync: {datetime.datetime.now()} ---")
    drive_files = get_drive_files()
    
    # Index GitHub files
    github_files = {}
    for root, dirs, files in os.walk(GITHUB_REPO_PATH):
        if ".git" in root: continue
        for f in files:
            github_files[f] = os.path.join(root, f)

    new_files_count = 0
    for f in drive_files:
        name = f["name"]
        f_id = f["id"]
        mime = f["mimeType"]
        
        if mime == "application/vnd.google-apps.folder" or ".trashed" in name:
            continue
            
        if name not in github_files:
            # Determine target directory
            target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets")
            if name.endswith(".py") or "Code" in name or "Script" in name:
                target_dir = os.path.join(GITHUB_REPO_PATH, "15_Scripts_And_Code")
            elif "Prompt" in name:
                target_dir = os.path.join(GITHUB_REPO_PATH, "10_AI_Systems")
            elif name.endswith(".pdf"):
                target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets/PDFs")
            elif name.endswith(".docx"):
                target_dir = os.path.join(GITHUB_REPO_PATH, "12_Content_Assets/Documents")

            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, name)
            
            print(f"Syncing new file: {name}...")
            try:
                if "google-apps" in mime:
                    export_mime = "text/markdown" if "document" in mime else "text/csv"
                    subprocess.run(["gws", "drive", "files", "export", "--params", json.dumps({"fileId": f_id, "mimeType": export_mime}), "--output", target_path], check=True)
                else:
                    subprocess.run(["gws", "drive", "files", "get", "--params", json.dumps({"fileId": f_id, "alt": "media"}), "--output", target_path], check=True)
                new_files_count += 1
            except Exception as e:
                print(f"Failed to sync {name}: {e}")

    if new_files_count > 0:
        print(f"Synced {new_files_count} new files. Committing to GitHub...")
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "commit", "-m", f"🔄 Auto-Sync: Added {new_files_count} new assets from Drive"], check=True)
        subprocess.run(["git", "-C", GITHUB_REPO_PATH, "push", "origin", "main"], check=True)
    else:
        print("No new files to sync.")

    # Update sync log
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "new_files": new_files_count,
        "status": "Success"
    }
    
    os.makedirs(os.path.dirname(SYNC_LOG_PATH), exist_ok=True)
    history = []
    if os.path.exists(SYNC_LOG_PATH):
        with open(SYNC_LOG_PATH, "r") as f:
            try: history = json.load(f)
            except: pass
    history.append(log_entry)
    with open(SYNC_LOG_PATH, "w") as f:
        json.dump(history[-50:], f, indent=2) # Keep last 50 entries

if __name__ == "__main__":
    sync()
