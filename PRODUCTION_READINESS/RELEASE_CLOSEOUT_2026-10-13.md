# Release closeout — 2026-10-13

Status updated October 14 at 09:42 UTC: storefront published, public shopping
checks passed, and web application deployed successfully. The merchant restored
the web service's Wait for CI setting; readback confirmed it enabled for both
web and product worker. The live performance gate remains failed and the
product-worker rollout remains blocked. This release is not complete.

[PR #70](https://github.com/juliantevon-droid/MVQUEEN_OS/pull/70) merged into
`main` as `089df163eb6eb4a2bec2d58c74e773d73ac13127`. It contains the shopping,
navigation, durable-worker, and release-validation fixes described in the
[pre-release verification](LAUNCH_FIX_VERIFICATION_2026-10-13.md). This closeout
records subsequent live observations; it does not replace the failed or
passing historical samples in that report.

## Published theme

The merchant duplicated the verified Working Preview and published the copy
through Shopify Admin at 19:44 UTC. The resulting theme roles are:

| Purpose | Theme | ID | Role |
| --- | --- | --- | --- |
| Public storefront | Copy of MVQueen — Working Preview | `155532296390` | MAIN |
| Automated deployment target | MVQueen — Working Preview | `155277918406` | UNPUBLISHED |
| Previous public storefront | MVQueen — Staging Preview | `155002798278` | UNPUBLISHED |

Automation remains pinned to the original unpublished Working Preview. The
governed deployment allowlist, role checks, and prohibition on automated writes
to MAIN are unchanged. Theme names are descriptive; resolve actual Shopify
roles before subsequent deployments or promotion.

## Public shopping verification

At 19:46 UTC, a fresh anonymous browser visited the public storefront without a
preview URL or preview cookie and verified theme `155532296390`, role `main`.
All nine shopping checks passed:

1. Mobile homepage renders without Liquid errors or horizontal overflow and
   prioritizes the main image.
2. Mobile navigation opens and closes with Escape.
3. The collection filter drawer opens and closes on mobile.
4. An available variant adds to the cart, with its image rendered.
5. A cart quantity update persists.
6. The cart reaches hosted Shopify checkout.
7. The temporary anonymous test cart is cleared.
8. Product search returns results.
9. Desktop homepage renders without Liquid errors or horizontal overflow.

Independent positive navigation checks also passed on mobile and desktop across
seven pages: homepage, both brand pages, MVQueen collection root, Dresses with
sorting, MVQueen page two, and Miss.Princess Beauty with a price filter. The
appropriate brand menus retain all **26 MVQueen** and **14 Miss.Princess**
populated category links, with no unsupported category links. These counts are
a release-time catalog snapshot, not fixed limits on future navigation.

## Live performance gate

The pre-publication main-branch run failed the old MAIN theme's LCP-discovery
audit. After publication, the unchanged live performance workflow was rerun as
[run 38455624825, attempt 2](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38455624825/attempts/2).

Attempt 2 completed with **FAILURE** at 19:47:56 UTC on October 13, after
publication of MAIN theme `155532296390`. Performance samples were **67, 59,
64**, with median **64**. The other category medians were accessibility **100**,
best practices **79**, and SEO **100**. All category release floors passed.

The required `render-blocking-resources` audit scored **0.5 in all three
samples**, below its required score of 1. The other four required audits
(`errors-in-console`, `uses-responsive-images`, `image-size-responsive`, and
`lcp-discovery-insight`) scored 1 in every sample. The earlier LCP-discovery
failure was therefore resolved, but the public gate still failed.

The remaining reported resource was Shopify's
`/cdn/shopifycloud/portable-wallets/latest/accelerated-checkout-backwards-compat.css`
(2,434 bytes). Lighthouse listed 150 ms against that resource while displaying
**estimated savings of 0 ms** for the audit. This is Shopify wallet CSS injected
through `content_for_header`; it is not a theme-owned stylesheet.

The October 14 investigation did not establish a legitimate theme change that
resolves this audit. An extra redundant preload was rejected. No platform
header content was removed, and no performance budget or required audit was
weakened. The failed result remains visible and unresolved.

A fresh unchanged three-sample run on October 14 confirmed the failure:
[run 38501216422](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38501216422)
completed with FAILURE at 02:30:07 UTC. Performance was **71, 60, 68**, median
**68**; accessibility **100**, best practices **79**, and SEO **100**. The
render-blocking audit again scored **0.5 in all three samples**, with the same
Shopify wallet stylesheet and zero estimated savings. Console audit scores were
1, 1, 0 (median 1); all other required audits were 1 in every sample. No further
retries were used to select a favorable result.

The configured release floors and enterprise targets are unchanged. Earlier
preview scores establish preview behavior only; they do not substitute for
this public-storefront gate.

## Production application rollout

The target application code is merged commit
`089df163eb6eb4a2bec2d58c74e773d73ac13127`. Its application CI passed. Railway
initially skipped the web and product-worker deployments because the public
performance workflow failed. Railway's enabled Wait for CI setting considers
all GitHub Actions workflow conclusions for the commit, including this public
storefront check.

On October 14, a manual reconnect of the web service to its existing repository
and `main` branch started deployment
`1f5156b3-3df0-4b65-8042-9449ada0e5df` at the target commit. It reached
**SUCCESS at 02:28:53 UTC**, with one running replica and no service issues.
The reconnect also
unexpectedly reset the web service's `source.checkSuites` from `true` to
`false`. This was an unintended tool side effect. The merchant restored
**Wait for CI** in Railway's service settings. Readback at **09:42 UTC on
October 14** verified `source.checkSuites=true` for both the web and product-worker
services. The connected mutation tools do not expose that setting, so source
reconnect must not be reused as a deployment retry.

| Service | Verified state |
| --- | --- |
| Web | Deployment `1f5156b3-3df0-4b65-8042-9449ada0e5df` SUCCESS at `089df163eb6eb4a2bec2d58c74e773d73ac13127`. Wait for CI restored and verified enabled at 09:42 UTC on October 14. |
| Product worker | Unchanged successful deployment `6d5ec54d-e6df-469d-8bd3-2ff3628e3d09` at `c7b7c68c98417ef5045ae07ec62185c04e098deb`; merged worker fixes are not deployed. Wait for CI remains enabled. |
| Agent worker | Deployment `b85db4e3` SUCCESS at documentation-only commit `6bccab34c860a03ec0a29686ffd0a8b2d0caebdc`; application code is unchanged from `089df163`. |

A fresh application CI run against `main` commit `6bccab34` completed with
**SUCCESS at 09:44 UTC on October 14**:
[run 38544282061](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38544282061).
Catalog, durable-worker, production-preflight and enterprise tests, typecheck,
production build, and both production container builds passed. This establishes
readiness for the backend source build. It does not replace the failed public
storefront performance gate or certify the full release. Documentation-only
commits can skip application CI and live Lighthouse through workflow path
filters, so green documentation checks alone are insufficient evidence.

At 09:42 UTC on October 14, the public health endpoint again reported database ready,
continuous worker fresh, healthy product webhooks, and **zero received,
processing, failed, and dead-letter jobs**. Price and compare-at-price
publishing flags were **false**. This health snapshot describes the serving
runtime. Deployment metadata independently verifies the merged web fixes;
the merged product-worker fixes are still not running in the worker service.

### Operational recovery

1. **Completed:** the merchant restored **Wait for CI** on `mvqueen-web`.
   Readback at 09:42 UTC on October 14 verified `source.checkSuites=true` for
   both web and product worker. Preserve those enabled gates. Do not reuse the
   source-reconnect tool as a deployment retry: its observed side effect
   disables this setting.
2. With application CI now passed, use Railway's **Deploy Latest Commit** for
   the product worker while preserving Wait for CI. Open the
   [product-worker service](https://railway.com/project/164952b3-9c65-4dd4-bcba-415a98439b2e/service/4f77beaa-c7a5-4cfa-a92f-4d8da414f6f0?environmentId=3ba92036-2cbf-4496-b031-580d0554b8ea),
   open the command palette, and select **Deploy Latest Commit**. Default
   redeploy reuses the existing old image. Verify the new source commit,
   terminal SUCCESS, runtime health, and both services' enabled CI settings.
3. The storefront performance gate remains an independent release blocker.
   Completing the backend deployment does not resolve or waive that failure.
   Keep its failed evidence and existing thresholds; do not declare the full
   release complete until that gate is resolved.

The subsequent closeout documentation may have a newer Git commit than the
application deployment. Documentation-only commits do not change the verified
application or theme implementation.

## Verification limits

The browser checks reached checkout without entering payment details or
submitting an order. Payment capture, completed-order behavior, and customer-event
analytics remain untested. Runtime health is a dated observation; it does not
establish successful payment capture or guarantee future performance or queue
state. The live performance gate remains failed and application rollout remains
incomplete.
