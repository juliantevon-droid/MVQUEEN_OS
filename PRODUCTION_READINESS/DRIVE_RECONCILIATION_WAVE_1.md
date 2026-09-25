# MVQUEEN_OS Drive Reconciliation — Wave 1

**Date:** 2026-09-25  
**Mode:** read-only evidence collection  
**Scope:** parallel Shopify and AI system folders in the known MVQUEEN_OS Drive root

## Executive finding

The apparent duplicates are not safe to delete by name alone. The newer June folder generation closely mirrors the older May structure, while the older folders also contain unique documentation. This is structural version drift, not yet proven byte-for-byte duplication.

## Shopify systems

### Newer structure: 08_Shopify_Systems
Observed 15 child folders, including Apps_And_Integrations, Checkout_Experience, Collections, Conversion_Optimization, CSV, Exports, Launch_Checklist, Homepage, Navigation, Mobile_Optimization, Policies, Product_Templates, SEO_Optimization, Themes, and Uploads.

### Older structure: 09_Shopify_Systems
Observed the same 15 functional child folders plus a unique README.md. The folder generation dates are primarily May 14, while the parallel 08 structure is primarily June 17–18.

**Disposition:** CONFLICT / SUPERSEDED-CANDIDATE. Preserve both until child content is compared. Do not merge/delete automatically.

## AI systems

### Newer structure: 09_AI_Systems
Observed 13 functional folders: Ad_Copy_Generator, AI_Brand_Voice, APIs, Automation_Workflows, Caption_Generator, Email_Generator, Hook_Generator, Models, Pipelines, Product_Description_Generator, Prompt_Library, Prompts, and SEO_Generator.

### Older structure: 10_AI_Systems
Observed the same functional folder set plus unique material including AGENT_BRAIN_SYSTEM.md, AI_Agents, AI_Agents.md, README.md, ai_prompts.md, ai_systems_rebuilds.md, and ai_quick_reference.md.

**Disposition:** CONFLICT / REFERENCE-RICH SUPERSEDED-CANDIDATE. The newer folder cannot simply replace the older folder because the older generation contains unique documentation and agent material.

## Production interpretation

GitHub main remains authoritative for executable production code, CI, tests, agent contracts, and theme source. Drive copies must be reconciled as reference/history/backup material before any content is promoted into production.

## Next reconciliation wave

1. Compare the paired Shopify child folders with highest launch impact: Themes, Navigation, Conversion_Optimization, Mobile_Optimization, SEO_Optimization, Product_Templates.
2. Compare AI_Brand_Voice, Product_Description_Generator, SEO_Generator, Pipelines, and Prompts against current GitHub engines/contracts.
3. Extract unique useful logic from older Drive material only when it improves current canonical GitHub logic without weakening safety.
4. Record every decision; perform no Drive deletion/move during reconciliation.
