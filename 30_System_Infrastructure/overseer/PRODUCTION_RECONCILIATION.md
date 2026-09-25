# MVQUEEN_OS Production Reconciliation

## Purpose

Controlled consolidation of historical branch logic into the current canonical `main` line.

## Classification

### KEEP
- canonical MVQueen brand doctrine and identity;
- persona and brand banks;
- Shopify-safe engine architecture;
- SEO/content architecture;
- agent/system architecture;
- Overseer and audit controls;
- runtime/module-loader controls;
- production documentation and recovery controls.

### EXCLUDE / CLEAN
- Python cache directories/files;
- temporary audit output;
- generated build artifacts;
- duplicate archives;
- obsolete scripts where a canonical replacement exists.

### MERGE CAREFULLY
- renamed engine/module paths;
- overlapping configuration;
- duplicate brand/content sources;
- product/catalog assets;
- deployment configuration;
- alternate application runtimes.

## Gate

No reconciled implementation is production-ready until the resulting `main` tree passes current CI, release, security, theme and catalog governance checks.

Evidence → Analysis → Approval → Change → Verify → Log.
