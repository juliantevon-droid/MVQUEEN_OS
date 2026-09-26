CREATE TABLE "ProductCommercialHealthState" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "sourceFingerprint" TEXT NOT NULL,
    "policyFingerprint" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "advertisingEligibility" TEXT NOT NULL,
    "maxBreakEvenCac" DOUBLE PRECISION,
    "breakEvenRoas" DOUBLE PRECISION,
    "targetRoas" DOUBLE PRECISION,
    "contributionAfterTargetCac" DOUBLE PRECISION,
    "contributionMarginAfterTargetCac" DOUBLE PRECISION,
    "stale" BOOLEAN NOT NULL DEFAULT false,
    "evaluatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "ProductCommercialHealthState_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "ProductCommercialHealthState_shop_productGid_key"
ON "ProductCommercialHealthState"("shop", "productGid");

CREATE INDEX "ProductCommercialHealthState_shop_state_stale_idx"
ON "ProductCommercialHealthState"("shop", "state", "stale");

CREATE TABLE "ProductCommercialHealthSnapshot" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "sourceFingerprint" TEXT NOT NULL,
    "policyFingerprint" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "advertisingEligibility" TEXT NOT NULL,
    "maxBreakEvenCac" DOUBLE PRECISION,
    "breakEvenRoas" DOUBLE PRECISION,
    "targetRoas" DOUBLE PRECISION,
    "contributionAfterTargetCac" DOUBLE PRECISION,
    "contributionMarginAfterTargetCac" DOUBLE PRECISION,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ProductCommercialHealthSnapshot_pkey" PRIMARY KEY ("id")
);

CREATE INDEX "ProductCommercialHealthSnapshot_shop_productGid_createdAt_idx"
ON "ProductCommercialHealthSnapshot"("shop", "productGid", "createdAt");

CREATE INDEX "ProductCommercialHealthSnapshot_shop_state_createdAt_idx"
ON "ProductCommercialHealthSnapshot"("shop", "state", "createdAt");
