CREATE TABLE "RuntimeHeartbeat" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "detailsJson" TEXT,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "RuntimeHeartbeat_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "RuntimeHeartbeat_name_key" ON "RuntimeHeartbeat"("name");
CREATE INDEX "RuntimeHeartbeat_state_updatedAt_idx" ON "RuntimeHeartbeat"("state", "updatedAt");
