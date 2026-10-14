# MVQueen Release Readiness

## Current safety state — 2026-10-13

- Shopify store: `tsucu0-1i.myshopify.com`
- Live MAIN theme: **Copy of MVQueen — Working Preview** (`155532296390`)
- Automated staging target: **MVQueen — Working Preview** (`155277918406`)
- Automated target role must remain: **UNPUBLISHED**
- Previous MAIN: **MVQueen — Staging Preview** (`155002798278`), now **UNPUBLISHED**
- GitHub `main` is the theme source of truth.
- Repository automation may write only to the unpublished Working Preview theme.
- Shopify MAIN is never an automated deployment target.
- Theme publication remains an explicit merchant/admin action.

Theme names are not role guarantees. Resolve roles from Shopify before each
deployment or promotion. The merchant published a duplicate at 19:44 UTC on
October 13, preserving the original unpublished automation target. See the
[October 13 release closeout](../../PRODUCTION_READINESS/RELEASE_CLOSEOUT_2026-10-13.md)
for merged code, public storefront verification, and production rollout evidence.

## Required theme gates

1. MVQUEEN control registry validation passes.
2. Storefront release audit passes.
3. Shopify Theme Check passes with no errors.
4. Theme Access credential remains only in GitHub Actions secrets.
5. Automated deployment identity is exactly:
   - store: `tsucu0-1i.myshopify.com`
   - theme: `155277918406`
6. Pre-deploy verification proves the target is not MAIN.
7. Theme push uses the governed allowlist from `storefront/theme` with `--nodelete`.
8. Post-deploy verification proves Working Preview remains unpublished.
9. Working Preview Lighthouse/non-regression gate passes after deployment.
   Automatic deployment alone does not establish this: dispatch the workflow
   with the canonical Working Preview URL or a fresh store-scoped visitor link.
   Each Lighthouse sample must verify the actual audited page's theme ID and
   unpublished role, including after cookie-based redirects.
10. Deployment evidence is retained as workflow artifacts.
11. Product/catalog writes remain separate from theme deployment.
12. No review/rating schema is emitted without verified review data.
13. Supplier/legacy brand strings remain blocked from storefront output.

## Current catalog/runtime gate

Shopify is the sole live-product source of truth.

At the earlier October 13, 13:37 UTC public health check:
- The always-on Shopify product runtime is live and healthy.
- Production `/healthz` reports database ready, continuous worker fresh, product webhooks healthy, and zero received, processing, failed, and dead-letter jobs.
- New/imported products are eligible for automatic governed enrichment through Shopify webhooks and the durable Railway worker.

This earlier health snapshot predates the merged worker fixes. The
[release closeout](../../PRODUCTION_READINESS/RELEASE_CLOSEOUT_2026-10-13.md)
records the subsequent deployment state and final runtime verification.

The earlier two-product snapshot is historical. Catalog contents and availability
must be checked against Shopify at release time; runtime health does not establish
that every product is purchasable or that payment capture has been tested.

Historical CSV recovery catalogs are archive/reference only and are not a release input.

## Operating rule

A push to `main` may validate and update **Working Preview** automatically. It must never publish a theme and must never write to Shopify MAIN.

Live promotion is always a separate merchant release decision.
