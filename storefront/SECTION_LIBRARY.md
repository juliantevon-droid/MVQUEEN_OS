# MVQUEEN section library

These optional Online Store sections are installed in **MVQueen — Release Candidate**. They do not change existing page layouts. Open that theme's editor, choose a page template, select **Add section**, and search for **MVQUEEN**. Add, reorder, and configure the sections before saving.

| Section | Content and controls |
| --- | --- |
| MVQUEEN Slideshow | Up to eight slides, desktop/mobile images, text, links, overlay strength, heights, alignment, optional autoplay. |
| MVQUEEN Before and after | Two images with a draggable divider and keyboard-accessible range control. Use matching crops for the clearest comparison. |
| MVQUEEN Blog posts | Articles from a selected blog; column count, image proportions, excerpt, and date controls. |
| MVQUEEN Product tabs | Tabs containing collections, a selected/current product's description, or rich text and page content. |
| MVQUEEN Custom content | Image, text, and custom Liquid blocks; full-width blocks and column controls. |
| MVQUEEN Showcase | A selected/current product with image, title, price, product link, and optional collapsible details. Purchases continue on the product page so customers can select variants. |
| MVQUEEN Collapsible tabs | Native expandable rows for details, FAQs, or linked page content. Optionally keep just one row open. |
| MVQUEEN Testimonials | Merchant-entered customer quotes, optional attribution, portrait, and rating. Empty quotes stay hidden on the storefront. |
| MVQUEEN Image overlay | Image banner with text, a link, adjustable shading, and separate mobile imagery. |
| MVQUEEN Parallax | Up to eight reorderable image blocks, each with desktop/mobile images, text, and a link. Panels stack vertically with adjustable spacing and shared heights and motion controls. Existing main-panel content remains first. Motion is disabled for reduced-motion preferences and off on mobile by default. |
| MVQUEEN Product slider | Selected products or products from a collection, with swipe and arrow controls. |
| MVQUEEN Collections | Grid of selected collections with images, titles, and optional descriptions. |

All sections include spacing and white, MVQUEEN ivory, or Miss.Princess blush palette controls. Product and collection cards use the store's real catalog. Add your own photography and approved customer quotes; no customer endorsements are supplied.

For multiple parallax images, open **MVQUEEN Parallax → Add block → Image**. Choose the desktop image and optional mobile image in each block, then drag blocks to reorder them. A missing mobile image uses the desktop image; a mobile image alone also works on both screen sizes. Keep the optional main panel for an opening banner, or clear its content to use only the blocks. Blank blocks appear only in the editor. Mobile images work whether or not mobile motion is enabled.

## Editor and accessibility behavior

- Slideshow autoplay is off by default and disabled in the editor. When enabled, customers can pause it; focus, hovering, reduced-motion preferences, and off-screen visibility pause advancement.
- Sliders support native touch scrolling. Tabs support arrow keys, Home, and End. The comparison slider supports native range keyboard controls. Accordion rows use native disclosure elements.
- Without JavaScript, carousel content remains scrollable, tab content remains visible, and disclosure rows still work.
- Selecting a slide, tab panel, or accordion block in the editor exposes that block. Section reloading does not accumulate event listeners.
- English, Spanish, French, and Brazilian Portuguese control labels are included. Merchant-entered content is edited or translated separately.

## Development and deployment

Shared styling and custom elements live in `theme/snippets/mvq-section-kit.liquid`; Shopify bundles its stylesheet and JavaScript once through `content_for_header`. The other helper snippets handle headings, carousel controls, and responsive imagery. There are no runtime library dependencies.

The workflow `.github/workflows/mvqueen-theme-cicd.yml` includes the new files in its explicit upload list. Existing validation and unpublished-theme checks still apply. Merchant settings and page-template layouts are not overwritten by this addition.

Run the repository validators, Shopify Theme Check, and the interaction test before deploying. The browser test needs Node.js and Playwright with Chromium:

```sh
node storefront/tests/section-kit.browser.cjs
```

Use `PLAYWRIGHT_MODULE` to specify an installed Playwright module when it is outside the normal Node module search path.

The parallax rendering regression test uses LiquidJS for template logic and local fixtures for Shopify image filters, then checks the rendered HTML in Chromium. It requires development-only `liquidjs` and `playwright` packages; use `LIQUID_MODULE` and `PLAYWRIGHT_MODULE` for custom module paths:

```sh
node storefront/tests/parallax-render.browser.cjs
```
