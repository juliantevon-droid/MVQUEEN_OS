# Prompt Chain Library
## MVQUEEN_OS / 38_Prompt_Chains

---

## Purpose

Library of multi-step AI prompt sequences for complex MVQUEEN tasks. Prompt chains produce better output than single prompts for creative, strategic, and analytical work.

---

## Chain Architecture

A prompt chain is a sequence of prompts where each output feeds the next input.

```
Prompt 1 (Context Load) → Prompt 2 (Analysis) → Prompt 3 (Generation) → Prompt 4 (Refinement)
```

---

## Chain Library

### Chain 01 — Product Description Chain
```
Step 1: Load brand voice rules + product category context
Step 2: Generate 3 description variations
Step 3: Select strongest, refine for SEO
Step 4: Final voice check + format
```

### Chain 02 — Content Calendar Chain
```
Step 1: Load brand themes + current promotions
Step 2: Generate monthly content themes
Step 3: Expand into weekly topics
Step 4: Assign to platforms + formats
```

### Chain 03 — Email Campaign Chain
```
Step 1: Define campaign goal + audience segment
Step 2: Generate subject line variations (5+)
Step 3: Write email body
Step 4: Write SMS companion
Step 5: Review for voice alignment
```

### Chain 04 — SEO Content Chain
```
Step 1: Load target keyword + search intent
Step 2: Generate content outline
Step 3: Write section by section
Step 4: Optimize meta title + description
Step 5: Internal link recommendations
```

### Chain 05 — Ad Copy Chain
```
Step 1: Define product + audience + platform
Step 2: Generate 5 hook variations
Step 3: Write 3 full ad copy variations
Step 4: Select winner + write 2 headline variants
Step 5: Format for platform specs
```

---

## Implementation Reference
All chains should be executed by the appropriate AI agent:
*   **Content Chains (01, 02, 03, 05):** Use [Content_Agent_Prompt.md](../10_AI_Systems/Content_Agent_Prompt.md).
*   **SEO Chains (04):** Use [SEO_Agent_Prompt.md](../10_AI_Systems/SEO_Agent_Prompt.md).

---

## Status
**Active** — Linked to operational agents.
