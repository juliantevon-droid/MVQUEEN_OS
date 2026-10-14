# Launch fix verification — 2026-10-13

> Historical pre-release snapshot. PR #70 has since merged, and the merchant
> published a duplicate of the verified preview. See the
> [October 13 release closeout](RELEASE_CLOSEOUT_2026-10-13.md) for the current
> theme identity, public storefront checks, and production rollout evidence.
> The earlier observations and release steps below remain as recorded.

Updated October 13; earlier observations below retain their dates.

The shopping-flow and worker fixes are prepared in [PR #70](https://github.com/juliantevon-droid/MVQUEEN_OS/pull/70).
The changes have not been merged into `main`, deployed to the production app,
or published as the live Shopify theme. The corrected preview passes the
existing release gates; live rollout remains a separate merchant decision.

## Changes

- Product and cart images render as image elements with correctly escaped alt
  text. Collection sorting preserves active filters and category routes; blank
  price limits stay blank.
- Brand navigation checks categories against the corresponding collection's
  tags, preserves supported descendants, and retains the full collection link.
  Tag arrays are passed explicitly through the nested menu snippets. Shopify
  returned empty `all_tags` for this store, so the header falls back to `tags`
  from the unfiltered global collection. Missing metadata leaves configured
  links accessible rather than hiding every category.
- The ordinary durable worker leaves backfill jobs to their dedicated runner,
  restores defaults for unset settings, observes retry limits, and rejects stale
  concurrent claims. The isolated regression suite makes no Shopify writes.
- GitHub Actions runs the storefront and worker regressions. Current category
  pricing changes from `main` through `7b9eb4f` are preserved.
- The preview performance workflow now accepts the canonical cookie-based
  Working Preview URL. Each Lighthouse sample verifies the actual audited
  page's theme ID and unpublished role; a silent fallback to MAIN fails.

## Code validation

- Storefront: 16 rendered Liquid regression tests and five preview-identity
  tests pass, including positive category visibility in desktop/mobile menus,
  the empty `all_tags` fallback, and rejection of MAIN-theme audit results.
- Worker, catalog automation, enterprise, production preflight, TypeScript, and
  production build checks pass. Worker and enterprise suites are rechecked after
  merging the latest category pricing changes.
- Shopify Theme Check: zero errors; four existing warnings remain.
- Control registry and theme contracts pass; storefront release audit passes
  all 31 checks. Theme CSS and JavaScript remain within the existing budgets.
- The latest multipack pricing safeguard required updating an outdated test:
  sets retain a pricing-review hold while a single-item control has no hold.
  The complete app suite and build pass after this correction.
- All applicable GitHub checks pass on code commit `e05d5b1`; the subsequent
  documentation commit changes no runtime or theme code. Skipped Lighthouse jobs
  on a pull request do not certify storefront speed; the separate manual run below
  does execute the preview gate.

## Staging and browser evidence

Shopify's live MAIN remains theme `155002798278`, named **MVQueen — Staging
Preview**. The deployment target is theme `155277918406`, named **MVQueen —
Working Preview**. The names alone do not establish roles.

[Initial staging run](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38290642700)
successfully deployed commit `c8de9e9` with pre/post checks proving the target
was unpublished. The later fixture-only change did not alter theme output.

On October 13 at 13:40 UTC, an anonymous browser rechecked the corrected preview on
mobile and desktop, no visible Liquid errors or horizontal overflow, working
menu/filter drawers, an available variant added to cart, a persisted quantity
update, search results, and handoff to hosted Shopify checkout. No payment or
order was submitted. The temporary cart was cleared. Loaded homepage images
were independently checked again in the final review.

The final menu correction `94d0429` was deployed successfully in
[run 38406484429](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38406484429).
On October 13 at 13:39 UTC, positive checks proved that exactly **26 MVQueen and
14 Miss.Princess** configured categories remain visible, with zero unsupported
category links. Both desktop and mobile menus passed across seven pages:
homepage, both brand pages, MVQueen collection root, filtered Dresses with
sorting, page two, and filtered Miss.Princess Beauty with a price filter.
Every page rendered the expected unpublished theme without Liquid errors or
temporary diagnostic markup. Mobile menu open/Escape behavior also passed.

The final [deployment and performance run 38406906279](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38406906279)
successfully staged `e05d5b1` and verified the unpublished theme on every
Lighthouse sample. Its theme files are identical to `94d0429` tested above;
the added change verifies preview identity in the performance workflow.

Use the [Working Preview](https://tsucu0-1i.myshopify.com/?preview_theme_id=155277918406&pb=0)
in a cookie-preserving browser. Shopify removes the query parameter after
setting its preview cookie; verify `Shopify.theme.id` rather than assuming the
redirect is still previewing the intended theme.

## Performance evidence

Budgets remain unchanged: performance release floor **55**, enterprise target
**90**, and all five required diagnostic audits must score **1**.

| Surface / sample set | Performance samples | Median | Result |
| --- | --- | --- | --- |
| Public MAIN, Oct 12 09:01 UTC | 58, 45, 49 | 49 | Fails performance floor and LCP discovery |
| Working Preview before this branch was staged, Oct 12 18:22 UTC | 74, 64, 44 | 64 | Passes preview floor; not evidence for later staged changes |
| Staged `c8de9e9`, Oct 12 23:33 UTC | 70, 40, 36 | 40 | Fails performance floor |
| Final `e05d5b1`, GitHub runner, Oct 13 13:42 UTC | 44, 89, 87 | 87 | Passes the unchanged preview release gate |

The 23:33 set scores 100 for accessibility, best practices, and SEO in every
sample and passes all five required audits. The two slow samples have LCP
around 9.4–9.5 seconds and substantial Shopify/Google script work and image
render delay. CPU variability adds uncertainty; no safe source change was
established from these results. Preview scores do not certify the future live
theme, and the older passing sample set does not override the later failure.

The final GitHub run audits the corrected candidate on the workflow runner:
performance **87**, accessibility **100**, best practices **79**, and SEO **100**
(three-run medians). All five required audits score **1 in every sample**, and
all three audited pages report theme `155277918406`, role `unpublished`.
Performance and best practices remain below their enterprise targets of 90;
their release floors remain 55 and 75. The raw first sample's performance of 44
is retained, so this is a median-gate pass rather than a claim of consistently
fast loads. These GitHub scores are not directly comparable to the earlier
cloud/proxy samples and do not establish the public MAIN theme's performance.

## Production runtime

On October 13 at 13:37 UTC, the public health endpoint still reports `ok: true`,
`production-automation-ready`, database ready, a fresh continuous worker,
healthy product webhooks, and zero received, processing, failed, and dead-letter
jobs. Price and compare-at publishing remain disabled. This observes the
existing production deployment, not this branch's worker fixes. See the
[earlier runtime verification](RUNTIME_VERIFICATION_2026-10-12.md) for service
and recovery evidence.

## Remaining release steps

1. Review and merge app changes into `main` after the final PR checks;
   verify the resulting production deployment and worker health afterward.
2. Obtain the merchant's separate live-theme promotion decision after reviewing
   the exact preview. Recheck theme roles immediately before promotion and run
   the public storefront release gate afterward.
   Keep an unpublished automation target for future pushes; promoting the
   currently pinned working theme makes it MAIN, which subsequent automated
   writes must reject until the staging identity is updated.
3. Payment capture and completed-order/customer-event analytics remain
   unverified; checkout handoff alone does not establish either.

The [release policy](../30_System_Infrastructure/automation/release-readiness.md)
states: “Theme publication remains an explicit merchant/admin action” and
“Live promotion is always a separate merchant release decision.”
