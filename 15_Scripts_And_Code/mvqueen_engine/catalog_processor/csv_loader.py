# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — UNIFIED CSV EXPORTER (BLOCK I)
# ---------------------------------------------------------

import csv
import json
from mvqueen_engine.catalog_processor.processor import process_product

# ---------------------------------------------------------
# FLATTEN METAFIELDS
# ---------------------------------------------------------

def flatten_metafields(metafields: dict) -> dict:
    """
    Shopify metafields must be flattened into:
    metafield.<key> = <value>
    Lists must be JSON-encoded.
    """
    flat = {}
    for key, value in metafields.items():
        if isinstance(value, list):
            value = json.dumps(value)
        flat[f"metafield.{key}"] = value
    return flat

# ---------------------------------------------------------
# FLATTEN TAGS + COLLECTIONS
# ---------------------------------------------------------

def flatten_tags(tags: list) -> str:
    return ", ".join(sorted(tags))

def flatten_collections(collections: list) -> str:
    return ", ".join(sorted(collections))

# ---------------------------------------------------------
# CONVERT PRODUCT DICTIONARY TO SHOPIFY CSV ROW
# ---------------------------------------------------------

def convert_to_csv_row(product: dict) -> dict:
    """
    Converts the unified Omniluxe product dictionary into a
    Shopify-ready CSV row with deterministic column ordering.
    """

    row = {
        # Core Shopify fields
        "Title": product.get("title", ""),
        "Handle": product.get("handle", ""),
        "Body (HTML)": product.get("editorial_long", ""),
        "Tags": flatten_tags(product.get("tags", [])),
        "Collections": flatten_collections(product.get("collections", [])),

        # SEO
        "SEO Title": product.get("seo_primary", ""),
        "SEO Description": product.get("seo_secondary", ""),

        # Alt Text
        "Image Alt Text": product.get("alt_text_long", ""),

        # Detection fields
        "Category": product.get("category", ""),
        "Product Type": product.get("product_type", ""),
        "Persona": product.get("persona", ""),
        "Trend": product.get("trend", ""),
        "Season": product.get("season", ""),
        "Vibe": product.get("vibe", ""),
        "Material": product.get("material", ""),
        "Silhouette": product.get("silhouette", ""),
        "Detail": product.get("detail", ""),

        # Omniluxe extras
        "input_text": product.get("input_text", ""),
        "seed": product.get("seed", ""),
    }

    # Add metafields
    row.update(flatten_metafields(product.get("metafields", {})))

    return row

# ---------------------------------------------------------
# BATCH CSV EXPORT
# ---------------------------------------------------------

def save_csv_from_texts(texts: list, filename: str = "mvqueen_output.csv"):
    rows = [convert_to_csv_row(process_product(t)) for t in texts]

    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)