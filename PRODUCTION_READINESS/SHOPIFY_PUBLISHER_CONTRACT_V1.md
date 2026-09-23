# MVQUEEN Shopify Publisher V1

## Purpose

Provide the single controlled transport adapter between an approved canonical MVQueen product record and Shopify.

## Boundary

The publisher is not a generator, editor, pricing engine, or approval engine. It consumes a record only after `PUBLISHING_BOUNDARY_V1` has authorized the exact content fingerprint.

Required path:

`Canonical Product → QA → Release Fingerprint → Approval → Publishing Boundary → SHOPIFY_PUBLISHER_V1 → Shopify`

## Allowed write scope V1

The first publisher version may update only:

- existing Shopify product ID
- title
- description/body HTML
- vendor (`MVQueen`)
- product type
- approved merchandising tags

## Explicitly protected in V1

The publisher must not modify:

- inventory quantities or inventory tracking
- SKU
- variant IDs or option identity
- handles
- variant prices
- source identifiers
- supplier facts

Pricing is an upstream approval concern and requires a separate controlled operation before variant-price publishing is introduced.

## Failure behavior

A rejected transport response is a failed publication. The publisher must raise a controlled error rather than report success.

The publisher must not silently retry business-invalid payloads or invent missing fields.

## Idempotency preparation

V1 identifies the target using the canonical `identity.product_id`. It does not perform handle-based upserts or create new products. Full idempotent create/update reconciliation is a later release concern.

## Testability

The Shopify transport is injectable so tests can verify payload mapping and write scope without contacting Shopify.

## Security

Credentials remain in the existing environment-backed Shopify transport. The publisher must never accept credentials inside the canonical product record or release artifact.
