# MVQueen Release Readiness

## Safety state
- Shopify store: tsucu0-1i.myshopify.com
- Target theme: 154876674246
- Target role: UNPUBLISHED
- Live MAIN theme: 154869825734 (MVQueen — Custom Production Build).\n- Repository automation may update only the unpublished next-production theme; publishing remains a merchant action.

## Required gates
1. Repository contract validator passes.
2. Shopify Theme Check passes with no errors.
3. Deployment token exists only as a GitHub Actions secret.
4. Deployment target exists and is not MAIN before push.
5. Theme push uses `storefront/theme` as its source path.
6. Post-push theme-role verification passes.
7. Deployment evidence is retained as a workflow artifact.
8. Product/catalog writes remain separate from theme deployment.
9. No review/rating schema is emitted without verified review data.
10. Supplier/legacy brand strings remain blocked from storefront output.

## Current catalog gate
The current Shopify store has 0 products. Product import/creation is intentionally not part of this release until catalog facts and QA are ready.

## Operating rule
Validation may run automatically. Shopify deployment remains controlled by the explicit MVQUEEN_DEPLOY_ENABLED variable and the unpublished-theme checks.
