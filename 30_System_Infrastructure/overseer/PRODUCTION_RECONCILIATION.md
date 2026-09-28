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

## Unified main disposition — 2026-09-28

### Canonical production line

- `main` is the single canonical implementation line.
- Historical branches are evidence/archive inputs only unless a specific capability is proven missing from `main` and passes current production gates.
- Stale branches are never merged wholesale merely to remove branch divergence.

### Consolidated into main

- GitHub Actions checkout runtime upgraded to v7.
- GitHub Actions setup-node runtime upgraded to v7.
- GitHub Actions setup-python runtime upgraded to v7.
- GitHub Actions upload-artifact runtime upgraded to v7.
- The consolidated line passed current Production Readiness, Overseer, Source Security, Shopify App CI, Theme CI/CD, Storefront Performance, Recovery Readiness, Dependency Audit, Deep Repository Audit, and Lint/Index validation where triggered.

### Dependency disposition

The Prisma 7, React Router 8, Shopify runtime group, and tooling group updates were not promoted because their pull-request heads failed MVQUEEN Shopify App CI. Production remains on the last known-green compatible dependency line until those upgrades are coordinated and fully validated.

### Historical branch disposition

Branches that are fully behind `main` are considered incorporated/superseded. Diverged historical branches that are hundreds or thousands of commits behind remain historical evidence only; useful capabilities must be harvested individually instead of merging their full trees.

The historical file `15_Scripts_And_Code/python_calls.py` is explicitly excluded from production. It is a shell/manual runbook stored with a `.py` extension, contains retired direct-Shopify-write examples, and includes obsolete shipping copy that conflicts with the governed current shipping contract. It must not be restored to `main`.

### Release rule

A green `main` establishes engineering readiness, not storefront/commercial launch completion. Catalog depth, inventory availability, production domain, checkout/order verification, and final mobile storefront QA remain independent launch gates.

