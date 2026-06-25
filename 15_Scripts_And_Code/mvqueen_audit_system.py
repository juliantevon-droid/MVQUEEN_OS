import json
import os
import subprocess
import datetime
from collections import defaultdict

# Configuration
DRIVE_SEARCH_QUERY = "name contains 'MvQueen' or name contains 'mvqueen' or name contains 'MVQUEEN' or name contains 'Miss.Princess'"
GITHUB_REPO_PATH = "/home/ubuntu/MVQUEEN_OS"
AUDIT_REPORT_PATH = os.path.join(GITHUB_REPO_PATH, "14_Data_And_Analytics/audit_reports")

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

def run_audit():
    print(f"--- Starting Audit: {datetime.datetime.now()} ---")
    drive_files = get_drive_files()
    
    # Duplicate detection (by hash)
    by_hash = defaultdict(list)
    for f in drive_files:
        f_hash = f.get("md5Checksum")
        if f_hash: by_hash[f_hash].append(f)
    
    duplicates = {h: files for h, files in by_hash.items() if len(files) > 1}
    
    # Index GitHub
    github_files = set()
    for root, dirs, files in os.walk(GITHUB_REPO_PATH):
        if ".git" in root: continue
        for f in files: github_files.add(f)
        
    # Discrepancy detection
    missing_in_github = [f for f in drive_files if f["name"] not in github_files and f["mimeType"] != "application/vnd.google-apps.folder" and ".trashed" not in f["name"]]

    # Generate Report
    report_name = f"audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    os.makedirs(AUDIT_REPORT_PATH, exist_ok=True)
    report_path = os.path.join(AUDIT_REPORT_PATH, report_name)
    
    with open(report_path, "w") as r:
        r.write(f"# MVQUEEN_OS Audit Report - {datetime.datetime.now()}\n\n")
        
        r.write("## 1. Google Drive Duplicates\n")
        if duplicates:
            for h, files in duplicates.items():
                r.write(f"- Hash `{h}`:\n")
                for f in files: r.write(f"  - {f['name']} (ID: {f['id']})\n")
        else:
            r.write("No duplicates found.\n")
            
        r.write("\n## 2. Missing in GitHub\n")
        if missing_in_github:
            for f in missing_in_github:
                r.write(f"- {f['name']} (ID: {f['id']})\n")
        else:
            r.write("All relevant Drive files are present in GitHub.\n")

    print(f"Audit complete. Report saved to: {report_path}")
    
    # Auto-cleanup duplicates if any
    if duplicates:
        print("Auto-cleaning duplicates...")
        for h, files in duplicates.items():
            to_delete = files[1:]
            for f in to_delete:
                print(f"Deleting duplicate: {f['name']} (ID: {f['id']})")
                subprocess.run(["gws", "drive", "files", "delete", "--params", json.dumps({"fileId": f["id"]})])

    # Commit report to GitHub
    subprocess.run(["git", "-C", GITHUB_REPO_PATH, "add", "."], check=True)
    subprocess.run(["git", "-C", GITHUB_REPO_PATH, "commit", "-m", f"🔍 Audit: Generated health report and cleaned up duplicates"], check=True)
    subprocess.run(["git", "-C", GITHUB_REPO_PATH, "push", "origin", "main"], check=True)

if __name__ == "__main__":
    run_audit()
