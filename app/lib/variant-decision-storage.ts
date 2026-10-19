import { createHash } from "node:crypto";

export const JSON_METAFIELD_LIMIT = 131_072;
const INLINE_LIMIT = 120 * 1024;
const PART_LIMIT = 60 * 1024;
const FORMAT = "mvq.variant-decisions.v1";
const KEY = "variant_decisions";

type Metafield = { namespace: string; key: string; type: string; value: string };
type RecordValue = { currency: string; representativeVariantId: string | null; variants: unknown[] };
const bytes = (value: string) => Buffer.byteLength(value, "utf8");
const digest = (value: string) => createHash("sha256").update(value, "utf8").digest("hex");
const field = (key: string, value: unknown): Metafield => ({
  namespace: "commercial", key, type: "json", value: JSON.stringify(value),
});

// Preserve the legacy shape for small products. Large products use whole variant
// records, never truncated JSON or split UTF-8 characters. Fixed part names are
// replaced together with the manifest; obsolete trailing parts are ignored.
export function buildVariantDecisionMetafields(record: RecordValue): Metafield[] {
  const serialized = JSON.stringify(record);
  if (bytes(serialized) <= INLINE_LIMIT) return [field(KEY, record)];
  const parts: Metafield[] = [];
  let variants: unknown[] = [];
  const flush = () => {
    parts.push(field(`${KEY}_part_${String(parts.length + 1).padStart(3, "0")}`, { variants }));
    variants = [];
  };
  for (const variant of record.variants) {
    if (bytes(JSON.stringify({ variants: [variant] })) > PART_LIMIT) {
      throw new Error("commercial.variant_decisions: one variant exceeds the 60 KiB part budget");
    }
    if (variants.length && bytes(JSON.stringify({ variants: [...variants, variant] })) > PART_LIMIT) flush();
    variants.push(variant);
  }
  if (variants.length) flush();
  if (!parts.length || parts.length > 20) throw new Error("commercial.variant_decisions: unsupported part count");
  const manifest = field(KEY, {
    currency: record.currency, representativeVariantId: record.representativeVariantId,
    storage: FORMAT, parts: parts.map((part) => part.key),
    variantCount: record.variants.length, sha256: digest(serialized),
  });
  return [manifest, ...parts];
}

export function assertJsonMetafieldSizes(metafields: Metafield[]): void {
  for (const item of metafields) {
    if (item.type === "json" && bytes(item.value) > JSON_METAFIELD_LIMIT) {
      throw new Error(`${item.namespace}.${item.key}: JSON value is ${bytes(item.value)} bytes; maximum is ${JSON_METAFIELD_LIMIT}`);
    }
  }
}

// All consumers can use this reader for both legacy and fragmented records.
// Only parts named by the manifest count; missing/corrupt data fails closed.
export function readVariantDecisionMetafields(fields: Array<{ key: string; value: string }>): RecordValue {
  const values = new Map(fields.map((item) => [item.key, item.value]));
  const raw = values.get(KEY);
  if (!raw) throw new Error("Missing commercial.variant_decisions");
  const manifest = JSON.parse(raw);
  if (!manifest.storage) {
    if (!Array.isArray(manifest.variants)) throw new Error("Invalid legacy variant decisions");
    return manifest;
  }
  if (manifest.storage !== FORMAT || !Array.isArray(manifest.parts) ||
      !manifest.parts.length || manifest.parts.length > 20 ||
      new Set(manifest.parts).size !== manifest.parts.length) throw new Error("Invalid variant decision manifest");
  const variants = manifest.parts.flatMap((key: string, index: number) => {
    if (key !== `${KEY}_part_${String(index + 1).padStart(3, "0")}`) throw new Error("Invalid variant decision part key");
    const value = values.get(key);
    if (!value) throw new Error(`Missing commercial.${key}`);
    const part = JSON.parse(value);
    if (!Array.isArray(part.variants)) throw new Error(`Invalid commercial.${key}`);
    return part.variants;
  });
  const record = { currency: manifest.currency, representativeVariantId: manifest.representativeVariantId, variants };
  if (variants.length !== manifest.variantCount || digest(JSON.stringify(record)) !== manifest.sha256) {
    throw new Error("Variant decision checksum/count mismatch");
  }
  return record;
}

type Admin = { graphql: (query: string, options: { variables: Record<string, unknown> }) => Promise<Response> };
export async function verifyVariantDecisionReadback(admin: Admin, productId: string, expected: Metafield[]): Promise<void> {
  if (expected.length === 1) return;
  const selections = expected.map((item, i) => `part${i}: metafield(namespace: "commercial", key: "${item.key}") { key value }`).join("\n");
  const response = await admin.graphql(`query MVQVariantDecisionReadback($id: ID!) { product(id: $id) { ${selections} } }`, { variables: { id: productId } });
  const body = await response.json();
  if (!response.ok || body.errors?.length || !body.data?.product) throw new Error("Variant decision readback query failed");
  const actual = expected.map((item, i) => {
    const saved = body.data.product[`part${i}`];
    if (!saved || saved.key !== item.key || saved.value !== item.value) throw new Error(`Variant decision readback mismatch: commercial.${item.key}`);
    return saved as { key: string; value: string };
  });
  readVariantDecisionMetafields(actual);
}
