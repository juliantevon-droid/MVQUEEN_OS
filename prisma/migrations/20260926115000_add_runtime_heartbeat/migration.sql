CREATE TABLE "RuntimeHeartbeat" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "detailsJson" TEXT,
    "updatedAt" DATETIME NOT NULL
);

CREATE UNIQUE INDEX "RuntimeHeartbeat_name_key" ON "RuntimeHeartbeat"("name");
CREATE INDEX "RuntimeHeartbeat_state_updatedAt_idx" ON "RuntimeHeartbeat"("state", "updatedAt");
