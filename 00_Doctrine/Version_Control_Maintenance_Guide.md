# MVQUEEN_OS Version Control and Maintenance Guide

**Author:** Manus AI  
**Date:** June 25, 2026

## 1. Introduction

This guide outlines the best practices for maintaining the `MVQUEEN_OS` ecosystem, focusing on version control, automated synchronization, and regular audits. Adhering to these practices will ensure the system remains stable, synchronized, and free from discrepancies across Google Drive and GitHub.

## 2. Version Control Best Practices (GitHub as Source of Truth)

To maintain the integrity and consistency of the `MVQUEEN_OS`, the GitHub repository (`juliantevon-droid/MVQUEEN_OS`) must be treated as the **primary source of truth** for all operational assets, code, and critical documentation. 

### 2.1. Minimize Direct Modifications in Google Drive

*   **Avoid editing critical files directly in Google Drive** once they have been synchronized to GitHub. If a file exists in both locations, the GitHub version should be considered authoritative.
*   For documents that require collaborative editing, consider using GitHub's native editing features or a workflow that ensures changes are pushed to GitHub promptly after Drive-based collaboration.

### 2.2. Consistent Commit Practices

*   **Meaningful Commit Messages:** Every commit to the GitHub repository should have a clear, concise, and descriptive message. Use a consistent format (e.g., `Type: Subject [Scope]`) to indicate the purpose of the changes (e.g., `Feat: Add new feature`, `Fix: Resolve bug`, `Docs: Update documentation`, `Chore: Maintenance tasks`).
*   **Atomic Commits:** Group related changes into single commits. Avoid committing unrelated modifications together.

### 2.3. Branching Strategy

*   For significant changes or new feature development, utilize a branching strategy (e.g., Git Flow or GitHub Flow). Work on feature branches and merge them into `main` only after thorough review and testing.

## 3. Automated Synchronization Workflow

An automated synchronization script (`mvqueen_maintenance_hub.py`) has been deployed to periodically sync assets from Google Drive to the GitHub repository. This script runs hourly and performs the following:

*   **Identifies New Files:** Scans Google Drive for new or updated MvQueen-related files.
*   **Downloads and Integrates:** Downloads these files and places them into their appropriate directories within the GitHub repository.
*   **Commits Changes:** Automatically commits and pushes these changes to the `main` branch on GitHub with a descriptive commit message.

### 3.1. Script Location

The synchronization script is located at: `/home/ubuntu/MVQUEEN_OS/15_Scripts_And_Code/mvqueen_maintenance_hub.py`

### 3.2. Scheduled Execution

The script is scheduled to run **hourly** via the Manus platform. This ensures that any new or updated files in Google Drive are regularly pulled into the GitHub repository.

## 4. Scheduled Audit System

In addition to synchronization, the `mvqueen_maintenance_hub.py` script also incorporates an audit system to detect discrepancies and duplicates.

*   **Duplicate Detection:** Identifies files in Google Drive that have identical content (MD5 checksums).
*   **Automated Cleanup:** Automatically deletes duplicate files in Google Drive, retaining one version.
*   **Report Generation:** Generates an audit report (saved in `/home/ubuntu/MVQUEEN_OS/14_Data_And_Analytics/audit_reports/`) detailing any discrepancies or cleanup actions taken.

### 4.1. Audit Frequency

The audit process is integrated into the hourly execution of the `mvqueen_maintenance_hub.py` script, providing continuous monitoring of the ecosystem's health.

## 5. Manual Intervention and Troubleshooting

While automation minimizes manual effort, occasional intervention may be required:

*   **Review Audit Reports:** Regularly check the audit reports for any unexpected findings or persistent issues.
*   **Manual Merges:** In cases where the automated sync cannot resolve conflicts (e.g., due to significant content differences in files with the same name), manual review and merging may be necessary.
*   **GitHub as Fallback:** If any issues arise with the automated sync, always refer to the GitHub repository as the definitive source of truth.

By following this guide, the `MVQUEEN_OS` ecosystem will remain robust, consistent, and efficiently managed.
