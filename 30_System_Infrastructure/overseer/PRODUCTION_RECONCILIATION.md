# MVQUEEN_OS Production Reconciliation

## Purpose

Controlled bridge between the existing `main` baseline and the verified production candidate.

## Release policy

`main` remains production-protected. Reconciliation must preserve required brand, Shopify, engine, agent, SEO, and system assets while excluding generated/cache/build artifacts.

## Evidence baseline

- Main baseline: `1d1c7e5fb45b760d19a9d23c6a0ad66af8f92692`
- Verified production candidate baseline: `fa80086c788a0f88e8e54405a1589580b4bed7fd`
- Common ancestor: `c6872dff3dc0fb6e198a7072e021e48b99d822df`

## Classification

### KEEP
- Canonical MVQUEEN brand doctrine and identity
- Canonical persona and brand banks
- Shopify-safe engine architecture
- SEO/content architecture
- Agent/system architecture
- Overseer and audit controls
- Runtime/module-loader controls
- Production documentation and recovery controls

### EXCLUDE / CLEAN
- Python cache directories/files
- temporary audit output
- generated build artifacts
- duplicate archives
- obsolete scripts where a canonical replacement exists

### MERGE CAREFULLY
- renamed engine/module paths
- overlapping configuration
- duplicate brand/content sources
- product/catalog assets
- deployment configuration

## Gate

No reconciliation commit may be promoted to `main` until the resulting tree passes the complete current Overseer workflow, including runtime boot, security/protected-source checks, audit, and report handoff.

Evidence → Analysis → Approval → Change → Verify → Log.
