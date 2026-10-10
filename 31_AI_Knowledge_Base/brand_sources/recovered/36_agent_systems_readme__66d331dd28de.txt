# 🤖 MVQUEEN — Agent Systems

---

## Purpose

The Agent Systems folder is the AI orchestration layer of MVQUEEN OS — governing the design, deployment, governance, and scaling of autonomous AI agents that execute defined operational tasks within the ecosystem.

This is not a prompt folder.
This is an agent infrastructure system.

The difference:
- A **prompt** asks AI to produce one output
- An **agent** is an AI system with memory, tools, decision logic, and a defined operational role that executes across multiple steps with minimal human intervention

As MVQUEEN scales, agents will handle increasing operational complexity — content pipelines, SEO execution, product copy, customer intelligence, and more — freeing human attention for brand strategy, creative direction, and relationship building.

---

## Agent Architecture Philosophy

### The Three Laws of MVQUEEN Agents

**Law 1 — Doctrine First**
No agent has authority that supersedes brand doctrine.
Every agent operates within the emotional intelligence, voice standards, and governance principles of the MVQUEEN OS.

**Law 2 — Humans Approve, Agents Execute**
Agents generate, analyze, draft, and recommend.
Humans approve, publish, decide, and direct.
No agent publishes to customer-facing channels without a human checkpoint.

**Law 3 — Prove Before Scaling**
Every agent is tested in `26_RnD_Lab/` before deployment.
Agents are given narrow scope first — scope expands only after proven performance.

---

## Agent System Architecture

```
HUMAN INPUT (goal, brief, context)
        ↓
AGENT RECEIVES TASK
        ↓
CONTEXT LOADING
├── Brand doctrine (from 00_Doctrine/)
├── Voice standards (from 06_Tone_And_Voice/)
├── Persona context (from 03_Customer_Psychology/)
├── Product context (from 04_Products/)
└── Task-specific data
        ↓
EXECUTION LOOP
├── Step 1: Analyze input
├── Step 2: Select framework / formula
├── Step 3: Generate output
├── Step 4: Self-review against quality standards
├── Step 5: Flag exceptions for human review
└── Step 6: Deliver structured output
        ↓
HUMAN REVIEW CHECKPOINT
        ↓
APPROVED → DEPLOY
REJECTED → REVISE → LOOP
        ↓
PERFORMANCE LOG
        ↓
AGENT IMPROVEMENT CYCLE
```

---

## Agent Library

### Agent 01 — Content Agent

**Purpose:** Generate draft content across all formats — captions, blogs, emails, product copy — aligned with brand voice and content pillars.

**Trigger:** Content brief submitted (manually or via calendar automation)

**Context Required:**
- Content type and platform
- Target persona
- Content pillar
- Keyword (if SEO)
- Tone directive (aspirational / educational / narrative)

**Tools:**
- Access to Tone Guide
- Access to Hook Systems and CTA Library
- Access to Prompt Library
- Access to Forbidden Words list

**Execution Steps:**
```
1. Load brand voice context
2. Identify content framework (from Copywriting Formulas)
3. Generate hook using Hook Systems
4. Build content body
5. Apply CTA from CTA Library
6. Run forbidden word scan
7. Self-review: Does this sound like MVQUEEN?
8. Deliver draft with confidence score and revision notes
```

**Output Format:**
```
CONTENT TYPE: [format]
PLATFORM: [platform]
PERSONA: [persona]
---
DRAFT:
[content]
---
QUALITY NOTES: [any flags or suggestions]
CONFIDENCE: [High / Medium / Low]
```

**Human Review:** Required before any publishing
**Performance Metric:** % of drafts approved without major revision

---

### Agent 02 — SEO Intelligence Agent

**Purpose:** Research keywords, generate metadata, optimize content for search — aligned with brand semantic identity.

**Trigger:** New product, new blog brief, monthly SEO audit

**Context Required:**
- Page type (product / collection / blog / homepage)
- Primary topic or product category
- Target audience intent

**Tools:**
- Access to Keyword Database
- Access to SEO Strategy and Semantic SEO docs
- Access to brand vocabulary

**Execution Steps:**
```
1. Analyze topic for search intent
2. Identify primary keyword (volume + difficulty + brand alignment)
3. Generate keyword cluster (primary + 3-5 secondary)
4. Generate meta title (3 variations)
5. Generate meta description (2 variations)
6. Generate H1 and H2 structure recommendation
7. Identify internal linking opportunities
8. Deliver full SEO brief
```

**Output Format:**
```
PAGE: [page name/URL]
PRIMARY KEYWORD: [keyword] | Volume: [X] | Difficulty: [X]
SECONDARY KEYWORDS: [list]
---
META TITLE OPTIONS:
1. [option] (X chars)
2. [option] (X chars)
3. [option] (X chars)
---
META DESCRIPTION OPTIONS:
1. [option] (X chars)
2. [option] (X chars)
---
H1 RECOMMENDATION: [H1]
H2 STRUCTURE: [H2 list]
INTERNAL LINKS: [suggestions with anchor text]
```

**Human Review:** Required before implementing metadata
**Performance Metric:** Organic ranking movement for targeted keywords

---

### Agent 03 — Product Copy Agent

**Purpose:** Generate complete product copy packages for every new product — title, descriptions, metadata, bullet points, alt text.

**Trigger:** New product intake form submitted

**Context Required:**
- Product name and category
- Key attributes (texture, scent, ingredients, function)
- Target persona
- Price point
- Collection it belongs to

**Execution Steps:**
```
1. Load product intelligence
2. Identify emotional promise of product
3. Generate product title (3 options)
4. Generate short description (sensory, 2 sentences)
5. Generate long description (full narrative arc)
6. Generate 5 benefit bullets (experience-framed, not feature-listed)
7. Generate SEO metadata
8. Generate image alt text recommendations
9. Run voice review — sensory and aspirational check
10. Deliver complete copy package
```

**Output Format:**
```
PRODUCT: [name]
---
TITLE OPTIONS:
1. [option]
2. [option]
3. [option]
---
SHORT DESCRIPTION:
[2 sentences]
---
LONG DESCRIPTION:
[full copy]
---
BULLET POINTS:
• [benefit 1]
• [benefit 2]
• [benefit 3]
• [benefit 4]
• [benefit 5]
---
SEO META TITLE: [title] (X chars)
SEO META DESCRIPTION: [description] (X chars)
---
IMAGE ALT TEXT:
Image 1: [alt text]
Image 2: [alt text]
```

---

### Agent 04 — Customer Intelligence Agent

**Purpose:** Analyze customer reviews, comments, survey responses, and behavioral data to generate actionable intelligence reports.

**Trigger:** Monthly analytics review, post-launch analysis, quarterly research cycle

**Context Required:**
- Data source (reviews / comments / survey / analytics)
- Analysis focus (sentiment / buying patterns / objections / retention)
- Time period

**Execution Steps:**
```
1. Ingest raw customer data
2. Categorize by sentiment (positive / neutral / negative)
3. Extract recurring language patterns
4. Identify top desires expressed
5. Identify top objections or frustrations
6. Cross-reference with persona profiles
7. Generate insight summary
8. Generate strategic recommendations
9. Flag unexpected patterns for founder attention
```

**Output Format:**
```
ANALYSIS PERIOD: [dates]
DATA SOURCE: [source]
RECORDS ANALYZED: [number]
---
SENTIMENT OVERVIEW:
Positive: [X%] | Neutral: [X%] | Negative: [X%]
---
TOP DESIRES EXPRESSED:
1. [desire] — mentioned [X] times
2. [desire] — mentioned [X] times
3. [desire] — mentioned [X] times
---
TOP OBJECTIONS / FRUSTRATIONS:
1. [objection] — mentioned [X] times
2. [objection] — mentioned [X] times
---
RECURRING LANGUAGE (use in copy):
"[phrase]", "[phrase]", "[phrase]"
---
PERSONA ALIGNMENT NOTES:
[which personas are most active / most vocal]
---
STRATEGIC RECOMMENDATIONS:
1. [recommendation]
2. [recommendation]
3. [recommendation]
---
FLAGS FOR FOUNDER REVIEW:
[anything unexpected or requiring human judgment]
```

---

### Agent 05 — Campaign Strategy Agent

**Purpose:** Build complete campaign strategy documents from a brief — concept, content plan, copy direction, and metrics framework.

**Trigger:** Upcoming campaign date on content calendar

**Context Required:**
- Campaign type (launch / seasonal / brand / retention)
- Goal (revenue / awareness / community)
- Budget range
- Timeline
- Product or theme focus

**Execution Steps:**
```
1. Load campaign context
2. Identify campaign emotional theme (from Messaging Pillars)
3. Generate campaign concept and name
4. Build week-by-week content schedule
5. Assign content types per platform
6. Generate core copy directions (not full copy — that's Content Agent)
7. Define success metrics
8. Identify risk factors
9. Deliver complete campaign brief
```

---

### Agent 06 — Analytics Summary Agent

**Purpose:** Pull, organize, and summarize performance data on a defined schedule — delivering clear intelligence snapshots for decision-making.

**Trigger:** Monday morning (weekly), 1st of month (monthly)

**Data Sources:**
- Shopify Analytics API
- Email platform metrics
- Social platform analytics
- Ad platform reports

**Output:** Structured performance summary with trend indicators and one recommended action per metric category

---

## Agent Governance System

### Deployment Checklist
Before any agent goes live in the main OS:

```
□ Agent documented in this folder with full spec
□ Tested minimum 20 runs in R&D Lab
□ Output quality reviewed by founder
□ Failure modes identified and documented
□ Human review checkpoint confirmed in workflow
□ Performance metric defined
□ 30-day review date set
```

### Agent Performance Review (Monthly)
For each active agent:
```
□ Output approval rate (target: 80%+ approved without major revision)
□ Time saved vs manual execution
□ Any off-brand outputs in past month?
□ Any failure modes triggered?
□ Scope adjustment needed?
□ Prompt updates required?
```

### Agent Retirement Protocol
An agent is retired when:
- Output quality falls below 60% approval rate after optimization attempts
- The system it serves is replaced or restructured
- A better architecture is available
- It consistently produces off-brand results

Retired agents are archived in `98_Archive/` with documentation of why they were retired.

---
*MVQUEEN Agent Systems — Living Document*
*Updated as agents are built, deployed, optimized, and retired.*
