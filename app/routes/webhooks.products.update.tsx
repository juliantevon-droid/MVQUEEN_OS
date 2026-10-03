import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import { enqueueProductWebhook } from "../lib/product-job-intake.server";

/**
 * Keep the Shopify webhook request path deliberately small:
 * authenticate -> durable idempotent enqueue -> 200.
 *
 * Automation-generated/no-op updates are suppressed by the durable worker's
 * source fingerprint + automation-version gate. Avoiding an additional
 * ProductAutomationState lookup here prevents DB contention from delaying
 * Shopify acknowledgements during update bursts.
 */
export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop, topic, webhookId, payload } = await authenticate.webhook(request);
  await enqueueProductWebhook({ shop, topic, webhookId, payload });
  return new Response(null, { status: 200 });
};
