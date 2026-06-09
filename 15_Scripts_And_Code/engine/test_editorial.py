# testing/test_editorial.py
"""
MVQueen Editorial Engine Tests
------------------------------

Validates:
- Description generation
- Frame generation
- SEO block generation
- Persona tone blending
"""

from editorial.descriptions import generate_description
from editorial.frames import generate_frames
from editorial.seo import generate_seo_block
from persona.tone import apply_persona_tone


def test_description_generation():
    sample = {
        "title": "Satin Slip Dress",
        "category": "dress",
        "vibe": "romantic",
        "trend": "timeless",
    }

    desc = generate_description(sample)
    assert isinstance(desc, str)
    assert len(desc) > 50


def test_frames_generation():
    frames = generate_frames("A soft knit sweater")
    assert isinstance(frames, list)
    assert len(frames) > 0


def test_seo_block():
    seo = generate_seo_block("black satin dress", ["romantic", "timeless"])
    assert isinstance(seo, str)
    assert "dress" in seo.lower()


def test_persona_tone():
    text = "A soft knit sweater perfect for layering."
    toned = apply_persona_tone(text, "vsangel")
    assert isinstance(toned, str)
    assert toned != text  # tone should modify the text


if __name__ == "__main__":
    test_description_generation()
    test_frames_generation()
    test_seo_block()
    test_persona_tone()
    print("Editorial tests passed.")