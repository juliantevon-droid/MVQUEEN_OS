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
}
