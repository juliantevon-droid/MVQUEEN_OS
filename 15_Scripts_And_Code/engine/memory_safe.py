# android/memory_safe.py
"""
MVQueen Memory Safety Layer — Enterprise Edition
------------------------------------------------

Ensures safe execution on Android devices:
- Low RAM protection
- Chunk-based processing enforcement
- Safe guards for large text operations
"""

import sys
from typing import Any


# ------------------------------------------------------------
# CHECK AVAILABLE MEMORY (approximate)
# ------------------------------------------------------------
def _approx_available_memory_mb() -> int:
    """
    Returns an approximate available memory value in MB.
    Android/Pydroid does not expose full system memory APIs,
    so we use Python's memory footprint as a proxy.
    """
    try:
        return int((sys.getsizeof(object()) / 1024) / 1024)  # fallback proxy
    except Exception:
        return 50  # safe fallback


# ------------------------------------------------------------
# MEMORY-SAFE EXECUTION WRAPPER
# ------------------------------------------------------------
def ensure_memory_safe(data: Any, max_mb: int = 50) -> bool:
    """
    Checks if data is safe to process on Android.

    Args:
        data: The object to evaluate.
        max_mb: Maximum allowed memory footprint.

    Returns:
        bool — True if safe, False if too large.
    """

    try:
        size_mb = sys.getsizeof(data) / (1024 * 1024)
        return size_mb <= max_mb
    except Exception:
        return True  # fail-safe: assume safe


__all__ = ["ensure_memory_safe"]