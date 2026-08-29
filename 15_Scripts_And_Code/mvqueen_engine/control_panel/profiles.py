"""Named operating profiles for safe MVQueen workflows."""
from __future__ import annotations

from dataclasses import replace
from .toggles import RuntimeToggles

PROFILES = {
    "preview": RuntimeToggles(dry_run=True, enable_shopify_reads=False, enable_shopify_writes=False),
    "catalog": RuntimeToggles(dry_run=True, enable_shopify_reads=False, enable_shopify_writes=False),
    "shopify_read": RuntimeToggles(dry_run=True, enable_shopify_reads=True, enable_shopify_writes=False),
    "production": RuntimeToggles(dry_run=False, enable_shopify_reads=True, enable_shopify_writes=True),
}


def get_profile(name: str) -> RuntimeToggles:
    key = str(name).strip().lower()
    if key not in PROFILES:
        raise KeyError(f"Unknown MVQueen profile: {name}")
    return replace(PROFILES[key])
