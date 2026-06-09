from pathlib import Path

context_file = Path("/sdcard/MVQUEEN_OS/vault_context.md")

print("\n=== MVQUEEN CONTEXT ===\n")

if context_file.exists():
    content = context_file.read_text(encoding="utf-8")

    print(content[:5000])

else:
    print("vault_context.md not found")

print("\nCONTEXT LOADED\n")

