# mvqueen_engine/brand_brain/brand_language.py
"""
PHASE 1 — BRAND LANGUAGE

Helpers to work with personas, profiles, CTAs, and language banks.
"""

from mvqueen_engine.brand_brain.brand_banks import (
    PERSONAS,
    PERSONA_PROFILES,
    SENSORY_WORDS,
    FASHION_VOCAB,
    OCCASIONS,
    FITS,
    MATERIALS,
    STYLES,
    EMOTIONAL_PHRASES,
    LUXURY_FINISHERS,
)

from mvqueen_engine.utils.deterministic import seed_from_text, pick_from_pool, pick_multiple

def get_persona_key(persona: str) -> str:
    return persona.lower().replace(" ", "_")

def get_persona_profile(persona: str) -> dict:
    key = get_persona_key(persona)
    return PERSONA_PROFILES.get(key, PERSONA_PROFILES["mvqueen_signature"])

def select_persona_from_handle(handle: str) -> str:
    seeds = seed_from_text(handle)
    return PERSONAS[seeds[0] % len(PERSONAS)]

def select_cta(persona: str, handle: str) -> str:
    profile = get_persona_profile(persona)
    ctas = profile.get("cta", [])
    seeds = seed_from_text(handle + "_cta")
    return pick_from_pool(ctas, seeds[1]) if ctas else ""

def select_sensory_word(handle: str) -> str:
    seeds = seed_from_text(handle + "_sensory")
    return pick_from_pool(SENSORY_WORDS, seeds[2])

def select_fashion_term(handle: str) -> str:
    seeds = seed_from_text(handle + "_fashion")
    return pick_from_pool(FASHION_VOCAB, seeds[3])

def select_occasion(handle: str) -> str:
    seeds = seed_from_text(handle + "_occasion")
    return pick_from_pool(OCCASIONS, seeds[4])

def select_fit(handle: str) -> str:
    seeds = seed_from_text(handle + "_fit")
    return pick_from_pool(FITS, seeds[5])

def select_material(handle: str) -> str:
    seeds = seed_from_text(handle + "_material")
    return pick_from_pool(MATERIALS, seeds[6])

def select_style(handle: str) -> str:
    seeds = seed_from_text(handle + "_style")
    return pick_from_pool(STYLES, seeds[7])

def select_emotional_phrase(handle: str) -> str:
    seeds = seed_from_text(handle + "_emotion")
    return pick_from_pool(EMOTIONAL_PHRASES, seeds[8])

def select_luxury_finisher(handle: str) -> str:
    seeds = seed_from_text(handle + "_finisher")
    return pick_from_pool(LUXURY_FINISHERS, seeds[9])