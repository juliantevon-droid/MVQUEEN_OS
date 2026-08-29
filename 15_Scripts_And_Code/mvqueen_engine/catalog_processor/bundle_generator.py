"""Safe deterministic bundle pairing for MVQueen products."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any


def generate_handle(first: str, second: str) -> str:
    """Create a deterministic, collision-resistant Shopify-safe bundle handle."""
    digest = hashlib.sha256(f"{first}|{second}".encode("utf-8")).hexdigest()[:12]
    return f"bundle-{digest}"


def _text(product: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(product.get(key, "") or "").strip()
        if value:
            return value
    return ""


def _tags(product: Mapping[str, Any]) -> list[str]:
    value = product.get("tags", product.get("Tags", []))
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(part).strip() for part in value if str(part).strip()]
    return []


def generate_bundles(products: Iterable[Mapping[str, Any]], discount_rate: float = 0.15) -> list[dict[str, Any]]:
    """Pair bundle-safe products by collection/intent with deterministic output.

    Existing product intelligence is carried into the generated bundle rather
    than discarded. Products without valid prices or without explicit bundle
    safety are skipped; the function never invents product facts.
    """
    if not 0 <= discount_rate < 1:
        raise ValueError("discount_rate must be between 0 and 1")

    groups: defaultdict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for product in products:
        safe = _text(product, "shopify_bundle_safe", "metafield.custom.shopify_bundle_safe").lower() == "true"
        if not safe:
            continue
        collection = _text(product, "collection", "metafield.custom.collection")
        intent = _text(product, "intent", "metafield.custom.intent")
        groups[(collection, intent)].append(product)

    bundles: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda p: _text(p, "handle", "Handle"))
        for index in range(0, len(group) - 1, 2):
            first, second = group[index], group[index + 1]
            try:
                first_price = float(first.get("price", first.get("Variant Price")))
                second_price = float(second.get("price", second.get("Variant Price")))
            except (TypeError, ValueError):
                continue

            first_title = _text(first, "title", "Title")
            second_title = _text(second, "title", "Title")
            total = first_price + second_price
            tags = {tag.lower(): tag for tag in (_tags(first) + _tags(second))}
            tags["bundle"] = "bundle"
            tags["mvqueen"] = "mvqueen"

            prestige_values = []
            quality_values = []
            for product in (first, second):
                try:
                    prestige_values.append(float(product.get("prestige_score", product.get("metafield.custom.prestige_score"))))
                except (TypeError, ValueError):
                    pass
                try:
                    quality_values.append(float(product.get("product_quality_score", product.get("metafield.custom.product_quality_score"))))
                except (TypeError, ValueError):
                    pass

            bundles.append({
                "Handle": generate_handle(_text(first, "handle", "Handle"), _text(second, "handle", "Handle")),
                "Title": f"{first_title} + {second_title} Bundle | MVQueen",
                "Body (HTML)": (
                    f"<p>Exclusive MVQueen bundle featuring {first_title} and {second_title}.</p>"
                    f"<p>Enjoy {int(discount_rate * 100)}% bundle savings with a curated pairing.</p>"
                ),
                "Variant Price": round(total * (1 - discount_rate), 2),
                "Variant Compare At Price": round(total, 2),
                "Vendor": "MVQueen",
                "Tags": ", ".join(sorted(tags.values())),
                "SEO Title": f"{first_title} + {second_title} Bundle | MVQueen"[:60],
                "SEO Description": f"Shop the {first_title} + {second_title} MVQueen bundle with exclusive savings."[:155],
                "Image Alt Text": f"{first_title} and {second_title} MVQueen bundle",
                "metafield.custom.shopify_bundle_safe": "true",
                "metafield.custom.collection": key[0],
                "metafield.custom.intent": key[1],
                "metafield.custom.voice": "luxury-modern-elegant",
                "metafield.custom.prestige_score": max(prestige_values) if prestige_values else "",
                "metafield.custom.product_quality_score": round(sum(quality_values) / len(quality_values), 1) if quality_values else "",
            })
    return bundles


__all__ = ["generate_handle", "generate_bundles"]
