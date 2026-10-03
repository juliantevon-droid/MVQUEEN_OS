# MVQueen Release Readiness

## Current safety state — 2026-10-03

- Shopify store: `tsucu0-1i.myshopify.com`
- Live MAIN theme: **MVQueen — Release Candidate** (`154876772550`)
- Automated staging target: **MVQueen — Staging Preview** (`155002798278`)
- Automated target role must remain: **UNPUBLISHED**
- GitHub `main` is the theme source of truth.
- Repository automation may write only to the unpublished Staging Preview theme.
- Shopify MAIN is never an automated deployment target.
- Theme publication remains an explicit merchant/admin action.

## Required theme gates

1. MVQUEEN control registry validation passes.
2. Storefront release audit passes.
3. Shopify Theme Check passes with no errors.
4. Theme Access credential remains only in GitHub Actions secrets.
5. Automated deployment identity is exactly:
   - store: `tsucu0-1i.myshopify.com`
   - theme: `155002798278`
6. Pre-deploy verification proves the target is not MAIN.
7. Theme push uses the governed allowlist from `storefront/theme` with `--nodelete`.
8. Post-deploy verification proves Staging Preview remains unpublished.
9. Staging-preview Lighthouse/non-regression gate runs after deployment.
10. Deployment evidence is retained as workflow artifacts.
11. Product/catalog writes remain separate from theme deployment.
12. No review/rating schema is emitted without verified review data.
13. Supplier/legacy brand strings remain blocked from storefront output.

## Current catalog/runtime gate

Shopify is the sole live-product source of truth.

At the latest verified production check:
- 2 ACTIVE products are present.
- Both have public Online Store URLs.
- The always-on Shopify product runtime is live and healthy.
- Production `/healthz` reports database ready, continuous worker fresh, product webhooks healthy, and queue/dead-letter counts healthy.
- New/imported products are eligible for automatic governed enrichment through Shopify webhooks and the durable Railway worker.

Historical CSV recovery catalogs are archive/reference only and are not a release input.

## Operating rule

A push to `main` may validate and update **Staging Preview** automatically. It must never publish a theme and must never write to Shopify MAIN.

Live promotion is always a separate merchant release decision.
