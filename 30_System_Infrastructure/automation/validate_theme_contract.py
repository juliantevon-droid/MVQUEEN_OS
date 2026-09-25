#!/usr/bin/env python3
"""MVQueen storefront contract validator."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "storefront" / "theme"

REQUIRED = {
    "layout/theme.liquid", "assets/mvqueen.css", "assets/mvqueen-design-system.css",
    "assets/mvqueen-header.css", "assets/mvqueen-product.css", "assets/brand-gateway.css",
    "assets/mvqueen.js", "assets/mvqueen-ux.js", "config/settings_schema.json",
    "sections/header.liquid", "sections/hero.liquid", "sections/brand-gateway.liquid",
    "sections/miss-princess-experience.liquid",
    "sections/editorial-curation.liquid", "sections/announcement-bar.liquid",
    "sections/footer.liquid", "sections/main-product.liquid", "sections/main-collection.liquid",
    "sections/main-search.liquid", "sections/main-cart.liquid", "sections/product-recommendations.liquid",
    "snippets/breadcrumbs.liquid", "snippets/product-schema.liquid", "snippets/seo-meta.liquid",
    "templates/index.json", "templates/product.json", "templates/collection.json",
    "templates/search.json", "templates/cart.json",
    "templates/page.mvqueen.json", "templates/page.miss-princess.json",
}

FORBIDDEN_BRANDS = [
    "MISS.QUEEN", "MISS. QUEEN", "OUHOE", "HOEGOA",
    "FANZHEN", "EELHOPE", "COLOR FIT", "WEST & MONTH",
]

def read(path: str) -> str:
    return (THEME / path).read_text(encoding="utf-8")

def main() -> int:
    failures: list[str] = []
    if not THEME.exists():
        print(f"THEME CONTRACT: FAIL\n- Theme source directory missing: {THEME}")
        return 1
    for rel in sorted(REQUIRED):
        if not (THEME / rel).is_file():
            failures.append(f"Missing required theme source: {rel}")
    if failures:
        print("THEME CONTRACT: FAIL")
        print("\n".join(f"- {x}" for x in failures))
        return 1

    layout = read("layout/theme.liquid")
    for token in [
        "{{ 'mvqueen.css' | asset_url | stylesheet_tag }}",
        "{{ 'mvqueen-design-system.css' | asset_url | stylesheet_tag }}",
        "{{ 'mvqueen-header.css' | asset_url | stylesheet_tag }}",
        "{{ 'mvqueen-product.css' | asset_url | stylesheet_tag }}",
        "{{ content_for_header }}", "{{ content_for_layout }}",
        "'mvqueen.js' | asset_url", "'mvqueen-ux.js' | asset_url",
        "{% render 'seo-meta' %}",
    ]:
        if token not in layout:
            failures.append(f"theme.liquid missing required integration: {token}")

    header = read("sections/header.liquid")
    for token in ["data-mvq-menu", "data-mvq-panel", 'aria-controls="MVQMobilePanel"', 'id="MVQMobilePanel"', 'aria-expanded="false"']:
        if token not in header:
            failures.append(f"header.liquid missing accessibility/navigation integration: {token}")

    # Canonical PDP content namespaces are part of the storefront contract.
    product = read("sections/main-product.liquid")
    for token in [
        "product.metafields.catalog.short_description.value",
        "product.metafields.catalog.highlights.value",
        "product.metafields.content.faq.value",
        "product.metafields.content.how_to_use",
        "product.metafields.content.care_instructions",
        "product.metafields.attributes.ingredients",
        "product.metafields.attributes.main_stone.value",
        'class="mvq-product-bullets"',
        "<details>",
        "<summary>Product details</summary>",
        "<summary>Shipping & returns</summary>",
        'href="/pages/shipping-policy"',
        'href="/pages/refund-policy"',
    ]:
        if token not in product:
            failures.append(f"main-product.liquid missing required custom PDP integration: {token}")

    gateway = read("sections/brand-gateway.liquid")
    if "Miss.Princess" not in gateway or "MVQueen" not in gateway:
        failures.append("Brand gateway must provide both MVQueen and Miss.Princess destinations")

    for rel in ["templates/page.mvqueen.json", "templates/page.miss-princess.json"]:
        if not (THEME / rel).is_file():
            failures.append(f"Missing brand-world page template: {rel}")

    schema = read("snippets/product-schema.liquid")
    schema_compact = re.sub(r"\s+", "", schema)
    if '"@type":"Product"' not in schema_compact or "assign product_brand = 'MVQueen'" not in schema:
        failures.append("Product schema must emit Product + MVQueen brand")
    if "aggregateRating" in schema or '"review"' in schema:
        failures.append("Review/rating schema must not be emitted without verified review data")

    for path in (THEME / "templates").glob("*.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"Invalid JSON: {path}: {exc}")
            continue
        for section in obj.get("sections", {}).values():
            section_type = section.get("type")
            if section_type and not (THEME / "sections" / f"{section_type}.liquid").exists():
                failures.append(f"Template {path.name} references missing section: {section_type}")

    # The MVQueen source must be self-contained. A custom source file may not
    # quietly depend on a snippet, section, or theme asset that exists only in
    # an inherited Shopify/Horizon/Helio base theme.
    liquid_files = list(THEME.rglob("*.liquid"))
    render_re = re.compile(r"{%\\s*render\\s+['\"]([^'\"]+)['\"]")
    section_re = re.compile(r"{%\\s*section\\s+['\"]([^'\"]+)['\"]")
    asset_re = re.compile(r"['\"]([^'\"]+)['\"]\\s*\\|\\s*asset_url")

    missing_dependencies: set[str] = set()
    for liquid_path in liquid_files:
        source = liquid_path.read_text(encoding="utf-8", errors="ignore")
        rel_source = liquid_path.relative_to(THEME).as_posix()

        for name in render_re.findall(source):
            target = THEME / "snippets" / f"{name}.liquid"
            if not target.is_file():
                missing_dependencies.add(f"{rel_source} -> snippets/{name}.liquid")

        for name in section_re.findall(source):
            target = THEME / "sections" / f"{name}.liquid"
            if not target.is_file():
                missing_dependencies.add(f"{rel_source} -> sections/{name}.liquid")

        for name in asset_re.findall(source):
            # Shopify may expose generated/platform assets, but customer-owned
            # theme source must not rely on undeclared local theme assets.
            if "/" in name or name.startswith(("http:", "https:")):
                continue
            target = THEME / "assets" / name
            if not target.is_file():
                missing_dependencies.add(f"{rel_source} -> assets/{name}")

    if missing_dependencies:
        failures.append(
            "Custom theme source has inherited/missing dependencies:\\n  - "
            + "\\n  - ".join(sorted(missing_dependencies))
        )

    all_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in THEME.rglob("*")
        if p.is_file() and p.suffix.lower() in {".liquid", ".css", ".js", ".json"}
    ).upper()
    if "\\n" in read("assets/mvqueen-design-system.css"):
        failures.append("Design-system CSS contains a literal escaped newline artifact")

    design = read("assets/mvqueen-design-system.css")
    for token in ["--ink: var(--mvq-charcoal)", "--display: var(--mvq-display)"]:
        if token not in design:
            failures.append(f"Design-system compatibility alias missing: {token}")

    ux = read("assets/mvqueen-ux.js")
    js = read("assets/mvqueen.js")
    if "data-filter-open" not in ux or "data-filter-close" not in ux:
        failures.append("Collection filter behavior must remain in mvqueen-ux.js")
    if "filterOpenButtons" in js or "filterDrawer" in js:
        failures.append("Duplicate collection filter controller detected in mvqueen.js")

    for brand in FORBIDDEN_BRANDS:
        if brand in all_text:
            failures.append(f"Forbidden supplier/legacy brand string found: {brand}")

    for framework in ["DAWN", "HORIZON", "HELIO"]:
        if framework in all_text:
            failures.append(f"Legacy/commercial theme framework reference found in custom theme source: {framework}")

    for workflow in (ROOT / ".github" / "workflows").glob("*.yml"):
        workflow_text = workflow.read_text(encoding="utf-8", errors="ignore")
        if "--allow-live" in workflow_text or "theme publish" in workflow_text:
            failures.append(f"Live-theme publishing control detected in workflow: {workflow}")

    if failures:
        print("THEME CONTRACT: FAIL")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("THEME CONTRACT: PASS")
    print(f"Validated {len(REQUIRED)} required theme source files.")
    print("Live-theme publishing is contractually blocked by this repository validator.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
