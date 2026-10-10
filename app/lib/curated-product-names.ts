// Product-by-product naming decisions governed by the two naming guides in
// 04_Products, the vocabulary banks, and Product_Description_Voice.md.
// An ID alone never freezes a name: the source identity must still match.
// The source title keeps category and palette decisions independent of poetry.
export type NamingRegister = "evocative" | "descriptive-poetic" | "identity-led";
export type CuratedProductName = {
  productId: string;
  brand: "mvqueen" | "miss-princess";
  register: NamingRegister;
  title: string;
  opening: string;
  sourceTitle: string;
  sourceAliases: readonly string[];
};

export const CURATED_PRODUCT_NAMES: readonly CuratedProductName[] = [
  {
    "productId": "gid://shopify/Product/9087726584006",
    "brand": "miss-princess",
    "register": "identity-led",
    "title": "Play Date Ruched Sports Bra & Shorts Set",
    "opening": "Movement belongs in your plans.",
    "sourceTitle": "Easy Ruched Sports Bra And High-Waisted Shorts Active Set",
    "sourceAliases": [
      "Easy Ruched Sports Bra And High-Waisted Shorts Active Set",
      "Ruched Sports Bra And High-Waisted Shorts Active Set",
      "ruched sports bra and high-waisted shorts active set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100000755910",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Two Hearts Crystal Anklet",
    "opening": "A small detail with a little meaning.",
    "sourceTitle": "Deliberate Crystal Double-Heart Anklet",
    "sourceAliases": [
      "Deliberate Crystal Double-Heart Anklet",
      "Crystal Double Heart Bracelet Love Barefoot Chain Bling Ankle Anklet",
      "crystal double heart bracelet love barefoot chain bling ankle anklet",
      "crystal double-heart anklet"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100059869382",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "True North Zircon Star Pendant Necklace",
    "opening": "Let one detail lead the look.",
    "sourceTitle": "Composed Stainless Steel Zircon Star Pendant Necklace",
    "sourceAliases": [
      "Composed Stainless Steel Zircon Star Pendant Necklace",
      "Stainless Steel Zircon Star Pendant Necklace",
      "stainless steel zircon star pendant necklace"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100060033222",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The In Motion Zip-Up Training Jumpsuit",
    "opening": "For the part of your day that moves.",
    "sourceTitle": "Elevated Long-Sleeve Zip-Up Training Jumpsuit",
    "sourceAliases": [
      "Elevated Long-Sleeve Zip-Up Training Jumpsuit",
      "Long Sleeve Outdoor Sports Workout Clothes Zipper Training Jumpsuit",
      "long sleeve outdoor sports workout clothes zipper training jumpsuit",
      "long-sleeve zip-up training jumpsuit"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061081798",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Fritillary Reverie Gold-Plated Steel Bracelet",
    "opening": "Your finishing detail deserves its own moment.",
    "sourceTitle": "Curated Stainless Steel Fritillary Bracelet 18K Gold Plating",
    "sourceAliases": [
      "Curated Stainless Steel Fritillary Bracelet 18K Gold Plating",
      "Stainless Steel Fritillary Bracelet 18K Gold Plating",
      "stainless steel fritillary bracelet 18k gold plating"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061114566",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Daily Detail Rechargeable Hair Removal Device",
    "opening": "Make a little room for your own routine.",
    "sourceTitle": "Elevated Rechargeable Ladies Hair Removal Device",
    "sourceAliases": [
      "Elevated Rechargeable Ladies Hair Removal Device",
      "Rechargeable Ladies Hair Removal Device",
      "rechargeable ladies hair removal device"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061147334",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Second Chapter Long-Sleeve Turtleneck Top",
    "opening": "A new chapter in your everyday wardrobe.",
    "sourceTitle": "Effortless Slim Long-Sleeve Turtleneck Top",
    "sourceAliases": [
      "Effortless Slim Long-Sleeve Turtleneck Top",
      "Y2k Slim Turtleneck T-Shirt Casual Long-Sleeved Pullover Tight Top",
      "y2k slim turtleneck t-shirt casual long-sleeved pullover tight top",
      "slim long-sleeve turtleneck top"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061180102",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Open Horizon Backless Yoga Jumpsuit",
    "opening": "Leave room for movement.",
    "sourceTitle": "Effortless Open-Back Yoga Jumpsuit",
    "sourceAliases": [
      "Effortless Open-Back Yoga Jumpsuit",
      "Hollow Beauty Back Yoga Clothes Dance Sports Jumpsuit",
      "hollow beauty back yoga clothes dance sports jumpsuit",
      "open-back yoga jumpsuit"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061212870",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Off-Duty Fleece Hooded Sportswear Set",
    "opening": "The hours between plans deserve a look.",
    "sourceTitle": "Polished Fleece-Lined Hooded Sportswear Set",
    "sourceAliases": [
      "Polished Fleece-Lined Hooded Sportswear Set",
      "Women's Fleece-Lined Hooded Sportswear Suit",
      "women's fleece-lined hooded sportswear suit",
      "fleece-lined hooded sportswear set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061245638",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Denim After Dark Sequin Top & Wide-Leg Pants Set",
    "opening": "Give the evening its own direction.",
    "sourceTitle": "Timeless Sequined Denim Tube Top And Wide-Leg Pants Set",
    "sourceAliases": [
      "Timeless Sequined Denim Tube Top And Wide-Leg Pants Set",
      "Denim Sequined Tube Top Wide Leg Pants Suit",
      "denim sequined tube top wide leg pants suit",
      "sequined denim tube top and wide-leg pants set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061278406",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Celestial Edit Gold-Plated 10-Piece Ring Set",
    "opening": "Your ring stack, in your own order.",
    "sourceTitle": "Intentional Gold-Plated Star And Moon 10-Piece Ring Set",
    "sourceAliases": [
      "Intentional Gold-Plated Star And Moon 10-Piece Ring Set",
      "Gold-Plated Bohemian Star Moon Love Pearl Leaf 10-Piece Ring",
      "gold-plated bohemian star moon love pearl leaf 10-piece ring",
      "gold-plated star and moon 10-piece ring set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061343942",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Arrival Plus Size Dress",
    "opening": "Dress for the woman who has already arrived.",
    "sourceTitle": "Understated Women's Solid Color Plus Size Dress",
    "sourceAliases": [
      "Understated Women's Solid Color Plus Size Dress",
      "Women's Solid Color Plus Size Dress",
      "women's solid color plus size dress"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061376710",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Morning Practice Moisturizing Skin Cream",
    "opening": "Begin with a moment that is yours.",
    "sourceTitle": "Elegant Moisturizing Skin Cream",
    "sourceAliases": [
      "Elegant Moisturizing Skin Cream",
      "Natural Transparent Skin Rejuvenation Moisturizing Beauty Cream",
      "natural transparent skin rejuvenation moisturizing beauty cream",
      "moisturizing skin cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061442246",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Crystal Overture Long Press-On Nails",
    "opening": "Let your fingertips make the entrance.",
    "sourceTitle": "Elegant Long Crystal Press-On Nails",
    "sourceAliases": [
      "Elegant Long Crystal Press-On Nails",
      "Long Crystal Press-On Nails",
      "long crystal press-on nails"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061507782",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Dew Point Snail Mucin Facial Serum",
    "opening": "A place for hydration in your daily edit.",
    "sourceTitle": "Intentional Snail Mucin Hydrating Serum",
    "sourceAliases": [
      "Intentional Snail Mucin Hydrating Serum",
      "Snail Mucin Hydrating Serum",
      "snail mucin hydrating serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061671622",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Golden Pause Peptide & Propolis Serum",
    "opening": "Take a moment before the day begins.",
    "sourceTitle": "Elegant Peptide Propolis Renewal Serum",
    "sourceAliases": [
      "Elegant Peptide Propolis Renewal Serum",
      "Peptide Propolis Renewal Serum",
      "peptide propolis renewal serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061704390",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Unhurried Flared Yoga Pants",
    "opening": "Set your own pace.",
    "sourceTitle": "Refined Elastic High Waist Slightly Flared Yoga Pants",
    "sourceAliases": [
      "Refined Elastic High Waist Slightly Flared Yoga Pants",
      "Elastic High Waist Slightly Flared Yoga Pants",
      "elastic high waist slightly flared yoga pants"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061769926",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Green Room Avocado Body Scrub",
    "opening": "Give your bathing routine a new scene.",
    "sourceTitle": "Intentional Avocado Ice Cream Body Scrub",
    "sourceAliases": [
      "Intentional Avocado Ice Cream Body Scrub",
      "Avocado Ice Cream Body Scrub",
      "avocado ice cream body scrub"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061835462",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Lotion — An Hour Apart",
    "opening": "An invitation to take your time.",
    "sourceTitle": "Deliberate Ultra-Rich Body Lotion",
    "sourceAliases": [
      "Deliberate Ultra-Rich Body Lotion",
      "Body Hydrate Glass Skin Ultra-Rich Lotion",
      "body hydrate glass skin ultra-rich lotion",
      "ultra-rich body lotion"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061900998",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Comfort Chapter Moisturizing Skin Cream",
    "opening": "Return to a routine that feels like yours.",
    "sourceTitle": "Curated Skin Moisturizing Repair Cream",
    "sourceAliases": [
      "Curated Skin Moisturizing Repair Cream",
      "Skin Moisturizing Repair Cream",
      "skin moisturizing repair cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100061966534",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Shea Interlude Face & Body Scrub",
    "opening": "Make space between one part of the day and the next.",
    "sourceTitle": "Intentional Shea Butter Facial Body Scrub Cream",
    "sourceAliases": [
      "Intentional Shea Butter Facial Body Scrub Cream",
      "Shea Butter Facial Body Scrub Cream",
      "shea butter facial body scrub cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062326982",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Ginger Prelude Spray",
    "opening": "Let your routine begin on your terms.",
    "sourceTitle": "Intentional Ginger Spray",
    "sourceAliases": [
      "Intentional Ginger Spray",
      "Ginger Spray",
      "ginger spray"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062392518",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Watermelon Reverie Body Cream",
    "opening": "A small escape within the everyday.",
    "sourceTitle": "Composed Watermelon Body Cream",
    "sourceAliases": [
      "Composed Watermelon Body Cream",
      "Watermelon Body Cream",
      "watermelon body cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062425286",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Oil — A Moment Kept",
    "opening": "Keep a little of the day for yourself.",
    "sourceTitle": "Elegant Nourishing Body Oil",
    "sourceAliases": [
      "Elegant Nourishing Body Oil",
      "Body Skin Nourishing And Moisturizing Treatment Oil",
      "body skin nourishing and moisturizing treatment oil",
      "nourishing body oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062458054",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Clear Intent Salicylic Acid Body Wash",
    "opening": "A considered place in your bathing edit.",
    "sourceTitle": "Curated Salicylic Acid Body Wash",
    "sourceAliases": [
      "Curated Salicylic Acid Body Wash",
      "Salicylic Acid Body Wash",
      "salicylic acid body wash"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062490822",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Waterline Hyaluronic Acid Facial Serum",
    "opening": "Bring hydration into the daily conversation.",
    "sourceTitle": "Polished Super Hyaluronic Acid Serum",
    "sourceAliases": [
      "Polished Super Hyaluronic Acid Serum",
      "Super Hyaluronic Acid Serum",
      "super hyaluronic acid serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062556358",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Dewy Dreams Moisturizing Toner",
    "opening": "A little daydream in your daily lineup.",
    "sourceTitle": "Lighthearted Moisturizing Toner",
    "sourceAliases": [
      "Lighthearted Moisturizing Toner",
      "Moisturizing Toner",
      "moisturizing toner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062589126",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Discovery Edit Mystery Beauty Box",
    "opening": "Leave room to discover something new.",
    "sourceTitle": "Timeless Mystery Beauty Boxes",
    "sourceAliases": [
      "Timeless Mystery Beauty Boxes",
      "Mystery Beauty Boxes",
      "mystery beauty boxes"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062621894",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Vitamin E Body Oil — Daily Grace",
    "opening": "Give an everyday step a little attention.",
    "sourceTitle": "Understated Vitamin E Body Oil",
    "sourceAliases": [
      "Understated Vitamin E Body Oil",
      "Vitamin E Body Oil",
      "vitamin e body oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062687430",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "New Perspective Resurfacing Body Serum",
    "opening": "A considered addition to your body care routine.",
    "sourceTitle": "Curated Resurfacing Body Serum",
    "sourceAliases": [
      "Curated Resurfacing Body Serum",
      "Resurfacing Body Serum",
      "resurfacing body serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062720198",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Composed Canvas Waterproof Concealer",
    "opening": "Your makeup, with your own point of view.",
    "sourceTitle": "Polished Moisturizing Waterproof Concealer",
    "sourceAliases": [
      "Polished Moisturizing Waterproof Concealer",
      "Moisturizing Oil Controlling Skin Brightening Waterproof And Concealer",
      "moisturizing oil controlling skin brightening waterproof and concealer",
      "moisturizing waterproof concealer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062785734",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Coconut Interval Hand Cream",
    "opening": "Make the in-between moments your own.",
    "sourceTitle": "Composed Coconut Hand Cream",
    "sourceAliases": [
      "Composed Coconut Hand Cream",
      "Coconut Hand Cream",
      "coconut hand cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062851270",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Oil — The Care Hour",
    "opening": "Set aside an hour, or just a moment.",
    "sourceTitle": "Deliberate Hair Care Body Oil 60ml",
    "sourceAliases": [
      "Deliberate Hair Care Body Oil 60ml",
      "Hair Care Body Oil 60ml",
      "hair care body oil 60ml"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062916806",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Sleek Sequence Hair Mask",
    "opening": "Let hair care take its place in your routine.",
    "sourceTitle": "Elevated Smooth And Sleek Hair Mask",
    "sourceAliases": [
      "Elevated Smooth And Sleek Hair Mask",
      "Smooth And Sleek Hair Mask",
      "smooth and sleek hair mask"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062949574",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Honey & Ceramide Toner — First Light",
    "opening": "A first step toward a day of your own.",
    "sourceTitle": "Restrained Honey Ceramide Toner",
    "sourceAliases": [
      "Restrained Honey Ceramide Toner",
      "Honey Ceramide Toner",
      "honey ceramide toner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100062982342",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Cloud Break Protein Hair Mask Spray",
    "opening": "A little pause before your next plan.",
    "sourceTitle": "Easy Protein Hair Mask Spray",
    "sourceAliases": [
      "Easy Protein Hair Mask Spray",
      "Protein Soft Nourishing Hair Mask Hot Dyeing Fluffy Spray",
      "protein soft nourishing hair mask hot dyeing fluffy spray",
      "protein hair mask spray"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063015110",
    "brand": "miss-princess",
    "register": "descriptive-poetic",
    "title": "Hair Mask Conditioner — A Fresh Chapter",
    "opening": "Give your hair routine a new chapter.",
    "sourceTitle": "Sweet Deep Repair Hair Mask Conditioner",
    "sourceAliases": [
      "Sweet Deep Repair Hair Mask Conditioner",
      "Deep Repair Hair Mask Nutritional Softening Conditioner",
      "deep repair hair mask nutritional softening conditioner",
      "deep repair hair mask conditioner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063047878",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Still Water Bath Oil",
    "opening": "Let the day settle here.",
    "sourceTitle": "Timeless Bath Care Oil",
    "sourceAliases": [
      "Timeless Bath Care Oil",
      "Care Bath Oil",
      "care bath oil",
      "bath care oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063113414",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Personal Edit Hair Removal Tool",
    "opening": "Choose how your routine comes together.",
    "sourceTitle": "Polished Hair Removal Tool With Rechargeable And Battery Options",
    "sourceAliases": [
      "Polished Hair Removal Tool With Rechargeable And Battery Options",
      "Women's Painless Hair Remover Tools Rechargeable And Battery Model",
      "women's painless hair remover tools rechargeable and battery model",
      "hair removal tool with rechargeable and battery options"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063146182",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Facial Roller — The Golden Interval",
    "opening": "A moment between the mirror and the day.",
    "sourceTitle": "Deliberate 24K Gold Vibrating Facial Roller",
    "sourceAliases": [
      "Deliberate 24K Gold Vibrating Facial Roller",
      "Face 24K Gold Vibration Pulse Beauty Bar Facial Roller",
      "face 24k gold vibration pulse beauty bar facial roller",
      "24k gold vibrating facial roller"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063211718",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Milk & Honey Hand Wax — Sweet Pause",
    "opening": "Keep a little sweetness in the schedule.",
    "sourceTitle": "Easy Milk And Honey Hand Wax",
    "sourceAliases": [
      "Easy Milk And Honey Hand Wax",
      "Milk Honey Nourish Hand Wax Moisturizing Hydrating Skin Care",
      "milk honey nourish hand wax moisturizing hydrating skin care",
      "milk and honey hand wax"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063244486",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Moroccan Herbal Hair Serum — Rooted",
    "opening": "Give this step a considered place.",
    "sourceTitle": "Deliberate Moroccan Herbal Hair Treatment Serum",
    "sourceAliases": [
      "Deliberate Moroccan Herbal Hair Treatment Serum",
      "Moroccan Herbal Hair Treatment Serum",
      "moroccan herbal hair treatment serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063277254",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Everyday Choice Multifunctional Lady Shaver",
    "opening": "Your everyday choices belong to you.",
    "sourceTitle": "Refined Multifunctional Lady Shaver",
    "sourceAliases": [
      "Refined Multifunctional Lady Shaver",
      "Multifunctional Lady Shaver",
      "multifunctional lady shaver"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063310022",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Wood Paddle Hair Brush — In Good Order",
    "opening": "Put a little intention into the familiar.",
    "sourceTitle": "Harmonious Wood Paddle Cushion Hair Brush",
    "sourceAliases": [
      "Harmonious Wood Paddle Cushion Hair Brush",
      "Wood Comb Professional Healthy Paddle Cushion Massage Brush",
      "wood comb professional healthy paddle cushion massage brush",
      "wood paddle cushion hair brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063342790",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Shea Butter Massage Cream — Time to Yourself",
    "opening": "Make time for a moment of your own.",
    "sourceTitle": "Understated Shea Butter Massage Cream",
    "sourceAliases": [
      "Understated Shea Butter Massage Cream",
      "Shea Butter Massage Cream",
      "shea butter massage cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063408326",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Lavender Stillness Essential Oil",
    "opening": "Let the atmosphere take its own shape.",
    "sourceTitle": "Elevated Essential Oil",
    "sourceAliases": [
      "Elevated Essential Oil",
      "Essential Oil",
      "essential oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063539398",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Everyday Face BB Cream Foundation",
    "opening": "Make your daily makeup your own.",
    "sourceTitle": "Refined BB Cream Foundation",
    "sourceAliases": [
      "Refined BB Cream Foundation",
      "BB Cream Foundation",
      "bb cream foundation"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063736006",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Clean Slate Hair Removal Cream",
    "opening": "Choose the next step in your routine.",
    "sourceTitle": "Timeless Hair Removal Cream",
    "sourceAliases": [
      "Timeless Hair Removal Cream",
      "Hair Removal Cream",
      "hair removal cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063867078",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Fine Grain Skincare — A Small Consideration",
    "opening": "The small considerations have their place.",
    "sourceTitle": "Harmonious Fine-Grain Skincare",
    "sourceAliases": [
      "Harmonious Fine-Grain Skincare",
      "Light Fine Grain Skin Care Products",
      "light fine grain skin care products",
      "fine-grain skincare"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063932614",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Daylight Mood Sunless Body Lotion",
    "opening": "Bring a little daylight to your body care edit.",
    "sourceTitle": "Intentional Sunless Body Lotion 30ml",
    "sourceAliases": [
      "Intentional Sunless Body Lotion 30ml",
      "The Black Oil 30ml Sunless Wheat Color Nutrition Body Lotion",
      "the black oil 30ml sunless wheat color nutrition body lotion",
      "sunless body lotion 30ml"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100063998150",
    "brand": "miss-princess",
    "register": "descriptive-poetic",
    "title": "Easy Company Elastin Leave-In Conditioner",
    "opening": "Keep a little ease in your hair routine.",
    "sourceTitle": "Sweet Elastin Leave-In Conditioner",
    "sourceAliases": [
      "Sweet Elastin Leave-In Conditioner",
      "Leave-In Conditioner Elastin To Repair Frizz",
      "leave-in conditioner elastin to repair frizz",
      "elastin leave-in conditioner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064194758",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Satin Hour Hair Oil",
    "opening": "Give the last step its own moment.",
    "sourceTitle": "Understated Silky Hair Essential Oil",
    "sourceAliases": [
      "Understated Silky Hair Essential Oil",
      "Silky Hair Essential Oil",
      "silky hair essential oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064293062",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Skin Lotion Cream — A Gentle Interval",
    "opening": "Leave a little space in the day for care.",
    "sourceTitle": "Restrained Skin Brightening Anti Drying Moisturizing Lotion Cream",
    "sourceAliases": [
      "Restrained Skin Brightening Anti Drying Moisturizing Lotion Cream",
      "Skin Brightening Anti Drying Moisturizing Lotion Cream",
      "skin brightening anti drying moisturizing lotion cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064424134",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Amethyst Poise Facial Massage Roller",
    "opening": "Give your dressing table a considered detail.",
    "sourceTitle": "Intentional Amethyst Roller Single And Double-Headed Beauty Jade Massager",
    "sourceAliases": [
      "Intentional Amethyst Roller Single And Double-Headed Beauty Jade Massager",
      "Amethyst Roller Single And Double-Headed Beauty Jade Massager",
      "amethyst roller single and double-headed beauty jade massager"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064456902",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Rose Room Petal Essential Oil",
    "opening": "Let the rose have its own room.",
    "sourceTitle": "Intentional Rose Petal Essential Oil 100Ml Aromatherapy Moisturizing",
    "sourceAliases": [
      "Intentional Rose Petal Essential Oil 100Ml Aromatherapy Moisturizing",
      "Rose Petal Essential Oil 100Ml Aromatherapy Moisturizing",
      "rose petal essential oil 100ml aromatherapy moisturizing"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064587974",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Cream — The Small Hours",
    "opening": "Care can have its own quiet hour.",
    "sourceTitle": "Composed Body Cream 40g",
    "sourceAliases": [
      "Composed Body Cream 40g",
      "Body Cream 40g",
      "body cream 40g"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100064817350",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Evening Exhale Body Massage Cream",
    "opening": "A place to pause when the day is done.",
    "sourceTitle": "Composed Body Massage Cream",
    "sourceAliases": [
      "Composed Body Massage Cream",
      "Big Skin And Cream Body Massage Care Creams",
      "big skin and cream body massage care creams",
      "body massage cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100065013958",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Cream — A Considered Pause",
    "opening": "A small pause, chosen with intention.",
    "sourceTitle": "Elegant Nourishing Body Cream 40ml",
    "sourceAliases": [
      "Elegant Nourishing Body Cream 40ml",
      "Universal 40ml Moisturizing Nourishing Body Cream",
      "universal 40ml moisturizing nourishing body cream",
      "nourishing body cream 40ml"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100065341638",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Fresh Perspective Face & Body Scrub",
    "opening": "Make this part of a routine you return to.",
    "sourceTitle": "Understated Exfoliating Face And Body Scrub",
    "sourceAliases": [
      "Understated Exfoliating Face And Body Scrub",
      "Exfoliating Dead Skin Cleansing Moisturizing Face Body Scrub",
      "exfoliating dead skin cleansing moisturizing face body scrub",
      "exfoliating face and body scrub"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100065505478",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Golden Rinse Body Wash",
    "opening": "Give your bathing edit a little atmosphere.",
    "sourceTitle": "Curated 24k Clean Foam Gold Body Wash",
    "sourceAliases": [
      "Curated 24k Clean Foam Gold Body Wash",
      "24k Clean Foam Gold Body Wash",
      "24k clean foam gold body wash"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100065702086",
    "brand": "miss-princess",
    "register": "identity-led",
    "title": "Little Finishing Touch Baby Hair Styling Gel",
    "opening": "Let the little details have their say.",
    "sourceTitle": "Playful Baby Hair Styling Gel",
    "sourceAliases": [
      "Playful Baby Hair Styling Gel",
      "Baby Hair Gel Fluffy Fixed And Anti Manic",
      "baby hair gel fluffy fixed and anti manic",
      "baby hair styling gel"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100065996998",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Petal Dream Perfume",
    "opening": "A daydream with a place on your dressing table.",
    "sourceTitle": "Petal Dream Perfume",
    "sourceAliases": [
      "Petal Dream Perfume",
      "Osmanthus Peony Pomegranate Fragrance Crystal Diamond Series Perfume",
      "osmanthus peony pomegranate fragrance crystal diamond series perfume",
      "petal dream perfume"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066226374",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Quiet Aura Fragranced Skincare Oil",
    "opening": "Bring your own atmosphere to the routine.",
    "sourceTitle": "Curated Moisturizing Fragranced Skincare Oil",
    "sourceAliases": [
      "Curated Moisturizing Fragranced Skincare Oil",
      "Deep Moisturizing Anti-Chapping Fragrance Brightening Skin Care Oil",
      "deep moisturizing anti-chapping fragrance brightening skin care oil",
      "moisturizing fragranced skincare oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066324678",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Ember Veil Dragon Blood Face Serum",
    "opening": "Let one step have its own identity.",
    "sourceTitle": "Restrained Dragon Blood Anti-Aging Face Serum",
    "sourceAliases": [
      "Restrained Dragon Blood Anti-Aging Face Serum",
      "Dragon Blood Anti-Aging Face Serum",
      "dragon blood anti-aging face serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066554054",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Face Cream — The Daily Return",
    "opening": "For a routine you make your own.",
    "sourceTitle": "Deliberate Moisturizer Face Cream",
    "sourceAliases": [
      "Deliberate Moisturizer Face Cream",
      "Moisturizer Face Cream",
      "moisturizer face cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066619590",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Turmeric Dawn Face Cream",
    "opening": "Begin the care hour with intention.",
    "sourceTitle": "Elevated Turmeric Care Face Cream",
    "sourceAliases": [
      "Elevated Turmeric Care Face Cream",
      "Turmeric Care Face Cream",
      "turmeric care face cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066783430",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Essential Hair Oil — A Last Word",
    "opening": "Give the last step a considered place.",
    "sourceTitle": "Timeless Essential Hair Oil",
    "sourceAliases": [
      "Timeless Essential Hair Oil",
      "Essential Hair Oil",
      "essential hair oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100066881734",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Body Butter — Warm Embrace",
    "opening": "Make room for a body care moment.",
    "sourceTitle": "Timeless Body Butter",
    "sourceAliases": [
      "Timeless Body Butter",
      "Body Butter",
      "body butter"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067012806",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Day by Day Moisturizer Cream",
    "opening": "Care has a place in the everyday.",
    "sourceTitle": "Composed Moisturizer Cream",
    "sourceAliases": [
      "Composed Moisturizer Cream",
      "Moisturizer Cream",
      "moisturizer cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067209414",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Prelude Mousse Toner",
    "opening": "Before the makeup, a moment of preparation.",
    "sourceTitle": "Effortless Pre Makeup Mousse Toner",
    "sourceAliases": [
      "Effortless Pre Makeup Mousse Toner",
      "Pre Makeup Mousse Toner",
      "pre makeup mousse toner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067340486",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Eye Cream — The Quiet Detail",
    "opening": "The little details deserve your attention.",
    "sourceTitle": "Elevated Eye Care Cream",
    "sourceAliases": [
      "Elevated Eye Care Cream",
      "Eye Care Cream",
      "eye care cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067406022",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Snail Secretion Moisturizer — Morning Dew",
    "opening": "A considered start to your skincare edit.",
    "sourceTitle": "Effortless Snail Secretion Moisturizer",
    "sourceAliases": [
      "Effortless Snail Secretion Moisturizer",
      "Snail Secretion Moisturizer Rejuvenates Skin",
      "snail secretion moisturizer rejuvenates skin",
      "snail secretion moisturizer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067635398",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Ritual Pause Electric Cupping Massager",
    "opening": "Keep a place for your own pace.",
    "sourceTitle": "Timeless Electric Vacuum Cupping Massager For Body Suction Cup Gua Sha Massage",
    "sourceAliases": [
      "Timeless Electric Vacuum Cupping Massager For Body Suction Cup Gua Sha Massage",
      "Electric Vacuum Cupping Massager For Body Suction Cup Gua Sha Massage",
      "electric vacuum cupping massager for body suction cup gua sha massage"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067733702",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Protein Shampoo — Back to the Beginning",
    "opening": "Give wash day a new beginning.",
    "sourceTitle": "Precise Protein Rich Shampoo",
    "sourceAliases": [
      "Precise Protein Rich Shampoo",
      "Protein Rich Shampoo",
      "protein rich shampoo"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067864774",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The First Impression Liquid Foundation",
    "opening": "Begin your makeup with your own intention.",
    "sourceTitle": "Polished Concealer Liquid Foundation",
    "sourceAliases": [
      "Polished Concealer Liquid Foundation",
      "Concealer Liquid Foundation",
      "concealer liquid foundation"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100067963078",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The At-Home Edit 23-Piece Waxing Kit",
    "opening": "Bring the care hour into your own space.",
    "sourceTitle": "Intentional 23-Piece Waxing Kit With Warmer And Wax Beads",
    "sourceAliases": [
      "Intentional 23-Piece Waxing Kit With Warmer And Wax Beads",
      "Waxing Kit 23 Items Hair Removal Wax With Warmer Beads Etc",
      "waxing kit 23 items hair removal wax with warmer beads etc",
      "23-piece waxing kit with warmer and wax beads"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068028614",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Scrub — A Change of Scene",
    "opening": "Make the bathing routine a moment in itself.",
    "sourceTitle": "Precise Body Scrub",
    "sourceAliases": [
      "Precise Body Scrub",
      "Body Scrub",
      "body scrub"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068061382",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Face Cream — Your Daily Constant",
    "opening": "An everyday step with a place of its own.",
    "sourceTitle": "Refined Face Cream",
    "sourceAliases": [
      "Refined Face Cream",
      "Face Cream",
      "face cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068126918",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Gold Dusk Bronzing Serum",
    "opening": "Let your makeup take an evening direction.",
    "sourceTitle": "Elegant Bronzing Serum",
    "sourceAliases": [
      "Elegant Bronzing Serum",
      "Bronzing Serum",
      "bronzing serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068192454",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Ultra-Rich Body Lotion — The Evening Return",
    "opening": "A body care moment at the end of the day.",
    "sourceTitle": "Precise Ultra-Rich Body Lotion",
    "sourceAliases": [
      "Precise Ultra-Rich Body Lotion",
      "Ultra-Rich Body Lotion",
      "body hydrate glass skin ultra-rich lotion",
      "ultra-rich body lotion"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068225222",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Care Oil — A Finishing Note",
    "opening": "Give your hair edit a final note.",
    "sourceTitle": "Precise Hair Care Oil",
    "sourceAliases": [
      "Precise Hair Care Oil",
      "Hair Care Oil",
      "hair care oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068290758",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Skincare Wardrobe Box",
    "opening": "Build a skincare edit in your own way.",
    "sourceTitle": "Elegant Skincare Box",
    "sourceAliases": [
      "Elegant Skincare Box",
      "Skincare Box",
      "skincare box"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068323526",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "After Hours Night Cream",
    "opening": "Keep a little of the evening for yourself.",
    "sourceTitle": "Harmonious Night Sleep Cream",
    "sourceAliases": [
      "Harmonious Night Sleep Cream",
      "Night Sleep Cream",
      "night sleep cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068356294",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Still Evening Perfume",
    "opening": "An atmosphere for the hours you keep.",
    "sourceTitle": "Still Evening Rose Forest Perfume",
    "sourceAliases": [
      "Still Evening Rose Forest Perfume",
      "Rose Forest Perfume For Women Lasting",
      "rose forest perfume for women lasting",
      "still evening rose forest perfume"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068421830",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Soft Midnight Perfume Kit",
    "opening": "Let the evening carry its own signature.",
    "sourceTitle": "Soft Midnight Perfume Kit",
    "sourceAliases": [
      "Soft Midnight Perfume Kit",
      "Perfume Kit Women's Long-Lasting Light Girly Heart",
      "perfume kit women's long-lasting light girly heart",
      "soft midnight perfume kit"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068487366",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Herbal Haircare Solution — Inner Circle",
    "opening": "A considered addition to the hair care lineup.",
    "sourceTitle": "Composed Herbal Haircare Solution",
    "sourceAliases": [
      "Composed Herbal Haircare Solution",
      "Herbal Hair Care Solution",
      "herbal hair care solution",
      "herbal haircare solution"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068585670",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Peach Daydream Body Scrub",
    "opening": "A little daydream for the bath shelf.",
    "sourceTitle": "Clean Peach Moisturizing Body Scrub Cream",
    "sourceAliases": [
      "Clean Peach Moisturizing Body Scrub Cream",
      "Peach Moisturizing Body Scrub Cream",
      "peach moisturizing body scrub cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068618438",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Soft Spell Perfume",
    "opening": "Give your fragrance edit a little play.",
    "sourceTitle": "Soft Spell Floral And Fruity Perfume 100ml",
    "sourceAliases": [
      "Soft Spell Floral And Fruity Perfume 100ml",
      "Perfume Women's Dream Bird 100ml Long-Lasting Light Floral And Fruity",
      "perfume women's dream bird 100ml long-lasting light floral and fruity",
      "soft spell floral and fruity perfume 100ml"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068683974",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Keratin Conditioner — In Balance",
    "opening": "Give this step its place beside wash day.",
    "sourceTitle": "Precise Nourishing Keratin Conditioner",
    "sourceAliases": [
      "Precise Nourishing Keratin Conditioner",
      "Keratin Conditioner Soft Scalp Deep Nourishing",
      "keratin conditioner soft scalp deep nourishing",
      "nourishing keratin conditioner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068749510",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Salt & Stillness Himalayan Body Scrub",
    "opening": "A pause with a place in your bathing edit.",
    "sourceTitle": "Curated Himalayan Salt Body Scrub Cream Exfoliating",
    "sourceAliases": [
      "Curated Himalayan Salt Body Scrub Cream Exfoliating",
      "Himalayan Salt Body Scrub Cream Exfoliating",
      "himalayan salt body scrub cream exfoliating"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100068847814",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Warm Silence Body Spray Perfume",
    "opening": "Let your fragrance speak in its own way.",
    "sourceTitle": "Warm Silence Body Spray Perfume",
    "sourceAliases": [
      "Warm Silence Body Spray Perfume",
      "Body Spray Perfume For Women",
      "body spray perfume for women",
      "warm silence body spray perfume"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100069044422",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Lotion — A Daily Intention",
    "opening": "A little attention to an everyday step.",
    "sourceTitle": "Elegant Moisturizing Body Lotion",
    "sourceAliases": [
      "Elegant Moisturizing Body Lotion",
      "Body Lotion Liquid Control Moisturizing",
      "body lotion liquid control moisturizing",
      "moisturizing body lotion"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100069339334",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Rosemary & Coconut Hair Oil — Root Notes",
    "opening": "Bring a considered note to your hair routine.",
    "sourceTitle": "Restrained Rosemary And Coconut Hair Oil",
    "sourceAliases": [
      "Restrained Rosemary And Coconut Hair Oil",
      "Rosemary Coconut Hair Oil Nourishing Moisturizing Fragrance Care",
      "rosemary coconut hair oil nourishing moisturizing fragrance care",
      "rosemary and coconut hair oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100069535942",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Four Little Moods Moisturizing Lip Balm",
    "opening": "Pick the little mood that feels like you.",
    "sourceTitle": "Fun Four-Color Moisturizing Lip Balm",
    "sourceAliases": [
      "Fun Four-Color Moisturizing Lip Balm",
      "4-color Brightening Lip Balm Moisturizing Exfoliating Skin Long-Lasting",
      "4-color brightening lip balm moisturizing exfoliating skin long-lasting",
      "four-color moisturizing lip balm"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100069699782",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Moisturizer — In Your Own Time",
    "opening": "Care belongs on your own schedule.",
    "sourceTitle": "Composed Body Moisturizer Hydrating Skin Care",
    "sourceAliases": [
      "Composed Body Moisturizer Hydrating Skin Care",
      "Body Moisturizer Hydrating Skin Care",
      "body moisturizer hydrating skin care"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100069863622",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Petal Skin Madagascar Centella Skincare",
    "opening": "Keep a little play in the skincare lineup.",
    "sourceTitle": "Youthful Madagascar Centella Asiatica Facial Skincare",
    "sourceAliases": [
      "Youthful Madagascar Centella Asiatica Facial Skincare",
      "Madagascar Centella Asiatica Facial Skin Care",
      "madagascar centella asiatica facial skin care",
      "madagascar centella asiatica facial skincare"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100786598086",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Milk & Honey Hand Soap — Welcome Home",
    "opening": "Give a familiar moment its own welcome.",
    "sourceTitle": "Harmonious Milk Honey Hand Soap",
    "sourceAliases": [
      "Harmonious Milk Honey Hand Soap",
      "Milk Honey Hand Soap",
      "milk honey hand soap"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100786696390",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Stone Conversation Crystal Roller & Scraping Plate",
    "opening": "Two details for a dressing-table moment.",
    "sourceTitle": "Intentional Crystal Roller And Scraping Plate Massager",
    "sourceAliases": [
      "Intentional Crystal Roller And Scraping Plate Massager",
      "Roller Scraping Crystal Plate Massager",
      "roller scraping crystal plate massager",
      "crystal roller and scraping plate massager"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100786860230",
    "brand": "miss-princess",
    "register": "descriptive-poetic",
    "title": "Shampoo Brush — Little Wash-Day Companion",
    "opening": "A little companion for the wash-day lineup.",
    "sourceTitle": "Youthful Silicone Scalp Massage Shampoo Brush",
    "sourceAliases": [
      "Youthful Silicone Scalp Massage Shampoo Brush",
      "Silicone Shampoo Brush Active Meridian Dry And Wet Massage Scalp",
      "silicone shampoo brush active meridian dry and wet massage scalp",
      "silicone scalp massage shampoo brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100786991302",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Double Take Microcurrent Roller Massager",
    "opening": "Make room for a new dressing-table detail.",
    "sourceTitle": "Lighthearted Double-Head Microcurrent Roller Massager",
    "sourceAliases": [
      "Lighthearted Double-Head Microcurrent Roller Massager",
      "Double Roller Massager Double Head Micro-current Beauty Instrument",
      "double roller massager double head micro-current beauty instrument",
      "double-head microcurrent roller massager"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787351750",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Brush — A Daily Arrangement",
    "opening": "Bring a little order to your everyday edit.",
    "sourceTitle": "Timeless Detangling Nylon Bristle Hair Brush",
    "sourceAliases": [
      "Timeless Detangling Nylon Bristle Hair Brush",
      "Hairbrush Anti Klit Brushy Haarborstel Women Detangler Bristle Nylon Hair Brush",
      "hairbrush anti klit brushy haarborstel women detangler bristle nylon hair brush",
      "detangling nylon bristle hair brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787581126",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Scalp Chapter Shampoo Massage Hair Comb",
    "opening": "A considered place beside wash day.",
    "sourceTitle": "Harmonious Shampoo Massage Hair Comb",
    "sourceAliases": [
      "Harmonious Shampoo Massage Hair Comb",
      "Hairdressing Adult Shampoo Massager And Hair Comb",
      "hairdressing adult shampoo massager and hair comb",
      "shampoo massage hair comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787679430",
    "brand": "miss-princess",
    "register": "identity-led",
    "title": "The Five-Step Play Electric Facial Cleansing Tool",
    "opening": "Give your care lineup a new direction.",
    "sourceTitle": "Lighthearted 5 In 1 Electric Facial Cleansing Instrument",
    "sourceAliases": [
      "Lighthearted 5 In 1 Electric Facial Cleansing Instrument",
      "5 In 1 Electric Facial Cleansing Instrument",
      "5 in 1 electric facial cleansing instrument"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787810502",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Mirror Moment Ultrasonic Facial Cleansing Tool",
    "opening": "A little moment before the mirror.",
    "sourceTitle": "Sweet Ultrasonic Facial Cleansing Tool",
    "sourceAliases": [
      "Sweet Ultrasonic Facial Cleansing Tool",
      "The Ultrasonic Facial Cleanser Peeling Machine Removes Blackheads",
      "the ultrasonic facial cleanser peeling machine removes blackheads",
      "ultrasonic facial cleansing tool"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787908806",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Warm Mist Beauty Steamer",
    "opening": "Set aside a little time at the dressing table.",
    "sourceTitle": "Deliberate Beauty Steamer",
    "sourceAliases": [
      "Deliberate Beauty Steamer",
      "Beauty Steamer",
      "beauty steamer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100787974342",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "The Care Measure Eye Cream & Facial Mask Spoon",
    "opening": "A considered tool for the care shelf.",
    "sourceTitle": "Precise Zinc Alloy Eye Cream And Facial Mask Spoon",
    "sourceAliases": [
      "Precise Zinc Alloy Eye Cream And Facial Mask Spoon",
      "Zinc Alloy Eye Cream Facial Mask Spoon Golden Massage Beauty Stick Metal",
      "zinc alloy eye cream facial mask spoon golden massage beauty stick metal",
      "zinc alloy eye cream and facial mask spoon"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788007110",
    "brand": "miss-princess",
    "register": "descriptive-poetic",
    "title": "Ready, Set, Me Pre-Makeup Cream",
    "opening": "Start the makeup moment your own way.",
    "sourceTitle": "Youthful Pre-Makeup Cream",
    "sourceAliases": [
      "Youthful Pre-Makeup Cream",
      "Pre-Makeup Cream, Cream",
      "pre-makeup cream, cream",
      "pre-makeup cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788072646",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Rose Quartz Rendezvous 4-in-1 Vibrating Face Roller",
    "opening": "Give the care hour a place to meet.",
    "sourceTitle": "Restrained 4 In 1 Vibrating Rose Quartz Face Roller",
    "sourceAliases": [
      "Restrained 4 In 1 Vibrating Rose Quartz Face Roller",
      "4 in 1 Vibrating Rose Quartz Face Roller",
      "4 in 1 vibrating rose quartz face roller"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788138182",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Jade Daydream Three-in-One Massage Stick",
    "opening": "Bring a little daydream to the dressing table.",
    "sourceTitle": "Clean Three-In-One Jade Massage Stick",
    "sourceAliases": [
      "Clean Three-In-One Jade Massage Stick",
      "The New Three-in-one Jade Massage Stick Contains Jade",
      "the new three-in-one jade massage stick contains jade",
      "three-in-one jade massage stick"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788170950",
    "brand": "miss-princess",
    "register": "identity-led",
    "title": "The Bath Bouquet Six-Piece Bath Bomb Set",
    "opening": "Pick a little atmosphere for bath time.",
    "sourceTitle": "Lighthearted Six-Piece Mint Lavender And Rose Bath Bomb Set",
    "sourceAliases": [
      "Lighthearted Six-Piece Mint Lavender And Rose Bath Bomb Set",
      "6 Pcs Organic Bath Bombs Bubble Mint Lavender Rose Flavor",
      "6 pcs organic bath bombs bubble mint lavender rose flavor",
      "six-piece mint lavender and rose bath bomb set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788269254",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Dryer Bonnet — The Home Hour",
    "opening": "Give your hair routine a place at home.",
    "sourceTitle": "Effortless Hair Dryer Bonnet Hood",
    "sourceAliases": [
      "Effortless Hair Dryer Bonnet Hood",
      "Hair Dryer Bonnet Hood",
      "hair dryer bonnet hood"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788367558",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Happy Little Break Heated Foot Massage Machine",
    "opening": "Set aside a little break for yourself.",
    "sourceTitle": "Sweet Heated Foot Massage And Pedicure Machine",
    "sourceAliases": [
      "Sweet Heated Foot Massage And Pedicure Machine",
      "Air pressure scraping pedicure machine foot massager home foot beauty foot machine heating pedicure instrument wheel beauty foot treasure",
      "air pressure scraping pedicure machine foot massager home foot beauty foot machine heating pedicure instrument wheel beauty foot treasure",
      "heated foot massage and pedicure machine"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788400326",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Care Choice Hair Removal Device",
    "opening": "Make the routine a choice of your own.",
    "sourceTitle": "Refined Hair Removal Device",
    "sourceAliases": [
      "Refined Hair Removal Device",
      "Hair Removal Device",
      "hair removal device"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788433094",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Water Veil Hyaluronic Acid Facial Gel",
    "opening": "A considered addition to your care shelf.",
    "sourceTitle": "Elevated Hyaluronic Acid Facial Gel",
    "sourceAliases": [
      "Elevated Hyaluronic Acid Facial Gel",
      "Facial gel hyaluronic acid white gel moisturizing gel",
      "facial gel hyaluronic acid white gel moisturizing gel",
      "hyaluronic acid facial gel"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788465862",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Repair Shampoo — The Wash-Day Chapter",
    "opening": "Let wash day have its own chapter.",
    "sourceTitle": "Refined Hair Repair Shampoo",
    "sourceAliases": [
      "Refined Hair Repair Shampoo",
      "Purc Straightening Hair Repair And Straighten Damage Products Brazilian Shampoo",
      "purc straightening hair repair and straighten damage products brazilian shampoo",
      "hair repair shampoo"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100788564166",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Fruit Parade Handmade Bath & Body Soap",
    "opening": "A little fruit, a little play, your bath shelf.",
    "sourceTitle": "Clean Handmade Fruit Bath And Body Soap",
    "sourceAliases": [
      "Clean Handmade Fruit Bath And Body Soap",
      "Thai Bumebime Handmade Soap White Natural Bath And Body Engineering Fruit",
      "thai bumebime handmade soap white natural bath and body engineering fruit",
      "handmade fruit bath and body soap"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790235334",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Dressing Table Skincare Instrument",
    "opening": "Give your care space a detail of its own.",
    "sourceTitle": "Restrained Skincare Beauty Instrument",
    "sourceAliases": [
      "Restrained Skincare Beauty Instrument",
      "Skin Rejuvenation Instrument",
      "skin rejuvenation instrument",
      "skincare beauty instrument"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790333638",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Pore Refining Serum — A Closer Look",
    "opening": "A considered place in your skincare routine.",
    "sourceTitle": "Understated Pore Refining Serum",
    "sourceAliases": [
      "Understated Pore Refining Serum",
      "Pore Refining Serum",
      "pore refining serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790366406",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Mountain Interval Himalayan Salt Body Scrub",
    "opening": "Make the bath hour feel like an interval.",
    "sourceTitle": "Effortless Himalayan Salt Body Scrub",
    "sourceAliases": [
      "Effortless Himalayan Salt Body Scrub",
      "Himalayan Salt Body Scrub",
      "himalayan salt body scrub"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790399174",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Warm Waist Belt — An Hour at Home",
    "opening": "A moment set aside in your own space.",
    "sourceTitle": "Polished Warm Waist Belt",
    "sourceAliases": [
      "Polished Warm Waist Belt",
      "New Warm Belt Menstrual Aunt Stomach Pain Artifact",
      "new warm belt menstrual aunt stomach pain artifact",
      "warm waist belt"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790431942",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Pocket Poise Lipstick-Shaped Eyebrow Shaver",
    "opening": "A little tool for your own finishing routine.",
    "sourceTitle": "Clean Lipstick-Shaped Electric Eyebrow Shaver",
    "sourceAliases": [
      "Clean Lipstick-Shaped Electric Eyebrow Shaver",
      "Lipstick Shape Ladies Electric Shaver Automatic Eyebrow Trimming Artifact",
      "lipstick shape ladies electric shaver automatic eyebrow trimming artifact",
      "lipstick-shaped electric eyebrow shaver"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790497478",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Honey Foot & Leg Cream — The Walk Home",
    "opening": "Give the end of the day a care moment.",
    "sourceTitle": "Deliberate Honey Moisturizing Foot And Leg Cream",
    "sourceAliases": [
      "Deliberate Honey Moisturizing Foot And Leg Cream",
      "Honey Moisturizing Cream Foot Leg",
      "honey moisturizing cream foot leg",
      "honey moisturizing foot and leg cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790530246",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "Quiet Confidence Perfume Spray Gift Box",
    "opening": "Give a little atmosphere, chosen with intention.",
    "sourceTitle": "Quiet Confidence Perfume Spray Gift Box",
    "sourceAliases": [
      "Quiet Confidence Perfume Spray Gift Box",
      "Perfume Spray Gift Box",
      "perfume spray gift box",
      "quiet confidence perfume spray gift box"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790726854",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "The Garden Perfume",
    "opening": "Keep a place for the atmosphere you choose.",
    "sourceTitle": "The Garden Perfume",
    "sourceAliases": [
      "The Garden Perfume",
      "Garden Private Perfume",
      "garden private perfume",
      "the garden perfume"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790759622",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Lotion — A Moment of Ease",
    "opening": "A body care step with room to pause.",
    "sourceTitle": "Timeless Moisturizing Body Lotion",
    "sourceAliases": [
      "Timeless Moisturizing Body Lotion",
      "Moisturizing Body Lotion",
      "body lotion liquid control moisturizing",
      "moisturizing body lotion"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790792390",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Curler — The Evening Shape",
    "opening": "Give the evening look your own direction.",
    "sourceTitle": "Curated Cordless Automatic Hair Curler",
    "sourceAliases": [
      "Curated Cordless Automatic Hair Curler",
      "Cordless Automatic Hair Curler Iron Wireless Curling",
      "cordless automatic hair curler iron wireless curling",
      "cordless automatic hair curler"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790857926",
    "brand": "miss-princess",
    "register": "identity-led",
    "title": "Switch It Up Dual-Purpose Hair Straightener",
    "opening": "Let your plans set the direction.",
    "sourceTitle": "Playful Dual-Purpose Hair Straightener With Display",
    "sourceAliases": [
      "Playful Dual-Purpose Hair Straightener With Display",
      "Display Hair Straightener Dual-purpose Does Not Hurt Hair Curls",
      "display hair straightener dual-purpose does not hurt hair curls",
      "dual-purpose hair straightener with display"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790890694",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Wireless Hair Styling Comb — A New Arrangement",
    "opening": "Choose a new arrangement for your hair edit.",
    "sourceTitle": "Composed Wireless Hair Straightener And Curler Comb",
    "sourceAliases": [
      "Composed Wireless Hair Straightener And Curler Comb",
      "Professional Wireless Hair Straightener Curler Comb Fast Heating Negative Ion",
      "professional wireless hair straightener curler comb fast heating negative ion",
      "wireless hair straightener and curler comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100790956230",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Carry-On Mini Hair Straightening Comb",
    "opening": "Keep a place for care in your travel edit.",
    "sourceTitle": "Timeless Mini Wireless Charging Hair Straightening Comb",
    "sourceAliases": [
      "Timeless Mini Wireless Charging Hair Straightening Comb",
      "Mini Hair Straightening Comb Wireless Charging Portable Multifunctional Hair Care Not Hurt Hair Styling Comb Hair Straightener",
      "mini hair straightening comb wireless charging portable multifunctional hair care not hurt hair styling comb hair straightener",
      "mini wireless charging hair straightening comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791120070",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Little Unwind Neck & Shoulder Roller Massager",
    "opening": "A little pause between your plans.",
    "sourceTitle": "Easy Plastic Handheld Neck And Shoulder Roller Massager",
    "sourceAliases": [
      "Easy Plastic Handheld Neck And Shoulder Roller Massager",
      "Plastic Pressure Point Therapy Neck Massageador Massagem Relieve Hand Roller Neck Massager For Neck Shoulder Trigger Point",
      "plastic pressure point therapy neck massageador massagem relieve hand roller neck massager for neck shoulder trigger point",
      "plastic handheld neck and shoulder roller massager"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791218374",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Self-Cleaning Hair Brush — The Order of Things",
    "opening": "Give familiar steps a little intention.",
    "sourceTitle": "Refined Self-Cleaning Scalp Massage Hair Brush",
    "sourceAliases": [
      "Refined Self-Cleaning Scalp Massage Hair Brush",
      "Self Cleaning For Women One-Key Airbag Massage Scalp Comb Anti-Static Hair Brush",
      "self cleaning for women one-key airbag massage scalp comb anti-static hair brush",
      "self-cleaning scalp massage hair brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791251142",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Brow Edit Trimming Knife & Comb",
    "opening": "Make the finishing detail your own.",
    "sourceTitle": "Restrained Curved Eyebrow Trimming Knife With Comb",
    "sourceAliases": [
      "Restrained Curved Eyebrow Trimming Knife With Comb",
      "Eyebrow Trimming Knife With Comb Curved Moon Small Beauty Supplies Gadgets",
      "eyebrow trimming knife with comb curved moon small beauty supplies gadgets",
      "curved eyebrow trimming knife with comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791316678",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Vitamin C Face Cream — Daybreak",
    "opening": "A considered start to the care hour.",
    "sourceTitle": "Elevated Vitamin C Face Cream",
    "sourceAliases": [
      "Elevated Vitamin C Face Cream",
      "Vitamin C Face Cream Skin Care Products",
      "vitamin c face cream skin care products",
      "vitamin c face cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791414982",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Body Canvas Waterproof Concealer",
    "opening": "Let your makeup have your point of view.",
    "sourceTitle": "Effortless Waterproof Body Concealer",
    "sourceAliases": [
      "Effortless Waterproof Body Concealer",
      "Body Concealer Waterproof Cover Tattoo Scar Birthmark Invisible",
      "body concealer waterproof cover tattoo scar birthmark invisible",
      "waterproof body concealer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791447750",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Light Study High-Gloss Makeup Palette",
    "opening": "Choose how the makeup moment comes together.",
    "sourceTitle": "Restrained High-Gloss Multi-Purpose Makeup Palette",
    "sourceAliases": [
      "Restrained High-Gloss Multi-Purpose Makeup Palette",
      "High-Gloss Natural Makeup Diamond Texture A Plate Of Multi-Purpose Daily",
      "high-gloss natural makeup diamond texture a plate of multi-purpose daily",
      "high-gloss multi-purpose makeup palette"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791480518",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Still Form Resin Facial Roller Set",
    "opening": "A considered detail for the dressing table.",
    "sourceTitle": "Deliberate Resin Facial Roller Set",
    "sourceAliases": [
      "Still Form Facial Gua Sha Stone",
      "Deliberate Resin Facial Roller Set",
      "Deliberate Facial Gua Sha Stone Scraper",
      "Face Lift Up Wrinkle Remover Gua Sha Stone For Face Massage Gua Sha Scraper",
      "face lift up wrinkle remover gua sha stone for face massage gua sha scraper",
      "facial gua sha stone scraper"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791513286",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Vitamin C Facial Serum — First Chapter",
    "opening": "Begin the skincare chapter with intention.",
    "sourceTitle": "Intentional Vitamin C Facial Serum",
    "sourceAliases": [
      "Intentional Vitamin C Facial Serum",
      "Vitamin C Serum Facial Amazon",
      "vitamin c serum facial amazon",
      "vitamin c facial serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791578822",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Little Jewel Loose Powder Makeup Brush",
    "opening": "Let a little detail finish the makeup moment.",
    "sourceTitle": "Sweet Embellished Loose Powder Brush",
    "sourceAliases": [
      "Sweet Embellished Loose Powder Brush",
      "Diamond Studded Small Waist Makeup Full Of Goblet Loose Powder Brush",
      "diamond studded small waist makeup full of goblet loose powder brush",
      "embellished loose powder brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791677126",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Green Edit 13-Piece Makeup Brush Set",
    "opening": "Give your makeup tools their own edit.",
    "sourceTitle": "Elevated 13-Piece Green Makeup Brush Set",
    "sourceAliases": [
      "Elevated 13-Piece Green Makeup Brush Set",
      "Set Of 13 Four Seasons Green Makeup Brushes",
      "set of 13 four seasons green makeup brushes",
      "13-piece green makeup brush set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791742662",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Styling Trio Curler, Straightener & Hair Dryer",
    "opening": "Three tools with a place in your styling routine.",
    "sourceTitle": "Curated Three-In-One Curling Iron Straightener And Hair Dryer",
    "sourceAliases": [
      "Curated Three-In-One Curling Iron Straightener And Hair Dryer",
      "Multifunctional Three-In-One High-Power Curling Iron Straightener Hair Dryer",
      "multifunctional three-in-one high-power curling iron straightener hair dryer",
      "three-in-one curling iron straightener and hair dryer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791775430",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Home Decision Laser Hair Removal Device",
    "opening": "Choose a care routine for your own space.",
    "sourceTitle": "Harmonious Home Laser Hair Removal Device",
    "sourceAliases": [
      "Harmonious Home Laser Hair Removal Device",
      "Home Laser Hair Removal Device",
      "home laser hair removal device"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791808198",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Playful Pause Scalp Massage Hair Comb",
    "opening": "Keep a little play beside wash day.",
    "sourceTitle": "Fresh Scalp Massage Hair Comb",
    "sourceAliases": [
      "Fresh Scalp Massage Hair Comb",
      "Hair Care Scalp Massage Comb Massager Meridian Brush Head Face",
      "hair care scalp massage comb massager meridian brush head face",
      "scalp massage hair comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791840966",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Milk Care Edit Lotion & Face Cream Set",
    "opening": "Bring the care steps together in your own way.",
    "sourceTitle": "Curated Milk Moisturizing Lotion And Face Cream Set",
    "sourceAliases": [
      "Curated Milk Moisturizing Lotion And Face Cream Set",
      "Milk Moisturizing Set Lotion Face Cream Skin Care Products",
      "milk moisturizing set lotion face cream skin care products",
      "milk moisturizing lotion and face cream set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791873734",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Orchard Hour Fruit Bath Salt Body Scrub",
    "opening": "Give the bath shelf a little orchard atmosphere.",
    "sourceTitle": "Effortless Fruit Bath Salt Body Scrub Cream",
    "sourceAliases": [
      "Effortless Fruit Bath Salt Body Scrub Cream",
      "Fruit Bath Salt Scrub Cream Exfoliating Body Care",
      "fruit bath salt scrub cream exfoliating body care",
      "fruit bath salt body scrub cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791906502",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Care Liquid — The Skin & Hair Chapter",
    "opening": "Make room for a step of its own.",
    "sourceTitle": "Harmonious Moisturizing Skin And Hair Care Liquid",
    "sourceAliases": [
      "Harmonious Moisturizing Skin And Hair Care Liquid",
      "Skin And Hair Moisturizing Nutritional Care Liquid",
      "skin and hair moisturizing nutritional care liquid",
      "moisturizing skin and hair care liquid"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100791939270",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Oil — The Closing Note",
    "opening": "A final note in your hair care edit.",
    "sourceTitle": "Elegant Nourishing Hair Essential Oil",
    "sourceAliases": [
      "Elegant Nourishing Hair Essential Oil",
      "Hair Essential Oil Improve Dryness And Irritability And Nourish",
      "hair essential oil improve dryness and irritability and nourish",
      "nourishing hair essential oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792070342",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Removal Mousse — A Fresh Start",
    "opening": "Choose the next part of your care routine.",
    "sourceTitle": "Understated Hair Removal Cream Mousse Foam Skin Care",
    "sourceAliases": [
      "Understated Hair Removal Cream Mousse Foam Skin Care",
      "Hair Removal Cream Mousse Foam Skin Care",
      "hair removal cream mousse foam skin care"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792135878",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Body Oil — The Space Between",
    "opening": "Keep a little space for care between plans.",
    "sourceTitle": "Elevated Skincare Body Oil",
    "sourceAliases": [
      "Elevated Skincare Body Oil",
      "Skincare Body Oil",
      "skincare body oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792168646",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Becoming Skincare Set",
    "opening": "Let your care edit come together.",
    "sourceTitle": "Polished Skincare Set",
    "sourceAliases": [
      "Polished Skincare Set",
      "Anti Skincare Set",
      "anti skincare set",
      "skincare set"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792234182",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Next Chapter Facial Serum",
    "opening": "Give the next chapter its own beginning.",
    "sourceTitle": "Understated Anti-Aging Serum",
    "sourceAliases": [
      "Understated Anti-Aging Serum",
      "Anti-Aging Serum",
      "anti-aging serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792266950",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Squalane Skincare Oil — A Daily Reserve",
    "opening": "Reserve a little time for a familiar step.",
    "sourceTitle": "Understated Moisturizing Squalane Wrinkle Reducing Skincare Oil",
    "sourceAliases": [
      "Understated Moisturizing Squalane Wrinkle Reducing Skincare Oil",
      "Moisturizing Squalane Wrinkle Reducing Skincare Oil",
      "moisturizing squalane wrinkle reducing skincare oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792332486",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Skincare Lotion — A Quiet Practice",
    "opening": "Make a familiar step a practice of your own.",
    "sourceTitle": "Curated Skincare Lotion",
    "sourceAliases": [
      "Curated Skincare Lotion",
      "Meihei Skincare Lotion",
      "meihei skincare lotion",
      "skincare lotion"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792365254",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Skincare Cream — The Care Constant",
    "opening": "A considered place on your care shelf.",
    "sourceTitle": "Effortless Skincare Cream",
    "sourceAliases": [
      "Effortless Skincare Cream",
      "Full Effect Skincare Cream",
      "full effect skincare cream",
      "skincare cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792398022",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Skincare Discovery Mystery Box",
    "opening": "Leave a little space for discovery.",
    "sourceTitle": "Elevated Skincare Mystery Box",
    "sourceAliases": [
      "Elevated Skincare Mystery Box",
      "Skincare Mystery Box",
      "skincare mystery box"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792430790",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Styling Pair Hair Straightener & Hot Comb",
    "opening": "Bring two styling tools into your own edit.",
    "sourceTitle": "Timeless Two-In-One Hair Straightener And Hot Comb",
    "sourceAliases": [
      "Timeless Two-In-One Hair Straightener And Hot Comb",
      "2 In 1 Hair Straightener Hot Comb Negative Ion Curling Tong Dual-Purpose",
      "2 in 1 hair straightener hot comb negative ion curling tong dual-purpose",
      "two-in-one hair straightener and hot comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792561862",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair & Beard Straightening Comb — In Line",
    "opening": "Put a little intention into the styling routine.",
    "sourceTitle": "Restrained Hair And Beard Straightening Comb",
    "sourceAliases": [
      "Restrained Hair And Beard Straightening Comb",
      "Multifunctional Hair Straightener Comb Brush Men Beard Straightening",
      "multifunctional hair straightener comb brush men beard straightening",
      "hair and beard straightening comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792692934",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Honeycomb Rhythm Wet & Dry Hair Comb",
    "opening": "Let familiar steps find their own rhythm.",
    "sourceTitle": "Deliberate Wet And Dry Honeycomb Hair Comb",
    "sourceAliases": [
      "Deliberate Wet And Dry Honeycomb Hair Comb",
      "Hollow Comb Dry Wet Dual Purpose Honeycomb Hairdressing",
      "hollow comb dry wet dual purpose honeycomb hairdressing",
      "wet and dry honeycomb hair comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792725702",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Warm Contour Microcurrent Neck Massager",
    "opening": "Set aside a dressing-table moment for yourself.",
    "sourceTitle": "Precise Thermal Microcurrent Neck Massager",
    "sourceAliases": [
      "Precise Thermal Microcurrent Neck Massager",
      "Ems Thermal Neck And Tighten Massager Electric Microcurrent Remover",
      "ems thermal neck and tighten massager electric microcurrent remover",
      "thermal microcurrent neck massager"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792856774",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "The Lash Detail Metal Tweezers & Comb",
    "opening": "Let the little finishing steps have their place.",
    "sourceTitle": "Harmonious Metal Eyelash Tweezers With Comb",
    "sourceAliases": [
      "Harmonious Metal Eyelash Tweezers With Comb",
      "Eyelash With Comb Aid Metal Tweezers Beauty Tools",
      "eyelash with comb aid metal tweezers beauty tools",
      "metal eyelash tweezers with comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792889542",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Eye Care — A Moment Considered",
    "opening": "A little attention to the care details.",
    "sourceTitle": "Elevated Eye Care Products",
    "sourceAliases": [
      "Elevated Eye Care Products",
      "Eye Care Products",
      "eye care products"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100792955078",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Personal Practice Laser Hair Removal Device",
    "opening": "Build a personal routine in your own space.",
    "sourceTitle": "Elevated Laser Hair Removal Device",
    "sourceAliases": [
      "Elevated Laser Hair Removal Device",
      "Household Whole Body Painless Laser Hair Removal Device",
      "household whole body painless laser hair removal device",
      "laser hair removal device"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793413830",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Sugar Hour Body Spray Perfume",
    "opening": "Keep a little sweetness in your fragrance edit.",
    "sourceTitle": "Petal Dream Body Spray Perfume",
    "sourceAliases": [
      "Petal Dream Body Spray Perfume",
      "Cross-Border Foreign Trade Long-Lasting Light Perfume Female Body Spray",
      "cross-border foreign trade long-lasting light perfume female body spray",
      "petal dream body spray perfume"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793446598",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Hair Mask Conditioner — A Deep Pause",
    "opening": "Give hair care an unhurried moment.",
    "sourceTitle": "Effortless Deep Moisturizing Hair Mask Conditioner",
    "sourceAliases": [
      "Effortless Deep Moisturizing Hair Mask Conditioner",
      "Deep Moisturizing Hair Mask Soft Conditioner Care",
      "deep moisturizing hair mask soft conditioner care",
      "deep moisturizing hair mask conditioner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793479366",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "The Bath Companion Loofah",
    "opening": "A familiar companion for the bath hour.",
    "sourceTitle": "Composed Bath Loofah",
    "sourceAliases": [
      "Composed Bath Loofah",
      "Independent High-End Large Bath Pearl Loofah Packaging Foaming Durable Shower",
      "independent high-end large bath pearl loofah packaging foaming durable shower",
      "bath loofah"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793544902",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Four Little Scenes Matte Highlight Eyeshadow",
    "opening": "Pick a little scene for your next look.",
    "sourceTitle": "Lighthearted Four-Color Matte Highlight Eyeshadow",
    "sourceAliases": [
      "Lighthearted Four-Color Matte Highlight Eyeshadow",
      "Matte Brightening Highlight Eyeshadow Four Colors",
      "matte brightening highlight eyeshadow four colors",
      "four-color matte highlight eyeshadow"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793610438",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Fine Line Liquid Eyeliner",
    "opening": "Let a little line set the direction.",
    "sourceTitle": "Harmonious Fine Liquid Eyeliner",
    "sourceAliases": [
      "Harmonious Fine Liquid Eyeliner",
      "Kakashow Very Thin Double Claw Liquid Eyeliner Mom Eyelashes Crouching Silkworm",
      "kakashow very thin double claw liquid eyeliner mom eyelashes crouching silkworm",
      "fine liquid eyeliner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793643206",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Starry Night Waterproof Eyeliner",
    "opening": "Give the evening look a detail of its own.",
    "sourceTitle": "Understated Starry Sky Waterproof Eyeliner",
    "sourceAliases": [
      "Understated Starry Sky Waterproof Eyeliner",
      "Starry Sky Eyeliner Waterproof And Sweatproof Long Lasting Non Smudge",
      "starry sky eyeliner waterproof and sweatproof long lasting non smudge",
      "starry sky waterproof eyeliner"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793675974",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Brow Signature Waterproof Eyebrow Cream",
    "opening": "Make the finishing gesture your own.",
    "sourceTitle": "Precise Waterproof Eyebrow Cream",
    "sourceAliases": [
      "Precise Waterproof Eyebrow Cream",
      "Stereo Eyebrow Cream Waterproof And Durable Non-decolorizing Not Smudge",
      "stereo eyebrow cream waterproof and durable non-decolorizing not smudge",
      "waterproof eyebrow cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793708742",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Blowout Edit Three-in-One Electric Hair Dryer",
    "opening": "Give your hair tools their own place.",
    "sourceTitle": "Elegant Three-In-One Electric Hair Dryer",
    "sourceAliases": [
      "Elegant Three-In-One Electric Hair Dryer",
      "Three-In-One Electric Hair Dryer Multi-Functional Household",
      "three-in-one electric hair dryer multi-functional household",
      "three-in-one electric hair dryer"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793741510",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Batana Hair Oil — The Root Ritual",
    "opening": "Make a little time for your hair care edit.",
    "sourceTitle": "Effortless Batana Hair Care Oil",
    "sourceAliases": [
      "Effortless Batana Hair Care Oil",
      "Batana Oil Hair Care Essential",
      "batana oil hair care essential",
      "batana hair care oil"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793807046",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Neck Cream — A Daily Gesture",
    "opening": "A care gesture with a place in the everyday.",
    "sourceTitle": "Intentional Neck Care Cream 50g",
    "sourceAliases": [
      "Intentional Neck Care Cream 50g",
      "Neck Cream 50g Fading",
      "neck cream 50g fading",
      "neck care cream 50g"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100793938118",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Wash-Day Edit Spray Bottle, Silicone Brush & Hair Comb",
    "opening": "Bring the wash-day tools into your own arrangement.",
    "sourceTitle": "Timeless Spray Bottle Silicone Brush And Hollow Hair Comb",
    "sourceAliases": [
      "Timeless Spray Bottle Silicone Brush And Hollow Hair Comb",
      "High Pressure Spray Bottle Cleaning Silicone Brush Hollow Comb Hair Care Shampoo",
      "high pressure spray bottle cleaning silicone brush hollow comb hair care shampoo",
      "spray bottle silicone brush and hollow hair comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794069190",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Jade Reflection Facial & Eye Massage Roller",
    "opening": "Make the dressing-table moment your own.",
    "sourceTitle": "Effortless Jade Facial And Eye Massage Roller",
    "sourceAliases": [
      "Effortless Jade Facial And Eye Massage Roller",
      "Facial Eye Scraping Massage Jade Roller",
      "facial eye scraping massage jade roller",
      "jade facial and eye massage roller"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794101958",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Little Current Electric Massage Hair Comb",
    "opening": "A little detail for the hair care lineup.",
    "sourceTitle": "Chic Electric Massage Hair Comb",
    "sourceAliases": [
      "Chic Electric Massage Hair Comb",
      "Electric Massage Hair Comb Household",
      "electric massage hair comb household",
      "electric massage hair comb"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794233030",
    "brand": "miss-princess",
    "register": "descriptive-poetic",
    "title": "Lemon & Turmeric Soap — Sunny Side",
    "opening": "A little sunshine for the bath shelf.",
    "sourceTitle": "Easy Turmeric Lemon Soap Handmade Cold Process",
    "sourceAliases": [
      "Easy Turmeric Lemon Soap Handmade Cold Process",
      "Turmeric Lemon Soap Handmade Cold Process",
      "turmeric lemon soap handmade cold process"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794298566",
    "brand": "mvqueen",
    "register": "descriptive-poetic",
    "title": "Neck Roller Cream — A Finishing Gesture",
    "opening": "Give a small care step your attention.",
    "sourceTitle": "Restrained Nourishing Neck Roller Cream",
    "sourceAliases": [
      "Restrained Nourishing Neck Roller Cream",
      "Neck Roller Cream Lifts Dilutes Lines Deeply Nourishes Easily Absorbed Skin Care",
      "neck roller cream lifts dilutes lines deeply nourishes easily absorbed skin care",
      "nourishing neck roller cream"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794331334",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Rose Flourish Loose Powder Makeup Brush",
    "opening": "A little flourish for the makeup moment.",
    "sourceTitle": "Youthful Rose Loose Powder Makeup Brush",
    "sourceAliases": [
      "Youthful Rose Loose Powder Makeup Brush",
      "Rose Loose Powder Makeup Brush Beauty Tool",
      "rose loose powder makeup brush beauty tool",
      "rose loose powder makeup brush"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794429638",
    "brand": "mvqueen",
    "register": "identity-led",
    "title": "The Anywhere Mirror Foldable LED Makeup Mirror",
    "opening": "Give your makeup moment a place wherever you are.",
    "sourceTitle": "Curated Portable Foldable LED Makeup Mirror With Built-In Lights",
    "sourceAliases": [
      "Curated Portable Foldable LED Makeup Mirror With Built-In Lights",
      "Portable Foldable Led Makeup Mirror With Built-In Lights",
      "portable foldable led makeup mirror with built-in lights"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794495174",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Ready Room Lighted Desktop Vanity Mirror",
    "opening": "Give the getting-ready hour its own scene.",
    "sourceTitle": "Playful Desktop Vanity Mirror With Fill Light And Charging Function",
    "sourceAliases": [
      "Playful Desktop Vanity Mirror With Fill Light And Charging Function",
      "Student Dormitory Fill-light Desktop Vanity Mirror With Charging Function",
      "student dormitory fill-light desktop vanity mirror with charging function",
      "desktop vanity mirror with fill light and charging function"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794527942",
    "brand": "miss-princess",
    "register": "evocative",
    "title": "Pink Prelude Peptide Facial Serum",
    "opening": "Begin your skincare lineup with a little play.",
    "sourceTitle": "Playful Pink Peptide Facial Serum",
    "sourceAliases": [
      "Playful Pink Peptide Facial Serum",
      "Pink Peptide Serum Moisturizing And Hydrating Facial",
      "pink peptide serum moisturizing and hydrating facial",
      "pink peptide facial serum"
    ]
  },
  {
    "productId": "gid://shopify/Product/9100794560710",
    "brand": "mvqueen",
    "register": "evocative",
    "title": "Mirror Muse Hydrating Lip Serum",
    "opening": "Give the finishing step a little reflection.",
    "sourceTitle": "Deliberate Hydrating Mirror-Like Lip Serum",
    "sourceAliases": [
      "Deliberate Hydrating Mirror-Like Lip Serum",
      "Anti-Chapping Mirror-Like Hydrating Lip Serum",
      "anti-chapping mirror-like hydrating lip serum",
      "hydrating mirror-like lip serum"
    ]
  }
];

export function normalizeProductName(value: string): string {
  return value.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

const BY_ID = new Map(CURATED_PRODUCT_NAMES.map((entry) => [entry.productId, entry]));
const BY_TITLE = new Map(CURATED_PRODUCT_NAMES.map((entry) => [normalizeProductName(entry.title), entry]));
if (BY_ID.size !== CURATED_PRODUCT_NAMES.length || BY_TITLE.size !== CURATED_PRODUCT_NAMES.length) {
  throw new Error("Curated product names must have distinct product IDs and names");
}

export function curatedNameByTitle(title: string): CuratedProductName | undefined {
  return BY_TITLE.get(normalizeProductName(title));
}

export function matchingCuratedName(productId: string, title: string): CuratedProductName | undefined {
  const entry = BY_ID.get(productId);
  const normalized = normalizeProductName(title);
  return entry && [entry.title, ...entry.sourceAliases].some((value) => normalizeProductName(value) === normalized)
    ? entry : undefined;
}
