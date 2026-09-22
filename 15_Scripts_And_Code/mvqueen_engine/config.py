# mvqueen_engine/config.py
"""
MVQUEEN OS — GLOBAL CONFIGURATION

Production catalog safety is fail-closed. Copy/SEO/merchandising workflows may
write only approved editorial fields. Operational Shopify identity, inventory,
variant, pricing, and source-image fields are protected unless a dedicated,
explicit migration workflow says otherwise.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# -----------------------------
# SHOPIFY CONFIG
# -----------------------------
SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "tsucu0-1i.myshopify.com")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2026-07")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

# -----------------------------
# BRAND / ENGINE SETTINGS
# -----------------------------
BRAND_NAME = "MVQueen"
CSV_CHUNK_SIZE = 15000
MAX_PRODUCTS_PER_IMPORT_FILE = 850
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# -----------------------------
# PRODUCTION SAFETY
# -----------------------------
# These fields are immutable during ordinary catalog curation.
# Image Alt Text is intentionally NOT protected because it is an approved
# editorial field for optimization.
SHOPIFY_PROTECTED_COLUMNS = [
    # Product identity
    "Handle", "Product ID", "ID", "Product GID",
    # Variant identity
    "Variant ID", "Variant SKU", "Variant Barcode",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
    "Option3 Name", "Option3 Value",
    # Pricing / commercial source data
    "Variant Price", "Variant Compare At Price",
    "Cost per item", "Variant Cost",
    # Inventory / fulfillment
    "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service",
    "Variant Requires Shipping", "Variant Taxable", "Variant Weight Unit",
    # Source image structure — URLs/position/identity must remain intact.
    "Image Src", "Image Position", "Image Width", "Image Height",
    "Image Variant ID",
    # Store operational state
    "Gift Card", "Published", "Status", "Published At",
]

# Explicitly editable editorial fields. The pipeline should reject writes to
# unknown operational fields rather than guessing.
SHOPIFY_EDITORIAL_COLUMNS = [
    "Title", "Body (HTML)", "Vendor", "Product Type", "Tags",
    "SEO Title", "SEO Description", "Image Alt Text",
]

# Vendor is normalized to MVQueen by policy. Inspiration brands such as
# Sephora, Victoria's Secret, Fenty Beauty, Dior, and Miss. Queen are never
# emitted as the product brand.
CANONICAL_BRAND = "MVQueen"
INSPIRATION_BRANDS = (
    "Sephora", "Victoria's Secret", "Fenty Beauty", "Dior", "Miss. Queen"
)

# Product import/export policy.
MAX_PRODUCTS_PER_IMPORT_FILE = 850
REQUIRE_HEADER_ROW_PER_FILE = True
PRESERVE_SOURCE_COLUMN_ORDER = True
PRESERVE_VARIANT_AND_IMAGE_ROWS = True
ONLY_EDIT_IMAGE_FIELD = "Image Alt Text"
