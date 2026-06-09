import os
import sys

def load_brand_bible(file_path="Brand_bible.md"):
    """
    Ensures MVQUEEN_OS can ingest local brand rules safely before running API calls.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] Permissions or Path Wall: Cannot locate {file_path}")
        print("Ensure the file sits in the working directory of the daemon script.")
        return None
        
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            brand_rules = file.read()
            print(f"[SUCCESS] MVQUEEN_OS loaded brand rules ({len(brand_rules)} characters).")
            return brand_rules
    except PermissionError:
        print(f"[CRITICAL] OS Permission Wall: Read access denied for {file_path}")
        print("Fix by running: chmod 644 Brand_bible.md")
        return None

# Example usage within the pipeline execution block
brand_context = load_brand_bible()