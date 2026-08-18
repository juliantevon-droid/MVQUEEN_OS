"""Canonical MVQueen persona profiles.

These profiles preserve the persona concepts already present in MVQUEEN_OS while
making them available to the new modular engine. They are data-first so editorial
and detection layers can consume the same vocabulary without duplicating rules.
"""

from __future__ import annotations

PERSONA_PROFILES = {
    "soft_luxury": {
        "name": "Soft Luxury",
        "adjectives": ["silky", "luminous", "romantic", "gentle", "glowing", "weightless", "velvety"],
        "cta": ["Slip into softness.", "Wrap yourself in quiet luxury.", "Let softness lead the moment."],
        "seo_focus": ["soft luxury dress", "romantic satin outfit", "feminine evening look"],
        "voice": "soft, intimate, luminous, understated",
    },
    "clinical_chic": {
        "name": "Clinical Chic",
        "adjectives": ["clean", "precise", "refined", "minimal", "structured", "polished", "streamlined"],
        "cta": ["Refine your uniform.", "Step into clean precision.", "Let structure speak for you."],
        "seo_focus": ["minimalist outfit", "clean girl aesthetic", "tailored modern look"],
        "voice": "precise, intelligent, polished, restrained",
    },
    "modern_confident": {
        "name": "Modern Confident",
        "adjectives": ["sculpted", "bold", "defined", "confident", "sharp", "striking", "empowered"],
        "cta": ["Own the room.", "Step into your power.", "Lead with presence."],
        "seo_focus": ["bodycon dress", "confidence outfit", "night out look"],
        "voice": "direct, confident, powerful, modern",
    },
    "mvqueen_signature": {
        "name": "MVQueen Signature",
        "adjectives": ["elevated", "polished", "luxurious", "refined", "timeless", "intentional"],
        "cta": ["Build your MVQueen wardrobe.", "Elevate your everyday.", "Make this a signature staple."],
        "seo_focus": ["MVQueen outfit", "elevated basics", "luxury everyday style"],
        "voice": "luxurious, confident, intentional, signature",
    },
    "miss_queen_style": {
        "name": "MISS.QUEEN Style",
        "adjectives": ["playful", "flirty", "sweet", "youthful", "chic", "lighthearted"],
        "cta": ["Make it a MISS.QUEEN moment.", "Play with your style.", "Keep it cute, keep it chic."],
        "seo_focus": ["cute outfit", "flirty dress", "youthful chic style"],
        "voice": "playful, feminine, flirty, light",
    },
    "editorial_couture": {
        "name": "Editorial Couture",
        "adjectives": ["dramatic", "runway-ready", "sculptural", "statement", "directional", "couture-inspired"],
        "cta": ["Make it a cover moment.", "Turn every entrance into a scene.", "Wear it like a headline."],
        "seo_focus": ["runway dress", "editorial outfit", "statement look"],
        "voice": "dramatic, editorial, directional, fashion-led",
    },
    "minimalist_luxe": {
        "name": "Minimalist Luxe",
        "adjectives": ["understated", "clean", "quiet", "refined", "streamlined", "subtle"],
        "cta": ["Invest in quiet luxury.", "Build your capsule.", "Let simplicity speak."],
        "seo_focus": ["minimalist dress", "quiet luxury outfit", "capsule wardrobe piece"],
        "voice": "understated, calm, refined, timeless",
    },
    "sensory_beauty": {
        "name": "Sensory Beauty",
        "adjectives": ["velvety", "buttery", "cloud-soft", "cooling", "breathable", "second-skin"],
        "cta": ["Feel the difference.", "Let texture lead.", "Wear what feels like you."],
        "seo_focus": ["comfortable dress", "soft fabric outfit", "second skin feel"],
        "voice": "sensory, tactile, intimate, comfort-focused",
    },
    "runway_modernity": {
        "name": "Runway Modernity",
        "adjectives": ["sharp", "structured", "angular", "directional", "modern", "architectural"],
        "cta": ["Step into the future.", "Wear the runway.", "Make modern your signature."],
        "seo_focus": ["structured dress", "modern outfit", "fashion forward look"],
        "voice": "architectural, sharp, modern, directional",
    },
    "feminine_empowerment": {
        "name": "Feminine Empowerment",
        "adjectives": ["uplifting", "confident", "radiant", "soft-strong", "empowering", "glowing"],
        "cta": ["Own your moment.", "Dress like you already are her.", "Let your presence speak."],
        "seo_focus": ["feminine outfit", "confidence dress", "empowering style"],
        "voice": "uplifting, radiant, confident, soft-strong",
    },
}


def get_persona_profile(persona: str | None) -> dict:
    """Return a safe persona profile, defaulting to MVQueen Signature."""
    key = str(persona or "").strip().lower().replace(" ", "_").replace(".", "")
    return PERSONA_PROFILES.get(key, PERSONA_PROFILES["mvqueen_signature"])
