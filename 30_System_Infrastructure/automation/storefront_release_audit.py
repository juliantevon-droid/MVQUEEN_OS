#!/usr/bin/env python3
"""MVQueen storefront static release audit.

Read-only release gate for the governed custom storefront source. It validates
customer-journey, mobile, accessibility, SEO, measurement, and performance
contracts that Shopify Theme Check does not fully express.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "storefront" / "theme"
OUT = ROOT / "build" / "storefront_release_audit"

CHECKS: dict[str, tuple[str, tuple[str, ...]]] = {
    "global_shell": (
        "layout/theme.liquid",
        (
            'name="viewport"',
            'class="mvq-skip-link"',
            "{% render 'seo-meta' %}",
            '"MVQAnalyticsContext"',
            "'mvqueen.js' | asset_url",
            "'mvqueen-ux.js' | asset_url",
            "'mvqueen-analytics.js' | asset_url",
            " defer",
            '"search_performed"',
            '"search_terms"',
        ),
    ),
    "mobile_navigation": (
        "sections/header.liquid",
        (
            "data-mvq-menu",
            "data-mvq-panel",
            'aria-controls="MVQMobilePanel"',
            'aria-expanded="false"',
            "Miss.Princess",
            "/pages/mvqueen",
            "/pages/miss-princess",
        ),
    ),
    "product_purchase": (
        "sections/main-product.liquid",
        (
            "{% form 'product'",
            'name="id"',
            'name="quantity"',
            'name="add"',
            "catalog.short_description",
            "catalog.highlights",
            "<summary>Shipping & returns</summary>",
            "/pages/shipping-policy",
            "/pages/refund-policy",
            "{% render 'trust-badges' %}",
            "mvq-mobile-purchase-bar",
            'form="{{ product_form_id }}"',
        ),
    ),
    "cart_checkout": (
        "sections/main-cart.liquid",
        (
            "{% form 'cart'",
            'name="updates[]"',
            'name="update"',
            'name="checkout"',
            "Secure checkout",
            "cart.total_price",
            "{% render 'trust-badges', compact: true %}",
        ),
    ),
    "collection_discovery": (
        "sections/main-collection.liquid",
        (
            "collection.filters",
            "data-filter-open",
            "data-filter-close",
            "data-filter-drawer",
            'aria-controls="CollectionFilters"',
            "collection.sort_options",
            "mvq-active-filters",
            "paginate collection.products",
        ),
    ),
    "search_discovery": (
        "sections/main-search.liquid",
        (
            'role="search"',
            'for="SearchInput"',
            'type="search"',
            "search.results_count",
            "mvq-search-empty",
            "paginate search.results",
        ),
    ),
    "contact_care": (
        "sections/contact-page.liquid",
        (
            "{% form 'contact'",
            'name="contact[email]"',
            'name="contact[body]"',
            "form.posted_successfully?",
            "form.errors",
            "required aria-required",
        ),
    ),
    "seo_indexability": (
        "snippets/seo-meta.liquid",
        (
            'rel="canonical"',
            'name="robots"',
            "request.page_type == 'search'",
            "request.page_type == 'cart'",
            "collection.products_count == 0",
            '"SearchAction"',
        ),
    ),
    "structured_data": (
        "snippets/product-schema.liquid",
        (
            '"@type":"Product"',
            "assign product_brand = 'MVQueen'",
        ),
    ),
    "analytics": (
        "assets/mvqueen-analytics.js",
        (
            'emit("mvq:view_item")',
            'emit("mvq:view_collection")',
            'emit("mvq:view_cart")',
            'emit("mvq:search"',
            'emit("mvq:add_to_cart"',
            'emit("mvq:begin_checkout"',
            "event.submitter",
            'getAttribute("name") === "checkout"',
        ),
    ),
    "mobile_filter_accessibility": (
        "assets/mvqueen-ux.js",
        (
            "aria-modal",
            "aria-hidden",
            "inert",
            "event.key==='Escape'",
            "event.key!=='Tab'",
            "returnFocus",
        ),
    ),
    "menu_accessibility": (
        "assets/mvqueen.js",
        (
            "aria-expanded",
            "aria-label",
            "returnFocus",
            "event.key === 'Escape'",
            "event.key !== 'Tab'",
            "prefers-reduced-motion",
        ),
    ),
    "mobile_purchase_css": (
        "assets/mvqueen-product.css",
        (
            ".mvq-mobile-purchase-bar",
            "@media(max-width:749px)",
            "env(safe-area-inset-bottom)",
            "min-height:48px",
        ),
    ),
    "global_accessibility_performance_css": (
        "assets/mvqueen-design-system.css",
        (
            ":focus-visible",
            "min-height: 48px",
            "@media (prefers-reduced-motion: reduce)",
        ),
    ),
    "trust": (
        "snippets/trust-badges.liquid",
        (
            "shop.enabled_payment_types",
            "payment_type_svg_tag",
            "Purchase reassurance",
        ),
    ),
    "translations": (
        "locales/en.default.json",
        (
            '"aria_label"',
            '"secure_title"',
            '"policy_title"',
            '"support_title"',
            '"payments_label"',
        ),
    ),
}

PERFORMANCE_CHECKS = {
    "product_primary_image_eager": ("sections/main-product.liquid", "fetchpriority: 'high'"),
    "product_secondary_images_lazy": ("sections/main-product.liquid", "loading: 'lazy'"),
    "product_card_images_lazy": ("snippets/product-card.liquid", "loading: 'lazy'"),
    "theme_scripts_deferred": ("layout/theme.liquid", " defer"),
}


def read(rel: str) -> str:
    return (THEME / rel).read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    failures: list[dict[str, str]] = []
    passed: list[str] = []

    for name, (rel, tokens) in CHECKS.items():
        path = THEME / rel
        if not path.is_file():
            failures.append({"check": name, "file": rel, "reason": "missing file"})
            continue
        source = read(rel)
        missing = [token for token in tokens if token not in source]
        if missing:
            failures.append({
                "check": name,
                "file": rel,
                "reason": "missing contract tokens: " + ", ".join(missing),
            })
        else:
            passed.append(name)

    for name, (rel, token) in PERFORMANCE_CHECKS.items():
        path = THEME / rel
        if not path.is_file() or token not in read(rel):
            failures.append({"check": name, "file": rel, "reason": f"missing performance token: {token}"})
        else:
            passed.append(name)

    external_gates = [
        "purchase completion analytics must be verified through Shopify Customer Events / approved pixel instrumentation",
        "payment-provider activation and a real test checkout remain account-level/manual commerce verification",
        "visual viewport QA still requires human/browser inspection of the unpublished staging theme",
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "scope": "governed storefront static release contract",
        "passed_checks": sorted(passed),
        "failures": failures,
        "external_release_gates": external_gates,
        "result": "PASS" if not failures else "FAIL",
    }
    (OUT / "report.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# MVQueen Storefront Release Audit",
        "",
        f"**Result:** {payload['result']}",
        f"**Passed checks:** {len(passed)}",
        f"**Failures:** {len(failures)}",
        "",
        "## External release gates",
        "",
        *[f"- {item}" for item in external_gates],
    ]
    if failures:
        md += ["", "## Failures", ""] + [
            f"- **{item['check']}** ({item['file']}): {item['reason']}" for item in failures
        ]
    (OUT / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"STOREFRONT RELEASE AUDIT: {payload['result']}")
    print(f"Passed: {len(passed)}")
    for item in failures:
        print(f"- {item['check']} [{item['file']}]: {item['reason']}")
    for gate in external_gates:
        print(f"EXTERNAL GATE: {gate}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
