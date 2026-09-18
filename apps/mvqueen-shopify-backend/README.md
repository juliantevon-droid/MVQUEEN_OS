# MVQUEEN Shopify Backend

Dedicated Shopify backend boundary for MVQUEEN_OS.

## Phase 1
- Shopify CLI configuration
- Authentication/session boundary
- Read-only GraphQL connectivity
- Catalog read/normalization
- Health/status endpoints
- Audit logging
- Dry-run enforcement
- Controlled product workflows
- Webhooks

## Safety
- Never commit Shopify access tokens or API secrets.
- Begin with minimum read scopes.
- Keep writes behind explicit dry-run controls.
- Preserve handles, SKUs, variants, inventory, and media unless a workflow explicitly authorizes a change.
- Validate GraphQL operations against the live Shopify schema before execution.
- Keep the existing GraphQL engine reusable; do not create a second catalog engine.

## Environments
Use separate Shopify app configurations for development, staging, and production. Do not actively develop against the live production installation.

The existing `15_Scripts_And_Code/mvqueen_engine` is the reusable domain/automation layer; this app is the Shopify integration boundary around it.
