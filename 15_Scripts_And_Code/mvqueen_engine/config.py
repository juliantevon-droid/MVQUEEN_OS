# mvqueen_engine/config.py
"""Central runtime configuration for the MVQueen engine.

Credentials remain environment-only. Production publishing is governed by the
canonical release gate and publishing boundary.
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

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "tsucu0-1i.myshopify.com")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2026-07")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

BRAND_NAME = "MVQueen"
CANONICAL_BRAND = "MVQueen"
CSV_CHUNK_SIZE = 15000
MAX_PRODUCTS_PER_IMPORT_FILE = 850
REQUIRE_HEADER_ROW_PER_FILE = True
PRESERVE_SOURCE_COLUMN_ORDER = True
PRESERVE_VARIANT_AND_IMAGE_ROWS = True
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Fields that the editorial/catalog layer must never modify.
SHOPIFY_PROTECTED_COLUMNS = [
    "Handle", "Product ID", "ID", "Product GID",
    "Variant ID", "SKU", "Variant SKU", "Variant Barcode",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
    "Option3 Name", "Option3 Value",
    "Variant Price", "Variant Compare At Price",
    "Cost per item", "Variant Cost", "Variant Grams",
    "Inventory quantity", "Inventory policy", "Inventory tracker",
    "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service",
    "Variant Requires Shipping", "Variant Taxable", "Variant Weight Unit",
    "Image Src", "Image Position", "Image Width", "Image Height",
    "Image Variant ID", "Variant Image", "Gift Card", "Published", "Status", "Published At",
]

EDITORIAL_COLUMNS = [
    "Title", "Body (HTML)", "Vendor", "Product Type", "Tags",
    "SEO Title", "SEO Description", "Image Alt Text",
]

# Canonical compatibility aliases used by hardened catalog modules.
SHOPIFY_EDITORIAL_COLUMNS = EDITORIAL_COLUMNS
ONLY_EDIT_IMAGE_FIELD = "Image Alt Text"

# These are inspiration/reference names only; they are never canonical product brands.
INSPIRATION_BRANDS = (
    "Sephora", "Victoria's Secret", "Fenty Beauty", "Dior", "Miss.Princess",
)

MASTER_CONFIG = {
    "brand_name": BRAND_NAME,
    "canonical_brand": CANONICAL_BRAND,
    "production": {
        "schema_version": "1.1",
        "seo_title_template": "MVQueen | {product_title}",
        "require_approved_publish_price": True,
        "allow_bulk_publish": False,
        "shopify_store_domain": SHOPIFY_STORE_DOMAIN,
        "shopify_api_version": SHOPIFY_API_VERSION,
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
