# mvqueen_engine/utils/chunking.py
"""
Android-safe text chunking utilities for the MVQueen Omniluxe Engine.

This module ensures:
- Large text blocks are safely split into smaller chunks
- Prevents memory issues on Android/Pydroid
- Supports long editorial, SEO, metafields, and Shopify payloads
"""

from typing import List


def chunk_text(text: str, size: int = 500) -> List[str]:
    """
    Splits text into Android-safe chunks.

    Parameters:
        text (str): The text to split.
        size (int): Maximum chunk size. Default = 500 chars.

    Returns:
        List[str]: List of chunked text segments.
    """
    if not text:
        return []

    return [text[i:i + size] for i in range(0, len(text), size)]