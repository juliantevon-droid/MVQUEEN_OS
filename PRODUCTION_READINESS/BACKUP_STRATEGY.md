# MVQUEEN_OS Backup Strategy

## Source-of-truth boundaries

- GitHub: source of truth for application code and configuration templates.
- Shopify: source of truth for live store/catalog data.
- Catalog snapshots: read-only JSON/CSV exports for recovery and audit.
- Google Drive: human-readable archive, source-asset and controlled inbox layer.
- Colab/local runtime: recovery and transformation workspace; never the only copy.

## Safety rules

1. Never commit Shopify access tokens, API secrets, session tokens, or .env files.
2. Catalog backups are read-only operations.
3. Product handles, SKUs, variants, inventory, and media are not modified by snapshot workflows.
4. Keep production writes disabled until authentication, audit logging, permissions, dry-run validation and explicit approval are complete.
5. Use timestamped snapshots for recovery.
6. GitHub should not store large catalog snapshots or credentials.

## Recovery principle

A snapshot is an input to a controlled restore workflow, not an automatic live overwrite. Any restore must preserve identity fields and require explicit approval before Shopify writes are enabled.
