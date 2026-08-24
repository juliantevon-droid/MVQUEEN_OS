# MVQUEEN_OS Overseer Operating Model

## Status
ACTIVE — Stabilization Phase

## Purpose
Define the operating model for the MVQUEEN_OS Overseer so monitoring becomes repeatable, auditable, and safe to automate.

## Source-of-Truth Hierarchy
1. `00_Doctrine/` — constitutional and governance constraints
2. `01_Brand_Strategy/` and `02_Brand_Identity/` — brand truth and identity
3. `10_AI_Systems/` — agent/AI operating rules
4. `30_System_Infrastructure/` — runtime and technical controls
5. Specialized systems and agents
6. Logs, reports, analytics, and derived recommendations

When sources conflict, the higher layer wins until the conflict is explicitly resolved.

## Overseer Loop

```text
DISCOVER → SNAPSHOT → VALIDATE → ANALYZE → CLASSIFY → REPORT → RECOMMEND → APPROVE → CHANGE → VERIFY → LOG
```

## Production Gate

The Overseer does not declare production readiness because code exists or because a workflow is configured. A production candidate requires evidence from the current repository state and a current validation run.

Required controls:
- architecture and governance validation
- protected brand-source validation
- agent and memory/system-intelligence validation
- runtime/module registry validation
- brand-bank contract tests
- Python and JSON validation
- security and sensitive-file protection
- backup/recovery readiness
- automation and scheduled execution
- deployment configuration
- current Google Drive report handoff

No unresolved Critical finding may remain. High findings must be fixed or explicitly approved before release.

## Branch Governance

`stabilization` is the engineering/audit workspace until a production candidate is explicitly approved. `main` is not promoted merely to reduce branch divergence.

Before merging any branch or pull request:
1. Compare it with current stabilization.
2. Classify changes as KEEP / REPLACE / MERGE / ARCHIVE.
3. Validate protected sources and architecture.
4. Run current tests/audits.
5. Record the decision.
6. Apply only the approved change.
7. Re-run verification.

## Runtime Safety

Registered modules must have unique names, explicit versions, allowed layers, valid paths, valid entrypoints, paths confined to the module directory, and a `boot()` entrypoint returning a dictionary with a ready/running/healthy status.

Module failures must be recorded in runtime state and result in a degraded system state rather than being silently ignored.

## Drive Reporting

The current report is maintained at `30_System_Infrastructure/overseer/reports/MVQUEEN_OS_CURRENT_AUDIT.md`.

GitHub remains the historical evidence trail. Google Drive receives one current report for operational access.

## Required Audit Record

```text
Audit ID:
Timestamp:
Trigger:
Branch/Commit:
Scope:
Health:
Risk Level:
Findings:
Evidence:
Recommended Actions:
Approval Required:
Verification:
Result:
Next Priority:
```