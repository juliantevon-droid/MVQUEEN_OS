# MVQUEEN pricing system — current operating policy

Updated: 2026-10-12. This document supersedes conflicting ranges and
price-ending advice in older brand strategy notes. Engine implementation:
`app/lib/enterprise/category-pricing.ts`; financial floor:
`app/lib/enterprise/pricing-engine.ts`.

## Brand position

Affordable luxury, not universal high markup. Small essentials should be
accessible; higher-ticket fashion, curated sets and verified equipment may
support higher prices. Merchandising bands are approximate review ranges,
not evidence of actual competitor pricing or guaranteed profitable prices.

## Simple, single-item category bands (USD)

| Category | Range |
|---|---:|
| Silicone shampoo/scalp brush | $12.99–$17.99 (preferred $16.99) |
| Basic beauty tools (tweezers, sponges, combs) | $7.99–$17.99 |
| Eyeliner | $6.99–$19.99 |
| Basic eyebrow makeup | $8.99–$19.99 |
| Lip makeup | $6.99–$19.99 |
| Single bar soap | $6.99–$17.99 |
| Everyday jewelry | $9.99–$39.99 |
| Basic tops | $14.99–$29.99 |
| Everyday dresses | $24.99–$49.99 |
| Bodysuits/skirts | $19.99–$39.99 |
| Pants/jeans | $29.99–$59.99 |
| Basic skincare | $12.99–$29.99 |

Multi-packs, bundles, premium fabric/finish, equipment, electrical devices,
verified luxury designs, wig/extension quality tiers, unusual sizes and
outlier suppliers **require an item-specific review**. Do not blindly apply
single-item bands to variant bundles or devices.

## Required two-channel economics

1. **Paid acquisition:** Preserve the existing verified cost + fulfillment +
   payment fee + returns reserve + configured target CAC and target contribution
   margin formula. If the resulting floor exceeds the category ceiling, flag
   paid-channel cost conflict; do not inflate the item to conceal the loss.
2. **Organic/add-on scenario:** Show an *advisory only* scenario with $0
   product-level paid acquisition cost and a 20% contribution margin after
   the configured return reserve/processing/fulfillment allowance.
   Organic is **not free**: overhead, discounts, customer support, taxes,
   fulfillment differences and order-level acquisition still matter.
3. **Supplier conflict:** If even the organic scenario cannot fit the
   category ceiling, flag sourcing, unit economics or bundle/quality for review.
   Do not force a below-cost price.

Prices may end in .99 or .00 depending on product and merchandising; .99 is
permitted. Always round **above** the true contribution floor. Use compare-at
prices only where a valid, substantiated prior/reference price exists. Never
manufacture discounts.

## Shopify and release safeguards

- Read live Shopify inventory-item cost per variant; do not infer missing
  costs from supplier text or assign one unit cost to distinct variant sizes.
- Respect market currency, actual quantity and packaging.
- Record category diagnosis alongside each variant in
  `commercial.variant_decisions` when the existing worker processes it.
- Flag mispriced products for review; restrict paid promotion of identified
  category conflicts; do not silently overwrite merchant-approved prices.
- Preserve approved product GID, global write gate, price-publish gate,
  SKU, inventory, handles, variant options, shipping, compare-at integrity
  and all existing audit controls.
- Adjust live prices only once correct shipping, acquisition channel and
  a verified per-variant cost support the approved retail price.

Example: Shampoo Brush (Shopify supplier cost $7.23, assumed delivery $3)
currently sells for $32.99 with $8 target CAC / 30% contribution margin.
This is a **paid acquisition conflict**, not a reason to charge $32.99 for
an ordinary brush. An organic/add-on scenario may support about $16.99
under current assumptions, but is not authorization to publish that price.

## Status

Category guardrails implemented in code. Existing Shopify product prices
remain untouched until review and approval.
