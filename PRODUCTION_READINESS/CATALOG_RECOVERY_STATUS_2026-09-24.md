# MVQUEEN Catalog Recovery Status — 2026-09-24

## Decision

**RECOVERY SOURCE FOUND — IMPORT ON HOLD.**

The historical repository contains a complete Shopify-format recovery catalog, but it is not safe to import directly into production. The recovery artifacts remain historical evidence only until they pass normalization, brand cleanup, media validation, operational-field preservation, and explicit release approval.

## Recovered artifacts

| Artifact | Git blob | Size | Shopify rows | Unique products |
|---|---|---:|---:|---:|
| `12_Content_Assets/products.csv` / `products_export_1.csv` | `798c74782c079f96e3fbf6bbb46f1a55df063959` | ~3.83 MB | 3,575 | 948 |
| `12_Content_Assets/products_final.csv` | `f00b71139268803d1e3c0f5cd79e326d540087d1` | ~2.84 MB | 3,575 | 948 |
| `12_Content_Assets/products_output.csv` | `a5328c1c8cad74b12e503f05e774cca333634fd6` | ~4.24 MB | 3,575 | row-aligned enrichment only |

The cleaned `main` branch intentionally does not restore these large recovery CSVs. They remain recoverable from Git history and must not become runtime dependencies.

## Quality gate results for products_final.csv

- 948 / 948 products have titles.
- 948 / 948 products have HTML descriptions.
- 948 / 948 products have SEO titles.
- 948 / 948 products have SEO descriptions.
- 946 / 948 products have tags.
- 837 / 948 products have an MVQUEEN category; **111 are unclassified**.
- 731 / 948 products have an MVQUEEN product type.
- 650 / 948 products have an MVQUEEN persona.
- Custom short-description field: **0 / 948 populated**.
- Custom focus-keyword field: **0 / 948 populated**.
- Source image rows found in the CSV: **21**.
- Image rows with ALT text: **0**.
- SKU-bearing rows: 3,569.
- Unique SKU values: 3,433; duplicate/repeated SKU relationships require reconciliation before any create/import path.

## Supplier and legacy-brand leakage

The recovery file is not customer-facing brand clean:

- Vendor `eprolo`: 941 products.
- Vendor `Dropsure`: 7 products.
- Supplier/manufacturer names also remain in titles, including OUHOE, Jaysuing, and Roxelis.

The production catalog validator now blocks the known supplier/legacy identities found during this audit, including EPROLO, DROPSURE, JAYSUING, ROXELIS, DESIRE GEM, and MIA JEWELRY, in addition to the existing legacy-brand denylist.

## Recovery rules

1. Never import the historical CSV directly.
2. Never overwrite handles, SKUs, variant relationships, prices, inventory, options, fulfillment fields, or source-image relationships during editorial transformation.
3. Do not use historical `active` status as permission to publish newly recreated products. A future create/recovery path must create products as **DRAFT** until individually or batch-approved.
4. Remove supplier identities from customer-facing title, description, SEO, tags, and brand fields while retaining supplier provenance only in an internal governed field if needed.
5. Verify unsupported claims, ingredients, materials, certifications, and product attributes rather than generating them.
6. Resolve duplicate/repeated SKU relationships before creation.
7. Restore/verify product media and create truthful ALT text from verified product facts.
8. Classify all products into the canonical collection/category system.
9. Split any Shopify CSV release by **unique products**, maximum 850 products per file, without separating variant/image rows from the parent product.
10. Run the governed catalog validation and explicit human release approval before Shopify mutation.

## Current production consequence

The connected Shopify store currently contains only two active products, so the recovered 948-product catalog is a **recovery candidate**, not proof of current live assortment.

The next catalog phase is:

`historical recovery blob → read-only normalization → supplier/claim cleanup → classification/media reconciliation → draft release artifacts → approval → controlled Shopify creation`

No new parallel runtime or production branch should be created for this work.

## Stabilization results — 2026-09-24

The real historical recovery source now passes the governed normalization and dedupe validation pipeline.

### Normalization

- Source: 3,575 Shopify rows / 948 product handles.
- Normalized REVIEW: 948.
- Normalized HOLD: 0.
- Supplier/reference-brand leakage after normalization: 0.
- Protected commerce-field changes: 0.
- Canonical taxonomy: complete; no unclassified category or product type remains in the normalized recovery set.

### Duplicate resolution

A read-only release planner resolves SKU collisions by selecting the richest canonical member of a proven duplicate family and excluding only records whose SKU set is fully represented by the canonical member.

- Collision components resolved: 36.
- Redundant handles excluded: 39.
- Unresolved collision components: 0.
- Canonical release candidates: **909**.
- Handles/SKUs are never rewritten during dedupe planning.

### Media recovery

Historical product-media coverage is the remaining data blocker:

- Canonical release candidates with recovered CSV media: 11.
- Canonical release candidates without recovered CSV media: **898**.
- Shopify Files currently contains five images, all belonging to the two live products.
- Google Drive MIME-filtered searches found no indexed MVQUEEN/product/catalog image archive.

The catalog therefore remains non-importable until verified product media is recovered or replaced. No placeholder or AI-invented product imagery should be treated as factual product media.

### Release boundary

No raw or normalized historical `active` / `published` value authorizes publication.

A future recovery release must be:
`normalized canonical record → media reconciliation → QA → approved DRAFT create artifact → explicit approval → authenticated Shopify writer`

The Python recovery stack remains network-free and cannot publish to Shopify.

