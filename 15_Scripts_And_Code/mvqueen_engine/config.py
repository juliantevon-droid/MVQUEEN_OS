# mvqueen_engine/config.py
"""
PHASE 0 — CONFIG

Global configuration for MVQueen Engine:
- Shopify API settings (via environment variables)
- General engine settings
- Safety toggles
"""

import os
from pathlib import Path

# Try to load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Look for .env in the parent directory of this file (15_Scripts_And_Code)
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# -----------------------------
# SHOPIFY CONFIG
# -----------------------------

# Use environment variables with fallbacks to placeholders for safety
SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "mvqueen.myshopify.com")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-01")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "REPLACE_WITH_ENV_VAR")

SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

# -----------------------------
# ENGINE SETTINGS
# -----------------------------

BRAND_NAME = "MVQueen"

# Max rows per CSV chunk when exporting
CSV_CHUNK_SIZE = 15000

# Whether to log debug info to console
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# -----------------------------
# SAFETY / PROTECTION
# -----------------------------

# Columns we NEVER touch in CSV workflows
SHOPIFY_PROTECTED_COLUMNS = [
    "Handle","Product ID","Variant ID",
    "Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value",
    "Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty",
    "Variant Inventory Policy","Variant Fulfillment Service","Variant Requires Shipping",
    "Variant Taxable","Image Position","Gift Card","Variant Weight Unit"
]
