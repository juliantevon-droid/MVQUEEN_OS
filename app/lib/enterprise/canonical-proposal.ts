import { createHash } from "node:crypto";

export type CanonicalProductRecord = {
  schema_version: string;
  identity: {
    product_id: string;
    source_name: string;
    handle?: string;
    sku?: string;
  };
  category: {
    product_type: string;
    category?: string;
    subcategory?: string;
  };
  pricing: {
    source_price: string | number;
    currency?: string;
    approved_publish_price?: string | number | null;
    recommended_price?: string | number | null;
    compare_at_price?: string | number | null;
  };
  shipping: {
    delivery_estimate: string;
    estimate_source: "verified_product_fact" | "checkout_fallback";
    specific_window_verified: boolean;
  };
  copy: {
    title: string;
    short_description: string;
    description: string;
    benefits?: string[];
    features?: string[];
    cta?: string;
  };
  seo: {
    seo_title: string;
    meta_description: string;
    primary_keyword: string;
    alt_texts: string[];
    secondary_keywords?: string[];
    long_tail_keywords?: string[];
    internal_links?: Array<{
      anchor: string;
      target: string;
      type: "product" | "collection";
      reason: string;
    }>;
  };
  content_suite: {
    content_version: string;
    metafields: Record<string, {
      type: string;
      value: unknown;
      source?: string;
    }>;
    qa: {
      errors: string[];
      passed: boolean;
      status: string;
    };
    [key: string]: unknown;
  };
  qa: {
    errors: string[];
    warnings: string[];
    passed: boolean;
  };
  status: string;
  [key: string]: unknown;
};

export type ReleaseArtifact = {
  release_schema_version: string;
  product_id: string;
  schema_version: string;
  content_fingerprint: string;
  decision: string;
  actor: string;
  timestamp: string;
};

export type ApprovedReleaseBundle = {
  record: CanonicalProductRecord;
  approval: ReleaseArtifact;
  canonical_record_json: string;
};

function stableValue(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    const obj = value as Record<string, unknown>;
    return Object.fromEntries(
      Object.keys(obj)
        .sort()
        .map((key) => [key, stableValue(obj[key])]),
    );
  }
  return value;
}

export function canonicalFingerprint(record: CanonicalProductRecord): string {
  const payload = JSON.stringify(stableValue(record));
  return createHash("sha256").update(payload, "utf8").digest("hex");
}

export function canonicalEnvelopeFingerprint(canonicalRecordJson: string): string {
  return createHash("sha256").update(canonicalRecordJson, "utf8").digest("hex");
}

export function validateApprovedReleaseBundle(bundle: ApprovedReleaseBundle): string[] {
  const errors: string[] = [];
  const record = bundle?.record;
  const approval = bundle?.approval;
  const canonicalRecordJson = bundle?.canonical_record_json;

  if (!record || typeof record !== "object") return ["Missing canonical record"];
  if (!approval || typeof approval !== "object") return ["Missing release approval"];
  if (!canonicalRecordJson?.trim()) return ["Missing canonical_record_json envelope"];

  let envelopeRecord: unknown;
  try {
    envelopeRecord = JSON.parse(canonicalRecordJson);
  } catch {
    return ["canonical_record_json is not valid JSON"];
  }

  if (JSON.stringify(stableValue(envelopeRecord)) !== JSON.stringify(stableValue(record))) {
    errors.push("canonical_record_json does not represent the submitted record");
  }

  if (record.status !== "PRODUCTION_READY") errors.push("Canonical record is not PRODUCTION_READY");
  if (record.qa?.passed !== true || (record.qa?.errors?.length ?? 0) > 0) {
    errors.push("Canonical QA gate has not passed");
  }

  const approvedPrice = record.pricing?.approved_publish_price;
  if (approvedPrice === null || approvedPrice === undefined || approvedPrice === "" || Number(approvedPrice) <= 0) {
    errors.push("Canonical record has no approved_publish_price");
  }

  if (approval.release_schema_version !== "1.0") errors.push("Unsupported release artifact version");
  if (approval.decision !== "APPROVED_FOR_PUBLISH") errors.push("Release decision is not APPROVED_FOR_PUBLISH");
  if (!record.identity?.product_id) errors.push("Missing identity.product_id");
  if (approval.product_id !== record.identity?.product_id) errors.push("Approval product_id mismatch");
  if (approval.schema_version !== record.schema_version) errors.push("Approval schema_version mismatch");
  if (!approval.actor?.trim()) errors.push("Approval actor is required");
  if (!approval.timestamp || Number.isNaN(Date.parse(approval.timestamp))) errors.push("Approval timestamp is invalid");

  const expected = canonicalEnvelopeFingerprint(canonicalRecordJson);
  if (approval.content_fingerprint !== expected) errors.push("Approval fingerprint does not match canonical_record_json");

  if (!record.shipping?.delivery_estimate?.trim()) errors.push("Missing shipping.delivery_estimate");
  if (!record.copy?.title?.trim()) errors.push("Missing approved copy.title");
  if (!record.copy?.description?.trim()) errors.push("Missing approved copy.description");
  if (!record.copy?.short_description?.trim()) errors.push("Missing approved copy.short_description");
  if (!record.seo?.seo_title?.trim()) errors.push("Missing approved seo.seo_title");
  if (!record.seo?.meta_description?.trim()) errors.push("Missing approved seo.meta_description");
  if (!record.content_suite || typeof record.content_suite !== "object") {
    errors.push("Missing approved content_suite");
  } else {
    if (record.content_suite.qa?.passed !== true || (record.content_suite.qa?.errors?.length ?? 0) > 0) {
      errors.push("Approved content_suite QA gate has not passed");
    }
    if (!record.content_suite.metafields || typeof record.content_suite.metafields !== "object") {
      errors.push("Approved content_suite metafields are missing");
    }
  }

  return errors;
}


const APPROVED_CONTENT_METAFIELDS = new Set([
  "catalog.short_description",
  "catalog.focus_keyword",
  "catalog.short_tail_keywords",
  "catalog.long_tail_keywords",
  "catalog.seo_keywords",
  "catalog.highlights",
  "catalog.review_status",
  "content.faq",
  "content.care_instructions",
  "content.how_to_use",
  "shipping.delivery_estimate",
  "attributes.material",
  "attributes.fabric",
  "attributes.color",
  "attributes.shade",
  "attributes.finish",
  "attributes.texture",
  "attributes.size",
  "attributes.dimensions",
  "attributes.fit",
  "attributes.occasion",
  "attributes.ingredient",
  "attributes.key_ingredient",
  "attributes.ingredients",
  "attributes.main_stone",
  "attributes.main_stone_size",
  "attributes.total_weight",
  "attributes.creation",
  "attributes.design_code",
  "attributes.item_code",
  "attributes.size_length",
]);

function serializeContentMetafieldValue(type: string, value: unknown): string {
  if (type === "json" || type.startsWith("list.")) return JSON.stringify(value);
  return String(value ?? "").trim();
}

function buildApprovedContentMetafields(record: CanonicalProductRecord) {
  const source = record.content_suite?.metafields ?? {};
  return Object.entries(source).flatMap(([qualifiedKey, field]) => {
    if (!APPROVED_CONTENT_METAFIELDS.has(qualifiedKey)) return [];
    const [namespace, key] = qualifiedKey.split(".", 2);
    if (!namespace || !key || !field?.type) return [];
    const value = serializeContentMetafieldValue(field.type, field.value);
    if (!value || value === "[]" || value === "{}") return [];
    return [{
      namespace,
      key,
      type: field.type,
      value,
    }];
  });
}

export function buildApprovedEditorialProductInput(record: CanonicalProductRecord) {
  const highlights = Array.from(
    new Set([...(record.copy.benefits ?? []), ...(record.copy.features ?? [])].map((item) => item.trim()).filter(Boolean)),
  ).slice(0, 8);

  const contentMetafields = buildApprovedContentMetafields(record);
  const approvedInternalLinks = (record.seo.internal_links ?? []).filter((item) => {
    const target = item?.target?.trim() ?? "";
    return Boolean(
      item?.anchor?.trim()
      && (target.startsWith("/products/") || target.startsWith("/collections/")),
    );
  });
  const internalLinkMetafields = approvedInternalLinks.length
    ? [{
        namespace: "seo",
        key: "internal_links",
        type: "json",
        value: JSON.stringify(approvedInternalLinks),
      }]
    : [];

  return {
    id: record.identity.product_id,
    title: record.copy.title.trim(),
    descriptionHtml: record.copy.description.trim(),
    productType: record.category.product_type.trim(),
    seo: {
      title: record.seo.seo_title.trim(),
      description: record.seo.meta_description.trim(),
    },
    metafields: [
      {
        namespace: "automation",
        key: "short_description",
        type: "multi_line_text_field",
        value: record.copy.short_description.trim(),
      },
      {
        namespace: "automation",
        key: "highlights",
        type: "list.single_line_text_field",
        value: JSON.stringify(highlights),
      },
      {
        namespace: "release",
        key: "approved_publish_price",
        type: "number_decimal",
        value: String(record.pricing.approved_publish_price),
      },
      ...contentMetafields,
      ...internalLinkMetafields,
    ],
  };
}
