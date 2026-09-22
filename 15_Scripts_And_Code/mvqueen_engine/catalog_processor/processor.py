# mvqueen_engine/catalog_processor/processor.py
"""
PHASE 4 — CATALOG PROCESSOR

This engine can run in two modes:

MODE A — CSV MODE (offline)
    - Load supplier CSV
    - Apply all MVQueen curation
    - Export new curated CSV

MODE B — SHOPIFY LIVE MODE
    - Fetch products from Shopify
    - Apply all MVQueen curation
    - Update Shopify products + metafields + prices

This file uses:
- Phase 0 utilities
- Phase 1 brand brain
- Phase 2 metafields engine
- Phase 3 Shopify API engine
"""

import pandas as pd
import os

from mvqueen_engine.config import (
    CSV_CHUNK_SIZE,
    SHOPIFY_PROTECTED_COLUMNS,
    BRAND_NAME,
)

from mvqueen_engine.utils.text_utils import (
    strip_html,
    normalize_whitespace,
    enforce_brand,
)

from mvqueen_engine.utils.price_logic import calculate_compare_price

from mvqueen_engine.brand_brain.editorial import (
    generate_title,
    generate_description,
)

from mvqueen_engine.brand_brain.alt_text import generate_alt_text

from mvqueen_engine.metafields.metafield_engine import generate_metafields

from mvqueen_engine.shopify_api.shopify_client import (
    get_all_products,
    update_product,
    update_metafields,
    update_variant_price,
)


# ---------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------

def clean_text(text):
    """Strip HTML, normalize whitespace, enforce MVQueen brand."""
    text = strip_html(text)
    text = normalize_whitespace(text)
    text = enforce_brand(text)
    return text


# ---------------------------------------------
# MODE A — CSV PROCESSING
# ---------------------------------------------

def process_csv(input_path: str, output_path: str):
    """
    Loads supplier CSV, applies full MVQueen curation,
    and exports a new curated CSV.
    """

    df = pd.read_csv(input_path)

    # Ensure required columns exist
    if "Handle" not in df.columns:
        raise ValueError("CSV must contain a 'Handle' column.")

    # Create new columns for curated output
    df["Title"] = ""
    df["Body (HTML)"] = ""
    df["Tags"] = ""
    df["SEO Title"] = ""
    df["SEO Description"] = ""
    df["Alt Text"] = ""

    # Metafields will be exported as JSON string
    df["Metafields"] = ""

    for idx, row in df.iterrows():
        handle = str(row["Handle"]).strip()
        base_title = str(row.get("Title", "")).strip()
        supplier_body = str(row.get("Body (HTML)", "")).strip()

        # Clean supplier text
        supplier_body_clean = clean_text(supplier_body)

        # Generate curated content
        curated_title = generate_title(base_title, handle)
        curated_desc = generate_description(base_title, handle, supplier_body_clean)
        curated_alt = generate_alt_text(base_title, handle)
        curated_meta = generate_metafields(base_title, handle)

        # SEO
        seo_title = curated_title[:60]
        seo_desc = strip_html(curated_desc)[:155]

        # Price logic
        price = row.get("Variant Price", None)
        compare_at = calculate_compare_price(price) if price else None

        # Write back to DataFrame
        df.at[idx, "Title"] = curated_title
        df.at[idx, "Body (HTML)"] = curated_desc
        df.at[idx, "SEO Title"] = seo_title
        df.at[idx, "SEO Description"] = seo_desc
        df.at[idx, "Alt Text"] = curated_alt
        df.at[idx, "Metafields"] = str(curated_meta)

        # Tags (persona + keywords)
        df.at[idx, "Tags"] = f"mvqueen, curated, persona-{handle}"

        # Compare-at price
        if compare_at:
            df.at[idx, "Variant Compare At Price"] = compare_at

    # Export curated CSV
    df.to_csv(output_path, index=False)
    return output_path


# ---------------------------------------------
# MODE B — SHOPIFY PROCESSING (GRAPHQL + SAFE GATE)
# ---------------------------------------------

from mvqueen_engine.shopify_graphql_client import get_client


PRODUCTS_QUERY = """
query Products($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    nodes {
      id
      handle
      title
      descriptionHtml
      vendor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


PRODUCT_UPDATE_MUTATION = """
mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      title
      vendor
    }
    userErrors {
      field
      message
    }
  }
}
"""


def _assert_editorial_payload(payload):
    """Fail closed if a catalog workflow attempts to touch protected fields."""
    forbidden = set(payload) & set(SHOPIFY_PROTECTED_COLUMNS)
    if forbidden:
        raise ValueError(
            "Protected Shopify fields cannot be changed by catalog curation: "
            + ", ".join(sorted(forbidden))
        )


def process_shopify_catalog(*, dry_run=True, first=100):
    """
    Process Shopify catalog through the canonical GraphQL client.

    Safety rules:
    - dry_run=True by default.
    - No SKU, handle, inventory, variant configuration, pricing, or source-image
      fields are changed.
    - Only approved editorial product fields are candidates for mutation.
    - Shopify userErrors are surfaced by the GraphQL client.
    """
    client = get_client(dry_run=dry_run)

    products = client.query_all(
        PRODUCTS_QUERY,
        ("products",),
        first=first,
    )

    results = []
    for product in products:
        base_title = str(product.get("title", "")).strip()
        handle = str(product.get("handle", "")).strip()
        supplier_body = str(product.get("descriptionHtml", "")).strip()

        supplier_body_clean = clean_text(supplier_body)
        curated_title = generate_title(base_title, handle)
        curated_desc = generate_description(
            base_title, handle, supplier_body_clean
        )
        curated_meta = generate_metafields(base_title, handle)

        # ProductUpdateInput is intentionally limited to editorial fields.
        product_input = {
            "id": product["id"],
            "title": curated_title,
            "descriptionHtml": curated_desc,
            "vendor": BRAND_NAME,
        }
        _assert_editorial_payload(product_input)

        mutation_result = client.mutate(
            PRODUCT_UPDATE_MUTATION,
            {"product": product_input},
        )

        results.append({
            "id": product["id"],
            "handle": handle,
            "title": curated_title,
            "seo_title": curated_title[:60],
            "seo_description": strip_html(curated_desc)[:155],
            "metafields": curated_meta,
            "dry_run": bool(mutation_result.get("dry_run")),
        })

    return results
