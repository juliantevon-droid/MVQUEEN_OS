# MVQUEEN OS — Shopify Backend App

This directory is the integration boundary for the dedicated MVQUEEN Shopify developer app.

## Role

The backend app is intentionally separate from the existing Shopify ChatGPT MCP App. It will own MVQUEEN-specific automation while the existing app remains untouched.

Planned responsibilities:

- Shopify Admin GraphQL authentication
- Product/catalog reads and controlled writes
- SEO/content optimization workflows
- Collections and merchandising automation
- Metafields/metaobjects
- Inventory-aware workflows where explicitly enabled
- Webhooks and event processing
- Redirect management
- Dry-run, audit logging, and rollback-aware operations
- Integration with the existing `15_Scripts_And_Code/mvqueen_engine`
- Future Google Sheets / Colab / Apps Script integrations

## Safety model

1. Development, staging, and production configurations remain separate.
2. Read-only connectivity is established before write scopes are enabled.
3. Write workflows default to dry-run.
4. High-volume catalog changes require an audit record before execution.
5. Existing handles, SKUs, variants, inventory, and media are preserved unless a workflow explicitly authorizes a change.
6. Shopify API credentials are never committed to Git.

## Shopify CLI

The actual app record and generated CLI configuration should be linked through Shopify CLI rather than manually inventing credentials.

From this directory's future app root, use the current Shopify CLI workflow:

```bash
shopify app init
shopify app config link
shopify app dev
```

For a new app, Shopify CLI can create the app record in the Dev Dashboard. For an existing app, `shopify app config link` can connect the local project to that app.

## Current MVQUEEN integration

The existing GraphQL client is located at:

`15_Scripts_And_Code/mvqueen_engine/shopify_graphql_client.py`

It already provides explicit API versioning, environment-only credentials, dry-run protection, retries/backoff, GraphQL error handling, mutation `userErrors`, and cursor pagination. The dedicated app should reuse those concepts rather than creating a second unsafe catalog engine.

## Initial rollout

### Phase 1 — connectivity
- Create/link dedicated Shopify app
- Verify OAuth/session handling
- Verify Admin GraphQL read access
- Add `/health` and `/api/shopify/status`
- Confirm store identity without modifying catalog data

### Phase 2 — read services
- Product inventory/catalog snapshot
- Collections
- Metafields
- Orders/customers only when actually required

### Phase 3 — controlled writes
- Product content
- SEO fields
- Tags/category metadata
- Collections
- Metafields

### Phase 4 — event automation
- Webhooks
- Queue/job layer
- Idempotency
- Audit logs
- Retry/dead-letter handling

No production catalog write should be enabled merely because the app can authenticate.
