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

  const queueHealthy = queue.deadLetterJobs === 0;
  const ok = preflight.ready && database && queueHealthy;
  return Response.json(
    {
      ok,
      mode: preflight.mode,
      database,
      queue,
      queueHealthy,
    },
    {
      status: ok ? 200 : 503,
      headers: { "Cache-Control": "no-store" },
    },
  );
};
