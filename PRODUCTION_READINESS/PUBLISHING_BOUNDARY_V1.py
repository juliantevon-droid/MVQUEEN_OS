"""MVQUEEN controlled publishing boundary V1.

This module is the only approved hand-off from a canonical product record to an
external publisher. It performs no Shopify/API work itself; the side effect is
injected as a publisher callable so authorization remains independently testable.

An optional caller-owned idempotency store can prevent duplicate publication of
the same approved product fingerprint. A durable implementation should back
that store with the system's persistent audit/ledger layer.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, MutableMapping, Tuple

try:
    from .RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate
except ImportError:
    from RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate

PUBLISHED = "PUBLISHED"
ALREADY_PUBLISHED = "ALREADY_PUBLISHED"

Publisher = Callable[[Dict[str, Any]], Any]


def idempotency_key(record: Dict[str, Any]) -> str:
    """Return the stable key for one canonical product content version."""
    product_id = record.get("identity", {}).get("product_id", "")
    return f"UPDATE_PRODUCT_EDITORIAL:{product_id}:{canonical_fingerprint(record)}"


def publish(
    record: Dict[str, Any],
    approval: Dict[str, Any] | None,
    publisher: Publisher,
    idempotency_store: MutableMapping[str, Dict[str, Any]] | None = None,
) -> Tuple[str, Dict[str, Any]]:
    """Authorize and hand off a canonical record to an injected publisher.

    The boundary is fail-closed: a blocked release never invokes ``publisher``.
    When ``idempotency_store`` is supplied, a successful prior publication for
    the exact product fingerprint is returned without invoking the publisher a
    second time. The store is caller-owned so production can use a durable
    ledger while tests can use an in-memory dictionary.
    """
    if not callable(publisher):
        raise TypeError("publisher must be callable")

    decision, reason = evaluate(record, approval)
    product_id = record.get("identity", {}).get("product_id", "")
    fingerprint = canonical_fingerprint(record)
    key = idempotency_key(record)

    if decision != APPROVED:
        return BLOCKED, {
            "product_id": product_id,
            "content_fingerprint": fingerprint,
            "idempotency_key": key,
            "decision": decision,
            "reason": reason,
        }

    if idempotency_store is not None and key in idempotency_store:
        prior = deepcopy(idempotency_store[key])
        return ALREADY_PUBLISHED, {
            **prior,
            "idempotency_key": key,
            "reason": "Exact approved product fingerprint was already published",
        }

    publish_result = publisher(deepcopy(record))
    audit = {
        "product_id": product_id,
        "content_fingerprint": fingerprint,
        "idempotency_key": key,
        "decision": APPROVED,
        "reason": "Release gate passed; publisher invoked",
        "publisher_result": publish_result,
    }

    if idempotency_store is not None:
        idempotency_store[key] = deepcopy(audit)

    return PUBLISHED, audit


__all__ = ["ALREADY_PUBLISHED", "BLOCKED", "PUBLISHED", "idempotency_key", "publish"]
