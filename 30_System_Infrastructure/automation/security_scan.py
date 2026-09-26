#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {'.git', 'node_modules', 'build', '.react-router', '__pycache__', '.pytest_cache', '_BACKUPS'}
SKIP_SUFFIXES = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf', '.zip', '.gz', '.sqlite'}

PATTERNS = {
    'Shopify access token': re.compile(r'\bshpat_[A-Za-z0-9]{16,}\b'),
    'Shopify shared secret/token': re.compile(r'\b(?:shpss|shpca)_[A-Za-z0-9]{16,}\b'),
    'GitHub token': re.compile(r'\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})\b'),
    'AWS access key': re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    'Private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}

failures: list[str] = []

for path in ROOT.rglob('*'):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in rel.parts):
        continue
    if path.suffix.lower() in SKIP_SUFFIXES:
        continue
    try:
        source = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue

    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(source):
            failures.append(f'{rel}: possible {label}: {match.group(0)[:12]}…')

    if path.name != '.env.example':
        for line_no, line in enumerate(source.splitlines(), 1):
            if re.search(r"(?i)(api[_-]?secret|access[_-]?token|private[_-]?key|password)\s*=\s*['\"]?[^\s'\"]{12,}", line):
                if 'process.env' not in line:
                    failures.append(f'{rel}:{line_no}: possible hard-coded credential assignment')

if failures:
    print('MVQUEEN SECURITY SCAN: FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('MVQUEEN SECURITY SCAN: PASS')
print('No high-confidence credential patterns detected in tracked source.')
