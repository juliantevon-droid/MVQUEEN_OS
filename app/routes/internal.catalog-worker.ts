import { timingSafeEqual } from "node:crypto";
import type { ActionFunctionArgs } from "react-router";
import { unauthenticated } from "../shopify.server";
import {
  advanceCatalogBackfillRun,
  nextRunnableBackfillRun,
} from "../lib/enterprise/catalog-backfill.server";

function authorized(request: Request): boolean {
  const expected = process.env.MVQ_BACKFILL_WORKER_TOKEN ?? "";
  if (expected.length < 32) return false;

  const header = request.headers.get("authorization") ?? "";
  const prefix = "Bearer ";
  if (!header.startsWith(prefix)) return false;

  const supplied = header.slice(prefix.length);
  const expectedBuffer = Buffer.from(expected, "utf8");
  const suppliedBuffer = Buffer.from(supplied, "utf8");
  return (
    expectedBuffer.length === suppliedBuffer.length &&
    timingSafeEqual(expectedBuffer, suppliedBuffer)
  );
}

function workerBatchSize(): number {
  const parsed = Number(process.env.MVQ_BACKFILL_BATCH_SIZE ?? "10");
  if (!Number.isFinite(parsed)) return 10;
  return Math.max(1, Math.min(50, Math.floor(parsed)));
}

export const action = async ({ request }: ActionFunctionArgs) => {
  if (!authorized(request)) {
    return Response.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const run = await nextRunnableBackfillRun();
  if (!run) {
    return Response.json({ ok: true, state: "idle" });
  }

  const { admin } = await unauthenticated.admin(run.shop);
  const result = await advanceCatalogBackfillRun({
    admin: admin as unknown as {
      graphql: (
        query: string,
        options?: { variables?: Record<string, unknown> },
      ) => Promise<Response>;
    },
    shop: run.shop,
    runId: run.id,
    batchSize: workerBatchSize(),
  });

  return Response.json({
    ok: true,
    run: {
      id: result.id,
      shop: result.shop,
      status: result.status,
      writeMode: result.writeMode,
      scanComplete: result.scanComplete,
      enqueuedJobs: result.enqueuedJobs,
      processedJobs: result.processedJobs,
      failedJobs: result.failedJobs,
    },
  });
};
