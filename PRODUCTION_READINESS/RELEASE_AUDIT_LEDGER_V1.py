"""MVQUEEN release audit ledger V1.

The ledger records authorization and publishing outcomes without storing
secrets or mutable Shopify inventory/variant state. It is intentionally small
and dependency-free so it can back the publishing boundary in local, CI, or
service environments. Production deployments should place the ledger on a
persistent, access-controlled volume.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

LEDGER_SCHEMA_VERSION = "1.0"


def build_entry(
    *,
    product_id: str,
    schema_version: str,
    content_fingerprint: str,
    idempotency_key: str,
    actor: str,
    decision: str,
    operation: str,
    result: str,
    timestamp: str,
    publisher_version: str = "SHOPIFY_PUBLISHER_V1",
    reason: str = "",
) -> Dict[str, Any]:
    """Create a validated, secret-free release audit entry."""
    required = {
        "product_id": product_id,
        "schema_version": schema_version,
        "content_fingerprint": content_fingerprint,
        "idempotency_key": idempotency_key,
        "actor": actor,
        "decision": decision,
        "operation": operation,
        "result": result,
        "timestamp": timestamp,
    }
    missing = [key for key, value in required.items() if value in (None, "")]
    if missing:
        raise ValueError(f"Missing audit fields: {missing}")

    return {
        "ledger_schema_version": LEDGER_SCHEMA_VERSION,
        **required,
        "publisher_version": publisher_version,
        "reason": reason,
    }


def append_entry(path: str | Path, entry: Dict[str, Any]) -> None:
    """Append one JSONL entry; reject malformed/non-object records."""
    if not isinstance(entry, dict):
        raise TypeError("entry must be a dictionary")
    if entry.get("ledger_schema_version") != LEDGER_SCHEMA_VERSION:
        raise ValueError("Unsupported ledger schema version")

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")


def read_entries(path: str | Path) -> Iterable[Dict[str, Any]]:
    """Read valid JSONL entries; malformed lines fail closed."""
    target = Path(path)
    if not target.exists():
        return []

    entries = []
    with target.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Malformed ledger line {line_number}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"Ledger line {line_number} is not an object")
            entries.append(value)
    return entries


__all__ = ["LEDGER_SCHEMA_VERSION", "append_entry", "build_entry", "read_entries"]
