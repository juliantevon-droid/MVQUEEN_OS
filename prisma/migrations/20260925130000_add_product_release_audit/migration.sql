-- Enterprise release ledger for approved canonical product publications.
CREATE TABLE "ProductReleaseAudit" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "contentFingerprint" TEXT NOT NULL,
    "actor" TEXT NOT NULL,
    "decision" TEXT NOT NULL,
    "operation" TEXT NOT NULL,
    "result" TEXT NOT NULL,
    "error" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "ProductReleaseAudit_shop_contentFingerprint_operation_result_idx"
ON "ProductReleaseAudit"("shop", "contentFingerprint", "operation", "result");

CREATE INDEX "ProductReleaseAudit_shop_productGid_createdAt_idx"
ON "ProductReleaseAudit"("shop", "productGid", "createdAt");

CREATE INDEX "ProductReleaseAudit_result_createdAt_idx"
ON "ProductReleaseAudit"("result", "createdAt");
