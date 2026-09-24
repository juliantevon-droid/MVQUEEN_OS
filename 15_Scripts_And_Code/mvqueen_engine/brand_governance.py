"""Canonical MVQUEEN brand-language governance helpers.

This module reads the source-of-truth markdown files directly. It does not
generate claims or product facts and performs no network I/O.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]

BRAND_GOVERNANCE_SOURCES = (
    "01_Brand_Strategy/Brand_Bible.md",
    "02_Brand_Identity/brand_vocabulary.md",
    "06_Tone_And_Voice/Brand_Vocabulary_Banks.md",
    "06_Tone_And_Voice/Forbidden_Words.md",
    "06_Tone_And_Voice/Product_Description_Voice.md",
    "06_Tone_And_Voice/Tone_Guide.md",
    "06_Tone_And_Voice/Voice_Consistency_Rules.md",
    "06_Tone_And_Voice/Writing_Rules.md",
)

LEGACY_SISTER_BRANDS = (
    "MISS." + "QUEEN",
    "MISS " + "QUEEN",
)

SUPPLIER_AND_REFERENCE_BRANDS = (
    *LEGACY_SISTER_BRANDS,
    # Suppliers / historical vendor identities
    "OUHOE", "HOEGOA", "FANZHEN", "EELHOPE", "COLOR FIT",
    "WEST & MONTH", "WEST&MONTH", "EPROLO", "DROPSURE", "JAYSUING",
    "ROXELIS", "DESIRE GEM", "MIA JEWELRY",
    # Reference brands: inspiration only, never product identity
    "SEPHORA", "VICTORIA'S SECRET", "VICTORIAS SECRET",
    "FENTY BEAUTY", "DIOR",
    # Manufacturer/brand prefixes confirmed in the recovered catalog
    "QIBEST", "IBEST", "EELHOE", "HANDAIYAN", "O.TWO.O", "PUDAIER",
    "IMAGIC", "HOYGI", "ZEPHOCO", "NICEFACE", "OCEAURA", "CMAADU",
    "MENOW", "M.N MENOW", "UCANBE", "CAKAILA", "KA CAYLA", "UBUB",
    "FOCALLURE", "MISSROSE", "MISS ROSE", "ZEESEA", "BREYLEE", "KOEC",
    "MYS", "BEAUTY GLAZED", "HOLD LIVE", "MARSKE", "LAVDIK", "FANA",
    "POPFEEL", "LANBENA", "DEROL", "HENGFEI", "LULAA", "MUSIC FLOWER",
    "SKIN EVER", "D.S.M", "TINT MY", "WOODSLEEP", "HOUKEA",
    "ROMANTIC BEAUTY",
)


def require_sources() -> None:
    missing = [rel for rel in BRAND_GOVERNANCE_SOURCES if not (REPO_ROOT / rel).exists()]
    if missing:
        raise RuntimeError(f"Missing canonical brand governance sources: {missing}")


def load_tier1_forbidden_terms() -> tuple[str, ...]:
    require_sources()
    text = (REPO_ROOT / "06_Tone_And_Voice/Forbidden_Words.md").read_text(
        encoding="utf-8"
    )
    try:
        section = text.split("## Tier 1", 1)[1].split("## Tier 2", 1)[0]
    except IndexError as exc:
        raise RuntimeError("Unable to locate Tier 1 forbidden-language section") from exc

    terms: list[str] = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        phrase = cells[0]
        if not phrase or phrase.lower() == "word / phrase" or set(phrase) <= {"-", ":"}:
            continue
        phrase = re.sub(r"\s*\([^)]*\)\s*$", "", phrase).strip()
        for part in re.split(r"\s+/\s+", phrase):
            part = part.strip()
            if part:
                terms.append(part)
    return tuple(dict.fromkeys(terms))


def contains_term(text: str, term: str) -> bool:
    """Match a governed term as a phrase/token, not as a substring of a word."""
    if not term:
        return False
    pattern = re.compile(r"(?<!\\w)" + re.escape(term) + r"(?!\\w)", re.I)
    return bool(pattern.search(str(text or "")))


def find_tier1_violations(text: str, terms: Iterable[str] | None = None) -> list[str]:
    pool = tuple(terms or load_tier1_forbidden_terms())
    return [term for term in pool if contains_term(text, term)]


__all__ = [
    "BRAND_GOVERNANCE_SOURCES",
    "LEGACY_SISTER_BRANDS",
    "SUPPLIER_AND_REFERENCE_BRANDS",
    "require_sources",
    "load_tier1_forbidden_terms",
    "find_tier1_violations",
]
