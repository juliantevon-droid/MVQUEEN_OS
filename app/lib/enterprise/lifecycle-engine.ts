import type { BrandRouting, Classification } from "../mvqueen-intelligence";
import { getEnterpriseIntegrationStatus } from "./integration-status";

export type LifecyclePlan = {
  state: "ready_for_adapter" | "needs_brand_review";
  brandWorld: "MVQueen" | "Miss.Princess" | "Needs Review";
  stages: Array<{ stage: string; purpose: string }>;
  execution: "connected" | "configured_disabled" | "not_connected";
};

export function buildLifecyclePlan(
  classification: Classification,
  brandRoute: BrandRouting,
): LifecyclePlan {
  const integration = getEnterpriseIntegrationStatus().lifecycle;
  if (!brandRoute.brand) {
    return {
      state: "needs_brand_review",
      brandWorld: "Needs Review",
      stages: [],
      execution: integration.state,
    };
  }

  const brandWorld = brandRoute.brand === "miss-princess" ? "Miss.Princess" : "MVQueen";
  const replenishable = ["Skincare", "Makeup", "Hair Care", "Bath & Body", "Fragrance"].includes(classification.family);

  return {
    state: "ready_for_adapter",
    brandWorld,
    stages: [
      { stage: "post_purchase", purpose: "Order confidence, care/use guidance and brand-world reinforcement." },
      { stage: "cross_sell", purpose: "Recommend genuinely complementary products from the same brand world." },
      ...(replenishable
        ? [{ stage: "replenishment", purpose: "Prompt replenishment only when product cadence is supported by product type and purchase timing." }]
        : []),
      { stage: "win_back", purpose: "Re-engage with relevant newness and editorial context without manufactured urgency." },
    ],
    execution: integration.state,
  };
}
