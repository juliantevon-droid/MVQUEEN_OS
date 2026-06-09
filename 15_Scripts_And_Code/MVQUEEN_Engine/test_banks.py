# testing/test_banks.py
"""
MVQueen Vocabulary Bank Tests
-----------------------------

Validates:
- Mood banks
- Vibe banks
- Trend banks
- Persona vocab
- Material vocab
- Silhouette vocab
- Brand brain integrity
"""

from brand_brain.brandindex import BRAND_INDEX


def test_brand_index_structure():
    assert isinstance(BRAND_INDEX, dict)
    assert "moods" in BRAND_INDEX
    assert "vibes" in BRAND_INDEX
    assert "trends" in BRAND_INDEX
    assert "materials" in BRAND_INDEX
    assert "silhouettes" in BRAND_INDEX


def test_moods():
    moods = BRAND_INDEX.get("moods", [])
    assert isinstance(moods, list)
    assert len(moods) > 0


def test_vibes():
    vibes = BRAND_INDEX.get("vibes", [])
    assert isinstance(vibes, list)
    assert len(vibes) > 0


def test_trends():
    trends = BRAND_INDEX.get("trends", [])
    assert isinstance(trends, list)
    assert len(trends) > 0


def test_materials():
    mats = BRAND_INDEX.get("materials", [])
    assert isinstance(mats, list)
    assert len(mats) > 0


def test_silhouettes():
    sil = BRAND_INDEX.get("silhouettes", [])
    assert isinstance(sil, list)
    assert len(sil) > 0


if __name__ == "__main__":
    test_brand_index_structure()
    test_moods()
    test_vibes()
    test_trends()
    test_materials()
    test_silhouettes()
    print("Bank tests passed.")