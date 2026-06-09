# COLLECTION VOCAB — COMPLETE BANKS

COLLECTION_TYPES = [
    "Vibe",
    "Material",
    "Silhouette",
    "Detail",
    "Benefit",
    "Routine",
    "Category",
    "Product Type",
    "Persona",
    "Trend",
    "Season",
    "Fashion",
    "SEO",
    "Occasion",
    "Mood"
]

TREND_KEYWORDS = [
    "quiet luxury", "soft glam", "clean girl", "street luxe",
    "editorial chic", "resort chic", "CEO energy", "vacation mode",
    "old money", "new money glam", "minimalist", "maximalist",
    "romantic feminine", "athleisure luxe"
]

SEASON_KEYWORDS = [
    "spring", "summer", "fall", "winter", "holiday", "resort"
]

CATEGORY_KEYWORDS = {
    "Skincare": [
        "serum", "cleanser", "moisturizer", "spf", "sunscreen", "toner",
        "mask", "cream", "gel", "treatment", "essence", "hydrating",
        "lotion", "balm", "oil", "exfoliant", "peel", "retinol",
        "niacinamide", "hyaluronic", "vitamin c", "brightening",
        "firming", "plumping", "soothing", "calming", "barrier",
        "repair", "recovery", "overnight", "eye cream", "eye gel",
        "spot treatment", "acne", "blemish", "pore", "texture",
    ],

    "Makeup": [
        "foundation", "concealer", "blush", "bronzer", "highlighter",
        "lipstick", "lip gloss", "mascara", "eyeshadow", "liner", "brow",
        "setting spray", "primer", "tint", "skin tint", "powder",
        "palette", "pigment", "cream blush", "liquid blush",
        "glow stick", "matte", "dewy", "radiant finish",
    ],
    
    "Haircare": [
        "shampoo", "conditioner", "hair oil", "hair mask", "styling",
        "leave-in", "heat protectant", "serum", "curl cream",
        "smoothing cream", "volumizing", "repair", "strengthening",
        "scalp", "detox", "clarifying", "shine spray",
    ],

    "Bodycare": [
        "body wash", "body lotion", "body oil", "scrub", "butter",
        "body cream", "exfoliating", "hydrating", "firming",
        "body polish", "body serum", "body mist",
    ],

    "Fragrance": [
        "perfume", "eau", "fragrance", "parfum", "mist",
        "rollerball", "scent", "body spray", "cologne",
    ],

    "Apparel": [
        "dress", "top", "skirt", "pants", "jacket", "coat", "hoodie",
        "tee", "tank", "corset", "bodysuit", "sweater",
        "blazer", "trench", "outerwear", "denim", "jeans",
        "maxi", "midi", "mini", "slip", "gown", "two-piece",
        "set", "co-ord", "crop top", "wide-leg", "straight-leg",
        "oversized", "tailored", "ribbed", "knit", "silk",
        "satin", "mesh", "lace", "tulle", "chiffon",
    ],

    "Jewelry": [
        "necklace", "bracelet", "ring", "earrings", "jewelry",
        "studs", "hoops", "chain", "pendant", "charm",
        "gold", "silver", "plated", "pearl", "gemstone",
    ],

    "Accessories": [
        "bag", "belt", "scarf", "sunglasses", "hat",
        "tote", "crossbody", "shoulder bag", "clutch",
        "beanie", "cap", "visor", "wrap", "shawl",
    ],

    "Footwear": [
        "boots", "heels", "sneakers", "sandals",
        "flats", "loafers", "mules", "platforms",
        "ankle boot", "knee-high", "thigh-high",
    ],
}

PRODUCT_TYPE_KEYWORDS = {
    "Serum": ["serum", "ampoule"],
    "Cleanser": ["cleanser", "wash", "gel cleanser"],
    "Moisturizer": ["moisturizer", "cream", "lotion"],
    "SPF": ["spf", "sunscreen", "sun cream"],
    "Foundation": ["foundation", "skin tint", "base"],
    "Concealer": ["concealer"],
    "Blush": ["blush"],
    "Bronzer": ["bronzer", "contour"],
    "Highlighter": ["highlighter", "glow stick"],
    "Lip Gloss": ["lip gloss", "gloss"],
    "Lipstick": ["lipstick"],
    "Mascara": ["mascara"],
    "Eyeshadow": ["eyeshadow", "shadow palette"],
    "Dress": ["dress"],
    "Top": ["top", "blouse", "shirt"],
    "Pants": ["pants", "trousers"],
    "Skirt": ["skirt"],
    "Jacket": ["jacket"],
    "Coat": ["coat"],
    "Sweater": ["sweater", "knit"],
    "Hoodie": ["hoodie"],
    "Bag": ["bag", "tote", "crossbody"],
}

VIBE_KEYWORDS = {
    "soft_luxe": ["soft", "luxe", "velvet", "silky"],
    "hyper_modern": ["modern", "futuristic", "sleek"],
    "romantic": ["romantic", "delicate", "feminine"],
    "bold_graphic": ["bold", "graphic", "statement"]
}

# ---------------------------------------------------------
# MISSING BANKS (added for engine compatibility)
# ---------------------------------------------------------

MATERIAL_KEYWORDS = {
    "Satin": ["satin", "silk-satin", "charmeuse", "glossy", "sheen"],
    "Wool": ["wool", "cashmere", "merino", "felted"],
    "Denim": ["denim", "jeans", "indigo", "washed"],
    "Cotton": ["cotton", "jersey", "poplin"],
    "Leather": ["leather", "vegan leather", "faux leather"],
}

SILHOUETTE_KEYWORDS = {
    "A-Line": ["a-line", "flared", "gentle flare"],
    "Bodycon": ["bodycon", "fitted", "curve-hugging"],
    "Oversized": ["oversized", "boxy", "relaxed"],
    "Straight": ["straight", "classic cut", "column"],
}

DETAIL_KEYWORDS = {
    "Lace Trim": ["lace trim", "delicate lace"],
    "Raw Hem": ["raw hem", "frayed hem"],
    "Silver Hardware": ["silver hardware", "metal zip"],
    "Structured Shoulders": ["structured shoulders", "padded shoulders"],
}

   # ---------------------------------------------------------
# EDITORIAL VOCAB BANKS (required by brand_language.py)
# ---------------------------------------------------------

LUXURY_ADJECTIVES = [
    "luminous", "velvety", "silky", "refined", "elevated",
    "polished", "radiant", "sumptuous", "sleek", "opulent",
    "weightless", "ultra-soft", "cushioned", "glossy",
    "sophisticated", "modern", "timeless", "minimal",
    "sculpted", "contoured", "premium", "rich", "buttery",
]

SENSORY_VERBS = [
    "envelops", "enhances", "elevates", "awakens",
    "revitalizes", "softens", "smooths", "defines",
    "illuminates", "transforms", "refines", "energizes",
    "conditions", "clarifies", "refreshes",
]

FASHION_VIBES = [
    "soft glam", "quiet luxury", "editorial minimalism",
    "street luxe", "romantic feminine", "modern classic",
    "resort chic", "urban sleek", "timeless elegance",
]

FASHION_MATERIALS = [
    "satin", "silk", "cashmere", "wool", "denim",
    "leather", "mesh", "lace", "tulle", "chiffon",
    "ribbed knit", "cotton poplin",
]

EDITORIAL_FRAMES = [
    "A {adj} expression of {mood} energy, crafted for {occasion} moments.",
    "Designed with {adj} intention, it channels {mood} presence for {occasion} wear.",
    "A study in {adj} texture and {mood} refinement, perfect for {occasion} styling.",
    "Rooted in {mood} elegance, its {adj} finish elevates every {occasion} moment.",
]

SEO_PRIMARY = [
    "luxury fashion", "premium apparel", "designer essentials",
    "elevated basics", "modern wardrobe", "quiet luxury style",
    "editorial fashion", "minimalist fashion", "street luxe style",
]

   # ---------------------------------------------------------
# SECONDARY SEO VOCAB (required by seo_keywords.py)
# ---------------------------------------------------------

SEO_SECONDARY = [
    "luxury essentials",
    "premium quality",
    "modern wardrobe staples",
    "elevated everyday style",
    "designer-inspired looks",
    "quiet luxury outfits",
    "minimalist fashion trends",
    "street luxe aesthetic",
    "editorial-inspired styling",
    "high-end beauty essentials",
    "glowing skin routine",
    "hydrating skincare favorites",
    "soft glam makeup looks",
    "romantic feminine style",
    "resort-ready fashion",
]   