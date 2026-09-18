# MVQUEEN Storefront Integration V1

Status: ACTIVE BUILD / UNPUBLISHED THEME ONLY
Branch: build/mvqueen-os-html-foundation-v2
Date: 2026-09-17

## Purpose
Transplant the production storefront foundation from the main MVQUEEN_OS architecture into the HTML-foundation branch without force-merging branches.

## Rules
- MVQUEEN owns customer-facing presentation and UX.
- Shopify remains the commerce engine.
- Dawn may remain the underlying Shopify theme during controlled development, but MVQUEEN storefront assets are the presentation layer.
- Horizon is not the customer-experience foundation.
- Native Liquid/CSS/JavaScript first.
- No live-theme publication from this workflow.
- Preserve handles, IDs, SKUs, inventory, variants, image sources/positions, and operational fields.
- Customer-facing brand language uses MVQUEEN only.
- Production catalog writes remain dry-run -> guard -> review -> approved mutation.
- Catalog capacity is unlimited; 850 is only the maximum products per Shopify import batch/file.

## Integrated surface
- theme layout and global assets
- header/footer/announcement
- home hero, trust, featured products, brand pillars, newsletter
- product template and recommendation surface
- collection/filter surface
- search and cart
- product card and breadcrumbs
- SEO metadata and Product JSON-LD

## Next gates
1. Theme syntax/contract validation.
2. Shopify unpublished-theme installation.
3. Mobile/desktop visual QA.
4. Catalog/metafield contract validation.
5. GraphQL catalog sync dry-run.
6. Explicit approval before any production write or publication.
