import os
import re

BIBLE = "/storage/emulated/0/MVQUEEN_OS/01_Brand_Strategy/Brand_Bible.md"
ROOT  = "/storage/emulated/0/MVQUEEN_OS"

with open(BIBLE, "r", encoding="utf-8") as f:
    content = f.read()

sections = re.split(r'\n(?=# )', content)

def get_section(keywords):
    matched = []
    for s in sections:
        first_line = s.split('\n')[0].lower()
        if any(k.lower() in first_line for k in keywords):
            matched.append(s.strip())
    return "\n\n---\n\n".join(matched) if matched else None

MAPPING = {

    # ── 04_Products ──────────────────────────────────────────────
    "04_Products/Product_Framework.md":         ["product ecosystem"],
    "04_Products/Collection_Structure.md":      ["product ecosystem", "long-term vision"],
    "04_Products/Product_Naming_System.md":     ["brand vocabulary", "semantic"],
    "04_Products/Packaging_Ideas.md":           ["sensory branding", "packaging experience"],
    "04_Products/Pricing_Strategy.md":          ["luxury positioning", "accessible luxury"],
    "04_Products/Product Photography Standards.md": ["photography direction", "cinematic femininity", "lighting philosophy"],
    "04_Products/Beauty_Products.md":           ["product ecosystem", "color psychology"],
    "04_Products/Fashion_Products.md":          ["product ecosystem", "visual identity"],
    "04_Products/Hair_Products.md":             ["product ecosystem", "sensory branding"],
    "04_Products/Accessories.md":               ["product ecosystem", "luxury positioning"],
    "04_Products/Trend_Products.md":            ["brand evolution", "future vision"],
    "04_Products/Competitor_Products.md":       ["competitive differentiation", "luxury positioning"],
    "04_Products/Product_Catalog.md":           ["product ecosystem"],
    "04_Products/Product_Templates.md":         ["product ecosystem", "brand governance"],
    "04_Products/SKU_Systems.md":               ["product ecosystem", "brand governance system"],
    "04_Products/inventory_systems.md":         ["shopify experience", "product ecosystem"],
    "04_Products/Cross-Sell Systems.md":        ["shopify experience architecture", "luxury experience"],
    "04_Products/Upsell Systems.md":            ["shopify experience architecture", "emotional pacing"],
    "04_Products/Product SEO.md":               ["seo semantic", "semantic seo", "content pillars"],

    # ── 05_SEO_And_Content ───────────────────────────────────────
    "05_SEO_And_Content/SEO_Strategy.md":       ["seo semantic", "content pillars"],
    "05_SEO_And_Content/Content_Calendar.md":   ["content pillars", "brand ritual"],
    "05_SEO_And_Content/Blog_Strategy.md":      ["content pillars", "long-term vision"],
    "05_SEO_And_Content/SEO_Clusters.md":       ["content pillars", "seo semantic"],
    "05_SEO_And_Content/Semantic SEO.md":       ["seo semantic", "brand vocabulary"],
    "05_SEO_And_Content/Search_Intent_Mapping.md": ["customer psychology", "target audience"],
    "05_SEO_And_Content/Keyword_Research.md":   ["brand vocabulary", "target audience"],
    "05_SEO_And_Content/Long_Tail_Keywords.md": ["brand vocabulary", "semantic"],
    "05_SEO_And_Content/Short_Tail_Keywords.md":["brand vocabulary", "brand meaning"],
    "05_SEO_And_Content/Metadata_Templates.md": ["brand governance", "content pillars"],
    "05_SEO_And_Content/Internal_Linking.md":   ["shopify experience", "content pillars"],
    "05_SEO_And_Content/Programmatic_SEO.md":   ["seo semantic", "brand evolution"],
    "05_SEO_And_Content/EEAT_Optimization.md":  ["emotional intelligence", "brand governance"],
    "05_SEO_And_Content/Evergreen Content.md":  ["emotional legacy", "long-term vision"],
    "05_SEO_And_Content/FAQ_Library.md":        ["customer psychology", "emotional safety"],
    "05_SEO_And_Content/Article_Structures.md": ["content pillars", "tone & voice"],
    "05_SEO_And_Content/Blog_Templates.md":     ["tone & voice", "content pillars"],
    "05_SEO_And_Content/Instagram_SEO.md":      ["content pillars", "community"],
    "05_SEO_And_Content/Pinterest_SEO.md":      ["visual identity", "content pillars"],
    "05_SEO_And_Content/TikTok_SEO.md":         ["content pillars", "community"],
    "05_SEO_And_Content/YouTube SEO.md":        ["content pillars", "long-term vision"],
    "05_SEO_And_Content/Trend_SEO.md":          ["brand evolution", "future vision"],
    "05_SEO_And_Content/Trend_Tracking.md":     ["brand evolution", "consumer"],
    "05_SEO_And_Content/Viral_Topics.md":       ["community", "emotional belonging"],
    "05_SEO_And_Content/Competitor SEO.md":     ["competitive differentiation"],

    # ── 06_Tone_And_Voice (remaining) ────────────────────────────
    "06_Tone_And_Voice/Ad_Copy_Voice.md":       ["tone & voice", "communication style"],
    "06_Tone_And_Voice/Email_Voice.md":         ["tone & voice", "emotional communication"],
    "06_Tone_And_Voice/SMS_Voice.md":           ["tone & voice", "communication style"],
    "06_Tone_And_Voice/Social_Voice.md":        ["tone & voice", "community"],
    "06_Tone_And_Voice/Product_Description_Voice.md": ["tone & voice", "luxury experience"],
    "06_Tone_And_Voice/blog_voice.md":          ["tone & voice", "content pillars"],
    "06_Tone_And_Voice/SEO Voice.md":           ["tone & voice", "seo semantic"],
    "06_Tone_And_Voice/Headline Frameworks.md": ["tone & voice", "emotional communication"],
    "06_Tone_And_Voice/Hook Systems.md":        ["emotional transformation", "buying psychology"],
    "06_Tone_And_Voice/CTA_Library.md":         ["emotional transformation", "customer experience"],
    "06_Tone_And_Voice/Messaging_Pillars.md":   ["content pillars", "tone & voice"],
    "06_Tone_And_Voice/Persuasion Frameworks.md":["customer psychology", "buying psychology"],
    "06_Tone_And_Voice/copywriting_formulas.md":["tone & voice", "communication style"],
    "06_Tone_And_Voice/copywriting_frameworks.md":["tone & voice", "brand governance"],
    "06_Tone_And_Voice/Example_Copy.md":        ["closing manifesto", "brand aura"],
    "06_Tone_And_Voice/Forbidden_Words.md":     ["brand governance", "emotional integrity"],

    # ── 07_Marketing (remaining) ─────────────────────────────────
    "07_Marketing/Funnel_Strategy.md":          ["customer psychology", "shopify experience"],
    "07_Marketing/Email_Marketing.md":          ["tone & voice", "customer experience"],
    "07_Marketing/SMS_Marketing.md":            ["tone & voice", "brand ritual"],
    "07_Marketing/Paid_Ads.md":                 ["emotional transformation", "target audience"],
    "07_Marketing/Retargeting.md":              ["customer psychology", "shopify experience"],
    "07_Marketing/Conversion_Psychology.md":    ["customer psychology", "buying psychology"],
    "07_Marketing/Product_Launch_Campaigns.md": ["brand ritual", "emotional transformation"],
    "07_Marketing/Seasonal_Campaigns.md":       ["brand ritual system", "community"],
    "07_Marketing/Giveaway_Systems.md":         ["community", "emotional belonging"],
    "07_Marketing/Affiliate_Program.md":        ["partnership & collaboration", "community"],
    "07_Marketing/Viral_Hooks.md":              ["emotional transformation", "community"],
    "07_Marketing/Analytics.md":               ["brand governance", "kpi", "long-term vision"],

    # ── 08_Social_Media ──────────────────────────────────────────
    "08_Social_Media/Content_Pillars.md":       ["content pillars"],
    "08_Social_Media/Caption_Templates.md":     ["tone & voice", "content pillars"],
    "08_Social_Media/Reel_Hooks.md":            ["emotional transformation", "cinematic"],
    "08_Social_Media/Story_Ideas.md":           ["brand story", "emotional storytelling"],
    "08_Social_Media/Carousel_Ideas.md":        ["content pillars", "visual identity"],
    "08_Social_Media/Hashtag_Systems.md":       ["brand vocabulary", "community"],
    "08_Social_Media/Engagement_Strategy.md":   ["community", "emotional belonging"],
    "08_Social_Media/Community_Building.md":    ["community & emotional belonging"],
    "08_Social_Media/Posting_Schedule.md":      ["brand ritual", "content pillars"],
    "08_Social_Media/Trend_Tracker.md":         ["brand evolution", "future vision"],
    "08_Social_Media/Viral_Content_Systems.md": ["community", "emotional transformation"],
    "08_Social_Media/Facebook_Strategy.md":     ["target audience", "content pillars"],
    "08_Social_Media/YouTube_Strategy.md":      ["content pillars", "long-term vision"],

    # ── 09_Shopify_Systems (remaining) ───────────────────────────
    "09_Shopify_Systems/Collection_Systems.md": ["shopify experience", "product ecosystem"],
    "09_Shopify_Systems/Navigation_Mapping.md": ["shopify experience architecture"],
    "09_Shopify_Systems/Conversion_Optimization.md": ["shopify experience", "customer psychology"],
    "09_Shopify_Systems/Upsell_Systems.md":     ["shopify experience", "luxury experience"],
    "09_Shopify_Systems/Store_Scaling.md":      ["long-term vision", "brand evolution"],
    "09_Shopify_Systems/Shopify_Apps.md":       ["shopify experience", "brand governance"],
    "09_Shopify_Systems/Analytics_Tracking.md": ["brand governance", "long-term vision"],
    "09_Shopify_Systems/Automation_Systems.md": ["brand governance system", "ai & luxury"],
    "09_Shopify_Systems/Product_SEO_SOP.md":    ["seo semantic", "shopify experience"],
    "09_Shopify_Systems/Product_Upload_SOP.md": ["brand governance", "product ecosystem"],
    "09_Shopify_Systems/Customer_Support_SOP.md":["customer experience", "emotional safety"],
    "09_Shopify_Systems/Shipping_SOP.md":       ["luxury experience", "packaging experience"],
    "09_Shopify_Systems/Refund_SOP.md":         ["emotional safety", "customer experience"],

    # ── 10_AI_Systems ────────────────────────────────────────────
    "10_AI_Systems/AI_Workflows.md":            ["ai & luxury", "governance & ai"],
    "10_AI_Systems/AI_Prompt_Library.md":       ["ai & luxury", "tone & voice"],
    "10_AI_Systems/Prompt_Templates.md":        ["brand governance", "tone & voice"],
    "10_AI_Systems/Ad_Copy_Prompts.md":         ["tone & voice", "emotional transformation"],
    "10_AI_Systems/Blog_Prompts.md":            ["content pillars", "tone & voice"],
    "10_AI_Systems/SEO_Prompts.md":             ["seo semantic", "tone & voice"],
    "10_AI_Systems/Social_Media_Prompts.md":    ["content pillars", "community"],
    "10_AI_Systems/Product_Description_Prompts.md": ["luxury experience", "tone & voice"],
    "10_AI_Systems/Image_Generation_Prompts.md":["creative direction", "visual identity"],
    "10_AI_Systems/Automation_Pipelines.md":    ["governance & ai", "brand evolution"],
    "10_AI_Systems/AI_Testing.md":              ["governance & ai", "brand governance"],
    "10_AI_Systems/API_Notes.md":               ["governance & ai", "ai & emotional intelligence"],
    "10_AI_Systems/OpenAI_Systems.md":          ["governance & ai", "ai & luxury"],
    "10_AI_Systems/Workflow_Automations.md":    ["brand governance system", "master workflow"],

    # ── 11_Operations ────────────────────────────────────────────
    "11_Operations/Daily_Operations.md":        ["brand ritual", "brand governance"],
    "11_Operations/Weekly_Operations.md":       ["brand ritual", "long-term vision"],
    "11_Operations/Monthly_Operations.md":      ["brand evolution", "long-term vision"],
    "11_Operations/SOPs.md":                    ["brand governance system"],
    "11_Operations/Workflow_Systems.md":        ["brand governance", "master workflow"],
    "11_Operations/KPI_Tracking.md":            ["brand governance", "long-term vision"],
    "11_Operations/Financial_Planning.md":      ["long-term vision", "luxury positioning"],
    "11_Operations/Inventory_Management.md":    ["product ecosystem", "shopify experience"],
    "11_Operations/Fulfillment_Systems.md":     ["luxury experience", "packaging experience"],
    "11_Operations/Scaling_Roadmap.md":         ["brand evolution", "long-term vision"],
    "11_Operations/Team_Structure.md":          ["internal leadership", "governance"],
    "11_Operations/Hiring_Systems.md":          ["internal leadership", "brand governance"],
    "11_Operations/Crisis_Management.md":       ["emotional safety", "brand governance"],
    "11_Operations/Productivity_Systems.md":    ["brand ritual", "brand governance system"],

    # ── 13_Research_And_Inspiration ──────────────────────────────
    "13_Research_And_Inspiration/Color_Palettes.md":     ["color psychology", "visual identity"],
    "13_Research_And_Inspiration/Typography.md":         ["visual identity system", "sensory branding"],
    "13_Research_And_Inspiration/Fashion_Inspiration.md":["visual identity", "luxury positioning"],
    "13_Research_And_Inspiration/Packaging_Inspiration.md":["sensory branding", "packaging experience"],
    "13_Research_And_Inspiration/Boutique_Inspiration.md":["luxury experience", "sensory branding"],
    "13_Research_And_Inspiration/Website_Inspiration.md":["shopify experience", "digital luxury"],
    "13_Research_And_Inspiration/Viral_Brands.md":       ["brand evolution", "community"],
    "13_Research_And_Inspiration/Consumer_Trends.md":    ["target audience", "brand evolution"],
    "13_Research_And_Inspiration/Trend_Forecasting.md":  ["brand evolution", "future vision"],
    "13_Research_And_Inspiration/Swipe_Files.md":        ["creative direction", "visual identity"],

    # ── 99_Command_Center (remaining) ────────────────────────────
    "99_Command_Center/quarterly_goals.md":     ["long-term vision", "brand evolution"],
    "99_Command_Center/priority_tasks.md":      ["brand governance", "brand ritual"],
    "99_Command_Center/current_campaigns.md":   ["brand ritual system", "content pillars"],
    "99_Command_Center/current_launches.md":    ["product ecosystem", "brand ritual"],
    "99_Command_Center/Brain_Dump.md":          ["closing manifesto", "emotional legacy"],
    "99_Command_Center/Tasks.md":               ["brand governance system", "brand ritual"],

    # ── Root files ────────────────────────────────────────────────
    "Weekly_Focus.md":                          ["brand ritual", "brand governance"],
}

written = 0
skipped = 0
no_match = 0

for rel_path, keywords in MAPPING.items():
    full_path = os.path.join(ROOT, rel_path)
    extracted = get_section(keywords)

    if not extracted:
        print(f"⚠️  No match:  {rel_path}")
        no_match += 1
        continue

    existing_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
    if existing_size > 500:
        print(f"⏭️  Has content: {rel_path}")
        skipped += 1
        continue

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- Extracted from Brand Bible -->\n\n")
        f.write(extracted)

    print(f"✅ {rel_path}")
    written += 1

print(f"\n🏁 Done — {written} written | {skipped} skipped (has content) | {no_match} no match")
