# testing/test_processor.py
"""
MVQueen Catalog Processor Tests
-------------------------------

Validates:
- Metafield generation
- Tag generation
- Collection routing
- Bundle generation
- Schema integrity
"""

from catalog_processor.metafields import build_metafields
from catalog_processor.tags import generate_tags
from catalog_processor.collection import assign_collections
from catalog_processor.bundle_generator import generate_bundles
from catalog_processor.schema import validate_schema


def test_metafields():
    sample = {
        "title": "Black Satin Dress",
        "category": "dress",
        "vibe": "romantic",
        "trend": "timeless",
    }

    mf = build_metafields(sample)
    assert isinstance(mf, dict)
    assert "category" in mf
    assert "vibe" in mf


def test_tags():
    tags = generate_tags("black satin dress", "romantic", "timeless")
    assert isinstance(tags, list)
    assert len(tags) > 0


def test_collections():
    cols = assign_collections("dress", "romantic", "timeless")
    assert isinstance(cols, list)
    assert len(cols) > 0


def test_bundles():
    bundles = generate_bundles(["dress", "heels", "bag"])
    assert isinstance(bundles, list)


def test_schema_validation():
    sample = {
        "title": "Black Satin Dress",
        "category": "dress",
        "vibe": "romantic",
        "trend": "timeless",
    }

    assert validate_schema(sample) is True


if __name__ == "__main__":
    test_metafields()
    test_tags()
    test_collections()
    test_bundles()
    test_schema_validation()
    print("Catalog processor tests passed.")