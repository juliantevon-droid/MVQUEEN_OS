# MVQueen Phone / GitHub / Shopify Operating Setup

## Current operating model — 2026-10-03

Production automation no longer depends on a scheduled Drive-to-GitHub code bridge.

- **GitHub `main`** is the code/theme authority.
- **Railway** runs the production Shopify app, continuous product worker and PostgreSQL.
- **Shopify** is the live commerce authority.
- **Google Drive** is assets/knowledge/archive/backup storage and never automatically overwrites `main`.
- Theme code changes on `main` validate and deploy only to the unpublished **MVQueen — Staging Preview** theme.

## Theme Access credential

The Shopify Theme Access password must remain in GitHub Actions secrets as:

- `SHOPIFY_CLI_THEME_TOKEN`

Never commit or paste that credential into repository files, Drive documents or screenshots.

## Canonical deployment identity

The workflow is pinned in repository code to:

- Store: `tsucu0-1i.myshopify.com`
- Automated target: `MVQueen — Staging Preview`
- Theme ID: `155002798278`
- Required role: `UNPUBLISHED`

Do not point automation at the current MAIN theme (`MVQueen — Release Candidate`, `154876772550`).

## What a storefront push to main does

For controlled theme changes, GitHub Actions:

1. validates the MVQUEEN control registry
2. validates the theme contract
3. runs the storefront release audit
4. runs Shopify Theme Check
5. verifies the configured target is not MAIN
6. pushes only the controlled allowlist with `--nodelete`
7. verifies the target is still unpublished
8. runs the staging-preview Lighthouse gate
9. stores deployment evidence

There is no automatic `theme publish` operation.

## Phone-friendly workflow

From a phone, make or approve the repository change through the connected GitHub workflow, then monitor GitHub Actions. Approved Drive material can be reviewed and promoted into GitHub deliberately, but Drive itself is not an executable source and has no scheduled auto-commit authority.

## Product automation is separate

Product automation does not require theme deployment. Shopify `products/create` and `products/update` webhooks feed the durable PostgreSQL queue, and the continuous Railway product worker processes eligible Shopify products 24/7.

Protected product identity/state remains governed. The worker must not fabricate product facts or silently overwrite protected SKU/inventory/variant identity.
