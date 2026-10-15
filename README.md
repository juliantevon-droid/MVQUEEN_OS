# MVQUEEN_OS

MVQUEEN_OS is the canonical operating system for the MVQueen storefront and its Miss.Princess sister-brand experience.

For the current release state, use the [October 13 release closeout](PRODUCTION_READINESS/RELEASE_CLOSEOUT_2026-10-13.md). [PR #70](https://github.com/juliantevon-droid/MVQUEEN_OS/pull/70) is merged, and the merchant published **Copy of MVQueen — Working Preview** (`155532296390`) as Shopify MAIN. Public shopping and category-navigation checks pass. The original **Working Preview** (`155277918406`) remains unpublished and is still the automated deployment target. The earlier launch verification and v1.0 closeout below are historical snapshots; resolve roles from Shopify before each deployment or promotion.

**Backend rollout verified October 14:** the web app and product worker run the merged fixes, with healthy database, worker, webhooks, and empty job queues at the documented checks. Wait for CI was verified enabled for both services after deployment. **Latest public performance check, October 15:** category release floors passed, but the required console-error audit failed on a Shop Pay iframe security-policy error. The render-blocking audit passed in this latest sample set; earlier wallet-CSS failures remain in the evidence. The full release is not yet certified.

Brand language is unified in [the brand guide](06_Tone_And_Voice/UNIFIED_BRAND_GUIDE.md) and [active content policy](06_Tone_And_Voice/Brand_Content_Policy.json). The [complete Drive source catalog](31_AI_Knowledge_Base/brand_sources/README.md) preserves substantive versions with provenance; the product writer consumes the reconciled policy.

For the next launch steps, use the [October 14 completion plan](PRODUCTION_READINESS/LAUNCH_COMPLETION_PLAN_2026-10-14.md) and [organic social launch kit](08_Social_Media/launch_2026_10/README.md). The kit contains profile copy, first-week drafts and a 30-day calendar. Three existing MVQUEEN profiles are identified. Metricool connections are verified for Facebook Mvqueen, Instagram @miss.mvqueen and TikTok @mvqueen_official. No campaign is claimed scheduled or published.

[PR #74](https://github.com/juliantevon-droid/MVQUEEN_OS/pull/74) merged after passing its applicable checks. Its optional Pinterest link support deployed successfully to the unpublished Working Preview on October 15. Metricool confirms Instagram **@miss.mvqueen** and TikTok **@mvqueen_official**, with the TikTok spelling confirmed by the owner. The owner's Facebook share link resolves to [Mvqueen](https://www.facebook.com/people/Mvqueen/61585903680200/), and Metricool now returns the matching Page name. The homepage, MVQueen and About templates contain these three links for the unpublished preview, with TikTok corrected to the underscore spelling. Public-theme publication remains separate.

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

- Railway `mvqueen-web` and `mvqueen-product-worker` follow GitHub `main`, with Wait for CI verified enabled for both after rollout at 09:51 UTC on October 14. Web runs merged commit `089df163`; the product worker runs `6bccab34`, which changes only documentation from that application version. Both contain the verified runtime fixes. See the current release closeout for deployment evidence and the remaining storefront performance blocker.
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

That historical snapshot listed test-order cleanup and the signed GitHub `v1.0.0` tag/release as owner-side follow-ups. **October 15 readback:** test order `#1001` was already cancelled on October 4 and is refunded and closed. Inventory restocking, notification delivery and the tag/release were not re-verified in that read. See the [current launch completion plan](PRODUCTION_READINESS/LAUNCH_COMPLETION_PLAN_2026-10-14.md) for the remaining current-release order test.

