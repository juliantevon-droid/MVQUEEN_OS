# MVQUEEN Finance Order Economics V1

**Status:** ACTIVE READ-ONLY CONTRACT  
**Authority:** Shopify order totals + verified commercial cost snapshots + audited Commercial Settings

## Purpose

The Finance control provides a conservative 30-day commerce-economics view without using customer identity data and without mutating orders.

It is not an accounting ledger and must not label estimates as exact processor fees or fully loaded profit.

## Shopify access boundary

Required:

- `read_orders`
- `read_products`

Not required or authorized by this finance workflow:

- `write_orders`
- refund mutations
- fulfillment mutations
- customer identity fields
- customer email
- customer phone
- shipping address
- billing address

The runtime checks its own granted access scopes before reading orders. If `read_orders` is absent, it reads zero order data and reports that reauthorization is required.

## Reporting window

The initial control-plane report covers the most recent 30 days and paginates backward with a safety cap.

## Order truth

The report uses Shopify's current order totals:

- current total price
- current tax
- current discounts
- total refunds for separate reporting
- current line-item quantity

Shopify current totals already reflect returns/refunds as defined by Shopify. `totalRefundedSet` is shown separately and is not subtracted a second time.

## Cost truth

COGS uses product `commercial.unit_cost`, which is the governed verified-cost snapshot.

Product-specific `commercial.inbound_shipping` is used when present. Otherwise the audited shop-level fulfillment/inbound default is used.

Missing verified costs fail closed: COGS and downstream contribution are reported unavailable rather than estimated from retail price.

## Payment fees

Payment fees are estimated from Commercial Settings until actual processor transaction fees are connected.

The report must label them as estimates.

## Contribution levels

`commerceContributionBeforeAds`:

```
net revenue excluding tax
- verified COGS
- estimated fulfillment/inbound cost
- estimated payment fees
```

`targetCacBenchmarkContribution` subtracts the configured target CAC for non-cancelled, positive-value commerce orders only.

`fullyLoadedContribution` is unavailable until actual ad spend is connected. It must not be inferred from the target CAC benchmark.

## Privacy rule

Finance queries are intentionally minimum-necessary and must not add customer name, email, phone, shipping address, billing address, or other customer identity fields unless a separate approved workflow requires them.

## Mutation rule

Finance V1 is read-only. It cannot change:

- orders
- refunds
- fulfillments
- customers
- payouts
- inventory
- product prices

Any future finance action requires a separate capability, explicit scope, authorization, audit trail, and release contract.
