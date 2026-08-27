"""Safe deterministic bundle pairing for MVQueen products."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any


def generate_handle(first: str, second: str) -> str:
    digest = hashlib.sha256(f"{first}|{second}".encode("utf-8")).hexdigest()[:12]
    return f"bundle-{digest}"


def generate_bundles(products: Iterable[Mapping[str, Any]], discount_rate: float = 0.15) -> list[dict[str, Any]]:
    """Pair bundle-safe products by collection/intent with deterministic output."""
    if not 0 <= discount_rate < 1:
        raise ValueError("discount_rate must be between 0 and 1")
    groups: defaultdict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for product in products:
        safe = str(product.get("shopify_bundle_safe", product.get("metafield.custom.shopify_bundle_safe", ""))).lower() == "true"
        if not safe:
            continue
        key = (str(product.get("collection", product.get("metafield.custom.collection", ""))).strip(), str(product.get("intent", product.get("metafield.custom.intent", ""))).strip())
        groups[key].append(product)

    bundles: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda p: str(p.get("handle", "")))
        for index in range(0, len(group) - 1, 2):
            first, second = group[index], group[index + 1]
            try:
                total = float(first.get("price")) + float(second.get("price"))
            except (TypeError, ValueError):
                continue
            bundles.append({
                "Handle": generate_handle(str(first.get("handle", "")), str(second.get("handle", ""))),
                "Title": f"{first.get('title', '')} + {second.get('title', '')} Bundle | MVQueen",
                "Variant Price": round(total * (1 - discount_rate), 2),
                "Variant Compare At Price": round(total, 2),
                "Vendor": "MVQueen",
                "Tags": "bundle,mvqueen",
                "metafield.custom.shopify_bundle_safe": "true",
                "metafield.custom.collection": key[0],
                "metafield.custom.intent": key[1],
            })
    return bundles
