# MVQUEEN Shopify Backend

Dedicated Shopify backend boundary for MVQUEEN_OS.

Initial phase: CLI configuration, authentication, read-only GraphQL connectivity, health/status, audit logging, dry-run enforcement, controlled product workflows, and webhooks.

Safety: never commit Shopify access tokens; begin read-only; keep writes behind explicit dry-run controls; preserve handles, SKUs, variants, inventory, and existing media unless explicitly authorized; validate GraphQL operations against the live schema; retain the legacy REST layer during migration.

Use separate Shopify app configurations for development, staging, and production. The existing `15_Scripts_And_Code/mvqueen_engine` remains the reusable domain/automation layer; this app is the Shopify app boundary around it.
