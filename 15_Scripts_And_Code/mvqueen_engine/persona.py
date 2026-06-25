PERSONAS = [
    "MVQueen Core",
    "MISS.QUEEN",
    "Victoria Soft Power",
    "Sephora Precision",
    "Runway Modern",
    "Clinical Chic",
    "Soft Luxury",
    "Glow Maestro",
    "Elegant Authority",
    "Street Luxe Femme",
]

PERSONA_CONFIG = {
    "MVQueen Core": {
        "tone": "luxury-confident-soft-feminine",
        "editorial_weight": "balanced",
        "default_editorial_length": "medium",
    },
    "MISS.QUEEN": {
        "tone": "playful-glam-feminine",
        "editorial_weight": "high-variation",
        "default_editorial_length": "medium",
    },
    "Runway Modern": {
        "tone": "editorial-bold-runway",
        "editorial_weight": "max-variation",
        "default_editorial_length": "long",
    },
    # Extend for all personas later
}

PERSONA_ADVANCED = {
    "MVQueen Core": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["soft", "sensual", "confident"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Elevate your routine.",
            "Feel the soft power.",
            "Confidence that whispers.",
        ],
        "metafield_overrides": {},
    },

    "MISS.QUEEN": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["playful", "glam", "feminine"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Glow up your glam.",
            "Play with luxury.",
            "Soft glam, big energy.",
        ],
        "metafield_overrides": {},
    },

    "Victoria Soft Power": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["elegant", "soft", "intentional"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Soft power, refined.",
            "Elegance in motion.",
            "Luxury with intention.",
        ],
        "metafield_overrides": {},
    },

    "Sephora Precision": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["clinical", "precise", "expert"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Clinically elevated.",
            "Precision meets beauty.",
            "Expert results, every time.",
        ],
        "metafield_overrides": {},
    },

    "Runway Modern": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["editorial", "bold", "modern"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Own the runway.",
            "Bold. Modern. You.",
            "Editorial energy unlocked.",
        ],
        "metafield_overrides": {},
    },

    "Clinical Chic": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["clean", "clinical", "minimal"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Clean beauty, elevated.",
            "Minimal. Clinical. Chic.",
            "Precision with softness.",
        ],
        "metafield_overrides": {},
    },

    "Soft Luxury": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["soft", "romantic", "luxurious"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Soft luxury, always.",
            "Romance the everyday.",
            "Luxury that whispers.",
        ],
        "metafield_overrides": {},
    },

    "Glow Maestro": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["radiant", "glowing", "uplifted"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Glow with intention.",
            "Radiance redefined.",
            "Your glow, elevated.",
        ],
        "metafield_overrides": {},
    },

    "Elegant Authority": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["elegant", "powerful", "refined"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Elegance in command.",
            "Refined power.",
            "Authority with grace.",
        ],
        "metafield_overrides": {},
    },

    "Street Luxe Femme": {
        "vocab_preferences": {
            "adjectives": [],
            "sensory_verbs": [],
            "confidence_phrases": [],
            "moods": [],
            "finishes": [],
            "textures": [],
        },
        "seo_bias": {
            "primary_keywords": [],
            "secondary_keywords": [],
        },
        "emotional_axes": ["street", "luxe", "feminine"],
        "editorial_structures": {
            "intro_frames": [],
            "body_frames": [],
            "fashion_frames": [],
            "closer_frames": [],
        },
        "cta_styles": [
            "Street meets luxury.",
            "Feminine with edge.",
            "Luxe energy, everyday.",
        ],
        "metafield_overrides": {},
    },
}
