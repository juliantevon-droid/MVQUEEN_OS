CREATE TABLE "Session" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "isOnline" BOOLEAN NOT NULL DEFAULT false,
    "scope" TEXT,
    "expires" TIMESTAMP(3),
    "accessToken" TEXT NOT NULL,
    "userId" BIGINT,
    "firstName" TEXT,
    "lastName" TEXT,
    "email" TEXT,
    "accountOwner" BOOLEAN NOT NULL DEFAULT false,
    "locale" TEXT,
    "collaborator" BOOLEAN DEFAULT false,
    "emailVerified" BOOLEAN DEFAULT false,
    "refreshToken" TEXT,
    "refreshTokenExpires" TIMESTAMP(3),

    CONSTRAINT "Session_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "ProductAutomationState" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "sourceFingerprint" TEXT,
    "lastAutomationUpdatedAt" TIMESTAMP(3),
    "automationVersion" TEXT NOT NULL DEFAULT 'mvq-catalog-v1',
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "ProductAutomationState_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "ProductJob" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "eventKey" TEXT NOT NULL,
    "topic" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'received',
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "error" TEXT,
    "receivedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "startedAt" TIMESTAMP(3),
    "completedAt" TIMESTAMP(3),

    CONSTRAINT "ProductJob_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "ProductReleaseAudit" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "contentFingerprint" TEXT NOT NULL,
    "actor" TEXT NOT NULL,
    "decision" TEXT NOT NULL,
    "operation" TEXT NOT NULL,
    "result" TEXT NOT NULL,
    "error" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ProductReleaseAudit_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "ProductAutomationState_shop_productGid_key"
ON "ProductAutomationState"("shop", "productGid");

CREATE UNIQUE INDEX "ProductJob_eventKey_key"
ON "ProductJob"("eventKey");

CREATE INDEX "ProductJob_shop_productGid_idx"
ON "ProductJob"("shop", "productGid");

CREATE INDEX "ProductJob_status_receivedAt_idx"
ON "ProductJob"("status", "receivedAt");

CREATE INDEX "ProductReleaseAudit_shop_contentFingerprint_operation_result_idx"
ON "ProductReleaseAudit"("shop", "contentFingerprint", "operation", "result");

CREATE INDEX "ProductReleaseAudit_shop_productGid_createdAt_idx"
ON "ProductReleaseAudit"("shop", "productGid", "createdAt");

CREATE INDEX "ProductReleaseAudit_result_createdAt_idx"
ON "ProductReleaseAudit"("result", "createdAt");
