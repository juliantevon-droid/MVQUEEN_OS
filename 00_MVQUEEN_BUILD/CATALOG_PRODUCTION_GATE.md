# MVQUEEN — Catalog Production Gate

**Status:** ACTIVE / PRE-WRITE CONTROL
**System:** MVQUEEN_OS
**Guard:** `15_Scripts_And_Code/mvqueen_engine/catalog_guard.py`

## Objective

No catalog optimization job is production-approved until the proposed changes pass a safety gate. The optimizer may improve customer-facing content, SEO, merchandising metadata, and approved metafields, but it must not silently alter operational catalog data.

## Protected by default

- Handles
- Product / Variant IDs
- SKUs and barcodes
- Inventory quantities, tracking, and policy
- Variant options and values
- Shipping/tax flags
- Image source, position, and variant-image relationships
- Gift-card state

## Content checks

Every proposed product record is checked for:

1. Required title and body content.
2. SEO title and SEO description presence.
3. SEO title length warnings.
4. SEO description length warnings.
5. Duplicate handles and titles.
6. Third-party/supplier brand contamination.
7. MVQUEEN brand-signal presence.
8. Protected-field mutations.

## Execution rule

`Catalog Guard -> dry run -> review report -> approved write plan -> Shopify mutation`

Never reverse this order.

## Failure policy

- **ERROR:** block the write plan.
- **WARNING:** allow review but do not silently ignore.
- **PASS:** eligible for the next production gate, not automatic publication.

## Rollback principle

The guard validates changes; it does not replace backups. Any production mutation must retain enough before-state data to restore the affected product fields.

## Brand rule

Customer-facing optimized content uses **MVQUEEN**. Sister-brand references and supplier-brand residue are not allowed to leak into customer-facing product copy.

## Scope

This gate is deliberately independent from Shopify credentials. It can run locally, in GitHub Actions, or inside a future catalog orchestration job before any Shopify mutation.
