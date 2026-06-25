from pathlib import Path
from datetime import datetime
import json

# Which environment is active?
ENV = "prod"  # "dev", "staging", "prod"

# Base directory for all engine operations
BASE_DIR = Path.cwd()

# Export directory for CSVs, logs, outputs
EXPORT_DIR = BASE_DIR / "MVQExports"
EXPORT_DIR.mkdir(exist_ok=True)

# Timestamp for file naming
DATE_STAMP = datetime.now().strftime("%Y-%m-%d")

# Full environment profiles
PROFILES = {
    "dev": {
        "DEBUG": True,
        "DRY_RUN": True,
        "SHOP_DOMAIN": "mvqueen-dev.myshopify.com",
        "API_VERSION": "2024-10",
        "ACCESS_TOKEN": "DEV_TOKEN_HERE",
        "LOG_LEVEL": "verbose",
        "ENABLE_RATE_LIMIT_LOGS": True,
    },
    "staging": {
        "DEBUG": True,
        "DRY_RUN": True,
        "SHOP_DOMAIN": "mvqueen-staging.myshopify.com",
        "API_VERSION": "2024-10",
        "ACCESS_TOKEN": "STAGING_TOKEN_HERE",
        "LOG_LEVEL": "info",
        "ENABLE_RATE_LIMIT_LOGS": True,
    },
    "prod": {
        "DEBUG": False,
        "DRY_RUN": False,
        "SHOP_DOMAIN": "mvqueen-2.myshopify.com",
        "API_VERSION": "2024-10",
        "ACCESS_TOKEN": "PROD_TOKEN_HERE",
        "LOG_LEVEL": "warning",
        "ENABLE_RATE_LIMIT_LOGS": False,
    },
}

# Active profile object
ACTIVE_PROFILE = PROFILES[ENV]
