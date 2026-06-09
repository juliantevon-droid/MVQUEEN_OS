import os

ROOT = "/storage/emulated/0/MVQUEEN_OS"
DL = "/storage/emulated/0/Download"

# Each tuple: (source file, section title keyword, destination path)
SPLITS = [
    # Shopify_SOPs.md
    ("Shopify_SOPs.md", "Shipping SOP", "09_Shopify_Systems/Shipping_SOP.md"),
    ("Shopify_SOPs.md", "Refund & Return SOP", "09_Shopify_Systems/Refund_SOP.md"),
    ("Shopify_SOPs.md", "Customer Support SOP", "09_Shopify_Systems/Customer_Support_SOP.md"),
    ("Shopify_SOPs.md", "Upsell Systems", "09_Shopify_Systems/Upsell_Systems.md"),
    # Operations_Social.md
    ("Operations_Social.md", "Fulfillment Systems", "11_Operations/Fulfillment_Systems.md"),
    ("Operations_Social.md", "Team Structure", "11_Operations/Team_Structure.md"),
    ("Operations_Social.md", "Posting Schedule", "08_Social_Media/Posting_Schedule.md"),
    ("Operations_Social.md", "Hashtag Systems", "08_Social_Media/Hashtag_Systems.md"),
    ("Operations_Social.md", "Engagement Strategy", "08_Social_Media/Engagement_Strategy.md"),
    # Marketing_Content.md
    ("Marketing_Content.md", "Viral Hooks", "07_Marketing/Viral_Hooks.md"),
    ("Marketing_Content.md", "Giveaway Systems", "07_Marketing/Giveaway_Systems.md"),
    ("Marketing_Content.md", "Seasonal Campaigns", "07_Marketing/Seasonal_Campaigns.md"),
    ("Marketing_Content.md", "Affiliate Program", "07_Marketing/Affiliate_Program.md"),
    ("Marketing_Content.md", "Viral Content Systems", "08_Social_Media/Viral_Content_Systems.md"),
    ("Marketing_Content.md", "Mission & Vision", "01_Brand_Strategy/Mission_And_Vision.md"),
    # AI_Prompts.md
    ("AI_Prompts.md", "Social Media Prompts", "10_AI_Systems/Social_Media_Prompts.md"),
    ("AI_Prompts.md", "Product Description Prompts", "10_AI_Systems/Product_Description_Prompts.md"),
    ("AI_Prompts.md", "Image Generation Prompts", "10_AI_Systems/Image_Generation_Prompts.md"),
    # SEO_Research_Doctrine.md
    ("SEO_Research_Doctrine.md", "Instagram SEO", "05_SEO_And_Content/Instagram_SEO.md"),
    ("SEO_Research_Doctrine.md", "Pinterest SEO", "05_SEO_And_Content/Pinterest_SEO.md"),
    ("SEO_Research_Doctrine.md", "TikTok SEO", "05_SEO_And_Content/TikTok_SEO.md"),
    ("SEO_Research_Doctrine.md", "EEAT Optimization", "05_SEO_And_Content/EEAT_Optimization.md"),
    ("SEO_Research_Doctrine.md", "Viral Topics Research", "05_SEO_And_Content/Viral_Topics.md"),
    ("SEO_Research_Doctrine.md", "Boutique Inspiration", "13_Research_And_Inspiration/Boutique_Inspiration.md"),
    ("SEO_Research_Doctrine.md", "Swipe File", "13_Research_And_Inspiration/Swipe_Files.md"),
    ("SEO_Research_Doctrine.md", "Executive Overview", "99_Command_Center/executive_overview.md"),
    ("SEO_Research_Doctrine.md", "Brain Dump", "99_Command_Center/Brain_Dump.md"),
    ("SEO_Research_Doctrine.md", "Luxury Language Guide", "06_Tone_And_Voice/Luxury_Language.md"),
    ("SEO_Research_Doctrine.md", "Emotional Language Guide", "06_Tone_And_Voice/Emotional_Language.md"),
    ("SEO_Research_Doctrine.md", "Emotional Intelligence Framework", "00_Doctrine/emotional_intelligence_framework.md"),
    ("SEO_Research_Doctrine.md", "Luxury Philosophy", "00_Doctrine/luxury_philosophy.md"),
    ("SEO_Research_Doctrine.md", "Brand Philosophy", "01_Brand_Strategy/brand_philosophy.md"),
]

file_cache = {}

def load_file(fname):
    if fname not in file_cache:
        path = os.path.join(DL, fname)
        with open(path, "r", encoding="utf-8") as f:
            file_cache[fname] = f.read()
    return file_cache[fname]

def extract_section(content, title_keyword):
    lines = content.split("\n")
    start = None
    for i, line in enumerate(lines):
        if title_keyword.lower() in line.lower() and line.startswith("#"):
            start = i
            break
    if start is None:
        return None
    # Find next section at same or higher level
    header_level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            level = len(lines[i]) - len(lines[i].lstrip("#"))
            if level <= header_level:
                end = i
                break
    return "\n".join(lines[start:end]).strip()

written = 0
for src_file, keyword, dest_rel in SPLITS:
    try:
        content = load_file(src_file)
        section = extract_section(content, keyword)
        if not section:
            print(f"⚠️  Not found: {keyword} in {src_file}")
            continue
        dest = os.path.join(ROOT, dest_rel)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(section)
        print(f"✅ {dest_rel}")
        written += 1
    except Exception as e:
        print(f"❌ Error: {dest_rel} — {e}")

print(f"\n🏁 {written} files written")
