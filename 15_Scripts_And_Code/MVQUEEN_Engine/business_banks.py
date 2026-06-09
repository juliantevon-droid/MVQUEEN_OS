# mvqueen_engine/brand_brain/brand_banks/business_banks.py
"""
MVQueen Business Vocabulary Banks

This file defines the business, merchandising, and catalog language
used across the MVQueen Omniluxe Engine. Even though these terms
serve structural and organizational purposes, they are still aligned
with the MVQueen brand DNA:

- women-centered
- modern and elevated
- soft but confident
- luxury-hybrid
- editorial and atmospheric
- Sephora clarity
- Victoria’s Secret femininity
- MVQueen poetic precision

These banks support:
- Shopify product type mapping
- Collection routing
- Tag generation
- Metafield structuring
- Catalog hierarchy
- Merchandising logic
"""

# ------------------------------------------------------------
# PRODUCT TYPES — Soft, Modern, Feminine Categorization
# ------------------------------------------------------------
PRODUCT_TYPES = [
    "dress",
    "top",
    "bodysuit",
    "skirt",
    "pants",
    "denim",
    "outerwear",
    "lingerie",
    "activewear",
    "loungewear",
    "jumpsuit",
    "romper",
    "set",
    "accessory",
    "beauty",
    "skincare",
]

# ------------------------------------------------------------
# COLLECTION THEMES — Editorial + Merchandising Hybrid
# ------------------------------------------------------------
COLLECTION_THEMES = [
    "Soft Essentials",
    "Evening Glow",
    "Modern Romance",
    "Quiet Luxury",
    "Everyday Ease",
    "Feminine Foundations",
    "Luminous Nights",
    "Weekend Movement",
    "Body Language",
    "Elevated Comfort",
]

# ------------------------------------------------------------
# BUSINESS TAGS — Feminine, Modern, Search-Friendly
# ------------------------------------------------------------
BUSINESS_TAGS = [
    "new arrival",
    "best seller",
    "editor’s pick",
    "limited edition",
    "online exclusive",
    "seasonal favorite",
    "luxury essential",
    "soft silhouette",
    "curve-friendly",
    "lightweight feel",
]

# ------------------------------------------------------------
# SHOPIFY METAFIELD KEYS — Clean, Structured, MVQueen-Aligned
# ------------------------------------------------------------
METAFIELD_KEYS = {
    "fit": "mvqueen.fit",
    "fabric": "mvqueen.fabric",
    "care": "mvqueen.care",
    "occasion": "mvqueen.occasion",
    "vibe": "mvqueen.vibe",
    "persona": "mvqueen.persona",
    "benefits": "mvqueen.benefits",
    "materials": "mvqueen.materials",
    "silhouette": "mvqueen.silhouette",
}

# ------------------------------------------------------------
# BUSINESS BENEFITS — Soft, Feminine, Editorial-Ready
# ------------------------------------------------------------
BUSINESS_BENEFITS = [
    "designed for movement",
    "made for everyday luxury",
    "crafted for feminine confidence",
    "built for softness and ease",
    "created to elevate your wardrobe",
    "made to feel as good as it looks",
]

__all__ = [
    "PRODUCT_TYPES",
    "COLLECTION_THEMES",
    "BUSINESS_TAGS",
    "METAFIELD_KEYS",
    "BUSINESS_BENEFITS",
]