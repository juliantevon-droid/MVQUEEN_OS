"""Enterprise release gate V1.

This module deliberately does not publish to Shopify. It evaluates a canonical
product record and produces a separate operational release decision.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

ALLOWED_PUBLISH_STATUS = "PRODUCTION_READY"


def canonical_json(record: Dict[str, Any]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_fingerprint(record: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(record).encode("utf-8")).hexdigest()


def evaluate_release(record: Dict[str, Any], approval: Dict[str, Any] | None = None) -> Tuple[bool, Dict[str, Any]]:
    qa = record.get("qa", {})
    pricing = record.get("pricing", {})
    identity = record.get("identity", {})
    errors = list(qa.get("errors", [])) if isinstance(qa.get("errors", []), list) else ["qa.errors must be a list"]
    reasons = []

    if record.get("status") != ALLOWED_PUBLISH_STATUS:
        reasons.append("Product record is not PRODUCTION_READY")
    if qa.get("passed") is not True:
        reasons.append("QA has not passed")
    if not pricing.get("approved_publish_price"):
        reasons.append("No approved_publish_price")
    if errors:
        reasons.append("QA contains blocking errors")
    if not identity.get("product_id"):
        reasons.append("Missing identity.product_id")

    approved = False
    if approval:
        approved = (
            approval.get("decision") == "APPROVED_FOR_PUBLISH"
            and bool(approval.get("approved_by"))
            and approval.get("fingerprint") == content_fingerprint(record)
        )
    if not approved:
        reasons.append("Explicit publish approval is missing or does not match the current content fingerprint")

    releasable = not reasons
    decision = {
        "release_schema_version": "1.0",
        "product_id": identity.get("product_id", ""),
        "fingerprint": content_fingerprint(record),
        "decision": "APPROVED_FOR_PUBLISH" if releasable else "HOLD",
        "reasons": reasons,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }
    return releasable, decision


def make_approval(record: Dict[str, Any], approved_by: str) -> Dict[str, Any]:
    """Create the data an external approval workflow can sign/store.

    This function does not authorize publication by itself; a separate actor or
    controlled workflow must make the approval decision.
    """
    return {
        "release_schema_version": "1.0",
        "product_id": record.get("identity", {}).get("product_id", ""),
        "fingerprint": content_fingerprint(record),
        "decision": "APPROVED_FOR_PUBLISH",
        "approved_by": approved_by,
    }


if __name__ == "__main__":
    import sys
    payload = json.load(sys.stdin)
    ok, result = evaluate_release(payload.get("record", {}), payload.get("approval"))
    result["releasable"] = ok
    print(json.dumps(result, indent=2, ensure_ascii=False))
