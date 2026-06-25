# testing/test_detection.py
"""
MVQueen Detection Engine Tests
------------------------------

Validates:
- Category detection
- Vibe detection
- Trend detection
- Persona routing integration
"""

from detection.router import detect_category, detect_vibe, detect_trend
from persona.router import route_persona


def test_category_detection():
    sample = "A soft ribbed knit sweater with a relaxed fit"
    result = detect_category(sample)
    assert isinstance(result, str)
    assert len(result) > 0


def test_vibe_detection():
    sample = "sleek minimal black satin dress"
    result = detect_vibe(sample)
    assert isinstance(result, str)
    assert len(result) > 0


def test_trend_detection():
    sample = "oversized blazer with padded shoulders"
    result = detect_trend(sample)
    assert isinstance(result, str)
    assert len(result) > 0


def test_persona_routing():
    sample = "romantic lace bodysuit"
    persona = route_persona(sample)
    assert persona in ["editorial", "sephora", "vsangel"]


if __name__ == "__main__":
    test_category_detection()
    test_vibe_detection()
    test_trend_detection()
    test_persona_routing()
    print("Detection tests passed.")