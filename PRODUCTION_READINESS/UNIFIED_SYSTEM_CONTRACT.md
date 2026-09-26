# MVQUEEN_OS Unified System Contract

**Status:** ACTIVE
**Canonical branch:** main

## Authority

| Layer | Source of truth |
|---|---|
| Code, contracts, tests | GitHub main |
| Live commerce state | Shopify |
| App runtime | app/ |
| Theme source | storefront/theme/ |
| Intelligence / dry-run | 15_Scripts_And_Code/mvqueen_engine/ |
| Release governance | PRODUCTION_READINESS/ |
| Assets / archives / backups | Google Drive |

## Non-negotiable boundaries

1. There is one live Shopify writer: the authenticated React Router app.
2. Python validates, classifies, generates proposals, fingerprints releases and builds artifacts; it has no default network transport.
3. Live app writes are off unless MVQ_WRITE_ENABLED=true.
4. A product is still blocked unless its exact GID is in MVQ_APPROVED_PRODUCT_GIDS.
5. Handles, SKUs, inventory, variants, prices and image relationships remain protected.
6. Theme deployment targets the verified unpublished theme until explicit launch approval.
7. Drive is not an alternate codebase and must not overwrite GitHub source.
8. Miss.Princess is the current sister-brand name. MISS.QUEEN references are legacy contamination terms unless explicitly documented as history.

## Repository hygiene

Production main does not track Obsidian plugin/runtime state, backup ZIPs, Python bytecode/cache, conflict copies, generated product exports, PDF/DOCX working copies, secrets or local .env files.

Git history and Drive preserve historical material without keeping it active.
## Governance note — 2026-09-25

Legacy sister-brand strings remain detection-only signals and must not appear as active customer-facing or canonical brand language. Governance scanners may reconstruct those legacy tokens programmatically for linting without reintroducing them into active brand documents.

## Shipping estimate contract — 2026-09-26

- Every production-ready product must carry a non-empty `shipping.delivery_estimate`.
- A supplier/carrier day range may be customer-facing only when it is backed by verified source evidence.
- When no verified window exists, the canonical fallback is: `Confirmed at checkout based on destination and fulfillment source.`
- The storefront displays the estimate near Add to Bag and inside Shipping & returns.
- `shipping.delivery_estimate` is a product metafield and is not stored in product descriptions.
- Future imports must preserve or generate the governed fallback; they must never invent optimistic shipping times.

