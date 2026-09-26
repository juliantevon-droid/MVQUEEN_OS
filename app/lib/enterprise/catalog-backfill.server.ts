import prisma from "../../db.server";
import { processProductJob } from "../product-processor";

type AdminClient = {
  graphql: (
    query: string,
    options?: { variables?: Record<string, unknown> },
  ) => Promise<Response>;
};

export type BackfillWriteMode = "dry_run" | "governed_write";

const BACKFILL_PAGE_QUERY = `#graphql
query MVQueenBackfillPage($first: Int!, $after: String) {
  products(first: $first, after: $after, sortKey: ID) {
    nodes { id }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
`;

function safeBatchSize(value: number | undefined): number {
  if (!Number.isFinite(value)) return 10;
  return Math.max(1, Math.min(50, Math.floor(value!)));
}

export async function createCatalogBackfillRun(args: {
  shop: string;
  requestedBy: string;
  reason: string;
  writeMode?: BackfillWriteMode;
}) {
  const reason = args.reason.trim();
  if (!reason) throw new Error("Backfill reason is required.");
  if (reason.length > 240) throw new Error("Backfill reason must be 240 characters or fewer.");

  const writeMode = args.writeMode ?? "dry_run";
  if (writeMode === "governed_write") {
    if (process.env.MVQ_WRITE_ENABLED !== "true") {
      throw new Error("Global Shopify write gate is disabled.");
    }
    if (process.env.MVQ_BACKFILL_WRITE_ENABLED !== "true") {
      throw new Error("Dedicated catalog-backfill write gate is disabled.");
    }
  }

  return prisma.catalogBackfillRun.create({
    data: {
      shop: args.shop,
      requestedBy: args.requestedBy,
      reason,
      writeMode,
      status: "scanning",
    },
  });
}

export async function scanNextCatalogBackfillPage(args: {
  admin: AdminClient;
  shop: string;
  runId: string;
}) {
  const run = await prisma.catalogBackfillRun.findUnique({
    where: { id: args.runId },
  });
  if (!run || run.shop !== args.shop) throw new Error("Backfill run not found.");
  if (run.status === "cancelled") throw new Error("Backfill run is cancelled.");
  if (run.scanComplete) return run;

  const response = await args.admin.graphql(BACKFILL_PAGE_QUERY, {
    variables: { first: 100, after: run.scanCursor },
  });
  const body = (await response.json()) as {
    data?: {
      products?: {
        nodes?: Array<{ id: string }>;
        pageInfo?: { hasNextPage?: boolean; endCursor?: string | null };
      } | null;
    };
  };
  const connection = body.data?.products;
  if (!connection) throw new Error("Shopify backfill scan returned no product connection.");

  const nodes = connection.nodes ?? [];
  if (nodes.length) {
    await prisma.$transaction(
      nodes.map((product) =>
        prisma.productJob.upsert({
          where: {
            eventKey: `backfill:${run.id}:${product.id}`,
          },
          update: {},
          create: {
            shop: run.shop,
            productGid: product.id,
            eventKey: `backfill:${run.id}:${product.id}`,
            topic: "CATALOG_BACKFILL",
            status: "received",
            backfillRunId: run.id,
          },
        }),
      ),
    );
  }

  const enqueuedJobs = await prisma.productJob.count({
    where: { backfillRunId: run.id },
  });
  const scanComplete = !connection.pageInfo?.hasNextPage;

  return prisma.catalogBackfillRun.update({
    where: { id: run.id },
    data: {
      scanCursor: connection.pageInfo?.endCursor ?? run.scanCursor,
      scanComplete,
      totalProducts: enqueuedJobs,
      enqueuedJobs,
      startedAt: run.startedAt ?? new Date(),
      status:
        scanComplete && enqueuedJobs === 0
          ? "completed"
          : scanComplete
            ? "queued"
            : "scanning",
      completedAt:
        scanComplete && enqueuedJobs === 0 ? new Date() : null,
    },
  });
}

async function refreshBackfillProgress(runId: string) {
  const run = await prisma.catalogBackfillRun.findUnique({ where: { id: runId } });
  if (!run) throw new Error("Backfill run not found.");

  const [enqueuedJobs, processedJobs, failedJobs, outstandingJobs] =
    await Promise.all([
      prisma.productJob.count({ where: { backfillRunId: runId } }),
      prisma.productJob.count({
        where: { backfillRunId: runId, status: "completed" },
      }),
      prisma.productJob.count({
        where: { backfillRunId: runId, status: "failed" },
      }),
      prisma.productJob.count({
        where: {
          backfillRunId: runId,
          status: { in: ["received", "processing"] },
        },
      }),
    ]);

  const finished = run.scanComplete && outstandingJobs === 0;
  const status = run.status === "cancelled"
    ? "cancelled"
    : finished
      ? failedJobs > 0
        ? "completed_with_errors"
        : "completed"
      : run.scanComplete
        ? "running"
        : "scanning";

  return prisma.catalogBackfillRun.update({
    where: { id: runId },
    data: {
      totalProducts: enqueuedJobs,
      enqueuedJobs,
      processedJobs,
      failedJobs,
      status,
      completedAt: finished ? (run.completedAt ?? new Date()) : null,
    },
  });
}

export async function processCatalogBackfillBatch(args: {
  runId: string;
  batchSize?: number;
}) {
  const run = await prisma.catalogBackfillRun.findUnique({
    where: { id: args.runId },
  });
  if (!run) throw new Error("Backfill run not found.");
  if (["cancelled", "completed", "completed_with_errors"].includes(run.status)) {
    return refreshBackfillProgress(run.id);
  }

  const governedWrite = run.writeMode === "governed_write";
  if (
    governedWrite &&
    (process.env.MVQ_WRITE_ENABLED !== "true" ||
      process.env.MVQ_BACKFILL_WRITE_ENABLED !== "true")
  ) {
    return prisma.catalogBackfillRun.update({
      where: { id: run.id },
      data: { status: "blocked_write_gate" },
    });
  }

  const jobs = await prisma.productJob.findMany({
    where: {
      backfillRunId: run.id,
      status: "received",
    },
    orderBy: { receivedAt: "asc" },
    take: safeBatchSize(args.batchSize),
    select: { id: true },
  });

  if (jobs.length && !run.startedAt) {
    await prisma.catalogBackfillRun.update({
      where: { id: run.id },
      data: { startedAt: new Date() },
    });
  }

  for (const job of jobs) {
    try {
      await processProductJob(job.id, {
        allowWrites: governedWrite,
      });
    } catch {
      // processProductJob owns the durable failed-job record.
    }
  }

  return refreshBackfillProgress(run.id);
}

export async function advanceCatalogBackfillRun(args: {
  admin: AdminClient;
  shop: string;
  runId: string;
  batchSize?: number;
}) {
  let run = await prisma.catalogBackfillRun.findUnique({
    where: { id: args.runId },
  });
  if (!run || run.shop !== args.shop) throw new Error("Backfill run not found.");
  if (run.status === "cancelled") return run;

  if (!run.scanComplete) {
    run = await scanNextCatalogBackfillPage({
      admin: args.admin,
      shop: args.shop,
      runId: run.id,
    });
  }

  if (run.status !== "completed") {
    run = await processCatalogBackfillBatch({
      runId: run.id,
      batchSize: args.batchSize,
    });
  }

  return run;
}

export async function cancelCatalogBackfillRun(args: {
  shop: string;
  runId: string;
}) {
  const run = await prisma.catalogBackfillRun.findUnique({
    where: { id: args.runId },
  });
  if (!run || run.shop !== args.shop) throw new Error("Backfill run not found.");
  if (["completed", "completed_with_errors"].includes(run.status)) return run;

  return prisma.catalogBackfillRun.update({
    where: { id: run.id },
    data: { status: "cancelled", completedAt: new Date() },
  });
}

export async function nextRunnableBackfillRun() {
  return prisma.catalogBackfillRun.findFirst({
    where: {
      status: { in: ["scanning", "queued", "running"] },
    },
    orderBy: { createdAt: "asc" },
  });
}
