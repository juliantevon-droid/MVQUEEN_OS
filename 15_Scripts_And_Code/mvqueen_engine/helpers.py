# mvqueen_engine/utils/helpers.py
"""
Helper utilities for the MVQueen Omniluxe Engine.

These functions provide:
- Safe dictionary access
- Keyword matching
- List utilities
- Defensive programming patterns

These helpers are used across:
- Detection modules
- Editorial generation
- Persona routing
- Tag + collection builders
- Metafield generation
"""

from typing import Any, Dict, List
import random
import os
import re

def safe_get(d: Dict, key: str, default: Any = None) -> Any:
    """
    Safe dictionary access.
    Returns d[key] if present, otherwise returns default.
    """
    return d[key] if key in d else default


def first_match(text: str, keyword_map: Dict[str, List[str]], default: str = None) -> str:
    """
    Returns the first key whose keyword list matches the text.

    Example:
        keyword_map = {
            "dress": ["dress", "slip", "gown"],
            "top": ["top", "tee", "shirt"]
        }

        first_match("black satin slip dress", keyword_map)
        → "dress"
    """
    t = text.lower()
    for label, keywords in keyword_map.items():
        if any(k in t for k in keywords):
            return label
    return default


def ensure_list(value: Any) -> List[Any]:
    """
    Ensures the returned value is always a list.
    Useful for tags, collections, and metafields.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]
    
    import random
from typing import Sequence, Any

def choose_safe(sequence: Sequence[Any], default: Any = None) -> Any:
    """
    Safely choose a random item from a sequence.
    Returns default if sequence is empty or invalid.
    """
    if not sequence:
        return default
    return random.choice(sequence)