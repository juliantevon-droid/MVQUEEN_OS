"""Product intelligence detection layer for MVQueen.

The detection layer converts raw product text into structured attributes that
can be consumed by persona, editorial, SEO, metafield, tag, and collection
systems. Existing MVQUEEN_OS detection vocabularies remain authoritative and
can be adapted into these interfaces without discarding them.
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

__all__ = [
    "detect_category", "detect_product_type", "detect_persona", "detect_vibe",
    "detect_trend", "detect_season", "detect_material", "detect_silhouette",
    "detect_details", "detect_benefits", "detect_ingredients",
    "detect_textures", "detect_finishes",
]
