# Overseer Drive Report Sync

## Objective
Maintain one current MVQUEEN_OS Overseer audit report in Google Drive, replacing the previous copy so the Drive location always contains the latest verified report.

## Required runner configuration

The GitHub Actions workflow must have access to an authenticated `rclone` configuration for the user's Google Drive. The authentication/configuration must be stored as a GitHub Actions secret or protected environment configuration; never commit credentials to the repository.

Recommended secret:

`RCLONE_CONFIG_B64`

The workflow should decode the protected configuration into the runner's temporary rclone config, upload:

`30_System_Infrastructure/overseer/reports/MVQUEEN_OS_CURRENT_AUDIT.md`

and replace the prior Drive copy with the same filename.

## Retention rule

Keep **one current report** in the designated Drive folder. Do not delete historical Git commits or audit evidence from GitHub merely to reduce storage. GitHub remains the audit trail; Drive is the convenient current-report handoff.

## Failure behavior

If Drive authentication or upload fails:

1. The GitHub audit must remain available.
2. The workflow must report the Drive-sync failure.
3. The failure must not silently appear as a successful Drive sync.
4. The next scheduled/event-driven run retries the sync.
