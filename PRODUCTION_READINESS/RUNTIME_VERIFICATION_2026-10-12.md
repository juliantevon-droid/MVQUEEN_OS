# Production runtime verification — 2026-10-12

Read-only verification completed at approximately **09:00 UTC** using Railway
service/deployment/log readbacks, the public health endpoint, and validated
Shopify Admin GraphQL queries. No deployment, configuration change, product
write, queue insertion, or theme publication was performed.

## Current production evidence

- [Railway project](https://railway.com/project/164952b3-9c65-4dd4-bcba-415a98439b2e)
  / production environment `3ba92036-2cbf-4496-b031-580d0554b8ea`:
  `mvqueen-web`, `mvqueen-product-worker`, `mvqueen-agent-worker`, and PostgreSQL
  are online, each with one running replica and no crashed replicas.
- Railway reports zero failed deployments and zero active warning/critical
  alerts in the preceding 24 hours.
- All three application services run GitHub `main` commit
  `3a92c37926a4913142cc66abb11f35352be83a75`, deployed on October 11.
  Local changes prepared after this commit are not included in this live evidence.
- [Public health endpoint](https://mvqueen-web-production.up.railway.app/healthz)
  returned `ok: true`, `production-automation-ready`, database ready, and zero
  received, processing, failed, and dead-letter jobs. Worker heartbeat was
  `2026-10-12T08:59:17.360Z`; webhook audit was healthy at
  `2026-10-12T08:55:29.556Z`.
- Recent product reconciliation runs occurred approximately every five minutes.
  The latest inspected run at `08:55:30 UTC` scanned 181 records for one shop and
  discovered zero missing jobs. This is a reconciliation scan count, not a
  claim that 181 products are published or sale-ready.
- The bounded worker error-log query from `08:00 UTC` to verification returned
  no entries. This does not assert that historical job errors never occurred.

## Capability and recovery evidence

The web health response reports catalog enrollment, editorial/SEO, title and
description publishing, existing-description rewriting, content surfaces,
reconciliation, image-alt repair, and cost synchronization enabled. Price and
compare-at price publishing are disabled. These are web-process capability
flags; Railway OAuth returns worker variable names but redacts their values, so
worker flag parity was not independently established.

On October 11, inspected worker logs recorded 122 transient Shopify `Throttled`
errors between `08:32:42` and `08:35:37 UTC`. Successful retry batches reduced the
failed backlog from 47 at `08:35:31` to zero at `08:36:39`; dead-letter count
remained zero. This provides production evidence that retries recovered that
incident, rather than relying solely on an idle health check.

## Theme source versus live storefront

Shopify file readbacks on October 12 confirm:

| Theme | Role | `sections/brand-gateway.liquid` |
| --- | --- | --- |
| `155002798278` — MVQueen — Staging Preview | MAIN | Last changed October 5; logo priority defaults to `low`, with conditional `high` |
| `155277918406` — MVQueen — Working Preview | UNPUBLISHED | Last changed October 9; logo priority is unconditionally `high` |

Working Preview file checksum `15b90059e653b3d55bb30a65e08abc07` matches the
checked-out gateway source. MAIN checksum is
`1d2fac5fcd6852f563d52626b8c2db2a`. The priority correction is therefore present
in the unpublished preview and is not live. This comparison covers the gateway
section only, not full-theme parity or a new Lighthouse performance result.

The read-only `OnlineStoreTheme` API exposes no visitor-preview URL. The standard
[Working Preview link](https://tsucu0-1i.myshopify.com/?preview_theme_id=155277918406)
was independently verified with an unauthenticated, cookie-preserving HTTP
client: the redirect destination's HTML reports `Shopify.theme.id` as
`155277918406`, name `MVQueen — Working Preview`, and role `unpublished`.
Shopify removes the preview parameter after setting its preview cookie.
Clients that discard cookies across redirects instead receive MAIN, so browser
and performance checks must preserve cookies and verify the rendered theme ID.

## Remaining verification limits

- These checks establish current runtime health and observed recovery; they do
  not substitute for storefront purchase-flow testing or a fresh performance run.
- Publication of Working Preview, paid order placement, and new catalog writes
  were outside this read-only verification.
- Earlier release documents naming Release Candidate `154876772550` as MAIN or
  Staging Preview `155002798278` as an unpublished deployment target are stale.
  Resolve current roles from Shopify before any future deployment or promotion.
