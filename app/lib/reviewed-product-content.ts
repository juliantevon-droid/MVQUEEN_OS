import { createHash } from "node:crypto";
import type { ProductSnapshot } from "./mvqueen-intelligence";

/** Only source facts participate: price or generated copy changes do not revoke review. */
export function editorialSourceFingerprint(product: ProductSnapshot): string {
  const source = {
    id: product.id,
    productType: product.productType ?? "",
    attributes: (product.attributeMetafields?.nodes ?? [])
      .map(({ key, value }) => ({ key, value: value ?? "" }))
      .sort((a, b) => a.key.localeCompare(b.key)),
    variants: (product.variants?.nodes ?? [])
      .map(({ id, sku }) => ({ id, sku: sku ?? "" }))
      .sort((a, b) => a.id.localeCompare(b.id)),
  };
  return createHash("sha256").update(JSON.stringify(source)).digest("hex");
}

/** Editorial ownership is not claim clearance. Changed facts keep copy held for human review. */
export function reviewedEditorialState(product: ProductSnapshot): {
  preserve: boolean;
  status: "reviewed" | "source_changed" | null;
} {
  try {
    const marker = JSON.parse(product.editorialApproval?.value ?? "null");
    if (!marker || marker.version !== 1 || marker.owner !== "mvqueen-content" ||
        marker.productId !== product.id ||
        typeof marker.sourceFingerprint !== "string" || !/^[a-f0-9]{64}$/.test(marker.sourceFingerprint) ||
        typeof marker.reviewedAt !== "string" || !Number.isFinite(Date.parse(marker.reviewedAt))) {
      return { preserve: false, status: null };
    }
    return { preserve: true, status: marker.sourceFingerprint === editorialSourceFingerprint(product)
      ? "reviewed" : "source_changed" };
  } catch {
    return { preserve: false, status: null };
  }
}
