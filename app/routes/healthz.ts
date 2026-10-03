import type { LoaderFunctionArgs } from "react-router";
import prisma from "../db.server";
import { productionPreflight } from "../lib/production-preflight";

export const loader = async (_args: LoaderFunctionArgs) => {
  const preflight = productionPreflight();
  let database = false;

  try {
    await prisma.$queryRaw`SELECT 1`;
    database = true;
  } catch {
    database = false;
  }

  let queue = {
    receivedJobs: 0,
    processingJobs: 0,
    failedJobs: 0,
    deadLetterJobs: 0,
  };

  if (database) {
    const [receivedJobs, processingJobs, failedJobs, deadLetterJobs] =
      await Promise.all([
        prisma.productJob.count({ where: { status: "received" } }),
        prisma.productJob.count({ where: { status: { in: ["leased", "processing"] } } }),
        prisma.productJob.count({ where: { status: "failed" } }),
        prisma.productJob.count({ where: { status: "dead_letter" } }),
      ]);
    queue = { receivedJobs, processingJobs, failedJobs, deadLetterJobs };
  }

  const continuousWorkerRequired =
    process.env.MVQ_PRODUCT_CONTINUOUS_WORKER_REQUIRED === "true";
  let workerHeartbeat: {
    state: string;
    updatedAt: Date;
  } | null = null;
  let webhookHeartbeat: {
    state: string;
    updatedAt: Date;
  } | null = null;

  if (database) {
    [workerHeartbeat, webhookHeartbeat] = await Promise.all([
      prisma.runtimeHeartbeat.findUnique({
        where: { name: "product-worker" },
        select: { state: true, updatedAt: true },
      }),
      prisma.runtimeHeartbeat.findUnique({
        where: { name: "product-webhooks" },
        select: { state: true, updatedAt: true },
      }),
    ]);
  }

  const heartbeatMaxAgeMs = 120_000;
  const workerHeartbeatFresh =
    !continuousWorkerRequired ||
    Boolean(
      workerHeartbeat?.state === "continuous" &&
      Date.now() - workerHeartbeat.updatedAt.getTime() <= heartbeatMaxAgeMs,
    );

  const webhookRequired =
    process.env.MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED === "true";
  const webhookAuditIntervalMs = Math.max(
    60_000,
    Math.min(
      86_400_000,
      Number(process.env.MVQ_PRODUCT_WEBHOOK_AUDIT_INTERVAL_MS ?? "300000") ||
        300000,
    ),
  );
  const webhookHeartbeatMaxAgeMs = Math.max(
    300_000,
    webhookAuditIntervalMs * 3,
  );
  const webhookHealthy =
    !webhookRequired ||
    Boolean(
      webhookHeartbeat?.state === "healthy" &&
      Date.now() - webhookHeartbeat.updatedAt.getTime() <=
        webhookHeartbeatMaxAgeMs,
    );

  const queueHealthy = queue.deadLetterJobs === 0;
  const ok =
    preflight.ready &&
    database &&
    queueHealthy &&
    workerHeartbeatFresh &&
    webhookHealthy;

  return Response.json(
    {
      ok,
      mode: preflight.mode,
      // Capabilities are non-secret booleans only; credentials are never returned.
      capabilities: preflight.capabilities,
      database,
      queue,
      queueHealthy,
      worker: {
        required: continuousWorkerRequired,
        fresh: workerHeartbeatFresh,
        state: workerHeartbeat?.state ?? "missing",
        lastSeenAt: workerHeartbeat?.updatedAt?.toISOString() ?? null,
      },
      webhooks: {
        required: webhookRequired,
        healthy: webhookHealthy,
        state: webhookHeartbeat?.state ?? "missing",
        lastCheckedAt: webhookHeartbeat?.updatedAt?.toISOString() ?? null,
      },
    },
    {
      status: ok ? 200 : 503,
      headers: { "Cache-Control": "no-store" },
    },
  );
};
