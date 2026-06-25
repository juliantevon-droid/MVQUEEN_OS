 # mvqueen_engine/editorial/frames.py
"""
MVQueen Editorial Frames — Enterprise Edition
---------------------------------------------

Frames are modular editorial structures that wrap or shape content.
They allow the engine to:
- Add emotional context
- Add atmospheric tone
- Add persona-driven nuance
- Add sensory framing
- Add cinematic presence

Frames are used to:
- Wrap descriptions
- Add intros or outros
- Build layered editorial moments
- Create consistent MVQueen tone across modules

All frames are:
- women-centered
- cinematic
- sensory
- atmospheric
- luxury-hybrid
- MVQueen-aligned
"""

from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    EMOTIONAL_LANGUAGE,
    ATMOSPHERIC_LANGUAGE,
    SENSORY_LANGUAGE,
)

from mvqueen_engine.utils import choose_safe


# ------------------------------------------------------------
# FRAME TEMPLATES — Cinematic, Feminine, MVQueen-Aligned
# ------------------------------------------------------------
INTRO_FRAMES = [
    "A moment shaped by {emotional} energy and {sensory} softness.",
    "An expression of {emotional} presence wrapped in {sensory} texture.",
    "A softly cinematic opening touched with {emotional} warmth.",
]

OUTRO_FRAMES = [
    "Finished with a {emotional} aura and {sensory} ease.",
    "A closing note of {emotional} clarity and {sensory} comfort.",
    "Wrapped in a final breath of {atmosphere}.",
]

WRAP_FRAMES = [
    "{intro} {content} {outro}",
    "{content} {outro}",
    "{intro} {content}",
]


# ------------------------------------------------------------
# GENERATOR FUNCTIONS — Modular, Cinematic, Sensory
# ------------------------------------------------------------
def generate_intro_frame() -> str:
    """Returns a cinematic MVQueen intro frame."""
    return choose_safe(INTRO_FRAMES).format(
        emotional=choose_safe(EMOTIONAL_LANGUAGE),
        sensory=choose_safe(SENSORY_LANGUAGE),
    )


def generate_outro_frame() -> str:
    """Returns a cinematic MVQueen outro frame."""
    return choose_safe(OUTRO_FRAMES).format(
        emotional=choose_safe(EMOTIONAL_LANGUAGE),
        sensory=choose_safe(SENSORY_LANGUAGE),
        atmosphere=choose_safe(ATMOSPHERIC_LANGUAGE),
    )


def wrap_with_frames(content: str) -> str:
    """
    Wraps editorial content in MVQueen intro/outro frames.

    Returns:
        str
    """
    intro = generate_intro_frame()
    outro = generate_outro_frame()

    template = choose_safe(WRAP_FRAMES)

    return template.format(
        intro=intro,
        content=content,
        outro=outro,
    ).strip()

def generate_frames(content: str) -> str:
    """
    Unified public API for editorial framing.
    """
    return wrap_with_frames(content)


__all__ = [
    "generate_intro_frame",
    "generate_outro_frame",
    "wrap_with_frames",
    "generate_frames",
]