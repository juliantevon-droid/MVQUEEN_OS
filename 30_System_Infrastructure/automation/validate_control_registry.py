#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / 'app' / 'config' / 'mvqueen-control-registry.json'
PERF_PATH = ROOT / '30_System_Infrastructure' / 'system' / 'registry' / 'performance_budget.json'
CAPABILITIES_PATH = ROOT / '30_System_Infrastructure' / 'system' / 'registry' / 'enterprise_capabilities.json'
TRUST_PATH = ROOT / 'storefront' / 'theme' / 'snippets' / 'trust-badges.liquid'
LOCALES = ROOT / 'storefront' / 'theme' / 'locales'
WORKER_WORKFLOW = ROOT / '.github' / 'workflows' / 'product-worker.yml'
WORKER_ROUTE = ROOT / 'app' / 'routes' / 'internal.product-worker.ts'
ENV_EXAMPLE = ROOT / '.env.example'

failures: list[str] = []

registry = json.loads(REGISTRY_PATH.read_text(encoding='utf-8'))
performance = json.loads(PERF_PATH.read_text(encoding='utf-8'))
capabilities = json.loads(CAPABILITIES_PATH.read_text(encoding='utf-8'))
trust = TRUST_PATH.read_text(encoding='utf-8')

available = registry['trustBadges']['available']
if len(available) != len(set(available)):
    failures.append('Duplicate trust badge keys in control registry')

badge_cases = set(re.findall(r"when '([a-z0-9_]+)'", trust))
preset_names = set(registry['trustBadges']['presets'])
badge_case_names = set(available)
missing_badge_cases = sorted(badge_case_names - badge_cases)
if missing_badge_cases:
    failures.append('Liquid trust snippet missing badge cases: ' + ', '.join(missing_badge_cases))

for preset_name, preset in registry['trustBadges']['presets'].items():
    if f"when '{preset_name}'" not in trust:
        failures.append(f'Liquid trust snippet missing preset: {preset_name}')
    invalid = [badge for badge in preset['badges'] if badge not in available]
    if invalid:
        failures.append(f"Preset {preset_name} contains unknown badges: {', '.join(invalid)}")
    expected_badges = ','.join(preset['badges'])
    preset_block_match = re.search(
        rf"when '{re.escape(preset_name)}'(?P<body>.*?)(?=\n\s*when '|\n\s*endcase)",
        trust,
        re.S,
    )
    if not preset_block_match:
        continue
    body = preset_block_match.group('body')
    if f"assign preset_badges = '{expected_badges}'" not in body:
        failures.append(f'Preset {preset_name} badge order differs from control registry')
    if f"assign preset_layout = '{preset['layout']}'" not in body:
        failures.append(f'Preset {preset_name} layout differs from control registry')
    expected_payment = 'true' if preset['showPaymentIcons'] else 'false'
    if f'assign preset_payment_icons = {expected_payment}' not in body:
        failures.append(f'Preset {preset_name} payment-icon setting differs from control registry')
    if preset['hideDescriptions'] and 'assign preset_hide_descriptions = true' not in body:
        failures.append(f'Preset {preset_name} hide-description setting differs from control registry')

locale_file_map = {'en': 'en.default.json', 'es': 'es.json', 'fr': 'fr.json', 'pt-BR': 'pt-BR.json'}
for locale in registry['localization']['preparedLocales']:
    filename = locale_file_map.get(locale, f'{locale}.json')
    if not (LOCALES / filename).is_file():
        failures.append(f'Prepared locale is missing from theme: {locale} -> {filename}')

if registry['performance']['lighthouseTarget'] / 100 != performance['lighthouse']['performance']:
    failures.append('Control registry Lighthouse target differs from performance budget')
if registry['performance']['maxThemeCssBytes'] != performance['theme']['maxTotalCssBytes']:
    failures.append('Control registry CSS budget differs from performance budget')
if registry['performance']['maxThemeJsBytes'] != performance['theme']['maxTotalJsBytes']:
    failures.append('Control registry JS budget differs from performance budget')
if registry['performance']['maxSingleAssetBytes'] != performance['theme']['maxSingleAssetBytes']:
    failures.append('Control registry single-asset budget differs from performance budget')

protected = registry['automation']['protectedFields']
capability_protected = capabilities.get('non_negotiable_gates', {}).get('protected_fields', [])
if protected != capability_protected:
    failures.append('Protected-field contract differs between control registry and enterprise capabilities')

if registry['security']['repositoryExpectedVisibility'] != 'private':
    failures.append('Control registry must require private repository visibility')

worker_workflow = WORKER_WORKFLOW.read_text(encoding='utf-8')
expected_fallback = registry['automation']['fallbackReconciliationMinutes']
if f'*/{expected_fallback} * * * *' not in worker_workflow:
    failures.append('Product worker fallback schedule differs from control registry')

worker_route = WORKER_ROUTE.read_text(encoding='utf-8')
for token in ['timingSafeEqual', 'runAlwaysOnProductWorker', 'recordProductWorkerHeartbeat']:
    if token not in worker_route:
        failures.append(f'Product worker route missing security/runtime contract: {token}')

env_example = ENV_EXAMPLE.read_text(encoding='utf-8')
for token in ['MVQ_PRODUCT_CONTINUOUS_WORKER_REQUIRED=true', 'MVQ_PRODUCT_RECONCILE_ENABLED=true']:
    if token not in env_example:
        failures.append(f'Environment template missing automation hardening flag: {token}')

if failures:
    print('MVQUEEN CONTROL REGISTRY: FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('MVQUEEN CONTROL REGISTRY: PASS')
print(f"Trust badges: {len(available)}")
print(f"Trust presets: {len(preset_names)}")
print(f"Prepared locales: {len(registry['localization']['preparedLocales'])}")
