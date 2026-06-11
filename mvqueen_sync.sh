#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# MVQUEEN OS — ENTERPRISE SYNC SYSTEM v2.0
# Bidirectional sync: Google Drive ↔ Phone ↔ GitHub
# Features: conflict detection, logging, verification,
#           token expiry alerts, safe archive before delete
# ============================================================

# ── CONFIG ──────────────────────────────────────────────────
PHONE_DIR="/sdcard/MVQUEEN_OS"
DRIVE_REMOTE="gdrive:MVQUEEN_OS"
GITHUB_REMOTE="origin"
GITHUB_BRANCH="main"
TOKEN_FILE="/sdcard/github_token.txt"
LOG_DIR="/sdcard/MVQUEEN_OS/99_Command_Center/sync_logs"
ARCHIVE_DIR="/sdcard/MVQUEEN_OS/98_Archive/pre_delete"
MAX_LOGS=30  # keep last 30 log files

# ── OLD DRIVE FOLDERS TO SAFELY DELETE ──────────────────────
DEPRECATED_FOLDERS=(
  "gdrive:MVQUEEN"
  "gdrive:MVQueen_Optimized_Scripts"
  "gdrive:Mvqueen_engine"
)

# ── COLORS ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── SETUP ───────────────────────────────────────────────────
mkdir -p "$LOG_DIR"
mkdir -p "$ARCHIVE_DIR"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
LOG_FILE="$LOG_DIR/sync_$TIMESTAMP.log"
ERRORS=0
WARNINGS=0

# ── LOGGING ─────────────────────────────────────────────────
log() {
  local level="$1"
  local msg="$2"
  local ts=$(date '+%H:%M:%S')
  echo "[$ts][$level] $msg" >> "$LOG_FILE"
  case "$level" in
    INFO)  echo -e "${CYAN}[$ts]${NC} $msg" ;;
    OK)    echo -e "${GREEN}[$ts] ✅ $msg${NC}" ;;
    WARN)  echo -e "${YELLOW}[$ts] ⚠️  $msg${NC}"; ((WARNINGS++)) ;;
    ERROR) echo -e "${RED}[$ts] ❌ $msg${NC}"; ((ERRORS++)) ;;
    STEP)  echo -e "\n${PURPLE}${BOLD}══ $msg ══${NC}" ;;
  esac
}

# ── HEADER ──────────────────────────────────────────────────
print_header() {
  echo -e "${PURPLE}${BOLD}"
  echo "╔══════════════════════════════════════════╗"
  echo "║     👑 MVQUEEN OS — ENTERPRISE SYNC      ║"
  echo "║         $(date '+%Y-%m-%d %H:%M:%S')         ║"
  echo "╚══════════════════════════════════════════╝"
  echo -e "${NC}"
  log INFO "Sync started — Log: $LOG_FILE"
}

# ── TOKEN CHECK ─────────────────────────────────────────────
check_token() {
  log STEP "GITHUB TOKEN HEALTH CHECK"

  if [ ! -f "$TOKEN_FILE" ]; then
    log ERROR "Token file not found at $TOKEN_FILE"
    log WARN "Run: echo 'YOUR_TOKEN' > $TOKEN_FILE"
    return 1
  fi

  TOKEN=$(cat "$TOKEN_FILE" | tr -d '[:space:]')

  if [ -z "$TOKEN" ]; then
    log ERROR "Token file is empty"
    return 1
  fi

  # Check token validity via GitHub API
  log INFO "Verifying token with GitHub API..."
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token $TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user 2>/dev/null)

  if [ "$RESPONSE" = "200" ]; then
    log OK "GitHub token is valid"

    # Check expiry from API headers
    EXPIRY=$(curl -s -I \
      -H "Authorization: token $TOKEN" \
      https://api.github.com/user 2>/dev/null | \
      grep -i "github-authentication-token-expiration" | \
      awk '{print $2, $3, $4}')

    if [ -n "$EXPIRY" ]; then
      log INFO "Token expires: $EXPIRY"
      # Warn if expiring within 7 days
      EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null)
      NOW_EPOCH=$(date +%s)
      DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
      if [ "$DAYS_LEFT" -lt 7 ] 2>/dev/null; then
        log WARN "Token expires in $DAYS_LEFT days — regenerate soon!"
        log WARN "Run: bash $PHONE_DIR/mvqueen_sync.sh --renew-token"
      fi
    else
      log INFO "Token has no expiry (no-expiration token)"
    fi
  elif [ "$RESPONSE" = "401" ]; then
    log ERROR "Token is INVALID or EXPIRED"
    log WARN "Go to github.com → Settings → Developer settings → Regenerate token"
    log WARN "Then run: echo 'NEW_TOKEN' > $TOKEN_FILE"
    return 1
  else
    log WARN "Could not verify token (HTTP $RESPONSE) — continuing anyway"
  fi

  # Configure git to use token
  git -C "$PHONE_DIR" config credential.helper store
  git -C "$PHONE_DIR" remote set-url origin \
    "https://$(cat $TOKEN_FILE | tr -d '[:space:]')@github.com/juliantevon-droid/MVQUEEN_OS.git" \
    2>/dev/null
  log OK "Git credentials configured"
}

# ── CONFLICT DETECTION ───────────────────────────────────────
check_conflicts() {
  log STEP "CONFLICT DETECTION"
  cd "$PHONE_DIR" || return 1

  # Check for uncommitted local changes
  CHANGED=$(git status --porcelain 2>/dev/null | wc -l)
  if [ "$CHANGED" -gt 0 ]; then
    log WARN "$CHANGED local files have changes — will be committed"
    git status --porcelain >> "$LOG_FILE"
  else
    log OK "No uncommitted conflicts detected"
  fi

  # Check if remote has changes we don't have
  git fetch origin "$GITHUB_BRANCH" --quiet 2>/dev/null
  BEHIND=$(git rev-list HEAD..origin/$GITHUB_BRANCH --count 2>/dev/null)
  AHEAD=$(git rev-list origin/$GITHUB_BRANCH..HEAD --count 2>/dev/null)

  if [ "$BEHIND" -gt 0 ]; then
    log WARN "Local is $BEHIND commits behind GitHub — will pull first"
  fi
  if [ "$AHEAD" -gt 0 ]; then
    log INFO "Local is $AHEAD commits ahead of GitHub — will push"
  fi
  if [ "$BEHIND" = "0" ] && [ "$AHEAD" = "0" ]; then
    log OK "Phone and GitHub are already in sync"
  fi
}

# ── PHASE 1: DRIVE → PHONE ───────────────────────────────────
sync_drive_to_phone() {
  log STEP "PHASE 1 — GOOGLE DRIVE → PHONE"
  log INFO "Pulling latest from Drive..."

  SYNC_OUTPUT=$(rclone sync "$DRIVE_REMOTE" "$PHONE_DIR" \
    --exclude ".git/**" \
    --exclude "*.tmp" \
    --exclude ".DS_Store" \
    --log-level INFO \
    2>&1)

  TRANSFERRED=$(echo "$SYNC_OUTPUT" | grep "Transferred:" | tail -1)
  CHECKS=$(echo "$SYNC_OUTPUT" | grep "Checks:" | tail -1)

  echo "$SYNC_OUTPUT" >> "$LOG_FILE"
  log OK "Drive → Phone complete | $TRANSFERRED | $CHECKS"
}

# ── PHASE 2: GIT PULL ────────────────────────────────────────
sync_github_pull() {
  log STEP "PHASE 2 — GITHUB → PHONE (PULL)"
  cd "$PHONE_DIR" || return 1

  PULL_OUTPUT=$(git pull origin "$GITHUB_BRANCH" 2>&1)
  echo "$PULL_OUTPUT" >> "$LOG_FILE"

  if echo "$PULL_OUTPUT" | grep -q "Already up to date"; then
    log OK "GitHub already up to date — nothing to pull"
  elif echo "$PULL_OUTPUT" | grep -q "CONFLICT"; then
    log ERROR "Git merge conflict detected!"
    log WARN "Resolve manually then re-run sync"
    return 1
  else
    log OK "GitHub pull complete"
  fi
}

# ── PHASE 3: COMMIT & PUSH ───────────────────────────────────
sync_phone_to_github() {
  log STEP "PHASE 3 — PHONE → GITHUB (PUSH)"
  cd "$PHONE_DIR" || return 1

  # Check if there's anything to commit
  CHANGED=$(git status --porcelain 2>/dev/null | wc -l)
  if [ "$CHANGED" -eq 0 ]; then
    log OK "Nothing to commit — GitHub already current"
    return 0
  fi

  git add . 2>> "$LOG_FILE"

  # Build smart commit message
  ADDED=$(git status --porcelain | grep "^A" | wc -l)
  MODIFIED=$(git status --porcelain | grep "^M" | wc -l)
  DELETED=$(git status --porcelain | grep "^D" | wc -l)
  COMMIT_MSG="🔄 Auto-sync $TIMESTAMP | +$ADDED ~$MODIFIED -$DELETED files"

  git commit -m "$COMMIT_MSG" 2>> "$LOG_FILE"
  PUSH_OUTPUT=$(git push origin "$GITHUB_BRANCH" 2>&1)
  echo "$PUSH_OUTPUT" >> "$LOG_FILE"

  if echo "$PUSH_OUTPUT" | grep -q "main -> main"; then
    log OK "GitHub push complete | $COMMIT_MSG"
  else
    log ERROR "GitHub push failed — check token"
    echo "$PUSH_OUTPUT"
    return 1
  fi
}

# ── PHASE 4: PHONE → DRIVE ───────────────────────────────────
sync_phone_to_drive() {
  log STEP "PHASE 4 — PHONE → GOOGLE DRIVE (PUSH)"
  log INFO "Pushing updates to Drive..."

  SYNC_OUTPUT=$(rclone sync "$PHONE_DIR" "$DRIVE_REMOTE" \
    --exclude ".git/**" \
    --exclude "*.tmp" \
    --exclude ".DS_Store" \
    --log-level INFO \
    2>&1)

  TRANSFERRED=$(echo "$SYNC_OUTPUT" | grep "Transferred:" | tail -1)
  echo "$SYNC_OUTPUT" >> "$LOG_FILE"
  log OK "Phone → Drive complete | $TRANSFERRED"
}

# ── SAFE ARCHIVE & DELETE OLD FOLDERS ────────────────────────
archive_deprecated_folders() {
  log STEP "ARCHIVING DEPRECATED DRIVE FOLDERS"
  log INFO "Checking deprecated folders before deletion..."

  for FOLDER in "${DEPRECATED_FOLDERS[@]}"; do
    FOLDER_NAME=$(basename "$FOLDER")
    log INFO "Checking: $FOLDER_NAME"

    # Count files in folder
    FILE_COUNT=$(rclone ls "$FOLDER" 2>/dev/null | wc -l)

    if [ "$FILE_COUNT" -eq 0 ]; then
      log OK "$FOLDER_NAME is empty — safe to delete manually"
    else
      log INFO "$FOLDER_NAME has $FILE_COUNT files — archiving first..."

      # Copy to archive inside MVQUEEN_OS on Drive
      rclone copy "$FOLDER" \
        "gdrive:MVQUEEN_OS/98_Archive/deprecated_$FOLDER_NAME" \
        --progress 2>> "$LOG_FILE"

      log OK "$FOLDER_NAME archived to 98_Archive/deprecated_$FOLDER_NAME"
      log WARN "$FOLDER_NAME can now be safely deleted from Drive manually"
    fi
  done

  log INFO "To delete: open drive.google.com → right-click folder → Move to trash"
}

# ── VERIFICATION ─────────────────────────────────────────────
verify_sync() {
  log STEP "VERIFICATION"

  # Count files in each location
  PHONE_COUNT=$(find "$PHONE_DIR" -type f \
    ! -path "*/.git/*" | wc -l)
  DRIVE_COUNT=$(rclone ls "$DRIVE_REMOTE" 2>/dev/null | wc -l)
  GITHUB_COMMITS=$(git -C "$PHONE_DIR" \
    rev-list --count HEAD 2>/dev/null)

  log INFO "Phone files:     $PHONE_COUNT"
  log INFO "Drive files:     $DRIVE_COUNT"
  log INFO "GitHub commits:  $GITHUB_COMMITS"

  # Check if counts are reasonably close (within 5%)
  DIFF=$(( PHONE_COUNT - DRIVE_COUNT ))
  DIFF=${DIFF#-}  # absolute value
  THRESHOLD=$(( PHONE_COUNT / 20 ))  # 5%

  if [ "$DIFF" -le "$THRESHOLD" ]; then
    log OK "File counts match within acceptable range"
  else
    log WARN "File count mismatch: Phone=$PHONE_COUNT Drive=$DRIVE_COUNT"
    log WARN "Run sync again or check for errors in log"
  fi
}

# ── CLEANUP OLD LOGS ─────────────────────────────────────────
cleanup_logs() {
  LOG_COUNT=$(ls "$LOG_DIR"/sync_*.log 2>/dev/null | wc -l)
  if [ "$LOG_COUNT" -gt "$MAX_LOGS" ]; then
    ls -t "$LOG_DIR"/sync_*.log | tail -n +$((MAX_LOGS + 1)) | \
      xargs rm -f
    log INFO "Cleaned up old logs — keeping last $MAX_LOGS"
  fi
}

# ── SUMMARY ──────────────────────────────────────────────────
print_summary() {
  echo -e "\n${PURPLE}${BOLD}"
  echo "╔══════════════════════════════════════════╗"
  echo "║           SYNC SUMMARY                   ║"
  echo "╠══════════════════════════════════════════╣"
  if [ "$ERRORS" -eq 0 ]; then
    echo -e "║  ${GREEN}Status:  ✅ ALL SYSTEMS ALIGNED${PURPLE}           ║"
  else
    echo -e "║  ${RED}Status:  ❌ COMPLETED WITH ERRORS${PURPLE}         ║"
  fi
  echo "║  Errors:   $ERRORS"
  echo "║  Warnings: $WARNINGS"
  echo "║  Log:      sync_$TIMESTAMP.log"
  echo "╚══════════════════════════════════════════╝"
  echo -e "${NC}"

  if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}Check log for details: cat $LOG_FILE${NC}"
  fi
}

# ── ARGUMENT HANDLING ────────────────────────────────────────
handle_args() {
  case "$1" in
    --archive-old)
      print_header
      check_token
      archive_deprecated_folders
      print_summary
      exit 0
      ;;
    --verify)
      print_header
      verify_sync
      print_summary
      exit 0
      ;;
    --renew-token)
      echo -e "${YELLOW}To renew your GitHub token:${NC}"
      echo "1. Go to: github.com/settings/tokens"
      echo "2. Find 'Termux' token → Regenerate"
      echo "3. Copy the new token"
      echo "4. Run: echo 'NEW_TOKEN' > $TOKEN_FILE"
      echo "5. Run this sync script again"
      exit 0
      ;;
    --logs)
      ls -lt "$LOG_DIR"/sync_*.log 2>/dev/null | head -10
      exit 0
      ;;
    --help)
      echo -e "${CYAN}MVQUEEN OS Sync — Usage:${NC}"
      echo "  bash mvqueen_sync.sh              # Full sync"
      echo "  bash mvqueen_sync.sh --archive-old # Archive deprecated folders"
      echo "  bash mvqueen_sync.sh --verify      # Verify sync status"
      echo "  bash mvqueen_sync.sh --renew-token # Token renewal guide"
      echo "  bash mvqueen_sync.sh --logs        # View recent logs"
      exit 0
      ;;
  esac
}

# ── MAIN ─────────────────────────────────────────────────────
main() {
  handle_args "$1"
  print_header
  check_token       || { log ERROR "Token check failed — aborting"; exit 1; }
  check_conflicts
  sync_drive_to_phone
  sync_github_pull
  sync_phone_to_github
  sync_phone_to_drive
  verify_sync
  cleanup_logs
  print_summary
}

main "$@"
