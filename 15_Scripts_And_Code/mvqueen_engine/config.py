# mvqueen_engine/config.py
"""Central runtime configuration for the MVQueen engine.

The legacy engine_core expects MASTER_CONFIG. V1 keeps that contract explicit and
safe while allowing environment-specific Shopify credentials to remain external.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "mvqueen.myshopify.com")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-01")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "REPLACE_WITH_ENV_VAR")
SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

BRAND_NAME = "MVQueen"
CSV_CHUNK_SIZE = 15000
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

SHOPIFY_PROTECTED_COLUMNS = [
    "Handle", "Product ID", "Variant ID",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
    "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Requires Shipping", "Variant Taxable",
    "Image Position", "Gift Card", "Variant Weight Unit",
]

# Canonical production contract settings. Existing engines may read these values,
# but the production pipeline remains the authoritative publisher.
MASTER_CONFIG = {
    "brand_name": BRAND_NAME,
    "production": {
        "schema_version": "1.0",
        "seo_title_template": "MVQueen | {product_title}",
        "require_approved_publish_price": True,
        "allow_bulk_publish": False,
    },
    "blocks": {
        "personas": {"fallback_persona": "MVQueen Core"},
        "editorial": {"lengths": {"short": {}, "medium": {}, "long": {}}},
        "seo": {"keyword_pools": {"default": []}},
        "vocab": {"default_pools": {}},
        "metafields": {},
        "title": {"patterns": ["{base}"]},
    },
}
