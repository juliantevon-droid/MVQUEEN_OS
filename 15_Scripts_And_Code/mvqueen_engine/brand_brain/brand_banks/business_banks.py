"""Controlled business vocabulary for catalog and operational metadata."""
from __future__ import annotations

CHANNELS = ("online", "ecommerce", "retail", "direct-to-consumer", "marketplace")
MERCHANDISING = ("new arrivals", "core collection", "seasonal edit", "limited edit", "best seller", "giftable", "everyday essentials")
OPERATIONS = ("inventory", "catalog", "product", "collection", "variant", "metafield", "tag", "bundle")

__all__ = ["CHANNELS", "MERCHANDISING", "OPERATIONS"]
