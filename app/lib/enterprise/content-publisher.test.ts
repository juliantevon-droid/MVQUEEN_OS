import assert from "node:assert/strict";
import { buildAutomaticSurfaceRecord } from "../automated-content-surfaces";
import { buildAutomatedProductContent } from "../product-content-automation";
import { publishAutomaticContentSurfaces } from "./content-publisher";
import type { Classification, ProductSnapshot } from "../mvqueen-intelligence";

const classification: Classification = {
  department: "Fashion", family: "Dresses", subcollection: "Dresses",
  route: "dresses", productType: "Dress", confidence: "high",
};
const product: ProductSnapshot = {
  id: "publisher-test", title: "Black Satin Midi Dress", handle: "existing-product-handle",
  descriptionHtml: "<p>" + "Review the listed measurements and options before choosing. ".repeat(6) + "</p><ul><li>Material: Satin</li><li>Color: Black</li><li>Length: Midi</li></ul>",
};
const flags = ["MVQ_WRITE_ENABLED", "MVQ_AUTO_CONTENT_SURFACES_ENABLED", "MVQ_BLOG_PUBLISH_ENABLED", "MVQ_COLLECTION_CONTENT_PUBLISH_ENABLED", "MVQ_BLOG_AUTHOR"];
const original = Object.fromEntries(flags.map((key) => [key, process.env[key]]));
try {
  // Exercise the publisher with the in-memory transport below. Live product
  // writes stay disabled throughout this fixture.
  process.env.MVQ_WRITE_ENABLED = "false";
  process.env.MVQ_AUTO_CONTENT_SURFACES_ENABLED = "true";
  process.env.MVQ_BLOG_PUBLISH_ENABLED = "true";
  process.env.MVQ_COLLECTION_CONTENT_PUBLISH_ENABLED = "false";
  delete process.env.MVQ_BLOG_AUTHOR;
  for (const brand of ["MVQUEEN", "Miss.Princess"]) {
    const content = buildAutomatedProductContent(product, classification, brand);
    const record = buildAutomaticSurfaceRecord(product, classification, content, brand);
    const blog = record.content_suite.blog as any;
    assert.equal(blog.auto_publish, true);
    for (const exists of [false, true]) {
      const requests: Array<{ query: string; variables: Record<string, any> }> = [];
      const admin = {
        async graphql(query: string, options?: { variables?: Record<string, unknown> }) {
          const variables = options?.variables ?? {};
          requests.push({ query, variables });
          let data;
          if (query.includes("MVQBlogByHandle")) data = { blogs: { nodes: [{ id: "gid://shopify/Blog/1", handle: "news" }] } };
          else if (query.includes("MVQArticleByHandle")) data = { articles: { nodes: exists ? [{ id: "gid://shopify/Article/1", handle: blog.slug }] : [] } };
          else if (query.includes("MVQCreateArticle")) data = { articleCreate: { article: { id: "gid://shopify/Article/1" }, userErrors: [] } };
          else if (query.includes("MVQUpdateArticle")) data = { articleUpdate: { article: { id: "gid://shopify/Article/1" }, userErrors: [] } };
          else throw new Error("Unexpected transport: " + query);
          return Response.json({ data });
        },
      };
      const results = await publishAutomaticContentSurfaces(admin, record);
      assert.equal(results.find((r) => r.surface === "blog")?.status, exists ? "UPDATED" : "PUBLISHED");
      const write = requests.find((r) => r.query.includes(exists ? "MVQUpdateArticle" : "MVQCreateArticle"));
      assert.ok(write);
      const article = write.variables.article;
      assert.equal(article.handle, blog.slug);
      assert.equal(article.title, blog.title);
      assert.equal(article.author.name, brand);
      assert.ok(article.tags.includes(brand));
      assert.ok(article.body.startsWith("<p>" + blog.introduction));
      assert.ok(article.body.includes(content.highlights[0]));
      assert.ok(article.body.includes("/products/" + product.handle));
      assert.ok(!/editorial framing|source information remains/.test(article.body));
      assert.equal(article.summary, "<p>" + blog.dek + "</p>");
      assert.equal(article.metafields.find((m: any) => m.namespace === "global" && m.key === "title_tag")?.value, blog.seo_title);
      assert.equal(article.metafields.find((m: any) => m.namespace === "global" && m.key === "description_tag")?.value, blog.meta_description);
      assert.ok(requests.every((r) => !/pageCreate|pageUpdate|productUpdate|collectionUpdate/.test(r.query)));
    }
  }
  const record = buildAutomaticSurfaceRecord(product, classification, buildAutomatedProductContent(product, classification));
  const noWrites = { graphql: async () => { throw new Error("Publishing gate was bypassed"); } };
  process.env.MVQ_BLOG_PUBLISH_ENABLED = "false";
  const disabled = await publishAutomaticContentSurfaces(noWrites, record);
  assert.equal(disabled.find((r) => r.surface === "blog")?.status, "SKIPPED");
  await assert.rejects(() => publishAutomaticContentSurfaces(noWrites, { ...record, qa: { ...record.qa, passed: false } }), /QA-passed/);
  process.env.MVQ_AUTO_CONTENT_SURFACES_ENABLED = "false";
  assert.equal((await publishAutomaticContentSurfaces(noWrites, record))[0].status, "SKIPPED");
} finally {
  for (const key of flags) {
    if (original[key] === undefined) delete process.env[key];
    else process.env[key] = original[key];
  }
}
console.log("content publisher tests passed: both voices, create/update, real SEO fields and gates");
