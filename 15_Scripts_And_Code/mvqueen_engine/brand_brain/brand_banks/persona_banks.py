"""Controlled persona vocabulary for MVQueen routing and editorial context."""
from __future__ import annotations

PERSONAS = (
    "modern_luxury_consumer",
    "style_forward_individual",
    "quality_driven_customer",
    "elevated_lifestyle_shopper",
)

DESCRIPTORS = {
    "modern_luxury_consumer": ("refined", "contemporary", "premium", "elevated"),
    "style_forward_individual": ("expressive", "polished", "fashion-forward", "statement"),
    "quality_driven_customer": ("precise", "crafted", "timeless", "quality"),
    "elevated_lifestyle_shopper": ("warm", "aspirational", "comfortable", "composed"),
}

__all__ = ["PERSONAS", "DESCRIPTORS"]
