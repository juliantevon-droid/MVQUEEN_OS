"""MVQUEEN OS engine configuration."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "").strip()
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2026-07").strip()
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_BASE_URL = (
    f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"
    if SHOPIFY_STORE_DOMAIN else ""
)

BRAND_NAME = "MVQueen"
CSV_CHUNK_SIZE = 15000

# Catalog is unlimited. 850 is only the maximum product count per import batch/file.
MAX_PRODUCTS_PER_IMPORT_FILE = 850
PRESERVE_SOURCE_COLUMN_ORDER = True
ONLY_EDIT_IMAGE_FIELD = "Image Alt Text"
SHOPIFY_EDITORIAL_COLUMNS = [
    "Title", "Body HTML", "Product Type", "Tags",
    "Image Alt Text", "SEO Title", "SEO Description",
]
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

SHOPIFY_PROTECTED_COLUMNS = [
    "Handle", "Product ID", "Variant ID", "SKU", "Barcode",
    "Inventory", "Inventory Qty",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
    "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Requires Shipping",
    "Variant Taxable", "Image Src", "Image Position", "Gift Card",
    "Variant Weight Unit",
]
