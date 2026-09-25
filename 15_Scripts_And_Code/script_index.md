# Script Index

## Canonical location

Active MVQueen Python logic lives under:

- `15_Scripts_And_Code/mvqueen_engine/` — deterministic brand/catalog intelligence and dry-run tooling.
- `PRODUCTION_READINESS/` — schema, QA, release, approval and audit contracts.
- `app/` — the only authenticated live Shopify mutation runtime.

## Retired bootstrap/runtime scripts

Legacy Termux/Drive pullers, direct Shopify REST uploaders, conflict copies, generated installers and local sync scripts are intentionally not active on `main`.

Google Drive is archive/assets/reference only. It does not overwrite GitHub source.

## Safety

- No committed credentials.
- No direct Python Shopify transport.
- Shopify writes require the React app write gate and an explicitly approved product GID.
- SKU, inventory, variants, handles, pricing and image relationships remain protected.

Status: **ACTIVE — unified architecture**
