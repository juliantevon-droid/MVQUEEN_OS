import { createHash } from "node:crypto";
import prisma from "../../db.server";
import {
  getCommercialConfig,
  type CommercialConfig,
  type CommercialConfigResolution,
} from "./commercial-config";

export type StoredCommercialSettings = {
  paymentRate: number | null;
  paymentFixed: number | null;
  returnReserveRate: number | null;
  targetContributionMarginRate: number | null;
  targetCac: number | null;
  inboundShippingDefault: number | null;
  currency: string;
};

function overridesFromRow(
  row: StoredCommercialSettings | null,
): Partial<CommercialConfig> {
  if (!row) return {};
  return {
    ...(row.paymentRate !== null ? { paymentRate: row.paymentRate } : {}),
    ...(row.paymentFixed !== null ? { paymentFixed: row.paymentFixed } : {}),
    ...(row.returnReserveRate !== null ? { returnReserveRate: row.returnReserveRate } : {}),
    ...(row.targetContributionMarginRate !== null
      ? { targetContributionMarginRate: row.targetContributionMarginRate }
      : {}),
    ...(row.targetCac !== null ? { targetCac: row.targetCac } : {}),
    ...(row.inboundShippingDefault !== null
      ? { inboundShippingDefault: row.inboundShippingDefault }
      : {}),
    ...(row.currency?.trim() ? { currency: row.currency } : {}),
  };
}

export async function getShopCommercialSettings(shop: string) {
  return prisma.commercialSettings.findUnique({
    where: { shop },
  });
}

export async function resolveShopCommercialConfig(
  shop: string,
): Promise<CommercialConfigResolution> {
  const row = await getShopCommercialSettings(shop);
  return getCommercialConfig(overridesFromRow(row));
}

export function commercialPolicyFingerprint(
  resolution: CommercialConfigResolution,
): string {
  const payload = JSON.stringify({
    paymentRate: resolution.config.paymentRate,
    paymentFixed: resolution.config.paymentFixed,
    returnReserveRate: resolution.config.returnReserveRate,
    targetContributionMarginRate: resolution.config.targetContributionMarginRate,
    targetCac: resolution.config.targetCac,
    inboundShippingDefault: resolution.config.inboundShippingDefault,
    currency: resolution.config.currency,
    missing: [...resolution.missing].sort(),
  });
  return createHash("sha256").update(payload, "utf8").digest("hex");
}

export async function saveShopCommercialSettings(args: {
  shop: string;
  actor: string;
  values: StoredCommercialSettings;
}) {
  const { shop, actor, values } = args;
  const snapshotJson = JSON.stringify(values);

  return prisma.$transaction(async (tx) => {
    const settings = await tx.commercialSettings.upsert({
      where: { shop },
      update: {
        ...values,
        updatedBy: actor,
      },
      create: {
        shop,
        ...values,
        updatedBy: actor,
      },
    });

    await tx.commercialSettingsAudit.create({
      data: {
        shop,
        actor,
        snapshotJson,
      },
    });

    await tx.productCommercialHealthState.updateMany({
      where: { shop },
      data: { stale: true },
    });

    await tx.productAutomationState.updateMany({
      where: { shop },
      data: { sourceFingerprint: null },
    });

    return settings;
  });
}
