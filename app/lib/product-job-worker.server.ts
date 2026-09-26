import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { processProductJob } from "./product-processor";

const RECONCILE_QUERY = "#graphql\nquery MVQueenRecentProducts($first: Int!, $after: String, $query: String!) { products(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) { nodes { id updatedAt } pageInfo { hasNextPage endCursor } } }";

function envInt(name: string, fallback: number, min: number, max: number): number {
  const parsed = Number(process.env[name] ?? "");
  if (!Number.isFinite(parsed)) return fallback;
  return Math.max(min, Math.min(max, Math.floor(parsed)));
}

function retryDelayMs(attempts: number): number {
  const baseSeconds = envInt("MVQ_PRODUCT_RETRY_BASE_SECONDS", 30, 5, 3600);
  const maxMinutes = envInt("MVQ_PRODUCT_RETRY_MAX_MINUTES", 60, 1, 1440);
  const exponent = Math.max(0, attempts - 1);
  return Math.min(baseSeconds * 1000 * Math.pow(2, exponent), maxMinutes * 60_000);
}

function retryReady(job: { attempts: number; startedAt: Date | null }, now: number): boolean {
  const started = job.startedAt?.getTime() ?? 0;
  return started + retryDelayMs(job.attempts) <= now;
}


export async function recordProductWorkerHeartbeat(
  state: "continuous" | "fallback" | "stopping" | "stopped" | "error",
  details?: Record<string, unknown>,
) {
  return prisma.runtimeHeartbeat.upsert({
    where: { name: "product-worker" },
    update: {
      state,
      detailsJson: details ? JSON.stringify(details) : null,
    },
    create: {
      name: "product-worker",
      state,
      detailsJson: details ? JSON.stringify(details) : null,
    },
  });
}

export async function recoverStaleProductJobs() {
  const staleMinutes = envInt("MVQ_PRODUCT_STALE_MINUTES", 10, 2, 120);
  const cutoff = new Date(Date.now() - staleMinutes * 60_000);
  return prisma.productJob.updateMany({
    where: {
      status: { in: ["processing", "leased"] },
      startedAt: { lt: cutoff },
    },
    data: {
      status: "received",
      error: "Recovered stale processing lease",
      startedAt: null,
    },
  });
}

export async function reconcileRecentShopifyProducts() {
  if (process.env.MVQ_PRODUCT_RECONCILE_ENABLED !== "true") {
    return { shops: 0, discovered: 0, scanned: 0 };
  }

  const lookbackMinutes = envInt("MVQ_PRODUCT_RECONCILE_LOOKBACK_MINUTES", 20, 5, 1440);
  const first = envInt("MVQ_PRODUCT_RECONCILE_PAGE_SIZE", 100, 10, 250);
  const maxPages = envInt("MVQ_PRODUCT_RECONCILE_MAX_PAGES", 20, 1, 100);
  const since = new Date(Date.now() - lookbackMinutes * 60_000).toISOString();
  const sessions = await prisma.session.findMany({
    where: { isOnline: false },
    select: { shop: true },
    distinct: ["shop"],
  });

  let discovered = 0;
  let scanned = 0;

  for (const { shop } of sessions) {
    try {
      const { admin } = await unauthenticated.admin(shop);
      let after: string | null = null;

      for (let page = 0; page < maxPages; page += 1) {
        const response = await admin.graphql(RECONCILE_QUERY, {
          variables: {
            first,
            after,
            query: "updated_at:>'" + since + "'",
          },
        });
        const body = await response.json();
        const connection = body.data?.products;
        const nodes = connection?.nodes ?? [];
        scanned += nodes.length;

        for (const product of nodes) {
          if (!product?.id || !product?.updatedAt) continue;
          const eventKey = "reconcile:" + product.id + ":" + product.updatedAt;
          const existing = await prisma.productJob.findUnique({
            where: { eventKey },
            select: { id: true },
          });
          if (existing) continue;

          await prisma.productJob.create({
            data: {
              shop,
              productGid: product.id,
              eventKey,
              topic: "PRODUCT_RECONCILE",
              status: "received",
            },
          });
          discovered += 1;
        }

        if (!connection?.pageInfo?.hasNextPage) break;
        after = connection.pageInfo.endCursor ?? null;
        if (!after) break;
      }
    } catch (error) {
      console.error("MVQueen product reconciliation failed for", shop, error);
    }
  }

  return { shops: sessions.length, discovered, scanned };
}

async function markExhaustedJobs(maxAttempts: number) {
  return prisma.productJob.updateMany({
    where: {
      status: "failed",
      attempts: { gte: maxAttempts },
    },
    data: {
      status: "dead_letter",
      completedAt: new Date(),
    },
  });
}

export async function processProductJobBatch() {
  const batchSize = envInt("MVQ_PRODUCT_WORKER_BATCH_SIZE", 10, 1, 50);
  const maxAttempts = envInt("MVQ_PRODUCT_MAX_ATTEMPTS", 5, 1, 12);
  const now = Date.now();

  await recoverStaleProductJobs();
  await markExhaustedJobs(maxAttempts);

  const [received, failed] = await Promise.all([
    prisma.productJob.findMany({
      where: { status: "received" },
      orderBy: { receivedAt: "asc" },
      take: batchSize,
      select: { id: true, attempts: true, startedAt: true },
    }),
    prisma.productJob.findMany({
      where: {
        status: "failed",
        attempts: { lt: maxAttempts },
      },
      orderBy: { startedAt: "asc" },
      take: batchSize,
      select: { id: true, attempts: true, startedAt: true },
    }),
  ]);

  const retryable = failed.filter((job) => retryReady(job, now));
  const selected = [...received, ...retryable]
    .slice(0, batchSize);

  let completed = 0;
  let failedCount = 0;
  for (const job of selected) {
    const claim = await prisma.productJob.updateMany({
      where: {
        id: job.id,
        status: { in: ["received", "failed"] },
      },
      data: {
        status: "leased",
        startedAt: new Date(),
      },
    });
    if (claim.count !== 1) continue;

    try {
      await processProductJob(job.id);
      completed += 1;
    } catch {
      failedCount += 1;
      const current = await prisma.productJob.findUnique({
        where: { id: job.id },
        select: { attempts: true },
      });
      if ((current?.attempts ?? 0) >= maxAttempts) {
        await prisma.productJob.update({
          where: { id: job.id },
          data: { status: "dead_letter", completedAt: new Date() },
        });
      }
    }
  }

  const [receivedCount, processingCount, failedQueue, deadLetterCount] = await Promise.all([
    prisma.productJob.count({ where: { status: "received" } }),
    prisma.productJob.count({ where: { status: "processing" } }),
    prisma.productJob.count({ where: { status: "failed" } }),
    prisma.productJob.count({ where: { status: "dead_letter" } }),
  ]);

  return {
    attempted: selected.length,
    completed,
    failed: failedCount,
    queue: {
      received: receivedCount,
      processing: processingCount,
      failed: failedQueue,
      deadLetter: deadLetterCount,
    },
  };
}

export async function runAlwaysOnProductWorker() {
  const reconciliation = await reconcileRecentShopifyProducts();
  const processing = await processProductJobBatch();
  return { reconciliation, processing };
}
