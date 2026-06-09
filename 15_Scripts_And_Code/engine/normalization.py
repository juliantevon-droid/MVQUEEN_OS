# mvqueen_engine/utils/normalization.py
"""
Normalization utilities for the MVQueen Omniluxe Engine.

This module prepares text for detection by:
- Lowercasing
- Removing punctuation
- Normalizing whitespace
- Ensuring Android-safe regex operations

This ensures consistent keyword matching across all detection modules.
"""

import re


def normalize_for_detection(text: str) -> str:
    """
    Normalize text for keyword-based detection.

    Steps:
    1. Lowercase the text.
    2. Remove punctuation and special characters.
    3. Collapse multiple spaces into one.
    4. Strip leading/trailing whitespace.

    Returns a clean, detection-ready string.
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove punctuation (Android-safe)
    text = re.sub(r"[^\w\s]", " ", text)

    # Collapse spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()