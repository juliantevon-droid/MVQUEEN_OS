import {
  processProductJobBatch,
  reconcileRecentShopifyProducts,
  recoverStaleProductJobs,
  recordProductWorkerHeartbeat,
} from "../app/lib/product-job-worker.server";

function envInt(name: string, fallback: number, min: number, max: number): number {
  const parsed = Number(process.env[name] ?? "");
  if (!Number.isFinite(parsed)) return fallback;
  return Math.max(min, Math.min(max, Math.floor(parsed)));
}

const pollMs = envInt("MVQ_PRODUCT_WORKER_POLL_MS", 2000, 1000, 60000);
const reconcileEveryMs = envInt(
  "MVQ_PRODUCT_RECONCILE_INTERVAL_MS",
  300000,
  60000,
  3600000,
);
const heartbeatEveryMs = envInt(
  "MVQ_PRODUCT_WORKER_HEARTBEAT_MS",
  30000,
  5000,
  120000,
);

let stopping = false;
let lastReconcile = 0;
let lastHeartbeat = 0;

for (const signal of ["SIGTERM", "SIGINT"] as const) {
  process.on(signal, () => {
    stopping = true;
  });
}

async function main() {
  await recoverStaleProductJobs();
  await recordProductWorkerHeartbeat("continuous", { pid: process.pid });
  lastHeartbeat = Date.now();

  while (!stopping) {
    const now = Date.now();

    if (now - lastHeartbeat >= heartbeatEveryMs) {
      await recordProductWorkerHeartbeat("continuous", { pid: process.pid });
      lastHeartbeat = now;
    }

    if (now - lastReconcile >= reconcileEveryMs) {
      await reconcileRecentShopifyProducts();
      lastReconcile = now;
    }

    const result = await processProductJobBatch();

    if (result.attempted === 0) {
      await new Promise((resolve) => setTimeout(resolve, pollMs));
    }
  }
}

main()
  .then(async () => {
    await recordProductWorkerHeartbeat("stopped", { pid: process.pid });
    process.stdout.write("MVQueen product worker stopped cleanly.\n");
  })
  .catch(async (error) => {
    try {
      await recordProductWorkerHeartbeat("error", {
        pid: process.pid,
        message: error instanceof Error ? error.message : String(error),
      });
    } catch {
      // Preserve the original worker failure as the process result.
    }
    console.error("MVQueen product worker terminated", error);
    process.exitCode = 1;
  });
