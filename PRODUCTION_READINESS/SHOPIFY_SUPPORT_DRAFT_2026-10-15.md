# Shopify support draft — Shop Pay cart-sync frame policy

**Draft only. Not submitted or sent.** Prepared October 15, 2026.

## Subject

Native Shop Pay cart-sync iframe intermittently logs a frame-ancestors CSP error
on our public storefront

## Message to support

Our public store is `https://tsucu0-1i.myshopify.com`. An automated anonymous
mobile Lighthouse check on October 15 at approximately 02:18 UTC recorded a
browser security error in two of three samples:

```text
Framing 'https://shop.app/' violates the following Content Security Policy
directive: "frame-ancestors 'self' https://shop.app https://admin.shopify.com".
The request has been blocked.
```

The evidence is in GitHub Actions
[run 38670160057](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38670160057).
The required `errors-in-console` audit scored 0, 1, 0; its median of 0 failed
our existing minimum of 1. Render-blocking, responsive images, image-size and
LCP-discovery audits passed in all three samples. Overall performance scores
were 58, 53 and 57; we are not attributing all performance cost to this frame.

A separate anonymous Chromium network trace identified the native frame:

- Frame title: **Shop Pay cart sync**.
- Frame URL: `https://shop.app/pay/hop` (query parameters removed).
- Initiating module:
  `https://cdn.shopify.com/shopifycloud/shop-js/modules/v2/chunk.casing_U_9x-Om3.esm.js`.
- The homepage uses Shopify's generated Shop.js scripts through the standard
  Liquid `content_for_header`; our theme source contains no custom iframe or
  `shop.app` reference.

The separate 12-second local trace did not reproduce the console error. It
establishes the native frame's source, not that the issue is fixed. We have kept
the failed automated result and have not changed the audit thresholds, filtered
`content_for_header`, changed payment settings or removed Shop Pay.

Could you investigate the native cart-sync frame/redirect response policy and
confirm whether this error is expected? If it is a platform issue, please
provide a supported remedy or incident reference that preserves the intended
Shop Pay behavior. We would also appreciate guidance on a reproducible check
for this condition.

## Evidence handling

Share only sanitized details above and the relevant CI diagnostic. Raw hop URLs
can contain temporary query values; omit those from public tickets and replies.
No customer, payment-card or account-login information is needed for this report.

The framed response controls its own `frame-ancestors` restriction; adding a
storefront CSP cannot relax that response's policy. See
[MDN's explanation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors)
and Shopify's guidance for
[`content_for_header`](https://shopify.dev/docs/api/liquid/objects/content_for_header).

---

## Update — October 17, 2026: Shopify accelerated-checkout CSS

**Status:** still a support draft; not submitted. This update adds the later October 16 three-sample live storefront evidence. It does not supersede the earlier Shop Pay cart-sync iframe report.

**Additional subject:** Shopify-injected accelerated-checkout stylesheet fails required render-blocking Lighthouse audit even with zero estimated savings.

**Affected public store:** `https://tsucu0-1i.myshopify.com/`

**Recent measured evidence:**
- GitHub Actions [public Lighthouse run 38979980116](https://github.com/juliantevon-droid/MVQUEEN_OS/actions/runs/38979980116) (October 16, 2026, 23:10 UTC).
- Mobile performance scores 69, 62, 47; median **62**. Best Practices 79, 79, 75; median **79**. Accessibility and SEO median **100** each.
- Required `render-blocking-resources` audit scores **0.5, 0.5, 0.5**; the existing release minimum is **1.0**, so the gate appropriately fails.
- Diagnostic identifies `/cdn/shopifycloud/portable-wallets/latest/accelerated-checkout-backwards-compat.css` (Shopify CDN): approximately **2,446 bytes**, **150 ms** attributed wasted time, while the audit displays **0 ms estimated savings**.
- LCP discovery is **1.0** in all three samples, with gateway image `loading=eager` and `fetchpriority=high`. The earlier discovery issue is not the cause of this required-audit failure.
- The theme's `layout/theme.liquid` uses a plain `{{ content_for_header }}` in `<head>`. The theme does not directly reference the `portable-wallets` CSS file.

**Request to Shopify support:** Please identify the platform-owned feature that injects this stylesheet, confirm whether the request and its render-blocking behavior are expected, and provide a supported way to prevent unnecessary render blocking **without removing native Shop Pay/accelerated checkout, disabling checkout services, or modifying `content_for_header`**. If it cannot be avoided, please provide an incident/reference and recommended way to distinguish this platform resource in performance analysis.

The theme developers have **not** changed Shopify's generated header, payment settings, the required Lighthouse audit, or its passing threshold. Shopify's own developer guidance states that `content_for_header` is required and must not be parsed or modified: https://shopify.dev/docs/api/liquid/objects/content_for_header and https://shopify.dev/docs/storefronts/themes/best-practices/performance/defer-non-critical-resources.

**Evidence sharing:** Strip request query tokens, customer details, and raw payment URLs before sharing. The GitHub run and the sanitized resource path are sufficient for the initial support request.
