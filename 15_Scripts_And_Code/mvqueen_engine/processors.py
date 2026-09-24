"""Retired Omniluxe all-in-one processor.

The former processor generated identity, variants, prices, editorial content,
SEO, collections, and metafields from free text. That path conflicts with the
canonical source-truth and protected-field contracts, so it now fails closed.
"""
from __future__ import annotations


def process_product(*args, **kwargs):
    raise RuntimeError(
        "The legacy Omniluxe processor is retired. Use the canonical "
        "PRODUCTION_READINESS product pipeline."
    )


def process_texts(*args, **kwargs):
    raise RuntimeError(
        "The legacy Omniluxe processor is retired. Use the canonical "
        "PRODUCTION_READINESS product pipeline."
    )


__all__ = ["process_product", "process_texts"]
