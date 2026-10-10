import prisma from "../db.server";
import { registerWebhooks, unauthenticated } from "../shopify.server";
import { AUTOMATION_VERSION, processProductJob } from "./product-processor";
import { createCorrelationId, errorFields, logMvqueenEvent } from "./enterprise/observability.server";

const RECONCILE_QUERY = "#graphql\nquery MVQueenRecentProducts($first: Int!, $after: String, $query: String!) { products(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) { nodes { id updatedAt } pageInfo { hasNextPage endCursor } } }";

const PRODUCT_WEBHOOK_AUDIT_QUERY = `#graphql
query MVQueenProductWebhookAudit {
  webhookSubscriptions(first: 50) {
    nodes {
      id
      topic
      uri
    }
  }
}`;


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

export async function recordProductWebhookHeartbeat(
  state: "healthy" | "degraded" | "error",
  details?: Record<string, unknown>,
) {
  return prisma.runtimeHeartbeat.upsert({
    where: { name: "product-webhooks" },
    update: {
      state,
      detailsJson: details ? JSON.stringify(details) : null,
    },
    create: {
      name: "product-webhooks",
      state,
      detailsJson: details ? JSON.stringify(details) : null,
    },
  });
}

export async function auditProductWebhookSubscriptions() {
  const sessions = await prisma.session.findMany({
    where: { isOnline: false },
    select: { shop: true },
    distinct: ["shop"],
  });

  const results: Array<{
    shop: string;
    productsCreate: boolean;
    productsUpdate: boolean;
    subscriptions: number;
  }> = [];

  for (const { shop } of sessions) {
    try {
      const { admin } = await unauthenticated.admin(shop);
      const response: Response = await admin.graphql(PRODUCT_WEBHOOK_AUDIT_QUERY);
      const body = (await response.json()) as {
        data?: {
          webhookSubscriptions?: {
            nodes?: Array<{
              id?: string | null;
              topic?: string | null;
              uri?: string | null;
            }>;
          } | null;
        };
      };

      const nodes = body.data?.webhookSubscriptions?.nodes ?? [];
      const productsCreate = nodes.some(
        (node) =>
          node.topic === "PRODUCTS_CREATE" &&
          node.uri?.includes("/webhooks/products/create"),
      );
      const productsUpdate = nodes.some(
        (node) =>
          node.topic === "PRODUCTS_UPDATE" &&
          node.uri?.includes("/webhooks/products/update"),
      );

      const result = {
        shop,
        productsCreate,
        productsUpdate,
        subscriptions: nodes.length,
      };
      results.push(result);

      logMvqueenEvent(
        "product.webhooks.audit",
        result,
        productsCreate && productsUpdate ? "info" : "error",
      );
    } catch (error) {
      logMvqueenEvent(
        "product.webhooks.audit_failed",
        { shop, ...errorFields(error) },
        "error",
      );
      results.push({
        shop,
        productsCreate: false,
        productsUpdate: false,
        subscriptions: 0,
      });
    }
  }

  return results;
}

export async function ensureProductWebhookSubscriptions() {
  const initial = await auditProductWebhookSubscriptions();
  const missing = initial.filter(
    (result) => !result.productsCreate || !result.productsUpdate,
  );

  for (const result of missing) {
    try {
      const { session } = await unauthenticated.admin(result.shop);
      const registration = await registerWebhooks({ session });
      logMvqueenEvent(
        "product.webhooks.repair_requested",
        {
          shop: result.shop,
          registration:
            registration === undefined ? "completed" : registration,
        },
        "info",
      );
    } catch (error) {
      logMvqueenEvent(
        "product.webhooks.repair_failed",
        { shop: result.shop, ...errorFields(error) },
        "error",
      );
    }
  }

  const final = missing.length
    ? await auditProductWebhookSubscriptions()
    : initial;
  const healthy =
    final.length > 0 &&
    final.every((result) => result.productsCreate && result.productsUpdate);

  await recordProductWebhookHeartbeat(
    healthy ? "healthy" : "degraded",
    {
      shops: final.length,
      missing: final
        .filter((result) => !result.productsCreate || !result.productsUpdate)
        .map((result) => ({
          shop: result.shop,
          productsCreate: result.productsCreate,
          productsUpdate: result.productsUpdate,
        })),
    },
  );

  logMvqueenEvent(
    "product.webhooks.ensure",
    {
      healthy,
      shops: final.length,
      repairedShops: missing.map((result) => result.shop),
    },
    healthy ? "info" : "error",
  );

  return { healthy, audits: final };
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

      // A policy release also applies to older products outside the recent
      // update window. Reuse the governed worker and one idempotent event per
      // version; never infer completion from an empty recent-update queue.
      const outdated = await prisma.productAutomationState.findMany({
        where: { shop, automationVersion: { not: AUTOMATION_VERSION } },
        orderBy: { productGid: "asc" },
        take: first * maxPages,
        select: { productGid: true },
      });
      for (const product of outdated) {
        const eventKey = `policy-refresh:${AUTOMATION_VERSION}:${product.productGid}`;
        const existing = await prisma.productJob.findUnique({
          where: { eventKey }, select: { id: true, status: true },
        });
        if (existing?.status === "completed") {
          // During a rolling release an older replica can complete a new
          // version's job. The outdated automation state proves the policy
          // was not applied, so resume the same audit record atomically.
          const resumed = await prisma.productJob.updateMany({
            where: { id: existing.id, status: "completed" },
            data: { status: "received", attempts: 0, startedAt: null,
              completedAt: null, error: null },
          });
          discovered += resumed.count;
          continue;
        }
        if (existing) continue;
        await prisma.productJob.upsert({
          where: { eventKey }, update: {},
          create: { shop, productGid: product.productGid, eventKey,
            topic: "PRODUCT_POLICY_REFRESH", status: "received" },
        });
        discovered += 1;
      }

      for (let page = 0; page < maxPages; page += 1) {
        const response: Response = await admin.graphql(RECONCILE_QUERY, {
          variables: {
            first,
            after,
            query: "updated_at:>'" + since + "'",
          },
        });
        const body = (await response.json()) as {
          data?: {
            products?: {
              nodes?: Array<{ id?: string | null; updatedAt?: string | null }>;
              pageInfo?: {
                hasNextPage?: boolean;
                endCursor?: string | null;
              };
            } | null;
          };
        };
        const connection = body.data?.products;
        const nodes: Array<{ id?: string | null; updatedAt?: string | null }> =
          connection?.nodes ?? [];
        scanned += nodes.length;

        for (const product of nodes) {
          if (!product?.id || !product?.updatedAt) continue;
          const eventKey = "reconcile:" + AUTOMATION_VERSION + ":" + product.id + ":" + product.updatedAt;
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
      logMvqueenEvent(
        "product.reconciliation.failed",
        { shop, ...errorFields(error) },
        "error",
      );
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
  const correlationId = createCorrelationId("product-worker");
  const batchSize = envInt("MVQ_PRODUCT_WORKER_BATCH_SIZE", 10, 1, 50);
  const maxAttempts = envInt("MVQ_PRODUCT_MAX_ATTEMPTS", 5, 1, 12);
  const now = Date.now();

  await recoverStaleProductJobs();

  // Standby mode must not consume Shopify events. Webhooks may continue to
  // enqueue durable jobs while live writes are disabled; preserving those jobs
  // lets production activation resume from the real event queue instead of
  // silently completing them as dry-runs.
  if (process.env.MVQ_WRITE_ENABLED !== "true") {
    const [receivedCount, processingCount, failedQueue, deadLetterCount] =
      await Promise.all([
        prisma.productJob.count({ where: { status: "received" } }),
        prisma.productJob.count({ where: { status: { in: ["leased", "processing"] } } }),
        prisma.productJob.count({ where: { status: "failed" } }),
        prisma.productJob.count({ where: { status: "dead_letter" } }),
      ]);

    const result = {
      attempted: 0,
      completed: 0,
      failed: 0,
      paused: true,
      queue: {
        received: receivedCount,
        processing: processingCount,
        failed: failedQueue,
        deadLetter: deadLetterCount,
      },
    };

    logMvqueenEvent("product.worker.paused", { correlationId, ...result }, "info");
    return result;
  }

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

  const result = {
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

  logMvqueenEvent("product.worker.batch", { correlationId, ...result }, deadLetterCount > 0 ? "warn" : "info");
  return result;
}

export async function runAlwaysOnProductWorker() {
  const reconciliation = await reconcileRecentShopifyProducts();
  const processing = await processProductJobBatch();
  return { reconciliation, processing };
}
