# MVQUEEN Historical Catalog Archive Notice — 2026-09-24

## Production decision

**THE HISTORICAL 948-PRODUCT RECOVERY SET IS NOT A PRODUCTION CATALOG.**

The merchant clarified that these files belong to an old product set. MVQUEEN production product work uses **only products currently imported into Shopify**.

## Source-of-truth rule

- Shopify is the source of truth for current products, variants, pricing, inventory, media, publication state and storefront assortment.
- Historical CSV blobs in Git history are archival evidence only.
- Historical recovery counts, duplicate families, media gaps and taxonomy results do not affect production readiness.
- No historical product may be recreated, imported, published, optimized or assigned to collections unless the merchant explicitly reintroduces that product into the current Shopify catalog.

## Current verified Shopify catalog

At the time of this correction:

- Total products: **2**
- ACTIVE: **2**
- DRAFT: **0**
- ARCHIVED: **0**

The active products are the Brown Aventurine Bead Necklace and Pink Thulite Pendant already present in Shopify.

## Historical tooling status

Recovery utilities remain available as read-only/reference engineering tools because they document safe handling of legacy data. They are **not active production gates**.

The following are no longer production blockers:

- historical 948-product normalization
- historical SKU collision analysis
- historical duplicate-handle planning
- historical media recovery
- historical taxonomy completion
- historical CSV release planning

Active production work must be based on the connected Shopify catalog only.
