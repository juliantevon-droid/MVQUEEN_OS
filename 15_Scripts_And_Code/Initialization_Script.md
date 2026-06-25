MVQUEEN_OS Project Setup Script
 framework. This script creates the required folder structure, modules, and boilerplate files.
MVQUEEN_OS
This document contains a comprehensive Google Apps Script intended to automate the initialization of the 
Prerequisites
1. Ensure you have the Google Drive API enabled under “Services” if needed, though this script uses the standard DriveApp service.
2. Paste the code below into the editor.
3. Create a new Apps Script project.
4. Open Google Apps Script.
The Script
/**
* MVQUEEN_OS Initialization Script
* 
* This script automates the creation of the MVQUEEN_OS workspace.
* It creates 42 modules (00-39 and 98-99), boilerplate README.md files,
* and a primary health tracking sheet.
*/

// CONFIGURATION
const ROOT_FOLDER_NAME = "MVQUEEN_OS_WORKSPACE";
const MODULE_PREFIX = "MOD_";

/**
* Main execution function.
*/
function initializeMVQUEEN() {
 const root = DriveApp.createFolder(ROOT_FOLDER_NAME);
 
 // Create Modules 00-39 and 98-99
 const modules = [];
 for (let i = 0; i < 40; i++) modules.push(i.toString().padStart(2, '0'));
 modules.push("98", "99");
 
 modules.forEach(id => {
   const folder = root.createFolder(`${MODULE_PREFIX}${id}`);
   
   // Create boilerplate README.md
   createFile(folder, "README.md", `# Module ${id}\n\nDescription for module ${id}.\n\n## Status\n- [ ] Active`);
 });
 
 // Create Health Tracking Sheet
 const sheet = SpreadsheetApp.create("MVQUEEN_OS_Health_Tracking");
 const file = DriveApp.getFileById(sheet.getId());
 file.moveTo(root);
 
 const sheetObj = sheet.getActiveSheet();
 sheetObj.appendRow(["Module ID", "Status", "Last Checked", "Notes"]);
 sheetObj.getRange("A1:D1").setFontWeight("bold");
 
 Logger.log(`MVQUEEN_OS initialized at: ${root.getUrl()}`);
}

/**
* Helper to create text files in Drive
*/
function createFile(folder, name, content) {
 folder.createFile(name, content, MimeType.PLAIN_TEXT);
}

/**
* Function (optional) to move existing files from Root to a Module if needed.
* Modify 'TARGET_FOLDER_ID' and 'SOURCE_FILE_ID' as necessary.
*/
function migrateFile(sourceFileId, targetFolderId) {
 const file = DriveApp.getFileById(sourceFileId);
 const folder = DriveApp.getFolderById(targetFolderId);
 file.moveTo(folder);
}
Setup Instructions
   1. Verify: Check your Google Drive. You will see a new folder named MVQUEEN_OS_WORKSPACE containing your modules and the health tracking sheet.
   2. Click “Allow”.
   3. Click “Go to [Project Name] (unsafe)”.
   4. Click “Advanced” (it may show a warning because this is a custom script).
   5. Select your Google account.
1. Authorize Permissions:
2. Run the Function: Click the “Run” button in the toolbar.
3. Paste into Script Editor: In your Apps Script project, delete any existing default code inside Code.gs and paste the code.
4. Copy the Code: Copy the entire block above.
Customization
5. README Templates: You can modify the string passed to the createFile function to include more detailed YAML front-matter or corporate documentation standards.
6. Migration: If you have existing files to move, use the migrateFile function provided in the script. You will need to retrieve the File IDs and Folder IDs from the browser URL bars when viewing them in Drive.
7. Click “Review Permissions”.