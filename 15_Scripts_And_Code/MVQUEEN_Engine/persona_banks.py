# mvqueen_engine/brand_brain/brand_banks/persona_banks.py
"""
MVQueen Persona Banks — BRAND TONE INFUSED VERSION

These personas are built directly from the MVQueen brand DNA:
- Sephora (beauty-forward, confident, modern, sensory)
- MVQueen (luxury-hybrid, editorial, poetic, cinematic, women-centered)
- Victoria’s Secret (feminine, sensual, glamorous, body-aware)

Every persona is:
- women-centered
- emotionally intelligent
- sensory and atmospheric
- confident without aggression
- poetic without losing clarity
- luxury-driven but warm
- modern, fluid, and editorial
- softly seductive without being explicit
- aligned with movement, silhouette, and texture

These personas shape:
- titles
- descriptions
- SEO
- benefit copy
- vibe/trend alignment
- emotional framing
- sensory language
"""

# ------------------------------------------------------------
# PERSONA KEYWORDS — MVQueen Signature Archetypes
# ------------------------------------------------------------
PERSONA_KEYWORDS = {
    "Runway Muse": [
        "cinematic", "runway", "editorial", "high_fashion", "sensory", "fluid",
        "spotlight", "movement", "glow", "soft_drama", "artful", "luminous",
        "silhouette", "statement", "impact", "poetic", "elevated", "modern",
        "fashion_forward", "couture", "camera_ready", "glide", "sleek", "refined",
        "magnetic", "presence", "aura", "polished", "clean_lines", "soft_edge",
        "luxury_moment", "quiet_drama", "skin_first", "radiant", "glossed",
        "diffused", "soft_focus", "runway_energy", "cinematic_glow",
        "editorial_sharp", "high_presence", "spotlight_ready", "movement_driven",
        "silk_motion", "gloss_light", "studio_finish", "fashion_lens",
        "model_energy", "camera_pull", "soft_flash", "runway_sheen",
        "hyper_modern", "art_direction", "fashion_sculpted", "clean_silhouette",
        "elevated_texture", "skin_architecture", "soft_glide", "liquid_motion",
        "high_glow", "soft_reflection", "diffused_edges", "runway_precision",
        "couture_softness", "editorial_depth", "cinematic_softness",
        "fashion_poetry", "movement_poetry", "spotlight_silhouette",
        "studio_glow", "runway_clarity", "high_definition", "soft_definition",
        "luxury_film", "camera_sculpted", "fashion_intent", "editorial_intent",
        "runway_pull", "magnetic_motion", "soft_sculpt", "skin_sculpt",
        "fashion_energy", "couture_energy", "cinematic_presence",
        "editorial_presence", "runway_precision", "movement_precision",
        "soft_power", "quiet_power", "elevated_power", "fashion_power",
        "skin_cinema", "skin_drama", "skin_poetry", "skin_movement",
        "runway_softness", "couture_glow", "editorial_glow", "cinematic_finish",
        "fashion_finish", "movement_finish", "luxury_finish"
    ],

    "Soft Minimalist": [
        "minimal", "clean", "refined", "quiet_luxury", "intentional", "calm",
        "clarity", "soft_lines", "understated", "elevated_basics", "pure",
        "neutral", "polished", "serene", "fresh", "light", "effortless",
        "pared_back", "soft_glow", "skin_like", "second_skin", "smooth",
        "balanced", "subtle", "gentle", "restraint", "precision", "quiet",
        "soft_matte", "airy", "weightless", "natural_finish", "soft_structure",
        "clean_silhouette", "timeless_minimal", "refined_ease", "calm_presence",
        "soft_geometry", "neutral_palette", "skin_tone_harmony", "soft_edges",
        "intentional_lines", "quiet_strength", "soft_balance", "clean_finish",
        "skin_clarity", "soft_neutral", "elevated_neutral", "minimal_glow",
        "soft_dimension", "light_dimension", "skin_simplicity", "pure_texture",
        "soft_refinement", "quiet_refinement", "calm_glow", "calm_sculpt",
        "soft_sculpt", "minimal_sculpt", "clean_sculpt", "skin_minimalism",
        "soft_precision", "quiet_precision", "elevated_precision",
        "minimal_intention", "soft_intention", "clean_intention",
        "skin_breathability", "weightless_texture", "soft_breath", "quiet_breath",
        "skin_stillness", "skin_peace", "skin_balance", "skin_harmony",
        "minimal_harmony", "soft_harmony", "quiet_harmony", "refined_harmony",
        "neutral_softness", "neutral_clarity", "neutral_balance",
        "soft_modernity", "clean_modernity", "minimal_modernity",
        "skin_modernity", "soft_elegance", "quiet_elegance", "clean_elegance",
        "minimal_elegance", "skin_elegance", "soft_purity", "clean_purity",
        "minimal_purity", "skin_purity", "soft_focus_minimal", "quiet_focus",
        "clean_focus", "minimal_focus"
    ],

    "Romantic Visionary": [
        "romantic", "feminine", "soft", "dreamy", "fluid", "warm", "glow",
        "petal_soft", "rosy", "blush", "poetic", "tender", "emotional",
        "flowing", "gentle", "aura", "soft_shimmer", "dewy", "luminous",
        "whimsical", "delicate", "heart_led", "warmth", "embrace", "soft_focus",
        "hazy", "diffused_light", "feminine_energy", "soft_curves", "silky",
        "romance", "daydream", "soft_bloom", "warm_glow", "emotive", "fluidity",
        "soft_movement", "dreamlike_presence", "petal_glow", "rose_tone",
        "soft_blur", "romantic_blur", "warm_blur", "soft_radiance",
        "romantic_radiance", "feminine_radiance", "soft_luminance",
        "romantic_luminance", "warm_luminance", "skin_poetry", "skin_romance",
        "skin_softness", "skin_femininity", "soft_femininity", "warm_femininity",
        "romantic_femininity", "soft_emotion", "warm_emotion", "romantic_emotion",
        "soft_intimacy", "warm_intimacy", "romantic_intimacy", "soft_glow_poetry",
        "romantic_glow_poetry", "warm_glow_poetry", "soft_dream", "warm_dream",
        "romantic_dream", "soft_fantasy", "warm_fantasy", "romantic_fantasy",
        "soft_aura", "warm_aura", "romantic_aura", "soft_pull", "warm_pull",
        "romantic_pull", "soft_sheen", "warm_sheen", "romantic_sheen",
        "soft_light", "warm_light", "romantic_light", "soft_motion",
        "warm_motion", "romantic_motion", "soft_whisper", "warm_whisper",
        "romantic_whisper", "soft_blooming", "warm_blooming", "romantic_blooming"
    ],

    "Bold Architect": [
        "bold", "structured", "architectural", "sharp", "defined", "modern",
        "high_impact", "precision", "geometry", "clean_angles", "commanding",
        "sleek", "graphic", "statement", "power", "confidence", "edge",
        "sculpted", "contour", "intensity", "clarity", "directional",
        "future_forward", "strong_lines", "high_contrast", "crisp", "assertive",
        "editorial_edge", "modern_femme", "cut_glass", "striking", "impactful",
        "engineered", "intentional_structure", "bold_silhouette",
        "clean_geometry", "architectural_lines", "precision_edges",
        "graphic_sculpt", "modern_sculpt", "power_sculpt", "bold_sculpt",
        "high_definition", "clean_definition", "sharp_definition",
        "architectural_definition", "modern_definition", "power_definition",
        "bold_presence", "structured_presence", "modern_presence",
        "architectural_presence", "graphic_presence", "precision_presence",
        "engineered_presence", "impact_presence", "command_presence",
        "bold_energy", "structured_energy", "modern_energy",
        "architectural_energy", "graphic_energy", "precision_energy",
        "engineered_energy", "impact_energy", "command_energy",
        "bold_motion", "structured_motion", "modern_motion",
        "architectural_motion", "graphic_motion", "precision_motion",
        "engineered_motion", "impact_motion", "command_motion",
        "bold_intent", "structured_intent", "modern_intent",
        "architectural_intent", "graphic_intent", "precision_intent",
        "engineered_intent", "impact_intent", "command_intent"
    ],

    "Classic Strategist": [
        "classic", "timeless", "polished", "elegant", "refined", "intelligent",
        "enduring", "balanced", "sophisticated", "heritage", "iconic",
        "strategic", "composed", "poised", "clean", "structured", "smart",
        "luxury", "neutral", "evergreen", "smooth", "sleek", "graceful",
        "intention", "quiet_confidence", "soft_glamour", "body_aware",
        "tailored", "cultured", "elevated", "strategic_beauty",
        "timeless_glow", "refined_silhouette", "classic_finish",
        "intelligent_design", "heritage_lines", "polished_lines",
        "timeless_lines", "classic_lines", "refined_lines", "strategic_lines",
        "poised_lines", "elegant_lines", "classic_balance", "timeless_balance",
        "refined_balance", "strategic_balance", "poised_balance",
        "classic_presence", "timeless_presence", "refined_presence",
        "strategic_presence", "poised_presence", "classic_energy",
        "timeless_energy", "refined_energy", "strategic_energy",
        "poised_energy", "classic_motion", "timeless_motion",
        "refined_motion", "strategic_motion", "poised_motion",
        "classic_intent", "timeless_intent", "refined_intent",
        "strategic_intent", "poised_intent", "classic_elegance",
        "timeless_elegance", "refined_elegance", "strategic_elegance",
        "poised_elegance", "classic_glow", "timeless_glow", "refined_glow",
        "strategic_glow", "poised_glow"
    ],

    "Velvet Rebel": [
        "rebel", "undone", "sensual", "intimate", "cool", "moody", "velvet",
        "soft_edge", "smudged", "lived_in", "seductive", "shadow", "warm_depth",
        "mysterious", "magnetic", "dark_glow", "skin_close", "whisper_soft",
        "raw", "unpolished", "effortless_cool", "quiet_rebellion",
        "soft_smoke", "body_heat", "after_dark", "moody_glow", "soft_grit",
        "undone_glamour", "intimate_texture", "low_light", "slow_burn",
        "soft_shadow", "velvet_finish", "cool_femme", "atmospheric",
        "subtle_danger", "dark_sheen", "shadow_sheen", "moody_sheen",
        "velvet_sheen", "soft_darkness", "warm_darkness", "magnetic_darkness",
        "skin_shadow", "skin_heat", "skin_depth", "skin_intimacy",
        "soft_intensity", "warm_intensity", "dark_intensity",
        "rebel_intensity", "cool_intensity", "moody_intensity",
        "soft_rebellion", "warm_rebellion", "dark_rebellion",
        "cool_rebellion", "moody_rebellion", "soft_pull", "warm_pull",
        "dark_pull", "cool_pull", "moody_pull", "soft_smoulder",
        "warm_smoulder", "dark_smoulder", "cool_smoulder", "moody_smoulder",
        "soft_gravity", "warm_gravity", "dark_gravity", "cool_gravity",
        "moody_gravity", "soft_edge_glow", "warm_edge_glow", "dark_edge_glow",
        "cool_edge_glow", "moody_edge_glow"
    ],

    "Ethereal Siren": [
        "ethereal", "siren", "luminous", "glow", "feminine", "soft_aura",
        "atmospheric", "floaty", "radiant", "halo", "glistening", "silken",
        "weightless", "airy", "dreamlike", "celestial", "soft_shimmer",
        "moonlit", "goddess", "allure", "pull", "magnetic_softness",
        "skin_lit", "veil", "misty", "soft_glow", "angelic", "fluid",
        "whisper_light", "soft_radiance", "feminine_pull", "glow_aura",
        "cinematic_softness", "light_drenched", "soft_halo", "atmospheric_glow",
        "moon_glow", "star_glow", "celestial_glow", "soft_light",
        "dream_light", "halo_light", "veil_light", "mist_light",
        "ethereal_light", "siren_light", "soft_pull", "gentle_pull",
        "magnetic_pull", "feminine_pull", "soft_motion", "float_motion",
        "glide_motion", "halo_motion", "veil_motion", "mist_motion",
        "ethereal_motion", "siren_motion", "soft_presence", "glow_presence",
        "halo_presence", "veil_presence", "mist_presence", "ethereal_presence",
        "siren_presence", "soft_energy", "glow_energy", "halo_energy",
        "veil_energy", "mist_energy", "ethereal_energy", "siren_energy",
        "soft_finish", "glow_finish", "halo_finish", "veil_finish",
        "mist_finish", "ethereal_finish", "siren_finish"
    ],
}

# ------------------------------------------------------------
# PERSONA NAMES — MVQueen Signature Archetypes
# ------------------------------------------------------------
PERSONA_NAMES = [
    "Runway Muse",
    "Soft Minimalist",
    "Romantic Visionary",
    "Bold Architect",
    "Classic Strategist",
    "Velvet Rebel",
    "Ethereal Siren",
]

# ------------------------------------------------------------
# PERSONA TONES — Editorial Voice Profiles
# ------------------------------------------------------------
PERSONA_TONES = {
    "Runway Muse": (
        "cinematic, sensory, high-fashion; blends MVQueen’s poetic luxury "
        "with Sephora’s modern clarity and VS’s soft, luminous femininity"
    ),
    "Soft Minimalist": (
        "clean, refined, intentional; merges quiet luxury with Sephora’s "
        "polished confidence and MVQueen’s elevated restraint"
    ),
    "Romantic Visionary": (
        "feminine, fluid, warm; combines VS’s sensual glow with MVQueen’s "
        "dreamlike editorial softness and Sephora’s emotional clarity"
    ),
    "Bold Architect": (
        "structured, modern, high-impact; fuses MVQueen’s architectural "
        "precision with Sephora’s confident directness and VS’s feminine power"
    ),
    "Classic Strategist": (
        "timeless, polished, intelligent; blends MVQueen’s refined elegance "
        "with Sephora’s modernity and VS’s soft, body-aware glamour"
    ),
    "Velvet Rebel": (
        "sensual, undone, intimate; merges VS’s seductive softness with "
        "MVQueen’s atmospheric tone and Sephora’s confident edge"
    ),
    "Ethereal Siren": (
        "luminous, feminine, atmospheric; combines VS’s glow with MVQueen’s "
        "cinematic aura and Sephora’s sensory clarity"
    ),
}

# ------------------------------------------------------------
# PERSONA CONFIDENCE SIGNATURES — Emotional Anchors
# ------------------------------------------------------------
PERSONA_CONFIDENCE = {
    "Runway Muse": "moves like the moment is already hers",
    "Soft Minimalist": "leads with quiet, effortless certainty",
    "Romantic Visionary": "softens every space she enters",
    "Bold Architect": "commands attention without raising her voice",
    "Classic Strategist": "chooses intention over noise",
    "Velvet Rebel": "breaks rules softly and beautifully",
    "Ethereal Siren": "glows with an unspoken pull",
}

# ------------------------------------------------------------
# PERSONA ENERGY — Emotional + Editorial Energy Axes
# ------------------------------------------------------------
PERSONA_ENERGY = {
    "Runway Muse": "high sensory, high presence, fluid movement",
    "Soft Minimalist": "low drama, high refinement, calm clarity",
    "Romantic Visionary": "warm, soft, emotionally expressive",
    "Bold Architect": "high impact, sharp structure, modern edge",
    "Classic Strategist": "balanced, timeless, composed strength",
    "Velvet Rebel": "cool, intimate, undone sensuality",
    "Ethereal Siren": "soft glow, feminine pull, atmospheric allure",
}

# ------------------------------------------------------------
# PERSONA EDITORIAL SIGNATURES — How They Describe Products
# ------------------------------------------------------------
PERSONA_EDITORIAL_STYLE = {
    "Runway Muse": [
        "frames the silhouette with quiet drama",
        "creates a soft cinematic moment",
        "brings artful movement to everyday luxury",
    ],
    "Soft Minimalist": [
        "elevates simplicity with intentional detail",
        "brings calm clarity to the silhouette",
        "softens structure with refined ease",
    ],
    "Romantic Visionary": [
        "wraps the body in feminine fluidity",
        "adds softness to every line",
        "creates a warm, dreamlike presence",
    ],
    "Bold Architect": [
        "defines the form with modern precision",
        "creates high-impact structure",
        "commands attention through clean geometry",
    ],
    "Classic Strategist": [
        "balances elegance with intelligent design",
        "brings timeless polish to the silhouette",
        "creates a refined, enduring presence",
    ],
    "Velvet Rebel": [
        "adds intimate, undone sensuality",
        "brings a soft-edge cool to the silhouette",
        "creates a quiet, irresistible pull",
    ],
    "Ethereal Siren": [
        "glows softly against the skin",
        "creates a luminous, feminine aura",
        "adds atmospheric allure to every movement",
    ],
}

__all__ = [
    "PERSONA_KEYWORDS",                                "PERSONA_NAMES",
    "PERSONA_TONES",
    "PERSONA_CONFIDENCE",
    "PERSONA_ENERGY",
    "PERSONA_EDITORIAL_STYLE",
]