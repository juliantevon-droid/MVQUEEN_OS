# Changelog

All notable production changes to MVQUEEN_OS are documented here.

## [1.0.0] - 2026-10-04

### Production architecture
- Consolidated GitHub `main` as the protected source of truth for code, contracts, automation and theme source.
- Kept Shopify as the live commerce authority for products, variants, inventory, collections and deployed themes.
- Kept Google Drive as archive/assets/reference storage rather than an executable code source.
- Standardized the authenticated React Router Shopify app as the only live application mutation boundary.
- Standardized Railway managed PostgreSQL plus continuously running `mvqueen-web` and `mvqueen-product-worker` services.

### Always-on Shopify product automation
- Registered authenticated `products/create` and `products/update` webhook intake.
- Added durable idempotent `ProductJob` queueing.
- Added continuous Railway queue processing, stale-lease recovery, bounded retry/dead-letter handling and reconciliation.
- Added periodic webhook audit/self-repair.
- Added loop prevention through source fingerprints and automation-version state.
- Added fail-closed production gates for editorial, pricing, compare-at, cost and broader content surfaces.
- Preserved protected handles, SKUs, variants, inventory and source-media relationships.
- Added deterministic dual-brand routing between MVQueen and Miss.Princess.
- Added factual SEO, focus/secondary/long-tail keywords, product highlights, structured ALT publication and commercial health/ad-readiness state.

### Custom storefront
- Promoted **MVQueen — Release Candidate** to Shopify MAIN.
- Kept **MVQueen — Staging Preview** unpublished as the automated deployment/QA target.
- Removed storefront password protection.
- Delivered custom MVQueen/Miss.Princess brand gateway, navigation, content sections and product experience.
- Added short descriptions, factual bullet highlights and progressive-disclosure product accordions.
- Added responsive/mobile navigation, focus management, keyboard handling and mobile-first layouts.
- Added current policy/navigation links, Size Guide support and structured SEO metadata.

### Performance and quality
- Protected `main` with repository rules.
- Passed Production Readiness, Source Security, Lint/Index, Overseer, Recovery Readiness and Theme CI/CD.
- Added live and staging Lighthouse median gates using three samples to reduce Shopify/Google runtime variance without lowering enterprise targets.
- Current staging median: Performance 79, Accessibility 100, Best Practices 79, SEO 100.
- Current live median release gate: Performance 66, Accessibility 100, Best Practices 79, SEO 100; individual live sample reached Performance 85.
- Required audits pass: console errors, render-blocking resources, responsive images, image-size responsiveness and LCP discovery.
- Remaining performance variance is dominated by Shopify Web Pixels / WPM and Google tag execution rather than MVQueen theme asset budgets.

### Commerce verification
- Verified successful Shopify test checkout/order #1001 at USD 62.99.
- Verified current product automation on a real active Shopify product including Miss.Princess routing, SEO, highlights, ALT completion and governed commercial data.
- Verified runtime queue healthy with zero failed/dead-letter jobs during release audit.
- Verified production webhooks continuously healthy: PRODUCTS_CREATE and PRODUCTS_UPDATE both present.

### Release notes
- Branded custom domain remains intentionally deferred and is not a v1.0 blocker.
- Historical catalog recovery data is archive-only; Shopify current products are the production catalog source of truth.
- Test order #1001 should be cancelled with inventory restock after launch verification; the connected Shopify safety layer blocks automated order cancellation.
- The connected GitHub toolset does not expose signed-tag/release creation, so the signed `v1.0.0` GitHub release is the final owner action after this release evidence is committed.
