import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import { processProductJob } from "../lib/product-processor";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop, topic, webhookId, payload } = await authenticate.webhook(request);
  const productGid = payload.admin_graphql_api_id ?? `gid://shopify/Product/${payload.id}`;
  const eventKey = webhookId || `products/update:${productGid}:${payload.updated_at ?? ""}`;
  const job = await prisma.productJob.upsert({
    where: { eventKey },
    update: {},
    create: { shop, productGid, eventKey, topic, status:"received" },
  });
  await processProductJob(job.id);
  return new Response(null, { status: 200 });
};
