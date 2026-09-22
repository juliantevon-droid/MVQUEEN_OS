import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  const response = await admin.graphql(`#graphql
    query MVQueenRuntimeHealth {
      shop { name myshopifyDomain }
    }
  `);
  return await response.json();
};

export default function Dashboard() {
  const data = useLoaderData<typeof loader>();
  const shop = data.data?.shop;
  return (
    <s-page heading="MVQUEEN OS">
      <s-section heading="Runtime foundation">
        <s-paragraph>
          Connected to {shop?.name ?? "Shopify"} ({shop?.myshopifyDomain ?? "unknown"}).
        </s-paragraph>
        <s-paragraph>Product automation runtime is installed in the repository and ready for deployment validation.</s-paragraph>
      </s-section>
    </s-page>
  );
}
