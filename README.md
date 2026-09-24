# MVQUEEN_OS

MVQUEEN_OS is the canonical operating system for the MVQueen storefront and its Miss.Princess sister-brand experience.

## One-system architecture

- GitHub main — canonical code, contracts, tests, theme source and automation logic.
- Shopify — canonical live commerce state: products, variants, inventory, IDs, collections and deployed themes.
- Google Drive — archive, source assets, references, imports/exports and backups. Drive is not an executable code source.
- app/ — the only live Shopify application runtime. It is React Router + Shopify Admin GraphQL.
- storefront/theme/ — the only canonical Shopify theme source.
- 15_Scripts_And_Code/mvqueen_engine/ — deterministic intelligence, catalog proposal, QA and dry-run tooling.
- PRODUCTION_READINESS/ — release, approval, preview, audit and production contracts.

## Shopify write boundary

The authenticated React app is the only repository component permitted to make live Shopify mutations. Writes require:

1. MVQ_WRITE_ENABLED=true
2. the exact product GID in MVQ_APPROVED_PRODUCT_GIDS

Python tooling produces validated artifacts and release evidence but has no default live Shopify transport.

## Safety

Never commit credentials. Protected product identity, SKU, inventory, variant, pricing and image-relationship fields are outside editorial automation.
