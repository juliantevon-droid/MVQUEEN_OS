# MVQUEEN OS — Runtime Validation Gate

## Purpose
Validate the backend before any live product webhook is enabled.

## Gate 1 — Static configuration
- Run `shopify app config validate --path .`.
- Confirm `shopify.app.toml` contains valid scopes and webhook topics.
- Replace placeholder application URL and client ID only after the real app is linked.

## Gate 2 — Dependencies and type safety
- Install dependencies from `package.json`.
- Run `npm run typecheck`.
- Run `npm run build`.

## Gate 3 — Local webhook test
- Start `shopify app dev` against a development store.
- Use Shopify's webhook trigger tooling for an initial delivery test.
- Then create/update an actual development-store product for an end-to-end test.

## Gate 4 — Data safety
Verify the processor does not modify:
SKU, inventory, price, variants, fulfillment, or handles.

## Gate 5 — Production
Only after Gates 1–4:
1. Deploy the web runtime to HTTPS hosting.
2. Link the Shopify app configuration.
3. Deploy the Shopify app configuration.
4. Install/authorize the app on the intended store.
5. Test one controlled product.
6. Begin catalog backfill in batches.

Shopify's current CLI separates app configuration deployment from deployment of the web application itself. The web runtime must therefore be hosted independently before live webhook processing is possible.
