"""Low-memory execution helpers for Android/Colab environments."""
from __future__ import annotations
import gc
from contextlib import contextmanager


def release_memory() -> None:
    gc.collect()


@contextmanager
def memory_scope():
    try:
        yield
    finally:
        release_memory()


def recommended_chunk_size(row_count: int, default: int = 850) -> int:
    if row_count < 1:
        return 1
    if row_count <= default:
        return row_count
    return default
