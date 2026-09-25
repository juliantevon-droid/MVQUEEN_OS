CREATE TABLE "CommercialSettings" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "paymentRate" DOUBLE PRECISION,
    "paymentFixed" DOUBLE PRECISION,
    "returnReserveRate" DOUBLE PRECISION,
    "targetContributionMarginRate" DOUBLE PRECISION,
    "targetCac" DOUBLE PRECISION,
    "inboundShippingDefault" DOUBLE PRECISION,
    "currency" TEXT NOT NULL DEFAULT 'USD',
    "updatedBy" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "CommercialSettings_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "CommercialSettings_shop_key"
ON "CommercialSettings"("shop");

CREATE TABLE "CommercialSettingsAudit" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "actor" TEXT NOT NULL,
    "snapshotJson" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "CommercialSettingsAudit_pkey" PRIMARY KEY ("id")
);

CREATE INDEX "CommercialSettingsAudit_shop_createdAt_idx"
ON "CommercialSettingsAudit"("shop", "createdAt");
