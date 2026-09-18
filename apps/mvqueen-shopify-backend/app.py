from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "15_Scripts_And_Code" / "mvqueen_engine"
BACKEND = ROOT / "apps" / "mvqueen-shopify-backend"

for path in (ENGINE, BACKEND):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from catalog_service import preview_products
from shopify_auth import auth_status, get_authenticated_client
from webhook_security import DeliveryDeduplicator, verify_shopify_hmac
from audit import audit_log

app = FastAPI(title="MVQUEEN OS Shopify Backend", version="0.5.0")
webhook_deduplicator = DeliveryDeduplicator()


@app.get("/health")
def health() -> dict:
    audit_log.record("health_check", dry_run=True)
    return {
        "status": "ok",
        "service": "mvqueen-shopify-backend",
        "environment": os.getenv("MVQUEEN_ENV", "development"),
        "dry_run": os.getenv("SHOPIFY_DRY_RUN", "true").lower() == "true",
    }


@app.get("/api/shopify/status")
def shopify_status() -> dict:
    try:
        client = get_authenticated_client(dry_run=True)
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


@app.get("/api/shopify/auth-status")
def shopify_auth_status() -> dict:
    """Expose configuration state without exposing credentials or tokens."""
    status = auth_status()
    audit_log.record("auth_status_check", dry_run=True)
    return {
        "configured": status["configured"],
        "authenticated": status["authenticated"],
        "token_cached": status["authenticated"],
    }


@app.post("/webhooks/products-update")
async def products_update_webhook(request: Request) -> JSONResponse:
    raw_body = await request.body()
    provided_hmac = request.headers.get("X-Shopify-Hmac-Sha256")
    if not verify_shopify_hmac(raw_body, provided_hmac):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    delivery_id = request.headers.get("X-Shopify-Webhook-Id")
    if webhook_deduplicator.seen(delivery_id):
        return JSONResponse({"status": "duplicate_ignored"})

    audit_log.record("webhook_received", shop_domain=request.headers.get("X-Shopify-Shop-Domain"), dry_run=True, details={"topic": request.headers.get("X-Shopify-Topic"), "delivery_id": delivery_id})
    return JSONResponse({
        "topic": request.headers.get("X-Shopify-Topic"),
        "shop": request.headers.get("X-Shopify-Shop-Domain"),
        "delivery_id": delivery_id,
    })


@app.get("/api/audit/recent")
def recent_audit(limit: int = Query(default=50, ge=1, le=200)) -> dict:
    return {"events": audit_log.recent(limit)}


@app.get("/api/shopify/products/preview")
def products_preview(
    first: int = Query(default=25, ge=1, le=50),
) -> dict:
    try:
        client = get_authenticated_client(dry_run=True)
        result = preview_products(client, first=first)
        return {
            "status": "connected",
            **result,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "error": str(exc)},
        ) from exc
