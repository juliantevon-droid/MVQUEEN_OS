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
- The governed store default is `7–15 business days` for products without a faster verified supplier/carrier window.
- Verified product-specific estimates such as `5–7 business days` or `6–10 business days` override the store default when supported by fulfillment evidence.
- The storefront displays the estimate near Add to Bag and inside Shipping & returns.
- `shipping.delivery_estimate` is a product metafield and is not stored in product descriptions.
- Future imports must preserve or generate the governed store default; they must never invent an unsupported faster shipping time.


## Operational integration boundary — 2026-09-29

- Railway `mvqueen-web`, `mvqueen-product-worker`, and Postgres are the production runtime. The background worker continuously owns queue draining, retries, dead-letter handling, and reconciliation.
- GitHub Actions monitors production `/healthz` every five minutes. It does not duplicate worker ownership and must not report a secret-missing no-op as runtime success.
- Railway services are sourced from GitHub `main`; deploy-on-push remains an account-level integration and is not assumed unless Railway reports it enabled.
- Google Drive is a knowledge/assets/archive/backup layer. Drive intake is explicit, manual, review-only, and fail-closed when source authentication is not configured. It never automatically commits or overwrites `main`.
- Automated theme deployment targets only the verified unpublished `MVQueen — Staging Preview` theme. The Shopify `MAIN` theme is never an automated write target.
- Shopify remains the sole authority for current production products, variants, inventory, collections, menus, pages, publications, policies, orders, and live-theme role.
