# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — TEXT CLEANING UTILITIES
# ---------------------------------------------------------

import re
from mvqueen_engine.config import BRAND_NAME


# ---------------------------------------------------------
# HTML STRIPPING
# ---------------------------------------------------------

def strip_html(html: str) -> str:
    """
    Remove HTML tags but preserve spacing.
    """
    if not isinstance(html, str):
        return ""

    # Remove tags
    text = re.sub(r"<[^>]+>", " ", html)

    # Collapse whitespace
    return " ".join(text.split())


# ---------------------------------------------------------
# WHITESPACE NORMALIZATION
# ---------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """
    Normalize all whitespace to single spaces.
    """
    if not isinstance(text, str):
        return ""

    # Replace all whitespace (tabs, newlines, unicode spaces)
    return " ".join(text.split())


# ---------------------------------------------------------
# BRAND ENFORCEMENT
# ---------------------------------------------------------

def enforce_brand(text: str) -> str:
    """
    Replace any MVQueen spelling with the configured BRAND_NAME.
    """
    if not isinstance(text, str):
        return ""

    # Case-insensitive replacement of MVQueen variants
    return re.sub(
        r"\bmvqueen\b",
        BRAND_NAME,
        text,
        flags=re.IGNORECASE
    ).strip()


# ---------------------------------------------------------
# FULL CLEANING PIPELINE
# ---------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Full Omniluxe cleaning pipeline:
    - strip HTML
    - normalize whitespace
    - enforce brand name
    """
    if not isinstance(text, str):
        return ""

    text = strip_html(text)
    text = normalize_whitespace(text)
    text = enforce_brand(text)
    return text