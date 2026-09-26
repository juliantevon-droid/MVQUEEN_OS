import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { processProductJob } from "./product-processor";

const RECONCILE_QUERY = "#graphql\nquery MVQueenRecentProducts($first: Int!, $query: String!) { products(first: $first, query: $query, sortKey: UPDATED_AT) { nodes { id updatedAt } } }";

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

export async function recoverStaleProductJobs() {
  const staleMinutes = envInt("MVQ_PRODUCT_STALE_MINUTES", 10, 2, 120);
  const cutoff = new Date(Date.now() - staleMinutes * 60_000);
  return prisma.productJob.updateMany({
    where: {
      status: "processing",
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
    return { shops: 0, discovered: 0 };
  }

  const lookbackMinutes = envInt("MVQ_PRODUCT_RECONCILE_LOOKBACK_MINUTES", 20, 5, 1440);
  const first = envInt("MVQ_PRODUCT_RECONCILE_PAGE_SIZE", 100, 10, 250);
  const since = new Date(Date.now() - lookbackMinutes * 60_000).toISOString();
  const sessions = await prisma.session.findMany({
    where: { isOnline: false },
    select: { shop: true },
    distinct: ["shop"],
  });

  let discovered = 0;
  for (const { shop } of sessions) {
    try {
      const { admin } = await unauthenticated.admin(shop);
      const response = await admin.graphql(RECONCILE_QUERY, {
        variables: {
          first,
          query: "updated_at:>='" + since + "'",
        },
      });
      const body = await response.json();
      const nodes = body.data?.products?.nodes ?? [];

      for (const product of nodes) {
        if (!product?.id || !product?.updatedAt) continue;
        const eventKey = "reconcile:" + product.id + ":" + product.updatedAt;
        const result = await prisma.productJob.upsert({
          where: { eventKey },
          update: {},
          create: {
            shop,
            productGid: product.id,
            eventKey,
            topic: "PRODUCT_RECONCILE",
            status: "received",
          },
        });
        if (result.receivedAt.getTime() >= Date.now() - 60_000) discovered += 1;
      }
    } catch (error) {
      console.error("MVQueen product reconciliation failed for", shop, error);
    }
  }

  return { shops: sessions.length, discovered };
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
