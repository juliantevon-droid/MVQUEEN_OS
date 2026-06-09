#!/bin/bash

ROOT="/storage/emulated/0/MVQUEEN_OS"
OUTPUT="$ROOT/00_Doctrine/MASTER_INDEX.md"

echo "# MVQUEEN_OS — Master Index" > "$OUTPUT"
echo "_Generated: $(date)_" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"

current_section=""

find "$ROOT" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" -o -name "*.json" \) | sort | while read -r file; do
  # Skip empty files
  if [ ! -s "$file" ]; then continue; fi
  content=$(tr -d '[:space:]' < "$file")
  if [ -z "$content" ]; then continue; fi

  # Get section (top-level folder)
  section=$(echo "$file" | sed "s|$ROOT/||" | cut -d'/' -f1)

  # Print section header if new
  if [ "$section" != "$current_section" ]; then
    echo "" >> "$OUTPUT"
    echo "## $section" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    current_section="$section"
  fi

  # File info
  rel_path=$(echo "$file" | sed "s|$ROOT/||")
  size=$(wc -c < "$file")
  preview=$(head -5 "$file" | tr '\n' ' ' | cut -c1-200)

  echo "### $rel_path" >> "$OUTPUT"
  echo "- **Size:** ${size} bytes" >> "$OUTPUT"
  echo "- **Preview:** $preview" >> "$OUTPUT"
  echo "" >> "$OUTPUT"

done

echo "✅ Done! Index saved to: $OUTPUT"
