# MVQUEEN_OS Enterprise Operating System V2

**Status:** ACTIVE ARCHITECTURE  
**Canonical branch:** `main`

## Objective

Turn MVQUEEN_OS from a repository of capable subsystems into one governed commerce operating system. Every capability must have an authority, an input contract, an output contract, an execution mode, an approval boundary, and an observable status.

## Canonical enterprise flow

```
SHOPIFY EVENT / CONTROLLED BACKFILL
        ↓
INGEST
        ↓
SOURCE TRUTH
        ↓
CLASSIFY
        ↓
BRAND ROUTE
        ↓
CONTENT → SEO → MERCHANDISING
        ↓
COMMERCIAL
        ↓
PRICING → PROFITABILITY
        ↓
CREATIVE / CAMPAIGN PLAN
        ↓
QA
        ↓
APPROVAL
        ↓
SHOPIFY / EXTERNAL ADAPTER
        ↓
MEASUREMENT
        ↓
LEARNING
        ↺
```

## Runtime ownership

- **GitHub main:** code, contracts, tests, capability registry.
- **Shopify:** authoritative products, variants, inventory, orders, collections and storefront commerce state.
- **React Router app:** sole authenticated Shopify runtime writer.
- **PRODUCTION_READINESS:** canonical deterministic production/intelligence contracts and QA.
- **Python engine:** offline intelligence, proposal generation, audit and validation only.
- **Storefront theme:** presentation plus first-party event emission.
- **External marketing providers:** advertising/analytics execution only through explicit adapters.
- **Google Drive:** references, assets, archives and backups; never production code authority.

## Enterprise capability rule

A capability is not considered complete because a file exists. It is complete only when:

1. Its upstream input is authoritative.
2. Its logic has a named owner.
3. Its output is consumed by the next stage.
4. Unsafe writes are fail-closed.
5. QA can detect failure.
6. State can be observed.
7. A human approval boundary exists where money, publication, legal exposure, or external spend is involved.

## Pricing and profitability

Pricing is now part of the live product decision path, but remains advisory.

Required production inputs:
- verified `commercial.unit_cost`
- payment percentage
- payment fixed fee
- return/refund reserve
- target CAC
- target contribution margin
- optional inbound shipping cost

Environment contract:
- `MVQ_PAYMENT_RATE`
- `MVQ_PAYMENT_FIXED`
- `MVQ_RETURN_RESERVE_RATE`
- `MVQ_TARGET_CONTRIBUTION_MARGIN_RATE`
- `MVQ_TARGET_CAC`
- optional `MVQ_INBOUND_SHIPPING_DEFAULT`
- optional `MVQ_CURRENCY`

The engine solves for a minimum viable selling price using contribution economics. It writes recommendation/status metadata only. It does **not** mutate Shopify variant prices.

## Marketing and advertising

Every classified product receives a channel/funnel/brand-world campaign plan. The planning layer is connected to the product decision path.

Paid advertising execution remains disabled until an approved provider is connected. The adapter contract must support:
- account discovery
- campaign/ad set/ad identity
- creative references
- budgets
- spend
- conversions
- revenue
- CAC/CPA
- ROAS
- change history
- explicit confirmation before spend or campaign-state changes

MVQueen and Miss.Princess share profitability governance but have distinct positioning and creative systems.

## Analytics

The storefront emits vendor-neutral first-party commerce events. No external tracking request is made by the core event bus.

Canonical events:
- `mvq:view_item`
- `mvq:view_collection`
- `mvq:add_to_cart`
- `mvq:view_cart`
- `mvq:begin_checkout`
- `mvq:brand_select`

External analytics/pixel adapters subscribe to these events only after consent/configuration requirements are satisfied.

## Release boundaries

Automatic product processing may update approved classification, brand-routing, commercial-status, marketing-status and analytics metadata.

Automatic processing must not silently mutate:
- live price / compare-at price
- SKU
- inventory
- variant identity
- handles
- product publication
- ad budgets
- campaign state
- discounts
- legal policies

These require dedicated operations, explicit scopes, approval and audit records.

## Database hardening

The current Prisma SQLite database is acceptable for development and validation. Production deployment must use a durable managed database before the runtime is called enterprise-production-ready.

## Definition of done

An area reaches enterprise-ready only when it is marked `connected` or `connected_advisory` in the capability registry, passes CI, has a failure path, and is observable from the control plane. Documentation-only areas remain visible as gaps rather than being counted as complete.

## Media ALT publication scope boundary

Shopify image/file ALT mutation requires a Files write scope that is not part of the current app authorization. The automatic catalog worker therefore records `catalog.media_alt_status=scope_required` when ALT text is missing and does not attempt an unauthorized mutation. Enabling automated media ALT publication is a separate permission change and release decision; it must not be hidden inside catalog processing.
