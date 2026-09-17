# MVQUEEN Theme Drift & Sync Policy

## Current production development target

- Shopify store: `tsucu0-1i.myshopify.com`
- Live theme: Horizon (`MAIN`) — protected and untouched
- Development target: `MVQUEEN — Custom Production Build` (`UNPUBLISHED`)
- Target theme ID: `154611515590`

## Source-of-truth model

GitHub `storefront/theme/` is the MVQUEEN-owned storefront source of truth for the customer experience.

MVQUEEN is being built as a **fully custom storefront experience**. Horizon is not the customer-experience foundation and must not be treated as the design, interaction, or architectural source for MVQUEEN.

Shopify remains the commerce infrastructure underneath the experience: products, variants, inventory, cart, checkout, customer accounts, payments, orders, and platform services remain Shopify-managed. MVQUEEN owns the presentation and interaction layer.

The development target may temporarily contain Shopify-native files that are not part of the MVQUEEN-owned source tree. Their presence must not be interpreted as a requirement to preserve Horizon as the storefront architecture.

## Deployment safety rules

1. Never publish from automation.
2. Never deploy to a `MAIN` theme.
3. Do not use Horizon as the customer-experience foundation.
4. Deploy only governed MVQUEEN-owned files through an explicit allowlist.
5. Validate the source tree before any Shopify write.
6. Keep Shopify credentials out of the repository.
7. Preserve product handles, SKUs, inventory, variants, and product media unless a separately governed catalog operation explicitly changes them.
8. Theme work must preserve mobile usability, accessibility, reduced-motion behavior, performance, and graceful failure states.
9. Customer-facing product content uses MVQUEEN identity and excludes supplier/legacy brand contamination.

## Verified current state — 2026-09-17

The unpublished target is the protected development environment for the custom MVQUEEN storefront.

The deployed MVQUEEN source includes the core layout, MVQUEEN assets, navigation/home/product/collection/search/cart sections, SEO/schema snippets, and JSON templates used by the current deployment allowlist.

The next architecture step is to progressively replace generic/native storefront behavior with MVQUEEN-owned presentation and interaction patterns rather than expanding a theme overlay around Horizon.

## Why this matters

MVQUEEN's intended experience is:

**private boutique × editorial fashion journal × personal curator × modern digital atelier**

The storefront should feel considered rather than mass-market, curated rather than crowded, and personal rather than corporate. Technical sophistication should remain underneath the experience rather than becoming the experience.

## Next synchronization gate

Before expanding the deployment surface:

- audit the complete `storefront/theme/` source tree;
- identify any remaining generic or inherited storefront behavior;
- define the custom design-system contract;
- verify every allowlisted file exists locally;
- verify the target remains `UNPUBLISHED`;
- run the contract validator and Shopify Theme Check;
- deploy only governed MVQUEEN-owned files;
- re-read the target theme metadata after deployment;
- then continue into catalog, redirect, content, SEO, and purchase-path automation.
