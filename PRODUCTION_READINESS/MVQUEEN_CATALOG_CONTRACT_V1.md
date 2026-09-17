# MVQueen Catalog Production Contract V1

This contract consolidates the useful production-safety principles from the enterprise-hardening work into the current `main` architecture without replacing `main` wholesale.

## Canonical flow

`Source CSV / Shopify → Canonical normalization → Editorial intelligence → SEO/E-E-A-T → QA → Release gate → Shopify export`

## Brand policy

- Canonical product brand: **MVQueen**.
- Sephora, Victoria's Secret, Fenty Beauty, Dior, and Miss. Queen are inspiration/reference brands only.
- Supplier/third-party brand names are removed from generated editorial copy when they are not the canonical MVQueen brand.
- Supplier filler, repeated fragments, malformed titles, and obvious keyword-stuffing artifacts are cleaned.
- The system must never invent unsupported ingredients, materials, certifications, performance claims, clinical claims, or product attributes.

## Immutable Shopify source fields

Ordinary catalog curation must not modify product/variant identity, handles, SKUs, prices, inventory, options, fulfillment, operational status, or source-image structure.

The only image field intentionally editable by the SEO/content workflow is `Image Alt Text`.

## CSV rules

- Preserve the original source column order.
- Preserve every original product/variant/image row relationship.
- Split exports by **unique product count**, never raw CSV row count.
- Maximum: **850 products per import file**.
- Every output file must begin with the complete original Shopify header row.
- Never split variants or image rows from their parent product.

## QA gate

A release is blocked when protected fields change, required identity is missing, generated copy contains unsupported high-risk claims, brand policy is violated, duplicate/near-duplicate editorial content exceeds the configured threshold, or image ALT text is missing.

## Human approval

Generated catalog content is a preparation layer. Publishing should occur only after validation and explicit approval. A later Shopify API publisher may consume an approved release artifact; it must not regenerate content or bypass the release gate.
