
SEO_ENGINE = {
    # ---------------------------------------------
    # GLOBAL SEO RULES
    # ---------------------------------------------
    "rules": {
        "title_max_length": 60,
        "meta_desc_min": 150,
        "meta_desc_max": 160,
        "avoid_duplicate_primary": True,
        "avoid_keyword_conflicts": True,
        "sanitize_output": True,
        "fallback_to_brand_prefix": True,
    },

    # ---------------------------------------------
    # SEO KEYWORD POOLS (EMPTY — FILLED LATER)
    # ---------------------------------------------
    "keyword_pools": {
        "primary": [],
        "secondary": [],
        "longtail": [],
        "category_keywords": {
            "skincare": [],
            "beauty": [],
            "fashion": [],
        },
        "persona_keywords": {
            "MVQueen Core": [],
            "MISS.QUEEN": [],
            "Victoria Soft Power": [],
            "Sephora Precision": [],
            "Runway Modern": [],
            "Clinical Chic": [],
            "Soft Luxury": [],
            "Glow Maestro": [],
            "Elegant Authority": [],
            "Street Luxe Femme": [],
        },
    },

    # ---------------------------------------------
    # PERSONA-SPECIFIC SEO BIAS
    # ---------------------------------------------
    "persona_bias": {
        "MVQueen Core": {
            "prefer": ["luxury", "soft", "sensual", "confident"],
        },
        "MISS.QUEEN": {
            "prefer": ["glam", "playful", "cute", "beauty"],
        },
        "Victoria Soft Power": {
            "prefer": ["elegant", "soft", "intentional"],
        },
        "Sephora Precision": {
            "prefer": ["clinical", "clean", "expert"],
        },
        "Runway Modern": {
            "prefer": ["editorial", "runway", "bold"],
        },
        "Clinical Chic": {
            "prefer": ["minimal", "clean", "clinical"],
        },
        "Soft Luxury": {
            "prefer": ["romantic", "luxury", "soft"],
        },
        "Glow Maestro": {
            "prefer": ["glow", "radiance", "bright"],
        },
        "Elegant Authority": {
            "prefer": ["refined", "power", "elegant"],
        },
        "Street Luxe Femme": {
            "prefer": ["street", "luxe", "feminine"],
        },
    },

    # ---------------------------------------------
    # CATEGORY-SPECIFIC SEO RULES
    # ---------------------------------------------
    "category_rules": {
        "skincare": {
            "required": ["skin_concern", "benefit"],
            "optional": ["texture", "finish"],
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
    # SEO METAFIELD RULES
    # ---------------------------------------------
    "metafield_rules": {
        "focus_keyword": {
            "source": "primary_keyword",
            "namespace": "seo",
            "key": "focus_keyword",
        },
        "secondary_keywords": {
            "source": "secondary_keywords",
            "namespace": "seo",
            "key": "secondary_keywords",
        },
        "alt_text": {
            "source": "alt_text",
            "namespace": "custom",
            "key": "alt_text",
        },
    },

    # ---------------------------------------------
    # ALT-TEXT ENGINE
    # ---------------------------------------------
    "alt_text_engine": {
        "structure": [
            "{brand}",
            "{product_type}",
            "{primary_keyword}",
            "{finish}",
            "{color}",
        ],
        "max_length": 120,
        "sanitize_output": True,
    },

    # ---------------------------------------------
    # SEO FALLBACK RULES
    # ---------------------------------------------
    "fallbacks": {
        "primary_keyword": "luxury",
        "secondary_keywords": ["beauty", "glow", "modern"],
        "meta_description": "Luxury beauty and fashion designed to elevate your everyday routine.",
    },

    # ---------------------------------------------
    # DETERMINISTIC SEO LOGIC
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