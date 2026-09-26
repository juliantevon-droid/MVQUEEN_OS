import { timingSafeEqual } from "node:crypto";
import type { ActionFunctionArgs } from "react-router";
import {
  recordProductWorkerHeartbeat,
  runAlwaysOnProductWorker,
} from "../lib/product-job-worker.server";
import { createCorrelationId, errorFields, logMvqueenEvent } from "../lib/enterprise/observability.server";

function authorized(request: Request): boolean {
  const expected =
    process.env.MVQ_PRODUCT_WORKER_TOKEN ??
    process.env.MVQ_BACKFILL_WORKER_TOKEN ??
    "";
  if (expected.length < 32) return false;

  const header = request.headers.get("authorization") ?? "";
  const prefix = "Bearer ";
  if (!header.startsWith(prefix)) return false;

  const supplied = header.slice(prefix.length);
  const expectedBuffer = Buffer.from(expected, "utf8");
  const suppliedBuffer = Buffer.from(supplied, "utf8");
  return expectedBuffer.length === suppliedBuffer.length &&
    timingSafeEqual(expectedBuffer, suppliedBuffer);
}

export const action = async ({ request }: ActionFunctionArgs) => {
  const correlationId = createCorrelationId("product-worker-endpoint");
  if (!authorized(request)) {
    logMvqueenEvent("product.worker.unauthorized", { correlationId }, "warn");
    return Response.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  try {
    const result = await runAlwaysOnProductWorker();
    await recordProductWorkerHeartbeat("fallback", { correlationId, ...result });
    logMvqueenEvent("product.worker.fallback.completed", { correlationId, ...result });
    return Response.json({ ok: true, correlationId, ...result });
  } catch (error) {
    const details = { correlationId, ...errorFields(error) };
    await recordProductWorkerHeartbeat("error", details);
    logMvqueenEvent("product.worker.failed", details, "error");
    return Response.json(
      {
        ok: false,
        correlationId,
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
};
