# MVQUEEN_OS Backup Strategy

## Source-of-truth boundaries

- GitHub: source of truth for application code and configuration templates.
- Shopify: source of truth for live store/catalog data.
- Catalog snapshots: read-only JSON/CSV exports for recovery and audit.
- Google Drive: intended human-readable archive destination when a Drive connection is available; this repository does not assume that connection exists.
- Colab/local runtime: recovery and transformation workspace; never treat it as the only copy.

## Safety rules

1. Never commit Shopify access tokens, API secrets, session tokens, or .env files.
2. Catalog backups are read-only operations.
3. Product handles, SKUs, variants, inventory, and media are not modified by the snapshot workflow.
4. Keep production writes disabled until authentication, audit logging, permissions, and dry-run validation are complete.
5. Keep development/staging/production app configurations separate.
6. Use timestamped snapshots so a previous catalog state can be recovered.

## Catalog snapshot

Run from the backend directory after installing dependencies:

    python backup_catalog.py

The script writes timestamped files under:

    backups/shopify_catalog/

The JSON snapshot is the richer recovery/audit copy. The CSV is convenient for Sheets/Colab processing.

## Cloud archive direction

The intended backup chain is:

    Shopify
       ↓
    MVQUEEN_OS read-only snapshot
       ↓
    JSON + CSV
       ↓
    Google Drive / approved cloud archive
       ↓
    Colab / Sheets for controlled transformations

Until a Google Drive connector or user-run Drive sync is available, the cloud archive step remains separate. GitHub should not be used to store large catalog snapshots or credentials.

## Recovery principle

A snapshot is an input to a future controlled restore workflow, not an automatic live overwrite. Any restore must preserve identity fields and require explicit approval before Shopify writes are enabled.
