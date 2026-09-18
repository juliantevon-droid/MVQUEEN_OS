import type { HeadersFunction, LoaderFunctionArgs } from "react-router";
import { Outlet, useLoaderData } from "react-router";
import { AppProvider } from "@shopify/shopify-app-react-router/react";
import { boundary } from "@shopify/shopify-app-react-router/server";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  await authenticate.admin(request);
  return { apiKey: process.env.SHOPIFY_API_KEY || "" };
};

export default function App() {
  const { apiKey } = useLoaderData<typeof loader>();
  return (
    <AppProvider embedded apiKey={apiKey}>
      <s-app-nav>
        <s-link href="/app">MVQUEEN OS</s-link>
      </s-app-nav>
      <Outlet />
    </AppProvider>
  );
}

export function ErrorBoundary() {
  return boundary.error(useLoaderData as never);
}

export const headers: HeadersFunction = (args) => boundary.headers(args);
