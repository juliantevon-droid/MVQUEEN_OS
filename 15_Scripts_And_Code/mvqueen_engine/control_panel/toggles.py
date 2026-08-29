"""Safety toggles for the MVQueen control panel."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuntimeToggles:
    optimize_catalog: bool = True
    generate_bundles: bool = True
    generate_collections: bool = True
    generate_editorial: bool = True
    enable_shopify_reads: bool = False
    enable_shopify_writes: bool = False
    dry_run: bool = True

    def can_write_shopify(self) -> bool:
        return self.enable_shopify_writes and not self.dry_run

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.enable_shopify_writes and self.dry_run:
            errors.append("Shopify writes are enabled while dry_run is active")
        return errors
