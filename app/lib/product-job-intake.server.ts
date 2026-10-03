import { Prisma } from "@prisma/client";
import prisma from "../db.server";

type ProductWebhookPayload = {
  id?: string | number;
  admin_graphql_api_id?: string;
  updated_at?: string | null;
};

export function productGidFromWebhook(payload: ProductWebhookPayload): string {
  if (payload.admin_graphql_api_id?.trim()) return payload.admin_graphql_api_id.trim();
  if (payload.id === undefined || payload.id === null || String(payload.id).trim() === "") {
    throw new Error("Product webhook payload is missing a product id");
  }
  return "gid://shopify/Product/" + String(payload.id);
}

export function productEventKey(args: {
  webhookId?: string | null;
  topic: string;
  productGid: string;
  updatedAt?: string | null;
}): string {
  if (args.webhookId?.trim()) return args.webhookId.trim();
  return [
    args.topic.toLowerCase().replace(/_/g, "/"),
    args.productGid,
    args.updatedAt ?? "",
  ].join(":");
}

export async function enqueueProductWebhook(args: {
  shop: string;
  topic: string;
  webhookId?: string | null;
  payload: ProductWebhookPayload;
}) {
  const productGid = productGidFromWebhook(args.payload);
  const eventKey = productEventKey({
    webhookId: args.webhookId,
    topic: args.topic,
    productGid,
    updatedAt: args.payload.updated_at,
  });

  try {
    const job = await prisma.productJob.upsert({
      where: { eventKey },
      update: {},
      create: {
        shop: args.shop,
        productGid,
        eventKey,
        topic: args.topic,
        status: "received",
      },
    });

    return { job, productGid, eventKey };
  } catch (error) {
    // Concurrent Shopify deliveries can race between the upsert read and create.
    // A unique eventKey collision means another request already persisted this
    // exact webhook, so return that job instead of turning a safe duplicate into
    // a 500 response. All other database failures remain fatal.
    if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2002") {
      const job = await prisma.productJob.findUnique({ where: { eventKey } });
      if (job) return { job, productGid, eventKey };
    }
    throw error;
  }
}
