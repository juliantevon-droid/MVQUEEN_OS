import type { CanonicalProductRecord, ReleaseArtifact } from "./canonical-proposal";

type AdminGraphql = {
  graphql: (query: string, options?: { variables?: Record<string, unknown> }) => Promise<Response>;
};

export type PublishResult = {
  surface: string;
  status: "PUBLISHED" | "UPDATED" | "SKIPPED";
  resourceId?: string;
  message: string;
};

const BLOG_QUERY = "#graphql\nquery MVQBlogByHandle($query: String!) { blogs(first: 1, query: $query) { nodes { id title handle } } }";
const BLOG_CREATE = "#graphql\nmutation MVQCreateBlog($blog: BlogCreateInput!) { blogCreate(blog: $blog) { blog { id title handle } userErrors { field message } } }";
const ARTICLE_QUERY = "#graphql\nquery MVQArticleByHandle($query: String!) { articles(first: 1, query: $query) { nodes { id title handle } } }";
const ARTICLE_CREATE = "#graphql\nmutation MVQCreateArticle($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id title handle } userErrors { field message } } }";
const ARTICLE_UPDATE = "#graphql\nmutation MVQUpdateArticle($id: ID!, $article: ArticleUpdateInput!) { articleUpdate(id: $id, article: $article) { article { id title handle } userErrors { field message } } }";
const COLLECTION_QUERY = "#graphql\nquery MVQCollectionByHandle($query: String!) { collections(first: 1, query: $query) { nodes { id title handle } } }";
const COLLECTION_UPDATE = "#graphql\nmutation MVQUpdateCollection($input: CollectionInput!) { collectionUpdate(input: $input) { collection { id title handle } userErrors { field message } } }";
const PAGE_QUERY = "#graphql\nquery MVQPageByHandle($query: String!) { pages(first: 1, query: $query) { nodes { id title handle isPublished } } }";
const PAGE_CREATE = "#graphql\nmutation MVQCreatePage($page: PageCreateInput!) { pageCreate(page: $page) { page { id title handle isPublished } userErrors { field message } } }";
const PAGE_UPDATE = "#graphql\nmutation MVQUpdatePage($id: ID!, $page: PageUpdateInput!) { pageUpdate(id: $id, page: $page) { page { id title handle isPublished } userErrors { field message } } }";

const LEGAL_PAGE_HANDLES = new Set([
  "privacy-policy",
  "terms-of-service",
  "terms",
  "shipping-policy",
  "refund-policy",
  "return-policy",
]);

function esc(value: unknown): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function exactHandleQuery(handle: string): string {
  return "handle:" + handle.replace(/[^a-z0-9-]/gi, "");
}

async function body(response: Response): Promise<any> {
  return response.json() as Promise<any>;
}

function userErrorMessage(errors: Array<{ field?: string[] | null; message: string }> = []): string {
  return errors.map((error) => (error.field?.join(".") || "resource") + ": " + error.message).join("; ");
}

function renderBlogBody(blog: any): string {
  const sections = Array.isArray(blog?.sections) ? blog.sections : [];
  const links = Array.isArray(blog?.internal_links) ? blog.internal_links : [];
  const sectionHtml = sections.map((section: any) => {
    const paragraphs = (Array.isArray(section?.paragraphs) ? section.paragraphs : [])
      .map((p: unknown) => "<p>" + esc(p) + "</p>")
      .join("");
    return "<h2>" + esc(section?.heading) + "</h2>" + paragraphs;
  }).join("");

  const linkHtml = links
    .filter((item: any) => String(item?.target || "").startsWith("/"))
    .map((item: any) => '<p><a href="' + esc(item.target) + '">' + esc(item.anchor || "Explore the product") + "</a></p>")
    .join("");

  return sectionHtml + linkHtml;
}

function renderFaqBody(entries: any[]): string {
  return "<h2>Frequently Asked Questions</h2>" + entries.map((item) =>
    "<h3>" + esc(item?.question) + "</h3><p>" + esc(item?.answer) + "</p>"
  ).join("");
}

async function ensureBlog(admin: AdminGraphql, handle: string) {
  const found = await body(await admin.graphql(BLOG_QUERY, {
    variables: { query: exactHandleQuery(handle) },
  }));
  const existing = found.data?.blogs?.nodes?.[0];
  if (existing) return existing;

  if (process.env.MVQ_BLOG_CREATE_IF_MISSING === "false") {
    throw new Error("Blog " + handle + " does not exist and creation is disabled");
  }

  const created = await body(await admin.graphql(BLOG_CREATE, {
    variables: {
      blog: {
        title: process.env.MVQ_BLOG_TITLE || "MVQueen Journal",
        handle,
        commentPolicy: "CLOSED",
      },
    },
  }));
  const errors = created.data?.blogCreate?.userErrors ?? [];
  if (errors.length) throw new Error(userErrorMessage(errors));
  const result = created.data?.blogCreate?.blog;
  if (!result?.id) throw new Error("Shopify did not return the created blog");
  return result;
}

async function publishBlog(admin: AdminGraphql, record: CanonicalProductRecord): Promise<PublishResult> {
  const blog: any = (record.content_suite as any)?.blog;
  if (!blog || blog.auto_publish !== true) {
    return { surface: "blog", status: "SKIPPED", message: "Blog output is not publish-eligible" };
  }
  if (process.env.MVQ_BLOG_PUBLISH_ENABLED === "false") {
    return { surface: "blog", status: "SKIPPED", message: "Blog publishing kill switch is disabled" };
  }

  const blogHandle = process.env.MVQ_BLOG_HANDLE || "news";
  const targetBlog = await ensureBlog(admin, blogHandle);
  const articleHandle = String(blog.slug || "").trim();
  const articleTitle = String(blog.title || "").trim();
  if (!articleHandle || !articleTitle) throw new Error("Approved blog output is missing title or slug");

  const numericBlogId = targetBlog.id.split("/").pop() || targetBlog.id;
  const existing = await body(await admin.graphql(ARTICLE_QUERY, {
    variables: { query: exactHandleQuery(articleHandle) + " AND blog_id:" + numericBlogId },
  }));
  const current = existing.data?.articles?.nodes?.[0];

  const articleInput = {
    blogId: targetBlog.id,
    handle: articleHandle,
    title: articleTitle,
    body: renderBlogBody(blog),
    summary: "<p>" + esc(blog.dek || blog.meta_description || "") + "</p>",
    isPublished: true,
    author: { name: process.env.MVQ_BLOG_AUTHOR || "MVQueen" },
    tags: Array.from(new Set(["MVQueen", "Editorial", String(blog.primary_keyword || "").trim()].filter(Boolean))),
    metafields: [
      {
        namespace: "seo",
        key: "meta_description",
        type: "single_line_text_field",
        value: String(blog.meta_description || "").trim(),
      },
    ],
  };

  if (current?.id) {
    const updated = await body(await admin.graphql(ARTICLE_UPDATE, {
      variables: { id: current.id, article: { ...articleInput, redirectNewHandle: true } },
    }));
    const errors = updated.data?.articleUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(userErrorMessage(errors));
    return { surface: "blog", status: "UPDATED", resourceId: updated.data?.articleUpdate?.article?.id, message: "Updated blog article " + articleHandle };
  }

  const created = await body(await admin.graphql(ARTICLE_CREATE, { variables: { article: articleInput } }));
  const errors = created.data?.articleCreate?.userErrors ?? [];
  if (errors.length) throw new Error(userErrorMessage(errors));
  return { surface: "blog", status: "PUBLISHED", resourceId: created.data?.articleCreate?.article?.id, message: "Published blog article " + articleHandle };
}

async function publishCollection(admin: AdminGraphql, record: CanonicalProductRecord): Promise<PublishResult> {
  const collection: any = (record.content_suite as any)?.collection;
  if (!collection || collection.auto_publish !== true) {
    return { surface: "collection", status: "SKIPPED", message: "Collection copy is not publish-eligible" };
  }
  if (process.env.MVQ_COLLECTION_CONTENT_PUBLISH_ENABLED === "false") {
    return { surface: "collection", status: "SKIPPED", message: "Collection publishing kill switch is disabled" };
  }

  const slug = String(collection.slug || "").trim();
  if (!slug) return { surface: "collection", status: "SKIPPED", message: "Collection output has no target slug" };

  const found = await body(await admin.graphql(COLLECTION_QUERY, {
    variables: { query: exactHandleQuery(slug) },
  }));
  const target = found.data?.collections?.nodes?.[0];
  if (!target?.id) {
    return { surface: "collection", status: "SKIPPED", message: "No existing collection matched " + slug + "; auto-creation is disabled" };
  }

  const updated = await body(await admin.graphql(COLLECTION_UPDATE, {
    variables: {
      input: {
        id: target.id,
        descriptionHtml: "<p>" + esc(collection.description) + "</p>",
        seo: {
          title: String(collection.seo_title || "").trim(),
          description: String(collection.meta_description || "").trim(),
        },
      },
    },
  }));
  const errors = updated.data?.collectionUpdate?.userErrors ?? [];
  if (errors.length) throw new Error(userErrorMessage(errors));
  return { surface: "collection", status: "UPDATED", resourceId: updated.data?.collectionUpdate?.collection?.id, message: "Updated existing collection " + slug };
}

async function upsertPage(admin: AdminGraphql, page: any): Promise<PublishResult> {
  const handle = String(page?.handle || page?.slug || "").trim();
  const title = String(page?.title || "").trim();
  if (!handle || !title) throw new Error("Page output is missing title or handle");
  if (LEGAL_PAGE_HANDLES.has(handle)) {
    return { surface: "page", status: "SKIPPED", message: "Legal/policy page " + handle + " is protected from automation" };
  }

  const found = await body(await admin.graphql(PAGE_QUERY, {
    variables: { query: exactHandleQuery(handle) },
  }));
  const current = found.data?.pages?.nodes?.[0];
  const input = {
    title,
    handle,
    body: String(page.body_html || page.body || ""),
    isPublished: true,
  };

  if (current?.id) {
    const updated = await body(await admin.graphql(PAGE_UPDATE, {
      variables: { id: current.id, page: { ...input, redirectNewHandle: true } },
    }));
    const errors = updated.data?.pageUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(userErrorMessage(errors));
    return { surface: "page", status: "UPDATED", resourceId: updated.data?.pageUpdate?.page?.id, message: "Updated page " + handle };
  }

  const created = await body(await admin.graphql(PAGE_CREATE, { variables: { page: input } }));
  const errors = created.data?.pageCreate?.userErrors ?? [];
  if (errors.length) throw new Error(userErrorMessage(errors));
  return { surface: "page", status: "PUBLISHED", resourceId: created.data?.pageCreate?.page?.id, message: "Published page " + handle };
}

async function publishGlobalFaq(admin: AdminGraphql, record: CanonicalProductRecord): Promise<PublishResult> {
  const faq: any = (record.content_suite as any)?.site_faq;
  if (!faq || faq.auto_publish !== true || faq.scope !== "global") {
    return { surface: "global_faq", status: "SKIPPED", message: "Product FAQ stays on the product; global FAQ page is preserved" };
  }
  if (process.env.MVQ_FAQ_PAGE_PUBLISH_ENABLED === "false") {
    return { surface: "global_faq", status: "SKIPPED", message: "FAQ page publishing kill switch is disabled" };
  }

  return upsertPage(admin, {
    title: "FAQ",
    handle: process.env.MVQ_FAQ_PAGE_HANDLE || "faq",
    body_html: renderFaqBody(Array.isArray(faq.entries) ? faq.entries : []),
  });
}

async function publishStaticPage(admin: AdminGraphql, record: CanonicalProductRecord): Promise<PublishResult> {
  const page: any = (record.content_suite as any)?.site_page;
  if (!page || page.auto_publish !== true) {
    return { surface: "page", status: "SKIPPED", message: "No governed static page is publish-eligible" };
  }
  if (process.env.MVQ_STATIC_PAGE_PUBLISH_ENABLED === "false") {
    return { surface: "page", status: "SKIPPED", message: "Static page publishing kill switch is disabled" };
  }
  return upsertPage(admin, page);
}

export async function publishApprovedContentSurfaces(
  admin: AdminGraphql,
  record: CanonicalProductRecord,
  approval: ReleaseArtifact,
): Promise<PublishResult[]> {
  const suite: any = record.content_suite;
  if (!suite || suite.qa?.passed !== true || (suite.qa?.errors?.length ?? 0) > 0) {
    throw new Error("Content suite is not QA-passed");
  }
  if (record.status !== "PRODUCTION_READY" || record.qa?.passed !== true) {
    throw new Error("Canonical product record is not production-ready");
  }
  if (approval.decision !== "APPROVED_FOR_PUBLISH") {
    throw new Error("Release approval does not authorize publication");
  }

  const results: PublishResult[] = [{
    surface: "product_faq",
    status: "PUBLISHED",
    resourceId: record.identity.product_id,
    message: "Product FAQ is included in the approved product metafield payload",
  }];

  for (const publisher of [publishBlog, publishCollection, publishGlobalFaq, publishStaticPage]) {
    try {
      results.push(await publisher(admin, record));
    } catch (error) {
      results.push({
        surface: publisher.name,
        status: "SKIPPED",
        message: error instanceof Error ? error.message : String(error),
      });
    }
  }
  return results;
}
