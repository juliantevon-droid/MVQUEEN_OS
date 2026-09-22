"""MVQueen editorial generation primitives.

These deterministic functions are intentionally conservative. They create a
clean brand presentation without inventing specifications, materials,
measurements, benefits, certifications, or claims not present in the source.
"""

from __future__ import annotations

import re
from html import escape


def _clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    value = re.sub(r"(?i)^mvqueen\s*[|:-]\s*", "", value)
    return value


def generate_title(base_title: str, handle: str) -> str:
    """Return a clean customer-facing title without supplier-brand stamping."""
    title = _clean_title(base_title)
    if not title:
        return "MVQueen Curated Selection"
    return title


def generate_description(base_title: str, handle: str, supplier_body: str) -> str:
    """Create a restrained description using supplied facts only."""
    title = _clean_title(base_title)
    source = re.sub(r"\s+", " ", str(supplier_body or "")).strip()

    if source:
        source = source.replace("MVQUEEN", "MVQueen").replace("mvqueen", "MVQueen")
        body = escape(source)
        return (
            f"<p><strong>{escape(title)}</strong></p>"
            f"<p>{body}</p>"
            "<p>Curated by MVQueen for a polished, feminine wardrobe and beauty edit.</p>"
        )

    return (
        f"<p><strong>{escape(title)}</strong></p>"
        "<p>A thoughtfully curated MVQueen selection designed for modern, "
        "confident style.</p>"
    )
