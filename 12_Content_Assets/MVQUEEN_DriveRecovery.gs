/\*\*  
 \* MVQUEEN Drive Recovery Script  
 \* ─────────────────────────────────────────────────────────────────  
 \* PURPOSE:  
 \*   1\. Find all MVQUEEN and MVQUEEN\_OS folders in Drive (including  
 \*      trashed, orphaned, or re-parented ones)  
 \*   2\. Show what exists and where it currently lives  
 \*   3\. Restore drifted folders back to the correct parent  
 \*   4\. Un-trash any folders that were accidentally deleted  
 \*  
 \* HOW TO USE:  
 \*   1\. Go to script.google.com → New Project  
 \*   2\. Paste this entire file in  
 \*   3\. Run AUDIT\_ONLY first (safe, read-only)  
 \*   4\. Check the Execution Log (View → Logs)  
 \*   5\. If things look right, run RESTORE\_DRIFTED\_FOLDERS  
 \*  
 \* KNOWN ROOT IDs (from your OS):  
 \*   MVQUEEN\_OS root  → 1i1Q8ifbFhzJx8n59Hsth-kZt\_ofkoM\_H  
 \*   (MVQUEEN brand folder — set MVQUEEN\_ROOT\_ID below once confirmed)  
 \* ─────────────────────────────────────────────────────────────────  
 \*/

// ── CONFIGURE THESE ──────────────────────────────────────────────  
const MVQUEEN\_OS\_ROOT\_ID  \= '1i1Q8ifbFhzJx8n59Hsth-kZt\_ofkoM\_H';  
const MVQUEEN\_ROOT\_ID     \= '';   // Fill this in if you know it, or leave blank

// Names to search for (partial match, case-insensitive in Apps Script)  
const TARGET\_NAMES \= \['MVQUEEN', 'MVQUEEN\_OS', 'Miss. Princess', 'Miss Princess'\];

// How many days back to look for recently modified/trashed files  
const DAYS\_BACK \= 7;  
// ─────────────────────────────────────────────────────────────────

/\*\*  
 \* STEP 1 — Run this first. Safe, read-only audit.  
 \* Check Execution Log (View → Logs) for results.  
 \*/  
function AUDIT\_ONLY() {  
  Logger.log('════════════════════════════════════════');  
  Logger.log('  MVQUEEN DRIVE AUDIT  —  ' \+ new Date().toLocaleString());  
  Logger.log('════════════════════════════════════════\\n');

  // 1a. Check known root folders  
  \_checkKnownRoot('MVQUEEN\_OS', MVQUEEN\_OS\_ROOT\_ID);  
  if (MVQUEEN\_ROOT\_ID) \_checkKnownRoot('MVQUEEN brand root', MVQUEEN\_ROOT\_ID);

  // 1b. Search all folders matching target names (including trashed)  
  Logger.log('\\n── SEARCHING ALL MATCHING FOLDERS ──────');  
  TARGET\_NAMES.forEach(name \=\> \_searchFolders(name, false));

  // 1c. Search trashed only  
  Logger.log('\\n── TRASHED FOLDERS ──────────────────────');  
  TARGET\_NAMES.forEach(name \=\> \_searchFolders(name, true));

  // 1d. Show recently modified files in MVQUEEN\_OS root  
  Logger.log('\\n── RECENT ACTIVITY IN MVQUEEN\_OS ROOT ──');  
  \_listRecentInFolder(MVQUEEN\_OS\_ROOT\_ID, DAYS\_BACK);

  Logger.log('\\n════ AUDIT COMPLETE ════════════════════\\n');  
  Logger.log('Next step: review the log, then run RESTORE\_DRIFTED\_FOLDERS if needed.');  
}

/\*\*  
 \* STEP 2 — Restore drifted or trashed folders.  
 \* Only run after reviewing AUDIT\_ONLY output.  
 \*/  
function RESTORE\_DRIFTED\_FOLDERS() {  
  Logger.log('════════════════════════════════════════');  
  Logger.log('  MVQUEEN RESTORE  —  ' \+ new Date().toLocaleString());  
  Logger.log('════════════════════════════════════════\\n');

  let restored \= 0;  
  let errors   \= 0;

  TARGET\_NAMES.forEach(name \=\> {  
    const query \= \`mimeType \= 'application/vnd.google-apps.folder' and title contains '${name}' and trashed \= true\`;  
    const files \= \_driveSearch(query);

    files.forEach(f \=\> {  
      try {  
        // Un-trash it  
        Drive.Files.update({ trashed: false }, f.id);  
        Logger.log(\`✅ UN-TRASHED: "${f.title}" (${f.id})\`);

        // Re-parent to MVQUEEN\_OS root if it's an OS subfolder  
        if (f.title.match(/MVQUEEN\_OS|^\\d{2}\_/)) {  
          Drive.Files.update({}, f.id, null, {  
            addParents: MVQUEEN\_OS\_ROOT\_ID,  
            removeParents: \_getOrphanParent(f)  
          });  
          Logger.log(\`  → Re-parented to MVQUEEN\_OS root\`);  
        }

        restored++;  
      } catch (e) {  
        Logger.log(\`❌ FAILED to restore "${f.title}": ${e.message}\`);  
        errors++;  
      }  
    });  
  });

  Logger.log(\`\\n────────────────────────────────────────\`);  
  Logger.log(\`Restored: ${restored} | Errors: ${errors}\`);  
  Logger.log('════ RESTORE COMPLETE ══════════════════\\n');  
}

/\*\*  
 \* STEP 3 — Pull a snapshot of ALL folders inside MVQUEEN\_OS  
 \* and log them with their parent chain. Use this to spot  
 \* anything that drifted to the wrong subfolder.  
 \*/  
function SNAPSHOT\_MVQUEEN\_OS() {  
  Logger.log('════════════════════════════════════════');  
  Logger.log('  MVQUEEN\_OS FULL SNAPSHOT');  
  Logger.log('════════════════════════════════════════\\n');

  \_recursiveList(MVQUEEN\_OS\_ROOT\_ID, 'MVQUEEN\_OS', 0);

  Logger.log('\\n════ SNAPSHOT COMPLETE ═════════════════');  
}

/\*\*  
 \* STEP 4 — Recovery by date. Find anything modified or trashed  
 \* in the last N days across your entire Drive matching MVQUEEN.  
 \*/  
function FIND\_RECENTLY\_CHANGED() {  
  const cutoff \= new Date();  
  cutoff.setDate(cutoff.getDate() \- DAYS\_BACK);  
  const iso \= cutoff.toISOString();

  Logger.log('════════════════════════════════════════');  
  Logger.log(\`  CHANGES SINCE: ${cutoff.toDateString()}\`);  
  Logger.log('════════════════════════════════════════\\n');

  // Modified recently  
  const modQuery \= \`title contains 'MVQUEEN' and modifiedDate \> '${iso}'\`;  
  const modFiles \= \_driveSearch(modQuery);  
  Logger.log(\`── RECENTLY MODIFIED (${modFiles.length} items) ──\`);  
  modFiles.forEach(f \=\> Logger.log(\`  \[${f.mimeType \=== 'application/vnd.google-apps.folder' ? 'DIR' : 'FILE'}\] ${f.title}  |  id: ${f.id}  |  modified: ${f.modifiedDate}  |  trashed: ${f.labels.trashed}\`));

  // Trashed recently  
  const trashQuery \= \`title contains 'MVQUEEN' and trashed \= true\`;  
  const trashFiles \= \_driveSearch(trashQuery);  
  Logger.log(\`\\n── TRASHED ITEMS (${trashFiles.length} items) ──\`);  
  trashFiles.forEach(f \=\> Logger.log(\`  \[${f.mimeType \=== 'application/vnd.google-apps.folder' ? 'DIR' : 'FILE'}\] ${f.title}  |  id: ${f.id}  |  trashed: ${f.labels.trashed}\`));

  Logger.log('\\n════ DONE ══════════════════════════════');  
}

// ─── INTERNAL HELPERS ────────────────────────────────────────────

function \_checkKnownRoot(label, folderId) {  
  if (\!folderId) return;  
  try {  
    const meta \= Drive.Files.get(folderId, { fields: 'id,title,labels,parents,modifiedDate' });  
    Logger.log(\`\[${label}\]\`);  
    Logger.log(\`  ID       : ${meta.id}\`);  
    Logger.log(\`  Title    : ${meta.title}\`);  
    Logger.log(\`  Trashed  : ${meta.labels.trashed}\`);  
    Logger.log(\`  Modified : ${meta.modifiedDate}\`);  
    Logger.log(\`  Parents  : ${JSON.stringify(meta.parents)}\`);  
  } catch (e) {  
    Logger.log(\`\[${label}\] ❌ Could not fetch — ${e.message}\`);  
  }  
}

function \_searchFolders(name, trashedOnly) {  
  const trashClause \= trashedOnly ? 'trashed \= true' : 'trashed \= false';  
  const query \= \`mimeType \= 'application/vnd.google-apps.folder' and title contains '${name}' and ${trashClause}\`;  
  const results \= \_driveSearch(query);

  if (results.length \=== 0\) {  
    Logger.log(\`  "${name}" — no ${trashedOnly ? 'trashed' : 'active'} folders found\`);  
    return;  
  }

  results.forEach(f \=\> {  
    const parentIds \= (f.parents || \[\]).map(p \=\> p.id).join(', ');  
    Logger.log(\`  ${trashedOnly ? '🗑' : '📁'} "${f.title}"  |  id: ${f.id}  |  parents: \[${parentIds}\]  |  modified: ${f.modifiedDate}\`);  
  });  
}

function \_listRecentInFolder(folderId, daysBack) {  
  if (\!folderId) return;  
  const cutoff \= new Date();  
  cutoff.setDate(cutoff.getDate() \- daysBack);  
  const iso \= cutoff.toISOString();

  const query \= \`'${folderId}' in parents and modifiedDate \> '${iso}'\`;  
  const results \= \_driveSearch(query);

  if (results.length \=== 0\) {  
    Logger.log(\`  No items modified in last ${daysBack} days in this folder.\`);  
    return;  
  }

  results.forEach(f \=\> {  
    const type \= f.mimeType \=== 'application/vnd.google-apps.folder' ? 'DIR' : 'FILE';  
    Logger.log(\`  \[${type}\] "${f.title}"  |  modified: ${f.modifiedDate}  |  trashed: ${f.labels.trashed}\`);  
  });  
}

function \_recursiveList(folderId, path, depth) {  
  if (depth \> 4\) return; // Safety limit  
  const query \= \`'${folderId}' in parents and trashed \= false\`;  
  const results \= \_driveSearch(query);

  results.forEach(f \=\> {  
    const indent \= '  '.repeat(depth);  
    const type   \= f.mimeType \=== 'application/vnd.google-apps.folder' ? '📁' : '📄';  
    Logger.log(\`${indent}${type} ${path}/${f.title}  \[${f.id}\]\`);

    if (f.mimeType \=== 'application/vnd.google-apps.folder') {  
      \_recursiveList(f.id, \`${path}/${f.title}\`, depth \+ 1);  
    }  
  });  
}

function \_getOrphanParent(file) {  
  // Returns current parent ID to remove when re-parenting  
  if (file.parents && file.parents.length \> 0\) {  
    return file.parents.map(p \=\> p.id).join(',');  
  }  
  return '';  
}

function \_driveSearch(query) {  
  try {  
    const response \= Drive.Files.list({  
      q: query,  
      maxResults: 200,  
      fields: 'items(id,title,mimeType,modifiedDate,labels,parents)',  
      includeItemsFromAllDrives: true,  
      supportsAllDrives: true  
    });  
    return response.items || \[\];  
  } catch (e) {  
    Logger.log(\`  ⚠ Search error: ${e.message}\`);  
    return \[\];  
  }  
}

// ─────────────────────────────────────────────────────────────────  
// ENABLE ADVANCED DRIVE SERVICE:  
//   In the Script Editor → Services (+ icon) → Drive API → Add  
//   This script uses Drive.Files.list / get / update which require  
//   the Advanced Drive Service, NOT just DriveApp.  
// ─────────────────────────────────────────────────────────────────  
