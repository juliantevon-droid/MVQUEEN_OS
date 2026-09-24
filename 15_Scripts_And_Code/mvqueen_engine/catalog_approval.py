"""MVQueen catalog approval boundary.

Consolidated from pre-production branch logic and adapted to the canonical
main-branch field policy. This module builds an editorial-only Shopify
ProductUpdateInput after explicit approval. It never performs network I/O.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from .config import SHOPIFY_PROTECTED_COLUMNS

WRITE_FIELDS = {
    "Title": "title",
    "Body (HTML)": "descriptionHtml",
    "Product Type": "productType",
    "Tags": "tags",
    "SEO Title": "seo.title",
    "SEO Description": "seo.description",
}
ALLOWED_TOP_LEVEL = {"id", "title", "descriptionHtml", "productType", "tags", "seo"}
ALLOWED_SEO = {"title", "description"}


def _normalise_tags(value: Any) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    raise ValueError("Tags must be a string or sequence.")


def build_product_update_input(
    dry_run_result: Dict[str, Any],
    *,
    approved: bool = False,
) -> Dict[str, Any]:
    """Return an editorial-only ProductUpdateInput after explicit approval."""
    if not approved:
        raise PermissionError("Explicit catalog approval is required.")

    status = str(dry_run_result.get("status") or "").upper()
    if status not in {"PASS", "REVIEW"}:
        raise ValueError("Only PASS or explicitly reviewed REVIEW results may be approved.")

    findings = dry_run_result.get("findings") or []
    if any(
        str(item.get("severity", "")).upper() == "ERROR"
        for item in findings
        if isinstance(item, dict)
    ):
        raise ValueError("Dry-run contains blocking findings.")

    if dry_run_result.get("write_performed"):
        raise ValueError("Dry-run result is already marked as written.")

    product_id = dry_run_result.get("product_id")
    if not product_id:
        raise ValueError("Missing Shopify product GID.")

    before = dry_run_result.get("before") or {}
    proposed = dry_run_result.get("proposed") or {}

    for field in SHOPIFY_PROTECTED_COLUMNS:
        if field in before and proposed.get(field) != before.get(field):
            raise ValueError(f"Protected field changed before approval: {field}")

    payload: Dict[str, Any] = {"id": product_id}
    changed_fields = set(dry_run_result.get("changed_fields") or [])

    for source_field, target_path in WRITE_FIELDS.items():
        if changed_fields and source_field not in changed_fields:
            continue
        if source_field not in proposed:
            continue

        value = proposed[source_field]
        if target_path == "seo.title":
            payload.setdefault("seo", {})["title"] = value
        elif target_path == "seo.description":
            payload.setdefault("seo", {})["description"] = value
        elif target_path == "tags":
            payload["tags"] = _normalise_tags(value)
        else:
            payload[target_path] = value

    unexpected = set(payload) - ALLOWED_TOP_LEVEL
    if unexpected:
        raise ValueError(f"Unexpected mutation fields: {sorted(unexpected)}")

    if "seo" in payload:
        unexpected_seo = set(payload["seo"]) - ALLOWED_SEO
        if unexpected_seo:
            raise ValueError(f"Unexpected SEO fields: {sorted(unexpected_seo)}")

    return deepcopy(payload)


def approval_manifest(dry_run_result: Dict[str, Any]) -> Dict[str, Any]:
    """Return a review manifest without creating or sending a mutation."""
    return {
        "mode": "approval-required",
        "product_id": dry_run_result.get("product_id"),
        "handle": dry_run_result.get("handle"),
        "status": dry_run_result.get("status"),
        "changed_fields": list(dry_run_result.get("changed_fields") or []),
        "findings": list(dry_run_result.get("findings") or []),
        "write_performed": False,
        "protected_fields": list(SHOPIFY_PROTECTED_COLUMNS),
        "approval_required": True,
    }
