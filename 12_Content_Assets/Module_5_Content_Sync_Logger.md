MVQUEEN OS - Module 5: Content Sync Logger Script
This document contains the final module for the MVQUEEN OS suite: The Content Sync Logger. It tracks exactly which modules and assets have been modified within the last 7 days, maintaining a clean ledger of your active workflow.
1. The Apps Script Code
/**
* MVQUEEN OS - Content Sync Logger
* Scans all files and logs any assets modified within the last 7 days.
*/
function logMVQUEENContentSync() {
 const ROOT_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE';
 const rootFolder = DriveApp.getFolderById(ROOT_FOLDER_ID);
 const subFolders = rootFolder.getFolders();

 let updatedAssets = [];
 let oneWeekAgo = new Date();
 oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

 Logger.log("Scanning for MVQUEEN OS pipeline updates from the past 7 days...");

 while (subFolders.hasNext()) {
   let folder = subFolders.next();
   let folderName = folder.getName();
   let files = folder.getFiles();

   while (files.hasNext()) {
     let file = files.next();
     let lastUpdated = file.getLastUpdated();

     if (lastUpdated > oneWeekAgo) {
       updatedAssets.push([
         folderName,
         file.getName(),
         lastUpdated.toLocaleDateString() + " " + lastUpdated.toLocaleTimeString(),
         file.getUrl()
       ]);
     }
   }
 }

 // Output findings to a dedicated tab inside the Health Report Spreadsheet
 let reportFiles = rootFolder.getFilesByName("MVQUEEN_OS_Health_Report");
 if (reportFiles.hasNext()) {
   let ss = SpreadsheetApp.openById(reportFiles.next().getId());
   let syncSheet = ss.getSheetByName("Weekly Sync Log");

   // Create tab if it doesn't exist
   if (!syncSheet) {
     syncSheet = ss.insertSheet("Weekly Sync Log");
     syncSheet.appendRow(["Module / Folder", "Updated Asset", "Timestamp", "Direct Link"]);
     syncSheet.getRange("A1:D1").setFontWeight("bold");
   } else {
     // Clear old records to keep the log fresh for the current week
     if (syncSheet.getLastRow() > 1) {
       syncSheet.deleteRows(2, syncSheet.getLastRow() - 1);
     }
   }

   if (updatedAssets.length > 0) {
     // Sort assets chronologically (newest first)
     updatedAssets.sort((a, b) => new Date(b[2]) - new Date(a[2]));
     syncSheet.getRange(2, 1, updatedAssets.length, 4).setValues(updatedAssets);
     Logger.log("Sync check complete. Activity logged to 'Weekly Sync Log' tab.");
   } else {
     syncSheet.appendRow(["No assets modified in the last 7 days.", "-", "-", "-"]);
     Logger.log("Sync check complete. No recent activity detected.");
   }
 } else {
   Logger.log("Warning: Health Report missing. Run Module 1 first.");
 }
}

2. The Final System Integration Matrix
Update your master orchestration function at the top of your Apps Script file to unite all five operational modules into a single automated pipeline:
function runMasterMVQUEENOSMaintenance() {
 // Module 1: Core Metrics & Separation Diagnostics
 runMVQUEENOSDiagnostics(); 
 
 // Module 2: Structural Void Blueprint Injection
 deployMVQUEENModuleStubs();
 
 // Module 3: Cross-Folder Redundancy Auditing
 detectMVQUEENDuplicates();
 
 // Module 4: Brand Voice Alignment Auditing
 runMVQUEENBrandVoiceLinter();
 
 // Module 5: Weekly Content Sync Tracking
 logMVQUEENContentSync();
}