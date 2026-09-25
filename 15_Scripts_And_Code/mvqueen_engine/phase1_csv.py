"""Compatibility CSV entrypoint for the consolidated MVQueen catalog pipeline.

Historical versions routed through the broad runtime engine and could regenerate
pricing-related fields. That behavior is retired. This module delegates only to
the protected, offline catalog processor and performs no Shopify network I/O.
"""
from __future__ import annotations

from pathlib import Path

from mvqueen_engine.catalog_processor.processor import process_csv as _process_csv


def run_products_csv(csv_path: str, output_path: str = "mvqueen_output.csv") -> str:
    """Run the governed offline editorial transformation."""
    source = Path(csv_path)
    if not source.exists():
        raise FileNotFoundError(source)
    return _process_csv(str(source), output_path)


def process_csv(csv_path: str, output_path: str = "mvqueen_output.csv") -> str:
    """Compatibility alias for existing scripts."""
    return run_products_csv(csv_path, output_path)


if __name__ == "__main__":
    raise SystemExit(
        "Use: python -m mvqueen_engine.main INPUT.csv OUTPUT.csv"
    )
