"""Control-panel configuration facade."""
from __future__ import annotations

from dataclasses import asdict
from .settings import EngineSettings


def load_config() -> dict:
    return asdict(EngineSettings.from_env())


def validate_config(config: dict) -> list[str]:
    errors = []
    if not str(config.get("brand_name", "")).strip():
        errors.append("brand_name is required")
    for key in ("csv_chunk_size", "max_products_per_export"):
        try:
            if int(config[key]) < 1:
                errors.append(f"{key} must be positive")
        except (KeyError, TypeError, ValueError):
            errors.append(f"{key} must be an integer")
    return errors
