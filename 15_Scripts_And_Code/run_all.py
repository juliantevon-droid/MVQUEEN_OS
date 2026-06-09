import os

ROOT = "/storage/emulated/0/MVQUEEN_OS"
DL = "/storage/emulated/0/Download"

def load(fname):
    with open(os.path.join(DL, fname), "r", encoding="utf-8") as f:
        return f.read()

def extract(content, keyword):
    lines = content.split("\n")
    start = None
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower() and line.startswith("#"):
            start = i
            break
    if start is None:
        return None
    hlevel = len(lines[start]) - len(lines[start].lstrip("#"))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            lvl = len(lines[i]) - len(lines[i].lstrip("#"))
            if lvl <= hlevel:
                end = i
                break
    return "\n".join(lines[start:end]).strip()

def write(rel, content):
    dest = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)

SPLITS = [
    ("rebuild_A.md","Viral Brands Research","13_Research_And_Inspiration/Viral_Brands.md"),
    ("rebuild_A.md","Social Voice Guide","06_Tone_And_Voice/Social_Voice.md"),
    ("rebuild_A.md","Product Description Voice","06_Tone_And_Voice/Product_Description_Voice.md"),
    ("rebuild_A.md","Carousel Ideas","08_Social_Media/Carousel_Ideas.md"),
    ("rebuild_A.md","Cross-Sell Systems","04_Products/Cross-Sell Systems.md"),
    ("rebuild_A.md","Fashion Products","04_Products/Fashion_Products.md"),
    ("rebuild_A.md","Example Copy Library","06_Tone_And_Voice/Example_Copy.md"),
    ("rebuild_B.md","Content Calendar","05_SEO_And_Content/Content_Calendar.md"),
    ("rebuild_B.md","Feminine Identity Framework","00_Doctrine/feminine_identity_framework.md"),
    ("rebuild_B.md","YouTube Strategy","08_Social_Media/YouTube_Strategy.md"),
    ("rebuild_B.md","YouTube SEO","05_SEO_And_Content/YouTube SEO.md"),
    ("rebuild_B.md","Blog Strategy","05_SEO_And_Content/Blog_Strategy.md"),
    ("rebuild_B.md","Email Marketing","07_Marketing/Email_Marketing.md"),
    ("rebuild_B.md","Internal Linking Strategy","05_SEO_And_Content/Internal_Linking.md"),
    ("rebuild_B.md","Hair Products","04_Products/Hair_Products.md"),
    ("rebuild_C.md","FAQ Library","05_SEO_And_Content/FAQ_Library.md"),
    ("rebuild_C.md","Caption Templates","08_Social_Media/Caption_Templates.md"),
    ("rebuild_C.md","Blog Voice","06_Tone_And_Voice/blog_voice.md"),
    ("rebuild_C.md","Messaging Pillars","06_Tone_And_Voice/Messaging_Pillars.md"),
    ("rebuild_C.md","Blog Templates","05_SEO_And_Content/Blog_Templates.md"),
    ("rebuild_C.md","Article Structures","05_SEO_And_Content/Article_Structures.md"),
    ("rebuild_C.md","Metadata Templates","05_SEO_And_Content/Metadata_Templates.md"),
    ("rebuild_C.md","Fashion Inspiration","13_Research_And_Inspiration/Fashion_Inspiration.md"),
    ("rebuild_C.md","Current Campaigns","99_Command_Center/current_campaigns.md"),
    ("rebuild_C.md","Current Launches","99_Command_Center/current_launches.md"),
    ("rebuild_C.md","Crisis Management","11_Operations/Crisis_Management.md"),
    ("Shopify_SOPs.md","Shipping SOP","09_Shopify_Systems/Shipping_SOP.md"),
    ("Shopify_SOPs.md","Refund & Return SOP","09_Shopify_Systems/Refund_SOP.md"),
    ("Shopify_SOPs.md","Customer Support SOP","09_Shopify_Systems/Customer_Support_SOP.md"),
    ("Shopify_SOPs.md","Upsell Systems","09_Shopify_Systems/Upsell_Systems.md"),
    ("Operations_Social.md","Fulfillment Systems","11_Operations/Fulfillment_Systems.md"),
    ("Operations_Social.md","Team Structure","11_Operations/Team_Structure.md"),
    ("Operations_Social.md","Posting Schedule","08_Social_Media/Posting_Schedule.md"),
    ("Operations_Social.md","Hashtag Systems","08_Social_Media/Hashtag_Systems.md"),
    ("Operations_Social.md","Engagement Strategy","08_Social_Media/Engagement_Strategy.md"),
    ("Marketing_Content.md","Viral Hooks","07_Marketing/Viral_Hooks.md"),
    ("Marketing_Content.md","Giveaway Systems","07_Marketing/Giveaway_Systems.md"),
    ("Marketing_Content.md","Seasonal Campaigns","07_Marketing/Seasonal_Campaigns.md"),
    ("Marketing_Content.md","Affiliate Program","07_Marketing/Affiliate_Program.md"),
    ("Marketing_Content.md","Viral Content Systems","08_Social_Media/Viral_Content_Systems.md"),
    ("Marketing_Content.md","Mission & Vision","01_Brand_Strategy/Mission_And_Vision.md"),
    ("AI_Prompts.md","Social Media Prompts","10_AI_Systems/Social_Media_Prompts.md"),
    ("AI_Prompts.md","Product Description Prompts","10_AI_Systems/Product_Description_Prompts.md"),
    ("AI_Prompts.md","Image Generation Prompts","10_AI_Systems/Image_Generation_Prompts.md"),
    ("SEO_Research_Doctrine.md","Instagram SEO","05_SEO_And_Content/Instagram_SEO.md"),
    ("SEO_Research_Doctrine.md","Pinterest SEO","05_SEO_And_Content/Pinterest_SEO.md"),
    ("SEO_Research_Doctrine.md","TikTok SEO","05_SEO_And_Content/TikTok_SEO.md"),
    ("SEO_Research_Doctrine.md","EEAT Optimization","05_SEO_And_Content/EEAT_Optimization.md"),
    ("SEO_Research_Doctrine.md","Viral Topics Research","05_SEO_And_Content/Viral_Topics.md"),
    ("SEO_Research_Doctrine.md","Boutique Inspiration","13_Research_And_Inspiration/Boutique_Inspiration.md"),
    ("SEO_Research_Doctrine.md","Swipe File","13_Research_And_Inspiration/Swipe_Files.md"),
    ("SEO_Research_Doctrine.md","Executive Overview","99_Command_Center/executive_overview.md"),
    ("SEO_Research_Doctrine.md","Brain Dump","99_Command_Center/Brain_Dump.md"),
    ("SEO_Research_Doctrine.md","Luxury Language Guide","06_Tone_And_Voice/Luxury_Language.md"),
    ("SEO_Research_Doctrine.md","Emotional Language Guide","06_Tone_And_Voice/Emotional_Language.md"),
    ("SEO_Research_Doctrine.md","Emotional Intelligence Framework","00_Doctrine/emotional_intelligence_framework.md"),
    ("SEO_Research_Doctrine.md","Luxury Philosophy","00_Doctrine/luxury_philosophy.md"),
    ("SEO_Research_Doctrine.md","Brand Philosophy","01_Brand_Strategy/brand_philosophy.md"),
]

cache = {}
written = 0
failed = 0

for fname, keyword, dest_rel in SPLITS:
    try:
        if fname not in cache:
            cache[fname] = load(fname)
        section = extract(cache[fname], keyword)
        if not section:
            print(f"⚠️  Not found: '{keyword}' in {fname}")
            failed += 1
            continue
        write(dest_rel, section)
        print(f"✅ {dest_rel}")
        written += 1
    except Exception as e:
        print(f"❌ {dest_rel} — {e}")
        failed += 1

print(f"\n🏁 {written} written | {failed} failed")
