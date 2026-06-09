# mvqueen_engine/utils/text_utils.py
"""
PHASE 0 — TEXT UTILITIES

Shared helpers:
- strip_html
- normalize_whitespace
- enforce_brand
"""

import re
from mvqueen_engine.config import BRAND_NAME

def strip_html(html: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    if not isinstance(html, str):
        return ""
    text = re.sub("<[^<]+?>", "", html)
    return " ".join(text.split())

def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/newlines into single spaces."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.split())

def enforce_brand(text: str) -> str:
    """Normalize MVQueen brand name and strip stray whitespace."""
    if not isinstance(text, str):
        return text
    text = re.sub(r"\b(MVQUEEN|mvqueen|Mvqueen)\b", BRAND_NAME, text)
    return text.strip()