#!/bin/bash
DRIVE_ROOT="gdrive:MVQUEEN_OS"
LOCAL_ROOT="$HOME/MVQUEEN_OS"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MVQUEEN_OS — HTML File Fix"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v rclone &> /dev/null; then
  echo "❌ rclone not found. Install: pkg install rclone"
  exit 1
fi

FILES=("index.html" "brand-themes.html" "os-dashboard.html")

echo "▶ Checking local files..."
for f in "${FILES[@]}"; do
  if [ -f "$LOCAL_ROOT/$f" ]; then
    echo "  ✓ $f found"
  else
    echo "  ✗ $f MISSING"
  fi
done

echo "▶ Pushing to Drive..."
for f in "${FILES[@]}"; do
  if [ -f "$LOCAL_ROOT/$f" ]; then
    rclone copyto "$LOCAL_ROOT/$f" "$DRIVE_ROOT/$f"
    echo "  ✓ Pushed: $f"
  fi
done

echo "▶ Verifying..."
rclone ls "$DRIVE_ROOT" --include "*.html"
echo "Done."
