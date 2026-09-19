import type { ActionFunctionArgs } from "react-router";
import { authenticate } from "../shopify.server";
export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop, topic } = await authenticate.webhook(request);
  console.log(`Compliance webhook: ${topic} for ${shop}`);
  return new Response(null, { status: 200 });
};
