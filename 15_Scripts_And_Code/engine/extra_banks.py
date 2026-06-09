# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — EXTRA BANKS (BLOCK T)
# ---------------------------------------------------------
PERSONA_CONFIG = {
    "MVQueen Core": {
        "tone": "luxury-confident-soft-feminine",
        "emotional_axes": ["radiance", "self-belief", "soft power"],
        "seo_bias": ["luxury skincare", "modern beauty", "elevated essentials"],
        "cta_style": "soft imperative",
    },

    "MISS.QUEEN": {
        "tone": "playful-glam-feminine",
        "emotional_axes": ["fun", "glow", "self-expression"],
        "seo_bias": ["soft glam", "night-out looks"],
        "cta_style": "playful invitation",
    },

    "Victoria Soft Power": {
        "tone": "sensual-soft-power",
        "emotional_axes": ["allure", "confidence", "intimacy"],
        "seo_bias": ["lingerie-inspired beauty", "soft power dressing"],
        "cta_style": "whispered persuasion",
    },

    "Sephora Precision": {
        "tone": "clinical-precise-modern",
        "emotional_axes": ["results", "clarity", "control"],
        "seo_bias": ["clinical skincare", "active ingredients"],
        "cta_style": "clear directive",
    },

    "Runway Modern": {
        "tone": "editorial-bold-runway",
        "emotional_axes": ["impact", "presence", "statement"],
        "seo_bias": ["runway looks", "editorial fashion"],
        "cta_style": "commanding",
    },

    "Clinical Chic": {
        "tone": "minimal-clinical-luxe",
        "emotional_axes": ["purity", "refinement", "assurance"],
        "seo_bias": ["dermatologist-inspired", "clean formulas"],
        "cta_style": "assured guidance",
    },

    "Soft Luxury": {
        "tone": "whisper-soft-luxury",
        "emotional_axes": ["comfort", "ease", "quiet confidence"],
        "seo_bias": ["everyday luxury", "soft textures"],
        "cta_style": "gentle suggestion",
    },

    "Glow Maestro": {
        "tone": "radiant-glow-obsessed",
        "emotional_axes": ["luminosity", "energy", "vitality"],
        "seo_bias": ["glowing skin", "radiant finish"],
        "cta_style": "hype but refined",
    },

    "Elegant Authority": {
        "tone": "refined-commanding-luxe",
        "emotional_axes": ["leadership", "presence", "composure"],
        "seo_bias": ["power dressing", "boardroom beauty"],
        "cta_style": "decisive invitation",
    },

    "Street Luxe Femme": {
        "tone": "street-modern-luxe",
        "emotional_axes": ["edge", "self-definition", "movement"],
        "seo_bias": ["street style", "city-ready looks"],
        "cta_style": "cool directive",
    },
}

PERSONA_BANKS = [
    "runway", "minimalist", "romantic", "bold", "classic",
    "editorial", "street luxe", "quiet luxury", "soft glam",  
    "Soft Luxury", "Runway Modern", "Clinical Chic", "Street Luxe Femme", "MISS.QUEEN", 
    "Glow Maestro", "Elegant Authority", "Content Creator Core", 
    "Old Money Modern", "MVQueen Core",
]

OCCASIONS = [
    # --- Core Occasions ---
    "Everyday", "Workday", "Weekend", "Evening", "Night Out",
    "Brunch", "Date Night", "Event", "Party", "Holiday",

    # --- Social Occasions ---
    "Girls Night", "Dinner Date", "Cocktail Hour", "Happy Hour",
    "Birthday Party", "Celebration", "Anniversary", "Engagement Party",
    "Bachelorette", "Wedding Guest", "Reception", "After Party",

    # --- Professional Occasions ---
    "Office", "Meeting", "Presentation", "Interview", "Conference",
    "Boardroom", "Client Dinner", "Networking Event", "Work Trip",

    # --- Lifestyle Occasions ---
    "Travel", "Vacation", "Resort", "Beach Day", "Pool Day",
    "Airport", "Jet Lag Day", "Gym", "Workout", "Errands",
    "City Day", "Shopping Day", "Coffee Run", "Day Trip",

    # --- Seasonal Occasions ---
    "Spring Event", "Summer Event", "Fall Event", "Winter Event",
    "Holiday Party", "New Year's Eve", "Festive Gathering",
    "Resort Season", "Summer Nights", "Winter Gala",

    # --- Beauty Occasions ---
    "Pre-Makeup", "Post-Makeup", "Event Prep", "Camera-Ready",
    "Photoshoot", "Runway", "Editorial Shoot", "Soft Glam Moment",
    "Full Glam Moment", "Fresh-Faced Day", "Glow Day",

    # --- Fashion Occasions ---
    "Street Style Moment", "Runway Moment", "Quiet Luxury Moment",
    "Old Money Moment", "Minimal Chic Moment", "Statement Moment",
    "Soft Luxe Moment", "Evening Glam Moment",

    # --- Persona-Based Occasions ---
    "Soft Luxury Occasion", "Runway Modern Occasion",
    "Clinical Chic Occasion", "Street Luxe Occasion",
    "MISS.QUEEN Occasion", "Glow Maestro Occasion",
    "Elegant Authority Occasion", "Content Creator Occasion",
    "Old Money Modern Occasion", "MVQueen Core Occasion",

    # --- Event-Level Occasions ---
    "Gala", "Black Tie", "Cocktail Event", "Formal Event",
    "Semi-Formal Event", "Red Carpet", "Premiere", "Opening Night",
    "Fashion Week", "Launch Party", "VIP Event",

    # --- Marketing-Friendly Occasions ---
    "Desk-to-Dinner", "Day-to-Night", "Weekend-to-Work",
    "Effortless Everyday", "Elevated Everyday", "Signature Occasion",
    "Statement Occasion", "Soft Power Occasion", "Glow Power Occasion",

    # --- High-End Luxury Occasions ---
    "Luxury Dinner", "Private Event", "Members Club Night",
    "Estate Party", "Yacht Event", "Penthouse Event",
    "Stealth Wealth Occasion", "Opulent Occasion"
]
OCCASION_BANK = [
    "evening", "daytime", "work", "weekend", "event",
    "vacation", "date night", "party", "formal"
]


MOODS = [
    "Soft Glam", "Clean Girl", "Luxury Glow", "Bold Beauty", "Minimal Chic",
    "Romantic", "Confident", "Effortless", "Polished", "Fresh Face", "Sultry",
    "Runway", "Editorial", "Natural Beauty", "High Glam", "Subtle Glam",
    "Power Look", "Soft Power", "Feminine", "Modern Muse", "Chic Minimal",
    "Golden Hour", "Bare Glow", "Statement Look", "Date Night", "CEO Energy",
    "Girl Boss", "Cool Girl", "City Glow", "Vacation Mode", "Parisian",
    "New York Glam", "LA Glow", "Beachy", "Bronzed", "Crystal Glow",
    "Velvet Nights", "Dream Skin", "Glow Queen", "MVQueen Energy",
    "Signature Glow", "Elevated Beauty", "Quiet Luxury", "High Shine",
    "Glow Mood", "Glossy Energy", "Soft Radiance", "Refined", "Delicate",
    "Bold Radiance", "Glow Era", "Velvet Era", "Skin Era", "Confidence Boost",
    "Flirty", "Graceful", "Glow Ritual", "Luxury Ritual", "Signature Routine",
    "Iconic Glow", "Daily Glam", "Glow Edit", "Radiant Mood", "Luxe Skin",
    "Timeless", "Youthful", "Ageless Glow", "Classic Beauty", "Modern Glow",
    "Elite Finish", "VIP Energy"
    # --- Original Core ---
    "Soft", "Romantic", "Bold", "Minimal", "Classic", "Modern",
    "Fresh", "Clean", "Warm", "Cool", "Neutral", "Elegant",

    # --- New: Beauty Moods ---
    "Glowy", "Radiant", "Dewy", "Matte", "Sculpted", "Airbrushed",
    "Natural Glam", "Soft Glam", "Full Glam", "Fresh-Faced",
    "Lit-From-Within", "Glass-Skin", "Cloud-Skin", "Skin-Like",
    "Hydrated", "Plump", "Supple", "Brightened", "Clarified",

    # --- New: Fashion Moods ---
    "Runway", "Editorial", "Street Luxe", "Quiet Luxury",
    "Old Money", "New Money", "Minimal Chic", "Maximalist",
    "Soft Luxe", "Effortless", "Polished", "Tailored",
    "Relaxed", "Structured", "Flowy", "Sleek", "Sharp",
    "City Cool", "Resort", "Vacation", "Evening Glam",

    # --- New: Emotional Moods ---
    "Confident", "Empowered", "Calm", "Serene", "Playful",
    "Sensual", "Mysterious", "Bold Energy", "Soft Energy",
    "Grounded", "Uplifted", "Focused", "Balanced",
    "Self-Assured", "Self-Expressive", "Refined", "Assured",

    # --- New: Seasonal Moods ---
    "Spring Fresh", "Summer Bright", "Fall Cozy", "Winter Luxe",
    "Holiday Glam", "Resort Escape", "Sun-Kissed", "Frosted",

    # --- New: Persona-Based Moods ---
    "Soft Luxury Mood", "Runway Modern Mood", "Clinical Chic Mood",
    "Street Luxe Mood", "MISS.QUEEN Mood", "Glow Maestro Mood",
    "Elegant Authority Mood", "Content Creator Mood",
    "Old Money Modern Mood", "MVQueen Core Mood",

    # --- New: Texture-Driven Moods ---
    "Velvety Mood", "Silky Mood", "Featherlight Mood",
    "Cushiony Mood", "Satin Mood", "Glossy Mood",
    "Matte Mood", "Sheer Mood", "Diffused Mood",

    # --- New: Finish-Driven Moods ---
    "Radiance Mood", "Soft Glow Mood", "Ultra-Matte Mood",
    "Satin Glow Mood", "Diamond Glow Mood", "Pearl Glow Mood",

    # --- New: Lifestyle Moods ---
    "Workday Mood", "Weekend Mood", "Brunch Mood",
    "Date Night Mood", "Event Mood", "Travel Mood",
    "Jet Lag Mood", "Gym Mood", "Desk-to-Dinner Mood",
    "Off-Duty Mood", "On-The-Go Mood", "Luxury Ritual Mood",

    # --- New: Marketing-Friendly Moods ---
    "Everyday Elevated", "Effortlessly Polished", "Softly Defined",
    "Boldly Defined", "Refined Radiance", "Quiet Confidence",
    "Statement Energy", "Soft Power", "Glow Power",
    "Modern Elegance", "Timeless Ease", "Signature Mood",

    # --- New: High-End Luxury Moods ---
    "Cashmere Mood", "Velvet Mood", "Silk Mood",
    "Opulent Mood", "Luxe Minimalism", "High-Gloss Luxury",
    "Understated Luxury", "Stealth Wealth Mood"
]

BENEFIT_BANK = [
    "hydration", "radiance", "softness", "comfort",
    "breathability", "durability", "lightweight feel"
]

BENEFITS = [
    # Hydration & Moisture
    "hydrating",
    "deeply hydrating",
    "moisture-locking",
    "moisture-restoring",
    "moisture-replenishing",
    "long-lasting hydration",
    "barrier-strengthening",
    "barrier-repairing",
    "dewy-finish hydration",

    # Brightening & Radiance
    "brightening",
    "radiance-boosting",
    "glow-enhancing",
    "tone-evening",
    "dark-spot-fading",
    "hyperpigmentation-correcting",
    "luminosity-enhancing",
    "dullness-reducing",
    "lit-from-within glow",
    "soft-focus radiance",

    # Texture & Pores
    "smoothing",
    "texture-refining",
    "pore-minimizing",
    "resurfacing",
    "softening",
    "clarifying",
    "exfoliating",
    "micro-polishing",
    "skin-blurring",
    "filter-like effect",

    # Anti-Aging & Firmness
    "firming",
    "lifting",
    "plumping",
    "wrinkle-reducing",
    "fine-line-smoothing",
    "elasticity-boosting",
    "collagen-supporting",
    "rejuvenating",
    "youthful-looking",

    # Calming & Sensitivity
    "soothing",
    "calming",
    "redness-reducing",
    "irritation-relieving",
    "inflammation-reducing",
    "gentle-balancing",
    "sensitive-skin-friendly",

    # Oil & Acne Control
    "oil-controlling",
    "shine-reducing",
    "sebum-balancing",
    "acne-clearing",
    "breakout-preventing",
    "pore-clearing",
    "blemish-reducing",

    # Protection & Defense
    "antioxidant-protecting",
    "pollution-shielding",
    "environmental-defense",

    # Makeup: Coverage & Finish
    "full-coverage",
    "medium-coverage",
    "sheer-coverage",
    "buildable-coverage",
    "matte-finish",
    "soft-matte",
    "natural-finish",
    "radiant-finish",
    "dewy-finish",
    "satin-finish",

    # Makeup: Wear & Performance
    "long-wearing",
    "all-day-wear",
    "transfer-resistant",
    "sweat-resistant",
    "smudge-proof",
    "crease-resistant",
    "fade-resistant",

    # Makeup: Complexion Enhancing
    "tone-evening",
    "redness-neutralizing",
    "brightening",
    "glow-enhancing",
    "sculpting",
    "highlighting",
    "skin-perfecting",

    # Makeup: Comfort & Skin Benefits
    "lightweight-feel",
    "breathable-wear",
    "non-comedogenic",
    "skin-soothing",

    # Makeup: Pigment & Blend
    "high-pigment",
    "soft-pigment",
    "blendable",
    "seamless-blend",
    "buildable-intensity",
    "color-true",
]

ROUTINE_BANK = [
    "morning routine", "evening routine", "travel routine",
    "event prep", "daily essentials"
]

ROUTINE_STEPS = [
    "Morning", "Night", "AM Routine", "PM Routine", "Daily Essential",
    "Prep Step", "Prime", "Treat", "Seal", "Refresh", "Boost", "Hydrate",
    "Tone", "Cleanse", "Exfoliate", "Mask", "Target", "Repair", "Protect",
    "SPF Layer", "Glow Boost", "Finish Step", "Setting Step", "On-The-Go",
    "Travel", "Gym Ready", "Post-Workout", "Desk Refresh", "Event Prep",
    "Pre-Makeup", "Post-Makeup", "Recovery", "Reset", "Weekend Routine",
    "Self-Care", "Deep Care", "Express Care", "Full Routine",
    "Minimal Routine", "Layer 1", "Layer 2", "Layer 3", "Final Step",
    "Touch-Up", "Midday Refresh", "Evening Repair", "Overnight Care",
    "Barrier Support", "Glow Layer", "Moisture Lock", "Oil Balance",
    "Texture Smooth", "Radiance Boost", "Firming Step", "Plump Step",
    "Calm Step", "Clarify", "Brighten", "Detox", "Replenish", "Restore",

    # --- New: Beauty Rituals ---
    "Double Cleanse", "Essence Layer", "Serum Cocktail", "Hydration Sandwich",
    "Barrier Rebuild", "Skin Cycling", "Retinol Night", "Acid Night",
    "Hydration Night", "Glow Night", "Treatment Night", "Recovery Night",
    "Mask Monday", "Treatment Tuesday", "Wellness Wednesday",
    "Thermal Reset", "Steam Prep", "Ice Facial", "Gua Sha Ritual",
    "Sculpting Routine", "Lymphatic Boost", "Under-Eye Revival",

    # --- New: Makeup Workflow ---
    "Base Prep", "Complexion Build", "Soft Sculpt", "Full Sculpt",
    "Glow Finish", "Matte Finish", "Soft Glam Routine", "Night-Out Routine",
    "Editorial Routine", "Runway Routine", "Camera-Ready Routine",
    "Flash-Proof Routine", "Long-Wear Prep", "Touch-Up Cycle",

    # --- New: Fashion / Styling Routines ---
    "Workday Edit", "Weekend Edit", "Evening Edit", "Brunch Edit",
    "Date Night Edit", "Event Edit", "Vacation Edit", "Resort Edit",
    "Airport Routine", "City Routine", "Office Routine",
    "Street Style Routine", "Minimal Chic Routine", "Soft Luxe Routine",
    "Old Money Routine", "Quiet Luxury Routine",

    # --- New: Bodycare / Haircare ---
    "Body Polish", "Body Hydration", "Body Treatment", "Body Glow",
    "Hair Repair", "Hair Mask Night", "Scalp Reset", "Curl Routine",
    "Sleek Routine", "Volume Routine", "Heat Prep", "Air-Dry Routine",

    # --- New: Lifestyle / Wellness ---
    "Morning Reset", "Night Reset", "Pre-Event Ritual", "Post-Event Ritual",
    "Travel Reset", "Jet Lag Routine", "Wellness Ritual", "Mindful Moment",
    "Slow Morning", "Soft Evening", "Luxury Ritual", "Signature Ritual",

    # --- New: Seasonal Routines ---
    "Winter Skin Routine", "Summer Skin Routine", "Spring Refresh",
    "Fall Reset", "Holiday Routine", "Resort Routine",

    # --- New: Persona-Based Routines ---
    "Soft Luxury Ritual", "Runway Modern Ritual", "Clinical Chic Ritual",
    "Street Luxe Ritual", "Glow Maestro Ritual", "Elegant Authority Ritual",
    "Content Creator Routine", "Old Money Routine", "MVQueen Core Routine"
]
EXTRA_EDITORIAL_FRAMES = [
    "Crafted with {adj} clarity for {occasion} moments.",
    "A {mood} expression shaped by {adj} detail.",
    "Designed to elevate your {occasion} presence with {adj} intention."
]

SKIN_PROFILES = [
    # --- Original Core ---
    "All Skin", "Normal", "Dry", "Very Dry", "Oily", "Very Oily",
    "Combination", "Sensitive", "Reactive", "Acne-Prone", "Hormonal",
    "Mature", "Teen", "Post-Treatment", "Redness-Prone", "Uneven Tone",
    "Textured", "Dull", "Dehydrated", "Sun-Exposed", "Balanced",
    "Resilient", "Fragile", "Irritated", "Stressed", "Urban Skin",
    "Pollution-Exposed", "Barrier-Compromised", "Elasticity Loss",
    "Fine Lines", "Deep Lines", "Dark Spot Concern", "Hyperpigmentation",
    "Large Pores", "Congested", "T-Zone Oily", "Flaky", "Rough",
    "Tight", "Over-Exfoliated",

    # --- New: Hydration States ---
    "Moisture-Depleted", "Water-Dry", "Oil-Dry", "Surface-Dry",
    "Deep-Dry", "Hydration-Imbalanced", "Thirsty Skin",

    # --- New: Oil Balance States ---
    "Shine-Prone", "Sebum-Heavy", "Oil-Flux Skin", "Oil-Imbalanced",
    "Matte-Seeking", "Shine-Control Focused",

    # --- New: Sensitivity Spectrum ---
    "Easily Irritated", "Barrier-Weakened", "Redness-Sensitive",
    "Rosacea-Prone", "Inflamed", "Heat-Sensitive", "Allergy-Prone",

    # --- New: Texture Profiles ---
    "Bumpy Texture", "Clog-Prone", "Keratinized", "Uneven Surface",
    "Refined Texture", "Smooth-Seeking", "Pore-Visible",

    # --- New: Tone & Clarity Profiles ---
    "Brightness-Seeking", "Glow-Seeking", "Clarity-Focused",
    "Tone-Correcting", "Spot-Prone", "Melanin-Rich",
    "Uneven Pigment", "Shadow-Prone",

    # --- New: Age-Related Profiles ---
    "Pre-Mature Aging", "Early Aging", "Advanced Aging",
    "Loss of Firmness", "Elasticity-Depleted", "Volume-Loss Skin",
    "Crepey Skin", "Thin Skin",

    # --- New: Lifestyle-Based Profiles ---
    "Screen-Exposed", "Blue-Light Stressed", "Late-Night Skin",
    "High-Stress Skin", "Workout Skin", "Sweat-Prone",
    "Travel-Fatigued", "Jet Lag Skin", "Shift-Worker Skin",

    # --- New: Climate-Based Profiles ---
    "Cold-Climate Skin", "Humid-Climate Skin", "Dry-Climate Skin",
    "Tropical Skin", "Seasonally Reactive", "Winter-Dry",
    "Summer-Oily", "Heat-Reactive",

    # --- New: Treatment-Based Profiles ---
    "Retinol User", "Acid User", "Peel Recovery", "Post-Laser",
    "Post-Microneedling", "Post-Extraction", "Post-Procedure Skin",

    # --- New: Makeup-Specific Profiles ---
    "Foundation-Separating Skin", "Makeup-Pilling Skin",
    "Makeup-Gripping Skin", "Long-Wear Focused", "Matte-Finish Skin",
    "Dewy-Finish Skin", "Transfer-Prone Skin",

    # --- New: Bodycare Skin Profiles ---
    "Body Acne-Prone", "Keratosis Pilaris", "Rough Body Skin",
    "Dry Body Skin", "Ingrown-Prone", "Shave-Sensitive",

    # --- New: Persona-Based Skin Profiles ---
    "Soft Luxury Skin", "Runway Skin", "Clinical Skin",
    "Glow Maestro Skin", "Street Luxe Skin", "Old Money Skin",
    "Minimalist Skin", "Maximalist Skin",

    # --- New: Marketing-Friendly Profiles ---
    "Radiance-Seeking", "Plumpness-Seeking", "Smoothness-Seeking",
    "Barrier-Strengthening", "Calm-Seeking", "Firmness-Seeking",
    "Even-Tone Seeking", "Texture-Refining", "Glow-Restoring",
    "Hydration-Restoring", "Youth-Restoring"
]

TEXTURES = [
    # --- Original Core ---
    "Smooth", "Velvety", "Silky", "Creamy", "Lightweight", "Airy",
    "Rich", "Dense", "Fluffy", "Soft", "Cushiony", "Cloud-Like",
    "Cooling", "Refreshing", "Gel-Like", "Fluid", "Milky", "Whipped",
    "Balmy", "Oily", "Buttery", "Mousse-Like", "Serum-Like",

    # --- New: Skincare Textures ---
    "Water-Gel", "Aqua-Light", "Jelly", "Hydro-Gel", "Essence-Light",
    "Ampoule-Thin", "Lotion-Soft", "Cream-Gel", "Balm-to-Oil",
    "Oil-to-Milk", "Milk-to-Water", "Melting Texture", "Cushion Texture",
    "Featherweight", "Weightless", "Skin-Quenching", "Dewy Finish",
    "Glass-Skin Finish", "Velvet-Matte", "Soft-Matte", "Radiant-Satin",

    # --- New: Makeup Textures ---
    "Cream-to-Powder", "Powder-to-Cream", "Soft-Focus", "Blurring",
    "Airbrushed", "Second-Skin", "Buildable", "Sheer", "Full-Coverage",
    "Flexible Film", "Grip Texture", "Long-Wear Film", "Transfer-Resistant",
    "Cushion Matte", "Soft Glow", "High-Shine", "Glossy", "Lacquered",

    # --- New: Bodycare Textures ---
    "Body-Butter Rich", "Body-Oil Silky", "Body-Cream Dense",
    "Body-Lotion Fluid", "Body-Serum Light", "Scrub-Gritty",
    "Sugar-Scrub Melt", "Salt-Scrub Grainy", "Polishing Texture",
    "Smoothing Texture", "Buffing Texture",

    # --- New: Haircare Textures ---
    "Creamy Conditioner", "Silky Serum", "Lightweight Mist",
    "Foamy Cleanser", "Rich Mask", "Slip Texture", "Detangling Slip",
    "Smoothing Film", "Volumizing Air", "Curl Cream Soft",

    # --- New: Fabric / Fashion Textures ---
    "Ribbed Knit", "Fine Knit", "Chunky Knit", "Satin Smooth",
    "Silk Gloss", "Matte Cotton", "Crisp Poplin", "Structured Denim",
    "Soft Fleece", "Brushed Texture", "Sheer Mesh", "Tulle Lightness",
    "Chiffon Floaty", "Velvet Plush", "Suede Soft", "Leather Smooth",
    "Quilted Texture", "Padded Texture", "Woolen Softness",

    # --- New: Persona-Based Textures ---
    "Soft Luxury Texture", "Runway Texture", "Clinical Smooth",
    "Glow Maestro Finish", "Street Luxe Texture", "Old Money Texture",

    # --- New: Marketing-Friendly Textures ---
    "Skin-Like", "Barely-There", "Feather-Soft", "Ultra-Fine",
    "Micro-Refined", "Macro-Smooth", "Plush Finish", "Cushion Finish",
    "Radiance Film", "Hydration Film", "Barrier Film", "Glow Veil",
    "Matte Veil", "Satin Veil", "Soft Veil", "Diffused Finish",

    # --- New: High-End Luxury Textures ---
    "Cashmere-Soft", "Cloud-Cream", "Velvet-Cloud", "Silk-Veil",
    "Pearl-Sheen", "Diamond-Glow", "Opal-Finish", "Luxe-Melt",
    "Cream-Soufflé", "Feather-Mousse"
]

FINISHES = [
    # --- Original Core ---
    "Matte", "Soft Matte", "Velvet Matte", "Natural", "Radiant",
    "Dewy", "Glowy", "Luminous", "Satin", "Soft Focus", "Blurring",
    "Airbrushed", "Second-Skin", "Sheer", "Full-Coverage",

    # --- New: Makeup Finishes ---
    "Glass Skin", "Cloud Skin", "Skin-Like Finish", "Feather-Matte",
    "Cushion Matte", "Soft Glow", "High Shine", "Glossy", "Lacquered",
    "Metallic", "Pearlescent", "Iridescent", "Holographic",
    "Chrome Finish", "Soft Diffused", "Ultra-Matte", "Creamy Finish",
    "Powder Finish", "Cream-to-Powder", "Powder-to-Cream",
    "Transfer-Resistant", "Long-Wear Finish", "Grip Finish",

    # --- New: Skincare Finishes ---
    "Hydrated Finish", "Plump Finish", "Supple Finish", "Moisture-Locked",
    "Barrier-Sealed", "Fresh Finish", "Cooling Finish", "Soft Radiance",
    "Healthy Glow", "Lit-From-Within", "Dewdrop Finish", "Serum-Sheen",
    "Moisture Veil", "Hydration Veil", "Glow Veil", "Satin Veil",
    "Matte Veil", "Soft Veil", "Nourished Finish",

    # --- New: Bodycare Finishes ---
    "Body Glow", "Body Radiance", "Soft Sheen", "Silky Finish",
    "Velvet Body Finish", "Supple Body Finish", "Conditioned Finish",
    "Polished Finish", "Buffed Finish", "Smooth Body Finish",

    # --- New: Haircare Finishes ---
    "Glossy Hair Finish", "Shine Finish", "Sleek Finish", "Frizz-Control Finish",
    "Soft Curl Finish", "Defined Curl Finish", "Volume Finish",
    "Lightweight Shine", "Silky Hair Finish", "Smooth Hair Finish",

    # --- New: Fashion / Fabric Finishes ---
    "Matte Fabric", "Satin Sheen", "Silk Gloss", "Velvet Plush",
    "Suede Soft", "Leather Smooth", "Metallic Sheen", "High-Gloss Fabric",
    "Soft Brushed Finish", "Polished Finish", "Crisp Finish",
    "Structured Finish", "Flowy Finish", "Sheer Finish", "Semi-Sheer Finish",

    # --- New: Persona-Based Finishes ---
    "Soft Luxury Finish", "Runway Finish", "Clinical Finish",
    "Glow Maestro Finish", "Street Luxe Finish", "Old Money Finish",
    "Minimalist Finish", "Maximalist Finish",

    # --- New: Marketing-Friendly Finishes ---
    "Photo-Ready Finish", "Camera-Ready Finish", "Editorial Finish",
    "Runway-Ready Finish", "Everyday Finish", "Event-Ready Finish",
    "Polished Glow", "Refined Matte", "Ultra-Radiant", "Soft Radiant",
    "Diffused Glow", "Micro-Glow", "Macro-Glow", "Feather Glow",
    "Diamond Glow", "Opal Glow", "Pearl Glow", "Luxe Glow",

    # --- New: High-End Luxury Finishes ---
    "Cashmere Finish", "Velvet Finish", "Silk Finish", "Satin Finish",
    "Cloud Finish", "Feather Finish", "Luxe Matte", "Luxe Radiance",
    "Diamond-Sheen", "Opal-Sheen", "Pearl-Sheen"
]

MOOD_BANK = [
    # --- Core Moods ---
    "Soft", "Romantic", "Bold", "Minimal", "Classic", "Modern",
    "Fresh", "Clean", "Warm", "Cool", "Neutral", "Elegant",

    # --- Beauty Moods ---
    "Glowy", "Radiant", "Dewy", "Matte", "Sculpted", "Airbrushed",
    "Natural Glam", "Soft Glam", "Full Glam", "Fresh-Faced",
    "Lit-From-Within", "Glass-Skin", "Cloud-Skin", "Skin-Like",
    "Hydrated", "Plump", "Supple", "Brightened", "Clarified",

    # --- Fashion Moods ---
    "Runway", "Editorial", "Street Luxe", "Quiet Luxury",
    "Old Money", "New Money", "Minimal Chic", "Maximalist",
    "Soft Luxe", "Effortless", "Polished", "Tailored",
    "Relaxed", "Structured", "Flowy", "Sleek", "Sharp",
    "City Cool", "Resort", "Vacation", "Evening Glam",

    # --- Emotional Moods ---
    "Confident", "Empowered", "Calm", "Serene", "Playful",
    "Sensual", "Mysterious", "Bold Energy", "Soft Energy",
    "Grounded", "Uplifted", "Focused", "Balanced",
    "Self-Assured", "Self-Expressive", "Refined", "Assured",

    # --- Seasonal Moods ---
    "Spring Fresh", "Summer Bright", "Fall Cozy", "Winter Luxe",
    "Holiday Glam", "Resort Escape", "Sun-Kissed", "Frosted",

    # --- Persona-Based Moods ---
    "Soft Luxury Mood", "Runway Modern Mood", "Clinical Chic Mood",
    "Street Luxe Mood", "MISS.QUEEN Mood", "Glow Maestro Mood",
    "Elegant Authority Mood", "Content Creator Mood",
    "Old Money Modern Mood", "MVQueen Core Mood",

    # --- Texture-Driven Moods ---
    "Velvety Mood", "Silky Mood", "Featherlight Mood",
    "Cushiony Mood", "Satin Mood", "Glossy Mood",
    "Matte Mood", "Sheer Mood", "Diffused Mood",

    # --- Finish-Driven Moods ---
    "Radiance Mood", "Soft Glow Mood", "Ultra-Matte Mood",
    "Satin Glow Mood", "Diamond Glow Mood", "Pearl Glow Mood",

    # --- Lifestyle Moods ---
    "Workday Mood", "Weekend Mood", "Brunch Mood",
    "Date Night Mood", "Event Mood", "Travel Mood",
    "Jet Lag Mood", "Gym Mood", "Desk-to-Dinner Mood",
    "Off-Duty Mood", "On-The-Go Mood", "Luxury Ritual Mood",

    # --- Marketing-Friendly Moods ---
    "Everyday Elevated", "Effortlessly Polished", "Softly Defined",
    "Boldly Defined", "Refined Radiance", "Quiet Confidence",
    "Statement Energy", "Soft Power", "Glow Power",
    "Modern Elegance", "Timeless Ease", "Signature Mood",

    # --- High-End Luxury Moods ---
    "Cashmere Mood", "Velvet Mood", "Silk Mood",
    "Opulent Mood", "Luxe Minimalism", "High-Gloss Luxury",
    "Understated Luxury", "Stealth Wealth Mood"
]

SKIN_CONCERNS = [
    "Dryness",
    "Oiliness",
    "Dehydration",
    "Sensitivity",
    "Redness",
    "Irritation",
    "Acne",
    "Breakouts",
    "Blemishes",
    "Clogged Pores",
    "Large Pores",
    "Texture",
    "Uneven Texture",
    "Dullness",
    "Dark Spots",
    "Hyperpigmentation",
    "Discoloration",
    "Uneven Tone",
    "Fine Lines",
    "Wrinkles",
    "Loss of Firmness",
    "Loss of Elasticity",
    "Sagging",
    "Aging Skin",

    # --- Barrier / Damage Concerns ---
    "Barrier Damage",
    "Barrier Weakness",
    "Over-Exfoliation",
    "Compromised Barrier",
    "Stressed Skin",
    "Inflamed Skin",
    "Reactive Skin",

    # --- Acne Spectrum ---
    "Hormonal Acne",
    "Cystic Acne",
    "Blackheads",
    "Whiteheads",
    "Congestion",
    "Post-Acne Marks",
    "Post-Inflammatory Hyperpigmentation",

    # --- Hydration / Moisture Concerns ---
    "Moisture Loss",
    "Water Loss",
    "Tightness",
    "Flakiness",
    "Roughness",

    # --- Tone / Radiance Concerns ---
    "Lack of Radiance",
    "Lack of Glow",
    "Shadowing",
    "Uneven Pigment",
    "Sun Damage",
    "Photoaging",

    # --- Environmental Concerns ---
    "Pollution Damage",
    "Urban Skin Stress",
    "Blue Light Exposure",
    "Climate Stress",
    "Heat Sensitivity",
    "Cold Sensitivity",

    # --- Treatment / Procedure Concerns ---
    "Post-Treatment Sensitivity",
    "Post-Laser Recovery",
    "Post-Peel Recovery",
    "Post-Microneedling",
    "Post-Extraction Redness",

    # --- Makeup-Related Concerns ---
    "Makeup Separation",
    "Makeup Pilling",
    "Makeup Oxidation",
    "Transfer Issues",
    "Foundation Settling",

    # --- Body Skin Concerns ---
    "Body Acne",
    "Keratosis Pilaris",
    "Ingrown Hairs",
    "Rough Body Skin",
    "Dry Body Skin",

    # --- Persona-Based Concerns ---
    "Soft Luxury Skin Concern",
    "Runway Skin Concern",
    "Clinical Skin Concern",
    "Street Luxe Skin Concern",
    "Glow Maestro Skin Concern",
    "Old Money Skin Concern",

    # --- Marketing-Friendly Concerns ---
    "Glow Loss",
    "Firmness Loss",
    "Plumpness Loss",
    "Barrier Instability",
    "Texture Irregularities",
    "Tone Irregularities",
    "Radiance Loss"
]
BUSINESS_TIERS = [
    # --- Core Tiers ---
    "Entry", 
    "Standard", 
    "Premium", 
    "Luxury", 
    "Ultra Luxury",

    # --- Beauty / Skincare Tiers ---
    "Dermatologist Grade",
    "Clinical Grade",
    "Spa Grade",
    "Pro Artist Grade",
    "High-Performance",
    "Active-Rich",
    "Treatment Level",

    # --- Fashion / Apparel Tiers ---
    "Essential",
    "Elevated Essential",
    "Designer",
    "Runway",
    "Couture",
    "Heritage Luxury",
    "Quiet Luxury Tier",

    # --- Persona-Based Tiers ---
    "Soft Luxury Tier",
    "Runway Modern Tier",
    "Clinical Chic Tier",
    "Street Luxe Tier",
    "MISS.QUEEN Tier",
    "Glow Maestro Tier",
    "Elegant Authority Tier",
    "Content Creator Tier",
    "Old Money Modern Tier",
    "MVQueen Core Tier",

    # --- Marketing-Friendly Tiers ---
    "Everyday Elevated",
    "Performance Elevated",
    "Signature Tier",
    "Statement Tier",
    "Soft Power Tier",
    "Glow Power Tier",
    "Modern Luxury Tier",

    # --- High-End Luxury Tiers ---
    "Prestige",
    "Ultra Prestige",
    "Collector Tier",
    "Exclusive Tier",
    "Members-Only Tier",
    "Private Label Tier",
    "Opulent Tier",
    "Stealth Wealth Tier"
]

SKIN_GOALS = [
    # --- Core Goals ---
    "Hydrated Skin",
    "Balanced Skin",
    "Clear Skin",
    "Glowing Skin",
    "Radiant Skin",
    "Smooth Skin",
    "Even Tone",
    "Brightened Skin",
    "Refined Texture",
    "Healthy Barrier",

    # --- Hydration Goals ---
    "Deep Hydration",
    "Long-Lasting Hydration",
    "Moisture Retention",
    "Plump Skin",
    "Supple Skin",
    "Dewy Skin",

    # --- Clarity & Tone Goals ---
    "Brighter Complexion",
    "Even Complexion",
    "Dark Spot Reduction",
    "Hyperpigmentation Correction",
    "Tone Correction",
    "Shadow Reduction",
    "Radiance Boost",

    # --- Texture Goals ---
    "Smoother Texture",
    "Pore Minimizing",
    "Refined Pores",
    "Softened Texture",
    "Glass Skin Finish",
    "Cloud Skin Finish",

    # --- Acne & Blemish Goals ---
    "Acne Reduction",
    "Breakout Prevention",
    "Blemish Control",
    "Clearer Complexion",
    "Oil Balance",
    "Congestion Reduction",

    # --- Anti-Aging Goals ---
    "Fine Line Reduction",
    "Wrinkle Reduction",
    "Firming",
    "Lifting",
    "Elasticity Boost",
    "Youthful Glow",
    "Age Defense",

    # --- Barrier & Sensitivity Goals ---
    "Barrier Repair",
    "Barrier Strengthening",
    "Reduced Redness",
    "Calmer Skin",
    "Less Irritation",
    "Sensitivity Support",

    # --- Environmental Goals ---
    "Pollution Defense",
    "Blue Light Defense",
    "Climate Protection",
    "Urban Skin Support",

    # --- Treatment-Based Goals ---
    "Post-Treatment Recovery",
    "Post-Laser Recovery",
    "Post-Peel Recovery",
    "Post-Microneedling Recovery",

    # --- Makeup-Related Skin Goals ---
    "Makeup Grip",
    "Makeup Longevity",
    "Smooth Base",
    "Non-Pilling Base",
    "Foundation-Friendly Skin",

    # --- Body Skin Goals ---
    "Smoother Body Skin",
    "Body Glow",
    "Even Body Tone",
    "Ingrown Reduction",
    "KP Smoothing",

    # --- Persona-Based Skin Goals ---
    "Soft Luxury Skin Goal",
    "Runway Skin Goal",
    "Clinical Skin Goal",
    "Street Luxe Skin Goal",
    "Glow Maestro Skin Goal",
    "Old Money Skin Goal",

    # --- Marketing-Friendly Goals ---
    "Lit-From-Within Glow",
    "Soft Radiance",
    "Youth-Restoring",
    "Texture-Refining",
    "Tone-Perfecting",
    "Glow-Restoring",
    "Hydration-Restoring",
    "Barrier-Restoring"
]

SKIN_TEXTURES = [
    # --- Core Skin Textures ---
    "Smooth",
    "Soft",
    "Supple",
    "Plump",
    "Firm",
    "Refined",
    "Even",
    "Balanced",

    # --- Texture Concerns ---
    "Rough",
    "Bumpy",
    "Uneven",
    "Textured",
    "Flaky",
    "Dry-Flaky",
    "Oily-Slick",
    "Combination Texture",
    "Clogged",
    "Congested",
    "Pore-Visible",
    "Large Pores",
    "Keratinized",

    # --- Hydration-Driven Textures ---
    "Dewy",
    "Hydrated",
    "Moisturized",
    "Water-Rich",
    "Moisture-Locked",
    "Quenched",
    "Velvety Hydrated",
    "Glass-Skin Smooth",

    # --- Oil Balance Textures ---
    "Matte",
    "Soft Matte",
    "Velvet Matte",
    "Balanced Matte",
    "Shine-Controlled",
    "Oil-Controlled",
    "Semi-Matte",

    # --- Glow / Radiance Textures ---
    "Radiant",
    "Glowy",
    "Luminous",
    "Lit-From-Within",
    "Soft Glow",
    "Pearl Glow",
    "Diamond Glow",
    "Healthy Glow",

    # --- Barrier / Sensitivity Textures ---
    "Barrier-Strong",
    "Barrier-Weakened",
    "Barrier-Compromised",
    "Fragile Texture",
    "Reactive Texture",
    "Redness-Prone Texture",
    "Inflamed Texture",

    # --- Aging-Related Textures ---
    "Fine-Line Texture",
    "Crepey Texture",
    "Elasticity-Loss Texture",
    "Thin-Skin Texture",
    "Firmness-Loss Texture",

    # --- Treatment-Based Textures ---
    "Post-Treatment Smooth",
    "Post-Peel Texture",
    "Post-Laser Texture",
    "Post-Microneedling Texture",
    "Retinol Night Texture",
    "Acid Night Texture",

    # --- Makeup-Related Skin Textures ---
    "Makeup-Gripping Texture",
    "Makeup-Friendly Texture",
    "Non-Pilling Texture",
    "Foundation-Smoothing Texture",
    "Base-Ready Texture",
    "Long-Wear Texture",

    # --- Body Skin Textures ---
    "Body Smooth",
    "Body Rough",
    "Body Soft",
    "Body Hydrated",
    "KP Texture",
    "Ingrown-Prone Texture",

    # --- Persona-Based Skin Textures ---
    "Soft Luxury Skin Texture",
    "Runway Skin Texture",
    "Clinical Skin Texture",
    "Street Luxe Skin Texture",
    "Glow Maestro Skin Texture",
    "Old Money Skin Texture",

    # --- Marketing-Friendly Textures ---
    "Feather-Smooth",
    "Cushion-Smooth",
    "Micro-Refined",
    "Macro-Refined",
    "Ultra-Smooth",
    "Skin-Like Texture",
    "Barely-There Texture",
    "Diffused Texture",
    "Soft-Focus Texture"
]

SKIN_BENEFIT_KEYWORDS = [
    # --- Hydration ---
    "hydrate", "hydrating", "hydration",
    "moisturize", "moisturizing", "moisture",
    "moisture-lock", "water-rich", "water-binding",
    "plumping", "plump", "dewy", "quenched",
    "moisture barrier", "hydration boost", "hydration restoring",

    # --- Barrier Support ---
    "barrier repair", "repairing", "barrier strengthening",
    "strengthen barrier", "barrier support", "barrier restore",
    "replenish barrier", "fortify barrier", "barrier protection",
    "soothing moisture", "nourishing moisture", "calming moisture",
    "barrier replenishing", "barrier fortifying",

    # --- Brightening / Tone ---
    "brighten", "brightening", "radiance", "radiant",
    "glow", "glowing", "tone-evening", "even tone",
    "dark spots", "spot fading", "spot corrector",
    "hyperpigmentation", "discoloration", "dullness",
    "tone correction", "tone perfecting", "radiance boosting",
    "glow restoring", "lit-from-within",

    # --- Texture Refining ---
    "smooth", "smoothing", "refine texture", "texture refining",
    "soften texture", "pore minimizing", "pore reduction",
    "pore refining", "bumpy skin", "rough texture",
    "glass skin", "cloud skin", "micro-refining",
    "soft-focus", "blurring", "airbrushed",

    # --- Acne / Blemish ---
    "acne", "acne-prone", "breakouts", "blemish",
    "blemish control", "oil control", "sebum control",
    "congestion", "congested", "blackheads", "whiteheads",
    "clarifying", "purifying", "post-acne marks",
    "acne clearing", "acne treatment", "pore clearing",

    # --- Anti-Aging ---
    "fine lines", "wrinkles", "firming", "lifting",
    "elasticity", "anti-aging", "age defense",
    "youthful", "renewal", "skin renewal",
    "collagen support", "resurfacing", "skin tightening",
    "plumping effect", "line smoothing",

    # --- Redness / Sensitivity ---
    "redness", "reduce redness", "calming", "soothing",
    "sensitive skin", "irritation", "anti-inflammatory",
    "cooling relief", "comforting", "skin calming",
    "rosacea-friendly", "gentle formula",

    # --- Environmental Protection ---
    "pollution defense", "anti-pollution", "urban defense",
    "blue light", "antioxidant", "environmental protection",
    "climate protection", "free radical defense",
    "environmental shield",

    # --- Treatment-Level Keywords ---
    "exfoliate", "exfoliating", "gentle exfoliation",
    "resurfacing", "cell turnover", "post-treatment",
    "post-peel", "post-laser", "post-microneedling",
    "aha", "bha", "pha", "enzyme treatment",

    # --- Makeup Prep ---
    "makeup grip", "gripping", "long-wear",
    "foundation smoothness", "non-pilling", "blurring",
    "soft-focus", "primer-like", "makeup-ready",
    "base-smoothing", "pore-blurring",

    # --- Body Skin Keywords ---
    "body smoothing", "body glow", "kp", "keratosis pilaris",
    "ingrown", "body firming", "body exfoliating",
    "body hydration",

    # --- Oil Balance ---
    "oil balancing", "shine control", "matte control",
    "oil absorbing", "sebum balancing",

    # --- Barrier / Recovery ---
    "barrier restoring", "barrier healing", "barrier stabilizing",
    "post-procedure", "post-treatment recovery",

    # --- Persona Keywords ---
    "soft luxury skin", "runway skin", "clinical skin",
    "street luxe skin", "glow maestro skin", "old money skin",

    # --- Marketing-Friendly Keywords ---
    "soft radiance", "youth-restoring", "texture-refining",
    "tone-perfecting", "hydration-restoring", "plumpness-restoring",
    "radiance-restoring", "glow-enhancing", "skin-transforming",
    "skin-renewing", "skin-perfecting"
]

EXTRA_DESCRIPTION = [
    # --- Sensory Descriptions ---
    "lightweight feel",
    "silky texture",
    "velvety glide",
    "cushiony feel",
    "featherlight finish",
    "cooling sensation",
    "soothing touch",
    "skin-quenching feel",
    "soft-focus effect",
    "airbrushed effect",
    "cloud-like texture",
    "water-gel feel",
    "buttery smoothness",

    # --- Application Experience ---
    "melts into skin",
    "absorbs instantly",
    "fast-absorbing",
    "non-greasy",
    "non-sticky",
    "breathable formula",
    "buildable texture",
    "layer-friendly",
    "makeup-friendly",
    "primer-like finish",

    # --- Luxury Descriptions ---
    "editorial-grade finish",
    "runway-ready skin",
    "soft luxury feel",
    "quiet luxury glow",
    "old money radiance",
    "clinical-luxe texture",
    "spa-grade experience",
    "dermatologist-grade feel",
    "premium skin finish",
    "couture-level smoothness",

    # --- Performance Descriptions ---
    "high-performance formula",
    "multi-corrective action",
    "multi-benefit treatment",
    "advanced skin renewal",
    "deep-penetrating actives",
    "targeted treatment",
    "fast-acting results",
    "visible improvement",
    "long-lasting hydration",
    "intensive nourishment",

    # --- Finish Descriptions ---
    "glass-skin effect",
    "cloud-skin effect",
    "lit-from-within glow",
    "soft matte veil",
    "radiant satin finish",
    "natural skin-like finish",
    "dewy luminosity",
    "velvet-matte finish",
    "soft-diffused glow",

    # --- Skin Feel Descriptions ---
    "skin feels balanced",
    "skin feels refreshed",
    "skin feels renewed",
    "skin feels comforted",
    "skin feels strengthened",
    "skin feels replenished",
    "skin feels soothed",
    "skin feels plump",
    "skin feels hydrated",

    # --- Clinical Descriptions ---
    "dermatologist tested",
    "clinically inspired",
    "science-backed formula",
    "active-rich treatment",
    "precision-targeted actives",
    "ph-balanced formula",
    "non-comedogenic",
    "hypoallergenic",
    "fragrance-free option",

    # --- Marketing-Friendly Descriptions ---
    "transformative results",
    "youth-restoring effect",
    "radiance-boosting glow",
    "texture-refining action",
    "tone-perfecting clarity",
    "barrier-strengthening support",
    "hydration-restoring power",
    "skin-renewing energy",
    "glow-enhancing finish",

    # --- Persona-Based Descriptions ---
    "soft luxury aesthetic",
    "runway modern aesthetic",
    "clinical chic aesthetic",
    "street luxe aesthetic",
    "glow maestro aesthetic",
    "old money modern aesthetic",
    "mvqueen core aesthetic"
]

SKINCARE_INGREDIENT_KEYWORDS = [
    # --- Hydration Ingredients ---
    "hyaluronic acid",
    "ha",
    "glycerin",
    "squalane",
    "squalene",
    "panthenol",
    "vitamin b5",
    "aloe",
    "aloe vera",
    "beta glucan",
    "urea",
    "ceramides",
    "ceramide",
    "amino acids",
    "electrolytes",

    # --- Barrier Support Ingredients ---
    "ceramide np",
    "ceramide ap",
    "ceramide eop",
    "cholesterol",
    "fatty acids",
    "omega fatty acids",
    "niacinamide",
    "centella",
    "cica",
    "madecassoside",
    "asiaticoside",
    "bisabolol",
    "allantoin",

    # --- Brightening Ingredients ---
    "vitamin c",
    "ascorbic acid",
    "ascorbyl glucoside",
    "tetrahexyldecyl ascorbate",
    "niacinamide",
    "alpha arbutin",
    "arbutin",
    "kojic acid",
    "licorice root",
    "tranexamic acid",
    "azelaic acid",
    "resveratrol",
    "mulberry extract",
    "bearberry extract",

    # --- Exfoliating Ingredients ---
    "aha",
    "bha",
    "pha",
    "lactic acid",
    "glycolic acid",
    "mandelic acid",
    "salicylic acid",
    "enzymes",
    "fruit enzymes",
    "papaya enzyme",
    "pumpkin enzyme",
    "exfoliating acids",

    # --- Acne / Clarifying Ingredients ---
    "salicylic acid",
    "benzoyl peroxide",
    "tea tree",
    "sulfur",
    "willow bark",
    "zinc",
    "niacinamide",
    "azelaic acid",
    "clay",
    "kaolin",
    "bentonite",
    "charcoal",

    # --- Anti-Aging Ingredients ---
    "retinol",
    "retinoid",
    "retinal",
    "retinaldehyde",
    "bakuchiol",
    "peptides",
    "copper peptides",
    "matrixyl",
    "collagen peptides",
    "coq10",
    "resveratrol",
    "ferulic acid",
    "growth factors",

    # --- Soothing / Redness Ingredients ---
    "centella asiatica",
    "cica",
    "green tea",
    "chamomile",
    "oat",
    "colloidal oatmeal",
    "aloe",
    "licorice root",
    "mugwort",
    "calendula",
    "bisabolol",
    "allantoin",

    # --- Antioxidants ---
    "vitamin e",
    "tocopherol",
    "ferulic acid",
    "resveratrol",
    "green tea",
    "coq10",
    "polyphenols",
    "flavonoids",
    "antioxidant complex",

    # --- Oil Control Ingredients ---
    "zinc",
    "niacinamide",
    "clay",
    "kaolin",
    "bentonite",
    "salicylic acid",
    "tea tree",
    "witch hazel",

    # --- SPF / UV Support (Non-SPF Claims) ---
    "zinc oxide",
    "titanium dioxide",
    "uva filter",
    "uvb filter",
    "mineral filter",
    "chemical filter",

    # --- Bodycare Ingredients ---
    "lactic acid",
    "urea",
    "salicylic acid",
    "glycolic acid",
    "retinol",
    "shea butter",
    "cocoa butter",
    "jojoba oil",
    "argan oil",

    # --- Hydrating Oils ---
    "rosehip oil",
    "marula oil",
    "argan oil",
    "jojoba oil",
    "squalane",
    "evening primrose oil",

    # --- Luxury / High-End Ingredients ---
    "24k gold",
    "gold peptides",
    "caviar extract",
    "diamond powder",
    "pearl extract",
    "silk protein",
    "snail mucin",
    "propolis",
    "royal jelly",

    # --- Clinical / Dermatologist Ingredients ---
    "ceramides",
    "urea",
    "azelaic acid",
    "retinoid",
    "benzoyl peroxide",
    "salicylic acid",
    "aha",
    "bha",
    "pha",

    # --- Marketing-Friendly Ingredients ---
    "superfood complex",
    "botanical blend",
    "plant extract",
    "fruit extract",
    "herbal complex",
    "peptide complex",
    "hydration complex",
    "radiance complex",
    "barrier complex"
]

SKIN_FINISH_PREFERENCES = [
    # --- Core Preferences ---
    "Matte Finish",
    "Soft Matte Finish",
    "Velvet Matte Finish",
    "Natural Finish",
    "Skin-Like Finish",
    "Radiant Finish",
    "Glowy Finish",
    "Dewy Finish",
    "Luminous Finish",
    "Satin Finish",

    # --- Glow Spectrum ---
    "Soft Glow Finish",
    "Healthy Glow Finish",
    "Lit-From-Within Finish",
    "Glass Skin Finish",
    "Cloud Skin Finish",
    "Pearl Glow Finish",
    "Diamond Glow Finish",
    "Opal Glow Finish",
    "Micro-Glow Finish",
    "Macro-Glow Finish",
    "Sheer Glow Finish",
    "Ultra-Radiant Finish",

    # --- Matte Spectrum ---
    "Feather-Matte Finish",
    "Semi-Matte Finish",
    "Balanced Matte Finish",
    "Oil-Control Matte Finish",
    "Shine-Control Finish",
    "Blurring Matte Finish",
    "Airbrushed Matte Finish",

    # --- Coverage Preferences ---
    "Sheer Skin Finish",
    "Light Coverage Finish",
    "Medium Coverage Finish",
    "Full Coverage Finish",
    "Buildable Coverage Finish",
    "Soft-Focus Finish",
    "Blurring Finish",
    "Airbrushed Finish",
    "Second-Skin Finish",

    # --- Texture-Driven Preferences ---
    "Smooth Finish",
    "Refined Finish",
    "Pore-Minimized Finish",
    "Even-Tone Finish",
    "Soft-Diffused Finish",
    "Feather-Smooth Finish",
    "Cushion-Smooth Finish",
    "Micro-Refined Finish",
    "Ultra-Smooth Finish",

    # --- Hydration-Driven Preferences ---
    "Hydrated Finish",
    "Plump Finish",
    "Moisture-Locked Finish",
    "Supple Finish",
    "Dewdrop Finish",
    "Moisture-Glow Finish",

    # --- Treatment-Driven Preferences ---
    "Barrier-Healthy Finish",
    "Barrier-Strengthened Finish",
    "Redness-Reduced Finish",
    "Calm Finish",
    "Post-Treatment Smooth Finish",
    "Clinical Smooth Finish",

    # --- Makeup-Ready Preferences ---
    "Makeup-Gripping Finish",
    "Foundation-Friendly Finish",
    "Long-Wear Finish",
    "Non-Pilling Finish",
    "Transfer-Resistant Finish",
    "Camera-Ready Finish",
    "Photo-Ready Finish",

    # --- Oil Balance Preferences ---
    "Balanced Finish",
    "Shine-Free Finish",
    "Oil-Balanced Finish",
    "Semi-Dewy Finish",
    "Matte-Glow Finish",

    # --- Radiance Spectrum ---
    "Soft Radiance Finish",
    "Refined Radiance Finish",
    "High-Shine Radiance Finish",
    "Satin Glow Finish",
    "Velvet Glow Finish",
    "Luxe Radiance Finish",

    # --- Persona-Based Preferences ---
    "Soft Luxury Finish",
    "Runway Finish",
    "Clinical Finish",
    "Street Luxe Finish",
    "Glow Maestro Finish",
    "Old Money Finish",
    "Minimalist Finish",
    "Maximalist Finish",
    "MVQueen Core Finish",

    # --- Marketing-Friendly Preferences ---
    "Editorial Finish",
    "Everyday Finish",
    "Event-Ready Finish",
    "Signature Skin Finish",
    "Elevated Natural Finish",
    "Quiet Luxury Skin Finish",
    "Stealth Wealth Skin Finish",
    "Soft Power Finish",
    "Statement Finish",

    # --- High-End Luxury Preferences ---
    "Cashmere Finish",
    "Silk Finish",
    "Velvet Finish",
    "Satin Veil Finish",
    "Glow Veil Finish",
    "Matte Veil Finish",
    "Soft Veil Finish",
    "Diamond-Sheen Finish",
    "Opal-Sheen Finish",
    "Pearl-Sheen Finish"
]

EXTRA_TAGS = [
    # --- General Product Tags ---
    "New Arrival",
    "Bestseller",
    "Limited Edition",
    "Online Exclusive",
    "Back in Stock",
    "Editor Favorite",
    "Trending Now",
    "Seasonal Favorite",

    # --- Pricing / Business Tier Tags ---
    "Entry Tier",
    "Standard Tier",
    "Premium Tier",
    "Luxury Tier",
    "Ultra Luxury Tier",
    "Quiet Luxury Tier",
    "Soft Luxury Tier",
    "Runway Tier",
    "Clinical Tier",

    # --- Occasion Tags ---
    "Everyday Use",
    "Workday Ready",
    "Weekend Ready",
    "Event Ready",
    "Travel Friendly",
    "Vacation Ready",
    "Date Night Ready",
    "Brunch Ready",
    "Office Approved",

    # --- Style / Aesthetic Tags ---
    "Minimalist",
    "Maximalist",
    "Classic Style",
    "Modern Style",
    "Street Luxe",
    "Old Money",
    "Soft Glam",
    "Clean Girl",
    "Runway Inspired",
    "Editorial Style",

    # --- Seasonal Tags ---
    "Spring Essential",
    "Summer Essential",
    "Fall Essential",
    "Winter Essential",
    "Holiday Essential",
    "Resort Essential",

    # --- Performance / Benefit Tags ---
    "High Performance",
    "Multi Benefit",
    "Fast Acting",
    "Long Lasting",
    "Clinically Inspired",
    "Dermatologist Inspired",
    "Active Rich",
    "Treatment Level",

    # --- Texture / Finish Tags ---
    "Lightweight",
    "Rich Texture",
    "Silky Finish",
    "Velvety Finish",
    "Dewy Finish",
    "Matte Finish",
    "Radiant Finish",
    "Soft Focus Finish",

    # --- Ingredient / Formula Tags ---
    "Clean Formula",
    "Vegan Formula",
    "Cruelty Free",
    "Fragrance Free",
    "Sensitive Skin Safe",
    "Non Comedogenic",
    "Oil Free",
    "Alcohol Free",
    "Paraben Free",
    "Sulfate Free",

    # --- Product Experience Tags ---
    "Quick Absorbing",
    "Buildable",
    "Layer Friendly",
    "Makeup Friendly",
    "Travel Size",
    "Full Size",
    "Refillable",

    # --- Persona Tags ---
    "Soft Luxury Persona",
    "Runway Modern Persona",
    "Clinical Chic Persona",
    "Street Luxe Persona",
    "Glow Maestro Persona",
    "Old Money Persona",
    "MVQueen Core Persona",

    # --- Marketing Tags ---
    "Glow Boosting",
    "Texture Refining",
    "Tone Perfecting",
    "Hydration Restoring",
    "Barrier Strengthening",
    "Youth Restoring",
    "Radiance Enhancing",
    "Skin Transforming",

    # --- Shopify Utility Tags ---
    "Giftable",
    "Bundle Friendly",
    "Starter Friendly",
    "Advanced Routine",
    "Hero Product",
    "Core Collection",
    "Limited Drop"
]