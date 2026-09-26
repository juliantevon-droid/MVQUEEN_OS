export const DEFAULT_SHIPPING_DELIVERY_ESTIMATE =
  "Confirmed at checkout based on destination and fulfillment source.";

export function resolveShippingDeliveryEstimate(
  existingValue?: string | null,
): string {
  const normalized = String(existingValue ?? "").replace(/\s+/g, " ").trim();
  return normalized || DEFAULT_SHIPPING_DELIVERY_ESTIMATE;
}
