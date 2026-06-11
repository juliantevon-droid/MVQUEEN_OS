#!/data/data/com.termux/files/usr/bin/bash

VAULT_ROOT="/storage/emulated/0/MVQUEEN_OS"
OUTPUT="$VAULT_ROOT/Command_Center/vault_registry.txt"

echo "Crawling vault at $VAULT_ROOT..."
echo "MVQUEEN_OS Registry – $(date)" > "$OUTPUT"

find "$VAULT_ROOT" -type f \
  | sed "s#$VAULT_ROOT/##g" \
  | sort >> "$OUTPUT"

echo "Registry written to $OUTPUT"
