"""Legacy text-engine facade.

The former all-in-one product generator could synthesize variants, inventory,
pricing, and unverified product attributes. It is intentionally unavailable in
production. Use the governed CSV recovery/dry-run pipeline for catalog work.
"""
from __future__ import annotations


def run(*args, **kwargs):
    raise RuntimeError(
        "The legacy generative engine is retired. Use "
        "mvqueen_engine.catalog_processor.processor.process_csv() for offline "
        "curation or the canonical product QA/release pipeline."
    )


__all__ = ["run"]
