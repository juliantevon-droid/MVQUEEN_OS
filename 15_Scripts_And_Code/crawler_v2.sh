#!/bin/bash

ROOT="/storage/emulated/0/MVQUEEN_OS"
OUTPUT="$ROOT/00_Doctrine/MASTER_INDEX_V2.md"
EMPTY_LOG="$ROOT/00_Doctrine/EMPTY_FILES_LOG.md"

# Folders to skip
SKIP_DIRS=(".obsidian" "copilot" "textgenerator" "scripts" "98_Archive")

echo "# MVQUEEN_OS — Master Index V2" > "$OUTPUT"
echo "_Generated: $(date)_" >> "$OUTPUT"
echo "_Content files only — system/config files excluded_" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"

echo "# MVQUEEN_OS — Empty Files Log" > "$EMPTY_LOG"
echo "_Generated: $(date)_" >> "$EMPTY_LOG"
echo "_These files exist but have no real content yet_" >> "$EMPTY_LOG"
echo "" >> "$EMPTY_LOG"

current_section=""

find "$ROOT" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" \) | sort | while read -r file; do

  # Skip system/config folders
  skip=false
  for dir in "${SKIP_DIRS[@]}"; do
    if [[ "$file" == *"/$dir/"* || "$file" == *"/$dir" ]]; then
      skip=true; break
    fi
  done
  $skip && continue

  # Skip root-level scan/index/log files
  rel=$(echo "$file" | sed "s|$ROOT/||")
  if [[ "$rel" != */* ]]; then
    [[ "$rel" == *scan* || "$rel" == *index* || "$rel" == *context* || "$rel" == crawler* ]] && continue
  fi

  # Check if file has real content (more than just a title/header)
  word_count=$(wc -w < "$file")
  if [ "$word_count" -lt 10 ]; then
    echo "- $rel (${word_count} words)" >> "$EMPTY_LOG"
    continue
  fi

  # Get section
  section=$(echo "$rel" | cut -d'/' -f1)

  if [ "$section" != "$current_section" ]; then
    echo "" >> "$OUTPUT"
    echo "## $section" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    current_section="$section"
  fi

  size=$(wc -c < "$file")
  preview=$(head -5 "$file" | tr '\n' ' ' | cut -c1-250)

  echo "### $rel" >> "$OUTPUT"
  echo "- **Words:** $word_count | **Size:** ${size}b" >> "$OUTPUT"
  echo "- **Preview:** $preview" >> "$OUTPUT"
  echo "" >> "$OUTPUT"

done

echo "✅ Done!"
echo "   Content index → 00_Doctrine/MASTER_INDEX_V2.md"
echo "   Empty files   → 00_Doctrine/EMPTY_FILES_LOG.md"
