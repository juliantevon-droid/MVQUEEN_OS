"""Scan production-readiness sources for credential-like literals without printing secret values.

Exit 0 when no matches are found; exit 1 when a likely literal credential is found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDED = {"__pycache__", ".git"}
PATTERN = re.compile(
    r"(?i)\\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\\b"
    r"\\s*[:=]\\s*([\\\"'])([^\\\"'\\n]{12,})\\1"
)

matches: list[tuple[Path, int]] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in EXCLUDED for part in path.parts):
        continue
    if path.suffix in {".pyc"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    for lineno, line in enumerate(text.splitlines(), 1):
        if PATTERN.search(line):
            matches.append((path.relative_to(ROOT), lineno))

if matches:
    print("Credential-like literals found:")
    for path, lineno in matches:
        print(f"- {path}:{lineno}")
    sys.exit(1)

print("Credential scan: PASS — no credential-like literals found.")
