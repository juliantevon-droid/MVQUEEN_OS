# MVQUEEN Dependency Security Overrides

## deepmerge-ts 8.0.1

**Reason:** GHSA-ggr8-5vv4-36mx / CVE-2026-40345 is a high-severity stack-exhaustion issue affecting `deepmerge-ts <8.0.0`.

**Dependency path:** Prisma → `@prisma/config` → `deepmerge-ts`.

**Decision:** Keep the validated Prisma 6 runtime line and force `deepmerge-ts=8.0.1` through npm `overrides` instead of accepting `npm audit fix --force`'s proposed Prisma downgrade.

**Runtime exposure:** The vulnerable dependency is reached through Prisma configuration tooling rather than MVQUEEN customer-request business logic, but the repository still treats the high-severity advisory as a release-blocking dependency issue.

**CI enforcement:**

1. Resolve the dependency graph.
2. Run `npm ls deepmerge-ts`.
3. Run `npm audit --omit=dev --audit-level=high`.
4. Fail the workflow if the override no longer produces a clean high-severity audit.

**Removal condition:** Remove this override only after the selected supported Prisma release resolves `@prisma/config` to `deepmerge-ts >=8.0.0` on its own and the dependency audit remains green without the override.
