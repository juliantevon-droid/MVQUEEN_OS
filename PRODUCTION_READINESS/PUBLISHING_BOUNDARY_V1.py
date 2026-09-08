"""MVQUEEN controlled publishing boundary V1.

This module is the only approved hand-off from a canonical product record to an
external publisher. It performs no Shopify/API work itself; the side effect is
injected as a publisher callable so authorization remains independently testable.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, Tuple

try:
    from .RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate
except ImportError:
    from RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate

PUBLISHED = "PUBLISHED"

Publisher = Callable[[Dict[str, Any]], Any]


def publish(
    record: Dict[str, Any],
    approval: Dict[str, Any] | None,
    publisher: Publisher,
) -> Tuple[str, Dict[str, Any]]:
    """Authorize and hand off a canonical record to an injected publisher.

    The boundary is fail-closed: a blocked release never invokes ``publisher``.
    A deep copy is handed to the publisher so the canonical record owned by the
    pipeline cannot be mutated by an external side effect.
    """
    if not callable(publisher):
        raise TypeError("publisher must be callable")

    decision, reason = evaluate(record, approval)
    product_id = record.get("identity", {}).get("product_id", "")
    fingerprint = canonical_fingerprint(record)

    if decision != APPROVED:
        return BLOCKED, {
            "product_id": product_id,
            "content_fingerprint": fingerprint,
            "decision": decision,
            "reason": reason,
        }

    publish_result = publisher(deepcopy(record))
    return PUBLISHED, {
        "product_id": product_id,
        "content_fingerprint": fingerprint,
        "decision": APPROVED,
        "reason": "Release gate passed; publisher invoked",
        "publisher_result": publish_result,
    }


__all__ = ["BLOCKED", "PUBLISHED", "publish"]
