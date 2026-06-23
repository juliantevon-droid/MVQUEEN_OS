mvqueen_engine/

│

├── \_\_init\_\_.py

│

├── config.py

├── price_logic.py

│

├── utils/

│ ├── \_\_init\_\_.py

│ ├── deterministic.py

│ ├── file_utils.py

│ └── text_cleaning.py

│

├── brand_brain/

│ ├── \_\_init\_\_.py

│ ├── brand_banks.py

│ ├── brand_language.py

│ ├── alt_text.py

│ ├── seo_keywords.py

│ └── persona_router.py

│

├── metafields/

│ ├── \_\_init\_\_.py

│ └── metafield_engine.py

│

├── shopify_api/

│ ├── \_\_init\_\_.py

│ ├── auth.py

│ ├── product_updater.py

│ └── session_manager.py

│

├── catalog_processor/

│ ├── \_\_init\_\_.py

│ ├── processor.py

│ ├── csv_loader.py

│ └── bundle_generator.py

│

└── control_panel/

├── \_\_init\_\_.py

└── control_panel.py

/data/data/ru.iiec.pydroid3/files/

"""

MVQUEEN ENGINE --- GLOBAL CONFIG

This file stores global settings used across all phases.

"""

BRAND_NAME = "MVQueen"

\# Shopify API placeholders (Phase 4 will use these)

SHOPIFY_STORE_DOMAIN = ""

SHOPIFY_API_VERSION = "2024-01"

SHOPIFY_ACCESS_TOKEN = ""

\# Engine settings

DEBUG = True

\# CSV export chunk size

CSV_CHUNK_SIZE = 15000

\# Columns we NEVER modify (Shopify safety)

SHOPIFY_PROTECTED_COLUMNS = \[

"Handle", "Product ID", "Variant ID",

"Option1 Name", "Option1 Value",

"Option2 Name", "Option2 Value",

"Option3 Name", "Option3 Value",

"Variant SKU", "Variant Grams",

"Variant Inventory Tracker", "Variant Inventory Qty",

"Variant Inventory Policy", "Variant Fulfillment Service",

"Variant Requires Shipping", "Variant Taxable",

"Variant Weight Unit"

\]

"""

MVQUEEN ENGINE --- PRICE LOGIC

Handles compare-at price psychology and tiered uplift.

"""

Def calculate_compare_price(price: float) -\> float:

"""

28% / 35% / 42% uplift based on price tiers.

"""

Try:

P = float(price)

Except:

Return 0.0

If p \< 20:

Return round(p \* 1.28, 2)

Elif p \< 60:

Return round(p \* 1.35, 2)

Else:

Return round(p \* 1.42, 2)

"""

Deterministic Engine --- MVQueen

Ensures consistent persona, vocabulary, and editorial selection.

"""

Import hashlib

Import random

Def seed_from_text(text: str, count: int = 16):

"""Generate deterministic seed list from any text."""

H = hashlib.sha256(text.encode()).hexdigest()

Seeds = \[\]

For I in range(count):

Chunk = h\[i\*4i+1)\*4\]

Seeds.append(int(chunk, 16))

Return seeds

Def deterministic_choice(pool, handle, index=0):

"""Pick a deterministic value from a pool."""

If not pool:

Return ""

Seeds = seed_from_text(handle)

Random.seed(seeds\[index % len(seeds)\])

Return random.choice(pool)

Def deterministic_multi(pool, handle, count=3):

"""Pick multiple deterministic values."""

If not pool:

Return \[\]

Seeds = seed_from_text(handle)

Random.seed(sum(seeds))

Count = min(count, len(pool))

Return random.sample(pool, count)

Def truncate(text: str, max_len: int):

"""Truncate text safely."""

If len(text) \<= max_len:

Return text

Return text\[:max_len-3\].rstrip() + "..."

"""

File Utilities --- MVQueen Engine

Handles CSV reading, writing, and safe file operations.

"""

Import csv

From pathlib import Path

Def read_csv(path: str):

"""Read CSV into list of dicts."""

P = Path(path)

If not p.exists():

Return \[\]

With open(p, newline="", encoding="utf-8") as f:

Return list(csv.DictReader(f))

Def write_csv(path: str, rows, fieldnames):

"""Write CSV safely."""

P = Path(path)

With open(p, "w", newline="", encoding="utf-8") as f:

Writer = csv.DictWriter(f, fieldnames=fieldnames)

Writer.writeheader()

Writer.writerows(rows)

"""

Text Cleaning --- MVQueen Engine

Handles HTML stripping, whitespace normalization, and brand enforcement.

"""

Import re

From mvqueen_engine.config import BRAND_NAME

Def strip_html(html: str) -\> str:

"""Remove HTML tags."""

If not isinstance(html, str):

Return ""

Text = re.sub("\<\[\^\<\]+?\>", "", html)

Return " ".join(text.split())

Def normalize_whitespace(text: str) -\> str:

"""Collapse multiple spaces/newlines."""

If not isinstance(text, str):

Return ""

Return " ".join(text.split())

Def enforce_brand(text: str) -\> str:

"""Normalize MVQueen brand name."""

If not isinstance(text, str):

Return text

Text = re.sub(r"\\b(MVQUEEN\|mvqueen\|Mvqueen)\\b", BRAND_NAME, text)

Return text.strip()

"""

MVQueen Brand Vocabulary Banks

This file contains ALL vocabulary pools used by the engine.

Populate with full lists in Step 4B.

"""

\# Luxury adjectives

LUXURY_ADJECTIVES = \[\]

\# Sensory verbs / phrases

SENSORY_VERBS = \[\]

\# Confidence / empowerment phrases

CONFIDENCE_PHRASES = \[\]

\# Moods

MOODS = \[\]

\# Finishes

FINISHES = \[\]

\# Textures

TEXTURES = \[\]

\# Routine steps

ROUTINE_STEPS = \[\]

\# Benefits

BENEFITS = \[\]

\# Business tiers

BUSINESS_TIERS = \[\]

\# Skin profiles

SKIN_PROFILES = \[\]

\# Occasions

OCCASIONS = \[\]

\# Fashion vocab

FASHION_SILHOUETTES = \[\]

FASHION_DETAILS = \[\]

FASHION_MATERIALS = \[\]

FASHION_VIBES = \[\]

\# Editorial frames

EDITORIAL_FRAMES = \[\]

\# SEO keyword pools

SEO_PRIMARY = \[\]

SEO_SECONDARY = \[\]

\# Personas

PERSONAS = \[

"MVQueen Core",

"MISS.QUEEN",

"Victoria Soft Power",

"Sephora Precision",

"Runway Modern",

"Clinical Chic",

"Soft Luxury",

"Glow Maestro",

"Elegant Authority",

"Street Luxe Femme",

\]

\# Persona configuration

PERSONA_CONFIG = {}

"""

Brand Language Engine --- MVQueen

Handles tone, phrasing, and brand-consistent language.

"""

From mvqueen_engine.utils.deterministic import deterministic_choice

From mvqueen_engine.brand_brain.brand_banks import (

LUXURY_ADJECTIVES, MOODS, OCCASIONS, BENEFITS

)

Def generate_brand_intro(title: str, handle: str) -\> str:

Adj = deterministic_choice(LUXURY_ADJECTIVES, handle, 0)

Mood = deterministic_choice(MOODS, handle, 1)

Occasion = deterministic_choice(OCCASIONS, handle, 2)

Benefit = deterministic_choice(BENEFITS, handle, 3)

Return (

F"\<p\>{adj.capitalize()} {title} designed for {occasion.lower()}
moments "

F"where {benefit.lower()} meets {mood.lower()} energy.\</p\>"

)

"""

Alt Text Generator --- MVQueen

Creates luxury, SEO-friendly alt text.

"""

From mvqueen_engine.utils.deterministic import deterministic_choice

From mvqueen_engine.brand_brain.brand_banks import (

TEXTURES, FINISHES, MOODS

)

Def generate_alt_text(title: str, handle: str) -\> str:

Texture = deterministic_choice(TEXTURES, handle, 0)

Finish = deterministic_choice(FINISHES, handle, 1)

Mood = deterministic_choice(MOODS, handle, 2)

Return f"{title} with {texture} texture, {finish} finish, and {mood}
mood --- MVQueen."

"""

SEO Keyword Engine --- MVQueen

Generates primary + secondary keyword stacks.

"""

From mvqueen_engine.utils.deterministic import deterministic_choice

From mvqueen_engine.brand_brain.brand_banks import (

SEO_PRIMARY, SEO_SECONDARY

)

Def generate_seo_keywords(handle: str):

Primary = deterministic_choice(SEO_PRIMARY, handle, 0)

Secondary = deterministic_choice(SEO_SECONDARY, handle, 1)

Return primary, secondary

"""

Persona Router --- MVQueen

Determines which persona controls the editorial voice.

"""

From mvqueen_engine.utils.deterministic import deterministic_choice

From mvqueen_engine.brand_brain.brand_banks import PERSONAS,
PERSONA_CONFIG

Def pick_persona(handle: str) -\> str:

Return deterministic_choice(PERSONAS, handle, 0)

Def get_persona_config(persona: str):

Return PERSONA_CONFIG.get(persona, {})

SKIN_PROFILES = \[

"All Skin", "Normal", "Dry", "Very Dry", "Oily", "Very Oily",
"Combination",

"Sensitive", "Reactive", "Acne-Prone", "Hormonal", "Mature", "Teen",

"Post-Treatment", "Redness-Prone", "Uneven Tone", "Textured", "Dull",

"Dehydrated", "Sun-Exposed", "Balanced", "Resilient", "Fragile",
"Irritated",

"Stressed", "Urban Skin", "Pollution-Exposed", "Barrier-Compromised",

"Elasticity Loss", "Fine Lines", "Deep Lines", "Dark Spot Concern",

"Hyperpigmentation", "Large Pores", "Congested", "T-Zone Oily", "Flaky",

"Rough", "Tight", "Over-Exfoliated"

\]

TEXTURES = \[

"Silky", "Velvety", "Lightweight", "Ultra-Light", "Creamy", "Rich
Cream",

"Whipped", "Airy", "Bouncy", "Gel", "Soft Gel", "Water Gel",
"Serum-Light",

"Fluid", "Lotion", "Milky", "Satin Smooth", "Glossy", "Sheer",
"Powdery",

"Mousse", "Cloud-Like", "Dense", "Featherlight", "Oil-Infused",

"Fast-Absorbing", "Quick-Dry", "Non-Sticky", "Weightless", "Luxurious",

"Soft Touch", "Cooling", "Refreshing", "Hydro-Burst", "Elastic",
"Plush",

"Flexible", "Buttery", "Slip-Finish", "Glide-On", "Melting", "Cushiony",

"Smooth Spread", "Grip-Prime", "Fine Mist", "Micro-Mist", "Dry Touch",

"Second-Skin", "Comfort Wear", "Stretch-Fit", "Seamless"

\]

FINISHES = \[

"Natural Glow", "Radiant", "Dewy", "Glass Skin", "Soft Matte", "Velvet
Matte",

"Satin", "Luminous", "Sheer Glow", "High Shine", "Glossy", "Blurred",

"Soft Blur", "Filtered Finish", "Airbrushed", "Barely-There", "Fresh
Finish",

"Healthy Glow", "Lit-From-Within", "Glow Boost", "Light Reflecting",

"Illuminated", "Skin-Like", "Flawless", "Polished", "Clean Finish",

"Silk Finish", "Smooth Finish", "Matte Control", "Shine-Free",
"Hydra-Glow",

"Reflective", "Velvet Skin", "Creamy Matte", "Modern Matte", "Soft
Focus",

"Bright Finish", "Natural Matte", "Long-Wear Matte", "Radiant Matte",

"Glow Lock", "Crystal Glow", "Bare Skin", "Second-Skin", "Soft
Radiance",

"Velvet Blur", "Pure Glow", "Demi-Matte", "Skin Veil", "Luxury Matte",

"Halo Glow", "Diffused", "Balanced Finish", "Air Glow", "Glam Glow",

"Runway Finish", "Subtle Shine", "Golden Glow", "Bronzed Glow", "Studio
Finish"

\]

ROUTINE_STEPS = \[

"Morning", "Night", "AM Routine", "PM Routine", "Daily Essential", "Prep
Step",

"Prime", "Treat", "Seal", "Refresh", "Boost", "Hydrate", "Tone",
"Cleanse",

"Exfoliate", "Mask", "Target", "Repair", "Protect", "SPF Layer", "Glow
Boost",

"Finish Step", "Setting Step", "On-The-Go", "Travel", "Gym Ready",

"Post-Workout", "Desk Refresh", "Event Prep", "Pre-Makeup",
"Post-Makeup",

"Recovery", "Reset", "Weekend Routine", "Self-Care", "Deep Care",

"Express Care", "Full Routine", "Minimal Routine", "Layer 1", "Layer 2",

"Layer 3", "Final Step", "Touch-Up", "Midday Refresh", "Evening Repair",

"Overnight Care", "Barrier Support", "Glow Layer", "Moisture Lock",

"Oil Balance", "Texture Smooth", "Radiance Boost", "Firming Step",

"Plump Step", "Calm Step", "Clarify", "Brighten", "Detox", "Replenish",

"Restore"

\]

MOODS = \[

"Soft Glam", "Clean Girl", "Luxury Glow", "Bold Beauty", "Minimal Chic",

"Romantic", "Confident", "Effortless", "Polished", "Fresh Face",
"Sultry",

"Runway", "Editorial", "Natural Beauty", "High Glam", "Subtle Glam",

"Power Look", "Soft Power", "Feminine", "Modern Muse", "Chic Minimal",

"Golden Hour", "Bare Glow", "Statement Look", "Date Night", "CEO
Energy",

"Girl Boss", "Cool Girl", "City Glow", "Vacation Mode", "Parisian",

"New York Glam", "LA Glow", "Beachy", "Bronzed", "Crystal Glow",

"Velvet Nights", "Dream Skin", "Glow Queen", "MVQueen Energy",

"Signature Glow", "Elevated Beauty", "Quiet Luxury", "High Shine",

"Glow Mood", "Glossy Energy", "Soft Radiance", "Refined", "Delicate",

"Bold Radiance", "Glow Era", "Velvet Era", "Skin Era", "Confidence
Boost",

"Flirty", "Graceful", "Glow Ritual", "Luxury Ritual", "Signature
Routine",

"Iconic Glow", "Daily Glam", "Glow Edit", "Radiant Mood", "Luxe Skin",

"Timeless", "Youthful", "Ageless Glow", "Classic Beauty", "Modern Glow",

"Elite Finish", "VIP Energy"

\]

OCCASIONS = \[

"Everyday Wear", "Date Night", "Event Ready", "Bridal Glow", "Vacation
Beauty",

"Work Ready", "Weekend Glow", "Photoshoot Ready", "Red Carpet",
"Birthday Glam",

"Anniversary", "Holiday Glam", "Summer Glow", "Winter Care", "Spring
Refresh",

"Fall Glow", "Travel Friendly", "On-The-Go", "Office Chic", "Dinner
Ready",

"Party Ready", "Festival", "Night Out", "Gym Bag", "Beach Day",
"Poolside",

"Airport Look", "Business Meeting", "Formal Event", "Casual Day",
"Brunch Ready",

"Quick Glam", "After Work", "Wedding Guest", "Baby Shower",
"Graduation",

"Prom", "Luxury Night", "VIP Event", "Self-Care Day", "Home Spa",
"Staycation",

"Content Shoot", "Influencer Edit", "Runway Ready", "TV Ready", "Camera
Friendly",

"Long Shift", "Quick Routine", "Touch-Up Kit", "Weekend Trip", "Road
Trip",

"Seasonal Glow", "Limited Drop", "Launch Day", "Holiday Gift",
"Giftable",

"Stocking Stuffer", "Signature Event", "Special Edition"

\]

BENEFITS = \[

"Hydrating", "Deep Hydration", "Oil Control", "Brightening", "Firming",

"Smoothing", "Plumping", "Balancing", "Calming", "Long-Lasting",

"Buildable", "Transfer-Resistant", "Sweat-Resistant", "Water-Resistant",

"Humidity Shield", "Pore Blurring", "Fine Line Smoothing", "Elasticity
Boost",

"Collagen Support", "Glow Enhancing", "Tone Correcting", "Texture
Refining",

"Barrier Repair", "Barrier Support", "Soothing", "Cooling",
"Refreshing",

"Lightweight Feel", "Non-Greasy", "Non-Sticky", "Quick Absorb", "Fast
Dry",

"Layer Friendly", "Makeup Friendly", "SPF Support", "UV Protection",

"Blue Light Shield", "Pollution Defense", "Detoxifying", "Clarifying",

"Purifying", "Exfoliating", "Gentle", "Sensitive Safe", "Derm Tested",

"Clean Formula", "Vegan Friendly", "Cruelty Free", "Paraben Free",

"Sulphate Free", "Silicone Free", "Fragrance Light", "High Pigment",

"Soft Pigment", "Gloss Boost", "Volume Boost", "Curl Boost", "Length
Boost",

"Strengthening", "Repairing", "Nourishing", "Moisture Lock", "Shine
Boost",

"Glow Lock", "Flexible Hold", "Strong Hold", "Soft Hold", "Flake-Free",

"Fade Resistant", "Smudge Resistant", "Feather Light", "Grip Boost",

"Smooth Glide", "Quick Style", "Heat Protect", "Damage Control",

"Split-End Care", "Scalp Friendly", "Hydro Boost"

\]

BUSINESS_TIERS = \[

"Core", "Hero", "Premium", "Elite", "Signature", "Limited", "Seasonal",

"Best Seller", "Top Rated", "Editor Pick", "Influencer Pick", "New
Arrival",

"Trending", "Featured", "Spotlight", "Collection Star", "High Demand",

"Fast Moving", "Boutique Select", "Curated Pick", "Launch Drop", "VIP
Edit",

"Luxury Tier", "Accessible Luxury", "Entry Luxe", "High Margin",

"Upsell Anchor", "Bundle Ready", "Gift Ready", "Routine Builder",

"Add-On Favorite", "Cross-Sell Hero", "AOV Booster", "High Visibility",

"Priority SKU", "Evergreen", "Restock Alert", "Low Stock", "Exclusive",

"Private Label", "MVQueen Exclusive", "Online Only", "Limited Batch",

"Rare Find", "Premium Blend", "Advanced Formula", "Pro Level", "Studio
Level",

"Runway Level", "Backstage Approved", "Retail Favorite", "Flagship",

"Anchor Product", "Core Essential", "Glow Essential", "Must Have",

"Signature SKU", "Daily Favorite", "Rising Star", "High Conversion",

"Strong Performer", "Stable Seller", "Seasonal Hero", "Limited Run",

"Collector", "Elevated Edition", "Refined Formula", "Enhanced", "Version
2",

"Reformulated", "Improved", "Next Gen", "Future Glow", "Advanced Glow",

"Icon Status", "Hall of Fame", "Classic", "Timeless Essential",

"Luxe Upgrade", "Power Product"

\]
