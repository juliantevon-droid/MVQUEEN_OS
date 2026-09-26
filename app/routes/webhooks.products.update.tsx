import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import {
  enqueueProductWebhook,
  productGidFromWebhook,
} from "../lib/product-job-intake.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop, topic, webhookId, payload } = await authenticate.webhook(request);
  const productGid = productGidFromWebhook(payload);

  if (payload.updated_at) {
    const state = await prisma.productAutomationState.findUnique({
      where: { shop_productGid: { shop, productGid } },
      select: { lastAutomationUpdatedAt: true },
    });
    if (state?.lastAutomationUpdatedAt?.getTime() === new Date(payload.updated_at).getTime()) {
      return new Response(null, { status: 200 });
    }
  }

  await enqueueProductWebhook({ shop, topic, webhookId, payload });
  return new Response(null, { status: 200 });
};
