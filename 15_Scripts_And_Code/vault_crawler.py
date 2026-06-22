import os
from pathlib import Path

VAULT_PATH = "/storage/emulated/0/MVQUEEN_OS"

output = []

output.append("# MVQUEEN VAULT CONTEXT\n")

for root, dirs, files in os.walk(VAULT_PATH):

    level = root.replace(VAULT_PATH, "").count(os.sep)
    indent = "  " * level

    folder_name = os.path.basename(root)

    output.append(f"\n{indent}## 📂 {folder_name}")

    for file in files:

        if file.endswith(".md"):

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                word_count = len(content.split())

                if not content:
                    status = "EMPTY"
                else:
                    status = f"{word_count} words"

                output.append(f"{indent}- {file} ({status})")

            except Exception as e:
                output.append(f"{indent}- {file} (ERROR: {e})")

context_file = Path(VAULT_PATH) / "vault_context.md"

with open(context_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Vault scan complete.")
print(f"Context saved to: {context_file}")

