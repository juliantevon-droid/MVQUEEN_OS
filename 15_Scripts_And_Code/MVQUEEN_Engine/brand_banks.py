# mvqueen_engine/brand_brain/brand_banks.py
"""
PHASE 1 — BRAND BANKS

All creative identity lives here:
- Personas (10)
- Persona profiles (adjectives, bullets, CTAs, SEO focus, metafield defaults)
- Sensory language
- Fashion vocabulary
- Occasion / Fit / Material / Style banks
- Emotional micro-phrases
- Luxury finishers
- SEO keyword banks
- Default metafields
"""

from mvqueen_engine.config import BRAND_NAME

# ---------------------------------------------
# PERSONAS
# ---------------------------------------------

PERSONAS = [
    "Soft Luxury",
    "Clinical Chic",
    "Modern Confident",
    "MVQueen Signature",
    "MISS.QUEEN Style",
    "Editorial Couture",
    "Minimalist Luxe",
    "Sensory Beauty",
    "Runway Modernity",
    "Feminine Empowerment",
]

# Persona profiles: vocab, bullets, CTAs, SEO focus, metafield flavor
PERSONA_PROFILES = {
    "soft_luxury": {
        "adjectives": [
            "silky", "luminous", "satin-soft", "romantic", "gentle", "glowing", "soft-focus",
            "weightless", "cloud-light", "velvety"
        ],
        "bullets": [
            "Softly sculpts the silhouette with a satin-soft finish.",
            "Wraps the body in luminous, romantic ease.",
            "Designed for evenings where subtle luxury speaks loudest.",
            "Glides against the skin with a weightless, cloud-light feel.",
            "Pairs effortlessly with delicate jewelry and soft glam."
        ],
        "cta": [
            "Slip into softness.",
            "Wrap yourself in quiet luxury.",
            "Let softness lead the moment."
        ],
        "seo_focus": ["soft luxury dress", "romantic satin outfit", "feminine evening look"],
        "metafield_flavor": "Silky, luminous, romantic, soft-focus luxury."
    },
    "clinical_chic": {
        "adjectives": [
            "clean", "precise", "refined", "minimal", "structured", "polished", "streamlined"
        ],
        "bullets": [
            "Clean lines and precise tailoring for a clinical-chic finish.",
            "Minimalist structure that feels intentional and elevated.",
            "Designed for women who prefer quiet, intelligent style.",
            "Pairs seamlessly with sharp accessories and modern beauty.",
            "A refined essential for workday polish and beyond."
        ],
        "cta": [
            "Refine your uniform.",
            "Step into clean precision.",
            "Let structure speak for you."
        ],
        "seo_focus": ["minimalist outfit", "clean girl aesthetic", "tailored modern look"],
        "metafield_flavor": "Clean, precise, minimal, refined modernity."
    },
    "modern_confident": {
        "adjectives": [
            "sculpted", "bold", "defined", "confident", "sharp", "striking", "empowered"
        ],
        "bullets": [
            "Sculpts the body with a confident, defined silhouette.",
            "Bold lines that move with you, not against you.",
            "Designed for women who lead the room, not follow.",
            "Pairs with statement heels and unapologetic energy.",
            "A modern essential for nights that matter."
        ],
        "cta": [
            "Own the room.",
            "Step into your power.",
            "Lead with presence."
        ],
        "seo_focus": ["bodycon dress", "confidence outfit", "night out look"],
        "metafield_flavor": "Sculpted, bold, empowered, modern confidence."
    },
    "mvqueen_signature": {
        "adjectives": [
            "elevated", "polished", "luxurious", "refined", "timeless", "intentional"
        ],
        "bullets": [
            "Signature MVQueen balance of polish and ease.",
            "Crafted for women who curate every detail.",
            "Designed to move from day to night with intention.",
            "Pairs with your favorite staples for effortless elevation.",
            "A core piece in the MVQueen wardrobe."
        ],
        "cta": [
            "Build your MVQueen wardrobe.",
            "Elevate your everyday.",
            "Make this a signature staple."
        ],
        "seo_focus": ["MVQueen outfit", "elevated basics", "luxury everyday style"],
        "metafield_flavor": "Elevated, polished, intentional, signature MVQueen energy."
    },
    "miss_queen_style": {
        "adjectives": [
            "playful", "flirty", "sweet", "youthful", "chic", "lighthearted"
        ],
        "bullets": [
            "Playful details that feel fun, not forced.",
            "Flirty silhouette with just the right amount of ease.",
            "Designed for weekends, dates, and everything in between.",
            "Pairs with sneakers or heels for instant mood lift.",
            "A sweet, chic piece for MISS.QUEEN moments."
        ],
        "cta": [
            "Make it a MISS.QUEEN moment.",
            "Play with your style.",
            "Keep it cute, keep it chic."
        ],
        "seo_focus": ["cute outfit", "flirty dress", "youthful chic style"],
        "metafield_flavor": "Playful, flirty, youthful, MISS.QUEEN energy."
    },
    "editorial_couture": {
        "adjectives": [
            "dramatic", "runway-ready", "sculptural", "statement", "directional", "couture-inspired"
        ],
        "bullets": [
            "Runway-inspired silhouette with sculptural lines.",
            "Designed for moments that deserve a statement.",
            "Directional details that photograph beautifully.",
            "Pairs with bold beauty and unapologetic styling.",
            "A couture-coded piece for editorial nights."
        ],
        "cta": [
            "Make it a cover moment.",
            "Turn every entrance into a scene.",
            "Wear it like a headline."
        ],
        "seo_focus": ["runway dress", "editorial outfit", "statement look"],
        "metafield_flavor": "Dramatic, sculptural, editorial couture energy."
    },
    "minimalist_luxe": {
        "adjectives": [
            "understated", "clean", "quiet", "refined", "streamlined", "subtle"
        ],
        "bullets": [
            "Understated lines with quiet luxury energy.",
            "Designed for women who prefer subtle impact.",
            "Pairs with minimal accessories and clean beauty.",
            "A refined essential for capsule wardrobes.",
            "Streamlined silhouette that never feels overdone."
        ],
        "cta": [
            "Invest in quiet luxury.",
            "Build your capsule.",
            "Let simplicity speak."
        ],
        "seo_focus": ["minimalist dress", "quiet luxury outfit", "capsule wardrobe piece"],
        "metafield_flavor": "Understated, clean, quiet, minimalist luxury."
    },
    "sensory_beauty": {
        "adjectives": [
            "velvety", "buttery", "cloud-soft", "cooling", "breathable", "second-skin"
        ],
        "bullets": [
            "Velvety feel that glides against the skin.",
            "Breathable comfort for all-day wear.",
            "Cooling, cloud-soft texture that moves with you.",
            "Feels like a second skin, looks like luxury.",
            "Designed for sensory-obsessed women."
        ],
        "cta": [
            "Feel the difference.",
            "Let texture lead.",
            "Wear what feels like you."
        ],
        "seo_focus": ["comfortable dress", "soft fabric outfit", "second skin feel"],
        "metafield_flavor": "Velvety, breathable, sensory-driven luxury."
    },
    "runway_modernity": {
        "adjectives": [
            "sharp", "structured", "angular", "directional", "modern", "architectural"
        ],
        "bullets": [
            "Sharp lines and structured shape for runway modernity.",
            "Architectural details that feel future-facing.",
            "Designed for women who love directional style.",
            "Pairs with sleek hair and bold accessories.",
            "A modern piece for fashion-forward wardrobes."
        ],
        "cta": [
            "Step into the future.",
            "Wear the runway.",
            "Make modern your signature."
        ],
        "seo_focus": ["structured dress", "modern outfit", "fashion forward look"],
        "metafield_flavor": "Sharp, structured, directional runway energy."
    },
    "feminine_empowerment": {
        "adjectives": [
            "uplifting", "confident", "radiant", "soft-strong", "empowering", "glowing"
        ],
        "bullets": [
            "Balances softness and strength in one silhouette.",
            "Designed to move with your body, not against it.",
            "Crafted for women who lead with heart and presence.",
            "Pairs with your favorite rituals of self-care.",
            "A reminder that femininity and power coexist."
        ],
        "cta": [
            "Own your moment.",
            "Dress like you already are her.",
            "Let your presence speak."
        ],
        "seo_focus": ["feminine outfit", "confidence dress", "empowering style"],
        "metafield_flavor": "Uplifting, radiant, soft-strong feminine empowerment."
    },
}

# ---------------------------------------------
# SENSORY LANGUAGE
# ---------------------------------------------

SENSORY_WORDS = [
    "silky", "weightless", "sculpted", "luminous", "velvety",
    "cooling", "breathable", "contouring", "satin-soft", "cloud-light",
    "buttery", "second-skin", "smooth", "soft-touch"
]

# ---------------------------------------------
# FASHION VOCABULARY
# ---------------------------------------------

FASHION_VOCAB = [
    "silhouette", "drape", "tailoring", "structure", "ruching",
    "pleating", "sculpted seams", "bias-cut", "fluid movement",
    "cinched waist", "clean neckline", "open back", "asymmetric hem"
]

# ---------------------------------------------
# OCCASION / FIT / MATERIAL / STYLE
# ---------------------------------------------

OCCASIONS = [
    "Evening elegance", "Weekend ease", "Workday polish",
    "Date-night confidence", "Resort escape", "Everyday luxury"
]

FITS = [
    "Bodycon", "Relaxed", "Tailored", "Sculpted", "Oversized", "Contour fit"
]

MATERIALS = [
    "Satin", "Modal", "Ribbed knit", "Sculpting stretch",
    "Silk blend", "Mesh", "Chiffon", "Jersey"
]

STYLES = [
    "Minimalist", "Glam", "Modern chic", "Street luxe",
    "Soft feminine", "Editorial"
]

# ---------------------------------------------
# EMOTIONAL MICRO-PHRASES
# ---------------------------------------------

EMOTIONAL_PHRASES = [
    "Feel unstoppable",
    "Embrace your radiance",
    "Elevate your everyday",
    "Step into confidence",
    "Own your moment",
    "Move with intention"
]

# ---------------------------------------------
# LUXURY FINISHERS
# ---------------------------------------------

LUXURY_FINISHERS = [
    "crafted for distinction",
    "designed to elevate your presence",
    "made for the woman who leads",
    "refined for modern elegance",
    "finished with premium detailing"
]

# ---------------------------------------------
# SEO KEYWORDS
# ---------------------------------------------

PRIMARY_KEYWORDS = [
    "MVQueen dress", "MVQueen outfit", "luxury womenswear", "elevated basics",
    "evening dress", "bodycon dress", "minimalist dress"
]

SECONDARY_KEYWORDS = [
    "quiet luxury", "soft feminine style", "modern chic outfit",
    "date night look", "capsule wardrobe piece", "editorial fashion"
]

# Master keyword pool (placeholder + extensible)
KEYWORDS_900 = list(set(PRIMARY_KEYWORDS + SECONDARY_KEYWORDS + [
    "soft luxury dress", "romantic satin outfit", "clean girl aesthetic",
    "tailored modern look", "confidence outfit", "night out look",
    "cute outfit", "flirty dress", "youthful chic style",
    "runway dress", "statement look", "capsule wardrobe",
    "comfortable dress", "second skin feel", "structured dress",
    "fashion forward look", "feminine outfit", "empowering style"
]))

# ---------------------------------------------
# TRUST BADGES / DEFAULT METAFIELDS
# ---------------------------------------------

TRUST_BADGES_BY_CATEGORY = {
    "General": "Cruelty-Free",
    "Dresses": "Premium Quality",
    "Loungewear": "Comfort-First",
    "Shapewear": "Sculpting Support",
}

DEFAULT_METAFIELDS = {
    "custom.care_instructions": "Handle with care. Follow garment label instructions.",
    "custom.return_policy": "Eligible for standard MVQueen return policy.",
    "custom.brand_story": (
        f"{BRAND_NAME} curates elevated essentials for women who lead with presence, "
        "softness, and intention."
    ),
}