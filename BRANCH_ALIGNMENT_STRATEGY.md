# MVQUEEN_OS Branch Alignment Strategy

**Date:** Sept 3, 2026  
**Current State:** 10 branches, 2 open PRs, 23 audit failures  
**Objective:** Align all branches before production promotion  

---

## Branch Status & Actions

| Branch | Commit | Status | Action |
|--------|--------|--------|--------|
| **main** | Aug 24 | 🔴 CI FAILS (23 issues) | Do NOT merge PRs yet. Audit failures block. |
| **stabilization** | Aug 24 | 🟡 Engineering workspace | Keep as base for all fixes. |
| **production-candidate** | Aug 26 | 🟡 Latest CI config | Merge stabilization into this. |
| **production-reconciliation** | older | ⚠️ Stale | Evaluate for merge into production-candidate. |
| PR #10 | release branch | ⏳ Waiting | HOLD until audit passes. |
| PR #11 | reconcile branch | ⏳ Waiting | HOLD until audit passes. |

---

## Blockers to Resolve

### Blocker 1: Missing/Incomplete Test Files
**Status:** ✅ Code exists in diff, need to verify on branch

- `30_System_Infrastructure/tests/test_brand_banks.py` — brand-bank contract tests
- `30_System_Infrastructure/tests/test_module_loader.py` — module loader tests
- **Action:** Commit these files to stabilization if not already present

### Blocker 2: Module System Boot Failures
**Status:** 🔴 Runtime boot test fails

The CI workflow expects:
```bash
python 30_System_Infrastructure/system/loader/module_loader.py
```

Current files in diff:
- `30_System_Infrastructure/system/loader/module_loader.py` ✅
- `30_System_Infrastructure/system/registry/system.json` ✅
- `30_System_Infrastructure/system/state/system_state.json` ✅
- `30_System_Infrastructure/modules/health_check.py` ✅

**Action:** Commit all system files to stabilization

### Blocker 3: Protected Source Missing
**Status:** 🔴 Validation fails looking for `memory/system_intelligence.json`

The CI workflow validates:
```bash
required=(
  ...
  'memory/system_intelligence.json'
  ...
)
```

**Action:** Create `memory/system_intelligence.json` with valid structure

### Blocker 4: CI Workflow Mismatch
**Status:** ⚠️ stabilization has old workflow; production-candidate has new

The old workflow on stabilization:
- Only monitors `main` and `stabilization` branches
- Doesn't run runtime boot smoke test

The new workflow on production-candidate:
- Monitors `main`, `stabilization`, `production-candidate`, `production-reconciliation`
- Includes runtime boot smoke test
- Has production-candidate-specific validation

**Action:** Sync CI workflow from production-candidate to stabilization

---

## Alignment Procedure (in order)

### Phase 1: Stabilization Branch Fixes (THIS SESSION)

1. **Commit missing test files** (if not present)
   - `30_System_Infrastructure/tests/test_brand_banks.py`
   - `30_System_Infrastructure/tests/test_module_loader.py`

2. **Commit missing module system files**
   - `30_System_Infrastructure/system/loader/module_loader.py`
   - `30_System_Infrastructure/system/registry/system.json`
   - `30_System_Infrastructure/system/state/system_state.json`
   - `30_System_Infrastructure/modules/health_check.py`
   - `30_System_Infrastructure/system/config/environment.json`
   - `30_System_Infrastructure/system/governance/` (all files)

3. **Create missing protected source**
   - `memory/system_intelligence.json` — valid JSON structure

4. **Sync audit checks** (if missing)
   - `30_System_Infrastructure/audit/mvqueen_audit/` (all check files)

5. **Update CI workflow** on stabilization to match production-candidate
   - Copy `.github/workflows/overseer.yml` from production-candidate to stabilization
   - Ensure both branches monitor same scope

6. **Run automated audit** to verify all tests pass locally before pushing

### Phase 2: Production-Candidate Alignment (NEXT)

1. Merge stabilization → production-candidate
2. Verify CI passes
3. Reconcile production-reconciliation changes (if any)

### Phase 3: Main Branch Promotion (AFTER AUDIT PASS)

1. Merge production-candidate → main
2. Merge PR #10 (release) and PR #11 (reconcile)
3. Tag release from main

---

## Test Verification Checklist

Before each push, confirm:

- [ ] JSON validation passes: `python -m py_compile 30_System_Infrastructure/tests/*.py`
- [ ] Python syntax passes: All `.py` files in audit/ modules/ and system/ are valid
- [ ] Brand-bank tests pass: `python -m unittest 30_System_Infrastructure/tests/test_brand_banks.py -v`
- [ ] Module-loader tests pass: `python -m unittest 30_System_Infrastructure/tests/test_module_loader.py -v`
- [ ] Runtime boot works: `python 30_System_Infrastructure/system/loader/module_loader.py`
- [ ] Protected sources exist: All files in protected source list checked
- [ ] Overseer model present: `30_System_Infrastructure/overseer/OVERSEER_OPERATING_MODEL.md` ✅
- [ ] CI workflow current: `.github/workflows/overseer.yml` is latest version

---

## Files to Commit (stabilization branch)

**If missing, commit these:**

### Tests
```
30_System_Infrastructure/tests/__init__.py
30_System_Infrastructure/tests/test_brand_banks.py
30_System_Infrastructure/tests/test_module_loader.py
```

### Module System
```
30_System_Infrastructure/system/loader/module_loader.py
30_System_Infrastructure/system/registry/system.json
30_System_Infrastructure/system/state/system_state.json
30_System_Infrastructure/system/config/environment.json
30_System_Infrastructure/system/governance/architecture_rules.json
30_System_Infrastructure/system/governance/validator.py
30_System_Infrastructure/modules/__init__.py
30_System_Infrastructure/modules/health_check.py
```

### Audit System
```
30_System_Infrastructure/audit/mvqueen_audit/__init__.py
30_System_Infrastructure/audit/mvqueen_audit/models.py
30_System_Infrastructure/audit/mvqueen_audit/runner.py
30_System_Infrastructure/audit/mvqueen_audit/checks/__init__.py
30_System_Infrastructure/audit/mvqueen_audit/checks/architecture_check.py
30_System_Infrastructure/audit/mvqueen_audit/checks/git_check.py
30_System_Infrastructure/audit/mvqueen_audit/checks/path_check.py
30_System_Infrastructure/audit/mvqueen_audit/checks/registry_check.py
```

### Overseer
```
30_System_Infrastructure/overseer/OVERSEER_OPERATING_MODEL.md
30_System_Infrastructure/overseer/DRIVE_REPORT_SYNC.md
30_System_Infrastructure/overseer/generate_current_report.py
```

### Protected Source (CREATE)
```
memory/system_intelligence.json
```

### CI/CD
```
.github/workflows/overseer.yml (sync from production-candidate)
```

---

## Next Steps

1. **Confirm these files exist on stabilization** — if not, I'll commit them
2. **Verify CI workflow is current** — if not, sync it
3. **Create `memory/system_intelligence.json`** — required for protected source validation
4. **Push to stabilization** and watch CI pass
5. **Merge stabilization → production-candidate** to unblock main
6. **Promote production-candidate → main** once all tests pass

---

**Status:** Ready for implementation. All blockers are addressable and documented.
