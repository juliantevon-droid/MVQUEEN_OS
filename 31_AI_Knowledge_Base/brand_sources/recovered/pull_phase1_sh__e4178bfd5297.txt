#!/bin/bash

# ============================================================
# MVQUEEN_OS — FULL CONTEXT PULLER v2
# Covers Phase 1 + Phase 2 + all future phases
# Run this before every Claude session
# Output: MVQUEEN_CONTEXT.md — upload this to Claude
# ============================================================

VAULT="$HOME/storage/shared/MVQUEEN_OS"
OUTPUT="$HOME/storage/shared/MVQUEEN_OS/MVQUEEN_CONTEXT.md"

echo "👑 MVQUEEN_OS — Full Context Pull v2"
echo "======================================"
echo ""

cat > "$OUTPUT" << 'HEADER'
# 👑 MVQUEEN_OS — SESSION CONTEXT FILE
# Upload this file at the start of every Claude session.

---

## WHO I AM
- Brand: MVQUEEN ("Most Valuable Queen")
- Sister Brand: Miss.Princess
- Positioning: Accessible luxury — emotional elevation, not status performance
- Stage: Building OS, pre-launch, Shopify-based e-commerce
- Tools: Obsidian (vault), Termux (Android), Pydroid3, Claude AI

## PHASE STATUS
- Phase 1: COMPLETE | Phase 2: COMPLETE | Phase 3: COMPLETE
- Phase 4: COMPLETE — AI Systems built
- Phase 5: IN PROGRESS — Shopify and Operations
- Production Plan: MVQUEEN_PRODUCTION_PLAN.md

## SOURCE OF TRUTH
- Brand Bible: 01_Brand_Strategy/Brand_Bible.md
- Master Doctrine: 00_Doctrine/master_doctrine.md
- Brand Constitution: 00_Doctrine/brand_constitution.md

---
HEADER

echo "✅ Header written"

echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "## FILE CONTENTS" >> "$OUTPUT"
echo "" >> "$OUTPUT"

EMPTY_COUNT=0
POPULATED_COUNT=0
MISSING_COUNT=0
REBUILT_COUNT=0

pull_file() {
  local FILE="$1"
  local FULL_PATH="$VAULT/$FILE"

  echo "" >> "$OUTPUT"
  echo "---" >> "$OUTPUT"
  echo "### FILE: $FILE" >> "$OUTPUT"

  if [ ! -f "$FULL_PATH" ]; then
    echo "**STATUS: MISSING**" >> "$OUTPUT"
    echo "⚠️  MISSING:    $FILE"
    MISSING_COUNT=$((MISSING_COUNT + 1))
    return
  fi

  SIZE=$(wc -c < "$FULL_PATH")
  LINES=$(wc -l < "$FULL_PATH")
  IS_REBUILT=$(head -3 "$FULL_PATH" | grep -c "MVQUEEN" 2>/dev/null || echo 0)

  if [ "$SIZE" -lt 100 ]; then
    echo "**STATUS: EMPTY — $SIZE bytes**" >> "$OUTPUT"
    echo "🔴 EMPTY:      $FILE"
    EMPTY_COUNT=$((EMPTY_COUNT + 1))
  elif [ "$IS_REBUILT" -gt 0 ]; then
    echo "**STATUS: REBUILT — $SIZE bytes, $LINES lines**" >> "$OUTPUT"
    echo "✅ REBUILT:    $FILE ($SIZE bytes)"
    REBUILT_COUNT=$((REBUILT_COUNT + 1))
    POPULATED_COUNT=$((POPULATED_COUNT + 1))
  else
    echo "**STATUS: POPULATED — $SIZE bytes, $LINES lines**" >> "$OUTPUT"
    echo "📄 POPULATED:  $FILE ($SIZE bytes)"
    POPULATED_COUNT=$((POPULATED_COUNT + 1))
  fi

  cat "$FULL_PATH" >> "$OUTPUT"
  echo "" >> "$OUTPUT"
}

# 00_Doctrine
pull_file "00_Doctrine/master_doctrine.md"
pull_file "00_Doctrine/brand_constitution.md"
pull_file "00_Doctrine/luxury_philosophy.md"
pull_file "00_Doctrine/feminine_identity_framework.md"
pull_file "00_Doctrine/emotional_intelligence_framework.md"
pull_file "00_Doctrine/ai_governance.md"
pull_file "00_Doctrine/master_workflow_system.md"

# 01_Brand_Strategy
pull_file "01_Brand_Strategy/Brand_Bible.md"
pull_file "01_Brand_Strategy/USP.md"
pull_file "01_Brand_Strategy/Elevator_Pitch.md"
pull_file "01_Brand_Strategy/Slogans.md"
pull_file "01_Brand_Strategy/Taglines.md"
pull_file "01_Brand_Strategy/Brand_Essence.md"
pull_file "01_Brand_Strategy/Brand_Values.md"
pull_file "01_Brand_Strategy/Brand_Positioning.md"
pull_file "01_Brand_Strategy/Brand_Story.md"
pull_file "01_Brand_Strategy/Mission_And_Vision.md"
pull_file "01_Brand_Strategy/Emotional_Transformation.md"
pull_file "01_Brand_Strategy/brand_manifesto.md"
pull_file "01_Brand_Strategy/brand_philosophy.md"

# 02_Brand_Identity
pull_file "02_Brand_Identity/color_system.md"
pull_file "02_Brand_Identity/typography_system.md"
pull_file "02_Brand_Identity/brand_rules.md"
pull_file "02_Brand_Identity/brand_vocabulary.md"
pull_file "02_Brand_Identity/visual_direction.md"
pull_file "02_Brand_Identity/packaging_identity.md"
pull_file "02_Brand_Identity/photography_direction.md"
pull_file "02_Brand_Identity/brand_identity.md"

# 03_Customer_Psychology
pull_file "03_Customer_Psychology/Customer_Personas.md"
pull_file "03_Customer_Psychology/customer_objections.md"
pull_file "03_Customer_Psychology/trust_building.md"
pull_file "03_Customer_Psychology/emotional_drivers.md"
pull_file "03_Customer_Psychology/Buying_Psychology.md"

# 04_Products
pull_file "04_Products/Product_Naming_System.md"
pull_file "04_Products/Pricing_Strategy.md"
pull_file "04_Products/Collection_Structure.md"
pull_file "04_Products/Product_Framework.md"
pull_file "04_Products/Product_Catalog.md"
pull_file "04_Products/Beauty_Products.md"
pull_file "04_Products/Fashion_Products.md"
pull_file "04_Products/Hair_Products.md"
pull_file "04_Products/SKU_Systems.md"

# 05_SEO_And_Content
pull_file "05_SEO_And_Content/SEO_Strategy.md"
pull_file "05_SEO_And_Content/Blog_Strategy.md"
pull_file "05_SEO_And_Content/Content_Calendar.md"
pull_file "05_SEO_And_Content/Keyword_Research.md"

# 06_Tone_And_Voice
pull_file "06_Tone_And_Voice/Forbidden_Words.md"
pull_file "06_Tone_And_Voice/Voice_Consistency_Rules.md"
pull_file "06_Tone_And_Voice/Writing_Rules.md"
pull_file "06_Tone_And_Voice/CTA_Library.md"
pull_file "06_Tone_And_Voice/Example_Copy.md"
pull_file "06_Tone_And_Voice/Product_Description_Voice.md"
pull_file "06_Tone_And_Voice/Hook_Systems.md"
pull_file "06_Tone_And_Voice/Brand_Messaging.md"
pull_file "06_Tone_And_Voice/Tone_Guide.md"
pull_file "06_Tone_And_Voice/Ad_Copy_Voice.md"
pull_file "06_Tone_And_Voice/Email_Voice.md"
pull_file "06_Tone_And_Voice/Social_Voice.md"
pull_file "06_Tone_And_Voice/SMS_Voice.md"

# 08_Social_Media
pull_file "08_Social_Media/Content_Pillars.md"
pull_file "08_Social_Media/Caption_Templates.md"
pull_file "08_Social_Media/Instagram_Strategy.md"
pull_file "08_Social_Media/TikTok_Strategy.md"
pull_file "08_Social_Media/Pinterest_Strategy.md"

# 10_AI_Systems
pull_file "10_AI_Systems/AI_Prompt_Library.md"
pull_file "10_AI_Systems/Product_Description_Prompts.md"
pull_file "10_AI_Systems/Ad_Copy_Prompts.md"
pull_file "10_AI_Systems/Image_Generation_Prompts.md"
pull_file "10_AI_Systems/Social_Media_Prompts.md"

# SUMMARY
echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "## PULL SUMMARY" >> "$OUTPUT"
echo "- Rebuilt: $REBUILT_COUNT" >> "$OUTPUT"
echo "- Populated (needs review): $((POPULATED_COUNT - REBUILT_COUNT))" >> "$OUTPUT"
echo "- Empty: $EMPTY_COUNT" >> "$OUTPUT"
echo "- Missing: $MISSING_COUNT" >> "$OUTPUT"
echo "- Pull timestamp: $(date)" >> "$OUTPUT"

echo ""
echo "======================================"
echo "✅ PULL COMPLETE"
printf "   %-28s %s\n" "Rebuilt:" "$REBUILT_COUNT files"
printf "   %-28s %s\n" "Populated (review):" "$((POPULATED_COUNT - REBUILT_COUNT)) files"
printf "   %-28s %s\n" "Empty:" "$EMPTY_COUNT files"
printf "   %-28s %s\n" "Missing:" "$MISSING_COUNT files"
echo ""
echo "📄 Saved to: $OUTPUT"
echo "📤 Upload MVQUEEN_CONTEXT.md to Claude."
echo "======================================"
