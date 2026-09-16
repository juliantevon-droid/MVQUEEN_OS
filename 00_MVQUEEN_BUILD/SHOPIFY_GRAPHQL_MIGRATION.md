# MVQUEEN Shopify GraphQL Migration

## Production standard

MVQUEEN OS is now **GraphQL-first** for new Shopify automation.

Shopify's 2026-07 release is the latest stable Admin API version as of September 2026. The new client defaults to `2026-07` while allowing the version to be overridden through `SHOPIFY_API_VERSION`. citeturn0search0turn0search2

## Existing system

`15_Scripts_And_Code/mvqueen_engine/shopify_client.py` is retained as the legacy REST maintenance layer.

## New system

`15_Scripts_And_Code/mvqueen_engine/shopify_graphql_client.py`

Capabilities:
- GraphQL Admin API
- explicit API version
- environment-only credentials
- dry-run protection for writes
- retry/backoff for transient failures
- structured top-level GraphQL errors
- mutation `userErrors` handling
- cursor pagination helper

## Migration rule

Do not delete the REST client immediately.

1. Keep legacy REST available for rollback.
2. Build new catalog workflows against GraphQL.
3. Run all destructive or high-volume writes in dry-run first.
4. Validate mutation shapes against the live Shopify schema before execution.
5. Move stable workflows to GraphQL one engine at a time.
6. Retire REST only after production parity is verified.

## Credential rule

Never commit Shopify access tokens to GitHub. Use environment variables or an approved secrets manager.

## Catalog safety

Product automation must preserve by default:
- handles
- SKUs
- variants
- inventory
- existing product media
- existing image rows

Content optimization should target approved fields only, with backups and audit logs before bulk writes.
