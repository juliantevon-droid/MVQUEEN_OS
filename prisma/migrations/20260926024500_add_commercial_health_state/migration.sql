CREATE TABLE "ProductCommercialHealthState" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "sourceFingerprint" TEXT NOT NULL,
    "policyFingerprint" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "advertisingEligibility" TEXT NOT NULL,
    "maxBreakEvenCac" REAL,
    "breakEvenRoas" REAL,
    "targetRoas" REAL,
    "contributionAfterTargetCac" REAL,
    "contributionMarginAfterTargetCac" REAL,
    "stale" BOOLEAN NOT NULL DEFAULT false,
    "evaluatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

CREATE UNIQUE INDEX "ProductCommercialHealthState_shop_productGid_key"
ON "ProductCommercialHealthState"("shop", "productGid");

CREATE INDEX "ProductCommercialHealthState_shop_state_stale_idx"
ON "ProductCommercialHealthState"("shop", "state", "stale");

CREATE TABLE "ProductCommercialHealthSnapshot" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "sourceFingerprint" TEXT NOT NULL,
    "policyFingerprint" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "advertisingEligibility" TEXT NOT NULL,
    "maxBreakEvenCac" REAL,
    "breakEvenRoas" REAL,
    "targetRoas" REAL,
    "contributionAfterTargetCac" REAL,
    "contributionMarginAfterTargetCac" REAL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "ProductCommercialHealthSnapshot_shop_productGid_createdAt_idx"
ON "ProductCommercialHealthSnapshot"("shop", "productGid", "createdAt");

CREATE INDEX "ProductCommercialHealthSnapshot_shop_state_createdAt_idx"
ON "ProductCommercialHealthSnapshot"("shop", "state", "createdAt");
