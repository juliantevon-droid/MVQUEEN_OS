"""Bounded text chunking for Android and memory-constrained processing."""
from __future__ import annotations


def chunk_text(text: object, max_chars: int = 4000) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    value = str(text or "")
    if not value:
        return []
    words = value.split()
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        added = len(word) + (1 if current else 0)
        if current and length + added > max_chars:
            chunks.append(" ".join(current))
            current, length = [], 0
        if len(word) > max_chars:
            if current:
                chunks.append(" ".join(current))
                current, length = [], 0
            for start in range(0, len(word), max_chars):
                chunks.append(word[start:start + max_chars])
        else:
            current.append(word)
            length += len(word) + (1 if len(current) > 1 else 0)
    if current:
        chunks.append(" ".join(current))
    return chunks

__all__ = ["chunk_text"]
