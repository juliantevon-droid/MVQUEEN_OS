# MVQueen SEO — Cluster Pillars & Redirect Architecture

## Purpose

This document defines the production URL architecture for MVQueen so SEO equity, navigation, product discovery, and future catalog growth remain connected.

## Pillar Model

Primary pillars:
- Fashion
- Beauty
- Skincare
- Jewelry
- Accessories
- Fragrance & Body
- Gifts
- The MVQueen Edit
- Miss.Princess — same-site sister experience with its own editorial direction

Each pillar should connect to supporting clusters, collections, editorial content, and products.

## Cluster Flow

`Pillar → Cluster → Collection → Product → Related Products / Editorial`

Examples:
- Jewelry → Necklaces → Pendant Necklaces → individual products
- Beauty → Makeup → Face Makeup → individual products
- Skincare → Face Care → Cleansers → individual products
- Fashion → Clothing → Dresses → individual products

## Redirect Rules

1. Every intentionally changed public URL must have a reviewed redirect from the old path to the closest final destination.
2. Product handle changes redirect directly to the final product URL.
3. Collection handle changes redirect directly to the final collection URL.
4. Page handle changes redirect directly to the final page URL.
5. Merged or retired collections redirect to the most relevant surviving collection or pillar.
6. Do not create redirect chains.
7. Do not redirect unrelated URLs simply to preserve traffic.
8. Internal navigation must link directly to final canonical URLs rather than relying on redirects.
9. Preserve existing product handles whenever there is no clear SEO or brand reason to change them.
10. Review redirects before publishing major taxonomy changes.

## Redirect Audit Status — 2026-09-21

Shopify currently reports **0 existing URL redirects** on the canonical store `tsucu0-1i.myshopify.com`.

This means the redirect layer is clean, but it also means historical URLs have not yet been mapped. We must not invent historical redirects. A source URL inventory/export is required before bulk creation.

## Required Redirect Sources

Build the production redirect map from:
- previous Shopify product exports
- previous Shopify collection/page exports
- any renamed handles
- Google Search Console indexed URLs
- analytics landing-page URLs
- old navigation destinations
- documented migrations from prior MVQueen builds

## SEO Safety

Redirects are a recovery layer, not the primary internal-linking strategy. The storefront should use canonical URLs, breadcrumbs, direct collection links, related products, editorial links, and pillar navigation.

## Ownership

This architecture is part of the proprietary MVQueen OS system and is intended only for the MVQueen project.