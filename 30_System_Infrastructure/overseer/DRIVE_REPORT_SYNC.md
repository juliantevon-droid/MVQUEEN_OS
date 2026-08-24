# Overseer Drive Report Sync

## Objective
Maintain one current MVQUEEN_OS Overseer audit report in Google Drive, replacing the previous copy so the Drive location always contains the latest verified report.

## Required GitHub configuration

The GitHub Actions workflow expects:

- Secret: `RCLONE_CONFIG_B64` — base64-encoded authenticated rclone configuration. Never commit this value.
- Repository variable: `MVQUEEN_DRIVE_AUDIT_PATH` — destination remote/path, for example `gdrive:MVQUEEN_OS/Overseer`.

The workflow uploads:

`30_System_Infrastructure/overseer/reports/MVQUEEN_OS_CURRENT_AUDIT.md`

as:

`MVQUEEN_OS_CURRENT_AUDIT.md`

## Retention rule

Keep **one current report** in the designated Drive folder. Do not delete historical Git commits or audit evidence from GitHub merely to reduce storage. GitHub remains the audit trail; Drive is the convenient current-report handoff.

## Failure behavior

If Drive authentication or upload fails:

1. The GitHub audit remains available as an artifact.
2. The workflow reports the Drive-sync failure.
3. The workflow does not silently claim a successful sync.
4. The next scheduled/event-driven run retries the sync.

If `RCLONE_CONFIG_B64` is not configured, the workflow explicitly reports that Drive sync is not configured and continues the audit so missing credentials do not hide the audit result.
