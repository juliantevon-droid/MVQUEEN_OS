
TITLE_ENGINE = {
    # ---------------------------------------------
    # GLOBAL TITLE RULES
    # ---------------------------------------------
    "rules": {
        "max_length": 60,
        "include_brand": True,
        "include_primary_keyword": True,
        "include_benefit": True,
        "include_product_type": True,
        "fallback_to_base_title": True,
        "sanitize_output": True,
    },

    # ---------------------------------------------
    # TITLE STRUCTURE PATTERNS
    # ---------------------------------------------
    "patterns": {
        "default": [
            "{brand} {primary_keyword} {product_type}",
            "{brand} {benefit} {product_type}",
            "{brand} {product_type} for {benefit}",
        ],

        "skincare": [
            "{brand} {primary_keyword} {product_type}",
            "{brand} {benefit} Treatment",
            "{brand} {product_type} for {skin_profile}",
        ],

        "beauty": [
            "{brand} {finish} {product_type}",
            "{brand} {mood} {product_type}",
            "{brand} {product_type} for {occasion}",
        ],

        "fashion": [
            "{brand} {vibe} {product_type}",
            "{brand} {material} {product_type}",
            "{brand} {silhouette} {product_type}",
        ],
    },

    # ---------------------------------------------
    # PERSONA-SPECIFIC TITLE BIAS
    # ---------------------------------------------
    "persona_bias": {
        "MVQueen Core": {
            "prefer": ["benefit", "primary_keyword", "finish"],
        },
        "MISS.QUEEN": {
            "prefer": ["mood", "occasion", "finish"],
        },
        "Runway Modern": {
            "prefer": ["vibe", "silhouette", "material"],
        },
        "Clinical Chic": {
            "prefer": ["skin_profile", "benefit", "primary_keyword"],
        },
        "Soft Luxury": {
            "prefer": ["finish", "mood", "benefit"],
        },
        "Glow Maestro": {
            "prefer": ["glow", "radiance", "finish"],
        },
        "Elegant Authority": {
            "prefer": ["silhouette", "material", "benefit"],
        },
        "Street Luxe Femme": {
            "prefer": ["vibe", "material", "occasion"],
        },
    },

    # ---------------------------------------------
    # CATEGORY-SPECIFIC TITLE RULES
    # ---------------------------------------------
    "category_rules": {
        "skincare": {
            "required": ["primary_keyword"],
            "optional": ["benefit", "skin_profile"],
        },
        "beauty": {
            "required": ["finish"],
            "optional": ["mood", "occasion"],
        },
        "fashion": {
            "required": ["silhouette"],
            "optional": ["material", "vibe"],
        },
    },

    # ---------------------------------------------
    # TITLE VOCAB POOLS (EMPTY — FILLED LATER)
    # ---------------------------------------------
    "vocab": {
        "benefits": [],
        "finishes": [],
        "moods": [],
        "occasions": [],
        "materials": [],
        "silhouettes": [],
        "vibes": [],
        "skin_profiles": [],
    },

    # ---------------------------------------------
    # DETERMINISTIC TITLE LOGIC
    # ---------------------------------------------
    "deterministic": {
        "use_seed": True,
        "seed_components": [
            "handle",
            "category",
            "persona",
            "primary_keyword",
        ],
        "fallback_seed": 42,
    },
}


