# mvqueen_engine/utils/deterministic.py
"""
PHASE 0 — DETERMINISTIC UTILITIES

Shared helpers:
- seed_from_text
- pick_from_pool
- pick_multiple
- truncate
"""

import hashlib

def seed_from_text(text: str):
    """Generate deterministic seed array from text."""
    if not isinstance(text, str):
        text = str(text)
    h = hashlib.sha256(text.encode()).hexdigest()
    return [int(h[i:i+8], 16) for i in range(0, 64, 8)]

def pick_from_pool(pool, seed: int):
    """Deterministic pick from any list."""
    if not pool:
        return ""
    return pool[seed % len(pool)]

def pick_multiple(pool, seeds, count: int = 3):
    """Pick multiple deterministic values from a pool."""
    if not pool:
        return []
    return [pool[s % len(pool)] for s in seeds[:count]]

def truncate(text: str, max_len: int):
    """Truncate text to a character limit, preserving whole words when possible."""
    if not isinstance(text, str):
        text = str(text)
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(" ", 1)[0]
    return cut + "…"