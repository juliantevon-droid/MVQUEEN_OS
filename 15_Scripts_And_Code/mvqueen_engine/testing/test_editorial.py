"""Smoke tests for editorial generation."""
from mvqueen_engine.brand_brain.editorial.seo import generate_seo
from mvqueen_engine.brand_brain.editorial.titles import generate_title


def test_title_is_nonempty():
    value = generate_title("Classic Satin Dress", "classic-satin-dress", {})
    assert isinstance(value, str)
    assert value.strip()


def test_seo_has_required_fields():
    value = generate_seo("Classic Satin Dress", {})
    assert set(("seo_title", "seo_description")).issubset(value)
    assert value["seo_title"]
    assert value["seo_description"]
