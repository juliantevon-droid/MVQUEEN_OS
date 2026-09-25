import type { LoaderFunctionArgs } from "react-router";
import { redirect, Form, useLoaderData } from "react-router";
import { login } from "../../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  if (url.searchParams.get("shop")) throw redirect(`/app?${url.searchParams.toString()}`);
  return { showForm: Boolean(login) };
};

export default function Index() {
  const { showForm } = useLoaderData<typeof loader>();
  return (
    <main style={{maxWidth: 720, margin: "4rem auto", padding: "1.5rem", fontFamily: "system-ui"}}>
      <h1>MVQueen OS</h1>
      <p>Shopify catalog intelligence and product automation runtime.</p>
      {showForm && (
        <Form method="post" action="/auth/login">
          <label>Shop domain<br /><input name="shop" placeholder="tsucu0-1i.myshopify.com" /></label>
          <button type="submit">Connect Shopify</button>
        </Form>
      )}
    </main>
  );
}
