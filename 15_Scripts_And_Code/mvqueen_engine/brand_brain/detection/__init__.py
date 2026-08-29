"""Deterministic product-attribute detection for MVQueen.

Each detector is deliberately conservative: supplied catalog text is classified
using transparent vocabulary/rules and no unsupported product claims are created.
"""
from .detect_category import detect_category
from .detect_product_type import detect_product_type
from .detect_persona import detect_persona
from .detect_vibe import detect_vibe
from .detect_trend import detect_trend
from .detect_season import detect_season
from .detect_material import detect_material
from .detect_silhouette import detect_silhouette
from .detect_details import detect_details
from .detect_benefits import detect_benefits
from .detect_ingredients import detect_ingredients
from .detect_textures import detect_textures
from .detect_finishes import detect_finishes


def detect_all(text: str) -> dict:
    """Run the complete detector set against one product's source text."""
    return {
        "category": detect_category(text),
        "product_type": detect_product_type(text),
        "persona": detect_persona(text),
        "vibe": detect_vibe(text),
        "trend": detect_trend(text),
        "season": detect_season(text),
        "material": detect_material(text),
        "silhouette": detect_silhouette(text),
        "details": detect_details(text),
        "benefits": detect_benefits(text),
        "ingredients": detect_ingredients(text),
        "textures": detect_textures(text),
        "finishes": detect_finishes(text),
    }

__all__ = ["detect_all", "detect_category", "detect_product_type", "detect_persona", "detect_vibe", "detect_trend", "detect_season", "detect_material", "detect_silhouette", "detect_details", "detect_benefits", "detect_ingredients", "detect_textures", "detect_finishes"]
