"""MVQueen Omniluxe Engine public entry point."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from mvqueen_engine.catalog_processor.processor import process_dataframe, process_product
from mvqueen_engine.catalog_processor.csv_loader import convert_to_csv_row
from mvqueen_engine.catalog_processor.batch_processor import process_dataframe_in_batches
from mvqueen_engine.catalog_processor.bundle_generator import generate_bundles


@dataclass(frozen=True)
class EngineConfig:
    """Safe local pipeline controls."""
    chunk_size: int = 850
    generate_bundles: bool = True
    discount_rate: float = 0.15


def run(text: str) -> dict[str, Any]:
    """Preserved legacy single-product API."""
    product = process_product(text)
    return {"product": product, "csv_row": convert_to_csv_row(product)}


def run_dataframe(df: pd.DataFrame, config: EngineConfig | None = None) -> dict[str, Any]:
    """Run catalog enrichment and optional bundle generation without Shopify side effects."""
    config = config or EngineConfig()
    products = process_dataframe_in_batches(df, process_dataframe, config.chunk_size)
    bundles = generate_bundles(products.to_dict("records"), config.discount_rate) if config.generate_bundles else []
    return {"products": products, "bundles": pd.DataFrame(bundles), "bundle_records": bundles}


def run_csv(input_path: str | Path, output_dir: str | Path, config: EngineConfig | None = None) -> dict[str, Path]:
    """Process a Shopify CSV and export optimized products and optional bundles."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"CSV not found: {source}")
    if source.suffix.lower() != ".csv":
        raise ValueError("input_path must point to a CSV file")
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(source, dtype=object, keep_default_na=False)
    config = config or EngineConfig()
    result = run_dataframe(frame, config)
    product_path = destination / f"{source.stem}_optimized.csv"
    result["products"].to_csv(product_path, index=False)
    paths = {"products": product_path}
    if config.generate_bundles:
        bundle_path = destination / f"{source.stem}_bundles.csv"
        result["bundles"].to_csv(bundle_path, index=False)
        paths["bundles"] = bundle_path
    return paths


__all__ = ["EngineConfig", "run", "run_dataframe", "run_csv"]
