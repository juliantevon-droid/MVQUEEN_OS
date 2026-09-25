"""MVQueen controlled publishing boundary V1.

This module is the only approved hand-off from a canonical product record to an
external publisher. It performs no Shopify/API work itself; the side effect is
injected as a publisher callable so authorization remains independently testable.

An optional caller-owned idempotency store prevents duplicate publication of the
same approved product fingerprint. An optional ledger path records release and
publishing outcomes in the durable JSONL audit ledger.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, MutableMapping, Tuple

try:
    from .RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate
    from .RELEASE_AUDIT_LEDGER_V1 import append_entry, build_entry
except ImportError:
    from RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate
    from RELEASE_AUDIT_LEDGER_V1 import append_entry, build_entry

PUBLISHED = "PUBLISHED"
ALREADY_PUBLISHED = "ALREADY_PUBLISHED"

Publisher = Callable[[Dict[str, Any]], Any]


def idempotency_key(record: Dict[str, Any]) -> str:
    """Return the stable key for one canonical product content version."""
    product_id = record.get("identity", {}).get("product_id", "")
    return f"UPDATE_PRODUCT_EDITORIAL:{product_id}:{canonical_fingerprint(record)}"


def _ledger(
    path: str | Path,
    *,
    record: Dict[str, Any],
    approval: Dict[str, Any] | None,
    decision: str,
    operation: str,
    result: str,
    key: str,
    fingerprint: str,
    reason: str,
    publisher_version: str = "SHOPIFY_PUBLISHER_V1",
) -> None:
    """Append an auditable outcome without storing secrets or inventory state."""
    actor = str((approval or {}).get("actor") or "SYSTEM")
    entry = build_entry(
        product_id=str(record.get("identity", {}).get("product_id", "")),
        schema_version=str(record.get("schema_version", "")),
        content_fingerprint=fingerprint,
        idempotency_key=key,
        actor=actor,
        decision=decision,
        operation=operation,
        result=result,
        timestamp=datetime.now(timezone.utc).isoformat(),
        publisher_version=publisher_version,
        reason=reason,
    )
    append_entry(path, entry)


def publish(
    record: Dict[str, Any],
    approval: Dict[str, Any] | None,
    publisher: Publisher,
    idempotency_store: MutableMapping[str, Dict[str, Any]] | None = None,
    ledger_path: str | Path | None = None,
) -> Tuple[str, Dict[str, Any]]:
    """Authorize and hand off a canonical record to an injected publisher.

    The boundary is fail-closed: a blocked release never invokes publisher.
    When idempotency_store is supplied, a successful prior publication for
    the exact product fingerprint is returned without invoking publisher.
    When ledger_path is supplied, release outcomes are written to the audit ledger.
    """
    if not callable(publisher):
        raise TypeError("publisher must be callable")

    decision, reason = evaluate(record, approval)
    product_id = record.get("identity", {}).get("product_id", "")
    fingerprint = canonical_fingerprint(record)
    key = idempotency_key(record)

    if decision != APPROVED:
        audit = {
            "product_id": product_id,
            "content_fingerprint": fingerprint,
            "idempotency_key": key,
            "decision": decision,
            "reason": reason,
        }
        if ledger_path is not None:
            _ledger(
                ledger_path,
                record=record,
                approval=approval,
                decision=decision,
                operation="RELEASE_GATE",
                result=BLOCKED,
                key=key,
                fingerprint=fingerprint,
                reason=reason,
            )
        return BLOCKED, audit

    if idempotency_store is not None and key in idempotency_store:
        prior = deepcopy(idempotency_store[key])
        reason = "Exact approved product fingerprint was already published"
        if ledger_path is not None:
            _ledger(
                ledger_path,
                record=record,
                approval=approval,
                decision=APPROVED,
                operation="PUBLISH",
                result=ALREADY_PUBLISHED,
                key=key,
                fingerprint=fingerprint,
                reason=reason,
            )
        return ALREADY_PUBLISHED, {
            **prior,
            "idempotency_key": key,
            "reason": reason,
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

    if ledger_path is not None:
        _ledger(
            ledger_path,
            record=record,
            approval=approval,
            decision=APPROVED,
            operation="PUBLISH",
            result=PUBLISHED,
            key=key,
            fingerprint=fingerprint,
            reason=audit["reason"],
        )

    return PUBLISHED, audit


__all__ = ["ALREADY_PUBLISHED", "BLOCKED", "PUBLISHED", "idempotency_key", "publish"]
