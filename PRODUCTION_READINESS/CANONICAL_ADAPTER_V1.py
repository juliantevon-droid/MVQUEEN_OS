"""Canonical adapter for turning source product records into MVQueen production records.

The adapter is intentionally side-effect free: it never writes to Shopify and never
changes protected source fields. Legacy engines may feed this adapter, but they are
not allowed to publish around the canonical QA gate.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping

from INTERNAL_LINKING_INTELLIGENCE_V1 import resolve_internal_links
from MERCHANDISING_INTELLIGENCE_V1 import resolve_catalog
from PRODUCT_PIPELINE_V1 import PROTECTED_FIELDS, run


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _snapshot(record: Dict[str, Any]) -> Dict[str, Any]:
    """Capture protected values wherever they exist in the incoming record."""
    snapshot: Dict[str, Any] = {}
    for key in PROTECTED_FIELDS:
        if key in record:
            snapshot[key] = deepcopy(record[key])
        if key in record.get("identity", {}):
            snapshot[f"identity.{key}"] = deepcopy(record["identity"][key])
        if key in record.get("protected_source", {}):
            snapshot[f"protected_source.{key}"] = deepcopy(record["protected_source"][key])
    return snapshot


def _assert_unchanged(before: Dict[str, Any], after: Dict[str, Any]) -> None:
    for path, expected in before.items():
        section, _, key = path.partition(".")
        if section == "identity":
            actual = after.get("identity", {}).get(key)
        elif section == "protected_source":
            actual = after.get("protected_source", {}).get(key)
        else:
            actual = after.get(section)
        if actual != expected:
            raise ValueError(f"Protected field changed during production pipeline: {path}")


def produce(raw_product: Dict[str, Any]) -> Dict[str, Any]:
    """Produce a canonical record; never publish, call Shopify, or mutate input."""
    source = deepcopy(raw_product)
    protected_snapshot = _snapshot(source)
    result = run(source)
    _assert_unchanged(protected_snapshot, result)
    return result


def produce_catalog(
    raw_products: Iterable[Dict[str, Any]],
    *,
    collection_handles: Mapping[str, str] | None = None,
) -> List[Dict[str, Any]]:
    """Produce a reviewable catalog with relationships and verified internal links."""
    sources = [deepcopy(item) for item in raw_products]
    canonical = [produce(item) for item in sources]
    blocked = [
        _text(record.get("identity", {}).get("product_id")) or "<unknown>"
        for record in canonical
        if record.get("status") != "PRODUCTION_READY"
    ]
    if blocked:
        raise ValueError(
            "Catalog merchandising requires every product to be PRODUCTION_READY: "
            + ", ".join(blocked)
        )
    merchandised = resolve_catalog(canonical)
    return resolve_internal_links(
        merchandised,
        collection_handles=collection_handles,
    )


if __name__ == "__main__":
    import json
    import sys
    payload = json.load(sys.stdin)
    output = produce_catalog(payload) if isinstance(payload, list) else produce(payload)
    print(json.dumps(output, indent=2, ensure_ascii=False))
