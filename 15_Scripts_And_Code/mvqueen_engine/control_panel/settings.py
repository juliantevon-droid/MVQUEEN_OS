"""Centralized, environment-aware MVQueen runtime settings."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class EngineSettings:
    brand_name: str = "MVQueen"
    dry_run: bool = True
    csv_chunk_size: int = 850
    max_products_per_export: int = 850
    shopify_api_version: str = "2025-01"

    @classmethod
    def from_env(cls) -> "EngineSettings":
        def flag(name: str, default: bool) -> bool:
            value = os.getenv(name)
            if value is None:
                return default
            return value.strip().lower() in {"1", "true", "yes", "on"}

        return cls(
            brand_name=os.getenv("MVQ_BRAND_NAME", "MVQueen"),
            dry_run=flag("MVQ_DRY_RUN", True),
            csv_chunk_size=int(os.getenv("MVQ_CSV_CHUNK_SIZE", "850")),
            max_products_per_export=int(os.getenv("MVQ_MAX_PRODUCTS_PER_EXPORT", "850")),
            shopify_api_version=os.getenv("SHOPIFY_API_VERSION", "2025-01"),
        )
