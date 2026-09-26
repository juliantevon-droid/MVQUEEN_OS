ALTER TABLE "ProductJob" ADD COLUMN "backfillRunId" TEXT;

CREATE INDEX "ProductJob_backfillRunId_status_receivedAt_idx"
ON "ProductJob"("backfillRunId", "status", "receivedAt");

CREATE TABLE "CatalogBackfillRun" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "reason" TEXT NOT NULL,
    "requestedBy" TEXT NOT NULL,
    "writeMode" TEXT NOT NULL DEFAULT 'dry_run',
    "status" TEXT NOT NULL DEFAULT 'scanning',
    "scanCursor" TEXT,
    "scanComplete" BOOLEAN NOT NULL DEFAULT false,
    "totalProducts" INTEGER NOT NULL DEFAULT 0,
    "enqueuedJobs" INTEGER NOT NULL DEFAULT 0,
    "processedJobs" INTEGER NOT NULL DEFAULT 0,
    "failedJobs" INTEGER NOT NULL DEFAULT 0,
    "startedAt" DATETIME,
    "completedAt" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

CREATE INDEX "CatalogBackfillRun_shop_status_createdAt_idx"
ON "CatalogBackfillRun"("shop", "status", "createdAt");

CREATE INDEX "CatalogBackfillRun_status_createdAt_idx"
ON "CatalogBackfillRun"("status", "createdAt");
