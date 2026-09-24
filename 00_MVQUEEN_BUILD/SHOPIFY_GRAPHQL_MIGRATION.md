# MVQUEEN Shopify GraphQL Runtime

## Production standard

MVQUEEN_OS uses Shopify Admin GraphQL through the authenticated React Router application in `app/`.

The application is the **only live Shopify network writer** in the repository.

## Active boundary

- API runtime: `app/shopify.server.ts`
- Product automation: `app/lib/product-processor.ts`
- API version: Shopify configuration, currently `2026-07`
- Live writes require `MVQ_WRITE_ENABLED=true`
- Each product must also be explicitly listed in `MVQ_APPROVED_PRODUCT_GIDS`

## Python role

`15_Scripts_And_Code/mvqueen_engine/` is offline/dry-run intelligence:

- classification
- editorial proposals
- SEO proposals
- protected-field checks
- catalog QA
- release artifacts

Python contains **no default Shopify HTTP client** and no access-token runtime configuration.

## Migration status

Legacy REST clients and the former standalone Python GraphQL transport were retired from active `main`. Their history remains recoverable through Git history and Drive archives.

## Catalog safety

Automation preserves handles, SKUs, inventory, variants, prices, media relationships and publication state unless a separately governed workflow explicitly authorizes a change.
