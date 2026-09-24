"""Current-Shopify-export normalization facade.

Production source of truth is Shopify. This module exposes the governed,
row-safe editorial normalizer for an explicitly supplied current Shopify export.
Historical recovery utilities remain compatibility/reference internals only.
"""
from __future__ import annotations

from mvqueen_engine.catalog_recovery_transform import transform_csv as normalize_shopify_csv

__all__ = ["normalize_shopify_csv"]
