MVQUEEN OS - Module 3: Duplicate Detector Script
This document contains the complete Google Apps Script code for the MVQUEEN OS Duplicate Detector. It automatically updates the existing MVQUEEN_OS_Health_Report spreadsheet with a dedicated "Duplicate Log" tab.
1. The Apps Script Code
/**
* MVQUEEN OS - Duplicate Detector
* Scans all subfolders to find files with identical names across different locations.
*/
function detectMVQUEENDuplicates() {
 // Centralized root identity connection
 const ROOT_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE'; 
 const rootFolder = DriveApp.getFolderById(ROOT_FOLDER_ID);
 const subFolders = rootFolder.getFolders();
 
 let fileMap = {}; 
 let duplicates = [];
 
 Logger.log("Starting MVQUEEN OS cross-folder duplicate scan...");
 
 while (subFolders.hasNext()) {
   let folder = subFolders.next();
   let folderName = folder.getName();
   let files = folder.getFiles();
   
   while (files.hasNext()) {
     let file = files.next();
     let fileName = file.getName();
     let fileId = file.getId();
     
     if (!fileMap[fileName]) {
       fileMap[fileName] = [];
     }
     fileMap[fileName].push({folder: folderName, id: fileId});
   }
 }
 
 // Isolate file names that appear more than once
 for (let fileName in fileMap) {
   if (fileMap[fileName].length > 1) {
     let locations = fileMap[fileName].map(item => item.folder).join(' | ');
     duplicates.push([
       fileName, 
       fileMap[fileName].length, 
       locations, 
       new Date().toLocaleDateString()
     ]);
   }
 }
 
 // Output findings to a dedicated tab inside the Health Report Spreadsheet
 let reportFiles = rootFolder.getFilesByName("MVQUEEN_OS_Health_Report");
 if (reportFiles.hasNext()) {
   let ss = SpreadsheetApp.openById(reportFiles.next().getId());
   let dupSheet = ss.getSheetByName("Duplicate Log");
   
   // Create tab if it doesn't exist yet
   if (!dupSheet) {
     dupSheet = ss.insertSheet("Duplicate Log");
     dupSheet.appendRow(["Duplicate Filename", "Occurrences", "Folder Locations", "Last Detected"]);
     dupSheet.getRange("A1:D1").setFontWeight("bold");
   } else {
     // Clear old records
     if (dupSheet.getLastRow() > 1) {
       dupSheet.deleteRows(2, dupSheet.getLastRow() - 1);
     }
   }
   
   if (duplicates.length > 0) {
     dupSheet.getRange(2, 1, duplicates.length, 4).setValues(duplicates);
     Logger.log("Scan complete. Duplicates logged to 'Duplicate Log' tab.");
   } else {
     dupSheet.appendRow(["No duplicates detected. Workspace clean.", 0, "All clear", new Date().toLocaleDateString()]);
     Logger.log("Scan complete. Zero duplicates found.");
   }
 } else {
   Logger.log("Warning: Run Module 1 first to initialize the core health report spreadsheet.");
 }
}

2. Complete System Integration Matrix
Update your master orchestration function at the top of your Apps Script file to combine all active engines seamlessly:
function runMasterMVQUEENOSMaintenance() {
 // Module 1: Core Metrics & Separation Diagnostics
 runMVQUEENOSDiagnostics(); 
 
 // Module 2: Structural Void Blueprint Injection
 deployMVQUEENModuleStubs();
 
 // Module 3: Cross-Folder Redundancy Auditing
 detectMVQUEENDuplicates();
}