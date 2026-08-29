"""Smoke tests for brand banks."""
from mvqueen_engine.brand_brain.brand_banks.fashion_banks import FASHION_BANK
from mvqueen_engine.brand_brain.brand_banks.beauty_banks import BEAUTY_BANK
from mvqueen_engine.brand_brain.brand_banks.skincare_banks import SKINCARE_BANK


def test_brand_banks_are_available():
    for bank in (FASHION_BANK, BEAUTY_BANK, SKINCARE_BANK):
        assert bank
        assert isinstance(bank, (list, tuple, dict))
