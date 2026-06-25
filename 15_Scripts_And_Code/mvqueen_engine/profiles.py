# persona/profiles.py
"""
MVQueen Persona Profiles — Enterprise Edition
---------------------------------------------

Defines the core identity profiles for each persona.
These profiles shape:
- editorial tone
- emotional presence
- sensory language
- movement language
- SEO emphasis
- product storytelling

Personas are:
- women-centered
- cinematic
- sensory
- atmospheric
- luxury-hybrid
"""

PERSONA_PROFILES = {
    "romantic": {
        "identity": "Soft, feminine, warm, emotionally open.",
        "emotion": "romantic glow",
        "sensory": "petal-soft texture",
        "movement": "gentle, flowing motion",
        "tone": "warm, poetic, dreamy",
    },
    "confident": {
        "identity": "Modern, elevated, clean, self-assured.",
        "emotion": "soft confidence",
        "sensory": "sleek, refined texture",
        "movement": "smooth, intentional motion",
        "tone": "crisp, sculpted, elevated",
    },
    "minimalist": {
        "identity": "Quiet, refined, understated, serene.",
        "emotion": "quiet radiance",
        "sensory": "weightless clarity",
        "movement": "calm, fluid motion",
        "tone": "clean, airy, minimal",
    },
    "editorial": {
        "identity": "Cinematic, atmospheric, expressive.",
        "emotion": "soft-focus emotion",
        "sensory": "dimensional texture",
        "movement": "sculpted, directional motion",
        "tone": "artistic, moody, elevated",
    },
    "glam": {
        "identity": "Luminous, feminine, radiant, sensual.",
        "emotion": "luminous calm",
        "sensory": "glow-rich texture",
        "movement": "smooth, spotlight-ready motion",
        "tone": "radiant, polished, glamorous",
    },
    "soft": {
        "identity": "Tender, delicate, gentle, airy.",
        "emotion": "gentle clarity",
        "sensory": "cloud-soft texture",
        "movement": "light, drifting motion",
        "tone": "whisper-soft, airy, delicate",
    },
    "bold": {
        "identity": "Striking, empowered, sculpted, expressive.",
        "emotion": "fluid strength",
        "sensory": "structured texture",
        "movement": "strong, directional motion",
        "tone": "assertive, sculpted, modern",
    },
}

__all__ = ["PERSONA_PROFILES"]