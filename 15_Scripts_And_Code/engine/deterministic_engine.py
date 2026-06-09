DETERMINISTIC_ENGINE = {
    # Global salt lets you "rotate the universe" without breaking consistency
    "GLOBAL_SALT": "MVQUEEN_OMNILUXE_V1",

    # What fields contribute to the seed?
    "SEED_COMPONENTS": {
        "use_handle": True,
        "use_title": True,
        "use_row_index": True,
        "use_category": True,
        "use_persona": True,
    },

    # How seeds are built
    "SEED_FORMAT": "{handle}-{title}-{index}-{category}-{persona}-{salt}",

    # Deterministic choice rules
    "CHOICE_RULES": {
        "adjectives_per_pick": 1,
        "sensory_verbs_per_pick": 1,
        "confidence_phrases_per_pick": 1,
        "benefits_per_pick": 3,
        "routine_steps_per_pick": 2,
        "fashion_terms_per_pick": 2,
    },

    # Deterministic multi-choice rules
    "MULTI_CHOICE_RULES": {
        "max_adjectives": 3,
        "max_sensory_verbs": 3,
        "max_confidence_phrases": 2,
        "max_secondary_keywords": 3,
        "max_tags": 6,
    },

    # Deterministic persona selection
    "PERSONA_SELECTION": {
        "use_category_bias": True,
        "use_price_tier_bias": True,
        "use_product_type_bias": True,
        "fallback_persona": "MVQueen Core",
    },

    # Deterministic SEO selection
    "SEO_SELECTION": {
        "primary_keyword_count": 1,
        "secondary_keyword_count": 3,
        "avoid_duplicates": True,
        "avoid_conflicts": True,
    },

    # Deterministic editorial structure
    "EDITORIAL_DETERMINISM": {
        "intro_frame_pick": "deterministic",
        "body_frame_pick": "deterministic",
        "fashion_frame_pick": "deterministic",
        "closer_frame_pick": "deterministic",
    },

    # Deterministic title generation
    "TITLE_DETERMINISM": {
        "use_primary_keyword": True,
        "use_benefit": True,
        "use_brand": True,
        "fallback_to_base_title": True,
    },

    # Deterministic metafield generation
    "METAFIELD_DETERMINISM": {
        "use_editorial_for_long_description": True,
        "use_benefits_for_key_benefits": True,
        "use_routine_steps_for_routine": True,
        "use_persona_for_brand_voice": True,
        "use_emotional_axes_for_emotional_axis": True,
    },
} 