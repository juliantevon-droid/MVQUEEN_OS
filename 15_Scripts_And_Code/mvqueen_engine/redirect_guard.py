"""MVQUEEN URL redirect validation guard.

Pure validation module: it does not write to Shopify. Production writes belong
behind an explicit approval step in the URL/SEO production gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Redirect:
    source: str
    destination: str
    reason: str = ""
    resource_type: str = ""
    resource_identifier: str = ""


def normalize_path(value: str) -> str:
    """Return a normalized Shopify-relative path."""
    value = (value or "").strip()
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f"Absolute URLs are not permitted: {value}")
    path = parsed.path or "/"
    if not path.startswith("/"):
        path = "/" + path
    if path != "/":
        path = path.rstrip("/")
    return path


def validate_redirects(redirects: Iterable[Redirect]) -> list[str]:
    """Validate a redirect set and return human-readable errors."""
    errors: list[str] = []
    seen_sources: set[str] = set()
    graph: dict[str, str] = {}

    for index, redirect in enumerate(redirects, start=1):
        try:
            source = normalize_path(redirect.source)
            destination = normalize_path(redirect.destination)
        except ValueError as exc:
            errors.append(f"#{index}: {exc}")
            continue

        if source == "/":
            errors.append(f"#{index}: root path cannot be used as a redirect source")
        if source == destination:
            errors.append(f"#{index}: self-redirect is not allowed: {source}")
        if source in seen_sources:
            errors.append(f"#{index}: duplicate source: {source}")

        seen_sources.add(source)
        graph[source] = destination

    # Detect chains and loops within the proposed redirect graph.
    for source in graph:
        visited: set[str] = set()
        current = source
        while current in graph:
            if current in visited:
                errors.append(f"redirect loop detected from {source}")
                break
            visited.add(current)
            current = graph[current]
            if current in graph and current != source:
                errors.append(f"redirect chain detected: {source} -> {current}")
                break

    return sorted(set(errors))


def assert_valid_redirects(redirects: Iterable[Redirect]) -> None:
    """Raise ValueError when a redirect plan fails validation."""
    errors = validate_redirects(redirects)
    if errors:
        raise ValueError("Invalid MVQUEEN redirect plan:\n- " + "\n- ".join(errors))


__all__ = [
    "Redirect",
    "normalize_path",
    "validate_redirects",
    "assert_valid_redirects",
]
