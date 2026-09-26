export type PaidMediaMetricSnapshot = {
  provider: string;
  accountId: string;
  campaignId: string;
  spend: number;
  conversions: number;
  revenue: number;
  currency: string;
  measuredAt: string;
};

export type PaidMediaCommercialEvidence = {
  productGid: string;
  advertisingEligibility: "eligible" | "blocked" | "not_ready";
  commercialState: string;
  stale: boolean;
  evaluatedAt: string;
  maxBreakEvenCac: number | null;
  maxCacAtTargetMargin: number | null;
  breakEvenRoas: number | null;
  targetMarginRoasFloor: number | null;
  policyFingerprint: string;
};

export type PaidMediaChange = {
  provider: string;
  accountId: string;
  campaignId?: string;
  action: "create_campaign" | "pause_campaign" | "enable_campaign" | "set_budget";
  payload: Record<string, unknown>;
  approvedBy: string;
  approvedAt: string;
  commercialEvidence: PaidMediaCommercialEvidence[];
};

export interface PaidMediaAdapter {
  readonly provider: string;
  readonly connected: boolean;
  readPerformance(): Promise<PaidMediaMetricSnapshot[]>;
  executeApprovedChange(change: PaidMediaChange): Promise<{ externalId?: string; status: string }>;
}

export class DisabledPaidMediaAdapter implements PaidMediaAdapter {
  readonly provider = "none";
  readonly connected = false;

  async readPerformance(): Promise<PaidMediaMetricSnapshot[]> {
    return [];
  }

  async executeApprovedChange(_change: PaidMediaChange): Promise<{ status: string }> {
    throw new Error(
      "Paid-media execution is disabled. Connect an approved provider and use an explicit human-approved change.",
    );
  }
}

export function assertApprovedPaidMediaChange(change: PaidMediaChange): void {
  if (!change.approvedBy?.trim()) throw new Error("Paid-media change requires approvedBy");
  if (!change.approvedAt || Number.isNaN(Date.parse(change.approvedAt))) {
    throw new Error("Paid-media change requires a valid approvedAt timestamp");
  }
  if (!change.accountId?.trim()) throw new Error("Paid-media change requires accountId");

  if (!Array.isArray(change.commercialEvidence) || change.commercialEvidence.length === 0) {
    throw new Error("Paid-media change requires product-level commercial evidence.");
  }

  const now = Date.now();
  for (const evidence of change.commercialEvidence) {
    if (!evidence.productGid?.startsWith("gid://shopify/Product/")) {
      throw new Error("Commercial evidence must reference a Shopify product GID.");
    }
    if (evidence.stale) {
      throw new Error(`Commercial evidence is stale for ${evidence.productGid}.`);
    }
    if (evidence.advertisingEligibility !== "eligible") {
      throw new Error(`Advertising is not commercially eligible for ${evidence.productGid}.`);
    }
    if (!evidence.policyFingerprint?.trim()) {
      throw new Error(`Commercial evidence is missing policy fingerprint for ${evidence.productGid}.`);
    }
    const evaluatedAt = Date.parse(evidence.evaluatedAt);
    if (Number.isNaN(evaluatedAt)) {
      throw new Error(`Commercial evidence has invalid evaluatedAt for ${evidence.productGid}.`);
    }
    if (now - evaluatedAt > 24 * 60 * 60 * 1000) {
      throw new Error(`Commercial evidence is older than 24 hours for ${evidence.productGid}.`);
    }
    if (
      evidence.maxBreakEvenCac === null ||
      !Number.isFinite(evidence.maxBreakEvenCac) ||
      evidence.maxBreakEvenCac <= 0
    ) {
      throw new Error(`Commercial evidence has no positive break-even CAC for ${evidence.productGid}.`);
    }
    if (
      evidence.maxCacAtTargetMargin === null ||
      !Number.isFinite(evidence.maxCacAtTargetMargin) ||
      evidence.maxCacAtTargetMargin <= 0
    ) {
      throw new Error(`Commercial evidence has no positive target-margin CAC ceiling for ${evidence.productGid}.`);
    }
  }

  if (change.action === "set_budget") {
    const budget = Number(change.payload.budget);
    if (!Number.isFinite(budget) || budget <= 0) {
      throw new Error("Budget change requires a positive budget.");
    }
  }
}
