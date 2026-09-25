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

export type PaidMediaChange = {
  provider: string;
  accountId: string;
  campaignId?: string;
  action: "create_campaign" | "pause_campaign" | "enable_campaign" | "set_budget";
  payload: Record<string, unknown>;
  approvedBy: string;
  approvedAt: string;
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
  if (change.action === "set_budget") {
    const budget = Number(change.payload.budget);
    if (!Number.isFinite(budget) || budget <= 0) throw new Error("Budget change requires a positive budget");
  }
}
