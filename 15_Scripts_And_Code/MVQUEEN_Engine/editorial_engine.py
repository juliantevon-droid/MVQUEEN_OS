# ============================================================
# BLOCK 32 — EDITORIAL ENGINE (FINAL VERSION ARCHITECTURE)
# ============================================================

from __future__ import annotations
import random
from typing import Dict, Any, List, Optional

from engine.engine_core import (
    get_engine,
    select_persona,
    select_primary_keyword,
    select_vocabulary_pool,
    sanitize_text,
    ensure_list,
    with_seed,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def generate_editorial(product: Dict[str, Any]) -> str:
    """
    Main editorial generator.
    Persona-aware, SEO-aware, category-aware, deterministic.
    Uses:
      - VOCAB_BANKS
      - PERSONA_ENGINE
      - CATEGORY_ENGINE
      - EDITORIAL_ENGINE config
    """
    editorial_engine = get_engine("editorial") or {}
    persona_engine = get_engine("personas") or {}
    category_engine = get_engine("category") or {}

    persona = select_persona(product)
    primary_keyword = select_primary_keyword(product)
    category = product.get("category")

    vocab = select_vocabulary_pool(persona)
    persona_rules = _get_persona_rules(persona_engine, persona)
    category_rules = _get_category_rules(category_engine, category)

    with_seed(
        product.get("handle"),
        persona,
        primary_keyword,
        category,
    )

    frame = _select_editorial_frame(
        editorial_engine,
        persona_rules,
        category_rules,
        persona,
        product,
    )

    intro = _build_intro(
        frame, persona, vocab, persona_rules, category_rules, product, primary_keyword
    )
    body = _build_body(
        frame, persona, vocab, persona_rules, category_rules, product, primary_keyword
    )
    closer = _build_closer(
        frame, persona, vocab, persona_rules, category_rules, product, primary_keyword
    )

    html = _assemble_html(intro, body, closer, editorial_engine)
    return html


# ------------------------------------------------------------
# CONFIG HELPERS
# ------------------------------------------------------------

def _get_persona_rules(persona_engine: Dict[str, Any], persona: str) -> Dict[str, Any]:
    personas = persona_engine.get("personas", {})
    return personas.get(persona, personas.get("default", {}))


def _get_category_rules(category_engine: Dict[str, Any], category: Optional[str]) -> Dict[str, Any]:
    if not category:
        return {}
    categories = category_engine.get("categories", {})
    return categories.get(category, categories.get("default", {}))


# ------------------------------------------------------------
# FRAME SELECTION
# ------------------------------------------------------------

def _select_editorial_frame(
    editorial_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    persona: str,
    product: Dict[str, Any],
) -> Dict[str, Any]:
    frames_config = editorial_engine.get("frames", {})

    persona_frames = ensure_list(persona_rules.get("editorial_frames"))
    if persona_frames:
        return random.choice(persona_frames)

    category_frames = ensure_list(category_rules.get("editorial_frames"))
    if category_frames:
        return random.choice(category_frames)

    global_frames = ensure_list(frames_config.get("default"))
    if global_frames:
        return random.choice(global_frames)

    return {
        "id": "fallback_frame",
        "intro_template": "{persona} introduction about {keyword}.",
        "body_sections": [
            "Describe benefits for {keyword}.",
            "Describe textures and finishes.",
            "Describe mood and emotional payoff.",
        ],
        "closer_template": "Close with a confident, persona-aligned CTA.",
    }


# ------------------------------------------------------------
# INTRO BUILDER
# ------------------------------------------------------------

def _build_intro(
    frame: Dict[str, Any],
    persona: str,
    vocab: Dict[str, List[str]],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    product: Dict[str, Any],
    primary_keyword: str,
) -> str:
    template = frame.get("intro_template") or persona_rules.get("intro_template")
    if not template:
        template = "{persona} introduction about {keyword}."

    context = _build_context(
        persona, vocab, persona_rules, category_rules, product, primary_keyword
    )
    return template.format(**context)


# ------------------------------------------------------------
# BODY BUILDER
# ------------------------------------------------------------

def _build_body(
    frame: Dict[str, Any],
    persona: str,
    vocab: Dict[str, List[str]],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    product: Dict[str, Any],
    primary_keyword: str,
) -> str:
    sections = ensure_list(frame.get("body_sections"))
    if not sections:
        sections = [
            "Describe benefits for {keyword}.",
            "Describe textures and finishes.",
            "Describe mood and emotional payoff.",
        ]

    context = _build_context(
        persona, vocab, persona_rules, category_rules, product, primary_keyword
    )
    rendered: List[str] = []

    for section in sections:
        rendered.append(section.format(**context))

    return "\n".join(rendered)


# ------------------------------------------------------------
# CLOSER BUILDER
# ------------------------------------------------------------

def _build_closer(
    frame: Dict[str, Any],
    persona: str,
    vocab: Dict[str, List[str]],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    product: Dict[str, Any],
    primary_keyword: str,
) -> str:
    template = frame.get("closer_template") or persona_rules.get("closer_template")
    if not template:
        template = "Close with a confident, persona-aligned CTA."

    context = _build_context(
        persona, vocab, persona_rules, category_rules, product, primary_keyword
    )
    return template.format(**context)


# ------------------------------------------------------------
# CONTEXT BUILDER
# ------------------------------------------------------------

def _build_context(
    persona: str,
    vocab: Dict[str, List[str]],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    product: Dict[str, Any],
    primary_keyword: str,
) -> Dict[str, Any]:
    context: Dict[str, Any] = {
        "persona": persona,
        "keyword": primary_keyword,
        "category": product.get("category", ""),
        "brand": product.get("brand", ""),
        "title": product.get("title", ""),
        "handle": product.get("handle", ""),
    }

    adjectives = ensure_list(vocab.get("adjectives"))
    sensory_verbs = ensure_list(vocab.get("sensory_verbs"))
    confidence_phrases = ensure_list(vocab.get("confidence_phrases"))
    moods = ensure_list(vocab.get("moods"))
    finishes = ensure_list(vocab.get("finishes"))
    textures = ensure_list(vocab.get("textures"))
    benefits = ensure_list(vocab.get("benefits"))
    routines = ensure_list(vocab.get("routine_steps"))

    def pick(pool: List[str], fallback: str = "") -> str:
        if not pool:
            return fallback
        return random.choice(pool)

    context.update(
        {
            "adj": pick(adjectives),
            "adj2": pick(adjectives),
            "sensory_verb": pick(sensory_verbs),
            "sensory_verb2": pick(sensory_verbs),
            "confidence_phrase": pick(confidence_phrases),
            "mood": pick(moods),
            "finish": pick(finishes),
            "texture": pick(textures),
            "benefit": pick(benefits),
            "benefit2": pick(benefits),
            "routine_step": pick(routines),
        }
    )

    emotional_axes = ensure_list(persona_rules.get("emotional_axes"))
    ctas = ensure_list(persona_rules.get("cta_styles"))
    fashion_vocab = ensure_list(persona_rules.get("fashion_language"))

    context.update(
        {
            "emotional_axis": pick(emotional_axes),
            "cta": pick(ctas, "Discover the difference."),
            "fashion_phrase": pick(fashion_vocab),
        }
    )

    context["occasion"] = product.get("occasion") or pick(
        ensure_list(category_rules.get("occasions"))
    )
    context["skin_profile"] = product.get("skin_profile") or pick(
        ensure_list(category_rules.get("skin_profiles"))
    )
    context["routine_context"] = pick(
        ensure_list(category_rules.get("routine_contexts"))
    )

    return context


# ------------------------------------------------------------
# HTML ASSEMBLY
# ------------------------------------------------------------

def _assemble_html(
    intro: str,
    body: str,
    closer: str,
    editorial_engine: Dict[str, Any],
) -> str:
    html_rules = editorial_engine.get("html", {})

    intro_tag = html_rules.get("intro_tag", "p")
    body_tag = html_rules.get("body_tag", "p")
    closer_tag = html_rules.get("closer_tag", "p")

    def wrap(tag: str, content: str) -> str:
        tag = tag.strip("<>").lower()
        return f"<{tag}>{content}</{tag}>"

    return "\n".join(
        [
            wrap(intro_tag, intro),
            wrap(body_tag, body),
            wrap(closer_tag, closer),
        ]
    )