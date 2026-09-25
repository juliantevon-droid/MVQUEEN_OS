# MVQueen Engine Contracts V1

## Single source of truth

The canonical product production record is defined by `PRODUCT_SCHEMA_V1.json`. Downstream engines consume and enrich that record; they do not create competing product truth.

## Ownership

| Layer | Owns | Must not own |
|---|---|---|
| Source Truth | verified supplier/product facts | marketing interpretation |
| Product Intelligence | need, desire, context, positioning | unsupported factual claims |
| Editorial | title, short/full copy, benefits/features | pricing or inventory |
| SEO | SEO title, metadata, keywords, ALT | product facts not in truth layer |
| Merchandising | collections, tags, related products, bundles | inventory mutation |
| Commercial | angles, offers, objections, proof mapping | fabricated proof |
| Creative | asset briefs and channel manifests | fabricated product claims |
| Content Intelligence | product-page blocks, verified metafields, FAQs, collection drafts, blog drafts | product truth, protected fields, auto-publication |
| Pricing | recommendations and approved publish price | silent publication of recommendations |
| Shopify | transport/export of approved record | rewriting upstream truth |
| QA/Overseer | validation and release gate | bypassing failed checks |

## Integration rule

Only the canonical product pipeline may produce the final production record. Downstream content generation may consume only `PRODUCTION_READY` records. Legacy runtimes, free-text all-in-one processors, and metafield generators that can invent facts are retired and must fail closed rather than compete with the canonical pipeline.

## Protected data

Inventory, SKU, variant identity, product IDs, source identifiers, and other protected fields are immutable unless an explicit controlled operation says otherwise.

## Release rule

No bulk catalog run begins until a representative product passes the complete pipeline and the same fixture passes repeatedly with deterministic output.
