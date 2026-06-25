# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — HYBRID DETECTION SYSTEM
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import deterministic_seed, deterministic_choice


# ---------------------------------------------------------
# VOCAB BANKS (KEYWORDS + FALLBACK OPTIONS)
# ---------------------------------------------------------

PERSONAS = {
    "Evening Elegance": ["gown", "satin", "silk", "evening", "formal"],
    "Street Luxe": ["denim", "oversized", "cargo", "street", "hoodie"],
    "Soft Glam": ["serum", "glow", "hydrating", "dewy", "radiance"],
    "Minimal Classic": ["tailored", "structured", "clean", "minimal"],
}

CATEGORIES = {
    "Dresses": ["dress", "gown", "slip"],
    "Outerwear": ["coat", "jacket", "trench"],
    "Tops": ["top", "blouse", "shirt", "tee"],
    "Bottoms": ["pants", "denim", "jeans", "skirt"],
    "Beauty": ["serum", "cream", "lip", "skin"],
}

PRODUCT_TYPES = {
    "Slip Dress": ["slip", "satin", "lace"],
    "Wool Coat": ["wool", "coat", "structured"],
    "Hydrating Serum": ["serum", "hydrating", "glow"],
    "High-Waisted Denim": ["denim", "high-waisted", "raw hem"],
}

TRENDS = {
    "Soft Glam": ["glow", "dewy", "radiance"],
    "Structured Minimalism": ["structured", "clean lines"],
    "Street Utility": ["cargo", "oversized"],
    "Romantic Lace": ["lace", "delicate"],
}

SEASONS = {
    "Spring": ["floral", "lightweight", "pastel"],
    "Summer": ["linen", "breezy", "sun"],
    "Fall": ["wool", "layered", "warm"],
    "Winter": ["coat", "thermal", "heavy"],
}

VIBES = {
    "Romantic": ["lace", "soft", "delicate"],
    "Edgy": ["leather", "hardware", "black"],
    "Minimal": ["clean", "simple", "structured"],
    "Glam": ["satin", "shine", "glow"],
}

MATERIALS = {
    "Satin": ["satin"],
    "Wool": ["wool"],
    "Denim": ["denim"],
    "Cotton": ["cotton"],
    "Leather": ["leather"],
}

SILHOUETTES = {
    "A-Line": ["a-line"],
    "Bodycon": ["bodycon", "fitted"],
    "Oversized": ["oversized"],
    "Straight": ["straight", "classic"],
}

DETAILS = {
    "Lace Trim": ["lace", "trim"],
    "Raw Hem": ["raw hem"],
    "Silver Hardware": ["silver hardware"],
    "Structured Shoulders": ["structured shoulders"],
    "Ribbed": ["ribbed"],
    "Pleated": ["pleated"],
    "Ruched": ["ruched"],
    "Smocked": ["smocked"],
    "Quilted": ["quilted"],
    "Padded": ["padded"],
    "Woven": ["woven"],
    "Cropped": ["cropped"],
    "Distressed": ["distressed"],
    "Raw Hem": ["raw hem", "frayed hem"],
    "Contrast Stitching": ["contrast stitching"],
    "Embroidered": ["embroidered"],
    "Beaded": ["beaded"],
    "Sequined": ["sequined"],
    "Embellished": ["embellished"],
    "Appliqué": ["applique", "appliqué"],
    "Laser Cut": ["laser cut"],
    "Cutout": ["cutout", "cut-out"],
    "Mesh Panel": ["mesh panel"],
    "Sheer Panel": ["sheer panel"],
    "Lace Trim": ["lace trim", "lace"],
    "Scalloped Edge": ["scalloped edge"],

    # --- Closure Details ---
    "Button Front": ["button front"],
    "Zip Front": ["zip front", "zipper front"],
    "Exposed Zipper": ["exposed zipper"],
    "Invisible Zipper": ["invisible zipper"],
    "Snap Closure": ["snap closure"],
    "Hook Closure": ["hook closure"],
    "Tie Waist": ["tie waist"],
    "Belted Waist": ["belted waist"],
    "Drawstring Waist": ["drawstring waist"],
    "Elastic Waist": ["elastic waist"],

    # --- Sleeve Details ---
    "Balloon Sleeve": ["balloon sleeve"],
    "Puff Sleeve": ["puff sleeve"],
    "Bishop Sleeve": ["bishop sleeve"],
    "Flutter Sleeve": ["flutter sleeve"],
    "Cap Sleeve": ["cap sleeve"],
    "Dolman Sleeve": ["dolman sleeve"],
    "Kimono Sleeve": ["kimono sleeve"],
    "Ruched Sleeve": ["ruched sleeve"],
    "Rolled Sleeve": ["rolled sleeve"],

    # --- Neckline Details ---
    "V-Neck": ["v-neck", "v neck"],
    "Deep V-Neck": ["deep v-neck", "deep v neck"],
    "Scoop Neck": ["scoop neck"],
    "Square Neck": ["square neck"],
    "Sweetheart Neck": ["sweetheart neck"],
    "Halter Neck": ["halter neck"],
    "Mock Neck": ["mock neck"],
    "Turtleneck": ["turtleneck"],
    "Off Shoulder": ["off shoulder", "off-shoulder"],
    "One Shoulder": ["one shoulder"],
    "Asymmetric Neckline": ["asymmetric neckline"],

    # --- Fit & Construction ---
    "Tailored Fit": ["tailored fit"],
    "Relaxed Fit": ["relaxed fit"],
    "Oversized Fit": ["oversized fit"],
    "Structured Fit": ["structured fit"],
    "Bodycon Fit": ["bodycon"],
    "Draped Fit": ["draped fit"],
    "Boxy Fit": ["boxy fit"],
    "Cinched Waist": ["cinched waist"],
    "Fitted Bodice": ["fitted bodice"],
    "Panel Construction": ["panel construction"],
    "Darted Bodice": ["darted bodice"],

    # --- Skirt / Dress Details ---
    "Tiered Skirt": ["tiered skirt"],
    "Ruffle Hem": ["ruffle hem"],
    "Slit Hem": ["slit hem"],
    "Side Slit": ["side slit"],
    "Front Slit": ["front slit"],
    "High Slit": ["high slit"],
    "Pleated Skirt": ["pleated skirt"],
    "Wrap Skirt": ["wrap skirt"],

    # --- Texture Details ---
    "Satin Finish": ["satin finish"],
    "Matte Finish": ["matte finish"],
    "Glossy Finish": ["glossy finish"],
    "Metallic Finish": ["metallic finish"],
    "Velvet Texture": ["velvet texture"],
    "Suede Texture": ["suede texture"],
    "Faux Leather Texture": ["faux leather texture"],
    "Rib Knit Texture": ["rib knit"],
    "Waffle Knit Texture": ["waffle knit"],

    # --- Hardware Details ---
    "Gold Hardware": ["gold hardware"],
    "Silver Hardware": ["silver hardware"],
    "Metal Hardware": ["metal hardware"],
    "Statement Buttons": ["statement buttons"],
    "Tortoise Buttons": ["tortoise buttons"],

    # --- Luxury Details ---
    "Couture Detail": ["couture detail", "couture-inspired"],
    "Runway Detail": ["runway detail"],
    "Editorial Detail": ["editorial detail"],
    "Quiet Luxury Detail": ["quiet luxury detail"],
    "Old Money Detail": ["old money detail"],
    "Soft Luxury Detail": ["soft luxury detail"],
    "Street Luxe Detail": ["street luxe detail"],

    # --- Marketing-Friendly Details ---
    "Elevated Detail": ["elevated detail"],
    "Signature Detail": ["signature detail"],
    "Statement Detail": ["statement detail"],
    "Minimal Detail": ["minimal detail"],
    "Refined Detail": ["refined detail"],
    "Modern Detail": ["modern detail"],
    "Classic Detail": ["classic detail"],
    "Trend-Forward Detail": ["trend-forward detail"],
}


# ---------------------------------------------------------
# GENERIC HYBRID DETECTION FUNCTION
# ---------------------------------------------------------

def _detect(text: str, vocab: dict, salt: str) -> str:
    lower = text.lower()

    # Keyword match
    for label, keywords in vocab.items():
        if any(k in lower for k in keywords):
            return label

    # Deterministic fallback
    seed = deterministic_seed(text)
    return deterministic_choice(seed, list(vocab.keys()), salt=salt)


# ---------------------------------------------------------
# PUBLIC DETECTION FUNCTIONS
# ---------------------------------------------------------

def detect_persona(text: str) -> str:
    return _detect(text, PERSONAS, "persona")


def detect_category(text: str) -> str:
    return _detect(text, CATEGORIES, "category")


def detect_product_types(text: str) -> str:
    return _detect(text, PRODUCT_TYPES, "product_types")


def detect_trend(text: str) -> str:
    return _detect(text, TRENDS, "trend")


def detect_season(text: str) -> str:
    return _detect(text, SEASONS, "season")


def detect_vibe(text: str) -> str:
    return _detect(text, VIBES, "vibe")


def detect_material(text: str) -> str:
    return _detect(text, MATERIALS, "material")


def detect_silhouette(text: str) -> str:
    return _detect(text, SILHOUETTES, "silhouette")


def detect_details(text: str) -> str:
    return _detect(text, DETAILS, "details")
   
 
def detect_skin_profile(text: str) -> str:
    return _detect(text, SKIN_PROFILE, "skin_profile")


def detect_skin_concerns(text: str) -> str:
    return _detect(text, SKIN_CONCERNS, "skin_concerns")
    
def detect_category_keywords(text: str) -> str:
    return _detect(text,CATEGORY_KEYWORDS, "category_keywords")