# mvqueen_engine/brand_brain/brand_banks/fashion_banks.py
"""
Fashion vocabulary banks for the MVQueen Omniluxe Engine.

These banks define the core fashion language used across:
- Editorial descriptions
- Titles
- SEO content
- Persona voice
- Detection fallback language
- Tag and collection generation

All vocab is women-centered, luxury-hybrid, and aligned with the
MVQueen brand voice: elevated, modern, sensual, confident, and intentional.
"""

# Core fashion adjectives (luxury, modern, editorial)
FASHION_SILHOUETTES = [
    "A-line", "Bodycon", "Slip", "Sheath", "Fit-and-Flare", "Oversized",
    "Tailored", "Cropped", "High-Waisted", "Wide-Leg", "Straight-Leg",
    "Relaxed Fit", "Boxy", "Structured", "Draped", "Asymmetric", "Wrap",
    "Peplum", "Midi", "Mini", "Maxi", "Off-Shoulder", "One-Shoulder",
    "Halter", "Racerback", "Bustier", "Corset", "Balloon Sleeve",
    "Puff Sleeve", "Cap Sleeve", "Longline", "Trench", "Bomber",
    "Blazer Cut", "Skater", "Column", "Empire Waist", "Tiered",
    "Pleated", "Ruched", "Gathered", "Panelled", "Cut-Out", "Sculpted",
    "Contour Fit", "Second-Skin", "Fluid Drape", "Box Pleat"
]

FASHION_DETAILS = [
    "gold hardware", "silver hardware", "contrast stitching", "raw hem",
    "distressed finish", "embellished trim", "pearl accents", "lace panel",
    "mesh overlay", "satin lining", "double-breasted buttons", "side slit",
    "front slit", "back vent", "adjustable straps", "elastic waistband",
    "hidden zipper", "exposed zipper", "button front", "hook-and-eye closure",
    "belted waist", "cinched waist", "pleated front", "cargo pockets",
    "patch pockets", "welt pockets", "ribbed cuffs", "ribbed hem",
    "feather trim", "sequin detail", "beaded detail", "embroidered detail",
    "quilted texture", "padded shoulders", "structured collar",
    "foldover collar", "shawl collar", "notched lapel", "waterfall drape",
    "tie-front", "wrap closure", "ruched sides", "gathered bust",
    "panel stitching", "contrast piping", "sheer sleeves"
]

FASHION_MATERIALS = [
    "cotton", "organic cotton", "linen", "silk", "satin", "velvet",
    "chiffon", "mesh", "lace", "tulle", "modal", "bamboo fiber",
    "cashmere", "wool", "merino wool", "alpaca blend", "faux fur",
    "faux leather", "vegan leather", "denim", "stretch denim",
    "rib knit", "jersey knit", "crepe", "tweed", "bouclé", "suede",
    "poly-blend", "nylon", "spandex", "elastane", "viscose", "rayon",
    "microfiber", "performance fabric", "athletic mesh", "airflow knit",
    "buttery-soft knit", "structured twill", "sateen", "organza"
]

FASHION_VIBES = [
    "quiet luxury", "soft glam", "street luxe", "editorial chic",
    "runway modern", "romantic feminine", "minimalist", "maximalist",
    "clean girl aesthetic", "old money", "new money glam", "city-ready",
    "vacation mode", "resort chic", "evening elegance", "day-to-night",
    "athleisure luxe", "soft power", "bold confidence", "effortless cool",
    "Parisian chic", "LA glow", "NYC edge", "Y2K revival", "retro modern",
    "classic timeless", "sultry night-out", "CEO energy", "influencer edit",
    "content creator ready", "festival glam", "holiday sparkle"
]

ADJECTIVES_FASHION = [
    "liquid", "sculpted", "weightless", "molten",
    "luminous", "tailored", "undone", "sleek",
    "soft-structured", "second-skin", "minimal", "refined",
    "polished", "effortless", "elevated", "clean-lined",
    "architectural", "romantic", "feminine", "bold",
    "striking", "timeless", "modern", "sensual",
    "fluid", "contoured", "silky", "buttery",
    "structured", "airy",
]

# Sensory verbs (movement, texture, presence)
SENSORY_VERBS_FASHION = [
    "skims the body", "catches the light", "frames the silhouette", "softens every line",
    "moves with you", "drifts as you walk", "wraps you in ease", "defines your shape",
    "flows effortlessly", "elevates your presence", "creates quiet drama", "brings softness to structure",
    "adds fluidity to form",
]

# Confidence phrases (brand signature closers)
CONFIDENCE_PHRASES_FASHION = [
    "made for women who lead with presence",
    "built for everyday luxury, not just occasions",
    "designed to feel as good as it looks",
    "created for the woman who refuses to dim down",
    "crafted for confidence in motion",
    "made to elevate your everyday",
    "built for the modern feminine wardrobe",
]

# Fashion moods (editorial tone anchors)
FASHION_MOODS = [
    "soft minimalism", "quiet luxury", "romantic ease",
    "modern femininity", "bold structure", "runway energy",
    "elevated essentials",
]

# Fashion occasions (SEO + editorial)
FASHION_OCCASIONS = [
    "everyday wear", "evening moments",
    "weekend ease", "office polish",
    "date nights", "special events",
    "travel days",
]

# Fashion trends
FASHION_TRENDS = [
    "quiet_luxury", "street_luxe", "runway_minimalism",
    "hyper_femininity", "soft_tailoring", "power_tailoring",
    "liquid_silhouettes", "sculpted_silhouettes", "oversized_proportions",
    "micro_proportions", "clean_lines", "architectural_lines",
    "draped_forms", "structured_forms", "second_skin_fit",
    "relaxed_fit", "athleisure_luxe", "elevated_athletic",
    "sporty_refinement", "editorial_sharp", "editorial_soft",
    "monochrome_dressing", "tonal_layering", "color_blocking",
    "neutral_sculpting", "earth_tone_minimalism", "high_gloss_finish",
    "matte_finish", "satin_shine", "liquid_metallics",
    "soft_metallics", "chrome_sheens", "pearlescent_sheens",
    "sheer_layers", "semi_sheer", "translucent_textures",
    "mesh_moments", "lacework_detailing", "cutout_architecture",
    "strategic_cutouts", "corset_revival", "balletcore",
    "romantic_grunge", "soft_grunge", "dark_romance",
    "femme_modern", "femme_classic", "femme_sculpted",
    "minimal_femme", "maximal_femme", "quiet_femme",
    "editorial_femme", "runway_femme", "street_femme",
    "sleek_modernism", "future_minimalism", "tech_luxe",
    "utility_luxe", "cargo_refined", "pocket_architecture",
    "military_softened", "aviator_revival", "retro_modern",
    "y2k_refined", "y2k_gloss", "y2k_sculpted",
    "coquette_modern", "coquette_dark", "coquette_minimal",
    "barbiecore_refined", "mermaidcore", "goddess_draping",
    "goddess_sculpting", "liquid_draping", "column_silhouettes",
    "hourglass_sculpting", "boxy_silhouettes",
    "cropped_proportions", "elongated_proportions", "maxi_movement",
    "mini_movement", "mid_length_modern", "elevated_basics",
    "premium_basics", "capsule_wardrobe", "editorial_capsule",
    "runway_capsule", "statement_outerwear", "sculptural_outerwear",
    "puffer_elevated", "trench_reimagined", "leather_refined",
    "vegan_leather_modern", "faux_fur_luxe", "feather_detailing",
    "fringe_movement", "beaded_embellishment", "crystal_embellishment",
    "metallic_embellishment", "hardware_focus", "minimal_hardware", "maximal_hardware",
    "chain_detailing", "strap_architecture", "asymmetric_lines",
    "diagonal_cutting", "bias_cutting", "panel_construction",
    "mixed_materials", "texture_play", "tonal_textures",
    "contrast_textures", "elevated_denim", "dark_denim",
    "washed_denim", "structured_denim", "denim_on_denim", "knit_luxe",
    "ribbed_knits", "open_knits", "crochet_modern",
    "cashmere_soft", "wool_blend_modern", "silk_blend_modern",
    "satin_blend_modern", "mesh_blend_modern", "evening_modern",
    "evening_minimal", "evening_sculpted", "evening_liquid",
    "evening_editorial", "day_to_night", "desk_to_dinner",
    "travel_luxe", "resort_luxe", "vacation_minimal",
    "city_modern", "urban_refined", "weekend_elevated",
    "off_duty_luxe", "model_off_duty", "celebrity_off_duty", "runway_inspired",
    "couture_inspired", "archive_revival", "heritage_modern",
    "heritage_minimal", "heritage_sculpted", "couture_sculpted",
    "couture_minimal", "couture_liquid", "couture_modern"
    "quiet_luxury_outfits", "capsule_wardrobe_essentials", "minimalist_outfits",
    "streetwear_outfits", "y2k_outfits", "coquette_aesthetic", "clean_girl_aesthetic",
    "soft_girl_aesthetic", "balletcore_outfits", "barbiecore_outfits",
    "old_money_style", "preppy_aesthetic", "dark_academia_style",
    "light_academia_style", "grunge_aesthetic", "soft_grunge_style",
    "edgy_outfits", "monochrome_outfits", "neutral_outfits",
    "all_black_outfits", "all_white_outfits", "oversized_blazer_trend",
    "wide_leg_pants_trend", "cargo_pants_outfits", "parachute_pants_trend",
    "denim_on_denim", "maxi_skirt_outfits", "mini_skirt_outfits",
    "sheer_trend", "mesh_trend", "cutout_dress_trend",
    "corset_top_trend", "slip_dress_trend", "satin_dress_trend",
    "metallic_outfits", "silver_trend", "gold_trend", "chrome_fashion",
    "red_outfit_trend", "brown_outfit_trend", "olive_green_trend",
    "winter_white_trend", "leather_jacket_outfits", "faux_leather_trend", "puffer_jacket_trend",
    "trench_coat_outfits", "oversized_sweater_outfits", "knit_dress_trend", "ribbed_knit_trend",
    "elevated_basics_trend", "athleisure_outfits", "sporty_chic_outfits",
    "model_off_duty_style", "celebrity_off_duty_style", "airport_outfits", "date_night_outfits",
    "girls_night_outfits", "brunch_outfits", "vacation_outfits", "resort_wear_trend", "beachwear_trend",
    "evening_gown_trend", "wedding_guest_dress_trend", "cocktail_dress_trend", "party_dress_trend", "festival_outfits",
    "concert_outfits", "street_style_trend", "runway_trend", "couture_trend", "editorial_fashion_trend",
    "statement_jewelry_trend", "chunky_boots_trend", "platform_shoes_trend", "ballet_flats_trend",
    "slingback_heels_trend", "loafers_outfits", "sneaker_trend",
    "retro_sneakers_trend", "vintage_fashion_trend", "thrifted_outfits",
    "sustainable_fashion_trend", "eco_friendly_fashion", "vegan_leather_trend",
    "linen_outfits", "silk_outfits", "satin_outfits",
    "mesh_dress_trend", "maxi_dress_trend", "midi_dress_trend",
    "mini_dress_trend","bodycon_dress_trend","oversized_shirt_outfits",
    "button_down_trend","cropped_blazer_trend","cropped_sweater_trend",
    "cropped_jacket_trend","flare_pants_trend", "bootcut_jeans_trend", "baggy_jeans_trend",
    "straight_leg_jeans_trend", "mom_jeans_trend", "90s_fashion_trend",
    "2000s_fashion_trend", "retro_modern_trend", "elevated_denim_trend",
    "dark_denim_trend", "washed_denim_trend", "distressed_denim_trend",
    "embellished_denim_trend", "liquid_curve_femme", "soft_sculpted_minimal", "draped_column_femme", "cinched_modern_silhouette",
    "editorial_drape_architecture", "romantic_bias_draping", "airy_femme_silhouettes", "sleek_contour_lines",
    "soft_hourglass_modern", "goddess_sculpted_drape", "fluid_femme_tailoring", "minimal_curve_refinement",
    "romantic_sculpted_lines", "soft_architectural_femme", "clean_sculpted_minimalism", "editorial_liquid_shape",
    "femme_column_modern", "soft_contour_modern", "draped_femme_sculpt", "liquid_modern_silhouette",
    "satin_liquid_glow", "velvet_depth_modern", "silk_cloud_finish", "matte_soft_sculpt",
    "sheer_femme_layers", "mesh_liquid_modern", "opaline_shimmer", "chrome_diffused_metallics",
    "satin_soft_reflection", "silk_luminous_drape", "velvet_romantic_depth", "mesh_editorial_sculpt",
    "sheer_romantic_modern", "satin_glow_minimal", "silk_soft_architecture", "chrome_soft_refinement",
    "pearlescent_femme_finish", "matte_cloud_minimal", "satin_sculpted_evening", "silk_liquid_minimal",
    "rose_quartz_minimal", "mocha_soft_luxury", "ink_black_editorial", "porcelain_white_clean",
    "blush_glow_femininity", "wine_depth_sculpted", "champagne_soft_luster", "storm_grey_minimal",
    "espresso_deep_modern", "cloud_white_femme", "midnight_soft_sculpt", "rosewater_femme_modern",
    "caramel_warm_minimal", "taupe_soft_architecture", "blush_neutral_modern", "berry_editorial_depth",
    "vanilla_cream_minimal", "smoke_grey_femme", "cocoa_soft_luxury", "ivory_glow_minimal",
    "femme_editorial_minimal", "romantic_soft_power", "sensual_sculpted_modern", "glamour_diffused_modern",
    "evening_femme_sculpt", "daylight_soft_minimal", "runway_femme_liquid", "quiet_femme_strength",
    "romantic_femme_modern", "editorial_femme_sharp", "soft_femme_precision", "glow_femme_minimal",
    "sleek_femme_modern", "evening_femme_liquid", "day_femme_clean", "night_femme_sculpt"
    "romantic_femme_depth", "femme_modern_architecture", "soft_femme_contour", "editorial_femme_liquid",
    "brunch_editorial_soft", "date_night_liquid_femme", "girls_night_glow_modern", "resort_soft_minimal",
    "vacation_liquid_luxe", "city_femme_modern", "off_duty_soft_luxury", "desk_to_dinner_femme",
    "weekend_soft_modern", "travel_femme_minimal", "evening_city_glow", "resort_femme_sculpt",
    "vacation_editorial_soft", "brunch_femme_minimal", "girls_night_sculpted", "date_night_soft_sculpt",
    "city_liquid_minimal", "resort_glow_femme", "evening_soft_architecture", "day_to_night_femme",
    "quiet_femme_editorial", "romantic_clean_girl", "dark_femme_minimal", "soft_grunge_femme_modern",
    "coquette_editorial_modern", "balletcore_soft_luxe", "mermaidcore_glow_femme", "angelic_minimalism",
    "ethereal_femme_modern", "dark_romantic_femme", "soft_gothic_modern", "editorial_coquette_femme",
    "romantic_femme_minimal", "celestial_femme_glow", "dreamcore_femme_modern", "soft_fantasy_minimal",
    "modern_fairytale_femme", "femme_mystique_modern", "editorial_balletcore", "femme_mermaid_liquid",
    "satin_soft_sculpted", "silk_liquid_minimal", "mesh_femme_editorial", "lace_romantic_modern",
    "leather_femme_sculpted", "faux_leather_soft_luxe", "knit_cloud_soft", "denim_modern_refined",
    "lace_femme_architecture", "mesh_sculpted_minimal", "satin_editorial_depth", "silk_femme_precision",
    "leather_modern_minimal", "faux_leather_femme_modern", "knit_sculpted_femme", "denim_soft_modern",
    "lace_soft_sculpt", "mesh_liquid_femme", "satin_glow_femme", "silk_editorial_modern"
]

__all__ = [
    "ADJECTIVES_FASHION",
    "SENSORY_VERBS_FASHION",
    "CONFIDENCE_PHRASES_FASHION",
    "FASHION_MOODS",
    "FASHION_OCCASIONS",
    "FASHION_SILHOUETTES",
    "FASHION_MATERIALS",
    "FASHION_DETAILS",
    "FASHION_VIBES",
    "FASHION_TRENDS",
]