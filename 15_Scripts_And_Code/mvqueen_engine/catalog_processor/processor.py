"""Governed offline catalog processor.

This module intentionally exposes only row-safe CSV normalization. Direct
Shopify transport and the historical all-in-one product generator are retired.
"""
from __future__ import annotations

from mvqueen_engine.catalog_normalization import normalize_shopify_csv


def process_csv(input_path: str, output_path: str) -> str:
    """Normalize a Shopify CSV offline while preserving protected fields."""
    normalize_shopify_csv(input_path, output_path)
    return output_path


def process_shopify_catalog(*args, **kwargs):
    """Fail closed: Python is not a production Shopify writer."""
    raise RuntimeError(
        "Direct Shopify catalog processing is disabled. Use the authenticated "
        "application plus the canonical QA/release/approval boundary."
    )


__all__ = ["process_csv", "process_shopify_catalog"]
