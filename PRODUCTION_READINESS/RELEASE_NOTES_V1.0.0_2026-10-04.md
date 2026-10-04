# MVQUEEN_OS v1.0.0 Production Release Evidence — 2026-10-04

## Release disposition

**Status: READY FOR OWNER SIGNED TAG / RELEASE**

The production architecture, live Shopify storefront, continuous product automation, security gates and release/staging topology have been verified. The connected tools cannot create a signed GitHub tag/release, so this document is the canonical evidence package for the final owner-side `v1.0.0` release action.

## Canonical topology

- Repository: `juliantevon-droid/MVQUEEN_OS`
- Canonical branch: `main`
- Branch protection: enabled
- Shopify store: `tsucu0-1i.myshopify.com`
- Shopify MAIN theme: **MVQueen — Release Candidate** (`154876772550`)
- Automated staging theme: **MVQueen — Staging Preview** (`155002798278`, UNPUBLISHED)
- Storefront password protection: OFF
- Runtime: Railway `mvqueen-web` + `mvqueen-product-worker` + managed PostgreSQL
- Production catalog authority: current Shopify catalog only

## Always-on product automation evidence

Railway production logs on 2026-10-04 repeatedly verified:

- `PRODUCTS_CREATE=true`
- `PRODUCTS_UPDATE=true`
- exactly 2 production product webhook subscriptions
- webhook self-repair health `true`
- continuous product-worker polling
- queue failed count: 0
- dead-letter count: 0

The live product path is:

`Shopify event → authenticated webhook → durable ProductJob → continuous Railway worker → authoritative Shopify re-read → classification / dual-brand routing → factual editorial / SEO / metafields / ALT / commercial processing → protected-field-safe write-back → fingerprinted loop suppression`

No app/worker runtime file has changed since the currently deployed Railway runtime commit `741159df283a24d0e5a1338056ec2c2a891cfa0c`; subsequent commits are theme, CI, documentation or tests only.

## Live product proof

Current active Shopify product audited during release closeout:

**Ruched Sports Bra and High-Waisted Shorts Active Set**

Verified automation outputs include:

- vendor normalized to MVQueen
- Miss.Princess routing
- factual short description
- factual product highlights
- focus keyword and long-tail SEO phrases
- SEO title/meta description
- complete ALT text across all current media
- governed pricing/commercial state
- protected SKU, variant and inventory relationships retained

## Checkout proof

Shopify test order `#1001`:

- `test=true`
- financial status: PAID
- fulfillment status: UNFULFILLED
- total: USD 62.99
- current product/SKU successfully traversed product → cart → checkout → payment/test order

The order is intentionally called out as cleanup evidence because the connected Shopify safety layer blocks automated `orderCancel`. Owner action: cancel #1001 with **Restock items** enabled after retaining this evidence.

## Storefront and theme QA

### Current passing gates

- Production Readiness: PASS
- Source Security Gate: PASS
- Lint / Index: PASS
- MVQUEEN_OS Overseer: PASS
- Recovery Readiness: PASS
- Theme CI/CD: PASS
- Staging deployment validation: PASS
- Shopify Theme Check: PASS
- Staging Preview Lighthouse release gate: PASS
- Live Storefront Performance median release gate: PASS

### Staging Lighthouse median

Three-run staging sample:

- Performance: 79 / 78 / 81 → median **79**
- Accessibility: 100 / 100 / 100 → median **100**
- Best Practices: 79 / 79 / 79 → median **79**
- SEO: 100 / 100 / 100 → median **100**
- Representative LCP: ~2.4s

Required audits pass in all three samples:

- console errors
- render-blocking resources
- responsive image sizing
- image resolution responsiveness
- LCP discovery

### Live Lighthouse median

Three-run live sample:

- Performance: 66 / 60 / 85 → median **66**
- Accessibility: 100 / 100 / 100 → median **100**
- Best Practices: 79 / 79 / 79 → median **79**
- SEO: 100 / 100 / 100 → median **100**

The live hard release floor passes. Enterprise targets remain 90 / 95 / 90 / 95 and were not lowered.

The remaining live score variance is predominantly third-party/platform execution:

- Google tag runtime
- Shopify Web Pixels / WPM
- Shop Pay browser-cookie behavior

Theme-owned responsive-image and LCP-discovery audits pass.

## Release/staging safety

- Shopify MAIN is never an automated theme deployment target.
- GitHub theme changes deploy only to the verified unpublished Staging Preview theme.
- Staging role is re-verified before and after deployment.
- Historical branches remain recovery/evidence references and are not wholesale production merge sources.
- Python catalog tooling is offline/governance-only and is not a second live Shopify writer.

## Deliberately deferred / non-blocking

- Branded custom domain: intentionally deferred by merchant.
- Large catalog expansion: future Shopify imports are handled automatically by the live product runtime; old historical CSV products are not production scope.
- Repository visibility: repository remains public. Source Security passes and `main` is protected, but changing visibility is an owner-level integration decision and is not performed silently.

## Final owner actions

1. Cancel Shopify test order `#1001` with **Restock items** enabled.
2. Create a signed GitHub tag `v1.0.0` on the final release commit and publish the GitHub release using `CHANGELOG.md` plus this evidence document.
3. After tagging, keep the existing production health monitor and staging/theme gates active for post-release regression monitoring.

No additional architecture rebuild is required for v1.0.
