import type { ActionFunctionArgs, LoaderFunctionArgs } from "react-router";
import { useActionData, useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import {
  advanceCatalogBackfillRun,
  cancelCatalogBackfillRun,
  createCatalogBackfillRun,
} from "../lib/enterprise/catalog-backfill.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const runs = await prisma.catalogBackfillRun.findMany({
    where: { shop: session.shop },
    orderBy: { createdAt: "desc" },
    take: 12,
  });

  return {
    shop: session.shop,
    runs,
    globalWritesEnabled: process.env.MVQ_WRITE_ENABLED === "true",
    backfillWritesEnabled: process.env.MVQ_BACKFILL_WRITE_ENABLED === "true",
    workerConfigured: Boolean(
      process.env.MVQ_BACKFILL_WORKER_TOKEN &&
      process.env.MVQ_BACKFILL_WORKER_TOKEN.length >= 32
    ),
  };
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  const form = await request.formData();
  const intent = String(form.get("intent") ?? "").trim();

  try {
    if (intent === "create_dry_run" || intent === "create_governed_write") {
      const reason = String(form.get("reason") ?? "").trim();
      const run = await createCatalogBackfillRun({
        shop: session.shop,
        requestedBy: session.id,
        reason,
        writeMode:
          intent === "create_governed_write" ? "governed_write" : "dry_run",
      });
      return {
        ok: true,
        message: `Created ${run.writeMode} backfill run ${run.id}.`,
      };
    }

    const runId = String(form.get("runId") ?? "").trim();
    if (!runId) return { ok: false, message: "Backfill run ID is required." };

    if (intent === "advance") {
      const run = await advanceCatalogBackfillRun({
        admin: admin as unknown as {
          graphql: (
            query: string,
            options?: { variables?: Record<string, unknown> },
          ) => Promise<Response>;
        },
        shop: session.shop,
        runId,
        batchSize: 10,
      });
      return {
        ok: true,
        message: `Advanced ${run.id}: ${run.status}; ${run.processedJobs}/${run.enqueuedJobs} processed; ${run.failedJobs} failed.`,
      };
    }

    if (intent === "cancel") {
      const run = await cancelCatalogBackfillRun({
        shop: session.shop,
        runId,
      });
      return {
        ok: true,
        message: `Backfill run ${run.id} is ${run.status}.`,
      };
    }

    return { ok: false, message: "Unknown catalog-backfill action." };
  } catch (error) {
    return {
      ok: false,
      message: error instanceof Error ? error.message : String(error),
    };
  }
};

export default function CatalogBackfillPage() {
  const data = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const governedWriteAvailable =
    data.globalWritesEnabled && data.backfillWritesEnabled;

  return (
    <s-page heading="Catalog Backfill">
      <s-section heading="Bulk safety">
        <s-paragraph>
          Backfill runs are durable, cursor-based and processed in bounded batches.
          Dry-run evaluates catalog logic and commercial health without Shopify product writes.
        </s-paragraph>
        <s-paragraph>
          Global writes: {data.globalWritesEnabled ? "enabled" : "disabled"} · dedicated backfill writes: {data.backfillWritesEnabled ? "enabled" : "disabled"}.
        </s-paragraph>
        <s-paragraph>
          Scheduled worker: {data.workerConfigured ? "token configured" : "not configured"}.
        </s-paragraph>
      </s-section>

      <s-section heading="Create backfill">
        <form method="post">
          <label htmlFor="reason">Reason</label>
          <input
            id="reason"
            name="reason"
            required
            maxLength={240}
            placeholder="Example: commercial policy change"
            style={{ display: "block", width: "100%", marginTop: "6px", marginBottom: "12px" }}
          />
          <button type="submit" name="intent" value="create_dry_run">
            Create dry-run backfill
          </button>
          {" "}
          <button
            type="submit"
            name="intent"
            value="create_governed_write"
            disabled={!governedWriteAvailable}
          >
            Create governed-write backfill
          </button>
        </form>
        {actionData?.message ? <p>{actionData.message}</p> : null}
      </s-section>

      <s-section heading="Recent runs">
        {data.runs.length ? (
          data.runs.map((run) => (
            <div key={run.id} style={{ marginBottom: "18px" }}>
              <s-paragraph>
                {run.status.toUpperCase()} · {run.writeMode} · {run.reason}
              </s-paragraph>
              <s-paragraph>
                Enqueued {run.enqueuedJobs} · processed {run.processedJobs} · failed {run.failedJobs} · scan {run.scanComplete ? "complete" : "in progress"}
              </s-paragraph>
              {!["completed", "completed_with_errors", "cancelled"].includes(run.status) ? (
                <form method="post" style={{ display: "inline" }}>
                  <input type="hidden" name="runId" value={run.id} />
                  <button type="submit" name="intent" value="advance">
                    Advance one bounded step
                  </button>
                  {" "}
                  <button type="submit" name="intent" value="cancel">
                    Cancel
                  </button>
                </form>
              ) : null}
            </div>
          ))
        ) : (
          <s-paragraph>No catalog-backfill runs recorded yet.</s-paragraph>
        )}
      </s-section>
    </s-page>
  );
}
