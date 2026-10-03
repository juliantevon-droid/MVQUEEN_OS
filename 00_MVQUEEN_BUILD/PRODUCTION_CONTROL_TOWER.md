# MVQueen — Production Control Tower

**Status:** ACTIVE BUILD  
**Target:** Production-ready, enterprise-strength Shopify storefront + MVQUEEN_OS commerce engine  
**Storefront rule:** Build and test on the unpublished Shopify theme only until final launch approval.  
**Brand rule:** Customer-facing product content uses MVQueen only.  

## Operating Doctrine

MVQueen is not being rebuilt from scratch. Existing brand, content, automation, theme, and engineering assets are treated as the source material and upgraded into one production system.

The standard for completion is not "looks good." The system must be coherent, maintainable, measurable, safe to deploy, mobile-first, accessible, SEO-ready, conversion-ready, and capable of scaling beyond the initial catalog.

## Build Stack

1. **Brand system** — doctrine, colors, typography, voice, positioning.
2. **Storefront system** — Liquid, CSS, JavaScript, Shopify native sections/templates.
3. **Commerce UX** — navigation, collection discovery, product page, cart, search, recommendations, trust signals.
4. **Catalog engine** — product normalization, naming, descriptions, SEO, alt text, tags, metafields, collection assignment.
5. **Shopify API layer** — GraphQL-first production automation, environment-only credentials, dry-run and rollback protections.
6. **Growth layer** — SEO, analytics readiness, merchandising, content and lifecycle systems.
7. **Quality layer** — mobile, accessibility, performance, structured data, purchase-path and catalog integrity testing.
8. **Launch layer** — policies, payments, shipping, domain, monitoring, backup, final acceptance.

## Source-of-Truth Hierarchy

When systems overlap, use this order:

1. MVQueen doctrine / brand identity
2. Approved product and voice standards
3. Existing MVQUEEN_OS production systems
4. Shopify theme architecture
5. New implementation code
6. Temporary experiments / legacy code

Legacy systems are preserved until their replacement is verified. Do not delete working assets merely because a newer layer exists.

## Current Architecture Decisions

- Shopify native-first.
- No unnecessary apps.
- GraphQL-first for new production automation.
- Existing REST client remains available for maintenance and rollback paths.
- Live Shopify theme is protected from development writes.
- Theme development happens on `MVQueen — Release Candidate` (`154876772550`), which remains unpublished. The live `MVQueen — Custom Production Build` (`154869825734`) is not a development-write target.
- Product handles, SKUs, inventory, variants, and existing images are protected unless an explicit migration requires a change.
- Product copy follows `06_Tone_And_Voice/Product_Description_Voice.md`.
- Collection architecture follows `04_Products/Collection_Structure.md`.

## Production Gates

### Gate 01 — Foundation
- [x] MVQUEEN_OS master repository established
- [x] Production execution doctrine established
- [x] Shopify engine map established
- [x] GraphQL client foundation established
- [x] Brand color and typography systems documented
- [ ] Whole-repository source audit complete

### Gate 02 — Storefront
- [x] Unpublished `MVQueen — Release Candidate` selected
- [x] Enterprise visual layer added
- [x] Product template upgraded
- [ ] Header/navigation final integration
- [ ] Homepage conversion architecture final
- [ ] Collection template final
- [ ] Search/filter UX final
- [ ] Cart/drawer final
- [ ] Footer and policy architecture final

### Gate 03 — Catalog
- [ ] Catalog integrity scan
- [ ] Vendor/brand contamination scan
- [ ] Product naming normalization
- [ ] Product description generation/validation
- [ ] SEO title/meta generation
- [ ] Alt-text generation
- [ ] Tag/metafield normalization
- [ ] Collection assignment engine
- [ ] Duplicate/near-duplicate detection
- [ ] Protected-field enforcement

### Gate 04 — Technical SEO
- [ ] Canonical validation
- [ ] Product/collection structured data
- [ ] Breadcrumb structured data
- [ ] Indexability controls
- [ ] Metadata completeness
- [ ] Image alt coverage
- [ ] Internal-link architecture
- [ ] Sitemap/search-engine readiness

### Gate 05 — Conversion
- [ ] Above-fold product clarity
- [ ] Variant UX
- [ ] Add-to-cart reliability
- [ ] Sticky mobile purchase action
- [ ] Trust/payment messaging
- [ ] Shipping/returns visibility
- [ ] Cross-sell/recommendations
- [ ] Cart upsell logic
- [ ] Empty/search/no-result states

### Gate 06 — Quality
- [ ] Mobile QA
- [ ] Desktop QA
- [ ] Accessibility QA
- [ ] Performance QA
- [ ] JavaScript error scan
- [ ] Liquid/rendering error scan
- [ ] Broken-link scan
- [ ] Image/loading audit
- [ ] Checkout-path test

### Gate 07 — Launch
- [ ] Payments verified
- [ ] Shipping verified
- [ ] Taxes verified
- [ ] Policies verified
- [ ] Domain verified
- [ ] Analytics/conversion tracking verified
- [ ] Catalog publication decision completed
- [ ] Final backup recorded
- [ ] Final unpublished-theme acceptance completed
- [ ] Explicit owner approval to publish

## Definition of Done

MVQueen is not considered production-ready until all launch gates pass and the final purchase path works from landing page → discovery → product → cart → checkout without known blocking defects.

**No production publish is implied by completing development work. Publishing remains a separate final action requiring explicit approval.**

## Continuous Upgrade Rule

At every implementation step, ask:

- Can this be made safer?
- Can this be made faster?
- Can this be made easier to maintain?
- Can this be made more accessible?
- Can this be made clearer for the customer?
- Can this reduce manual catalog work?
- Can this produce better measurement?
- Can this scale from hundreds to thousands of products?

If the answer is yes, upgrade the architecture before calling the step complete.


## Verified staging synchronization — 2026-09-26

- GitHub `main` remains the source of truth for controlled theme code.
- The full controlled theme deployment set was synchronized from `storefront/theme` to Shopify theme `MVQueen — Release Candidate` (`154876772550`).
- Shopify accepted all synchronized batches with zero theme-file user errors.
- Staging remains `UNPUBLISHED`, is not processing, and reports no processing failure.
- The live theme remains `MVQueen — Custom Production Build` (`154869825734`) with role `MAIN`; it was not modified by this synchronization.
- The approved MVQueen editorial homepage direction remains on staging until explicit launch approval.
## Release candidate verification — 2026-09-27

- Shopify theme `154876772550` is now named `MVQueen — Release Candidate` and remains `UNPUBLISHED`.
- The MVQueen landing page at `/pages/mvqueen` is published and uses the `page.mvqueen` template.
- Miss.Princess remains published at `/pages/miss-princess`.
- All three active products carry `shipping.delivery_estimate = 7–15 business days` and have active United States delivery methods.
- Footer legal/customer-care destinations are published; Privacy Policy uses Shopify's native policy route.
- Payment-provider activation and a real/test checkout remain the final manual commerce-certification gate.
- Theme publishing remains an explicit merchant action; connected automation must not publish MAIN.

## Current control-tower state — 2026-10-03

This section supersedes the older point-in-time theme/catalog checklist above.

### Runtime

- GitHub `main` is protected and is the canonical code source.
- Railway `mvqueen-web`, `mvqueen-product-worker`, `mvqueen-agent-worker` and PostgreSQL are online.
- Web and product worker are sourced from `juliantevon-droid/MVQUEEN_OS` branch `main`.
- Production health reports `production-automation-ready`.
- Continuous product-worker heartbeat is fresh.
- Product webhook heartbeat is healthy.
- Queue received / processing / failed / dead-letter counts are all healthy.
- Reconciliation, retry/backoff and stale-lease recovery are active.

### Always-on product automation

Authenticated Shopify `products/create` and `products/update` events automatically enter the durable queue. Eligible products can receive governed:

- MVQueen vs Miss.Princess routing
- Shopify category / department / family / subcollection classification
- vendor normalization with source-vendor provenance
- short description and governed long description
- product highlights/bullets
- focus, secondary and long-tail SEO phrases
- Shopify SEO title and meta description
- FAQ/content metafields
- image ALT repair
- Google Shopping / catalog attributes
- shipping metadata
- commercial cost/pricing/health analysis
- collection/system routing tags
- marketing/lifecycle planning state
- analytics measurement identity

Protected commerce identity remains guarded; unverified facts are not invented.

### Theme topology

- Live MAIN: **MVQueen — Release Candidate** (`154876772550`)
- Automated staging: **MVQueen — Staging Preview** (`155002798278`, UNPUBLISHED)
- Automation may never deploy to MAIN.
- Publishing remains manual/explicit.
- The custom storefront is MVQueen-owned Liquid/CSS/JS, not Dawn/Helio/Horizon-based.

### Current launch/operation gates

Core platform and always-on product automation are operational. Remaining business/external certification work is tracked separately from architecture, including payment/test-checkout confirmation, external marketing/lifecycle providers where desired, resilience/restore drills, and continuing live performance optimization.

