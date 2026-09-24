# MVQUEEN Shopify Engine Map

## Canonical runtime
- app/ — authenticated React Router Shopify application.
- app/lib/product-processor.ts — only live Shopify mutation path; classification/transport only, not a copy generator.
- Shopify Admin API — GraphQL, current configured API version.
- Writes require MVQ_WRITE_ENABLED=true and explicit product GID approval.

## Intelligence layer
- 15_Scripts_And_Code/mvqueen_engine/
- Product classification and deterministic brand intelligence.
- Catalog dry-runs and protected-field validation.
- Historical Python engine code is non-authoritative for production copy; governed content is produced under PRODUCTION_READINESS.
- No default live Shopify transport.

## Release governance
- PRODUCTION_READINESS/
- Schema validation, QA, release fingerprint, explicit approval, publish preview and audit ledger.
- Transport-neutral payload contract.
- CONTENT_INTELLIGENCE_V1.py — product-page, verified metafield, FAQ, collection, and blog draft generation from PRODUCTION_READY records.

## Theme
- storefront/theme/
- One custom MVQUEEN / Miss.Princess storefront source.
- CI validates theme structure and blocks live-theme publication from repository automation.

## Data authority
- GitHub main: code.
- Shopify: live commerce data.
- Google Drive: archive/assets/backups.

## Production sequence
Evidence → Proposal → Guard → QA → Fingerprint → Approval → Authenticated app mutation → Verify → Audit.
