# mvqueen_engine/brand_brain/editorial.py
"""
PHASE 1 — EDITORIAL ENGINE

Title + description templates using:
- Personas
- Persona profiles
- Sensory / fashion vocab
- Emotional phrases
- Luxury finishers
- SEO keyword stack
"""

from mvqueen_engine.config import BRAND_NAME
from mvqueen_engine.brand_brain.brand_language import (
    select_persona_from_handle,
    get_persona_profile,
    select_sensory_word,
    select_fashion_term,
    select_occasion,
    select_fit,
    select_style,
    select_emotional_phrase,
    select_luxury_finisher,
)
from mvqueen_engine.brand_brain.seo_keywords import get_keyword_stack
from mvqueen_engine.utils.deterministic import seed_from_text, pick_from_pool
from mvqueen_engine.utils.text_utils import strip_html
from mvqueen_engine.utils.deterministic import truncate

# ---------------------------------------------
# TITLE GENERATION
# ---------------------------------------------

def generate_title(base_title: str, handle: str) -> str:
    persona = select_persona_from_handle(handle)
    profile = get_persona_profile(persona)
    seeds = seed_from_text(handle + "_title")

    adj_pool = profile.get("adjectives", [])
    adj1 = pick_from_pool(adj_pool, seeds[1]) if adj_pool else ""
    adj2 = pick_from_pool(adj_pool, seeds[2]) if adj_pool else ""

    pieces = [BRAND_NAME, base_title]
    if adj1 or adj2:
        pieces.append("–")
        pieces.append(" ".join([w for w in [adj1.title(), adj2.title()] if w]))

    title = " ".join([p for p in pieces if p])
    return truncate(title, 65)

# ---------------------------------------------
# DESCRIPTION GENERATION
# ---------------------------------------------

def generate_description(base_title: str, handle: str, supplier_body_html: str = "") -> str:
    persona = select_persona_from_handle(handle)
    profile = get_persona_profile(persona)
    seeds = seed_from_text(handle + "_desc")

    sensory = select_sensory_word(handle)
    fashion_term = select_fashion_term(handle)
    occasion = select_occasion(handle)
    fit = select_fit(handle)
    style = select_style(handle)
    emotion = select_emotional_phrase(handle)
    finisher = select_luxury_finisher(handle)
    kw_stack = get_keyword_stack(handle)

    bullet_pool = profile.get("bullets", [])
    bullets = []
    if bullet_pool:
        from mvqueen_engine.utils.deterministic import pick_multiple
        bullets = pick_multiple(bullet_pool, seeds[3:], count=4)

    intro = (
        f"<p>{persona} expression of {base_title}, "
        f"crafted with a {sensory} feel and {fashion_term}-focused {fit.lower()} silhouette. "
        f"Perfect for {occasion.lower()}.</p>"
    )

    emotion_line = f"<p>{emotion}. {finisher.capitalize()}.</p>"

    seo_line = (
        f"<p>Styled for {style.lower()} wardrobes and optimized around "
        f"{kw_stack['focus'].lower()}.</p>"
    )

    bullet_html = ""
    if bullets:
        bullet_html = "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"

    supplier_clean = strip_html(supplier_body_html)
    supplier_block = f"<p>{supplier_clean}</p>" if supplier_clean else ""

    body = intro + emotion_line + seo_line + bullet_html + supplier_block
    return body