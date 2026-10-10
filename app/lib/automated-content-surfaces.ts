import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { AutomatedProductContent } from "./product-content-automation";
import { brandedSeoTitle, productEditorialCategory } from "./product-content-automation";
import type { CanonicalProductRecord } from "./enterprise/canonical-proposal";
import { BRAND_VOCABULARY, canonicalBrandLabel, removeForbiddenLanguage, type BrandVocabulary } from "./brand-vocabulary.server";

function cleanText(value?: string | null): string {
  return String(value ?? "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/\s+/g, " ")
    .trim();
}

function slug(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function pluralSlug(value: string): string {
  const base = slug(value);
  if (!base) return "";
  if (base.endsWith("ss") || base.endsWith("sh") || base.endsWith("ch") || /[xz]$/.test(base)) return base + "es";
  if (base.endsWith("y") && !/[aeiou]y$/.test(base)) return base.slice(0, -1) + "ies";
  if (base.endsWith("s")) return base;
  return base + "s";
}

function seed(value: string): number {
  let result = 2166136261;
  for (const char of value) result = Math.imul(result ^ char.charCodeAt(0), 16777619);
  return result >>> 0;
}

function boundedText(value: string, limit: number): string {
  if (value.length <= limit) return value;
  return value.slice(0, limit).replace(/\s+\S*$/, "").trim();
}

function surfaceContext(
  product: ProductSnapshot,
  classification: Classification,
  content: AutomatedProductContent,
  brandLabel: string,
  vocabulary: BrandVocabulary,
) {
  const brand = canonicalBrandLabel(brandLabel, vocabulary);
  const brandKey = brand === "Miss.Princess" ? "miss-princess" : "mvqueen";
  if (brand !== vocabulary.contentPolicy.profiles[brandKey].displayName) {
    throw new Error(`Unknown brand for content surfaces: ${brand}`);
  }
  const productType = cleanText(classification.productType).toLowerCase();
  const values: Record<string, string> = {
    brand, title: cleanText(content.title), productType,
    family: cleanText(classification.family).toLowerCase(),
    focusKeyword: cleanText(content.focusKeyword),
    article: /^[aeiou]/i.test(productType) ? "an" : "a",
  };
  const render = (template: string): string => {
    const text = cleanText(template.replace(/\{(\w+)\}/g, (_match, key: string) => {
      if (!(key in values)) throw new Error(`Unknown content template field: ${key}`);
      return values[key];
    }));
    if (!text || removeForbiddenLanguage(text, vocabulary) !== text) {
      throw new Error(`Content surface requires a language review: ${product.id}`);
    }
    return text;
  };
  const productIdentity = product.id || product.handle || content.title;
  const choose = (pool: string[], key: string, identity = productIdentity) =>
    render(pool[seed(identity + ":" + key) % pool.length]);
  return {
    brand, brandKey, render, choose,
    templates: vocabulary.contentPolicy.profiles[brandKey].surfaces,
    category: productEditorialCategory(classification),
  };
}

export function buildAutomatedProductFaq(
  product: ProductSnapshot,
  classification: Classification,
  content: AutomatedProductContent,
  brandLabel = "MVQUEEN",
  vocabulary = BRAND_VOCABULARY,
) {
  const { templates, render } = surfaceContext(product, classification, content, brandLabel, vocabulary);
  const entry = (item: { question: string; answer: string }) => ({
    question: render(item.question), answer: render(item.answer),
  });
  const faq = [entry(templates.faq.overview), entry(templates.faq.choosing), entry(templates.faq.policies)];

  const specificFacts = [
    [templates.faq.factQuestions.material, /^(?:material(?: composition)?|metal|stone|ingredients?|main ingredients|product ingredients)\s*:/i],
    [templates.faq.factQuestions.quantity, /^(?:net (?:content|weight|wt)|capacity|number of pieces|dimensions|length(?: dimensions)?|product size|item size)\s*:/i],
    [templates.faq.factQuestions.care, /^(?:care(?: instructions)?|washing instructions|storage method)\s*:|^(?:machine|hand) wash\b|^dry clean\b/i],
  ] as const;
  const answered = new Set<string>();
  for (const [question, pattern] of specificFacts) {
    const facts = content.highlights.filter(fact => pattern.test(fact));
    if (!facts.length) continue;
    facts.forEach(fact => answered.add(fact));
    faq.splice(faq.length - 1, 0, { question: render(question), answer: facts.slice(0, 3).join("; ").replace(/[.;]+$/, "") + "." });
  }
  const options = new Map<string, Set<string>>();
  for (const variant of product.variants?.nodes ?? []) {
    for (const option of variant.selectedOptions ?? []) {
      if (!/^(?:colou?r|size|shade)$/i.test(option.name) || /default title|https?:|\b[A-Z]{2,}[-_]?\d{3,}/i.test(option.value)) continue;
      if (!options.has(option.name)) options.set(option.name, new Set());
      options.get(option.name)!.add(option.value);
    }
  }
  if (options.size) {
    const details = [...options].map(([name, values]) => `${name}: ${[...values].slice(0, 12).join(" / ")}${values.size > 12 ? " (more options are listed on this page)" : ""}`);
    faq.splice(faq.length - 1, 0, { question: render(templates.faq.factQuestions.options), answer: details.join("; ") + ". Check the option selector for current availability." });
  }
  const otherDetails = content.highlights.filter(fact => !answered.has(fact));
  if (otherDetails.length) {
    faq.splice(1, 0, {
      question: render(templates.faq.detailsQuestion),
      answer: render(templates.faq.detailsLead) + " " + otherDetails.slice(0, 5).join("; ").replace(/[.;]+$/, "") + ".",
    });
  }

  return faq;
}

export function buildAutomaticSurfaceRecord(
  product: ProductSnapshot,
  classification: Classification,
  content: AutomatedProductContent,
  brandLabel = "MVQUEEN",
  vocabulary = BRAND_VOCABULARY,
): CanonicalProductRecord {
  const context = surfaceContext(product, classification, content, brandLabel, vocabulary);
  brandLabel = context.brand;
  const { templates, choose, render, category } = context;
  const faq = buildAutomatedProductFaq(product, classification, content, brandLabel, vocabulary);
  const descriptionPlain = cleanText(product.descriptionHtml);
  const blogPublishEligible =
    descriptionPlain.length >= 240 && content.highlights.length >= 3;

  const collectionName = brandLabel + " " + classification.family + " Edit";
  const collectionTargetHandles = Array.from(new Set([
    slug(classification.route),
    slug(classification.subcollection),
    slug(classification.family),
    slug(classification.productType),
    pluralSlug(classification.productType),
    slug(classification.department),
  ].filter(Boolean)));

  const blogTitle = boundedText(choose(templates.blog.title, "blog.title"), 120);
  // Keep the established identity even when an editor changes the headline.
  const blogSlug = slug("A Closer Look at " + content.title);
  const listedDetails = content.highlights.slice(0, 5).join("; ");
  const cta = choose(templates.cta, "cta");
  // A collection is shared by products. Its copy must not alternate as each
  // product runs, so select its wording by brand and taxonomy, not product ID.
  const collectionIdentity = context.brandKey + ":" + classification.family.toLowerCase();

  const firstPrice = product.variants?.nodes?.[0]?.price ?? "0";

  return {
    schema_version: "1.0",
    identity: {
      product_id: product.id,
      source_name: "Shopify",
      handle: product.handle ?? undefined,
    },
    category: {
      product_type: classification.productType,
      category: classification.department,
      subcategory: classification.family,
    },
    pricing: {
      source_price: firstPrice,
      approved_publish_price: null,
    },
    shipping: {
      delivery_estimate: "7–15 business days",
      estimate_source: "store_default",
      specific_window_verified: false,
    },
    copy: {
      title: content.title,
      short_description: content.shortDescription,
      description: content.descriptionHtml,
      benefits: [],
      features: content.highlights,
      cta,
    },
    seo: {
      seo_title: content.seoTitle,
      meta_description: content.metaDescription,
      primary_keyword: content.focusKeyword,
      secondary_keywords: content.secondaryKeywords,
      long_tail_keywords: content.longTailKeywords,
      alt_texts: [],
    },
    content_suite: {
      content_version: "mvq-auto-surfaces-v2-" + vocabulary.version,
      metafields: {
        "content.faq": {
          type: "json",
          value: faq,
          source: "shopify_source_product",
        },
        "shipping.delivery_estimate": {
          type: "single_line_text_field",
          value: "7–15 business days",
          source: "store_default",
        },
      },
      product_page: {
        faq,
      },
      collection: {
        name: collectionName,
        slug: slug(collectionName),
        target_handles: collectionTargetHandles,
        description: choose(templates.collection.description, "collection.description", collectionIdentity),
        seo_title: brandedSeoTitle(classification.family + " Edit", brandLabel, vocabulary.contentPolicy.limits.seoTitle),
        meta_description: boundedText(choose(templates.collection.metaDescription, "collection.metaDescription", collectionIdentity), vocabulary.contentPolicy.limits.metaDescription),
        primary_keyword: classification.family.toLowerCase(),
        status: "PUBLISH_ELIGIBLE",
        auto_publish: true,
      },
      blog: {
        title: blogTitle,
        slug: blogSlug,
        brand_label: brandLabel,
        dek: choose(templates.blog.dek, "blog.dek"),
        introduction: choose(templates.blog.introduction[category], "blog.introduction"),
        sections: [
          {
            heading: choose(templates.blog.detailsHeading, "blog.detailsHeading"),
            paragraphs: [
              listedDetails
                ? render(templates.faq.detailsLead) + " " + listedDetails.replace(/[.;]+$/, "") + "."
                : render(templates.faq.choosing.answer),
            ],
          },
          {
            heading: choose(templates.blog.choiceHeading, "blog.choiceHeading"),
            paragraphs: [
              choose(templates.blog.choice[category], "blog.choice"),
            ],
          },
          {
            heading: choose(templates.blog.closingHeading, "blog.closingHeading"),
            paragraphs: [
              choose(templates.blog.closing, "blog.closing"), cta,
            ],
          },
        ],
        internal_links: product.handle
          ? [{ anchor: content.title, target: "/products/" + product.handle, type: "product" }]
          : [],
        primary_keyword: content.focusKeyword,
        seo_title: brandedSeoTitle(blogTitle, brandLabel, vocabulary.contentPolicy.limits.seoTitle),
        meta_description: boundedText(choose(templates.blog.dek, "blog.dek"), vocabulary.contentPolicy.limits.metaDescription),
        status: blogPublishEligible ? "PUBLISH_ELIGIBLE" : "DRAFT_REVIEW",
        publish_eligible: blogPublishEligible,
        auto_publish: blogPublishEligible,
      },
      site_faq: {
        topic: content.title,
        entries: faq,
        scope: "product",
        publish_target: "product.metafields.content.faq",
        status: "PUBLISH_ELIGIBLE",
        auto_publish: true,
      },
      governance: {
        brand: context.brandKey,
        brand_policy_version: vocabulary.version,
        fact_policy: "shopify_source_product_only",
        protected_fields_mutated: false,
        approved_release_controls_publish: false,
        automatic_product_event_controls_publish: true,
      },
      qa: {
        errors: [],
        passed: true,
        status: "CONTENT_PUBLISH_ELIGIBLE",
      },
    },
    qa: {
      errors: [],
      warnings: [],
      passed: true,
    },
    status: "PRODUCTION_READY",
  };
}
