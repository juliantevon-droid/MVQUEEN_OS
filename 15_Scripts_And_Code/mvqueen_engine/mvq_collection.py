# catalog_processor/collection.py
"""
MVQueen Collection Assignment — Enterprise Edition
--------------------------------------------------

Assigns products to Shopify collections using:
- Category
- Product type
- Persona
- Vibe
- Trend
- Season
- Silhouette
- Material

Collections are:
- deterministic
- MVQueen-aligned
- Shopify-safe
"""

from typing import Dict, List


# ------------------------------------------------------------
# HELPER — Normalize collection handles
# ------------------------------------------------------------
def _handle(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


# ------------------------------------------------------------
# MAIN COLLECTION BUILDER
# ------------------------------------------------------------
def assign_collections(profile: Dict) -> List[str]:
    """
    Determines Shopify collection handles for a product.

    Returns:
        List[str]
    """

    collections = []

    # Category-based
    if profile.get("category"):
        collections.append(f"cat-{_handle(profile['category'])}")

    # Product type
    if profile.get("product_type"):
        collections.append(f"type-{_handle(profile['product_type'])}")

    # Persona
    if profile.get("persona"):
        collections.append(f"persona-{_handle(profile['persona'])}")

    # Trend
    if profile.get("trend"):
        collections.append(f"trend-{_handle(profile['trend'])}")

    # Vibe
    if profile.get("vibe"):
        collections.append(f"vibe-{_handle(profile['vibe'])}")

    # Season
    if profile.get("season"):
        collections.append(f"season-{_handle(profile['season'])}")

    # Silhouette
    for s in profile.get("silhouette", []):
        collections.append(f"silhouette-{_handle(s)}")

    # Material
    for m in profile.get("material", []):
        collections.append(f"material-{_handle(m)}")

    # Deduplicate + sort
    return sorted(list(set(collections)))


__all__ = ["assign_collections"]