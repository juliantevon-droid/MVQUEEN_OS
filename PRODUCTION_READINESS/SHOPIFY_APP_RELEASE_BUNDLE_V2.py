"""Build the exact approved release envelope consumed by the Shopify app.

The canonical_record_json string preserves Python's canonical serialization
byte-for-byte so the React/Node publisher can verify the exact fingerprint
without cross-language number-format ambiguity.
"""
from __future__ import annotations

import json
from typing import Any, Dict

try:
    from .RELEASE_GATE_V1 import APPROVED, canonical_fingerprint, evaluate
except ImportError:
    from RELEASE_GATE_V1 import APPROVED, canonical_fingerprint, evaluate


def canonical_record_json(record: Dict[str, Any]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def build_bundle(record: Dict[str, Any], approval: Dict[str, Any]) -> Dict[str, Any]:
    decision, reason = evaluate(record, approval)
    if decision != APPROVED:
        raise ValueError(f"Release bundle blocked: {reason}")

    payload = canonical_record_json(record)
    expected = canonical_fingerprint(record)
    if approval.get("content_fingerprint") != expected:
        raise ValueError("Approval fingerprint mismatch")

    return {
        "record": record,
        "approval": approval,
        "canonical_record_json": payload,
    }


__all__ = ["build_bundle", "canonical_record_json"]
