import type { LoaderFunctionArgs } from "react-router";

export const loader = async (_args: LoaderFunctionArgs) =>
  Response.json(
    {
      ok: true,
      service: "mvqueen-web",
      status: "alive",
      timestamp: new Date().toISOString(),
    },
    {
      status: 200,
      headers: { "Cache-Control": "no-store" },
    },
  );
