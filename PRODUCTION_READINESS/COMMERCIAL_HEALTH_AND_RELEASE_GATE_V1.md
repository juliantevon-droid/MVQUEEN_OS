# MVQUEEN Commercial Health & Release Gate V1

**Status:** ACTIVE CONTRACT  
**Authority:** authenticated Shopify app runtime

## Purpose

Commercial Health converts current Shopify price, verified cost, and audited shop-level business assumptions into one profitability decision used by pricing, catalog release readiness, and paid-media eligibility.

This prevents pricing, marketing, and catalog QA from using different margin formulas.

## Required inputs

Per product:

- current selling price
- verified unit cost
- optional product-specific inbound/fulfillment cost

Per shop:

- payment percentage
- payment fixed fee
- return/refund reserve rate
- target contribution margin
- target CAC
- default inbound/fulfillment cost
- currency

Missing required inputs fail closed.

## Canonical calculations

```
payment_cost =
    selling_price × payment_rate
    + payment_fixed

return_reserve =
    selling_price × return_reserve_rate

contribution_before_ads =
    selling_price
    - unit_cost
    - inbound_shipping
    - payment_cost
    - return_reserve

max_break_even_cac =
    max(0, contribution_before_ads)

contribution_after_target_cac =
    contribution_before_ads
    - target_cac

contribution_margin_after_target_cac =
    contribution_after_target_cac
    / selling_price

break_even_roas =
    selling_price
    / max_break_even_cac

target_roas =
    selling_price
    / target_cac
```

ROAS outputs are omitted when their denominator is zero.

## Health states

- `needs_configuration` — required shop assumptions are missing.
- `needs_cost` — verified unit cost is missing.
- `needs_price` — selling price is missing/invalid.
- `invalid_inputs` — percentage assumptions cannot produce a viable commercial model.
- `blocked` — contribution is non-positive after configured CAC.
- `thin` — contribution is positive but below the configured target contribution margin.
- `healthy` — current price supports configured CAC and target contribution margin.

Only `healthy` products may be marked advertising-eligible.

## Policy versioning and staleness

Every product decision binds to a commercial-policy fingerprint.

When Commercial Settings change:

1. persisted product health becomes stale;
2. cached product automation fingerprints are invalidated;
3. live Catalog Health immediately evaluates against the new policy;
4. the next product processing/backfill creates a new current state and history snapshot.

Stale evidence can never authorize paid-media execution.

## Catalog release decision

Catalog Health combines:

- canonical brand-world integrity
- SEO brand integrity
- required content presence
- verified commercial cost
- valid selling price
- commercial health
- collection integrity

Blockers prevent release eligibility. Warnings produce review state. Advertising eligibility additionally requires healthy current economics.

## Paid-media boundary

A connected ad account is **not** sufficient authorization.

Campaign creation, enabling, pausing, and budget changes require:

- explicit human approval
- provider/account identity
- product-level commercial evidence
- `advertisingEligibility=eligible`
- non-stale evidence
- policy fingerprint
- positive max break-even CAC
- health evaluation no older than 24 hours

The external ad adapter must fail closed when any requirement is absent.
