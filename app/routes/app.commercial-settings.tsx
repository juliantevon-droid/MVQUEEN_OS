import type { ActionFunctionArgs, LoaderFunctionArgs } from "react-router";
import { useActionData, useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import {
  getShopCommercialSettings,
  resolveShopCommercialConfig,
  saveShopCommercialSettings,
  type StoredCommercialSettings,
} from "../lib/enterprise/commercial-settings.server";

function parseOptionalNumber(
  form: FormData,
  name: string,
  args: { min: number; max: number },
): number | null {
  const raw = String(form.get(name) ?? "").trim();
  if (!raw) return null;
  const value = Number(raw);
  if (!Number.isFinite(value) || value < args.min || value > args.max) {
    throw new Error(`${name} must be between ${args.min} and ${args.max}.`);
  }
  return value;
}

function percentageToRate(value: number | null): number | null {
  return value === null ? null : value / 100;
}

function rateToPercentage(value: number | null | undefined): string {
  return value === null || value === undefined ? "" : String(Math.round(value * 10000) / 100);
}

function moneyInput(value: number | null | undefined): string {
  return value === null || value === undefined ? "" : String(value);
}

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const [settings, resolution, recentAudit] = await Promise.all([
    getShopCommercialSettings(session.shop),
    resolveShopCommercialConfig(session.shop),
    prisma.commercialSettingsAudit.findMany({
      where: { shop: session.shop },
      orderBy: { createdAt: "desc" },
      take: 10,
      select: {
        id: true,
        actor: true,
        createdAt: true,
      },
    }),
  ]);

  return {
    shop: session.shop,
    settings,
    resolved: resolution.config,
    missing: resolution.missing,
    recentAudit,
  };
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const form = await request.formData();

  try {
    const paymentRatePercent = parseOptionalNumber(form, "paymentRatePercent", { min: 0, max: 25 });
    const returnReservePercent = parseOptionalNumber(form, "returnReservePercent", { min: 0, max: 100 });
    const targetMarginPercent = parseOptionalNumber(form, "targetMarginPercent", { min: 0, max: 95 });
    const paymentFixed = parseOptionalNumber(form, "paymentFixed", { min: 0, max: 100 });
    const targetCac = parseOptionalNumber(form, "targetCac", { min: 0, max: 10000 });
    const inboundShippingDefault = parseOptionalNumber(form, "inboundShippingDefault", { min: 0, max: 10000 });

    const currency = String(form.get("currency") ?? "USD").trim().toUpperCase();
    if (!/^[A-Z]{3}$/.test(currency)) {
      return { ok: false, message: "Currency must be a three-letter code such as USD." };
    }

    const values: StoredCommercialSettings = {
      paymentRate: percentageToRate(paymentRatePercent),
      paymentFixed,
      returnReserveRate: percentageToRate(returnReservePercent),
      targetContributionMarginRate: percentageToRate(targetMarginPercent),
      targetCac,
      inboundShippingDefault,
      currency,
    };

    await saveShopCommercialSettings({
      shop: session.shop,
      actor: session.id,
      values,
    });

    const resolution = await resolveShopCommercialConfig(session.shop);
    return {
      ok: true,
      message: resolution.missing.length
        ? `Commercial settings saved. Pricing is still blocked by: ${resolution.missing.join(", ")}.`
        : "Commercial settings saved. Pricing recommendations now have a complete shop configuration.",
    };
  } catch (error) {
    return {
      ok: false,
      message: error instanceof Error ? error.message : String(error),
    };
  }
};

export default function CommercialSettings() {
  const data = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const settings = data.settings;

  return (
    <s-page heading="Commercial Settings">
      <s-section heading="Pricing assumptions">
        <s-paragraph>
          These values drive the contribution-floor pricing engine. Shop-specific settings override environment fallbacks and every saved change is audited.
        </s-paragraph>
        <s-paragraph>
          Pricing readiness: {data.missing.length ? `blocked — missing ${data.missing.join(", ")}` : "ready"}
        </s-paragraph>

        <form method="post">
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="paymentRatePercent">Payment fee (%)</label>
            <input
              id="paymentRatePercent"
              name="paymentRatePercent"
              type="number"
              min="0"
              max="25"
              step="0.001"
              defaultValue={rateToPercentage(settings?.paymentRate)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="paymentFixed">Fixed payment fee ({data.resolved.currency})</label>
            <input
              id="paymentFixed"
              name="paymentFixed"
              type="number"
              min="0"
              max="100"
              step="0.01"
              defaultValue={moneyInput(settings?.paymentFixed)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="returnReservePercent">Return/refund reserve (%)</label>
            <input
              id="returnReservePercent"
              name="returnReservePercent"
              type="number"
              min="0"
              max="100"
              step="0.01"
              defaultValue={rateToPercentage(settings?.returnReserveRate)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="targetMarginPercent">Target contribution margin (%)</label>
            <input
              id="targetMarginPercent"
              name="targetMarginPercent"
              type="number"
              min="0"
              max="95"
              step="0.01"
              defaultValue={rateToPercentage(settings?.targetContributionMarginRate)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="targetCac">Target CAC ({data.resolved.currency})</label>
            <input
              id="targetCac"
              name="targetCac"
              type="number"
              min="0"
              max="10000"
              step="0.01"
              defaultValue={moneyInput(settings?.targetCac)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="inboundShippingDefault">Default inbound/fulfillment cost ({data.resolved.currency})</label>
            <input
              id="inboundShippingDefault"
              name="inboundShippingDefault"
              type="number"
              min="0"
              max="10000"
              step="0.01"
              defaultValue={moneyInput(settings?.inboundShippingDefault)}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="currency">Currency</label>
            <input
              id="currency"
              name="currency"
              maxLength={3}
              defaultValue={settings?.currency ?? data.resolved.currency ?? "USD"}
              style={{ display: "block", width: "100%", marginTop: "6px" }}
            />
          </div>

          <button type="submit">Save commercial settings</button>
        </form>

        {actionData?.message ? <p>{actionData.message}</p> : null}
      </s-section>

      <s-section heading="Audit history">
        {data.recentAudit.length ? (
          data.recentAudit.map((item) => (
            <s-paragraph key={item.id}>
              Saved by {item.actor} · {new Date(item.createdAt).toLocaleString()}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>No stored commercial-setting changes yet.</s-paragraph>
        )}
      </s-section>
    </s-page>
  );
}
