# MVQUEEN Theme Drift & Sync Policy

## Current production development target

- Shopify store: `tsucu0-1i.myshopify.com`
- Live theme: Horizon (`MAIN`)
- Development target: `MVQUEEN — Custom Production Build` (`UNPUBLISHED`)
- Target theme ID: `154611515590`

## Source-of-truth model

GitHub `storefront/theme/` is the MVQUEEN-owned overlay source. The unpublished Shopify theme also contains the native Horizon base files required by Shopify and by the storefront runtime.

The deployment system therefore **must not treat the small MVQUEEN source tree as a complete replacement theme**.

## Deployment safety rules

1. Never publish from automation.
2. Never deploy to a `MAIN` theme.
3. Use `--nodelete` so native Horizon files are preserved.
4. Use an explicit `--only` allowlist for MVQUEEN-owned files.
5. Validate the source tree before any Shopify write.
6. Keep Shopify credentials out of the repository.
7. Preserve product handles, SKUs, inventory, variants, and product media unless a separately governed catalog operation explicitly changes them.

## Verified current state — 2026-09-17

The unpublished target reports `processing=false` and `processingFailed=false`.

The deployed MVQUEEN overlay includes the core layout, MVQUEEN assets, navigation/home/product/collection/search/cart sections, SEO/schema snippets, and JSON templates used by the automation allowlist.

The Shopify theme also retains the native Horizon asset/component library. These files are intentionally not copied into `storefront/theme/` as part of the current overlay workflow.

## Why this matters

A future full-theme synchronization must first capture and version the complete Horizon base. Until that is deliberately completed, the safe architecture is an **overlay deployment**, not a destructive full-theme mirror.

## Next synchronization gate

Before expanding the deployment surface:

- compare the GitHub overlay against the unpublished Shopify target;
- verify every allowlisted file exists locally;
- verify the target remains `UNPUBLISHED`;
- run the contract validator and Shopify Theme Check;
- deploy with `--nodelete` and explicit `--only` paths;
- re-read the target theme metadata after deployment;
- only then proceed to catalog/content automation.
