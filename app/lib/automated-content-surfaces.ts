import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { AutomatedProductContent } from "./product-content-automation";
import type { CanonicalProductRecord } from "./enterprise/canonical-proposal";

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

export function buildAutomatedProductFaq(
  product: ProductSnapshot,
  classification: Classification,
  content: AutomatedProductContent,
) {
  const faq = [
    {
      question: "What is " + content.title + "?",
      answer:
        content.title +
        " is listed as a " +
        classification.productType.toLowerCase() +
        " in the MVQueen catalog. Review the product details and images on this page for the currently available specifications.",
    },
    {
      question: "Where can I check product details before ordering?",
      answer:
        "Use the product details, images, options, and any listed specifications on this page as the current reference before purchasing.",
    },
    {
      question: "Where can I find shipping and return information?",
      answer:
        "Use the Shipping Policy and Refund & Returns Policy linked from the product page for the current store terms.",
    },
  ];

  if (content.highlights.length) {
    faq.splice(1, 0, {
      question: "What details are listed for this product?",
      answer:
        "The source product information currently lists: " +
        content.highlights.slice(0, 5).join("; ") +
        ".",
    });
  }

  return faq;
}

export function buildAutomaticSurfaceRecord(
  product: ProductSnapshot,
  classification: Classification,
  content: AutomatedProductContent,
): CanonicalProductRecord {
  const faq = buildAutomatedProductFaq(product, classification, content);
  const descriptionPlain = cleanText(product.descriptionHtml);
  const blogPublishEligible =
    descriptionPlain.length >= 240 && content.highlights.length >= 3;

  const collectionName = "MVQueen " + classification.family + " Edit";
  const collectionTargetHandles = Array.from(new Set([
    slug(classification.route),
    slug(classification.subcollection),
    slug(classification.family),
    slug(classification.productType),
    pluralSlug(classification.productType),
    slug(classification.department),
  ].filter(Boolean)));

  const blogTitle = "A Closer Look at " + content.title;
  const blogSlug = slug(blogTitle);
  const listedDetails = content.highlights.slice(0, 5).join("; ");

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
      delivery_estimate: "Confirmed at checkout based on destination and fulfillment source.",
      estimate_source: "checkout_fallback",
      specific_window_verified: false,
    },
    copy: {
      title: content.title,
      short_description: content.shortDescription,
      description: product.descriptionHtml ?? "",
      benefits: [],
      features: content.highlights,
      cta: "Explore the MVQueen edit.",
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
      content_version: "mvq-auto-surfaces-v1",
      metafields: {
        "content.faq": {
          type: "json",
          value: faq,
          source: "shopify_source_product",
        },
        "shipping.delivery_estimate": {
          type: "single_line_text_field",
          value: "Confirmed at checkout based on destination and fulfillment source.",
          source: "checkout_fallback",
        },
      },
      product_page: {
        faq,
      },
      collection: {
        name: collectionName,
        slug: slug(collectionName),
        target_handles: collectionTargetHandles,
        description:
          "Explore the MVQueen " +
          classification.family.toLowerCase() +
          " edit with clear product details, intentional styling, and a refined everyday point of view.",
        seo_title: (collectionName + " | MVQueen").slice(0, 60),
        meta_description:
          ("Explore MVQueen " +
            classification.family.toLowerCase() +
            " with clear product details, intentional styling, and a considered feminine point of view.").slice(0, 160),
        primary_keyword: classification.family.toLowerCase(),
        status: "PUBLISH_ELIGIBLE",
        auto_publish: true,
      },
      blog: {
        title: blogTitle,
        slug: blogSlug,
        dek:
          "A practical MVQueen guide to " +
          content.focusKeyword +
          ", grounded in the product information currently available on the product page.",
        sections: [
          {
            heading: "Start with the listed details",
            paragraphs: [
              listedDetails
                ? "The source product information currently lists: " + listedDetails + "."
                : "Review the currently listed product details and imagery before choosing.",
              "MVQueen keeps product facts separate from editorial framing so the source information remains the reference.",
            ],
          },
          {
            heading: "Consider how it fits your needs",
            paragraphs: [
              "Compare the listed details with how you plan to wear, use, or style the product.",
              "When a specification is not listed, it should not be treated as a verified product fact.",
            ],
          },
          {
            heading: "Review the product page",
            paragraphs: [
              "Use the product page for the latest images, options, shipping information, and currently available specifications.",
            ],
          },
        ],
        internal_links: product.handle
          ? [{ anchor: content.title, target: "/products/" + product.handle, type: "product" }]
          : [],
        primary_keyword: content.focusKeyword,
        meta_description: content.metaDescription,
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
