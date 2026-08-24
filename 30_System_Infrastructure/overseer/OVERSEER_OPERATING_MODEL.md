# MVQUEEN_OS Overseer — Operating Model

## Mission

The Overseer is the independent audit, safety, governance, and production-readiness control plane for MVQUEEN_OS.

It does not blindly mutate core system files. Its default behavior is to inspect, validate, report, recommend, and gate changes.

## Continuous operating cycle

**DISCOVER → SNAPSHOT → VALIDATE → ANALYZE → CLASSIFY → REPORT → RECOMMEND → APPROVE → CHANGE → VERIFY → LOG**

## Production rule

No production release is considered ready solely because code exists or a workflow is configured. Production readiness requires evidence from the current repository state and current validation run.

## Audit layers

1. Repository integrity
2. Architecture/governance
3. Protected brand sources
4. Agent definitions
5. Memory/system intelligence
6. Runtime/module registry
7. Brand-bank contracts
8. Python/JSON validation
9. Shopify-safe engine controls
10. Security and sensitive-file protections
11. Backup/recovery readiness
12. Automation and scheduled execution
13. Deployment configuration
14. Current Drive report handoff

## Severity

- **CRITICAL** — immediate production stop
- **HIGH** — production blocker until dispositioned
- **MEDIUM** — remediation required and tracked
- **LOW** — improvement / technical debt
- **PASS** — verified control

## Branch governance

`stabilization` is the engineering/audit workspace until a production candidate is explicitly approved.

`main` is not promoted merely because branch divergence is inconvenient.

Before merging any branch or pull request:

1. Compare it with current stabilization.
2. Classify changes as KEEP / REPLACE / MERGE / ARCHIVE.
3. Validate protected sources and architecture.
4. Run current tests/audits.
5. Record the decision.
6. Apply only the approved change.
7. Re-run verification.

## Runtime safety

Registered modules must have:

- unique names
- explicit versions
- allowed layers
- valid paths
- valid entrypoints
- paths confined to the module directory
- a `boot()` entrypoint returning a dictionary
- a ready/running/healthy status at successful boot

Module failures must be recorded in runtime state and result in a degraded system state rather than being silently ignored.

## Drive reporting

The current report is maintained at:

`30_System_Infrastructure/overseer/reports/MVQUEEN_OS_CURRENT_AUDIT.md`

GitHub remains the historical evidence trail. Google Drive receives one current report for operational access.

## Release gate

A production candidate may advance only when:

- no unresolved CRITICAL findings exist
- all HIGH findings have been fixed or explicitly approved
- current CI/Overseer results are captured
- runtime boot is verified
- recovery/backup controls are verified
- security controls are verified
- Drive handoff is verified or explicitly waived
- production deployment configuration is verified
- the release decision is documented
