"""Raw text cleaning without changing semantic product facts."""
from __future__ import annotations
import re
from html import unescape


def clean_text(value: object) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_lines(value: object) -> list[str]:
    text = unescape(str(value or ""))
    return [line.strip() for line in re.split(r"[\n\r]+", text) if line.strip()]

__all__ = ["clean_text", "clean_lines"]
