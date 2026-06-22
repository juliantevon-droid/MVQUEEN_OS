MVQUEEN & MVQUEEN_OS Unified Architecture Blueprint
1. Overview
This document serves as the central orchestration blueprint for integrating the MVQUEEN E-commerce Engine and the MVQUEEN_OS Local File Management system. Both systems are designed to operate in sync using a shared logic layer.
2. Synchronization Protocol
Component
	Sync Method
	Frequency
 
	MASTER_INDEX_V2.md
	rclone (via sync_vault.sh)
	On-demand / Scheduled
	Asset Libraries
	Bidirectional Cloud-to-Local
	Continuous
	Health Logs
	Google Apps Script
	Automated Hourly
	3. GitHub API Authentication Strategy
* Phase 1 (Development): Use Personal Access Tokens (PATs) for local Termux/Pydroid3 scripts. Store tokens in a local .env file.
* Phase 2 (Scale): Migrate to GitHub Apps if multi-user access or enhanced security scoping is required for repository management.
4. Extraction & Logic Integration
Leverage deterministic.py to assign immutable file IDs. This logic ensures that MVQUEEN_OS maintains file integrity during sync events, preventing duplicate assets across the Drive and local storage.