# MVQueen Omniluxe Engine — Master README
Built: February 2026 | Organized: June 2026
Status: Architecturally complete. Ready for production deployment.
Location in OS: 15_Scripts_And_Code/MVQueen_Engine/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT THIS ENGINE DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automates Shopify product content at catalog scale:
→ Generates product descriptions using 10 editorial personas
→ Creates SEO titles, meta descriptions, and focus keywords
→ Assigns 13 custom metafields per product
→ Builds tag sets (category + type + benefits + vibes + SEO)
→ Maps products to Shopify collections
→ Exports CSV ready for Shopify bulk import
→ Deterministic output — same input = same output every time


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FILE MAP (READ IN ORDER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
01_engine_skeleton     → Master architecture blueprint — start here
02_codes1              → config.py, price_logic.py, deterministic.py, brand_banks.py (core layer)
03_codes2              → PERSONA_CONFIG (10 personas), Shopify API, metafield_engine.py
04_codes3              → csv_loader.py, processor.py, main.py, fashion vocab, tag/category detection
05_codes4              → Collections-as-Metafields architecture, editorial frames v1 (160 templates)
06_codes5              → Full vocab population: LUXURY_ADJECTIVES, SENSORY_VERBS, BUSINESS_TIERS
07_codes6              → SENSORY_VERBS compound expansion (micro-glows, feather-glows, veil-glows...)
08_codes7              → EDITORIAL_FRAMES v2 expansion (300+ total copy templates)
09_codes8              → Detection layer: category/type detection, Tag Engine, deterministic imports
10_Meta_update         → Shopify metafield flattening, PlatformConfig, control panel settings
11_codes9              → Official engine documentation / user manual (hand to any developer)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE 10 EDITORIAL PERSONAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1.  MVQueen Core          — Confident, aspirational, inclusive luxury
2.  MISS.QUEEN            — Youthful, playful, soft-glam (sister brand)
3.  Victoria Soft Power   — Quiet authority, old money tone
4.  Sephora Precision     — Clinical, ingredient-forward
5.  Runway Modern         — Editorial, high-fashion voice
6.  Clinical Chic         — Skincare expert authority
7.  Soft Luxury           — Sensory, tactile, deeply feminine
8.  Glow Maestro          — Radiance-focused, beauty editorial
9.  Elegant Authority     — Prestige positioning, aspirational
10. Street Luxe Femme     — Urban, confident, culturally aware


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHOPIFY METAFIELDS GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Namespace: custom
Fields: emotional_axes, seo_keywords, care_instructions, shipping_note,
        size_guide, trust_badges, short_description, focus_keyword,
        faq, ingredients, how_to_use, highlights, badge


Full schema: see 09_Shopify_Systems/Metafields_Schema


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOCABULARY BANKS BUILT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LUXURY_ADJECTIVES        — 80+ premium descriptors
SENSORY_VERBS            — 200+ including compound forms (micro-glows, feather-glows)
CONFIDENCE_PHRASES       — 60+ empowerment phrases
BUSINESS_TIERS           — 80+ product tier labels
FASHION_SILHOUETTES      — 50 silhouette types
FASHION_DETAILS          — 48 design detail descriptors
FASHION_MATERIALS        — 42 material descriptors
FASHION_VIBES            — 32 aesthetic vibes (quiet luxury, old money, etc.)
EDITORIAL_FRAMES         — 300+ copy template strings
SEO_PRIMARY              — 20 primary keyword categories
SEO_SECONDARY            — 20 secondary keyword modifiers


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRICING TIERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Standard: 28% margin
Premium:  35% margin
Luxury:   42% margin


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TO RUN THE ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
See 11_codes9 (official user manual) for full execution instructions.
Original build environment: Android (Pydroid3 / Termux)
Recommended production environment: Python 3.9+ on Mac/PC or cloud runner


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CROSS-REFERENCES IN OS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Personas extracted to:    10_AI_Systems/MVQUEEN_Persona_Config.md
Editorial frames ref:     06_Tone_And_Voice/Editorial_Frames_Library.md
Sensory vocab ref:        06_Tone_And_Voice/Brand_Vocabulary_Banks.md
Metafield schema:         09_Shopify_Systems/Metafields_Schema.md
Architecture blueprint:   35_System_Blueprints/MVQueen_Engine_Blueprint.md