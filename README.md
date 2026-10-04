# MVQUEEN_OS

MVQUEEN_OS is the canonical operating system for the MVQueen storefront and its Miss.Princess sister-brand experience.

## One-system architecture

- GitHub main — canonical code, contracts, tests, theme source and automation logic.
- Shopify — canonical live commerce state: products, variants, inventory, IDs, collections and deployed themes.
- Google Drive — archive, source assets, references, imports/exports and backups. Drive is not an executable code source.
- app/ — the only live Shopify application runtime. It is React Router + Shopify Admin GraphQL.
- storefront/theme/ — the only canonical Shopify theme source.
- 15_Scripts_And_Code/mvqueen_engine/ — deterministic intelligence, catalog proposal, QA and dry-run tooling.
- PRODUCTION_READINESS/ — release, approval, preview, audit and production contracts.

## Shopify write boundary

The authenticated React app is the only repository component permitted to make live Shopify mutations.

Production has two authorization modes:

1. **Automatic catalog mode** — `MVQ_WRITE_ENABLED=true` and `MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED=true`. Every authenticated Shopify `products/create` or `products/update` event is eligible for the safe catalog writer.
2. **Manual product mode** — automatic enrollment is off and the exact product GID must appear in `MVQ_APPROVED_PRODUCT_GIDS`.

`MVQ_EDITORIAL_PUBLISH_ENABLED=true` separately controls automatic customer-facing editorial/SEO enrichment. `MVQ_AUTO_CONTENT_SURFACES_ENABLED=true` extends the same product event into product FAQ, qualifying blog content, and matched collection content. Protected handles, SKUs, prices, inventory, variants, fulfillment and source-media relationships remain outside the automatic writer.

### Always-on recovery

- `products/create` and `products/update` webhooks are the immediate trigger.
- `ProductJob` is the durable idempotent queue record.
- `/internal/product-worker` retries failed jobs with exponential backoff, recovers stale leases, and dead-letters exhausted jobs.
- Reconciliation queries recently updated Shopify products and enqueues anything missed by webhook delivery.
- The Railway `mvqueen-product-worker` service is the continuously running queue/reconciliation owner.
- `.github/workflows/product-worker.yml` is a five-minute production health monitor that checks the public `/healthz` endpoint; it does not duplicate queue ownership.
- `/healthz` reports database readiness plus received, processing, failed, and dead-letter queue counts.

Python tooling produces validated artifacts and release evidence but has no default live Shopify transport.

## Safety

Never commit credentials. Protected product identity, SKU, inventory, variant, pricing and image-relationship fields are outside editorial automation.

## Current cross-system boundary

- Railway `mvqueen-web` and `mvqueen-product-worker` are verified sourced from GitHub `main`; Railway reports the GitHub source integration active. The latest app-code deployment matched the verified app-code commit; documentation/theme-only commits do not require those runtime services to rebuild.
- Google Drive remains assets/knowledge/archive storage. Its GitHub intake workflow is manual and fail-closed; it never commits or overwrites canonical source automatically.
- Theme changes deploy to the verified unpublished `MVQueen — Staging Preview` theme. The current Shopify MAIN theme is never an automated deployment target.

## v1.0 release closeout

As of 2026-10-04:

- Shopify MAIN is **MVQueen — Release Candidate**.
- Storefront password protection is off.
- GitHub `main` is protected.
- Production web/product-worker/PostgreSQL are healthy on Railway.
- Shopify `products/create` and `products/update` automation is live 24/7 through the continuous Railway product worker.
- Production Readiness, Source Security, Lint/Index, Overseer, Recovery Readiness and Theme CI/CD are passing.
- Live and staging Lighthouse release gates use three-run median sampling while retaining the MVQUEEN enterprise targets.
- Current Shopify products are the only production catalog source of truth; historical recovery products remain archive-only.
- `CHANGELOG.md` and `PRODUCTION_READINESS/RELEASE_NOTES_V1.0.0_2026-10-04.md` contain the v1.0 evidence package.

Final owner-side closeout is limited to cancelling test order `#1001` with inventory restock and publishing the signed GitHub `v1.0.0` tag/release. The connected safety/tooling boundaries intentionally do not perform those two operations.

