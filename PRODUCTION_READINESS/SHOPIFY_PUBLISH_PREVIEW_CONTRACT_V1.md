# MVQueen Shopify Publish Preview V1

## Purpose
Create a deterministic, non-live review artifact before any approved product is handed to the Shopify publisher.

## Contract
Canonical Product → QA → Release Fingerprint → Approval → Publish Preview → Publishing Boundary → SHOPIFY_PUBLISHER_V1 → Shopify

The preview itself never calls Shopify and does not grant approval.

## V1 proposed writes
- title
- description/body HTML
- vendor
- product type
- approved merchandising tags

## V1 protected fields
- handle
- SKU
- variants/options
- inventory
- variant prices
- compare-at price

## Real-product rule
The Pink Thulite specimen may be used to generate and inspect a preview. Generating a preview does not change the live Shopify product. A live write requires the existing release gate, explicit approval artifact, publishing boundary, and controlled publisher.