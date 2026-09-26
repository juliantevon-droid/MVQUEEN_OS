import type { LoaderFunctionArgs } from "react-router";
import prisma from "../db.server";
import { productionPreflight } from "../lib/production-preflight";

export const loader = async (_args: LoaderFunctionArgs) => {
  const preflight = productionPreflight();
  let database = false;

  try {
    await prisma.$queryRaw`SELECT 1`;
    database = true;
  } catch {
    database = false;
  }

  const ok = preflight.ready && database;
  return Response.json(
    {
      ok,
      mode: preflight.mode,
      database,
    },
    {
      status: ok ? 200 : 503,
      headers: { "Cache-Control": "no-store" },
    },
  );
};
