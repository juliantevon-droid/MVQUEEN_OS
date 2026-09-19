"""MVQUEEN catalog approval boundary.

Converts an approved dry-run proposal into a strictly editorial Shopify
ProductUpdateInput. It never performs the mutation itself.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from .config import SHOPIFY_EDITORIAL_COLUMNS, SHOPIFY_PROTECTED_COLUMNS

WRITE_FIELDS = {
    "Title": "title",
    "Body HTML": "descriptionHtml",
    "Product Type": "productType",
    "Tags": "tags",
    "SEO Title": "seo.title",
    "SEO Description": "seo.description",
}

def build_product_update_input(
    dry_run_result: Dict[str, Any],
    *,
    approved: bool = False,
) -> Dict[str, Any]:
    """Build a mutation input only after explicit approval."""
    if not approved:
        raise PermissionError("Explicit catalog approval is required before building a write payload.")

    if dry_run_result.get("status") not in {"PASS", "REVIEW"}:
        raise ValueError("Only PASS or explicitly reviewed REVIEW results may be approved.")

    if dry_run_result.get("write_performed"):
        raise ValueError("Dry-run result is already marked as written.")

    product_id = dry_run_result.get("product_id")
    if not product_id:
        raise ValueError("Missing Shopify product ID.")

    proposed = dry_run_result.get("proposed") or {}
    payload: Dict[str, Any] = {"id": product_id}

    for source_field, target_path in WRITE_FIELDS.items():
        if source_field not in proposed:
            continue
        value = proposed[source_field]
        if target_path == "seo.title":
            payload.setdefault("seo", {})["title"] = value
        elif target_path == "seo.description":
            payload.setdefault("seo", {})["description"] = value
        elif target_path == "tags":
            if isinstance(value, str):
                payload["tags"] = [x.strip() for x in value.split(",") if x.strip()]
            elif isinstance(value, list):
                payload["tags"] = [str(x).strip() for x in value if str(x).strip()]
            else:
                raise ValueError("Tags must be a string or list.")
        else:
            payload[target_path] = value

    for protected in SHOPIFY_PROTECTED_COLUMNS:
        if protected in payload:
            raise ValueError(f"Protected field leaked into mutation payload: {protected}")

    allowed = {"id", "title", "descriptionHtml", "productType", "tags", "seo"}
    unexpected = set(payload) - allowed
    if unexpected:
        raise ValueError(f"Unexpected mutation fields: {sorted(unexpected)}")

    if "seo" in payload:
        seo_keys = set(payload["seo"])
        allowed_seo = {"title", "description"}
        if not seo_keys <= allowed_seo:
            raise ValueError(f"Unexpected SEO fields: {sorted(seo_keys - allowed_seo)}")

    return deepcopy(payload)

def approval_manifest(dry_run_result: Dict[str, Any]) -> Dict[str, Any]:
    """Return a review manifest without creating a write payload."""
    return {
        "mode": "approval-required",
        "product_id": dry_run_result.get("product_id"),
        "handle": dry_run_result.get("handle"),
        "status": dry_run_result.get("status"),
        "changed_fields": dry_run_result.get("changed_fields", []),
        "flags": dry_run_result.get("flags", []),
        "write_performed": False,
        "protected_fields": list(SHOPIFY_PROTECTED_COLUMNS),
        "editorial_fields": list(SHOPIFY_EDITORIAL_COLUMNS),
        "approval_required": True,
    }
