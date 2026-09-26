import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import { enqueueProductWebhook } from "../lib/product-job-intake.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop, topic, webhookId, payload } = await authenticate.webhook(request);
  await enqueueProductWebhook({ shop, topic, webhookId, payload });
  return new Response(null, { status: 200 });
};
