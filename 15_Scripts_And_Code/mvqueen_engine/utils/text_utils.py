import re

def strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def normalize_whitespace(text: str) -> str:
    """Normalize multiple spaces and newlines."""
    if not text:
        return ""
    return " ".join(text.split())

def enforce_brand(text: str) -> str:
    """Enforce brand-specific linguistic rules."""
    # Example: Ensure brand name capitalization
    text = text.replace("mvqueen", "MVQueen").replace("MVQUEEN", "MVQueen")
    return text
