#!/usr/bin/env python3
"""MVQUEEN storefront contract validator.

Runs without third-party dependencies so it can execute on GitHub Actions,
ChromeOS/Linux, or a phone-driven workflow runner.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "storefront" / "theme"

REQUIRED = {
    "layout/theme.liquid",
    "assets/mvqueen.css",
    "assets/mvqueen.js",
    "assets/mvqueen-ux.js",
    "sections/header.liquid",
    "sections/hero.liquid",
    "sections/announcement-bar.liquid",
    "sections/footer.liquid",
    "sections/main-product.liquid",
    "sections/main-collection.liquid",
    "sections/main-search.liquid",
    "sections/main-cart.liquid",
    "sections/product-recommendations.liquid",
    "snippets/breadcrumbs.liquid",
    "snippets/product-schema.liquid",
    "snippets/seo-meta.liquid",
    "templates/index.json",
    "templates/product.json",
    "templates/collection.json",
    "templates/search.json",
    "templates/cart.json",
}

FORBIDDEN_BRANDS = [
    "MISS.QUEEN",
    "MISS. QUEEN",
    "OUHOE",
    "HOEGOA",
    "FANZHEN",
    "EELHOPE",
    "COLOR FIT",
    "WEST & MONTH",
]


def read(path: str) -> str:
    return (THEME / path).read_text(encoding="utf-8")


def json_without_header(text: str) -> dict:
    # Shopify JSON templates may begin with an auto-generated comment block.
    text = re.sub(r"^/\*.*?\*/\s*", "", text, flags=re.S)
    return json.loads(text)


def main() -> int:
    failures: list[str] = []
    if not THEME.exists():
        failures.append(f"Theme source directory missing: {THEME}")
        print("\n".join(failures))
        return 1

    for rel in sorted(REQUIRED):
        if not (THEME / rel).is_file():
            failures.append(f"Missing required theme source: {rel}")

    if failures:
        print("THEME CONTRACT: FAIL")
        print("\n".join(failures))
        return 1

    layout = read("layout/theme.liquid")
    for token in [
        "{{ 'mvqueen.css' | asset_url | stylesheet_tag }}",
        "{{ content_for_header }}",
        "{{ content_for_layout }}",
        "'mvqueen.js' | asset_url",
        "'mvqueen-ux.js' | asset_url",
        "{% render 'seo-meta' %}",
    ]:
        if token not in layout:
            failures.append(f"theme.liquid missing required integration: {token}")

    schema = read("snippets/product-schema.liquid")
    if '"@type":"Product"' not in schema or '"@type":"Brand","name":"MVQUEEN"' not in schema:
        failures.append("Product schema must emit Product + MVQUEEN brand")
    if "aggregateRating" in schema or '"review"' in schema:
        failures.append("Review/rating schema must not be emitted without verified review data")

    # Validate every template JSON and every referenced section exists locally.
    for path in (THEME / "templates").glob("*.json"):
        try:
            obj = json_without_header(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"Invalid JSON: {path}: {exc}")
            continue
        for key, section in obj.get("sections", {}).items():
            section_type = section.get("type")
            if section_type and not (THEME / "sections" / f"{section_type}.liquid").exists():
                failures.append(f"Template {path.name} references missing section: {section_type}")

    all_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in THEME.rglob("*")
        if p.is_file() and p.suffix.lower() in {".liquid", ".css", ".js", ".json"}
    ).upper()
    for brand in FORBIDDEN_BRANDS:
        if brand in all_text:
            failures.append(f"Forbidden supplier/legacy brand string found: {brand}")

    # Catch accidental live-theme deployment controls in the source workflow.
    for workflow in (ROOT / ".github" / "workflows").glob("*.yml"):
        text = workflow.read_text(encoding="utf-8", errors="ignore")
        if "--allow-live" in text or "theme publish" in text:
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
