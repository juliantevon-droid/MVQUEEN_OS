from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "15_Scripts_And_Code" / "mvqueen_engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from shopify_graphql_client import get_client

app = FastAPI(title="MVQUEEN OS Shopify Backend", version="0.2.0")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "mvqueen-shopify-backend",
        "environment": os.getenv("MVQUEEN_ENV", "development"),
        "dry_run": os.getenv("SHOPIFY_DRY_RUN", "true").lower() == "true",
    }


@app.get("/api/shopify/status")
def shopify_status() -> dict:
    try:
        client = get_client(dry_run=True)
        body = client.execute(
            "query MVQueenShopStatus { shop { id name myshopifyDomain currencyCode } }"
        )
        shop = (body.get("data") or {}).get("shop")
        if not shop:
            raise RuntimeError("Shopify returned no shop data")
        return {
            "status": "connected",
            "shop": shop,
            "api_version": client.api_version,
            "dry_run": client.dry_run,
            "read_only": True,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "disconnected", "error": str(exc)},
        ) from exc


@app.get("/api/shopify/products/preview")
def products_preview(
    first: int = Query(default=10, ge=1, le=50),
) -> dict:
    try:
        client = get_client(dry_run=True)
        body = client.execute(
            """
            query MVQueenProductsPreview($first: Int!) {
              products(first: $first) {
                nodes {
                  id
                  title
                  handle
                  status
                  updatedAt
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
            """,
            {"first": first},
        )
        products = (body.get("data") or {}).get("products")
        if products is None:
            raise RuntimeError("Shopify returned no product connection")
        return {
            "status": "connected",
            "count_returned": len(products["nodes"]),
            "products": products["nodes"],
            "page_info": products["pageInfo"],
            "read_only": True,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "error": str(exc)},
        ) from exc
