from pathlib import Path

vault = Path("/sdcard/MVQUEEN_OS")

print("\n=== MVQUEEN OS ===\n")

for folder in sorted(vault.iterdir()):
    print(f"📁 {folder.name}")

print("\nSYSTEM ONLINE\n")
