# MVQUEEN Shopify Backend

Dedicated Shopify backend boundary for MVQUEEN_OS.

## Purpose

This service owns controlled Shopify automation while the existing Shopify ChatGPT MCP connection remains separate.

Initial phase:

1. Shopify CLI configuration
2. Authentication and store identity
3. Read-only GraphQL connectivity
4. Health/status endpoint
5. Audit logging
6. Dry-run enforcement
7. Controlled product workflows
8. Webhooks and automation

## Safety rules

- Never commit Shopify access tokens.
- Start with read-only access.
- Keep write operations behind explicit dry-run controls.
- Preserve handles, SKUs, variants, inventory, and existing media unless a workflow explicitly authorizes a change.
- Validate GraphQL operations against the live Shopify schema before execution.
- Keep the existing legacy REST layer available during migration.

## Environment targets

Use separate Shopify app configurations for development, staging, and production. Do not actively develop against the live production installation.

## Relationship to existing MVQUEEN engine

The existing `15_Scripts_And_Code/mvqueen_engine` remains the reusable domain/automation layer. This app provides the dedicated Shopify app boundary around that engine rather than duplicating its catalog logic.
