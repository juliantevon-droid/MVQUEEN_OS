# ⛓️ MVQUEEN — Prompt Chains System

---

## Purpose

The Prompt Chains System is the advanced AI orchestration layer of MVQUEEN — a library of sequential, chained prompts designed to produce complex, multi-stage outputs that a single prompt cannot achieve alone.

A single prompt generates a response.
A prompt chain generates a system.

---

## What Is a Prompt Chain?

A prompt chain is a sequence of prompts where each output feeds into the next input — creating layered, sophisticated results that maintain brand intelligence across every stage.

```
PROMPT 1 → OUTPUT 1 → PROMPT 2 (uses Output 1) → OUTPUT 2 → PROMPT 3 → FINAL OUTPUT
```

Prompt chains are used when:
- The output requires multiple stages of thinking
- Brand context must be preserved across a complex generation task
- Quality at each stage must be verified before proceeding
- The final output is too complex for a single prompt to produce well

---

## Core Prompt Chain Library

---

### Chain 01 — Full Product Launch Chain

**Purpose:** Generate all content needed for a complete product launch.
**Stages:** 6
**Output:** Product copy, launch email, social content, ad creative, SEO metadata

**Stage 1 — Product Intelligence Brief**
```
You are the brand intelligence system for MVQUEEN, a luxury feminine ecommerce brand.
Brand voice: quiet confidence, warm luxury, feminine precision.
Never use aggressive sales language. Always lead with feeling before function.

Product details:
- Name: [PRODUCT NAME]
- Category: [CATEGORY]
- Key attributes: [TEXTURE / SCENT / FUNCTION / INGREDIENTS]
- Target persona: [PERSONA NAME]
- Price point: [PRICE]

Generate a product intelligence brief covering:
1. The emotional promise of this product
2. The transformation it creates
3. The woman it was made for
4. Three sensory descriptors
5. The brand story behind it
```

**Stage 2 — Product Copy (uses Stage 1 output)**
```
Using this product intelligence brief: [STAGE 1 OUTPUT]

Generate:
1. Product title (3-7 words, evocative, brand-aligned)
2. Short description (2 sentences, sensory and aspirational)
3. Long description (4 paragraphs: atmosphere, transformation, product truth, invitation)
4. 5 bullet points (benefits written as experiences, not features)
5. SEO meta title (50-60 characters, keyword-led)
6. SEO meta description (150-160 characters)
```

**Stage 3 — Launch Email (uses Stage 1 + 2 output)**
```
Using this product intelligence and copy: [STAGE 1 + 2 OUTPUT]

Write a product launch email:
- Subject line: 3 variations (curiosity, identity, atmosphere-driven)
- Preview text: 1 option per subject line
- Email body: Opens with atmosphere, introduces product through transformation,
  builds desire through sensory language, closes with invitation not pressure
- CTA: Soft and inviting
Tone: Personal, warm, like a letter from someone who knows her
```

**Stage 4 — Social Content (uses Stage 1 + 2)**
```
Using this product intelligence: [STAGE 1 + 2 OUTPUT]

Generate:
1. Instagram caption (aspirational, identity-driven, ends with invitation)
2. TikTok hook (first 3 seconds — stops the scroll)
3. TikTok script (15-30 seconds, authentic, not scripted-sounding)
4. Pinterest description (SEO-aware, aesthetic, 100-150 words)
5. 3 story ideas for launch week
```

**Stage 5 — Ad Creative (uses Stage 1 + 2)**
```
Using this product intelligence: [STAGE 1 + 2 OUTPUT]

Generate 3 Meta ad variations:
Each variation includes:
- Primary text (2-3 sentences, identity or transformation angle)
- Headline (5-8 words, stops the scroll)
- Description (1 line, supports headline)
- CTA button text (beyond just "Shop Now")

Variation 1: Emotional transformation angle
Variation 2: Sensory experience angle
Variation 3: Identity/aspiration angle
```

**Stage 6 — Review & Alignment Check**
```
Review all content generated across Stages 2-5.

Check each piece against these standards:
1. Does it sound like MVQUEEN — not a generic brand?
2. Does it lead with feeling before function?
3. Is any language too aggressive or salesy?
4. Is the voice consistent across all pieces?
5. Does any piece contain forbidden language patterns?

Flag any issues and provide revised versions.
```

---

### Chain 02 — Blog Article SEO Chain

**Purpose:** Generate a fully optimized, brand-aligned blog article.
**Stages:** 4
**Output:** Complete SEO article with brand voice

**Stage 1 — SEO Research Brief**
```
Topic: [TOPIC]
Primary keyword: [KEYWORD]
Secondary keywords: [KEYWORD 2], [KEYWORD 3]
Search intent: [informational / transactional / navigational]
Target persona: [PERSONA]

Generate:
1. Recommended article title (H1) — brand voice, keyword-led
2. Article outline with H2 and H3 structure
3. Key points to cover per section
4. Recommended word count per section
5. Internal linking opportunities
6. CTA recommendation for end of article
```

**Stage 2 — Article Draft (uses Stage 1)**
```
Using this outline: [STAGE 1 OUTPUT]

Write the full article in MVQUEEN brand voice:
- Warm, intelligent, feminine — not clinical or generic
- Sensory language where relevant
- Emotional intelligence woven into practical advice
- Never keyword-stuffed — keywords placed naturally
- Opens with atmosphere or a woman-centered scenario
- Closes with an invitation, not just information
Target length: [WORD COUNT]
```

**Stage 3 — SEO Optimization (uses Stage 2)**
```
Review this article draft: [STAGE 2 OUTPUT]

Optimize for SEO without compromising brand voice:
1. Confirm primary keyword in: title, first 100 words, 2-3 H2s, conclusion
2. Confirm secondary keywords placed naturally throughout
3. Suggest image alt text for 3 images
4. Write optimized meta title (50-60 chars)
5. Write optimized meta description (150-160 chars)
6. Identify 3 internal linking opportunities with anchor text
```

**Stage 4 — Final Voice Review (uses Stage 2 + 3)**
```
Final review of this article: [STAGE 2 + 3 OUTPUT]

Check:
1. Opening paragraph — does it pull you in?
2. Any sections that sound robotic or generic?
3. Any overuse of a single word or phrase?
4. Does the conclusion feel like an invitation?
5. Overall — does this sound like MVQUEEN editorial?

Provide specific revision suggestions for any weak sections.
```

---

### Chain 03 — Customer Persona Research Chain

**Purpose:** Generate deep customer intelligence from research inputs.
**Stages:** 3
**Output:** Detailed persona profile with strategy recommendations

**Stage 1 — Raw Research Analysis**
```
Analyze the following customer data sources:
[REVIEWS / SURVEY RESPONSES / SOCIAL COMMENTS / ANALYTICS DATA]

Extract:
1. Recurring emotional language customers use
2. Primary desires and aspirations expressed
3. Frustrations and objections mentioned
4. Purchase decision triggers identified
5. Lifestyle signals and identity markers
6. Language patterns — exact words and phrases they use
```

**Stage 2 — Persona Construction (uses Stage 1)**
```
Using this research analysis: [STAGE 1 OUTPUT]

Build a detailed customer persona:
- Name and archetype
- Age range and life stage
- Emotional identity (how she sees herself, wants to see herself)
- Primary desires (what she wants from MVQUEEN)
- Core fears and objections (what stops her from buying)
- Buying psychology (how she makes decisions)
- Lifestyle and aesthetic values
- Content she responds to
- Language that resonates with her
- What makes her loyal to a brand
```

**Stage 3 — Strategy Recommendations (uses Stage 1 + 2)**
```
Using this persona profile: [STAGE 2 OUTPUT]

Generate strategic recommendations:
1. Top 3 messaging angles that will resonate
2. Content types and formats she prefers
3. Platforms where she is most reachable
4. Offer structures that match her psychology
5. Retention strategies aligned with her loyalty triggers
6. Language and words to use — and avoid — with her
```

---

### Chain 04 — Campaign Strategy Chain

**Purpose:** Build a complete campaign strategy from concept to execution.
**Stages:** 4
**Output:** Full campaign brief, content plan, copy, and metrics

**Stage 1 — Campaign Concept**
```
Campaign type: [PRODUCT LAUNCH / SEASONAL / BRAND / REENGAGEMENT]
Goal: [AWARENESS / SALES / RETENTION / COMMUNITY]
Budget: [BUDGET RANGE]
Timeline: [DATES]
Target persona: [PERSONA]

Generate:
1. Campaign concept and emotional theme
2. Core message (one sentence — the campaign truth)
3. Visual direction brief
4. Campaign name
5. Key offer or hook
```

**Stage 2 — Content Plan (uses Stage 1)**
```
Using this campaign concept: [STAGE 1 OUTPUT]

Build the content plan:
- Week-by-week content schedule
- Platform-by-platform breakdown
- Content types per platform
- Posting frequency
- Email sequence timing
- Ad launch and scaling timeline
```

**Stage 3 — Copy Generation (uses Stage 1 + 2)**
```
Using this campaign concept and plan: [STAGE 1 + 2 OUTPUT]

Generate:
1. Hero campaign caption (IG/TikTok)
2. Email 1 — campaign launch
3. Email 2 — mid-campaign nurture
4. Email 3 — final push (never pressure — invitation)
5. 3 ad headlines
6. SMS campaign message (160 chars)
```

**Stage 4 — Metrics Framework**
```
Using this campaign brief: [STAGE 1 OUTPUT]

Define:
1. Primary success metric
2. Secondary metrics to track
3. Daily check-in data points
4. Go/no-go decision criteria for ad scaling
5. End-of-campaign analysis framework
```

---

## Prompt Chain Governance

1. All prompt chains are versioned — label each version clearly
2. Stage outputs are saved before proceeding to next stage
3. Human review at minimum at Stage final output
4. Chains are updated when brand voice evolves
5. New chains are documented here before deployment
6. Performance of chain outputs is tracked and used to refine prompts

---
*MVQUEEN Prompt Chains System — Operational Document*
