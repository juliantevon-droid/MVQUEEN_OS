# 🔄 MVQUEEN — Content Pipelines System

---

## Purpose

The Content Pipelines System is the production infrastructure that transforms brand strategy into published content — consistently, at scale, without losing quality or voice.

A pipeline is not a content calendar.
A pipeline is the engine that fills it.

---

## Pipeline Architecture

```
STRATEGY → IDEATION → BRIEFING → CREATION → REVIEW → SCHEDULING → PUBLISHING → ANALYSIS → ARCHIVE
```

Every piece of content flows through this pipeline.
No content skips stages. No content is rushed to publish without review.

---

## Content Pipeline Types

| Pipeline | Output | Cadence | AI-Assisted |
|----------|--------|---------|------------|
| Blog Pipeline | SEO articles, guides | 2-4x/month | Yes |
| Social Pipeline | Captions, hooks, carousels | Daily | Yes |
| Email Pipeline | Campaigns, sequences | 2-3x/week | Yes |
| Product Copy Pipeline | Descriptions, metadata | Per new product | Yes |
| Video Pipeline | Reel scripts, YouTube outlines | 3-5x/week | Partial |
| Ad Creative Pipeline | Copy, headlines, CTAs | Per campaign | Yes |
| UGC Pipeline | Community content curation | Ongoing | No |

---

## Pipeline 01 — Blog Content

**Weekly output:** 1-2 articles
**Average length:** 1,200-2,500 words
**Primary goal:** SEO traffic + brand authority

### Stage 1 — Ideation (Monday)
- Pull from `05_SEO_And_Content/Keyword_Research.md`
- Cross-reference with `05_SEO_And_Content/Content_Calendar.md`
- Select topic aligned with content pillar and keyword opportunity
- Define target persona for this article

### Stage 2 — Brief (Monday)
Complete brief template:
```
Topic:
Target keyword:
Secondary keywords:
Content pillar:
Target persona:
Search intent:
Target word count:
CTA at end:
Internal links to include:
```

### Stage 3 — Creation (Tuesday-Wednesday)
- Load brief into AI blog prompt system
- Generate full draft
- Human edit for voice, depth, and emotional intelligence
- Add brand-specific examples, language, and perspective

### Stage 4 — Review (Thursday)
- Voice check against Tone Guide
- SEO check: keyword placement, headers, meta
- Readability check: flows naturally, not robotic
- Image and visual brief created

### Stage 5 — Publish (Friday)
- Upload to blog platform
- Add metadata, alt text, internal links
- Pin to Pinterest
- Repurpose key section into social carousel

---

## Pipeline 02 — Social Content

**Weekly output:** 7-10 posts across platforms
**Platforms:** Instagram, TikTok, Pinterest, Facebook
**Primary goal:** Community growth + brand presence

### Weekly Social Production Rhythm

| Day | Task |
|-----|------|
| Monday | Pull weekly content themes from calendar |
| Monday | Generate 7 caption drafts via AI |
| Tuesday | Review and edit all captions for voice |
| Tuesday | Source or brief visual assets for each post |
| Wednesday | Schedule all posts for the week |
| Daily | Monitor comments and engagement |
| Friday | Analyze week's performance |

### Content Mix (Weekly)
- 2x Product-focused posts
- 2x Lifestyle / aesthetic posts
- 2x Educational / value posts
- 1x Community / UGC feature
- 1x Brand story / philosophy post
- 2x Reels / video content

### Reel Production Pipeline
```
Hook concept → Script (15-60 sec) → Film brief → Edit direction → Caption + audio → Post
```

Reel hooks generated from: `08_Social_Media/Reel_Hooks.md`
Scripts generated using: `10_AI_Systems/Social_Media_Prompts.md`

---

## Pipeline 03 — Email

**Weekly output:** 2-3 emails
**Types:** Campaigns, newsletters, automated sequences
**Primary goal:** Revenue + retention

### Campaign Email Production (Per send)

| Stage | Task | Timeline |
|-------|------|---------|
| Brief | Define campaign goal, segment, offer | 5 days before send |
| Creation | Write subject lines (3 options), preview text, body | 4 days before |
| Review | Voice, brand, offer clarity check | 3 days before |
| Design | Layout in email platform | 2 days before |
| Test | Send test to internal address | 1 day before |
| Send | Schedule for optimal time | Send day |
| Analysis | Review open rate, CTR, revenue | 48hrs post-send |

### Email Send Times (Tested Best Practices)
- Tuesday-Thursday outperforms Monday/Friday
- 10am-12pm and 7pm-9pm highest open rates
- Avoid major holidays unless campaign-relevant
- Never send more than 3 emails in one week

---

## Pipeline 04 — Product Copy

**Triggered by:** New product intake
**Output:** Title, short description, long description, SEO meta, alt text

### Product Copy Checklist

```
□ Product title (3-7 words, evocative)
□ Short description (1-2 sentences, sensory)
□ Long description (3-5 paragraphs, narrative)
□ Bullet points (key benefits, max 5)
□ SEO meta title (50-60 chars)
□ SEO meta description (150-160 chars)
□ Image alt text (all images)
□ Collection description (if new collection)
□ Upsell/cross-sell pairings identified
□ Tags applied in Shopify
□ Price set and reviewed
```

Prompts: `10_AI_Systems/Product_Description_Prompts.md`
SOP: `09_Shopify_Systems/Product_Upload_SOP.md`

---

## Pipeline 05 — Ad Creative

**Triggered by:** Campaign launch
**Output:** Primary text, headlines, CTAs, visual brief

### Ad Creative Production

| Format | Copy Elements | Volume Per Campaign |
|--------|-------------|-------------------|
| Meta Feed Ad | Primary text, headline, CTA | 3 variations |
| Meta Story/Reel Ad | Hook text, overlay copy, CTA | 2 variations |
| TikTok Spark Ad | Hook, body, CTA | 2 variations |
| Pinterest Promoted Pin | Title, description | 2 variations |

**Testing rule:** Always launch with minimum 2 creative variations.
**Kill rule:** Pause creative under 0.5% CTR after 1,000 impressions.
**Scale rule:** Increase budget on creative achieving 3x+ ROAS.

---

## Content Repurposing Matrix

| Original Content | Repurposed Into |
|-----------------|----------------|
| Blog article (1500 words) | 5 captions, 1 carousel, 1 email section, 3 Pinterest pins |
| Reel (60 sec) | TikTok, IG Reel, YouTube Short, story clip |
| Email campaign | Blog post, 2 social posts, SMS |
| Product description | Ad copy (3 formats), caption, Pinterest description |
| Customer review | Social proof caption, story graphic, email testimonial |

---

## Content Quality Gates

Before any content is published, it passes these gates:

| Gate | Check |
|------|-------|
| Voice | Sounds like MVQUEEN — not generic |
| Feeling | Makes her feel something intentional |
| Strategy | Serves a defined content pillar |
| Technical | Meets platform specifications |
| Brand | No visual or language violations |

Content that fails any gate is returned for revision — never published as-is.

---

## Content Performance Tracking

All published content is tracked at:
`14_Data_And_Analytics/`

Metrics captured per piece:
- Reach / impressions
- Engagement rate
- Link clicks (if applicable)
- Revenue attributed (if applicable)
- Saves and shares (quality signal)

Top performing content is logged in: `12_Content_Assets/` for repurposing.

---
*MVQUEEN Content Pipelines System — Operational Document*
