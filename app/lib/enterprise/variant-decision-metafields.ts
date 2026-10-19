import { createHash } from "node:crypto";

// Shopify JSON metafields have a 128 KiB limit; partition under 48 KiB.
export const VARIANT_DECISION_PART_MAX_BYTES = 48 * 1024;
const MAX_PARTS = 80;
const NAMESPACE = "commercial";
const MANIFEST_KEY = "variant_decisions_manifest";
const PART_PREFIX = "variant_decisions_part_";
const SCHEMA = "mvqueen.variant_decisions.v1";

export type VariantDecisionPayload<T = unknown> = {
  currency: string;
  representativeVariantId: string | null;
  variants: T[];
};
export type VariantDecisionMetafield = {
  namespace: string;
  key: string;
  type: string;
  value: string;
};
type Manifest = {
  schema: string;
  currency: string;
  representativeVariantId: string | null;
  parts: string[];
  variantCount: number;
  sha256: string;
};
const byteLength = (value: string) => Buffer.byteLength(value, "utf8");
const sha256 = (value: string) => createHash("sha256").update(value, "utf8").digest("hex");
const keyFor = (index: number) => PART_PREFIX + String(index + 1).padStart(3, "0");

export function assertMetafieldWriteSizes(fields: ReadonlyArray<VariantDecisionMetafield>): void {
  for (const field of fields) {
    // Leave headroom below Shopify's type-specific maximums.
    const safeLimit = field.type === "json" ? 96 * 1024 : 60 * 1024;
    const actual = byteLength(field.value);
    if (actual > safeLimit) throw new Error(
      "Refusing oversized Shopify metafield " + field.namespace + "." +
      field.key + ": " + actual + " bytes (safe limit " + safeLimit + ")",
    );
  }
}

export function buildVariantDecisionMetafields<T>(
  payload: VariantDecisionPayload<T>,
): VariantDecisionMetafield[] {
  if (!Array.isArray(payload.variants)) throw new Error("Variant decisions must be an array");
  const arrays: T[][] = [];
  let current: T[] = [];
  for (const variant of payload.variants) {
    const candidate = [...current, variant];
    if (byteLength(JSON.stringify(candidate)) > VARIANT_DECISION_PART_MAX_BYTES) {
      if (!current.length) throw new Error("One variant decision is too large to preserve safely");
      arrays.push(current);
      current = [variant];
      if (byteLength(JSON.stringify(current)) > VARIANT_DECISION_PART_MAX_BYTES) {
        throw new Error("One variant decision is too large to preserve safely");
      }
    } else current = candidate;
  }
  if (current.length || !arrays.length) arrays.push(current);
  if (arrays.length > MAX_PARTS) throw new Error("Too many variant decision chunks");
  const pieces = arrays.map((array, index) => ({
    namespace: NAMESPACE, key: keyFor(index), type: "json", value: JSON.stringify(array),
  }));
  const manifest: Manifest = {
    schema: SCHEMA,
    currency: payload.currency,
    representativeVariantId: payload.representativeVariantId,
    parts: pieces.map((field) => field.key),
    variantCount: payload.variants.length,
    sha256: sha256(JSON.stringify(payload)),
  };
  const result = [
    ...pieces,
    { namespace: NAMESPACE, key: MANIFEST_KEY, type: "json", value: JSON.stringify(manifest) },
  ];
  assertMetafieldWriteSizes(result);
  return result;
}

// New readers prefer the manifest. Older products without a manifest can still
// load their legacy value. Never use stale legacy data if a manifest is invalid.
export function readVariantDecisionMetafields<T = unknown>(
  fields: ReadonlyArray<{ key: string; value: string; namespace?: string | null }>,
): VariantDecisionPayload<T> | null {
  const entries = fields.filter((field) => !field.namespace || field.namespace === NAMESPACE);
  const manifestField = entries.find((field) => field.key === MANIFEST_KEY);
  if (!manifestField) {
    const legacy = entries.find((field) => field.key === "variant_decisions");
    if (!legacy) return null;
    const data = JSON.parse(legacy.value) as VariantDecisionPayload<T>;
    if (!Array.isArray(data?.variants)) throw new Error("Invalid legacy variant decisions");
    return data;
  }
  const manifest = JSON.parse(manifestField.value) as Manifest;
  if (manifest.schema !== SCHEMA || !Array.isArray(manifest.parts) ||
      !manifest.parts.length || manifest.parts.length > MAX_PARTS ||
      !Number.isSafeInteger(manifest.variantCount) ||
      typeof manifest.currency !== "string" ||
      typeof manifest.sha256 !== "string" ||
      new Set(manifest.parts).size !== manifest.parts.length ||
      manifest.parts.some((key, index) => key !== keyFor(index))) {
    throw new Error("Invalid variant decision manifest");
  }
  const variants: T[] = [];
  for (const key of manifest.parts) {
    const matches = entries.filter((field) => field.key === key);
    if (matches.length !== 1) throw new Error("Missing or duplicate variant decision part: " + key);
    if (byteLength(matches[0].value) > VARIANT_DECISION_PART_MAX_BYTES) {
      throw new Error("Oversized stored variant decision part: " + key);
    }
    const values = JSON.parse(matches[0].value) as T[];
    if (!Array.isArray(values)) throw new Error("Invalid variant decision part: " + key);
    variants.push(...values);
  }
  const data: VariantDecisionPayload<T> = {
    currency: manifest.currency, representativeVariantId: manifest.representativeVariantId, variants,
  };
  if (variants.length !== manifest.variantCount ||
      sha256(JSON.stringify(data)) !== manifest.sha256) {
    throw new Error("Variant decision readback failed digest or count verification");
  }
  return data;
}

const READBACK_QUERY = `#graphql
query MVQueenVariantDecisionReadback($id: ID!, $after: String) {
  product(id: $id) {
    metafields(first: 250, after: $after, namespace: "commercial") {
      nodes { namespace key value }
      pageInfo { hasNextPage endCursor }
    }
  }
}`;

// Verify Shopify's actual saved shards *before* the worker completes the job.
export async function verifySavedVariantDecisionMetafields<T>(
  graphql: (query: string, options: { variables: Record<string, unknown> }) => Promise<Response>,
  productId: string,
  expected: VariantDecisionPayload<T>,
): Promise<void> {
  const stored: Array<{ namespace: string; key: string; value: string }> = [];
  let after: string | null = null;
  let finished = false;
  for (let page = 0; page < 12; page += 1) {
    const response = await graphql(READBACK_QUERY, { variables: { id: productId, after } });
    const body = await response.json();
    if (body.errors?.length) throw new Error("Shopify variant decision readback query failed");
    const connection = body.data?.product?.metafields;
    if (!connection?.nodes || !connection.pageInfo) {
      throw new Error("Missing Shopify variant decision readback");
    }
    stored.push(...connection.nodes);
    if (!connection.pageInfo.hasNextPage) {
      finished = true;
      break;
    }
    after = connection.pageInfo.endCursor;
    if (!after) throw new Error("Incomplete variant decision readback cursor");
  }
  if (!finished) throw new Error("Variant decision readback exceeded pagination safety cap");
  const actual = readVariantDecisionMetafields<T>(stored);
  if (!actual || sha256(JSON.stringify(actual)) !== sha256(JSON.stringify(expected))) {
    throw new Error("Saved Shopify variant decisions differ from submitted decisions");
  }
}
