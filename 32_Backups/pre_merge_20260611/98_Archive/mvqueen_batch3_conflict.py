#!/usr/bin/env python3
"""MVQUEEN_OS — Batch 3: Folders 30–39 + 98_Archive"""

import os

BASE = "/storage/emulated/0/MVQUEEN_OS"

files = {

# ── 30_AI_Datasets ─────────────────────────────────────────────────────────
"30_AI_Datasets/dataset_index.md": """# AI Dataset Index
## MVQUEEN_OS / 30_AI_Datasets

---

## Purpose

Stores curated datasets that train, inform, or calibrate AI systems operating within the MVQUEEN ecosystem. Every dataset must be doctrine-aligned and voice-consistent.

---

## Dataset Types

| Type | Description | Use |
|---|---|---|
| Voice Samples | Approved copy examples | AI voice calibration |
| Product Data | Titles, descriptions, specs | AI product writing |
| Customer Language | Real customer words, phrases | Copy resonance |
| Competitor Analysis | Market positioning data | Strategic reference |
| SEO Data | Keywords, search intent clusters | Content + SEO AI |
| Hook Library | Proven opening lines | AI content generation |

---

## Dataset Standards

All datasets must:
- be reviewed for brand voice alignment before use
- be stored as clean `.md` or `.json` files
- include a source note and date collected
- never contain personally identifiable customer information

---

## Active Datasets

| Dataset | File | Status |
|---|---|---|
| Voice calibration samples | Pull from `06_Tone_And_Voice` | Active |
| Hook library | Pull from `06_Tone_And_Voice/Hook_Systems.md` | Active |
| Product description examples | Pull from `12_Content_Assets` | Active |

---

## Status
Active
""",

"30_AI_Datasets/voice_calibration_dataset.md": """# Voice Calibration Dataset
## MVQUEEN_OS / 30_AI_Datasets

---

## Purpose

Curated set of approved MVQUEEN copy examples used to calibrate AI output. When prompting AI systems, reference this file to establish the correct voice before generating content.

---

## Approved Voice Examples

### Product Description — Fragrance
She sprays it before she's ready. That's the ritual. A scent that settles into skin like a decision — warm, deliberate, unmistakably hers.

### Product Description — Jewelry
Delicate doesn't mean small. This piece sits quietly until the room notices. Wear it like you already knew it would.

### Caption — Empowerment
She's not waiting for permission to feel like this. Neither are you.

### Caption — Product Launch
New. And worth the wait. [Product name] is here.

### Email Opening — Welcome
You found us. Or maybe you already knew you belonged here. Either way — welcome to the world.

### Hook — TikTok
The scent that made three people ask what I was wearing in one day →

### CTA — Soft
Step into it →

### CTA — Confident
Claim yours →

---

## Voice Anti-Examples (Do Not Use)

❌ "We are excited to announce..."
❌ "This amazing product will change your life!"
❌ "Hurry! Limited time only!!!"
❌ "Emotionally resonant fragrance experience"
❌ Any sentence starting with "We believe..."

---

## Status
Active
""",

"30_AI_Datasets/README.md": """# 30_AI_Datasets
## MVQUEEN_OS

Curated datasets for training and calibrating AI systems within the MVQUEEN ecosystem. Voice samples, product data, and SEO data stored here.
""",

# ── 31_AI_Knowledge_Base ───────────────────────────────────────────────────
"31_AI_Knowledge_Base/knowledge_base_index.md": """# AI Knowledge Base Index
## MVQUEEN_OS / 31_AI_Knowledge_Base

---

## Purpose

Centralized knowledge repository that AI systems can query to produce doctrine-aligned, brand-accurate outputs. This is the intelligence layer above the dataset layer.

---

## Knowledge Domains

| Domain | Source Files | Priority |
|---|---|---|
| Brand Identity | `01_Brand_Strategy/` | Critical |
| Voice + Tone | `06_Tone_And_Voice/` | Critical |
| Customer Psychology | `03_Customer_Psychology/` | High |
| Product Knowledge | `04_Products/` | High |
| SEO Strategy | `05_SEO_And_Content/` | High |
| Doctrine Rules | `00_Doctrine/` | Constitutional |

---

## Knowledge Base Architecture

```
31_AI_Knowledge_Base/
├── brand_summary.md          ← Compressed brand identity for AI context
├── voice_rules.md            ← Hard voice rules for AI
├── customer_profile.md       ← Compressed customer psychology
├── product_knowledge.md      ← Product categories and positioning
└── knowledge_base_index.md   ← This file
```

---

## Usage Protocol

When initializing an AI session for MVQUEEN work:
1. Load `00_Doctrine/master_doctrine.md`
2. Load `31_AI_Knowledge_Base/brand_summary.md`
3. Load `31_AI_Knowledge_Base/voice_rules.md`
4. Load task-specific files as needed

---

## Status
Active
""",

"31_AI_Knowledge_Base/brand_summary.md": """# Brand Summary — AI Context File
## MVQUEEN_OS / 31_AI_Knowledge_Base

---

## Use This File

Load this at the start of any AI session requiring brand knowledge. It is a compressed, AI-optimized summary of the full Brand Bible.

---

## Brand Identity

**Name:** MVQUEEN (Most Valuable Queen)
**Sister Brand:** Miss.Queen
**Category:** Accessible luxury feminine lifestyle
**Positioning:** Luxury aesthetics at real-world prices
**Audience:** Women who want to feel elegant, confident, and worthy without overspending

---

## Voice in One Sentence
Quiet confidence. Warm luxury. Feminine precision. Never loud, never generic, never apologetic.

---

## Core Emotional Pillars
- Confidence without arrogance
- Softness without weakness
- Elegance without exclusivity
- Transformation through beauty and self-care

---

## What MVQUEEN Is Not
- Not a budget brand
- Not loud or aggressive
- Not generic or trend-chasing
- Not emotionally hollow
- Not corporate in tone

---

## Product Universe
Fashion, beauty, skincare, haircare, fragrance, jewelry, shoes, feminine lifestyle essentials

---

## Hard Voice Rules
1. Never start with "We are excited to..."
2. Never use exclamation points in excess
3. Never use the word "emotionally" as a filler
4. Write to one woman — never a crowd
5. Luxury is felt, not announced

---

## Status
Active — use at session start
""",

"31_AI_Knowledge_Base/voice_rules.md": """# Voice Rules — AI Reference
## MVQUEEN_OS / 31_AI_Knowledge_Base

---

## Hard Rules (Never Violate)

| Rule | Correct | Incorrect |
|---|---|---|
| Tone | Quiet confidence | Loud excitement |
| Person | Write to one woman | Write to "everyone" |
| Luxury | Show it, don't announce it | "This luxury product..." |
| Punctuation | Deliberate, minimal | Multiple !! or ??? |
| Forbidden word | Never use "emotionally" as filler | "emotionally resonant" |
| Opening | Hook or statement | "We are pleased to..." |
| CTA | Soft, directional | "BUY NOW!!!" |

---

## Tone Spectrum

| Context | Tone |
|---|---|
| Product description | Sensory, precise, warm |
| Instagram caption | Confident, brief, intimate |
| TikTok hook | Bold, pattern-interrupt |
| Email | Personal, value-first |
| SMS | Direct, exclusive |
| Blog | Editorial, knowledgeable |

---

## Sentence Construction

- Short sentences land harder than long ones
- White space is part of the voice
- One idea per sentence when impact matters
- Fragments are allowed when deliberate

---

## Words That Work
elegant, deliberate, soft, worthy, signature, ritual, quiet, precise, refined, elevated, intentional

## Words to Avoid
amazing, excited, incredible, game-changer, revolutionary, literally, honestly, basic

---

## Status
Active
""",

"31_AI_Knowledge_Base/README.md": """# 31_AI_Knowledge_Base
## MVQUEEN_OS

Intelligence layer for AI systems — compressed brand knowledge, voice rules, and customer profiles optimized for AI context loading.
""",

# ── 32_Backups ─────────────────────────────────────────────────────────────
"32_Backups/backup_protocol.md": """# Backup Protocol
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
""",

"32_Backups/README.md": """# 32_Backups
## MVQUEEN_OS

Backup protocol, versioning standards, and recovery procedures for MVQUEEN_OS files.
""",

# ── 33_Content_Pipelines ───────────────────────────────────────────────────
"33_Content_Pipelines/content_pipeline_system.md": """# Content Pipeline System
## MVQUEEN_OS / 33_Content_Pipelines

---

## Purpose

Defines the end-to-end content production pipeline for MVQUEEN — from idea to published, every step documented and systematized.

---

## Pipeline Overview

```
Idea → Brief → Create → Review → Schedule → Publish → Analyze → Archive
```

---

## Stage Definitions

### Stage 1 — Idea
- Source: content calendar, trending topics, product launches, customer questions
- Document in weekly planning session
- Assign to content type: video / graphic / caption / email / blog

### Stage 2 — Brief
- Fill out visual brief template (see `12_Content_Assets/visual_brief_templates.md`)
- Define: platform, format, tone, CTA, deadline

### Stage 3 — Create
- First draft created (AI-assisted or manual)
- Visual assets produced or sourced
- Voice check against `06_Tone_And_Voice/Tone_Guide.md`

### Stage 4 — Review
- Read aloud test: does it sound like MVQUEEN?
- Brand rule check: `02_Brand_Identity/brand_rules.md`
- Final approval before scheduling

### Stage 5 — Schedule
- Platform-specific formatting applied
- Hashtags added (reference `08_Social_Media`)
- Scheduled via platform scheduler or Later/Buffer

### Stage 6 — Publish + Monitor
- Confirm published correctly
- Monitor comments/engagement in first 2 hours
- Respond to comments within response time window

### Stage 7 — Analyze
- Pull metrics at Day 3 and Day 7
- Log in analytics dashboard (`14_Data_And_Analytics`)
- Note: what worked, what to repeat, what to adjust

### Stage 8 — Archive
- Move to content archive with date tag
- High-performers flagged for repurposing

---

## Content Calendar Rhythm

| Cadence | Platform | Volume |
|---|---|---|
| Daily | TikTok | 1 video |
| 5x/week | Instagram | Mix of Reels, Feed, Stories |
| 5-10x/day | Pinterest | Scheduled pins |
| 1x/week | Email | Newsletter |
| 2x/week | Blog | SEO articles |

---

## Status
Active
""",

"33_Content_Pipelines/content_calendar_framework.md": """# Content Calendar Framework
## MVQUEEN_OS / 33_Content_Pipelines

---

## Purpose

Governs the content calendar system — how content is planned, batched, and distributed across the MVQUEEN ecosystem.

---

## Planning Rhythm

| Session | Frequency | Output |
|---|---|---|
| Monthly planning | First Sunday of month | 30-day content themes |
| Weekly planning | Sunday evening | 7-day calendar |
| Daily execution | Each morning | Confirm schedule, engage |

---

## Monthly Theme Framework

Each month should have:
- 1 primary product focus
- 1 brand story theme
- 1 educational angle
- 1 community/UGC push
- Seasonal or cultural moment (if relevant)

---

## Content Mix Formula (Weekly)

| Type | % of Content |
|---|---|
| Product-forward | 30% |
| Lifestyle / Aspirational | 30% |
| Educational / Value | 20% |
| Community / UGC | 10% |
| Behind the scenes | 10% |

---

## Batching Protocol

Batch content creation by type, not by day:
- Film all videos in one session
- Write all captions in one session
- Edit all graphics in one session
- Schedule all at once

---

## Status
Active
""",

"33_Content_Pipelines/README.md": """# 33_Content_Pipelines
## MVQUEEN_OS

End-to-end content production pipeline and calendar framework. Every piece of content moves through a defined system — idea to archive.
""",

# ── 34_Master_Systems ──────────────────────────────────────────────────────
"34_Master_Systems/master_system_index.md": """# Master System Index
## MVQUEEN_OS / 34_Master_Systems

---

## Purpose

The Master Systems folder is the architectural overview layer — it maps how all MVQUEEN systems connect, depend on each other, and operate as a unified ecosystem.

---

## System Map

```
00_Doctrine ─────────────────────── Constitutional Layer
     │
     ├── 01_Brand_Strategy ───────── Identity + Positioning
     ├── 02_Brand_Identity ───────── Visual + Voice Identity
     ├── 03_Customer_Psychology ──── Audience Intelligence
     ├── 04_Products ─────────────── Product Catalog
     ├── 05_SEO_And_Content ──────── Discovery Layer
     ├── 06_Tone_And_Voice ───────── Voice Governance
     ├── 07_Marketing ────────────── Acquisition
     ├── 08_Social_Media ─────────── Distribution
     ├── 09_Shopify_Systems ──────── Commerce Layer
     ├── 10_AI_Systems ───────────── Intelligence Layer
     ├── 11_Operations ───────────── Execution Layer
     └── 99_Command_Center ───────── Control Hub
```

---

## Cross-System Dependencies

| System | Depends On | Feeds Into |
|---|---|---|
| Content | Tone + Voice, Brand Identity | Social, Email, SEO |
| SEO | Brand Strategy, Product | Shopify, Blog |
| AI Systems | Doctrine, Knowledge Base | All systems |
| Marketing | Customer Psychology, Analytics | All channels |
| Shopify | Product, Brand Identity | Revenue |

---

## Master Rules

1. All systems inherit from `00_Doctrine`
2. No system operates in isolation
3. Changes to Brand Identity cascade to all output systems
4. AI systems query the Knowledge Base before generating

---

## Status
Active
""",

"34_Master_Systems/README.md": """# 34_Master_Systems
## MVQUEEN_OS

Architectural overview of all MVQUEEN systems — how they connect, depend, and operate as a unified ecosystem.
""",

# ── 35_System_Blueprints ───────────────────────────────────────────────────
"35_System_Blueprints/blueprint_index.md": """# System Blueprint Index
## MVQUEEN_OS / 35_System_Blueprints

---

## Purpose

Detailed technical blueprints for building and deploying each major MVQUEEN system. Blueprints live here before systems are built — they are the architectural plans.

---

## Blueprint Library

| Blueprint | Status | Priority |
|---|---|---|
| Email System Blueprint | Build | High |
| Paid Ads System Blueprint | Build | High |
| SEO Content System Blueprint | Build | High |
| Shopify Optimization Blueprint | Build | High |
| AI Agent Blueprint | Planned | Medium |
| Creator Program Blueprint | Planned | Low |

---

## Blueprint Template

```
## System Blueprint: [System Name]
**Purpose:** [What this system does]
**Dependencies:** [What it needs to function]
**Inputs:** [What goes in]
**Outputs:** [What comes out]
**Tools Required:** [Platform / software]
**Build Steps:**
  1. [Step 1]
  2. [Step 2]
  3. ...
**Success Criteria:** [How we know it's working]
**Owner:** [Who maintains it]
```

---

## Email System Blueprint

**Purpose:** Automated email flows that generate revenue while preserving brand voice
**Dependencies:** Klaviyo, product catalog, customer segments
**Tools:** Klaviyo, Shopify
**Key Flows:**
- Welcome series (3 emails)
- Abandoned cart (3 touches: email, SMS, email)
- Post-purchase (4 emails)
- Win-back (3 emails)
- Browse abandonment (2 emails)

**Success Criteria:** 35%+ open rate, 3%+ click rate, 15%+ revenue attribution

---

## Status
Active
""",

"35_System_Blueprints/README.md": """# 35_System_Blueprints
## MVQUEEN_OS

Technical blueprints for all major MVQUEEN systems. Plans are documented here before systems are built.
""",

# ── 36_Agent_Systems ───────────────────────────────────────────────────────
"36_Agent_Systems/agent_architecture.md": """# Agent Architecture
## MVQUEEN_OS / 36_Agent_Systems

---

## Purpose

Defines the AI agent infrastructure for MVQUEEN — autonomous systems that handle repetitive, high-volume, or complex tasks while preserving brand voice and doctrine alignment.

---

## Agent Philosophy

MVQUEEN agents must:
- always operate within doctrine constraints
- produce brand-voice output — never generic
- flag for human review when uncertain
- never publish without review on sensitive content
- fail gracefully — errors must be visible, not silent

---

## Planned Agent Types

| Agent | Function | Status |
|---|---|---|
| Content Agent | Generates captions, emails, product copy | Planned |
| SEO Agent | Generates meta titles, descriptions, blog outlines | Planned |
| Customer Service Agent | First-response to common inquiries | Planned |
| Analytics Agent | Pulls and summarizes weekly metrics | Planned |
| Inventory Agent | Monitors stock levels, alerts on low inventory | Planned |

---

## Agent Workflow (Standard)

```
Trigger → Load Doctrine Context → Load Task Brief → Generate Output → Review Flag → Human Approval → Deploy
```

---

## Context Loading Protocol

Every agent session must load:
1. `00_Doctrine/master_doctrine.md`
2. `31_AI_Knowledge_Base/brand_summary.md`
3. `31_AI_Knowledge_Base/voice_rules.md`
4. Task-specific files

---

## Status
Active — architecture defined, agents in planning
""",

"36_Agent_Systems/README.md": """# 36_Agent_Systems
## MVQUEEN_OS

AI agent architecture, workflow protocols, and deployment standards for MVQUEEN autonomous systems.
""",

# ── 37_Databases ───────────────────────────────────────────────────────────
"37_Databases/database_index.md": """# Database Index
## MVQUEEN_OS / 37_Databases

---

## Purpose

Documents all structured data stores within the MVQUEEN ecosystem — product databases, customer segments, keyword databases, and content libraries.

---

## Database Registry

| Database | Format | Location | Purpose |
|---|---|---|---|
| Product Catalog | Shopify / CSV | Shopify Admin | All active products |
| Keyword Database | Markdown / CSV | `05_SEO_And_Content` | SEO targeting |
| Customer Segments | Klaviyo | Klaviyo | Email targeting |
| Content Library | Markdown | `12_Content_Assets` | Reusable content |
| Hook Library | Markdown | `06_Tone_And_Voice` | Opening lines |
| CTA Library | Markdown | `06_Tone_And_Voice` | Call-to-action copy |
| Ecosystem Index | JSON | `_ecosystem_index.json` | OS file map |

---

## Data Standards

- All CSV files use UTF-8 encoding
- Markdown databases use consistent table formatting
- JSON files must be validated before use
- No PII stored in OS — customer data lives in Klaviyo/Shopify only

---

## Status
Active
""",

"37_Databases/README.md": """# 37_Databases
## MVQUEEN_OS

Registry of all structured data stores across the MVQUEEN ecosystem — product, customer, keyword, and content databases.
""",

# ── 38_Prompt_Chains ───────────────────────────────────────────────────────
"38_Prompt_Chains/prompt_chain_library.md": """# Prompt Chain Library
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

## Status
Active
""",

"38_Prompt_Chains/README.md": """# 38_Prompt_Chains
## MVQUEEN_OS

Multi-step AI prompt sequences for complex creative, strategic, and analytical tasks. Chains produce better output than single prompts.
""",

# ── 39_SOP_Library ─────────────────────────────────────────────────────────
"39_SOP_Library/sop_index.md": """# SOP Index
## MVQUEEN_OS / 39_SOP_Library

---

## Purpose

Master index of all Standard Operating Procedures for MVQUEEN. SOPs ensure consistency, quality, and speed across all operations — regardless of who executes them.

---

## SOP Categories

| Category | SOPs |
|---|---|
| Content | Product photo shoot, caption writing, video posting |
| Shopify | New product upload, inventory update, collection management |
| Customer Service | DM response, complaint handling, refund processing |
| Marketing | Campaign launch, ad setup, email send |
| Operations | Weekly review, monthly audit, backup protocol |
| AI | Session initialization, output review, prompt execution |

---

## SOP Template

```
## SOP: [Name]
**Version:** 1.0
**Owner:** [Role]
**Last Updated:** [Date]
**Trigger:** [What initiates this SOP]

---

### Steps
1. [Step 1]
2. [Step 2]
3. ...

### Quality Check
- [ ] [Check 1]
- [ ] [Check 2]

### Notes
[Any exceptions or edge cases]
```

---

## Core SOPs (Priority Build)

### SOP: New Product Upload (Shopify)
1. Photograph product (reference visual brief template)
2. Write title: `[Product Name] — [Category] | MVQUEEN`
3. Write description (use product description chain)
4. Add meta title + description (SEO-optimized)
5. Set price per pricing system
6. Add to correct collection
7. Tag correctly
8. Preview on mobile before publishing
9. Publish
10. Create 3 Pinterest pins within 24 hours

### SOP: Weekly Content Batch
1. Sunday: plan 7 days of content in calendar
2. Batch film all videos in one session
3. Write all captions using voice rules
4. Edit and format all graphics
5. Schedule all posts
6. Confirm Monday posts are live

### SOP: AI Session Initialization
1. Load `00_Doctrine/master_doctrine.md`
2. Load `31_AI_Knowledge_Base/brand_summary.md`
3. Load `31_AI_Knowledge_Base/voice_rules.md`
4. State task clearly
5. Review all output before use

---

## Status
Active
""",

"39_SOP_Library/README.md": """# 39_SOP_Library
## MVQUEEN_OS

Master SOP library for all MVQUEEN operations. Every repeated task has a documented procedure — consistency is the standard.
""",

# ── 98_Archive ─────────────────────────────────────────────────────────────
"98_Archive/archive_log.md": """# Archive Log
## MVQUEEN_OS / 98_Archive

---

## Purpose

Long-term archive for files that have been superseded, restructured, or retired from active use. Unlike `28_Archives` (operational archive), `98_Archive` is the permanent historical record.

---

## Archive Log

| File | Original Location | Archived Date | Reason |
|---|---|---|---|
| [None yet] | | | |

---

## Archive Rules

1. Files here are read-only — never edit archived content
2. Log every entry with reason and date
3. Review quarterly — permanent deletion requires founder decision
4. Distinguish from `28_Archives`: 98 is permanent history, 28 is recent operational archive

---

## Status
Active
""",

"98_Archive/README.md": """# 98_Archive
## MVQUEEN_OS

Permanent historical archive. Long-term storage for superseded files. Read-only — log all entries in `archive_log.md`.
""",

}

created = 0
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {rel_path}")
    created += 1

print(f"\n🟣 Batch 3 complete — {created} files created")
