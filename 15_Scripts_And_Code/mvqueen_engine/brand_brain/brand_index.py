"""Central registry for MVQueen controlled vocabulary banks."""
from __future__ import annotations

from .brand_banks import beauty_banks, business_banks, extra_banks, fashion_banks, persona_banks, seo_banks, skincare_banks

BANKS = {
    "fashion": fashion_banks,
    "beauty": beauty_banks,
    "skincare": skincare_banks,
    "seo": seo_banks,
    "persona": persona_banks,
    "business": business_banks,
    "extra": extra_banks,
}


def get_bank(name: str):
    """Return a registered bank module by canonical name."""
    try:
        return BANKS[name]
    except KeyError as exc:
        raise KeyError(f"Unknown MVQueen brand bank: {name}") from exc


def get_vocab(name: str, attribute: str):
    """Return one vocabulary collection from a registered bank."""
    bank = get_bank(name)
    try:
        return getattr(bank, attribute)
    except AttributeError as exc:
        raise AttributeError(f"Bank '{name}' has no vocabulary '{attribute}'") from exc


__all__ = ["BANKS", "get_bank", "get_vocab"]
