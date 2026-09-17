"""MVQUEEN OS Shopify backend runtime.

Phase 1 intentionally exposes only safe health/status endpoints. Shopify reads
are optional and require environment credentials; write operations remain
protected by the existing GraphQL client's dry-run guard.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI


REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = REPO_ROOT / "15_Scripts_And_Code" / "mvqueen_engine"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))


app = FastAPI(
    title="MVQUEEN OS Shopify Backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "mvqueen-shopify-backend",
        "environment": os.getenv("MVQUEEN_ENV", "development"),
        "dry_run": os.getenv("SHOPIFY_DRY_RUN", "true").lower() == "true",
    }


@app.get("/api/shopify/status")
def shopify_status() -> dict[str, Any]:
    """Report configuration state without exposing credentials."""
    store = os.getenv("SHOPIFY_STORE_DOMAIN", "").strip()
    token_present = bool(os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip())
    api_version = os.getenv("SHOPIFY_API_VERSION", "2026-07")
    dry_run = os.getenv("SHOPIFY_DRY_RUN", "true").lower() == "true"

    return {
        "configured": bool(store and token_present),
        "store_domain": store or None,
        "api_version": api_version,
        "access_token_present": token_present,
        "dry_run": dry_run,
        "writes_enabled": not dry_run,
    }
