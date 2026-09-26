import type { CatalogAuditIssue } from "./catalog-audit";
import type { CommercialHealth } from "./commercial-health";

export type ReleaseGateState = "blocked" | "review" | "ready";

export type ReleaseGateDecision = {
  state: ReleaseGateState;
  publishEligible: boolean;
  advertisingEligible: boolean;
  blockers: string[];
  warnings: string[];
};

export function buildReleaseGate(args: {
  issues: CatalogAuditIssue[];
  commercialHealth: CommercialHealth;
}): ReleaseGateDecision {
  const blockers = args.issues
    .filter((issue) => issue.severity === "blocker")
    .map((issue) => issue.code);
  const warnings = args.issues
    .filter((issue) => issue.severity === "warning")
    .map((issue) => issue.code);

  if (
    args.commercialHealth.state === "needs_configuration" ||
    args.commercialHealth.state === "needs_cost" ||
    args.commercialHealth.state === "needs_price" ||
    args.commercialHealth.state === "invalid_inputs" ||
    args.commercialHealth.state === "blocked" ||
    args.commercialHealth.state === "thin"
  ) {
    blockers.push(`commercial_health:${args.commercialHealth.state}`);
  }

  const uniqueBlockers = Array.from(new Set(blockers));
  const uniqueWarnings = Array.from(new Set(warnings));

  return {
    state: uniqueBlockers.length ? "blocked" : uniqueWarnings.length ? "review" : "ready",
    publishEligible: uniqueBlockers.length === 0,
    advertisingEligible:
      uniqueBlockers.length === 0 &&
      args.commercialHealth.advertisingEligibility === "eligible",
    blockers: uniqueBlockers,
    warnings: uniqueWarnings,
  };
}
