import assert from "node:assert/strict";
import { buildCommercialHealth } from "./commercial-health";
import { buildReleaseGate } from "./release-gate";
import { assertApprovedPaidMediaChange } from "./paid-media-adapter";
import type { CommercialConfigResolution } from "./commercial-config";

const policy: CommercialConfigResolution = {
  config: {
    paymentRate: 0.03,
    paymentFixed: 0.30,
    returnReserveRate: 0.05,
    targetContributionMarginRate: 0.20,
    targetCac: 15,
    inboundShippingDefault: 5,
    currency: "USD",
  },
  missing: [],
};

const healthy = buildCommercialHealth(
  { sellingPrice: 100, unitCost: 20, inboundShipping: null },
  policy,
);
assert.equal(healthy.state, "healthy");
assert.equal(healthy.advertisingEligibility, "eligible");
assert.equal(healthy.maxBreakEvenCac, 66.7);
assert.equal(healthy.maxCacAtTargetMargin, 46.7);
assert.equal(healthy.contributionAfterTargetCac, 51.7);
assert.equal(healthy.contributionMarginAfterTargetCac, 0.517);

const thin = buildCommercialHealth(
  { sellingPrice: 50, unitCost: 20, inboundShipping: null },
  policy,
);
assert.equal(thin.state, "thin");
assert.equal(thin.advertisingEligibility, "blocked");

const blocked = buildCommercialHealth(
  { sellingPrice: 35, unitCost: 20, inboundShipping: null },
  policy,
);
assert.equal(blocked.state, "blocked");
assert.equal(blocked.advertisingEligibility, "blocked");

const missingCost = buildCommercialHealth(
  { sellingPrice: 100, unitCost: null, inboundShipping: null },
  policy,
);
assert.equal(missingCost.state, "needs_cost");
assert.equal(missingCost.advertisingEligibility, "not_ready");

const reviewGate = buildReleaseGate({
  issues: [
    {
      productGid: "gid://shopify/Product/1",
      title: "Fixture",
      severity: "warning",
      code: "short_description_missing",
      message: "warning",
    },
  ],
  commercialHealth: healthy,
});
assert.equal(reviewGate.state, "review");
assert.equal(reviewGate.publishEligible, true);
assert.equal(reviewGate.advertisingEligible, true);

const blockedGate = buildReleaseGate({
  issues: [
    {
      productGid: "gid://shopify/Product/1",
      title: "Fixture",
      severity: "blocker",
      code: "unit_cost_missing",
      message: "blocker",
    },
  ],
  commercialHealth: missingCost,
});
assert.equal(blockedGate.state, "blocked");
assert.equal(blockedGate.publishEligible, false);
assert.equal(blockedGate.advertisingEligible, false);

const approvedChange = {
  provider: "fixture",
  accountId: "acct-1",
  action: "set_budget" as const,
  payload: { budget: 25 },
  approvedBy: "owner",
  approvedAt: new Date().toISOString(),
  commercialEvidence: [
    {
      productGid: "gid://shopify/Product/1",
      advertisingEligibility: "eligible" as const,
      commercialState: "healthy",
      stale: false,
      evaluatedAt: new Date().toISOString(),
      maxBreakEvenCac: 66.7,
      maxCacAtTargetMargin: 46.7,
      breakEvenRoas: healthy.breakEvenRoas,
      targetMarginRoasFloor: healthy.targetMarginRoasFloor,
      policyFingerprint: "fixture-policy",
    },
  ],
};
assert.doesNotThrow(() => assertApprovedPaidMediaChange(approvedChange));

assert.throws(
  () =>
    assertApprovedPaidMediaChange({
      ...approvedChange,
      commercialEvidence: [
        {
          ...approvedChange.commercialEvidence[0],
          stale: true,
        },
      ],
    }),
  /stale/i,
);

assert.throws(
  () =>
    assertApprovedPaidMediaChange({
      ...approvedChange,
      commercialEvidence: [
        {
          ...approvedChange.commercialEvidence[0],
          advertisingEligibility: "blocked",
        },
      ],
    }),
  /not commercially eligible/i,
);

console.log("enterprise commercial-health and paid-media gate tests passed");
