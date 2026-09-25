CREATE TABLE "CommercialSettings" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "paymentRate" REAL,
    "paymentFixed" REAL,
    "returnReserveRate" REAL,
    "targetContributionMarginRate" REAL,
    "targetCac" REAL,
    "inboundShippingDefault" REAL,
    "currency" TEXT NOT NULL DEFAULT 'USD',
    "updatedBy" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

CREATE UNIQUE INDEX "CommercialSettings_shop_key"
ON "CommercialSettings"("shop");

CREATE TABLE "CommercialSettingsAudit" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "actor" TEXT NOT NULL,
    "snapshotJson" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "CommercialSettingsAudit_shop_createdAt_idx"
ON "CommercialSettingsAudit"("shop", "createdAt");
