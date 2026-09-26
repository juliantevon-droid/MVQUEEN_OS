import {
  processProductJobBatch,
  reconcileRecentShopifyProducts,
  recoverStaleProductJobs,
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

let stopping = false;
let lastReconcile = 0;

for (const signal of ["SIGTERM", "SIGINT"] as const) {
  process.on(signal, () => {
    stopping = true;
  });
}

async function main() {
  await recoverStaleProductJobs();

  while (!stopping) {
    const now = Date.now();

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
  .then(() => {
    process.stdout.write("MVQueen product worker stopped cleanly.\n");
  })
  .catch((error) => {
    console.error("MVQueen product worker terminated", error);
    process.exitCode = 1;
  });
