"""Retired legacy metafield generator.

The previous implementation could fabricate material, fit, origin, shelf life,
certifications, bestseller badges, results, usage, and other unsupported facts.
All production metafields must now be produced by CONTENT_INTELLIGENCE_V1 from a
PRODUCTION_READY canonical record and verified source_truth facts.
"""
from __future__ import annotations


def generate_metafields(*args, **kwargs):
    raise RuntimeError(
        "The legacy metafield generator is retired. Use "
        "PRODUCTION_READINESS.CONTENT_INTELLIGENCE_V1.generate_content_suite()."
    )


def generate_all_metafields(*args, **kwargs):
    raise RuntimeError(
        "The legacy metafield generator is retired. Use "
        "PRODUCTION_READINESS.CONTENT_INTELLIGENCE_V1.generate_content_suite()."
    )


__all__ = ["generate_metafields", "generate_all_metafields"]
