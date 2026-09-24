# MVQUEEN_OS Branch Consolidation — 2026-09-23

## Production rule

`main` is the canonical code and governance line. Branch logic is promoted only when it is additive, current, testable, and compatible with the canonical React Router Shopify app and guarded catalog publishing boundary.

## Logic preserved and promoted

- Shopify React Router runtime, authentication, compliance webhooks, product event runtime and Prisma state remain canonical on `main`.
- Catalog dry-run and explicit approval concepts from `build/mvqueen-os-html-foundation-v2` are consolidated into the canonical Python engine.
- App ecosystem governance from the foundation branch is retained.
- Backup/recovery policy from `feature/mvqueen-shopify-backend-v3` is retained.
- Production reconciliation policy from `production-reconciliation` is retained.
- Brand-bank, module-loader, catalog-control, storefront design, release-gate and publishing-boundary logic already represented by newer `main` implementations remains on the newer implementation rather than being duplicated.

## Alternate architectures intentionally not activated

The static HTML control tower branches and the separate Python Shopify backend contain useful ideas, but activating either beside the current React Router Shopify app would create competing application, authentication, webhook or write paths. Their useful governance concepts are consolidated; their duplicate runtimes remain historical Git references.

## CI repairs included

- fix product-form Liquid ID construction;
- shorten the Miss.Princess section schema name;
- add the locale key required by the 404 section;
- remove invalid pip-cache configuration from lint/index CI;
- extend ignore rules for caches, workspace state and generated archives.

## Safety

No live Shopify catalog write or theme publication is performed by this consolidation. Protected fields, approval gates and unpublished-theme deployment controls remain authoritative.
