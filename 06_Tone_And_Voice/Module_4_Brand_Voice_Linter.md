MVQUEEN OS - Module 4: Brand Voice Linter Script
This document contains the complete Google Apps Script code for the MVQUEEN OS Brand Voice Linter. It scans your markdown files for non-luxury vocabulary and aggressive punctuation, outputting the results to a new "Brand Voice Log" tab in your master report.
1. The Apps Script Code
/**
* MVQUEEN OS - Brand Voice Linter
* Scans .md assets for non-luxury vocabulary and stylistic errors.
*/
function runMVQUEENBrandVoiceLinter() {
 const ROOT_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE';
 const rootFolder = DriveApp.getFolderById(ROOT_FOLDER_ID);
 const subFolders = rootFolder.getFolders();

 let infractions = [];
 
 // Define non-luxury or forbidden brand terms and patterns
 const forbiddenPatterns = [
   { regex: /girlboss/gi, issue: "Non-luxury terminology (girlboss)" },
   { regex: /!!!+/g, issue: "Aggressive punctuation (multiple exclamation points)" },
   { regex: /\bcheap\b/gi, issue: "Off-brand pricing terminology (cheap)" },
   { regex: /\bhustle\b/gi, issue: "Non-luxury terminology (hustle)" }
 ];

 Logger.log("Initiating MVQUEEN OS Brand Voice Linter...");

 while (subFolders.hasNext()) {
   let folder = subFolders.next();
   let folderName = folder.getName();
   let files = folder.getFiles();

   while (files.hasNext()) {
     let file = files.next();
     let fileName = file.getName();
     let mime = file.getMimeType();

     if (mime === MimeType.PLAIN_TEXT || fileName.endsWith('.md')) {
       let content = file.getAs('text/plain').getDataAsString();
       let fileInfractions = [];

       forbiddenPatterns.forEach(pattern => {
         if (pattern.regex.test(content)) {
           fileInfractions.push(pattern.issue);
         }
       });

       if (fileInfractions.length > 0) {
         infractions.push([
           fileName,
           folderName,
           fileInfractions.join(' | '),
           new Date().toLocaleDateString()
         ]);
       }
     }
   }
 }

 // Output findings to a dedicated tab inside the Health Report Spreadsheet
 let reportFiles = rootFolder.getFilesByName("MVQUEEN_OS_Health_Report");
 if (reportFiles.hasNext()) {
   let ss = SpreadsheetApp.openById(reportFiles.next().getId());
   let voiceSheet = ss.getSheetByName("Brand Voice Log");

   // Create tab if it doesn't exist
   if (!voiceSheet) {
     voiceSheet = ss.insertSheet("Brand Voice Log");
     voiceSheet.appendRow(["Asset Name", "Module / Folder", "Detected Infractions", "Last Scanned"]);
     voiceSheet.getRange("A1:D1").setFontWeight("bold");
   } else {
     // Clear old records
     if (voiceSheet.getLastRow() > 1) {
       voiceSheet.deleteRows(2, voiceSheet.getLastRow() - 1);
     }
   }

   if (infractions.length > 0) {
     voiceSheet.getRange(2, 1, infractions.length, 4).setValues(infractions);
     Logger.log("Linter complete. Infractions logged to 'Brand Voice Log' tab.");
   } else {
     voiceSheet.appendRow(["System fully aligned. No infractions.", "All Modules", "None", new Date().toLocaleDateString()]);
     Logger.log("Linter complete. Brand voice is 100% compliant.");
   }
 } else {
   Logger.log("Warning: Health Report missing. Run Module 1 first.");
 }
}

2. Complete System Integration Matrix
Update your master orchestration function at the top of your Apps Script file to combine all four active engines seamlessly:
function runMasterMVQUEENOSMaintenance() {
 // Module 1: Core Metrics & Separation Diagnostics
 runMVQUEENOSDiagnostics(); 
 
 // Module 2: Structural Void Blueprint Injection
 deployMVQUEENModuleStubs();
 
 // Module 3: Cross-Folder Redundancy Auditing
 detectMVQUEENDuplicates();
 
 // Module 4: Brand Voice Alignment Auditing
 runMVQUEENBrandVoiceLinter();
}