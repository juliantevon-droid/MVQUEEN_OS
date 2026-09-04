"""MVQueen enterprise release gate V1.

Publishing authorization is intentionally separate from product generation and QA.
This module is pure and does not perform Shopify writes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

APPROVED = "APPROVED_FOR_PUBLISH"
BLOCKED = "BLOCKED"


def canonical_fingerprint(record: Dict[str, Any]) -> str:
    """Return a stable SHA-256 fingerprint for a canonical product record."""
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def evaluate(record: Dict[str, Any], approval: Dict[str, Any] | None = None) -> Tuple[str, str]:
    """Evaluate whether a product has satisfied the operational publish gate."""
    if record.get("status") != "PRODUCTION_READY":
        return BLOCKED, "Product is not PRODUCTION_READY"
    qa = record.get("qa", {})
    if qa.get("passed") is not True or qa.get("errors"):
        return BLOCKED, "QA gate has not passed"
    price = record.get("pricing", {}).get("approved_publish_price")
    if price in (None, "", 0, "0", 0.0):
        return BLOCKED, "No approved_publish_price"
    if not approval:
        return BLOCKED, "Explicit publish approval is required"
    if approval.get("decision") != APPROVED:
        return BLOCKED, "Publish approval decision is not approved"
    expected = canonical_fingerprint(record)
    if approval.get("content_fingerprint") != expected:
        return BLOCKED, "Approval fingerprint does not match current product record"
    if not approval.get("actor"):
        return BLOCKED, "Approval actor is required"
    if not approval.get("timestamp"):
        return BLOCKED, "Approval timestamp is required"
    return APPROVED, "Release gate passed"


def create_approval(record: Dict[str, Any], actor: str, decision: str = APPROVED) -> Dict[str, Any]:
    """Create an auditable approval artifact without changing the product record."""
    if not actor.strip():
        raise ValueError("actor is required")
    return {
        "release_schema_version": "1.0",
        "product_id": record.get("identity", {}).get("product_id", ""),
        "schema_version": record.get("schema_version", ""),
        "content_fingerprint": canonical_fingerprint(record),
        "decision": decision,
        "actor": actor.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
