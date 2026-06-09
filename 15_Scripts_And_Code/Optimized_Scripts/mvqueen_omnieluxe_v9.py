
# ============================================================
# MVQUEEN OMNILUXE SUPREME v9.7 - CORE OPTIMIZER (Category from Title)
# ============================================================
import pandas as pd
import os
from pathlib import Path
import random, hashlib
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
BRAND_NAME = "MVQueen"
INPUT_FILE = Path.cwd() / "shopify_input.csv"  # upload in Colab
EXPORT_DIR = Path.cwd() / "MVQ_Exports"
EXPORT_DIR.mkdir(exist_ok=True)
MAX_PRODUCTS_PER_FILE = 850
DATE_STAMP = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# BRAND LANGUAGE POOLS
# ============================================================
BRAND_VOICE = [
"luxury-modern-elegant", "refined-luxury", "elevated-minimalism",
"confident-femininity", "modern-prestige", "quiet-opulence", "statement-elegance",
"timeless-refinement"
]

OPENING_SENTENCES = {
"beauty": [
"A luxurious formula to enhance natural radiance.",
"Infused with premium botanicals for healthy, glowing skin.",
"Elevate your daily ritual with indulgent skincare.",
"Designed to soothe, nourish, and revitalize.",
"Premium care for self-care enthusiasts."
],
"skincare": [
"Hydrates deeply and revitalizes the skin.",
"Protects and nourishes sensitive skin naturally.",
"A daily essential for a radiant complexion.",
"Crafted with active ingredients for lasting results.",
"Clean, effective, and luxurious skincare."
],
"fashion": [
"Designed to accentuate confidence and elegance.",
"A statement piece crafted for effortless style.",
"Modern luxury meets timeless design.",
"Elevate your wardrobe with refined essentials.",
"Sartorial excellence for the style-conscious."
],
"default": [
"Crafted for those who expect more from everyday luxury.",
"A refined essential designed to elevate your daily routine.",
"Where modern design meets uncompromising quality.",
"An elevated staple created for confident, style-conscious individuals.",
"Designed to empower the modern connoisseur in all aspects of life."
]
}

BENEFIT_PHRASES = {
"beauty": [
"hydrates deeply and revitalizes skin",
"infused with active botanicals for radiant results",
"soothes and protects sensitive skin",
"luxurious textures for daily indulgence",
"enhances natural beauty with premium ingredients"
],
"skincare": [
"delivers lasting hydration",
"restores balance and softness",
"supports radiant, healthy-looking skin",
"crafted for optimal absorption and efficacy",
"gentle yet powerful formulation"
],
"fashion": [
"crafted to inspire confidence and elevate style",
"designed for effortless elegance",
"luxurious materials for comfort and appeal",
"statement-making design with modern flair",
"refined details for elevated aesthetics"
],
"default": [
"elevated performance with refined aesthetics",
"thoughtful design with lasting quality",
"premium craftsmanship with modern appeal",
"intentional details that elevate everyday use",
"refined materials chosen for comfort and durability"
]
}

TARGET_AUDIENCE = [
"modern luxury consumers",
"style-forward individuals",
"detail-oriented buyers",
"elevated lifestyle shoppers",
"quality-driven customers",
"skincare enthusiasts",
"beauty-conscious individuals",
"self-care seekers",
"fashion-savvy shoppers"
]

TEXTURE_POOL = ["smooth", "soft-touch", "refined", "lightweight", "structured", "velvety", "creamy", "silky finish"]
FINISH_POOL = ["polished", "satin", "refined matte", "softly luminous", "clean-finished", "luminous", "matte elegance"]
MOOD_POOL = ["confident", "empowered", "effortless", "elevated", "composed", "refined", "luxurious"]

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def select_deterministic(pool, handle, idx):
    seed = f"{handle}-{idx}"
    random.seed(int(hashlib.md5(seed.encode()).hexdigest(), 16) % (10**8))
    return random.choice(pool)

def select_category_text(pool_dict, category, handle, idx):
    return select_deterministic(pool_dict.get(category, pool_dict["default"]), handle, idx)

def ensure_column(df, col_name):
    if col_name not in df.columns:
        df[col_name] = ""

# ============================================================
# CATEGORY INFERENCE FROM TITLE
# ============================================================
def get_category_from_title(title):
    title_lower = str(title).lower()
    if any(k in title_lower for k in ["serum","moisturizer","lotion","mask","exfoliant"]):
        return "skincare"
    elif any(k in title_lower for k in ["lipstick","mascara","eyeshadow","fragrance","perfume"]):
        return "beauty"
    elif any(k in title_lower for k in ["dress","top","jacket","pants","skirt","coat"]):
        return "fashion"
    else:
        return "default"

# ============================================================
# LOAD INPUT
# ============================================================
df = pd.read_csv(INPUT_FILE)

# Ensure necessary columns exist
for col in ["Handle","Title","Body (HTML)","Tags","Vendor","Variant Price","Variant Compare At Price",
             "Image Alt Text","SEO Title","SEO Description"]:
    ensure_column(df, col)

# Metafield columns
metafields = [
    "metafield.custom.voice","metafield.custom.intent","metafield.custom.collection",
    "metafield.custom.prestige_score","metafield.custom.product_quality_score",
    "metafield.custom.shopify_bundle_safe","metafield.custom.alt_text",
    "metafield.custom.target_audience","metafield.custom.key_benefits",
    "metafield.custom.product_type_detailed","metafield.custom.texture",
    "metafield.custom.finish","metafield.custom.mood",
    "metafield.custom.short_description","metafield.custom.long_description",
    "metafield.custom.who_its_for","metafield.custom.results"
]
for col in metafields:
    ensure_column(df, col)

# ============================================================
# APPLY CATEGORY-SPECIFIC BRAND LANGUAGE
# ============================================================
for idx, row in df.iterrows():
    handle = row["Handle"]
    category = get_category_from_title(row["Title"])

    # Body
    df.at[idx, "Body (HTML)"] = f"<p>{select_category_text(OPENING_SENTENCES, category, handle, idx)}</p>"

    # Metafields
    df.at[idx, "metafield.custom.voice"] = select_deterministic(BRAND_VOICE, handle, idx)
    df.at[idx, "metafield.custom.key_benefits"] = select_category_text(BENEFIT_PHRASES, category, handle, idx)
    df.at[idx, "metafield.custom.target_audience"] = select_deterministic(TARGET_AUDIENCE, handle, idx)
    df.at[idx, "metafield.custom.texture"] = select_deterministic(TEXTURE_POOL, handle, idx)
    df.at[idx, "metafield.custom.finish"] = select_deterministic(FINISH_POOL, handle, idx)
    df.at[idx, "metafield.custom.mood"] = select_deterministic(MOOD_POOL, handle, idx)

    # Short & long descriptions
    df.at[idx, "metafield.custom.short_description"] = df.at[idx, "Body (HTML)"][:155]
    df.at[idx, "metafield.custom.long_description"] = df.at[idx, "Body (HTML)"]

# ============================================================
# EXPORT SPLIT FILES
# ============================================================
num_parts = (len(df) // MAX_PRODUCTS_PER_FILE) + 1
for i in range(num_parts):
    part_df = df.iloc[i*MAX_PRODUCTS_PER_FILE:(i+1)*MAX_PRODUCTS_PER_FILE]
    part_path = EXPORT_DIR / f"{BRAND_NAME}Optimized_Part{i+1}_{DATE_STAMP}.csv"
    part_df.to_csv(part_path, index=False)

print(f"✅ Phase 1 complete: {num_parts} files exported to {EXPORT_DIR}")
