# mvqueen_engine/catalog_processor/processor.py
"""
LEGACY CATALOG PROCESSOR

CSV MODE remains available for offline transformation. The former Shopify live
mode is intentionally disabled on the enterprise production branch because it
could bypass the canonical production pipeline, QA gate, release fingerprint,
and explicit approval gate.

Production publishing must use:
Canonical Product → QA → Release Gate → Publishing Boundary → Publisher
"""

import pandas as pd

from mvqueen_engine.config import CSV_CHUNK_SIZE, SHOPIFY_PROTECTED_COLUMNS, BRAND_NAME
from mvqueen_engine.utils.text_utils import strip_html, normalize_whitespace, enforce_brand
from mvqueen_engine.utils.price_logic import calculate_compare_price
from mvqueen_engine.brand_brain.editorial import generate_title, generate_description
from mvqueen_engine.brand_brain.alt_text import generate_alt_text
from mvqueen_engine.metafields.metafield_engine import generate_metafields


def clean_text(text):
    """Strip HTML, normalize whitespace, and enforce the MVQueen brand."""
    text = strip_html(text)
    text = normalize_whitespace(text)
    return enforce_brand(text)


def process_csv(input_path: str, output_path: str):
    """Load supplier CSV, apply legacy offline curation, and export CSV."""
    df = pd.read_csv(input_path)

    if "Handle" not in df.columns:
        raise ValueError("CSV must contain a 'Handle' column.")

    df["Title"] = ""
    df["Body (HTML)"] = ""
    df["Tags"] = ""
    df["SEO Title"] = ""
    df["SEO Description"] = ""
    df["Alt Text"] = ""
    df["Metafields"] = ""

    for idx, row in df.iterrows():
        handle = str(row["Handle"]).strip()
        base_title = str(row.get("Title", "")).strip()
        supplier_body = str(row.get("Body (HTML)", "")).strip()
        supplier_body_clean = clean_text(supplier_body)

        curated_title = generate_title(base_title, handle)
        curated_desc = generate_description(base_title, handle, supplier_body_clean)
        curated_alt = generate_alt_text(base_title, handle)
        curated_meta = generate_metafields(base_title, handle)

        seo_title = curated_title[:60]
        seo_desc = strip_html(curated_desc)[:155]

        df.at[idx, "Title"] = curated_title
        df.at[idx, "Body (HTML)"] = curated_desc
        df.at[idx, "SEO Title"] = seo_title
        df.at[idx, "SEO Description"] = seo_desc
        df.at[idx, "Alt Text"] = curated_alt
        df.at[idx, "Metafields"] = str(curated_meta)
        df.at[idx, "Tags"] = f"mvqueen, curated, persona-{handle}"

        price = row.get("Variant Price", None)
        compare_at = calculate_compare_price(price) if price else None
        if compare_at:
            df.at[idx, "Variant Compare At Price"] = compare_at

    df.to_csv(output_path, index=False)
    return output_path


def process_shopify_catalog(*args, **kwargs):
    """Fail closed: legacy direct Shopify publishing is prohibited."""
    raise RuntimeError(
        "Direct Shopify catalog processing is disabled on the enterprise branch. "
        "Use the canonical production pipeline, release gate, publishing boundary, "
        "and dedicated publisher adapter."
    )


__all__ = ["clean_text", "process_csv", "process_shopify_catalog"]
