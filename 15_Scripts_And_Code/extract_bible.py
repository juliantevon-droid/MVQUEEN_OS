import os
import re

BIBLE = "/storage/emulated/0/MVQUEEN_OS/01_Brand_Strategy/Brand_Bible.md"
ROOT  = "/storage/emulated/0/MVQUEEN_OS"

# Read the full Bible
with open(BIBLE, "r", encoding="utf-8") as f:
    content = f.read()

# Split into sections by top-level headers
sections = re.split(r'\n(?=# )', content)

def get_section(keywords):
    """Extract all sections matching any keyword."""
    matched = []
    for s in sections:
        first_line = s.split('\n')[0].lower()
        if any(k.lower() in first_line for k in keywords):
            matched.append(s.strip())
    return "\n\n---\n\n".join(matched) if matched else None

# Map: target file → keywords to extract from Bible
MAPPING = {
    # 01_Brand_Strategy
    "01_Brand_Strategy/Mission_And_Vision.md":      ["mission", "vision"],
    "01_Brand_Strategy/Brand_Story.md":             ["brand story", "story"],
    "01_Brand_Strategy/Brand_Values.md":            ["brand values", "values"],
    "01_Brand_Strategy/Brand_Positioning.md":       ["positioning"],
    "01_Brand_Strategy/Brand_Personality.md":       ["personality"],
    "01_Brand_Strategy/Brand_Essence.md":           ["essence"],
    "01_Brand_Strategy/Emotional_Transformation.md":["emotional transformation"],
    "01_Brand_Strategy/Elevator_Pitch.md":          ["brand overview", "brand meaning"],
    "01_Brand_Strategy/brand_manifesto.md":         ["closing manifesto", "declaration"],
    "01_Brand_Strategy/brand_philosophy.md":        ["emotional intelligence principles", "governance"],
    "01_Brand_Strategy/USP.md":                     ["competitive differentiation", "positioning"],
    "01_Brand_Strategy/Taglines.md":                ["brand aura", "essence of mvqueen"],
    "01_Brand_Strategy/Slogans.md":                 ["emotional transformation statement", "what the brand truly sells"],

    # 06_Tone_And_Voice
    "06_Tone_And_Voice/Tone_Guide.md":              ["communication style", "emotional communication"],
    "06_Tone_And_Voice/Luxury_Language.md":         ["luxury experience standards", "emotional luxury"],
    "06_Tone_And_Voice/Feminine_Language.md":       ["feminine philosophy", "femininity"],
    "06_Tone_And_Voice/Emotional_Language.md":      ["emotional intelligence", "emotional safety"],
    "06_Tone_And_Voice/Brand_Messaging.md":         ["emotional recognition", "brand aura"],
    "06_Tone_And_Voice/Voice_Consistency_Rules.md": ["brand governance", "emotional integrity"],
    "06_Tone_And_Voice/Writing_Rules.md":           ["creative governance", "emotional quality control"],
    "06_Tone_And_Voice/Storytelling Frameworks.md": ["emotional storytelling", "cinematic femininity"],

    # 03_Customer_Psychology (supplement existing)
    "03_Customer_Psychology/Customer_Personas.md":  ["customer personas", "persona 01", "persona 02", "persona 03", "persona 04"],
    "03_Customer_Psychology/Buying_Psychology.md":  ["buying psychology"],
    "03_Customer_Psychology/Identity_Aspirations.md":["aspiration", "emotional identity shift"],
    "03_Customer_Psychology/Customer_Transformation.md":["transformation process", "after mvqueen", "before mvqueen"],

    # 02_Brand_Identity
    "02_Brand_Identity/brand_rules.md":             ["brand governance", "emotional integrity standards"],
    "02_Brand_Identity/photography_direction.md":   ["photography direction", "cinematic femininity", "lighting philosophy"],
    "02_Brand_Identity/videography_direction.md":   ["video & motion", "emotional storytelling direction"],

    # 07_Marketing
    "07_Marketing/Campaign_Strategy.md":            ["emotional transformation", "brand evolution"],
    "07_Marketing/Offer_Strategy.md":               ["accessible luxury", "aspiration without exclusion"],
    "07_Marketing/Influencer_Strategy.md":          ["community governance", "partnership & collaboration"],
    "07_Marketing/UGC_Strategy.md":                 ["community over consumers", "community governance"],

    # 09_Shopify_Systems
    "09_Shopify_Systems/Store_Structure.md":        ["digital luxury experience", "customer experience standards"],
    "09_Shopify_Systems/Checkout_Optimization.md":  ["emotional pacing", "luxury experience"],
    "09_Shopify_Systems/Homepage_Layout.md":        ["emotional visual identity", "luxury atmosphere"],

    # 99_Command_Center
    "99_Command_Center/executive_overview.md":      ["brand overview", "brand meaning", "closing manifesto"],
}

written = 0
skipped = 0

for rel_path, keywords in MAPPING.items():
    full_path = os.path.join(ROOT, rel_path)
    extracted = get_section(keywords)

    if not extracted:
        print(f"⚠️  No match: {rel_path}")
        skipped += 1
        continue

    # Only write if file is empty or near-empty
    existing_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
    if existing_size > 500:
        print(f"⏭️  Skipping (has content): {rel_path}")
        skipped += 1
        continue

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- Extracted from Brand Bible -->\n\n")
        f.write(extracted)

    print(f"✅ Written: {rel_path}")
    written += 1

print(f"\n🏁 Done — {written} files written, {skipped} skipped")
