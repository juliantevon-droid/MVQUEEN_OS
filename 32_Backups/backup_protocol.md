# Backup Protocol
## MVQUEEN_OS / 32_Backups

---

## Purpose

Defines the backup architecture for MVQUEEN_OS. No file is ever permanently lost. Every major build phase is preserved before changes.

---

## Backup Tiers

### Tier 1 — Pre-Edit Backup
Before editing any critical file, copy the original here with the date suffix:
`filename_BACKUP_YYYYMMDD.md`

### Tier 2 — Phase Backup
Before completing a major OS phase, create a full snapshot:
`phase_N_snapshot_YYYYMMDD/`

### Tier 3 — Drive Sync
DriveSync handles continuous backup to Google Drive. Confirm sync is active weekly.

---

## Backup Index

| Backup | Date | Contents |
|---|---|---|
| `_BACKUPS/` folder | Active | Phase 3 working files |
| DriveSync | Continuous | Full OS mirror |

---

## Recovery Protocol

1. Check `_BACKUPS/` first for recent copies
2. Check `28_Archives/` for archived versions
3. Check Google Drive for synced versions
4. Rebuild from Brand Bible if no backup available

---

## Status
Active
