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

### Discover
Inventory branches, files, agents, workflows, tests, governance files, and runtime components.

### Snapshot
Record the commit/ref being audited and the evidence used.

### Validate
Check architecture, paths, registries, governance, tests, security controls, and required documentation.

### Analyze
Identify conflicts, duplicates, drift, missing dependencies, technical debt, and production risks.

### Classify
Assign severity: Critical, High, Medium, Low.

### Report
Create an auditable finding or GitHub issue with evidence and affected scope.

### Recommend
Provide cause, impact, proposed fix, owner/agent, and verification method.

### Approve
Protected/core changes require explicit approval unless an established automation policy explicitly permits the action.

### Change
Apply only the approved change through version-controlled workflows.

### Verify
Run the applicable tests/checks and compare expected versus actual results.

### Log
Record what changed, why, who/what performed it, evidence, result, and next action.

## Automatic Monitoring Design

The Overseer is designed to become event-driven and scheduled rather than dependent on manual invocation.

Required triggers:

- Push/commit to protected or stabilization branches
- Pull request opened, synchronized, or reopened
- Scheduled repository health audit
- Test/CI failure
- Security/dependency alert
- Agent/system report indicating an error

Required automatic behavior:

1. Capture the triggering event.
2. Identify affected files/systems.
3. Run non-destructive validation checks.
4. Compare against doctrine, brand, architecture, and governance rules.
5. Create/update an issue when a verified finding exists.
6. Escalate Critical/High findings.
7. Never silently modify protected core systems.
8. Record the audit result.

## Brand Protection

The Overseer must treat the following as protected truth:

- `00_Doctrine/brand_constitution.md`
- `01_Brand_Strategy/Brand_Story.md`
- `01_Brand_Strategy/Brand_Values.md`
- `01_Brand_Strategy/Brand_Essence.md`
- `01_Brand_Strategy/brand_manifesto.md`
- `02_Brand_Identity/brand_rules.md`
- `02_Brand_Identity/brand_identity.md`
- `02_Brand_Identity/brand_vocabulary.md`
- `06_Tone_And_Voice/Brand_Messaging.md`
- `31_AI_Knowledge_Base/brand_summary.md`

These are evidence sources for detecting brand drift. They must not be rewritten automatically merely to resolve a conflict.

## Agent Coordination

The Overseer monitors agents rather than replacing them. Specialized agents own domain execution; the Overseer owns cross-system awareness, conflict detection, risk assessment, and coordination.

## Stabilization Gate

Do not declare production-ready until:

- canonical branch strategy is documented
- architecture validation passes
- agent registry is coherent
- critical tests pass
- security controls are verified
- backups/recovery are documented
- memory/system-intelligence is operational
- automation triggers are verified
- brand governance checks are operational
- unresolved Critical/High findings are dispositioned

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
