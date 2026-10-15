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
