# MVQUEEN Phone → Drive → GitHub → Shopify Setup

## What is already automated

`Phone → Google Drive → GitHub Actions → validation → Shopify unpublished theme`

The workflows are already committed to MVQUEEN_OS. The Shopify deployment gate is intentionally disabled until the store credential is added.

## One-time Shopify credential bridge

Shopify's current CI/CD guidance uses a Theme Access password as `SHOPIFY_CLI_THEME_TOKEN`. The password should be stored as a GitHub Actions secret, not committed to the repository.

1. In Shopify admin for `tsucu0-1i.myshopify.com`, install/open the **Theme Access** app.
2. Create a theme password for the developer/automation account.
3. In GitHub, open `juliantevon-droid/MVQUEEN_OS`.
4. Go to **Settings → Secrets and variables → Actions → Secrets**.
5. Create secret:
   - Name: `SHOPIFY_CLI_THEME_TOKEN`
   - Value: the Theme Access password.
6. In the same **Secrets and variables → Actions** area, open **Variables** and create:
   - `MVQUEEN_DEPLOY_ENABLED` = `true`
   - `MVQUEEN_SHOPIFY_STORE` = `tsucu0-1i.myshopify.com`
   - `MVQUEEN_SHOPIFY_THEME_ID` = `154611515590`
7. Do not add the password to any file, commit, workflow YAML, Google Drive document, or chat message.

## Result

After the bridge is enabled, a push to `main` that changes the controlled storefront source will:

1. run the MVQUEEN contract validator
2. run Shopify Theme Check
3. verify the target theme exists
4. refuse deployment if the target is the live `MAIN` theme
5. push the controlled files with `--nodelete`
6. leave the theme unpublished
7. store deployment evidence as a GitHub Actions artifact

There is no automatic `theme publish` operation.

## Phone operation

From a phone, the normal workflow becomes:

**Upload/edit approved work in Drive → wait for the scheduled Drive bridge → GitHub validates → Shopify unpublished theme updates automatically.**

For an immediate run, use GitHub Actions → `MVQUEEN Phone → Drive → GitHub Bridge` → **Run workflow**.

## Safety gates

- Drive bridge rejects secrets/credentials/keys/executables/archives and oversized files.
- Catalog worker defaults to dry-run.
- Product records without verified facts are held.
- Supplier/legacy brand strings are blocked.
- Protected fields such as handles, SKUs, inventory, variants, images, and vendor are not changed by the catalog worker.
- Live-theme publishing is not part of the automation.
