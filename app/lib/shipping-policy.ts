export const DEFAULT_SHIPPING_DELIVERY_ESTIMATE =
  "7–15 business days";

export function resolveShippingDeliveryEstimate(
  existingValue?: string | null,
): string {
  const normalized = String(existingValue ?? "").replace(/\s+/g, " ").trim();
  return normalized || DEFAULT_SHIPPING_DELIVERY_ESTIMATE;
}
