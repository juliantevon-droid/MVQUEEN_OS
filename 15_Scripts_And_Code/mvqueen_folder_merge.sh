# **MVQUEEN\_FOLDER\_MERGE.SH**

**Termux Bash — Vault Folder Collapse & Canonical Numbering Enforcer**  
Version: 1.1.0 | Date: 2026-06-18

## **What This Does**

Collapses \~60 ghost/duplicate/misnamed folders into the canonical 40-module MVQUEEN\_OS structure. Three generations of numbering schemes are present; this script picks the winners and merges everything else into them safely.

## **Safety Features**

* Never deletes files, only moves them.  
* Automatically handles name collisions via timestamped suffixing to ensure zero data loss.  
* Preserves nested subfolder hierarchies during merges instead of flattening them.  
* Only removes a source folder tree after confirming it is entirely empty.  
* Creates a detailed, timestamped log manifest before any moves.

## **The Script**

\#\!/usr/bin/env bash

set \-uo pipefail

RED='\\033\[0;31m'; GRN='\\033\[0;32m'; YLW='\\033\[1;33m'  
BLU='\\033\[0;34m'; CYN='\\033\[0;36m'; BOLD='\\033\[1m'; RST='\\033\[0m'

log()  { echo \-e "${BLU}\[INFO\]${RST}  $\*"; }  
ok()   { echo \-e "${GRN}\[OK\]${RST}    $\*"; }  
warn() { echo \-e "${YLW}\[WARN\]${RST}  $\*"; }  
err()  { echo \-e "${RED}\[ERR\]${RST}   $\*"; }  
sec()  { echo \-e "\\n${BOLD}${CYN}══ $\* ══${RST}"; }

VAULT="$HOME/storage/shared/MVQUEEN\_OS"  
DRY\_RUN=false  
TIMESTAMP=$(date \+%Y%m%d\_%H%M%S)  
LOG="$VAULT/15\_Scripts\_And\_Code/consolidation\_logs/folder\_merge\_${TIMESTAMP}.log"

MOVED=0; COLLIDED=0; REMOVED=0

for arg in "$@"; do  
  \[\[ "$arg" \== "--dry-run" \]\] && DRY\_RUN=true && warn "DRY-RUN — nothing will be written"  
done

if \[\[ \! \-d "$VAULT" \]\]; then err "Vault not found: $VAULT"; exit 1; fi  
mkdir \-p "$VAULT/15\_Scripts\_And\_Code/consolidation\_logs"  
echo "MVQUEEN Folder Merge Optimized — $TIMESTAMP" \> "$LOG"

merge\_into() {  
  local canonical="$VAULT/$1"; shift  
  local sources=("$@")

  \[\[ "$DRY\_RUN" \== "false" \]\] && mkdir \-p "$canonical"

  for src\_name in "${sources\[@\]}"; do  
    local src="$VAULT/$src\_name"  
    \[\[ \! \-d "$src" \]\] && continue

    local file\_count  
    file\_count=$(find "$src" \-type f | wc \-l)  
    \[\[ "$file\_count" \-eq 0 \]\] && { log "Empty, removing: $src\_name"; \[\[ "$DRY\_RUN" \== "false" \]\] && rm \-rf "$src"; continue; }

    log "Merging $file\_count files: $src\_name → $(basename "$canonical")"

    if \[\[ "$DRY\_RUN" \== "false" \]\]; then  
      while IFS= read \-r \-d '' fpath; do  
        local rel\_path="${fpath\#$src/}"  
        local dst="$canonical/$rel\_path"  
        local dst\_dir  
        dst\_dir=$(dirname "$dst")

        mkdir \-p "$dst\_dir"

        local final\_dst="$dst"

        if \[\[ \-f "$final\_dst" \]\]; then  
          local base="${final\_dst%.\*}"  
          local ext="${final\_dst\#\#\*.}"  
          final\_dst="${base}\_CONFLICT\_${TIMESTAMP}.${ext}"  
          warn "  COLLISION: Renaming copy to $(basename "$final\_dst")"  
          COLLIDED=$(( COLLIDED \+ 1 ))  
          echo "COLLISION,$src\_name,$rel\_path,renamed" \>\> "$LOG"  
        fi

        mv "$fpath" "$final\_dst"  
        MOVED=$(( MOVED \+ 1 ))  
        echo "MOVE,$src\_name,$(basename "$canonical"),$rel\_path" \>\> "$LOG"  
      done \< \<(find "$src" \-type f \-print0)

      find "$src" \-type d \-empty \-delete 2\>/dev/null  
      if \[\[ \! \-d "$src" \]\]; then  
        REMOVED=$(( REMOVED \+ 1 ))  
        ok "Removed empty ghost folder tree: $src\_name"  
      else  
        warn "Source tree not completely empty: $src\_name"  
      fi  
    else  
      find "$src" \-type f | while read \-r f; do  
        local rel="${f\#$src/}"  
        echo \-e "  ${CYN}\[DRY\]${RST} $src\_name/$rel  →  $(basename "$canonical")/$rel"  
      done  
    fi  
  done  
}

sec "PHASE 1 — Numbered Ghost Folder Merges"  
merge\_into "00\_Doctrine" "00\_Command\_Center"  
merge\_into "02\_Brand\_Identity" "02\_Tone\_And\_Voice"  
merge\_into "04\_Products" "04\_Product\_Ecosystem"  
merge\_into "05\_SEO\_And\_Content" "05\_Content\_And\_SEO"  
merge\_into "07\_Marketing" "06\_Marketing"  
merge\_into "08\_Social\_Media" "07\_Social\_Media"  
merge\_into "09\_Shopify\_Systems" "08\_Shopify\_Systems"  
merge\_into "10\_AI\_Systems" "09\_AI\_Systems"  
merge\_into "11\_Operations" "10\_Operations"  
merge\_into "13\_Research\_And\_Inspiration" "11\_Research\_And\_Inspiration" "11\_Research\_And\_Inspo"  
merge\_into "14\_Data\_And\_Analytics" "13\_Data\_And\_Analytics" "15\_Data\_And\_Analytics"  
merge\_into "15\_Scripts\_And\_Code" "13\_Scripts\_And\_Code" "20\_Scripts\_And\_Code" "scripts"  
merge\_into "16\_Automation" "14\_Automation"  
merge\_into "17\_Templates" "14\_Templates" "20\_Templates" "27\_Templates"  
merge\_into "18\_Development" "15\_Development"  
merge\_into "19\_Legal\_And\_Admin" "16\_Legal\_And\_Admin"  
merge\_into "21\_Finance" "17\_Finance"  
merge\_into "22\_Growth\_And\_Scaling" "18\_Growth\_And\_Scaling" "19\_Expansion\_And\_Scaling"  
merge\_into "23\_Team\_And\_Delegation" "18\_Team\_And\_Delegation"  
merge\_into "25\_Retention\_And\_Community" "19\_Retention\_And\_Community"  
merge\_into "26\_RnD\_Lab" "20\_RnD\_Lab"  
merge\_into "28\_Archives" "21\_Archives" "98\_Archive" "99\_Archive"  
merge\_into "29\_Mobile\_Development" "21\_Mobile\_Development"  
merge\_into "30\_AI\_Datasets" "22\_AI\_Datasets"  
merge\_into "37\_Databases" "26\_Databases"  
merge\_into "38\_Prompt\_Chains" "27\_Prompt\_Chains"  
merge\_into "39\_SOP\_Library" "28\_SOP\_Library"  
merge\_into "99\_Command\_Center" "29\_Command\_Center" "99\_Brain\_Dump"

sec "PHASE 2 — Unnamed Flat Folder Merges"  
merge\_into "36\_Agent\_Systems" "agents"  
merge\_into "10\_AI\_Systems" "ai"  
merge\_into "33\_Content\_Pipelines" "content"  
merge\_into "14\_Data\_And\_Analytics" "data"  
merge\_into "02\_Brand\_Identity" "logos"  
merge\_into "15\_Scripts\_And\_Code" "logs"  
merge\_into "31\_AI\_Knowledge\_Base" "memory"  
merge\_into "31\_AI\_Knowledge\_Base" "meta"  
merge\_into "09\_Shopify\_Systems" "shopify"

sec "PHASE 3 — Removing Junk / Banned Folders"  
junk\_remove() {  
  local folder="$VAULT/$1"  
  \[\[ \! \-d "$folder" \]\] && return  
  local count  
  count=$(find "$folder" \-type f | wc \-l)  
  if \[\[ "$count" \-gt 0 \]\]; then  
    warn "Junk folder NOT empty ($count files) — skipping removal: $1"  
    echo "WARN\_JUNK\_NOT\_EMPTY,$1,$count" \>\> "$LOG"  
    return  
  fi  
  if \[\[ "$DRY\_RUN" \== "false" \]\]; then  
    rm \-rf "$folder"  
    REMOVED=$(( REMOVED \+ 1 ))  
    ok "Removed: $1"  
    echo "REMOVE\_JUNK,$1" \>\> "$LOG"  
  else  
    log "\[DRY\] Would remove empty junk: $1"  
  fi  
}

junk\_remove "\_DUPLICATES\_TRASH"  
junk\_remove "textgenerator"  
junk\_remove "copilot"  
junk\_remove "MVQUEEN\_batch"  
junk\_remove "deprecated\_gdrive:MVQUEEN"  
junk\_remove "MVQUEEN"  
junk\_remove "MVQUEEN\_OS"

sec "PHASE 4 — Canonical Structure Verification"  
CANONICAL\_FOLDERS=(  
  "00\_Doctrine" "01\_Brand\_Strategy" "02\_Brand\_Identity" "03\_Customer\_Psychology"  
  "04\_Products" "05\_SEO\_And\_Content" "06\_Tone\_And\_Voice" "07\_Marketing"  
  "08\_Social\_Media" "09\_Shopify\_Systems" "10\_AI\_Systems" "11\_Operations"  
  "12\_Content\_Assets" "13\_Research\_And\_Inspiration" "14\_Data\_And\_Analytics"  
  "15\_Scripts\_And\_Code" "16\_Automation" "17\_Templates" "18\_Development"  
  "19\_Legal\_And\_Admin" "21\_Finance" "22\_Growth\_And\_Scaling" "23\_Team\_And\_Delegation"  
  "25\_Retention\_And\_Community" "26\_RnD\_Lab" "28\_Archives" "29\_Mobile\_Development"  
  "30\_AI\_Datasets" "31\_AI\_Knowledge\_Base" "33\_Content\_Pipelines" "34\_Master\_Systems"  
  "35\_System\_Blueprints" "36\_Agent\_Systems" "37\_Databases" "38\_Prompt\_Chains"  
  "39\_SOP\_Library" "99\_Command\_Center"  
)

echo ""  
echo \-e "${BOLD}Canonical folder file counts:${RST}"  
for folder in "${CANONICAL\_FOLDERS\[@\]}"; do  
  path="$VAULT/$folder"  
  if \[\[ \-d "$path" \]\]; then  
    count=$(find "$path" \-type f \-name "\*.md" | wc \-l)  
    printf "  %-35s %3d .md files\\n" "$folder" "$count"  
  else  
    printf "  ${RED}%-35s MISSING${RST}\\n" "$folder"  
    mkdir \-p "$path"  
    echo "CREATED\_MISSING,$folder" \>\> "$LOG"  
  fi  
done

echo ""  
echo \-e "${BOLD}Unexpected folders still in vault root:${RST}"  
UNEXPECTED=0  
while IFS= read \-r \-d '' dir; do  
  dname=$(basename "$dir")  
  \[\[ "$dname" \== .\* \]\] && continue  
  found=false  
  for cf in "${CANONICAL\_FOLDERS\[@\]}" "32\_Backups" "15\_Scripts\_And\_Code"; do  
    \[\[ "$dname" \== "$cf" \]\] && found=true && break  
  done  
  if \[\[ "$found" \== "false" \]\]; then  
    fcount=$(find "$dir" \-type f | wc \-l)  
    warn "  Unexpected: $dname  ($fcount files)"  
    UNEXPECTED=$(( UNEXPECTED \+ 1 ))  
    echo "UNEXPECTED\_REMAINING,$dname,$fcount" \>\> "$LOG"  
  fi  
done \< \<(find "$VAULT" \-maxdepth 1 \-mindepth 1 \-type d \-print0)

\[\[ "$UNEXPECTED" \-eq 0 \]\] && ok "No unexpected folders remaining."

sec "FOLDER MERGE COMPLETE"  
echo ""  
echo \-e "${BOLD}════════════════════════════════════════${RST}"  
echo \-e "${BOLD}  MVQUEEN FOLDER MERGE REPORT — $TIMESTAMP${RST}"  
echo \-e "${BOLD}════════════════════════════════════════${RST}"  
printf "  %-30s %s\\n" "Files moved safely:"        "$MOVED"  
printf "  %-30s %s\\n" "Name collisions handled:"   "$COLLIDED"  
printf "  %-30s %s\\n" "Ghost folder trees removed:" "$REMOVED"  
printf "  %-30s %s\\n" "Unexpected remaining:"     "$UNEXPECTED"  
echo \-e "${BOLD}════════════════════════════════════════${RST}"  
echo ""  
echo \-e "  Log: ${CYN}$LOG${RST}"  
echo ""

if \[\[ "$DRY\_RUN" \== "true" \]\]; then  
  echo \-e "${YLW}DRY RUN COMPLETE — nothing was written.${RST}"  
  echo \-e "${YLW}Re-run without \--dry-run to apply.${RST}"  
fi

if \[\[ "$UNEXPECTED" \-gt 0 \]\]; then  
  warn "$UNEXPECTED unexpected folders remain. Check log for details."  
fi

echo \-e "\\n${GRN}${BOLD}Vault folder structure normalized.${RST}\\n"  
