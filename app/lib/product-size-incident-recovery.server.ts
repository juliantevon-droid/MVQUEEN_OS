import prisma from "../db.server";
import { logMvqueenEvent } from "./enterprise/observability.server";

// User-authorized recovery for the October 17–18 size-limit incident. This is
// deliberately not a general dead-letter retry: unrelated failures stay held.
export const SIZE_INCIDENT = {
  receipt: "recovery:variant-json-size:2026-10-19:v1",
  shop: "tsucu0-1i.myshopify.com",
  productGid: "gid://shopify/Product/9100787351750",
  error: "Value exceeds the maximum size of 131072 bytes. Current size is 142688 bytes.",
  jobIds: [
    "cmvcqnq5t002uo60o5kzgs7bp", "cmvcqnqui0064o60oo2qwkche",
    "cmvcrppxv007oqo1ryac0a233", "cmvcrqxf6010do60o6szncgv6",
    "cmvd2fmu40085qo1r7mu26ln5", "cmvd2fpeo0086qo1rmo2kxi6s",
    "cmvd2hfq201jdo60odrojdii5",
  ],
};

export async function recoverProductSizeIncident(): Promise<number> {
  if (process.env.MVQ_WRITE_ENABLED !== "true") return 0;
  if (await prisma.runtimeHeartbeat.findUnique({ where: { name: SIZE_INCIDENT.receipt } })) return 0;
  try {
    const count = await prisma.$transaction(async (tx) => {
      // Unique receipt serializes concurrent replicas; a rollback also rolls
      // back the receipt. A restart can never reset the retry budget twice.
      await tx.runtimeHeartbeat.create({ data: { name: SIZE_INCIDENT.receipt, state: "recovering" } });
      const where = {
        id: { in: SIZE_INCIDENT.jobIds }, shop: SIZE_INCIDENT.shop,
        productGid: SIZE_INCIDENT.productGid, status: "dead_letter",
        error: SIZE_INCIDENT.error, backfillRunId: null,
      };
      const previous = await tx.productJob.findMany({ where, orderBy: { id: "asc" } });
      const result = await tx.productJob.updateMany({ where, data: {
        status: "received", attempts: 0, startedAt: null, completedAt: null, error: null,
      } });
      if (result.count) {
        await tx.productAutomationState.updateMany({
          where: { shop: SIZE_INCIDENT.shop, productGid: SIZE_INCIDENT.productGid },
          data: { automationVersion: "variant-json-size-recovery:pending" },
        });
      }
      await tx.runtimeHeartbeat.update({ where: { name: SIZE_INCIDENT.receipt }, data: {
        state: "requeued", detailsJson: JSON.stringify({
          reason: "User-authorized retry after size-safe variant decision storage", previous, requeued: result.count,
        }),
      } });
      return result.count;
    });
    logMvqueenEvent("product.size_incident.requeued", { receipt: SIZE_INCIDENT.receipt, count });
    return count;
  } catch (error) {
    if ((error as { code?: string }).code === "P2002") return 0;
    throw error;
  }
}
