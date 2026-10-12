import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { mock } from "node:test";
import type { Prisma } from "@prisma/client";
import { envInt } from "./runtime-config";

const originalEnv = { ...process.env };
const directory = mkdtempSync(join(tmpdir(), "mvqueen-worker-test-"));
let disconnect: (() => Promise<void>) | undefined;
const restoreLogs = [mock.method(console, "info", () => {}), mock.method(console, "error", () => {}), mock.method(console, "warn", () => {})];
let externalRequests = 0;
const fetchMock = mock.method(globalThis, "fetch", async () => {
  externalRequests += 1;
  throw new Error("Worker regression tests must not make external requests");
});

try {
  // This suite owns an isolated SQLite file and no real Shopify session.
  for (const key of Object.keys(process.env)) {
    if (key.startsWith("MVQ_") || key.startsWith("SHOPIFY_")) delete process.env[key];
  }
  Object.assign(process.env, {
    NODE_ENV: "test",
    DATABASE_URL: `file:${join(directory, "worker.db")}`,
    MVQ_DATABASE_PROFILE: "development",
    SHOPIFY_API_KEY: "worker-test-key",
    SHOPIFY_API_SECRET: "worker-test-secret",
    SHOPIFY_APP_URL: "https://worker-test.example.com",
    MVQ_WRITE_ENABLED: "true",
  });

  for (const value of [undefined, "", "   ", "invalid", "Infinity"]) {
    if (value === undefined) delete process.env.MVQ_TEST_INTEGER;
    else process.env.MVQ_TEST_INTEGER = value;
    assert.equal(envInt("MVQ_TEST_INTEGER", 30, 5, 60), 30);
  }
  for (const [value, expected] of [["0", 5], ["12.9", 12], ["90", 60]] as const) {
    process.env.MVQ_TEST_INTEGER = value;
    assert.equal(envInt("MVQ_TEST_INTEGER", 30, 5, 60), expected);
  }

  writeFileSync(join(directory, "worker.db"), "");
  execFileSync(process.execPath, [
    "node_modules/prisma/build/index.js", "migrate", "deploy", "--schema", "prisma/schema.prisma",
  ], { env: process.env, stdio: "pipe" });

  const { default: prisma } = await import("../db.server");
  disconnect = () => prisma.$disconnect();
  const { processProductJobBatch, reconcileRecentShopifyProducts } = await import("./product-job-worker.server");
  const { enqueueProductWebhook } = await import("./product-job-intake.server");

  const shop = "worker-regression.example.invalid";
  let serial = 0;
  const minutesAgo = (minutes: number) => new Date(Date.now() - minutes * 60_000);
  async function createJob(overrides: Partial<Prisma.ProductJobCreateInput> = {}) {
    serial += 1;
    return prisma.productJob.create({ data: {
      shop,
      productGid: `gid://shopify/Product/${serial}`,
      eventKey: `worker-test:${serial}`,
      topic: "PRODUCTS_UPDATE",
      ...overrides,
    } });
  }
  async function job(id: string) {
    return prisma.productJob.findUniqueOrThrow({ where: { id } });
  }

  // The always-on runner must never turn a dry-run/cancelled catalog job into
  // an ordinary live job or dead-letter its failures. Shared stale recovery
  // still returns crashed backfill jobs to their dedicated runner.
  const backfill = await prisma.catalogBackfillRun.create({ data: {
    shop, reason: "regression fixture", requestedBy: "test", writeMode: "dry_run",
  } });
  const cancelled = await prisma.catalogBackfillRun.create({ data: {
    shop, reason: "cancelled fixture", requestedBy: "test", status: "cancelled",
  } });
  const backfillJobs = await Promise.all([
    createJob({ backfillRunId: backfill.id, topic: "CATALOG_BACKFILL" }),
    createJob({ backfillRunId: cancelled.id, topic: "CATALOG_BACKFILL" }),
    createJob({ backfillRunId: backfill.id, status: "failed", attempts: 12, startedAt: minutesAgo(20) }),
    createJob({ backfillRunId: backfill.id, status: "leased", attempts: 1, startedAt: minutesAgo(20) }),
  ]);
  const ordinary = await createJob();
  const isolated = await processProductJobBatch();
  assert.equal(isolated.attempted, 1);
  assert.equal(isolated.failed, 1);
  assert.equal((await job(ordinary.id)).attempts, 1);
  for (const original of backfillJobs) {
    const expected = original.status === "leased"
      ? { ...original, status: "received", startedAt: null, error: "Recovered stale processing lease" }
      : original;
    assert.deepEqual(await job(original.id), expected);
  }
  assert.deepEqual(isolated.queue, { received: 0, processing: 0, failed: 1, deadLetter: 0 });
  await prisma.productJob.deleteMany();

  // A first transient failure retains the default five-attempt budget and
  // thirty-second backoff; omitted environment settings must keep defaults.
  const due = await createJob({ status: "failed", attempts: 1, startedAt: new Date(Date.now() - 31_000) });
  const waiting = await createJob({ status: "failed", attempts: 1, startedAt: new Date(Date.now() - 10_000) });
  const exhausted = await createJob({ status: "failed", attempts: 5, startedAt: minutesAgo(20) });
  const retry = await processProductJobBatch();
  assert.equal(retry.attempted, 1);
  assert.equal((await job(due.id)).attempts, 2);
  assert.equal((await job(due.id)).status, "failed");
  assert.deepEqual(await job(waiting.id), waiting);
  assert.equal((await job(exhausted.id)).status, "dead_letter");
  await prisma.productJob.deleteMany();

  // The default ten-minute lease must not steal a three-minute running job;
  // repeatedly crashed jobs must still stop at the retry budget.
  const active = await createJob({ status: "leased", attempts: 1, startedAt: minutesAgo(3) });
  const stale = await createJob({ status: "processing", attempts: 4, startedAt: minutesAgo(11) });
  const staleExhausted = await createJob({ status: "processing", attempts: 5, startedAt: minutesAgo(11) });
  const recovered = await processProductJobBatch();
  assert.deepEqual(await job(active.id), active);
  assert.equal(recovered.attempted, 1);
  assert.equal(recovered.queue.processing, 1);
  assert.equal((await job(stale.id)).status, "dead_letter");
  assert.equal((await job(staleExhausted.id)).status, "dead_letter");
  assert.equal((await job(staleExhausted.id)).attempts, 5);
  await prisma.productJob.deleteMany();

  process.env.MVQ_WRITE_ENABLED = "false";
  const pausedJob = await createJob();
  const paused = await processProductJobBatch();
  assert.ok("paused" in paused);
  assert.equal(paused.paused, true);
  assert.equal(paused.attempted, 0);
  assert.deepEqual(await job(pausedJob.id), pausedJob);
  process.env.MVQ_WRITE_ENABLED = "true";
  await prisma.productJob.deleteMany();

  for (let index = 0; index < 12; index += 1) await createJob();
  const batch = await processProductJobBatch();
  assert.equal(batch.attempted, 10);
  assert.equal(batch.queue.received, 2);
  assert.equal(batch.queue.failed, 10);
  await prisma.productJob.deleteMany();

  // Another replica can finish and fail a selected job before this replica
  // claims it. The stale selection must not immediately retry that failure.
  const contested = await createJob();
  const originalUpdateMany = prisma.productJob.updateMany.bind(prisma.productJob);
  prisma.productJob.updateMany = (async (args: Prisma.ProductJobUpdateManyArgs) => {
    if (args.where?.id === contested.id && args.data.status === "leased") {
      await prisma.productJob.update({ where: { id: contested.id }, data: {
        status: "failed", attempts: 1, startedAt: new Date(), error: "Other replica failed",
      } });
    }
    return originalUpdateMany(args);
  }) as unknown as typeof prisma.productJob.updateMany;
  let contestedBatch;
  try {
    contestedBatch = await processProductJobBatch();
  } finally {
    prisma.productJob.updateMany = originalUpdateMany;
  }
  assert.equal(contestedBatch.attempted, 0);
  assert.equal((await job(contested.id)).attempts, 1);
  assert.equal((await job(contested.id)).error, "Other replica failed");
  await prisma.productJob.deleteMany();

  const duplicates = await Promise.all(Array.from({ length: 6 }, () => enqueueProductWebhook({
    shop, topic: "PRODUCTS_UPDATE", webhookId: "duplicate-delivery",
    payload: { id: 42, updated_at: "2026-10-11T00:00:00Z" },
  })));
  assert.equal(new Set(duplicates.map(({ job }) => job.id)).size, 1);
  assert.equal(await prisma.productJob.count(), 1);
  await assert.rejects(enqueueProductWebhook({ shop, topic: "PRODUCTS_UPDATE", payload: {} }), /missing a product id/);

  // Recover missed product updates across multiple pages using the intended
  // default window. Repeating reconciliation must keep one job per version.
  await prisma.productJob.deleteMany();
  await prisma.session.create({ data: {
    id: `offline_${shop}`, shop, state: "regression", isOnline: false, accessToken: "placeholder",
  } });
  await prisma.productAutomationState.create({ data: {
    shop, productGid: "gid://shopify/Product/older", automationVersion: "old-policy",
  } });
  const { unauthenticated } = await import("../shopify.server");
  const originalAdmin = unauthenticated.admin;
  const reconciliationRequests: Array<Record<string, unknown>> = [];
  unauthenticated.admin = (async () => ({ admin: {
    async graphql(_query: string, options: { variables: Record<string, unknown> }) {
      reconciliationRequests.push(options.variables);
      const nextPage = options.variables.after === "page-1";
      return Response.json({ data: { products: {
        nodes: [{ id: `gid://shopify/Product/${nextPage ? "second" : "first"}`, updatedAt: "2026-10-11T00:00:00Z" }],
        pageInfo: { hasNextPage: !nextPage, endCursor: nextPage ? "page-2" : "page-1" },
      } } });
    },
  } })) as unknown as typeof unauthenticated.admin;
  process.env.MVQ_PRODUCT_RECONCILE_ENABLED = "true";
  const reconciliationStarted = Date.now();
  try {
    const first = await reconcileRecentShopifyProducts();
    assert.deepEqual(first, { shops: 1, discovered: 3, scanned: 2 });
    const repeated = await reconcileRecentShopifyProducts();
    assert.deepEqual(repeated, { shops: 1, discovered: 0, scanned: 2 });
  } finally {
    unauthenticated.admin = originalAdmin;
  }
  assert.equal(await prisma.productJob.count(), 3);
  assert.equal(reconciliationRequests[0].first, 100);
  assert.equal(reconciliationRequests[1].after, "page-1");
  const since = /updated_at:>'([^']+)'/.exec(String(reconciliationRequests[0].query));
  assert.ok(since);
  const windowMs = reconciliationStarted - Date.parse(since[1]);
  assert.ok(windowMs >= 20 * 60_000 - 5000 && windowMs <= 20 * 60_000);
  assert.equal(externalRequests, 0);
} finally {
  if (disconnect) await disconnect();
  for (const key of Object.keys(process.env)) if (!(key in originalEnv)) delete process.env[key];
  Object.assign(process.env, originalEnv);
  rmSync(directory, { recursive: true, force: true });
  fetchMock.mock.restore();
  for (const log of restoreLogs) log.mock.restore();
}

console.log("product worker tests passed: defaults, retries, stale leases, backfill isolation, paused writes, concurrent claims, duplicate intake, paginated reconciliation");
