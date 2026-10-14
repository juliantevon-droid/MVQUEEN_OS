# MVQUEEN_OS

MVQUEEN_OS is the canonical operating system for the MVQueen storefront and its Miss.Princess sister-brand experience.

For the current release state, use the [October 13 release closeout](PRODUCTION_READINESS/RELEASE_CLOSEOUT_2026-10-13.md). [PR #70](https://github.com/juliantevon-droid/MVQUEEN_OS/pull/70) is merged, and the merchant published **Copy of MVQueen — Working Preview** (`155532296390`) as Shopify MAIN. Public shopping and category-navigation checks pass. The original **Working Preview** (`155277918406`) remains unpublished and is still the automated deployment target. The earlier launch verification and v1.0 closeout below are historical snapshots; resolve roles from Shopify before each deployment or promotion.

**October 14 rollout remains incomplete:** the web app successfully deployed the merged fixes and its health checks pass. The merchant restored the web service's Wait for CI setting after the source-reconnect side effect; readback at 09:42 UTC confirmed it enabled for both web and product worker. The public performance gate still fails its required render-blocking audit for Shopify wallet CSS, despite passing all category release floors. The product worker still runs older code. Resolve the failed release gate and finish the worker rollout before closing the release.

Brand language is unified in [the brand guide](06_Tone_And_Voice/UNIFIED_BRAND_GUIDE.md) and [active content policy](06_Tone_And_Voice/Brand_Content_Policy.json). The [complete Drive source catalog](31_AI_Knowledge_Base/brand_sources/README.md) preserves substantive versions with provenance; the product writer consumes the reconciled policy.

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

- Railway `mvqueen-web` and `mvqueen-product-worker` follow GitHub `main`, with Wait for CI verified enabled for both at 09:42 UTC on October 14. Web runs merged commit `089df163`; the product worker remains on `c7b7c68`. See the current release closeout for deployment evidence and recovery steps.
- Google Drive remains assets/knowledge/archive storage. Its GitHub intake workflow is manual and fail-closed; it never commits or overwrites canonical source automatically.
- Theme changes deploy to the verified unpublished `MVQueen — Working Preview` theme (`155277918406`). The current Shopify MAIN theme is never an automated deployment target.

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

