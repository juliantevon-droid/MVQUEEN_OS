"""CSV formatting helpers retained for read-only compatibility.

The historical text-to-product generator is retired because it could synthesize
operational commerce data. This module only formats already-governed product
records.
"""
from __future__ import annotations

import csv
import json


def flatten_metafields(metafields: dict) -> dict:
    flat = {}
    for key, value in (metafields or {}).items():
        if isinstance(value, list):
            value = json.dumps(value)
        flat[f"metafield.{key}"] = value
    return flat


def flatten_tags(tags: list) -> str:
    return ", ".join(sorted(tags or []))


def flatten_collections(collections: list) -> str:
    return ", ".join(sorted(collections or []))


def convert_to_csv_row(product: dict) -> dict:
    """Format an already-governed product dictionary; never invent values."""
    row = {
        "Title": product.get("title", ""),
        "Handle": product.get("handle", ""),
        "Body (HTML)": product.get("editorial_long", ""),
        "Tags": flatten_tags(product.get("tags", [])),
        "Collections": flatten_collections(product.get("collections", [])),
        "SEO Title": product.get("seo_primary", ""),
        "SEO Description": product.get("seo_secondary", ""),
        "Image Alt Text": product.get("alt_text_long", ""),
        "Category": product.get("category", ""),
        "Product Type": product.get("product_type", ""),
        "Persona": product.get("persona", ""),
        "Trend": product.get("trend", ""),
        "Season": product.get("season", ""),
        "Vibe": product.get("vibe", ""),
        "Material": product.get("material", ""),
        "Silhouette": product.get("silhouette", ""),
        "Detail": product.get("detail", ""),
        "input_text": product.get("input_text", ""),
        "seed": product.get("seed", ""),
    }
    row.update(flatten_metafields(product.get("metafields", {})))
    return row


def save_csv_from_texts(*args, **kwargs):
    raise RuntimeError(
        "Text-to-product generation is retired. Normalize verified Shopify CSV "
        "records through mvqueen_engine.catalog_processor.processor.process_csv()."
    )


def save_csv_from_products(products: list[dict], filename: str) -> str:
    rows = [convert_to_csv_row(product) for product in products]
    if not rows:
        raise ValueError("No governed product records supplied.")
    with open(filename, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return filename


__all__ = [
    "flatten_metafields",
    "flatten_tags",
    "flatten_collections",
    "convert_to_csv_row",
    "save_csv_from_products",
    "save_csv_from_texts",
]
