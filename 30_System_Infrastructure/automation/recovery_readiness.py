#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
failures: list[str] = []

required = [
    'PRODUCTION_READINESS/BACKUP_STRATEGY.md',
    'SECURITY.md',
    '.gitignore',
    '.github/workflows/mvqueen-theme-cicd.yml',
    'prisma/schema.prisma',
    'prisma/production/schema.prisma',
    '30_System_Infrastructure/automation/verify_unpublished_theme.py',
]
for rel in required:
    if not (ROOT / rel).is_file():
        failures.append(f'Missing recovery dependency: {rel}')

theme_ci = (ROOT / '.github/workflows/mvqueen-theme-cicd.yml').read_text(encoding='utf-8')
if 'verify_unpublished_theme.py' not in theme_ci:
    failures.append('Theme deployment does not verify unpublished target')
if '--allow-live' in theme_ci or 'theme publish' in theme_ci:
    failures.append('Live theme publishing path detected in automated theme workflow')

gitignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
for token in ['.env', '_BACKUPS/', 'backups/shopify_catalog/']:
    if token not in gitignore:
        failures.append(f'.gitignore missing recovery/security exclusion: {token}')

security = (ROOT / 'SECURITY.md').read_text(encoding='utf-8')
if 'Repository visibility should be **Private**.' not in security:
    failures.append('Security policy does not require a private repository')

dev_migrations = list((ROOT / 'prisma' / 'migrations').glob('*/migration.sql'))
prod_migrations = list((ROOT / 'prisma' / 'production' / 'migrations').glob('*/migration.sql'))
if not dev_migrations:
    failures.append('No development database migrations available for recovery')
if not prod_migrations:
    failures.append('No production database migrations available for recovery')

if failures:
    print('MVQUEEN RECOVERY READINESS: FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('MVQUEEN RECOVERY READINESS: PASS')
print(f'Development migrations: {len(dev_migrations)}')
print(f'Production migrations: {len(prod_migrations)}')
print('Automated theme publishing remains restricted to an unpublished target.')
