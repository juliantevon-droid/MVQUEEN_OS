#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / 'storefront' / 'theme'
BUDGET_PATH = ROOT / '30_System_Infrastructure' / 'system' / 'registry' / 'performance_budget.json'

budget = json.loads(BUDGET_PATH.read_text(encoding='utf-8'))['theme']
assets = THEME / 'assets'
css_files = sorted(assets.glob('*.css'))
js_files = sorted(assets.glob('*.js'))

css_total = sum(path.stat().st_size for path in css_files)
js_total = sum(path.stat().st_size for path in js_files)
failures: list[str] = []

if css_total > budget['maxTotalCssBytes']:
    failures.append(f"Total CSS {css_total} exceeds {budget['maxTotalCssBytes']} bytes")
if js_total > budget['maxTotalJsBytes']:
    failures.append(f"Total JS {js_total} exceeds {budget['maxTotalJsBytes']} bytes")

for path in css_files + js_files:
    size = path.stat().st_size
    if size > budget['maxSingleAssetBytes']:
        failures.append(f"{path.relative_to(THEME)} is {size} bytes; max is {budget['maxSingleAssetBytes']}")

liquid_files = list(THEME.rglob('*.liquid'))
legacy_img_tags = []
for path in liquid_files:
    source = path.read_text(encoding='utf-8', errors='ignore')
    if '| img_tag' in source or '| img_url' in source:
        legacy_img_tags.append(str(path.relative_to(THEME)))
if legacy_img_tags:
    failures.append('Deprecated image filters found: ' + ', '.join(legacy_img_tags))

print(f'MVQUEEN PERFORMANCE AUDIT: CSS={css_total} bytes JS={js_total} bytes')
if failures:
    print('MVQUEEN PERFORMANCE AUDIT: FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('MVQUEEN PERFORMANCE AUDIT: PASS')
