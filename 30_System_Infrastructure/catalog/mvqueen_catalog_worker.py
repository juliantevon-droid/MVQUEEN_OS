#!/usr/bin/env python3
"""MVQUEEN catalog governance worker.

Input: JSONL records containing verified facts and an optimized product payload.
Default behavior is validation/dry-run. Shopify writes require explicit
MVQ_WRITE_ENABLED=true plus Shopify Admin credentials in the environment.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

FORBIDDEN = ["MISS.QUEEN", "MISS. QUEEN", "OUHOE", "HOEGOA", "FANZHEN", "EELHOPE", "COLOR FIT", "WEST & MONTH"]
PROTECTED = {"handle", "sku", "inventory", "variants", "variant", "images", "image", "vendor"}
REQUIRED_FACTS = {"title", "description_html", "seo_title", "seo_description"}
ENDPOINT = "https://{}/admin/api/2026-07/graphql.json"


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate_record(record: dict, line: int) -> dict:
    if not isinstance(record, dict):
        fail(f"line {line}: record must be an object")
    pid = record.get("id")
    if not pid:
        fail(f"line {line}: missing Shopify product id")
    if not record.get("verified_facts"):
        fail(f"line {line}: HOLD — verified_facts is required")
    content = record.get("optimized", {})
    missing = REQUIRED_FACTS - set(content)
    if missing:
        fail(f"line {line}: HOLD — missing optimized fields: {sorted(missing)}")
    blob = json.dumps(content, ensure_ascii=False).upper()
    for brand in FORBIDDEN:
        if brand in blob:
            fail(f"line {line}: forbidden supplier/legacy brand found: {brand}")
    protected = set(record.get("protected_changes", [])) & PROTECTED
    if protected:
        fail(f"line {line}: protected field change requested: {sorted(protected)}")
    if not isinstance(content.get("tags", []), list):
        fail(f"line {line}: tags must be a list")
    return {"id": pid, **content}


def shopify_update(store: str, token: str, payload: dict) -> dict:
    mutation = """
    mutation MVQProductUpdate($product: ProductUpdateInput!) {
      productUpdate(product: $product) {
        product { id title updatedAt }
        userErrors { field message code }
      }
    }
    """
    product = {
        "id": payload["id"],
        "title": payload["title"],
        "descriptionHtml": payload["description_html"],
        "seo": {"title": payload["seo_title"], "description": payload["seo_description"]},
    }
    if "product_type" in payload:
        product["productType"] = payload["product_type"]
    if "tags" in payload:
        product["tags"] = payload["tags"]
    if "category_id" in payload:
        product["category"] = payload["category_id"]
    body = json.dumps({"query": mutation, "variables": {"product": product}}).encode()
    req = urllib.request.Request(
        ENDPOINT.format(store), data=body,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Shopify HTTP {exc.code}") from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"]))
    result = data["data"]["productUpdate"]
    if result["userErrors"]:
        raise RuntimeError(json.dumps(result["userErrors"]))
    return result["product"]


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("12_Content_Assets/drive_inbox/catalog_ready.jsonl")
    if not source.exists():
        print(f"No catalog input found: {source}")
        return 0
    records = []
    for n, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        records.append(validate_record(json.loads(raw), n))
    write_enabled = os.getenv("MVQ_WRITE_ENABLED", "false").lower() == "true"
    store = os.getenv("SHOPIFY_STORE")
    token = os.getenv("SHOPIFY_ADMIN_TOKEN")
    if write_enabled and (not store or not token):
        print("WRITE GATE: FAIL — credentials missing")
        return 1
    if not write_enabled:
        print(f"DRY RUN: validated {len(records)} PRODUCTION_READY candidate(s); Shopify writes disabled.")
        return 0
    for payload in records:
        result = shopify_update(store, token, payload)
        print(f"UPDATED {result['id']} — {result['title']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CATALOG PIPELINE: HOLD/FAIL — {exc}")
        raise SystemExit(1)
