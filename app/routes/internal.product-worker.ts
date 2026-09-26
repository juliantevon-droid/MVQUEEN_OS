import { timingSafeEqual } from "node:crypto";
import type { ActionFunctionArgs } from "react-router";
import {
  recordProductWorkerHeartbeat,
  runAlwaysOnProductWorker,
} from "../lib/product-job-worker.server";

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
  if (!authorized(request)) {
    return Response.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  try {
    const result = await runAlwaysOnProductWorker();
    await recordProductWorkerHeartbeat("fallback", result);
    return Response.json({ ok: true, ...result });
  } catch (error) {
    console.error("MVQueen product worker failed", error);
    return Response.json(
      {
        ok: false,
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
};
