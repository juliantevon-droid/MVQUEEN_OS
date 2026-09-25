import type { BrandRouting, Classification } from "../mvqueen-intelligence";
import type { PricingDecision } from "./pricing-engine";
import { getEnterpriseIntegrationStatus, type IntegrationState } from "./integration-status";

export type MarketingPlan = {
  state: "ready_for_briefing" | "needs_brand_review" | "needs_commercial_inputs";
  brandWorld: "MVQueen" | "Miss.Princess" | "Needs Review";
  positioning: string;
  channels: string[];
  funnel: {
    discovery: string;
    consideration: string;
    conversion: string;
    retention: string;
  };
  creativeAngles: string[];
  measurementEvents: string[];
  paidExecution: IntegrationState;
  paidExecutionReason: string;
};

export function buildMarketingPlan(
  classification: Classification,
  brandRoute: BrandRouting,
  pricing: PricingDecision,
): MarketingPlan {
  const paidMedia = getEnterpriseIntegrationStatus().paidMedia;
  if (!brandRoute.brand) {
    return {
      state: "needs_brand_review",
      brandWorld: "Needs Review",
      positioning: "Brand-world assignment must be resolved before campaign generation.",
      channels: [],
      funnel: { discovery: "", consideration: "", conversion: "", retention: "" },
      creativeAngles: [],
      measurementEvents: ["view_item", "add_to_cart", "begin_checkout", "purchase"],
      paidExecution: paidMedia.state,
      paidExecutionReason: "No ad-platform execution adapter is connected.",
    };
  }

  const isPrincess = brandRoute.brand === "miss-princess";
  const commercialReady = pricing.state === "ready_for_approval";

  return {
    state: commercialReady ? "ready_for_briefing" : "needs_commercial_inputs",
    brandWorld: isPrincess ? "Miss.Princess" : "MVQueen",
    positioning: isPrincess
      ? "Soft, bright, playful feminine discovery with a polished finish."
      : "Neutral, bold, refined modern luxury with cross-generational styling.",
    channels: ["Meta", "TikTok", "Pinterest", "Google", "Email", "SMS"],
    funnel: {
      discovery: isPrincess
        ? "Color, styling play, newness and social-native product discovery."
        : "Editorial authority, styling confidence, quality cues and refined aspiration.",
      consideration: `${classification.productType} education, verified details, styling context and proof.`,
      conversion: commercialReady
        ? "Use approved price/value architecture, product proof, shipping and returns."
        : "Hold paid conversion creative until commercial inputs are complete.",
      retention: "Post-purchase education, complementary products, replenishment where relevant and brand-world storytelling.",
    },
    creativeAngles: isPrincess
      ? ["color story", "playful styling", "soft glamour", "social discovery"]
      : ["modern polish", "quiet statement", "refined confidence", "editorial styling"],
    measurementEvents: ["view_item", "add_to_cart", "begin_checkout", "purchase"],
    paidExecution: paidMedia.state,
    paidExecutionReason:
      "Campaign planning is connected; external ad-account execution remains disabled until an approved adapter/account is connected.",
  };
}
