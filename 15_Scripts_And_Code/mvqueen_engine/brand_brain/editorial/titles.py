"""Title generation for MVQueen products."""

from typing import Any, Mapping


def generate_title(base_title: str, handle: str = "", context: Mapping[str, Any] | None = None, max_length: int = 65) -> str:
    """Generate a conservative editorial title while preserving product identity."""
    base = " ".join(str(base_title or "").split()).strip()
    if not base:
        return ""
    # Product identity is never replaced with invented attributes.
    title = base
    if len(title) > max_length:
        title = title[:max_length].rstrip(" -–,;:")
    return title
