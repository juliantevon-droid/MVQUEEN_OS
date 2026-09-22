-- CreateTable
CREATE TABLE "Session" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "isOnline" BOOLEAN NOT NULL DEFAULT false,
    "scope" TEXT,
    "expires" DATETIME,
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
    "refreshTokenExpires" DATETIME
);

-- CreateTable
CREATE TABLE "ProductAutomationState" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "lastAutomationUpdatedAt" DATETIME,
    "automationVersion" TEXT NOT NULL DEFAULT '1',
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "ProductJob" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shop" TEXT NOT NULL,
    "productGid" TEXT NOT NULL,
    "eventKey" TEXT NOT NULL,
    "topic" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'received',
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "error" TEXT,
    "receivedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "startedAt" DATETIME,
    "completedAt" DATETIME
);

-- CreateIndex
CREATE UNIQUE INDEX "ProductAutomationState_shop_productGid_key" ON "ProductAutomationState"("shop", "productGid");

-- CreateIndex
CREATE UNIQUE INDEX "ProductJob_eventKey_key" ON "ProductJob"("eventKey");

-- CreateIndex
CREATE INDEX "ProductAutomationState_shop_productGid_idx" ON "ProductAutomationState"("shop", "productGid");

-- CreateIndex
CREATE INDEX "ProductJob_shop_productGid_idx" ON "ProductJob"("shop", "productGid");

-- CreateIndex
CREATE INDEX "ProductJob_status_receivedAt_idx" ON "ProductJob"("status", "receivedAt");
