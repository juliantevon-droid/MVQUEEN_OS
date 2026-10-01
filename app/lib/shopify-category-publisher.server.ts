import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { CatalogAttributeEnrichment, CatalogMetafieldInput } from "./catalog-attribute-enrichment";
import {
  selectTaxonomyValues,
  type TaxonomyAttributeCandidate,
  type TaxonomyValueCandidate,
} from "./shopify-category-enrichment";

type AdminClient = {
  graphql: (
    query: string,
    options?: { variables?: Record<string, unknown> },
  ) => Promise<Response>;
};

type StandardTemplate = {
  id: string;
  namespace: string;
  key: string;
  name: string;
  ownerTypes: string[];
  type?: { name?: string | null } | null;
};

type CategoryContext = {
  categoryId: string;
  attributes: TaxonomyAttributeCandidate[];
  templates: StandardTemplate[];
  activeKeys: Set<string>;
};

const CATEGORY_CONTEXT_QUERY = `#graphql
query MVQueenCategoryContext(
  $categoryId: ID!,
  $constraint: MetafieldDefinitionConstraintSubtypeIdentifier!
) {
  node(id: $categoryId) {
    ... on TaxonomyCategory {
      id
      name
      fullName
      attributes(first: 100) {
        nodes {
          __typename
          ... on TaxonomyChoiceListAttribute {
            id
            name
            values(first: 100) { nodes { id name } }
          }
        }
      }
    }
  }
  standardMetafieldDefinitionTemplates(
    first: 250,
    constraintSubtype: $constraint
  ) {
    nodes {
      id
      namespace
      key
      name
      ownerTypes
      type { name }
    }
  }
  metafieldDefinitions(
    ownerType: PRODUCT,
    first: 250,
    constraintSubtype: $constraint
  ) {
    nodes {
      namespace
      key
    }
  }
}`;

const ENABLE_STANDARD_DEFINITION = `#graphql
mutation MVQueenEnableStandardDefinition($id: ID!) {
  standardMetafieldDefinitionEnable(id: $id, ownerType: PRODUCT) {
    createdDefinition { id namespace key name type { name } }
    userErrors { field message code }
  }
}`;

const UPSERT_CATEGORY_VALUE = `#graphql
mutation MVQueenUpsertCategoryValue(
  $handle: MetaobjectHandleInput!,
  $metaobject: MetaobjectUpsertInput!
) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
    metaobject { id handle displayName type }
    userErrors { field message code }
  }
}`;

const CATEGORY_CONTEXT_CACHE = new Map<
  string,
  { expiresAt: number; value: CategoryContext }
>();
const METAOBJECT_CACHE = new Map<string, string>();

function normalize(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function systemTypeForKey(key: string): string {
  return `shopify--${key}`;
}

function categoryValueHandle(key: string, valueId: string): string {
  const id = valueId.split("/").at(-1) ?? valueId;
  return `mvqueen-${key}-${id}`
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 255);
}

async function loadCategoryContext(
  admin: AdminClient,
  categoryId: string,
): Promise<CategoryContext | null> {
  const cached = CATEGORY_CONTEXT_CACHE.get(categoryId);
  if (cached && cached.expiresAt > Date.now()) return cached.value;

  const response = await admin.graphql(CATEGORY_CONTEXT_QUERY, {
    variables: {
      categoryId,
      constraint: { key: "category", value: categoryId },
    },
  });
  const body = (await response.json()) as {
    data?: {
      node?: {
        id?: string;
        attributes?: {
          nodes?: Array<{
            __typename?: string;
            id?: string;
            name?: string;
            values?: { nodes?: Array<{ id?: string; name?: string }> };
          }>;
        };
      } | null;
      standardMetafieldDefinitionTemplates?: {
        nodes?: Array<StandardTemplate>;
      } | null;
      metafieldDefinitions?: {
        nodes?: Array<{ namespace?: string; key?: string }>;
      } | null;
    };
  };

  const node = body.data?.node;
  if (!node?.id) return null;

  const attributes: TaxonomyAttributeCandidate[] = (
    node.attributes?.nodes ?? []
  )
    .filter(
      (item) =>
        item.__typename === "TaxonomyChoiceListAttribute" &&
        Boolean(item.id) &&
        Boolean(item.name),
    )
    .map((item) => ({
      id: item.id!,
      name: item.name!,
      values: (item.values?.nodes ?? [])
        .filter(
          (value): value is { id: string; name: string } =>
            Boolean(value.id) && Boolean(value.name),
        )
        .map((value) => ({ id: value.id, name: value.name })),
    }));

  const templates = (
    body.data?.standardMetafieldDefinitionTemplates?.nodes ?? []
  ).filter(
    (template) =>
      template.namespace === "shopify" &&
      template.ownerTypes?.includes("PRODUCT") &&
      template.type?.name === "list.metaobject_reference",
  );

  const activeKeys = new Set(
    (body.data?.metafieldDefinitions?.nodes ?? [])
      .filter((item) => item.namespace && item.key)
      .map((item) => `${item.namespace}.${item.key}`),
  );

  const value = { categoryId, attributes, templates, activeKeys };
  CATEGORY_CONTEXT_CACHE.set(categoryId, {
    expiresAt: Date.now() + 30 * 60_000,
    value,
  });
  return value;
}

async function ensureTemplateEnabled(
  admin: AdminClient,
  context: CategoryContext,
  template: StandardTemplate,
): Promise<boolean> {
  const key = `${template.namespace}.${template.key}`;
  if (context.activeKeys.has(key)) return true;

  const response = await admin.graphql(ENABLE_STANDARD_DEFINITION, {
    variables: { id: template.id },
  });
  const body = (await response.json()) as {
    data?: {
      standardMetafieldDefinitionEnable?: {
        createdDefinition?: { id?: string | null } | null;
        userErrors?: Array<{ message?: string | null }>;
      } | null;
    };
  };
  const payload = body.data?.standardMetafieldDefinitionEnable;
  const errors = payload?.userErrors ?? [];
  if (errors.length || !payload?.createdDefinition?.id) return false;

  context.activeKeys.add(key);
  return true;
}

function patternValueForColor(
  context: CategoryContext,
  product: ProductSnapshot,
  enrichment: CatalogAttributeEnrichment,
  classification: Classification,
): TaxonomyValueCandidate | null {
  const pattern = context.attributes.find(
    (attribute) => normalize(attribute.name) === "pattern",
  );
  if (!pattern) return null;

  const selected = selectTaxonomyValues({
    attribute: pattern,
    product,
    enrichment,
    classification,
  });
  if (selected.length) return selected[0];

  return (
    pattern.values.find((value) => normalize(value.name) === "solid") ?? null
  );
}

async function upsertCategoryValue(
  admin: AdminClient,
  template: StandardTemplate,
  value: TaxonomyValueCandidate,
  extra: {
    patternValue?: TaxonomyValueCandidate | null;
  } = {},
): Promise<string | null> {
  const cacheKey = `${template.key}:${value.id}:${extra.patternValue?.id ?? ""}`;
  const cached = METAOBJECT_CACHE.get(cacheKey);
  if (cached) return cached;

  const fields: Array<{ key: string; value: string }> = [
    { key: "label", value: value.name },
  ];

  if (template.key === "color-pattern") {
    if (!extra.patternValue) return null;
    fields.push(
      {
        key: "color_taxonomy_reference",
        value: JSON.stringify([value.id]),
      },
      {
        key: "pattern_taxonomy_reference",
        value: extra.patternValue.id,
      },
    );
  } else {
    fields.push({
      key: "taxonomy_reference",
      value: value.id,
    });
  }

  const response = await admin.graphql(UPSERT_CATEGORY_VALUE, {
    variables: {
      handle: {
        type: systemTypeForKey(template.key),
        handle: categoryValueHandle(template.key, value.id),
      },
      metaobject: { fields },
    },
  });
  const body = (await response.json()) as {
    data?: {
      metaobjectUpsert?: {
        metaobject?: { id?: string | null } | null;
        userErrors?: Array<{ message?: string | null }>;
      } | null;
    };
  };
  const payload = body.data?.metaobjectUpsert;
  if ((payload?.userErrors ?? []).length || !payload?.metaobject?.id) {
    // Some Shopify category metaobjects have specialized schemas. Unsupported
    // shapes are skipped instead of failing the entire product job.
    return null;
  }

  METAOBJECT_CACHE.set(cacheKey, payload.metaobject.id);
  return payload.metaobject.id;
}

export async function buildShopifyCategoryMetafields(args: {
  admin: AdminClient;
  categoryId: string;
  product: ProductSnapshot;
  enrichment: CatalogAttributeEnrichment;
  classification: Classification;
}): Promise<CatalogMetafieldInput[]> {
  const context = await loadCategoryContext(args.admin, args.categoryId);
  if (!context) return [];

  const templateByName = new Map(
    context.templates.map((template) => [normalize(template.name), template]),
  );
  const patternValue = patternValueForColor(
    context,
    args.product,
    args.enrichment,
    args.classification,
  );

  const metafields: CatalogMetafieldInput[] = [];

  for (const attribute of context.attributes) {
    const template = templateByName.get(normalize(attribute.name));
    if (!template) continue;

    const selected = selectTaxonomyValues({
      attribute,
      product: args.product,
      enrichment: args.enrichment,
      classification: args.classification,
    });
    if (!selected.length) continue;

    if (!(await ensureTemplateEnabled(args.admin, context, template))) continue;

    const metaobjectIds: string[] = [];
    for (const value of selected) {
      const id = await upsertCategoryValue(args.admin, template, value, {
        patternValue:
          template.key === "color-pattern" ? patternValue : undefined,
      });
      if (id) metaobjectIds.push(id);
    }

    if (!metaobjectIds.length) continue;

    metafields.push({
      namespace: template.namespace,
      key: template.key,
      type: "list.metaobject_reference",
      value: JSON.stringify(Array.from(new Set(metaobjectIds))),
    });
  }

  return metafields;
}
