"""Retired legacy MVQueen runtime facade.

This module previously generated titles, handles, prices, image data, and
metafields outside the canonical QA/release pipeline. It is intentionally
fail-closed so protected fields cannot be changed by an alternate runtime.
"""
from __future__ import annotations


def run_mvqueen(*args, **kwargs):
    raise RuntimeError(
        "The legacy runtime is retired. Use PRODUCTION_READINESS/"
        "CANONICAL_ADAPTER_V1.produce() and the governed content/release pipeline."
    )


__all__ = ["run_mvqueen"]
