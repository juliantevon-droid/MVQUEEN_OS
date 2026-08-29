"""Smoke tests for detection modules."""
from mvqueen_engine.brand_brain.detection.detect_category import detect_category
from mvqueen_engine.brand_brain.detection.detect_product_type import detect_product_type


def test_category_returns_value():
    value = detect_category("Silk Evening Dress")
    assert isinstance(value, str)
    assert value


def test_product_type_returns_value():
    value = detect_product_type("Hydrating Face Serum")
    assert isinstance(value, str)
    assert value
