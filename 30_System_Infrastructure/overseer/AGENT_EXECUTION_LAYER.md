# MVQUEEN_OS Agent Execution Layer

## Status

The production specialist system is executable, not only documentary.

The runtime chain is:

**Crawler → Overseer routing → Specialist execution → QA requirements → Release disposition → outcome learning**

## Components

- `core/vault_crawler.py` — read-only repository and production-contract crawler.
- `30_System_Infrastructure/overseer/route_findings.py` — maps findings to specialist owners/reviewers.
- `30_System_Infrastructure/overseer/agent_registry.json` — canonical 14-agent runtime registry.
- `30_System_Infrastructure/overseer/agent_executor.py` — executes specialist analysis and produces QA/release records.
- `scripts/agent_worker.py` — continuous Railway-compatible worker.
- `memory/agent_outcome_ledger.json` — governed learning history.

## Runtime authority

The execution layer is fail-closed.

Agents may automatically:

- inspect evidence
- classify findings
- produce diagnoses
- recommend repairs
- define verification checks
- place blocking findings on release hold
- generate auditable execution artifacts

Agents may not automatically:

- publish Shopify themes or catalog changes
- alter prices, inventory, SKUs, variants, handles, credentials, or permissions
- delete Git/Drive history
- promote their own learning into operating rules
- weaken QA/security/release controls

Protected changes require explicit approval plus verification.

## Railway

`Dockerfile.agent` runs the continuous agent worker. The default cycle is every 900 seconds and cannot be configured below 300 seconds.

The worker scans the deployed repository snapshot and writes runtime artifacts to a temporary directory, so it does not mutate the repository checkout.

## CI

The Overseer GitHub Actions workflow runs the same specialist executor after routing findings and uploads both JSON and Markdown execution evidence.
